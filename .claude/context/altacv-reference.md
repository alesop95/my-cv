---
generated-from-commit: 3485498
generated-from-branch: main
generated-date: 2026-07-06
covers-paths:
  - "main.tex"
last-verified-commit: 3485498
---

# Riferimento tecnico: la classe altaCV

> Scheda consolidata dalle diciassette note sparse raccolte durante l'apprendimento della classe,
> ora archiviate in `_notes/tbc-archive/altacv-notes/`. Copre solo cio' che e' gia' in uso o
> direttamente rilevante per `main.tex`; non e' un manuale generale della classe.

## Premessa architetturale

AltaCV non espone un'opzione globale per centrare il testo, e questo e' intenzionale piuttosto
che una lacuna. Il template persegue due obiettivi che convergono sulla stessa scelta di
allineamento a sinistra: la leggibilita' umana, perche' un testo allineato con date e titoli
allineati permette una scansione visiva rapida delle informazioni, e la compatibilita' con gli
*ATS*[^1], che tipicamente interpretano male il testo centrato o le formattazioni complesse a
base di *TikZ* o box centrati, con il rischio concreto di perdere informazioni durante il
parsing. La scelta di non offrire quella scorciatoia stilistica e' quindi una scelta di
leggibilita' duale, per l'occhio umano e per il software.

## Preambolo e documentclass

`main.tex` dichiara `\documentclass[10pt,a4paper,ragged2e,withhyper]{altacv}`. L'opzione
alternativa `normalphoto` produce una foto non ritagliata a cerchio, se in futuro si volesse
cambiare la resa della foto in testata. La classe include gia' `xcolor` internamente, motivo per
cui i comandi `\definecolor` e `\colorlet` funzionano senza un `\usepackage{xcolor}` esplicito in
testa al file.

Il preambolo definisce un ambiente locale, `cveventblock`, non fornito dalla classe ma introdotto
nel template stesso:

```latex
\newenvironment{cveventblock}{%
  \begingroup
    \footnotesize
    \setlist[itemize]{topsep=2pt, itemsep=1pt, left=0.5em}
}{%
  \endgroup
}
```

Il punto sottile e' che `\cvevent` e' una macro autonoma che chiude il proprio ambito interno:
la dimensione dichiarata da `cveventblock` non ha effetto sul testo passato direttamente dentro
`\cvevent`, ma si applica correttamente all'elenco `itemize` che segue nello stesso blocco,
perche' quello resta davvero dentro l'ambiente. La sequenza corretta e' quindi aprire
`cveventblock`, scrivere `\cvevent{...}`, e subito dopo l'`itemize` con i punti, tutto prima di
chiudere l'ambiente.

## Colonne con paracol

Il layout a due colonne si ottiene con `\usepackage{paracol}` e `\columnratio{x}`. Verificato
leggendo direttamente `paracol.sty` (la nota originale su questo punto era sbagliata ed è stata
corretta il 2026-07-06): con un solo argomento, `x` è la frazione assegnata alla colonna
*sinistra*, non alla destra; la colonna destra riceve il complemento a 1. Con
`\columnratio{0.545}` (valore corrente in `main.tex`) la colonna sinistra occupa il 54.5% e la
destra il 45.5%. Dentro `\begin{paracol}{2} ... \end{paracol}` si passa dalla prima alla seconda
colonna con `\switchcolumn`; entrambe le colonne vanno a capopagina automaticamente se il
contenuto eccede lo spazio disponibile, restando sincronizzate pagina per pagina.

Quando le due colonne non si esauriscono alla stessa altezza, l'ultima pagina mostra uno spazio
bianco sotto la colonna piu' corta: non è un difetto della classe, è la conseguenza diretta di
quanto contenuto reale c'è in ciascuna colonna. Per bilanciare, le leve utili sono, in ordine di
impatto osservato praticamente: la quantità di contenuto in ciascuna colonna (spostare sezioni da
una colonna all'altra), il valore di `\columnratio` (dare più larghezza alla colonna più densa
riduce il numero di righe in cui va a capo), e solo per ultimo la spaziatura verticale
(`\medskip`/`\smallskip`, margini di `\geometry`, `\linespread`), che aiuta a ridurre il numero
di pagine totali ma non risolve da sola uno sbilanciamento tra le due colonne.

## Font

Il blocco font e' scritto per funzionare sia con motori *TeX moderni* (*XeLaTeX*, *LuaLaTeX*) sia
con `pdflatex`, tramite il test `\iftutex`:

