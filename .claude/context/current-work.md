---
generated-from-commit: 828275c
generated-from-branch: main
generated-date: 2026-07-06
covers-paths:
  - "main.tex"
last-verified-commit: c994a08
---

# Feature attiva

## Stato al c994a08 (verificato il 2026-08-27)

Non c'è nessuna sezione del CV in lavorazione. Il documento è completo, compila nelle tre lingue e sta su una pagina sola in tutte e tre: quello, non le tre pagine citate ripetutamente nelle cronache qui sotto, è il formato corrente, raggiunto con i commit `07921cc`, `aef38eb` e `aa8284d`. Il layer testuale del PDF è stato reso pulito con `7ea1955`, e tre dei dieci allegati su Google Drive sono passati a Proton Drive con lo stesso commit.

Tutto ciò che segue in questa scheda resta cronologia archiviata delle sessioni del 2026-07-06 e 2026-07-07, conservata perché contiene il razionale di scelte grafiche ancora in vigore. Va letta come storia, non come lavoro aperto, e ogni riferimento a "3 pagine" al suo interno è superato.

Decisione ancora in vigore, da non rimettere in discussione senza motivo: il tagline in testata ("IT manager, Software architect, Sysadmin") non si traduce e resta invariato in tutte e tre le lingue.

Restano aperti tre punti, tutti di contenuto e nessuno tecnico. "Ongoing studies" è tuttora disattivata con `\iffalse ... \fi` e contiene i segnaposto letterali `aaaaaaa`: si riattiva rimuovendo la coppia `\iffalse` e `\fi` quando il contenuto sarà pronto. La versione spagnola non ha mai avuto una revisione madrelingua, vincolo dichiarato e mai risolto, da sciogliere prima di un uso professionale reale di quella versione. I frammenti Coaching (Onova S.p.A. e Intracademy) restano rimandati per mancanza di esperienza reale da raccontare, mentre la sezione Consultant è stata esclusa in via definitiva per motivi fiscali, non soltanto rimandata.

## In lavorazione al 2026-07-06 (cronologia)

`main.tex` esiste già come punto di partenza (classe altaCV, struttura completa a due colonne) ed è stato riorganizzato il 2026-07-06 insieme alle cartelle satellite: vedi Fase 1 e Fase 2 di `roadmap.md` per l'elenco completo. La Fase 1 (bootstrap tecnico) è chiusa: `main.pdf` compila senza errori con `scripts/build.ps1`. Nella Fase 2, risolti nella stessa sessione: le quattro voci segnaposto di Intrawelt (rimosse, da ripopolare in futuro), "Developing app for listening test" (link al repository GitHub della tesi), "Acting, Theatre, Performing arts" (link allo spettacolo e date corrette). Rimandati esplicitamente dall'utente: i frammenti Coaching e Consultant, perché non ancora svolti in forma formale.

Risolto anche: "Private projects/applications" riscritta come lista sintetica per area tematica dopo ricognizione di ~25 cartelle progetto (dettagli ed esclusioni motivate in Fase 2 di `roadmap.md`); shortlist di 8 progetti candidati per un'eventuale pagina web dedicata futura, non costruita in questa sessione.

Fase 4 avanzata nella stessa sessione: 19 bullet di "Work experience" > Intrawelt ora linkano le Capability page corrispondenti su `alesop95.github.io/skills/` (verificato live), inclusi i quattro bullet rimandati in precedenza - recuperati come link invece che come prosa da scrivere. Vincolo aperto: la tassonomia di `skills-repo` non è stabile e i link possono rompersi quando cambia; nessun controllo automatico esiste ancora (dettagli in Fase 4 di `roadmap.md`).

"Ongoing studies" è stata disattivata con `\iffalse ... \fi` (non cancellata) invece di restare segnaposto visibile in un PDF altrimenti pronto: il testo letterale `aaaaaaa` compariva davvero nella pagina 3 del PDF compilato. Da riattivare rimuovendo `\iffalse`/`\fi` quando il contenuto sarà pronto.

## Primo PDF (2026-07-06): stato e revisione grafica

