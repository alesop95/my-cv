---
generated-from-commit: aa8284d604ce0c126c828f775a63f9b3c2b702cb
generated-from-branch: main
generated-date: 2026-07-15
covers-paths:
  - "main.tex"
last-verified-commit: c994a08
---

# Inventario dei link esterni citati nel CV

Elenco completo di ogni URL raggiungibile da `main.tex` (link letterali `\href`, le macro
`\linkedin`/`\github`/`\githubCorp`/`\blog`/`\projectsSite`/`\phone`, e le 16 chiamate
`\bloglinkwrap`/`\bloglink` verso le topic page del blog), 54 link unici alla data sopra.
Ricostruito con lo script di estrazione descritto in fondo alla scheda, non a mano: per
rigenerarlo dopo modifiche a `main.tex`, rilanciare quello script piuttosto che aggiornare le
righe sottostanti manualmente.

## Identità e contatti (5)

| Link | Uso |
|---|---|
| `mailto:alessio.sopranzi.95@gmail.com` | Header |
| `tel:+39 3201950043` | Header |
| `https://linkedin.com/in/alessio-sopranzi` | Header |
| `https://github.com/alesop95` | Header |
| `https://github.com/asopranzi-intrawelt` | Header (GitHub aziendale Intrawelt) |

## Rete di siti satellite propri (24)

Tre siti pubblici mantenuti dallo stesso autore, tutti su GitHub Pages. Vedi
`external-dependencies.md` per come ciascuno viene generato e come verificarne i link.

**skills-repo** (`alesop95.github.io/skills/`, repo `E:\skills`), 6 link:
- Home: `https://alesop95.github.io/skills/` (Skills, sezione "Dettagli completi")
- 5 Capability tecniche sotto `/technical/`: infrastructure-virtualization, leadership-management,
  project-planning-scheduling, cybersecurity-it-governance, fullstack-development-devops
  (tutte sotto Esperienza lavorativa → Intrawelt)

**projects** (`alesop95.github.io/projects/`, repo `E:\projects`), 8 link:
- Home: `https://alesop95.github.io/projects`
- `/company/` (Progetti principali → Progetti aziendali)
- `/company/network-infrastructure-documentation/` (Di cosa sono fiero)
- `/personal/` (Progetti principali → Progetti personali)
- `/personal/harmony-book/` (Interessi → Chitarra e teoria armonica)
- `/academic/` (Progetti accademici)
- `/courses/` (Corsi ed eventi)

**blog** (`alesop95.github.io/blog/`, repo `E:\blog-alessio`), 16 link (tutti da Interessi, via
`\bloglinkwrap`, target IT `/blog/it/tag/<tag>` con fallback EN `/blog/en/tags/<tag>` per ES):
analisi-dati/data-analysis, android, audiofilia/audiophile, collezionismo/collecting,
ecosistema-digitale/digital-ecosystem, finanza-personale/personal-finance, linux,
ottimizzazione-domestica/home-optimization, psicologia/psychology, puzzle/puzzles,
ripetizioni/teaching, songwriting, videogiochi/gaming (13 tag, non 14: "musica"/"music" è stato
tolto il 2026-07-15 quando "Chitarra e teoria armonica" è passata a linkare direttamente
`projects/personal/harmony-book/` invece del tag blog, stesso trattamento di Stampa 3D e Bisogni
Educativi Speciali sotto).

## Google Drive → Proton Drive, migrazione in corso (3/10 fatto)

Vedi la sezione dedicata in `external-dependencies.md` per il piano. Flusso confermato
funzionante il 2026-07-15: carica su Proton Drive (app desktop o mobile) nella cartella
indicata, "Share with anyone" con permesso "Can view" (mai modifica), nessuna password/scadenza
per i file pensati per essere consultati liberamente da chi legge il CV. Attenzione: ogni link
Proton contiene un carattere `#` che in LaTeX va scappato come `\#`, altrimenti la build fallisce.

