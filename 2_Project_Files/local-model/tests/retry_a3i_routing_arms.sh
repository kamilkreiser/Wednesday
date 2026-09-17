#!/bin/bash
# retry_a3i_routing_arms.sh — red-proof for night_run.sh's RETRY-ONCE routing of an A3i INDENT SHIFT (2026-09-17),
# and the owed A3c INCOMPLETE verdict extraction (IMPROVEMENTS rows 2026-09-17 11:00 and 13:27).
# The runner does not expose the retry decision or the retry_feedback builder as callable units, so this arm CUTS
# THE RUNNER'S OWN LINES out of whichever runner file it is given (never a re-implemented regex):
#   - the VERDICT line   (the one reading '^RESULT:' from "$RUN/checker.out")
#   - the trigger `if`   (from `if [ "${NIGHT_RETRY_ON_PARTIAL:-1}"` to its first `; then`)
#   - the builder        (the python heredoc between `<<'PYR'` and `PYR`)
# and runs them on REAL checker outputs. Every extraction asserts it found exactly one unit.
#   ARM a   A3i real FAIL (KS-623, checker f3ce186c): NEW retries; verdict starts FAIL A3i INDENT SHIFT;
#           missed_sites == []; instruction carries the sentence.  a-neg: OLD does NOT retry (negative control).
#   ARM a2  an A3i FAIL line longer than 600 chars (synthesised from the real line): the sentence survives the cap
#   ARM b   A3c real FAIL (KS-1180-P1 r1): NEW verdict carries FAIL A3c INCOMPLETE; OLD carried the generic text
#   ARM c   A3i MEASURE error (wording read out of checker.sh): NEW does not retry
#   ARM d   A3b PARTIAL FIX real (KS-1121): NEW == OLD (retry, identical retry_feedback, missed_sites non-empty)
#   ARM e   PASS real (KS-730): neither runner retries
# Usage: bash retry_a3i_routing_arms.sh <new night_run.sh> <old night_run.sh>
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(cd -P "$HERE/.." && pwd)"
NEW="${1:?new runner}"; OLD="${2:?old runner}"
CHECKER="$LM/tasks/code_patch/checker.sh"
RUNS="$LM/runs"
W="$(mktemp -d "${TMPDIR:-/tmp}/retry_a3i.XXXXXX")"
PASS=0; FAIL=0
ok()  { echo "PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }
SENT="The previous attempt shifted the indentation of lines the brief adds; copy every line of the brief byte-for-byte, including its leading spaces."

A_RUN="/private/tmp/claude-501/night/a3i_0917/arms/A_new_ks623"; A_IN="$RUNS/2026-09-17_ks623-ornith35b-night/input.json"
B_RUN="$RUNS/2026-09-17_ks1180p1-ornith35b-night";           B_IN="$B_RUN/input.json"
D_RUN="$RUNS/2026-09-16_ks1121-ornith35b-night";             D_IN="$D_RUN/input.json"
E_RUN="$RUNS/2026-09-17_ks730-ornith35b-night";              E_IN="$E_RUN/input.json"

# ---------------------------------------------------------------- extraction (the runner's own lines)
extract() { # $1 runner  $2 outdir  -> $2/decide.sh (RUN=$1 arg) and $2/builder.py ; rc 1 if a unit is not found exactly once
  local r="$1" o="$2"; mkdir -p "$o"
  local nv nt nb
  nv="$(/usr/bin/grep -c -F "VERDICT=\"\$(/usr/bin/grep -m1 '^RESULT:' \"\$RUN/checker.out\"" "$r")"
  nt="$(/usr/bin/grep -c -F 'if [ "${NIGHT_RETRY_ON_PARTIAL:-1}" = "1" ]' "$r")"
  nb="$(/usr/bin/grep -c -x -F "PYR" "$r")"
  if [ "$nv" != 1 ] || [ "$nt" != 1 ] || [ "$nb" != 1 ]; then echo "extract $r: verdict=$nv trigger=$nt PYR-end=$nb (each must be 1)"; return 1; fi
  {
    echo '#!/bin/bash'
    echo 'set -uo pipefail'
    echo 'RUN="$1"; crc=1'
    /usr/bin/grep -F "VERDICT=\"\$(/usr/bin/grep -m1 '^RESULT:' \"\$RUN/checker.out\"" "$r"
    echo 'printf "VERDICT=%s\n" "$VERDICT"'
    awk 'index($0, "if [ \"${NIGHT_RETRY_ON_PARTIAL:-1}\" = \"1\" ]") {on=1} on {print} on && /; then$/ {exit}' "$r"
    echo '  echo DECISION=RETRY'
    echo 'else'
    echo '  echo DECISION=NORETRY'
    echo 'fi'
  } > "$o/decide.sh"
  awk '/<<'"'"'PYR'"'"'$/ {on=1; next} on && /^PYR$/ {exit} on {print}' "$r" > "$o/builder.py"
  [ -s "$o/builder.py" ] && bash -n "$o/decide.sh"
}
decide() { # $1 new|old  $2 run dir  -> prints DECISION=...
  bash "$W/x_$1/decide.sh" "$2" > "$W/dec_$1_$3.out" 2>&1
  echo "rc=$?" >> "$W/dec_$1_$3.out"
  /usr/bin/grep -i -o 'DECISION=[A-Z]*' "$W/dec_$1_$3.out" | head -1
}
build() { # $1 new|old  $2 input  $3 run dir  $4 tag  -> $W/fb_$1_$4.json
  python3 "$W/x_$1/builder.py" "$2" "$3/checker.out" "$W/fb_$1_$4.json" > "$W/fb_$1_$4.out" 2>&1
  echo $?
}
fb() { # $1 json  $2 python expr over f (retry_feedback)
  python3 -c "import json,sys; f=json.load(open(sys.argv[1]))['retry_feedback']; print($2)" "$1" 2>&1
}

