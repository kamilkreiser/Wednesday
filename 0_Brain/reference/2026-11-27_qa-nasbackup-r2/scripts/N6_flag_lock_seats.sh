#!/bin/bash
# N6/N7/N9 — the flag channel, the lock and process group, the seats table and root isolation. Fresh checker. Fake NAS only.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib2.sh"
W() { echo "$T/vol/WEDNESDAY"; }
TREE_OF_COPY="$(cd -P "$LANE/../.." && pwd)"
doctor_block() { # <now> [strict]  : the proposed block as doctor.sh sources it; strict = under doctor's own `set -uo pipefail`
  ( [ "${2:-}" = strict ] && set -uo pipefail
    QUIET="--quiet"; HARD_FAIL=0; WARNS=0
    ok()   { [ "$QUIET" = "--quiet" ] || printf "  ✓ %s\n" "$1"; }
    warn() { printf "  ⚠ %-38s %s\n" "$1" "${2:-}"; WARNS=$((WARNS+1)); }
    fail() { printf "  ✗ %-38s %s\n" "$1" "${2:-}"; HARD_FAIL=1; }
    PROJECT_DIR="$TREE_OF_COPY"; unset WED_AGENT
    export NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" NB_DOCTOR_NOW="$1"
    . "$LANE/proposed/doctor_nasbackup_block.sh"; echo "  [block done: HARD_FAIL=$HARD_FAIL WARNS=$WARNS]" ) 2>&1; }
w() { watch "$@" > "$T/out/w_$RANDOM.txt" 2>&1; echo "rc=$? $(ls -t "$T"/out/w_*.txt | head -1 | xargs head -1 | cut -c1-230)"; }
pyof() { pgrep -f "nb_core.py backup --seat wednesday --tree $T/vol/WEDNESDAY" | head -1; }

say "### N6a CONTROL: last good day 0; the NAS away on nights 1, 2, 3. What a seat's boot (doctor) sees on day 3 at 08:00."
fixture N6a; rc=$(nightly --now "$(at 0 0 31)" > "$T/out/n0.txt" 2>&1; echo $?); write_mounts none
for d in 1 2 3; do nightly --now "$(at $d 0 31)" > "$T/out/n$d.txt" 2>&1; done
say "doctor day 3 08:00 -> $(doctor_block "$(at 3 8 0)" strict | tr '\n' '~' | cut -c1-330)"
say "   as the launcher cuts it for a rotation prompt: [$(doctor_block "$(at 3 8 0)" strict | /usr/bin/grep -i '✗' | cut -c1-400)]"
say "   card commands printed by the three nightly fires (a launchd log): $(cat "$T"/out/n[123].txt | /usr/bin/grep -c -F 'CARD-COMMAND:')"

say; say "### N6b the SAME, but the state file is damaged on day 2 at noon and the next reader is the NIGHTLY job (launchd, a log no seat reads)."
fixture N6b; rc=$(nightly --now "$(at 0 0 31)" > "$T/out/n0.txt" 2>&1; echo $?); write_mounts none
for d in 1 2; do nightly --now "$(at $d 0 31)" > "$T/out/n$d.txt" 2>&1; done
echo '{"seat": "wednesday", "last_good": {"time": 17' > "$T/lane/state/wednesday.json"
nightly --now "$(at 3 0 31)" > "$T/out/n3.txt" 2>&1; say "nightly day 3 00:31: rc=$? ; DAMAGED lines in ITS output: $(/usr/bin/grep -c -F 'STATE FILE DAMAGED' "$T/out/n3.txt")"
say "doctor day 3 08:00 -> $(doctor_block "$(at 3 8 0)" | tr '\n' '~' | cut -c1-330)"
for d in 4 5; do nightly --now "$(at $d 0 31)" > "$T/out/n$d.txt" 2>&1; done
say "doctor day 5 08:00 (5 days without a backup) -> $(doctor_block "$(at 5 8 0)" | tr '\n' '~' | cut -c1-260)"
nightly --now "$(at 6 0 31)" > "$T/out/n6.txt" 2>&1
say "doctor day 6 08:00 -> $(doctor_block "$(at 6 8 0)" | tr '\n' '~' | cut -c1-260)"
say "   quarantined state files: $(find "$T/lane/state" -name '*.damaged.*' | wc -l | tr -d ' ')"

