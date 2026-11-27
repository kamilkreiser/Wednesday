#!/bin/bash
# C — lock, catch-up, clock edges, the three-day watch.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
run() { nb --run --now "$1" > "$T/out/$2.txt" 2>&1; echo $?; }
cards() { cat "$T"/out/$1* 2>/dev/null | /usr/bin/grep -c -F 'CARD-COMMAND:'; }
delay_stub() { local f="$T/stub/rsync_delay"; { echo '#!/bin/bash'; echo "REAL=$REAL_RSYNC"
  echo 'for a in "$@"; do if [ "$a" = "--version" ]; then exec "$REAL" --version; fi; done'
  echo 'sleep 3; exec "$REAL" "$@"'; } > "$f"; chmod +x "$f"; echo "$f"; }

say "### C1 two real runs started together, 8 trials: exactly one may win"
fixture C1; CONF_RSYNC="$(delay_stub)"; write_conf
for i in 1 2 3 4 5 6 7 8; do
  echo "trial $i" > "$T/vol/WEDNESDAY/a.txt"
  nb --run --now "$(at $i 1 0)" > "$T/out/p${i}a.txt" 2>&1 & A=$!
  nb --run --now "$(at $i 1 0)" > "$T/out/p${i}b.txt" 2>&1 & B=$!
  wait $A; ra=$?; wait $B; rb=$?
  msg="$(cat "$T/out/p${i}a.txt" "$T/out/p${i}b.txt" | /usr/bin/grep -o -E 'another run holds the lock|STALE lock' | head -1)"
  printf 'trial %s: rc %s and %s ; loser was told: [%s] ; lock left behind: %s\n' "$i" "$ra" "$rb" "$msg" "$([ -d "$T/lane/state/wednesday.lock.d" ] && echo YES || echo no)"
done
say "winners per trial must be 1: GOOD lines in total = $(cat "$T"/out/p*.txt | /usr/bin/grep -c 'GOOD:') of 8 trials"

say; say "### C2 lock owner pid: dead; alive but UNRELATED; alive, unrelated, with 'nas_backup' in its command line"
fixture C2; mkdir -p "$T/lane/state/wednesday.lock.d"
echo '{"pid": 999999, "started_local": "test"}' > "$T/lane/state/wednesday.lock.d/owner.json"
rc=$(run "$(at 0 1 0)" d); say "dead pid: rc=$rc [$(/usr/bin/grep -o -E 'another run holds the lock|STALE lock' "$T/out/d.txt" | head -1)]"
sleep 300 & U=$!; echo "{\"pid\": $U, \"started_local\": \"test\"}" > "$T/lane/state/wednesday.lock.d/owner.json"
rc=$(run "$(at 0 1 0)" u); say "pid reused by an unrelated 'sleep': rc=$rc [$(/usr/bin/grep -o -E 'another run holds the lock|STALE lock' "$T/out/u.txt" | head -1)]"; kill $U 2>/dev/null
bash -c 'exec -a "less /tmp/notes_about_nas_backup.md" sleep 300' & V=$!; sleep 1; echo "{\"pid\": $V, \"started_local\": \"test\"}" > "$T/lane/state/wednesday.lock.d/owner.json"
rc=$(run "$(at 0 1 0)" v); say "pid reused by an unrelated process whose command line mentions nas_backup: rc=$rc [$(/usr/bin/grep -o -E 'another run holds the lock|STALE lock' "$T/out/v.txt" | head -1)]"
nb --clear-stale-lock > "$T/out/v2.txt" 2>&1; say "  --clear-stale-lock on it: rc=$? [$(head -1 "$T/out/v2.txt" | cut -c1-90)]"
nightly --now "$(at 0 0 31)" > "$T/out/v3.txt" 2>&1; say "  nightly decision: $(head -1 "$T/out/v3.txt" | cut -c1-110)"; kill $V 2>/dev/null
say "  lock dir with NO owner.json (the window between mkdir and the owner write):"; mkdir -p "$T/held"; mv "$T/lane/state/wednesday.lock.d/owner.json" "$T/held/"
rc=$(run "$(at 0 1 0)" n); say "  rc=$rc [$(/usr/bin/grep -o -E 'another run holds the lock|STALE lock' "$T/out/n.txt" | head -1)]"

