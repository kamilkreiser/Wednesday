#!/bin/bash
# N1 — is GOOD truthful on round 2's NEW code (prove_arrival, the pass loop, "gone from the source during the run")?
# Fresh checker, 2026-11-27. Fake NAS only.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib2.sh"
W() { echo "$T/vol/WEDNESDAY"; }

say "### N1a a source file that is UNREADABLE (mode 000) from the first night on. Expected: the run is NOT GOOD (an in-scope file is not at the destination)."
fixture N1a; printf 'PRIVATE-LEDGER-MARK-1a\n' > "$(W)/ledger.db"; chmod 000 "$(W)/ledger.db"
for n in 0 1 2; do rc=$(run "$(at $n 1 0)" r$n); say "night $n: rc=$rc GOOD=$(good r$n) | marker on NAS=$(onnas 'PRIVATE-LEDGER-MARK-1a') | $(line r$n 'gone from the source' 1 400 | sed 's/^ *//')"; done
say "state: last_attempt=$(state last_attempt.status) last_good.counts.src_files=$(state last_good.counts.src_files) vanished=$(state last_good.counts.vanished) ; file exists at destination: $([ -e "$(CUR)/ledger.db" ] && echo yes || echo NO)"
say "engine stderr night 0: $(line r0 'stderr' 1 420 | sed 's/^ *//')"
chmod 644 "$(W)/ledger.db"
say "CONTROL the same file readable: $(fixture N1a_ctl; printf 'PRIVATE-LEDGER-MARK-1a\n' > "$(W)/ledger.db"; rc=$(run "$(at 0 1 0)" r0); echo "rc=$rc GOOD=$(good r0) marker on NAS=$(onnas 'PRIVATE-LEDGER-MARK-1a')")"

say; say "### N1b a file that was backed up, then CHANGES and becomes unreadable. Expected: NOT GOOD; destination holds the OLD content."
fixture N1b; printf 'LEDGER-v1\n' > "$(W)/ledger.db"; rc=$(run "$(at 0 1 0)" r0); say "night 0: rc=$rc GOOD=$(good r0)"
sleep 1; printf 'LEDGER-v2-newer-content\n' > "$(W)/ledger.db"; chmod 000 "$(W)/ledger.db"
for n in 1 2; do rc=$(run "$(at $n 1 0)" r$n); say "night $n: rc=$rc GOOD=$(good r$n) | destination=[$(cat "$(CUR)/ledger.db")] | $(line r$n 'gone from the source' 1 400 | sed 's/^ *//')"; done
chmod 644 "$(W)/ledger.db"; say "source (after restoring the mode, to show it): [$(cat "$(W)/ledger.db")]"

say; say "### N1c a source FOLDER becomes unreadable (mode 000) between the listing and the copy (stub does it before calling the real engine). 50 files inside."
fixture N1c; for i in $(seq 1 50); do echo "payload-1c $i" > "$(W)/sub/f$i.txt"; done
CONF_RSYNC="$(mkstub rsync_chmod 'case "$DEST" in */current/WEDNESDAY/) chmod 000 "$T2/vol/WEDNESDAY/sub";; esac; exec "$REAL" "$@"')"; write_conf
rc=$(run "$(at 0 1 0)" r0); chmod 755 "$(W)/sub"
say "rc=$rc GOOD=$(good r0) | files of sub/ at destination: $(find "$(CUR)/sub" -type f 2>&1 | /usr/bin/grep -c 'f[0-9]') of 51 | $(line r0 'proven at the destination' 1 420 | sed 's/^ *//')"
say "state: last_attempt=$(state last_attempt.status) recorded src_files=$(state last_good.counts.src_files) set_counts=$(state last_good.set_counts)"

