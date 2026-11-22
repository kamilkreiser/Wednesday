GATE B1903: GO WITH FINDINGS @ e0dcea6 on main d8e6d05

Tier G1, one Opus reader (in-session), 2026-11-22 evening.
- Head: e0dcea6814b9e024aacf3ed9b09dbed73a4e88c5.
- Base: ec281cfb35a1356d59e23e1c69e8eab1e1852f2e.
- Main: d8e6d0506035961a4e901a2031a9a432414962d4.

Every number below was printed by a program in this gate's own scratch copies:
- a `gh api -X GET` tarball of each of the three shas;
- a MERGE tree: main with the kit's two frozen scripts applied.

Runs used node v24.22.2 and npm 11.19.1 from the kit's path, `TZ=UTC`, and the installed Chrome. The seat's STATUS was read as a claim, and none of its numbers was copied.

Rules kept:
- No write to the project, Jira or GitHub. No `cd`. No `az`, no deploy, no message.
- The project's `.tools/.heavy-lock-*` was NOT taken, because taking it is a write in the project tree. Heavy jobs ran one at a time with load1 between 3.3 and 10.2 (under 24).
- The pricebook store was never opened.

## Reads
- **The kit.** The stamped kit B1901 was read whole in three pages. S5 holds Tuesday's answer to Q1: the change is built and gated G1 with the rendered pages.
- **The seat's STATUS.** It reads READY e0dcea68.
- **Origin.**
  - main is d8e6d050, which is PR 227 (merged 07:27Z); `compare ec281cfb...d8e6d050` names one file, `web/src/screens/QuoteScreen.autosave.test.tsx`.
  - The branch ref is ONE row at e0dcea68.
  - The head commit has one parent (ec281cfb). Its author and committer are the repo's Datasec address.
  - `compare d8e6d050...e0dcea68` reads ahead 1, behind 1, with exactly the four lane paths.
  - Open PRs: 0. PRs with this head branch: 0. Open code-scanning alerts: 0.
- **Jira by GET** (credentials loaded in-process from the project `.env`, never printed):
  - 427: Backlog, updated 2026-11-20T17:53:47, 0 comments, 0 links.
  - 428: Backlog, updated 2026-11-20T17:54:29, 0 comments, 0 links.
  - JQL `project = MPSCALC AND ( key in (...) )` returns 2 rows. Control: MPSCALC-361 reads Done.

## Rule 1: the diff equals the frozen text (MET)
- **Frozen scripts.** The kit's `apply_edits_427.py` and `apply_edits_428.py` were extracted from the kit BY PROGRAM and applied to the base tarball. `diff -r` of that tree against the head tarball returns rc 0, so the two are byte-identical.
- **Changed paths.** A whole-tree compare of base and head shows exactly four paths changed: three modified files and one new spec.
- **The four blobs at head equal the kit's:**

| File | Blob |
|---|---|
| `proposal.css` | e717857f9359a8cacc682718e7d5d878d18fdad3 |
| `playwright.config.ts` | 9d608eef16a7d1df594d864eaae8015c9fe55967 |
| `proposal-long-code.spec.ts` | aed713b5a0cb90c92e3860d4ad2db9cac6c87e1d |
| `unpriced.test.tsx` | f2731084e7de4db7980207fb70aca26b696afeca |

- **Numstat** matches the kit: 1/1 for the css, 1/1 for the config, 91/18 for the test file, and 78 lines for the new spec.
- **The four files on main.** Main's copies of the four lane files are still the base blobs, so the frozen scripts apply cleanly to main. The MERGE tree differs from head only by PR 227's test file.
- **No word of any document.**
  - The css diff is the one line `+ overflow-wrap: anywhere;` and adds no string.
  - The config diff adds one file name to `STUB_OFF_ONLY`.
  - `ProposalDocument.tsx`, `OnePager.tsx`, `one-pager.css` and `ProposalPage.tsx` are untouched.
- **No priced-document byte.** Nothing on the priced path changes. The priced S4 print is equal before and after the rule (Rule 2).
- **No `pdftotext` call** in any committed file. The census test passes as part of the whole run.
  - TEXT NOTE: the new spec holds the WORD once, in its header comment at line 11 ("no pdftotext is used"). This is the kit's frozen text and is not a call; see F4.
