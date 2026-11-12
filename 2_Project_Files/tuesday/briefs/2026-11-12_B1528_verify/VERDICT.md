GO WITH FINDINGS
Gate G2, one round, 2026-11-12 10:20-10:55 AEDT. Project MPS Calculator, ticket MPSCALC-110, branch b1528/mps-110-rental-short-one-page @ 3d082016deb18c2bead655b12cac148c03148643 (shown as 3d08201) on main 793d0a9c52c961852b4a1f04bb826ffff752ce74 (shown as 793d0a9). No security-shaped issue found (web rendering of existing data; no input, URL, regex-from-variable or HTML sink added).

Short answer on "always fits one page": MET for the Devices table (the cap), NOT MET for a quote with many hardware and software rows (F1), and not for device names long enough to wrap over several lines (F3). The product owner decides whether F1 needs a follow-up.

## Refs and merge (measured)
- `git ls-remote origin` at 10:50: branch = 3d082016deb18c2bead655b12cac148c03148643 (one b1528 ref), main = 793d0a9c52c961852b4a1f04bb826ffff752ce74. Head is 1 ahead and 1 behind main (`rev-list --left-right --count`: 1 1); the one commit behind is #185.
- Commit identity: `git log --format='%h %ae | %ce'` = `3d08201 kamil.kreiser@datasec.com.au | kamil.kreiser@datasec.com.au`, the repo's own address, committer equal to author.
- Changed paths: 4 of 4 inside the lane (`grep -c -v -x -E` over the allowed list prints 0; the 4 are ProposalPage.tsx, ProposalPage.test.tsx, print.spec.ts, proposal-buttons.spec.ts). Diff +133 -2 base..head. The 2 removed lines are exactly `expect(n).toBeGreaterThanOrEqual(1);` and `{p.lines.map((l) => (`.
- #185 (main's one new commit) touches `src/MpsCalc.Api/Feedback/FeedbackStore.cs` and 3 files under `tests/`: overlap with the head 0. Open PRs 0 (`gh -X GET pulls?state=open` printed no row; control `pulls/99999` is 404 and `pulls?state=all` returns #185). The sibling lane B1527's granted paths (per the kit's S3) are src/docs/tests only: overlap 0.
- `git merge-tree --write-tree 793d0a9 3d08201` rc 0, tree fb0ce6be. `git diff --cached --name-only 793d0a9` against that tree (in my own merge tree) lists exactly the 4 head paths, so the merge is main plus the head blobs. All merge runs below used that tree (a local read-tree, never committed, never pushed).
- Purchase short form unchanged: blob of `web/src/proposal/OnePager.tsx` e8dab2ac at base and at head; `one-pager.css` 8b75cdab at both. `proposal-buttons.spec.ts` `B109ROOM` lines (9 lines, 3 pages each, coverRoomLeftMm 89/83/131/56/50/73/73/68/68) are identical at main, head and merge.
- Landing: only workflow is `ci.yml` (push to main runs CI; no deploy workflow). A merge triggers no deploy.

## CI by program (my clones under fleet/state/s271/g1528; Node v24.22.2; Playwright 1.63.0 installed Chrome; ports 9870-9874 and 9879 dead API origin)
| Check | main 793d0a9 | head 3d08201 | merge |
|---|---|---|---|
| `npm run lint` | not run | rc 0 | rc 0 |
| vitest (`npx vitest run`, same script as `npm test`) | 1531 passed, 0 failed, 145 files | 1541 passed, 0 failed, 145 files | 1541 / 0 / 145 |
| sorted `path :: fullName` lists | - | lost 0, gained 10 = the 10 new Vitest rows | lost 0 vs main, 0 differ from head |
| `VITE_MPSCALC_AUTH=entra npm run build` + `check-bundle.mjs dist` | not run | rc 0; 8 files, 1109118 bytes, markers 0/57 | same, 1109118 bytes |
| Playwright, CI step 2 (MODE=api-off, whole `npx playwright test`, the CI command) | 46 passed | 51 passed (print.spec 6 of 6) | 51 passed |
| Playwright, CI step 1 (MODE=stub, VITE_MPSCALC_API_STUB=1, whole) | 192 passed, 5 skipped | 192 passed, 10 skipped (5 new print rows skipped, reason printed) | 192 passed, 10 skipped |
| `proposal-buttons.spec.ts` (local, pdftotext), stub off | 22 of 22; B86RENTAL pages 1,1,1,2,3 at 3,5,7,12,40 | 22 of 22; pages 1,1,1,1,1; `MPS110SUMMARY` finds `and 2/7/35 more lines (see full proposal)` | 22 of 22, same |
Controls: a name not in the list is found 0 times and a name removed from a copy shows `lost 1`; a mutation (below) made vitest and Playwright fail rc 1 before I trusted the greens.
Other jobs: Python tests that name the changed paths: `grep -rl` over tests, scripts/tests, infra/tests, tools/demo/test for ProposalPage|ProposalView|SHORT_FORM_BUTTON|print.spec|proposal-buttons printed 0 (control: `ci\.yml` finds test_ci_workflow.py and test_sdk_pin.py). dotnet and package jobs read no changed path.
Repo-wide Cf scan of `git ls-files` at head and merge: 7 files, all pre-existing test fixtures and none in the diff (control: planted U+200B reads 1).