Prima build "presentabile" ottenuta e ispezionata pagina per pagina (conversione in PNG via Ghostscript, `gswin64c` di TinyTeX, per revisione visiva). Due problemi emersi nella prima ispezione sono stati risolti nello stesso giorno, su richiesta esplicita dell'utente:

- Risolto: il documento occupava 4 pagine con la quarta per lo più vuota. Sceso a 3 pagine ben bilanciate tramite (in ordine di intervento) spaziatura delle liste puntate uniformata a livello globale, `\medskip` convertiti in `\smallskip` in tutto il corpo, margini di `\geometry` ristretti, interlinea globale a `\linespread{0.94}`, e `\columnratio` corretto da 0.53 a 0.545 dopo aver scoperto (leggendo `paracol.sty`) che il parametro imposta la frazione della colonna *sinistra*, non della destra come riportava erroneamente la nota originale ora corretta in `altacv-reference.md`. Dettagli e razionale completo in quella scheda, sezione "Ridurre il numero di pagine".
- Risolto: i link erano visivamente indistinguibili dal testo (altacv.cls attiva `\hypersetup{hidelinks}`). Aggiunto un bordino sottile (0.6pt, colore `accent`) intorno a ogni link tramite override di `\hypersetup` dopo `\begin{document}`, testo invariato. Dettagli in `altacv-reference.md`, sezione "Personalizzazione dei link".

Difetto minore pre-esistente nel testo originale, non introdotto in questa sessione e non ancora corretto: la voce "Hold Me Tight" EFT couples workshop (Courses and Events) ha una virgoletta di chiusura dritta `"` invece che tipografica, asimmetrica rispetto all'apertura.

## Seconda revisione grafica (2026-07-06): link meno invasivi e testo giustificato

Dopo revisione dell'utente sul PDF reale (screenshot, non sulle anteprime PNG di questa sessione): il riquadro pieno (`/S/S`) attorno a quasi ogni bullet di "Work experience" risultava troppo aggressivo, a scapito della leggibilità. Sostituito con una sottolineatura sottile (`/S/U`, stesso colore `accent`), verificata leggendo la struttura interna del PDF generato (`/BS<<...>>` nel file grezzo) perché l'anteprima Ghostscript usata in questa sessione non distingue visivamente `/S/U` da `/S/S`: per questo aspetto specifico l'anteprima PNG non è affidabile, serve il PDF aperto in un lettore reale o l'ispezione della struttura interna.

Aggiunta anche la giustificazione del testo (richiesta separata, confrontando con l'allineamento di Word): `\raggedright` ridefinito come `\justifying` subito dopo `\makecvheader` (non nel preambolo: rompeva l'intestazione, vedi `altacv-reference.md`). Il documento resta a 3 pagine dopo entrambe le modifiche.

## Terza revisione grafica (2026-07-06): terzo tentativo sui link, bug del titolo, font, Interests

La sottolineatura si è rivelata comunque troppo invasiva alla densità di link di questo CV (quasi ogni bullet di "Work experience" e molte frasi di "Private projects" sono linkate). Dopo due tentativi con bordo (riquadro pieno, poi sottolineatura), terzo tentativo con colore di testo puro (`colorlinks=true, allcolors=accent`, nessun bordo, nessuna sottolineatura): il colore da solo non aggiunge peso grafico riga per riga, a differenza di qualunque bordo. Dettagli e motivazione completa in `altacv-reference.md`.

