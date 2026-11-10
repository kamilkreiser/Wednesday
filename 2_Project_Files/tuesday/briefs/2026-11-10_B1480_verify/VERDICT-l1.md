GATE B1480-l1: GO WITH FINDINGS @ 70709c6 on main 849b808

Branch `b1480/nexusai-s-l1-design-inventory`, head `70709c61d4f555cd6e28f3bb83ad75d811a32907`, parent `3929b794` (the predecessor's cut, not re-cut). Tickets RD-929, RD-977, RD-978. Tier 1 handling (auth-surface design table). This is the STACK BASE; it lands first. It adds no gate and changes no route behaviour: a capability table module, the inventory tool and its generated docs, and three tests.

BLUF: 0 Blockers, 0 Majors, 3 Minors. 7 of 7 paths inside OWNS-S, 0 overlap with siblings. Merge clean, equal to head + main's HISTORY.md. Plain verify of main + head PASS 5507/329 with EADDRINUSE 0. All 8 new tests red without the change. The merge starts a Deploy demo run whose jobs are gated (expected skipped). The landing needs a counts commit (5507/329).

## Evidence
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Ref = READY sha | origin = `70709c61...`; main `849b808c` | `git ls-remote`, control main |
| 2 | Parent | `3929b794`, an ancestor of main; main moved by HISTORY.md only (76 lines, 1 file) | git |
| 3 | Paths | 7 of 7 in OWNS-S (3 new rd929/977/978 tests by `+new`, `capabilities.js`, inventory script, 2 docs); 0 in any of B1481/B1482/B1431/B1432/B1433; 0 with the 8 other-lane pushed branches | partition program; controls fire |
| 4 | Merge | `merge-tree` rc 0, tree `456a46e1` = head tree + main's HISTORY.md blob | merge-tree, diff |
| 5 | Verify main + head | plain, counts file at 5507/329: `VERDICT: PASS - 5507/5507 tests passed across 329 suites`, EADDRINUSE 0, band 20000-20639 empty before and after | verify-suite under the jest lock |
| 6 | Main and names | main itself PASS 5493/326; main -> main+head: +14 tests (rd929, rd977, rd978), removed 0, failing suites added none. Whole stack PASS 5516/332, all four PASS 5522/334 | verify-suite; compare.py |
| 7 | Red without the change | the 3 test files planted on main: 3/3 suites red; rd929 cannot load `../backend/services/capabilities` (by construction), rd977 3/3 red, rd978 5/5 red | `raw/red1.json` |
| 8 | Deploy demo | STARTS A RUN (`__tests__/`, `backend/`, `scripts/` not ignored; the 2 docs ignored); workflow untouched; jobs gated on `vars.CI_DEPLOY_ENABLED == 'true'` (:53, :91), expected skipped | workflow text |
| 9 | CI | `node --check` server.js, azureLogAnalytics.js, model-config.js OK (control rc 1); gitleaks rc 0 (control rc 1); no package/azure-marketplace change | |
| 10 | Scans | names 0 in 551 added lines + 14 message lines (controls fire); secrets/GUID/hosts/Cf/non-ASCII 0; repo-wide Cf 5 = 5; md links 8 broken at main = 8 at all-four, 0 new | scans.py, repowide.py |
| 11 | CodeQL pre-scan | 0 hits for each of the four patterns (controls fire) | |

## Findings
| ID | Sev | Finding |
|---|---|---|
| F1 | Minor | Counts file unchanged on the branch (5493/326); the landing needs a counts commit to 5507/329 on the tree as it will be merged, else the PR Build reads VERDICT: FAIL. |
| F2 | Minor | Its stacked children (gates, colmap) are NO GO (VERDICT-gates F1); this branch lands alone without them. Its `PENDING_GATE` list in `capabilities.js` still names RD-958's routes as pending, which is true until the gates branch lands. |
| F3 | Minor (metadata) | Commit author `kamilDatasec <...noreply.github.com>`; no name in message or added lines. |

## Builder STATUS claims
| Claim | Grade |
|---|---|
| plain PASS 5507/329, EADDRINUSE 0 | true (my plain run on main + head: same) |
| red-first at base (predecessor's 12/12 covers both rescued branches: rd977 3 + rd978 5 + rd972 3 + rd976 1, rd929 not loadable) | true (my run: rd977 3/3, rd978 5/5 red, rd929 suite fails to load) |
| merges clean onto 849b808c | true |
| partition 7/7 | true |

## NOT RUN
- Hosted CodeQL, npm-audit, arm-ttk, `CI_DEPLOY_ENABLED` read, Jira (fences).
- A separate run at the head commit itself (head differs from the merge by HISTORY.md only).
