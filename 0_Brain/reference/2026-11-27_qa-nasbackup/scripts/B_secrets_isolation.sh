#!/bin/bash
# B — can a secret or another client's folder reach the fake NAS? Every planted item carries a unique marker
# string in its CONTENT; the instrument is grep -r for the marker under the fake NAS (so a renamed arrival counts).
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
run() { nb --run --now "$1" > "$T/out/$2.txt" 2>&1; echo $?; }
onnas() { /usr/bin/grep -r -l -a -F -- "$1" "$T/nas" 2>/dev/null | /usr/bin/grep -v '/manifests/' | wc -l | tr -d ' '; }
plant() { mkdir -p "$(dirname "$1")"; echo "MARK[$2]" > "$1"; }
report() { # label marker   -> LEAKED / kept out
  local n; n="$(onnas "MARK[$2]")"; if [ "$n" = 0 ]; then printf 'kept out   %-34s %s\n' "$2" "$1"; else printf 'LEAKED     %-34s %s -> %s\n' "$2" "$1" "$(/usr/bin/grep -r -l -a -F -- "MARK[$2]" "$T/nas" | /usr/bin/grep -v /manifests/ | head -1 | sed "s|$T/nas/||")"; fi; }

say "### B1 the listed secret names, nested deep, with spaces in the path (expected: all kept out) + POSITIVE CONTROL"
fixture B1; W="$T/vol/WEDNESDAY"; X="$T/vol/CODING/Secuura/Blockchain"
plant "$W/deep/a b/c/4_Credentials/k.txt" s1; plant "$W/deep/a b/c/3_Access_Keys/github_deploy_rw" s2; plant "$W/deep/.env" s3; plant "$W/deep/.env.production" s4
plant "$W/deep/prod.env" s5; plant "$W/deep/cert.pem" s6; plant "$W/deep/tls.key" s7; plant "$W/deep/id_rsa" s8; plant "$W/deep/id_ed25519.pub" s9
plant "$X/4_Credentials/.azure/msal_token_cache.json" s10; plant "$X/sub dir/credentials.json" s11; plant "$X/.ssh/config" s12; plant "$W/deep/ordinary.txt" CONTROL
rc=$(run "$(at 0 1 0)" r); say "run rc=$rc ($(/usr/bin/grep -c 'GOOD:' "$T/out/r.txt") GOOD line)"
for m in s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12; do report "listed name" "$m"; done
verdict "B1 POSITIVE CONTROL: the ordinary file's marker IS found on the fake NAS by the same grep" 1 "$(onnas 'MARK[CONTROL]')"

say; say "### B3 the SAME secret names in a different CASE (the drive is case-sensitive; fnmatchcase is used)"
fixture B3; W="$T/vol/WEDNESDAY"
plant "$W/p/4_credentials/k.txt" c1; plant "$W/q/4_CREDENTIALS/k.txt" c2; plant "$W/p/3_access_keys/deploy" c3; plant "$W/p/.ENV" c4; plant "$W/p/.Env.local" c5
plant "$W/p/server.PEM" c6; plant "$W/p/private.KEY" c7; plant "$W/p/ID_RSA" c8; plant "$W/p/Credentials.json" c9; plant "$W/p/Secrets.json" c10; plant "$W/p/.SSH/config" c11; plant "$W/p/.AWS/credentials" c12
rc=$(run "$(at 0 1 0)" r); say "run rc=$rc ($(/usr/bin/grep -c 'GOOD:' "$T/out/r.txt") GOOD line)"
for m in c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 c12; do report "case variant" "$m"; done

say; say "### B4 secret-shaped names the fixed list does not have (copies, conflict copies, common credential files)"
fixture B4; W="$T/vol/WEDNESDAY"
plant "$W/p/4_Credentials (conflict_on_2026-09-17)/k.txt" n1; plant "$W/p/4_Credentials.bak/k.txt" n2; plant "$W/p/4_Credentials copy/k.txt" n3; plant "$W/p/old_3_Access_Keys/deploy" n4
plant "$W/p/.env (conflict_on_2026-09-17)" n5; plant "$W/p/prod.env.bak" n6; plant "$W/p/env.backup" n7; plant "$W/p/.envrc" n8
plant "$W/p/github_deploy_rw" n9; plant "$W/p/deploy_key" n10; plant "$W/p/key.ppk" n11; plant "$W/p/.git-credentials" n12; plant "$W/p/.kube/config" n13; plant "$W/p/.docker/config.json" n14
plant "$W/p/terraform.tfstate" n15; plant "$W/p/client_secret.json" n16; plant "$W/p/token.json" n17; plant "$W/p/secrets.yaml" n18; plant "$W/p/azureProfile.json" n19; plant "$W/p/Agent Mail.md" n20
plant "$W/p/cert.crt" n21; plant "$W/p/wallet.skey" n22; plant "$W/p/.htpasswd" n23; plant "$W/p/application_default_credentials.json" n24
rc=$(run "$(at 0 1 0)" r); say "run rc=$rc"
for m in n1 n2 n3 n4 n5 n6 n7 n8 n9 n10 n11 n12 n13 n14 n15 n16 n17 n18 n19 n20 n21 n22 n23 n24; do report "unlisted shape" "$m"; done

