#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigenera la roadmap operativa fondendo le voci aperte con lo stato misurato dal vivo.

Perché esiste. La domanda "che cosa resta da fare, in ogni punto del progetto e su ogni link" non
aveva una risposta unica: `roadmap.md` porta la cronaca narrativa delle sette fasi, `index.md` un
punto di ripresa, la mappa dello stato una tabella parziale, e tutti e tre sono scritti a mano,
quindi invecchiano. È lo stesso difetto che ADR-008 ha risolto per l'inventario dei link e che
`extract-ecosystem.py` ha risolto per il grafo di architettura, e la risposta qui è la stessa:
separare ciò che una macchina non può dedurre da ciò che deve misurare a ogni esecuzione.

Divisione di responsabilità. `tools/roadmap-items.yml` contiene il solo giudizio umano, cioè quale
lavoro resta, dove vive, perché e a che costo; questo strumento non lo modifica mai. Lo stato
misurabile, cioè il commit di riferimento, la distanza delle schede da HEAD, la deriva dei due
artefatti generati, la convenzione Markdown e la raggiungibilità dei link, non compare in quel file
e viene rilevato qui a ogni invocazione. Una voce che porta una sonda si chiude da sola quando la
misura dice che il difetto non c'è più, così la lista non può dichiarare aperto un difetto già
corretto, che è esattamente l'errore trovato il 2026-09-22 su "Hold Me Tight".

Perché non scrive in una scheda tracciata. La roadmap è un derivato, come i PDF e come i log di
compilazione, quindi vive in `build/` che è ignorato da git. Le schede di `.claude/context/`
restano la fonte narrativa e si aggiornano a mano, per la regola di team che vieta all'agente di
scrivervi senza richiesta esplicita.

Uso:
    python tools/roadmap.py                       # riepilogo a schermo
    python tools/roadmap.py --format md           # Markdown su stdout
    python tools/roadmap.py --format html --write # pagina pronta da stampare in build/
    python tools/roadmap.py --link-check          # aggiunge la verifica HTTP dei link (lenta)
    python tools/roadmap.py --check               # exit 1 se resta una voce di livello 0
"""

import argparse
import datetime as _dt
import html as _html
import io
import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS = os.path.join(ROOT, 'tools', 'roadmap-items.yml')
BUILD = os.path.join(ROOT, 'build')


# --------------------------------------------------------------------------- misure


def run(args, timeout=600):
    """Esegue un comando nella radice del progetto e restituisce (exit, stdout+stderr)."""
    try:
        p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=timeout)
        return p.returncode, (p.stdout or '') + (p.stderr or '')
    except (OSError, subprocess.SubprocessError) as exc:
        return None, str(exc)


def git(*args):
    code, out = run(['git'] + list(args), timeout=60)
    return out.strip() if code == 0 else ''


def measure_git():
    head = git('rev-parse', '--short', 'HEAD')
    return {
        'head': head,
        'head_long': git('rev-parse', 'HEAD'),
        'branch': git('branch', '--show-current'),
        'data_commit': git('log', '-1', '--format=%ad', '--date=short'),
        'oggetto': git('log', '-1', '--format=%s'),
        'pulito': git('status', '--porcelain') == '',
        'modificati': [l[3:] for l in git('status', '--porcelain').splitlines() if l],
    }


FRONTMATTER = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.S)


def measure_schede(head_long):
    """Distanza di ogni scheda di contesto da HEAD, letta dal frontmatter di riconciliazione."""
    cartella = os.path.join(ROOT, '.claude', 'context')
    schede = []
    if not os.path.isdir(cartella):
        return schede
    for nome in sorted(os.listdir(cartella)):
        if not nome.endswith('.md'):
            continue
        with io.open(os.path.join(cartella, nome), encoding='utf-8') as fh:
            testo = fh.read()
        m = FRONTMATTER.match(testo)
        verificato = ''
        if m:
            try:
                fm = yaml.safe_load(m.group(1)) or {}
                verificato = str(fm.get('last-verified-commit', '') or '')
            except yaml.YAMLError:
                verificato = ''
        distanza = ''
        if verificato:
            conteggio = git('rev-list', '--count', verificato + '..' + head_long)
            distanza = conteggio if conteggio else '?'
        schede.append({'scheda': nome, 'verificato': verificato, 'distanza': distanza})
    return schede


def measure_controlli():
    """I tre controlli documentali che l'hook di apertura esegue, più il loro esito leggibile."""
    esiti = []

    code, out = run([sys.executable, 'tools/extract-ecosystem.py', '--check'])
    esiti.append({'nome': 'grafo di architettura', 'chiave': 'ecosystem', 'exit': code,
                  'ok': code == 0, 'dettaglio': _prima_riga(out),
                  'rimedio': 'python tools/extract-ecosystem.py --write'})

    code, out = run([sys.executable, 'tools/extract-cv-links.py', '--check'])
    esiti.append({'nome': 'inventario dei link', 'chiave': 'cvlinks', 'exit': code,
                  'ok': code == 0, 'dettaglio': _prima_riga(out),
                  'rimedio': 'python tools/extract-cv-links.py --write'})

    code, out = run([sys.executable, 'tools/md-unwrap.py', '--check', '.'])
    sporchi = re.findall(r'cambierebbe\s+(.+?)\s+\(', out)
    tracciati = _solo_tracciati(sporchi)
    esiti.append({'nome': 'convenzione Markdown', 'chiave': 'mdunwrap', 'exit': code,
                  'ok': not tracciati, 'dettaglio': _riassunto_md(sporchi, tracciati),
                  'rimedio': 'python tools/md-unwrap.py <file>'})
    return esiti


