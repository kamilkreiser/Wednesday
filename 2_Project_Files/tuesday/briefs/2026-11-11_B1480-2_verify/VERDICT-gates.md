GATE B1480-2-gates: GO WITH FINDINGS @ ef0ff56 on main 0364b25

Branch `b1480/nexusai-s-viewer-write-gates`, head `ef0ff56e1fb7ab87a55617c0632c05a19e728c53`: two commits on round 1's `f913fef`, `f7639de` (the fix + new cells) and `ef0ff56` (counts only). STACKED ON `70709c61` (l1), which is NOT on main (`merge-base --is-ancestor 70709c6 0364b25` rc 1; control `3929b794` rc 0). Tickets RD-958 (16 routes), RD-793 (4 routes). Tier 1 (write-gate / permission surface). Round 4 verifier (fourth on this commission; rounds 2a, 2b and 3 died before a verdict). Round 3's files were re-checked and reused only where re-measured below. Own clone `fleet/state/s267/b1480-2r4/clone` (`--no-hardlinks` from the project repo, fetched from origin with the project deploy key as repo-local `core.sshCommand`, push URL `invalid://no-push-verifier`), worktrees under `.../b1480-2r4/wt/` (no dot component), read-only to origin.

BLUF: GO WITH FINDINGS (0 Blockers, 0 Majors, 5 Minors). Round 1's Blocker (a viewer writes the sustainability config by changing the letter case of the path) is closed: at the old head the bypass reproduces on 7 routed forms + 4 raw request lines and the viewer's write PERSISTS; on this head merged with current main 0 of 220 viewer forms and 0 raw lines pass, the stored value is unchanged, and the administrator controls prove every form reaches the handler. The shipped cells go red on exactly the 3 case rows without the fix (at the old head AND with the fix taken out of the merged tree) and green with it. A FRESH plain verify of this head merged with main 0364b25 reads `VERDICT: PASS - 5559/5559 tests passed across 337 suites`, EADDRINUSE 0, rd407-r2 green (17 cells). Lands only after l1, by merge commit, with the counts file regenerated on the merged tree (it conflicts with main by design).

## Red-first
### probe3 (round 3's instrument `probe3-test.js.txt`, copied byte-equal: `cmp` rc 0), re-run by round 4
One jest-lock acquisition `qa-b1480-2r4-red` (16:35:29-16:36:28 AEDT, after 3405 s in the FIFO behind the landing chain), plant -> run alone -> plant quarantined, porcelain 0 before and after in each tree, EADDRINUSE 0. Raw: `p4-old-g.probe.json`, `p4-mrg-g.probe.json`, `p4-mrg-c.probe.json` in this folder.

| Probe section | old head f913fef | main 0364b25 + ef0ff56 (merged, counts 5559/337) | main + ccb7aa4 |
|---|---|---|---|
| A: 20 gated routes x 11 routed forms, viewer, not `403 Admin access required` | **7**, all `POST /api/sustainability/config`: UPPER, Title, aLtErNaTe x2, last-segment upper, UPPER/, UPPER/?query -> 200 | **0 / 220** | **0 / 220** |
| D: raw request lines, viewer -> 200 | **4** (`CONFIG#frag`, three absolute-form targets) | 0 | 0 |
| F: stored sustainability region after the viewer's marked writes (before `AU-NSW`) | **`VIEWER-125`: the viewer's write persisted** | `AU-NSW` (unchanged) | `AU-NSW` |
| F control: administrator writes all 11 forms, then reads | `ADMIN-upper-slash-query` (read instrument fires) | same | same |
| F: real feedback item, 66 PATCH + 66 DELETE viewer forms incl. id aliases | 0 not 403; item unchanged | same | same |
| B: administrator on the 33 forms of the two router-level-gated routes | all routed (config 200, feedback handler 404) | same | same |
| C: 22 forms Express does not route, viewer and administrator | identical for both roles (404/400): not routed | same | same |
| E: method variants / override header on the config path | identical | same | same |
| G: round 1's 36 cases verbatim | 3 case rows 200 | those 3 -> 403; other 33 identical | same |