```latex
\iftutex
  \setmainfont{Fira Sans}
  \setsansfont{Fira Sans}
  \renewcommand{\familydefault}{\sfdefault}
\else
  \usepackage[rm]{roboto}
  \usepackage[defaultsans]{lato}
  \renewcommand{\familydefault}{\sfdefault}
\fi
```

Con `pdflatex` (il ramo `\else`, quello attivo secondo ADR-001 in `memory/decisions.md`) i
pacchetti `roboto` e `lato` forniscono i font via *font maps* invece che via `fontspec`, che
richiederebbe un motore Unicode. Questo e' il motivo per cui la scelta della classe altaCV non
obbliga di per se' a cambiare motore: la doppia via nel preambolo la rende compatibile con
`pdflatex`, a condizione che `roboto` e `lato` siano nel manifesto `tex-packages.txt`.

Distinti dai font fisici sono i comandi che ne definiscono l'uso in punti specifici del
documento, con effetto locale invece che globale: `\namefont`, `\personalinfofont`,
`\cvsectionfont`, `\cvsubsectionfont`. Sono combinazioni di famiglia, dimensione e peso applicate
solo dove la classe li richiama, e vanno ridefinite con `\renewcommand` come gia' avviene in
`main.tex`.

## Colori

I colori semantici della classe (`name`, `tagline`, `heading`, `headingrule`, `subheading`,
`accent`, `emphasis`, `body`) si assegnano con `\colorlet` a partire da colori definiti con
`\definecolor{...}{HTML}{...}`. Cambiare la palette significa quindi ridefinire le cinque o sei
tonalita' di base e poi rimappare gli otto colori semantici, senza toccare il resto del
documento: la palette attuale in `main.tex` (blu notte, blu medio, celeste pastello) segue
esattamente questo schema.

## Icone

AltaCV include gia' *FontAwesome*[^2] internamente, motivo per cui comandi come `\faTrophy` o
`\faEnvelope` funzionano senza un `\usepackage{fontawesome}` esplicito. L'elenco completo delle
icone disponibili si consulta su fontawesome.com nella versione 4.7, che e' quella storicamente
inclusa dalla classe. I marker di default si personalizzano con `\renewcommand`:
`\cvItemMarker` per il punto elenco, `\cvRatingMarker` per la valutazione a stelle di `\cvskill`,
`\cvDateMarker` per l'icona accanto alla data negli eventi.

## Informazioni personali

Il blocco `\personalinfo{...}` accetta sia i campi predefiniti (`\phone`, `\linkedin`, `\github`)
sia campi liberi con `\printinfo{icona}{testo}[link opzionale]`. Per servizi senza una relazione
diretta tra username e URL si usa `\printinfo` con l'URL completo tra parentesi quadre; per
integrare un campo dedicato e riutilizzabile altrove si usa `\NewInfoField{nome}{icona}[prefisso
url]`, che genera un nuovo comando `\nome{valore}`.

## cvevent e il quarto argomento vuoto

`\cvevent{titolo}{organizzazione}{date}{luogo}` stampa sempre l'icona della posizione se il
quarto argomento contiene un token qualsiasi, spazio non-interrompibile incluso: la classe
testa la vacuita' con `\ifstrempty`, che riconosce come vuoto solo un argomento letteralmente
`{}`, non uno che contiene `~` o uno spazio. Per sopprimere l'icona quando non c'e' una
posizione da mostrare, come nel caso della voce Labilia in `main.tex`, l'argomento va lasciato
`{}` senza alcun contenuto visivo.

## cvtag