extract "$NEW" "$W/x_new" > "$W/extract_new.out" 2>&1; xn=$?
extract "$OLD" "$W/x_old" > "$W/extract_old.out" 2>&1; xo=$?
if [ "$xn" -ne 0 ] || [ "$xo" -ne 0 ]; then
  bad "EXTRACT new rc=$xn old rc=$xo: $(cat "$W/extract_new.out" "$W/extract_old.out" | tr '\n' ' ')"
  echo "RESULT: $PASS passed, $FAIL failed (work dir kept: $W)"; exit 1
fi
ok "EXTRACT both runners: VERDICT line, trigger if, PYR builder found exactly once (new builder $(wc -l < "$W/x_new/builder.py" | tr -d ' ') lines, old $(wc -l < "$W/x_old/builder.py" | tr -d ' '))"
echo "new runner sha256 $(shasum -a 256 "$NEW" | cut -c1-12) · old $(shasum -a 256 "$OLD" | cut -c1-12) · checker $(shasum -a 256 "$CHECKER" | cut -c1-12)"

for f in "$A_RUN/checker.out" "$A_IN" "$B_RUN/checker.out" "$B_IN" "$D_RUN/checker.out" "$D_IN" "$E_RUN/checker.out" "$E_IN"; do
  [ -s "$f" ] || { bad "FIXTURE missing: $f"; }
done

# ---------------------------------------------------------------- ARM a  (A3i real FAIL)
if /usr/bin/grep -q -i '^FAIL A3i INDENT SHIFT' "$A_RUN/checker.out"; then
  DN="$(decide new "$A_RUN" a)"; DO="$(decide old "$A_RUN" a)"
  if [ "$DN" = "DECISION=RETRY" ]; then ok "a1 NEW retries on KS-623's A3i FAIL ($(/usr/bin/grep -m1 '^VERDICT=' "$W/dec_new_a.out" | cut -c1-90))"; else bad "a1 NEW decision '$DN': $(tr '\n' ' ' < "$W/dec_new_a.out")"; fi
  if [ "$DO" = "DECISION=NORETRY" ]; then ok "a-neg OLD does NOT retry on the same checker.out (negative control)"; else bad "a-neg OLD decision '$DO'"; fi
  brc="$(build new "$A_IN" "$A_RUN" a)"
  if [ "$brc" = 0 ]; then
    V="$(fb "$W/fb_new_a.json" "f['verdict'][:60]")"; M="$(fb "$W/fb_new_a.json" "f['missed_sites']")"
    S="$(python3 -c "import json,sys; f=json.load(open(sys.argv[1]))['retry_feedback']; print(sys.argv[2] in f['instruction'])" "$W/fb_new_a.json" "$SENT" 2>&1)"
    case "$V" in "FAIL A3i INDENT SHIFT"*) ok "a2 verdict starts FAIL A3i INDENT SHIFT ('$V')";; *) bad "a2 verdict '$V'";; esac
    if [ "$M" = "[]" ]; then ok "a3 missed_sites == [] (the A3i line carries no ':NNN \`' shape)"; else bad "a3 missed_sites $M"; fi
    if [ "$S" = "True" ]; then ok "a4 instruction carries the INDENT SHIFT sentence"; else bad "a4 sentence in instruction: $S"; fi
  else
    bad "a2-a4 NEW builder rc=$brc: $(tail -3 "$W/fb_new_a.out" | tr '\n' ' ')"
  fi
  orc="$(build old "$A_IN" "$A_RUN" a)"
  echo "  (info) OLD builder on the same file rc=$orc, verdict='$(fb "$W/fb_old_a.json" "f['verdict'][:70]")'"
