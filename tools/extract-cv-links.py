#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estrae dal sorgente LaTeX del CV l'inventario completo dei link e il grafo delle dipendenze.

Perché esiste. L'inventario dei link del CV era prosa scritta a mano in
.claude/context/external-links.md, dichiarata come rigenerata da uno script che viveva nello
scratchpad di sessione e andava ricreato ogni volta. Un artefatto derivato che nessuno strumento
rigenera deriva, e la deriva era misurabile: conteggi sbagliati per categoria e, soprattutto, un
perimetro confuso fra i link ancora presenti in main.tex e quelli migrati sulle pagine di
E:\\projects. Questo strumento rende l'inventario e il grafo artefatti derivati e verificabili:
la fonte di verità è il sorgente, non il documento.

Contratto, identico agli altri strumenti di tools/. Legge e non scrive mai sul sorgente: main.tex
e altacv.cls sono di sola lettura per questo script, sempre. Scrive solo dentro le regioni marcate
delle due schede, lasciando intatta la prosa scritta a mano intorno. Offre una verifica non
distruttiva --check che esce con codice diverso da zero quando l'artefatto committato non
corrisponde più al sorgente, come tools/md-unwrap.py --check e tools/lint-md-commands.py.

Nota di progetto sulle regioni generate: non contengono né la data di estrazione né il commit di
riferimento. Sarebbe metadato volatile, e renderebbe --check rosso dopo qualunque commit
successivo, anche non pertinente, addestrando a ignorarlo. L'ancoraggio al commit resta compito del
frontmatter delle schede e della skill sync-context.

Uso:
    python tools/extract-cv-links.py                      # riepilogo leggibile su stdout
    python tools/extract-cv-links.py --format json        # stato ispezionabile, formato canonico
    python tools/extract-cv-links.py --format md          # tabelle dell'inventario
    python tools/extract-cv-links.py --format mermaid     # blocco del grafo
    python tools/extract-cv-links.py --write              # aggiorna le regioni delle schede
    python tools/extract-cv-links.py --check              # verifica la deriva, exit 1 se c'è
    python tools/extract-cv-links.py --projects-root PATH # secondo salto su un altro percorso