`\cvtag` produce testo normale, quindi eredita dimensione e colore come qualunque altro testo
(`\small`, `\color{gray!70!black}`), ma inserisce una spaziatura fissa che la classe non espone
come parametro modificabile senza intervenire sulla definizione della macro in `altacv.sty`. La
classe usa spesso `\raggedright` per l'impaginazione, e l'opzione documento `ragged2e` puo' far
fallire l'a-capo automatico tra una sequenza di `\cvtag` ravvicinati: il workaround e' racchiudere
il blocco di tag in `{\LaTeXraggedright ... }` oppure inserire `\\` manuali dove serve forzare il
ritorno a capo. Un primo tentativo di elencare le hard skill del CV direttamente come sequenza di
`\cvtag` (conservato come riferimento in `cvtag hardskills (aborted).txt` dentro l'archivio) e'
stato abbandonato a favore dell'approccio per link a `skills-repo` descritto nella Fase 4 di
`roadmap.md`: elencare ogni tecnologia come tag perde la distinzione tra livello Capability e
livello Technology, e produce l'effetto "keyword dumping" che nei CV senior e' percepito
negativamente.

## Hyperlink su due righe

`\href` tratta l'intero testo del link come un'unica parola indivisibile: LaTeX non applica mai
la sillabazione dentro un URL o dentro il testo linkato, quindi anche avvolgendo il tutto in
`\parbox` o `minipage` il contenuto non va a capo da solo. Il workaround usato per la tesi
magistrale in `main.tex` e' spezzare manualmente il testo in due `\href` separati sulla stessa
destinazione, uniti da un ritorno a capo esplicito dentro il `\parbox`:

```latex
{\footnotesize Thesis:
  \parbox{\dimexpr0.53\textwidth\relax}{
    \href{https://tinyurl.com/Tesi-trienn}{Study and development of synchronization systems } \\
    \href{https://tinyurl.com/Tesi-trienn}{performances for gps-based WSN}
  }
}
```

## Wheelchart

`\wheelchart{raggio esterno}{raggio interno}{lista separata da virgole}` disegna un grafico a
torta dove ogni voce ha la forma `valore/larghezza-testo/colore/etichetta`. Tutti i primi valori
vengono sommati e la quota di ciascuno spicchio e' proporzionale al totale, trasformato in 360
gradi: con sei valori che sommano a 24, uno spicchio di valore 8 occupa 120 gradi. La larghezza
in `em` non descrive lo spicchio ma il box massimo in cui il testo dell'etichetta viene
impaginato, per evitare che debordi. Se un'etichetta contiene virgole, l'intera etichetta va
racchiusa in `{...}`, altrimenti LaTeX interpreta la virgola interna come separatore tra spicchi
diversi. Lo spostamento con `\hspace*{-1.5cm}` prima del comando compensa il fatto che
`\wheelchart` disegna in un `picture` environment centrato rispetto alla colonna corrente, che
altrimenti risulterebbe visivamente spostato a destra.

## Pubblicazioni

La classe supporta un elenco pubblicazioni via `biblatex`, con `\addbibresource{sample.bib}` e
uno stile a scelta tra autore-anno (per convenzioni tipo APA) o numerico (stile IEEE), inclusi
come file `.tex` separati da richiamare con `\input`. `main.tex` non usa questa sezione: e' una
funzionalita' disponibile ma non attivata, da valutare solo se in futuro il CV dovesse includere
pubblicazioni accademiche.

## Dimensione del testo

I comandi di dimensione relativa disponibili, dal piu' piccolo al piu' grande, sono `\tiny`,
`\scriptsize`, `\footnotesize`, `\small`, `\normalsize`, `\large`, `\Large`, `\LARGE`, `\huge`,
`\Huge`. In un documento con corpo base 10pt, a titolo indicativo (i valori cambiano con la
dimensione base del documento), `\footnotesize` corrisponde a circa 8pt e `\LARGE` a circa 17pt.
Ai comandi di dimensione si combinano quelli di peso e stile: `\bfseries` per il grassetto,
`\itshape` per il corsivo, `\scshape` per il maiuscoletto, indipendenti dalla famiglia di font
(`\rmfamily` serif, `\sffamily` sans-serif, `\ttfamily` a spaziatura fissa).

## Traduzione italiana e accessibilita' del PDF

Le icone associate a `\cvLocationMarker` e `\cvDateMarker` dentro `\cvevent` sono puramente
visive: quando il PDF viene copiato come testo, per esempio incollandolo su LinkedIn o
estraendolo con `pdftotext`, quelle icone non producono un equivalente testuale leggibile. La
classe espone un livello di etichette rinominabili per questo scopo esatto, utile sia per la
traduzione in italiano sia per l'estrazione di testo pulito:

```latex
\renewcommand{\datename}{Data}
\renewcommand{\locationname}{Luogo}
\renewcommand{\eventname}{Evento}
```

Una traduzione completa del documento richiede tre passaggi distinti: tradurre manualmente tutto
il contenuto (titoli, descrizioni, esperienza), ridefinire le etichette automatiche della classe
come sopra, e caricare `babel` con l'opzione `italian`. Questo e' rilevante per la Fase 5 della
roadmap (multilingua): se si introduce un layer di contenuto parametrizzato per lingua, le
etichette di classe vanno parametrizzate allo stesso modo del contenuto, non lasciate fisse in
inglese.

## Personalizzazione dei link: colore di testo, dopo due tentativi con bordo

La classe altaCV, con l'opzione documento `withhyper`, attiva `\hypersetup{hidelinks}` subito
dopo `\begin{document}`: nessun colore, nessun bordo, i link sono visivamente indistinguibili dal
testo normale. Serve sovrascrivere `\hypersetup` con un'istruzione propria posizionata anch'essa
subito dopo `\begin{document}` (cosi' esegue dopo quella della classe, non prima).

Cronologia dei tre tentativi del 2026-07-06, a densita' di link molto alta (quasi ogni bullet di
"Work experience" e molte frasi di "Private projects" sono interamente o parzialmente linkate):
un riquadro pieno (`pdfborderstyle={/S/S/W 0.6}`) e' risultato troppo aggressivo, spezzando la
lettura riga per riga; sostituito con una sottolineatura (`/S/U`), risultata comunque troppo
invasiva alla stessa densita'; risolto passando al colore di testo puro, senza alcun bordo:

```latex
\hypersetup{
  colorlinks=true,
  allcolors=accent,
}
```

Il colore da solo non aggiunge peso grafico riga per riga (nessuna linea, nessun riquadro), a
differenza di qualunque stile di bordo, che a questa densita' di link si accumula visivamente. Il
colore `accent` (`SoftBlue`) e' lo stesso gia' usato altrove nel documento per segnalare elementi
interattivi (l'icona e il testo della nota "Interactive .pdf" in testata), quindi coerente con un
significato semantico gia' stabilito nel documento invece di introdurne uno nuovo. `allcolors`
imposta in un colpo solo `linkcolor`, `urlcolor`, `citecolor`, `filecolor`: e' l'opzione piu'
semplice quando, come qui, tutti i link devono avere lo stesso trattamento visivo.

Nota per verifiche future sugli stili di bordo (`/S/S`, `/S/U`): il renderer di annotazioni di
Ghostscript non distingue visivamente i due stili nelle anteprime PNG e disegna comunque un
riquadro; per verificarli in modo affidabile serve aprire il PDF in un lettore reale oppure
cercare `/BS<<...>>` nella struttura interna del file grezzo. Non e' un problema per il colore di
testo, verificabile a colpo d'occhio in qualunque renderer.

## Bug: titolo di cvachievement giustificato insieme alla descrizione

`\cvachievement{icona}{titolo}{descrizione}` (righe 338-344 di `altacv.cls`) mette titolo e
descrizione nella STESSA colonna di una `tabularx`, con un solo `>{\raggedright\arraybackslash}X`
dichiarato una volta per l'intera colonna. Quando si ridefinisce `\raggedright` per ottenere la
giustificazione (vedi sezione sotto), l'effetto si applica quindi anche al titolo, non solo alla
descrizione. Su un titolo corto che va a capo il risultato e' una riga stirata in modo innaturale
con l'ultima parola isolata (caso osservato: "Full IT Infrastructure end-to-end transforma-tion",
con "tion" solo sulla seconda riga). Corretto vendorizzando la patch direttamente in `altacv.cls`:

```latex
\let\altacv@titleraggedright\raggedright  % cattura il vero raggedright PRIMA della ridefinizione

\newcommand{\cvachievement}[3]{%
  \begin{tabularx}{\linewidth}{@{}p{2em} @{\hspace{1ex}} >{\raggedright\arraybackslash}X@{}}
  \multirow{2}{*}{...#1...} & {\altacv@titleraggedright\bfseries\textcolor{emphasis}{#2}}\\
  & #3
  \end{tabularx}%
  \smallskip
}
```

Il punto chiave e' l'ordine: `\let\altacv@titleraggedright\raggedright` deve stare nel file della
classe, quindi eseguito quando pdflatex legge `altacv.cls` durante il caricamento del documento,
*prima* che `main.tex` ridefinisca `\raggedright` piu' avanti nel proprio corpo. La macro
`\cvachievement` referenzia `\raggedright` per nome, non per valore congelato: senza questo `\let`
precedente, anche l'alias erediterebbe la ridefinizione successiva, vanificando la separazione tra
titolo (sempre ragged) e descrizione (giustificata quando richiesto).

## Date scritte a mano: dimensione e stile uniformi

Distinte dalle date generate automaticamente da `\cvevent` (terzo argomento, reso con
`\cvDateMarker` e la relativa icona), ci sono le date scritte direttamente nel testo dei bullet,
tipicamente dopo il titolo di una voce, per esempio `\textbf{\textsc{Titolo}} (01/2021 – 05/2021):
descrizione`. Queste ereditano la dimensione del contesto in cui compaiono invece di avere una
dimensione propria, e nel documento c'erano due contesti diversi: dentro `cveventblock` (o dopo
la chiusura di un gruppo `\small` locale, come `{\textbf{\small Titolo}} (data)`, dove il gruppo
si chiude PRIMA della data) il default e' `\footnotesize`; nelle itemize non wrappate in
`cveventblock` (es. "Academic projects", che non usa l'ambiente) il default e' l'ambiente
normale, quindi la data ereditava lo `\small` dichiarato esplicitamente a inizio riga per il
titolo, un passo piu' grande di `\footnotesize`. Risultato: la stessa informazione (una data tra
parentesi) appariva a due dimensioni diverse a seconda della sezione, oltre a non distinguersi
graficamente dal resto del testo.