else
  bad "a FIXTURE: $A_RUN/checker.out has no FAIL A3i INDENT SHIFT line (re-derive per a3i_indent_arms.sh)"
fi

# ---------------------------------------------------------------- ARM a2 (a >600-char A3i FAIL line)
mkdir -p "$W/a_long"
python3 - "$A_RUN/checker.out" "$W/a_long/checker.out" > "$W/a_long/synth.out" 2>&1 <<'PY'
import sys
src, dst = sys.argv[1:3]
out = []
for ln in open(src, encoding="utf-8", errors="replace").read().split("\n"):
    if ln.startswith("FAIL A3i INDENT SHIFT"):
        head, sep, rest = ln.partition(": :")
        seg = ":" + rest.split(" — indentation shifted")[0]
        tail = " — indentation shifted" + rest.split(" — indentation shifted", 1)[1]
        ln = head + ": " + " · ".join([seg] * 6) + tail
    out.append(ln)
open(dst, "w", encoding="utf-8").write("\n".join(out))
PY
L2="$(/usr/bin/grep -i -m1 '^FAIL A3i INDENT SHIFT' "$W/a_long/checker.out" | wc -c | tr -d ' ')"
if [ "${L2:-0}" -gt 600 ]; then
  DN="$(decide new "$W/a_long" along)"; brc="$(build new "$A_IN" "$W/a_long" along)"
  R="$(python3 -c "import json,sys; f=json.load(open(sys.argv[1]))['retry_feedback']; print(len(f['verdict']), f['verdict'].startswith('FAIL A3i INDENT SHIFT'), sys.argv[2] in f['instruction'], f['missed_sites'])" "$W/fb_new_along.json" "$SENT" 2>&1)"
  if [ "$DN" = "DECISION=RETRY" ] && [ "$brc" = 0 ] && [ "$R" = "600 True True []" ]; then ok "a5 ${L2}-byte A3i line: retry, verdict capped at 600, sentence survives the cap, missed_sites []"; else bad "a5 decision=$DN rc=$brc got '$R' (want '600 True True []')"; fi
else
  bad "a5 synthesis produced a ${L2}-byte line (need > 600): $(cat "$W/a_long/synth.out")"
fi

# ---------------------------------------------------------------- ARM b  (A3c real FAIL)
if /usr/bin/grep -q -i '^FAIL A3c INCOMPLETE' "$B_RUN/checker.out"; then
  DN="$(decide new "$B_RUN" b)"
  brc="$(build new "$B_IN" "$B_RUN" b)"; orc="$(build old "$B_IN" "$B_RUN" b)"
  VN="$(fb "$W/fb_new_b.json" "f['verdict'][:48]")"; VO="$(fb "$W/fb_old_b.json" "f['verdict'][:60]")"
  SN="$(python3 -c "import json,sys; f=json.load(open(sys.argv[1]))['retry_feedback']; print(sys.argv[2] in f['instruction'])" "$W/fb_new_b.json" "$SENT" 2>&1)"
  if [ "$DN" = "DECISION=RETRY" ] && [ "$brc" = 0 ]; then ok "b1 NEW retries on KS-1180-P1's A3c FAIL (builder rc 0)"; else bad "b1 decision=$DN builder rc=$brc"; fi
  case "$VN" in "FAIL A3c INCOMPLETE"*) ok "b2 NEW verdict carries it: '${VN}...'";; *) bad "b2 NEW verdict '$VN'";; esac
  if [ "$orc" = 0 ] && [ "$VO" = "the checker refused the first attempt (see verdict)" ]; then ok "b3 OLD verdict was the generic text (control: '$VO')"; else bad "b3 OLD rc=$orc verdict '$VO'"; fi
  if [ "$SN" = "False" ]; then ok "b4 the INDENT sentence is NOT added to an A3c instruction"; else bad "b4 sentence present on A3c: $SN"; fi
