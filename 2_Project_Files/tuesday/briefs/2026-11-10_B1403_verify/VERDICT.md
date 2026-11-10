GATE B1403: GO WITH FINDINGS @ 4d06d65 on main 97cf7a9

Tier G2 (tests only), per the kit's S8. Gate run 09:20-09:58 AEDT 2026-11-10, own clone under the session scratchpad (push URL set to INVALID-NO-PUSH; nothing pushed). Final origin read 09:57:27 AEDT by `git ls-remote` over the deploy key: branch = 4d06d65e0df9250652faa63f73936d093c3317bc (= READY sha), main = 97cf7a9af9dfd6cf20e66fc8d0bc19454a4d9e4b.

## Evidence (each by program, with its control)
| Step | Result |
|---|---|
| Refs | ls-remote branch = READY sha. merge-base(main, head) = 31234f5f (= S2). Head is 1 ahead, 4 behind main (089a639, 94b24e8, 8d665e3 = #169, 97cf7a9 = #170). |
| Paths | `git diff --name-only 31234f5f 4d06d65e` = 1 path, `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs`; it is in the lane's OWNS (1 of 1). Removed lines 0; added 67. |
| Overlap with the two morning merges | #169 (8d665e3f) touches infra/tests, scripts/** (5 files); #170 (97cf7a9a) touches src/MpsCalc.Api/Sources/** and two new LaneM5*.cs tests (5 files). Path overlap with this head: 0. Neither touches src/MpsCalc.Api/Quotes/** (the code the new rows exercise): `git diff --stat 31234f5f 97cf7a9a -- src/MpsCalc.Api/Quotes` is empty, so QuoteEndpoints.cs is byte-equal at base, head and main (sha256 42c7885b...). Semantic overlap: measured at the merge tree below, 0 failures. |
| Overlap with sibling lanes / open PR heads | Every fetched origin `b14*` branch diffed from its merge-base with main: overlap with QuoteRefusalOrder.cs = 0 for b1402, b1404, b1405, b1406, b1407 (control: b1403 itself = 1). PR heads by ls-remote: #167 = b1406, #168 = b1402, #171 = b1405 (all 0 overlap); #169/#170 are on main. |
| Merge | `git merge-tree --write-tree main head` rc 0, tree 3b34021f; `diff main tree` = exactly the one path, and its blob c756bdd6 = the head blob (main/base blob ea91657d). Clean, = main + head blob. |
| CI `dotnet` (the only job reading the changed path; web/python/package do not read it, `git grep` for the path/class in *.py, *.sh, *.mjs, *.ts, *.yml = 0) | Same commands as ci.yml:42-43, SDK 10.0.401 (global.json 10.0.100 latestFeature), restore offline from the local cache. main: build rc 0, 0 Warning(s); test rc 0; trx Engine 743 / Import 196 / Api 3398, 0 failed. head: build rc 0, 0 Warning(s); test rc 0; 743 / 196 / 3389 (= builder's 4328). merge: build rc 0, 0 Warning(s); test rc 0; 743 / 196 / 3420, 0 failed. By name: main-not-in-merge 0; merge gained 22 = exactly the head's 22 new names (9 + 2 cases x DevStub and Entra hosts). head-vs-main "lost 31" = the tests main gained after the branch point (#170's LaneM5 rows, 089a639's TemplateIsolation rows), not a loss. |
| Red without the fix (head tree copy, 22 new results filtered) | no mutant: 22 pass. M7b (InternalInputs moved after the edit check): 6 red, all `internal`. M9 (TaxRateFixed moved): 6 red, all `tax`. Mv (whole body chain moved after the lookup): 18 red = all 9 x 2 R1 cases. M3 (NotEditable before NotOwner): 4 red = all R2 cases. Planted Assert.Fail control: rc 1. Mutant file restored from `git show` after each, sha256 back to 42c7885b, `git diff --quiet` rc 0. |
| Survival at main (are the rows new kills?) | Whole Api project at main 97cf7a9 (no new rows) under Mv: 3398 passed, 0 failed; under M3: 3398 passed, 0 failed. Both orders are pinned by no committed row on main; the new rows are the only kill. Not vacuous. |
| Closed lines re-verified at main 97cf7a9 | MPSCALC-340: GovernedNullClassEdges.cs:526, :534, :539 are the named rows. MPSCALC-341: :352, :356, :362, :363, :364, :397 are the named assertions. MPSCALC-324: StoreLoadFaultMapping.cs:72, :88 and BodyRefusedLastBranch.cs:25, :33 are the named rows. MPSCALC-333 clauses 1-3: QuoteRefusalOrderGuard.cs:127, :141, :150; QuoteRefusalOrder.cs:168, :186. All green in the main run (0 failed). MPSCALC-310 pointers: QuoteEndpoints.cs:756, :761 and QuoteFigures.cs:27, :117 read as the STATUS says. docs/API.md:49-50 ("owner only ... 403 NOT_QUOTE_OWNER") and CLARIFICATIONS.md C-62 (owner/state/existence before range; rules no body-check order) read as stated. |
| Scans | Name scan `(?<![A-Za-z])<name>(?![a-z])` (ban list) over 67 added lines and the commit message: 0 (control `_by_Kam_` fires). B-number/seat/C-entry/finding ids: 0 (control `B591` fires). Secret regex 0 (control `ghp_` fires); gitleaks 8.30.1 random synthetic canary rc 1, range 31234f5f..4d06d65e rc 0. GUIDs, hosts, URLs: 0. Cf and non-ASCII in added lines and message: 0 (control U+200B fires). Repo-wide Cf walk over all 684 tracked files: main 6 files, merge 6 files, identical lists (pre-existing test data, not this lane). Markdown changed main..merge: 0 files, so link results are unchanged. |
| Deploy | MPS ci.yml has no deploy job; on main the package job keeps an artifact only. A merge deploys nothing. |

## Findings
| # | Severity | Finding |
|---|---|---|
| 1 | Minor | Not shown by this gate (HTTP to hosted hosts is fenced): the STATUS's Jira reads (5 tickets Backlog, 0 comments after 2026-11-09), the closed-PR scan (#1-#166), and Jira comment pointers 40538/40773/40220/40478/40156. Graded "not shown"; the code-side pointers they support were re-verified at main above. |
| 2 | Minor | Not re-run: the builder's Sf result (30 existing rows already kill "NotEditable on the first version") and the batch-1 M8r reading (killed only through a null read). Graded "not shown"; neither changes the diff (no row was added for either). |
| 3 | Note | R1 (18 results) pins an order that no doc line or C-entry rules (body checks before the lookup); C-62 rules owner/state/existence before range only. It is a characterisation pin, flagged by the builder; if the product owner ever wants existence/ownership checked before the body, R1 is the row to change. Not a defect. |
| 4 | Note | Builder self-reported two process slips outside the repo (one `sed -i` on its own scratch script; the pre-push main re-read was printed, not program-gated). Nothing in the diff or history is affected. |
| 5 | Note | The commit's author metadata is the repo's git identity (a person's name); it is not in the message, and the head-pinned squash writes a new commit. landing.txt necessarily carries the branch ref name. |

## Claims graded (builder STATUS)
| Claim | Grade |
|---|---|
| Base 31234f5f = S2; one commit; 1 path changed | true |
| global.json 10.0.100 latestFeature; SDK 10.0.401 | true |
| Owned files at base 789 / 193 / 157 / 749 lines | true |
| Baseline 4306 (743/196/3367), head 4328, lost 0, gained 22 = R1/R2 | true (head measured 4328; 4328 - 22 = 4306) |
| Head build 0 warnings, 0 failed | true |
| M3 4 red, M7b 6, M9 6, Mv 18, each only in the new rows | true (reproduced exactly; survival of Mv and M3 at main measured over the whole Api project) |
| M8r batch-1 reading; Sf already pinned by 30 rows | not shown |
| 67 added lines, non-ASCII 0, removed 0, names/ids 0, gitleaks rc 0 | true |
| Pushed head 4d06d65e; compare at push ahead 1 behind 2, 1 file | true (now behind 4: main moved, paths disjoint) |
| Commit subject 92 characters | true |
| ALREADY-ON-MAIN 340/341/324 and 333 clauses 1-3 file:line pointers | true at main 97cf7a9 |
| 310 needs a product seam (QuoteEndpoints.cs:761, QuoteFigures.cs:117, static class :27) | true as source reading (pointers verified; no mutant run by the gate) |
| Jira states/comments, closed-PR scan | not shown (fenced) |

## NOT RUN
- Hosted CI (all four jobs on the Linux runner) and CodeQL: hosted CI is the proof; read them on the PR before landing.
- web, python and package jobs: they read no changed path (web/ untouched; no tests outside the dotnet job reference the file).
- Any Jira or GitHub API read (fenced: no HTTP to hosted hosts). Open-PR state taken from `refs/pull/*/head` by ls-remote only, not from the PR API.
- The SQL Server leg, Playwright/e2e, any hosted site, real price books.
- Mutants M8r and Sf (not needed for the diff; see findings 2).
