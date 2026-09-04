#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estrae lo stato misurabile dell'ecosistema personale e rigenera il grafo di architettura.

Perché esiste, e perché è separato da extract-cv-links.py. Il diagramma di architettura dell'
ecosistema viveva in `_notes/architecture-diagram.html`, scritto a mano il 2026-07-13 e ignorato
da git. Al controllo del 2026-09-04 portava quattro affermazioni false: dichiarava `projects` non
ancora collegato al CV mentre il CV ne linka otto pagine, dichiarava gli interessi non ancora
collegati alle topic page mentre i tag collegati sono quindici, contava 29 repository personali
dove oggi ce ne sono 38 con un remote, e diceva di vivere anche in un `ARCHITECTURE.md` che non
esiste in nessuna cartella del progetto. Nessuna di quelle quattro è una svista di scrittura: sono
il risultato prevedibile di numeri scritti a mano in un documento che nessuno rigenera, cioè lo
stesso difetto che ADR-008 ha risolto per l'inventario dei link.

Divisione di responsabilità, decisa il 2026-09-04. Questo strumento misura e disegna a livello di
banda: quante fonti, quanti motori, quanti siti, quanti bersagli. Il dettaglio dei progetti che
vivono su D: appartiene al repository `projects`, perché sono progetti aziendali e quello è il
sito che li descrive; qui si contano le cartelle e non si leggono né si trascrivono nomi, domini
o indirizzi, per la stessa ragione già registrata nel diagramma di luglio a proposito
dell'anonimizzazione insufficiente a monte.

Separato da extract-cv-links.py perché risponde a un'altra domanda. Quello descrive dove punta il
CV e con quale strumento si verifica; questo descrive come l'ecosistema si aggiorna. Lo strato dei
link del CV non viene ricalcolato qui: si chiede a extract-cv-links.py il suo JSON, così esiste
una sola definizione di "link del CV" anche in questo diagramma.

Uso:
    python tools/extract-ecosystem.py                  # riepilogo leggibile
    python tools/extract-ecosystem.py --format json     # stato ispezionabile
    python tools/extract-ecosystem.py --format mermaid  # blocco del grafo
    python tools/extract-ecosystem.py --write           # aggiorna la regione della scheda
    python tools/extract-ecosystem.py --check           # verifica la deriva, exit 1 se c'è
