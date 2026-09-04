#!/usr/bin/env bash
# Verifica di coerenza all'apertura della sessione, invocata dall'hook SessionStart.
#
# Perché esiste. `CLAUDE.md` prescriveva di leggere l'indice e invocare `sync-context` a inizio
# sessione, ma quella era una prescrizione all'agente, non un meccanismo: se l'agente dimentica, o
# se la sessione parte con una richiesta urgente, nessuno controlla niente. La differenza fra una
# regola e un meccanismo è esattamente ciò che ha prodotto la deriva dell'inventario dei link e le
# quattro affermazioni false del diagramma di architettura di luglio.
#
# I quattro controlli sono di sola lettura e nessuno modifica un file: segnalano e basta. Girano in
# circa due secondi e mezzo in totale, misurati, quindi non pesano sull'apertura.
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
  "grafo di architettura|python tools/extract-ecosystem.py --check"
)

failed_names=()
details=""

for entry in "${CHECKS[@]}"; do
  name="${entry%%|*}"
  cmd="${entry#*|}"
  out="$(eval "$cmd" 2>&1)"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    failed_names+=("$name")
    details="${details}--- ${name} (exit ${rc}) ---"$'\n'"${out}"$'\n\n'
  fi
done

if [ "${#failed_names[@]}" -eq 0 ]; then
  jq -n --arg m "Stato del progetto coerente: i quattro controlli di apertura passano." \
    '{systemMessage: $m, suppressOutput: true}'
  exit 0
fi

joined=$(printf '%s, ' "${failed_names[@]}")
joined="${joined%, }"

jq -n \
  --arg m "Deriva rilevata all'apertura: ${joined}. Il dettaglio è nel contesto della sessione." \
  --arg ctx "Controlli di apertura falliti. Rigenerare gli artefatti derivati prima di lavorare: python tools/extract-cv-links.py --write per l'inventario dei link, python tools/extract-ecosystem.py --write per il grafo di architettura, python tools/md-unwrap.py <file> per la convenzione Markdown.

${details}" \
  '{systemMessage: $m, hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
exit 0
