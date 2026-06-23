# Registro delle decisioni (ADR-lite)

> Una voce per decisione rilevante. Includere contesto, opzioni valutate, scelta fatta e motivazione.

---

## ADR-001 — Engine LaTeX: pdflatex

Data: 2026-06-23

Opzioni valutate: pdflatex, lualatex, xelatex.

Scelta: pdflatex, fissato in .latexmkrc.

Motivazione: massima compatibilita' con le classi CV piu' diffuse (moderncv, europasscv) e con
TinyTeX su Windows. lualatex e xelatex sono superiori per la gestione dei font OpenType, ma
richiedono pacchetti diversi e alcune classi CV non li supportano pienamente. Se si sceglie altacv
(che preferisce lualatex), aggiornare .latexmkrc a `$pdf_mode = 4` e `$lualatex = ...`.

---

## ADR-002 — Classe CV: da scegliere

Data: 2026-06-23

Opzioni candidate: moderncv (matura, ampiamente testata, template molto usato nei portali HR),
europasscv (standard europeo, riconoscibile), altacv (piu' moderna, richiede lualatex), custom
(massima flessibilita', piu' lavoro).

Scelta: da definire nella prima sessione di lavoro.

Motivazione: la scelta della classe determina i pacchetti da aggiungere a tex-packages.txt e
l'engine (vedi ADR-001). Decidere in base all'estetica e ai contesti di utilizzo del CV (tech,
accademico, candidature europee).
