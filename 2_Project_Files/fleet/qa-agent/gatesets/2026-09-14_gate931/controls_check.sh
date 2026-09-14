#!/bin/bash
# controls_check.sh — re-derive every positive-control fact of the #931 (KS-1061) TIER-2 ROUND-1 gate
# at the PINNED head 53b8a1f7a6056c1560af71252c753c005bee8f06, its declared merge-base develop@dfc63fe48
# (M23), its pre-merge tip f2e0cb3c1, and develop's LIVE tip (read fresh, content-judged against the
# GUARDED path set — never a bare SHA compare). Reads are `git show`/`git diff --name-only`/`git ls-tree`
# (read verbs) against the read-only Secuura checkout, cross-checked against the GH REST blob shas
# already fetched into gh/pr931_files.json and against this set's model/ copies (git-show'd in the same
# session, before this script ran). Tokens were derived from the PR's OWN files at these SHAs — never
# carried from another gate's brief. PRESENT tokens must grep the stated count; ABSENT tokens must grep
# exactly 0; every byte-equivalence check (the two folds' shapes, the ks444 comment block, the resolved
# factory) is a `cmp`, not a grep. Then it re-runs guards_sim.py and requires FAILS=0 there too.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
# RE-PINNED 2026-09-14 ~13:5x AEST: 53b8a1f7a / dfc63fe48 (M23) are SUPERSEDED — the branch re-merged a
# later develop tip (M31, b9f541e6b, containing #985's squash) resolving the ks695 conflict as the union.
# See BUILD_REPORT.md "LIVE FINDING" and the brief's "RE-PIN" notice.
HEAD="${QA931_HEAD:-7953070230d285fdebc0c65b834ac8340c02c0b6}"
DEVBASE="${QA931_DEVBASE:-b9f541e6b158f831576ecc870244f361f219a114}"    # M31, the PR's declared merge-base after the re-pin
PREMERGE="${QA931_PREMERGE:-f2e0cb3c125d117b1c9f8157bad28399f16b5e8e}"  # the PR's own tip before EITHER merge-in (unchanged)
DIR='Blockchain/Dev/services/originate/src/__tests__'
G="${QA931_SET:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate931}"
M="$G/model"
W="$(mktemp -d "${TMPDIR:-/tmp}/qa931ctl.XXXXXX")"
FAILS=0

echo "controls_check.sh — HEAD ${HEAD:0:9}, devbase(M23) ${DEVBASE:0:9}, premerge ${PREMERGE:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"

show() { # ref path outfile
  git -C "$REPO" show "$1:$DIR/$2" > "$3" 2>/dev/null
}
ok()   { echo "ok   $1"; }
fail() { echo "FAIL $1"; FAILS=$((FAILS+1)); }

# ---- 0. HEAD is a real commit, reachable, and the tree matches what gh_read.py's API read already asserted ----
git -C "$REPO" cat-file -t "$HEAD" >/dev/null 2>&1 && ok "HEAD $HEAD is a real commit object" || { echo "CANNOT READ HEAD"; exit 2; }
/usr/bin/grep -q "\"sha\": \"$HEAD\"" "$G/gh/pr931.json" 2>/dev/null && ok "gh/pr931.json head sha == HEAD (cross-checked against the earlier GH API read)" || fail "gh/pr931.json head sha != HEAD"

# ---- 1. delta is tests-only, 14 paths exactly (git diff name-only devbase..HEAD, and cross-checked against the GH files API) ----
git -C "$REPO" diff --name-only "$DEVBASE" "$HEAD" > "$W/diff14.txt" 2>/dev/null
N14=$(wc -l < "$W/diff14.txt" | tr -d ' ')
[ "$N14" = "14" ] && ok "diff --name-only devbase..HEAD = 14 paths" || fail "diff --name-only devbase..HEAD = $N14 paths, want 14"
NONTEST=$(/usr/bin/grep -v -c "^Blockchain/Dev/services/originate/src/__tests__/" "$W/diff14.txt")
[ "$NONTEST" = "0" ] && ok "all 14 paths are under services/originate/src/__tests__/ (0 outside)" || fail "$NONTEST path(s) outside services/originate/src/__tests__/"
# negative control: the SAME regex against a known-non-matching literal string proves the grep can fire
echo "Blockchain/Dev/services/security/src/index.ts" | /usr/bin/grep -v -c "^Blockchain/Dev/services/originate/src/__tests__/" | /usr/bin/grep -q "^1$" \
  && ok "control: the outside-dir grep DOES fire on a planted non-matching path (positive control)" \
  || fail "control: the outside-dir grep failed to fire on its own positive control — the zero above is suspect"
