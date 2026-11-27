#!/bin/bash
# A2 — interrupted runs (SIGTERM, SIGKILL), a FULL destination, real case-colliding names (case-sensitive source
# image -> case-insensitive HFS+ image as the fake NAS, which also returns names in NFD).
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
run() { nb --run --now "$1" > "$T/out/$2.txt" 2>&1; echo $?; }
tailmsg() { /usr/bin/grep -E 'GOOD:|FAILED|PROBLEM|  - |REFUSED|Traceback|Error|NOT BACKED UP' "$T/out/$1.txt" | head -8 | cut -c1-330; }
mkbig() { "$PY" -c 'import sys,os; open(sys.argv[1],"wb").write((sys.argv[2].encode()*70000)[:int(sys.argv[3])])' "$1" "$2" "$3"; }
slow_stub() { local f="$T/stub/rsync_slow"; { echo '#!/bin/bash'; echo "REAL=$REAL_RSYNC"
  echo 'for a in "$@"; do if [ "$a" = "--version" ]; then exec "$REAL" --version; fi; done'
  echo 'exec "$REAL" --bwlimit=250 "$@"'; } > "$f"; chmod +x "$f"; echo "$f"; }

for SIG in TERM KILL; do
  say; say "### A10-$SIG a run interrupted mid-copy by SIG$SIG, then a rerun"
  fixture "A10$SIG"; for i in 1 2 3 4 5; do mkbig "$T/vol/WEDNESDAY/big$i.bin" "v1-$i-" 1000000; done
  rc=$(run "$(at 0 1 0)" r1); verdict "A10-$SIG first run rc" 0 "$rc"; snap a
  for i in 1 2 3 4 5; do mkbig "$T/vol/WEDNESDAY/big$i.bin" "v2-$i-" 1000001; done
  CONF_RSYNC="$(slow_stub)"; write_conf
  nb --run --now "$(at 1 1 0)" > "$T/out/r2.txt" 2>&1 &
  sleep 7
  PIDS="$(pgrep -f "nb_core.py backup --seat wednesday --tree $T/")"; say "python pid(s): $PIDS ; rsync children before the signal: $(pgrep -f "rsync.*$T/" | wc -l | tr -d ' ')"
  kill -$SIG $PIDS; sleep 3; wait 2>/dev/null
  say "after SIG$SIG: rsync processes still running on this fixture: $(pgrep -f "rsync.*$T/" | wc -l | tr -d ' ')"
  say "state last_attempt.status=$(state last_attempt.status); lock dir present: $([ -d "$T/lane/state/wednesday.lock.d" ] && echo yes || echo no)"
  say "current/ v2 files so far: $(/usr/bin/grep -l -r 'v2-' "$(CUR)" 2>/dev/null | wc -l | tr -d ' ') of 5; temp files left: $(find "$T/nas" -path '*_tmp_incoming*' -type f | wc -l | tr -d ' ')"
  lost a | tail -2; verdict "A10-$SIG nothing lost right after the interruption" 0 "${PIPESTATUS[0]}"
  sleep 25   # let any orphan engine finish
  say "25 s later: rsync still running: $(pgrep -f "rsync.*$T/" | wc -l | tr -d ' '); current/ v2 files: $(/usr/bin/grep -l -r 'v2-' "$(CUR)" 2>/dev/null | wc -l | tr -d ' ') of 5 (an orphan engine kept writing if this grew)"
  CONF_RSYNC=""; write_conf
  rc=$(run "$(at 1 2 0)" r3); say "rerun rc=$rc"; tailmsg r3
  if [ "$rc" = 6 ]; then nb --clear-stale-lock > "$T/out/clr.txt" 2>&1; say "clear-stale-lock rc=$? : $(head -1 "$T/out/clr.txt" | cut -c1-160)"; rc=$(run "$(at 1 3 0)" r4); say "rerun after clearing rc=$rc"; tailmsg r4; fi
  lost a | tail -2; verdict "A10-$SIG nothing lost after the rerun" 0 "${PIPESTATUS[0]}"
  verdict "A10-$SIG all 5 current files are v2" 5 "$(/usr/bin/grep -l -r 'v2-' "$(CUR)" 2>/dev/null | wc -l | tr -d ' ')"
  verdict "A10-$SIG all 5 v1 files are under versions/" 5 "$(/usr/bin/grep -l -r 'v1-' "$(VER)" 2>/dev/null | wc -l | tr -d ' ')"
  say "state: last_attempt=$(state last_attempt.status) ; leftover temp files: $(find "$T/nas" -path '*_tmp_incoming*' -type f | wc -l | tr -d ' ')"
done

