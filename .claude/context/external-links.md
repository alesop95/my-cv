---
generated-from-commit: 1ac5d0078e1a5b9a45f7d70793f28889b6e6ca72
generated-from-branch: main
generated-date: 2026-09-03
covers-paths:
  - "main.tex"
  - "altacv.cls"
  - "tools/extract-cv-links.py"
last-verified-commit: 330249e
---

# Inventario dei link citati dal CV

Inventario completo di ogni link raggiungibile dal CV, per categoria, con il numero di riga di `main.tex` e la sezione del documento in cui compare. Le tabelle di questa scheda sono un artefatto derivato: le genera `tools/extract-cv-links.py` leggendo il sorgente, e non si aggiornano a mano. La prosa attorno alle regioni marcate, invece, è scritta a mano e contiene le decisioni e gli stati di avanzamento che nessuno strumento può dedurre dal sorgente.

Il perimetro comprende due livelli. Il primo è `main.tex`, cioè i link che il CV contiene direttamente. Il secondo sono le pagine di dettaglio del repository `projects` a cui il CV delega quattro sezioni intere ("Progetti aziendali", "Progetti personali", "Progetti accademici", "Corsi ed eventi") più due pagine linkate singolarmente: sono la seconda sponda del percorso che il lettore del CV compie davvero quando clicca "Dettagli", e i documenti di archivio che vivono lì erano finora fuori da ogni tracciamento.

Come rigenerare l'inventario dopo una modifica a `main.tex`, e come verificarlo prima di un commit.

```powershell
python tools/extract-cv-links.py --write
python tools/extract-cv-links.py --check
```

```bash
python tools/extract-cv-links.py --write
python tools/extract-cv-links.py --check
```

Perché lo strumento esiste, dato che questa scheda fino al 2026-09-03 dichiarava già di essere stata ricostruita con uno script di estrazione. Quello script viveva nello scratchpad di sessione e andava ricreato ogni volta, quindi l'inventario era di fatto prosa scritta a mano, e la deriva era misurabile: dichiarava cinquantaquattro link contro i cinquantadue bersagli reali, attribuiva otto pagine a `projects` elencandone sette e sedici link al blog dove i tag sono tredici, nominava le cinque Capability tecniche senza il segmento di categoria che gli URL reali contengono, e soprattutto teneva in un'unica tabella di migrazione due insiemi disgiunti, i link ancora presenti nel CV e quelli che nel luglio 2026 si erano trasferiti sulle pagine di `projects`. Un artefatto derivato che nessuno strumento rigenera deriva: non è una questione di disciplina ma di meccanismo.

## Distinzione fra bersagli e stringhe URL

Le due colonne del riepilogo non misurano la stessa cosa, e confonderle è ciò che ha prodotto il conteggio sbagliato della versione precedente di questa scheda. Un bersaglio è una risorsa distinta a cui il CV punta; una stringa URL è una forma testuale che compare nel PDF compilato. I tredici tag del blog valgono tredici bersagli e ventisei stringhe, perché ciascuno esiste in una variante italiana e in una inglese, e la compilazione spagnola ricade sulla seconda dato che il blog non ha una terza lingua. Nessun'altra categoria ha varianti di lingua, quindi altrove le due colonne coincidono.

<!-- BEGIN GENERATED cv-links: inventario -->

### Riepilogo per categoria

| Categoria | Bersagli | Stringhe URL |
|---|---|---|
| Contatti e identità | 5 | 5 |
| skills-repo | 6 | 6 |
| projects | 8 | 8 |
| blog | 16 | 31 |
| Proton Drive | 5 | 5 |
| Google Drive | 0 | 0 |
| Redirect tinyurl | 8 | 8 |
| Siti di terze parti | 4 | 4 |
| **Totale** | **52** | **67** |

