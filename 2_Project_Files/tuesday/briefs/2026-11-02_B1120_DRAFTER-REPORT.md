STARTABLE: YES (after the stamp; ten slots, all four-underscore; the last `date` of drafting read 12:35 AEDT 2026-11-02)

# B1120 DRAFTER REPORT (Sonnet C8 drafter for Tuesday), kit `2026-11-02_B1120_SEAT-R134_mps-records-red-first-317-b1106.md`

## BLUF
One kit, 25,269 bytes (24.7 KiB; decimal 25.3 kB, 270 over a 25,000 count, under 25,600), R131's form: C-82 and C-83, 14 Jira writes at most (1 create, 8 comments, 5 moves), one section on `records/b1120`, BACKLOG rows, ff-only. Texts are fixed in the kit (default TEXTS = APPROVED-AS-DRAFTED; the stamp names the sha256 of the THE TEXTS block, 9,441 bytes). Default slots: MOVE-TO-DONE for -253, -317, -357, -343, -344; -257, -362, -367 never move. Nothing was written anywhere but the two files.

## Facts re-measured (instrument, control; clocks from `date` in the same action)
- Root main = `records/b1111` = 4d96215b (rev-parse, 12:18); root repo has no remote (`[remote` 0), so the ff-only land is the project's form (R131 landed that way); CLARIFICATIONS 2201 lines, highest C-81 :2133, batch 7 :2167, readings (ad)(ae) :2171; no C-82 anywhere (grep 0, control C-81 1). BACKLOG 4471, JIRA.md 511, history 1310. `records/b1120`, `.tools/b1120`, `.git-lock`, MERGE_HEAD, index.lock: absent (ls rc 1 each).
- Code main 7104179f (`git/ref/heads/main`; control pulls/99999 404). #142: merged, squash 7104179f, head 05d6b1db, merged 2026-11-02T00:57:34Z, 5 files +333 -4; web subtree f3d3323f = the gate's; 5 of 5 blobs head = squash (control: `QuoteScreen.tsx` at 19d084fa is 7bbeefff, different); check-runs 8 of 8; ci push run 41369924301 attempt 1 success. #141: merged, squash f8f808c4, merged 00:23:30Z, 4 files +224 -0; 4 of 4 blobs equal; tree ce147dba = the gate's T; check-runs 8 of 8; ci run 41366894741 attempt 1. Squash(#142) vs hosted build e027ebd0: behind 42.
- Jira (paged to isLast, 12:20): 368 issues, Done 130; -253 Backlog (comments 40640, 40649), -257 Backlog (40655), -367 Backlog 0 comments, -317, -357, -343, -344, -362 Backlog 0 comments; Done id 41 on each. Highest MPSCALC-368 (R131's two creates exist: -367, -368).
- `b1117*` branches on origin: 0; M76's STATUS last line at 12:05 `WORKING: step 3 done`. So the user's "has not landed" holds.
- Ports: `lsof` 9900-9999 empty. Panes (12:18): tuesday, fleet-monitor, MPS-M76, four HPSM-POC; `^Datasec/MPS-R[0-9]+$` count 0 before launch. Kit names: R134 and B1120 each 0 hits (R131 control 1). Disk: `/Volumes/Laptop-DEV` 40 GiB free (the 25 GiB stop is 15 GiB away).
- Duplicate search for the new ticket (12:20, tokenised, each `project = MPSCALC AND ( ... )`): PriceReason 0, PurchaseBomEditor 17 (read the timeout-bearing ones: none holds these rows), load-sensitive 1 (MPSCALC-163, Api overlay burst tests, a different set), timed out 11 and timeout+load 5 (e2e and feedback tickets; regex over candidates read), E8 1 (MPSCALC-20, unrelated), B1103/B1106/B1070/testTimeout 0; controls zzqxnonexist 0, key = MPSCALC-368 1, annualRecurringGp finds -364. Not read: a dump of all 368 descriptions (only candidate keys); the seat does the full dump.
- Text-block scan of THE TEXTS (python, 12:34): digit-dot-digit 0, percent 0, `deployed` 0, `live` 0, `complet` 0, names 0, `@` 0, card-slug class 0, non-ASCII 0 (the only non-ASCII in the kit is the verbatim em dash in the two ruling quotes, outside the Jira texts).
- Gate pointers printed by `grep -n` 12:22 (positive control: each pattern fired): B1103 :1 verdict, :146-151 B1103-1..6, :176 landing item 7; B1106 :1, :84-90, :104-107, :123, :60; B1070 :238 (-2), :240 (-4); B1075 :158-162, :174-175; B1117 kit :1, :5 (ruling), :24 (KNOWN CONTRADICTION).

## D-decisions (mine)
- D-1 C-82 = the blocked reading (11:48:01), C-83 = red-first (11:48:10): numbered in ruling-time order, as C-80/C-81 were; the assignment listed them the other way round.
- D-2 Card ids (`mps-257-253-red-first-meaning-1102`, `mps-257-blocked-warning-reading-1102`) are left out of record text, as C-80 does (rule 7); the words, letter and option detail are quoted verbatim.
- D-3 TX-317 paraphrases gate line 1 ("PROVISIONAL GO WITH FINDINGS, INCOMPLETE ..."): the word INCOMPLETE trips the banned `complet` scan, so a verbatim quote would HOLD the text.
- D-4 -253: default MOVE, with three candidate holds named and judged not to hold (gate's PARTLY-DONE sentence :175 beside its Done sentence :174; spelling gap B1075-8; word pack). The seat can only downgrade to COMMENT-ONLY (variant HOLD in TX-253).
- D-5 -362: comment only, PARTLY-DONE sentence per the gate; no move slot exists.
- D-6 New ticket labelled lane-v0 (web, as -317), tier 2, summary prefix `[B1103-4] `, type/priority/assignee from -362. Five rows named: three in PurchaseBomEditor.test.tsx (E8, the seller per-persona row, the manual-item-on-two-lines row), two in PriceReason.test.tsx (path is `web/src/screens/bom/PriceReason.test.tsx`, confirmed in the tree at 7104179f).
- D-7 Write order puts the create first, so the -317 text can name the new key.

## Q-questions for Tuesday (each with a default)
- Q-1 Stamp DONE-253 MOVE-TO-DONE? Default yes (precedent -252, -256; the Acceptance names no Api clause; C-83 closes the only open reading).
- Q-2 B1103-1 is "Tuesday ruled a Note": I found no record of that ruling in any file (B1103's STATUS ends `STOPPED: NEEDS TUESDAY`). The stamp must carry its time and words; default: stamp them, else DONE-317 = COMMENT-ONLY.
- Q-3 TX-NEW acceptance: "all of 20 whole-suite runs at load above seven" - the 20 is mine, not a gate figure. Default keep; change at the stamp.
- Q-4 The em dash in the verbatim ruling words: default the C-entry keeps U+2014 as relayed (CLARIFICATIONS uses ASCII ` -- ` elsewhere); alternative write it ` - `.
- Q-5 Disk margin: 40 GiB free against a 25 GiB stop; default launch (the seat stops itself at Step 0 if it falls).
- Q-6 If M76 lands before the seat runs, TX-257 and TX-367 HOLD (REFUSE 8). Default: leave to the seat; a re-draft of those two texts would then be needed.

## Contradictions found
- The assignment says -367 "asks for the opposite": confirmed (its Recommendation and Acceptance: a priced quote with an expired source raises NO SITE ALLOCATION DIFFERS).
- -257's comment 40655 says "reading B ... is not what is built"; that stays true until M76 lands; TX-257 says so and C-82 says so.
- B1075's own sentence at :175 is PARTLY-DONE for -253; B1099's comment 40640 adopted the same sentence; the move rests on the Done sentence :174 and the -252/-256 precedent, which is a reading (coordinator's), stated in TX-253.
- -317's description (existing text) contains the word "deployed" and "live"; our texts do not repeat it.
- The brief rule "figures printed by program": TX counts quoted from B1087/B1103 (1 of 8, 23 of 23, 20 alone, 14 of 20 dropped from the text) are printed by the seat from those lines with `<<...>>` slots; any mismatch HOLDS TX-NEW.

## UNMEASURED
No write of any kind; the hosted state; whether M76 lands first; that B1075 clause-5 pointers hold at code main (#141 added 31 lines to ComponentQuantityRuleTests.cs, so the comment-40649 lines may have moved); the test method names of #141 (read from the PR patch by the seat); the exact titles of the five TX-NEW rows; the ruling times beyond the relay (decision store not read); full-text dump of all 368 tickets for the duplicate search.

## Outside-the-fences disclosure
Wrote only the kit and this report. Used scratchpad scripts `jr.py`, `dup.py`, `trim*.py` under the session scratchpad (Jira GET only; JIRA_ values read in-process from the project `.env`, never printed). Read, did not run, `.tools/b1111/j1111.py` and `lib1111.py` for the create/fence form. `gh api -X GET` only, under the project `GH_CONFIG_DIR`. No decision_queue.sh, no fleet/briefs_staged, no scoreboard, no ledger, no WEDNESDAY/FRIDAY tree, no non-Datasec project; no git write; no HTTP to any hosted site. A first draft ran to 36 KB and was trimmed to size; intermediate versions lived only in the kit file.