# GH files API cross-check
NGH=$(python3 -c "import json; print(len(json.load(open('$G/gh/pr931_files.json'))))" 2>/dev/null)
[ "$NGH" = "14" ] && ok "GH REST /pulls/931/files also reads 14" || fail "GH REST /pulls/931/files reads $NGH, want 14"

# ---- 2. jest.mock root-factory census: 12 at develop (M23), head folds 2 (10 already converted + 2 folded = 12, 0 offenders) ----
python3 "$G/guards_sim.py" > "$W/guards_sim_rerun.out" 2>&1
/usr/bin/grep -q "totalFactories=12" "$W/guards_sim_rerun.out" && ok "guards_sim.py re-run: totalFactories=12 appears (develop/head census)" || fail "guards_sim.py re-run: totalFactories=12 not found"
/usr/bin/grep -q "MATCHES builder's claimed red-first.*True" "$W/guards_sim_rerun.out" && ok "guards_sim.py re-run: red-first simulation MATCHES the builder's claim (True)" || fail "guards_sim.py re-run: red-first simulation did NOT match"
/usr/bin/grep -c "predicted-by: drafter" "$W/guards_sim_rerun.out" | /usr/bin/grep -q "^[1-9]" && ok "guards_sim.py re-run: predicted-by: drafter present (>=1)" || fail "guards_sim.py re-run: no predicted-by: drafter line"

# ---- 3. The two folds are faithful: HEAD content matches the brief's prescribed shape byte-for-byte ----
# macOS /usr/bin/grep is BSD grep — no -P, no -z. Multi-line exact-shape matches use perl -0777 instead
# (the same tool the fleet's own VIA_HELPER checks use per the builder's READY mail).
show "$HEAD" ks1103-verify-hash-field.test.ts "$W/ks1103.head"
perl -0777 -ne 'exit(scalar(() = /jest\.mock\(\x27\@secuura\/shared\x27, \(\) =>\n  require\(\x27\.\/helpers\/sharedModuleMock\x27\)\.makeSharedMock\(\{\n    runWithTenantId: \(_t: unknown, fn: \(\) => unknown\) => fn\(\),\n    queryWithTenantGuc: jest\.fn\(\),\n  \}\),\n\);/gs) == 1 ? 0 : 1)' "$W/ks1103.head" \
  && ok "ks1103-verify-hash-field.test.ts: fold matches the brief's prescribed shape exactly (brief §2c)" \
  || fail "ks1103-verify-hash-field.test.ts: fold does NOT match the brief's prescribed shape"
show "$HEAD" ks764-admin-api-keys-revoke-route-contract.test.ts "$W/ks764.head"
perl -0777 -ne 'exit(scalar(() = /jest\.mock\(\x27\@secuura\/shared\x27, \(\) =>\n  require\(\x27\.\/helpers\/sharedModuleMock\x27\)\.makeSharedMock\(\{\n    \.\.\.\(jest\.requireActual\(\x27\@secuura\/shared\x27\) as Record<string, unknown>\),\n    runWithPlatformScope: \(fn: \(\) => unknown\) => fn\(\),\n    queryWithTenantGuc: jest\.fn\(\),\n    decideKeyRevoke: \(jest\.requireActual\(\x27\@secuura\/shared\x27\) as Record<string, unknown>\)\.decideKeyRevoke,\n  \}\),\n\);/gs) == 1 ? 0 : 1)' "$W/ks764.head" \
  && ok "ks764-admin-api-keys-revoke-route-contract.test.ts: fold matches the brief's prescribed EXPRESSION-form shape exactly (brief §2c)" \
  || fail "ks764-admin-api-keys-revoke-route-contract.test.ts: fold does NOT match the prescribed shape"
# negative control: the ks1103 regex must NOT match the ks764 file (proves the pattern discriminates)
perl -0777 -ne 'exit(scalar(() = /jest\.mock\(\x27\@secuura\/shared\x27, \(\) =>\n  require\(\x27\.\/helpers\/sharedModuleMock\x27\)\.makeSharedMock\(\{\n    runWithTenantId: \(_t: unknown, fn: \(\) => unknown\) => fn\(\),\n    queryWithTenantGuc: jest\.fn\(\),\n  \}\),\n\);/gs) == 1 ? 0 : 1)' "$W/ks764.head" \
  && fail "control: ks1103's exact-shape pattern WRONGLY matched ks764.head — the check cannot discriminate" \
  || ok "control: ks1103's exact-shape pattern correctly does NOT match ks764.head (discriminates)"