say; say "### C3 catch-up: missed nights are caught up exactly once; fires outside the window never run"
fixture C3
seq_fire() { nightly --now "$1" > "$T/out/$2.txt" 2>&1; printf '%-28s rc=%s  %s\n' "$3" "$?" "$(head -1 "$T/out/$2.txt" | sed 's/^nightly\[wednesday\]: //' | cut -c1-120)"; }
seq_fire "$(at 0 0 30)" n00 "night0 00:30"
seq_fire "$(at 0 1 40)" n01 "night0 01:40"; seq_fire "$(at 0 2 50)" n02 "night0 02:50"; seq_fire "$(at 0 4 0)" n03 "night0 04:00"
say "(nights 1,2: nothing fires - machine asleep)"
seq_fire "$(at 2 14 0)" n20 "day2 14:00 wake fire"
seq_fire "$(at 3 0 30)" n30 "night3 00:30"; seq_fire "$(at 3 1 40)" n31 "night3 01:40"
seq_fire "$(at 3 5 30)" n32 "night3 05:30 (window end)"; seq_fire "$(at 3 5 29)" n33 "night3 05:29"
say "real runs on the fake NAS (STARTED markers / 2 clients): $(( $(find "$T/nas" -name 'RUN_*_STARTED.txt' | wc -l) / 2 )) ; expected 2"
say "--- a window that crosses midnight (fire=23:00, 5 h)"
fixture C3b; sed -i '' 's/^fire=00:30/fire=23:00/' "$T/lane/seats/wednesday.conf"
seq_fire "$(at 0 22 59)" m0 "22:59 (before open)"; seq_fire "$(at 0 23 0)" m1 "23:00"; seq_fire "$(at 1 0 30)" m2 "00:30 next day (same window)"; seq_fire "$(at 1 3 59)" m3 "03:59"; seq_fire "$(at 1 4 0)" m4 "04:00 (closed)"; seq_fire "$(at 1 23 5)" m5 "23:05 next night"
say "--- daylight saving (TZ=Australia/Sydney): Tuesday's fire=02:30 on 2027-10-03, when 02:00-03:00 does not exist"
"$PY" - "$LANE" <<'PYEOF'
import sys, os, time, datetime
os.environ["TZ"] = "Australia/Sydney"; time.tzset()
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); import nb_core
def ep(y, mo, d, h, mi): return datetime.datetime(y, mo, d, h, mi).timestamp()
for label, now in [("2027-10-03 01:59 AEST", ep(2027,10,3,1,59)), ("2027-10-03 03:00 AEDT (the instant after 01:59:59)", ep(2027,10,3,1,59)+60), ("2027-10-03 03:20 AEDT (2nd fire)", ep(2027,10,3,3,20)), ("2027-10-03 04:10 AEDT (3rd fire)", ep(2027,10,3,4,10)), ("2027-10-03 05:00 AEDT (4th fire)", ep(2027,10,3,5,0)), ("2027-10-03 06:00 AEDT", ep(2027,10,3,6,0))]:
    o, c, inw = nb_core.window_for(now, 2, 30, 3)
    print("  %-52s window %s -> %s  in_window=%s" % (label, time.strftime("%m-%d %H:%M %Z", time.localtime(o)), time.strftime("%m-%d %H:%M %Z", time.localtime(c)), inw))
for label, now in [("2027-04-04 02:30 AEDT (first 02:30)", ep(2027,4,4,2,30)), ("2027-04-04 02:30 AEST (second 02:30, +1h)", ep(2027,4,4,2,30)+3600), ("2027-04-04 05:00 AEST", ep(2027,4,4,5,0))]:
    o, c, inw = nb_core.window_for(now, 2, 30, 3)
    print("  %-52s window %s -> %s  in_window=%s" % (label, time.strftime("%m-%d %H:%M %Z", time.localtime(o)), time.strftime("%m-%d %H:%M %Z", time.localtime(c)), inw))
