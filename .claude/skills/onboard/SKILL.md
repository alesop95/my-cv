---
name: onboard
description: >
  Produce una spiegazione completa e strutturata del progetto a partire dal suo sistema di
  contesto versionato, per chi apre il progetto da zero o vi torna dopo molto tempo. Legge
  CLAUDE.md, memory/index.md, context/current-work.md, le schede di context/ e
  memory/decisions.md. È di sola lettura: non modifica file e non esegue git.
disable-model-invocation: true
---

## Contesto git (best-effort, pre-iniettato)

!`git status --short` !`git branch --show-current` !`git log -1 --format="%h %ad %s" --date=short`

Se la cartella non è ancora un repository git, questi comandi stampano un errore "not a git repository": il progetto non è ancora versionato, e l'onboarding si limita a ciò che le schede documentano.

## Scopo

Questa skill dà il quadro completo del progetto a chi parte da zero. È distinta dalla procedura di ripresa in `CLAUDE.md` e nella sezione 12 di `.claude/PROJECT-SYSTEM.md`, che è veloce e mirata alla prossima azione e serve a chi sta già lavorando al progetto; per sapere che cosa resta da fare la risposta misurata è `/roadmap`. `onboard` invece ricostruisce l'intero quadro per chi non conosce ancora il progetto.

## Cosa legge, e in quest'ordine

1. `CLAUDE.md` di radice, che indicizza i file satellite tracciati e la procedura di ripresa.
2. `.claude/memory/index.md`, per branch, commit di riferimento, stato di verifica delle schede e prossima azione concreta.
3. `.claude/context/current-work.md`, per la sezione CV in lavorazione e le domande aperte.
4. Le schede di `.claude/context/`, elencate con Glob invece che da una lista fissa: oggi `STACK.md`, `altacv-reference.md`, `architecture.md`, `deployment.md`, `dev-testing.md`, `external-dependencies.md`, `external-links.md` e `roadmap.md`, oltre a `current-work.md` già letta al punto 3.
5. `.claude/memory/decisions.md`, per le decisioni di layout e struttura con la loro motivazione.
6. `.claude/memory/progress.md`, per le tappe principali del work-log.

Il materiale privato sotto `_notes/` non si legge, salvo richiesta esplicita dell'utente.

## Cosa produce

Una spiegazione discorsiva che copre: cos'è il progetto e a cosa serve; lo stack LaTeX (distribuzione, engine, classe CV, pacchetti principali); la struttura del documento e le scelte di layout; lo stato attuale (branch, commit, sezioni complete e mancanti); le decisioni rilevanti con la motivazione; come si builda il PDF; i punti aperti. Chiude indicando la prossima azione concreta da `index.md`.

Se l'utente indica un taglio, ad esempio solo la build o solo l'ecosistema dei siti collegati, si apre per esteso la scheda pertinente e si riassume il resto, per non bruciare contesto inutilmente.

## Vincoli

Sola lettura: non modifica file e non esegue mai `git add`, `commit` o `push`. Non inventa: se una scheda manca o è vuota, lo si dichiara. Se il sistema di contesto non è presente, segnalare che il progetto non è ancora inizializzato.
