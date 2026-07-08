#!/bin/sh
# Compila main.tex nelle tre lingue (EN/IT/ES) producendo tre PDF datati e nominati.
# Sezione "Fase 5" di .claude/context/roadmap.md: main.tex e' parametrizzato per lingua tramite
# \CVlanguage (\providecommand, default "en") e la macro \cvtext{italiano}{spagnolo}{inglese}.
# Compila una volta per lingua iniettando "\providecommand\CVlanguage{<lingua>}\input{main.tex}"
# come argomento di pdflatex al posto del nome file (main.tex usa \providecommand, non
# \newcommand, quindi l'iniezione esterna vince senza errori "gia' definito").
#
# Compila con pdflatex direttamente, non con latexmk: due passaggi fissi, sufficienti per questo
# documento (hyperref/pdfx richiedono un secondo passaggio, osservato nelle build reali). Non usa
# latexmk perche' l'argomento iniettato non e' un vero nome di file, comprometterebbe la sua
# analisi delle dipendenze, comunque inutile per una singola build pulita come questa.
#
# I PDF prodotti si chiamano cv-sopranzi-alessio-<lingua>-<AAAA-MM-GG>.pdf, raccolti in
# sottocartelle separate per lingua sotto OUT_DIR (OUT_DIR/en/, OUT_DIR/it/, OUT_DIR/es/): a
# differenza di main.pdf (un solo file che si aggiorna, versionato per ADR-004), questi PDF
# datati si accumulano nel tempo, e le sottocartelle per lingua evitano che si mescolino tutti
# insieme dopo settimane di build (richiesta del 2026-07-07). Il nome del file mantiene comunque
# la lingua, cosi' resta riconoscibile anche se estratto dalla cartella. Senza componente oraria
# nel nome, rilanciare lo script piu' volte lo stesso giorno sovrascrive semplicemente il file di
# quel giorno, mentre le date diverse restano distinte come istantanee storiche.
#
# Uso:
#   sh scripts/build-multilang.sh [--main FILE.tex] [--out-dir DIR] [--tex-dir DIR]
set -eu

MAIN=""
OUT_DIR=""
TEX_DIR=""

while [ $# -gt 0 ]; do
  case "$1" in
    --main)     MAIN="$2"; shift ;;
    --out-dir)  OUT_DIR="$2"; shift ;;
    --tex-dir)  TEX_DIR="$2"; shift ;;
    *) echo "[build-multilang] Argomento sconosciuto: $1" >&2; exit 2 ;;
  esac
  shift
done

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname -- "$SCRIPT_DIR")
[ -n "$MAIN" ]    || MAIN="$PROJECT_ROOT/main.tex"
[ -n "$OUT_DIR" ] || OUT_DIR="$PROJECT_ROOT/dated-builds"
[ -n "$TEX_DIR" ] || TEX_DIR="$HOME/.TinyTeX"

[ -f "$MAIN" ] || { echo "[build-multilang] File non trovato: $MAIN" >&2; exit 1; }

find_pdflatex() {
  if command -v pdflatex >/dev/null 2>&1; then command -v pdflatex; return 0; fi
  for p in "$TEX_DIR"/bin/*/pdflatex; do
    [ -x "$p" ] && { echo "$p"; return 0; }
  done
  return 1
}

PDFLATEX=$(find_pdflatex) || { echo "[build-multilang] pdflatex non trovato. Esegui prima sh scripts/setup-tex.sh." >&2; exit 1; }

DATE=$(date +%Y-%m-%d)
MAIN_DIR=$(dirname -- "$MAIN")
MAIN_NAME=$(basename -- "$MAIN" .tex)

cd "$MAIN_DIR"

for lang in en it es; do
  JOBNAME="cv-sopranzi-alessio-$lang-$DATE"
  LANG_DIR="$OUT_DIR/$lang"
  mkdir -p "$LANG_DIR"
  TEX_INPUT="\\providecommand\\CVlanguage{$lang}\\input{$MAIN_NAME.tex}"
  echo "[build-multilang] Compilo $MAIN_NAME.tex in lingua '$lang' -> $lang/$JOBNAME.pdf ..."
  for pass in 1 2; do
    if ! "$PDFLATEX" -interaction=nonstopmode -halt-on-error -synctex=1 -file-line-error "-jobname=$JOBNAME" "$TEX_INPUT" >/dev/null; then
      echo "[build-multilang] Compilazione fallita (lingua $lang, passaggio $pass). Vedi $JOBNAME.log." >&2
      exit 1
    fi
  done
  [ -f "$JOBNAME.pdf" ] || { echo "[build-multilang] PDF non prodotto per la lingua $lang: $JOBNAME.pdf" >&2; exit 1; }
  # Sposta TUTTI i file di questo jobname (pdf, aux, log, out, synctex.gz), non solo il pdf:
  # pdflatex li scrive sempre in MAIN_DIR (la radice del progetto), e senza questo spostamento
  # restavano li' a sporcare la root a ogni build (richiesta del 2026-07-08).
  for f in "$JOBNAME".*; do
    [ -f "$f" ] && mv -f "$f" "$LANG_DIR/$f"
  done
  echo "[build-multilang] Fatto: $LANG_DIR/$JOBNAME.pdf"
done

echo ""
echo "[build-multilang] Tutte le lingue compilate in $OUT_DIR."