"""

import argparse
import bisect
import io
import json
import os
import re
import subprocess
import sys

BS = chr(92)  # backslash, scritto così per non moltiplicare gli escape nelle regex sotto

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DEFAULT_TEX = os.path.join(ROOT, 'main.tex')
DEFAULT_CLS = os.path.join(ROOT, 'altacv.cls')
DEFAULT_PROJECTS_ROOT = os.path.join('E:' + os.sep, 'projects')

LINKS_CARD = os.path.join(ROOT, '.claude', 'context', 'external-links.md')
DEPS_CARD = os.path.join(ROOT, '.claude', 'context', 'external-dependencies.md')

# Categorie in ordine di presentazione. La chiave è quella usata dal JSON, dal grafo e dal
# parametro -Category di scripts/check-links.ps1: cambiarla è un cambio di interfaccia.
CATEGORIES = [
    ('contatti', 'Contatti e identità'),
    ('skills', 'skills-repo'),
    ('projects', 'projects'),
    ('blog', 'blog'),
    ('proton', 'Proton Drive'),
    ('gdrive', 'Google Drive'),
    ('tinyurl', 'Redirect tinyurl'),
    ('terzi', 'Siti di terze parti'),
]
CATEGORY_LABELS = dict(CATEGORIES)
CATEGORY_ORDER = [k for k, _ in CATEGORIES]


# ----------------------------------------------------------------------------------------------
# I/O che preserva la forma del file
# ----------------------------------------------------------------------------------------------

def read_text(path):
    """Restituisce (testo con newline normalizzati a LF, newline originale, presenza di BOM)."""
    with open(path, 'rb') as fh:
        raw = fh.read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    if bom:
        raw = raw[3:]
    text = raw.decode('utf-8')
    newline = '\r\n' if '\r\n' in text else '\n'
    return text.replace('\r\n', '\n'), newline, bom


def write_text(path, text, newline, bom):
    """Riscrive il file conservando fine riga e BOM rilevati in lettura."""
    out = text.replace('\r\n', '\n')
    if newline != '\n':
        out = out.replace('\n', newline)
    data = out.encode('utf-8')
    if bom:
        data = b'\xef\xbb\xbf' + data
    with open(path, 'wb') as fh:
        fh.write(data)


# ----------------------------------------------------------------------------------------------
# Parsing LaTeX: commenti, gruppi bilanciati, chiamate di macro
# ----------------------------------------------------------------------------------------------

def strip_comments(text):
    """Neutralizza i commenti sostituendoli con spazi, conservando ogni offset di carattere.

    Conservare gli offset non è un vezzo: i numeri di riga dell'inventario si calcolano da
    quelli, e tagliare le righe li falserebbe. Un % preceduto da backslash è un carattere
    letterale, non l'inizio di un commento, quindi il ciclo salta le coppie di escape.

    Senza questo passaggio finirebbero nell'inventario come attivi i link che il documento tiene
    deliberatamente commentati: la riga Telegram, il certificato 24 CFU e la vecchia riga Thesis.
    """
    out = []
    for line in text.split('\n'):
        cut = None
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == BS:
                i += 2
                continue
            if ch == '%':
                cut = i
                break
            i += 1
        out.append(line if cut is None else line[:cut] + ' ' * (len(line) - cut))
    return '\n'.join(out)


def skip_ws(text, i):
    while i < len(text) and text[i] in ' \t\n':
        i += 1
    return i


def read_group(text, i):
    """text[i] deve essere '{'. Restituisce (contenuto, indice dopo la graffa di chiusura)."""
    if i >= len(text) or text[i] != '{':
        raise ValueError('atteso { alla posizione %d' % i)
    depth = 0
    j = i
    while j < len(text):
        ch = text[j]
        if ch == BS:
            j += 2
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j + 1
        j += 1
    raise ValueError('gruppo non bilanciato aperto alla posizione %d' % i)


def find_calls(text, name, nargs=1):
    """Itera (offset, [argomenti]) per ogni \\name con nargs argomenti obbligatori.

    Il lookahead negativo su [A-Za-z] evita che \\github catturi anche \\githubCorp: i due campi
    info convivono nell'header del CV e confonderli produrrebbe un URL con il prefisso sbagliato.
    """
    pattern = re.compile(re.escape(BS + name) + r'(?![A-Za-z])')
    for match in pattern.finditer(text):
        j = match.end()
        args = []
        try:
            for _ in range(nargs):
                j = skip_ws(text, j)
                content, j = read_group(text, j)
                args.append(content)
        except ValueError:
            continue
        yield match.start(), args


def line_index(text):
    """Offset di inizio di ogni riga, per tradurre un offset in numero di riga."""
    starts = [0]
    for i, ch in enumerate(text):
        if ch == '\n':
            starts.append(i + 1)
    return starts


def line_of(starts, offset):
    return bisect.bisect_right(starts, offset)


def rel(path, start=None):
    """Percorso relativo alla radice del progetto, con ricaduta sul percorso assoluto.

    Su Windows os.path.relpath solleva ValueError quando i due percorsi stanno su unità diverse:
    succede appena si passa --tex o --projects-root su un altro disco, ed è esattamente il caso
    del test di deriva, che lavora su una copia nello scratchpad di sessione sotto C:. Un percorso
    assoluto nel report è informazione buona; un'eccezione non lo è.
    """
    try:
        return os.path.relpath(path, ROOT if start is None else start).replace(os.sep, '/')
    except ValueError:
        return path.replace(os.sep, '/')


def unescape_latex(url):
    """Riporta una URL dalla forma scritta nel .tex alla forma reale.

    Serve soprattutto ai tre link Proton Drive: contengono un frammento hash che in LaTeX va
    scappato come \\#, quindi la stringa nel sorgente non è la URL che un browser apre.
    """
    for esc, real in (('#', '#'), ('%', '%'), ('&', '&'), ('_', '_'), ('~', '~'), ('$', '$')):
        url = url.replace(BS + esc, real)
    return url.strip()


def parse_info_fields(text):
    """Restituisce {nome campo: prefisso URL} da ogni \\NewInfoField dichiarata nel testo.

    I prefissi non si presumono: \\linkedin, \\github e \\phone li dichiara altacv.cls, mentre
    \\blog, \\projectsSite e \\githubCorp li dichiara main.tex. Leggerli invece di scriverli qui
    è ciò che impedisce a un inventario di restare plausibile mentre è sbagliato.
    """
    fields = {}
    pattern = re.compile(re.escape(BS + 'NewInfoField') + r'\*?')
    for match in pattern.finditer(text):
        j = match.end()
        try:
            name, j = read_group(text, skip_ws(text, j))
            _icon, j = read_group(text, skip_ws(text, j))
        except ValueError:
            # Cattura anche la \NewDocumentCommand che *definisce* \NewInfoField in altacv.cls:
            # là dopo il nome non c'è un gruppo, quindi la voce si scarta da sé.
            continue
        k = skip_ws(text, j)
        prefix = ''
        if k < len(text) and text[k] == '[':
            end = text.find(']', k)
            if end != -1:
                prefix = text[k + 1:end]
        fields[name.strip()] = prefix
    return fields


def parse_blog_templates(text):
    """Estrae i due template URL delle topic page del blog dalle definizioni in main.tex.

    Si leggono dal corpo di \\newcommand{\\bloglinkwrap} invece di essere scritti qui, così un
    cambio di template non produce un inventario silenziosamente sbagliato. Il template italiano
    è quello che consuma il primo parametro (#1), l'inglese il secondo (#2); lo spagnolo ricade
    sull'inglese perché il blog non ha una terza lingua.
    """
    templates = {}
    for macro in ('bloglinkwrap', 'bloglink'):
        pattern = re.compile(re.escape(BS + 'newcommand') + r'\s*\{\s*' + re.escape(BS + macro) + r'\s*\}')
        for match in pattern.finditer(text):
            j = skip_ws(text, match.end())
            if j < len(text) and text[j] == '[':
                j = text.find(']', j) + 1
                j = skip_ws(text, j)
            try:
                body, _ = read_group(text, j)
            except ValueError:
                continue
            for _off, args in find_calls(body, 'href', 1):
                url = args[0]
                if re.search(r'(?<!' + re.escape(BS) + r')#1', url):
                    templates.setdefault('it', url)
                elif re.search(r'(?<!' + re.escape(BS) + r')#2', url):
                    templates.setdefault('en', url)
    if 'it' not in templates or 'en' not in templates:
        raise SystemExit('[extract-cv-links] Template del blog non trovati in main.tex: '
                         'le definizioni di \\bloglink/\\bloglinkwrap sono cambiate, '
                         'lo strumento va aggiornato invece di indovinare.')
    return templates


def parse_sections(text, starts):
    """Elenco (offset, etichetta) di ogni \\cvsection, per dire dove sta un link nel CV.

    L'etichetta è la variante italiana del \\cvtext contenuto nel titolo, quando c'è: i
    documenti del progetto sono in italiano e il titolo tradotto è la forma leggibile.
    """
    sections = []
    for offset, args in find_calls(text, 'cvsection', 1):
        label = None
        for _o, targs in find_calls(args[0], 'cvtext', 3):
            label = targs[0].strip()
            break
        if not label:
            label = re.sub(re.escape(BS) + r'[A-Za-z]+', ' ', args[0])
            label = re.sub(r'[{}]', '', label)
            label = re.sub(r'\s+', ' ', label).strip()
        sections.append((offset, label, line_of(starts, offset)))
    return sections


def section_for(sections, offset):
    label = 'Header'
    for soff, slabel, _line in sections:
        if soff <= offset:
            label = slabel
        else:
            break
    return label


def classify(url):
    if url.startswith('mailto:') or url.startswith('tel:'):
        return 'contatti'
    host = re.sub(r'^[a-z]+://', '', url).split('/')[0].lower()
    if host.startswith('www.'):
        host = host[4:]
    if host in ('linkedin.com', 'github.com'):
        return 'contatti'
    if host == 'alesop95.github.io':
        path = url.split('alesop95.github.io', 1)[1]
        if path.startswith('/skills'):
            return 'skills'
        if path.startswith('/projects'):
            return 'projects'
        if path.startswith('/blog'):
            return 'blog'
    if host == 'drive.proton.me':
        return 'proton'
    if host == 'drive.google.com':
        return 'gdrive'
    if host == 'tinyurl.com':
        return 'tinyurl'
    return 'terzi'


# ----------------------------------------------------------------------------------------------
# Estrazione dal CV
# ----------------------------------------------------------------------------------------------

def extract_cv(tex_path, cls_path):
    raw_tex, _nl, _bom = read_text(tex_path)
    text = strip_comments(raw_tex)
    starts = line_index(text)
    sections = parse_sections(text, starts)

    fields = {}
    if os.path.exists(cls_path):
        cls_raw, _n, _b = read_text(cls_path)
        fields.update(parse_info_fields(strip_comments(cls_raw)))
    fields.update(parse_info_fields(text))

    templates = parse_blog_templates(text)
    param_re = re.compile(r'(?<!' + re.escape(BS) + r')#[0-9]')

    targets = {}

    def add(url, offset, kind, variants=None, note=None):
        url = unescape_latex(url)
        if not url:
            return
        entry = targets.setdefault(url, {
            'url': url,
            'category': classify(url),
            'kind': kind,
            'lines': [],
            'sections': [],
            'variants': variants or {},
            'note': note,
        })
        line = line_of(starts, offset)
        if line not in entry['lines']:
            entry['lines'].append(line)
        sect = section_for(sections, offset)
        if sect not in entry['sections']:
            entry['sections'].append(sect)
        if variants:
            entry['variants'].update(variants)
        if note and not entry['note']:
            entry['note'] = note

    # 1. \href letterali. I due template del blog si riconoscono dai parametri #1/#2 e si
    #    escludono: non sono URL ma stampi, e le loro istanze arrivano dal passo 3.
    for offset, args in find_calls(text, 'href', 1):
        url = args[0]
        if param_re.search(url):
            continue
        add(url, offset, 'href')

    # 2. URL costruite dai campi info dell'header (\linkedin, \github, \githubCorp, \blog,
    #    \projectsSite, \phone): il prefisso viene dalla dichiarazione, il valore dalla chiamata.
    for name, prefix in sorted(fields.items(), key=lambda kv: -len(kv[0])):
        if not prefix:
            continue
        for offset, args in find_calls(text, name, 1):
            value = args[0].strip()
            if not value:
                continue
            add(prefix + value, offset, 'infofield:' + name)

    # 3. Topic page del blog: 13 chiamate, due URL ciascuna (italiano e inglese/spagnolo).
    #    Il bersaglio è l'argomento, non la lingua: l'inventario conta 13 bersagli e 26 stringhe.
    for macro, nargs in (('bloglinkwrap', 3), ('bloglink', 2)):
        for offset, args in find_calls(text, macro, nargs):
            tag_it, tag_en = args[0].strip(), args[1].strip()
            url_it = templates['it'].replace('#1', tag_it)
            url_en = templates['en'].replace('#2', tag_en)
            add(url_it, offset, 'blogtag', variants={'it': url_it, 'en': url_en},
                note='tag `%s` / `%s`' % (tag_it, tag_en))

    ordered = sorted(targets.values(),
                     key=lambda e: (CATEGORY_ORDER.index(e['category']), e['url']))
    url_strings = 0
    for entry in ordered:
        url_strings += 2 if entry['variants'] else 1

    counts = {key: 0 for key in CATEGORY_ORDER}
    for entry in ordered:
        counts[entry['category']] += 1

    return {
        'targets': ordered,
        'counts_by_category': counts,
        'targets_total': len(ordered),
        'url_strings_total': url_strings,
        'blog_templates': templates,
        'info_field_prefixes': {k: v for k, v in sorted(fields.items()) if v},
    }


# ----------------------------------------------------------------------------------------------
# Secondo salto: le pagine di E:\projects a cui il CV delega
# ----------------------------------------------------------------------------------------------

MD_LINK_RE = re.compile(r'\]\((https?://[^)\s]+)\)|<(https?://[^>\s]+)>')

# Le sole pagine che il CV raggiunge davvero. Una sezione porta con sé le proprie pagine di
# dettaglio (sono i "Dettagli" a cui il rimando del CV punta); una pagina singola porta solo le
# proprie varianti di lingua.
SECOND_HOP_MAP = [
    ('/projects', ('docs', None), ('index',)),
    ('/projects/company/', ('docs', 'company'), None),
    ('/projects/personal/', ('docs', 'personal'), None),
    ('/projects/academic/', ('docs', 'academic'), None),
    ('/projects/courses/', ('docs', 'courses'), None),
    ('/projects/company/network-infrastructure-documentation/',
     ('docs', 'company'), ('network-infrastructure-documentation',)),
    ('/projects/personal/harmony-book/', ('docs', 'personal'), ('harmony-book',)),
]


def resolve_second_hop_files(projects_root, cv_projects_paths):
    """Mappa i rimandi del CV sui file Markdown locali del repo projects.

    Le due pagine di dettaglio linkate direttamente dal CV (network-infrastructure-documentation
    e harmony-book) vivono dentro sezioni che il CV linka anche per intero: la loro riga è quindi
    un sottoinsieme di quella della sezione, marcato con "subset" perché sommare le colonne
    conterebbe due volte gli stessi file. La deduplicazione per URL fa sì che i totali dei
    bersagli restino comunque corretti.
    """
    pages = []
    seen_dirs = set()
    for cv_path, (docs, section), stems in SECOND_HOP_MAP:
        if cv_path not in cv_projects_paths:
            continue
        directory = os.path.join(projects_root, docs) if section is None \
            else os.path.join(projects_root, docs, section)
        if not os.path.isdir(directory):
            continue
        files = []
        for name in sorted(os.listdir(directory)):
            if not name.endswith('.md') or name.startswith('_'):
                continue
            stem = name.split('.')[0]
            if stems is not None and stem not in stems:
                continue
            files.append(os.path.join(directory, name))
        relpath = rel(directory, projects_root)
        label = relpath if stems is None else relpath + '/' + stems[0]
        pages.append({'cv_path': cv_path, 'dir': directory, 'label': label,
                      'subset': directory in seen_dirs, 'files': files})
        seen_dirs.add(directory)
    return pages


def extract_second_hop(projects_root, cv_targets):
    """Link esterni portati dalle pagine di dettaglio, con i repository GitHub aggregati.

    I 90 link a github.com sotto /personal/ sono generati da scripts/update_personal_projects.py:
    nel grafo valgono un nodo aggregato, non 90 archi, perché non sono manutenzione manuale del
    CV e nasconderebbero il segnale utile, che sono gli asset Google Drive ancora da migrare.
    """
    if not projects_root or not os.path.isdir(projects_root):
        return {'available': False, 'root': projects_root, 'pages': [], 'assets': [],
                'github_aggregate': 0, 'github_occurrences': 0, 'counts_by_host': {}}

    cv_projects_paths = set()
    for entry in cv_targets:
        if entry['category'] != 'projects':
            continue
        cv_projects_paths.add(entry['url'].split('alesop95.github.io', 1)[1])

    pages = resolve_second_hop_files(projects_root, cv_projects_paths)

    assets = {}
    github_urls = set()
    github_occurrences = 0
    page_reports = []
    for page in pages:
        found = 0
        for path in page['files']:
            text, _n, _b = read_text(path)
            relpath = rel(path, projects_root)
            for match in MD_LINK_RE.finditer(text):
                url = match.group(1) or match.group(2)
                found += 1
                host = re.sub(r'^https?://(www\.)?', '', url).split('/')[0].lower()
                if host == 'github.com':
                    github_urls.add(url)
                    if not page['subset']:
                        github_occurrences += 1
                    continue
                entry = assets.setdefault(url, {'url': url, 'host': host, 'files': []})
                if relpath not in entry['files']:
                    entry['files'].append(relpath)
        page_reports.append({
            'cv_path': page['cv_path'],
            'dir': page['label'],
            'subset': page['subset'],
            'files': len(page['files']),
            'links': found,
        })

    counts_by_host = {}
    for entry in assets.values():
        counts_by_host[entry['host']] = counts_by_host.get(entry['host'], 0) + 1

    return {
        'available': True,
        'root': projects_root,
        'pages': page_reports,
        'assets': sorted(assets.values(), key=lambda e: (e['host'], e['url'])),
        'github_aggregate': len(github_urls),
        'github_occurrences': github_occurrences,
        'counts_by_host': counts_by_host,
    }


# ----------------------------------------------------------------------------------------------
# Uscite
# ----------------------------------------------------------------------------------------------

def short_url(url, width=78):
    return url if len(url) <= width else url[:width - 3] + '...'


def render_md(state):
    cv = state['cv']
    hop = state['second_hop']
    out = []

    out.append('### Riepilogo per categoria')
    out.append('')
    out.append('| Categoria | Bersagli | Stringhe URL |')
    out.append('|---|---|---|')
    for key in CATEGORY_ORDER:
        n = cv['counts_by_category'][key]
        strings = sum(2 if e['variants'] else 1
                      for e in cv['targets'] if e['category'] == key)
        out.append('| %s | %d | %d |' % (CATEGORY_LABELS[key], n, strings))
    out.append('| **Totale** | **%d** | **%d** |'
               % (cv['targets_total'], cv['url_strings_total']))
    out.append('')

    for key in CATEGORY_ORDER:
        entries = [e for e in cv['targets'] if e['category'] == key]
        if not entries:
            continue
        out.append('### %s (%d)' % (CATEGORY_LABELS[key], len(entries)))
        out.append('')
        out.append('| URL | Riga | Sezione del CV | Nota |')
        out.append('|---|---|---|---|')
        for e in entries:
            url = e['url']
            if e['variants']:
                url = e['variants'].get('it', url)
            lines = ', '.join(str(n) for n in e['lines'])
            sects = ', '.join(e['sections'])
            note = e['note'] or ''
            if e['variants'] and e['variants'].get('en'):
                note = (note + ' - EN/ES: `%s`' % e['variants']['en']).strip(' -')
            out.append('| `%s` | %s | %s | %s |' % (url, lines, sects, note))
        out.append('')

    out.append('### Secondo salto: pagine di dettaglio in `projects`')
    out.append('')
    if not hop['available']:
        out.append('Repo `projects` non disponibile a `%s`: secondo salto non estratto.'
                   % hop['root'])
        out.append('')
    else:
        out.append('| Rimando dal CV | Cartella o pagina | File | Link esterni | |')
        out.append('|---|---|---|---|---|')
        for p in hop['pages']:
            out.append('| `%s` | `%s` | %d | %d | %s |'
                       % (p['cv_path'], p['dir'], p['files'], p['links'],
                          'sottoinsieme della riga di sezione' if p['subset'] else ''))
        out.append('')
        out.append('Le due righe marcate come sottoinsieme sono pagine di dettaglio che il CV linka direttamente ma che stanno dentro una sezione linkata per intero: le loro colonne non si sommano alle altre, mentre i bersagli restano corretti perché deduplicati per URL.')
        out.append('')
        out.append('I %d repository `github.com` distinti (%d occorrenze nelle pagine `/personal/`, moltiplicate dalle varianti di lingua) sono generati da `scripts/update_personal_projects.py` e valgono un solo nodo aggregato: non sono manutenzione manuale del CV.'
                   % (hop['github_aggregate'], hop['github_occurrences']))
        out.append('')
        out.append('| Host | Bersagli |')
        out.append('|---|---|')
        for host, n in sorted(hop['counts_by_host'].items(), key=lambda kv: (-kv[1], kv[0])):
            out.append('| `%s` | %d |' % (host, n))
        out.append('| `github.com` (aggregato) | %d |' % hop['github_aggregate'])
        out.append('')
        out.append('| Bersaglio | Host | Pagine che lo citano |')
        out.append('|---|---|---|')
        for a in hop['assets']:
            out.append('| `%s` | `%s` | %s |'
                       % (short_url(a['url']), a['host'], ', '.join('`%s`' % f for f in a['files'])))
        out.append('')

    return '\n'.join(out).rstrip('\n')


# Redirect tinyurl la cui destinazione è un documento di archivio, non un sito: sono i due
# elaborati di tesi, e si migrano aggiornando il target del redirect invece di main.tex. La
# destinazione reale la conferma scripts/check-links.ps1, che segue i reindirizzamenti.
THESIS_REDIRECTS = ('Tesi-magistrale', 'Tesi-trienn')


def render_mermaid(state):
    cv = state['cv']
    hop = state['second_hop']
    c = cv['counts_by_category']

    gdrive_hop = hop['counts_by_host'].get('drive.google.com', 0)
    youtube_hop = hop['counts_by_host'].get('youtube.com', 0)

    blog_tags = sum(1 for e in cv['targets'] if e['category'] == 'blog' and e['variants'])
    blog_other = c['blog'] - blog_tags
    thesis = sum(1 for e in cv['targets'] if e['category'] == 'tinyurl'
                 and any(t in e['url'] for t in THESIS_REDIRECTS))
    terzi_hosts = sorted({re.sub(r'^https?://(www\.)?', '', e['url']).split('/')[0]
                          for e in cv['targets'] if e['category'] == 'terzi'})
    gdrive_total = c['gdrive'] + gdrive_hop + thesis

    lines = []
    lines.append('```mermaid')
    lines.append('flowchart LR')
    lines.append('    CV["main.tex (EN/IT/ES)<br/>%d bersagli, %d URL"]'
                 % (cv['targets_total'], cv['url_strings_total']))
    lines.append('')
    lines.append('    CV -->|"%d link<br/>check-links -Category skills"| SKILLS["skills-repo<br/>E:\\skills"]'
                 % c['skills'])
    lines.append('    CV -->|"%d pagine<br/>check-links -Category projects"| PROJECTS["projects<br/>E:\\projects"]'
                 % c['projects'])
    lines.append('    CV -->|"%d tag x 2 lingue + %d home<br/>check-links -Category blog"| BLOG["blog<br/>E:\\blog-alessio"]'
                 % (blog_tags, blog_other))
    lines.append('    CV -->|"%d contatti"| ID["Identità<br/>mail, tel, LinkedIn, GitHub x2"]'
                 % c['contatti'])
    lines.append('    CV -->|"%d file migrati"| PROTON["Proton Drive<br/>destinazione"]' % c['proton'])
    lines.append('    CV -->|"%d cartelle da migrare"| GDRIVE_CV["Google Drive<br/>residuo in main.tex"]'
                 % c['gdrive'])
    lines.append('    CV -->|"%d redirect<br/>destinazione da seguire"| TINYURL["tinyurl.com"]'
                 % c['tinyurl'])
    lines.append('    CV -.->|"%d siti"| TERZI["Terze parti<br/>%s"]'
                 % (c['terzi'], ', '.join(terzi_hosts)))
    lines.append('')
    lines.append('    GDRIVE_CV -.->|"da migrare, lavoro di questo repo"| PROTON')
    lines.append('')

    if hop['available']:
        lines.append('    subgraph HOP["Secondo salto: pagine di dettaglio in E:\\projects\\docs"]')
        for p in hop['pages']:
            node = 'P_' + (re.sub(r'[^a-z]', '', p['cv_path'].replace('/projects', '')) or 'home')
            lines.append('    %s["%s<br/>%d file, %d link"]'
                         % (node, p['dir'], p['files'], p['links']))
        lines.append('    end')
        lines.append('    PROJECTS --> HOP')
        lines.append('    HOP -->|"%d repo distinti, generati da<br/>update_personal_projects.py"| GH["github.com<br/>nodo aggregato"]'
                     % hop['github_aggregate'])
        lines.append('    HOP -.->|"%d file"| GDRIVE_HOP["Google Drive<br/>nelle pagine projects"]'
                     % gdrive_hop)
        if youtube_hop:
            lines.append('    HOP -.->|"%d video"| YT["YouTube"]' % youtube_hop)
    else:
        lines.append('    GDRIVE_HOP["Google Drive<br/>nelle pagine projects<br/>(non estratto)"]')

    lines.append('    TINYURL -.->|"%d target di tesi<br/>ancora su Drive"| GDRIVE_HOP' % thesis)
    lines.append('    GDRIVE_HOP -.->|"da migrare, lavoro del repo projects"| PROTON')
    lines.append('')
    lines.append('    SKILLS -->|"/technical/*"| SKILLS_TECH["Capability tecniche"]')
    lines.append('    SKILLS -->|"/soft/"| SKILLS_SOFT["Soft skills"]')
    lines.append('```')
    lines.append('')
    lines.append('Gli asset di archivio nel perimetro raggiungibile sono %d: %d già migrati su Proton Drive e %d ancora su Google Drive, cioè %d citati direttamente da `main.tex`, %d nelle pagine di `projects` e %d dietro i redirect di tesi. I tre insiemi sono disgiunti e si migrano in modi diversi: sostituzione nel sorgente, lavoro del repo `projects`, riconfigurazione del solo target del redirect.'
                 % (c['proton'] + gdrive_total, c['proton'], gdrive_total,
                    c['gdrive'], gdrive_hop, thesis))
    return '\n'.join(lines)


def render_urls(state):
    """Proiezione tabellare per i checker: categoria, lingua, URL, separati da tabulazione.

    Esiste perché scripts/check-links.sh e .ps1 debbano consumare la stessa fonte del grafo e
    dell'inventario senza interpretare JSON in shell, così che una sola definizione di "link del
    CV" valga per tutti e tre. La colonna della lingua vale "-" per i bersagli senza varianti.
    """
    rows = []
    for entry in state['cv']['targets']:
        if entry['variants']:
            for lang in ('it', 'en'):
                url = entry['variants'].get(lang)
                if url:
                    rows.append('%s\t%s\t%s' % (entry['category'], lang, url))
        else:
            rows.append('%s\t-\t%s' % (entry['category'], entry['url']))
    return '\n'.join(rows)


def render_summary(state):
    cv = state['cv']
    hop = state['second_hop']
    out = ['[extract-cv-links] %d bersagli unici, %d stringhe URL.'
           % (cv['targets_total'], cv['url_strings_total'])]
    for key in CATEGORY_ORDER:
        out.append('  %-24s %3d' % (CATEGORY_LABELS[key], cv['counts_by_category'][key]))
    if hop['available']:
        files = sum(p['files'] for p in hop['pages'] if not p['subset'])
        out.append('  secondo salto            %3d bersagli non-GitHub in %d pagine, %d repo GitHub aggregati'
                   % (len(hop['assets']), files, hop['github_aggregate']))
    else:
        out.append('  secondo salto            non disponibile (%s)' % hop['root'])
    return '\n'.join(out)


# ----------------------------------------------------------------------------------------------
# Regioni generate nelle schede
# ----------------------------------------------------------------------------------------------

def markers(name):
    return ('<!-- BEGIN GENERATED cv-links: %s -->' % name,
            '<!-- END GENERATED cv-links: %s -->' % name)


def replace_region(text, name, body):
    begin, end = markers(name)
    i = text.find(begin)
    j = text.find(end)
    if i < 0 or j < 0 or j < i:
        raise SystemExit('[extract-cv-links] Regione "%s" assente o malformata: '
                         'i marcatori vanno inseriti a mano una volta.' % name)
    return text[:i] + begin + '\n\n' + body.rstrip('\n') + '\n\n' + text[j:]


def region_body(text, name):
    begin, end = markers(name)
    i = text.find(begin)
    j = text.find(end)
    if i < 0 or j < 0 or j < i:
        return None
    return text[i + len(begin):j].strip('\n')


REGIONS = [
    (LINKS_CARD, 'inventario', render_md),
    (DEPS_CARD, 'grafo', render_mermaid),
]


def apply_regions(state, write):
    drift = []
    for path, name, renderer in REGIONS:
        if not os.path.exists(path):
            drift.append((path, name, 'scheda assente'))
            continue
        text, newline, bom = read_text(path)
        body = renderer(state)
        current = region_body(text, name)
        if current is None:
            drift.append((path, name, 'marcatori assenti'))
            continue
        if current.strip('\n') == body.strip('\n'):
            continue
        drift.append((path, name, 'contenuto non allineato al sorgente'))
        if write:
            write_text(path, replace_region(text, name, body), newline, bom)
    return drift


# ----------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------

def git_commit():
    try:
        out = subprocess.run(['git', '-C', ROOT, 'rev-parse', '--short', 'HEAD'],
                             capture_output=True, timeout=15)
        return out.stdout.decode('utf-8', 'replace').strip() or None
    except Exception:
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Estrae inventario e grafo dei link del CV dal sorgente LaTeX.')
    parser.add_argument('--tex', default=DEFAULT_TEX, help='sorgente principale (default main.tex)')
    parser.add_argument('--cls', default=DEFAULT_CLS, help='classe altaCV, per i prefissi dei campi info')
    parser.add_argument('--projects-root', default=DEFAULT_PROJECTS_ROOT,
                        help='radice del repo projects per il secondo salto; ignorata se assente')
    parser.add_argument('--format', choices=('summary', 'json', 'md', 'mermaid', 'urls'),
                        default='summary')
    parser.add_argument('--write', action='store_true',
                        help='aggiorna le regioni generate delle due schede')
    parser.add_argument('--check', action='store_true',
                        help='verifica la deriva fra schede e sorgente, exit 1 se presente')
    args = parser.parse_args(argv)

    if not os.path.exists(args.tex):
        raise SystemExit('[extract-cv-links] Sorgente non trovato: %s' % args.tex)

    cv = extract_cv(args.tex, args.cls)
    hop = extract_second_hop(args.projects_root, cv['targets'])
    state = {
        'source': {
            'tex': rel(args.tex),
            'cls': rel(args.cls),
            'projects_root': args.projects_root,
            'commit': git_commit(),
        },
        'cv': cv,
        'second_hop': hop,
    }

    if args.check:
        drift = apply_regions(state, write=False)
        if drift:
            print('[extract-cv-links] Deriva rilevata fra sorgente e schede:')
            for path, name, why in drift:
                print('  %s (regione "%s"): %s'
                      % (rel(path), name, why))
            print('[extract-cv-links] Rigenerare con: python tools/extract-cv-links.py --write')
            return 1
        print('[extract-cv-links] Schede allineate al sorgente.')
        return 0

    if args.write:
        drift = apply_regions(state, write=True)
        if drift:
            for path, name, why in drift:
                print('[extract-cv-links] aggiornata %s (regione "%s"): %s'
                      % (rel(path), name, why))
        else:
            print('[extract-cv-links] Nessuna modifica: le schede erano già allineate.')
        return 0

    if args.format == 'json':
        print(json.dumps(state, indent=2, ensure_ascii=False, sort_keys=False))
    elif args.format == 'md':
        print(render_md(state))
    elif args.format == 'mermaid':
        print(render_mermaid(state))
    elif args.format == 'urls':
        print(render_urls(state))
    else:
        print(render_summary(state))
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    else:  # pragma: no cover
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.exit(main())
