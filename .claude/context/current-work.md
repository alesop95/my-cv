---
generated-from-commit: 3485498
generated-from-branch: main
generated-date: 2026-07-06
covers-paths:
  - "*.tex"
  - "sections/**"
last-verified-commit: 3485498
---

# Feature attiva

## In lavorazione

`main.tex` esiste gia' come punto di partenza (classe altaCV, struttura completa a due colonne)
ed e' stato riorganizzato il 2026-07-06 insieme alle cartelle satellite: vedi Fase 1 e Fase 2 di
`roadmap.md` per l'elenco completo. La Fase 1 (bootstrap tecnico) e' chiusa: `main.pdf` compila
senza errori con `scripts/build.ps1`. Nella Fase 2, risolti nella stessa sessione: le quattro
voci segnaposto di Intrawelt (rimosse, da ripopolare in futuro), "Developing app for listening
test" (link al repository GitHub della tesi), "Acting, Theatre, Performing arts" (link allo
spettacolo e date corrette). Rimandati esplicitamente dall'utente: i frammenti Coaching e
Consultant, perche' non ancora svolti in forma formale.

Risolto anche: "Private projects/applications" riscritta come lista sintetica per area
tematica dopo ricognizione di ~25 cartelle progetto (dettagli ed esclusioni motivate in Fase 2 di
`roadmap.md`); shortlist di 8 progetti candidati per un'eventuale pagina web dedicata futura,
non costruita in questa sessione.

Fase 4 avanzata nella stessa sessione: 19 bullet di "Work experience" > Intrawelt ora linkano le
Capability page corrispondenti su `alesop95.github.io/skills/` (verificato live), inclusi i
quattro bullet rimandati in precedenza — recuperati come link invece che come prosa da scrivere.
Vincolo aperto: la tassonomia di `skills-repo` non e' stabile e i link possono rompersi quando
cambia; nessun controllo automatico esiste ancora (dettagli in Fase 4 di `roadmap.md`).

"Ongoing studies" e' stata disattivata con `\iffalse ... \fi` (non cancellata) invece di restare
segnaposto visibile in un PDF altrimenti pronto: il testo letterale `aaaaaaa` compariva davvero
nella pagina 3 del PDF compilato. Da riattivare rimuovendo `\iffalse`/`\fi` quando il contenuto
sara' pronto.

## Primo PDF (2026-07-06): stato e revisione grafica

Prima build "presentabile" ottenuta e ispezionata pagina per pagina (conversione in PNG via
Ghostscript, `gswin64c` di TinyTeX, per revisione visiva). Due problemi emersi nella prima
ispezione sono stati risolti nello stesso giorno, su richiesta esplicita dell'utente:

- Risolto: il documento occupava 4 pagine con la quarta per lo piu' vuota. Sceso a 3 pagine ben
  bilanciate tramite (in ordine di intervento) spaziatura delle liste puntate uniformata a livello
  globale, `\medskip` convertiti in `\smallskip` in tutto il corpo, margini di `\geometry`
  ristretti, interlinea globale a `\linespread{0.94}`, e `\columnratio` corretto da 0.53 a 0.545
  dopo aver scoperto (leggendo `paracol.sty`) che il parametro imposta la frazione della colonna
  *sinistra*, non della destra come riportava erroneamente la nota originale ora corretta in
  `altacv-reference.md`. Dettagli e razionale completo in quella scheda, sezione "Ridurre il
  numero di pagine".
- Risolto: i link erano visivamente indistinguibili dal testo (altacv.cls attiva
  `\hypersetup{hidelinks}`). Aggiunto un bordino sottile (0.6pt, colore `accent`) intorno a ogni
  link tramite override di `\hypersetup` dopo `\begin{document}`, testo invariato. Dettagli in
  `altacv-reference.md`, sezione "Personalizzazione dei link".

Difetto minore pre-esistente nel testo originale, non introdotto in questa sessione e non ancora
corretto: la voce "Hold Me Tight" EFT couples workshop (Courses and Events) ha una virgoletta di
chiusura dritta `"` invece che tipografica, asimmetrica rispetto all'apertura.

