#!/bin/bash
# qm_gate61r2.sh — gate61 ROUND 2's Q-M instrument: the round-1 c4_docs_gate61.py (predict | qm) with the ROUND-2 head and the KEEP close tag
# FIXED, so nobody can judge #1383's merge-in against the round-1 head (M2 would fail) or with the round-1 default anchor `carry` (the round-1
# report ruled `keep`). It adds nothing to c4's logic: M0-M7 are c4's. It refuses a caller-supplied --head or --anchor, a non-40-hex sha, and a
# round-1 c4 / lib whose sha256 differs from this kit's kit.json (a tool changed under the verdict).
# Usage:
#   qm_gate61r2.sh predict --repo <YOUR scratch clone> --out <dir> --develop-after <D 40-hex>
#   qm_gate61r2.sh qm      --repo <YOUR scratch clone> --out <dir> --merge-in-head <M 40-hex> --develop-after <D 40-hex>
#   qm_gate61r2.sh --check-args <same args as above>     (validates and prints the exact c4 command; runs nothing, writes nothing)
# The clone must be OUTSIDE /Volumes/DevMASTER (c4's own guard refuses otherwise, rc 2) and must hold the round-2 head, D and M.
# rc: c4's (0 PASS / 1 FAIL / 2 usage), or 2 from this wrapper's own refusals.
set -u
export PYTHONDONTWRITEBYTECODE=1   # importing the round-1 lib must not write __pycache__ into the round-1 kit
GS="$(dirname "$(/bin/realpath "$0")")"
KJ() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$GS/kit.json" "$1"; }
R1="$(KJ round1_kit)"; HEAD="$(KJ head)"
CHECK=0; [ "${1:-}" = "--check-args" ] && { CHECK=1; shift; }
MODE="${1:-}"; shift || true
case "$MODE" in predict|qm) ;; *) echo "REFUSING: mode must be predict or qm (got '$MODE')"; exit 2;; esac
ARGS=("$@"); M=""; D=""; REPO=""; OUT=""
i=0
while [ $i -lt ${#ARGS[@]} ]; do
  a="${ARGS[$i]}"; v="${ARGS[$((i+1))]:-}"
  case "$a" in
    --head|--anchor) echo "REFUSING: $a is FIXED by this wrapper (head $HEAD, anchor keep); do not pass it"; exit 2;;
    --merge-in-head) M="$v";; --develop-after) D="$v";; --repo) REPO="$v";; --out) OUT="$v";;
    *) echo "REFUSING: unknown argument '$a'"; exit 2;;
  esac
  i=$((i+2))
done
for s in "$D" ${M:+"$M"}; do printf '%s' "$s" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: '$s' is not a full 40-hex sha"; exit 2; }; done
[ -n "$D" ] || { echo "REFUSING: --develop-after is required"; exit 2; }
[ "$MODE" = qm ] && [ -z "$M" ] && { echo "REFUSING: qm needs --merge-in-head"; exit 2; }
[ -n "$REPO" ] && [ -n "$OUT" ] || { echo "REFUSING: --repo and --out are required"; exit 2; }
for pair in "c4_docs_gate61.py:round1_c4_sha256" "lib_gate61.py:round1_lib_sha256" "kit.json:round1_kit_json_sha256"; do
  f="${pair%%:*}"; k="${pair##*:}"; got="$(shasum -a 256 "$R1/$f" | awk '{print $1}')"; want="$(KJ "$k")"
  [ "$got" = "$want" ] || { echo "REFUSING: round-1 $f sha256 $got != kit $k $want (the instrument changed under the verdict)"; exit 2; }
done
CMD=(python3 "$R1/c4_docs_gate61.py" "$MODE" --repo "$REPO" --out "$OUT" --head "$HEAD" --develop-after "$D" --anchor keep)
[ "$MODE" = qm ] && CMD+=(--merge-in-head "$M")
echo "qm_gate61r2: round-1 c4/lib/kit sha256 verified; head FIXED $HEAD; anchor FIXED keep"
printf 'command:'; printf ' %q' "${CMD[@]}"; echo
[ "$CHECK" = 1 ] && { echo "CHECK-ARGS OK (nothing run)"; exit 0; }
exec "${CMD[@]}"
