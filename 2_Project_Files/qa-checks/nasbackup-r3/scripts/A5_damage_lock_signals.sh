#!/bin/bash
# A5 — item 5: tracebacks, the lock on every exit path, the hold, the damage notice, signals after the accounting.
. "$(dirname "$0")/lib3.sh"; date; uptime
tb() { /usr/bin/grep -c -F 'Traceback' "$T/o/$1.txt"; }
lk() { [ -d "$T/lane/state/wednesday.lock.d" ] && echo LEFT || echo released; }
say "== a. a signal AFTER the accounting (fault injection, scripts/A5_inject.py)"
for pt in manifest after_complete; do for sg in SIGTERM SIGHUP; do
  fixture "sig_${pt}_$sg"
  env -u WED_AGENT NB_TEST_ROOT="$T" "$PY" "$(dirname "$0")/A5_inject.py" "$LANE" "$pt" "$sg" -- backup --seat wednesday --tree "$T/vol/WEDNESDAY" --run --now "$(at 0 1 0)" > "$T/o/r.txt" 2>&1; rc=$?
  say "  $sg at '$pt': rc=$rc traceback lines=$(tb r) GOOD line=$(good r) lock=$(lk) state.last_attempt=$(state last_attempt.status) last_good=$( [ "$(state last_good)" = None ] && echo None || echo set) COMPLETE on NAS=$(completed)"
  say "     watch then says: $(watch --check --now "$(at 0 2 0)" 2>&1 | head -1 | cut -c1-170)"
  say "     next run: rc=$(run "$(at 0 2 5)" r2) GOOD=$(good r2)"
done; done
say "== b. things that are not Refused: unwritable state folder, state file that is a folder, lock folder cannot be made"
fixture st_dir; mkdir -p "$T/lane/state/wednesday.json"
rc=$(run "$(at 0 1 0)" r); say "  state file is a FOLDER: run rc=$rc traceback=$(tb r) lock=$(lk); first line: $(sed -n 2p "$T/o/r.txt" | cut -c1-150)"
watch --check --now "$(at 0 2 0)" > "$T/o/w.txt" 2>&1; say "    watch rc=$? traceback=$(tb w)"
fixture st_ro; mkdir -p "$T/lane/state"; echo garbage > "$T/lane/state/wednesday.json"; chmod 555 "$T/lane/state"
rc=$(run "$(at 0 1 0)" r); say "  damaged state in a READ-ONLY state folder: run rc=$rc traceback=$(tb r) last line: $(tail -1 "$T/o/r.txt" | cut -c1-130)"
watch --check --now "$(at 0 2 0)" > "$T/o/w.txt" 2>&1; say "    watch rc=$? traceback=$(tb w) last line: $(tail -1 "$T/o/w.txt" | cut -c1-130)"
nightly --now "$(at 0 0 31)" > "$T/o/n.txt" 2>&1; say "    nightly rc=$? traceback=$(tb n)"
chmod 755 "$T/lane/state"
fixture lock_file; mkdir -p "$T/lane/state"; echo x > "$T/lane/state/wednesday.lock.d"
rc=$(run "$(at 0 1 0)" r); say "  the lock path is a FILE: run rc=$rc traceback=$(tb r); line: $(line r 'lock' 1 150)"
fixture idx_dir; mkdir -p "$T/lane/state/wednesday.index.sqlite"
rc=$(run "$(at 0 1 0)" r); say "  the index path is a FOLDER: run rc=$rc traceback=$(tb r) GOOD=$(good r) lock=$(lk) notice=$([ -s "$T/lane/state/DAMAGE_NOTICE_wednesday.jsonl" ] && echo yes || echo no)"
fixture idx_locked; say "  night0 rc=$(run "$(at 0 1 0)" r0)"
"$PY" -c 'import sqlite3,sys,time
db=sqlite3.connect(sys.argv[1]); db.execute("BEGIN EXCLUSIVE"); open(sys.argv[2],"w").write("held"); time.sleep(14)' "$T/lane/state/wednesday.index.sqlite" "$T/o/held.flag" & HP=$!
i=0; while [ ! -f "$T/o/held.flag" ] && [ $i -lt 50 ]; do sleep 0.1; i=$((i+1)); done
rc=$(run "$(at 1 1 0)" r1); wait $HP
say "  a healthy index LOCKED by another reader for 14 s: run rc=$rc GOOD=$(good r1) traceback=$(tb r1); $(line r1 'INDEX DAMAGED' 1 150)"
say "     healthy index quarantined as damaged: $(find "$T/lane/state" -name '*.index.sqlite.damaged.*' | wc -l | tr -d ' ') ; damage notice written: $([ -s "$T/lane/state/DAMAGE_NOTICE_wednesday.jsonl" ] && echo yes || echo no)"
say "== c. every caller finding a damaged state; the notice until --ack-damage; a dry run moves nothing"
for caller in nightly watch run dry; do
  fixture "dm_$caller"; x=$(run "$(at 0 1 0)" r0); echo '{"seat": "wednesday", "last_good": 7}' > "$T/lane/state/wednesday.json"
  case $caller in nightly) nightly --now "$(at 1 0 31)" > "$T/o/c.txt" 2>&1;; watch) watch --check --now "$(at 1 0 31)" > "$T/o/c.txt" 2>&1;; run) nb --run --now "$(at 1 0 31)" > "$T/o/c.txt" 2>&1;; dry) nb --dry > "$T/o/c.txt" 2>&1;; esac; rc=$?
  n=$([ -s "$T/lane/state/DAMAGE_NOTICE_wednesday.jsonl" ] && wc -l < "$T/lane/state/DAMAGE_NOTICE_wednesday.jsonl" | tr -d ' ' || echo 0)
  watch --check --now "$(at 1 9 0)" > "$T/o/w.txt" 2>&1; wrc=$?
  say "  found by $caller: rc=$rc traceback=$(tb c) notice lines=$n moved aside=$(find "$T/lane/state" -name 'wednesday.json.damaged.*' | wc -l | tr -d ' ') ; the watch afterwards rc=$wrc"