### Contatti e identità (5)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://github.com/alesop95` | 265 | Header |  |
| `https://github.com/asopranzi-intrawelt` | 266 | Header |  |
| `https://linkedin.com/in/alessio-sopranzi` | 264 | Header |  |
| `mailto:alessio.sopranzi.95@gmail.com` | 261 | Header |  |
| `tel:+39 3201950043` | 262 | Header |  |

### skills-repo (6)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://alesop95.github.io/skills/` | 324, 753 | Esperienza lavorativa, Skills |  |
| `https://alesop95.github.io/skills/technical/infrastructure/infrastructure-virtualization/` | 320 | Esperienza lavorativa |  |
| `https://alesop95.github.io/skills/technical/management/leadership-management/` | 321 | Esperienza lavorativa |  |
| `https://alesop95.github.io/skills/technical/management/project-planning-scheduling/` | 319 | Esperienza lavorativa |  |
| `https://alesop95.github.io/skills/technical/security/cybersecurity-it-governance/` | 323 | Esperienza lavorativa |  |
| `https://alesop95.github.io/skills/technical/software-engineering/fullstack-development-devops/` | 322 | Esperienza lavorativa |  |

### projects (8)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://alesop95.github.io/projects` | 268 | Header |  |
| `https://alesop95.github.io/projects/academic/` | 437 | Progetti principali |  |
| `https://alesop95.github.io/projects/company/` | 402 | Progetti principali |  |
| `https://alesop95.github.io/projects/company/network-infrastructure-documentation/` | 637 | Di cosa sono fiero |  |
| `https://alesop95.github.io/projects/courses/` | 506 | Corsi ed eventi |  |
| `https://alesop95.github.io/projects/personal/` | 416 | Progetti principali |  |
| `https://alesop95.github.io/projects/personal/harmony-book/` | 707 | Interessi |  |
| `https://alesop95.github.io/projects/personal/spanish-learning/` | 664 | Lingue |  |

### blog (16)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://alesop95.github.io/blog` | 267 | Header |  |
| `https://alesop95.github.io/blog/it/tag/analisi-dati` | 719 | Interessi | tag `analisi-dati` / `data-analysis` - EN/ES: `https://alesop95.github.io/blog/en/tags/data-analysis` |
| `https://alesop95.github.io/blog/it/tag/android` | 717 | Interessi | tag `android` / `android` - EN/ES: `https://alesop95.github.io/blog/en/tags/android` |
| `https://alesop95.github.io/blog/it/tag/audiofilia` | 708 | Interessi | tag `audiofilia` / `audiophile` - EN/ES: `https://alesop95.github.io/blog/en/tags/audiophile` |
| `https://alesop95.github.io/blog/it/tag/collezionismo` | 711 | Interessi | tag `collezionismo` / `collecting` - EN/ES: `https://alesop95.github.io/blog/en/tags/collecting` |
| `https://alesop95.github.io/blog/it/tag/ecosistema-digitale` | 716 | Interessi | tag `ecosistema-digitale` / `digital-ecosystem` - EN/ES: `https://alesop95.github.io/blog/en/tags/digital-ecosystem` |
| `https://alesop95.github.io/blog/it/tag/finanza-personale` | 709 | Interessi | tag `finanza-personale` / `personal-finance` - EN/ES: `https://alesop95.github.io/blog/en/tags/personal-finance` |
| `https://alesop95.github.io/blog/it/tag/linux` | 715 | Interessi | tag `linux` / `linux` - EN/ES: `https://alesop95.github.io/blog/en/tags/linux` |
| `https://alesop95.github.io/blog/it/tag/ottimizzazione-domestica` | 714 | Interessi | tag `ottimizzazione-domestica` / `home-optimization` - EN/ES: `https://alesop95.github.io/blog/en/tags/home-optimization` |
| `https://alesop95.github.io/blog/it/tag/pedagogia` | 721 | Interessi | tag `pedagogia` / `education-theory` - EN/ES: `https://alesop95.github.io/blog/en/tags/education-theory` |
| `https://alesop95.github.io/blog/it/tag/psicologia` | 713 | Interessi | tag `psicologia` / `psychology` - EN/ES: `https://alesop95.github.io/blog/en/tags/psychology` |
| `https://alesop95.github.io/blog/it/tag/puzzle` | 720 | Interessi | tag `puzzle` / `puzzles` - EN/ES: `https://alesop95.github.io/blog/en/tags/puzzles` |
| `https://alesop95.github.io/blog/it/tag/ripetizioni` | 712 | Interessi | tag `ripetizioni` / `teaching` - EN/ES: `https://alesop95.github.io/blog/en/tags/teaching` |
| `https://alesop95.github.io/blog/it/tag/songwriting` | 722 | Interessi | tag `songwriting` / `songwriting` - EN/ES: `https://alesop95.github.io/blog/en/tags/songwriting` |
| `https://alesop95.github.io/blog/it/tag/stampa-3d` | 718 | Interessi | tag `stampa-3d` / `3d-printing` - EN/ES: `https://alesop95.github.io/blog/en/tags/3d-printing` |
| `https://alesop95.github.io/blog/it/tag/videogiochi` | 710 | Interessi | tag `videogiochi` / `gaming` - EN/ES: `https://alesop95.github.io/blog/en/tags/gaming` |

