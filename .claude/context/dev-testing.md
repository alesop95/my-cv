---
generated-from-commit: PENDING-FIRST-COMMIT
generated-from-branch: main
generated-date: 2026-06-23
covers-paths:
  - "*.tex"
  - "sections/**"
last-verified-commit: PENDING-FIRST-COMMIT
---

# Revisione e verifica del documento

## Ciclo di sviluppo tipico

Il ciclo e' modifica-compila-leggi. Non esiste una test suite automatizzata: la verifica e'
visiva sul PDF prodotto.

1. Modificare il sorgente `.tex` o le sezioni in `sections/`.
2. Compilare: `scripts\build.ps1`.
3. Aprire il PDF con il visualizzatore PDF preferito (SumatraPDF su Windows e' comodo perche'
   ricarica automaticamente il file alla ricompilazione).
4. Verificare layout, spaziatura, link cliccabili, encoding dei caratteri accentati.

## Errori di compilazione

latexmk stampa l'errore con il numero di riga. Cercare la prima riga che inizia con `!` nell'output.
Se un pacchetto non e' trovato, il messaggio indica il file `.sty` mancante: aggiungere il pacchetto
a `tex-packages.txt` e rieseguire il setup.

## Revisione del contenuto

La tassonomia delle competenze in `skills-repo` e' la fonte di verita' per i nomi delle skill
incluse nel CV. Prima di aggiungere o rimuovere una competenza, verificare come e' denominata
nel sito `alesop95.github.io/skills/` o nel grafo `graphify-out/graph.html`.

## Verifica visiva pre-distribuzione

Prima di inviare il PDF a un recruiter o di pubblicarlo:
- Verificare che tutti i link siano cliccabili e puntino agli URL giusti.
- Verificare che i dati di contatto siano presenti e corretti.
- Verificare che non ci siano overfull hbox visibili (righe che escono dal margine).
- Verificare che la spaziatura tra sezioni sia uniforme.
