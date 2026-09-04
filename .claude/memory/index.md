# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di riferimento e mappa ogni scheda al suo stato di verifica.

## Stato

```
Branch attivo:         main
Commit di riferimento: c994a08 (2026-08-27, "Sync delle schede a 828275c e riallineamento della memoria")
Data snapshot:         2026-08-27
```

Dal bootstrap (3485498) sono arrivati ventuno commit. Il CV è completo, trilingue e sta su una pagina sola in tutte e tre le lingue. Il working tree è pulito: tutto quello che era in sospeso è stato versionato il 2026-08-27 nei tre commit descritti in fondo a questo file.

## Stato di verifica delle schede

Tutte le schede di `.claude/context/` tracciate da git sono ora ancorate a un commit reale. Le tre che portavano ancora il segnaposto `PENDING-FIRST-COMMIT`, cioè `STACK.md`, `deployment.md` e `dev-testing.md`, sono state ancorate il 2026-08-27 come prescrive il passo 0 della skill `sync-context`. Nella seconda passata dello stesso giorno tutte, comprese le due schede appena entrate in git, sono state portate a `c994a08`.

| Scheda | last-verified | Stato |
|---|---|---|
| index.md (questo file) | c994a08 | riscritto il 2026-08-27, aggiornato dopo la seconda passata |
| decisions.md | c994a08 | due note di precisazione ad ADR-001 e ADR-003, più ADR-007 sul layer testuale |
| progress.md | c994a08 | verificata, tre voci nuove in testa |
| STACK.md | 1ac5d00 | estesa con `extract-cv-links.py` e `check-links.*` |
| deployment.md | 1ac5d00 | sezione di verifica dei link riscritta su `check-links`, tutte le categorie |
| dev-testing.md | 1ac5d00 | aggiunto `extract-cv-links --check` ai controlli documentali pre-commit |
| altacv-reference.md | c994a08 | aggiunte le macro locali di collegamento, l'esito a una pagina e il layer testuale |
| current-work.md | c994a08 | riallineata: sezione di stato in testa, il resto marcato come cronologia |
| roadmap.md | 634aa6e | Fase 3 riscritta sul perimetro vero e sull'esito dei tre link Drive, Fase 4 sul checker generalizzato |
| external-links.md | 634aa6e | 52 bersagli e 67 URL generati da `extract-cv-links`, secondo salto, chiusura dei tre link Drive del CV |
| external-dependencies.md | 634aa6e | grafo generato al posto di quello scritto a mano, verifiche per dipendenza riscritte, Drive a zero nel CV |

## Punto di ripresa

Il CV è completo e non ha sezioni in lavorazione: struttura a due colonne su classe altaCV vendorizzata, contenuto trilingue IT/EN/ES tramite `\CVlanguage` e `\cvtext{}{}{}`, skill allineate alla tassonomia di `skills-repo` con script di verifica dei link, tre PDF stabili `cv-sopranzi-alessio-{en,it,es}.pdf` versionati in radice e sempre rigenerati insieme da `scripts/build.ps1`, più un archivio storico datato in `dated-builds/` non versionato (ADR-004, 005 e 006 in `decisions.md`). Il formato attuale è una pagina sola in tutte e tre le lingue: ogni aggiunta di contenuto va compensata con un taglio altrove, e va verificata prima sullo spagnolo, che è la lingua che sconfina per prima.

Fasi della roadmap, con il dettaglio completo in `roadmap.md`.