Bug scoperto durante la stessa revisione (screenshot dell'utente): il titolo di `\cvachievement` ("Full IT Infrastructure end-to-end transformation") giustificava insieme alla descrizione, perché titolo e descrizione condividono la stessa colonna `tabularx` nella macro della classe. Su un titolo corto che va a capo, la giustificazione produce una riga stirata in modo innaturale. Corretto patchando `altacv.cls` (vendorizzata nel progetto): il titolo forza sempre il vero ragged-right catturato prima della ridefinizione, la descrizione resta giustificata. Dettagli in `altacv-reference.md`.

Font base ridotto da 10pt a 9pt (`\documentclass[9pt,...]`) su richiesta esplicita. Sezione "Interests and personal growth" compattata: rimosso uno `\smallskip` esplicito ridondante tra le 14 voci `\cvachievement`, che si sommava allo `\smallskip` già incluso nella definizione della macro stessa, raddoppiando lo spazio (equivalente a un `\medskip`).

Il documento resta a 3 pagine dopo tutte queste modifiche, ma ora con parecchio spazio bianco in coda alla pagina 3 (il font più piccolo ha liberato spazio): segnalato, nessun intervento ulteriore senza indicazione esplicita (es. aumentare di nuovo leggermente il font, o riattivare "Ongoing studies").

## Quarta revisione grafica (2026-07-06): font e testata

Il font a 9pt della revisione precedente è stato giudicato illeggibile in stampa al 100%: riportato a 10pt. Nonostante l'aumento, il documento resta a 3 pagine grazie alle altre modifiche di compattazione già fatte (giustificazione, spaziatura liste, Interests compattata). Ridotta anche la foto in testata da 4.8cm a 3.6cm: il blocco nome/tagline/personalinfo era più basso della foto, quindi l'altezza della testata era dettata dalla foto stessa, con spazio bianco sotto la nota "Interactive .pdf" fino al bordo inferiore della foto. Link lasciati invariati (colore `accent`, poco visibile): segnalato dall'utente come "quasi non si vede", esplicitamente rimandato per ora.

## Quinta revisione grafica (2026-07-06): date scritte a mano uniformate

Le 16 date scritte a mano dentro il testo dei bullet (non quelle generate da `\cvevent` tramite `\cvDateMarker`, quelle restano com'erano) avevano due dimensioni diverse a seconda della sezione: `\small` in "Academic projects" (itemize non wrappata in `cveventblock`, quindi ambiente di default più grande), `\footnotesize` altrove (dentro `cveventblock`, o dopo la chiusura di un gruppo `\small` locale che non si estendeva alla data). Uniformate con un nuovo comando `\itemdate{...}` (`\footnotesize\itshape`, nessun colore: `accent`/`subheading` sono la stessa tonalità usata per i link, un colore condiviso avrebbe confuso date e link). Dettagli completi in `altacv-reference.md`.

## Backlog di feature (separato dai contenuti, 2026-07-06)

Su richiesta esplicita, la roadmap è stata divisa in un backlog di feature (lavoro tecnico sul template, senza scrivere contenuto) e un backlog di contenuti (da riprendere uno alla volta in sessioni future: Ongoing studies, frammenti Coaching/Consultant, traduzione italiana, migrazione documentale su Proton Drive, eventuale pagina statica per i progetti più rilevanti).

Primo elemento del backlog di feature, scelto dall'utente e completato: script di verifica dei link a skills-repo (`scripts/check-skill-links.ps1` e `.sh`), vedi Fase 4 di `roadmap.md` per il dettaglio. Testato con successo sia sul caso di link validi (23 su 23 raggiungibili) sia su un link volutamente inesistente (rilevato correttamente, exit code 1).

Chiuse nella stessa sessione: ATS-safety (Fase 6) rimandata esplicitamente a data da destinarsi, non è un'esigenza attiva; `main.pdf` versionato nel repository; `main.md` eliminato. Dettagli e motivazioni in ADR-004 (`memory/decisions.md`) e Fase 6 di `roadmap.md`. Nessuna voce aperta resta nel backlog di feature per ora.

Aggiornamento del 2026-07-08 (ADR-006 in `memory/decisions.md`): `main.pdf` non esiste più. Sostituito da tre PDF stabili versionati, uno per lingua (`cv-sopranzi-alessio-{en,it,es}.pdf`), sempre rigenerati insieme da `scripts/build.ps1`, così un commit non può più lasciare una lingua disallineata dalle altre due.

## Definition of done

Il CV è pronto quando:
- il PDF compila senza errori o warning rilevanti.
- tutte le sezioni principali sono presenti e popolate (informazioni personali, istruzione, esperienza lavorativa, competenze, lingue), in tutte e tre le lingue.
- nessun segnaposto (`aaaa`, `aaaaaaaaa`, `[TBC]`) resta nel sorgente.
- i nomi delle competenze sono allineati alla tassonomia di `skills-repo` (Fase 4 di `roadmap.md`).
- il PDF è leggibile e professionale sia su schermo che stampato.

## Multilingua esteso a tre lingue, con traduzione da fare sezione per sezione (2026-07-06)

Il meccanismo `\cvtext` è stato esteso da due a tre lingue (EN/IT/ES) su richiesta esplicita, vedi Fase 5 di `roadmap.md` per il dettaglio tecnico e il vincolo sullo spagnolo (lingua di studio in corso dell'utente, 1.5/5: da valutare se pubblicarne una versione senza revisione madrelingua). Verificato con un test isolato che il selettore funziona in tutti e tre gli stati.

Confermato dall'utente: la trilingua si applica anche a tutto il contenuto inglese già scritto (non solo al contenuto nuovo). Su richiesta esplicita di procedere senza fermarsi per piccole approvazioni (per non consumare token inutilmente), la traduzione è stata eseguita per intero il 2026-07-07 in un'unica sessione di lavoro, sezione per sezione ma senza pause di conferma intermedie, con verifica finale tramite build e ispezione visiva invece che revisione riga per riga durante il lavoro.

Creati e verificati `scripts/build-multilang.ps1`/`.sh`: producono i tre PDF datati per lingua (`cv-sopranzi-alessio-<lingua>-<data>.pdf`), non tracciati in git (ADR-005). Dettagli in Fase 5 di `roadmap.md`.

## Traduzione completa EN/IT/ES eseguita (2026-07-07)

Tutto il contenuto di `main.tex` è ora bilingue/trilingue tramite `\cvtext{...}{...}{...}`. Durante il lavoro è emerso un bug reale (non solo una questione di contenuto): `\ifdefstring` di etoolbox, usato inizialmente per il confronto di `\CVlanguage`, non è "edef-safe" e si rompe dentro `\MakeUppercase` (usato da `\cvsection` per i titoli), facendo restare tutti i titoli di sezione in inglese indipendentemente dalla lingua impostata. Diagnosticato con un test isolato e corretto sostituendo `\ifdefstring` con un confronto `\ifx` di TeX puro, affidabile in ogni contesto di espansione. Dettagli tecnici completi in `altacv-reference.md`.

Verificato con build reali di tutte e tre le lingue dopo la correzione: titoli di sezione tradotti correttamente ovunque, 3 pagine in tutte e tre le lingue (`\linespread` ridotto da 0.94 a 0.925 perché lo spagnolo, più lungo, sconfinava di una voce in una quarta pagina).

Rispettata la decisione di non tradurre il tagline in testata. Non fatta alcuna revisione madrelingua dello spagnolo (vincolo dichiarato, non risolto: vedi Fase 5 di `roadmap.md`).

## Rifiniture post-traduzione (2026-07-07)

Segnalato dall'utente via screenshot: il titolo di sezione "De lo que estoy más orgulloso" (spagnolo di "Most Proud of") andava a capo su due righe, e la riga decorativa sotto il titolo (`\cvsectionfont`/`\MakeUppercase` in altacv.cls) finiva posizionata male, a metà tra le due righe invece che sotto entrambe. La stessa cosa NON succedeva in inglese con "Interests and personal growth" (titolo altrettanto lungo, va a capo ma la riga si posiziona correttamente): non è quindi un bug generale del wrapping su più righe, sembra specifico a come il titolo spagnolo si spezzava (con sillabazione automatica a metà parola, "ORGUL-LOSO"). Non approfondito oltre a livello di causa: risolto pragmaticamente accorciando la traduzione a "Mis mayores logros", che sta su una riga sola. Se in futuro ricapitasse su un altro titolo lungo, vale la stessa soluzione (titolo più corto) prima di investigare la classe.

Riorganizzati anche gli output di `scripts/build-multilang.ps1`/`.sh` in sottocartelle per lingua (`dated-builds/en/`, `.../it/`, `.../es/`) su richiesta dell'utente, per non mescolare i file dopo settimane di build ripetute. Dettagli in ADR-005 aggiornata (`memory/decisions.md`).

## Domande aperte

Nessuna domanda tecnica. I tre punti di contenuto ancora aperti sono elencati nella sezione "Stato al 828275c" in testa a questa scheda.