PYEOF

say; say "### C4a watch threshold: exactly 72 h after the last good run's START"
fixture C4a; rc=$(run "$(at 0 1 0)" g)
for hm in "2 23 59" "3 0 59" "3 1 0" "3 1 1"; do set -- $hm; watch --check --now "$(at $1 $2 $3)" > "$T/out/w.txt" 2>&1; printf 'day+%s %02d:%02d -> rc=%s  %s\n' "$1" "$2" "$3" "$?" "$(head -1 "$T/out/w.txt" | cut -c1-70)"; done

say; say "### C4b NEVER a good backup, the arming mark NOT set, the job fires 4 times a night and is refused (NAS away): does the flag EVER fire?"
fixture C4b; write_mounts none
for d in 0 1 2 3 4 5 6 7 8 9; do
  for hm in "0 31" "1 41" "2 51" "4 1"; do set -- $hm; nightly --now "$(at $d $1 $2)" > "$T/out/k_${d}_$1.txt" 2>&1; done
  watch --flag --now "$(at $d 9 0)" > "$T/out/kw_$d.txt" 2>&1; printf 'day %s 09:00 launcher check: rc=%s  %s\n' "$d" "$?" "$(head -1 "$T/out/kw_$d.txt" | cut -c1-110)"
done
say "CARD-COMMAND lines over 10 days of failed nights (40 refused fires, 10 boots): $(cards k)"
say "--- CONTROL: the same 10 days with --mark-armed run once at day 0"
fixture C4c; write_mounts none; watch --mark-armed --now "$(at 0 0 0)" > "$T/out/arm.txt" 2>&1
for d in 0 1 2 3 4; do for hm in "0 31" "1 41" "2 51" "4 1"; do set -- $hm; nightly --now "$(at $d $1 $2)" > "$T/out/k_${d}_$1.txt" 2>&1; done
  watch --flag --now "$(at $d 9 0)" > "$T/out/kw_$d.txt" 2>&1; printf 'day %s 09:00: rc=%s  %s\n' "$d" "$?" "$(head -1 "$T/out/kw_$d.txt" | cut -c1-80)"; done
say "CARD-COMMAND lines with the arming mark: $(cards k)"

say; say "### C4d WHERE does the one card command land? (the nightly job calls the watch with --flag too)"
fixture C4d; rc=$(run "$(at 0 1 0)" g); write_mounts none
for d in 1 2 3; do nightly --now "$(at $d 1 1)" > "$T/out/launchd_stdout_night$d.txt" 2>&1; done
say "the scheduled job's own stdout on night 3 (under launchd this is ~/Library/Logs/<seat>_nasbackup.out) holds $(/usr/bin/grep -c 'CARD-COMMAND:' "$T/out/launchd_stdout_night3.txt") CARD-COMMAND line"
watch --flag --now "$(at 3 9 0)" > "$T/out/launcher_boot.txt" 2>&1; say "the launcher's --flag at the next boot: rc=$? ; CARD-COMMAND lines printed: $(/usr/bin/grep -c 'CARD-COMMAND:' "$T/out/launcher_boot.txt") ; it says: $(sed -n 2p "$T/out/launcher_boot.txt" | cut -c1-200)"
watch --check --now "$(at 3 9 1)" > "$T/out/doctor.txt" 2>&1; say "doctor's --check: rc=$? ; CARD-COMMAND lines: $(/usr/bin/grep -c 'CARD-COMMAND:' "$T/out/doctor.txt")"
watch --reprint --now "$(at 3 9 2)" > "$T/out/reprint.txt" 2>&1; say "--reprint: rc=$? ; CARD-COMMAND lines: $(/usr/bin/grep -c 'CARD-COMMAND:' "$T/out/reprint.txt")"
say "30 further boots in the same gap print $(for i in $(seq 1 30); do watch --flag --now "$(( $(at 4 9 0) + i*3600 ))" 2>&1; done | /usr/bin/grep -c 'CARD-COMMAND:') more CARD-COMMAND lines (flood check; 0 expected)"
say "state flag: raised=$(state flag.raised) printed_at=$(state flag.printed_at)"

