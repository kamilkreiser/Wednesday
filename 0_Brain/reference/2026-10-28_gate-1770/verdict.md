# QA gate verdict: Secuura/Blockchain PR #1770 (KS-1774), tier 2 (qs 6.16.0 -> 6.16.1, lockfile-only)

Run: Wed 28 Oct 2026 05:25:26 AEDT (gate seat, findings only; nothing pushed, commented or mailed)
Pins read by git ls-remote at start: head e3702275d60be81f83534a199f21f5d18cf80e04 (matches), develop c18552d94de23b4da365ce02e02be5d06793bbcb (matches). Gated exactly these.
Clone: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-1770-1028/repo ; scratch: .../gate-1770-1028/tmp

## VERDICT: GO

| # | Result | Evidence | Control |
|---|---|---|---|
| G1 Topology | PASS | head's single parent = c18552d9 (develop pin). 27 changed paths, all end package-lock.json, 0 package.json. Blockchain/Dev/package-lock.json and services/mcp-server/package-lock.json not in the diff. | Repo has 46 tracked locks; the 19 not in the diff were listed: those two (qs 6.16.1 already) + 17 with no qs entry at all. Count 27 matches claim. |
| G2 Minimal diff (parsed) | PASS | python3 -I json-load of both sides of all 27: each differs in exactly 3 leaves, packages["node_modules/qs"].{version,resolved,integrity}; version 6.16.0 -> 6.16.1; resolved = https://registry.npmjs.org/qs/-/qs-6.16.1.tgz in all 27. 27/27 pass, 0 other leaves. Each lock has exactly one qs entry. | Planted description edit on a nested package plus lockfileVersion=99 in a scratch copy: differ reported both (5 leaves vs 3 real). It can fail. |
| G3 Integrity | PASS | sha512 of registry tarball qs-6.16.1.tgz = sha512-5Px6J7rfHBAGUhNQ3es4YzcOdBBw0SDcVtThJml4RdnKw4tKs2epA0kPZ+K8X+WiHktT93RHVcQ/3ym5aTCgtg== ; all 27 head locks carry that single string (set of size 1). | Hashed 6.16.0 tarball = sha512-h6fhOIaR...P1vA==; equals the integrity in all 27 BASE locks (27/27 single value). Method reproduces known-good. |
| G4 Ranges | PASS | 54 dependents of qs across the 27 head locks declare only 3 distinct ranges: ^6.11.0, ^6.12.3, ~6.16.0. npm's bundled semver (/opt/homebrew/lib/node_modules/npm/node_modules/semver) satisfies('6.16.1', each) = true for all 3. Sweep of all 46 head locks: every qs entry is 6.16.1 (29 locks), none vulnerable remain. | satisfies('6.16.0', same ranges) also true, so the check is not vacuous on the version side only; the sweep would have listed any <=6.16.0 entry. |
| G5 Advisory gate | PASS | Repo's own scripts/audit/audit-locks.mjs run with node directly (no npm install; semver resolved by symlinking npm's bundled copy into an untracked Blockchain/node_modules in my clone). Registry reachable. develop: rc 1, "FAIL - 1 advisory ... GHSA-6pq8-jhm2-2vcw qs pinned 6.16.0 in 27 lock(s)". head: rc 0, "44 standalone lockfiles ... OK - no standalone-lock advisories outside the triaged baseline"; GHSA-6pq8 absent. | The same script at develop failed on exactly this advisory in exactly 27 locks, so it detects the condition. Matches the author's "rc 1 at develop, rc 0 at head". |

## Findings
- MAJOR: none.
- MINOR: none.
- LOW: none.
- INFO: audit-locks.mjs excludes the workspace root lock (audit-gate covers it) and mobile/secuura-app (KS-769). Root lock is already qs 6.16.1 and mobile has no qs entry, so neither hides a vulnerable qs. I did not run audit-gate.mjs (workspace-root audit).
- INFO: the advisory is moderate DoS in qs.stringify arrayFormat comma. Whether the code reaches it was not assessed; the bump is the fix regardless.

## NOT TESTED
No stack start, no docker image build, no npm ci/install of any of the 27 locks, no unit/integration tests, no CI run read, no deploy. Whether npm ci succeeds against the bumped locks (tarball availability aside from the one fetched) was not exercised. audit-gate.mjs (root) not run. package.json byte-identity checked via name-only diff (0 package.json paths), not byte comparison.

## Instrument errors (mine)
1. The work dir already existed (I had created tmp/ in it first), so the prescribed git clone failed, and my first fetch ran inside the parent WEDNESDAY repo, writing refs/g/develop, refs/g/pr1770 and tag dev-2026-05-11 into it. Early G1/G2/G3 evidence came from that repo's object store (same SHAs). I removed those three refs (update-ref -d x2, tag -d) and verified refs/g is empty there; unreachable fetched objects remain in /Volumes/DevMASTER/WEDNESDAY/.git until gc. I then made a real clone in .../gate-1770-1028/repo, re-fetched the pins and re-ran G1 (file list identical, cmp same) and G4/G5 there.
2. ls-tree / git archive returned empty because the cwd-relative prefix was the subdirectory of the wrong repo; resolved by the proper clone.
3. Several Bash calls were refused by hooks (cd, rm -rf on variable path, write verbs with variable paths); no state change from those.
