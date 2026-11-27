#!/bin/bash
# N11 — what governs a long first copy: the cap, an interruption, resumability, the index, the watchdog; and a
# detected-but-unrepaired destination mismatch (N3e); a 2.2 GiB file (N2e redo); conventional credential names (N12).
# Fresh checker. Fake NAS only.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib2.sh"
W() { echo "$T/vol/WEDNESDAY"; }
many() { for i in $(seq 1 "$1"); do head -c 1024 /dev/urandom | base64 > "$(W)/sub/f$i.txt"; done; }
pyof() { pgrep -f "nb_core.py backup --seat wednesday --tree $T/vol/WEDNESDAY" | head -1; }
delivered() { find "$(CUR)/sub" -type f 2>/dev/null | wc -l | tr -d ' '; }
SLOW='exec "$REAL" --bwlimit=60 "$@"'

say "### N11a a first copy INTERRUPTED (SIGTERM) in the middle of pass 1. 1,500 files; the engine is throttled."
fixture N11a; many 1500; CONF_RSYNC="$(mkstub rsync_bw "$SLOW")"; write_conf
nb --run --now "$(at 0 14 0)" --out-of-sequence card-first-copy-01 --max-seconds 3600 > "$T/out/k.txt" 2>&1 & sleep 9; P="$(pyof)"; kill -TERM "$P" 2>&1; sleep 3
say "after SIGTERM: delivered to the destination: $(delivered) of 1500 | index rows: $(idxrows) | state last_attempt=$(state last_attempt.status) last_good=$(state last_good) | lock left: $([ -d "$T/lane/state/wednesday.lock.d" ] && echo YES || echo no) | COMPLETE markers: $(find "$T/nas" -name '*COMPLETE*' | wc -l | tr -d ' ')"
say "   its last lines: $(tail -4 "$T/out/k.txt" | head -2 | tr '\n' '~' | cut -c1-200)"
CONF_RSYNC=""; write_conf; rc=$(nb --run --now "$(at 0 14 30)" --out-of-sequence card-first-copy-01 --max-seconds 3600 > "$T/out/r2.txt" 2>&1; echo $?)
say "the resume: rc=$rc GOOD=$(good r2) | $(line r2 'to copy:' 1 50 | sed 's/^ *//') | $(line r2 'compared by sha256' 1 110 | sed 's/^ *//') | index rows now: $(idxrows)"

say; say "### N11b the same copy stopped by the CAP (--max-seconds 8)."
fixture N11b; many 1500; CONF_RSYNC="$(mkstub rsync_bw "$SLOW")"; write_conf
rc=$(nb --run --now "$(at 0 14 0)" --out-of-sequence card-first-copy-01 --max-seconds 8 > "$T/out/k.txt" 2>&1; echo $?)
say "rc=$rc | delivered: $(delivered) of 1500 | index rows: $(idxrows) | state last_attempt=$(state last_attempt.status) last_good=$(state last_good) | NOT DELIVERED count in state: $(state last_attempt.undelivered_count)"
rc=$(nb --run --now "$(at 0 14 30)" --out-of-sequence card-first-copy-01 --max-seconds 8 > "$T/out/k2.txt" 2>&1; echo $?); say "second capped run: rc=$rc | delivered: $(delivered) | index rows: $(idxrows) | $(line k2 'to copy:' 1 50 | sed 's/^ *//')"
CONF_RSYNC=""; write_conf; rc=$(nb --run --now "$(at 0 15 0)" --out-of-sequence card-first-copy-01 --max-seconds 3600 > "$T/out/r3.txt" 2>&1; echo $?); say "finishing run: rc=$rc GOOD=$(good r3) | $(line r3 'to copy:' 1 50 | sed 's/^ *//')"