say; say "### B5/B6 links INTO a secrets folder: symlink (file, folder) and HARD link"
fixture B6; W="$T/vol/WEDNESDAY"; plant "$W/4_Credentials/master.txt" h1; plant "$W/4_Credentials/other.txt" h2; mkdir -p "$W/notes"
ln -s ../4_Credentials/master.txt "$W/notes/sym_to_secret.txt"; ln -s ../4_Credentials "$W/notes/sym_to_folder"; ln "$W/4_Credentials/other.txt" "$W/notes/innocent_name.txt"
rc=$(run "$(at 0 1 0)" r); say "run rc=$rc"; report "symlink target (file + folder link)" h1; report "HARD link named innocent_name.txt" h2
say "link count of the planted hard link at the source: $(stat -f %l "$W/notes/innocent_name.txt")"

say; say "### B7 another client's material by NAME, and its case variants (wednesday seat: other client = Datasec)"
fixture B7; W="$T/vol/WEDNESDAY"; X="$T/vol/CODING/Secuura"
plant "$W/x/Datasec/a.md" d1; plant "$W/x/datasec-plan.md" d2; plant "$W/x/DATASEC/a.md" d3; plant "$X/vendor/Datasec/a.md" d4
plant "$W/x/DataSec/a.md" d5; plant "$W/x/dataSec_notes.md" d6; plant "$W/x/DATAsec/a.md" d7; plant "$X/vendor/DataSec/a.md" d8; plant "$W/x/Data sec/a.md" d9; plant "$W/x/DS-NexusAI/a.md" d10
plant "$W/x/Tuesday/a.md" t1; plant "$W/x/TuesDay/a.md" t2; plant "$W/x/tUESDAY.md" t3; plant "$X/tuesday/a.md" t4
rc=$(run "$(at 0 1 0)" r); say "run rc=$rc"
for m in d1 d2 d3 d4; do report "Datasec, spellings on the list" "$m"; done; for m in d5 d6 d7 d8 d9 d10; do report "Datasec, other spellings" "$m"; done
for m in t1; do report "other seat, listed spelling, seat tree" "$m"; done; for m in t2 t3; do report "other seat, other spelling, seat tree" "$m"; done; report "other seat name inside a PROJECT set (documented as not applied)" t4

say; say "### B9 a set= SOURCE that is another client's folder, by routes the forbid check may miss"
fixture B9; mkdir -p "$T/vol/CODING/Datasec/proj" "$T/vol/CODING/Datasec-archive" "$T/vol/CODING/NexusAI"; plant "$T/vol/CODING/Datasec/proj/d.md" r1; plant "$T/vol/CODING/Datasec-archive/d.md" r2
ln -s Datasec "$T/vol/CODING/alias"
for src in "$T/vol/CODING/Datasec/proj" "$T/vol/CODING/Datasec/proj/" "$T/vol/CODING/DATASEC/proj" "$T/vol/CODING/Secuura/../Datasec/proj" "$T/vol/CODING/./Datasec/proj" "$T/vol/CODING/alias/proj" "$T/vol/CODING/alias" "$T/vol/CODING/Datasec-archive" " $T/vol/CODING/Datasec/proj "; do
  write_conf "set=General|Other|$src"; rc=$(run "$(at 0 1 0)" r_$RANDOM)
  printf 'rc=%s  r1 on NAS=%s  r2 on NAS=%s  source=[%s]\n' "$rc" "$(onnas 'MARK[r1]')" "$(onnas 'MARK[r2]')" "$(echo "$src" | sed "s|$T/||g")"
done

