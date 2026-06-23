---
generated-from-commit: PENDING-FIRST-COMMIT
generated-from-branch: main
generated-date: 2026-06-23
covers-paths:
  - "*.tex"
  - "sections/**"
last-verified-commit: PENDING-FIRST-COMMIT
---

# Roadmap e priorita'

## Fase 1 — Bootstrap (corrente)

- Scegliere la classe LaTeX (ADR-002 in `memory/decisions.md`).
- Aggiungere la classe a `tex-packages.txt` e fare il primo `setup-tex.ps1`.
- Creare `cv.tex` con il preambolo e le sezioni vuote.
- Verificare che la build produca un PDF senza errori.

## Fase 2 — Contenuto iniziale

- Popolare le sezioni: informazioni personali, istruzione (triennale + magistrale), esperienza
  lavorativa, competenze IT (allineate alla tassonomia skills-repo), lingue.
- Aggiungere i progetti universitari (tesi magistrale, tesi triennale, harmonic-tension-vst3,
  gesture_glove_harmonizer) nella sezione progetti.

## Fase 3 — Rifinitura

- Ottimizzare il layout (margini, spaziatura, font, colori).
- Verificare tutti i link ipertestuali (GitHub, portfolio, LinkedIn se presente).
- Produrre il PDF finale e decidere se versionarlo.

## Note di direzione

Il CV e' sia un documento tradizionale (PDF per invio diretto) sia un pezzo del portfolio
pubblico. Il grafo delle skill a `alesop95.github.io/skills/graphify-out/graph.html` e' il
complemento interattivo: il CV dichiara le competenze, il grafo le contestualizza con le relazioni
semantiche e i progetti che le evidenziano.
