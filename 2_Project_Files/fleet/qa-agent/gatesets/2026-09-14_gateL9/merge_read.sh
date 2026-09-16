#!/bin/bash
# merge_read.sh — merge-tree simulations in the drafter's OWN --shared clone (write verbs only here; the Secuura checkout is read-only).
set -u
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL9
C=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL9/model/clone
H940=1aa708be9fcf7a23575398546d84848c967e81c5; H941=d105e07a81c8549b7f47c0542e9594204ce6f599; H942=53b9c3cc1a89f513620516c580a5de5bd60c64de; DEV=8861e62161466c40f08d2b10a30edeb203123993; BASE=a1e49d15152102acec7c97d96918211227c7fe1e
date '+%Y-%m-%d %H:%M:%S %Z'
for s in $H940 $H941 $H942 $DEV $BASE; do printf '%s ' "${s:0:9}"; git -C "$C" cat-file -t "$s"; done
echo "== merge-tree develop x #940"; T1="$(git -C "$C" merge-tree --write-tree $DEV $H940)"; echo "rc=$? tree=$T1"; git -C "$C" ls-tree "$T1" -- .github/workflows/security-scan.yml
echo "== merge-tree develop x #941"; T2="$(git -C "$C" merge-tree --write-tree $DEV $H941)"; echo "rc=$? tree=$T2"; git -C "$C" ls-tree "$T2" -- .github/workflows/security-scan.yml Blockchain/Dev/.security/exceptions.yml
echo "== merge-tree #940 x #941 (merge-base a1e49d151; the post-#940 shape of #941's file)"; T3="$(git -C "$C" merge-tree --write-tree $H940 $H941 2>&1)"; echo "rc=$? tree=$T3"
T3a="${T3%%$'\n'*}"; git -C "$C" ls-tree "$T3a" -- .github/workflows/security-scan.yml
git -C "$C" show "$T3a:.github/workflows/security-scan.yml" > "$G/model/security-scan.yml.940+941"; echo "show rc=$?"; wc -l "$G/model/security-scan.yml.940+941"
/usr/bin/grep -in 'shell: bash' "$G/model/security-scan.yml.940+941"; /usr/bin/grep -in 'rc=\$?' "$G/model/security-scan.yml.940+941"
echo "-- diff (develop x #940 x #941 merged file) vs #941's head file = exactly #940's hunks?"; git -C "$C" diff --stat $H941 "$T3a" -- .github/workflows/security-scan.yml; git -C "$C" diff $H941 "$T3a" -- .github/workflows/security-scan.yml | /usr/bin/grep -c '^[+-][^+-]'
echo "-- and vs #940's head file = exactly #941's hunks?"; git -C "$C" diff --stat $H940 "$T3a" -- .github/workflows/security-scan.yml
echo "-- the merged tree's other files = #941's (only the one shared file differs from #941's tree)"; git -C "$C" diff --stat $H941 "$T3a" | tail -3
echo "== merge-tree develop x #942 (develop is an ancestor -> tree == head tree)"; T4="$(git -C "$C" merge-tree --write-tree $DEV $H942)"; echo "rc=$? tree=$T4"; git -C "$C" rev-parse "${H942}^{tree}"
echo "== ancestry"; git -C "$C" merge-base --is-ancestor $DEV $H942; echo "develop is-ancestor of #942 head rc=$?"; git -C "$C" merge-base --is-ancestor $DEV $H940; echo "develop is-ancestor of #940 head rc=$? (1 = no, expected)"; git -C "$C" merge-base --is-ancestor $DEV $H941; echo "develop is-ancestor of #941 head rc=$? (1 = no, expected)"
echo "== #942: the original commit vs base, and the merge commit vs each parent"
git -C "$C" diff --numstat $BASE c1676269d
echo "-- merge commit vs parent1 (c1676269d): develop's 109 commits + the two resolutions"; git -C "$C" diff --shortstat c1676269d $H942
echo "-- merge commit vs parent2 (develop): the PR's delta on develop"; git -C "$C" diff --numstat $DEV $H942
echo "-- conflict re-derivation: merge-tree c1676269d x develop (expected: CONFLICT in the two files)"; T5="$(git -C "$C" merge-tree --write-tree c1676269d $DEV 2>&1)"; echo "rc=$?"; echo "$T5" | /usr/bin/grep -i 'conflict\|^[0-9a-f]\{40\}$' | head -10
echo "-- the resolution, re-derived: the merged suite's :66 line"; sed -n '66p' "$G/model/manifest_quarantine.test.sh.53b9c3cc1"
echo "-- live 2>&1 outside comments in the merged suite (positive control: the total count incl. comments)"; /usr/bin/grep -c '2>&1' "$G/model/manifest_quarantine.test.sh.53b9c3cc1"; /usr/bin/grep -v '^\s*#' "$G/model/manifest_quarantine.test.sh.53b9c3cc1" | /usr/bin/grep -c '2>&1'
echo "-- BACKLOG.md: both blocks whole?"; /usr/bin/grep -n 'quarantine_call_sites.test.sh. uses the same\|smoke\|KS-731' "$G/model/BACKLOG.md.53b9c3cc1" | head; /usr/bin/grep -c '^- \[ \]' "$G/model/BACKLOG.md.8861e6216" "$G/model/BACKLOG.md.53b9c3cc1"
echo "-- develop's BACKLOG lines all present in the merged copy (every line of develop's file is a line of the head's file, in order)?"; python3 - "$G/model/BACKLOG.md.8861e6216" "$G/model/BACKLOG.md.53b9c3cc1" <<'PY'
import sys
a=open(sys.argv[1],encoding='utf-8').read().splitlines(); b=open(sys.argv[2],encoding='utf-8').read().splitlines()
i=0
for line in a:
    while i<len(b) and b[i]!=line: i+=1
    if i>=len(b): print("MISSING develop line:", line[:80]); sys.exit(1)
    i+=1
print("every develop line present in order: yes; head has", len(b)-len(a), "extra lines")
PY
echo "-- bash -n the merged suite (and develop's, control)"; /bin/bash -n "$G/model/manifest_quarantine.test.sh.53b9c3cc1"; echo "rc=$?"; /bin/bash -n "$G/model/manifest_quarantine.test.sh.8861e6216"; echo "rc=$?"
echo "== the merge commit's message"; git -C "$C" log -1 --format=%B $H942
echo "== #940/#941 commit messages: ids"; for s in $H940 $H941 c1676269d; do printf '%s: ' "${s:0:9}"; git -C "$C" log -1 --format=%B $s | python3 -c "
import sys,re; m=sys.stdin.read(); print('chars',len(m),'KS',sorted(set(re.findall(r'KS-\d+',m))),'PRrefs',sorted(set(re.findall(r'#\d{3,4}',m))),'at',m.count('@'))"; done
date '+%H:%M:%S %Z'
