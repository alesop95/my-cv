# Work-log (append-only, ordine cronologico inverso)

> Aggiungere voci in testa. Non modificare voci esistenti.

---

## 2026-07-08 — main.pdf sostituito da tre PDF stabili per lingua (ADR-006)

`main.pdf` eliminato dalla radice del progetto insieme ai suoi ausiliari. Sostituito da `cv-sopranzi-alessio-en.pdf`, `cv-sopranzi-alessio-it.pdf`, `cv-sopranzi-alessio-es.pdf`, tutti e tre versionati in git e sempre rigenerati insieme. Motivazione: l'unico riferimento stabile versionato era in inglese (default di `\CVlanguage`), le versioni italiana e spagnola esistevano solo come istantanee datate non versionate in `dated-builds/` (ADR-005), mai garantite allineate al contenuto corrente. Riscritti `scripts/build.ps1` e `.sh`: non usano piu' latexmk ne' compilano una sola lingua di default, compilano sempre le tre lingue con pdflatex diretto (stessa tecnica di `build-multilang.ps1`/`.sh`, che restano invariati per l'archivio datato separato). Root del progetto ripulita da 12 file ausiliari sparsi lasciati da esecuzioni precedenti di `build-multilang` (bug: spostava solo il `.pdf` nella sottocartella di lingua, non gli ausiliari; corretto). Dettagli completi in ADR-006 (`memory/decisions.md`); schede aggiornate di conseguenza: `context/deployment.md`, `context/dev-testing.md`, `context/roadmap.md`, `context/current-work.md`.

Nella stessa sessione, non ancora loggate qui in dettaglio: icona footer del blog cambiata da `\faRss` a `\faBlog` (piu' pertinente), aggiunto footer con icone social (LinkedIn/GitHub/Telegram/ email) sia su questo repository sia su `E:\skills`, corrette le date di inizio dei progetti aziendali nel navigator `E:\projects` su indicazione dell'utente, uniformati i trattini doppi a singoli in tutto `E:\projects`.

---

## 2026-06-23 — Setup iniziale del progetto

Inizializzato il progetto my-cv con il template di sviluppo standard. Creati: struttura .claude/ (rules, agents, skills, memory, context), scripts LaTeX (build.ps1/sh, setup-tex.ps1/sh), .latexmkrc, tex-packages.txt, tools/latest-screenshot.ps1. Il progetto e' vuoto: nessun file .tex ancora presente. Prossimo passo: scegliere la classe CV e creare cv.tex.
