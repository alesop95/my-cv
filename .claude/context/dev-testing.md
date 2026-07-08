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

1. Modificare `main.tex`.
2. Compilare: `scripts\build.ps1` (ADR-006: compila sempre tutte e tre le lingue in un colpo solo,
   sovrascrivendo `cv-sopranzi-alessio-{en,it,es}.pdf` nella radice; non esiste piu' una build a
   lingua singola separata).
3. Aprire uno dei tre PDF con il visualizzatore preferito (SumatraPDF su Windows e' comodo perche'
   ricarica automaticamente il file alla ricompilazione).
4. Verificare layout, spaziatura, link cliccabili, encoding dei caratteri accentati, e che il
   contenuto `\cvtext{}{}{}` sia coerente tra le tre lingue.

## Errori di compilazione

`scripts/build.ps1` compila con pdflatex direttamente (non latexmk, dal 2026-07-08): l'errore
compare nell'output del comando con il numero di riga, oppure nel file
`cv-sopranzi-alessio-<lingua>.log` della lingua che ha fallito. Cercare la prima riga che inizia
con `!`. Se un pacchetto non e' trovato, il messaggio indica il file `.sty` mancante: aggiungere il
pacchetto a `tex-packages.txt` e rieseguire il setup.

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