say; say "### C4e a damaged state file"
for kind in garbage empty truncated; do
  fixture "C4e$kind"; rc=$(run "$(at 0 1 0)" g)
  case $kind in garbage) echo "{not json" > "$T/lane/state/wednesday.json";; empty) : > "$T/lane/state/wednesday.json";; truncated) head -c 200 "$T/lane/state/wednesday.json" > "$T/x" && cp "$T/x" "$T/lane/state/wednesday.json";; esac
  watch --flag --now "$(at 5 9 0)" > "$T/out/w.txt" 2>&1; wrc=$?
  nightly --now "$(at 5 0 31)" > "$T/out/n.txt" 2>&1; nrc=$?
  nb --run --now "$(at 5 1 0)" > "$T/out/r.txt" 2>&1; rrc=$?
  say "$kind state file, 5 days after the last good run: watch rc=$wrc [$(tail -1 "$T/out/w.txt" | cut -c1-70)] ; nightly rc=$nrc [$(tail -1 "$T/out/n.txt" | cut -c1-60)] ; nightly.log lines for that fire: $(/usr/bin/grep -c '2026-12-06' "$T/lane/logs/wednesday/nightly.log" 2>/dev/null) ; run rc=$rrc [$(/usr/bin/grep -c 'GOOD:' "$T/out/r.txt") GOOD] state after: $(head -c 30 "$T/lane/state/wednesday.json" | tr '\n' ' ')"
done

say; say "### C5 NAS not mounted but a plain local folder sits at the mount path; and the NAS vanishing mid-run"
fixture C5; write_mounts none; b="$(find "$T/nas" | wc -l | tr -d ' ')"
rc=$(run "$(at 0 1 0)" r); say "rc=$rc ; entries under the local folder before/after: $b/$(find "$T/nas" | wc -l | tr -d ' ') ; state: last_attempt=$(state last_attempt.status) last_good=$(state last_good)"
nightly --now "$(at 0 1 5)" > "$T/out/n.txt" 2>&1; say "nightly rc=$? ; watch after 4 such days: $(watch --check --now "$(at 4 9 0)" 2>&1 | head -1 | cut -c1-90)"
fixture C5b; f="$T/stub/rsync_unmount"; { echo '#!/bin/bash'; echo "REAL=$REAL_RSYNC"; echo 'for a in "$@"; do if [ "$a" = "--version" ]; then exec "$REAL" --version; fi; done'
  echo "mv '$T/nas' '$T/nas_unmounted'; mkdir '$T/nas'; echo 'rsync: connection unexpectedly closed' >&2; exit 12"; } > "$f"; chmod +x "$f"; CONF_RSYNC="$f"; write_conf
rc=$(run "$(at 0 1 0)" r); say "share replaced mid-run by an EMPTY LOCAL folder: rc=$rc ; state=$(state last_attempt.status) ; files the tool then wrote into the local folder: $(find "$T/nas" -type f | wc -l | tr -d ' ') ; dirs: $(find "$T/nas" -mindepth 1 -type d | wc -l | tr -d ' ')"
/usr/bin/grep -E '  - ' "$T/out/r.txt" | cut -c1-200

say; say "### C6 HOLD present: nightly fires, watch"
fixture C6; echo held > "$T/lane/HOLD_wednesday"; watch --mark-armed --now "$(at 0 0 0)" > /dev/null 2>&1
nightly --now "$(at 5 0 31)" > "$T/out/n.txt" 2>&1; say "nightly under HOLD, 5 days after arming: rc=$? ; CARD lines: $(/usr/bin/grep -c 'CARD-COMMAND' "$T/out/n.txt") ; $(tail -1 "$T/out/n.txt" | cut -c1-140)"
