# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di riferimento e mappa ogni scheda al suo stato di verifica.

## Stato

```
Branch attivo:         main
Commit di riferimento: 828275c (2026-08-07, "Linter dei comandi: heredoc idiomatico in bash non e' un errore")
Data snapshot:         2026-08-27
```

Dal bootstrap (3485498) sono arrivati diciotto commit. Il CV è completo, trilingue e sta su una pagina sola in tutte e tre le lingue. Alla data di questo snapshot lo stato su disco era avanti rispetto al commit di riferimento: i tre gruppi di modifiche e l'ordine in cui sono stati versionati stanno in fondo a questo file.

## Stato di verifica delle schede

Tutte le schede di `.claude/context/` tracciate da git sono ora ancorate a un commit reale. Le tre che portavano ancora il segnaposto `PENDING-FIRST-COMMIT`, cioè `STACK.md`, `deployment.md` e `dev-testing.md`, sono state ancorate il 2026-08-27 come prescrive il passo 0 della skill `sync-context`.

| Scheda | last-verified | Stato |
|---|---|---|
| index.md (questo file) | 828275c | riscritto il 2026-08-27 |
| decisions.md | 828275c | verificata, nessun ADR nuovo: due note di precisazione ad ADR-001 e ADR-003 |
| progress.md | 828275c | verificata, voce nuova in testa |
| STACK.md | 828275c | riscritta: albero dei file reale, classe scelta, `.latexmkrc` vestigiale, foto sotto `attachments/` |
| deployment.md | 828275c | verificata, aggiunta la sezione su `check-skill-links` |
| dev-testing.md | 828275c | verificata, aggiunti i controlli documentali e il vincolo a una pagina |
| altacv-reference.md | 828275c | verificata, aggiunte le macro locali di collegamento e l'esito a una pagina |
| current-work.md | 828275c | riallineata: sezione di stato in testa, il resto marcato come cronologia |
| roadmap.md | 828275c | verificata, corrette Fase 2 (pagina dei progetti) e Fase 5 (numero di pagine) |
| external-links.md | aa8284d | non ancora tracciata da git, descrive già il working tree: si riancora al commit che la introdurrà |
| external-dependencies.md | aa8284d | come sopra |

## Punto di ripresa

Il CV è completo e non ha sezioni in lavorazione: struttura a due colonne su classe altaCV vendorizzata, contenuto trilingue IT/EN/ES tramite `\CVlanguage` e `\cvtext{}{}{}`, skill allineate alla tassonomia di `skills-repo` con script di verifica dei link, tre PDF stabili `cv-sopranzi-alessio-{en,it,es}.pdf` versionati in radice e sempre rigenerati insieme da `scripts/build.ps1`, più un archivio storico datato in `dated-builds/` non versionato (ADR-004, 005 e 006 in `decisions.md`). Il formato attuale è una pagina sola in tutte e tre le lingue: ogni aggiunta di contenuto va compensata con un taglio altrove, e va verificata prima sullo spagnolo, che è la lingua che sconfina per prima.

Fasi della roadmap, con il dettaglio completo in `roadmap.md`.

- Fase 1 (bootstrap tecnico): completata il 2026-07-06.
- Fase 2 (contenuti pendenti): quasi chiusa. Restano fuori "Ongoing studies", ancora disattivata con `\iffalse` e `\fi` e piena di segnaposto `aaaaaaa`, e i frammenti Coaching (Onova S.p.A. e Intracademy), rimandati per mancanza di esperienza reale da raccontare. La sezione Consultant è invece esclusa in via definitiva per motivi fiscali, non rimandata.
- Fase 3 (migrazione allegati a Proton Drive): avviata nel working tree, non ancora nel commit di riferimento. A `828275c` il sorgente ha ancora sette link Google Drive e nessun link Proton, mentre su disco tre link su dieci sono già migrati. L'inventario e la procedura stanno in `context/external-links.md`.
- Fase 4 (allineamento skill a skills-repo): in gran parte completata il 2026-07-06, con `scripts/check-skill-links.ps1` e `.sh` a verifica automatica dei link.
- Fase 5 (multilingua): completata. Traduzione integrale il 2026-07-07, bug di `\ifdefstring` non edef-safe diagnosticato e corretto con `\ifx`, verificata con build reali nelle tre lingue. Deliberatamente non fatta la revisione madrelingua dello spagnolo: resta un rischio da sciogliere prima di un uso professionale reale di quella versione.
- Fase 6 (ATS-safety del layout): rimandata a data da destinarsi come esigenza di layout. Un controllo pragmatico sul layer testuale del PDF è però stato fatto nel working tree, con `\decoicon` e le etichette esplicite di `\printinfo`, e va registrato quando quel lavoro verrà committato.

Repository correlati, tutti sotto `E:` e distinti da questo, citati dal CV: `skills-repo` (tassonomia delle competenze, pubblicata su `alesop95.github.io/skills/`), `projects` (navigator dei progetti personali e aziendali, ventinove progetti auto-scoperti), il blog personale, e `fiscal-toolkit` insieme a `legal-consultant` per il materiale fiscale e normativo. Le dipendenze verso questi siti, e cosa fare quando cambiano, stanno in `context/external-dependencies.md`.

### Lavoro versionato il 2026-08-27

Il working tree accumulato dopo `828275c` conteneva tre gruppi di modifiche distinti, separati in tre commit invece di uno solo perché rispondono a intenti diversi.

Il primo è una normalizzazione tipografica che ha toccato 36 file tracciati, circa 349 inserimenti e 332 rimozioni: accenti scritti con l'apostrofo convertiti in accenti veri, accenti mancanti ripristinati, trattini lunghi normalizzati a trattini brevi. Gli strumenti che l'hanno prodotta sono `tools/fix-accents.py`, `tools/fix-dashes.py` e `tools/fix-missing-accents.py` con la lista di esclusioni `tools/dashes-exclude.txt`, versionati nello stesso commit. Avvertenza verificata: questi strumenti non preservano la fine riga dei file su cui passano, e hanno convertito `main.tex` da LF a CRLF gonfiandone il diff da 41 righe reali a 1462. Il file è stato riportato a LF il 2026-08-27, gli strumenti non sono ancora stati corretti.

Il secondo riguarda `main.tex` nel merito, ed è il lavoro sostanziale non ancora committato: l'accessibilità del layer testuale del PDF, con il comando `\decoicon` che azzera l'`ActualText` delle icone decorative e le etichette esplicite passate a `\printinfo` per Email e Indirizzo, e la migrazione di tre link su dieci da Google Drive a Proton Drive.

Il terzo è documentale: le due schede nuove `context/external-links.md` e `context/external-dependencies.md`, l'indice di `CLAUDE.md` esteso per elencarle, e le schede riallineate dalla passata di sync del 2026-08-27, questo file compreso.

Commit e push restano manuali dell'utente, come da vincoli di team.
