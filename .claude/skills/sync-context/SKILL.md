---
description: >
  Verifica e sincronizza le schede tecniche in .claude/context/ con lo stato corrente del
  progetto. Confronta il last-verified-commit di ogni scheda con HEAD del branch, individua i
  file cambiati nelle covers-paths, e propone delta update mirati senza rigenerare i documenti.
  Usare a inizio sessione, dopo modifiche significative, o dopo un git pull.
---

## Stato attuale del contesto

### Commit HEAD corrente
!`git log -1 --format="%H  %h  %ad  %s" --date=short`

### Branch corrente
!`git branch --show-current`

### Commit recenti
!`git log --oneline --no-decorate -10`

### Snapshot e frontmatter delle schede
Leggere con lo strumento Read: prima `.claude/memory/index.md` (snapshot), poi i file `.claude/context/*.md` (elencabili con Glob), estraendo dal frontmatter di ciascuna scheda `last-verified-commit` e `covers-paths`.

## Istruzioni operative

Le schede tecniche tracciate vivono in `.claude/context/` e ognuna porta in testa un frontmatter con `covers-paths` e `last-verified-commit`. La skill scopre le schede da quella cartella, non da una lista fissa.

### 0. Primo ancoraggio dopo un init greenfield

Se una scheda porta `last-verified-commit` uguale al segnaposto `PENDING-FIRST-COMMIT`, e il repository ha ora almeno un commit, sostituire il segnaposto con l'hash di HEAD in tutte le schede che lo portano, aggiornare `memory/index.md`, e appendere una voce in `memory/progress.md` con data, hash e schede ancorate.

### 1. Per ogni scheda, determinare lo stato

Per ciascuna scheda presente in `.claude/context/`:

- Leggere `last-verified-commit` e `covers-paths` dal frontmatter.
- Eseguire `git diff --name-only <last-verified-commit>..HEAD -- <covers-paths>`.
- Classificare: aggiornata (nessun file coperto cambiato), stale (almeno un file cambiato), obsoleta (rename o delete di moduli interi, o la scheda cita simboli che non esistono piu').

### 2. Mostrare un report all'utente

Formato:

```
## Sync report (HEAD = abc1234 @ 2026-06-23)

| Scheda | last-verified | Stato | File toccati |
|---|---|---|---|
| STACK.md | abc1234 | aggiornata |  |
| deployment.md | abc1234 | stale | cv.tex |
```

### 3. Per ogni scheda stale, proporre il delta update

Non rigenerare il file. Leggere il diff reale, individuare la sola sezione impattata, e proporre un edit chirurgico. Non rifare la struttura della scheda.

### 4. Dopo l'edit, aggiornare frontmatter e meta-stato

Bumpare `last-verified-commit` al nuovo HEAD, aggiornare `memory/index.md`, appendere una voce in `memory/progress.md`.

### 5. Schede aggiornate

Su conferma bumpare `last-verified-commit` a HEAD come checkpoint.

## Note

Non eseguire mai `git pull` o altre operazioni di scrittura su git: la skill legge e propone soltanto. Se HEAD coincide con tutti i `last-verified-commit`, rispondere con un singolo messaggio di allineamento.