say; say "### N1d the WHOLE source folder of a set goes away mid-run (stub moves it aside before the real engine: a sub-volume unmounted, a folder renamed). 2 sets; it happens during the first."
fixture N1d; for i in $(seq 1 30); do echo "payload-1d $i" > "$(W)/sub/g$i.txt"; done
CONF_RSYNC="$(mkstub rsync_gone 'case "$DEST" in */current/WEDNESDAY/) mv -n "$T2/vol/WEDNESDAY" "$T2/vol/WEDNESDAY.gone";; esac; "$REAL" "$@"; exit $?')"; write_conf
rc=$(run "$(at 0 1 0)" r0)
say "rc=$rc GOOD=$(good r0) | files at destination under current/WEDNESDAY: $(find "$(CUR)" -type f 2>&1 | wc -l | tr -d ' ') of 32 | $(line r0 'proven at the destination' 1 420 | sed 's/^ *//')"
say "engine line: $(line r0 'engine pass 1' 1 300 | sed 's/^ *//')"
say "last line: $(/usr/bin/grep -F -e 'GOOD:' -e 'FAILED' "$T/out/r0.txt" | head -1 | cut -c1-200)"
say "state: last_attempt=$(state last_attempt.status) last_good.counts.src_files=$(state last_good.counts.src_files) vanished=$(state last_good.counts.vanished)"
say "COMPLETE markers on the NAS: $(find "$T/nas" -name 'RUN_*_COMPLETE.txt' | wc -l | tr -d ' ')"
mv -n "$T/vol/WEDNESDAY.gone" "$T/vol/WEDNESDAY"

say; say "### N2a a file appended to after EVERY pass (stub appends after the real engine). Expected: FAIL, file named; last night's kept copy not overwritten by a re-send."
fixture N2a; printf 'LIVE-v1-night0\n' > "$(W)/live.log"; rc=$(run "$(at 0 1 0)" r0); say "night 0 rc=$rc GOOD=$(good r0)"
sleep 1; printf 'LIVE-v2-night1-start\n' > "$(W)/live.log"
CONF_RSYNC="$(mkstub rsync_append '"$REAL" "$@"; rc=$?; case "$DEST" in */current/WEDNESDAY/) sleep 1; echo "appended after pass $N" >> "$T2/vol/WEDNESDAY/live.log";; esac; exit $rc')"; write_conf
rc=$(run "$(at 1 1 0)" r1)
say "night 1 rc=$rc GOOD=$(good r1) | $(/usr/bin/grep -c -F 'NOT DELIVERED: WEDNESDAY/live.log' "$T/out/r1.txt") NOT DELIVERED line(s) for live.log | engine passes: $(/usr/bin/grep -c -F 'engine pass' "$T/out/r1.txt")"
say "versions folders: $(ls "$(VER)" | tr '\n' ' ')"
say "copies of live.log under versions/: $(find "$(VER)" -name live.log | wc -l | tr -d ' ') ; the night-0 copy (LIVE-v1-night0) kept: $(/usr/bin/grep -r -l -F 'LIVE-v1-night0' "$(VER)" | wc -l | tr -d ' ')"

say; say "### N2b the DESTINATION copy is altered between the copy and the proof (stub rewrites it, same size). Expected: FAIL."
fixture N2b; CONF_RSYNC="$(mkstub rsync_altdst '"$REAL" "$@"; rc=$?; f="$T2/nas/General/Wednesday/nightly-backup/current/WEDNESDAY/a.txt"; [ -f "$f" ] && printf "XXX content of a\n" > "$f"; exit $rc')"; write_conf
rc=$(run "$(at 0 1 0)" r0); say "rc=$rc GOOD=$(good r0) | $(line r0 'NOT DELIVERED: ' 1 120 | sed 's/^ *//')"

say; say "### N2c a source file is replaced by a FOLDER between the copy and the proof."
fixture N2c; CONF_RSYNC="$(mkstub rsync_f2d '"$REAL" "$@"; rc=$?; f="$T2/vol/WEDNESDAY/a.txt"; if [ -f "$f" ]; then mv -n "$f" "$T2/a.aside"; mkdir "$f"; echo inner > "$f/inner.txt"; fi; exit $rc')"; write_conf
rc=$(run "$(at 0 1 0)" r0); say "night 0 rc=$rc GOOD=$(good r0) | $(line r0 'gone from the source' 1 420 | sed 's/^ *//')"
CONF_RSYNC=""; write_conf; rc=$(run "$(at 1 1 0)" r1); say "night 1 rc=$rc GOOD=$(good r1) | $(line r1 'TYPE CHANGE' 1 200 | sed 's/^ *//') | old file content under versions: $(/usr/bin/grep -r -l -F 'old content of a' "$(VER)" 2>&1 | wc -l | tr -d ' ') | inner.txt at destination: $([ -f "$(CUR)/a.txt/inner.txt" ] && echo yes || echo NO)"

