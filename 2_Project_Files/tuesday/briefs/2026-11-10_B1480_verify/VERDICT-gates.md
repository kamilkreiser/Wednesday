GATE B1480-gates: NO GO @ f913fef on main 849b808

Branch `b1480/nexusai-s-viewer-write-gates`, head `f913fefb805928fc56b9cd11fc12bac476d2ac92`, STACKED ON `70709c61` (l1). Tickets RD-958 (16 routes), RD-793 (4 routes). Treated as tier 1 (permission / write-gate change; kit Level row C3). Verifier worked in its own clone and worktrees under the session scratchpad (push URL invalid, no dot component in any path), read-only to origin.

BLUF: 1 Blocker (security), 0 Majors, 3 Minors. The branch is clean, green and inside the lane, but one of its twenty gates can be walked round: a signed-in viewer still writes the sustainability config by changing the case of the path (`POST /api/sustainability/CONFIG` answers 200 at head, as it did at base). The kit's property for this lane is "every listed route refuses a viewer write"; that is false for 1 of 20. Fix is one forward commit (see F1). Every other gate held under every variant tried, and no other viewer or anonymous status changed.

## Evidence
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Ref = READY sha | origin `refs/heads/b1480/nexusai-s-viewer-write-gates` = `f913fefb...` (4 of 4 b1480 refs equal STATUS); main `849b808c` (3929b794 + HISTORY.md only) | `git ls-remote`; control `refs/heads/main` printed |
| 2 | Stack | `merge-base --is-ancestor 70709c6 f913fef` rc 0; parent of the 5 new commits is `70709c6`; control: branch 2 is not an ancestor of the stack (rc 1) | git |
| 3 | Paths in OWNS-S | 8 of 8 (`server.js`, `capabilities.js`, inventory script, the two docs, rd793 and rd958 new, rd978 which is `+new` against main) | fnmatch program over the kit's OWNS-S block; controls: `static/index.html` not S, `docs/x.md` in T fires |
| 4 | Sibling lanes / pending | 0 of 8 paths in OWNS of B1481, B1482, B1431, B1432, B1433; 0 overlap with the 8 pushed b1431/b1432/b1433 branches (39 files) | same program |
| 5 | Merge | parent-on-parent `merge-tree` rc 0 = head tree `6e3cffec`; onto main rc 0, tree `387a5359`, equal to the head tree plus main's HISTORY.md (head->merge diff = HISTORY.md only, blob = main's) | `git merge-tree --write-tree`, `git diff` |
| 6 | Whole stack onto main | main + `2a584f7` rc 0 (tree `6914e3e9`); that + branch 2 rc 0 (tree `be5e838c`) | merge-tree |
| 7 | Verify, cumulative merge trees (all plain runs) | main+l1: PASS 5507/329. main+colmap (contains this branch): PASS 5516/332. All four: PASS 5522/334. EADDRINUSE 0 each | `scripts/verify-suite.sh --maxWorkers=2` under the jest lock, plain run, counts file set to the claimed pair |
| 8 | Verify main + this head | plain, counts at 5513/331: `VERDICT: PASS - 5513/5513 tests passed across 331 suites`, EADDRINUSE 0. Names vs main+l1: +7 (rd958 3, rd793 3, renamed rd978 probe cell), -1 (old rd978 probe cell); failing suites added none. Main itself: PASS 5493/326 | verify-suite under the jest lock |
| 9 | Names l1 -> stack | added rd958 x3, rd793 x3, rd967 x3, one renamed rd978 probe cell; removed the old rd978 probe cell; failing suites added none | `compare.py` over the jest JSON |
| 10 | Red without the fix | rd958, rd793 and the new rd978 cell planted on main+l1: the viewer cell of each RED, rd978 probe RED, the administrator and open cells green (their controls) | jest on the 3 files, `raw/red3.json` |
| 11 | ADVERSARIAL PROBE (viewer, enforced shape) | 22 path variants of the gated writes and 14 neighbouring routes, at main+l1 and at all-four. Gated: canonical, trailing slash and query on sustainability config; feedback PATCH/DELETE canonical, trailing slash, `/API/FEEDBACK/`, `/Api/Feedback/`; `/API/SETTINGS/COSTS`, `/api/settings/costs/`, `/api/Models/Switch`, `/api/DATA-SOURCES/:id`, `/api/data-sources/:id/tables/` -> all 403. **NOT gated: `POST /api/sustainability/CONFIG`, `/Config`, `/API/SUSTAINABILITY/CONFIG` -> 200 (base 200).** 14 neighbours (GETs, triage, `/test`, batch, settings/agent, health) equal base vs head. Anonymous: 36 of 36 equal base vs head | `__tests__/zz-gate-probe.test.js` planted in two scratch worktrees (never committed), through `inventory.bootShape`; `raw/p-base.probe.json`, `raw/p-head.probe.json` |
| 12 | Cause of row 11 | `sustainabilityConfigWriteGate` tests `/^\/config\/?$/` (case-sensitive) on `req.path`, but the router is `express.Router()` with default `caseSensitive: false` (Express ^5.1.0), so `router.post('/config')` matches `/CONFIG` and the gate's regex does not. The feedback gate's regex `/^\/[^/]+\/?$/` has no letters and holds; the 17 handler gates run inside the handler and hold | `backend/server.js` (mount block after `createSustainabilityRouter` comment), `backend/routes/sustainability.js:164,339`, `package.json:58` |
| 13 | Deploy demo | the merge STARTS A RUN (`backend/`, `__tests__/`, `scripts/` not in paths-ignore; docs ignored); `deploy-demo.yml` untouched; jobs gated on `vars.CI_DEPLOY_ENABLED == 'true'` (:53, :91), so expected all jobs skipped. The variable was not read (no HTTP) | `git show origin/main:.github/workflows/deploy-demo.yml` |
| 14 | Other CI | `node --check` of server.js, azureLogAnalytics.js, model-config.js at every merge tree: OK (control: a broken file rc 1). gitleaks stdin over the diff rc 0 (control token rc 1). No package or azure-marketplace change | |
| 15 | Scans | Names: 0 hits in 315 added lines and 58 message lines (9 names, `_by_<name>_` controls fire, longer words do not). Secrets, GUIDs, hosts, non-ASCII, Cf: 0. Repo-wide Cf: 5 files at main, same 5 at all-four. Relative markdown links: 8 broken at main, the same 8 at all-four, 0 new | `scans.py`, `repowide.py` |
| 16 | CodeQL pre-scan | `new RegExp(var)`, hand-escape `.replace`, innerHTML, child_process template: 0 in added lines (each pattern's control fires). New regexes are literal and linear | |

## Findings
| ID | Sev | Finding |
|---|---|---|
| F1 | Blocker (security, tier 1) | A signed-in viewer bypasses the RD-958 gate on `POST /api/sustainability/config` by letter case (`/CONFIG`, `/Config`, `/API/SUSTAINABILITY/CONFIG` all answer 200, the handler's status). The branch claims all 16 RD-958 routes refuse a viewer; 15 do. Not a regression (base is 200 too), but the gate as written does not close the ticket and its test cannot see it (it drives canonical paths only). Fix: make the check case-insensitive (`/^\/config\/?$/i`) or, better, gate inside the router's handler or on `router.post('/config', gate, ...)` so routing and gating cannot disagree; add a cell that drives `/CONFIG` as a viewer and expects 403. One forward commit, then re-gate. |
| F2 | Minor | Builder's partition flag on `backend/server.js` (shared with branch 2) is a false positive: the kit's PENDING table is the other lanes' 8 branches; this lane's own branches share `server.js` by the kit's design (stack base + rescued branch 2 with a fixed parent). Measured: all four merge clean in either order onto main and the all-four tree is green. |
| F3 | Minor | RD-958 part 3 (fixed password `'access'` on `POST /api/models/switch`) is HELD as the builder says; the role gate now runs before the password check (viewer 403, verified). The literal stays in source. |
| F4 | Minor (metadata) | Commit author `kamilDatasec <...noreply.github.com>`, same as every lane; messages and added lines carry no name. |

## Builder STATUS claims
| Claim | Grade |
|---|---|
| 16 RD-958 routes + 4 RD-793 routes refuse a viewer | FALSE for 1 of 20 (F1); true for the canonical paths and for 19 of 20 under variants |
| admin and open-window statuses unchanged | true (its own cells green; probe shows no neighbour change) |
| update PASS 5513/331 at f913fef | true (my plain run on main + head PASS 5513/331) |
| plain PASS 5513/331 (b958-plain) | true (same run) |
| first run red on a stale rd978 cell, fixed forward | true (rd978 cell red on main+l1, green on the stack) |
| inventory: 20 rows changed, only viewer -> 403 | not re-generated; consistent with the probe |
| merge-tree rc 0 with branch 2 | true; plus a full verify of all four PASS 5522/334 |

## NOT RUN
- Hosted CodeQL, hosted gitleaks history scan, npm-audit, arm-ttk; `CI_DEPLOY_ENABLED` and open PRs (no HTTP).
- Inventory regeneration (`--generate`); Jira (fence).
- Load was 16-25 through every run (Spotlight indexing, not this gate); every run read EADDRINUSE 0.

No landing files: NO GO.
