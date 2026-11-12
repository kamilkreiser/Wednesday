GO WITH FINDINGS
Gate G2, round 1 of 2, 2026-11-12 13:02-14:25 AEDT. Project MPS Calculator, ticket MPSCALC-110, branch b1536/mps-110-options-cap @ f2ffe2ca08c9d7c5f635a4befb8c87ace0e5ccfe (f2ffe2c) on main 1515a71dc5a5f28eaf6c13ac129cc600f8d10b02 (1515a71). Findings: Blocker 0, Major 0, Minor 4 (F1-F4), Note 4 (F5-F8). No security-shaped issue (web rendering of existing data; no input, URL, regex-from-variable or HTML sink added).

Short answer on "always fits one page": MET for every line and option COUNT (1 page at 3/12/12, 12/3/12, 12/12/3, 40/40/40, 100/100/100; article 236.00 mm of 265 mm, margin 29.0 mm = 2.67 Devices rows, reproduced). NOT MET for very long device or option text (F3), same class as the earlier device-cap gate's long-name finding. Linux page metrics are UNMEASURED: the hosted api-off step runs print.spec.ts on Linux and is the net.

## Refs and merge (measured)
- `git ls-remote origin` at 13:03: branch = f2ffe2ca08c9d7c5f635a4befb8c87ace0e5ccfe (one b1536 ref via `matching-refs`), main = 1515a71dc5a5f28eaf6c13ac129cc600f8d10b02. Head is 1 ahead and 1 behind main (`rev-list --left-right --count`: 1 1); merge-base = 5239020 (the base). The one commit behind is the #187 squash.
- Identity: `git log --format='%h %ae | %ce'` = `f2ffe2c kamil.kreiser@datasec.com.au | kamil.kreiser@datasec.com.au`; equals the project repo's `config --local --get user.email`.
- Changed paths: 4 of 4 inside the lane and inside the answer's file list (web/e2e/print.spec.ts, web/e2e/proposal-buttons.spec.ts, web/src/screens/ProposalPage.test.tsx, web/src/screens/ProposalPage.tsx). +213 -24.
- Overlap: #187 (landed; main moved onto 1515a71) touches docs/API.md, docs/ENGINE.md, docs/api/openapi.json, src/MpsCalc.Api/Quotes/{PricingPolicy,QuoteEndpoints}.cs, three files under tests/MpsCalc.Api.Tests, web/src/api/generated/{SOURCE.txt,openapi.snapshot.json,schema.ts}: overlap with the head 0 (control: #186's file list printed the same 4 paths as this head, so the compare fires). #186 is the earlier device-cap PR (closed). Open PRs: 0 (`pulls?state=open` printed no row; control `pulls/99999` is 404, `pulls?state=all` returns #187, #186, #185, #184). Main's blobs for the 4 paths equal the base's (main did not touch them).
- Merge: in my own clone, `git merge-tree --write-tree 1515a71 f2ffe2c` rc 0, tree dbe390d5. `git diff --name-only 1515a71 <tree>` lists exactly the 4 head paths, and the 4 blobs in the tree equal the head blobs (print.spec 1a13c97, proposal-buttons 853b3f9, ProposalPage.test a1ac99f, ProposalPage cabd332). All "merge" runs below used a local commit-tree of that tree (never pushed; push URL set invalid).
- Purchase short form unchanged: `OnePager.tsx` blob e8dab2ac and `one-pager.css` 8b75cdab are identical at base, main and head. `git diff --name-only main head` matches `OnePager|one-pager|ProposalDocument|RentalDocument|template|styles.css`: 0. `B109ROOM` lines (9 purchase lines, 3 pages each, coverRoomLeftMm 89/83/131/56/50/73/73/68/68) are byte-identical at main and head (diff rc 0; control: 9 lines counted at main).
- Landing: only workflow is `ci.yml` (push to main and pull_request); no deploy workflow. A merge triggers no deploy. Project rule (CLAUDE.md:50): seats push a branch only, the PR is opened and merged once CodeQL is green; squash, head-pinned.

