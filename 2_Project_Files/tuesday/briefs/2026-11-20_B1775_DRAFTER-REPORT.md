STARTABLE: YES - the kit is complete, `stamp_check.py` exits 0 (134 claims, 134 measured), the nine slot lines and the last line are four underscores, and every RED/GREEN set the kit states for the function was run in a scratch copy of the head (node 24). Four things are Tuesday's at the stamp: the slot values, the port block re-read, the level, and the two UNMEASURED items below that the seat measures first (the whole suite and the browser steps).

# B1775 drafter report (Sonnet drafter, commissioned by Tuesday s297; drafted 14:04 to 14:22 AEDT 2026-11-20)
Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1775_SEAT-M168_mps-part-codes-round2-oracle-boundary.md` (470 lines, 0 non-ASCII bytes) with sidecar `...md.measured` (134 lines). This report: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1775_DRAFTER-REPORT.md`. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s297/d1775/` (tarball copy of the head, my variants and logs, the reference diff `work/fixS.diff`, the census cell in `quarantine/`).

## BLUF
- **The fix is a closed list of three places a code can start**, not the review's "character before is not a digit, a dot or a comma". The three: the start of the text; the start of a text node (`scanText` writes U+0001 before each node); right after `<digit> x ` (a digit, space, U+00D7, space). A code anywhere else, and every attribute line, stays in the scanned text. The review's rule is mutant M9: it closes the Major but 4 cells go RED because it strips a code that equals an amount after any space or letter and at the start of an attribute line, so the stated limit would be wider than "in its own place".
- **Proved by census (MEASURED, throw-away cell, node 24, TZ=UTC):** 273 occurrences of a coded pair in text nodes of the 8 unpriced renders (4 fixtures x 2 documents): 99 at the start of a text node, 174 after `<digit> x `, **0 anywhere else**; per fixture the sums equal the first round's counts (30/8, 30/8, 11/5, 164/17).
- **Right side answered:** a figure cannot hide by running on after the description (the strip removes the code and one space, nothing after). Cell B4 proves it, mutant M6 (eat a following digit run) turns it red. No product fault; the two source files are not edited.
- **Dry run of the reference diff (`unpriced.test.tsx` only, +158 -9 lines, 8 hunks):** head 77 tests green; the 11 new cells over the OLD function: **5 failed | 83 passed (88)**; with the fix **88 passed**; eslint rc 0 on the file; `tsc --noEmit -p tsconfig.test.json` rc 0; 0 non-ASCII bytes. The gate's case (code `0.50`, price `1250.50`) is RED at the round-1 head, GREEN after.
- **Plants and mutants all RED as the kit tabulates** (tables below). No mutant stayed green.
- The seat is Sonnet (row C2), second commit, fast-forward push, one path changed in the repository, plus a dated section in the ADDENDUM.

## The boundary rule and the table that proves it
Property: the strip removes a code only where the documents begin to print a line item's code; anything before it stays. Closed list (at least these; any other shape: prove it or STOP): `startOfText` (offset 0), `startOfTextNode` (right after U+0001), `afterQuantity` (`<digit>`, space, U+00D7, space, then the code).
| Fixture | Full: start of text node / after "x " | Short form: start of text node / after "x " |
|---|---|---|
| s4 draft | 12 / 18 (30) | 2 / 6 (8) |
| s4 approved | 12 / 18 (30) | 2 / 6 (8) |
| five classes with a deal pair | 1 / 10 (11) | 0 / 5 (5) |
| eight packages | 68 / 96 (164) | 2 / 15 (17) |
By site (s4 full): stream cards 7 and fleet detail 11 after the quantity (18); office table 8, optional items 2, software table 2 at a node start (12). Short form: detail cell 6 after the quantity; software table 2 at a node start. Census log: `.../d1775/work/logs/census.log`.

## Plants (dry run, drafter's copy; each restored and byte-compared)
| Plant | Round-1 function, old cells (head) | Round-1 function + 11 cells | Fixed |
|---|---|---|---|
| P5 optional item: unit price in the code slot (the gate's mutant) | 12 red | 17 red, **B5 green (blind)** | 13 red, **B5 red** |
| P6 short form software row: amount in the code slot | 11 | 16, B5 green | 12, B5 red |
| P7 full proposal software row: amount in the code slot | 13 | 18, B5 green | 14, B5 red |
| P1 `data-total` on the KPI strip | 8 (the review: 8) | - | 9 (8 + B5) |
| P2 `57,940` ending the schedule cell | 12 (the review: 12) | - | 13 |
| P3 the words `package price` in the Qty cell | 1 | - | 1 (U10 full) |
| P4 `22%` to `23%` | - | - | 4 red, 57 pass over the three files (goldens 4 short-form cells; `OnePager.test.tsx`, `ProposalDocument.test.tsx` green) |
## Mutants of the function (on the reference file; the rest stayed green)
M1 boundary removed again 6 red; M2 wrong side (the character after the match) 15; M3 list emptied 16; M4 a start after a space 3; M4b the quantity start without the digit 1; M5 the node-start dropped 7; M6 right side eaten 1; M7 attribute lines marked as starts 1; M8 a start after any non-alphanumeric 4; M9 the review's rule 4 (and the B1 cells green). Short-form-only exception: with an empty list for the short form exactly 1 cell red. Logs: `.../d1775/work/logs/run-*.log`.

## Files
Written (three): the kit, its `.measured` sidecar, this report. Read-only reads: the commission, `DRAFTER_RULES.md`, the verdict folder (`VERDICT.md`, `FOR-RECORDS.md`, `landing.txt`, `squash-body.txt`, `squash-subject.txt`, `pr-body.md`), the round-1 kit (+ `.measured` sample), STATUS and ADDENDUM of round 1, root `CLARIFICATIONS.md` lines 3544 to 3559, `stamp_check.py`, `stamp_brief.py`, `brief_seat.sh`, `model-routing.md`, `models_latest.json`, the review's `/private/tmp/b1770-gate/` listing (names only) and its `head/web/node_modules` (copied).

## Facts re-measured (instruments in the sidecar)
- **Refs re-read three times**, `gh api -X GET` under the MPS `GH_CONFIG_DIR`, account `kamilDatasec` verified first: 14:04:23-25, 14:14:48 (main), 14:20:37-39: main `565ba142d4d07b183099eee42c1b73f94242489b` unmoved; `matching-refs/heads/b1767` one row `fa71fc87218120192aa0c68c2c85936978b997d9`; open PRs 0; `compare main...fa71fc87` ahead 1 behind 0, 12 files.
- Head blobs (tarball copy equals the compare's): `unpriced.test.tsx` `e7584a6f`, `ProposalDocument.tsx` `df4b6bb9`, `OnePager.tsx` `9d02239f`, `pricedUnchanged.test.tsx` `9f2aa36e`; eight golden blobs in the kit (FACT 2). Added source lines 21 + 5 = 26 (compare's `additions`).
- Cells by the indented pattern: 68 at the head, 79 with the diff; column-1 pattern 0 at both; runtime tests 77 and 88. Selectors measured against the 88-test file (11, 1, 1, 2, 3, 2, 4, 8).
- Node 24: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin/node` prints `v24.22.2`, npm `11.19.1`; the machine's node `v26.13.0`; CI `node-version: 24` at `ci.yml:58`; the project's `.tools` holds no node folder. The seat uses the node 24 path (fallback to the machine's node, said in STATUS).
- Machine at 14:12: 0 listeners on 9980-9989 (control: 15 listeners in all), `df` 1030 GiB free, 0 `lock` entries in the project's `.tools` (control: 3 name `dotnet`), no `Datasec/MPS-` pane; load1 2.5 to 3.3 at every read.
- Port scan, word-boundary `(^|[^0-9])998[0-9]([^0-9]|$)` over the 26 non-`.pre-` SEAT kits of 2026-11-19 and 2026-11-20 (frame: `SEAT-` kits in the briefs folder without `.pre-` or `.measured`): hits only in `B1746` (8 lines), `B1747` (12) and `B1767` (10), all finished lanes (landed #219, #221, round 1 pushed); the other 23 read 0.
- Model: `claude-sonnet-5-5` (`models_latest.json:23`), routing row C2 (`model-routing.md:92`); C8 is this drafting job. `brief_seat.sh:31` reads `${BRIEF_SEAT_LEVEL:-opus}`.

## Chain inputs (rule 4: every step's inputs are produced earlier or exist at the head)
Step 0: this kit, the stamp slots, the project's `.tools` (exists). 1: origin branch head (exists), node 24 path (exists), deploy key (exists). 2: baseline numbers (step 1). 3: head tree (step 1), the reference diff text (the kit). 4: the cells (step 3). 5: the function (step 4). 6: plants and mutants over the files of steps 3 and 4. 7: the ADDENDUM (exists at the project path). 8: all of the above. 9: the diff and the checks of step 8. 10: the commit (step 9). No step needs a file a later step makes.

## D decisions (Tuesday's choices as coordinator, each written that way in the kit; none the product owner's)
D1 the closed list with start marks (not the review's rule). D2 the one U10 exception scoped to the short form (three changed lines, IN). D3 `ProposalDocument.tsx` and `OnePager.tsx` not edited. D4 one changed expected value in an existing cell (the `SKU` line of the U10 function cell: a code after a word is no longer at a start; the leaf stays unexplained either way). D5 the commit subject ends `(MPSCALC-278)`. D6 the first round's STATUS is not edited (the 24 vs 26 correction goes in the ADDENDUM and the records pass). D7 the long-code layout is OUT (a follow-up the records pass files).

## Q for Tuesday (each with the default the kit assumes)
- Q1 the rule: closed list (default) vs the review's rule (M9 measured as wider). Q2 scope the exception: yes. Q3 ticket in the subject: `(MPSCALC-278)`; alternative `MPSCALC-426`. Q4 node: 24 by the Tuesday-tools path. Q5 gate tier: same as the first round; PDF row only if a source file changes. Q6 level: `sonnet` inside the quotes. Q7 port block: 9980-9989 (second port 9981), free now; re-read at the stamp. Q8 the long-code follow-up ticket and the STATUS correction: the records pass's. Q9 whole-suite total 1723: DERIVED.
- **Recommended slot answers (facts the DRAFTER measured, marked; Tuesday writes the readings only after doing them):** S0 the ruling quoted in the kit's AUTHORITY (the drafter read the ruling line at `### C-186`, `CLARIFICATIONS.md:3548`); the product owner has said nothing else on this ticket that the drafter read (Tuesday to confirm from the card). S2 main `565ba142d4d07b183099eee42c1b73f94242489b` (the drafter read it at 14:20:37); S3 branch head `fa71fc87218120192aa0c68c2c85936978b997d9` (read 14:20:37); S4 open PRs 0, no `Datasec/MPS-` pane, 0 listeners on 9980-9989, 0 lock entries (the drafter's reads, 14:12 to 14:20; Tuesday re-prints); S5 the Q answers above; S7 block 9980-9989 and port 9981, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, `claude-sonnet-5-5`; S8 absolute hard stop: Tuesday's (the first round used 16:56 AEDT; a later window is Tuesday's to set). `@NOW@` for Tuesday's own read clocks; no slot value repeats its label.

## Corrections to the commission
1. **"(d) the count of added source lines is 26, not 24" is not in the ADDENDUM**: the 24 is in the first round's STATUS (check (b)); the ADDENDUM has no such count. The kit adds the correction as item 4 of the ADDENDUM's round-2 section and leaves the STATUS to the records pass.
2. **The review's recommended rule (character before is not a digit, dot or comma) is not what the kit uses**: measured as M9, it closes the Major but is wider than the stated limit (4 cells red). The kit explains and keeps it as a mutant and as Q1's alternative.
3. **A rendered proof of the gate's case through the real documents cannot be a committed cell that is RED without editing a source file**: the committed cell B5 (real documents, tail codes) is a guard that goes RED only under the source plants P5 to P7; the cells that are RED at the round-1 head with no plant are the string and small-DOM cells B1 and B3 (5 RED in all). The kit says so.
4. The commission gives the round-1 code counts as "30" etc. without the split; the kit adds the census split (99 / 174).
5. `squash-body.txt` and `pr-body.md` in the review's folder say "rounded or regrouped" and omit "abbreviated"; the kit's commit body carries all three words; aligning the squash text is Tuesday's (the kit's FOR TUESDAY line asks the seat to say so).
6. The hosted-CI note: a middle-slice code (`PN57940.00X` contains an amount) is covered by the same sentence as the tails; the kit states it under L-A and the `limit, stated` cell.

