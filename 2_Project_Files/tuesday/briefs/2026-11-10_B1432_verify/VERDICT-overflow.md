GATE B1432: GO WITH FINDINGS @ a1d7f46 on main 849b808

Branch `b1432/nexusai-f-overflow-settings-390-printing-820`, head `a1d7f46da0915f2c58b10f23c74dc196b903e85a` (RD-962, RD-963). Tier 2 (front end). Own clone and worktrees under the session scratchpad, read-only to origin. Ports used: 9881-9884 only; 0 listeners after (control: the spec's server answered during the run).

BLUF: 0 Blockers, 0 Majors, 5 Minors. 4 of 4 paths are inside OWNS-F. Overlap is 0. The merge is clean, equals main plus the head blobs, and passes `npm run verify` exactly like main (PASS 5493/5493, 326 suites). The new browser spec is red on all 6 behaviour cells with the fix removed and green on all 7 at the head. The branch adds no jest test, so its counts equal the committed counts and no counts commit is needed. The merge WOULD start a `Deploy demo` run (jobs gated, see row 8).

## Evidence
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Ref = READY sha | origin ref = `a1d7f46d...` (read at start and end); main = `849b808c` | `git ls-remote`; control main printed |
| 2 | Paths in OWNS-F | 4 of 4: `static/css/settings-styles.css`, `static/index.html` (HOLD 12 files, yours), `tests/e2e/shell-layout-today.json`, `tests/e2e/rd962-rd963-page-overflow.spec.js` (A) | fnmatch program with controls |
| 3 | Overlap | 0 with all `b1431/*`, `b1433/*` branches and the other F branch. HOLD 12: 0 of 451 origin heads match `rd-?937|l3|roles-?shell` (control `refs/heads/main$` = 1). RD-937 status not read (no Jira). | `ls-remote` |
| 4 | Merge | `merge-tree --write-tree` rc 0, tree `42c7f1fe`; main->merge equals base->head (4 paths, statuses, blobs byte-equal). Both branches together also merge clean (rc 0). | `git diff --raw`, `cmp` |
| 5 | Tree of head | `3fd36275a629`, equal to the builder's stated tree | `rev-parse` |
| 6 | CI: verify | main PASS 5493/5493, 326 suites. Merge PASS 5493/5493, 326 suites, 0 failed suites, counts predicate satisfied with the committed file. | `verify-suite.sh --maxWorkers=2` under the jest lock |
| 7 | Red without the fix | The new spec copied onto main: 6 failed, 1 passed (the control). RD-962 cells: brand ends at 435, viewport 390 (light, dark). RD-963 cells (printers, scanning, light, dark): tile rows 1, not 2. At the head: 7 passed. | Playwright against a seeded server (1445 demo rows), port 9881 then 9882 |
| 8 | Deploy demo | The merge TRIGGERS a run: `static/**` is not in `paths-ignore` (`**.md`, `docs/**`, `tests/**`). Jobs gated on `vars.CI_DEPLOY_ENABLED == 'true'`; the variable was not read (no HTTP): after landing the run must read all jobs `skipped`. | `git show origin/main:.github/workflows/deploy-demo.yml` |
| 9 | Other CI | gitleaks over the branch diff exit 0 (control exit 1). npm-audit, arm-ttk: no package or marketplace change. Hosted CodeQL not run. | `gitleaks stdin` |
| 10 | Repo-wide scans | Cf scan over tracked text: same 5 files at main and merge. Name scan (added lines + message) 0; 9 planted controls fire. Secrets, GUIDs 0; hosts: `http://127.0.0.1` only; non-ASCII: 4 lines, all U+2014 (em dash) in the spec comments. | python scans |
| 11 | CodeQL pre-scan | `new RegExp(` variable, `$&` hand-escape, innerHTML, child_process, eval: 0 added hits (controls fire). The spec reads `path.join(VENDOR_DIR, hit[0])` where `hit` comes from a fixed map keyed by request path and `VENDOR_DIR` is an operator env var; no request data reaches a path. | grep with controls |
| 12 | Boundary probe | Overflow and tile fit (figure inside tile, label not clipped) at widths 320, 360, 390, 414, 767, 768, 820, 991, 992, 1100, 1440, main vs head. Settings overflow main 115, 75, 45, 21 at 320/360/390/414 -> head 0 at all. Printing/Scanning: main 768 overflow 21 and 6, all 4 tiles bad at 768-1100 -> head 0 bad at 768-991. No width got worse. | own Playwright probe, same seeded data |
| 13 | Layout record | `shell-layout-today.json` diff: engine version line plus exactly the 12 cells `settings|390`, `index:printers|820`, `index:scanning|820` x light/dark x two data states; all other cells byte-equal. The overflow figures move 60->0 (settings), 2->0 (printers, rows). | `git diff -U0` |
| 14 | index.html edit | exactly the 12 `col-md-3` columns that wrap a `.stat-card` changed to `col-md-6 col-lg-3 mb-md-3 mb-lg-0`; 0 stat-card columns keep `col-md-3`. | grep before/after |

## Findings
| ID | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | The tiles are still clipped (label cut or figure outside the tile) at 992 to about 1199 px, on all 4 tiles of Printing and Scanning; at 1440 one Scanning tile. Unchanged from main (not caused by the branch) and outside the tickets' named widths, but the builder only reported 1100. | probe row 992/1100: bad 4 of 4 at both main and head |
| F2 | Minor | The 2 px page overflow of RD-963 did not reproduce in my headless browser (overlay scrollbars, overflow 0 at 820 on main); only the tile clipping did (4 of 4 bad at 820 on main). The builder's 2 px comes from classic scrollbars in the recorder. The spec's red cells rest on tile geometry, which does reproduce. | probe row 820 main |
| F3 | Minor | The Overview user-detail row is changed in `index.html` (4 of the 12 columns) but no cell drives it; the spec covers Printing and Scanning only. | spec reads `#printers`, `#scanning` |
| F4 | Minor | The 820 cells assert "two tile rows", which pins the chosen design (2 per row) and not only the defect. A different valid fix (for instance a smaller figure) would read red. | spec lines for `tops.length` |
| F5 | Minor | The appended CSS rule is indented by one space and the comment is a single long line; style only. Also the spec comment uses em dashes. | `git diff` |

## Counts commit
None needed. The branch adds no jest test (the spec lives in `tests/e2e`, which jest ignores). Measured at the merge: 5493 tests / 326 suites, equal to the committed `scripts/verify-expected-counts.json`. If the shell branch lands first, the file will read 5494/327 and this branch's merge then measures 5494/327 too, with no further change.

## Builder STATUS claims
| Claim | Grade |
|---|---|
| RD-962 brand 423 px wide, overflow 60 (435 vs 375) | true (scrollWidth 435 reproduced; 45 at a 390 client width) |
| RD-963 label shrinks to 0, figures outside tiles at 820 | true (tile geometry reproduced) |
| 2 px page overflow with rows | not shown here (see F2) |
| base 6 failed + 1 passed, head 7 passed | true |
| record regenerated, only 13 cells moved | true by diff; the recorder re-run is not shown by me |
| tree `3fd36275...` equals h1; verify PASS 5493/326 | true |
| gitleaks 0, name scan 0, CodeQL pre-scan 0, partition empty, HOLD 12 0 refs | true |

## NOT RUN
- Hosted CodeQL, hosted gitleaks history scan, npm-audit, arm-ttk.
- The `CI_DEPLOY_ENABLED` variable, the open-PR list and RD-937's Jira status (no HTTP, no Jira).
- The shell-layout recorder against the new record (it boots servers on the jest helper's port band, outside 9880-9889); Chrome with classic scrollbars; dark-mode probes beyond the spec's own cells.
- A separate verify at the head commit (differs from the merge only by HISTORY.md).