### Proton Drive (5)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://drive.proton.me/urls/08GSDD51FC#Sl9ZV3ExCWC-` | 555 | Istruzione |  |
| `https://drive.proton.me/urls/1YR8GEJF4M#1tEN9WAaB_e9` | 573 | Istruzione |  |
| `https://drive.proton.me/urls/6FBQ5M2JG0#s_IgqhLKnby-` | 564 | Istruzione |  |
| `https://drive.proton.me/urls/W1H29CBYHM#U0UQezNeHjvW` | 583 | Istruzione |  |
| `https://drive.proton.me/urls/Y0YWKXG708#-VO43ecQ-A2j` | 600 | Istruzione |  |

### Redirect tinyurl (8)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://tinyurl.com/Intrawelt-location` | 308 | Esperienza lavorativa |  |
| `https://tinyurl.com/cerolini` | 392 | Esperienza lavorativa |  |
| `https://tinyurl.com/clementoni-location` | 338 | Esperienza lavorativa |  |
| `https://tinyurl.com/clementoni-site` | 335 | Esperienza lavorativa |  |
| `https://tinyurl.com/elettromedia-location` | 358 | Esperienza lavorativa |  |
| `https://tinyurl.com/elettromedia-site` | 355 | Esperienza lavorativa |  |
| `https://tinyurl.com/h0mem1` | 263 | Header |  |
| `https://tinyurl.com/hundredwords` | 642 | Di cosa sono fiero |  |

### Siti di terze parti (4)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://intrawelt.com` | 305 | Esperienza lavorativa |  |
| `https://scenia.it/` | 406 | Progetti principali |  |
| `https://www.labilia.it/` | 391 | Esperienza lavorativa |  |
| `https://www.rgsound.it/stampa/p-id-45507.html` | 643 | Di cosa sono fiero |  |

### Secondo salto: pagine di dettaglio in `projects`

| Rimando dal CV | Cartella o pagina | File | Link esterni | |
|---|---|---|---|---|
| `/projects` | `docs/index` | 3 | 6 |  |
| `/projects/company/` | `docs/company` | 42 | 9 |  |
| `/projects/personal/` | `docs/personal` | 93 | 96 |  |
| `/projects/academic/` | `docs/academic` | 4 | 3 |  |
| `/projects/courses/` | `docs/courses` | 3 | 10 |  |
| `/projects/company/network-infrastructure-documentation/` | `docs/company/network-infrastructure-documentation` | 3 | 0 | sottoinsieme della riga di sezione |
| `/projects/personal/harmony-book/` | `docs/personal/harmony-book` | 3 | 3 | sottoinsieme della riga di sezione |

