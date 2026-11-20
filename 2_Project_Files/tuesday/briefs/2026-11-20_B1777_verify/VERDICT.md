GATE B1777: GO WITH FINDINGS @ b1c0e4b on main 565ba14

Gate G1 Tier 1, round 2 of 2, independent reviewer for Tuesday. Clock by `date`: start 15:11:55, last read 15:31:24 AEDT 2026-11-20. Load1 never above 3.68 (uptime reads; under 24). Nothing pushed, no PR, no Jira read or write, no deploy, no `az`. Network: `gh api -X GET` (account kamilDatasec), one clone with the project deploy key (push URL `invalid://no-push`), and the npm registry for `npm ci` (from the copied cache) and `npm audit`. The project checkout and every other seat's folder were read only. Port block 9960-9969: 0 listeners before, between and after the two browser steps (port 9961 used).

**Why GO WITH FINDINGS:** the round-1 Major is CLOSED. The predecessor's own rendered proof (an amount in the optional-items code slot, code `0.50`, unit price `1250.50`) now FINDS `1250.50`, and the gate widened that proof to all six code slots: with every coded line's code set to a tail of the amount, and each site's code slot planted with that amount, the new check finds the amount in every case (the round-1 check read 0 hits at three of the six). The product is the one round 1 reviewed: one path changed, the two source files, the priced goldens and their test byte-equal. Every CI web step is green on node 24, `npm audit` included, and local CodeQL reads 0. No Blocker, no Major. Three Minor findings and four Info rows remain. **None of them is a reason not to merge. All are follow-ups.** One Minor (the first row) touches the wording of the first limit, which the product owner will read. Tuesday may want that sentence fixed before the word pack goes to him.

## Findings
| Severity | Finding | Blocks the merge? | Recommendation |
|---|---|---|---|
| Minor | **L-A says a little more than is true.** L-A ends "The same text printed anywhere else is still found." The gate measured two ways that text printed elsewhere reads clean. Each one needs data the server sends in a DESCRIPTION, or in free text, not in a code. (a) **Cascade:** line A's description begins with line B's `<code> <description>`, and line B's code equals an amount (`1250.50`). The strip removes line A's code first, and line B's pair is then at a start, so it is removed too. Measured through the real short form, where line B is the fifth detail line and is never printed: `7 x SYN-A 1250.50 Synthetic widget` reads clean (oracle P `[]`, old check `[]` too). The control (no line B) finds `1250.50` (`out/cascade.jsonl`). (b) **A forged start mark:** text the server sends that holds U+0001 makes a start. A description `Synthetic kit 125<U+0001>0.50 Synthetic widget`, beside a line with code `0.50`, prints `1250.50` to the reader, and oracle P reads `[]`. The same happens in a narrative field and in an attribute value holding U+0001 (`out/attack.jsonl` rows A8 and A9). Without the mark, the same description is found (A8 control). **Why it is not a Major:** in every case the text removed is a string the server sent as a code, at a place made by data, not by the product. U10 flags the leftover leaf in every rendered case (A8 and the cascade: U10 non-empty). The product writes no data into attributes, which is the one place U10 does not read. Round 1's check was blind to all of these too. | No, follow-up | Two lines in the test file. (1) Decide the starts on the text as it stood before any strip, in one pass, so no cascade. (2) Remove any U+0001 from the text nodes and attribute values before writing the marks. Add a cell for each. Until then, tell the product owner the true shape of L-A: "... still found, except where a description begins with another line's code and description, or the sent text holds a control character." |
| Minor | **No cell fails when `figuresIn` keeps the start marks.** Gate mutant T5 (`figuresInText(stripCodes(text, p), p)`, marks left in) leaves all 88 cells green. The line matters: a figure split across two text nodes (`1,250` then `.50 Synthetic`) is found at the head and missed under T5 (`out/split.jsonl`). | No, follow-up | Add one cell: a figure split across two text nodes, no code involved, must be found. |
| Minor | **The ADDENDUM still does not report the page counts the round-1 review printed.** Section 6, bullet 2 says "This lane did not print a real PDF; the gate prints both". It relays 13 and 3 pages from another fixture. The round-2 section says that bullet "is not changed by this round". A reader of the word pack is not told the measured result. Round 1 printed: `s4` full proposal 12 pages before and after, short form 3 and 3; eight packages 13 and 13, 3 and 3; the review's seven-package hostile proposal 13 pages before and 14 after, "longer cells" (VERDICT B1770 lines 56-58). Longer lines can add a page, and a customer would notice that. | No, follow-up (records text) | Add one sentence to the ADDENDUM before the word pack goes to the product owner. |
| Info | An amount split across two text nodes, its tail starting the second node (`125` then `0.50 Synthetic widget`), reads clean with both the new and the old check (A2 rows). No product site prints a figure that way. Every code is printed by `partCoded` as one string with its description. The gate's six-site matrix found every planted amount. U10 is green over the four fixtures, which shows that every code the documents print sits at one of the three starts. | No | None needed. A whole figure in the first node is found (A2 last row). |
| Info | Giving the full proposal the U10 exception too (gate mutant T11) stays green. The short-form-only scope is true at the head, but no cell holds it. That is harmless today: the full proposal renders no such leaf. | No | Optional cell. |
| Info | The STATUS says the +164 -13 against the reference's +158 -9 is "comments and one blank line". Measured: the code equals the reference diff applied to fa71fc8. The differences are the comments (the three limits lines, the `stripCodes` comment, one `scanText` comment line, the "x" note) and TWO dropped blank lines (reference lines 151 and 469), not one. | No | None (true in substance). |
| Info | The builder did not run `npm audit` (its STATUS, NOT RUN). The gate ran it: rc 0, "found 0 vulnerabilities". | No | None. |

