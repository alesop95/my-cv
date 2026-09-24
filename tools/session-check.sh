#!/usr/bin/env bash
# Verifica di coerenza all'apertura della sessione, invocata dall'hook SessionStart.
#
# Perché esiste. `CLAUDE.md` prescriveva di leggere l'indice e invocare `sync-context` a inizio
# sessione, ma quella era una prescrizione all'agente, non un meccanismo: se l'agente dimentica, o
# se la sessione parte con una richiesta urgente, nessuno controlla niente. La differenza fra una
# regola e un meccanismo è esattamente ciò che ha prodotto la deriva dell'inventario dei link e le
# quattro affermazioni false del diagramma di architettura di luglio.
#
# Tre dei quattro controlli sono di sola lettura e segnalano soltanto. Il quarto, il grafo di
# architettura, si ripara da solo: dal 2026-09-24, per decisione dell'utente, una sua deriva viene
# rigenerata con `--write` e poi riverificata. La ragione della differenza è che quel grafo misura i
# dischi della macchina e non il repository, quindi deriva ogni volta che nasce o sparisce una
# cartella su D: o E:, senza che sia in gioco alcuna scelta di contenuto; la rigenerazione tocca
# solo la regione generata di `architecture.md`, e il file modificato resta da committare a mano.
# Gli altri tre restano in sola lettura perché una loro deriva nasce da una modifica al sorgente, e
# chi l'ha fatta deve vederla. Girano in circa due secondi e mezzo in totale, misurati, quindi non
# pesano sull'apertura.
#
# Il risultato torna a Claude Code come JSON: `systemMessage` per l'utente, e `additionalContext`
# con l'output reale dei controlli falliti, così l'agente vede la deriva prima di iniziare a
# lavorare invece di scoprirla a metà.
#
# Fuori da questo insieme, deliberatamente: `scripts/check-links.ps1` e `.sh`, che fanno richieste
# HTTP verso una sessantina di URL. Non si eseguono all'apertura di ogni sessione, sia per il tempo
# sia perché un fallimento di rete non è una deriva del progetto.

set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 0

CHECKS=(
  "convenzione Markdown|python tools/md-unwrap.py --check --only-tracked ."
  "comandi nei blocchi|python tools/lint-md-commands.py ."
  "inventario dei link|python tools/extract-cv-links.py --check"
  "grafo di architettura|python tools/extract-ecosystem.py --check|python tools/extract-ecosystem.py --write"
)

# Un terzo campo facoltativo è il comando di riparazione: se il controllo fallisce, lo si esegue e
# si ripete il controllo, e solo se fallisce ancora la voce conta come deriva.
failed_names=()
fixed_names=()
details=""

for entry in "${CHECKS[@]}"; do
  name="${entry%%|*}"
  rest="${entry#*|}"
  cmd="${rest%%|*}"
  fix=""
  [ "$rest" != "$cmd" ] && fix="${rest#*|}"
  out="$(eval "$cmd" 2>&1)"
  rc=$?
  if [ "$rc" -ne 0 ] && [ -n "$fix" ]; then
    eval "$fix" >/dev/null 2>&1
    out="$(eval "$cmd" 2>&1)"
    rc=$?
    [ "$rc" -eq 0 ] && fixed_names+=("$name")
  fi
  if [ "$rc" -ne 0 ]; then
    failed_names+=("$name")
    details="${details}--- ${name} (exit ${rc}) ---"$'\n'"${out}"$'\n\n'
  fi
done

fixed_note=""
if [ "${#fixed_names[@]}" -gt 0 ]; then
  fixed_joined=$(printf '%s, ' "${fixed_names[@]}")
  fixed_note=" Rigenerato in automatico: ${fixed_joined%, }, da committare."
fi

if [ "${#failed_names[@]}" -eq 0 ]; then
  jq -n --arg m "Stato del progetto coerente: i quattro controlli di apertura passano.${fixed_note}" \
    '{systemMessage: $m, suppressOutput: true}'
  exit 0
fi

joined=$(printf '%s, ' "${failed_names[@]}")
joined="${joined%, }"

jq -n \
  --arg m "Deriva rilevata all'apertura: ${joined}. Il dettaglio è nel contesto della sessione.${fixed_note}" \
  --arg ctx "Controlli di apertura falliti. Rigenerare gli artefatti derivati prima di lavorare: python tools/extract-cv-links.py --write per l'inventario dei link, python tools/extract-ecosystem.py --write per il grafo di architettura, python tools/md-unwrap.py <file> per la convenzione Markdown.

${details}" \
  '{systemMessage: $m, hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
exit 0
