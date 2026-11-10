GATE B1480-colmap: NO GO @ 2a584f7 on main 849b808

Branch `b1480/nexusai-s-setup-column-mapping`, head `2a584f7de26ed0b3dfeed9795187fe3cbf71b232`, a MERGE commit (parents `18a0b1c`, `f913fef`), STACKED ON the write-gates branch. Ticket RD-967. Tier 1 by stack (it carries the write-gates commits).

BLUF: NO GO because it carries its parent's Blocker (VERDICT-gates F1: viewer bypasses the sustainability-config gate by letter case); landing this branch lands that gate. Its OWN change (4 files) is clean: inside the lane, red without the fix, green on the merged tree, no behaviour change outside the route. When the parent is fixed and re-gated, this branch needs the fix merged in (forward merge, as it did for `f913fef`) and a re-gate; its own content needs nothing. The builder's UNMEASURED plain run is now MEASURED: PASS 5516/332 on main + this head.

## Evidence
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Ref = READY sha | origin = `2a584f7d...` | `git ls-remote`, control main |
| 2 | Stack | `merge-base --is-ancestor f913fef 2a584f7` rc 0; `git diff f913fef..2a584f7` = 4 files (A rd967 test, M server.js, M ROLE-CAPABILITIES.md, M role-capabilities.json) | git |
| 3 | Paths | 4 of 4 in OWNS-S; 0 in any sibling kit's OWNS; 0 overlap with other lanes' pushed branches | partition program with controls |
| 4 | Merge | on parent: `merge-tree` rc 0 = head tree `905864e1`; onto main rc 0, tree `6914e3e9` = head tree + main's HISTORY.md | merge-tree, diff |
| 5 | Verify main + head (whole stack) | **plain** run with the counts file at the claimed 5516/332: `VERDICT: PASS - 5516/5516 tests passed across 332 suites`, EADDRINUSE 0, band empty before/after | verify-suite under the jest lock |
| 6 | Verify all four onto main | PASS 5522/334, EADDRINUSE 0 | same |
| 7 | Names | vs main+l1: +3 rd967, +6 gates, rd978 probe cell renamed; failing suites added none | compare.py |
| 8 | Red without the fix | rd967 planted on main + write-gates head: 3/3 RED (GET 500; POST registered twice) | `raw/red4.json` |
| 9 | Cause / fix at source | GET called `jsonStorage.get('columnMapping')`; JsonStorage has no `get()`, so 500. Now `getSetting('logAnalyticsColumnMapping')`, the key the first (live) POST writes (server.js:15037) and boot reads (:4387). The removed second POST was unreachable: the first handler always responds and takes no `next` | git grep |
| 10 | Deploy demo | STARTS A RUN (`backend/`, `__tests__/`); workflow untouched; jobs gated on `CI_DEPLOY_ENABLED`, expected skipped | workflow text |
| 11 | Scans | names 0 (86 added lines, 27 message lines incl. the merge), secrets/GUID/hosts/Cf/non-ASCII 0, gitleaks rc 0 (control rc 1), CodeQL pre-scan 0, `node --check` OK | scans.py |

## Findings
| ID | Sev | Finding |
|---|---|---|
| F1 | Blocker (inherited) | Carries VERDICT-gates F1. |
| F2 | Minor | Behaviour change by design: `GET /api/setup/column-mapping` now answers 200 with the stored wizard mapping to ANY signed-in session, viewer included (was 500 for everyone). The admin route `GET /api/admin/column-mapping` is admin-only and reads a different key (`columnMapping`). So a viewer can now read the wizard's Log Analytics column names. Low sensitivity (identifiers only), but it is a new viewer read; the roles rulings (RD-930ff) may want it admin-only. Also two keys for one concept remain (pre-existing). |
| F3 | Minor | Landing by merge commit carries the builder's internal merge `2a584f7` into main's history (no rebase was used, per the hold). Fine under C-68; noted. |

## Builder STATUS claims
| Claim | Grade |
|---|---|
| cause: store has no get(); first POST answers | true |
| update PASS 5516/332 | consistent (my plain run PASS 5516/332 on main + head) |
| plain run UNMEASURED | now measured: PASS |
| inventory: exactly 2 rows change | true by doc diff (GET row 500->200 x3, POST note) |
| partition flag on server.js | false positive (see VERDICT-gates F2) |

## NOT RUN
- Hosted CodeQL, npm-audit, arm-ttk, `CI_DEPLOY_ENABLED` read, Jira. Inventory regeneration.

No landing files: NO GO.
