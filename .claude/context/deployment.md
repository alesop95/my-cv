---
generated-from-commit: 828275c
generated-from-branch: main
generated-date: 2026-06-23
covers-paths:
  - "main.tex"
  - "scripts/**"
  - ".latexmkrc"
  - "tex-packages.txt"
last-verified-commit: c994a08
---

# Build e distribuzione

## Prerequisiti

TinyTeX installato user-local. Se assente, eseguire una volta:

```
powershell -ExecutionPolicy Bypass -File scripts\setup-tex.ps1
```

## Compilare il PDF (ADR-006)

`main.tex` è parametrizzato per lingua tramite `\CVlanguage` e la macro `\cvtext{italiano}{spagnolo}{inglese}`. Non esiste più un `main.pdf` singolo: `scripts/build.ps1` compila sempre tutte e tre le lingue in un'unica esecuzione e sovrascrive tre file stabili nella radice del progetto.

```
powershell -ExecutionPolicy Bypass -File scripts\build.ps1
```

Produce (sovrascrivendoli) `cv-sopranzi-alessio-en.pdf`, `cv-sopranzi-alessio-it.pdf`, `cv-sopranzi-alessio-es.pdf` nella radice, tutti e tre versionati in git. Da lanciare prima di ogni commit che tocca `main.tex`, così le tre lingue non si disallineano mai tra loro. Compila con pdflatex direttamente (due passaggi fissi), non con latexmk: l'argomento `-jobname` iniettato per selezionare la lingua non è un vero nome di file e comprometterebbe l'analisi delle dipendenze di latexmk.

## Pulire i file ausiliari

```
powershell -ExecutionPolicy Bypass -File scripts\build.ps1 -Clean
```

Rimuove i tre PDF stabili e i loro ausiliari (`.aux`/`.log`/`.out`/`.synctex.gz`) dalla radice. Non esiste più un flag `-CleanAll` separato (rimosso insieme al vecchio flusso a lingua singola basato su latexmk).

## Istantanee datate multilingua (archivio storico, separato)

```
powershell -ExecutionPolicy Bypass -File scripts\build-multilang.ps1
```

Scopo diverso dal build standard sopra: produce PDF datati (`cv-sopranzi-alessio-<lingua>-<data>.pdf`) in `dated-builds/<lingua>/`, un archivio locale **non versionato** (`dated-builds/` è in `.gitignore`, ADR-005), utile per conservare uno storico di cosa è stato inviato e quando. Non sostituisce `scripts/build.ps1`: quello resta l'unico comando da lanciare prima di un commit.

## Verifica dei link prima di una build definitiva

Il CV cita 52 bersagli esterni e quasi tutti possono rompersi senza che il sorgente cambi: le Capability page di `alesop95.github.io/skills/` appartengono a una tassonomia che continua ad aggiornarsi e che può rinominare o rimuovere pagine, i documenti di archivio possono perdere la condivisione pubblica, i redirect possono puntare a una destinazione sbagliata. Fino al 2026-09-03 il controllo automatico copriva 5 di quei 52 bersagli; ora li copre tutti, raggruppati per categoria, con `scripts/check-links.ps1` e il gemello `.sh`.

```
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check-links.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check-links.ps1 -Category skills,projects
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check-links.ps1 -Category tinyurl -ShowFinalUrl
```

```bash
bash scripts/check-links.sh
bash scripts/check-links.sh --category skills,projects
bash scripts/check-links.sh --category tinyurl --show-final-url
```

L'elenco dei link non viene ricavato da una regex propria dello script ma dalla proiezione tabellare di `tools/extract-cv-links.py`, la stessa fonte che genera l'inventario e il grafo delle dipendenze: esiste una sola definizione di cosa sia un link del CV, e aggiungerne uno nel sorgente lo mette automaticamente sotto controllo.

Tre comportamenti da conoscere per leggere il rapporto. I redirect vengono seguiti un salto alla volta e la destinazione finale viene riportata, che è il modo per sapere senza aprire un browser dove atterrano davvero i dieci link `tinyurl`. Un fallimento a livello di rete, stampato come `WARN` e con codice di uscita 2, non è la stessa cosa di un errore HTTP, stampato come `FAIL` e con codice di uscita 1: il primo può dipendere dal resolver locale, come verificato il 2026-09-03 su `intrawelt.com`, che il DNS del router non risolveva mentre i resolver pubblici restituivano regolarmente il suo indirizzo. Un 2xx su una topic page del blog, infine, dice che la pagina esiste e non che il suo contenuto sia pertinente.

Non fa parte della build: `scripts/build.ps1` non lo invoca. Va eseguito a mano prima di ogni build che produce un PDF destinato a essere inviato o pubblicato, e periodicamente anche senza modifiche al CV, perché a rompersi è la destinazione remota, non il sorgente locale.

## Distribuzione del CV

I tre PDF stabili (`cv-sopranzi-alessio-{en,it,es}.pdf`) sono versionati deliberatamente nel repository (ADR-004, esteso alle tre lingue in ADR-006): danno un link diretto e sempre aggiornato al CV compilato in ciascuna lingua, direttamente su GitHub. Verificare che non contengano dati sensibili (indirizzo di casa, telefono) prima di rendere il repository pubblico, se non lo è già.

## Aggiunta di un pacchetto

1. Aggiungere il nome tlmgr a `tex-packages.txt`.
2. Rieseguire `scripts\setup-tex.ps1` (installa solo ciò che manca).
3. Aggiungere `\usepackage{...}` nel preambolo del `.tex`.
