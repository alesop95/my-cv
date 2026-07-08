---
generated-from-commit: 3485498
generated-from-branch: main
generated-date: 2026-07-06
covers-paths:
  - "*.tex"
  - "sections/**"
last-verified-commit: 3485498
---

# Roadmap e priorita'

> Riscritta il 2026-07-06 a partire dal contenuto reale delle quattro note di analisi trovate in
> `[TBC]_DA SISTEMARE, LATEX, VARIE, PENDING/` (ora archiviate in
> `_notes/tbc-archive/da-sistemare/`), non dai soli titoli dei file. Le fasi sotto sono ordinate
> per dipendenza, non per urgenza uniforme: la Fase 1 blocca tutte le altre, le Fasi 3-6 sono
> indipendenti tra loro e si possono affrontare in qualunque ordine dopo la Fase 2.

## Fase 1 — Bootstrap tecnico (completata il 2026-07-06)

- ADR-002 e' chiusa: la classe e' altaCV, gia' operativa in `main.tex` fornito come punto di
  partenza.
- `tex-packages.txt` e' completo e la prima build reale e' andata a buon fine: `main.pdf` si
  genera in 4 pagine con solo warning cosmetici (font shape sostituito per il grassetto
  maiuscoletto di Lato, link vuoti sui due segnaposto di Fase 2). ADR-001 (pdflatex) confermata:
  il fallback `\iftutex` funziona come previsto, nessun cambio di motore necessario.
- Scoperta operativa non anticipabile dalla sola lettura del preambolo: `altacv.cls` non e' un
  pacchetto CTAN/tlmgr, e' distribuito solo su GitHub (`liantze/AltaCV`, licenza LPPL). E'
  vendorizzato nella root del progetto come `altacv.cls`, tracciato in git, fonte confermata
  dall'utente il 2026-07-06 (vedi `tex-packages.txt` per l'URL esatto). Inoltre altacv.cls e le
  sue dipendenze dirette (`pdfx`, `dashrule`, `tcolorbox` con la libreria skins, i font
  `roboto`/`lato`) portano una lunga catena di dipendenze transitive non elencate nella
  documentazione della classe, scoperte una per una per iterazione build-fallisce/leggi
  errore/installa: `extsizes`, `everyshi`, `colorprofiles`, `xmpincl`, `cmap`, `ragged2e`,
  `tikzfill`, `ifmtarg`, `fontaxes`, oltre a `adjustbox` (che fornisce `trimclip.sty` sotto un
  nome pacchetto diverso dal file). Tutte documentate con il relativo motivo direttamente come
  commento in `tex-packages.txt`: su una macchina nuova, `scripts/setup-tex.ps1` le installa
  tutte in un solo passaggio, senza dover ripetere la scoperta.
- Un secondo problema reale, non di pacchetti ma di sintassi, e' stato trovato e corretto in
  `main.tex`: nella sezione "Courses and Events" un gruppo `{` aperto per racchiudere due coppie
  `\cvevent`/`itemize` non veniva mai chiuso prima di `\end{cveventblock}`, con conseguente
  "Missing } inserted" fatale. Corretto aggiungendo la `}` mancante.

## Fase 2 — Completamento dei contenuti pendenti (in corso)

`main.tex` contiene gia' la struttura completa del CV, ma con segnaposto ancora da scrivere.
Stato aggiornato al 2026-07-06:

- Risolto: le quattro righe segnaposto in "Work experience" (Intrawelt) — `\textsc{Entrepreneurship
  and technical leading}`, `\textsc{Full-stack development and devOps (SaaS)}`, "[TBC] Data
  management, analytics & reporting", "[TBC] IT service design and user experience" — sono state
  rimosse su richiesta esplicita dell'utente, da ripopolare in una sessione futura quando ci sara'
  contenuto reale per ciascuna.
- Risolto: "Developing app for listening test" (Academic projects) ora linka
  `github.com/alesop95/feature-based_characterization_loudspeakers`, la GUI MATLAB per il test
  d'ascolto sviluppata per la stessa tesi magistrale gia' citata in Education.
