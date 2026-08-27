# Work-log (append-only, ordine cronologico inverso)

> Aggiungere voci in testa. Non modificare voci esistenti.

---

## 2026-08-27 - Passata di sync-context: schede riancorate a 828275c

Eseguita la skill `sync-context` contro HEAD `828275c`. Tutte e sei le schede tracciate risultavano fuori allineamento, tre di esse (`STACK.md`, `deployment.md`, `dev-testing.md`) ancora sul segnaposto `PENDING-FIRST-COMMIT` nonostante diciotto commit dal bootstrap: applicato il passo 0 della skill e ancorate a `828275c`, insieme alle altre tre.

Prima di ogni edit, correzione di un problema meccanico: `main.tex` era l'unico file tracciato del repository con fini riga CRLF, convertito da LF dalla passata di normalizzazione tipografica in corso nel working tree. Il suo diff risultava di 1462 righe cambiate invece delle 41 reali, mascherando le modifiche vere. Riportato a LF senza toccare il contenuto, verificato che `git diff --stat HEAD` e `git diff --stat --ignore-cr-at-eol HEAD` coincidano. La causa a monte non è stata corretta: `tools/fix-accents.py`, `tools/fix-dashes.py` e `tools/fix-missing-accents.py` riscrivono i file senza preservare la fine riga originale, e resta un intervento da fare.

Delta applicati alle schede. `STACK.md` era la più fuori asse ed è stata riscritta: descriveva un albero `cv.tex`, `sections/`, `assets/` mai esistito in questo progetto e dichiarava la classe CV ancora "da scegliere" nonostante ADR-002. Il nuovo testo riporta l'albero reale, registra che `.latexmkrc` è ormai vestigiale (nessuno script lo invoca dal 2026-07-08), e documenta un fatto architetturale prima non scritto da nessuna parte: la foto della testata sta sotto `attachments/`, ignorato da git per ADR-003, quindi un clone pulito del repository non compila finché quel file non viene rimesso a mano. `deployment.md` è risultata corretta nel merito e ha ricevuto solo la sezione mancante su `scripts/check-skill-links.ps1`, che era dentro i suoi `covers-paths` ma documentato solo nella roadmap. `dev-testing.md` ha guadagnato i controlli documentali pre-commit (`md-unwrap.py --check` e `lint-md-commands.py`), l'avvertenza sulle fini riga, e il vincolo di formato a una pagina nella checklist pre-distribuzione. `altacv-reference.md` non nominava le macro locali di collegamento: aggiunta una sezione su `\NewInfoField` per `blog`, `projectsSite` e `githubCorp` e su `\bloglinkwrap`, con il vincolo tecnico per cui la scelta fra i due URL deve avvenire prima di chiamare `\href` e non dentro il suo argomento; registrato anche che `\bloglink` è codice morto, definito ma mai chiamato dopo il passaggio a `\bloglinkwrap`. `current-work.md` presentava come lavoro attivo la cronaca di cinque revisioni grafiche del 2026-07-06 e ripeteva cinque volte "3 pagine": aggiunta una sezione di stato in testa e marcato il resto come cronologia archiviata, rimossa la sezione sull'infrastruttura multilingua "non ancora scritta" che citava `\ifCVitalian`, macro non più esistente. `roadmap.md` ha ricevuto due correzioni di fatto: la pagina dei progetti della Fase 2 è stata costruita davvero, come repository separato e su ventinove progetti invece degli otto della shortlist, e l'esito della Fase 5 non è più tre pagine ma una.

Riscritto `memory/index.md`, che era il file più sbagliato del progetto: dichiarava testualmente che nessun commit era stato fatto dal bootstrap e che tutto il lavoro viveva nel working tree, con una sezione "Da committare" che elencava come pendente materiale versionato da mesi.

Non fatto in questa passata, deliberatamente: `context/external-links.md` e `context/external-dependencies.md` restano ancorate ad `aa8284d` perché non sono ancora tracciate da git e descrivono già il working tree, quindi si riancorano al commit che le introdurrà. In `decisions.md` nessun ADR nuovo, solo due note di precisazione datate: ad ADR-001, perché la frase "fissato in .latexmkrc" non descrive più il meccanismo reale, e ad ADR-003, perché la foto citata non è più quella in uso. Quello sull'accessibilità del layer testuale del PDF (`\decoicon`, `ActualText` vuoto, etichette esplicite di `\printinfo`) va scritto quando quel lavoro sarà committato.