Corretto con un comando dedicato invece di sistemare caso per caso i gruppi di scoping esistenti:

```latex
\newcommand{\itemdate}[1]{{\footnotesize\itshape#1}}
```

Applicato a ciascuna delle 16 date manuali del documento, es. `\itemdate{(01/2021 – 05/2021)}`.
Deliberatamente senza colore: la palette ha `accent` e `subheading` allo stesso `SoftBlue` gia'
usato per i link (`\hypersetup{colorlinks=true, allcolors=accent}`), quindi colorare le date con
uno di questi due le farebbe sembrare cliccabili. Il solo corsivo, a dimensione fissa, basta a
distinguerle dal testo circostante senza introdurre quella ambiguita'.

## Testo giustificato invece di ragged-right

La classe non espone un'opzione documento per la giustificazione: le macro `\cvevent` e
`\cvachievement` chiamano `\raggedright` direttamente nella propria definizione interna (righe
291, 483, 489 di `altacv.cls`), non tramite l'opzione `ragged2e` del documentclass, che si limita
a caricare il pacchetto `ragged2e` senza attivarne di per se' il ragged-right (la vera causa del
testo ragged era quindi interna alla classe, non l'opzione stessa; l'ipotesi opposta nella
Premessa qui sopra riguardava solo l'assenza di un'opzione per centrare, non la giustificazione).