- Fase 1 (bootstrap tecnico): completata il 2026-07-06.
- Fase 2 (contenuti pendenti): quasi chiusa. Restano fuori "Ongoing studies", ancora disattivata con `\iffalse` e `\fi` e piena di segnaposto `aaaaaaa`, e i frammenti Coaching (Onova S.p.A. e Intracademy), rimandati per mancanza di esperienza reale da raccontare. La sezione Consultant è invece esclusa in via definitiva per motivi fiscali, non rimandata.
- Fase 3 (migrazione allegati a Proton Drive): tre certificati migrati con `7ea1955`, e il 2026-09-03 i tre link Google Drive che `main.tex` citava direttamente sono usciti dal sorgente senza passare da Proton, perché per tutti e tre la risposta giusta era un'altra: Stampa 3D e Bisogni Educativi Speciali sono rientrate nella convenzione delle topic page del blog, che già conteneva le loro descrizioni, e lo studio dello spagnolo punta alla pagina del repository `spanish-learning`. `main.tex` non contiene più alcun link a Google Drive. Restano undici asset Drive nel perimetro, cioè nove nelle pagine del repository `projects` e due dietro i redirect di tesi, questi ultimi da sostituire con link Proton diretti ritirando i redirect. Inventario e precedente in `context/external-links.md`.
- Fase 4 (allineamento skill a skills-repo): in gran parte completata il 2026-07-06. La verifica automatica dei link, nata come `check-skill-links` sui soli cinque link di `skills-repo`, è stata generalizzata il 2026-09-03 in `scripts/check-links.ps1` e `.sh` su tutte le categorie, con seguito dei redirect.
- Fase 5 (multilingua): completata. Traduzione integrale il 2026-07-07, bug di `\ifdefstring` non edef-safe diagnosticato e corretto con `\ifx`, verificata con build reali nelle tre lingue. Deliberatamente non fatta la revisione madrelingua dello spagnolo: resta un rischio da sciogliere prima di un uso professionale reale di quella versione.
- Fase 6 (ATS-safety del layout): rimandata a data da destinarsi per quel che riguarda l'ordine di lettura delle colonne. Il problema distinto del layer testuale del PDF è invece risolto e versionato con `7ea1955`, con `\decoicon` e le etichette esplicite di `\printinfo`: motivazione in ADR-007, dettagli tecnici in `context/altacv-reference.md`.

Repository correlati, tutti sotto `E:` e distinti da questo, citati dal CV: `skills-repo` (tassonomia delle competenze, pubblicata su `alesop95.github.io/skills/`), `projects` (navigator dei progetti personali e aziendali, ventinove progetti auto-scoperti), il blog personale, e `fiscal-toolkit` insieme a `legal-consultant` per il materiale fiscale e normativo. Le dipendenze verso questi siti, e cosa fare quando cambiano, stanno in `context/external-dependencies.md`.

### Lavoro versionato il 2026-08-27

Il working tree accumulato dopo `828275c` conteneva tre gruppi di modifiche distinti, separati in tre commit invece di uno solo perché rispondono a intenti diversi.

Il primo è una normalizzazione tipografica che ha toccato 36 file tracciati, circa 349 inserimenti e 332 rimozioni: accenti scritti con l'apostrofo convertiti in accenti veri, accenti mancanti ripristinati, trattini lunghi normalizzati a trattini brevi. Gli strumenti che l'hanno prodotta sono `tools/fix-accents.py`, `tools/fix-dashes.py` e `tools/fix-missing-accents.py` con la lista di esclusioni `tools/dashes-exclude.txt`, versionati nello stesso commit. Avvertenza verificata: questi strumenti non preservano la fine riga dei file su cui passano, e hanno convertito `main.tex` da LF a CRLF gonfiandone il diff da 41 righe reali a 1462. Il file è stato riportato a LF il 2026-08-27, gli strumenti non sono ancora stati corretti.

Il secondo riguarda `main.tex` nel merito, ed è il lavoro sostanziale non ancora committato: l'accessibilità del layer testuale del PDF, con il comando `\decoicon` che azzera l'`ActualText` delle icone decorative e le etichette esplicite passate a `\printinfo` per Email e Indirizzo, e la migrazione di tre link su dieci da Google Drive a Proton Drive.

Il terzo è documentale: le due schede nuove `context/external-links.md` e `context/external-dependencies.md`, l'indice di `CLAUDE.md` esteso per elencarle, e le schede riallineate dalla passata di sync del 2026-08-27, questo file compreso.

Dopo quei tre commit è stata eseguita una seconda passata di `sync-context`, che ha riportato tutte le schede a `c994a08`, riancorato le due appena entrate in git, recepito la migrazione Proton nella Fase 3, registrato ADR-007 sul layer testuale del PDF ed esteso l'indice di `CLAUDE.md` con la sezione `tools/`. Quel lavoro è nel working tree e attende un quarto commit.

Commit e push restano manuali dell'utente, come da vincoli di team.