say; say "### N6c the state file damaged, and the FIRST reader is doctor (a seat's boot)."
fixture N6c; rc=$(nightly --now "$(at 0 0 31)" > "$T/out/n0.txt" 2>&1; echo $?); : > "$T/lane/state/wednesday.json"
say "doctor -> $(doctor_block "$(at 1 8 0)" strict | tr '\n' '~' | cut -c1-420)"
say "then the command it names -> $(w --card --now "$(at 1 8 1)")"
say "doctor at the next boot -> $(doctor_block "$(at 1 9 0)" | tr '\n' '~' | cut -c1-200)"

say; say "### N6d the REAL lane's state as it is today (one refused attempt, first_attempt_at 2026-11-27 14:46, no good backup), hold lifted on 2026-12-01 09:00 for the first full copy."
fixture N6d; mkdir -p "$T/lane/state"; cp /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup/state/wednesday.json "$T/lane/state/wednesday.json"
echo held > "$T/lane/HOLD_wednesday"; say "held:   $(w --check --now "$(at 0 9 0)")"
mv "$T/lane/HOLD_wednesday" "$T/lane/HOLD_wednesday.lifted"; say "lifted: $(w --check --now "$(at 0 9 0)")"
say "doctor at a boot that morning -> $(doctor_block "$(at 0 9 5)" | tr '\n' '~' | cut -c1-300)"
mkdir -p "$T/lane/state/wednesday.lock.d"; bash -c 'exec -a nas_backup_fakeholder sleep 60' & HP=$!; sleep 1
printf '{"pid": %s, "pid_started": "%s", "started_local": "2026-12-01 09:10:00", "engine_pgid": null}\n' "$HP" "$(ps -o lstart= -p "$HP" | sed -e 's/^ *//' -e 's/ *$//')" > "$T/lane/state/wednesday.lock.d/owner.json"
say "with a first copy RUNNING (live lock): $(w --check --now "$(at 0 12 0)")"
say "doctor during that run -> $(doctor_block "$(at 0 12 5)" | tr '\n' '~' | cut -c1-200)"
kill "$HP" 2>&1; wait "$HP" 2>&1

say; say "### N6e --mark-raised: can a caller mark a card raised when nothing is overdue, or pre-mark a future gap?"
fixture N6e; rc=$(nightly --now "$(at 0 0 31)" > "$T/out/n0.txt" 2>&1; echo $?); say "not overdue: $(w --mark-raised some-card-id --now "$(at 1 9 0)")"

say; say "### N7a SIGKILL of the tool while its engine is copying (stub engine: sleeps 12 s, then the real copy)."
fixture N7a; CONF_RSYNC="$(mkstub rsync_slow 'sleep 12; exec "$REAL" "$@"')"; write_conf
nb --run --now "$(at 0 1 0)" > "$T/out/k.txt" 2>&1 & sleep 5; P="$(pyof)"; say "tool python pid: ${P:-NOT FOUND} ; engine group recorded in the lock: $(/opt/homebrew/bin/python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("engine_pgid"))' "$T/lane/state/wednesday.lock.d/owner.json" 2>&1)"
kill -KILL "$P" 2>&1; sleep 1
nb --clear-stale-lock > "$T/out/c1.txt" 2>&1; say "clear-stale-lock beside the orphan engine: rc=$? ($(head -1 "$T/out/c1.txt" | cut -c1-120))"
rc=$(run "$(at 0 1 5)" r2); say "a second run beside it: rc=$rc ($(line r2 'REFUSED' 1 120))"
nightly --now "$(at 0 1 31)" > "$T/out/n.txt" 2>&1; say "a nightly fire beside it: $(head -1 "$T/out/n.txt" | cut -c1-140)"
say "state while the orphan runs: last_attempt=$(state last_attempt.status) last_good=$(state last_good)"
sleep 12; say "after the orphan engine ended: files it delivered unrecorded: $(find "$T/nas" -path '*current*' -type f | wc -l | tr -d ' ') ; COMPLETE markers: $(find "$T/nas" -name '*COMPLETE*' | wc -l | tr -d ' ')"
nb --clear-stale-lock > "$T/out/c2.txt" 2>&1; say "clear-stale-lock now: rc=$?"; CONF_RSYNC=""; write_conf; rc=$(run "$(at 0 2 0)" r3); say "rerun: rc=$rc GOOD=$(good r3) | $(line r3 'compared by sha256' 1 120 | sed 's/^ *//')"