## Closed list of existing lines (the answer's list), graded by program
`git diff -U0 base head | grep '^-[^-]'` printed whole = 24 removed lines:
- ProposalPage.tsx: `RENTAL_SHORT_LINE_CAP = 5` (:37, listed) and the two `.map(` lines (`p.hardware.map` / `p.software.map`, the kit's own allowed removals). In list.
- ProposalPage.test.tsx: removed lines all inside the old 417-482 block (the cap-is-five row, the 1/3/5 row, the one-over row, the 7/10/40 rows, the five model names, the 40-line `toHaveLength(5)`). In list. The import line is untouched; a second import line was added.
- print.spec.ts: `CAP = 5` (:81), the `[3,5,6,10,40]` rows (:84-90) and **the `test(...)` title at :91 ("five lines" -> "three lines")**. The title line is NOT in the list (F1).
- proposal-buttons.spec.ts: `if (lines > 5)` (:392) only. In list.
No other existing line changed.

## CI by program (my clones under fleet/state/s272/g1536; Node v24.22.2; Playwright installed Chrome; ports 9980-9986; API origin 9989 dead)
| Check | main 1515a71 | head f2ffe2c | merge |
|---|---|---|---|
| `npm run lint` | rc 0 | rc 0 | rc 0 |
| vitest (`npx vitest run`, JSON reporter) | 1541 passed, 0 failed, 145 files | run 1: 1550 passed, **1 failed** (PriceReason.test.tsx, F7); run 2: 1551 passed, 0 failed | 1551 passed, 0 failed, 145 files |
| sorted `path :: fullName` lists (`LC_ALL=C comm`) | - | head run 2 vs merge: 0 differ | **lost 6, gained 16** vs main, all in ProposalPage.test.tsx (F6) |
| `VITE_MPSCALC_AUTH=entra npm run build` + `check-bundle.mjs dist` | not run | rc 0; 8 files, 1109460 bytes, markers 0/57 | rc 0; same 1109460 bytes, 0/57 |
| Playwright CI step 1 (MODE=stub, VITE_MPSCALC_API_STUB=1, whole `npx playwright test`) | 192 passed, 10 skipped | 192 passed, 17 skipped | 192 passed, 17 skipped |
| Playwright CI step 2 (MODE=api-off, whole) | 51 passed | 58 passed | 58 passed |
| `proposal-buttons.spec.ts` (local, pdftotext, stub off) | 22 passed | 25 passed | not run |
Skip delta 7 = the 7 new print.spec option rows (they skip with the stub ON by design); api-off +7 = the same 7 rows running. print.spec at head alone (api-off): 13 passed.
Controls: planted failing tests (below) made vitest and Playwright exit rc 1 before I trusted the greens; the same loops print `0` or the item name for a name removed from a copy.
Python job: no test under tests/, scripts/, infra/, tools/, src/ names ProposalPage|ProposalView|SHORT_FORM_BUTTON|print.spec|proposal-buttons|RENTAL_SHORT (0 files; control: `ci\.yml` finds scripts/tests/test_ci_workflow.py and test_sdk_pin.py). I ran the python tests I could on the merge tree (`python3 -I`): test_demo_doc, test_seed, test_seed_hosted, test_seed_purchase, test_ci_workflow, test_sdk_pin rc 0; test_run_demo, test_deploy_pre1, test_entra_all_roles, test_scripts hit my 120 s timeout (rc 124; slow under load or need tools I do not have; none reads a changed path). Repo-wide Cf scan of `git ls-files` at head (704 files read) and merge (706): 7 files, identical set, all pre-existing fixtures (scripts/tests/test_deploy_pre1.py and six files under tests/) and none in the diff (control: planted U+202E reads 1). Added lines: Cf 0.

## Own measurement (throw-away spec, quarantined after; stub OFF; route-intercepted SYNTHETIC proposal with the four breakdown parts; `emulateMedia print`; `page.pdf` A4; pages by `/\/Type\s*\/Page[^s]/g`; article mm = getBoundingClientRect().height / 3.7795, read before page.pdf; margin = 265 - mm)
| lines/hw/sw | rows (dev, hw, sw) | pages | article mm (703 px) | margin mm | pages at 1280 px |
|---|---|---|---|---|---|
| 12/12/12 | 4, 3, 3 | 1 | 236.00 | 29.0 | 1 (204.78 mm) |
| 40/40/40 | 4, 3, 3 | 1 | 236.00 | 29.0 | 1 |
| 100/100/100 | 4, 3, 3 | 1 | 236.00 | 29.0 | 1 |
| 3/12/12 | 3, 3, 3 | 1 | 229.39 | 35.6 | 1 |
| 12/3/12 | 4, 3, 3 | 1 | 236.00 | 29.0 | 1 |
| 12/12/3 | 4, 3, 3 | 1 | 236.00 | 29.0 | 1 |
| 5/50/50 | 4, 3, 3 | 1 | 236.00 | 29.0 | 1 |
| 10/4/4 | 4, 3, 3 | 1 | 236.00 | 29.0 | 1 |
| 4/3/3 (one over every cap) | 4, 3, 3 | 1 | 236.00 | 29.0 | 1 |
| 10/2/2 | 4, 2, 2 | 1 | 222.77 | 42.2 | 1 |
| 3/3/3 | 3, 3, 3 | 1 | 229.39 | 35.6 | 1 |
| 3/1/1 | 3, 1, 1 | 1 | 202.93 | 62.1 | 1 |
| 40/0/0 | 4, 0, 0 | 1 | 166.15 | 98.9 | 1 |
| 0/40/40 | 0, 3, 3 | 1 | 193.67 | 71.3 | 1 |
The builder's figure is reproduced exactly: 236.00 mm, margin 29.0 mm = 2.67 Devices rows (one Devices row 10.85 mm at 703 px), constant above the caps, both print paths. Controls: a planted `<div style="height:300mm">` in the 3/1/1 case reads 2 pages (502.93 mm); two full runs of the grid (44 cells each) are byte-identical; the old behaviour planted on a copy reads 3 pages at 40/40/40 and 2 pages at 10/4/4 (below), so the instrument sees multi-page.
Long text probes (recorded, not asserted): ~50-character option descriptions at 12/12/12 and 40/40/40: 1 page, 247.64 mm, margin 17.4 mm (1.60 rows; matches the builder's figure; below the two-row property). Device names of about 75 characters plus option text of about 70 characters: **2 pages, 260.34 mm** (limit about 258 mm). See F3.

## Summary rows: exact words and the singular/plural boundary (measured on the printed article)
- Devices: `and 1 more line (see full proposal)` at 4 lines; `and 2 more lines ...` at 5; `and 37 more lines ...` at 40 (function `moreRentalLines`, unchanged).
- Options (both tables, `moreRentalOptions`, ProposalPage.tsx:45): 3 options -> `and 1 more option (see full proposal)` (singular, n === 1); 4 -> `and 2 more options (see full proposal)`; 5 -> `and 3 more options`; 12 -> `and 10 more options`; 40 -> `and 38 more options`; 50 -> `and 48 more options`. At 2 options (the cap) and at 1: no summary row. Hardware row `colSpan={4}` (:163) = the 4 header cells; software row `colSpan={6}` (:196) = the 6 header cells (read at head). Independent per table: 3/12/12 shows `and 10 more options` twice and no devices pointer; 12/3/12 shows `and 1 more option` under hardware and `and 10 more options` under software.

## Red without the fix (own copy `plant`, head's tests with ProposalPage.tsx altered; restored and compared with cmp after)
Vitest, ProposalPage.test.tsx (50 tests):
| Plant | failed | reds |
|---|---|---|
| head (control) | 0 | - |
| device cap back to 5 | 7 | the cap literal, one-over, 5/10/40 lines, 40-line totals, and the 40/40/40 row |
| option cap 3 | 6 | cap literal, one-over, 5/10/40 options, 40/40/40 |
| option cap 1 | 7 | those plus the "at 2 options" guard |
| options uncapped (slice and summary removed) | 6 | one-over, 5/10/40 options, independence, 40/40/40 |
| summary rows removed only | 6 | the same six |
| software table left uncapped | 6 | the same six |
| device cap 5 AND options uncapped (= main's behaviour) | 12 | all 6 device rows and 6 option rows |
| main's ProposalPage.tsx plus a stub export so the import resolves | 13 | the same 12 plus the words row (`moreRentalOptions` not the real function) |
print.spec.ts (api-off, 13 tests): device cap 5: 8 fail (3 device-pointer rows and 5 option rows on the Devices row count); option cap 3: 5 fail; option cap 1: 6; options uncapped: 5 fail with **40/40/40 = 3 pages, 3/12/12 and 12/3/12 and 12/12/3 = 2 pages**; summary removed: 5; software uncapped: 5 fail (40/40/40, 3/12/12 and 12/3/12 = 2 pages); device 5 + options uncapped: 9 fail with 40/40/40 = 3 pages and 10/4/4 = 2 pages. The "10/2/2" and "3/1/1" rows and the first 3 rows are guards that pass before the fix by design (the 10/2/2 row fails with the device cap at 5).
proposal-buttons.spec.ts, old behaviour planted: 2 of 25 fail (10/4/4 prints 2 pages, 40/40/40 prints 3 pages); the 40/2/2 row stays green (guard).
So every new Vitest row except the three at-the-cap guards, and the page-count assertions of the 40/40/40, 3/12/12, 12/3/12, 12/12/3 and 10/4/4 rows, can fail.

## Scans (201 added lines plus the commit message; every pattern has a planted control that fires)
Names (ban list Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite plus Tuesday, Wednesday, Friday, Sonnet, Opus, Claude; underscore-aware `(?<![A-Za-z])name(?![a-z])`, planted `x_by_name_y`): 0 in code; in the commit message the only hits are the attribution footer. B-number 0, decision-card id 0, GUID 0, secrets (ghp_, AKIA, BEGIN, eyJ) 0, hosts (http, azurewebsites) 0, non-ASCII 0, Cf 0, digit-dot-digit in code 0. CodeQL JS pre-scan: `new RegExp(` 0, `eval(` 0, `innerHTML`/`dangerouslySetInnerHTML` 0, `child_process`/exec/spawn 0, `.replace(/[` hand-escape 0. The only regex literals are the files' own `/\/Type\s*\/Page[^s]/g` and two bounded `/and \d+ more (?:lines?|options?) \(see full proposal\)/` forms (test code, matched against pdftotext output). skip/fixme/only/waitForTimeout/eslint-disable/ts-ignore: 0 except the two intended conditional `test.skip(<stub marker>, STUB_ON_REASON)` (print.spec.ts and proposal-buttons.spec.ts). New user-visible strings: exactly the singular/plural pair of `moreRentalOptions`.

## Findings
| # | Sev | Finding |
|---|---|---|
| F1 | Minor | One existing line changed outside the answer's closed list: `web/e2e/print.spec.ts:91`, the `test(...)` title of the loop, "five lines" -> "three lines". Builder disclosed it (RESIDUE) and without it the title would be false; the property (only lines that state the old cap) holds, it is not a behaviour change. Not blocking. |
| F2 | Minor | Stale comments now state the old rule: `ProposalPage.tsx:33-36` ("five lines plus the pointer row leave over two device rows of room"; "Only the Devices table is capped; ... the options and the software still cover the whole quote", false after this PR); `print.spec.ts:75-78` ("at most five device lines"); the comment above the old block in `ProposalPage.test.tsx` (:414-416, "Only the Devices table is capped"); `proposal-buttons.spec.ts:372` stale `R1_RENTAL_PAGES` label (known, left by rule). A follow-up can refresh them; they were outside the closed list. |
| F3 | Minor | "Always one page" holds for any COUNT but not for long text. Own probes at 703 px, 12 or 40 lines/options: ~50-character option text 1 page, 247.64 mm, margin 17.4 mm (1.6 rows, below the two-row margin, still 1 page); ~75-character device names plus ~70-character option text **2 pages, 260.34 mm**. Same class as the earlier device-cap gate's long-name finding; the kit records it as out of scope. |
| F4 | Minor | Linux print UNMEASURED (macOS only). Arithmetic headroom 29.0 / 236.00 = 12.3%. The only Linux datum in the records is an older, different shape and was larger (+18.5%, RELAYED by the builder from the ticket), which would exceed this headroom. The hosted web job's api-off step runs print.spec.ts (13 rows, 12 of them this feature's) on Linux and is the first read; if it shows 2 pages, lower `RENTAL_SHORT_OPTION_CAP` (ProposalPage.tsx:43) or `RENTAL_SHORT_LINE_CAP` (:37) and the literals in the Vitest and print rows. |
| F5 | Note | The three new `proposal-buttons.spec.ts` rows (:409-) assert the page count only (`toBe(1)`); the summary words found by pdftotext are logged, not asserted (as the kit specified; the words are asserted by the Vitest literals and the print.spec rows). That spec stays out of CI (pdftotext). |
| F6 | Note | The kit's "vitest names lost 0" cannot hold: lost 6, gained 16 vs main, all in ProposalPage.test.tsx. The 6 lost are the retitled device-cap rows inside the closed list (cap five, 5 line(s) or fewer, one over: five data rows, 7/10/40 lines: first five); the 16 gained are their 6 re-expressed twins plus 10 new rows. No other file lost or gained a name (comm over 1551 names). |
| F7 | Note | Head's first full vitest run (13:42, load1 about 38, parallel with my Playwright runs) failed one test, `src/screens/bom/PriceReason.test.tsx` "G-9 ... reason box is sent with the save" ("Unable to find an element with the text: DEMO-A3C-50"). The file is untouched by the diff and not related to the proposal. It passed 3 of 3 alone at head and 3 of 3 at main, and the whole suite passed on the rerun at head (1551/0) and on the merge (1551/0). A timing flake under load; hosted CI is the arbiter. |
| F8 | Note | At exactly 3 options the pointer row ("and 1 more option") replaces one option and occupies the same height as the row it hides (the builder noted this); a product point for the product owner, not a defect. |

## Claims graded (builder STATUS)
- 236.00 mm, margin 29.0 mm = 2.67 rows, constant above caps, 1 page on both print paths: true (my table).
- Red-first: Vitest 14 red at base; print/buttons rows red: true in kind (my plants: 12-13 Vitest reds; print.spec 8; buttons 2). Builder's count "14 of 50" not re-run in that exact form (I planted on head's code; counts differ by plant).
- Vitest 1551 passed, 0 failed, lint, build (1109460 bytes, 0/57): true. package.sh rc 0: not re-run (NOT RUN).
- "lost 6, gained 16": true.
- Stub-on skip 12 new/re-expressed rows, api-off 13 passed: true (stub step: 17 skipped vs main 10 = +7 new rows; the 5 re-expressed rows were already skipped).
- Purchase short form byte-identical, B109ROOM identical: true.
- Edits of existing lines beyond the list: one (print.spec.ts:91): true (F1).
- "No other file changed": true (4 paths).
- 40/40/40 reads 3 pages at base, 10/4/4 reads 2: true (my old-behaviour plant: 3 and 2 pages).
- Stale-comment list in RESIDUE: true, plus ProposalPage.test.tsx :414-416 (F2).

## NOT RUN
- Hosted CI and CodeQL (they decide; the CodeQL pre-scan is pattern-based only). Linux print counts (UNMEASURED). `dotnet` job (no changed path reads it), `bash scripts/package.sh` (needs the pinned dotnet SDK; the builder reports rc 0; the bundle check I ran covers the SPA marker scan), the infra/bicep python tests (no bicep) and four slower python tests that timed out at 120 s (none reads a changed path).
- A fresh main build (the builder's base 1109118 bytes is RELAYED; head and merge both read 1109460).
- Three-run repeats of each Playwright spec (one run per tree and mode here; the builder reports three; my measurement grid ran twice, identical).
- No push, no PR, no Jira, no mail, no az, no hosted HTTP except `git clone`/`ls-remote` over SSH and `gh api -X GET`. Load waits: npm ci waited from 13:04 to 13:40 for the load gate (my first fixed 2 x 120 s reads kept straddling load spikes between 5 and 38; I switched to rolling reads every 30 s, same rule: load1 under 24 now and 120 s earlier, not independent reads); the vitest and build jobs then waited 0 to 16 minutes; both heavy slots I used were released (holders moved to `logs/holder-*.txt`), no process or listener of mine is left, ports 9980-9989 free.

## FOR TUESDAY
- **Landing:** GO WITH FINDINGS; findings are Minor and Note. Open the PR from `b1536/mps-110-options-cap` (files in this folder), watch hosted CI (web job: the api-off step is the first Linux read of print.spec.ts; the stub-on step skips the 7 new rows) and CodeQL, then land with `landing.txt` (head-pinned squash). Main is 1 ahead of the branch point but disjoint (the merge is clean and equals main plus the head blobs).
- **WORD PACK (as built, for the product owner before any deploy; the code carries the slot, `WORDS: PENDING APPROVAL`):**
  - Plural, both option tables: `and N more options (see full proposal)` (N = the options NOT shown in that table).
  - Singular, both option tables: `and 1 more option (see full proposal)`.
  - Devices table (existing words, now after THREE lines instead of five): `and N more lines (see full proposal)` / `and 1 more line (see full proposal)`.
  - Where they print: the last row of "Configured options (included in the base charge)" (after 2 options, only when there are 3 or more) and the last row of "Software" (same). Function `moreRentalOptions` at `web/src/screens/ProposalPage.tsx:45`.
  - Offered alternative (not built): `and N more hardware options (see full proposal)` under the hardware table and `and N more software products (see full proposal)` under the Software table (singulars `and 1 more hardware option ...` / `and 1 more software product ...`). Changing to it needs two functions, four literal strings in ProposalPage.test.tsx and six in print.spec.ts, and a re-measure at the longer words.
  - He should also hear: the device cap went from five lines to three (Tuesday's design call under his two rulings); a quote with 3 options in a table shows 2 and a pointer for the third; very long names or descriptions can still push the page to two.
- **Fallback if Linux spills:** lower a cap (F4); the measured alternative from the builder is device cap 5 with one option per table (244.47 mm, margin 20.5 mm).
- **Commit footer:** the squash body ends with the Opus footer required by the gate standard (the builder's commit carries the Sonnet 5.5 footer). Change it if the PR convention is the other.