## Measured rows (each printed by a program in this session)
- **Refs:** main 565ba142d4d07b183099eee42c1b73f94242489b at 15:11:55 and again at 15:31:24 (unmoved). `matching-refs/heads/b1767` has 1 row, b1c0e4b9ad18ad9abb3228b2b80e468639eb9999. `matching-refs/heads/b1775`: 0. Open PRs: 0. `compare fa71fc87...b1c0e4b9`: ahead 1, behind 0, 1 commit, 1 file (`web/src/proposal/unpriced.test.tsx` +164 -13, blob eb3f7e7b). `compare main...b1c0e4b9`: ahead 2, behind 0, 12 files. Merge base = main, branch 0 behind, so the merge is the head tree 8c937570 (a fast-forward; `git merge-tree` not run, as in round 1).
- **Scope (rule 1):** `git diff --name-only fa71fc8 b1c0e4b` prints the one path. `diff-tree` has 1 row (control: `565ba14..b1c0e4b` prints 12). The parent of b1c0e4b is fa71fc8. Blobs at fa71fc8 and at the head are EQUAL for 11 of the 12 branch paths: `ProposalDocument.tsx` df4b6bb9, `OnePager.tsx` 9d02239f, `pricedUnchanged.test.tsx` 9f2aa36e, and the eight goldens (f2b423dc, 23143888, e82946b2, cb87c344, b27ff6fe, 41720380, bb763aa1, ace95f55). Equal at main and head: `ProposalPage.tsx`, `RentalDocument.tsx`, `package.json`, the lock, `playwright.config.ts`, `ci.yml`, `rentalUnchanged.test.tsx`. **The product is what round 1 reviewed. The product review and the PDF rows were not repeated.** The extracted head tree equals the commit: 734 blobs, 0 differing, 0 stray files, checked after every run.
- **The Major (rule 2):**
  - **Round-1 proof re-run:** the predecessor's `zzprobe2.test.tsx`, with only its output path changed, run against `zzoracle.ts` (a sed copy of lines 76-244 of the new test file). The mutant is the predecessor's own, in the optional-items site: `partCoded(o.unitSellExTax ?? o.code, o.description)`. Results:
    - code `0.50`: oracle P `["0.50 shown as 0.50","1250.50 shown as 1250.50"]`, **FOUND** (round 1: `[]`);
    - code `50`: FOUND;
    - control `SYN-GATE-1`: found.
  - **The predecessor's `zzprobe.test.tsx` at the head:**
    - the tails `0.50`/`1250.50`, `0.00`/`57940.00` and `0`/`1234.50` are now found;
    - a code that holds the amount (`PN57940.00X`) and a code equal to the amount, both in position, read clean (L-A);
    - the rounded `57,941`, the space-grouped `57 940` and `57.9k` read clean (L-B).
  - **Six-site matrix (the gate's own):** a fixture where every coded line's code is a tail of the amount a site mutant prints in its slot: codes `0`, `00`, `.00`, `0.00`, `40.00`, `940.00`, `7940.00` and `50.00`. Each run planted the amount in one site's code slot (S1 for L1 and L5, then S2, S3, S4, S6); the table shows the hits for each run.

    | Run | New check | Round-1 check |
    |---|---|---|
    | No mutant | 0 hits in both documents | (not run) |
    | S1: L1 and L5 detail lines, package totals | 7 hits, both documents | 2 |
    | S2: L2 office table | 6 | 1 |
    | S3: L3 optional items, unit price | 4 (`2150.00` found) | **0** |
    | S4: L4 software, amount | 6 (`12150.00`, `-12150.00`) | **0** |
    | S6: L6 short-form software, amount | 6 | **0** |

    Each mutant also turns 12 to 27 committed cells red, B5 among them in every run (`out/sites-run.txt`).
  - **Attacks (51 rows, `out/attack.jsonl`; each row also read by the round-1 check as a control):**
    - (a) **Tail codes after the quantity:** `7 x 1250.50 Synthetic widget` with codes `0.50`, `50`, `.50`, `250.50`, `50 ` (trailing space) and ` 0.50`, and the grouped and dollar forms: all found.
    - (b) **Split across two text nodes:** blind, old and new (Info).
    - (c) **Tail after a digit-and-sign run:**
      - `57 x 940.00 <desc>` (code `940.00`, amount `57940.00`): not the amount, so nothing hidden;
      - a figure as the quantity (`1,250.50 x 0.50 <desc>`, `57,940 x SYN-1 <desc>`): found.
    - (d) **A price-shaped quantity:** rendered quantity 1250 with total `1250.00`: found as `1,250` in both documents.
    - (e) **A code beginning with the sign or with a digit and the sign:** reads as a code in its own place (L-A). The amount after it is found.
    - (f) **A description that repeats:** found. A cascade through a description: blind (Minor (a)).
    - (g) **The same pair twice in one node,** in either order: the amount is found and the legitimate pair is stripped.
    - (h) **The mark typed into data:** blind (Minor (b)). A code holding the mark reads clean as a code (L-A).
    - (i) **An attribute that begins with or holds the mark:** blind (Minor (b)). Otherwise attributes are read (B3).
    - (j) **Whitespace collapsing:**
      - a node `125 ` then `0.50 <desc>` is not a figure;
      - a no-break space or a tab inside the quantity separator is not a start, so the amount is found.
    - (k) **Longest-first:** a long pair stripped before a tail pair leaves the amount found. The only loss is the cascade in Minor (a).
  - **Severity rule applied:** no way found for the PRODUCT to print a figure that hides without the server sending the overlapping text as a code. No Major.
- **Cells and mutants (rule 3):** each run is the gate's own string edit, restored and sha256-proved (the 3 files equal their start hashes after every batch).
  - **The four round-1 plants, still red:** P1 9 red; P2 13 (the predecessor's exact edit: the fleet-detail cell); P3 1 (U10 full proposal); P4 4 (the short-form goldens, over the 4-file family, 149 tests).
  - **Test-function mutants:**

    | Mutant | Red | Cells |
    |---|---|---|
    | T1 the boundary removed (strip at every match) | 5 | B1 x2, B3 x2, the SKU cell |
    | T2 the start mark written on attribute lines too | 1 | B3 attribute |
    | T3 the quantity start without its digit test | 1 | B3 anywhere (`a x 4521.10 ...`) |
    | T4 the predecessor's rule ("the character before is not a digit, `.` or `,`") in place of the list | 3 | B3 anywhere, B3 attribute, the SKU cell |
    | T5 marks kept before the scan | 0 | none (Minor) |
    | T6 a node start after a mark and a space | 1 | B3 anywhere |
    | T7 node lines unmarked | 5 | B2 node, B5, 3 numeric-code cells |
    | T8 startOfText never true | 5 | U10 x2, B2 starts, B4, U10 function |
    | T9 visible line unmarked | 5 | as T7 |
    | T10 short-form exception emptied | 1 | short form U10 only |
    | T11 the full proposal given the exception | 0 | expected; Info |
    | T12 the quantity start dropped from the list | 13 | the closed-list cell, B2, B4, limit, ... |
    | T13 the strip removes the code anywhere, no pair | 14 | B1 x3 (the middle-slice guard included), B2, B3 x2, B4, ... |
    | T14 afterQuantity never true | 12 | |

    - **The predecessor's rule is wider than the stated limit: CONFIRMED.** Under T4, the B1 cells stay green (it closes the Major), and B3 fails on `Total 4521.10 Synthetic widget`, a code equal to an amount printed after the word "Total", which T4 reads clean.
  - **Every one of the 11 new cells goes red under at least one gate mutant:**
    - closed list: T12;
    - B1 tail: T1, T13;
    - B1 quantity and grouped form: T1, T13;
    - B1 middle slice: T13;
    - B2 starts: T8, T12, T14;
    - B2 node after a digit: T7, T9;
    - B3 anywhere: T1, T3, T4, T6;
    - B3 attribute: T1, T2, T4;
    - B4: T8, T12-T14;
    - limit: T12, T14;
    - B5: T7, T9, S1-S6, P1, P2.
  - **The changed U10 cell (the SKU line):** the new expectation `['SKU SYN-ABC-1 Synthetic widget']` is right under the closed list. A code after `SKU ` follows a letter and a space, so it is not a start. T1 and T4 turn it red. The leaf is unexplained under both readings.
  - **The scoped exception:** the full proposal's render cell passes `[]` and is green over all four fixtures.
- **Web checks (rule 4), node v24.22.2 / npm 11.19.1, `TZ=UTC`:**
  - `npm ci --prefer-offline` rc 0 (273 packages; "found 0 vulnerabilities").
  - **`npm audit --omit=dev --audit-level=high` rc 0, "found 0 vulnerabilities".**
  - `npm run lint` rc 0.
  - `npm test`: 149 files and 1723 tests passed, 0 failed. `unpriced.test.tsx` alone: 88 passed.
  - `npx tsc -b` rc 0, no output.
  - Stub step (port 9961; `--list` 277 tests in 19 files): 260 passed, 17 skipped, rc 0, 4.1 min. Stub-off step (`--list` 161 in 8): 161 passed, rc 0, 2.5 min.
  - `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist` rc 0 ("dist: 8 files, 1112492 bytes; markers found 0/57").
  - The goldens are byte-unchanged (same blobs) and green on node 24 inside the whole run.
- **CodeQL (rule 5):** `pr_codeql_check.sh --base 565ba142 --head b1c0e4b9 --lang javascript`, CLI 2.27.4, javascript-security-extended (103 rules). Both sarif files written: head 670 artifacts, base 661. Diff pack: 12 files, 34 ranges.
  ```
  VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
    results   head 0   base 0
    KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
    NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
    GONE      total 0
    RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
  ```
  rc 0. This is a local approximation: the hosted `CodeQL` and `Analyze (javascript-typescript)` checks on the PR head remain the authority.
- **ADDENDUM (rule 6):**
  - **Round-1 text byte-unchanged:** the first 6805 bytes of the live file (10211 bytes) `cmp` equal to the before-copy (55 lines, sha256 7ca75960...; the round-1 commission gave 55 lines). The added 3406 bytes hold 0 non-ASCII lines. The file is untracked by git, so the before-copy (the builder's `.tools/b1775/out/addendum.before`, mtime 13:32, before the round-1 gate began) is the only prior image. The gate also re-checked the round-1 content: the 7 before-and-after lines are still true against round 1's base and head dumps (7 of 7).
  - **The round-2 section:**
    - L-A, L-B and L-C verbatim, 1 each; "abbreviated" present.
    - The count 26 (`git diff --numstat fa71fc8^ fa71fc8`: 21 and 5) is TRUE.
    - R2-1 is faithful to VERDICT B1770 line 13 (16 and 14 price-shaped strings, all inside codes, 0 without them).
    - R2-2 is faithful to line 12: 16.76, 16.61, 15.64, 14.78 and 13.30 pt; 11.19 pt at 60 characters; 14 to 13 to 12 pages; `s4` unchanged up to 40 characters.
    - "No source file, no priced golden and no word changes" is TRUE (blobs).
    - No sentence attributes anything to the product owner.
  - **What a customer would notice that is still missing:** the measured page counts (Minor), and the shape of L-A (Minor (a)).
  - **Nits, Info only:**
    - "prints exactly as typed": the product trims spaces around a code, and a code equal to its description prints nothing (section 3 says this);
    - the intro's "the review's hostile fixture: the four builder fixtures and four fixtures of its own" runs together the detector's eight fixtures and the one seven-package hostile proposal that was printed.
- **Text (rule 7):**
  - The second commit's message (30 lines) and its 164 added lines: underscore-aware name scan, 0 hits each for Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, Tuesday, Wednesday and Friday (each planted `x_by_<name>_y` control fires 1).
  - B-numbers 0 (control fires), seat or card ids 0, non-ASCII or control-character lines 0 (U+200B control fires), Cf 0. Literal 0x01 or U+00D7 bytes in added lines: 0 (both built by `String.fromCharCode`).
  - Product-owner wording (`product owner|approv|ruled|ruling|decid`): 0 in both.
  - Hand rows over the added lines: `new RegExp(`, hand-escape, `innerHTML =`, `dangerouslySetInnerHTML`, `eval(`, `child_process`, `eslint-disable`, `waitForTimeout`, `.only(`, ts-ignore, storage, `console.log`, `.skip(`: all 0.
  - Subject 98 characters. One trailer `Co-Authored-By: Claude Sonnet 5.5`. Author and committer are the repo's identity.
  - The ruling sentence is present once in entry C-186 of the root records.
- **Commit text vs measurement:**
  - The second commit's body carries L-A to L-C. "A code printed anywhere else ... stays in the scanned text and is read" holds except for the two data cases of Minor (a).
  - The first commit's body still says "equal". The squash text below replaces both.

## Builder claims graded (STATUS B1775)
- One path; the 11 others byte-equal: TRUE.
- Cells over the round-1 function: 5 red, the named set. NOT RE-RUN as a separate state; the gate's T1 and T13 (no boundary, and code-anywhere) give the same red B1 and B3 cells.
- Fixed file 88 passed; whole suite 149 files and 1723 tests: TRUE (node 24).
- P1 9, P2 13, P3 1, P4 4: TRUE.
- P5, P6, P7 red over the fixed file: TRUE in kind. The gate's S3, S4 and S6 turn B5 red. The cells-only state was not re-run.
- Mutants M1 to M9 and M4b: not re-run as written. The gate's 14 test-function mutants cover the same shapes. 12 went red. The 2 green are named (T5 Minor, T11 Info).
- Census 273 pairs, 0 elsewhere: not re-run. U10 green over the 4 fixtures in both documents, and the six-site matrix, stand in for it.
- +164 -13 is "comments and one blank line": TRUE for the code; two blank lines, not one (Info).
- Browser steps 260 + 17 and 161; build, bundle, eslint, tsc rc 0: TRUE.
- ADDENDUM 6805 to 10211 bytes, prefix equal, 0 non-ASCII added: TRUE.
- `npm audit` NOT RUN by the builder: the gate ran it, rc 0.

## TESTED / NOT TESTED / HOW
- **HOW:**
  - A clone at `/private/tmp/b1777-gate/repo` (push URL invalid). The head tree was extracted with `git archive` to `/private/tmp/b1777-gate/head`, with `node_modules` from `npm ci` against the cache copied from gate B1770.
  - The gate's files were copied into the tree only for their runs, then moved to `/private/tmp/b1777-gate/quar/head-proposal/` before the CI checks:
    - `zzoracle.ts`: sed lines 76-244 of the new test file;
    - `zzoracle_old.ts`: round 1's copy;
    - `zzprobe*.test.tsx`: round 1's, path changed;
    - `zzattack`, `zzsites`, `zzcascade` and `zzsplit`.
  - Mutants were applied by `scripts/mutants.py` with a sha256 restore check. Outputs are in `/private/tmp/b1777-gate/out/` and logs in `/private/tmp/b1777-gate/logs/`.
- **NOT TESTED:**
  - A real PDF: no source file changed, so the round-1 PDF rows stand; the commission says not to repeat them.
  - The 16-render base and head compare: unaffected, the source blobs are equal.
  - The builder's census and its cells-only state, as written (stand-ins above).
  - Whether the server or the input screens accept a control character (U+0001) in a code, description or narrative field, which Minor (a)(b) needs. The Api was not read.
  - The hosted CI and hosted CodeQL on a PR head (none exists).
  - `git merge-tree` (the fast-forward argument stands in).
  - Dotnet and python jobs (no file of theirs changed).
  - Real Api data and real part codes (synthetic only).
  - The Jira text of MPSCALC-278 and MPSCALC-426: not read (no hosted request). The clauses are carried from round 1.
  - The heavy-lock files of the project's `.tools` (outside the gate's write folders). Heavy jobs ran one at a time instead.