done
say "== d. the HOLD: does anything run or reach the NAS under it; what is recorded when the conf is ALSO refused under the hold"
fixture hold; echo held > "$T/lane/HOLD_wednesday"; B4="$(find "$T/nas" | sort | shasum | cut -c1-12)"
for args in "--run" "--run --out-of-sequence card-abcdef" "--run --accept-shrink card-abcdef" "--run --max-seconds 9"; do nb $args --now "$(at 0 1 0)" > "$T/o/h.txt" 2>&1; printf '  %s -> rc=%s; ' "$args" "$?"; done; echo
nightly --now "$(at 0 0 31)" > "$T/o/hn.txt" 2>&1; say "  nightly -> rc=$? ; fake NAS unchanged: $([ "$B4" = "$(find "$T/nas" | sort | shasum | cut -c1-12)" ] && echo yes || echo NO) ; engine processes started: $(/usr/bin/grep -c -F 'engine:' "$T/o/h.txt")"
say "  state after held runs: last_attempt=$(state last_attempt.status) first_attempt_at=$(state first_attempt_at) held_seen=$(state held_seen)"
sed -e 's/^status=confirmed/status=unconfirmed/' "$T/lane/seats/wednesday.conf" > "$T/c.tmp"; mv "$T/c.tmp" "$T/lane/seats/wednesday.conf"
nb --run --now "$(at 0 2 0)" > "$T/o/h2.txt" 2>&1; say "  a --run under the hold with an UNCONFIRMED conf: rc=$? recorded as $(state last_attempt.status); first_attempt_at=$(state first_attempt_at) (None = clock not started)"
std_conf; mv "$T/lane/HOLD_wednesday" "$T/lane/HOLD_wednesday.lifted"
watch --check --now "$(at 4 9 0)" > "$T/o/h3.txt" 2>&1; say "  hold lifted four days later, first check: rc=$? $(head -1 "$T/o/h3.txt" | cut -c1-150)"
say "  a HOLD file spelled in another case (hold_wednesday) on this case-folding scratch volume:"
fixture hold2; echo held > "$T/lane/hold_wednesday"; say "    rc=$(run "$(at 0 1 0)" r) (3 = held)"
say "== e. mount: another share mounted at the NAS path; the share leaves mid-chunk"
fixture mnt; { echo "/dev/disk9s1 on $T/vol (apfs, local, nodev)"; echo "//user@nas.example/SomeOtherShare on $T/nas (smbfs, nodev, nosuid)"; } > "$T/mount.txt"
say "  another share's name on the mount line: rc=$(run "$(at 0 1 0)" r) GOOD=$(good r)"
fixture mnt2; for i in $(seq 1 12); do echo "p $i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done
CONF_RSYNC="$(mk_stub unm 'if [ "$N" = 2 ]; then /usr/bin/grep -v smbfs "$STUBDIR/../mount.txt" > "$STUBDIR/../mount.tmp"; mv "$STUBDIR/../mount.tmp" "$STUBDIR/../mount.txt"; fi; exec "$REAL" "$@"')"; CONF_CHUNK=4; std_conf
say "  share leaves the table during chunk 2 of 4: rc=$(run "$(at 0 1 0)" r) GOOD=$(good r) engine calls=$(cat "$T/stub/calls") index rows=$(idxrows); $(line r 'no longer mounted' 1 120)"
date; uptime
