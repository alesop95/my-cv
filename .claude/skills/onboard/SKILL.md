---
name: onboard
description: >
  Produce una spiegazione completa e strutturata del progetto a partire dal suo sistema di
  contesto versionato, per chi apre il progetto da zero o vi torna dopo molto tempo. Legge
  CLAUDE.md, memory/index.md, context/current-work.md, le schede di context/ e
  memory/decisions.md. E' di sola lettura: non modifica file e non esegue git.
disable-model-invocation: true
---

## Contesto git (best-effort, pre-iniettato)

!`git status --short` !`git branch --show-current` !`git log -1 --format="%h %ad %s" --date=short`

## Scopo

Questa skill da' il quadro completo del progetto a chi parte da zero. E' distinta dalla procedura di ripresa in `CLAUDE.md`, che e' veloce e mirata alla prossima azione. `onboard` invece ricostruisce l'intero quadro per chi non conosce ancora il progetto.

## Cosa legge, e in quest'ordine

1. `CLAUDE.md` di radice, che indicizza i file satellite tracciati e la procedura di ripresa.
2. `.claude/memory/index.md`, per branch, commit di riferimento, stato di verifica delle schede e prossima azione concreta.
3. `.claude/context/current-work.md`, per la sezione CV in lavorazione e le domande aperte.
4. Le schede di `.claude/context/`: `STACK.md`, `deployment.md`, `dev-testing.md`, `roadmap.md`.
5. `.claude/memory/decisions.md`, per le decisioni di layout e struttura con la loro motivazione.
6. `.claude/memory/progress.md`, per le tappe principali del work-log.

## Cosa produce

Una spiegazione discorsiva che copre: cos'e' il progetto e a cosa serve; lo stack LaTeX (distribuzione, engine, classe CV, pacchetti principali); la struttura del documento e le scelte di layout; lo stato attuale (branch, commit, sezioni complete e mancanti); le decisioni rilevanti con la motivazione; come si builda il PDF; i punti aperti. Chiude indicando la prossima azione concreta da `index.md`.

## Vincoli

Sola lettura. Non inventa: se una scheda manca o e' vuota, lo si dichiara. Se il sistema di contesto non e' presente, segnalare che il progetto non e' ancora inizializzato.