Le due righe marcate come sottoinsieme sono pagine di dettaglio che il CV linka direttamente ma che stanno dentro una sezione linkata per intero: le loro colonne non si sommano alle altre, mentre i bersagli restano corretti perché deduplicati per URL.

I 31 repository `github.com` distinti (93 occorrenze nelle pagine `/personal/`, moltiplicate dalle varianti di lingua) sono generati da `scripts/update_personal_projects.py` e valgono un solo nodo aggregato: non sono manutenzione manuale del CV.

| Host | Bersagli |
|---|---|
| `drive.google.com` | 9 |
| `youtube.com` | 2 |
| `alesop95.github.io` | 1 |
| `contemporanea2-0.it` | 1 |
| `guide.univpm.it` | 1 |
| `klippel.de` | 1 |
| `openforce.it` | 1 |
| `scenia.it` | 1 |
| `github.com` (aggregato) | 31 |

| Bersaglio | Host | Pagine che lo citano |
|---|---|---|
| `https://alesop95.github.io/skills/` | `alesop95.github.io` | `docs/index.en.md`, `docs/index.es.md`, `docs/index.md` |
| `https://www.contemporanea2-0.it/landing-dizione/` | `contemporanea2-0.it` | `docs/courses/humanities.md` |
| `https://drive.google.com/file/d/19jc-MpTL5mdlmXTW2RFm_myuLzoeXkg7/view?usp=...` | `drive.google.com` | `docs/courses/humanities.md` |
| `https://drive.google.com/file/d/1FzGM9FFX__uIk8BlBm7w7u2bP4W2Jv8Z/view?usp=...` | `drive.google.com` | `docs/courses/humanities.md` |
| `https://drive.google.com/file/d/1N0UwI3dExQAdXNcg4RRWr1Z4s7J45c5S/view?usp=...` | `drive.google.com` | `docs/academic/eolo-tv-spot.md` |
| `https://drive.google.com/file/d/1SY_hhVEVb_BRHdIC3KPAX9xB0RloQlUj/view?usp=...` | `drive.google.com` | `docs/courses/humanities.md` |
| `https://drive.google.com/file/d/1W6TS1cJAvJIVbbDPXks47_ELpmxMrD7K/view` | `drive.google.com` | `docs/courses/technical-training.md` |
| `https://drive.google.com/file/d/1eS5HOIdAQOYIgZ6Zu7NUIhUQN49fZtlT/view?usp=...` | `drive.google.com` | `docs/courses/humanities.md` |
| `https://drive.google.com/file/d/1mBimN4uUJW4we3oNSqjRNWTAyJeGdqY9/view` | `drive.google.com` | `docs/courses/technical-training.md` |
| `https://drive.google.com/file/d/1rcLwkmahByoFxohc8-fUiOFDsGwrRSnk/view?usp=...` | `drive.google.com` | `docs/academic/channel-estimation-mimo.md` |
| `https://drive.google.com/file/d/1zAWtISx8ASWQVDsE84zTjYZjaEvbSz6l/view?usp=...` | `drive.google.com` | `docs/personal/harmonic-tension-vst3.en.md`, `docs/personal/harmonic-tension-vst3.es.md`, `docs/personal/harmonic-tension-vst3.md` |
| `https://guide.univpm.it/af.php?af=113475` | `guide.univpm.it` | `docs/academic/nonlinear-devices-guitar-speakers.md` |
| `https://www.klippel.de/fileadmin/klippel/Files/News/VIRTUAL%20LECTURE%20202...` | `klippel.de` | `docs/courses/technical-training.md` |
| `https://www.openforce.it/` | `openforce.it` | `docs/courses/technical-training.md` |
| `https://scenia.it/` | `scenia.it` | `docs/company/index.en.md`, `docs/company/index.es.md`, `docs/company/index.md`, `docs/company/translation-service-portal.en.md`, `docs/company/translation-service-portal.es.md`, `docs/company/translation-service-portal.md` |
| `https://www.youtube.com/watch?v=RFfEyYXSV2s` | `youtube.com` | `docs/courses/humanities.md` |
| `https://www.youtube.com/watch?v=wB-U9s4ASQo` | `youtube.com` | `docs/personal/harmonic-tension-vst3.en.md`, `docs/personal/harmonic-tension-vst3.es.md`, `docs/personal/harmonic-tension-vst3.md` |

