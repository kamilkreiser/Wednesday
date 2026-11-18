GATE B1709: GO WITH FINDINGS @ a2af734 on main 8ae5db6

Gate tier G2 for B1707 (MPSCALC-413). Head a2af7340c0ac869c0fd766f739bae6e8513b3c47 = branch ref (gh api). Main read at the end: 8ae5db6e (unchanged; ahead 1 behind 0; open PRs 0). The sibling branch b1706 has not landed.

## Checks
1. Diff: one path .github/workflows/ci.yml, +4 -0, one commit, one parent, author and committer equal the repo address. Python: base text with the frozen replacement == head file byte for byte (control: a planted extra space is unequal). OLD occurs once at base. Job keys and names equal (Ruby YAML); web steps 9 -> 10; other jobs equal. grep audit = 3 lines, all added; npm = 10 lines. diff --check rc 0; added lines ASCII (0 non-ASCII), no Cf/Cc.
2. Authority: decision card client_project Datasec/MPS, ruled a, 'Add a production audit step: Passes today with 0; developer tools updated at the next routine round'. The step is exactly that and nothing more (no dependency file touched).
3. Merge: git merge-tree --write-tree base head clean, tree d229b1cb = head tree (head is a direct child of main).
4. Own clone at head, Node 26.13 (CI runs Node 24, not available here): npm ci OK; `npm audit --omit=dev --audit-level=high` rc 0 'found 0 vulnerabilities'. Control: full audit rc 1, '12 high severity vulnerabilities'. Plant: minimist 1.2.5 as production dependency -> rc 1, '1 critical severity vulnerability'; as dev dependency -> rc 0 (scratch /private/tmp/b1709-gate/plant, never staged).
5. CI text tests test_ci_workflow.py, test_sdk_pin.py, test_sdk_pin_routes.py: each rc 0 and prints OK at head.
6. Scans over added lines and commit message: ban list 0 (control _by_Kam_ fires), B-numbers 0, secrets/ids/hosts/URLs 0, Cf 0. CodeQL pre-scan rows: no RegExp, replace, innerHTML, child_process, os.chmod or sensitive-name writes in the added lines.
7. Builder claims (STATUS): production audit 0 true; full audit 12 high true; planted production fails true; planted dev passes true; YAML equalities true; three CI text tests OK true; no dependency file changed true.

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| 1 | Minor (known behaviour, product owner chose it) | The step reaches the npm registry at CI time. A newly published high or critical advisory on any of the 4 production dependencies turns the web check red on every PR with no code change. Level high means moderate-only advisories do not. | Accept. The step name already says 'blocks on high/critical'. The comment (lines 62-63) does not say the result can change with no code change; optional one-line addition, but the frozen words rule forbids a reword in this lane: record the behaviour in the PR body (done) and Jira rather than edit. |
| 2 | Minor | Node 24 (CI) was not measured; audit depends on lockfile and registry data, not the Node version. | The PR's own hosted web run is the arbiter: the step log must print 'found 0 vulnerabilities'. |
| 3 | Info | The step's check name is unchanged; the ruleset has an empty required-checks list, so no name is enforced either way. | None. |

## NOT RUN
- CodeQL query pack (the change is one workflow file; the actions pack was not run locally; hosted CodeQL 'Analyze (actions)' is the proof).
- dotnet, npm run lint, npm test, Playwright, python harness, package.sh (no code or test changed; hosted CI is the arbiter).
- Red-without-fix (no new or changed test).
- Hosted first run of the step on Node 24.
- git ls-remote over SSH (not needed; gh api refs read instead).
- Re-read main again before landing: do it, since the b1706 sibling may land first; the squash is head-pinned and ci.yml does not overlap it.