def _prima_riga(out):
    for riga in (out or '').splitlines():
        riga = riga.strip()
        if riga:
            return re.sub(r'^\[[^\]]+\]\s*', '', riga)
    return ''


def _solo_tracciati(percorsi):
    if not percorsi:
        return []
    tracciati = set(git('ls-files').splitlines())
    fuori = []
    for p in percorsi:
        normalizzato = p.replace('\\', '/').lstrip('./')
        if normalizzato in tracciati:
            fuori.append(normalizzato)
    return fuori


def _riassunto_md(sporchi, tracciati):
    if not sporchi:
        return 'nessun file da normalizzare'
    if not tracciati:
        return '%d file da normalizzare, tutti ignorati da git' % len(sporchi)
    return '%d file tracciati da normalizzare: %s' % (len(tracciati), ', '.join(tracciati))


RIGA_LINK = re.compile(r'^\s*(OK|FAIL|WARN|SKIP|FORMA)\s+(\S+)?\s*(https?://\S+|mailto:\S+|tel:.*)?')


def measure_link(attivo):
    """Verifica HTTP di tutti i link del CV, delegata allo script che il progetto già ha."""
    if not attivo:
        return None
    code, out = run(['bash', 'scripts/check-links.sh'], timeout=900)
    if code is None:
        return {'eseguito': False, 'nota': 'check-links non eseguibile: ' + out.strip()[:200]}
    categorie = []
    corrente = None
    conteggi = {'ok': 0, 'fail': 0, 'warn': 0, 'skip': 0, 'forma': 0}
    rossi = []
    for riga in out.splitlines():
        intestazione = re.match(r'^([A-Za-z].*?)\s+\((\d+)\)\s*$', riga)
        if intestazione:
            corrente = {'nome': intestazione.group(1), 'quanti': int(intestazione.group(2)),
                        'ok': 0, 'fail': 0, 'warn': 0, 'skip': 0, 'forma': 0}
            categorie.append(corrente)
            continue
        m = RIGA_LINK.match(riga)
        if not m or corrente is None:
            continue
        esito = m.group(1).lower()
        chiave = 'forma' if esito == 'forma' else esito
        if chiave in conteggi:
            conteggi[chiave] += 1
            corrente[chiave] += 1
        if esito in ('fail', 'warn'):
            rossi.append(riga.strip())
    return {'eseguito': True, 'exit': code, 'categorie': categorie,
            'conteggi': conteggi, 'rossi': rossi}


# --------------------------------------------------------------------------- sonde


