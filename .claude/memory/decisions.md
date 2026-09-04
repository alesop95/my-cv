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

## ADR-008 - Inventario e grafo dei link come artefatti derivati dal sorgente

Data: 2026-09-03.

Contesto: `.claude/context/external-links.md` dichiarava di essere stata ricostruita con uno script di estrazione, ma quello script viveva nello scratchpad di sessione e andava ricreato ogni volta, come la scheda stessa ammetteva in fondo. L'inventario era quindi prosa scritta a mano che descriveva un artefatto derivato, e la deriva era misurabile su HEAD `1ac5d00`: cinquantaquattro link dichiarati contro cinquantadue bersagli reali, otto pagine `projects` annunciate ed elencate sette, sedici link attribuiti al blog dove i tag sono tredici, le cinque Capability tecniche nominate senza il segmento di categoria che gli URL reali contengono. La deriva peggiore era di perimetro: la tabella della migrazione verso Proton teneva in un solo insieme i link ancora citati da `main.tex` e quelli che nel luglio 2026 si erano trasferiti sulle pagine del repository `projects`, così la Fase 3 della roadmap prometteva sette link residui su un insieme che non esisteva. Nello stesso perimetro c'erano cinque documenti Drive che nessuna scheda aveva mai tracciato.

Opzioni valutate: (a) riscrivere le schede a mano con i numeri corretti, costo minore subito e deriva garantita alla prossima modifica di `main.tex`, perché il meccanismo che l'ha prodotta resterebbe intatto; (b) generare le tabelle da uno strumento versionato e verificabile, con una modalità di controllo non distruttiva sulla falsariga di `md-unwrap --check`; (c) rinunciare all'inventario e consultare il sorgente ogni volta, scartata perché il sorgente non dice a quale categoria appartiene un link, quale sia il suo stato di migrazione, né cosa lo rompe.

Scelta: la (b). `tools/extract-cv-links.py` legge `main.tex` e `altacv.cls`, non li scrive mai, e genera le tabelle dell'inventario e il blocco Mermaid del grafo dentro regioni marcate delle due schede, lasciando intatta la prosa scritta a mano attorno. La prosa continua a portare ciò che nessuno strumento può dedurre dal sorgente, cioè le decisioni, gli stati di avanzamento e le cause di rottura; le tabelle portano i fatti misurabili.

Tre vincoli di progetto che vale registrare, perché non sono evidenti. I template URL delle topic page del blog e i prefissi dei campi info non sono scritti nello strumento ma letti dalle definizioni `\newcommand` e `\NewInfoField` del sorgente: scriverli a mano riprodurrebbe in forma nuova lo stesso difetto di un inventario che sembra derivato e non lo è. I commenti LaTeX si neutralizzano conservando ogni offset di carattere, perché i numeri di riga dell'inventario si calcolano da quelli e perché altrimenti i tre `\href` che il documento tiene deliberatamente commentati entrerebbero nell'inventario come attivi. Le regioni generate non contengono né la data di estrazione né il commit di riferimento: sarebbero metadato volatile e renderebbero `--check` rosso dopo qualunque commit successivo, anche non pertinente, addestrando a ignorarlo.

Verifica: `--check` è stato provato deliberatamente in fallimento, iniettando un `\href` finto in una copia di `main.tex` nello scratchpad, prima di essere considerato funzionante. Uno strumento di verifica che non ha mai fallito una volta non è verificato.

Conseguenza per il lavoro futuro: dopo ogni modifica ai link di `main.tex` si esegue `python tools/extract-cv-links.py --write`, e `--check` entra fra i controlli documentali pre-commit accanto a `md-unwrap --check` e `lint-md-commands`. Le tabelle delle due schede non si modificano a mano: una modifica manuale viene sovrascritta al primo rigenero, ed è per questo che i marcatori di regione lo dichiarano nel testo.

## ADR-009 - Proton come superficie di pubblicazione, Google Drive come archivio

Data: 2026-09-04.

Contesto: dal 2026-07-15 questo lavoro era descritto come una migrazione da Google Drive a Proton Drive, e la scheda `context/external-links.md` portava un memo che chiedeva di cancellare gli originali da Drive a migrazione verificata end-to-end. Quella formulazione ha prodotto due frizioni concrete. La prima è apparsa sui Bisogni Educativi Speciali, dove il materiale è un albero di sottocartelle di studio: spostarlo su Proton significava replicare un archivio, e la domanda su come gestirlo là era senza risposta buona. La seconda è apparsa sulle tesi, dove la cancellazione da Drive avrebbe rotto ogni copia del CV già inviata, perché i due redirect tinyurl continuano a esistere fuori dal repository e a puntare a Drive.

Opzioni valutate: (a) migrare l'archivio, cioè replicare su Proton la struttura completa e poi cancellare da Drive - scartata dall'utente, perché costringe a gestire su Proton una raccolta che su Drive è già organizzata, e perché la cancellazione distrugge i link delle copie del CV in circolazione; (b) tenere tutto su Drive e limitarsi a sistemare le condivisioni - scartata implicitamente, perché non risolve la percezione di privacy che aveva motivato Proton nel 2026-07-15; (c) separare i due ruoli, scelta.

Scelta: Google Drive resta l'archivio e conserva la raccolta completa, senza cancellazioni. Proton riceve soltanto il singolo file che il CV linka, uno per link, e ha quindi il ruolo di superficie di pubblicazione e non di destinazione di migrazione. Nessun documento va cancellato da Drive come parte di questo lavoro, e il memo che lo chiedeva è ritirato.

Conseguenza che semplifica una decisione ricorrente. Quando un link del CV punta a una raccolta e non a un documento, questa regola non chiede più dove spostare la raccolta: chiede quale singolo file pubblicare, e se quel file non esiste allora il link non deve puntare a un archivio ma a una pagina descrittiva. È esattamente ciò che il 2026-09-03 è stato deciso caso per caso per Stampa 3D, Bisogni Educativi Speciali e lo studio dello spagnolo, e che da qui in avanti ha una ragione di principio invece di tre giustificazioni separate.

Conseguenza sui redirect. Ritirare un redirect da `main.tex` non lo ritira dal mondo: `tinyurl.com/Tesi-magistrale` e `tinyurl.com/Tesi-trienn` esistono ancora e puntano ancora a Drive, e ogni copia del CV inviata prima del 2026-09-04 li contiene. Riconfigurarli sui link Proton ripara tutte quelle copie in una volta, ed è quindi un'azione che conviene indipendentemente dalla cancellazione, che non ci sarà.

Verifica: la forma di un link Proton è controllabile automaticamente, il suo contenuto no. `check-links -Category proton` verifica la forma e riporta la lunghezza della chiave, perché il percorso `/urls/<id>` risponde 200 a qualunque identificativo e la chiave dopo il `#` non raggiunge mai il server. La verifica reale resta aprire il link in una finestra privata, ed è stata fatta su tutti e cinque i link oggi presenti nel CV.
