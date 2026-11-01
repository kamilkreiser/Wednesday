#!/bin/bash
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator57
REPO=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate89-e25-1904-1906-1907/repo
g() { local mode="$1" pat="$2"; git -C "$REPO" grep $mode -E "$pat" origin/develop -- Blockchain/Dev/services | sed 's#^origin/develop:Blockchain/Dev/services/##' | grep -E '^[^:]+/src/' | grep -vE '__tests__|\.test\.|\.spec\.'; }
g -n "instanceof Error \? [a-zA-Z_.]+\.message : String\(" > $D/s_ternary.out
g -n "String\((err|error|e|saveErr|dbErr)\)" > $D/s_string.out
g -n "\b(err|error|e|saveErr|dbErr)\??\.(message|code|name|stack)\b" > $D/s_member.out
g -n "describeThrown|safeErrorMessage|describeError|readThrown" > $D/s_helper.out
for f in s_ternary s_string s_member s_helper; do echo "== $f $(wc -l < $D/$f.out)"; awk -F: '{print $1}' $D/$f.out | sort | uniq -c | sort -rn | head -45; done
