---
generated-from-commit: 1ac5d0078e1a5b9a45f7d70793f28889b6e6ca72
generated-from-branch: main
generated-date: 2026-09-03
covers-paths:
  - "main.tex"
  - "altacv.cls"
  - "tools/extract-cv-links.py"
last-verified-commit: 1ac5d00
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
| projects | 7 | 7 |
| blog | 14 | 27 |
| Proton Drive | 3 | 3 |
| Google Drive | 3 | 3 |
| Redirect tinyurl | 10 | 10 |
| Siti di terze parti | 4 | 4 |
| **Totale** | **52** | **65** |

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
| `https://alesop95.github.io/skills/` | 324, 732 | Esperienza lavorativa, Skills |  |
| `https://alesop95.github.io/skills/technical/infrastructure/infrastructure-virtualization/` | 320 | Esperienza lavorativa |  |
| `https://alesop95.github.io/skills/technical/management/leadership-management/` | 321 | Esperienza lavorativa |  |
| `https://alesop95.github.io/skills/technical/management/project-planning-scheduling/` | 319 | Esperienza lavorativa |  |
| `https://alesop95.github.io/skills/technical/security/cybersecurity-it-governance/` | 323 | Esperienza lavorativa |  |
| `https://alesop95.github.io/skills/technical/software-engineering/fullstack-development-devops/` | 322 | Esperienza lavorativa |  |

### projects (7)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://alesop95.github.io/projects` | 268 | Header |  |
| `https://alesop95.github.io/projects/academic/` | 437 | Progetti principali |  |
| `https://alesop95.github.io/projects/company/` | 402 | Progetti principali |  |
| `https://alesop95.github.io/projects/company/network-infrastructure-documentation/` | 631 | Di cosa sono fiero |  |
| `https://alesop95.github.io/projects/courses/` | 506 | Corsi ed eventi |  |
| `https://alesop95.github.io/projects/personal/` | 416 | Progetti principali |  |
| `https://alesop95.github.io/projects/personal/harmony-book/` | 686 | Interessi |  |

### blog (14)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://alesop95.github.io/blog` | 267 | Header |  |
| `https://alesop95.github.io/blog/it/tag/analisi-dati` | 698 | Interessi | tag `analisi-dati` / `data-analysis` - EN/ES: `https://alesop95.github.io/blog/en/tags/data-analysis` |
| `https://alesop95.github.io/blog/it/tag/android` | 696 | Interessi | tag `android` / `android` - EN/ES: `https://alesop95.github.io/blog/en/tags/android` |
| `https://alesop95.github.io/blog/it/tag/audiofilia` | 687 | Interessi | tag `audiofilia` / `audiophile` - EN/ES: `https://alesop95.github.io/blog/en/tags/audiophile` |
| `https://alesop95.github.io/blog/it/tag/collezionismo` | 690 | Interessi | tag `collezionismo` / `collecting` - EN/ES: `https://alesop95.github.io/blog/en/tags/collecting` |
| `https://alesop95.github.io/blog/it/tag/ecosistema-digitale` | 695 | Interessi | tag `ecosistema-digitale` / `digital-ecosystem` - EN/ES: `https://alesop95.github.io/blog/en/tags/digital-ecosystem` |
| `https://alesop95.github.io/blog/it/tag/finanza-personale` | 688 | Interessi | tag `finanza-personale` / `personal-finance` - EN/ES: `https://alesop95.github.io/blog/en/tags/personal-finance` |
| `https://alesop95.github.io/blog/it/tag/linux` | 694 | Interessi | tag `linux` / `linux` - EN/ES: `https://alesop95.github.io/blog/en/tags/linux` |
| `https://alesop95.github.io/blog/it/tag/ottimizzazione-domestica` | 693 | Interessi | tag `ottimizzazione-domestica` / `home-optimization` - EN/ES: `https://alesop95.github.io/blog/en/tags/home-optimization` |
| `https://alesop95.github.io/blog/it/tag/psicologia` | 692 | Interessi | tag `psicologia` / `psychology` - EN/ES: `https://alesop95.github.io/blog/en/tags/psychology` |
| `https://alesop95.github.io/blog/it/tag/puzzle` | 699 | Interessi | tag `puzzle` / `puzzles` - EN/ES: `https://alesop95.github.io/blog/en/tags/puzzles` |
| `https://alesop95.github.io/blog/it/tag/ripetizioni` | 691 | Interessi | tag `ripetizioni` / `teaching` - EN/ES: `https://alesop95.github.io/blog/en/tags/teaching` |
| `https://alesop95.github.io/blog/it/tag/songwriting` | 701 | Interessi | tag `songwriting` / `songwriting` - EN/ES: `https://alesop95.github.io/blog/en/tags/songwriting` |
| `https://alesop95.github.io/blog/it/tag/videogiochi` | 689 | Interessi | tag `videogiochi` / `gaming` - EN/ES: `https://alesop95.github.io/blog/en/tags/gaming` |