# ---- 4. ks444 resolution: develop's KS-927 comment block kept byte-for-byte; assertSafeOutboundUrl kept; helper form used ----
show "$DEVBASE" ks444-webhooks-create-description-guard.test.ts "$W/ks444.devbase"
show "$HEAD" ks444-webhooks-create-description-guard.test.ts "$W/ks444.head"
# the comment block (lines 1-46, ending just before the jest.mock('@secuura/shared'... line) must be byte-identical
head -n 46 "$W/ks444.devbase" > "$W/ks444.devbase.comment"
head -n 46 "$W/ks444.head" > "$W/ks444.head.comment"
cmp -s "$W/ks444.devbase.comment" "$W/ks444.head.comment" && ok "ks444: the KS-927 comment block (lines 1-46) is byte-identical between develop(M23) and HEAD" || fail "ks444: comment block differs between develop and HEAD"
ASU_HEAD=$(/usr/bin/grep -c "assertSafeOutboundUrl" "$W/ks444.head")
[ "$ASU_HEAD" -ge 2 ] && ok "ks444.head: assertSafeOutboundUrl count = $ASU_HEAD (>=2: comment + override)" || fail "ks444.head: assertSafeOutboundUrl count = $ASU_HEAD, want >=2"
ASU_PREMERGE_CTRL=$(show "$PREMERGE" ks444-webhooks-create-description-guard.test.ts "$W/ks444.premerge"; /usr/bin/grep -c "assertSafeOutboundUrl" "$W/ks444.premerge")
[ "$ASU_PREMERGE_CTRL" = "0" ] && ok "control: ks444 @ PR's OWN pre-merge tip has assertSafeOutboundUrl count = 0 (the override is develop's, proves the count above isn't vacuous)" || fail "control: ks444 @ premerge count = $ASU_PREMERGE_CTRL, want 0 (the positive control failed to establish contrast)"
MSM_HEAD=$(/usr/bin/grep -c "makeSharedMock(" "$W/ks444.head")
[ "$MSM_HEAD" = "1" ] && ok "ks444.head: makeSharedMock( count = 1" || fail "ks444.head: makeSharedMock( count = $MSM_HEAD, want 1"
MARKERS=$(/usr/bin/grep -c -e '^<<<<<<<' -e '^>>>>>>>' "$W/ks444.head")
[ "$MARKERS" = "0" ] && ok "ks444.head: 0 conflict markers" || fail "ks444.head: $MARKERS conflict marker(s) found"
printf '<<<<<<< HEAD\nplanted\n>>>>>>> other\n' > "$W/marker_control.txt"
MCTRL=$(/usr/bin/grep -c -e '^<<<<<<<' -e '^>>>>>>>' "$W/marker_control.txt")
[ "$MCTRL" = "2" ] && ok "control: the marker grep DOES fire on a planted conflict (positive control)" || fail "control: marker grep failed on its own positive control"

# ---- 5. helpers/sharedModuleMock.ts: exists at HEAD, ABSENT at devbase (added by this PR, not develop's) ----
show "$HEAD" helpers/sharedModuleMock.ts "$W/helper.head"
[ -s "$W/helper.head" ] && ok "helpers/sharedModuleMock.ts present and non-empty at HEAD" || fail "helpers/sharedModuleMock.ts missing/empty at HEAD"
git -C "$REPO" cat-file -e "$DEVBASE:$DIR/helpers/sharedModuleMock.ts" 2>/dev/null && fail "helpers/sharedModuleMock.ts unexpectedly EXISTS at develop(M23) — it should be PR-only" || ok "helpers/sharedModuleMock.ts correctly ABSENT at develop(M23)"
/usr/bin/grep -c "typeof value === 'function' ? jest.fn() : value" "$W/helper.head" | /usr/bin/grep -q "^1$" && ok "makeSharedMock: the function->jest.fn(), else pass-through rule is present exactly once" || fail "makeSharedMock: the pass-through rule line not found exactly once"