## UNMEASURED (named; the seat or the gate measures)
The whole suite after the change (kit says 149 files and 1723 tests, DERIVED 1712 + 11); the two browser steps and their totals (RELAYED 260 + 17 and 161); `npm audit`; the entra build and bundle check; `npx tsc -b` (only `tsc --noEmit -p tsconfig.test.json` on the scratch copy, rc 0); CodeQL; whether `npm ci` of the seat comes wholly from the machine cache; the Jira state of MPSCALC-278 now (no Jira call by the drafter; round 1's STATUS read comment 41409 at 13:31); how long real catalogue codes are; the PDF figures (RELAYED from the verdict with the fixture named; the kit says the hostile proposal is a review file, not committed).

## Outside-the-fences disclosure
- The drafter copied the review's `/private/tmp/b1770-gate/head/web/node_modules` (223M) into its scratch to run vitest (a read of the review's tree; nothing written there) and executed Tuesday's node 24 binary by path. All test runs were single-file `vitest` runs (plus one run of three files for plant P4), one `eslint` on one file, one `tsc --noEmit -p tsconfig.test.json`, in the scratch copy, at load1 under 3.5, with no MPS lock held by anyone (0 lock entries, no MPS pane). The commission allows this ("a single-file vitest run on a copy"); the P4 run adds two more existing test files.
- Nothing was run in the project's checkout or any `.tools` tree; the project `.tools` listing was read by `ls -A` (names only); `.local/`, `Source_Documents/**`, price books, decision cards, `fleet/briefs_staged/`, the ledger and the scoreboard were not read.
- Every `gh` call was `gh api -X GET` under the MPS project's `GH_CONFIG_DIR` (account `kamilDatasec` verified); no Jira call; no hosted call; no listener started.
- One `rm -f` of a file that did not yet exist was typed in a shell command and refused by the no-delete hook (the whole command was refused, so nothing ran); nothing was deleted anywhere. The throw-away census cell was moved (not deleted) to `.../d1775/quarantine/` twice. A scratch control file `scratch_ctl.txt` (a U+200B line for the ASCII-scan control) sits in the scratch folder.
- No text in the kit says the product owner decided anything beyond the ruling quoted from C-186; the kit names Tuesday only in headings and process lines, not in the commit text (the commit body drafted in the kit holds no name, no B-number and no card id).
