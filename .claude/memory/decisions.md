# Registro delle decisioni (ADR-lite)

> Una voce per decisione rilevante. Includere contesto, opzioni valutate, scelta fatta e motivazione.

---

## ADR-001 - Engine LaTeX: pdflatex

Data: 2026-06-23

Opzioni valutate: pdflatex, lualatex, xelatex.

Scelta: pdflatex, fissato in .latexmkrc.

Motivazione: massima compatibilità con le classi CV più diffuse (moderncv, europasscv) e con TinyTeX su Windows. lualatex e xelatex sono superiori per la gestione dei font OpenType, ma richiedono pacchetti diversi e alcune classi CV non li supportano pienamente. Se si sceglie altacv (che preferisce lualatex), aggiornare .latexmkrc a `$pdf_mode = 4` e `$lualatex = ...`.

Conferma del 2026-07-06: con altaCV scelta in ADR-002, il timore che servisse lualatex non si è concretizzato. Il preambolo di `main.tex` gestisce il ramo pdflatex esplicitamente (pacchetti `roboto`/`lato` invece di `fontspec`), e la prima build reale con `scripts/build.ps1` produce `main.pdf` senza errori sotto pdflatex. Nessuna modifica a `.latexmkrc` necessaria.

Precisazione del 2026-08-27: la scelta di pdflatex resta valida, ma la frase "fissato in .latexmkrc" qui sopra non descrive più il meccanismo reale. Dal 2026-07-08 (ADR-006) la build invoca pdflatex direttamente e nessuno script legge `.latexmkrc`, che resta in radice solo come comodità per chi compila a mano con latexmk. L'engine è oggi fissato dal preambolo di `main.tex` e dalla riga di comando degli script di build.

---

## ADR-002 - Classe CV: altaCV

Data: 2026-06-23 (aperta), chiusa il 2026-07-06.

Opzioni candidate: moderncv (matura, ampiamente testata, template molto usato nei portali HR), europasscv (standard europeo, riconoscibile), altacv (più moderna, richiede lualatex), custom (massima flessibilità, più lavoro).

Scelta: altaCV.

Motivazione: la decisione è stata presa empiricamente, non per confronto delle opzioni sopra. L'utente ha fornito il 2026-07-06 un `main.tex` già sostanzialmente completo (599 righe, layout a due colonne con `paracol`, palette blu personalizzata, wheelchart) scritto con `\documentclass[10pt,a4paper,ragged2e,withhyper]{altacv}` come punto di partenza per continuare lo sviluppo. Il preambolo gestisce sia il ramo `pdflatex` sia il ramo `xelatex`/`lualatex` tramite `\iftutex`, quindi il vincolo "altacv richiede lualatex" ipotizzato quando l'ADR era aperta non si applica a questo sorgente: ADR-001 (pdflatex) resta valida, vedi `.claude/context/roadmap.md` Fase 1. Dettagli di sintassi e pattern d'uso della classe sono in `.claude/context/altacv-reference.md`.

---

## ADR-003 - Collocazione degli allegati personali: dentro al repo, gitignored

Data: 2026-07-06

Contesto: la cartella `[TBC] ATTACHMENTS/` contiene diplomi, attestati e la foto usata in `main.tex` (`\photoR{4.8cm}{...}`), alcuni file con dati sensibili nel nome (es. codice fiscale nel nome di un attestato). Non deve mai essere committata, ma alcuni suoi file sono referenziati da path relativi nel sorgente LaTeX.

Opzioni valutate: tenere la cartella dentro il repository ma esclusa da git tramite `.gitignore`, oppure spostarla interamente fuori da `E:\my-cv` (es. una cartella sorella) per rendere strutturalmente impossibile un commit accidentale.

Scelta: dentro il repository, rinominata `attachments/` e aggiunta a `.gitignore`.

