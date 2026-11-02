#!/bin/bash
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate116-ks1413-pr1934; R=$D/repo
for f in $R/Start_Up/start-secuura.sh $R/Blockchain/Dev/scripts/start-local.sh; do
echo "=== $f"
/usr/bin/grep -niE '://[^ "]*:[^ "@]*@|\$\{?[A-Z_]*(PASS|PASSWORD|SECRET|TOKEN|PRIVATE|PW)[A-Z_]*\}?' "$f" | /usr/bin/grep -niE 'echo|printf|success|warn|fail|info|log' | head -30
echo "--- positive control (count of echo lines in file)"; /usr/bin/grep -ciE '^\s*echo' "$f"
echo "--- set -x"; /usr/bin/grep -niE 'set -[a-z]*x|xtrace' "$f"
done
echo "--- 660-680 start-secuura"; sed -n 660,680p $R/Start_Up/start-secuura.sh
echo "--- start-local 30-100"; sed -n 30,100p $R/Blockchain/Dev/scripts/start-local.sh