<!-- END GENERATED cv-links: inventario -->

## Migrazione da Google Drive a Proton Drive

Il flusso è confermato funzionante dal 2026-07-15: si carica su Proton Drive, dall'app desktop o mobile, nella cartella indicata; si condivide con "Share with anyone" e permesso "Can view", mai di modifica; nessuna password e nessuna scadenza per i documenti pensati per essere consultati liberamente da chi legge il CV. Avvertenza tecnica: ogni link Proton contiene un carattere `#`, che in LaTeX va scappato come `\#` altrimenti la build fallisce. Lo strumento di estrazione de-escapizza quel carattere, quindi l'inventario mostra la URL reale e non la forma scritta nel sorgente.

Il lavoro residuo è un solo insieme, i nove file nelle pagine del repository `projects`. Gli altri due si sono chiusi in due giorni e in due modi diversi, entrambi istruttivi. I tre link Drive che il CV citava direttamente sono usciti dal sorgente il 2026-09-03 senza passare da Proton, perché per tutti e tre la risposta giusta era rimandare a una pagina descrittiva invece che a un archivio: il dettaglio è nella sezione successiva e vale come precedente. I due elaborati di tesi sono invece migrati su Proton il 2026-09-04, perché sono documenti singoli e non alberi, ed è il caso in cui un allegato è la forma giusta.

Insieme chiuso il 2026-09-04, i due elaborati di tesi. Fino al 2026-09-04 erano raggiunti da due redirect tinyurl, e la scelta registrata è di ritirarli: i due `\href` di `main.tex` puntano direttamente ai link Proton e i redirect escono dal CV. La destinazione di un redirect si ispeziona con `powershell -NoProfile -File scripts/check-links.ps1 -Category tinyurl`, che segue i reindirizzamenti e riporta l'URL finale; è così che i due target di tesi sono stati risolti per la prima volta.

| Elaborato | Link nel CV prima | Link nel CV ora | ID Drive di provenienza |
|---|---|---|---|
| Magistrale, "Feature-based characterization of loudspeakers" | `tinyurl.com/Tesi-magistrale` | `drive.proton.me/urls/6FBQ5M2JG0` | `1IsA_k4n3kN-aN7k15qZ6RbwHvVzBFUJ4` |
| Triennale, "Study and development of synchronization systems performances for gps-based WSN" | `tinyurl.com/Tesi-trienn` | `drive.proton.me/urls/1YR8GEJF4M` | `1ImfQH5jVxXkvgVd8DHWF8VRAkjjDgSpa` |

Perché i redirect sono stati ritirati invece di essere riconfigurati. Il vantaggio dell'indirezione è che il link nel CV non cambia mai quando cambia la destinazione; il costo è che la destinazione reale è invisibile a chi legge il sorgente, ed è esattamente così che entrambi i link di tesi sono rimasti puntati per mesi a documenti non pubblici, uno con 401 e uno con reindirizzamento al login, senza che nessuno se ne accorgesse. Ora che `check-links` segue i redirect quel costo è mitigato ma non annullato, e un'indirezione in meno è un posto in meno dove la verità può nascondersi.