| Stato | Link Google Drive originale (troncato) | Cosa | Cartella Proton |
|---|---|---|---|
| ✅ fatto | `.../10Fix2VgkGGppyMpVO5t98uLWLYiw4mk2` | Certificato Percorso formativo 24 CFU | Certifications |
| ✅ fatto | `.../1AuoxhnFKHdG9JOFLe0lWNDtXxuUiniGc` | Supplemento al diploma di laurea magistrale (elenco materie/CFU, non l'elaborato di tesi - corretto il 2026-07-16) | Certifications |
| ✅ fatto | `.../1bDc5zx8FScL6RPJToyWeVkla9M2eFoVI` | Attestato Master ISTAO | Certifications |
| da fare | `.../folders/13jewppJEBq8q4wIYuPm0Tfr537edjO81` | Cartella prototipi Stampa 3D | Portfolio |
| da fare | `.../folders/1k-_ZgzrJgkYqf3f5I520qndM_S8HgA5C` | Cartella Bisogni Educativi Speciali | Portfolio |
| da fare | `.../folders/12BgdsaPS-rXPPI41lwpU4a3ZHbshTCNi` | Materiale studio spagnolo in corso | Portfolio |
| da fare | `.../1FzGM9FFX__uIk8BlBm7w7u2bP4W2Jv8Z` | Certificato public speaking e dizione | Certifications |
| da fare | `.../1SY_hhVEVb_BRHdIC3KPAX9xB0RloQlUj` | Recensione personale corso public speaking | Portfolio |
| da fare | `.../1eS5HOIdAQOYIgZ6Zu7NUIhUQN49fZtlT` | Riferimento Sue Johnson (workshop EFT) | References |
| da fare | `.../19jc-MpTL5mdlmXTW2RFm_myuLzoeXkg7` | Certificato "Hold Me Tight" EFT workshop (link diretto, non redirect - riga aggiunta il 2026-07-16, mancava dal tracciamento) | Certifications |
| da fare (redirect) | `tinyurl.com/Tesi-magistrale` → Drive | Vero elaborato di tesi magistrale, "Feature-based characterization of loudspeakers" | Thesis - migrazione = aggiornare la destinazione del redirect tinyurl, non `main.tex` |
| da fare (redirect) | `tinyurl.com/Tesi-trienn` → Drive | Elaborato di tesi triennale | Thesis - stesso discorso, solo redirect |

Nota: `Tesi-magistrale`/`Tesi-trienn` (tinyurl) puntano anch'essi a Drive dietro il redirect
(vedi sezione successiva) - stessa migrazione da fare quando si aggiorna il target del redirect,
senza toccare il link nel CV. Il certificato "Hold Me Tight" invece è un link Drive diretto in
`E:\projects\docs\courses\humanities.md`, non un redirect: va migrato come gli altri 9.

## tinyurl.com - redirect (10)

Tutti puntano a Google Drive dietro al redirect (verificato uno per uno in sessioni precedenti).
Il vantaggio del redirect è che il link nel CV non cambia mai quando cambia la destinazione:
la migrazione a Proton Drive per questi si fa **aggiornando solo il redirect tinyurl**, non
`main.tex`.

`h0mem1` (indirizzo, header), `Intrawelt-location`, `clementoni-site`, `clementoni-location`,
`elettromedia-site`, `elettromedia-location`, `cerolini`, `hundredwords`, `Tesi-magistrale`,
`Tesi-trienn`.

## Siti aziendali/di terzi (6)

`intrawelt.com`, `scenia.it`, `labilia.it`, `rgsound.it/stampa/p-id-45507.html`,
`openforce.it` (ora citato solo su `E:\projects\docs\courses\technical-training.md`, non più
in `main.tex` da quando "Corsi ed eventi" è stata compattata), `contemporanea2-0.it` (idem,
ora su `docs/courses/humanities.md`).

## YouTube (3, ora fuori da main.tex)

Spostati su pagine progetto quando le rispettive sezioni sono state compattate: video Callaghan/
spettacolo teatrale (`docs/courses/humanities.md`), video Festivalle Harmonic Tension Extractor
(`data/personal_overrides/harmonic-tension-vst3.*.md`), video EOLO tv spot (`docs/academic/
eolo-tv-spot.md`).

## Come rigenerare questo inventario

Script Python, non versionato (vive nello scratchpad di sessione, va ricreato se serve):
estrae ogni `\href{URL}` letterale da `main.tex` con una regex a parentesi bilanciate, aggiunge le
URL costruite dalle macro `\linkedin`/`\github`/`\githubCorp`/`\blog`/`\projectsSite`/`\phone`
(prefissi noti in `altacv.cls` via `\NewInfoField`) e da `\bloglink`/`\bloglinkwrap` (template
`https://alesop95.github.io/blog/it/tag/#1` con fallback `/blog/en/tags/#2`, definizione a inizio
`main.tex`). Confrontabile con `git show HEAD:main.tex` per un diff mirato prima/dopo una sessione
di modifiche, così come fatto per l'audit del 2026-07-15 che ha trovato 6 link persi senza
sostituzione durante la compattazione (poi ripristinati, vedi `memory/progress.md`).