- **Scans.** `scans1901.py` reports:
  - 171 added lines;
  - 0 non-ASCII lines (control 1), 0 Cf characters (control 1), 0 GUIDs (control 1);
  - names: 12 quiet, 12 controls fired;
  - 0 tabs; the longest added line is 412 characters.
- **Banned constructs.** The spec holds no `eslint-disable`, `.only`, `waitForTimeout`, screenshot, video or trace.
- **Existing cells kept.** No existing cell or assertion of `unpriced.test.tsx` was removed.
  - The removed lines are the old `replaceAtStarts`, the reduce, the two scan lines and the old header line.
  - Indented `it(` lines go from 79 to 85, and `expect(` calls from 187 to 200.
  - `replaceAtStarts` now has 0 references in `web/src`.

## Rule 2: the re-runs (all as the kit says)

| Run | Head e0dcea68 | MERGE (d8e6d050 + lane) | Base ec281cfb |
|---|---|---|---|
| `npm ci --prefer-offline` (head copy; others link its node_modules; the three lockfiles are byte-equal) | rc 0, 0 vulnerabilities | linked | linked |
| `vitest run src/proposal/unpriced.test.tsx` | `Tests  94 passed (94)` | `Tests  94 passed (94)` | `Tests  88 passed (88)` |
| same file, `-t 'MPSCALC-428'` | `Tests  6 passed \| 88 skipped (94)` | not run | not run |
| whole `vitest run` | `Test Files 149 passed (149)`, `Tests 1740 passed (1740)`, rc 0 | `Test Files 149 passed (149)`, `Tests 1742 passed (1742)`, rc 0 (1740 + PR 227's two cells) | not run (the seat reports 1734) |
| `npx eslint .` | rc 0, no output | rc 0, no output | not run |
| `npx tsc -b` | rc 0, no output | rc 0, no output | not run |
| `playwright test --list` api-off | not run | 1 line naming long-code, `Total: 162 tests in 9 files` | not run |
| `playwright test --list` stub | not run | 0 lines naming long-code, `Total: 277 tests in 19 files` | not run |
| api-off step as CI runs it, port 9983 | not run | `162 passed (2.5m)`, rc 0; the spec's own lines read short and long both `{"pages":12,"overflow":0,"columns":[297,297]}` | not run |

Listeners on 9980-9989 were 0 before and after every browser run.

`red428.py` (the kit's block, extracted by program) was run with base = the base tarball's web folder and head = the head tarball's. All 6 labels read MATCH, `labels 6 | DIFF 0`:
- base0: 88 passed (88).
- head0: 94 passed (94).
- cells-only: 4 failed (N1, N2, N3, N4), 90 passed.
- m-cascade: 1 failed (N1).
- m-forge: 3 failed (N2, N3, N4).
- m-marks: 1 failed (N5).

`red427.py` was run against the head web folder on PORT 9983. All 5 labels read MATCH, `labels 5 | DIFF 0`, and listeners were 0 after:
- head0: passed. Short and long both `{'pages': 12, 'overflow': 0, 'columns': [297, 297]}`.
- no-rule: failed. Short 12 pages, [297, 297]; long `{'pages': 13, 'overflow': 0, 'columns': [469, 125]}`.
- break-word: failed. Same figures as no-rule.
- s4-before: passed, 13 pages.
- s4-after: passed, 13 pages.

`compare427.py` (the gate's own PDFs):

| Pair compared | PDF | Pages | Text | Pictures |
|---|---|---|---|---|
| no-rule vs head0 | long-code-long | 13 vs 12 | DIFFERENT | DIFFERENT |
| no-rule vs head0 | long-code-short | 12 vs 12 | EQUAL | EQUAL |
| S4 before vs after | proposal-purchase-S4-synthetic | 13 vs 13 | EQUAL | EQUAL |
| no-rule vs break-word | long-code-long | 13 vs 13 | EQUAL | EQUAL |

The last row shows `break-word` is a no-op here.

`pdfbox.py`: the median word height is 9.493 pt in all four long-code and short-code PDFs (13, 12, 12 and 12 pages).

**Why the long-code text differs, and why no word changed.** A word-multiset diff of the two long-code PDFs explains the "text DIFFERENT":
- 41 tokens appear only before the rule. They are hyphenated words that `pdftotext` joins when the 125 px column breaks them at a line end (`large-format`, `48-month` and the synthetic codes), plus the running header and footer of the extra 13th page.
- 14 tokens appear only after the rule. They are those same words unbroken, and the 60-character synthetic code wrapped into two pieces.

No word changed.

**The rendered pages** (the seat's, read-only, viewed by this gate): `<project>/.tools/b1901-m175/evidence/before_no-rule_long-code-long-p3-03.png` and `after_head0_long-code-long-p3-03.png`. They agree with Tuesday's description:
- Before: Stream A spans about 3/4 of the width, and the right column is a strip that wraps every few words.
- After: two equal columns, with the code wrapped over two lines inside Stream A's card.

**NOT RUN by this gate:**
- The stub-mode Playwright step (the seat reports 260 passed, 17 skipped, 0 failed, equal to its baseline).
- `VITE_MPSCALC_AUTH=entra npm run build` with `check-bundle.mjs` (the seat reports rc 0).
- `npm audit` (nobody ran it; no package file changed).
- The base whole run (the seat reports 1734).

Hosted CI runs all of these on the PR.

## Rule 3: acceptance, line by line

**MPSCALC-427**

1. "A part code of 60 characters with no break in it, in the first stream card of the seven-package test proposal, prints the unpriced full proposal with the same page count ... as the same proposal with a short code, shown by a PDF printed in Chrome and read back": **MET.**
   - The spec's `LONG_CODE` is 60 characters (asserted at spec line 67) and sits on the first line of package 1 of 7.
   - The spec prints with `page.pdf` in Chrome (`channel: 'chrome'`) and reads the page count back from the PDF's page objects.
   - red427 head0 gives 12 = 12. On the merge's api-off run the long and short prints each read 12 pages. no-rule gives 13 (red).
2. "... and the same text size": **MET for the Chrome `page.pdf` print, as EVIDENCE, not as an assertion.**
   - pdfbox gives a median word height of 9.493 pt in all four PDFs.
   - The committed check pins the page count and the column widths, which are the cause, but does not assert text size. This is Tuesday's Q4 choice.
   - The review's `window.print` path is UNMEASURED, and this print path never scaled down even without the rule. "Same text size" is therefore met by measurement here but not guarded by the committed check (F1).
3. "the check is committed or its method is written down with its figures": **MET.** The spec is committed. The figures (12 pages, 297/297; without the rule 13 pages, 469/125) are in the commit body and the squash body.
4. "the real catalogue code lengths are measured first and printed (lengths only, no price)": **MET on the seat's record (RELAYED, not re-run: this gate never opens the pricebook store).**
   - The seat's STATUS records its LENGTHS section, the control on a synthetic file and then the one real read, before BASELINE and before THE EDITS. The figures are 1878 values, 6 to 8 characters (6:1734 7:77 8:67), with `reference.json` never opened.
   - The figures, count 1878 and length 6 to 8, are in the commit body.
   - Order evidence is the STATUS section order only; there are no timestamps per step.
5. "the three words, every priced document and every other word are unchanged": **MET.**
   - No product source file other than one css property changed (Rule 1).
   - The priced S4 PDF before and after has EQUAL text and EQUAL pictures.
   - The short-code PDF before and after has EQUAL text and EQUAL pictures.
   - The long-code word diff shows only layout artefacts.
6. "the existing checks stay green": **MET** for what this gate ran: vitest 1740 and 1742, eslint, tsc, and api-off 162. The stub step and the build were NOT RUN here (seat's claim above). Hosted CI decides.

**MPSCALC-428**

1. "A cell for the cascade turns red under the present function and green under the fix": **MET.** cells-only (the present function) turns N1 red; m-cascade turns N1 red; head0 is green.
2. "a cell for U+0001 in a description, in a narrative field and in an attribute value likewise": **MET.** N2, N3 and N4 are red in cells-only and in m-forge, and green at head0.
3. "a cell for a figure split across two text nodes, with no code involved, turns red under the change that keeps the marks": **MET.** m-marks turns N5 red, and only N5.
4. "the real documents stay green over all the fixtures": **MET.**
   - head0 passes 94/94, including the 88 pre-existing cells (none removed; Rule 1).
   - N1, N2 and N3 each run through both real documents (the `DOCS` loop).
5. "the first limit's text matches what the check does": **MET.** E3 adds one sentence naming both behaviours, and the code at head does exactly that: `noMark` on attributes and text nodes, and `stripCodes` deciding the starts on the unstripped text.
6. "the count of cells is printed before and after": **MET.** 88 before and 94 after, printed in red428's base0 and head0 lines and in the commit body.
7. "no source byte of the two documents changes and no word changes": **MET.** `ProposalDocument.tsx` and `OnePager.tsx` are byte-equal at base and head.

## Rule 4: outside the frame (what the rule is handed that is not the tested shape)

1. **The one-pager's detail cell, `OnePager.tsx:246` (`td.pd-one-detail`): NOT COVERED. This is a NAMED LIMIT and is out of the lane.**
   - The rule is `.pd-card .pd-bullets li` and never reaches it.
   - `one-pager.css:29` sets `table-layout: fixed` on that table and has no wrap rule. A long code there would overflow its cell visually; it would not widen the column. This is DERIVED from the CSS and UNMEASURED.
   - The one-pager also prints a code in its credit label (`OnePager.tsx:368`).
   - This is a records line and a candidate ticket.
2. **A priced full proposal with a long code: COVERED.**
   - The priced path prints no part code. `detail(x, !priced)` at `ProposalDocument.tsx:345` and `:398`, and `priced ? description : partCoded(...)` at `:360`, `:419` and `:467`.
   - So the rule never receives a code in a priced document. It does receive priced card text: the outcome cards at `:329` and the stream cards.
   - The priced S4 print is byte-equal in text and page images with and without the rule (MEASURED).
3. **A code with a hyphen: COVERED by the rule, NOT pinned by a committed cell. This is a NAMED LIMIT.** This gate measured it in scratch copies of the spec, with `LONG_CODE` swapped and four one-spec runs on port 9983, 0 listeners after each:
   - `SYN-` followed by a 56-character segment: without the rule, 13 pages and columns [437, 157] (red, the same defect); with the rule, 12 pages and [297, 297] (green).
   - A hyphen every 10 characters: 12 pages and [297, 297] both with and without the rule. A hyphen is already a break opportunity.
4. **The other places an unpriced code prints in the full proposal**, the tables at `ProposalDocument.tsx:360`, `:398`, `:419` and `:467` (not under the rule): **PARTLY COVERED.**
   - The measured seven-package print puts the 60-character code into the package table (`:398`) as well, with overflow 0 and an equal page count.
   - The office, option and software tables are UNMEASURED with a long code. This is a records line.

## Findings (all Minor / records / text; none blocks)
- **F1 (Minor, records): text size is evidence only.** The 427 check pins the page count and the column widths, not the text size. Text size was 9.493 pt in all prints by `page.pdf`. The review's `window.print` shrink is UNMEASURED, and the ticket's "scales the whole PDF down" did not reproduce in `page.pdf`.
- **F2 (Minor, records): the hosted page count is unmeasured.** Page-count equality depends on the data and fonts (kit Q5). The hosted runner's absolute page count has not been measured, and the first hosted run is that measurement. A red there is fixed, never weakened.
- **F3 (records): places the rule does not reach.** Rule 4 items 1, 3 and 4: the one-pager detail cell and credit label, the three unmeasured full-proposal tables, and the hyphen shape not pinned by a committed cell. These are candidate tickets, not this lane's.
- **F4 (text): the word `pdftotext` in a comment.** The new spec holds the word once, in a comment (line 11). It is not a call, the census is green, and it is frozen kit text. Read the commission's "no `pdftotext` in any committed file" as "no call", which holds.
- **F5 (records, process): the seat's push and the move rule.** The seat pushed before evaluating the move rule; it reported this itself. There was no consequence: main's move is one file outside the lane, and this gate measured the MERGE tree green.

## Grade
**GO WITH FINDINGS.**
- No test was weakened or skipped.
- No word or priced byte changed.
- No red.
- No scope breach: exactly four paths, byte-equal to the frozen scripts.
- No acceptance line was claimed met that is not. 427's "same text size" is met by measurement only (F1), and the lengths line is met on the seat's relayed record.

Landing texts are in this folder: `pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`, `landing.txt` and `FOR-RECORDS.md`.

NO DEPLOY. The next MPS hosted deploy card must name the `proposal.css` change.

Scratch copies (head, base, main, merge, the red folders, the hyphen variants): `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/7b945764-6be0-4d12-8fda-0fa7eefbc864/scratchpad/g/`.