def sonda_aperta(sonda, controlli):
    """Vero se la voce è ancora aperta, falso se la misura dice che il difetto non c'è più."""
    if not sonda:
        return True, 'nessuna sonda, si chiude a mano'
    for c in controlli:
        if c['chiave'] == sonda:
            return (not c['ok']), c['dettaglio']
    for prefisso, atteso in (('presente:', True), ('assente:', False)):
        if sonda.startswith(prefisso):
            resto = sonda[len(prefisso):]
            percorso, _, regex = resto.partition(':')
            assoluto = os.path.join(ROOT, percorso.replace('/', os.sep))
            if not os.path.exists(assoluto):
                return True, 'file non trovato: ' + percorso
            with io.open(assoluto, encoding='utf-8', errors='replace') as fh:
                trovato = re.search(regex, fh.read()) is not None
            dettaglio = ('trovato' if trovato else 'non trovato') + ' in ' + percorso
            return (trovato == atteso), dettaglio
    return True, 'sonda sconosciuta: ' + sonda


# --------------------------------------------------------------------------- raccolta


def raccogli(link_check=False):
    with io.open(ITEMS, encoding='utf-8') as fh:
        dati = yaml.safe_load(fh)
    g = measure_git()
    controlli = measure_controlli()
    stato = {
        'data': _dt.date.today().isoformat(),
        'git': g,
        'schede': measure_schede(g['head_long']),
        'controlli': controlli,
        'link': measure_link(link_check),
        'livelli': dati.get('livelli', {}),
        'aperte': [],
        'chiuse': [],
    }
    for voce in dati.get('voci', []):
        aperta, dettaglio = sonda_aperta(voce.get('sonda'), controlli)
        voce = dict(voce)
        voce['misura'] = dettaglio
        (stato['aperte'] if aperta else stato['chiuse']).append(voce)
    stato['aperte'].sort(key=lambda v: (v.get('livello', 9), v.get('id', 0)))
    stato['chiuse'].sort(key=lambda v: v.get('id', 0))
    return stato


# --------------------------------------------------------------------------- rese


def _intestazione_righe(s):
    g = s['git']
    righe = [
        ('Data', s['data']),
        ('Branch', g['branch'] or '?'),
        ('HEAD', '%s (%s) %s' % (g['head'], g['data_commit'], g['oggetto'])),
        ('Working tree', 'pulito' if g['pulito'] else '%d file modificati' % len(g['modificati'])),
    ]
    dietro = sorted({sc['distanza'] for sc in s['schede'] if sc['distanza'] not in ('', '0')})
    if dietro:
        righe.append(('Schede di contesto', 'indietro di %s commit rispetto a HEAD' % ', '.join(dietro)))
    else:
        righe.append(('Schede di contesto', 'allineate a HEAD'))
    for c in s['controlli']:
        etichetta = c['nome'][0].upper() + c['nome'][1:]
        righe.append((etichetta, ('ok, ' if c['ok'] else 'da sistemare, ') + c['dettaglio']))
    l = s['link']
    if l and l.get('eseguito'):
        n = l['conteggi']
        righe.append(('Link del CV', '%d raggiungibili, %d rotti, %d errori di rete, %d saltati, %d di sola forma'
                      % (n['ok'], n['fail'], n['warn'], n['skip'], n['forma'])))
        for rosso in l['rossi']:
            righe.append(('  da guardare', rosso))
    elif l:
        righe.append(('Link del CV', l.get('nota', 'non verificati')))
    else:
        righe.append(('Link del CV', 'non verificati in questa esecuzione, usa --link-check'))
    return righe