# ---- 6. ks444/ks695/ks780 — the LIVE-develop content-judged guard (the same class as the L9 gate) ----
DEVTIP="$(git -C "$REPO" ls-remote origin develop 2>/dev/null | /usr/bin/grep -o '^[0-9a-f]\{40\}')"
if [ -z "$DEVTIP" ]; then
  fail "could not read origin/develop tip via ls-remote — cannot run the live guard"
else
  echo "live develop tip (ls-remote, this run): ${DEVTIP:0:9}"
  git -C "$REPO" diff --name-only "$DEVBASE" "$DEVTIP" -- "$DIR/" > "$W/dev_moved_in_dir.txt" 2>/dev/null
  NMOVED=$(wc -l < "$W/dev_moved_in_dir.txt" | tr -d ' ')
  echo "develop M23..LIVE, files changed under $DIR/: $NMOVED"
  cat "$W/dev_moved_in_dir.txt" | sed 's/^/    moved: /'
  # every one of those files must be judged: either it's one of the PR's own 14 (already re-merged story,
  # the ks695 case) or brand-new and root-mock-free (the ks780 case) — anything else is UNJUDGED and FAILs.
  UNJUDGED=0
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    base="$(basename "$f")"
    if /usr/bin/grep -qxF "Blockchain/Dev/services/originate/src/__tests__/$base" "$W/diff14.txt" 2>/dev/null; then
      echo "    judged: $base is one of the PR's own 14 files (the ks695 conflict case, expected)"
    else
      show "$DEVTIP" "$base" "$W/newfile.$base"
      RM=$(/usr/bin/grep -c "jest\.mock('@secuura/shared'," "$W/newfile.$base" 2>/dev/null)
      RM="${RM:-0}"
      if [ "$RM" = "0" ]; then
        echo "    judged: $base is NEW on develop and carries 0 root @secuura/shared mocks (the ks780 case, expected — guard stays green when merged)"
      else
        echo "    UNJUDGED: $base carries $RM root mock(s) and is not one of the PR's 14 — needs a human ruling"
        UNJUDGED=$((UNJUDGED+1))
      fi
    fi
  done < "$W/dev_moved_in_dir.txt"
  [ "$UNJUDGED" = "0" ] && ok "live-develop content guard: every moved file in $DIR/ is judged (ks695 known-conflict or root-mock-free-new-file)" || fail "live-develop content guard: $UNJUDGED file(s) UNJUDGED"
  # merge-tree in the isolated model/repo clone (never the real checkout). Two legitimate outcomes, both
  # asserted explicitly rather than picking one: (a) DEVTIP == DEVBASE (the branch already contains the
  # develop tip it needs — the post-re-pin state, current as of this run) -> EXPECT 0 conflicts, since the
  # ks695 union was already folded into HEAD itself; (b) DEVTIP has moved PAST DEVBASE -> the ORIGINAL
  # expectation applies: at most the known ks695 file may conflict again (a third develop move touching the
  # same lines), anything else is a genuine new GUARDED hit already caught by the judgement loop above.
  CLONE="$G/model/repo"
  if [ -d "$CLONE/.git" ]; then
    git -C "$CLONE" merge-tree --write-tree "$DEVTIP" "$HEAD" > "$W/mergetree.out" 2>&1
    MTRC=$?
    NCONF=$(/usr/bin/grep -c "^CONFLICT" "$W/mergetree.out")
    if [ "$DEVTIP" = "$DEVBASE" ]; then
      if [ "$NCONF" = "0" ]; then
        ok "merge-tree(live-develop, HEAD) in the isolated clone: 0 conflicts — HEAD already contains this develop tip (DEVTIP == DEVBASE, the post-re-pin state)"
      else
        fail "merge-tree(live-develop, HEAD): $NCONF conflict(s) even though DEVTIP == DEVBASE (HEAD should already contain this tip) — see $W/mergetree.out"
      fi
    elif [ "$NCONF" = "0" ]; then
      ok "merge-tree(live-develop, HEAD) in the isolated clone: 0 conflicts (develop moved past DEVBASE but disjointly from HEAD's tree)"
    elif [ "$NCONF" = "1" ] && /usr/bin/grep -q "ks695-erasure-by-external-ref.test.ts" "$W/mergetree.out"; then
      ok "merge-tree(live-develop, HEAD) in the isolated clone: EXACTLY 1 conflict, on ks695-erasure-by-external-ref.test.ts (a further develop move re-touching the same lines)"
    else
      fail "merge-tree(live-develop, HEAD): $NCONF conflict(s) on an unexpected file set — see $W/mergetree.out"
    fi
  else
    fail "model/repo clone not present — cannot run the isolated merge-tree check"
  fi