---

## 2026-08-27 - Recupero del work-log fra il 2026-07-08 e il 2026-08-07

Voce retrospettiva, scritta per colmare un buco: l'ultima voce reale era del 2026-07-08 e nel frattempo sono arrivati diciotto commit dal bootstrap, nessuno dei quali loggato qui. Ricostruzione dai soli messaggi di commit e dal diff, non da memoria di sessione.

Il CV è entrato in git per davvero l'8 luglio, con `dd35523` che porta la struttura altaCV e il contenuto trilingue, seguito dagli script di build trilingue, dall'archivio datato, dalla verifica dei link skill e dai tre PDF compilati. Da lì il lavoro è stato quasi tutto di compattazione: `07921cc` scende a due pagine tagliando contenuto e correggendo un overflow di paracol, `68d853c` compatta ancora e collega le voci della sezione Interessi alle topic page del blog tramite `\bloglinkwrap`, `aef38eb` porta l'italiano a una pagina sola rifinendo contenuti e link, `aa8284d` allinea inglese e spagnolo allo stesso formato. In mezzo, la foto della testata sostituita con uno scatto nuovo e la decisione, registrata in `roadmap.md` con `b81af63`, di lasciare "Ongoing studies" disattivata trattandola come contenuto sempre disponibile invece che come item scaduto.

Due commit del 10 luglio (`170111a` e `e0a3cb0`) registrano lavoro fatto fuori da questo repository: la nascita di `E:\fiscal-toolkit` e lo scarto motivato di uno scraper per le offerte LinkedIn, sostituito dai Job Alert nativi e dall'API pubblica di Adzuna.

Gli ultimi quattro commit, fra il 6 e il 7 agosto, non toccano il CV ma la disciplina documentale del repository: `ad1f46a` introduce la convenzione dei paragrafi su una riga sorgente continua, `15949be` la propaga insieme agli strumenti di verifica, e `163ea16` con `828275c` raffinano il linter dei comandi togliendo due falsi positivi, il backslash finale e l'heredoc idiomatico in bash.

---

## 2026-07-08 - main.pdf sostituito da tre PDF stabili per lingua (ADR-006)

`main.pdf` eliminato dalla radice del progetto insieme ai suoi ausiliari. Sostituito da `cv-sopranzi-alessio-en.pdf`, `cv-sopranzi-alessio-it.pdf`, `cv-sopranzi-alessio-es.pdf`, tutti e tre versionati in git e sempre rigenerati insieme. Motivazione: l'unico riferimento stabile versionato era in inglese (default di `\CVlanguage`), le versioni italiana e spagnola esistevano solo come istantanee datate non versionate in `dated-builds/` (ADR-005), mai garantite allineate al contenuto corrente. Riscritti `scripts/build.ps1` e `.sh`: non usano più latexmk né compilano una sola lingua di default, compilano sempre le tre lingue con pdflatex diretto (stessa tecnica di `build-multilang.ps1`/`.sh`, che restano invariati per l'archivio datato separato). Root del progetto ripulita da 12 file ausiliari sparsi lasciati da esecuzioni precedenti di `build-multilang` (bug: spostava solo il `.pdf` nella sottocartella di lingua, non gli ausiliari; corretto). Dettagli completi in ADR-006 (`memory/decisions.md`); schede aggiornate di conseguenza: `context/deployment.md`, `context/dev-testing.md`, `context/roadmap.md`, `context/current-work.md`.

Nella stessa sessione, non ancora loggate qui in dettaglio: icona footer del blog cambiata da `\faRss` a `\faBlog` (più pertinente), aggiunto footer con icone social (LinkedIn/GitHub/Telegram/ email) sia su questo repository sia su `E:\skills`, corrette le date di inizio dei progetti aziendali nel navigator `E:\projects` su indicazione dell'utente, uniformati i trattini doppi a singoli in tutto `E:\projects`.

---

## 2026-06-23 - Setup iniziale del progetto

Inizializzato il progetto my-cv con il template di sviluppo standard. Creati: struttura .claude/ (rules, agents, skills, memory, context), scripts LaTeX (build.ps1/sh, setup-tex.ps1/sh), .latexmkrc, tex-packages.txt, tools/latest-screenshot.ps1. Il progetto è vuoto: nessun file .tex ancora presente. Prossimo passo: scegliere la classe CV e creare cv.tex.