def render_summary(s):
    out = []
    out.append('Roadmap operativa di my-cv, rigenerata il %s' % s['data'])
    out.append('')
    for etichetta, valore in _intestazione_righe(s):
        out.append('  %-22s %s' % (etichetta + ':', valore))
    out.append('')
    livello_corrente = None
    for v in s['aperte']:
        if v.get('livello') != livello_corrente:
            livello_corrente = v.get('livello')
            out.append('')
            out.append('Livello %s: %s' % (livello_corrente, s['livelli'].get(livello_corrente, '')))
            out.append('-' * 78)
        out.append('%3d. [%s] %s' % (v['id'], v.get('dove', ''), v.get('titolo', '')))
        out.append('     stato: %s' % v.get('stato', ''))
        out.append('     passo: %s' % v.get('passo', ''))
        if v.get('fonte'):
            out.append('     fonte: %s' % v['fonte'])
    if s['chiuse']:
        out.append('')
        out.append('Chiuse dalla misura, non piu da fare')
        out.append('-' * 78)
        for v in s['chiuse']:
            out.append('%3d. %s (%s)' % (v['id'], v.get('titolo', ''), v.get('misura', '')))
    out.append('')
    out.append('%d voci aperte, %d chiuse dalla misura.' % (len(s['aperte']), len(s['chiuse'])))
    return '\n'.join(out)


def render_md(s):
    out = ['# Roadmap operativa di my-cv e del suo ecosistema', '',
           '> Documento generato da `tools/roadmap.py` il %s. Non si scrive a mano: le voci stanno in `tools/roadmap-items.yml`, lo stato qui sotto e misurato a ogni esecuzione.' % s['data'],
           '', '## Stato misurato', '', '| Misura | Valore |', '|---|---|']
    for etichetta, valore in _intestazione_righe(s):
        out.append('| %s | %s |' % (etichetta.strip(), valore))
    livello_corrente = None
    for v in s['aperte']:
        if v.get('livello') != livello_corrente:
            livello_corrente = v.get('livello')
            out.append('')
            out.append('## Livello %s: %s' % (livello_corrente, s['livelli'].get(livello_corrente, '')))
        out.append('')
        out.append('### %d. %s' % (v['id'], v.get('titolo', '')))
        out.append('')
        out.append('%s' % v.get('stato', ''))
        out.append('')
        out.append('Prossimo passo: %s' % v.get('passo', ''))
        if v.get('fonte'):
            out.append('')
            out.append('Dove vive: `%s`, repository %s.' % (v['fonte'], v.get('dove', '')))
    if s['chiuse']:
        out.append('')
        out.append('## Chiuse dalla misura')
        out.append('')
        for v in s['chiuse']:
            out.append('- %d. %s, %s.' % (v['id'], v.get('titolo', ''), v.get('misura', '')))
    out.append('')
    return '\n'.join(out)


CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin: 0; font: 11pt/1.5 Georgia, 'Times New Roman', serif; color: #1c1c1c; background: #fff; }
main { max-width: 190mm; margin: 0 auto; padding: 14mm 12mm; }
h1 { font-size: 20pt; margin: 0 0 2mm; letter-spacing: -0.01em; }
.sotto { font-size: 9.5pt; color: #555; margin: 0 0 8mm; font-style: italic; }
h2 { font-size: 13pt; margin: 9mm 0 3mm; padding-bottom: 1.5mm; border-bottom: 1.2pt solid #1c1c1c; }
h3 { font-size: 11pt; margin: 5mm 0 1.5mm; }
p { margin: 0 0 2mm; }
table.stato { width: 100%; border-collapse: collapse; font-size: 9.5pt; margin-bottom: 4mm; }
table.stato td { border-bottom: 0.4pt solid #ccc; padding: 1.4mm 2mm; vertical-align: top; }
table.stato td.k { width: 42mm; color: #555; }
.voce { page-break-inside: avoid; break-inside: avoid; margin-bottom: 4mm; padding-left: 4mm; border-left: 2pt solid #bbb; }
.voce.l0 { border-left-color: #1c1c1c; }
.voce.l1 { border-left-color: #666; }
.passo { font-size: 10pt; }
.passo b { font-variant: small-caps; letter-spacing: 0.03em; font-weight: normal; color: #444; }
.fonte { font-size: 8.5pt; color: #666; font-family: Consolas, 'Courier New', monospace; }
code { font-family: Consolas, 'Courier New', monospace; font-size: 0.92em; }
.rosso { color: #8a1c1c; }
ul.chiuse { font-size: 9.5pt; color: #555; padding-left: 5mm; }
@media print {
  @page { size: A4; margin: 14mm 12mm; }
  main { padding: 0; max-width: none; }
  h2 { page-break-after: avoid; break-after: avoid; }
  a { color: inherit; text-decoration: none; }
}
"""


def render_html(s):
    e = _html.escape
    p = ['<!doctype html><html lang="it"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>Roadmap my-cv %s</title><style>%s</style></head><body><main>' % (e(s['data']), CSS)]
    p.append('<h1>Roadmap operativa di my-cv</h1>')
    p.append('<p class="sotto">Generata da tools/roadmap.py il %s. Le voci stanno in tools/roadmap-items.yml, lo stato qui sotto e misurato a ogni esecuzione.</p>' % e(s['data']))
    p.append('<h2>Stato misurato</h2><table class="stato">')
    for etichetta, valore in _intestazione_righe(s):
        classe = ' class="rosso"' if etichetta.strip() == 'da guardare' else ''
        p.append('<tr><td class="k">%s</td><td%s>%s</td></tr>' % (e(etichetta.strip()), classe, e(str(valore))))
    p.append('</table>')
    livello_corrente = None
    for v in s['aperte']:
        if v.get('livello') != livello_corrente:
            livello_corrente = v.get('livello')
            p.append('<h2>Livello %s: %s</h2>' % (e(str(livello_corrente)), e(s['livelli'].get(livello_corrente, ''))))
        p.append('<div class="voce l%s">' % e(str(v.get('livello', ''))))
        p.append('<h3>%d. %s</h3>' % (v['id'], e(v.get('titolo', ''))))
        p.append('<p>%s</p>' % e(v.get('stato', '')))
        p.append('<p class="passo"><b>Prossimo passo</b> %s</p>' % e(v.get('passo', '')))
        if v.get('fonte'):
            p.append('<p class="fonte">%s &middot; %s</p>' % (e(v['fonte']), e(v.get('dove', ''))))
        p.append('</div>')
    if s['chiuse']:
        p.append('<h2>Chiuse dalla misura</h2><ul class="chiuse">')
        for v in s['chiuse']:
            p.append('<li>%d. %s, %s.</li>' % (v['id'], e(v.get('titolo', '')), e(v.get('misura', ''))))
        p.append('</ul>')
    p.append('</main></body></html>')
    return '\n'.join(p)


# --------------------------------------------------------------------------- cli


def main(argv=None):
    ap = argparse.ArgumentParser(description='Rigenera la roadmap operativa dallo stato corrente.')
    ap.add_argument('--format', choices=('summary', 'md', 'html', 'json'), default='summary')
    ap.add_argument('--link-check', action='store_true',
                    help='verifica anche la raggiungibilita HTTP dei link del CV (lenta, va in rete)')
    ap.add_argument('--write', action='store_true',
                    help='scrive in build/ invece che su stdout')
    ap.add_argument('--out', help='percorso di uscita esplicito, implica --write')
    ap.add_argument('--check', action='store_true',
                    help='exit 1 se resta aperta almeno una voce di livello 0')
    a = ap.parse_args(argv)

    s = raccogli(link_check=a.link_check)

    if a.check:
        zero = [v for v in s['aperte'] if v.get('livello') == 0]
        if zero:
            print('[roadmap] %d voci di livello 0 ancora aperte: %s'
                  % (len(zero), ', '.join(str(v['id']) for v in zero)))
            return 1
        print('[roadmap] nessuna voce di livello 0 aperta.')
        return 0

    testo = {'summary': render_summary, 'md': render_md, 'html': render_html,
             'json': lambda st: json.dumps(st, ensure_ascii=False, indent=2)}[a.format](s)

    if a.out or a.write:
        estensione = {'summary': 'txt', 'md': 'md', 'html': 'html', 'json': 'json'}[a.format]
        destinazione = a.out or os.path.join(BUILD, 'roadmap-%s.%s' % (s['data'], estensione))
        os.makedirs(os.path.dirname(os.path.abspath(destinazione)), exist_ok=True)
        with io.open(destinazione, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(testo if testo.endswith('\n') else testo + '\n')
        print('[roadmap] scritto %s' % os.path.relpath(destinazione, ROOT))
        return 0

    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print(testo)
    return 0


if __name__ == '__main__':
    sys.exit(main())
