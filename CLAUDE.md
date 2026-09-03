# my-cv

> Istruzioni di team, versionate. Questo file è l'indice del progetto.

## Cos'è questo progetto

`my-cv` è il Curriculum Vitae in formato LaTeX di Alessio Sopranzi. Il CV è scritto a mano e aggiornato manualmente: non si genera automaticamente da nessuna pipeline. La tassonomia delle competenze IT in `skills-repo` è però la fonte di verità per selezionare, nominare e descrivere le skill da includere: quando si aggiunge o rimuove una competenza, si verifica prima che il nome sia coerente con come quella skill compare nel sito pubblico `alesop95.github.io/skills/`. Il grafo interattivo a `alesop95.github.io/skills/graphify-out/graph.html` (141 nodi, 195 archi, 14 comunità) è lo strumento di lettura per capire i cluster di competenze e decidere cosa enfatizzare.

`skills-repo` vive localmente a `$env:LETTERDOC_SKILLS_REPO`. La pipeline che lo popola parte da `lettore-doc` (E:\lettore-doc). `my-cv` non chiama nessuna pipeline: legge come riferimento.

## Procedura di ripresa in una sessione nuova

Leggere per primo `.claude/memory/index.md` (branch, commit di riferimento, stato di verifica delle schede, punto di ripresa). Leggere poi `.claude/context/current-work.md` se c'è una sezione del CV in lavorazione. Invocare la skill `sync-context` per verificare il drift tra schede e sorgente LaTeX. Leggere solo le schede pertinenti al task, mai tutte insieme. Il work-log `.claude/memory/progress.md` e il registro `.claude/memory/decisions.md` (in particolare ADR-001 sull'engine e ADR-002 sulla classe CV) forniscono la storia e le decisioni quando servono.

Per riprendere da zero: invocare `/onboard`. Per compilare il PDF: `/latex-build`.

## Indice dei file satellite tracciati

Memoria e meta-stato, sotto `.claude/memory/`, letti sempre a inizio sessione.

```
.claude/memory/index.md       snapshot e tabella di sincronizzazione, da leggere per primo
.claude/memory/progress.md    work-log append-only di passi e compilazioni
.claude/memory/decisions.md   registro ADR-lite (engine, classe CV, scelta PDF versionato)
```

Schede tecniche, sotto `.claude/context/`, con frontmatter di riconciliazione.

```
.claude/context/STACK.md                stack LaTeX, distribuzione, flussi di build
.claude/context/deployment.md           come buildare e distribuire il PDF
.claude/context/dev-testing.md          ciclo modifica-compila-verifica, errori comuni
.claude/context/current-work.md         sezione CV in lavorazione, definition of done
.claude/context/roadmap.md              fasi di sviluppo e direzione
.claude/context/external-links.md       inventario di ogni link esterno citato nel CV, per categoria
.claude/context/external-dependencies.md dipendenze verso skills-repo/projects/blog/Drive, come
                                         verificarle e cosa fare quando cambiano
```

Build LaTeX, sotto `scripts/` e nella radice.

```
scripts/build.ps1              compila i tre PDF stabili EN/IT/ES, sempre insieme (Windows)
scripts/build.sh               compila i tre PDF stabili EN/IT/ES, sempre insieme (Unix/macOS)
scripts/setup-tex.ps1          installa TinyTeX e i pacchetti (Windows)
scripts/setup-tex.sh           installa TinyTeX e i pacchetti (Unix/macOS)
scripts/check-links.ps1        verifica HTTP di tutti i link del CV, per categoria (Windows)
scripts/check-links.sh         verifica HTTP di tutti i link del CV, per categoria (Unix/macOS)
scripts/check-skill-links.ps1  involucro storico su check-links -Category skills (Windows)
scripts/check-skill-links.sh   involucro storico su check-links --category skills (Unix/macOS)
scripts/build-multilang.ps1    compila i tre PDF datati EN/IT/ES (Windows)
scripts/build-multilang.sh     compila i tre PDF datati EN/IT/ES (Unix/macOS)
.latexmkrc                     configurazione latexmk, non più usata dalla build (vedi STACK.md)
tex-packages.txt               manifesto dei pacchetti tlmgr (fonte riproducibile dell'ambiente)
```

Strumenti di verifica e normalizzazione, sotto `tools/`.

```
tools/extract-cv-links.py     estrae inventario e grafo dei link dal sorgente, rigenera le schede
tools/md-unwrap.py            applica e verifica la convenzione Markdown a riga sorgente unica
tools/lint-md-commands.py     linter dei comandi di shell nei blocchi Markdown
tools/fix-accents.py          converte gli accenti scritti con l'apostrofo in accenti veri
tools/fix-missing-accents.py  ripristina gli accenti mancanti del tutto, dove sono decidibili
tools/fix-dashes.py           normalizza i trattini lunghi in trattini brevi
tools/dashes-exclude.txt      percorsi esclusi dalla normalizzazione dei trattini
tools/latest-screenshot.ps1   percorso dell'ultimo screenshot, per la revisione visiva
```

Skill richiamabili, sotto `.claude/skills/`.

```
.claude/skills/latex-build/SKILL.md    build e setup dell'ambiente LaTeX
.claude/skills/sync-context/SKILL.md   verifica drift schede vs sorgente
.claude/skills/onboard/SKILL.md        spiegazione completa del progetto
```

## Vincoli di team

Le operazioni di `git add`, commit e push restano sempre manuali. L'identità git è quella personale: `alesop95` / `alessio.sopranzi.95@gmail.com` / alias SSH `github-personal`. Lo stile di documentazione e di interazione segue `.claude/rules/interaction-style.md`. Claude non scrive autonomamente nei file di memoria e di contesto: li aggiorna solo su richiesta esplicita.
