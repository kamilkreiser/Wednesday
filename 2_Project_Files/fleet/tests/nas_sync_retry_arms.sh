#!/bin/bash
# nas_sync_retry_arms.sh — arms for the NAS-sync RETRY PASS parser (scheduler/nas_sync_lib.sh)
# and the STALENESS line (scheduler/nas_staleness.sh). Built 2026-09-21 (Kam 09:48).
#
# NO UNISON IS RUN HERE. Every arm works on captured text (fixtures/nas_sync/) or on temp
# trees in a mktemp dir. A check that cannot fail is not a check, so every "zero" arm has
# a positive control beside it, and every count is compared to an independent grep.
#
# Run: bash nas_sync_retry_arms.sh → PASS/FAIL lines, then FAILS=<n>; exit code = n.
set -u
SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
LIB="$SELF_DIR/../../scheduler/nas_sync_lib.sh"
STALE="$SELF_DIR/../../scheduler/nas_staleness.sh"
FX="$SELF_DIR/fixtures/nas_sync"
T=$(mktemp -d "${TMPDIR:-/tmp}/nas_sync_arms.XXXXXX")
fails=0
pass() { echo "PASS $1"; }
fail() { echo "FAIL $1"; fails=$((fails+1)); }
check() { # name got want
  if [ "$2" = "$3" ]; then pass "$1 ($2)"; else fail "$1 — got [$2] want [$3]"; fi
}

[ -f "$LIB" ]   || { echo "FAIL lib missing at $LIB"; exit 1; }
[ -f "$STALE" ] || { echo "FAIL nas_staleness.sh missing at $STALE"; exit 1; }
# shellcheck source=../../scheduler/nas_sync_lib.sh
. "$LIB"

REAL="$FX/2026-09-21_033004_tail_67failed.log"
CLEAN_SKIP="$FX/2026-09-11_033003_clean_skipped.log"
CLEAN_FULL="$FX/scratch_clean_complete.log"
ABORT="$FX/scratch_confirmbigdel_abort.log"
for f in "$REAL" "$CLEAN_SKIP" "$CLEAN_FULL" "$ABORT"; do [ -f "$f" ] || { echo "FAIL fixture missing: $f"; exit 1; }; done

# ── ARM 1: 67 failed paths parsed exactly from last night's log ─────────────────────────────
# Independent count: the same normalisation, a plain grep. The fixture is RAW (\r kept), so a
# parser that forgot to normalise would read fewer lines — and the fixture proves it holds \r.
CRS=$(tr -cd '\r' < "$REAL" | wc -c | tr -d ' ')
[ "$CRS" -gt 0 ] && pass "arm1 fixture is carriage-return separated ($CRS CRs)" || fail "arm1 fixture has no \\r — it does not exercise normalisation"
nas_failed_paths "$REAL" > "$T/real.paths"
GREP_N=$(tr '\r' '\n' < "$REAL" | /usr/bin/grep -c 'failed: ')
check "arm1 grep -c 'failed: ' on the fixture" "$GREP_N" "67"
check "arm1 parser count" "$(nas_count "$T/real.paths")" "67"
check "arm1 unison's own summary agrees" "$(tr '\r' '\n' < "$REAL" | /usr/bin/grep -oiE '[0-9]+ failed' | tail -1)" "67 failed"
# exact content: first, last, and the one with a space
check "arm1 first path" "$(head -1 "$T/real.paths")" "WEDNESDAY/0_Brain/dashboard/data/agentmail.json"
check "arm1 last path" "$(tail -1 "$T/real.paths")" "WEDNESDAY/logs/combined.log"
check "arm1 path with a space kept whole" "$(/usr/bin/grep -c '^Notes (MASTER)/daily/2026-09-21.md$' "$T/real.paths")" "1"
check "arm1 no path carries trailing whitespace" "$(/usr/bin/grep -c '[[:space:]]$' "$T/real.paths")" "0"
check "arm1 no non-printable bytes in any path" "$(LC_ALL=C /usr/bin/grep -c '[^[:print:]]' "$T/real.paths")" "0"
check "arm1 raw-anchor control (^failed: on the raw file must be 0 — the indent is real)" "$(/usr/bin/grep -c '^failed:' "$REAL")" "0"

