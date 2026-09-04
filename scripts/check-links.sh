#!/usr/bin/env bash
# Verifica la raggiungibilità di tutti i link citati dal CV, per categoria.
#
# Equivalente Unix di scripts/check-links.ps1, con la stessa semantica e gli stessi codici di
# uscita. L'elenco dei link arriva dalla proiezione tabellare di tools/extract-cv-links.py, non da
# una regex propria: esiste una sola definizione di cosa sia un link del CV, condivisa con
# l'inventario e con il grafo delle dipendenze.
#
# I redirect si seguono e la destinazione finale viene riportata: è il modo per sapere, senza
# aprire un browser, quali dei dieci redirect tinyurl puntano ancora a Google Drive.
#
# Avvertenza sui tag del blog: uno stato 2xx dice che la topic page esiste, non che il suo
# contenuto sia pertinente all'interesse che la linka.
#
# Codici di uscita: 0 tutto raggiungibile, 1 almeno un errore HTTP, 2 solo errori di rete (che
# possono dipendere dal resolver locale, non dal link).
#
# Uso:
#   bash scripts/check-links.sh
#   bash scripts/check-links.sh --category tinyurl --show-final-url
#   bash scripts/check-links.sh --category skills,projects

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
EXTRACTOR="$PROJECT_ROOT/tools/extract-cv-links.py"

KNOWN_CATEGORIES="contatti skills projects blog proton gdrive tinyurl terzi"
CATEGORY="all"
SHOW_FINAL_URL=0
TIMEOUT=20
MAX_HOPS=5
USER_AGENT="my-cv-check-links"

label_for() {
  case "$1" in
    contatti) echo "Contatti e identità" ;;
    skills)   echo "skills-repo" ;;
    projects) echo "projects" ;;
    blog)     echo "blog" ;;
    proton)   echo "Proton Drive" ;;
    gdrive)   echo "Google Drive" ;;
    tinyurl)  echo "Redirect tinyurl" ;;
    terzi)    echo "Siti di terze parti" ;;
    *)        echo "$1" ;;
  esac
}

usage() {
  echo "uso: bash scripts/check-links.sh [--category <lista>] [--show-final-url] [--timeout N] [--max-hops N]"
  echo "categorie ammesse: all, $(echo "$KNOWN_CATEGORIES" | tr ' ' ',')"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --category) CATEGORY="${2:-}"; shift 2 ;;
    --category=*) CATEGORY="${1#*=}"; shift ;;
    --show-final-url) SHOW_FINAL_URL=1; shift ;;
    --timeout) TIMEOUT="${2:-20}"; shift 2 ;;
    --max-hops) MAX_HOPS="${2:-5}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "[check-links] Argomento non riconosciuto: $1" >&2; usage >&2; exit 64 ;;
  esac
done

if [ "$CATEGORY" = "all" ]; then
  WANTED="$KNOWN_CATEGORIES"
else
  WANTED="$(echo "$CATEGORY" | tr ',' ' ')"
  for c in $WANTED; do
    case " $KNOWN_CATEGORIES " in
      *" $c "*) ;;
      *) echo "[check-links] Categoria non riconosciuta: $c. Ammesse: all, $(echo "$KNOWN_CATEGORIES" | tr ' ' ',')" >&2; exit 64 ;;
    esac
  done
fi

if [ ! -f "$EXTRACTOR" ]; then
  echo "[check-links] Estrattore non trovato: $EXTRACTOR" >&2
  exit 1
fi

ROWS="$(python "$EXTRACTOR" --format urls)" || {
  echo "[check-links] L'estrattore ha restituito un errore." >&2
  exit 1
}

# probe URL MODE -> stampa "codice<TAB>url_finale"; codice 000 significa errore di rete.
# MODE vale "head" per una richiesta HEAD, qualunque altro valore per una GET.
probe() {
  local url="$1" mode="$2"
  if [ "$mode" = "head" ]; then
    curl --silent --location --max-redirs "$MAX_HOPS" --max-time "$TIMEOUT" \
         --user-agent "$USER_AGENT" --head \
         --output /dev/null --write-out '%{http_code}\t%{url_effective}' "$url" 2>/dev/null
  else
    curl --silent --location --max-redirs "$MAX_HOPS" --max-time "$TIMEOUT" \
         --user-agent "$USER_AGENT" \
         --output /dev/null --write-out '%{http_code}\t%{url_effective}' "$url" 2>/dev/null
  fi
}

total=0
skipped=0
unverifiable=0
declare -a failed=()
declare -a warned=()

