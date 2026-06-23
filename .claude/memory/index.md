# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di
> riferimento e mappa ogni scheda al suo stato di verifica.

## Stato

```
Branch attivo:         main
Commit di riferimento: PENDING-FIRST-CONTENT-COMMIT
Data snapshot:         2026-06-23
```

## Stato di verifica delle schede

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | PENDING-FIRST-COMMIT | da ancorare |
| deployment.md | PENDING-FIRST-COMMIT | da ancorare |
| dev-testing.md | PENDING-FIRST-COMMIT | da ancorare |
| current-work.md | PENDING-FIRST-COMMIT | da ancorare |
| roadmap.md | PENDING-FIRST-COMMIT | da ancorare |

## Punto di ripresa

Scegliere la classe LaTeX per il CV (moderncv, europasscv, altacv o custom), aggiungerne il
pacchetto a tex-packages.txt, creare cv.tex con la struttura iniziale, e fare la prima build
con scripts/setup-tex.ps1 poi scripts/build.ps1.
