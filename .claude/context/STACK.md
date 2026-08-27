---
generated-from-commit: 828275c
generated-from-branch: main
generated-date: 2026-06-23
covers-paths:
  - "main.tex"
  - "altacv.cls"
  - ".latexmkrc"
  - "tex-packages.txt"
last-verified-commit: c994a08
---

# Stack applicativo

## Stack e runtime

Linguaggio: LaTeX (pdflatex). Distribuzione: TinyTeX user-local (`%APPDATA%\TinyTeX` su Windows), condivisa fra i progetti. Build: pdflatex diretto (non latexmk dal 2026-07-08, ADR-006), invocato via `scripts/build.ps1` (Windows) o `scripts/build.sh` (Unix); compila sempre le tre lingue EN/IT/ES in un'unica esecuzione, sovrascrivendo `cv-sopranzi-alessio-{en,it,es}.pdf` nella radice. Manifesto pacchetti: `tex-packages.txt` (fonte riproducibile dell'ambiente). Classe CV: altaCV, scelta in ADR-002 e vendorizzata nella radice come `altacv.cls`, con una patch locale a `\cvachievement` documentata in `altacv-reference.md`.

`.latexmkrc` è un residuo del flusso originario e non governa più nessuna build: fissa engine e opzioni per latexmk, ma dal 2026-07-08 nessuno script lo invoca. `scripts/build.ps1` nomina latexmk solo nei commenti che spiegano perché lo evita, cioè che l'argomento `-jobname` iniettato per selezionare la lingua non è un vero nome di file e comprometterebbe l'analisi delle dipendenze. Resta in radice come comodità per chi compila a mano con latexmk durante la scrittura, non perché la build lo legga.

La foto della testata non è nel repository. `main.tex` la carica con `\photoR{2.6cm}{attachments/Template e photos/photo-me-gemini.jpeg}`, e `attachments/` è ignorato da git per ADR-003 insieme al resto dei materiali privati. La conseguenza pratica va tenuta presente prima di clonare altrove: un clone pulito non compila finché quel file non viene rimesso a mano al suo posto.

## Alternative deliberatamente escluse

lualatex/xelatex: supportano meglio i font OpenType, ma riducono la compatibilità con le classi CV più diffuse su Windows. La rivalutazione prevista al momento della scelta della classe è stata fatta e ha confermato pdflatex (ADR-001): altaCV non richiede font OpenType e compila senza attriti con l'engine attuale.

Overleaf: editor cloud comodo per la collaborazione, ma introduce una dipendenza esterna per la compilazione e non si integra con il sistema di contesto versionato. Il workflow locale con TinyTeX è riproducibile e offline.

## Flussi di codice e ruolo architetturale dei file

```
main.tex                     documento unico: preambolo, macro multilingua, tutto il contenuto (nessun include)
altacv.cls                   classe altaCV vendorizzata e patchata in locale (ADR-002)
attachments/                 materiali privati, ignorati da git (ADR-003): contiene la foto della testata
.latexmkrc                   configurazione latexmk, non più usata dalla build (vedi sopra)
tex-packages.txt             manifesto dei pacchetti tlmgr
scripts/build.ps1 / .sh      compila insieme i tre PDF stabili EN/IT/ES (ADR-006)
scripts/build-multilang.*    archivio datato in dated-builds/, non versionato (ADR-005)
scripts/check-skill-links.*  verifica HTTP dei link a skills-repo citati nel .tex
scripts/setup-tex.*          installa TinyTeX e i pacchetti di tex-packages.txt
tools/md-unwrap.py           applica la convenzione Markdown a riga sorgente unica
tools/lint-md-commands.py    linter dei comandi di shell nei blocchi Markdown
tools/fix-accents.py         converte gli accenti scritti con l'apostrofo in accenti veri
tools/fix-missing-accents.py ripristina gli accenti mancanti del tutto, dove sono decidibili
tools/fix-dashes.py          normalizza i trattini lunghi in trattini brevi
tools/dashes-exclude.txt     percorsi esclusi dalla normalizzazione dei trattini
tools/latest-screenshot.ps1  percorso dell'ultimo screenshot, per la revisione visiva
```

## Riferimenti a snippet

Gli snippet annotati della classe e delle macro locali vivono in `altacv-reference.md`, che è la scheda dedicata. Qui resta il solo ruolo architetturale dei file.