Motivazione: `main.tex` referenzia già un file al suo interno con un path relativo (`attachments/Template e photos/photo_2024-08-07_09-31-03.jpg`); tenerla fuori dal repository avrebbe richiesto un path assoluto specifico di questa macchina o una copia manuale sincronizzata del singolo file usato, entrambe più fragili di una singola voce di `.gitignore`. Il rischio residuo, la possibilità di rimuovere per errore la riga da `.gitignore` e committare la cartella, si mitiga verificando `git status` prima di ogni `git add` esteso, già prassi indicata in `.claude/rules/security-permissions.md` e nelle istruzioni di sistema.

Aggiornamento del 2026-08-27: la decisione regge invariata, ma i riferimenti concreti citati sopra sono cambiati. La foto in uso non è più `photo_2024-08-07_09-31-03.jpg` a 4.8cm ma `attachments/Template e photos/photo-me-gemini.jpeg` a 2.6cm, sostituita con uno scatto nuovo il 2026-07-10 e ridotta durante la compattazione del CV. La conseguenza operativa della scelta va tenuta presente e non era stata scritta: poiché `attachments/` è ignorato da git, un clone pulito del repository non compila finché quel file non viene rimesso a mano al suo posto.

---

## ADR-004 - main.pdf versionato nel repository; main.md eliminato

Data: 2026-07-06

Contesto: dopo la prima build reale (Fase 1 di `roadmap.md`), `main.pdf` esiste come file generato. Il `.gitignore` aveva una riga `*.pdf` già presente ma commentata, cioè la decisione era esplicitamente rimandata fin dal bootstrap del progetto. Esisteva inoltre `main.md`, mirror pandoc di `main.tex` fornito insieme al sorgente iniziale, già disallineato dal contenuto reale del `.tex` dopo le prime modifiche (correzione path foto, graffa mancante) e senza uno scopo attivo dichiarato, se non un'ipotesi non confermata legata all'architettura multi-output della Fase 6.

Opzioni valutate per il PDF: versionarlo (link stabile su GitHub, storia con revisioni binarie ad ogni modifica di contenuto) oppure lasciarlo solo generato on-demand (repository più pulito, nessun link diretto scaricabile).

Scelta: versionare `main.pdf`. Motivazione: per un CV personale, la comodità di un link stabile al PDF compilato direttamente su GitHub (utile per condividere il repository come riferimento) pesa più del costo, trascurabile per un repository di queste dimensioni, delle revisioni binarie accumulate nella storia. La riga `*.pdf` in `.gitignore` resta commentata, non rimossa: il `.gitignore` sotto altre condizioni (es. build automatizzata in CI) potrebbe voler tornare a escluderlo.

Scelta collegata: `main.md` eliminato invece di essere risincronizzato. Motivazione: la Fase 6 (ATS-safety), unica ragione dichiarata per una futura architettura multi-output che avrebbe dato un ruolo a un mirror Markdown, è stata esplicitamente rimandata a data da destinarsi nella stessa sessione ("domanda di principio per il futuro", non un'esigenza attiva secondo l'utente). Mantenere un file già disallineato e senza consumatore reale sarebbe stata igiene di repository negativa; si rigenera in un minuto con pandoc se e quando la Fase 6 verrà effettivamente ripresa.

---

## ADR-005 - PDF multilingua datati: nome file e non tracciati in git

Data: 2026-07-06

Contesto: estesa la Fase 5 (multilingua) a tre lingue (EN/IT/ES) su richiesta esplicita, con l'intenzione dichiarata di avere sempre tre PDF paralleli, uno per lingua, generati da `main.tex`. Serviva uno schema di nome che distinguesse i tre file e gestisse le rigenerazioni dello stesso giorno.

Scelta: `scripts/build-multilang.ps1`/`.sh` (nuovi script) producono `cv-sopranzi-alessio-<lingua>-<AAAA-MM-GG>.pdf` (`<lingua>` = `en`/`it`/`es`). Assenza deliberata della componente oraria nel nome: rilanciare la build più volte lo stesso giorno sovrascrive semplicemente il file di quel giorno (stesso nome = stessa destinazione), mentre le date diverse restano distinte come istantanee storiche, senza bisogno di confrontare timestamp esplicitamente.

