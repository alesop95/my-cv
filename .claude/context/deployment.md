---
generated-from-commit: PENDING-FIRST-COMMIT
generated-from-branch: main
generated-date: 2026-06-23
covers-paths:
  - "*.tex"
  - "scripts/**"
  - ".latexmkrc"
  - "tex-packages.txt"
last-verified-commit: PENDING-FIRST-COMMIT
---

# Build e distribuzione

## Prerequisiti

TinyTeX installato user-local. Se assente, eseguire una volta:

```
powershell -ExecutionPolicy Bypass -File scripts\setup-tex.ps1
```

## Compilare il PDF

```
powershell -ExecutionPolicy Bypass -File scripts\build.ps1
```

Il PDF viene prodotto nella radice accanto al `.tex` principale. Se ci sono piu' file `.tex`
nella radice, specificare il principale con `-Main cv.tex`.

## Pulire i file ausiliari

```
powershell -ExecutionPolicy Bypass -File scripts\build.ps1 -Clean
```

Il flag `-Clean` rimuove gli ausiliari e lascia il PDF. `-CleanAll` rimuove anche il PDF.

## Distribuzione del CV

Il PDF e' il deliverable finale. Due opzioni:

- Versionare il PDF nel repository (utile per avere sempre l'ultima versione pubblicata
  accanto al sorgente): verificare prima che non contenga dati sensibili (indirizzo di casa,
  telefono) se il repository e' pubblico.
- Non versionare il PDF (generato localmente on-demand): aggiungere `*.pdf` al `.gitignore`.
  Attualmente il `.gitignore` commenta `*.pdf` per ricordare questa scelta.

## Aggiunta di un pacchetto

1. Aggiungere il nome tlmgr a `tex-packages.txt`.
2. Rieseguire `scripts\setup-tex.ps1` (installa solo cio' che manca).
3. Aggiungere `\usepackage{...}` nel preambolo del `.tex`.
