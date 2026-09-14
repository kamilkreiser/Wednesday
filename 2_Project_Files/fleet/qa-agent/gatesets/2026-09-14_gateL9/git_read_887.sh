#!/bin/bash
set -u
G=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL9
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
C=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL9/model/clone
H887=3aee3deed2e3ac557f0a52c0797c2a4a8df25f69
date '+%Y-%m-%d %H:%M:%S %Z'
git -C "$R" ls-remote origin refs/heads/develop refs/pull/887/head refs/heads/feature/ks-961-workspace-suites-advisory-on-pr
for s in $H887 de376a9f1 cb7a3e3be 6899de33d bb0502c80 b6884888d; do printf '%s ' "$s"; git -C "$R" cat-file -t "$s" 2>&1; done
echo "== log (develop..head)"; git -C "$R" log --format='%H parents=%P tree=%T %aI | %s' 8861e6216..$H887
echo "== merge-base + rev-list"; git -C "$R" merge-base $H887 8861e6216; git -C "$R" rev-list --left-right --count 8861e6216...$H887; git -C "$R" merge-base --is-ancestor 8861e6216 $H887; echo "develop is-ancestor rc=$?"
echo "== delta vs develop (numstat/name-status)"; git -C "$R" diff --numstat 8861e6216 $H887; git -C "$R" diff --shortstat 8861e6216 $H887
echo "== delta since cb7a3e3be restricted to the PR's two files + whole"; git -C "$R" diff --numstat cb7a3e3be $H887 -- .github/workflows/pr-platform-suites.yml Blockchain/Dev/docs/DEV-PROCESS.md; git -C "$R" diff --shortstat cb7a3e3be $H887
echo "== the doc commit alone (3aee3deed vs de376a9f1)"; git -C "$R" diff --numstat de376a9f1 $H887; git -C "$R" diff --name-status de376a9f1 $H887
echo "== the merge commit vs develop: the PR's original hunks only?"; git -C "$R" diff --numstat 8861e6216 de376a9f1
echo "== blobs"; for p in .github/workflows/pr-platform-suites.yml Blockchain/Dev/docs/DEV-PROCESS.md Blockchain/Dev/package-lock.json Blockchain/Dev/scripts/audit/audit-baseline.json; do for s in b6884888d cb7a3e3be 8861e6216 de376a9f1 $H887; do printf '%-48s %-10s ' "$p" "${s:0:9}"; git -C "$R" ls-tree "$s" -- "$p" | awk '{print $3}'; done; done
echo "== the PR's three-dot hunk on pr-platform-suites.yml: byte-for-byte the reviewed one? (diff of the two diffs)"
git -C "$R" diff b6884888d cb7a3e3be -- .github/workflows/pr-platform-suites.yml > "$G/model/diff_887_wf_reviewed.patch"; git -C "$R" diff 8861e6216 $H887 -- .github/workflows/pr-platform-suites.yml > "$G/model/diff_887_wf_head.patch"; wc -l "$G/model/diff_887_wf_reviewed.patch" "$G/model/diff_887_wf_head.patch"
diff <(/usr/bin/grep '^[+-][^+-]' "$G/model/diff_887_wf_reviewed.patch") <(/usr/bin/grep '^[+-][^+-]' "$G/model/diff_887_wf_head.patch") && echo "the +/- lines of the workflow hunk are IDENTICAL reviewed vs head"
echo "== develop's own two hunks on the workflow since b6884888d"; git -C "$R" diff --numstat b6884888d 8861e6216 -- .github/workflows/pr-platform-suites.yml; git -C "$R" diff -U0 b6884888d 8861e6216 -- .github/workflows/pr-platform-suites.yml | /usr/bin/grep '^@@'
echo "== the head's workflow vs cb7a3e3be's = exactly develop's two hunks?"; git -C "$R" diff -U0 cb7a3e3be $H887 -- .github/workflows/pr-platform-suites.yml | /usr/bin/grep '^@@'
diff <(git -C "$R" diff b6884888d 8861e6216 -- .github/workflows/pr-platform-suites.yml | /usr/bin/grep '^[+-][^+-]') <(git -C "$R" diff cb7a3e3be $H887 -- .github/workflows/pr-platform-suites.yml | /usr/bin/grep '^[+-][^+-]') && echo "head-vs-reviewed workflow delta == develop's own delta (the merge brought it; no seat line)"
echo "== the doc commit's hunks"; git -C "$R" diff -U0 de376a9f1 $H887 -- Blockchain/Dev/docs/DEV-PROCESS.md | /usr/bin/grep '^@@'
git -C "$R" diff de376a9f1 $H887 > "$G/model/diff_887_doc.patch"
git -C "$R" show "${H887}:.github/workflows/pr-platform-suites.yml" > "$G/model/pr-platform-suites.yml.3aee3deed"
git -C "$R" show "cb7a3e3be:.github/workflows/pr-platform-suites.yml" > "$G/model/pr-platform-suites.yml.cb7a3e3be"
git -C "$R" show "8861e6216:.github/workflows/pr-platform-suites.yml" > "$G/model/pr-platform-suites.yml.8861e6216"
git -C "$R" show "${H887}:Blockchain/Dev/docs/DEV-PROCESS.md" > "$G/model/DEV-PROCESS.md.3aee3deed"
git -C "$R" show "de376a9f1:Blockchain/Dev/docs/DEV-PROCESS.md" > "$G/model/DEV-PROCESS.md.de376a9f1"
git -C "$R" show "cb7a3e3be:Blockchain/Dev/docs/DEV-PROCESS.md" > "$G/model/DEV-PROCESS.md.cb7a3e3be"
echo "== commit messages"; for s in $H887 de376a9f1; do printf '%s: ' "${s:0:9}"; git -C "$R" log -1 --format=%B $s | python3 -c "
import sys,re; m=sys.stdin.read(); print('chars',len(m),'KS',sorted(set(re.findall(r'KS-\d+',m))),'PRrefs',sorted(set(re.findall(r'#\d{3,4}',m))),'at',m.count('@'),'| subj:',m.splitlines()[0][:120])"; done
echo "== merge-tree re-derivation (in the drafter's clone): cb7a3e3be x develop clean?"; T="$(git -C "$C" merge-tree --write-tree cb7a3e3be 8861e6216 2>&1)"; echo "rc=$? $T" | head -3; printf 'de376a9f1 tree: '; git -C "$C" rev-parse "de376a9f1^{tree}"
echo "== rollup platform binaries in the root lockfile at head (the new finding's mechanism)"; git -C "$C" grep -c -F 'rollup-linux-x64-gnu' $H887 -- Blockchain/Dev/package-lock.json; git -C "$C" grep -o -E '"node_modules/@rollup/rollup-[a-z0-9-]+"' $H887 -- Blockchain/Dev/package-lock.json | sort -u | head
echo "== the workspace-suites job in the head workflow (names, continue-on-error, steps)"; python3 - "$G/model/pr-platform-suites.yml.3aee3deed" "$G/model/pr-platform-suites.yml.cb7a3e3be" "$G/model/pr-platform-suites.yml.8861e6216" <<'PY'
import sys,yaml
for p in sys.argv[1:]:
    d=yaml.safe_load(open(p)); jobs=d['jobs']
    print(p.split('/')[-1], 'jobs', len(jobs), sorted(jobs))
    j=jobs.get('workspace-suites')
    if j: print('   workspace-suites: name=%r continue-on-error=%r steps=%d %s' % (j.get('name'), j.get('continue-on-error'), len(j['steps']), [s.get('name','')[:40] for s in j['steps']]))
PY
date '+%H:%M:%S %Z'
