---
generated-from-commit: PENDING-FIRST-COMMIT
generated-from-branch: main
generated-date: 2026-06-23
covers-paths:
  - "*.tex"
  - "sections/**"
  - ".latexmkrc"
  - "tex-packages.txt"
last-verified-commit: PENDING-FIRST-COMMIT
---

# Stack applicativo

## Stack e runtime

Linguaggio: LaTeX (pdflatex, fissato in `.latexmkrc`). Distribuzione: TinyTeX user-local (`%APPDATA%\TinyTeX` su Windows), condivisa fra i progetti. Build: pdflatex diretto (non latexmk dal 2026-07-08, ADR-006), invocato via `scripts/build.ps1` (Windows) o `scripts/build.sh` (Unix); compila sempre le tre lingue EN/IT/ES in un'unica esecuzione, sovrascrivendo `cv-sopranzi-alessio-{en,it,es}.pdf` nella radice. Manifesto pacchetti: `tex-packages.txt` (fonte riproducibile dell'ambiente). Classe CV: da scegliere (vedi `memory/decisions.md`, ADR-002).

## Alternative deliberatamente escluse

lualatex/xelatex: supportano meglio i font OpenType, ma riducono la compatibilita' con le classi CV piu' diffuse su Windows. Rivalutare se si sceglie altacv.

Overleaf: editor cloud comodo per la collaborazione, ma introduce una dipendenza esterna per la compilazione e non si integra con il sistema di contesto versionato. Il workflow locale con TinyTeX e' riproducibile e offline.

## Flussi di codice e ruolo architetturale dei file

```
cv.tex              documento principale: preambolo, include delle sezioni, configurazione classe
sections/           sottosezioni separate (education.tex, experience.tex, skills.tex, ...)
assets/             immagini e loghi referenziati nel documento
.latexmkrc          fissa engine e opzioni di compilazione
tex-packages.txt    manifesto dei pacchetti tlmgr
scripts/build.ps1   compila il documento (Windows)
scripts/build.sh    compila il documento (Unix/macOS)
scripts/setup-tex.ps1   installa TinyTeX e i pacchetti (Windows)
scripts/setup-tex.sh    installa TinyTeX e i pacchetti (Unix/macOS)
```

## Riferimenti a snippet

Da popolare dopo la creazione di `cv.tex`.
