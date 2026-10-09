#!/bin/bash
# hosted/check.sh <run_dir> <tier> <tip> <work_dir> [<golden.diff>] — the checker leg of a hosted replay (2026-10-09).
#
# This is spark/round.sh steps 7 (clone + prepare), 9 (checker) and 10 (golden) with the SAME scripts, in the SAME
# order, with the SAME arguments — sequencing copied from round.sh, no checker reimplemented:
#   code_patch   tasks/code_patch/prepare_clone.sh, then tasks/code_patch/spark_checker.sh (checker.sh + A2a)
#   code_patch2  tasks/code_patch/prepare_clone.sh, then tasks/code_patch2/checker.sh + A2a (as round.sh)
#   bash_patch   tasks/bash_patch/checker.sh + A2a (sections_with_n.json + code_patch/a2a_anchor.py)
#   bash_patch2  tasks/bash_patch2/checker.sh + A2a
# The clone is `git clone --shared --no-checkout spark/cache/src` + `checkout --detach <tip>` (the tip the Spark round
# used, from its round.json), under <work_dir>/clone. Writes checker.out, out.md.checker/, prepare_clone.out,
# golden_cmp.out into <run_dir>. Prints ONE last line:  CHECK <PASS|FAIL|HARNESS> golden=<...> result=<...>
# Exit: 0 PASS · 1 FAIL (a model verdict) · 5 HARNESS (clone/prepare — not a model verdict) · 64 usage.
# Never writes under !CODING (git read verbs on spark/cache/src only). bash 3.2; stderr never discarded; no cd.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(dirname "$HERE")"
SRC="${HOSTED_SPARK_SRC:-$LM/spark/cache/src}"
RUN="${1:-}"; TIER="${2:-}"; TIP="${3:-}"; WORK="${4:-}"; GOLDEN="${5:-}"
[ -n "$RUN" ] && [ -n "$TIER" ] && [ -n "$TIP" ] && [ -n "$WORK" ] || { echo "usage: check.sh <run_dir> <tier> <tip> <work_dir> [golden.diff]" >&2; exit 64; }
case "$TIER" in code_patch|code_patch2|bash_patch|bash_patch2) ;; *) echo "CHECK HARNESS golden=none result=unknown tier '$TIER'"; exit 5 ;; esac
[ -f "$RUN/input.json" ] && [ -f "$RUN/out.md" ] || { echo "CHECK HARNESS golden=none result=run dir lacks input.json/out.md"; exit 5; }
harness() { echo "CHECK HARNESS golden=none result=$*"; exit 5; }