# ── ARM 2: a clean log parses to 0 and the retry is SKIPPED with a printed reason ──────────
# Two clean shapes: the engine skipped (no unison output at all) and a real unison run that
# completed with 0 failed. Both must yield an empty list; the skip DECISION is the same
# branch nas_sync.sh takes (N_BEFORE -eq 0), reproduced here verbatim so the arm tests the
# rule, not a paraphrase of it.
for c in "$CLEAN_SKIP" "$CLEAN_FULL"; do
  nas_failed_paths "$c" > "$T/clean.paths"
  N=$(nas_count "$T/clean.paths")
  check "arm2 $(basename "$c") parses to" "$N" "0"
  if [ "$N" -eq 0 ]; then
    R="retry: 0 → 0 (skipped: no failed: lines in the main run)"
  else
    R="retry would RUN"
  fi
  check "arm2 $(basename "$c") decision" "$R" "retry: 0 → 0 (skipped: no failed: lines in the main run)"
done
# positive control for the zero: the clean-full fixture DOES contain unison output
check "arm2 positive control — clean-full fixture holds a unison summary" "$(tr '\r' '\n' < "$CLEAN_FULL" | /usr/bin/grep -ic 'synchronization complete')" "1"
check "arm2 positive control — parser on the real fixture is non-zero" "$([ "$(nas_count "$T/real.paths")" -gt 0 ] && echo nonzero)" "nonzero"

# ── ARM 3: the -path argv is built from the parsed paths ONLY ───────────────────────────────
# Plant a foreign path in a SEPARATE file that is never given to the builder; then prove the
# argv has 2 elements per parsed path, every odd element is "-path", every even element is a
# parsed path, and the foreign path is absent. Also: the own-log exclusion and the
# gone-from-source filter (the two ways nas_sync.sh narrows the list) only ever REMOVE.
FOREIGN="WEDNESDAY/0_Brain/identity/persona.md"
printf '%s\n' "$FOREIGN" > "$T/foreign.txt"
nas_build_path_args "$T/real.paths"
check "arm3 argv length = 2 × 67" "${#NAS_PATH_ARGS[@]}" "134"
odd_ok=1; even_ok=1; i=0
for a in "${NAS_PATH_ARGS[@]}"; do
  if [ $((i % 2)) -eq 0 ]; then [ "$a" = "-path" ] || odd_ok=0
  else /usr/bin/grep -qxF -- "$a" "$T/real.paths" || even_ok=0; fi
  i=$((i+1))
done
check "arm3 every odd argv element is -path" "$odd_ok" "1"
check "arm3 every even argv element is a parsed path" "$even_ok" "1"
FOREIGN_HITS=0; for a in "${NAS_PATH_ARGS[@]}"; do [ "$a" = "$FOREIGN" ] && FOREIGN_HITS=$((FOREIGN_HITS+1)); done
check "arm3 planted foreign path absent from argv" "$FOREIGN_HITS" "0"
# positive control for that zero: the foreign path IS a real file, so its absence is a choice, not an accident
[ -f "$SELF_DIR/../../../0_Brain/identity/persona.md" ] && pass "arm3 positive control — foreign path exists on disk" || fail "arm3 control: persona.md not found — the foreign path is not a real file"
# the space-bearing path is ONE argv element
SPACE_ELEMS=0; for a in "${NAS_PATH_ARGS[@]}"; do [ "$a" = "Notes (MASTER)/daily/2026-09-21.md" ] && SPACE_ELEMS=$((SPACE_ELEMS+1)); done
check "arm3 'Notes (MASTER)/…' is a single argv element" "$SPACE_ELEMS" "1"
# own-log exclusion: grep -vxF removes exactly one line
OWN="WEDNESDAY/2_Project_Files/scheduler/logs/nas_sync_wednesday_2026-09-21_033004_25224.log"
/usr/bin/grep -vxF -- "$OWN" "$T/real.paths" > "$T/minus_own.paths"
check "arm3 own-log exclusion removes exactly one" "$(nas_count "$T/minus_own.paths")" "66"
check "arm3 own-log exclusion removed the right one" "$(/usr/bin/grep -cxF -- "$OWN" "$T/minus_own.paths")" "0"
# gone-from-source filter on a temp tree: 3 paths, 2 present, 1 gone
mkdir -p "$T/src/a"; : > "$T/src/a/x.txt"; : > "$T/src/a/y.txt"
printf 'a/x.txt\na/y.txt\na/gone.txt\n' > "$T/three.paths"
nas_filter_present "$T/src" "$T/three.paths" "$T/present.paths" "$T/gone.paths"
check "arm3 filter_present keeps the present" "$(nas_count "$T/present.paths")" "2"
check "arm3 filter_present names the gone" "$(cat "$T/gone.paths")" "a/gone.txt"
# emptied-paths parser on the captured abort + set subtraction
nas_emptied_paths "$ABORT" > "$T/emptied.paths"
check "arm3 emptied parser on the real abort" "$(cat "$T/emptied.paths")" "d/gone.txt"
printf 'd/keep.txt\nd/gone.txt\n' > "$T/two.paths"
nas_minus "$T/two.paths" "$T/emptied.paths" "$T/rest.paths"
check "arm3 nas_minus drops the emptied path" "$(cat "$T/rest.paths")" "d/keep.txt"
check "arm3 emptied parser on a clean log is empty" "$(nas_emptied_paths "$CLEAN_FULL" | nas_count /dev/stdin)" "0"