Trappola verificata su questo passaggio, da conoscere prima del prossimo link Proton. Il link della magistrale è arrivato con la chiave di decifratura troncata a nove caratteri invece di dodici, e una chiave troncata rende il link inservibile senza che alcun controllo automatico possa accorgersene, perché il frammento dopo il `#` non viene mai inviato al server. L'indizio disponibile è solo la lunghezza: tutte e cinque le chiavi Proton oggi nel CV sono di dodici caratteri, e `check-links -Category proton` la riporta per ciascuna proprio per rendere visibile un troncamento. Verificato inoltre che nel PDF compilato l'URI dell'annotazione contiene la chiave completa, che è il punto in cui un `\#` mal gestito si manifesterebbe.

Secondo insieme, nove file nelle pagine del repository `projects`: sono lavoro di quel repository, non di questo, e la loro migrazione va pianificata là. Quattro erano già tracciati come usciti dal CV nel luglio 2026 quando "Corsi ed eventi" e "Progetti accademici" sono state compattate; cinque non erano tracciati da nessuna parte prima del 2026-09-03, e li ha scoperti il secondo salto dell'estrattore.

| File Drive | Pagina che lo cita | Tracciato prima |
|---|---|---|
| Certificato public speaking e dizione | `docs/courses/humanities.md` | sì |
| Recensione personale del corso di public speaking | `docs/courses/humanities.md` | sì |
| Riferimento Sue Johnson, workshop EFT | `docs/courses/humanities.md` | sì |
| Certificato "Hold Me Tight", workshop EFT | `docs/courses/humanities.md` | sì |
| Documento del progetto harmonic-tension VST3 | `docs/personal/harmonic-tension-vst3.md` e varianti | no |
| Channel Estimation MIMO | `docs/academic/channel-estimation-mimo.md` | no |
| Spot televisivo EOLO | `docs/academic/eolo-tv-spot.md` | no |
| Due documenti di formazione tecnica | `docs/courses/technical-training.md` | no |

Memo confermato: durante la migrazione i file restano anche su Google Drive, e si cancellano da là solo a migrazione verificata end-to-end su tutti i documenti, cioè link Proton raggiungibile e contenuto corretto.

## Chiusura dei tre link Drive del CV, 2026-09-03

I tre link Google Drive che `main.tex` citava direttamente sono usciti tutti e tre dal sorgente, e nessuno dei tre è finito su Proton Drive. Vale registrare perché, perché è un precedente che si applica al prossimo caso simile: quando un link del CV punta a un archivio di materiali, la domanda giusta non è dove spostare l'archivio ma che cosa deve leggere chi clicca.

| Voce del CV | Dove puntava | Dove punta ora | Perché |
|---|---|---|---|
| Interessi, Stampa 3D | cartella Drive `13jewpp...` | topic del blog `stampa-3d` / `3d-printing` | il registro dei topic del blog conteneva già la voce, con la descrizione editoriale identica al testo tagliato dal CV il 2026-07-13 |
| Interessi, Bisogni Educativi Speciali | cartella Drive `1k-_Zgz...` | topic del blog `pedagogia` / `education-theory` | idem, e un albero di sottocartelle di materiale di studio non è leggibile da un estraneo mentre un abstract lo è |
| Lingue, studio in corso | cartella Drive `12Bgdsa...` con prefisso `/u/1/` | pagina di progetto `projects/personal/spanish-learning/` | lo studio dello spagnolo è diventato un repository con una pagina pubblicata e descrittiva |

Le due voci degli Interessi erano le uniche due eccezioni alla convenzione generale del CV, per cui il titolo di un interesse rimanda alla propria topic page: sono rientrate nella regola invece di essere migrate. Con questo `main.tex` non contiene più alcun link a Google Drive, e la categoria `gdrive` dell'inventario è a zero.

Nota sulle topic page del blog, che smentisce un allarme che sembrava fondato. Dodici dei quindici tag citati dal CV non hanno alcun post che li porti, verificato sul frontmatter dei tredici post esistenti e non sullo stato HTTP. Non è un difetto: `src/config/topics.ts` del repository del blog definisce un *topic* come area di interesse curata che riceve una descrizione editoriale sulla propria pagina anche prima che esista un articolo, per decisione registrata come ADR-018 in quel repository. Le pagine rendono quell'abstract, verificato su tutte e quattro le nuove.

