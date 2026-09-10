# Snapshot di sincronizzazione

> Da leggere per primo a inizio sessione. Fotografa lo stato del progetto al commit di riferimento e mappa ogni scheda al suo stato di verifica.

## Stato

```
Branch attivo:         main
Commit di riferimento: abb3ef4 (2026-09-09, "Topologia del mirror: perimetro del sync locale e capienza corretta")
Data snapshot:         2026-09-09
```

Dal bootstrap (3485498) sono arrivati quaranta commit. Il CV è completo, trilingue e sta su una pagina sola in tutte e tre le lingue. Il working tree era pulito al momento dello snapshot; le modifiche della passata di sincronizzazione che ha prodotto questo file attendono un commit manuale, come da vincoli di team.

Nota di ripresa dopo un incidente, che vale conservare perché è la ragione per cui questo file è stato riscritto. La sessione del 2026-09-08 è terminata per crash, e la verifica su disco ha stabilito che il crash non ha perso lavoro: i tre commit di quella giornata erano tutti presenti e il working tree era pulito. Il costo è stato la manutenzione di fine sessione, che non era stata eseguita, e si è manifestato come deriva del grafo di architettura, rilevata dall'hook di apertura, e come dodici commit di distanza fra le schede e HEAD. Il rilievo generale è che i commit sopravvivono a un crash e la memoria no, quindi la manutenzione di fine sessione non è una formalità.

Seconda chiusura anomala, il 2026-09-09, e la stessa lezione confermata con un dettaglio nuovo. La sessione si è fermata subito dopo la verifica locale del microstep 1 della Fase 7, lasciando senza risposta la verifica del caricamento in cloud, la voce di work-log e due decisioni. Anche qui nessun lavoro perso e working tree pulito; la differenza è che l'operazione è proseguita dopo la fine della sessione e per mano dell'utente, quindi la trascrizione non bastava a ricostruirne lo stato ed è servito leggere i log del client Proton e gli attributi dei file su disco. La regola che ne esce, in `progress.md` per esteso: lo stato di un'operazione che vive fuori dal repository si ricostruisce dai log del sistema che l'ha eseguita, e la trascrizione dice soltanto fin dove l'agente ha guardato.

## Stato di verifica delle schede

Tutte e nove le schede di `.claude/context/` sono ancorate a `abb3ef4`. Nessuna porta più il segnaposto `PENDING-FIRST-COMMIT`. Il riancoraggio dal precedente `67c3561` è stato di solo frontmatter, senza alcun delta di contenuto, e la ragione è verificata e non assunta: fra i due commit sono cambiati soltanto file sotto `.claude/`, nessuno dei quali compare nelle `covers-paths` di alcuna scheda. La colonna di stato qui sotto descrive quindi l'ultima verifica di merito, che risale al 2026-09-08, e non una verifica nuova.

| Scheda | last-verified | Stato |
|---|---|---|
| STACK.md | abb3ef4 | i derivati in `build/` e la riga dedicata nel `.gitignore` |
| altacv-reference.md | abb3ef4 | verificata, nessuna modifica necessaria |
| architecture.md | abb3ef4 | regione generata rigenerata, `D:` da ventitre a ventiquattro cartelle |
| current-work.md | abb3ef4 | sezione di stato riscritta sugli allegati verificati, titolo riancorato |
| deployment.md | abb3ef4 | derivati in `build/`, e l'avvertenza sul flag `-Clean` che non li rimuove più |
| dev-testing.md | abb3ef4 | il log di compilazione si legge in `build/` |
| external-dependencies.md | abb3ef4 | stato al 2026-09-08, struttura Proton fissata, `folder-sync-watcher` |
| external-links.md | abb3ef4 | verificata, porta già la tabella dei dodici link |
| roadmap.md | abb3ef4 | Fase 3 chiusa, Fase 7 con i due obiettivi separati |

Meta-stato, sotto `.claude/memory/`, fuori dalla tabella perché non porta frontmatter di riconciliazione: questo file aggiornato al 2026-09-09, `progress.md` con in testa la voce del microstep 1 della Fase 7, `decisions.md` con ADR-011 e con l'emendamento del 2026-09-08 ad ADR-010.

## Punto di ripresa

Il CV è completo e non ha sezioni in lavorazione: struttura a due colonne su classe altaCV vendorizzata, contenuto trilingue IT/EN/ES tramite `\CVlanguage` e `\cvtext{}{}{}`, skill allineate alla tassonomia di `skills-repo` con script di verifica dei link, tre PDF stabili `cv-sopranzi-alessio-{en,it,es}.pdf` versionati in radice e sempre rigenerati insieme da `scripts/build.ps1`, con i derivati di compilazione in `build/` dal 2026-09-04, più un archivio storico datato in `dated-builds/` non versionato (ADR-004, 005 e 006 in `decisions.md`). Il formato attuale è una pagina sola in tutte e tre le lingue: ogni aggiunta di contenuto va compensata con un taglio altrove, e va verificata prima sullo spagnolo, che è la lingua che sconfina per prima.