## Own measurement (throw-away spec in my folder, quarantined after; `emulateMedia print`, `page.pdf` A4, page count by the file's `/Type /Page` regex; article height in mm; margin = 265 - height)
| lines | pages | article mm | margin mm (703 px, the print.spec path, matches paper width) |
|---|---|---|---|
| 5 (breakdown parts) | 1 | 224.6 | 40.4 |
| 6 | 1 | 231.2 | 33.8 |
| 10 | 1 | 231.2 | 33.8 |
| 40 | 1 | 231.2 | 33.8 |
| 6 / 10 / 40, no breakdown parts | 1 | 191.6 | 73.4 |
The default-viewport (1280) path gives 1 page at 5, 6, 10, 40 as well (article 191.6 mm with parts); the builder's claim of margin 33.8 mm with C=5 is true. Effective limit: 10 lines + 3 hw + 3 sw is 257.7 mm and still 1 page, so the real margin at 6+ lines is at least 26.5 mm (2.4 device rows of 10.85 mm), above the kit's two-row rule on the print.spec path. Builder's "NOT under two rows" sentence in its FOR TUESDAY block is a mis-wording: both numbers it gives are over two rows.

## Red without the fix (my own copy `plant`, restored and `git diff --quiet` rc 0 after)
| Plant | Vitest (ProposalPage.test.tsx) | print.spec api-off |
|---|---|---|
| cap 9 | 6 failed (cap literal, 6/7/10/40 lines, totals) | 3 failed (6, 10, 40 lines: 2 pages) |
| summary row removed (`false &&`) | 4 failed (6, 7, 10, 40 lines) | 3 failed (pointer row missing) |
| cap not applied (`p.lines.map`) | 5 failed | 3 failed (2 pages at 6 lines or 10, 3 at 40) and proposal-buttons 12 and 40 lines fail `toBe(1)` (2 and 3 pages) |
| main's ProposalPage.tsx (base) with the head tests | 7 failed, 33 passed | 3 failed, 3 passed (the 3 and 5 line rows are green by design) |
So the 5 print rows at 6, 10, 40 lines and 7 of the 10 Vitest rows can fail; the 3 rows at 1, 3, 5 lines are guards that pass at base by design (the builder said so).

## Scans (added lines, 123 lines, plus the commit message; each pattern has a planted control that fires)
Names (ban list plus seat names, underscore-aware `(?<![A-Za-z])name(?![a-z])`, planted `x_by_name_y`): 0 in code and in the message; B-number 0; decision-card id 0; GUID/tenant 0; secrets (ghp_, AKIA, BEGIN, eyJ) 0; hosts (http) 0; non-ASCII 0; Cf 0; price-like digit.digit 0 in code (the one hit is the commit footer "5.5"). CodeQL JS pre-scan: `new RegExp(` 0, `eval(` 0, `innerHTML`/`dangerouslySetInnerHTML` 0, `child_process` 0, `.replace(/[` hand-escape 0; the only regex literal is `/and \d+ more lines? \(see full proposal\)/` (one quantifier, no nesting; test code, matched against pdftotext output, no sanitisation role). Added skip/fixme/only/waitForTimeout/eslint-disable/ts-ignore: only the intended conditional `test.skip(<stub marker>, STUB_ON_REASON)` at print.spec.ts:100.