# ── ARM 4: nas_staleness.sh on a temp pair of trees — SAME / STALE / MISSING each once ─────
# Hours are what `stat -f %m` says, not what a clock was typed as: the stale file's NAS copy
# is aged with touch -t to a known epoch and the expected figure is computed from the same
# two stat values the script reads.
mkdir -p "$T/S/k" "$T/D/k"
printf 'same\n' > "$T/S/k/same.md";  cp "$T/S/k/same.md" "$T/D/k/same.md"
printf 'new content\n' > "$T/S/k/stale.md"; printf 'old content\n' > "$T/D/k/stale.md"
touch -t 202609150300 "$T/D/k/stale.md"        # NAS copy dated 2026-09-15 03:00 local
printf 'only here\n' > "$T/S/k/missing.md"     # planted: present on ONE side only
SM=$(stat -f %m "$T/S/k/stale.md"); DM=$(stat -f %m "$T/D/k/stale.md")
WANT_H=$(awk -v a="$SM" -v b="$DM" 'BEGIN{printf "%.1f", (a-b)/3600}')
OUT=$(bash "$STALE" --src "$T/S" --dst "$T/D" --file k/same.md --file k/stale.md --file k/missing.md --warn-hours 36 2>&1); RC=$?
printf '%s\n' "$OUT" > "$T/stale.out"
check "arm4 SAME fires once"    "$(/usr/bin/grep -c '^SAME ' "$T/stale.out")" "1"
check "arm4 STALE fires once"   "$(/usr/bin/grep -c '^STALE ' "$T/stale.out")" "1"
check "arm4 MISSING fires once" "$(/usr/bin/grep -c '^MISSING ' "$T/stale.out")" "1"
check "arm4 STALE hours come from stat" "$(/usr/bin/grep '^STALE ' "$T/stale.out" | awk '{print $2}')" "${WANT_H}h"
check "arm4 STALE is the stale file"     "$(/usr/bin/grep '^STALE ' "$T/stale.out" | awk '{print $NF}')" "k/stale.md"
check "arm4 MISSING is the planted file" "$(/usr/bin/grep '^MISSING ' "$T/stale.out" | awk '{print $NF}')" "k/missing.md"
check "arm4 summary line" "$(/usr/bin/grep '^staleness:' "$T/stale.out")" "staleness: same=1 stale=1 (over 36h: 1) nas-newer=0 missing=1 no-src=0"
check "arm4 --warn-hours exit is 1 (MISSING + STALE>36h)" "$RC" "1"
# the same trees with only the SAME file: exit 0 and no STALE/MISSING — the check can pass, too
OUT2=$(bash "$STALE" --src "$T/S" --dst "$T/D" --file k/same.md --warn-hours 36 2>&1); RC2=$?
check "arm4 all-same exit is 0" "$RC2" "0"
check "arm4 all-same has no STALE/MISSING" "$(printf '%s\n' "$OUT2" | /usr/bin/grep -cE '^(STALE|MISSING)')" "0"
# NAS-newer branch and NO-SRC branch, once each
printf 'nas wrote\n' > "$T/D/k/nasnewer.md"; printf 'src older\n' > "$T/S/k/nasnewer.md"; touch -t 202609150300 "$T/S/k/nasnewer.md"
OUT3=$(bash "$STALE" --src "$T/S" --dst "$T/D" --file k/nasnewer.md --file k/absent-at-source.md 2>&1)
check "arm4 DIFF-NAS-NEWER fires once" "$(printf '%s\n' "$OUT3" | /usr/bin/grep -c '^DIFF-NAS-NEWER ')" "1"
check "arm4 NO-SRC fires once" "$(printf '%s\n' "$OUT3" | /usr/bin/grep -c '^NO-SRC ')" "1"
# unmounted NAS is a SKIP, not a pass: point --dst at a path that is not mounted
OUT4=$(bash "$STALE" --src "$T/S" --dst "$T/does-not-exist" --file k/same.md --warn-hours 36 2>&1); RC4=$?
check "arm4 absent root is a stated SKIP" "$(printf '%s\n' "$OUT4" | /usr/bin/grep -c '^SKIP')" "1"
check "arm4 SKIP exits 0 (nothing measured is not a failure)" "$RC4" "0"

echo "FAILS=$fails"
exit $fails