say; say "### N2d a source file is replaced by a SYMLINK into a secrets folder between the copy and the proof. Expected: FAIL or out of scope; the secret never on the NAS."
fixture N2d; mkdir -p "$(W)/4_Credentials"; printf 'S3CR3T-MARK-2d\n' > "$(W)/4_Credentials/secret.txt"
CONF_RSYNC="$(mkstub rsync_f2l '"$REAL" "$@"; rc=$?; f="$T2/vol/WEDNESDAY/a.txt"; if [ -f "$f" ] && [ ! -L "$f" ]; then mv -n "$f" "$T2/a.aside"; ln -s 4_Credentials/secret.txt "$f"; fi; exit $rc')"; write_conf
rc=$(run "$(at 0 1 0)" r0); say "rc=$rc GOOD=$(good r0) | secret marker on NAS=$(onnas 'S3CR3T-MARK-2d') | engine passes: $(/usr/bin/grep -c -F 'engine pass' "$T/out/r0.txt") | $(line r0 'NOT DELIVERED: ' 1 120 | sed 's/^ *//')"

say; say "### N2f a file that WAS delivered becomes unreadable before the proof (stub: chmod 000 after the real engine)."
fixture N2f; CONF_RSYNC="$(mkstub rsync_post000 '"$REAL" "$@"; rc=$?; chmod 000 "$T2/vol/WEDNESDAY/a.txt"; exit $rc')"; write_conf
rc=$(run "$(at 0 1 0)" r0); chmod 644 "$(W)/a.txt"; say "rc=$rc GOOD=$(good r0) | a.txt at destination identical to source: $(cmp -s "$(W)/a.txt" "$(CUR)/a.txt" && echo yes || echo NO) | $(line r0 'gone from the source' 1 420 | sed 's/^ *//')"

say; say "### N10 the NAS leaves the mount table after the preflight (stub rewrites the fake mount table on its first call). Expected: the run does not say GOOD without re-checking."
fixture N10; CONF_RSYNC="$(mkstub rsync_unmount 'if [ "$N" = 1 ]; then /usr/bin/grep -v smbfs "$T2/mount.txt" > "$T2/mount.tmp"; mv "$T2/mount.tmp" "$T2/mount.txt"; fi; exec "$REAL" "$@"')"; write_conf
rc=$(run "$(at 0 1 0)" r0); say "rc=$rc GOOD=$(good r0) | smbfs lines left in the mount table: $(/usr/bin/grep -c smbfs "$T/mount.txt") | sets processed after the unmount: $(/usr/bin/grep -c -F -- '--- set' "$T/out/r0.txt")"
rc=$(run "$(at 1 1 0)" r1); say "CONTROL the next run with the table as left: rc=$rc ($(line r1 'not mounted' 1 80))"

say; say "### N2e a 2.2 GiB sparse file (size above 2^31): copy and proof."
fixture N2e; /usr/bin/mkfile -n 2200m "$(W)/big.bin"; t0=$(date +%s); rc=$(run "$(at 0 1 0)" r0); t1=$(date +%s)
say "rc=$rc GOOD=$(good r0) in $((t1-t0)) s | destination size $(stat -f %z "$(CUR)/big.bin" 2>&1) vs source $(stat -f %z "$(W)/big.bin")"
mkdir -p "$S/held"; mv "$(CUR)/big.bin" "$S/held/big_$$.dst"; mv "$(W)/big.bin" "$S/held/big_$$.src"; : > "$S/held/big_$$.dst"; : > "$S/held/big_$$.src"
