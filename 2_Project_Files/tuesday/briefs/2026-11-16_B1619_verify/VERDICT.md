GATE B1619: GO WITH FINDINGS @ 3bcdd21 on main 5e80009

Tier G2 (dev stub and tests only). Gate run 2026-11-16 15:40 to 16:20 AEDT by an independent QA seat, own clone and own instruments; the builder's numbers were not used.

## Refs and merge
- `git ls-remote` of `b1617/mps-lane-ms-stub-duplicate-and-update-pins` = 3bcdd21cf9c10067d88687b41ed371daa7b578c0 = the READY sha. Main re-read twice (15:40 and 16:15) = 5e80009525138879031c4b07a18436242dadf46c (no move).
- 3 commits on main; changed paths 2 of 2 inside the lane: `web/src/api/stub/purchaseQuotes.ts`, `web/src/api/stub/stubApi.test.ts` (`stubApi.ts` untouched). Added lines 293.
- Open work on the same paths: none. Highest PR head ref on origin is now 200 (builder saw 199); PR 200 changes only `scripts/tests/test_sdk_pin.py` and `src/MpsCalc.Api/MpsCalc.Api.csproj` (another lane): overlap 0. Open-PR state itself was not read (no hosted HTTP); read by `ls-remote` refs and a fetch of the PR head.
- `git merge-tree --write-tree main head` rc 0, tree c57abd4de84af006fcef77f805a6ea0a60350f56 = the head tree exactly (0 differing files). So merge = head blobs on main.
- All commit author and committer addresses equal each other (the repo's own); each message ends with one attribution line; `git diff --check` clean.

## Instruments and counts (node v26.13.0 on the box; CI uses node 24: NOT run on 24)
| Check | main | head (= merge tree) |
|---|---|---|
| `npx vitest run` whole web | 146 files, 1580 tests, 0 failed | 146 files, 1610 tests, 0 failed |
| test names by program (sorted, `LC_ALL=C comm`) | | 0 lost, 30 gained (13 + 1 + 16, all in the lane's test file; listed in the work folder) |
| `npx eslint .` | rc 0 | rc 0 |
| `npx tsc -b` | rc 0 | rc 0 |
| `npx playwright test`, mode stub (MPSCALC_E2E_MODE=stub, VITE_MPSCALC_API_STUB=1, port 5183, as ci.yml) | not run | 253 passed, 17 skipped (the specs the config names as left out for the mode), 0 failed, rc 0 |
| `npx playwright test`, mode api-off (as ci.yml) | not run | 157 passed, 0 failed, rc 0 |
| `VITE_MPSCALC_AUTH=entra npm run build` then `node scripts/check-bundle.mjs dist` | not run | rc 0 and rc 0; `dist: 8 files, 1109639 bytes; markers found 0/57`; no `requireCopyable` or `INTERNAL_INPUT_FORBIDDEN` text in dist (control: the word `function` is found in 2 files) |
| CodeQL CLI 2.27.4, javascript-code-scanning (87 rules, pack 2.5.0), database over `web/src` at head | not run | 0 results; planted control file fires 2 (`js/incomplete-sanitization`, `js/xss`) |
| gitleaks | | range main..head: 3 commits, no leaks, rc 0; random `ghp_` canary rc 1 |
Playwright was run at the head only (the merge tree is the head tree). No spec reaches the changed code (the one duplicate spec uses the route mock), and the run is green, so a head-red-main-green case cannot arise. The config prints the three specs it leaves out (smoke, feedback attachments, print book styles) as in CI.

## Red without the fix (my copy: main source plus the head test file; lane test files 130 tests)
17 red, 113 green, all red rows new: the 5 Seller refusal rows (target GP, manual item, manual line, sell override, fixed click rate), the 2 order rows, 10 Part C rows (101 units, 50 emoji and a letter, C0, DEL, C1, target-GP-with-long-reference, derived 96, 100, 94+emoji, 93+emoji). First failure of each refusal row: "expected undefined to be an instance of ApiError" (the copy was not refused); of the derived rows, a wrong reference value. The 8 moved rows, the 5 analyst rows, the hidden-only Seller row, the accepted-side rows and the Part B row are green at main by design (Part B is a pin on code that is already right).

## My own mutants (planted in a separate worktree, restored and `git diff --quiet` each time)
| Mutant | Red rows | Result |
|---|---|---|
| target-GP check off | 2 (its row, the target-GP-and-manual order row) | killed |
| manual items and lines check off | 3 | killed |
| manual items only off / manual lines only off | 2 / 1 (each its own row) | killed |
| sell-override half off | 1 | killed |
| fixed-rate half off | 1 | killed |
| manual and price checks swapped | 1 (the order row) | killed |
| check applied to every caller | 13 (8 moved rows, 5 analyst rows) | killed |
| Part B: update answer built from the stored draft (`stubApi.ts` answer without `draftForCaller`) | 1 (the new row, first failure on `rebatePercent`) | killed; every other of 130 rows green |
| Part B: `draftForCaller` stops omitting `supplies` | 2 (the new row; the hidden-only Seller row) | killed |
| length bound 101 | 7 | killed |
| surrogate step removed | 1 | killed |
| control check removed | 3 | killed |
| DEL (127) excluded | 1 | killed |
| `>=` instead of `>` on the length | 2 (the exactly-100 rows) | killed |
| reference check moved after the draft check | 1 (order row) | killed |
| lower control bound 31 instead of 32 (code 31 not refused) | 0 | SURVIVED |
| upper C1 bound 158 instead of 159 (code 159 not refused) | 0 | SURVIVED |
| target-GP test `!== undefined` only (a null target accepted as set) | 0 | SURVIVED |

## Findings
| # | Severity | Finding |
|---|---|---|
| 1 | Minor | The control-character rows pin one value per range (code 1, 127, 0x85). The boundaries code 31 and code 159 are not pinned: two mutants of the loop bounds survive. The source is correct (it matches `char.IsControl`: 0-31, 127-159); only the pin is thin. Not a ticket requirement (the ticket asks for a C0 and a C1 value). |
| 2 | Minor | No row stores an explicit null target GP, so a mutant that treats null as set survives. The source is right (the server's `is not null` also treats null as absent); pin gap only. |
| 3 | Minor | The three refusal titles now exist twice in `purchaseQuotes.ts` (`guarded` and `requireCopyable`), verbatim. A change to one needs the other. The builder reported it; the kit forbade the edit that would share them. |
| 4 | Minor | Gate-process deviation, not a product finding: the heavy-run gate (load1 under 7) was not met. Reads: 6.85 and 9.82 at the two whole-suite runs, 6.76 at the stub-mode playwright start (met), 9.61 at the api-off start after the 15-minute wait (waited from 15:55 to 16:10; other seats kept the box at 8 to 15), 9.4 at the build. All runs were green and no result looks load-sensitive. |
| 5 | Observation | The builder's claim set graded below; none contradicted. |

No Blocker. No Major: merge clean, no claim contradicted, no vacuous new row (every refusal row first reads the stored draft for a marker, so a refusal cannot pass vacuously; each is red at main), no path outside the lane, no name, secret, id, host or Cf character in added lines or messages, no eslint-disable, no control-character regex literal (a `charCodeAt` loop), no `new RegExp`, no sensitive-name write, no new refusal code or sentence (the 400 title is the server's own plus " (stub)", as the kit's ruling), no deploy: ci.yml has no deploy job and no CodeQL job (the org default setup runs CodeQL on the PR); the merge triggers only the CI jobs, none of which publishes anything.

## Builder claims graded
- 1580 -> 1610 tests, 0 lost: TRUE (my run; 30 gained, 0 lost by name).
- 7 + 3 mutants killed: TRUE (all killed again by my own set, plus the extra ones above).
- Part B red under the stored-draft answer: TRUE (exactly 1 red of 130 lane rows; whole suite not repeated under the mutant).
- Files exactly the two named: TRUE.
- entra build and bundle check rc 0, 0/57: TRUE. CodeQL pre-scan 0 results: TRUE (mine, over `web/src`). gitleaks rc 0: TRUE.
- The 8 moved rows keep their assertions: TRUE by diff reading; one assertion (the Seller's copy answer holds no `rebatePercent`) moved to the hidden-only Seller row, which also reads `supplies`.
- Removed lines per numstat: Part A 5 + 8 = 13, Part B 0, Part C 5: TRUE.

## FOR TUESDAY items 1 to 5 (observations only; none is made worse by this diff)
1. `draftForCaller` does not omit `assumptions.targetGrossMargin`: TRUE at source (`purchaseQuotes.ts` lines 44-53). What the server returns on a read: not shown.
2. `guarded` has no target-GP check, so a stub update by a Seller is not refused one: TRUE at source. The server's PATCH path: not shown.
3. The stub trims a typed reference and the server does not (`QuoteEndpoints.cs` line 542 uses the request value as given when not blank; the length and control checks read it untrimmed): TRUE at source; whether request binding trims: not shown.
4. A whitespace-only source reference: server `CopyRef` returns none; the stub's derived reference would be the spaces plus `-COPY`: TRUE at source (not run).
5. The server refuses a present-but-empty `manualItems` list, the stub copies it, and the docstring says so: TRUE at source.

## NOT RUN
- node 24 (CI's version): every run here is node 26.13.0.
- Playwright at main (not needed: no red at head), and not at a separate merge checkout (merge tree = head tree).
- `scripts/package.sh`, the dotnet and python CI jobs (no stub source is read by them; the builder's grep and the kit's census say 0 files; I did not repeat the grep over those folders).
- Hosted CI and hosted CodeQL (only the CLI pre-run over `web/src` was done; C# and Python not applicable to this diff).
- Open-PR list by HTTP (read by refs only).
- Whole-suite run under each mutant (lane files only, 130 tests, except as stated).