say; say "### B8 DAMAGED configuration: does it fail open?"
fixture B8; W="$T/vol/WEDNESDAY"; plant "$W/cache/huge/blob.bin" e1; plant "$W/keep/k.txt" e2; plant "$T/vol/CODING/Secuura/quarantine/q.txt" e3
write_conf "exclude_path=WEDNESDAY|cache/huge" "exclude_name_in=Secuura|quarantine"
cp "$T/lane/seats/wednesday.conf" "$T/good.conf"
rc=$(run "$(at 0 1 0)" g); say "(control) intact conf: rc=$rc, excluded blob on NAS=$(onnas 'MARK[e1]'), quarantine file on NAS=$(onnas 'MARK[e3]'), kept file on NAS=$(onnas 'MARK[e2]')"
tryconf() { # label ; conf already written
  local f2="B8_$RANDOM"; T2="$T"; fixture "$f2"; W="$T/vol/WEDNESDAY"; plant "$W/cache/huge/blob.bin" e1; plant "$W/keep/k.txt" e2; plant "$T/vol/CODING/Secuura/quarantine/q.txt" e3
  sed "s|$T2|$T|g" "$T2/try.conf" > "$T/lane/seats/wednesday.conf"; rc=$(run "$(at 0 1 0)" t)
  printf 'rc=%s good=%s  excluded-blob on NAS=%s  quarantine file on NAS=%s  kept file on NAS=%s  | %s\n' "$rc" "$(/usr/bin/grep -c 'GOOD:' "$T/out/t.txt")" "$(onnas 'MARK[e1]')" "$(onnas 'MARK[e3]')" "$(onnas 'MARK[e2]')" "$1"; T="$T2"; }
head -c $(( $(wc -c < "$T/good.conf") - 40 )) "$T/good.conf" > "$T/try.conf"; say "truncated tail: [$(tail -c 60 "$T/try.conf" | tr '\n' '~')]"; tryconf "TRUNCATED 40 bytes before the end (mid-line in the last exclude)"
/usr/bin/grep -v '^exclude' "$T/good.conf" > "$T/try.conf"; tryconf "every exclude line LOST (file cut after the set= lines)"
sed 's|cache/huge|cache/hug|' "$T/good.conf" > "$T/try.conf"; tryconf "exclude_path with a one-letter typo (names nothing that exists)"
sed 's|^exclude_path=WEDNESDAY|#exclude_path=WEDNESDAY|' "$T/good.conf" > "$T/try.conf"; tryconf "an exclude line commented out"
: > "$T/try.conf"; tryconf "EMPTY conf file"
/usr/bin/grep -v '^status=' "$T/good.conf" > "$T/try.conf"; tryconf "status= line missing"
{ cat "$T/good.conf"; echo "garbage line with no equals"; } > "$T/try.conf"; tryconf "a garbage line"
{ cat "$T/good.conf"; echo "exclude_name=*"; } > "$T/try.conf"; tryconf "exclude_name=* (excludes EVERYTHING)"
sed 's/$/\r/' "$T/good.conf" > "$T/try.conf"; tryconf "CRLF line endings"
{ printf '\xef\xbb\xbf'; cat "$T/good.conf"; } > "$T/try.conf"; tryconf "UTF-8 BOM at the start"
mv -n "$T/lane/seats/wednesday.conf" "$T/conf.aside"; rc=$(run "$(at 0 1 0)" nomiss); say "rc=$rc | conf file MISSING ($(/usr/bin/grep -c -i 'no seat configuration' "$T/out/nomiss.txt") refusal line)"

say; say "### B10 an EMPTY source set (e.g. the folder was emptied or is a bare mount point): is that a GOOD backup?"
fixture B10; mkdir -p "$T/held"; mv -n "$T/vol/WEDNESDAY/a.txt" "$T/vol/WEDNESDAY/sub" "$T/held/"; mv -n "$T/vol/CODING/Secuura/Blockchain" "$T/held/"
rc=$(run "$(at 0 1 0)" r); say "rc=$rc ; $(/usr/bin/grep -E 'GOOD:|totals' "$T/out/r.txt" | cut -c1-150 | tr '\n' ' ')"; say "state last_good.counts.src_files=$(state last_good.counts.src_files)"
say "--- and after a good 3-file backup, the source set becomes EMPTY the next night:"
fixture B10b; rc=$(run "$(at 0 1 0)" r1); mkdir -p "$T/held"; mv -n "$T/vol/WEDNESDAY/a.txt" "$T/vol/WEDNESDAY/sub" "$T/held/"; mv -n "$T/vol/CODING/Secuura/Blockchain" "$T/held/"
rc=$(run "$(at 1 1 0)" r2); say "rc=$rc ; state last_attempt=$(state last_attempt.status) src_files=$(state last_good.counts.src_files) ; $(/usr/bin/grep -c -i 'warn\|drop\|fewer' "$T/out/r2.txt") warning line(s) about the drop from 3 files to 0"

say; say "### B11 test-mode fence: nas_root that is a symlink leading OUTSIDE the test root must be refused"
fixture B11; mkdir -p "$S/fx/outside_$$/General" "$S/fx/outside_$$/Secuura"; mkdir -p "$T/held"; mv -n "$T/nas" "$T/held/nas"; ln -s "$S/fx/outside_$$" "$T/nas"
rc=$(run "$(at 0 1 0)" r); verdict "B11 rc (refused = 2)" 2 "$rc"; verdict "B11 nothing written outside" 0 "$(find "$S/fx/outside_$$" -type f | wc -l | tr -d ' ')"