## Seconda revisione grafica (2026-07-06): link meno invasivi e testo giustificato

Dopo revisione dell'utente sul PDF reale (screenshot, non sulle anteprime PNG di questa sessione):
il riquadro pieno (`/S/S`) attorno a quasi ogni bullet di "Work experience" risultava troppo
aggressivo, a scapito della leggibilita'. Sostituito con una sottolineatura sottile (`/S/U`,
stesso colore `accent`), verificata leggendo la struttura interna del PDF generato (`/BS<<...>>`
nel file grezzo) perche' l'anteprima Ghostscript usata in questa sessione non distingue
visivamente `/S/U` da `/S/S`: per questo aspetto specifico l'anteprima PNG non e' affidabile,
serve il PDF aperto in un lettore reale o l'ispezione della struttura interna.

Aggiunta anche la giustificazione del testo (richiesta separata, confrontando con l'allineamento
di Word): `\raggedright` ridefinito come `\justifying` subito dopo `\makecvheader` (non nel
preambolo: rompeva l'intestazione, vedi `altacv-reference.md`). Il documento resta a 3 pagine
dopo entrambe le modifiche.

## Terza revisione grafica (2026-07-06): terzo tentativo sui link, bug del titolo, font, Interests

La sottolineatura si e' rivelata comunque troppo invasiva alla densita' di link di questo CV
(quasi ogni bullet di "Work experience" e molte frasi di "Private projects" sono linkate). Dopo
due tentativi con bordo (riquadro pieno, poi sottolineatura), terzo tentativo con colore di testo
puro (`colorlinks=true, allcolors=accent`, nessun bordo, nessuna sottolineatura): il colore da
solo non aggiunge peso grafico riga per riga, a differenza di qualunque bordo. Dettagli e
motivazione completa in `altacv-reference.md`.

Bug scoperto durante la stessa revisione (screenshot dell'utente): il titolo di `\cvachievement`
("Full IT Infrastructure end-to-end transformation") giustificava insieme alla descrizione,
perche' titolo e descrizione condividono la stessa colonna `tabularx` nella macro della classe.
Su un titolo corto che va a capo, la giustificazione produce una riga stirata in modo innaturale.
Corretto patchando `altacv.cls` (vendorizzata nel progetto): il titolo forza sempre il vero
ragged-right catturato prima della ridefinizione, la descrizione resta giustificata. Dettagli in
`altacv-reference.md`.

Font base ridotto da 10pt a 9pt (`\documentclass[9pt,...]`) su richiesta esplicita. Sezione
"Interests and personal growth" compattata: rimosso uno `\smallskip` esplicito ridondante tra le
14 voci `\cvachievement`, che si sommava allo `\smallskip` gia' incluso nella definizione della
macro stessa, raddoppiando lo spazio (equivalente a un `\medskip`).

Il documento resta a 3 pagine dopo tutte queste modifiche, ma ora con parecchio spazio bianco in
coda alla pagina 3 (il font piu' piccolo ha liberato spazio): segnalato, nessun intervento
ulteriore senza indicazione esplicita (es. aumentare di nuovo leggermente il font, o riattivare
"Ongoing studies").

## Multilingua: infrastruttura avviata, contenuto non ancora scritto

Su richiesta esplicita, avviata la Fase 5 di `roadmap.md` in anticipo rispetto alla sua priorita'
originaria. Aggiunto il meccanismo (`\ifCVitalian`, `\cvtext{IT}{EN}`) senza applicarlo a nessun
contenuto: tradurre un CV professionale richiede scelte terminologiche che non vanno inventate.
Domanda aperta per l'utente, non ancora risposta: preferisce scrivere lui il testo italiano
sezione per sezione, o vuole una bozza proposta da rivedere insieme?

Prima decisione di contenuto per la futura traduzione, dichiarata esplicitamente il 2026-07-06:
il tagline in testata ("IT manager, Software architect, Sysadmin") NON va tradotto, resta
invariato anche nella versione italiana.

## Quarta revisione grafica (2026-07-06): font e testata

Il font a 9pt della revisione precedente e' stato giudicato illeggibile in stampa al 100%:
riportato a 10pt. Nonostante l'aumento, il documento resta a 3 pagine grazie alle altre modifiche
di compattazione gia' fatte (giustificazione, spaziatura liste, Interests compattata). Ridotta
anche la foto in testata da 4.8cm a 3.6cm: il blocco nome/tagline/personalinfo era piu' basso
della foto, quindi l'altezza della testata era dettata dalla foto stessa, con spazio bianco sotto
la nota "Interactive .pdf" fino al bordo inferiore della foto. Link lasciati invariati (colore
`accent`, poco visibile): segnalato dall'utente come "quasi non si vede", esplicitamente rimandato
per ora.

## Quinta revisione grafica (2026-07-06): date scritte a mano uniformate

Le 16 date scritte a mano dentro il testo dei bullet (non quelle generate da `\cvevent` tramite
`\cvDateMarker`, quelle restano com'erano) avevano due dimensioni diverse a seconda della
sezione: `\small` in "Academic projects" (itemize non wrappata in `cveventblock`, quindi ambiente
di default piu' grande), `\footnotesize` altrove (dentro `cveventblock`, o dopo la chiusura di un
gruppo `\small` locale che non si estendeva alla data). Uniformate con un nuovo comando
`\itemdate{...}` (`\footnotesize\itshape`, nessun colore: `accent`/`subheading` sono la stessa
tonalita' usata per i link, un colore condiviso avrebbe confuso date e link). Dettagli completi in
`altacv-reference.md`.

## Backlog di feature (separato dai contenuti, 2026-07-06)

Su richiesta esplicita, la roadmap e' stata divisa in un backlog di feature (lavoro tecnico sul
template, senza scrivere contenuto) e un backlog di contenuti (da riprendere uno alla volta in
sessioni future: Ongoing studies, frammenti Coaching/Consultant, traduzione italiana, migrazione
documentale su Proton Drive, eventuale pagina statica per i progetti piu' rilevanti).

Primo elemento del backlog di feature, scelto dall'utente e completato: script di verifica dei
link a skills-repo (`scripts/check-skill-links.ps1` e `.sh`), vedi Fase 4 di `roadmap.md` per il
dettaglio. Testato con successo sia sul caso di link validi (23 su 23 raggiungibili) sia su un
link volutamente inesistente (rilevato correttamente, exit code 1).

Chiuse nella stessa sessione: ATS-safety (Fase 6) rimandata esplicitamente a data da destinarsi,
non e' un'esigenza attiva; `main.pdf` versionato nel repository; `main.md` eliminato. Dettagli e
motivazioni in ADR-004 (`memory/decisions.md`) e Fase 6 di `roadmap.md`. Nessuna voce aperta resta
nel backlog di feature per ora.

Aggiornamento del 2026-07-08 (ADR-006 in `memory/decisions.md`): `main.pdf` non esiste piu'.
Sostituito da tre PDF stabili versionati, uno per lingua (`cv-sopranzi-alessio-{en,it,es}.pdf`),
sempre rigenerati insieme da `scripts/build.ps1`, cosi' un commit non puo' piu' lasciare una
lingua disallineata dalle altre due.

## Definition of done

Il CV e' pronto quando:
- il PDF compila senza errori o warning rilevanti.
- tutte le sezioni principali sono presenti (informazioni personali, istruzione, esperienza
  lavorativa, competenze, lingue) — gia' vero nella struttura di `main.tex`, manca il contenuto.
- nessun segnaposto (`aaaa`, `aaaaaaaaa`, `[TBC]`) resta nel sorgente.
- i nomi delle competenze sono allineati alla tassonomia di `skills-repo` (Fase 4 di
  `roadmap.md`).
- il PDF e' leggibile e professionale sia su schermo che stampato.

## Multilingua esteso a tre lingue, con traduzione da fare sezione per sezione (2026-07-06)

Il meccanismo `\cvtext` e' stato esteso da due a tre lingue (EN/IT/ES) su richiesta esplicita,
vedi Fase 5 di `roadmap.md` per il dettaglio tecnico e il vincolo sullo spagnolo (lingua di
studio in corso dell'utente, 1.5/5: da valutare se pubblicarne una versione senza revisione
madrelingua). Verificato con un test isolato che il selettore funziona in tutti e tre gli stati.

Confermato dall'utente: la trilingua si applica anche a tutto il contenuto inglese gia' scritto
(non solo al contenuto nuovo). Su richiesta esplicita di procedere senza fermarsi per piccole
approvazioni (per non consumare token inutilmente), la traduzione e' stata eseguita per intero il
2026-07-07 in un'unica sessione di lavoro, sezione per sezione ma senza pause di conferma
intermedie, con verifica finale tramite build e ispezione visiva invece che revisione riga per
riga durante il lavoro.

Creati e verificati `scripts/build-multilang.ps1`/`.sh`: producono i tre PDF datati per lingua
(`cv-sopranzi-alessio-<lingua>-<data>.pdf`), non tracciati in git (ADR-005). Dettagli in Fase 5 di
`roadmap.md`.

## Traduzione completa EN/IT/ES eseguita (2026-07-07)

Tutto il contenuto di `main.tex` e' ora bilingue/trilingue tramite `\cvtext{...}{...}{...}`.
Durante il lavoro e' emerso un bug reale (non solo una questione di contenuto): `\ifdefstring` di
etoolbox, usato inizialmente per il confronto di `\CVlanguage`, non e' "edef-safe" e si rompe
dentro `\MakeUppercase` (usato da `\cvsection` per i titoli), facendo restare tutti i titoli di
sezione in inglese indipendentemente dalla lingua impostata. Diagnosticato con un test isolato e
corretto sostituendo `\ifdefstring` con un confronto `\ifx` di TeX puro, affidabile in ogni
contesto di espansione. Dettagli tecnici completi in `altacv-reference.md`.

Verificato con build reali di tutte e tre le lingue dopo la correzione: titoli di sezione
tradotti correttamente ovunque, 3 pagine in tutte e tre le lingue (`\linespread` ridotto da 0.94
a 0.925 perche' lo spagnolo, piu' lungo, sconfinava di una voce in una quarta pagina).

Rispettata la decisione di non tradurre il tagline in testata. Non fatta alcuna revisione
madrelingua dello spagnolo (vincolo dichiarato, non risolto: vedi Fase 5 di `roadmap.md`).

## Rifiniture post-traduzione (2026-07-07)

Segnalato dall'utente via screenshot: il titolo di sezione "De lo que estoy más orgulloso"
(spagnolo di "Most Proud of") andava a capo su due righe, e la riga decorativa sotto il titolo
(`\cvsectionfont`/`\MakeUppercase` in altacv.cls) finiva posizionata male, a meta' tra le due
righe invece che sotto entrambe. La stessa cosa NON succedeva in inglese con "Interests and
personal growth" (titolo altrettanto lungo, va a capo ma la riga si posiziona correttamente):
non e' quindi un bug generale del wrapping su piu' righe, sembra specifico a come il titolo
spagnolo si spezzava (con sillabazione automatica a meta' parola, "ORGUL-LOSO"). Non approfondito
oltre a livello di causa: risolto pragmaticamente accorciando la traduzione a "Mis mayores
logros", che sta su una riga sola. Se in futuro ricapitasse su un altro titolo lungo, vale la
stessa soluzione (titolo piu' corto) prima di investigare la classe.

Riorganizzati anche gli output di `scripts/build-multilang.ps1`/`.sh` in sottocartelle per lingua
(`dated-builds/en/`, `.../it/`, `.../es/`) su richiesta dell'utente, per non mescolare i file dopo
settimane di build ripetute. Dettagli in ADR-005 aggiornata (`memory/decisions.md`).

## Domande aperte

Nessuna al momento.
