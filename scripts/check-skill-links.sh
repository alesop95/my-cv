#!/bin/sh
# Involucro storico: verifica i soli link a skills-repo invocando scripts/check-links.sh.
#
# Fino al 2026-09-03 questo script conteneva una propria estrazione a grep dei soli URL
# https://alesop95.github.io/skills/... citati nel .tex, e verificava 5 link sui 52 bersagli del
# CV. Quella logica è stata generalizzata in scripts/check-links.sh, che prende l'elenco dei link
# dalla proiezione tabellare di tools/extract-cv-links.py e copre tutte le categorie.
#
# Il nome resta perché è citato per nome in .claude/context/deployment.md, nella Fase 4 di
# .claude/context/roadmap.md e nel registro delle decisioni: un rinvio esplicito costa meno di una
# caccia ai riferimenti, e mantiene valida la documentazione storica.
#
# Per verificare tutto il CV, non solo skills-repo, usare direttamente:
#   bash scripts/check-links.sh
#
# Uso:
#   sh scripts/check-skill-links.sh
set -eu

while [ $# -gt 0 ]; do
  case "$1" in
    --main)
      # Accettato e ignorato: l'elenco dei link non viene più ricavato da un .tex passato a mano
      # ma dall'estrattore, che conosce main.tex, altacv.cls e i template delle macro.
      echo "[check-skill-links] Il parametro --main non ha più effetto: l'elenco dei link arriva da tools/extract-cv-links.py."
      shift 2
      ;;
    *) echo "[check-skill-links] Argomento sconosciuto: $1" >&2; exit 2 ;;
  esac
done

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

echo "[check-skill-links] Involucro su check-links.sh --category skills."
exec bash "$SCRIPT_DIR/check-links.sh" --category skills
