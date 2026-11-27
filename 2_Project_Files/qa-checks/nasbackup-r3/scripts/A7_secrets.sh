#!/bin/bash
# A7 — item 7: the folder-name rule and hard-link rule as hard guarantees; what a run leaves BY NAME about secret-shape exclusions.
. "$(dirname "$0")/lib3.sh"; date; uptime
M="QA3SECRETMARK"
say "== a. the two folder names in case, decoration and look-alike spellings (each holds one marked file)"
fixture s1; W="$T/vol/WEDNESDAY"
"$PY" - "$W" "$M" <<'PYEOF'
import os, sys
W, M = sys.argv[1], sys.argv[2]
names = ["4_Credentials", "4_CREDENTIALS", "4_credentials.", "4_Credentials ", " 4_Credentials", "4_Credentials-old", "x4_Credentials", "3_Access_Keys", "3_ACCESS_KEYS", "3_access_keys~",
         "4_Credentialſ",            # long s: casefolds to s
         "3_Access_Keys",            # Kelvin sign for K
         "４_Credentials",            # fullwidth digit 4
         "4_Cre​dentials",           # zero-width space inside
         "4_Credentıals",            # dotless i
         "4_Сredentials",            # Cyrillic Es for C
         "4-Credentials", "4 Credentials", "4_Credentialś", "Credentials", "4_Creds"]
made = 0
for i, n in enumerate(names):
    d = os.path.join(W, "h%02d" % i, n)
    try:
        os.makedirs(d); open(os.path.join(d, "inside.txt"), "w").write("%s %02d %r\n" % (M, i, n)); made += 1
    except OSError as e:
        print("  could not create %r: %s" % (n, e))
print("  planted %d folders" % made)
PYEOF
rc=$(run "$(at 0 1 0)" r); say "  rc=$rc GOOD=$(good r)"
say "  marked files that reached the fake NAS (the folder name each sat in):"
/usr/bin/grep -r -h -F "$M" "$T/nas" 2>&1 | sort | sed 's/^/     /'
say "  count on the NAS: $(/usr/bin/grep -r -l -F "$M" "$T/nas" 2>&1 | wc -l | tr -d ' ') of 21 ; credentials-folder-name count the run printed: $(line r 'excluded as secret-shaped' 1 200 | sed 's/.*only): //')"
say "== b. hard links: into a secrets folder; a file whose link count rises between plan and copy; a symlink into a secrets folder"
fixture s2; W="$T/vol/WEDNESDAY"; mkdir -p "$W/4_Credentials" "$W/files"; echo "$M token" > "$W/4_Credentials/token.txt"; ln "$W/4_Credentials/token.txt" "$W/files/innocent.txt"; ln -s ../4_Credentials/token.txt "$W/files/sym.txt"; ln -s ../4_Credentials "$W/files/symdir"
echo "plain v1" > "$W/files/later.txt"
CONF_RSYNC="$(mk_stub swap 'if [ "$N" = 1 ]; then mv "$V/files/later.txt" "$STUBDIR/taken/"; ln "$V/4_Credentials/token.txt" "$V/files/later.txt"; fi; exec "$REAL" "$@"')"; std_conf
rc=$(run "$(at 0 1 0)" r); say "  rc=$rc GOOD=$(good r); marked copies on the NAS: $(/usr/bin/grep -r -l -F "$M" "$T/nas" 2>&1 | sed "s|$T/nas/General/Wednesday/nightly-backup/||" | tr '\n' ' ')"
say "    (files/later.txt was an ordinary planned file, replaced by a hard link to the secret AFTER the plan)"
say "== c. a planned folder swapped for the secrets folder between plan and copy (same file name inside)"
fixture s3; W="$T/vol/WEDNESDAY"; mkdir -p "$W/4_Credentials" "$W/conf"; echo "$M real secret" > "$W/4_Credentials/settings.json"; echo "ordinary settings" > "$W/conf/settings.json"
CONF_RSYNC="$(mk_stub swapdir 'if [ "$N" = 1 ]; then mv "$V/conf" "$STUBDIR/taken/conf"; mv "$V/4_Credentials" "$V/conf"; fi; exec "$REAL" "$@"')"; std_conf
rc=$(run "$(at 0 1 0)" r); say "  rc=$rc GOOD=$(good r); marked copies on the NAS: $(/usr/bin/grep -r -l -F "$M" "$T/nas" 2>&1 | sed "s|$T/nas/General/Wednesday/nightly-backup/||" | tr '\n' ' ') ; a folder NAMED 4_Credentials on the NAS: $(find "$T/nas" -iname '*4_credentials*' | wc -l | tr -d ' ')"
say "== d. what a real run leaves BY NAME about what the secret-shape rule left out (ANSWER-5 item 1's condition)"
fixture s4; W="$T/vol/WEDNESDAY"; mkdir -p "$W/src" "$W/certs" "$W/ev"; echo "export const x=1" > "$W/src/secrets.ts"; echo "PUBLIC CERT" > "$W/certs/root-ca.crt"; echo "{}" > "$W/ev/post_api_credentials_ok.json"; echo "A=1" > "$W/.env.example"; echo ok > "$W/src/main.ts"
rc=$(run "$(at 0 1 0)" r); say "  rc=$rc GOOD=$(good r); the run's line: $(line r 'excluded as secret-shaped' 1 200)"
for n in secrets.ts root-ca.crt post_api_credentials_ok.json .env.example; do
  say "    '$n' named in: run output $(/usr/bin/grep -c -F "$n" "$T/o/r.txt") | lane logs $(/usr/bin/grep -r -l -F "$n" "$T/lane/logs" 2>&1 | wc -l | tr -d ' ') | lane manifests $(/usr/bin/grep -r -l -F "$n" "$T/lane/manifests" 2>&1 | wc -l | tr -d ' ') | NAS manifests $(/usr/bin/grep -r -l -F "$n" "$T/nas/General/Wednesday/nightly-backup/manifests" 2>&1 | wc -l | tr -d ' ')"; done
say "    CONTROL 'main.ts' (travels) named in lane logs: $(/usr/bin/grep -r -l -a -F "main.ts" "$T/lane/logs" 2>&1 | wc -l | tr -d ' ') ; a hard-link skip IS named in manifests (fixture s2): $(/usr/bin/grep -r -l -F 'innocent.txt' "$FXBASE/s2/lane/manifests" 2>&1 | wc -l | tr -d ' ')"
say "    what the manifest holds for the secret category: $("$PY" -c 'import json,glob,sys
m=json.load(open(sorted(glob.glob(sys.argv[1]+"/lane/manifests/wednesday/*_run_manifest.json"))[-1]))
print([e for e in m["sets"][0]["excluded"] if e["category"]=="secret"], m["secret_shape_counts"])' "$T")"
date; uptime
