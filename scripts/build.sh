#!/bin/sh
# Compila main.tex nelle tre lingue (EN/IT/ES), sovrascrivendo i tre PDF stabili versionati.
#
# Sostituisce la build a lingua singola (via latexmk) del 2026-07-06: da quando main.tex e'
# parametrizzato per lingua (\CVlanguage), l'utente ha chiesto (2026-07-08) che ogni
# ricompilazione aggiorni sempre e comunque tutte e tre le lingue insieme, cosi' che un commit
# non possa mai lasciarne una disallineata dalle altre.
#
# Produce cv-sopranzi-alessio-en.pdf, cv-sopranzi-alessio-it.pdf, cv-sopranzi-alessio-es.pdf nella
# radice del progetto: nomi stabili (nessuna data), pensati per essere versionati in git come link
# diretto e sempre aggiornato al CV in ciascuna lingua (estende ADR-004 alle tre lingue). Diverso
# da scripts/build-multilang.sh, che produce invece istantanee DATATE in dated-builds/<lingua>/,
# un archivio storico locale non versionato (ADR-005): i due script coesistono per due scopi
# diversi, build.sh e' quello da lanciare prima di ogni commit.
#
# Compila con pdflatex direttamente (due passaggi fissi), non con latexmk, per lo stesso motivo di
# build-multilang.sh: l'argomento "-jobname" iniettato non e' un vero nome di file e
# comprometterebbe l'analisi delle dipendenze di latexmk.
#
# Uso:
#   sh scripts/build.sh [--main FILE.tex] [--tex-dir DIR] [--clean]
set -eu

MAIN=""
TEX_DIR=""
CLEAN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --main)     MAIN="$2"; shift ;;
    --tex-dir)  TEX_DIR="$2"; shift ;;
    --clean)    CLEAN=1 ;;
    *) echo "[build] Argomento sconosciuto: $1" >&2; exit 2 ;;
  esac
  shift
done

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname -- "$SCRIPT_DIR")
[ -n "$MAIN" ]    || MAIN="$PROJECT_ROOT/main.tex"
[ -n "$TEX_DIR" ] || TEX_DIR="$HOME/.TinyTeX"

MAIN_DIR=$(dirname -- "$MAIN")
MAIN_NAME=$(basename -- "$MAIN" .tex)

if [ "$CLEAN" -eq 1 ]; then
  for lang in en it es; do
    rm -f "$MAIN_DIR"/cv-sopranzi-alessio-"$lang".*
  done
  echo "[build] Rimossi i PDF stabili e gli ausiliari nelle tre lingue."
  exit 0
fi

[ -f "$MAIN" ] || { echo "[build] File non trovato: $MAIN" >&2; exit 1; }

find_pdflatex() {
  if command -v pdflatex >/dev/null 2>&1; then command -v pdflatex; return 0; fi
  for p in "$TEX_DIR"/bin/*/pdflatex; do
    [ -x "$p" ] && { echo "$p"; return 0; }
  done
  return 1
}

PDFLATEX=$(find_pdflatex) || { echo "[build] pdflatex non trovato. Esegui prima sh scripts/setup-tex.sh." >&2; exit 1; }

cd "$MAIN_DIR"

for lang in en it es; do
  JOBNAME="cv-sopranzi-alessio-$lang"
  TEX_INPUT="\\providecommand\\CVlanguage{$lang}\\input{$MAIN_NAME.tex}"
  echo "[build] Compilo $MAIN_NAME.tex in lingua '$lang' -> $JOBNAME.pdf ..."
  for pass in 1 2; do
    if ! "$PDFLATEX" -interaction=nonstopmode -halt-on-error -synctex=1 -file-line-error "-jobname=$JOBNAME" "$TEX_INPUT" >/dev/null; then
      echo "[build] Compilazione fallita (lingua $lang, passaggio $pass). Vedi $JOBNAME.log." >&2
      exit 1
    fi
  done
  [ -f "$JOBNAME.pdf" ] || { echo "[build] PDF non prodotto per la lingua $lang: $JOBNAME.pdf" >&2; exit 1; }
  echo "[build] Fatto: $MAIN_DIR/$JOBNAME.pdf"
done

echo ""
echo "[build] Tutte e tre le lingue aggiornate nella radice del progetto."
