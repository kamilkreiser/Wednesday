GATE B1502: GO WITH FINDINGS @ b46322d on main acd6aec

Tier G2 (independent QA gate), one round. Subject: branch b1502/mps-web-e2e-print @ b46322dd972bf7ed4ce36e46173675c4113a79b3 (8 commits on base 54ed7627, 18 files, all under web/** and .github/workflows/ci.yml). Gate run 2026-11-11 19:00-19:25 AEDT, Node v24.22.2. Own clone and worktrees (head, base, the merged tree, a mutation tree): /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s269/gate1502/ (push URL INVALID-NO-PUSH; nothing pushed, no PR opened, nothing deployed, no Jira write). Logs in `logs/` there.

## Why GO WITH FINDINGS (one line)
Every claim I could reproduce reproduced: on the tree merged with current main lint, tsc, vitest (145 files, 1517 tests, 0 failed; 25 new names, 0 lost), the production build with its bundle check and the two new CI e2e steps (168 passed + 5 in-spec skips; 22 passed) all pass, twice for the e2e; the PriceView move is proven by diff to change no line but `export`, imports and comments; each new vitest row and each new style row is red when its behaviour is removed. What is left is Minors and Info, and a long, honest list of clauses that stay NOT MET (the PR text says each plainly).

## Refs read at source
- `git/ref/heads/b1502/mps-web-e2e-print` = b46322dd972bf7ed4ce36e46173675c4113a79b3 (matches the commission).
- `git/ref/heads/main` = acd6aec03e707a2c6fb30ac9adeccb4230b05764. Base 54ed7627 -> main: 16 files, all `src/MpsCalc.Api/**` and `tests/MpsCalc.Api.Tests/**`; 0 under `web/` or `.github/`.
- `git merge-tree --write-tree origin/main origin/b1502/...` rc 0, tree cc1321e3. I built a merge commit from that tree (d81e28f) and ran the web checks on it; the merged tree differs from main by exactly the 18 branch files.

## Findings

| # | Sev | Ticket | Finding | Evidence |
|---|---|---|---|---|
| 1 | Minor | MPSCALC-121 | **The `queue.current.catch(() => undefined).then(...)` change in FeedbackDialog.tsx has no row that goes red without it.** The two new rows go red only when BOTH changes are removed (2 of 2 red). Remove only the dialog change and both rows stay green (2 of 2 pass), because attachments.ts now turns an unreadable file into a refusal, so the chain never rejects. The behaviour the ticket names (an unreadable file refuses and the form does not wedge) is pinned; the defence-in-depth `.catch`, which covers any other rejection in the add chain (for example the hash step), is not. | `FeedbackDialog.tsx:85`; mutants in `logs/mut-121a.log` (attachments.ts to base: 1 of 2 red), `logs/mut-121b.log` (dialog to base: 0 of 2 red, 2 passed), `logs/mut-121c.log` (both: 2 of 2 red) |
| 2 | Minor | MPSCALC-96 | **The narrowed console assertion in bom.spec lets through any one "Bad Gateway" console message in stub mode, from any request, not only the stub's create.** Stub mode only; every other console error still fails the row (the regex is anchored: `^Failed to load resource: the server responded with a status of #+ \(Bad Gateway\)$`; the spec masks digits to `#` at `bom.spec.ts:311`; the original `toEqual([])` at `:352` stays). The builder named it (FOR TUESDAY item 6). With stub on there is no API behind the proxy, so a 502 is the expected answer to the stub's first ask; a second 502 fails the row (`toBeLessThanOrEqual(1)`). Accepted as written; a tighter form would tie the message to the create request. | `web/e2e/bom.spec.ts:347-352`; the 3 bom rows pass inside the stub e2e run (this gate, twice: rows at `bom.spec.ts:309`, `:355`, `:377`) |
| 3 | Minor | MPSCALC-148 | **A known-red spec is left out of the new CI step by name.** `b100-picker-many.spec.ts` is red at its base (the six-lines row counts 6 rows and the section now has a seventh, the page-estimate row; spec drift, not a product defect). It is listed in `LEFT_OUT` with its reason and the run prints the list, so it is not hidden, but it stays red with no ticket of its own on the branch. Needs a card. | `web/playwright.config.ts:10-19` (`'b100-picker-many.spec.ts'`), builder STATUS BASELINE |
| 4 | Info | MPSCALC-198 | **The two new steps sit inside the required `web` check and are unproven on the hosted runner.** I reproduced both locally with the same commands and the installed Chrome (stub on: rc 0, 168 passed + 5 skipped, 2.6 m; api-off: rc 0, 22 passed, 6 s; second run identical). Whether `channel: 'chrome'` resolves on `ubuntu-latest` is proven only by the PR's own CI. The job name is unchanged, no new `uses:`, no secret, no `permissions:` change. `timeout-minutes` is 40 (was 20) for the whole job. | `ci.yml:48,67-79`; `logs/e2e-merged.log`, `logs/e2e-merged2.log`; `scripts/tests/test_ci_workflow.py` OK (8 tests, 9 action references SHA-pinned) |
| 5 | Info | MPSCALC-135 | Formatting only: in `smoke.spec.ts` the new `else` at line 43 is followed by an unindented statement at line 44. It is correct as written (the else binds to the next statement) and lint passes; a block would read better. Not in CI. | `web/e2e/smoke.spec.ts:42-44` |
| 6 | Info | MPSCALC-130, 135, 251, 297, 369, 57 | Clauses that stay NOT MET after this branch (the PR must say each; its text does): see "Clauses that stay open" below. | builder STATUS RESIDUE; reproduced where possible |
| 7 | Info | MPSCALC-57 | A pre-existing intermittent hang in the four `pdftotext` specs (the PDF is fed to `pdftotext` on stdin; about 1 in 25 prints never returns within the bound; present at base). Those four specs are not in the new CI steps, so it has no effect on the gate. It passed in my one run of all four (40 passed with `print` and `proposal-content`). Suggest a follow-up card (write the PDF to a temp file first). | builder STATUS part 14; `logs/print.log` |

No Blocker or Major: every path is in the lane (0 outside `web/**` and `ci.yml`); no secret (gitleaks over `54ed7627..b46322d`: 8 commits, no leaks); no non-ASCII added line, no person's name, no `test.skip(`/`.only(`/`eslint-disable`/`@ts-ignore`/`waitForTimeout` in any added line; no new product word (the one sentence in the 121 rows exists once in `words.ts`).

## What the builder's hardest items turned out to be

### PriceView.tsx -139 lines -> PriceViewColumns.tsx: behaviour-neutral, proved by diff
I compared every removed line of PriceView.tsx (141, whitespace-stripped) with PriceViewColumns.tsx (script `out/cmp_move.py`, input `out/pv.diff`): 118 are present verbatim. The other 23 differ only in these ways, all read in the diff: (a) 11 import lines (the type import block and two component imports, re-split); (b) `interface Column`/`Card`, `function lineColumns/hardwareColumns/softwareColumns`, `const CARDS`, and `money`, `rate`, `pct` gain the keyword `export`; (c) the `sourcePrice` fallback `'—'` is written `'—'` (the same character); (d) two comment lines lose internal ids. The new file adds only: a 3-line header comment, two import lines, and the `export`-prefixed forms of (b). `PriceView.tsx` keeps `INTERNAL_LABELS` and `StatusChip` through `export { INTERNAL_LABELS, StatusChip }` (line 11) and calls the same `lineColumns`, `hardwareColumns`, `softwareColumns`, `CARDS`. Runtime proof: the 94 related vitest rows and the whole suite pass on the merged tree. Planted fault: appending `import './bom-v5.css';` to pricingHint.ts makes `playwright test --list` fail again (rc 1, `SyntaxError ... bom-v5.css`, 0 tests in 0 files); clean it lists 220 tests in 26 files (`logs/print.log` D).

### MPSCALC-121: attachments.ts / FeedbackDialog.tsx
- `attachments.ts:69-77`: `readBytes` wrapped in try/catch; a read failure pushes the existing `'type'` refusal and `continue`s; no new word.
- Red-first: see Finding 1. Both rows red at base behaviour (2 of 2, `Unable to find an element with the text: Only PNG, JPEG or PDF files can be attached.` and 2 unhandled rejections), green at head.
- The words question the builder raised stands: the existing sentence is shown for an unreadable PNG and does not read true there. Not a gate defect; it is a product-owner words question.

### proposal.css print rules (MPSCALC-130 style half)
- The three new rules sit inside the existing `@media print` block (`proposal.css:109-121`; the block opens at `:109`, the rules are at `:118-120`, the closing brace at `:121`), so screen is untouched by construction. `.pd th { border-bottom: none }` removes only the app's global th border; the document's own `.pd-table th` rule (`:59`) draws none, and `.pd-table td` keeps its own bottom rule (`:60`).
- Red-first: `print-book-styles.spec.ts` on the merged tree: 6 of 6 pass (2 rows x 3 repeats, stub off, mock folder via `MPSCALC_RENTAL_MOCK_DIR`). With `proposal.css` put back to base (5 lines removed) the typical-book row goes red with a long list of `app ["border-box | ..."] vs mock ["content-box | ..."]` differences for the right reason (`style`, `section.pd-cover.pd-page`, `p.pd-screen-head`, `img.pd-logo`, ... each border-box vs content-box). Restored (`git diff --quiet` rc 0).
- Printed-text side: rental-book, proposal-purchase, proposal-buttons, itemised-summaries, proposal-content, print: 40 passed in one run at the merged tree (stub off). The large book still prints 15 pages against the mock's 16 (`B94PAGES {"shape":"large","pages":15,"mockPages":16,...}`), which is the builder's finding and is inside the spec's 10-16 bound.

### ci.yml and playwright.config.ts: do the new steps run what they claim
- The two steps run `npx playwright test` with `MPSCALC_E2E_MODE` stub / api-off and `MPSCALC_E2E_START_WEB=1`; the config starts `npx vite` itself (`playwright.config.ts:37`), reads the port from `MPSCALC_WEB_PORT`, and prints the left-out list with reasons (line 27). A bad mode throws (line 25); no mode set leaves the local default unchanged (listing 220 tests in 26 files).
- Stub step census at the merged tree: 173 tests in 17 files = 168 passed + 5 skipped (the 5 are in-spec skips with printed reasons: b28 x4 live-only rows and the b30 live row, the same as the base census); api-off: 22 passed in 4 files. `bom.spec.ts` and `fleet-line-identity.spec.ts` and `v3-zero-errors.spec.ts` are inside the stub step, so MPSCALC-96, -198 and -251's CI claims are real.
- The ports in my run were 9611/9612 (CI uses 5183 for both, one after the other); `MPSCALC_E2E_BASE_URL` was set to match. Not a difference in what runs.

### MPSCALC-135 clause 4 (the smoke journey in all four legs): NOT MET on stub and no-API, and the rows say so
I reproduced all three legs of the builder's table against an API of my own, built from the merged tree and started on 9696 with an invented store written by the importer's own synthetic books (4 devices):
| Leg | Result |
|---|---|
| API on the synthetic store, stub off | **3 of 3 pass** (`logs/smoke.log` F) |
| same with the Short-form lines removed (mutation tree) | red at `Approved snapshot` not found in the Proposal article (the right reason) |
| dev stub on (`VITE_MPSCALC_API_STUB=1`), no API | **red**: `region "Commercial outcome"` never appears (`logs/smoke2.log`) |
| stub off, no API behind the proxy | **red**: the `New quote` dialog count stays 1 instead of 0 (`logs/smoke2.log`) |
So clause 4 is MET on the third leg only and NOT MET on stub and no-API; `smoke.spec.ts` is left out of CI by name with that reason. The PR must not say the smoke journey is green; it says it is edited, run green once against an API on invented data, and not in CI.

### New vitest rows: red-first (mutations of the production code in a throw-away worktree, restored each time)
| Ticket | Fault planted | New rows | Result |
|---|---|---|---|
| MPSCALC-377 | `quantityAuditModel.ts:100` `r.line.quantity > 0` -> `!== 0` | `(c6)` of QuantityAudit.severalDevices | exactly 1 of 21 red (the new row) |
| MPSCALC-334 | stubApi.ts `scope === 'mine'` -> `!==` (F1) | stubApi.test.ts (69) | 6 red |
| MPSCALC-334 | `stubOutcomes.set(` -> `.get(` (R3) | same | 2 red |
| MPSCALC-334 | `'Administrator'` -> `'Administrators'` (F3) | same | 2 red |
| MPSCALC-334 | duplicate path `heldSummaries().some` negated (D1) | same | 2 red |
| MPSCALC-121 | see Finding 1 | FeedbackDialog.unreadable | 2 red only with both changes undone |
All four stubApi mutants reproduce the builder's counts (6, 2, 2, 2); stubApi.test.ts passes 69 of 69 unmutated.

## What I ran (counts)
- Merged tree (main acd6aec + the branch): `npm ci` rc 0; `npm run lint` rc 0; `tsc -b` rc 0; `npm test` 145 files, **1517 tests, 0 failed**; `VITE_MPSCALC_AUTH=entra npm run build` + `check-bundle.mjs dist` rc 0 (8 files, 1108580 bytes, markers 0/57); `playwright test --list` rc 0, **220 tests in 26 files**.
- Names (vitest JSON, `path :: fullName`): base 54ed7627 **1492 tests**, merged **1517**; **lost 0, gained 25** = 22 stubApi.test.ts + 2 FeedbackDialog.unreadable + 1 QuantityAudit.severalDevices (`out/names.py`).
- e2e as CI runs it, twice: stub 168 passed + 5 skipped (rc 0); api-off 22 passed (rc 0).
- print-book-styles 6/6 at head, red at base CSS; the 40-row print/PDF set green; smoke legs as above; mutants as above.
- `python3 -I scripts/tests/test_ci_workflow.py` OK (8 tests). gitleaks over the 8 commits: no leaks. Property scan of the 651 added lines: non-ASCII 0, names 0, B-numbers 0, banned patterns 0. Every commit: author = committer = the project repo address; each message carries one attribution line.

## What I did NOT run
Hosted CI and CodeQL: NOT RUN. The dotnet job and the python job (other than `test_ci_workflow.py`): NOT RUN (nothing under `web/` or `ci.yml` is read by them; the builder's grep found two doc comments only). `scripts/package.sh`: NOT RUN here (the builder reports rc 0 at head; the web build and bundle check, which it calls, I did run). `b83-feedback-attachments.spec.ts` (needs the real feedback store): NOT RUN. The base-red MPSCALC-96 row `bom.spec.ts:308` before the edit: not re-run (the edit is exercised green, 3 of 3 rows, in each of my two stub runs). The builder's MPSCALC-369 whole-suite loop (25 runs): NOT RUN; I take it as a builder's measurement (see below). MPSCALC-185 and -251 planted-element controls: NOT RUN (evidence parts with no commit). `channel: 'chrome'` on `ubuntu-latest`: NOT RUN.

## Clauses that stay open (the PR text states each)
| Ticket | Clause | State |
|---|---|---|
| MPSCALC-135 | 4: the smoke journey green in all four legs | NOT MET on the dev-stub leg and the no-API leg; MET only on a third leg (API on invented data) which CI does not run. Clauses 1-3 MET |
| MPSCALC-130 | per-page word sets equal the approved mock's on all four variants | NOT MET and open by the coordinator's ruling, pending the product owner's words; the style half is MET. The large book prints 15 pages (the mock 16) |
| MPSCALC-369 | the five named rows pass in 20 whole-suite runs started under load | NOT MET: 19 of 20 counted runs clean among the five rows; evidence only, no change in this PR |
| MPSCALC-251 | 1: a sign-in leg | NOT MET (ruled out); 3: runs in CI | MET for the stub step, unproven on the hosted runner |
| MPSCALC-297 | smoke green at desktop and phone | MET on the invented-data API leg only; not in CI |
| MPSCALC-57 | the PDF-text specs in CI | NOT MET: they stay out (runner `pdftotext` unmeasured) |
| MPSCALC-334 | 4: `updateDraft` for a held-created rental quote answers 502 | NOT built (it is also why the smoke journey cannot go green on the stub leg) |
| MPSCALC-121 | e2e step with a folder drop; the unreadable-file words | not built; words question open |

## Corrections to the builder's record
1. PART 9: "getQuoteFigures 13 with the it.each expansions, recordOutcome 6, duplicateQuote 2, plus one more of figures" does not add as written. The file's own rows are figures 14, recordOutcome 6, duplicateQuote 2 = 22; the 22 itself (names gained in `stubApi.test.ts`) is right.
2. PART 14 "bom.spec" is "not in the census loop" in the builder's text; it is inside the stub CI step (its 3 rows passed there, in both of my runs), so the CI step does cover MPSCALC-96.
3. The `INTERNAL_LABELS` before/after dump (29 labels) is the builder's; I did not repeat it. I proved the move by diff instead (section above), which also covers the cards and the status chip.
4. Everything else I could reproduce matched STATUS to the digit: 145/1517, 220 in 26, 173 = 168 + 5, 22 passed, lost 0 / gained 25, the mutant counts, smoke 3 of 3 / 0 of 3 / 0 of 3 (the stub and no-API legs read red for the reasons stated), `B94PAGES` 15 vs 16.