"""

import argparse
import glob
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CARD = os.path.join(ROOT, '.claude', 'context', 'architecture.md')
REGION = 'ecosistema'

DEFAULT_E = 'E:' + os.sep
DEFAULT_D = 'D:' + os.sep

# I repository di E: che sono infrastruttura dell'ecosistema, non progetti personali da mostrare
# nel navigator: si contano a parte perché il loro numero non deve gonfiare il conteggio dei
# progetti, ed è la confusione che rendeva incomprensibile il "29 repository" del diagramma vecchio.
INFRASTRUCTURE = {'my-cv', 'projects', 'skills', 'blog-alessio', 'lettore-doc',
                  'template-claude-developing'}


# ----------------------------------------------------------------------------------------------
# I/O che preserva la forma del file, e regioni generate
# ----------------------------------------------------------------------------------------------

def read_text(path):
    with open(path, 'rb') as fh:
        raw = fh.read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    if bom:
        raw = raw[3:]
    text = raw.decode('utf-8')
    newline = '\r\n' if '\r\n' in text else '\n'
    return text.replace('\r\n', '\n'), newline, bom


def write_text(path, text, newline, bom):
    out = text.replace('\r\n', '\n')
    if newline != '\n':
        out = out.replace('\n', newline)
    data = out.encode('utf-8')
    if bom:
        data = b'\xef\xbb\xbf' + data
    with open(path, 'wb') as fh:
        fh.write(data)


def markers(name):
    return ('<!-- BEGIN GENERATED ecosystem: %s -->' % name,
            '<!-- END GENERATED ecosystem: %s -->' % name)


def region_body(text, name):
    begin, end = markers(name)
    i, j = text.find(begin), text.find(end)
    if i < 0 or j < 0 or j < i:
        return None
    return text[i + len(begin):j].strip('\n')


def replace_region(text, name, body):
    begin, end = markers(name)
    i, j = text.find(begin), text.find(end)
    if i < 0 or j < 0 or j < i:
        raise SystemExit('[extract-ecosystem] Regione "%s" assente o malformata in %s.'
                         % (name, CARD))
    return text[:i] + begin + '\n\n' + body.rstrip('\n') + '\n\n' + text[j:]


# ----------------------------------------------------------------------------------------------
# Misura
# ----------------------------------------------------------------------------------------------

def git_remote(path):
    try:
        out = subprocess.run(['git', '-C', path, 'remote', 'get-url', 'origin'],
                             capture_output=True, timeout=15)
        if out.returncode != 0:
            return None
        url = out.stdout.decode('utf-8', 'replace').strip()
        m = re.search(r'[:/]([^/]+/[^/]+?)(?:\.git)?$', url)
        return m.group(1) if m else url
    except Exception:
        return None


def measure_e(e_root):
    """Repository sotto E: con un remote GitHub, separando infrastruttura e progetti."""
    if not os.path.isdir(e_root):
        return {'available': False, 'root': e_root, 'repos': [], 'infrastructure': [],
                'projects': []}
    repos = []
    for entry in sorted(os.listdir(e_root)):
        path = os.path.join(e_root, entry)
        if not os.path.isdir(os.path.join(path, '.git')):
            continue
        remote = git_remote(path)
        if remote:
            repos.append({'name': entry, 'remote': remote})
    infra = [r['name'] for r in repos if r['name'] in INFRASTRUCTURE]
    proj = [r['name'] for r in repos if r['name'] not in INFRASTRUCTURE]
    return {'available': True, 'root': e_root, 'repos': repos,
            'infrastructure': sorted(infra), 'projects': sorted(proj)}


def measure_d(d_root):
    """Solo il conteggio delle cartelle di primo livello. Nessun nome viene letto o riportato.

    Il vincolo non è di stile: quelle cartelle contengono nomi di clienti, domini aziendali e
    indirizzi reali, e il diagramma di luglio registra che l'anonimizzazione a monte del progetto
    sorgente era insufficiente. Contare è sufficiente per un diagramma di architettura; leggere no.
    """
    if not os.path.isdir(d_root):
        return {'available': False, 'root': d_root, 'folders': 0}
    n = 0
    try:
        for entry in os.listdir(d_root):
            if os.path.isdir(os.path.join(d_root, entry)) and not entry.startswith('$'):
                n += 1
    except OSError:
        return {'available': False, 'root': d_root, 'folders': 0}
    return {'available': True, 'root': d_root, 'folders': n}


def measure_blog(path):
    """Post reali, topic dichiarati nel registro, e quanti topic hanno almeno un post.

    La distinzione conta: il blog dichiara un topic come area di interesse curata che riceve una
    descrizione editoriale anche a zero articoli (ADR-018 di quel repository), quindi una topic
    page senza post non è una pagina vuota. Confonderli produce un allarme falso, come verificato
    il 2026-09-03.
    """
    posts_dir = os.path.join(path, 'content', 'posts')
    topics_file = os.path.join(path, 'src', 'config', 'topics.ts')
    if not os.path.isdir(posts_dir):
        return {'available': False, 'root': path}
    tags = set()
    posts = 0
    for p in glob.glob(os.path.join(posts_dir, '*', '*.md*')):
        posts += 1
        text = open(p, encoding='utf-8', errors='replace').read()
        m = re.search(r'^tags:\s*\[(.*?)\]', text, re.M)
        if m:
            tags.update(re.findall(r'["\']([^"\']+)["\']', m.group(1)))
    topics = []
    if os.path.exists(topics_file):
        ts = open(topics_file, encoding='utf-8', errors='replace').read()
        topics = re.findall(r"\{\s*id:\s*'([^']+)',\s*tags:\s*\{\s*en:\s*'([^']+)',\s*it:\s*'([^']+)'",
                            ts)
    with_posts = [t[0] for t in topics if t[1] in tags or t[2] in tags]
    return {'available': True, 'root': path, 'posts': posts, 'topics': len(topics),
            'topics_with_posts': len(with_posts), 'tags_in_posts': sorted(tags)}


def measure_projects(path):
    """Pagine per sezione, contando una sola volta le varianti di lingua."""
    docs = os.path.join(path, 'docs')
    if not os.path.isdir(docs):
        return {'available': False, 'root': path, 'sections': {}}
    sections = {}
    for name in sorted(os.listdir(docs)):
        d = os.path.join(docs, name)
        if not os.path.isdir(d) or name in ('assets', 'stylesheets'):
            continue
        stems = set()
        for f in os.listdir(d):
            if f.endswith('.md') and not f.startswith('_'):
                stems.add(f.split('.')[0])
        stems.discard('index')
        sections[name] = len(stems)
    return {'available': True, 'root': path, 'sections': sections}


def measure_skills(path):
    docs = os.path.join(path, 'docs')
    if not os.path.isdir(docs):
        return {'available': False, 'root': path, 'pages': 0}
    pages = 0
    for _root, _dirs, files in os.walk(docs):
        pages += sum(1 for f in files if f.endswith('.md'))
    return {'available': True, 'root': path, 'pages': pages}


def measure_cv():
    """Lo strato dei link del CV non si ricalcola: si chiede a extract-cv-links.py."""
    tool = os.path.join(HERE, 'extract-cv-links.py')
    if not os.path.exists(tool):
        return {'available': False}
    try:
        out = subprocess.run([sys.executable, tool, '--format', 'json'],
                             capture_output=True, timeout=180, cwd=ROOT)
        if out.returncode != 0:
            return {'available': False}
        data = json.loads(out.stdout.decode('utf-8'))
    except Exception:
        return {'available': False}
    cv = data['cv']
    return {
        'available': True,
        'targets': cv['targets_total'],
        'url_strings': cv['url_strings_total'],
        'by_category': cv['counts_by_category'],
    }


def measure(e_root, d_root):
    e = measure_e(e_root)
    return {
        'e': e,
        'd': measure_d(d_root),
        'blog': measure_blog(os.path.join(e_root, 'blog-alessio')),
        'projects': measure_projects(os.path.join(e_root, 'projects')),
        'skills': measure_skills(os.path.join(e_root, 'skills')),
        'cv': measure_cv(),
    }


# ----------------------------------------------------------------------------------------------
# Grafo
# ----------------------------------------------------------------------------------------------

def render_mermaid(m):
    e, d, blog, proj, skills, cv = m['e'], m['d'], m['blog'], m['projects'], m['skills'], m['cv']
    L = []
    L.append('```mermaid')
    L.append('flowchart TB')
    L.append('    subgraph FONTI["1. Fonti: dove il lavoro reale succede"]')
    if d['available']:
        L.append('    D_ROOT["D:\\ progetti aziendali<br/>%d cartelle, solo contate"]' % d['folders'])
    L.append('    VM["VM aziendali su Proxmox<br/>dettaglio nel repo projects"]')
    if e['available']:
        # L'infrastruttura sta nell'etichetta e non in un nodo proprio: come nodo resterebbe
        # appeso senza archi, perché quei repository *sono* i motori e i siti delle bande 2 e 3.
        L.append('    E_ROOT["E:\\ repository personali<br/>%d con remote GitHub<br/>più %d di infrastruttura"]'
                 % (len(e['projects']), len(e['infrastructure'])))
    L.append('    DOCS["Corpus documentali<br/>OneDrive aziendale e sorgenti personali"]')
    L.append('    end')
    L.append('')
    L.append('    subgraph MOTORI["2. Motori: da fonte grezza a pagina"]')
    L.append('    UPD["update_personal_projects.py<br/>scopre i repo, genera le pagine"]')
    L.append('    CHK["check_company_changes.py<br/>segnala i cambi su D:, solo metadati"]')
    L.append('    LETT["lettore-doc<br/>estrae la tassonomia di competenze"]')
    L.append('    GRAPHIFY["graphify<br/>corpus verso knowledge graph"]')
    L.append('    end')
    L.append('')
    L.append('    subgraph SITI["3. Siti pubblicati su GitHub Pages"]')
    if proj['available']:
        secs = ', '.join('%s %d' % (k, v) for k, v in sorted(proj['sections'].items()))
        L.append('    S_PROJ["projects<br/>%s"]' % secs)
    if blog['available']:
        L.append('    S_BLOG["blog<br/>%d post, %d topic di cui %d con post"]'
                 % (blog['posts'], blog['topics'], blog['topics_with_posts']))
    if skills['available']:
        L.append('    S_SKILLS["skills<br/>%d pagine + grafo graphify"]' % skills['pages'])
    L.append('    end')
    L.append('')
    L.append('    subgraph CONSUMO["4. Consumo: il CV"]')
    if cv['available']:
        L.append('    CV["main.tex verso 3 PDF<br/>%d bersagli, %d URL"]'
                 % (cv['targets'], cv['url_strings']))
    else:
        L.append('    CV["main.tex verso 3 PDF"]')
    L.append('    PROTON["Proton Drive<br/>archivio privato + link pubblici"]')
    L.append('    end')
    L.append('')
    if e['available']:
        L.append('    E_ROOT --> UPD')
    if d['available']:
        L.append('    D_ROOT --> CHK')
    L.append('    VM -.->|"monitoraggio SSH da scrivere"| CHK')
    L.append('    DOCS --> LETT')
    L.append('    LETT --> GRAPHIFY')
    L.append('    UPD --> S_PROJ')
    L.append('    CHK -->|"segnala, non pubblica"| S_PROJ')
    L.append('    GRAPHIFY --> S_SKILLS')
    L.append('')
    if cv['available']:
        c = cv['by_category']
        L.append('    CV -->|"%d pagine"| S_PROJ' % c.get('projects', 0))
        L.append('    CV -->|"%d link"| S_SKILLS' % c.get('skills', 0))
        L.append('    CV -->|"%d bersagli"| S_BLOG' % c.get('blog', 0))
        L.append('    CV -->|"%d documenti pubblicati"| PROTON' % c.get('proton', 0))
        if c.get('gdrive'):
            L.append('    CV -.->|"%d ancora su Google Drive"| GDRIVE["Google Drive"]'
                     % c['gdrive'])
        if c.get('tinyurl'):
            L.append('    CV -.->|"%d redirect"| TINY["tinyurl.com"]' % c['tinyurl'])
    L.append('```')
    return '\n'.join(L)


def render_summary(m):
    out = ['[extract-ecosystem] stato misurato:']
    e = m['e']
    if e['available']:
        out.append('  E:\\  %d repository con remote, di cui %d progetti e %d infrastruttura'
                   % (len(e['repos']), len(e['projects']), len(e['infrastructure'])))
    if m['d']['available']:
        out.append('  D:\\  %d cartelle di primo livello, solo contate' % m['d']['folders'])
    b = m['blog']
    if b['available']:
        out.append('  blog     %d post, %d topic nel registro, %d con almeno un post'
                   % (b['posts'], b['topics'], b['topics_with_posts']))
    p = m['projects']
    if p['available']:
        out.append('  projects %s'
                   % ', '.join('%s %d' % (k, v) for k, v in sorted(p['sections'].items())))
    if m['skills']['available']:
        out.append('  skills   %d pagine' % m['skills']['pages'])
    c = m['cv']
    if c['available']:
        out.append('  CV       %d bersagli, %d stringhe URL' % (c['targets'], c['url_strings']))
    return '\n'.join(out)


# ----------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="Misura l'ecosistema e rigenera il grafo di architettura.")
    ap.add_argument('--e-root', default=DEFAULT_E, help='radice dei repository personali')
    ap.add_argument('--d-root', default=DEFAULT_D, help='radice dei progetti aziendali, solo contata')
    ap.add_argument('--format', choices=('summary', 'json', 'mermaid'), default='summary')
    ap.add_argument('--write', action='store_true', help='aggiorna la regione generata della scheda')
    ap.add_argument('--check', action='store_true', help='verifica la deriva, exit 1 se presente')
    args = ap.parse_args(argv)

    m = measure(args.e_root, args.d_root)

    if args.check or args.write:
        if not os.path.exists(CARD):
            print('[extract-ecosystem] Scheda assente: %s' % CARD)
            return 1
        text, newline, bom = read_text(CARD)
        body = render_mermaid(m)
        current = region_body(text, REGION)
        if current is None:
            print('[extract-ecosystem] Marcatori della regione "%s" assenti in architecture.md.'
                  % REGION)
            return 1
        if current.strip('\n') == body.strip('\n'):
            print('[extract-ecosystem] Scheda allineata allo stato misurato.')
            return 0
        if args.check:
            print('[extract-ecosystem] Deriva rilevata fra stato misurato e architecture.md.')
            print('[extract-ecosystem] Rigenerare con: python tools/extract-ecosystem.py --write')
            return 1
        write_text(CARD, replace_region(text, REGION, body), newline, bom)
        print('[extract-ecosystem] architecture.md aggiornata.')
        return 0

    if args.format == 'json':
        print(json.dumps(m, indent=2, ensure_ascii=False))
    elif args.format == 'mermaid':
        print(render_mermaid(m))
    else:
        print(render_summary(m))
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    else:  # pragma: no cover
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.exit(main())