say; say "### N7b SIGHUP (the terminal that started a hand-run first copy is closed) versus SIGTERM, mid-engine."
for sig in TERM HUP; do fixture "N7b_$sig"; CONF_RSYNC="$(mkstub rsync_slow 'sleep 10; exec "$REAL" "$@"')"; write_conf
  nb --run --now "$(at 0 1 0)" > "$T/out/k.txt" 2>&1 & sleep 4; P="$(pyof)"; kill -$sig "$P" 2>&1; sleep 2
  say "SIG$sig: tool alive=$(kill -0 "$P" 2>/dev/null && echo yes || echo no) | engine processes still alive=$(pgrep -f "$T/stub/rsync_slow" | wc -l | tr -d ' ') | lock left=$([ -d "$T/lane/state/wednesday.lock.d" ] && echo YES || echo no) | state last_attempt=$(state last_attempt.status) | last output line: $(tail -1 "$T/out/k.txt" | cut -c1-90)"
  sleep 10; done

say; say "### N7c lock shapes: an owner-less lock (old and fresh), a reused pid, a reused ENGINE GROUP id."
fixture N7c; mkdir -p "$T/lane/state/wednesday.lock.d"; rc=$(run "$(at 0 1 0)" r0); say "owner-less lock, seconds old: rc=$rc ($(line r0 'REFUSED' 1 90))"
touch -t 202611010000 "$T/lane/state/wednesday.lock.d"; rc=$(run "$(at 0 1 0)" r1); say "owner-less lock, old: rc=$rc ($(line r1 'REFUSED' 1 60))"; nb --clear-stale-lock > "$T/out/c.txt" 2>&1; say "   clear: rc=$?"
mkdir -p "$T/lane/state/wednesday.lock.d"; sleep 30 & SP=$!; printf '{"pid": %s, "pid_started": "Thu Jan  1 00:00:00 2026", "started_local": "x", "engine_pgid": null}\n' "$SP" > "$T/lane/state/wednesday.lock.d/owner.json"
rc=$(run "$(at 0 1 0)" r2); say "live pid, different start time (pid reuse): rc=$rc ($(line r2 'REFUSED' 1 60))"; nb --clear-stale-lock > "$T/out/c.txt" 2>&1; say "   clear: rc=$?"
mkdir -p "$T/lane/state/wednesday.lock.d"; SG="$(ps -o pgid= -p "$SP" | tr -d ' ')"; printf '{"pid": 999999, "pid_started": "x", "started_local": "x", "engine_pgid": %s}\n' "$SG" > "$T/lane/state/wednesday.lock.d/owner.json"
nb --clear-stale-lock > "$T/out/c3.txt" 2>&1; say "dead holder, engine_pgid = the group of an UNRELATED live process (a reused group id, e.g. after a reboot): clear rc=$? ($(head -1 "$T/out/c3.txt" | cut -c1-150))"
kill "$SP" 2>&1; wait "$SP" 2>&1; nb --clear-stale-lock > "$T/out/c4.txt" 2>&1; say "   after that process ended: clear rc=$?"

say; say "### N9a only Wednesday can run: every command from a TUESDAY and a FRIDAY tree"
fixture N9a; for seatdir in TUESDAY FRIDAY Tuesday friday; do mkdir -p "$T/vol/$seatdir"; echo x > "$T/vol/$seatdir/x.md"
  for cmd in "nas_backup.sh --dry" "nas_backup.sh --run" "nas_backup.sh --scan" "nas_backup.sh --clear-stale-lock" "nas_backup_nightly.sh" "nas_backup_nightly.sh --decide-only" "nas_backup_watch.sh --check" "nas_backup_watch.sh --card" "nas_backup_watch.sh --mark-armed"; do
    set -- $cmd; s="$1"; shift; env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/$seatdir" "$LANE/$s" "$@" > "$T/out/x.txt" 2>&1; printf '   %-8s %-38s rc=%s\n' "$seatdir" "$cmd" "$?"; done; done | sort | uniq -c -f2 | sed 's/^/  /' | awk '{print}' | head -40