Per passare a un testo giustificato su entrambi i margini (richiesta del 2026-07-06) senza
modificare `altacv.cls`, si ridefinisce `\raggedright` perche' esegua `\justifying` (fornito da
`ragged2e`, gia' caricato):

```latex
\let\raggedright\justifying
```

Punto critico verificato sul campo: questa ridefinizione va fatta *dopo* `\makecvheader`, non nel
preambolo. L'intestazione (nome, tagline, tabella di `\personalinfo`) usa `\raggedright` per il
proprio calcolo di impaginazione interno, e ridefinirlo prima rompe la disposizione di foto e
nome (spostamenti visibili, verificato empiricamente il 2026-07-06). Il fix e' inserire
`\let\raggedright\justifying` subito dopo `\makecvheader` e prima di `\begin{paracol}{2}`: da
quel punto in poi ogni chiamata interna della classe (dentro le due colonne) giustifica, mentre
l'intestazione resta con il ragged-right originale che la classe si aspetta.

## Bug: \ifdefstring di etoolbox non e' edef-safe, si rompe dentro \MakeUppercase

Scoperto il 2026-07-07 durante la prima traduzione completa del CV in tre lingue. Il meccanismo
`\cvtext{italiano}{spagnolo}{inglese}` (Fase 5 di `roadmap.md`) inizialmente confrontava
`\CVlanguage` con `\ifdefstring` di `etoolbox`:

```latex
\newcommand{\cvtext}[3]{%
  \ifdefstring{\CVlanguage}{it}{#1}{%
  \ifdefstring{\CVlanguage}{es}{#2}{#3}}%
}
```