- Risolto: "Acting, Theatre, Performing arts" (Courses and Events) aggiornata con il link allo
  spettacolo teatrale conclusivo e la partecipazione come narratore in "Callaghan" (35 minuti);
  date corrette da "01/2026 -- ongoing" a "01/2026 -- 07/2026".
- Rimandato su richiesta esplicita dell'utente: i due frammenti Coaching (Onova S.p.A. /
  Intracademy) e Consultant, recuperati da `_notes/tbc-archive/da-sistemare/`, restano
  nell'archivio e non vengono integrati in `main.tex`. Motivazione dichiarata: non e' ancora
  stata svolta ne' consulenza ne' coaching in forma formale, quindi il contenuto sarebbe
  prematuro.
- Risolto: "Private projects/applications" riscritta come lista sintetica raggruppata per area
  tematica (infrastruttura/self-hosting, AI e automazione, web app, audio/hardware, strumenti
  dati personali) invece di un bullet per singolo progetto, dopo una ricognizione di ~25
  cartelle progetto sotto `E:\`. Esclusi esplicitamente dalla lista: `app-cross-training`,
  `totocalcio`, `serp.systems-full-early_mvp` (dichiarati dai rispettivi README "nessuna
  implementazione ancora", solo idee/appunti); `civitanext` e `discoteca-api` (stadio
  skeleton/mockup, esclusi per ora, non per principio); `telegram-drive-secure-fork` (fork di un
  progetto open source di terzi, "Telegram Drive" di caamer20, omesso dalla lista per non
  diluire il segnale di originalita' — da riconsiderare se si vuole comunque menzionarlo
  etichettato esplicitamente come fork). `harmony-book` non e' stata duplicata qui: e' gia'
  referenziata (ora con link al repository) nella sezione "Interests and personal growth", voce
  "Instruments and music theory".
- Shortlist emersa dalla ricognizione per un'eventuale pagina web statica dedicata ai progetti
  piu' rilevanti (stile skills-repo/MkDocs, da costruire come attivita' separata e successiva,
  non in questa sessione): `my-wedding-day`, `windows-status`, `pw-manager`,
  `legal-consultant`, `local-audio-transcriptor`, `pok--competitive-teambuilder`, `trader-bot`,
  `blog-alessio`. Nessuna pagina e' stata costruita: e' solo una lista di candidati.
- Ancora da fare, non affrontato in questa sessione: l'intera sezione "Ongoing studies" (titolo
  segnaposto `........` e due voci `aaaaaaa`).

## Fase 3 — Gestione documentale degli allegati

La nota archiviata sull'hosting documentale analizza le alternative a Google Drive per i link
del CV (molti dei link attuali in `main.tex` puntano ancora a Google Drive). La conclusione
motivata nella nota e' Proton Drive: zero setup, hosting gestito, crittografia end-to-end reale,
link con password e scadenza, percezione professionale migliore rispetto a MEGA nel contesto
enterprise. La struttura a cartelle proposta e' per contenuto, non per formato: `Certifications`,
`Portfolio`, `Projects`, `Publications`, `Thesis`, `References`, condividendo il singolo
documento necessario invece della cartella radice intera. Fase indipendente dal codice LaTeX:
si puo' affrontare separatamente, sostituendo i link uno alla volta.

## Fase 4 — Allineamento delle skill alla tassonomia di skills-repo (in gran parte completata il 2026-07-06)

Verificato che `skills-repo` e' gia' pubblicato e navigabile su `alesop95.github.io/skills/`
(sito raggiungibile, controllato con richieste dirette). Ogni bullet della sezione "Work
experience" > Intrawelt in `main.tex` che aveva una Capability page corrispondente in
`mkdocs.yml` e' stato trasformato in link diretto a quella pagina (19 bullet su 20; "Support and
automation" resta testo semplice, nessuna Capability corrispondente trovata). Questo ha permesso
di ripristinare, come semplice link invece che come prosa, i quattro bullet rimossi in un passo
precedente di questa stessa Fase 2 ("Entrepreneurship and technical leading", "Full-stack
development and devOps (SaaS)", "Data management, analytics & reporting", "IT service design and
user experience"): esistevano gia' le Capability page corrispondenti, quindi linkarle e' stato
sufficiente, senza bisogno di scrivere contenuto nuovo.

Vincolo di manutenzione dichiarato esplicitamente dall'utente il 2026-07-06: la tassonomia di
`skills-repo` non e' congelata, continuera' ad aggiornarsi e la lista delle Capability puo'
cambiare (rinominare, spostare o rimuovere pagine). I link aggiunti in `main.tex` sono quindi
fragili per costruzione. Risolto lo stesso giorno con `scripts/check-skill-links.ps1` (e
l'equivalente `.sh`): estrae ogni URL `alesop95.github.io/skills/...` citato nel `.tex`
principale e verifica con una richiesta HTTP HEAD che risponda 2xx, segnalando quelli rotti con
exit code diverso da zero. Non fa parte della build stessa (non e' invocato da `build.ps1`/`.sh`):
va eseguito manualmente prima di ogni build definitiva del CV, o periodicamente. Verificato il
2026-07-06 su tutti i 23 link attualmente presenti: tutti raggiungibili.

Testo originale della fase, ancora valido come principio generale:

La nota archiviata sulla tassonomia propone una gerarchia a tre livelli per le hard skill:
*Domain* (macroarea tecnica, es. Infrastructure, Security, Cloud), *Capability* (competenza
concreta, es. "Infrastructure & Virtualization", "Networking"), *Technology* (strumenti concreti,
es. Proxmox VE, Docker). Il principio operativo per il CV altaCV e' linkare sempre il livello
Capability, mai il livello Technology: il CV resta sintetico e rimanda a una pagina esterna per
il dettaglio tecnico, separando il livello leggibile da un recruiter dal livello di
approfondimento per un IT Director o un CTO. Questo e' coerente con quanto gia' indicato in
`CLAUDE.md` sulla verifica dei nomi delle skill contro `skills-repo`. Un primo tentativo di
elencare le hard skill direttamente come sequenza di `\cvtag` e' stato scartato (vedi
`altacv-reference.md`, sezione cvtag) proprio perche' produce "keyword dumping" senza la
distinzione Capability/Technology. Azione da completare quando `skills-repo` sara' pubblicato e
consultabile: sostituire le voci di skill in `main.tex` con link alle pagine Capability
corrispondenti.

## Fase 5 — Multilingua (avviata il 2026-07-06, estesa a tre lingue lo stesso giorno)

Meccanismo scaffolded su richiesta esplicita dell'utente, prima che il contenuto inglese fosse
completamente stabile (deroga alla priorita' originaria di questa fase, decisa dall'utente).
Aggiunto in `main.tex`: una macro-variabile `\CVlanguage` (default `"en"`, valori possibili `"en"`,
`"it"`, `"es"`) e una macro `\cvtext{italiano}{spagnolo}{inglese}` che seleziona il testo attivo
in base a `\CVlanguage` — altaCV resta solo motore di rendering, il contenuto diventa un dato
parametrico. Prima versione (2026-07-06, mattina) era un semplice flag booleano a due stati
(italiano/inglese); estesa lo stesso giorno a tre lingue su richiesta esplicita.

**Traduzione completa eseguita il 2026-07-07**: su richiesta esplicita dell'utente ("la trilingua
vale per quello che c'e' gia' ovviamente"), tutto il contenuto inglese esistente in `main.tex` e'
stato tradotto in italiano e spagnolo tramite `\cvtext{...}{...}{...}`, sezione per sezione
(scelta di pacing esplicita dell'utente), invece di fermarsi ad aspettare approvazione riga per
riga. Coperti: tutti i titoli di sezione, tutte le voci di "Work experience", "Projects",
"Courses and Events", "Soft skills", "Education", "Most Proud of", "Languages", "Interests and
personal growth", "Volunteering", la nota "Interactive .pdf" in testata, e le etichette del
wheelchart. Lasciati intenzionalmente invariati in tutte le lingue: il tagline in testata (vedi
sotto), le testate di prodotto/azienda (nomi propri: Intrawelt, Clementoni, Elettromedia,
Labilia), i titoli di tesi (titoli ufficiali di documenti reali, non si traducono), gli
acronimi/nomi tecnici internazionali (SaaS, DevOps, MCP, RAG, LLM, GUI, VST3, ecc.).

**Bug scoperto e corretto durante la traduzione**: il meccanismo originale usava `\ifdefstring` di
`etoolbox` per il confronto di `\CVlanguage`. `\ifdefstring` non e' "edef-safe": si rompe
silenziosamente dentro `\MakeUppercase` (usato da `\cvsection` sui titoli di sezione tramite
altacv.cls) e anche dentro un `\edef` di pre-risoluzione, cadendo sempre sul terzo argomento
(inglese) indipendentemente dal valore reale di `\CVlanguage`. Risultato osservato: tutti i titoli
di sezione restavano in inglese anche compilando in italiano o spagnolo, mentre il resto del
contenuto (fuori da `\MakeUppercase`) traduceva correttamente. Diagnosticato con un test isolato
fuori da `main.tex` (non modificando il documento reale per il debug) che ha confrontato
`\ifdefstring` con un confronto `\ifx` di TeX puro; `\ifx` si e' rivelato affidabile in ogni
contesto di espansione. `\cvtext` ora usa `\ifx\CVlanguage\CVlangIT`/`\CVlangES` (macro ausiliarie
con la stessa definizione letterale "it"/"es"), non `\ifdefstring`. Dettagli completi in
`altacv-reference.md`.

Verificato con una build reale di tutte e tre le lingue dopo la traduzione completa e la
correzione del bug: tutti i titoli di sezione si traducono correttamente, 3 pagine in tutte e tre
le lingue (lo spagnolo, naturalmente piu' lungo, ha richiesto di ridurre `\linespread` da 0.94 a
0.925 per rientrare in 3 pagine invece di sconfinare in una quarta per una sola voce).

Deliberatamente non fatto: nessuna revisione madrelingua dello spagnolo. Nella sezione
"Languages" del CV stesso lo spagnolo e' dichiarato lingua di studio in corso (1.5/5): pubblicare
la versione spagnola del CV senza una revisione madrelingua resta un rischio professionale da
valutare esplicitamente con l'utente prima dell'uso reale, non solo una questione di tempo di
traduzione. La traduzione italiana e inglese non necessitano della stessa cautela (italiano e'
la lingua madre dell'utente, inglese il contenuto originale gia' esistente).

Prima decisione di contenuto per la traduzione, dichiarata esplicitamente il 2026-07-06: il
tagline in testata ("IT manager, Software architect, Sysadmin") NON va tradotto, resta invariato
in tutte le lingue (rispettata nella traduzione del 2026-07-07: il tagline non e' stato wrappato
in `\cvtext`).

Intenzione dichiarata dall'utente per il lavoro futuro: da qui in avanti, ogni nuovo contenuto
scritto per il CV (quando si riprendono le voci del backlog contenuti una alla volta) va scritto
contestualmente nelle lingue attive tramite `\cvtext{...}{...}{...}`, invece di scrivere prima
in inglese e tradurre dopo in un passaggio separato.

Confermato esplicitamente dall'utente il 2026-07-06: la trilingua si applica anche al contenuto
inglese gia' esistente in `main.tex` (l'intero documento attuale), non solo al contenuto nuovo.
Data l'entita' del lavoro (l'intero documento, diverse centinaia di righe), si procede sezione per
sezione (scelta esplicita dell'utente tra "sezione per sezione" e "bozza completa in un colpo
solo"): una sezione alla volta, mostrata per revisione prima di passare alla successiva, invece di
tradurre tutto in blocco e correggere alla fine. Non ancora iniziata la traduzione vera e propria
in questa sessione: fatta solo l'infrastruttura (vedi sotto, build multilingua).

### Build multilingua: tre PDF datati, uno per lingua

Creati `scripts/build-multilang.ps1` e `.sh` (ADR-005 in `memory/decisions.md`): compilano
`main.tex` una volta per lingua (EN/IT/ES), producendo `cv-sopranzi-alessio-<lingua>-<data>.pdf` in
`dated-builds/<lingua>/`. Verificato con una build reale di tutte e tre le lingue: compilazione
riuscita, contenuto identico nelle tre (atteso, nessuna sezione e' ancora stata tradotta). I PDF
datati NON sono tracciati in git (si accumulano nel tempo): restano un archivio locale, distinto
dai tre PDF stabili versionati in root (aggiornamento del 2026-07-08, ADR-006: `main.pdf` non
esiste piu', sostituito da `cv-sopranzi-alessio-{en,it,es}.pdf` sempre rigenerati insieme da
`scripts/build.ps1`).

## Fase 6 — Valutazione ATS-safety del layout (rimandata a data da destinarsi il 2026-07-06)

Nota sul titolo: il file originale si intitolava "studio per scrivere CV non controllato
dall'AI", ma il contenuto reale riguarda il parsing dei CV da parte degli *ATS* (Applicant
Tracking System, i software usati da recruiter e portali di candidatura per leggere
automaticamente i CV), non un
controllo editoriale da parte di un'intelligenza artificiale. La discrepanza tra titolo e
contenuto e' segnalata qui come da verificare, non e' stata risolta rileggendo un contesto
esterno al file stesso. Il contenuto analizza come i layout multi-colonna di altaCV possano
confondere l'ordine di lettura degli ATS, che si basano sulla geometria di pagina piu' che sulla
struttura logica. La raccomandazione pragmatica, senza abbandonare altaCV: mantenere la colonna
principale come unica sede delle informazioni critiche per il matching (esperienza, competenze)
in ordine cronologico lineare, degradare la sidebar a informazione secondaria non critica, e
valutare in futuro un output derivato in HTML o Markdown come sorgente neutra da cui generare sia
un PDF ATS-safe sia il PDF estetico attuale.

Rimandata esplicitamente dall'utente il 2026-07-06 dopo discussione: non e' un'esigenza attiva
(nessuna candidatura in corso tramite portale con parsing automatico), ma "una domanda di
principio per il futuro". Chiarito anche il compromesso dimensionale: comprimere il contenuto
attuale in una sola colonna alla stessa dimensione del testo raddoppierebbe circa le pagine (una
colonna singola ha meta' della capacita' di testo per pagina di due colonne affiancate), quindi
la soluzione corretta quando servira' davvero non e' convertire questo documento ma generare una
seconda variante separata, piu' semplice e a colonna singola, senza le stesse esigenze estetiche
del PDF principale. Nessuna modifica strutturale in questa sessione. `main.md`, il mirror
Markdown che avrebbe potuto essere un primo passo in questa direzione, e' stato eliminato (ADR-004
in `memory/decisions.md`) proprio perche' questa fase non e' piu' imminente: si rigenera in un
minuto con pandoc quando la fase verra' effettivamente ripresa.

## Fuori scope per questo repository

Il documento piu' esteso trovato nell'archivio (890 righe, circa 14800 parole) descrive la
pipeline `lettore-doc` + `skills-repo` (file `sources.yml`, run di `graphify`, tassonomia delle
skill estratta dai documenti sorgente). Riguarda il progetto `lettore-doc`, non `my-cv`: coerente
con quanto gia' scritto in `CLAUDE.md` ("`my-cv` non chiama nessuna pipeline: legge come
riferimento"), il suo contenuto non viene riportato qui e resta di competenza di quel repository.

## Note di direzione

Il CV e' sia un documento tradizionale (PDF per invio diretto) sia un pezzo del portfolio
pubblico. Il grafo delle skill a `alesop95.github.io/skills/graphify-out/graph.html` e' il
complemento interattivo: il CV dichiara le competenze, il grafo le contestualizza con le relazioni
semantiche e i progetti che le evidenziano.