### Proton Drive (3)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://drive.proton.me/urls/08GSDD51FC#Sl9ZV3ExCWC-` | 555 | Istruzione |  |
| `https://drive.proton.me/urls/W1H29CBYHM#U0UQezNeHjvW` | 577 | Istruzione |  |
| `https://drive.proton.me/urls/Y0YWKXG708#-VO43ecQ-A2j` | 594 | Istruzione |  |

### Google Drive (3)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://drive.google.com/drive/folders/13jewppJEBq8q4wIYuPm0Tfr537edjO81?usp=drive_link` | 697 | Interessi |  |
| `https://drive.google.com/drive/folders/1k-_ZgzrJgkYqf3f5I520qndM_S8HgA5C?usp=drive_link` | 700 | Interessi |  |
| `https://drive.google.com/drive/u/1/folders/12BgdsaPS-rXPPI41lwpU4a3ZHbshTCNi` | 649 | Lingue |  |

### Redirect tinyurl (10)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://tinyurl.com/Intrawelt-location` | 308 | Esperienza lavorativa |  |
| `https://tinyurl.com/Tesi-magistrale` | 559 | Istruzione |  |
| `https://tinyurl.com/Tesi-trienn` | 567 | Istruzione |  |
| `https://tinyurl.com/cerolini` | 392 | Esperienza lavorativa |  |
| `https://tinyurl.com/clementoni-location` | 338 | Esperienza lavorativa |  |
| `https://tinyurl.com/clementoni-site` | 335 | Esperienza lavorativa |  |
| `https://tinyurl.com/elettromedia-location` | 358 | Esperienza lavorativa |  |
| `https://tinyurl.com/elettromedia-site` | 355 | Esperienza lavorativa |  |
| `https://tinyurl.com/h0mem1` | 263 | Header |  |
| `https://tinyurl.com/hundredwords` | 636 | Di cosa sono fiero |  |

### Siti di terze parti (4)

| URL | Riga | Sezione del CV | Nota |
|---|---|---|---|
| `https://intrawelt.com` | 305 | Esperienza lavorativa |  |
| `https://scenia.it/` | 406 | Progetti principali |  |
| `https://www.labilia.it/` | 391 | Esperienza lavorativa |  |
| `https://www.rgsound.it/stampa/p-id-45507.html` | 637 | Di cosa sono fiero |  |

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

Il lavoro residuo si divide in tre insiemi disgiunti, che si migrano in modi diversi e appartengono a repository diversi. Tenerli in un'unica tabella, come faceva la versione precedente di questa scheda, faceva sembrare lavoro di questo repository anche ciò che non lo è.

Primo insieme, tre link ancora citati da `main.tex`: si migrano sostituendo l'argomento di `\href` nel sorgente, ricompilando e verificando il conteggio pagine.

| Cosa | Cartella Proton | Dove nel CV |
|---|---|---|
| Cartella prototipi Stampa 3D | `Portfolio` | Interessi |
| Cartella Bisogni Educativi Speciali | `Portfolio` | Interessi |
| Materiale di studio dello spagnolo | `Portfolio` | Lingue |

Secondo insieme, due redirect di tesi: si migrano aggiornando la destinazione del redirect sul pannello tinyurl, senza toccare `main.tex`. È il vantaggio strutturale del redirect, e il motivo per cui i link di tesi nel CV non cambiano mai. La destinazione effettiva si verifica senza aprire un browser con `pwsh scripts/check-links.ps1 -Category tinyurl -FollowRedirects`, che riporta l'URL finale di ogni redirect.