say; say "### A11 a FULL destination (12 MB HFS+ image as the fake NAS)"
T="$S/fx/IMG"; mkdir -p "$T/vol/WEDNESDAY/sub" "$T/vol/CODING/Secuura" "$T/nas/Secuura" "$T/nas/General" "$T/lane/seats" "$T/out" "$T/stub"
echo 5000 > "$T/free_gib.txt"; CONF_STATUS=confirmed; CONF_RSYNC=""; write_conf; write_mounts
for i in 1 2 3; do mkbig "$T/vol/WEDNESDAY/full$i.bin" "v1-$i-" 2500000; done
rc=$(run "$(at 0 1 0)" f1); verdict "A11 first run rc (7.5 MB into 12 MB)" 0 "$rc"; snap full; df -k "$T/nas" | tail -1
for i in 1 2 3; do mkbig "$T/vol/WEDNESDAY/full$i.bin" "v2-$i-" 2500001; done
rc=$(run "$(at 1 1 0)" f2); say "A11 second run (needs 7.5 MB more, about 4 MB free) rc=$rc"; tailmsg f2; df -k "$T/nas" | tail -1
lost full | tail -2; verdict "A11 nothing lost on a full destination" 0 "${PIPESTATUS[0]}"
verdict "A11 the run is not recorded good" failed "$(state last_attempt.status)"
say "A11 current/: v1 files $(/usr/bin/grep -l -r 'v1-' "$(CUR)" 2>/dev/null | wc -l | tr -d ' '), v2 files $(/usr/bin/grep -l -r 'v2-' "$(CUR)" 2>/dev/null | wc -l | tr -d ' '); versions/: v1 files $(/usr/bin/grep -l -r 'v1-' "$(VER)" 2>/dev/null | wc -l | tr -d ' '); temp leftovers $(find "$T/nas" -path '*_tmp_incoming*' -type f | wc -l | tr -d ' ')"
say "A11 free-space floor reads free_gib.txt in test mode; the REAL statvfs path was not exercised by this case"

say; say "### A15 REAL case-colliding names on a case-sensitive source, case-insensitive NFD-returning destination"
mkdir -p "$T/held"; for i in 1 2 3; do mv -n "$T/vol/WEDNESDAY/full$i.bin" "$T/held/"; done
mkdir -p "$T/vol/WEDNESDAY/ev/Logs" "$T/vol/WEDNESDAY/ev/logs"; echo "in Logs" > "$T/vol/WEDNESDAY/ev/Logs/x.txt"; echo "in logs" > "$T/vol/WEDNESDAY/ev/logs/y.txt"
echo "upper" > "$T/vol/WEDNESDAY/ev/A.out"; echo "lower" > "$T/vol/WEDNESDAY/ev/a.out"; echo "single v1" > "$T/vol/WEDNESDAY/ev/report.txt"
"$PY" -c 'import os,sys,unicodedata; open(os.path.join(sys.argv[1], unicodedata.normalize("NFC","résumé.txt")),"w").write("nfc name v1\n")' "$T/vol/WEDNESDAY/ev"
rc=$(run "$(at 2 1 0)" c1); say "A15 rc=$rc"; tailmsg c1; snap case
say "A15 dest ev/: $($PY -c 'import os,sys; print(sorted(ascii(x) for x in os.listdir(sys.argv[1])))' "$(CUR)/ev")"
verdict "A15 neither of the colliding files is at the destination" 0 "$(find "$(CUR)/ev" \( -iname 'a.out' -o -name 'x.txt' -o -name 'y.txt' \) | wc -l | tr -d ' ')"
say "--- a sibling that differs only in case APPEARS beside an already-backed-up file; then the original goes away"
echo "second file, capital R" > "$T/vol/WEDNESDAY/ev/Report.txt"
rc=$(run "$(at 3 1 0)" c2); say "A15b rc=$rc"; tailmsg c2; lost case | tail -1
say "A15b dest report.txt content: $(cat "$(CUR)/ev/report.txt")"
mv -n "$T/vol/WEDNESDAY/ev/report.txt" "$T/held/report.txt"
rc=$(run "$(at 4 1 0)" c3); say "A15c rc=$rc"; tailmsg c3; lost case | tail -2; verdict "A15 nothing lost across the case-collision sequence" 0 "${PIPESTATUS[0]}"
say "A15c dest names: $($PY -c 'import os,sys; print(sorted(ascii(x) for x in os.listdir(sys.argv[1])))' "$(CUR)/ev") ; content now: $(cat "$(CUR)/ev/report.txt")"
say "--- NFC source name vs NFD name returned by the destination: second run must copy 0 and version 0"
rc=$(run "$(at 4 2 0)" c4); /usr/bin/grep -E 'to copy:' "$T/out/c4.txt" | head -1
"$PY" -c 'import os,sys,unicodedata; open(os.path.join(sys.argv[1], unicodedata.normalize("NFC","résumé.txt")),"w").write("nfc name v2 longer\n")' "$T/vol/WEDNESDAY/ev"
rc=$(run "$(at 5 1 0)" c5); say "A15d rc=$rc"; lost case | tail -1; verdict "A15d nothing lost (NFC/NFD)" 0 "${PIPESTATUS[0]}"
say "A15d versions holding the old résumé: $(/usr/bin/grep -r -l 'nfc name v1' "$(VER)" 2>/dev/null | wc -l | tr -d ' ')"
