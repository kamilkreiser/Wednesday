#!/bin/bash
# H — can a run be recorded GOOD while a changed file did NOT reach the destination?
# Route under test: a SAME-SIZE content change whose transfer fails for that one file (engine exit 23, which the
# tool tolerates by design and "accounts for one by one afterwards" - by SIZE). Per-file failure is produced two
# ways: (1) the destination copy is immutable (chflags uchg: stands in for a file locked or ACL-protected on the
# share); (2) a stub engine that skips one listed file and exits 23 (stands in for any per-file transfer error).
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
run() { nb --run --now "$1" > "$T/out/$2.txt" 2>&1; echo $?; }
mk() { fixture "$1"; for i in $(seq 1 300); do printf 'filler %04d\n' "$i" > "$T/vol/WEDNESDAY/sub/f$i.txt"; done; printf 'LEDGER-v1-AAAA\n' > "$T/vol/WEDNESDAY/ledger.db"; sed -i '' 's/^hash_sample=10/hash_sample=40/' "$T/lane/seats/wednesday.conf"; }

say "### H1 destination copy immutable (uchg), same-size change at the source; hash_sample=40 (the shipped default), 303 files in the set"
mk H1; rc=$(run "$(at 0 1 0)" r0); say "first run rc=$rc"
chflags uchg "$(CUR)/ledger.db"
for night in 1 2 3 4 5 6; do
  sleep 1; printf 'LEDGER-v%d-BBBB\n' "$((night+1))" > "$T/vol/WEDNESDAY/ledger.db"
  rc=$(run "$(at $night 1 0)" r$night)
  printf 'night %s: rc=%s  GOOD lines=%s  engine rc=[%s]  source=[%s]  destination current=[%s]  state=%s\n' "$night" "$rc" "$(/usr/bin/grep -c 'GOOD:' "$T/out/r$night.txt")" "$(/usr/bin/grep -o -E 'engine result: [a-z-]+ rc=[0-9]+' "$T/out/r$night.txt" | head -1)" "$(cat "$T/vol/WEDNESDAY/ledger.db")" "$(cat "$(CUR)/ledger.db")" "$(state last_attempt.status)"
done
/usr/bin/grep -h -E 'engine stderr|sha256 sample|PROBLEM|  - ' "$T"/out/r1.txt | cut -c1-240
say "night 7, NOTHING changed at the source since night 6:"; rc=$(run "$(at 7 1 0)" r7); say "  rc=$rc ; $(/usr/bin/grep -m1 'to copy:' "$T/out/r7.txt" | cut -c1-60) ; source=[$(cat "$T/vol/WEDNESDAY/ledger.db")] destination=[$(cat "$(CUR)/ledger.db")] ; versions of ledger.db kept: $(find "$(VER)" -name ledger.db | wc -l | tr -d ' ')"
chflags nouchg "$(CUR)/ledger.db"

say; say "### H2 an engine that skips one listed file and exits 23 (per-file transfer error), same-size change"
mk H2; rc=$(run "$(at 0 1 0)" r0)
f="$T/stub/rsync_skip_one"; { echo '#!/bin/bash'; echo "REAL=$REAL_RSYNC"; echo 'for a in "$@"; do if [ "$a" = "--version" ]; then exec "$REAL" --version; fi; done'
  echo 'args=(); for a in "$@"; do case "$a" in --files-from=*) L="${a#--files-from=}"; tr "\0" "\n" < "$L" | /usr/bin/grep -v "^ledger.db$" | tr "\n" "\0" > "$L.filtered"; args+=( "--files-from=$L.filtered" );; *) args+=( "$a" );; esac; done'
  echo '"$REAL" "${args[@]}"; echo "rsync: [sender] read errors mapping \"ledger.db\": Input/output error (5)" >&2; exit 23'; } > "$f"; chmod +x "$f"; CONF_RSYNC="$f"; write_conf; sed -i '' 's/^hash_sample=10/hash_sample=40/' "$T/lane/seats/wednesday.conf"
good=0; for night in 1 2 3 4 5 6 7 8 9 10; do sleep 1; printf 'LEDGER-v%d-CCCC\n' "$((night+1))" > "$T/vol/WEDNESDAY/ledger.db"; echo "also changed $night" > "$T/vol/WEDNESDAY/a.txt"
  rc=$(run "$(at $night 1 0)" r$night); g="$(/usr/bin/grep -c 'GOOD:' "$T/out/r$night.txt")"; good=$((good+g)); printf 'night %s: rc=%s GOOD=%s destination=[%s]\n' "$night" "$rc" "$g" "$(cat "$(CUR)/ledger.db")"; done
say "H2: nights recorded GOOD with the changed file NOT delivered: $good of 10 ; source now [$(cat "$T/vol/WEDNESDAY/ledger.db")], destination [$(cat "$(CUR)/ledger.db")]"

say; say "### H3 CONTROLS: (a) the same per-file failure with a DIFFERENT-size change must FAIL; (b) the same same-size change with a healthy engine must arrive"
mk H3; rc=$(run "$(at 0 1 0)" r0); CONF_RSYNC="$T/../H2_$$/stub/rsync_skip_one"; cp "$S/fx/H2_$$/stub/rsync_skip_one" "$T/stub/"; CONF_RSYNC="$T/stub/rsync_skip_one"; write_conf
printf 'LEDGER-v2-longer-than-before\n' > "$T/vol/WEDNESDAY/ledger.db"; rc=$(run "$(at 1 1 0)" r1); say "(a) different size, transfer fails: rc=$rc GOOD=$(/usr/bin/grep -c 'GOOD:' "$T/out/r1.txt") state=$(state last_attempt.status)"
mk H3b; rc=$(run "$(at 0 1 0)" r0); sleep 1; printf 'LEDGER-v2-DDDD\n' > "$T/vol/WEDNESDAY/ledger.db"; rc=$(run "$(at 1 1 0)" r1); say "(b) same size, healthy engine: rc=$rc destination=[$(cat "$(CUR)/ledger.db")]"