| Redirect | Cosa | Cartella Proton |
|---|---|---|
| `tinyurl.com/Tesi-magistrale` | Elaborato di tesi magistrale, "Feature-based characterization of loudspeakers" | `Thesis` |
| `tinyurl.com/Tesi-trienn` | Elaborato di tesi triennale | `Thesis` |

Terzo insieme, nove file nelle pagine del repository `projects`: sono lavoro di quel repository, non di questo, e la loro migrazione va pianificata là. Quattro erano già tracciati come usciti dal CV nel luglio 2026 quando "Corsi ed eventi" e "Progetti accademici" sono state compattate; cinque non erano tracciati da nessuna parte prima del 2026-09-03, e li ha scoperti il secondo salto dell'estrattore.

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

## Raggiungibilità verificata il 2026-09-03

Prima verifica automatica estesa a tutte le categorie, eseguita con `scripts/check-links.ps1` e riverificata con `curl` in GET sui casi negativi, per escludere che un errore fosse il rifiuto del metodo HEAD invece di una risposta reale. Esito per categoria: raggiungibili tutti e 5 i contatti HTTP, i 6 link a `skills-repo`, le 7 pagine di `projects`, le 27 URL del blog e i 3 link Proton; raggiungibili anche tutti e 10 i redirect tinyurl, nel senso che il redirect funziona.

Il risultato che conta, però, è negativo, e riguarda i documenti di archivio.

| Link | Esito | Lettura |
|---|---|---|
| Cartella Stampa 3D (`13jewpp...`) | 404 in HEAD e in GET, nessun redirect | non apribile da un lettore anonimo |
| Cartella Bisogni Educativi Speciali (`1k-_Zgz...`) | redirect alla pagina di accesso di Google | richiede autenticazione |
| Materiale di studio dello spagnolo (`12Bgdsa...`) | 404 in HEAD e in GET | non apribile, e la URL porta un prefisso `/u/1/` |
| Target di `tinyurl.com/Tesi-magistrale` | 401 in GET su `drive.google.com/file/d/1IsA_k4n3kN-aN7k15qZ6RbwHvVzBFUJ4/view` | non pubblico |
| Target di `tinyurl.com/Tesi-trienn` | redirect alla pagina di accesso su `drive.google.com/file/d/1ImfQH5jVxXkvgVd8DHWF8VRAkjjDgSpa/view` | non pubblico |

Due note di lettura, perché la differenza fra ciò che è verificato e ciò che è inferito qui conta. Un 404 di Google Drive su una risorsa non condivisa è indistinguibile dall'esterno da una risorsa che non esiste più: si può affermare che chi legge il CV non apre quei documenti, non che i file siano stati cancellati. Il prefisso `/u/1/` della URL dello studio dello spagnolo, invece, è un difetto certo e diagnosticabile a vista: lega la URL all'account con indice 1 nella sessione di chi l'ha generata, quindi quel link non è mai stato condivisibile con nessuno.

I due ID Drive dietro i redirect di tesi sono stati risolti qui per la prima volta: non erano registrati da nessuna parte, e servono per ritrovare i file da caricare su Proton.

## Tre link deliberatamente commentati

Il sorgente contiene tre `\href` dentro righe commentate, che l'estrattore scarta per costruzione neutralizzando i commenti prima di qualunque ricerca: la riga Telegram rimossa il 2026-07-14, il certificato 24 CFU commentato sotto la voce Istruzione, e la vecchia riga "Thesis" della magistrale. Non compaiono nell'inventario perché non sono link del CV, ma restano nel sorgente per essere riattivabili senza riscriverli.

## Nota sulla verifica dei tag del blog

Uno stato HTTP 2xx su una topic page del blog dice che la pagina esiste, non che il suo contenuto sia pertinente all'interesse che la linka. È stato verificato concretamente il 2026-07-15 sul tag "musica", raggiungibile ma privo di qualunque riferimento al progetto harmony-book a cui l'interesse "Chitarra e teoria armonica" puntava; da allora quell'interesse linka direttamente la pagina del progetto. Il controllo di pertinenza si fa sul sorgente del blog, cercando il tag nel frontmatter di `content/posts/<lingua>/*.mdx`, non sullo stato della pagina.