Instrument check (required before reuse of round 3's table): every section of round 4's old-head row equals round 3's `p3-old-g` (A, B, C, D, E, G: 0 differing keys), and round 4's merged rows equal round 3's `p3-mrg3-g` / `p3-mrg3-c` (0 differing keys). The instrument still fires (old head 7 + 4 + persisted write) and still reads closed at the new head. Old vs new on the same forms: only the 7 A rows, 4 D rows and 3 G rows changed; B, C, E identical (the fix changes nothing else observable).

### Shipped cells red without the fix (`__tests__/rd958-write-gate-path-variants.test.js`, same acquisition)
| Run | Test 1 (viewer, 80 forms) | Test 2 (admin control) | Test 3 (unrouted, 404) |
|---|---|---|---|
| planted at old head f913fef | RED on exactly `upper POST /API/SUSTAINABILITY/CONFIG`, `title POST /Api/Sustainability/Config`, `upper-slash POST /API/SUSTAINABILITY/CONFIG/` (each 200) | green | green |
| merged tree main+ef0ff56 with the two `/i` flags removed from server.js (2 -> 0 occurrences, 4 diff lines) | RED on exactly the same 3 rows | green | green |
| same tree restored by blob (`013edba...`, hash equal, porcelain 0) | green | green | green |
| merged colmap tree main+ccb7aa4, same removal / restore (`0649326...`) | RED on the same 3 rows / green after | green | green |

## Evidence
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Refs (15:35:02 AEDT) | origin write-gates `ef0ff56e1fb7ab87a55617c0632c05a19e728c53`, column-mapping `ccb7aa4a10791c8a8f548a7301d41935648ba5c9`, l1 `70709c61...`, revocation `5fbad1ba...`, main `0364b252b826576bde6dad43ca5000df436c97b7` | `git ls-remote origin`; main printed as control |
| 2 | Stack | `70709c6` ancestor of `ef0ff56` rc 0; `ef0ff56` parent `f7639de`, parent `f913fef`; none of l1 / f913fef / ef0ff56 / ccb7aa4 / revocation is on main (rc 1 each; control `3929b794` rc 0) | `merge-base --is-ancestor`, `log --format=%p` |
| 3 | Fix diff | `f913fef..ef0ff56`: `backend/server.js` +4/-2, exactly 2 hunks, inside `feedbackItemWriteGate` and `sustainabilityConfigWriteGate` (the `i` flag on each regex + one comment line each); new `rd958-write-gate-path-variants.test.js` +169; counts +3/-3 (5516/332) | `git diff --numstat`, `-U3` |
| 4 | Partition | 9 of 10 paths in `70709c6..ef0ff56` (11 of 12 since base `3929b79`) inside OWNS-S; the one outside is `scripts/verify-expected-counts.json`, owned by no lane, written under the fix kit's OWNS (commit B only) and COUNTS AT LANDING | fnmatch program over the kit's OWNS-S block, `+new __tests__/rd<N>-*` limited to the kit's 74 keys; controls: `static/index.html` not owned, an unknown `rd99999` not owned |
| 5 | Pending sweep branches | 0 path overlap with the 3 open lane-T branches (`b1431/*` suites-from-git-archive, smtp-route-cells, csp-tool-edge-cases). The lane's own revocation branch shares `backend/server.js` (by design, round 1 F2) and merges clean onto the colmap head (`merge-tree` rc 0) | `git diff --name-only` from each merge base; control l1 vs this branch fires (7 shared paths) |
| 6 | Merge onto current main | `merge-tree 0364b25 ef0ff56` rc 1: **CONFLICT in `scripts/verify-expected-counts.json` only** (main 5536/331 vs branch 5516/332), as predicted; every other path clean. Verifier's local merge `10b8512` (tree `546dc98`) with the counts file set to the predicted pair: main->merge paths = exactly the branch's 12 paths since base; every branch path's blob in the merge equals the branch blob; branch->merge differences = exactly main's 20 paths since base | `git merge-tree --write-tree`, `git merge` in own worktree, blob compare |
| 7 | Predicted counts pair | main 5536/331 + the stack's +23 tests / +6 suites since base (5493/326 -> 5516/332) = **5559/337**. Main's newest merge `0364b25` changes one test file in place and no count (counts at `0ab365b` also 5536/331) | `git show <sha>:scripts/verify-expected-counts.json` |
| 8 | **FRESH plain verify, main 0364b25 + ef0ff56** | `npm run verify -- --maxWorkers=2` (no `--update-counts`), one acquisition `qa-b1480-2r4-v-mrg-g` 16:36:40-17:13:01: rc 0, **`VERDICT: PASS - 5559/5559 tests passed across 337 suites (jest exit 0)`**, failed 0, pending 0; **EADDRINUSE 0**; band 28960-29599 (slot 14 by the helper) listeners 0 before and after (control: all listeners 20); porcelain 0 before and after. rd407-r2: 17 cells, all passed (round 3's 3 reds are gone with main's fix, as expected) | `scripts/verify-suite.sh` through a pass-through `JEST_BIN` wrapper that only keeps jest's JSON |
| 9 | Names | merged run vs the builder's branch-alone update report (`.tools/b1483/raw/jest-g-update.json`): 0 branch names missing; the 43 extra names are all in main's 5 new test files (rd544, rd605, rd759-796, rd798-learning-manager, rd979) = main's +43 | name program over the jest JSON |
| 10 | Other CI (build.yml) | `node -c` of `backend/server.js`, `backend/azureLogAnalytics.js`, `model-config.js` at main, merged gates and merged colmap: rc 0 (control: a broken file rc 1). Lint is a placeholder script. `assert-browser.js`: OK. No package, workflow or marketplace change (npm-audit, arm-ttk not triggered by these paths) | `.github/workflows/build.yml` read at the merged tree |
| 11 | Secrets | gitleaks 8.30.1 `git --log-opts 3929b794..ccb7aa4` (11 commits): no leaks; `stdin` over `git diff 3929b794 ccb7aa4`: no leaks; control: same stdin + a planted AWS-shaped pair -> `leaks found: 1` | gitleaks |
| 12 | Names, non-ASCII, Cf, hosts, GUIDs | 0 over every added line and commit message in `f913fef..ef0ff56` (176 lines, 20 msg lines), `70709c6..ef0ff56` (489, 78) and `3929b794..ccb7aa4` (1103, 129) for Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite (`(?<![A-Za-z])<name>(?![a-z])`, re.I); controls: `x_by_<name>_y` fires for all 9, `kamera kamikaze paulownia peterson inches waiter steven` 0. Secret / GUID / host / password-literal patterns 0 (controls fire) | `scans.py` |
| 13 | Repo-wide (tracked files) | Cf characters: 5 files at main, the same 5 in both merged trees. Relative markdown links: 8 broken at main, the same 8 in both merged trees, 0 new | `repowide.py` |
| 14 | CodeQL pre-scan (added lines, tests included) | `new RegExp(<variable>)` 0, hand-escape `.replace(/[...]/g, "\\$&")` 0, innerHTML / dangerouslySetInnerHTML with a variable 0, child_process with a template string 0 (each control fires). The two changed regexes are literals and linear | `scans.py` |
| 15 | Deploy demo | the merge STARTS A RUN: not ignored after l1 lands `__tests__/rd793..`, `rd958..` x2, `rd978..`, `backend/server.js`, `backend/services/capabilities.js`, `scripts/role-capability-inventory.js`, the counts file (controls: `docs/x.md` ignored, `backend/x.js` not). `deploy-demo.yml` diff main..branch 0 lines; jobs gated on `vars.CI_DEPLOY_ENABLED == 'true'` (:53, :91 at main), so expected conclusion `skipped`. The variable was not read (no HTTP) | `git show 0364b25:.github/workflows/deploy-demo.yml`, fnmatch over `**.md`, `docs/**`, `tests/**` |

## Findings
| ID | Sev | Finding |
|---|---|---|
| F1 | Minor (landing) | The counts file conflicts with main on merge (main 5536/331, branch 5516/332): expected, the branch's pair is branch-local. Landing must regenerate it on the merged tree. Measured 5559/337 on main 0364b25 + this head; l1's commits are inside this branch, so main + l1 + this head has the same content if main has not moved. Re-measure on the actual merged tree at landing. |
| F2 | Minor (info) | The `i` flag on the feedback gate regex `/^\/[^/]+\/?$/i` is a no-op (the pattern has no letters); only the sustainability `i` is load-bearing. The shipped cells cannot see the feedback flag's removal (with both flags removed only the 3 sustainability rows go red), which is correct, and the builder's own P2 plant (a letter regex) proved the feedback rows would see a case-blind feedback gate. No action. |
| F3 | Minor (carried, round 1 F3) | RD-958 part 3, the fixed password literal on `POST /api/models/switch`, stays in source (HELD); the role gate runs before it (viewer 403, probe row A). |
| F4 | Minor (carried, round 1 F4) | Commit author on every lane commit is the shared GitHub noreply identity; messages and added lines carry no name. Not fixable without a history rewrite. |
| F5 | Minor (records, not built) | An anonymous `/API/...` request answers 302 (login redirect) instead of 401: the auth middleware's API test `req.path.startsWith('/api/')` is case-sensitive. No handler is reached (not a bypass); a response-shape item for the records pass. |

Round 3 claims re-checked: the mrg3-g verify (main 0ab365b + ef0ff56) did read 5559/337 with ONLY rd407-r2 M2/R1/R3 red (raw log, 0 EADDRINUSE): TRUE. The mrg3-c verify was killed mid-run (`Terminated: 15` at 216 suites, rd407 already red): no verdict from it. Superseded by rows 8 here and in VERDICT-colmap.

## Builder STATUS claims (fix builder STATUS, READY `ef0ff56`)
| Claim | Grade |
|---|---|
| Fix = `i` flag on both router-level regexes + one comment each, 2 hunks inside the two gate functions | TRUE (row 3) |
| Base red on exactly the 3 sustainability case rows (200) at f913fef; 3/3 green with the fix | TRUE (re-measured, red-first table) |
| P2 / P3 plants red on 4 rows each | not re-run (the stronger fix-removed-on-merged-tree plant was run instead) |
| Viewer refused on every case and slash form of all 20 routes | TRUE and wider (220 forms per tree, raw lines, persistence) |
| update and plain PASS 5516/332 at the branch | not re-run branch-alone; consistent: merged PASS at 5516/332 + main's +43/+5 with no branch name missing (rows 8, 9) |
| commit B = counts only, 5516/332 | TRUE (`f7639de..ef0ff56` 1 file) |
| name scan 0, gitleaks no leaks, deploy STARTS A RUN / skipped | TRUE (rows 11, 12, 15) |
| counts branch-local, regenerated at landing | TRUE; the conflict is measured (row 6, F1) |

## NOT RUN
- Hosted CodeQL, hosted gitleaks, CI on Linux, npm-audit, arm-ttk; `CI_DEPLOY_ENABLED` and open pull requests (no HTTP).
- A verify of main + l1 + this head as separate merges (l1 is contained in the branch; the measured tree is main + head).
- Inventory regeneration (`--generate`); Jira (fence).