Lavoro chiuso il 2026-09-08 e precondizione di tutto il resto della Fase 7: l'anonimizzazione alla fonte dei quattro file del sottoalbero specchiato con la OneDrive aziendale, decisa in ADR-011. I quattro originali sono stati sostituiti dalle versioni anonimizzate e verificati per md5, gli originali pre-intervento sono conservati in `J:\_originali-prima-anonimizzazione\` e verificati fedeli, e la cartella di lavoro `J:\_anonimizzati\` è stata rimossa a verifica compiuta. Con questo cade la premessa che teneva `Ongoing studies` fuori dallo spostamento su Proton, che era il punto su cui la fase si era incagliata.

Il punto di ripresa vero è dentro il microstep 1 della Fase 7, che è stato eseguito il 2026-09-09 e non è ancora chiuso. Tre delle quattro cartelle candidate, cioè `IT-RELATED`, `Progetti (consulenza)` e `Progetti (idee)`, sono state copiate nella cartella locale del client Proton sotto `My files\Portfolio and ongoing studies`, 1994 file per 315,6 MB verificati per SHA256, e il client le ha caricate in cloud nella passata del pomeriggio. Restano tre cose, tutte descritte nella voce del 2026-09-09 di `progress.md`: riavviare il client, che è terminato per un guasto della sua interfaccia a propagazione già finita, e confermare che non restano operazioni pendenti; risolvere il file di conflitto che una transazione fallita ha prodotto sotto `pycparser-2.22.dist-info/`, tenendo presente che una rimozione dentro quella cartella si propaga al cloud; e rendere le tre cartelle disponibili solo online, perché su questa macchina aziendale in locale deve restare soltanto il sottoalbero anonimizzato.

Le misure valide sono quelle del 2026-09-09 e non quelle registrate il 2026-09-04: `IT-RELATED` 308,5 MB, `Progetti (consulenza)` 4,7 MB, `Progetti (idee)` 2,4 MB e `Ongoing studies` 1939,7 MB, per un totale di circa 2,26 GB invece di 2,53. La capienza non è un vincolo.

Da non presentare come chiuso, per decisione dell'utente del 2026-09-09: la sorgente su `J:\googleDrive_sync` resta dov'è, quindi l'obiettivo A della Fase 7 è raggiunto come copia su Proton e non come archivio unico. La rimozione della sorgente si decide come passo separato, e fino a quel momento ADR-009 resta rispettato alla lettera.

Il passo successivo del filone, non ancora fatto, è lo spostamento di `Ongoing studies`, che è l'unica delle quattro con un mirror aziendale e per questo dipende dal watcher. La topologia del mirror è stata decisa il 2026-09-08 ed è la più semplice: `C:\Scripts\folder-sync-watcher` resta bidirezionale con la OneDrive aziendale e con la stessa politica di conflitto, e si allinea alla stessa cartella nella sua nuova posizione dentro l'albero locale di Proton. Cambia il percorso, non il comportamento. Le tre condizioni che quella scelta richiede stanno nella Fase 7 di `roadmap.md` con le misure che le motivano, e la dipendenza in sé è descritta in `context/external-dependencies.md`. Il vincolo da non violare, perché la macchina è aziendale, è che l'unico oggetto del sync locale sono i file di studio anonimizzati per ADR-011: il resto di Proton resta solo in cloud, e il pin si dichiara per quel sottoalbero e non in blocco. La modifica al codice del watcher si fa in una sessione dedicata sul suo repository, per decisione dell'utente del 2026-09-09, e non da qui: quel progetto ha una propria memoria e farla da fuori la lascerebbe disallineata.

Il fatto nuovo di settembre sul CV, e il più rilevante per chi riprende quel lato, è che il perimetro dei link è chiuso. `drive.google.com` è a zero sia in `main.tex` sia nelle pagine del repository `projects`, i dodici link Proton che ne risultano sono stati aperti in finestra privata e verificati end-to-end il 2026-09-08, e i due redirect tinyurl delle tesi sono stati ritirati. Nulla è stato cancellato da Google Drive, per ADR-009, e Drive resta come copia dormiente. Il seguito non è più sui link ma sull'archivio, ed è la Fase 7.

Fasi della roadmap, con il dettaglio completo in `roadmap.md`.

