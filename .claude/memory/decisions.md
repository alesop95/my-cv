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

Conferma del 2026-07-06: con altaCV scelta in ADR-002, il timore che servisse lualatex non si e'
concretizzato. Il preambolo di `main.tex` gestisce il ramo pdflatex esplicitamente (pacchetti
`roboto`/`lato` invece di `fontspec`), e la prima build reale con `scripts/build.ps1` produce
`main.pdf` senza errori sotto pdflatex. Nessuna modifica a `.latexmkrc` necessaria.

---

## ADR-002 — Classe CV: altaCV

Data: 2026-06-23 (aperta), chiusa il 2026-07-06.

Opzioni candidate: moderncv (matura, ampiamente testata, template molto usato nei portali HR),
europasscv (standard europeo, riconoscibile), altacv (piu' moderna, richiede lualatex), custom
(massima flessibilita', piu' lavoro).

Scelta: altaCV.

Motivazione: la decisione e' stata presa empiricamente, non per confronto delle opzioni sopra.
L'utente ha fornito il 2026-07-06 un `main.tex` gia' sostanzialmente completo (599 righe, layout
a due colonne con `paracol`, palette blu personalizzata, wheelchart) scritto con
`\documentclass[10pt,a4paper,ragged2e,withhyper]{altacv}` come punto di partenza per continuare
lo sviluppo. Il preambolo gestisce sia il ramo `pdflatex` sia il ramo `xelatex`/`lualatex` tramite
`\iftutex`, quindi il vincolo "altacv richiede lualatex" ipotizzato quando l'ADR era aperta non si
applica a questo sorgente: ADR-001 (pdflatex) resta valida, vedi `.claude/context/roadmap.md`
Fase 1. Dettagli di sintassi e pattern d'uso della classe sono in
`.claude/context/altacv-reference.md`.

---

## ADR-003 — Collocazione degli allegati personali: dentro al repo, gitignored

Data: 2026-07-06

Contesto: la cartella `[TBC] ATTACHMENTS/` contiene diplomi, attestati e la foto usata in
`main.tex` (`\photoR{4.8cm}{...}`), alcuni file con dati sensibili nel nome (es. codice fiscale
nel nome di un attestato). Non deve mai essere committata, ma alcuni suoi file sono referenziati
da path relativi nel sorgente LaTeX.

Opzioni valutate: tenere la cartella dentro il repository ma esclusa da git tramite
`.gitignore`, oppure spostarla interamente fuori da `E:\my-cv` (es. una cartella sorella) per
rendere strutturalmente impossibile un commit accidentale.

Scelta: dentro il repository, rinominata `attachments/` e aggiunta a `.gitignore`.

Motivazione: `main.tex` referenzia gia' un file al suo interno con un path relativo
(`attachments/Template e photos/photo_2024-08-07_09-31-03.jpg`); tenerla fuori dal repository
avrebbe richiesto un path assoluto specifico di questa macchina o una copia manuale sincronizzata
del singolo file usato, entrambe piu' fragili di una singola voce di `.gitignore`. Il rischio
residuo, la possibilita' di rimuovere per errore la riga da `.gitignore` e committare la
cartella, si mitiga verificando `git status` prima di ogni `git add` esteso, gia' prassi indicata
in `.claude/rules/security-permissions.md` e nelle istruzioni di sistema.

---

## ADR-004 — main.pdf versionato nel repository; main.md eliminato

Data: 2026-07-06

Contesto: dopo la prima build reale (Fase 1 di `roadmap.md`), `main.pdf` esiste come file
generato. Il `.gitignore` aveva una riga `*.pdf` gia' presente ma commentata, cioe' la decisione
era esplicitamente rimandata fin dal bootstrap del progetto. Esisteva inoltre `main.md`, mirror
pandoc di `main.tex` fornito insieme al sorgente iniziale, gia' disallineato dal contenuto reale
del `.tex` dopo le prime modifiche (correzione path foto, graffa mancante) e senza uno scopo
attivo dichiarato, se non un'ipotesi non confermata legata all'architettura multi-output della
Fase 6.

Opzioni valutate per il PDF: versionarlo (link stabile su GitHub, storia con revisioni binarie ad
ogni modifica di contenuto) oppure lasciarlo solo generato on-demand (repository piu' pulito,
nessun link diretto scaricabile).

Scelta: versionare `main.pdf`. Motivazione: per un CV personale, la comodita' di un link stabile
al PDF compilato direttamente su GitHub (utile per condividere il repository come riferimento)
pesa piu' del costo, trascurabile per un repository di queste dimensioni, delle revisioni binarie
accumulate nella storia. La riga `*.pdf` in `.gitignore` resta commentata, non rimossa: il
`.gitignore` sotto altre condizioni (es. build automatizzata in CI) potrebbe voler tornare a
escluderlo.

Scelta collegata: `main.md` eliminato invece di essere risincronizzato. Motivazione: la Fase 6
(ATS-safety), unica ragione dichiarata per una futura architettura multi-output che avrebbe dato
un ruolo a un mirror Markdown, e' stata esplicitamente rimandata a data da destinarsi nella stessa
sessione ("domanda di principio per il futuro", non un'esigenza attiva secondo l'utente). Mantenere
un file gia' disallineato e senza consumatore reale sarebbe stata igiene di repository negativa;
si rigenera in un minuto con pandoc se e quando la Fase 6 verra' effettivamente ripresa.

---

## ADR-005 — PDF multilingua datati: nome file e non tracciati in git

Data: 2026-07-06

Contesto: estesa la Fase 5 (multilingua) a tre lingue (EN/IT/ES) su richiesta esplicita, con
l'intenzione dichiarata di avere sempre tre PDF paralleli, uno per lingua, generati da `main.tex`.
Serviva uno schema di nome che distinguesse i tre file e gestisse le rigenerazioni dello stesso
giorno.

Scelta: `scripts/build-multilang.ps1`/`.sh` (nuovi script) producono
`cv-sopranzi-alessio-<lingua>-<AAAA-MM-GG>.pdf` (`<lingua>` = `en`/`it`/`es`). Assenza deliberata
della componente oraria nel nome: rilanciare la build piu' volte lo stesso giorno sovrascrive
semplicemente il file di quel giorno (stesso nome = stessa destinazione), mentre le date diverse
restano distinte come istantanee storiche, senza bisogno di confrontare timestamp esplicitamente.

Aggiornamento del 2026-07-07: i tre PDF inizialmente finivano tutti nella root del progetto:
dopo la prima traduzione completa e i primi cicli di build ripetuti, l'utente ha notato che si
sarebbero mescolati nella root dopo settimane di uso. Spostati in sottocartelle per lingua,
`dated-builds/en/`, `dated-builds/it/`, `dated-builds/es/`, mantenendo comunque la lingua anche
nel nome file (ridondante con la cartella, ma utile se il PDF viene estratto dalla cartella, es.
per essere allegato a un'email). `OutDir` di default e' passato da "radice del progetto" a
"dated-builds/ nella radice".

Scelta collegata: questi PDF datati NON sono tracciati in git (l'intera cartella `dated-builds/`
aggiunta a `.gitignore`, non piu' un pattern sul nome file), a differenza di `main.pdf` che resta
versionato in root (ADR-004). Motivazione: `main.pdf` e' un singolo file che si aggiorna; i PDF
datati per lingua si accumulano nel tempo (fino a tre file nuovi per ogni giorno di build), lo
stesso ragionamento sul costo trascurabile delle revisioni binarie fatto in ADR-004 per un file
singolo non regge piu' quando il numero di file cresce senza limite. Restano un archivio
locale/personale delle istantanee inviate nel tempo, non un artefatto da versionare.

Implementazione tecnica: `main.tex` usa `\providecommand{\CVlanguage}{en}` (non `\newcommand`)
proprio per permettere agli script di iniettare `\providecommand\CVlanguage{<lingua>}\input{main.tex}`
come argomento di pdflatex al posto del nome file, sovrascrivendo il default senza errori di
"comando gia' definito". Gli script compilano con pdflatex direttamente (due passaggi fissi),
non con latexmk, perche' l'argomento iniettato non e' un vero nome di file e comprometterebbe
l'analisi delle dipendenze di latexmk.

---

## ADR-006 — main.pdf sostituito da tre PDF stabili, uno per lingua, sempre rigenerati insieme

Data: 2026-07-08

Contesto: dopo ADR-004 (main.pdf versionato, solo inglese perche' `\CVlanguage` di default vale
"en") e ADR-005 (PDF trilingue datati, non versionati, in `dated-builds/`), l'utente ha notato che
per avere una versione stabile in italiano o spagnolo doveva sempre andare a cercarla tra le
istantanee datate di `dated-builds/`, mai allineata per costruzione con `main.pdf` perche'
prodotta da uno script diverso in un momento diverso. Ha inoltre richiesto esplicitamente che ogni
ricompilazione prima di un commit aggiorni sempre e comunque tutte e tre le lingue insieme, cosi'
che un commit non possa mai lasciarne una disallineata dalle altre.

Opzioni valutate: (a) rigenerare `main.pdf` in una lingua scelta di volta in volta - scartata,
produrrebbe una storia git incoerente (un commit in inglese, il successivo in italiano, senza che
il contenuto segnali il cambio di lingua); (b) eliminare il riferimento stabile in root a favore
del solo archivio in `dated-builds/` - scartata, `dated-builds/` e' deliberatamente escluso da git
(ADR-005): perderebbe l'intero scopo di ADR-004, un link diretto e stabile su GitHub; (c) tre file
stabili, uno per lingua, sempre versionati e sempre rigenerati insieme - scelta.

Scelta: `main.pdf` non esiste piu'. I tre file stabili si chiamano `cv-sopranzi-alessio-en.pdf`,
`cv-sopranzi-alessio-it.pdf`, `cv-sopranzi-alessio-es.pdf`, nella radice del progetto, versionati
in git (stesso ragionamento sul costo trascurabile di ADR-004, esteso a tre file che si
sovrascrivono invece di uno: bounded, non cresce nel tempo come i PDF datati di ADR-005).
`scripts/build.ps1`/`.sh` non compilano piu' una singola lingua di default via latexmk: ora
compilano sempre le tre lingue in un'unica esecuzione (stessa tecnica pdflatex diretto a due
passaggi di `build-multilang.ps1`/`.sh`, jobname iniettato via `\providecommand\CVlanguage`), e
vanno lanciati prima di ogni commit che tocca `main.tex`. Il flag `-Clean`/`--clean` rimuove ora i
tre PDF stabili e i loro ausiliari invece di invocare `latexmk -c`.

`scripts/build-multilang.ps1`/`.sh` restano invariati e continuano a coesistere: producono le
istantanee DATATE in `dated-builds/<lingua>/`, archivio storico locale non versionato (ADR-005),
uno scopo diverso e volutamente separato dal riferimento stabile in root.

Conseguenza sul `.gitignore`: nessuna modifica alla riga `*.pdf` (resta commentata/non attivata,
come in ADR-004); il commento e' stato aggiornato per riflettere i tre nomi file invece di uno
solo. `dated-builds/` resta escluso come da ADR-005.
