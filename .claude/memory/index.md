# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di
> riferimento e mappa ogni scheda al suo stato di verifica.

## Stato

```
Branch attivo:         main
Commit di riferimento: 3485498 (2026-07-06, bootstrap del template)
Data snapshot:         2026-07-08
```

Nessun commit e' stato fatto da 3485498 in poi: tutto il lavoro descritto in questo file (CV
completo e trilingue, riorganizzazione dell'output PDF, scheda di ogni fase della roadmap) vive
ancora nel working tree, non versionato. Vedi "Da committare" in fondo per l'elenco.

## Stato di verifica delle schede

Nessuna scheda e' ancora ancorabile a un commit reale (nulla e' stato committato dal bootstrap):
"verificata" qui significa riletta e allineata al working tree attuale il 2026-07-08, non a un
commit.

| Scheda | last-verified | Stato |
|---|---|---|
| index.md (questo file) | working tree 2026-07-08 | riallineato allo stato reale |
| decisions.md | working tree 2026-07-08 | verificata (ADR-006 aggiunta) |
| progress.md | working tree 2026-07-08 | verificata (nuova voce in testa) |
| roadmap.md | working tree 2026-07-08 | verificata parzialmente (vedi nota sotto) |
| current-work.md | working tree 2026-07-08 | verificata |
| deployment.md | working tree 2026-07-08 | verificata (riscritta) |
| dev-testing.md | working tree 2026-07-08 | verificata (riscritta) |
| STACK.md | working tree 2026-07-08 | verificata parzialmente (riga build corretta, resto della scheda ancora generico/mai popolato: cita ancora `cv.tex`/`sections/`/`assets/` che non esistono in questo progetto) |
| altacv-reference.md | 3485498 (2026-07-06) | non riverificata in questa sessione, nessun segnale di drift noto |

Nota su roadmap.md: la Fase 2 contiene ancora una shortlist di 8 progetti candidati per "un'eventuale
pagina web statica dedicata ai progetti... da costruire come attivita' separata e successiva" —
questa pagina e' stata nel frattempo effettivamente costruita, ma come repository a se stante
(`E:\projects`, non parte di questo repository), con una copertura molto piu' ampia (29 progetti
personali auto-scoperti da GitHub, non la shortlist di 8). La sezione non e' stata riscritta in
questo passaggio per restare nello scope richiesto (riallineare `index.md`); da aggiornare quando
si tocca `roadmap.md` di nuovo.

## Punto di ripresa

Il CV e' sostanzialmente completo nel suo stato attuale: struttura a due colonne su classe altaCV
vendorizzata, contenuto trilingue (IT/EN/ES) tramite `\CVlanguage`/`\cvtext{}{}{}`, skill allineate
alla tassonomia di `skills-repo` con script di verifica link, e un'architettura di output PDF
ridisegnata due volte (vedi ADR-004, 005, 006 in `decisions.md`) fino all'assetto attuale: tre PDF
stabili `cv-sopranzi-alessio-{en,it,es}.pdf` versionati in root, sempre rigenerati insieme da
`scripts/build.ps1`, piu' un archivio storico datato separato in `dated-builds/` (non versionato).

Fasi della roadmap (dettaglio completo in `roadmap.md`):

- Fase 1 (bootstrap tecnico): completata il 2026-07-06.
- Fase 2 (contenuti pendenti): in gran parte fatta (placeholder di "Work experience" rimossi,
  link ad "Academic projects" e "Acting/Theatre" popolati, "Private projects" riscritta come lista
  sintetica). Restano aperti, deliberatamente rimandati o non ancora affrontati: i due frammenti
  Coaching (Onova S.p.A. / Intracademy) e Consultant (rimandati esplicitamente, manca esperienza
  reale da raccontare), l'intera sezione "Ongoing studies" (ancora segnaposto `........`/`aaaaaaa`).
- Fase 3 (migrazione allegati a Proton Drive): non affrontata, indipendente dal codice LaTeX,
  da fare sostituendo i link uno alla volta quando si riprende.
- Fase 4 (allineamento skill a skills-repo): in gran parte completata il 2026-07-06, con
  `scripts/check-skill-links.ps1`/`.sh` a verifica automatica dei link (23/23 raggiungibili
  all'ultima verifica).
- Fase 5 (multilingua): completata. Traduzione integrale eseguita il 2026-07-07, bug di
  `\ifdefstring` non edef-safe diagnosticato e corretto (sostituito con `\ifx`), verificata con
  build reale nelle tre lingue. Deliberatamente non fatto: revisione madrelingua dello spagnolo
  (rischio da valutare prima di un uso professionale reale della versione ES).
- Fase 6 (ATS-safety): rimandata esplicitamente a data da destinarsi, non e' un'esigenza attiva
  secondo l'utente.

Lavoro correlato svolto nella stessa sessione ma in repository distinti, per contesto: un
navigator dei progetti personali e aziendali (`E:\projects`, MkDocs, palette del CV, trilingue,
non ancora inizializzato a git dall'utente) e un footer con icone social (LinkedIn/GitHub/
Telegram/email) aggiunto sia li' sia a `E:\skills`. Nel CV stesso e' stato aggiunto un link al
blog personale (`\faBlog`, campo `\blog{}` in `main.tex`) vicino ai riferimenti di contatto.

Aggiornamento del 2026-07-10: nuovo repository esterno `E:\fiscal-toolkit` (remoto
`github.com/alesop95/fiscal-toolkit`, identita' e remoto git gia' configurati, commit iniziale
non ancora fatto dall'utente), nato da una ricognizione del materiale fiscale/consulenza
dell'utente (dettagli non pubblici in `_notes/consulting-and-fiscal-tracking-2026-07-10.md`).
Collegato concettualmente a `E:\legal-consultant` per gli aggiornamenti normativi. Nessuna
sezione "Consultant" e' stata aggiunta al CV: la decisione e' di escluderla in modo definitivo
per motivi fiscali attuali, non solo di rimandarla (vedi `roadmap.md`, Fase 2). Scartata anche
l'idea di uno scraper per le offerte LinkedIn dopo una ricerca sui rischi legali/di ban: si
useranno i Job Alert nativi di LinkedIn e l'API pubblica di Adzuna.

### Da committare

Nulla di quanto sopra e' stato ancora versionato: dal bootstrap (3485498) il repository ha
accumulato modifiche a `main.tex` (intero contenuto trilingue), `altacv.cls` (patch
`\cvachievement`), tutti gli script di build (riscritti per ADR-006, piu' `build-multilang.*` e
`check-skill-links.*` nuovi), `.gitignore`, `.latexmkrc`, `CLAUDE.md`, tutte le schede
`.claude/context/*` e `.claude/memory/*`, e i tre PDF stabili in root. Prossimo passo pratico:
revisione e commit manuale (a cura dell'utente, come da vincoli di team), presumibilmente in piu'
commit logici invece di uno solo, prima di riprendere il backlog di contenuti Fase 2/3.