else
  bad "b FIXTURE: no FAIL A3c INCOMPLETE line in $B_RUN/checker.out"
fi

# ---------------------------------------------------------------- ARM c  (A3i MEASURE error, wording from checker.sh)
mkdir -p "$W/c_measure"
CF="$(/usr/bin/grep -F 'fail "A3i INDENT MEASURE ERROR' "$CHECKER" | head -1 | sed -e 's/^[[:space:]]*fail "/FAIL /' -e 's/\$A3I_RC/2/' -e 's#\$A3_TARGET#Blockchain/Dev/services/auth/src/middleware/authenticate.ts#' -e 's/: \$(head.*$/: Traceback (synthetic measure fault)/')"
CR="$(/usr/bin/grep -F 'stopped at the A3i measure' "$CHECKER" | head -1 | sed -e 's/^[[:space:]]*echo "//' -e 's/"$//' -e 's/\$FAILS/1/')"
if [ -n "$CF" ] && [ -n "$CR" ] && ! printf '%s' "$CF$CR" | /usr/bin/grep -q -F '$'; then
  /usr/bin/grep -v -i -E '^(FAIL A3i|RESULT:)' "$A_RUN/checker.out" > "$W/c_measure/checker.out"
  printf '%s\n%s\n' "$CF" "$CR" >> "$W/c_measure/checker.out"
  DN="$(decide new "$W/c_measure" c)"; DO="$(decide old "$W/c_measure" c)"
  if [ "$DN" = "DECISION=NORETRY" ] && [ "$DO" = "DECISION=NORETRY" ]; then ok "c1 measure error '$(echo "$CR" | cut -c1-80)…' → NEW no retry (OLD no retry)"; else bad "c1 new=$DN old=$DO on '$CR'"; fi
else
  bad "c FIXTURE: could not read the measure wording out of checker.sh (fail='$CF' result='$CR')"
fi

# ---------------------------------------------------------------- ARM d  (A3b PARTIAL FIX real) — unchanged
if /usr/bin/grep -q -i '^FAIL A3b PARTIAL FIX' "$D_RUN/checker.out"; then
  DN="$(decide new "$D_RUN" d)"; DO="$(decide old "$D_RUN" d)"
  brc="$(build new "$D_IN" "$D_RUN" d)"; orc="$(build old "$D_IN" "$D_RUN" d)"
  EQ="$(python3 -c "import json,sys; a=json.load(open(sys.argv[1]))['retry_feedback']; b=json.load(open(sys.argv[2]))['retry_feedback']; print(a==b, len(a['missed_sites']), a['verdict'][:40])" "$W/fb_new_d.json" "$W/fb_old_d.json" 2>&1)"
  if [ "$DN" = "DECISION=RETRY" ] && [ "$DO" = "DECISION=RETRY" ] && [ "$brc" = 0 ] && [ "$orc" = 0 ]; then ok "d1 A3b PARTIAL: NEW and OLD both retry"; else bad "d1 new=$DN old=$DO rc new=$brc old=$orc"; fi
  case "$EQ" in "True "[1-9]*" FAIL A3b PARTIAL FIX"*) ok "d2 retry_feedback identical NEW vs OLD, missed_sites non-empty ($EQ)";; *) bad "d2 '$EQ'";; esac
else
  bad "d FIXTURE: no FAIL A3b PARTIAL FIX line in $D_RUN/checker.out"
fi

# ---------------------------------------------------------------- ARM e  (PASS real)
if /usr/bin/grep -q -i '^RESULT: PASS' "$E_RUN/checker.out"; then
  DN="$(decide new "$E_RUN" e)"; DO="$(decide old "$E_RUN" e)"
  if [ "$DN" = "DECISION=NORETRY" ] && [ "$DO" = "DECISION=NORETRY" ]; then ok "e1 PASS ($(/usr/bin/grep -i -m1 '^RESULT:' "$E_RUN/checker.out")) → no retry, NEW and OLD"; else bad "e1 new=$DN old=$DO"; fi
else
  bad "e FIXTURE: no RESULT: PASS in $E_RUN/checker.out"
fi

echo "RESULT: $PASS passed, $FAIL failed (work dir kept: $W)"
[ "$FAIL" -eq 0 ]