Aggiornamento del 2026-07-07: i tre PDF inizialmente finivano tutti nella root del progetto: dopo la prima traduzione completa e i primi cicli di build ripetuti, l'utente ha notato che si sarebbero mescolati nella root dopo settimane di uso. Spostati in sottocartelle per lingua, `dated-builds/en/`, `dated-builds/it/`, `dated-builds/es/`, mantenendo comunque la lingua anche nel nome file (ridondante con la cartella, ma utile se il PDF viene estratto dalla cartella, es. per essere allegato a un'email). `OutDir` di default è passato da "radice del progetto" a "dated-builds/ nella radice".

Scelta collegata: questi PDF datati NON sono tracciati in git (l'intera cartella `dated-builds/` aggiunta a `.gitignore`, non più un pattern sul nome file), a differenza di `main.pdf` che resta versionato in root (ADR-004). Motivazione: `main.pdf` è un singolo file che si aggiorna; i PDF datati per lingua si accumulano nel tempo (fino a tre file nuovi per ogni giorno di build), lo stesso ragionamento sul costo trascurabile delle revisioni binarie fatto in ADR-004 per un file singolo non regge più quando il numero di file cresce senza limite. Restano un archivio locale/personale delle istantanee inviate nel tempo, non un artefatto da versionare.

Implementazione tecnica: `main.tex` usa `\providecommand{\CVlanguage}{en}` (non `\newcommand`) proprio per permettere agli script di iniettare `\providecommand\CVlanguage{<lingua>}\input{main.tex}` come argomento di pdflatex al posto del nome file, sovrascrivendo il default senza errori di "comando già definito". Gli script compilano con pdflatex direttamente (due passaggi fissi), non con latexmk, perché l'argomento iniettato non è un vero nome di file e comprometterebbe l'analisi delle dipendenze di latexmk.

---

## ADR-006 - main.pdf sostituito da tre PDF stabili, uno per lingua, sempre rigenerati insieme

Data: 2026-07-08

Contesto: dopo ADR-004 (main.pdf versionato, solo inglese perché `\CVlanguage` di default vale "en") e ADR-005 (PDF trilingue datati, non versionati, in `dated-builds/`), l'utente ha notato che per avere una versione stabile in italiano o spagnolo doveva sempre andare a cercarla tra le istantanee datate di `dated-builds/`, mai allineata per costruzione con `main.pdf` perché prodotta da uno script diverso in un momento diverso. Ha inoltre richiesto esplicitamente che ogni ricompilazione prima di un commit aggiorni sempre e comunque tutte e tre le lingue insieme, così che un commit non possa mai lasciarne una disallineata dalle altre.

Opzioni valutate: (a) rigenerare `main.pdf` in una lingua scelta di volta in volta - scartata, produrrebbe una storia git incoerente (un commit in inglese, il successivo in italiano, senza che il contenuto segnali il cambio di lingua); (b) eliminare il riferimento stabile in root a favore del solo archivio in `dated-builds/` - scartata, `dated-builds/` è deliberatamente escluso da git (ADR-005): perderebbe l'intero scopo di ADR-004, un link diretto e stabile su GitHub; (c) tre file stabili, uno per lingua, sempre versionati e sempre rigenerati insieme - scelta.

Scelta: `main.pdf` non esiste più. I tre file stabili si chiamano `cv-sopranzi-alessio-en.pdf`, `cv-sopranzi-alessio-it.pdf`, `cv-sopranzi-alessio-es.pdf`, nella radice del progetto, versionati in git (stesso ragionamento sul costo trascurabile di ADR-004, esteso a tre file che si sovrascrivono invece di uno: bounded, non cresce nel tempo come i PDF datati di ADR-005). `scripts/build.ps1`/`.sh` non compilano più una singola lingua di default via latexmk: ora compilano sempre le tre lingue in un'unica esecuzione (stessa tecnica pdflatex diretto a due passaggi di `build-multilang.ps1`/`.sh`, jobname iniettato via `\providecommand\CVlanguage`), e vanno lanciati prima di ogni commit che tocca `main.tex`. Il flag `-Clean`/`--clean` rimuove ora i tre PDF stabili e i loro ausiliari invece di invocare `latexmk -c`.

`scripts/build-multilang.ps1`/`.sh` restano invariati e continuano a coesistere: producono le istantanee DATATE in `dated-builds/<lingua>/`, archivio storico locale non versionato (ADR-005), uno scopo diverso e volutamente separato dal riferimento stabile in root.

Conseguenza sul `.gitignore`: nessuna modifica alla riga `*.pdf` (resta commentata/non attivata, come in ADR-004); il commento è stato aggiornato per riflettere i tre nomi file invece di uno solo. `dated-builds/` resta escluso come da ADR-005.

---

## ADR-007 - Accessibilità del layer testuale del PDF: ActualText esplicito su ogni icona

Data: 2026-07-15, versionata con `7ea1955` il 2026-08-27.

Contesto: la Fase 6 di `roadmap.md` (ATS-safety del layout) è rimandata a data da destinarsi, ma durante la compattazione del CV è emerso un problema vicino e molto più economico da risolvere, distinto dall'ordine di lettura delle colonne. Estraendo il testo del PDF compilato, cioè simulando quel che fa un parser o un semplice copia-incolla verso un modulo di candidatura, le icone FontAwesome comparivano come glifi grezzi senza mappatura Unicode sensata: `Z`, `\'B9` e `\DH` al posto delle icone della sezione "Di cosa sono fiero". Nella riga dei contatti il danno era peggiore, perché `\printinfo` chiamato senza etichetta produceva la stringa letterale `\faEnvelope :` accanto all'indirizzo email.

Opzioni valutate: (a) lasciare così, sul presupposto che nessuna candidatura in corso passi da un parser automatico - scartata, la correzione costa poche righe di preambolo e il rumore nel testo estratto danneggia anche il semplice copia-incolla manuale; (b) togliere le icone dalle sezioni critiche - scartata, sono parte dell'identità visiva del CV e il problema sta nel layer testuale, non in quello grafico; (c) dichiarare esplicitamente con `accsupp` che cosa ogni icona rappresenta nel testo estratto - scelta.

Scelta: ogni icona porta un `ActualText` esplicito, con un valore che dipende dal suo ruolo. Le icone ornamentali passano per il nuovo comando `\decoicon`, che imposta `ActualText={}`, stringa vuota e non attributo assente: vuoto dichiara che l'elemento non contribuisce alcun carattere, assente lascia il parser ricadere sul glifo. Le icone che accompagnano un dato reale, cioè Email e Indirizzo nella riga dei contatti, ricevono invece un'etichetta vera passata come primo argomento opzionale di `\printinfo` e tradotta con `\cvtext` insieme al resto del documento.

Motivazione della distinzione: un'etichetta vuota su un campo di contatto perderebbe informazione utile a chi legge il testo estratto, mentre un'etichetta piena su un'icona ornamentale aggiungerebbe rumore. Un tentativo intermedio del 2026-07-13, `ActualText={#1: }` con il contenuto stesso come etichetta, è stato rimosso perché senza etichetta esplicita ricade sul `\detokenize` del comando icona, cioè produce esattamente il bug che doveva risolvere.

Verifica: estrazione reale del testo dai PDF compilati, non ispezione del sorgente. Frammenti e dettagli tecnici in `context/altacv-reference.md`, sezione sul layer testuale.

Conseguenza per il lavoro futuro: ogni icona aggiunta al documento va classificata come ornamentale o portante prima di essere inserita, e non resta senza `ActualText`. Questa decisione non chiude la Fase 6, che riguarda l'ordine di lettura delle colonne e resta rimandata.