- Fase 1 (bootstrap tecnico): completata il 2026-07-06.
- Fase 2 (contenuti pendenti): quasi chiusa. Restano fuori "Ongoing studies", ancora disattivata con `\iffalse` e `\fi` e piena di segnaposto `aaaaaaa`, e i frammenti Coaching (Onova S.p.A. e Intracademy), rimandati per mancanza di esperienza reale da raccontare. La sezione Consultant è invece esclusa in via definitiva per motivi fiscali, non rimandata. Fatto rilevato il 2026-09-04 che cambia la natura del primo punto: il materiale di studio in corso esiste e pesa 2,0 GB, quindi "Ongoing studies" non è più un problema di contenuto assente ma di contenuto non selezionato.
- Fase 3 (gestione documentale degli allegati): completata il 2026-09-07 e verificata il 2026-09-08. I cinque documenti che `main.tex` linka stanno su Proton, i sette delle pagine di `projects` pure, due asset non sono stati migrati ma rimossi con motivazione, e tutti e dodici i link risultanti sono verificati end-to-end. La struttura di Proton è fissata in quattro cartelle e non va riorganizzata, perché un link Proton è legato alla copia specifica del file e spostarla lo rompe: è già successo una volta, il 2026-09-07, invalidando dodici link in un colpo.
- Fase 4 (allineamento skill a skills-repo): in gran parte completata il 2026-07-06. La verifica automatica dei link, nata come `check-skill-links` sui soli cinque link di `skills-repo`, è stata generalizzata il 2026-09-03 in `scripts/check-links.ps1` e `.sh` su tutte le categorie, con seguito dei redirect.
- Fase 5 (multilingua): completata. Traduzione integrale il 2026-07-07, bug di `\ifdefstring` non edef-safe diagnosticato e corretto con `\ifx`, verificata con build reali nelle tre lingue. Deliberatamente non fatta la revisione madrelingua dello spagnolo: resta un rischio da sciogliere prima di un uso professionale reale di quella versione.
- Fase 6 (ATS-safety del layout): rimandata a data da destinarsi per quel che riguarda l'ordine di lettura delle colonne. Il problema distinto del layer testuale del PDF è invece risolto e versionato con `7ea1955`, con `\decoicon` e le etichette esplicite di `\printinfo`: motivazione in ADR-007, dettagli tecnici in `context/altacv-reference.md`.
- Fase 7 (riordino dell'archivio documentale, e la sua narrazione): aperta il 2026-09-04, ed è il punto di ripresa vero. Il chiarimento del 2026-09-08 ne separa i due obiettivi, che hanno percorsi diversi e non si ostacolano. Il primo è avere un archivio solo, e riguarda tutte e quattro le cartelle candidate, cioè `Ongoing studies` (1939,7 MB), `IT-RELATED` (308,5 MB), `Progetti (consulenza)` (4,7 MB) e `Progetti (idee)` (2,4 MB), per circa 2,26 GB misurati il 2026-09-09 contro i 3,24 GB liberi: `Ongoing studies` è dentro, non fuori, perché l'anonimizzazione di ADR-011 ha rimosso la sola cosa che la escludeva. Le tre cartelle senza mirror aziendale sono state copiate su Proton il 2026-09-09 e caricate in cloud, con la chiusura del microstep descritta nel punto di ripresa qui sopra; resta `Ongoing studies`, che comporta il riorientamento di `C:\Scripts\folder-sync-watcher` secondo la topologia decisa. Il secondo obiettivo è dare valore a competenze reali che oggi non compaiono da nessuna parte, e non passa dallo spostamento dei file ma dalla pipeline di `lettore-doc` verso `skills-repo`, che il CV già linka. Per il materiale che non è di studio ma di portfolio, il primo passo resta classificare cartella per cartella se il contenuto va pubblicato come allegato, raccontato in una pagina o lasciato dove è.

Repository correlati, tutti sotto `E:` e distinti da questo, citati dal CV: `skills-repo` (tassonomia delle competenze, pubblicata su `alesop95.github.io/skills/`), `projects` (navigator dei progetti personali e aziendali), il blog personale, e `fiscal-toolkit` insieme a `legal-consultant` per il materiale fiscale e normativo. Le dipendenze verso questi siti, e cosa fare quando cambiano, stanno in `context/external-dependencies.md`; l'architettura complessiva in quattro bande, con il grafo generato, sta in `context/architecture.md`.

## Difetti noti e non ancora corretti

Tre difetti verificati che nessuno ha ancora chiuso, elencati qui perché una sessione nuova li incontrerebbe senza preavviso.

Il flag `-Clean` di `scripts/build.ps1` e `--clean` di `scripts/build.sh` non rimuovono più i file ausiliari: dal riordino della radice del 2026-09-04 quei file vivono in `build/` mentre entrambi gli script spazzano la sola cartella di `main.tex`, e il messaggio finale continua ad annunciare una rimozione che non avviene. Per svuotare davvero i derivati si cancella `build/`.

Gli strumenti di normalizzazione tipografica sotto `tools/` non preservano la fine riga dei file su cui passano, e hanno convertito `main.tex` da LF a CRLF il 2026-08-27 gonfiandone il diff da 41 righe reali a 1462. Il file è stato riportato a LF, gli strumenti non sono stati corretti.

Una virgoletta di chiusura dritta invece che tipografica resta nella voce "Hold Me Tight" della sezione dei corsi, difetto pre-esistente e mai corretto.

Commit e push restano manuali dell'utente, come da vincoli di team.