## Raggiungibilità verificata il 2026-09-03

Prima verifica automatica estesa a tutte le categorie, eseguita con `scripts/check-links.ps1` e riverificata con `curl` in GET sui casi negativi, per escludere che un errore fosse il rifiuto del metodo HEAD invece di una risposta reale. Esito per categoria: raggiungibili tutti e 5 i contatti HTTP, i 6 link a `skills-repo`, le 7 pagine di `projects`, le 27 URL del blog e i 3 link Proton; raggiungibili anche tutti e 10 i redirect tinyurl, nel senso che il redirect funziona.

Il risultato che conta, però, è negativo, e riguarda i documenti di archivio.

| Link | Esito | Lettura |
|---|---|---|
| Cartella Stampa 3D (`13jewpp...`) | 404 in HEAD e in GET, nessun redirect; 404 anche per il proprietario | contenuto non più a quell'ID, link poi rimosso dal CV |
| Cartella Bisogni Educativi Speciali (`1k-_Zgz...`) | redirect alla pagina di accesso di Google, esiste per il proprietario | richiede autenticazione, link poi rimosso dal CV |
| Materiale di studio dello spagnolo (`12Bgdsa...`) | 404 in HEAD e in GET, 404 anche per il proprietario | non apribile, e la URL portava un prefisso `/u/1/`; link poi rimosso dal CV |
| I nove file Drive nelle pagine di `projects` | 401 tutti e nove | nessuno è pubblico; lavoro del repository `projects` |
| Target di `tinyurl.com/Tesi-magistrale` | 401 in GET su `drive.google.com/file/d/1IsA_k4n3kN-aN7k15qZ6RbwHvVzBFUJ4/view` | non pubblico |
| Target di `tinyurl.com/Tesi-trienn` | redirect alla pagina di accesso su `drive.google.com/file/d/1ImfQH5jVxXkvgVd8DHWF8VRAkjjDgSpa/view` | non pubblico |

Due note di lettura, perché la differenza fra ciò che è verificato e ciò che è inferito qui conta. Un 404 di Google Drive su una risorsa non condivisa è indistinguibile dall'esterno da una risorsa che non esiste più: si può affermare che chi legge il CV non apre quei documenti, non che i file siano stati cancellati. Il prefisso `/u/1/` della URL dello studio dello spagnolo, invece, è un difetto certo e diagnosticabile a vista: lega la URL all'account con indice 1 nella sessione di chi l'ha generata, quindi quel link non è mai stato condivisibile con nessuno.

I due ID Drive dietro i redirect di tesi sono stati risolti qui per la prima volta: non erano registrati da nessuna parte, e servono per ritrovare i file da caricare su Proton.

## Tre link deliberatamente commentati

Il sorgente contiene tre `\href` dentro righe commentate, che l'estrattore scarta per costruzione neutralizzando i commenti prima di qualunque ricerca: la riga Telegram rimossa il 2026-07-14, il certificato 24 CFU commentato sotto la voce Istruzione, e la vecchia riga "Thesis" della magistrale. Non compaiono nell'inventario perché non sono link del CV, ma restano nel sorgente per essere riattivabili senza riscriverli.

## Nota sulla verifica dei tag del blog

Uno stato HTTP 2xx su una topic page del blog dice che la pagina esiste, non che il suo contenuto sia pertinente all'interesse che la linka. È stato verificato concretamente il 2026-07-15 sul tag "musica", raggiungibile ma privo di qualunque riferimento al progetto harmony-book a cui l'interesse "Chitarra e teoria armonica" puntava; da allora quell'interesse linka direttamente la pagina del progetto. Il controllo di pertinenza si fa sul sorgente del blog, cercando il tag nel frontmatter di `content/posts/<lingua>/*.mdx`, non sullo stato della pagina.
