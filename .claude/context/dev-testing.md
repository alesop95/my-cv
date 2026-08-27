---
generated-from-commit: 828275c
generated-from-branch: main
generated-date: 2026-06-23
covers-paths:
  - "main.tex"
  - "tools/**"
last-verified-commit: 828275c
---

# Revisione e verifica del documento

## Ciclo di sviluppo tipico

Il ciclo è modifica-compila-leggi. Non esiste una test suite automatizzata: la verifica è visiva sul PDF prodotto.

1. Modificare `main.tex`.
2. Compilare: `scripts\build.ps1` (ADR-006: compila sempre tutte e tre le lingue in un colpo solo, sovrascrivendo `cv-sopranzi-alessio-{en,it,es}.pdf` nella radice; non esiste più una build a lingua singola separata).
3. Aprire uno dei tre PDF con il visualizzatore preferito (SumatraPDF su Windows è comodo perché ricarica automaticamente il file alla ricompilazione).
4. Verificare layout, spaziatura, link cliccabili, encoding dei caratteri accentati, e che il contenuto `\cvtext{}{}{}` sia coerente tra le tre lingue.

## Errori di compilazione

`scripts/build.ps1` compila con pdflatex direttamente (non latexmk, dal 2026-07-08): l'errore compare nell'output del comando con il numero di riga, oppure nel file `cv-sopranzi-alessio-<lingua>.log` della lingua che ha fallito. Cercare la prima riga che inizia con `!`. Se un pacchetto non è trovato, il messaggio indica il file `.sty` mancante: aggiungere il pacchetto a `tex-packages.txt` e rieseguire il setup.

## Revisione del contenuto

La tassonomia delle competenze in `skills-repo` è la fonte di verità per i nomi delle skill incluse nel CV. Prima di aggiungere o rimuovere una competenza, verificare come è denominata nel sito `alesop95.github.io/skills/` o nel grafo `graphify-out/graph.html`.

## Verifica visiva pre-distribuzione

Prima di inviare il PDF a un recruiter o di pubblicarlo:
- Verificare che tutti i link siano cliccabili e puntino agli URL giusti.
- Verificare che i dati di contatto siano presenti e corretti.
- Verificare che non ci siano overfull hbox visibili (righe che escono dal margine).
- Verificare che la spaziatura tra sezioni sia uniforme.
- Verificare che il documento stia ancora su una pagina sola in tutte e tre le lingue, non solo in inglese: è il formato raggiunto con i commit `07921cc`, `aef38eb` e `aa8284d`, e lo spagnolo, naturalmente più lungo, è la lingua che sconfina per prima.

## Controlli documentali prima di un commit

La verifica non riguarda solo il PDF. Le schede di contesto, le regole e le skill di questo repository seguono due convenzioni vincolanti che hanno uno strumento di controllo ciascuna, ed entrambi vanno eseguiti prima di un commit che tocca file `.md`.

```
python tools/md-unwrap.py --check .
python tools/lint-md-commands.py
```

Il primo applica la convenzione di `interaction-style.md`, cioè un paragrafo di prosa su una riga sorgente unica, ed esce con codice diverso da zero se qualche file non la rispetta. Il secondo applica `git-commands-format.md` percorrendo i blocchi di shell dei file Markdown e segnalando continuazioni di riga, heredoc e comandi git che proseguono sulla riga seguente: serve proprio perché md-unwrap per contratto non tocca il contenuto dei blocchi recintati, quindi un comando spezzato dentro un blocco di codice non lo corregge nessun altro.

Una nota che vale come avvertenza operativa: gli strumenti di normalizzazione tipografica sotto `tools/` riscrivono i file su cui passano, e almeno una volta hanno convertito le fini riga di `main.tex` da LF a CRLF, gonfiando il suo diff da 41 righe reali a 1462. Dopo una passata di normalizzazione conviene controllare con `git diff --stat HEAD` che il numero di righe cambiate sia plausibile, e confrontarlo con `git diff --stat --ignore-cr-at-eol HEAD`: se i due numeri divergono, il file ha cambiato fine riga e va riportato a LF prima del commit.