say "   files written under the fake NAS by all of that: $(find "$T/nas" -type f | wc -l | tr -d ' ') ; state files created: $(ls "$T/lane/state" 2>/dev/null | wc -l | tr -d ' ')"
say "### N9b other routes to run as another seat or from a wrongly named tree"
t() { printf '   rc=%s  %-92s | %s\n' "$("$@" > "$T/out/y.txt" 2>&1; echo $?)" "$LABEL" "$(head -1 "$T/out/y.txt" | cut -c1-110)"; }
LABEL="WED_AGENT=wednesday on a TUESDAY tree"; t env WED_AGENT=wednesday NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/TUESDAY" "$LANE/nas_backup.sh" --dry
LABEL="WED_AGENT=tuesday on the WEDNESDAY tree"; t env WED_AGENT=tuesday NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$LANE/nas_backup.sh" --dry
ln -s "$T/vol/TUESDAY" "$T/vol/alias_dir"; mkdir -p "$T/vol/links"; ln -s "$T/vol/TUESDAY" "$T/vol/links/WEDNESDAY"
LABEL="a symlink NAMED WEDNESDAY that points at the TUESDAY tree"; t env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/links/WEDNESDAY" "$LANE/nas_backup.sh" --dry
LABEL="engine called directly: --seat wednesday --tree <TUESDAY tree>"; t env -u WED_AGENT NB_TEST_ROOT="$T" "$PY" "$LANE/nb_core.py" backup --seat wednesday --tree "$T/vol/TUESDAY" --dry
LABEL="engine called directly: --seat tuesday --tree <TUESDAY tree>"; t env -u WED_AGENT NB_TEST_ROOT="$T" "$PY" "$LANE/nb_core.py" backup --seat tuesday --tree "$T/vol/TUESDAY" --dry
LABEL="engine called directly: --seat tuesday --tree <WEDNESDAY tree>"; t env -u WED_AGENT NB_TEST_ROOT="$T" "$PY" "$LANE/nb_core.py" backup --seat tuesday --tree "$T/vol/WEDNESDAY" --dry
LABEL="engine called directly: --seat WEDNESDAY (upper case)"; t env -u WED_AGENT NB_TEST_ROOT="$T" "$PY" "$LANE/nb_core.py" backup --seat WEDNESDAY --tree "$T/vol/WEDNESDAY" --dry
mkdir -p "$T/vol/WeDnEsDaY"; LABEL="a tree named WeDnEsDaY"; t env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WeDnEsDaY" "$LANE/nas_backup.sh" --dry
LABEL="engine called directly, no test mode, --tree = the scratch copy's own tree (not the real lane)"; t env -u WED_AGENT -u NB_TEST_ROOT "$PY" "$LANE/nb_core.py" watch --seat tuesday --tree "$TREE_OF_COPY"
mkdir -p "$T/vol/TUESDAY/WEDNESDAY"; echo "TUE-NESTED-MARK" > "$T/vol/TUESDAY/WEDNESDAY/n.md"
write_conf "set=General|nested|$T/vol/TUESDAY/WEDNESDAY"; LABEL="a set= naming a folder called WEDNESDAY inside the TUESDAY tree"; t nb --run --now "$(at 0 1 0)"

say; say "### N9c ROOT ISOLATION by an ANCESTOR: a set= whose source is a PARENT of the other seats' trees and of the Datasec folder (the drive root; the folder that holds the seat trees)."
fixture N9c; mkdir -p "$T/vol/TUESDAY/0_Brain" "$T/vol/FRIDAY" "$T/vol/CODING/Datasec/NexusAI" "$T/vol/Notes"
echo "TUE-SEAT-MARK" > "$T/vol/TUESDAY/0_Brain/tuesday_ledger.md"; echo "TUE-SEAT-MARK-2" > "$T/vol/TUESDAY/plain.md"; echo "FRI-SEAT-MARK" > "$T/vol/FRIDAY/plain.md"; echo "DATASEC-MARK" > "$T/vol/CODING/Datasec/NexusAI/plain.md"; echo "VAULT-MARK" > "$T/vol/Notes/n.md"
write_conf "set=General|DRIVE|$T/vol"
rc=$(run "$(at 0 1 0)" r0); say "set=General|DRIVE|<drive root>: rc=$rc GOOD=$(good r0)"
for m in TUE-SEAT-MARK TUE-SEAT-MARK-2 FRI-SEAT-MARK DATASEC-MARK VAULT-MARK; do printf '   %-18s copies on the fake NAS: %s %s\n' "$m" "$(onnas "$m")" "$(/usr/bin/grep -r -l -F -- "$m" "$T/nas" 2>&1 | head -1 | sed "s|$T/nas/||")"; done
say "   (VAULT-MARK is the positive control: an ordinary folder under the same root must arrive)"
fixture N9c2; mkdir -p "$T/vol/CODING/Datasec/NexusAI" "$T/vol/CODING/tuesday-handover"; echo "DATASEC-MARK" > "$T/vol/CODING/Datasec/NexusAI/plain.md"; echo "TUE-HANDOVER-MARK" > "$T/vol/CODING/tuesday-handover/h.md"
write_conf "set=General|CODINGALL|$T/vol/CODING"; rc=$(run "$(at 0 1 0)" r0); say "set=General|CODINGALL|<the folder that holds the client folders>: rc=$rc | DATASEC-MARK on NAS: $(onnas DATASEC-MARK) | a 'tuesday-handover' folder beside the clients on NAS: $(onnas TUE-HANDOVER-MARK)"