selected_count=0
while IFS=$'\t' read -r cat lang url; do
  [ -z "${cat:-}" ] && continue
  case " $WANTED " in *" $cat "*) selected_count=$((selected_count + 1)) ;; esac
done <<< "$ROWS"

echo "[check-links] $selected_count URL da verificare, categorie: $(echo "$WANTED" | tr ' ' ',')"
echo

for cat in $KNOWN_CATEGORIES; do
  case " $WANTED " in *" $cat "*) ;; *) continue ;; esac
  group="$(echo "$ROWS" | awk -F'\t' -v c="$cat" '$1==c')"
  [ -z "$group" ] && continue
  echo "$(label_for "$cat") ($(echo "$group" | wc -l | tr -d ' '))"
  while IFS=$'\t' read -r _c lang url; do
    [ -z "${url:-}" ] && continue
    total=$((total + 1))
    prefix=""
    [ "$lang" != "-" ] && prefix="[$lang] "
    # mailto: e tel: non sono risorse HTTP: verificarle non ha significato.
    case "$url" in
      mailto:*|tel:*) skipped=$((skipped + 1)); printf '  SKIP        %s\n' "$url"; continue ;;
    esac
    # I link Proton non sono verificabili via HTTP: /urls/<id> risponde 200 a qualunque
    # identificativo e la chiave dopo il # non raggiunge mai il server. Si controlla la forma.
    if [ "$cat" = "proton" ]; then
      if printf '%s' "$url" | grep -Eq '^https://drive\.proton\.me/urls/[A-Za-z0-9]{10}#.{8,}$'; then
        unverifiable=$((unverifiable + 1))
        keylen=$(printf '%s' "${url#*#}" | tr -d '\n' | wc -c | tr -d ' ')
        printf '  FORMA ok    %s%s  (chiave %s car)\n' "$prefix" "$url" "$keylen"
      else
        failed+=("[$cat] $url (forma inattesa)")
        printf '  FORMA NO    %s%s (atteso /urls/<10 caratteri>#<chiave>)\n' "$prefix" "$url"
      fi
      continue
    fi
    result="$(probe "$url" head)"
    code="${result%%$'\t'*}"
    final="${result#*$'\t'}"
    # Un 405 o un 501 sono il rifiuto del metodo HEAD, non un link rotto: si riprova in GET.
    if [ "$code" = "405" ] || [ "$code" = "501" ]; then
      result="$(probe "$url" get)"
      code="${result%%$'\t'*}"
      final="${result#*$'\t'}"
    fi
    if [ "$code" = "000" ]; then
      warned+=("[$cat] $url")
      printf '  WARN   -   %s%s (errore di rete)\n' "$prefix" "$url"
    elif [ "$code" -ge 200 ] && [ "$code" -lt 300 ]; then
      if [ "$SHOW_FINAL_URL" = "1" ] || [ "$final" != "$url" ]; then
        printf '  OK   %3s   %s%s -> %s\n' "$code" "$prefix" "$url" "$final"
      else
        printf '  OK   %3s   %s%s\n' "$code" "$prefix" "$url"
      fi
    else
      failed+=("[$cat] $url (status $code)")
      printf '  FAIL %3s   %s%s\n' "$code" "$prefix" "$url"
    fi
  done <<< "$group"
  echo
done

if [ "$skipped" -gt 0 ]; then
  echo "[check-links] $skipped non-HTTP saltati (mailto/tel)."
fi
if [ "$unverifiable" -gt 0 ]; then
  echo "[check-links] $unverifiable link Proton con forma corretta ma NON verificabili via HTTP."
  echo "[check-links] La chiave dopo il # non raggiunge mai il server e /urls/<id> risponde 200 a qualunque identificativo: l'unica verifica reale è aprire il link in una finestra privata."
fi
if [ "${#warned[@]}" -gt 0 ]; then
  echo "[check-links] ${#warned[@]} su $total non raggiungibili a livello di rete:"
  for w in "${warned[@]}"; do echo "  ? $w"; done
  echo "[check-links] Un errore di rete può dipendere dal resolver locale: prima di considerare rotto il link, riprovare la risoluzione con un DNS pubblico (nslookup <host> 8.8.8.8)."
fi
if [ "${#failed[@]}" -gt 0 ]; then
  echo "[check-links] ${#failed[@]} su $total hanno risposto con un errore HTTP:"
  for f in "${failed[@]}"; do echo "  - $f"; done
  exit 1
fi
if [ "${#warned[@]}" -gt 0 ]; then
  exit 2
fi
echo "[check-links] Tutti i link verificati sono raggiungibili."