say; say "### N11c the WATCHDOG fires while the proof loop is still reading files back (INSTRUMENT: a patched COPY of the engine — the 900 s margin made 2 s and each sha256 slowed by 20 ms — so the case fits in seconds; the real margin is 900 s after the cap)."
fixture N11c; many 1500; PL="$T/patched/WEDNESDAY/2_Project_Files"; mkdir -p "$PL/nas-backup" "$PL/fleet/cockpit" "$PL/tools"
cp "$LANE"/nb_core.py "$LANE"/nb_common.sh "$LANE"/nas_backup.sh "$PL/nas-backup/"; cp "$LANE/../fleet/cockpit/seat_resolve.sh" "$PL/fleet/cockpit/"; cp "$LANE/../tools/seat_note.sh" "$PL/tools/"
/opt/homebrew/bin/python3 - "$PL/nas-backup/nb_core.py" <<'EOF'
import sys
p = sys.argv[1]; s = open(p).read()
a = 'signal.alarm(int(cap) + 900)'; b = 'def sha256_of(path):\n    h = hashlib.sha256()'
assert s.count(a) == 1 and s.count(b) == 1
s = s.replace(a, 'signal.alarm(int(cap) + 2)').replace(b, 'def sha256_of(path):\n    time.sleep(0.02)\n    h = hashlib.sha256()')
open(p, "w").write(s)
EOF
CONF_RSYNC="$(mkstub rsync_bw "$SLOW")"; write_conf
rc=$(env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$PL/nas-backup/nas_backup.sh" --run --now "$(at 0 14 0)" --out-of-sequence card-first-copy-01 --max-seconds 8 > "$T/out/k.txt" 2>&1; echo $?)
say "rc=$rc | delivered: $(delivered) of 1500 | index rows: $(idxrows) | WATCHDOG lines: $(/usr/bin/grep -c -F 'WATCHDOG' "$T/out/k.txt") | state last_attempt=$(state last_attempt.status)"
rc=$(env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$PL/nas-backup/nas_backup.sh" --run --now "$(at 0 14 30)" --out-of-sequence card-first-copy-01 --max-seconds 8 > "$T/out/k2.txt" 2>&1; echo $?)
say "the next capped run (must first re-read everything delivered, at plan time): rc=$rc | delivered: $(delivered) | index rows: $(idxrows) | WATCHDOG lines: $(/usr/bin/grep -c -F 'WATCHDOG' "$T/out/k2.txt") | engine passes started: $(/usr/bin/grep -c -F 'engine pass' "$T/out/k2.txt")"
rc=$(env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/WEDNESDAY" "$PL/nas-backup/nas_backup.sh" --run --now "$(at 0 15 0)" --out-of-sequence card-first-copy-01 --max-seconds 8 > "$T/out/k3.txt" 2>&1; echo $?)
say "and the next: rc=$rc | delivered: $(delivered) | index rows: $(idxrows) | WATCHDOG lines: $(/usr/bin/grep -c -F 'WATCHDOG' "$T/out/k3.txt") | engine passes started: $(/usr/bin/grep -c -F 'engine pass' "$T/out/k3.txt")"

say; say "### N3e ONE destination file altered behind the tool's back in a 12-file set (hash_sample=10): once the sample has CAUGHT it, is it repaired, and what do the following nights say?"
fixture N3e; for i in $(seq 1 10); do printf 'filler %05d\n' "$i" > "$(W)/sub/f$i.txt"; done; rc=$(run "$(at 0 1 0)" r0)
printf 'FILLER 00003\n' > "$(CUR)/sub/f3.txt"
for n in 1 2 3 4 5 6 7 8; do rc=$(run "$(at $n 1 0)" r$n); printf '   night %s: rc=%s GOOD=%s | destination f3 = [%s] | %s | %s\n' "$n" "$rc" "$(good r$n)" "$(cat "$(CUR)/sub/f3.txt")" "$(line r$n 'to copy:' 1 22 | sed 's/^ *//')" "$(line r$n 'sha256 sample of files' 1 110 | sed 's/^ *//')"; done

say; say "### N2e (redo; my first try used a tool this Mac lacks) a 2.2 GiB sparse file: copy and proof above 2^31 bytes."
fixture N2e; /opt/homebrew/bin/python3 -c 'import sys; f=open(sys.argv[1],"wb"); f.truncate(2200*1024*1024); f.close()' "$(W)/big.bin"; t0=$(date +%s); rc=$(run "$(at 0 1 0)" r0); t1=$(date +%s)
say "rc=$rc GOOD=$(good r0) in $((t1-t0)) s | destination size $(stat -f %z "$(CUR)/big.bin" 2>&1) vs source $(stat -f %z "$(W)/big.bin")"
: > "$(CUR)/big.bin"; : > "$(W)/big.bin"

say; say "### N12 CONVENTIONAL credential names: does each travel? (marker = arrived on the fake NAS)"
fixture N12; P="$(W)/proj"; i=0
plant() { mkdir -p "$(dirname "$1")"; printf 'MARK[%s]\n' "$2" > "$1"; }
while IFS='|' read -r tag rel; do [ -n "$tag" ] || continue; plant "$P/$rel" "$tag"; done <<'EOF'
c01|.netrc
c02|.pgpass
c03|credentials.json
c04|service-account.json
c05|service-account-prod-1234.json
c06|.aws/credentials
c07|.kube/config
c08|release.keystore
c09|upload.jks
c10|.htpasswd
c11|secrets.yml
c12|.npmrc
c13|terraform.tfvars
c14|prod.auto.tfvars
c15|.docker/config.json
c16|api/local.settings.json
c17|playwright/.auth/token.json
c18|application_default_credentials.json
c19|serviceAccountKey.json
c20|.git-credentials
c21|id_ed25519
c22|payment.skey
c23|mnemonic.txt
c24|wallet/seed-phrase.txt
c25|.vault-token
c26|kubeconfig
c27|auth.json
c28|secrets.toml
c29|AuthKey_ABC123.p8
c30|private_key.txt
c31|.dockercfg
c32|.boto
c33|credentials
c34|htpasswd
c35|key.der
c36|backup.kdbx
c37|terraform.tfstate
c38|.env.production
c39|client_secret_123.json
c40|.pypirc
x01|ordinary-neighbour.md
EOF
rc=$(run "$(at 0 1 0)" r0); say "run rc=$rc GOOD=$(good r0)"
while IFS='|' read -r tag rel; do [ -n "$tag" ] || continue; printf '   %-10s %-40s %s\n' "$( [ "$(onnas "MARK[$tag]")" = 0 ] && echo 'kept out' || echo TRAVELS)" "$rel" "$tag"; done <<'EOF'
c01|.netrc
c02|.pgpass
c03|credentials.json
c04|service-account.json
c05|service-account-prod-1234.json
c06|.aws/credentials
c07|.kube/config
c08|release.keystore
c09|upload.jks
c10|.htpasswd
c11|secrets.yml
c12|.npmrc
c13|terraform.tfvars
c14|prod.auto.tfvars
c15|.docker/config.json
c16|api/local.settings.json
c17|playwright/.auth/token.json
c18|application_default_credentials.json
c19|serviceAccountKey.json
c20|.git-credentials
c21|id_ed25519
c22|payment.skey
c23|mnemonic.txt
c24|wallet/seed-phrase.txt
c25|.vault-token
c26|kubeconfig
c27|auth.json
c28|secrets.toml
c29|AuthKey_ABC123.p8
c30|private_key.txt
c31|.dockercfg
c32|.boto
c33|credentials
c34|htpasswd
c35|key.der
c36|backup.kdbx
c37|terraform.tfstate
c38|.env.production
c39|client_secret_123.json
c40|.pypirc
x01|ordinary-neighbour.md
EOF