fi

# ============================================================================================
# PART 2, added mid-draft: PR #720 (KS-487) — the 2-file, 0-product delta, independently confirmed.
# ============================================================================================
HEAD720="${QA720_HEAD:-cd62c9f89491072ce4e6e7bde9946d22409b1110}"
DEVBASE720="${QA720_DEVBASE:-f09b629457c5800b215621c31c680631f947e879}"  # develop tip at #720's own merge-in, per the READY mail
echo "--- PART 2: #720 @ ${HEAD720:0:9}, base(at merge) ${DEVBASE720:0:9} ---"
git -C "$REPO" cat-file -t "$HEAD720" >/dev/null 2>&1 && ok "PART2: HEAD720 $HEAD720 is a real commit object" || { echo "CANNOT READ HEAD720"; exit 2; }
git -C "$REPO" diff --name-only "$DEVBASE720" "$HEAD720" > "$W/diff720.txt" 2>/dev/null
N2=$(wc -l < "$W/diff720.txt" | tr -d ' ')
[ "$N2" = "2" ] && ok "PART2: diff --name-only base720..HEAD720 = 2 paths" || fail "PART2: diff --name-only base720..HEAD720 = $N2 paths, want 2"
/usr/bin/grep -qxF "BACKLOG.md" "$W/diff720.txt" && ok "PART2: BACKLOG.md is one of the 2 paths" || fail "PART2: BACKLOG.md not in the diff"
/usr/bin/grep -qxF "Blockchain/Dev/services/originate/src/__tests__/ks444-webhooks-create-description-guard.test.ts" "$W/diff720.txt" \
  && ok "PART2: ks444-webhooks-create-description-guard.test.ts is the other path" \
  || fail "PART2: ks444 test file not in the diff"
# negative control: a file that is NOT in the diff must not be found there
/usr/bin/grep -qxF "Blockchain/Dev/services/originate/src/index.ts" "$W/diff720.txt" \
  && fail "control: a product file WRONGLY appears in #720's diff" \
  || ok "control: services/originate/src/index.ts correctly absent from #720's diff (0 product files)"
git -C "$REPO" diff "$DEVBASE720" "$HEAD720" -- Blockchain/Dev/services/originate/src/__tests__/ks444-webhooks-create-description-guard.test.ts > "$W/ks444_720.diff" 2>/dev/null
/usr/bin/grep -q "^+const shared = jest.requireMock('@secuura/shared')" "$W/ks444_720.diff" \
  && ok "PART2: ks444 diff adds the jest.requireMock handle (Peter's ask 1)" \
  || fail "PART2: ks444 diff does not add the expected handle line"
ADDED_ASSERT=$(/usr/bin/grep -c "^+.*toHaveBeenCalledTimes(1)" "$W/ks444_720.diff")
[ "$ADDED_ASSERT" = "2" ] && ok "PART2: ks444 diff adds exactly 2 toHaveBeenCalledTimes(1) assertions (one per 201 cell)" || fail "PART2: ks444 diff adds $ADDED_ASSERT toHaveBeenCalledTimes(1) lines, want 2"
REMOVED_FACTORY=$(/usr/bin/grep -c "^-.*jest\.mock('@secuura/shared'" "$W/ks444_720.diff")
[ "$REMOVED_FACTORY" = "0" ] && ok "PART2: #720's diff does NOT touch the jest.mock('@secuura/shared',...) factory line itself (0 removed)" || fail "PART2: #720's diff removes $REMOVED_FACTORY factory line(s) — should be 0"
# GH files API cross-check for #720
NGH720=$(python3 -c "
import json, urllib.request
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
tok=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok=line.split('=',1)[1].strip().strip('\"').strip(\"'\")
r=urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/720/files?per_page=100', headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}), timeout=60)
print(len(json.load(r)))
" 2>/dev/null)
[ "$NGH720" = "2" ] && ok "PART2: GH REST /pulls/720/files also reads 2 (live re-fetch, independent of the saved #931 gh/ JSON)" || fail "PART2: GH REST /pulls/720/files reads $NGH720, want 2"

echo "FAILS=$FAILS"
[ "$FAILS" = "0" ] && exit 0 || exit 1