Funzionava correttamente in quasi tutto il documento, ma i titoli di sezione (`\cvsection`)
restavano sempre in inglese anche compilando con `\CVlanguage` impostato su `it` o `es`.
`\cvsection` applica `\MakeUppercase{#2}` al proprio titolo (vedi altacv.cls riga 307): dentro
quel `\MakeUppercase`, `\ifdefstring` valuta sempre la condizione come falsa, cadendo sempre
sull'ultimo ramo (`#3`, inglese) indipendentemente dal valore reale di `\CVlanguage`. Lo stesso
accade dentro un `\edef` di pre-risoluzione (tentativo di fix intermedio, anch'esso fallito):
`\ifdefstring` non e' quindi "edef-safe" in generale, si rompe in qualunque contesto che forzi
l'espansione completa dell'argomento invece della normale esecuzione a runtime.

Diagnosticato con un test isolato fuori dal documento reale (file scratch temporaneo, non
`main.tex`, per non rischiare di introdurre altri problemi durante il debug): confrontando
`\MakeUppercase{\cvtext{...}}` costruito con `\ifdefstring` (fallisce, mostra sempre il terzo
argomento) contro la stessa costruzione con un confronto `\ifx` di TeX puro (funziona
correttamente in tutti e tre gli stati). Fix applicato a `\cvtext` in `main.tex`:

```latex
\def\CVlangIT{it}
\def\CVlangES{es}
\newcommand{\cvtext}[3]{%
  \ifx\CVlanguage\CVlangIT #1\else
  \ifx\CVlanguage\CVlangES #2\else
  #3\fi\fi
}
```

`\ifx` confronta due macro per *definizione*, non per nome: quando `\CVlanguage` vale `it` (cioe'
la sua espansione e' la stringa "it"), `\ifx\CVlanguage\CVlangIT` e' vero perche' `\CVlangIT` ha
la stessa identica definizione (`\def\CVlangIT{it}`). Questo confronto e' un primitivo di TeX
puro, non un meccanismo costruito su `\def` ausiliari come `\ifdefstring`, quindi resta affidabile
dentro `\MakeUppercase`, `\edef`, o qualunque altro contesto di espansione forzata. Lezione
generale per questo progetto: quando un comando condizionale deve funzionare dentro
`\MakeUppercase` (o altri comandi che manipolano token a basso livello, come `\wheelchart` che
fa il proprio parsing di `,`), preferire `\ifx` diretto a `\ifdefstring`/`\ifdefequal` di
etoolbox, che assumono un contesto di esecuzione normale.

## Ridurre il numero di pagine senza tagliare contenuto

Richiesta del 2026-07-06: comprimere il documento nel minor numero di pagine possibile a parita'
di contenuto. Le leve usate, in ordine di intervento:

Uniformare la spaziatura delle liste puntate con un `\setlist[itemize]{...}` globale nel
preambolo (fuori da `cveventblock`), cosi' anche le itemize di "Projects" e "Courses and Events"
(che altrimenti userebbero la spaziatura di default, piu' larga) diventano compatte quanto quelle
di "Work experience".

Convertire i `\medskip` in `\smallskip` in tutto il corpo del documento: con decine di occorrenze
(specialmente tra i molti blocchi `\cvachievement` di "Interests and personal growth"), la somma
e' significativa. Va fatta con un replace globale sul token esatto, poi verificato a mano che non
restino coppie `\smallskip\smallskip` doppie ereditate da `\medskip\medskip` preesistenti.

Restringere i margini di `\geometry` (`top`/`bottom`, poi se serve `left`/`right`): efficace ma
con rendimento decrescente, e con un limite pratico prima che il documento sembri troppo
compresso per la stampa.

Ridurre l'interlinea globale con `\linespread{0.94}` nel preambolo: leva ad alto impatto perche'
si applica a tutto il testo del documento, non solo a punti specifici; una riduzione del 5-6% e'
percettivamente quasi invisibile ma somma su tre pagine di corpo testo.

Bilanciare `\columnratio` in base a quale colonna trabocca per prima (vedi sezione sopra): utile
solo dopo aver gia' ridotto lo spazio totale, perche' da solo sposta il problema da una colonna
all'altra invece di eliminarlo.

[^1]: *ATS*, Applicant Tracking System - software usato dai reparti HR per acquisire, analizzare
e in alcuni casi assegnare un punteggio ai CV prima della valutazione umana.

[^2]: *FontAwesome* - libreria di icone vettoriali distribuita come font, usata da altaCV per i
simboli accanto ai campi di contatto, alle date e alle sezioni del CV.
