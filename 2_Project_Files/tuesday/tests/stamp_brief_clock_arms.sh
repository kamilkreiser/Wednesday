#!/bin/bash
# stamp_brief_clock_arms.sh — red/green arms for stamp_brief.py's typed-clock refusal (ledger 2026-10-24 w=4).
# Each arm stamps a throwaway brief in a temp dir; REFUSE arms must exit 1 with the brief byte-identical,
# PASS arms must exit 0 with 0 four-underscore lines left. The legitimate shapes (a drafter's quoted
# measurement, a ruling time, a deadline, @NOW@) are CLEAN arms so the guard cannot grow into a blanket ban.
S="$(cd "$(dirname "$0")/../tools" && pwd)/stamp_brief.py"
T=$(mktemp -d); FAIL=0; N=0
U='____'
arm() { # arm <name> <expect rc> <value> [env]
  N=$((N+1)); local name="$1" want="$2" val="$3" envv="$4"
  printf '# brief\n- STAMP: %s\nbody\n' "$U" > "$T/b.md"; cp "$T/b.md" "$T/b.orig"
  python3 -c 'import json,sys; json.dump({"STAMP:": sys.argv[1]}, open(sys.argv[2],"w"))' "$val" "$T/s.json"
  if [ -n "$envv" ]; then env STAMP_ALLOW_CLOCK="$envv" python3 "$S" "$T/b.md" "$T/s.json" > "$T/out" 2>&1; rc=$?
  else python3 "$S" "$T/b.md" "$T/s.json" > "$T/out" 2>&1; rc=$?; fi
  ok=1; [ "$rc" = "$want" ] || ok=0
  if [ "$want" = 1 ]; then cmp -s "$T/b.md" "$T/b.orig" || ok=0; fi
  if [ "$want" = 0 ]; then /usr/bin/grep -q "$U" "$T/b.md" && ok=0; fi
  if [ "$ok" = 1 ]; then echo "PASS $name (rc $rc)"; else echo "FAIL $name (rc $rc, want $want): $(tail -1 "$T/out")"; FAIL=$((FAIL+1)); fi
}
arm refuse-x-placeholder        1 'Tuesday s156, read whole 08:2x (101 lines)'
arm refuse-x-upper              1 'lsof empty, checked 9:1X'
arm refuse-read-whole-literal   1 'Tuesday s156, read whole 08:14 (102 lines)'
arm refuse-read-whole-at        1 'Tuesday s156, read whole at 09:00 (104 lines)'
arm refuse-printed-nothing-at   1 '`lsof -iTCP:9150-9159 -sTCP:LISTEN` printed nothing (rc 1) at 08:56.'
arm pass-now                    0 'Tuesday s157, read whole @NOW@ (90 lines)'
arm pass-drafter-quote          0 'pins equal (MEASURED-BY-DRAFTER 08:56:24 AEDT: both equal it)'
arm pass-ruling-and-deadline    0 'the product owner ruled at 08:52; target verdict 10:30, HARD STOP 11:30 AEDT'
arm pass-override               0 'read whole 08:14' 'arms: override path'
rm -rf "$T"
echo "arms: $((N-FAIL))/$N PASS"; [ "$FAIL" = 0 ]
