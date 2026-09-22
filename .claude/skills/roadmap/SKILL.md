---
description: >
  Rigenera la roadmap operativa di my-cv e del suo ecosistema allo stato corrente, fondendo le
  voci aperte di tools/roadmap-items.yml con lo stato misurato dal vivo (commit, deriva dei due
  artefatti generati, convenzione Markdown, raggiungibilita dei link). Produce anche una pagina
  pronta da stampare. Usare quando serve sapere che cosa resta da fare, a inizio sessione o prima
  di decidere su che cosa lavorare.
---

## Roadmap allo stato corrente

!`python tools/roadmap.py`

## Che cosa hai davanti

La lista qui sopra non è un documento scritto a mano: è un derivato, rigenerato a ogni invocazione. Le voci, cioè il giudizio su quale lavoro resti e perché, vivono in `tools/roadmap-items.yml` ed è l'unico file che si modifica a mano. Tutto il resto, cioè il commit di riferimento, la distanza delle schede da HEAD, la deriva del grafo di architettura e dell'inventario dei link, la convenzione Markdown e la raggiungibilità dei link, viene misurato sul momento da `tools/roadmap.py`.

Le voci sono ordinate per costo crescente. Il livello 0 si chiude in minuti e non richiede alcuna decisione, il livello 1 in mezz'ora e non richiede decisioni di contenuto, il livello 2 richiede una decisione dell'utente sul contenuto del CV, il livello 3 è lavoro che non si chiude dentro questo repository e va portato in una sessione sul repository che lo ospita.

La sezione finale, "chiuse dalla misura", elenca le voci che una sonda ha dichiarato non più aperte. Una sonda è un controllo automatico dichiarato nel file dati: la presenza o l'assenza di una stringa in un file, oppure l'esito di uno dei tre controlli documentali. Serve a impedire che la lista dichiari aperto un difetto già corretto, che è l'errore trovato il 2026-09-22 sulla voce "Hold Me Tight". Una voce chiusa dalla misura va tolta dal file dati quando qualcuno conferma che il lavoro è davvero finito, non prima.

## Come si usa

Per la sola lista a schermo basta questa skill. Per gli altri usi si invoca lo strumento direttamente.

```
python tools/roadmap.py                        # riepilogo a schermo, come qui sopra
python tools/roadmap.py --link-check           # aggiunge la verifica HTTP di tutti i link del CV
python tools/roadmap.py --format md --write    # Markdown in build/roadmap-<data>.md
python tools/roadmap.py --format html --write  # pagina da stampare in build/roadmap-<data>.html
python tools/roadmap.py --format json          # stato ispezionabile, per un altro strumento
python tools/roadmap.py --check                # exit 1 se resta aperta una voce di livello 0
```

La verifica dei link è esclusa dall'esecuzione di default perché va in rete e impiega circa un minuto: si aggiunge con `--link-check` quando serve davvero, tipicamente prima di inviare il CV o dopo un lavoro su `skills-repo`, `projects` o il blog. Da sapere quando la si legge: i cinque link Proton non sono verificabili in HTTP per costruzione, perché l'identificativo risponde a qualunque valore e la chiave dopo il cancelletto non raggiunge mai il server, quindi lo strumento ne controlla la sola forma. E `intrawelt.com` risulta irraggiungibile su questa macchina per un limite del resolver locale, non perché il sito sia giù: con DNS pubblico risponde.

## Per stamparla

La resa HTML è pensata per la carta: A4, serif, margini di 14 millimetri, nessuna voce spezzata a metà fra due pagine, link non sottolineati in stampa. Si genera e si apre così.

```
python tools/roadmap.py --format html --write
start build\roadmap-2026-09-22.html
```

Dal browser si stampa con la funzione di stampa, che legge il foglio di stile dedicato. Il file vive in `build/`, che è ignorato da git: è un derivato e si rigenera, non si versiona.

## Dove finisce questa lista e dove comincia la memoria

Questa skill non scrive in alcun file tracciato e non aggiorna le schede. Quando una voce viene davvero chiusa, le due cose da fare sono toglierla da `tools/roadmap-items.yml` e aggiornare a mano la scheda che la citava, tipicamente `.claude/memory/index.md` per i difetti noti o la mappa dello stato in testa a `.claude/context/roadmap.md`. La regola di team resta quella: l'agente non scrive nei file di memoria e di contesto senza richiesta esplicita.
