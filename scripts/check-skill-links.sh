#!/bin/sh
# Verifica che i link a skills-repo citati nel .tex principale siano ancora raggiungibili.
# Sezione "Fase 4" di .claude/context/roadmap.md: la tassonomia di skills-repo
# (alesop95.github.io/skills/) non e' congelata, le pagine Capability possono essere
# rinominate, spostate o rimosse. Estrae ogni URL https://alesop95.github.io/skills/...
# citato nel file .tex e verifica con una richiesta HTTP HEAD (curl) che risponda 2xx.
# Da eseguire prima di ogni build definitiva del CV, o periodicamente: non fa parte della
# build stessa.
#
# Uso:
#   sh scripts/check-skill-links.sh [--main FILE.tex]
set -eu

MAIN=""

while [ $# -gt 0 ]; do
  case "$1" in
    --main) MAIN="$2"; shift ;;
    *) echo "[check-skill-links] Argomento sconosciuto: $1" >&2; exit 2 ;;
  esac
  shift
done

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname -- "$SCRIPT_DIR")

if [ -z "$MAIN" ]; then
  set -- "$PROJECT_ROOT"/*.tex
  if [ "$#" -eq 1 ] && [ -f "$1" ]; then
    MAIN="$1"
  elif [ "$#" -eq 0 ] || [ ! -f "$1" ]; then
    echo "[check-skill-links] Nessun .tex nella radice: specifica --main." >&2; exit 1
  else
    echo "[check-skill-links] Piu' .tex nella radice: specifica --main FILE.tex." >&2; exit 1
  fi
elif [ ! -f "$MAIN" ]; then
  MAIN="$PROJECT_ROOT/$MAIN"
fi

URLS=$(grep -oE 'https://alesop95\.github\.io/skills/[A-Za-z0-9/-]+/' "$MAIN" | sort -u || true)

if [ -z "$URLS" ]; then
  echo "[check-skill-links] Nessun link a skills-repo trovato in $MAIN."
  exit 0
fi

COUNT=$(printf '%s\n' "$URLS" | wc -l | tr -d ' ')
echo "[check-skill-links] Verifico $COUNT link a skills-repo citati in $MAIN ..."

BROKEN=0
BROKEN_LIST=""
for url in $URLS; do
  STATUS=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 -I "$url" || echo "000")
  case "$STATUS" in
    2??) echo "  OK    $url" ;;
    *)
      echo "  FAIL  $url (status $STATUS)"
      BROKEN=$((BROKEN + 1))
      BROKEN_LIST="$BROKEN_LIST  - $url\n"
      ;;
  esac
done

echo ""
if [ "$BROKEN" -gt 0 ]; then
  echo "[check-skill-links] $BROKEN di $COUNT link non raggiungibili:"
  printf '%b' "$BROKEN_LIST"
  exit 1
fi

echo "[check-skill-links] Tutti i $COUNT link sono raggiungibili."