## Findings
| # | Sev | Finding |
|---|---|---|
| F1 | Major (scope; builder-disclosed; decision for the product owner) | The ruling says "cap it so it always fits one page". The cap covers the Devices table only. I measured at head, 703 px, 10 device lines with k hardware rows and k software rows: k=3 257.7 mm, 1 page (7.3 mm left); **k=4 270.9 mm, 2 pages**; k=5 284.2 mm, 2 pages (and 231.2 / 244.5 mm for k=1 / k=2 in the builder's table). At the default viewport path k=4 and k=5 also read 2 pages. So the builder's measurement is confirmed, and "always one page" is true only while hardware plus software rows are below about 4 each. The kit's Q-3 scoped hw/sw out by default, so this is not a defect of the build; it is a gap against the ruling's wording. Pointers: hardware (Configured options) table captions at `web/src/screens/ProposalPage.tsx:137`, rows `:147`; software table `:161`, rows `:173` (printed by `grep -n` at head; Devices cap `:115`, `:127`). Suggested follow-up (not done here): cap or compress hardware and software the same way, or tell the customer the short form is for quotes with few options. |
| F2 | Minor | Linux print not measured (macOS only; comment 39452 on the ticket reports Linux block heights larger than macOS and a 12-line spill there). Margin 33.8 mm (about 3.1 rows) is the buffer. The hosted `web` job's stub-off step runs the 5 new print rows and is the first Linux read. If it shows 2 pages at 6, 10 or 40 lines, lower `RENTAL_SHORT_LINE_CAP` (`ProposalPage.tsx:37`) and the literal `CAP` (`print.spec.ts:81`) and the Vitest literal. |
| F3 | Minor | Long device names or sites eat the margin and can break "one page" even with the cap. My probe (synthetic, wrapped model and site text in every row, 703 px): ~50-character model names, 6 lines: 1 page, margin 12.6 mm (5 lines 19.2 mm); ~120-character model plus a long site, 5 lines: **2 pages (291.3 mm)**, 6 lines 297.9 mm. The 5-line case is the same markup as at base, so the PR did not cause it. |
| F4 | Minor | `web/e2e/proposal-buttons.spec.ts:372` `R1_RENTAL_PAGES` still says `{12:'2/1', 40:'3/2'}` and the log line `B86RENTAL ... r1MacLinux` therefore prints "2/1" next to `pages:1`. Comment-grade label, noted by the builder, left unedited by the one-edit rule. |
| F5 | Note | The builder's "NOT under two rows" line (STATUS FOR TUESDAY, Gate tier) contradicts its own numbers (33.8 mm = 3.11 rows; 26.0 mm = 2.40 rows); I graded it as a mis-wording, so G2 stands on my numbers too. |
| F6 | Note | The 5 new print.spec rows skip in the stub-on CI step by design (the proposal route is not reached there); the proof is the stub-off step only. proposal-buttons.spec.ts stays out of CI (pdftotext). |
| F7 | Note | The one new customer-visible line (`and N more lines (see full proposal)`, singular `and 1 more line (see full proposal)`) is pending the product owner; the code carries the drafted slot (`ProposalPage.tsx:39`). A wording change is one line plus six literal strings in the Vitest and print rows. Nothing is deployed. |

## Claims graded (builder STATUS)
- C=5 chosen by the two-device-row margin property, s=9 on the breakdown shape: not re-derived in full (I measured the post-change side); the post-change numbers it rests on are true (231.2 mm, margin 33.8 mm). The base table (s=9 parts, 12 plain) is not shown by me; base rows at main read 1 page at 3, 5, 7 and 2 at 12, 3 at 40 (true, proposal-buttons).
- Head prints 1 page at 6..40 lines on both print paths with margin 33.8 mm: true (703 px; and 1 page at the default path).
- Vitest 1541/0 with exactly 10 gained names, 0 lost: true.
- print.spec 6/6 in the api-off shape and 1 passed + 5 skipped in the stub shape: true (my whole-job counts 51 passed / 192 passed + 10 skipped).
- Purchase short form byte-identical (OnePager*, one-pager.css untouched; B109ROOM lines equal): true.
- Only 2 removed lines: true.
- Red-first at base: true (7 Vitest rows red and 3 print rows red against main's ProposalPage.tsx, plus 3 plants).
- hw/sw rows uncapped, k=4 pages 2: true (F1).

## NOT RUN
- Hosted CI and CodeQL (they decide; the CodeQL pre-scan is pattern-based only). The dotnet job (no changed path reads it) and the `python` and `package` jobs (Python tests naming the changed paths: 0; `scripts/package.sh` not run, its input is the same build that passed).
- Linux print counts; the builder's whole base-measurement table for counts other than 5, 6, 10, 40 (I read the builder's table for 1-14, 20, 30 and did not re-run those).
- Three-run repeats of each Playwright spec (one run per shape and tree here, all green; the builder reports 3 each).
- No push, no PR, no Jira, no mail, no az, no hosted HTTP except `git ls-remote`/clone/fetch over SSH and `gh -X GET`. Vitest was run as `npx vitest run` (the `npm test` script's command) so the JSON reporter could be added. Both heavy slots used by me were released (holder files moved into the gate folder), no process or listener left in 9870-9879, the measurement spec moved to `_quarantine`, plants undone (`git diff --quiet` rc 0).