# ---------------------------------------------------------------- 7. clone (+ prepare) — round.sh step 7
[ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" = "commit" ] || harness "tip $TIP is not in $SRC (fetch it with a Spark round first)"
CLONE="$WORK/clone"
[ -e "$CLONE" ] && harness "$CLONE already exists (a previous check's clone; move it aside)"
mkdir -p "$WORK"
printf 'run_dir=%s\npid=%s\ncreated=%s\nby=hosted/check.sh\n' "$RUN" "$$" "$(date '+%F %T')" > "$WORK/.hosted_check_work"
git clone -q --shared --no-checkout "$SRC" "$CLONE" > "$WORK/clone.out" 2>&1 \
  && git -C "$CLONE" checkout -q --detach "$TIP" >> "$WORK/clone.out" 2>&1 \
  || harness "clone failed: $(tail -2 "$WORK/clone.out" | tr '\n' ' ')"
[ "$(git -C "$CLONE" rev-parse HEAD)" = "$TIP" ] || harness "clone HEAD is not $TIP"
if [ "$TIER" = code_patch ] || [ "$TIER" = code_patch2 ]; then
  bash "$LM/tasks/code_patch/prepare_clone.sh" "$RUN/input.json" "$CLONE" > "$RUN/prepare_clone.out" 2>&1 \
    || harness "prepare_clone.sh failed: $(tail -2 "$RUN/prepare_clone.out" | tr '\n' ' ' | cut -c1-240)"
fi

# ---------------------------------------------------------------- 9. checker — round.sh step 9
if [ "$TIER" = code_patch ]; then
  bash "$LM/tasks/code_patch/spark_checker.sh" "$RUN/input.json" "$RUN/out.md" "$CLONE" > "$RUN/checker.out" 2>&1; CRC=$?
else
  bash "$LM/tasks/$TIER/checker.sh" "$RUN/input.json" "$RUN/out.md" "$CLONE" > "$RUN/checker.out" 2>&1; BCRC=$?
  REP="$RUN/out.md.checker"
  if [ -f "$REP/sections.json" ]; then
    python3 -c 'import json,sys; s=json.load(open(sys.argv[1])); [d.__setitem__("n", i+1) for i, d in enumerate(s)]; json.dump(s, open(sys.argv[2], "w"))' "$REP/sections.json" "$REP/sections_with_n.json"
    python3 "$LM/tasks/code_patch/a2a_anchor.py" "$RUN/input.json" "$CLONE" "$REP/sections_with_n.json" > "$REP/a2a_anchor.out" 2>&1; ARC=$?
  else
    mkdir -p "$REP"
    echo "no sections.json — the checker stopped before splitting the diff" > "$REP/a2a_anchor.out"; ARC=5
  fi
  SUMLINE="$(/usr/bin/grep -m1 '^SUMMARY' "$REP/a2a_anchor.out" 2>/dev/null)"
  {
    if [ "$ARC" -eq 0 ]; then echo "PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip ($SUMLINE)"
    elif [ "$ARC" -eq 1 ]; then echo "FAIL A2a ANCHOR: a hunk's header does NOT name the line its old side sits at: $(/usr/bin/grep -m2 '^BAD' "$REP/a2a_anchor.out" | tr '\n' ' ' | cut -c1-400) ($SUMLINE)"
    elif [ "$ARC" -eq 5 ]; then echo "INFO A2a skipped — $(head -1 "$REP/a2a_anchor.out")"
    else echo "FAIL A2a ANCHOR MEASURE ERROR (rc=$ARC): $(head -2 "$REP/a2a_anchor.out" | tr '\n' ' ')"; fi
    if [ "$BCRC" -eq 0 ] && [ "$ARC" -eq 0 ]; then echo "SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)"
    else echo "SPARK RESULT: FAIL (checker rc=$BCRC; A2a rc=$ARC)"; fi
  } >> "$RUN/checker.out"
  if [ "$BCRC" -eq 0 ] && [ "$ARC" -eq 0 ]; then CRC=0; else CRC=1; fi
fi
RESULT="$(/usr/bin/grep -m1 '^RESULT:' "$RUN/checker.out" | cut -c9-)"
SRESULT="$(/usr/bin/grep -m1 '^SPARK RESULT:' "$RUN/checker.out" | cut -c15-)"

# ---------------------------------------------------------------- 10. golden — round.sh step 10
GOLD="none"
if [ -n "$GOLDEN" ] && [ -f "$GOLDEN" ] && [ -f "$RUN/out.md.checker/patch.diff" ]; then
  if cmp -s "$RUN/out.md.checker/patch.diff" "$GOLDEN"; then GOLD="BYTE-IDENTICAL"
  else
    tree_of() {
      GIT_INDEX_FILE="$2" git -C "$CLONE" read-tree "$TIP" > "$2.out" 2>&1 \
        && GIT_INDEX_FILE="$2" git -C "$CLONE" apply --cached -p1 "$1" >> "$2.out" 2>&1 \
        && GIT_INDEX_FILE="$2" git -C "$CLONE" write-tree 2>> "$2.out"
    }
    GT="$(tree_of "$GOLDEN" "$WORK/golden_cmp.index")"; PT="$(tree_of "$RUN/out.md.checker/patch.diff" "$WORK/patch_cmp.index")"
    if [ -n "$GT" ] && [ "$GT" = "$PT" ]; then GOLD="TREE-IDENTICAL"; else GOLD="DIFFERS"; fi
    echo "golden tree ${GT:-not-built} · patch tree ${PT:-not-built} -> $GOLD" > "$RUN/golden_cmp.out"
  fi
elif [ -n "$GOLDEN" ] && [ -f "$GOLDEN" ]; then GOLD="no-patch"; fi

if [ "$CRC" -eq 0 ]; then V=PASS; else V=FAIL; fi
echo "CHECK $V golden=$GOLD result=${SRESULT:-$RESULT} | checker=${RESULT:-none}"
[ "$CRC" -eq 0 ] && exit 0 || exit 1
