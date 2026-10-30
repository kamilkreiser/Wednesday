STARTABLE: YES (after your stamp; the machine is loaded, so the launch waits on launch_when_cool; no sweep pointer blocks it)

# B945 drafter report (Sonnet 5.5, 2026-10-30 about 14:55 to 15:25 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B945_SEAT-H70_hpsmpoc-384-revenue.md` (142 lines; 9 lines with four underscores = 8 slots + the last line, counted by python and by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0; non-ASCII 0 after repair, see Disclosure 2). Read-only everywhere else: gh `-X GET` under the project `.gh-config`, Jira GET through `.tools/b649/jira.py`, no ref written, no card, no mail, no `cd`, no hosted HTTP, no test run. No file was written in the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H70` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes), branch `b945/hpsmpoc-384-revenue` off `7365165d` (H3 is in base, so no merge). It restyles `RevenueCalculator.tsx`, `RevenueResults.tsx`, `OneCustomerEstimate.tsx` (+ one new test file `Revenue.restyle.test.tsx`) only. The two real tables (Comparison, one-customer) move onto the `ui/Table` class constants by import; the metric rows and Stat cards take the card and square-tile look. Figures are proved byte-equal by program: an untracked text-extraction harness over about 60 states at base and head, plus a browser `textContent` comparison, each with a figure plant that must turn it red. Ends at READY FOR QA; a tier-2 gate follows.

## What #244 means for the builder (asked for)
`commits/7365165d` lists 4 paths, +13 -5: `customer/parts.tsx`, `customer/parts.restyle.test.tsx`, `ui/Table.tsx`, `ui/Table.test.tsx`. `thClass` and `tdClass` now carry `max-md:px-1` (and `thClass` `max-md:tracking-normal`); `rowHeadClass` is `tdClass` + `text-left font-medium`; export names unchanged. Consequences in the kit: (1) import the constants, never edit; (2) do NOT use `rowHeadClass` for the scenario-name cells (its `font-medium` would change today's `font-semibold`); (3) PR #244's measured 496.7 -> 399.3 px is the BarChart "Show as table" table (H3's file), not the two own tables, so the kit has a width row (C2) that measures them at base and head and names the Revenue pages at 390 px (HPSMPOC-401's Done-when).

## Facts re-measured (instrument; control)
- Main `7365165d50193082ec3daf6eca137cd0ff0d4588` (`commits/main`, 15:01 re-read). Open PRs #245 b928, #246 b934, #247 b931, #248 b935, #249 b930, #250 b936, #251 b933, #252 b932 (`pulls?state=open`, 8 PRs, 45 file rows). Intersection with the 4 lane paths: 0 (per path `grep -c -x -F`; control: the same file list read 1 for `ActionPlanScreen.tsx`; and 0 names matching `revenue|OneCustomer`). `b937` (no PR) compare: 34 files, 0 matching.
- Panes (`tmux list-panes -a -F`) at 14:59: tuesday, H59, H63, H66, H68, G216-G220, fleet-monitor. `lsof` 9760-9769: 0 lines. Word scan of the 10-30 kits for `H70`/`B945`: none; `9760` appears only in the finished kit B916 line 23 ("B889/B890 9760-9779"). Load 10.32/14.02/14.00 at 14:59, 17.70 at 15:01.
- Files at 7365165d (tarball in scratch): `RevenueCalculator.tsx` 264 lines `8b01319f2629ebd2`, `RevenueResults.tsx` 145 `4a5aef2b63173a30`, `OneCustomerEstimate.tsx` 99 `d7d8fa4f14c236fb`, `revenue-words.ts` 8 lines, `Revenue.test.tsx` 169 lines `52695025cefd3d96`, 11 `it(`, 0 class assertions. Two `<table` in total (RevenueResults line 127, OneCustomerEstimate line 70). 0 occurrences of `Progress` in the three files. Non-ASCII per file listed in the kit (U+2192 x3, U+201C/U+201D x2 each, U+2026 x1).
- Model rows: C2 line 92, G2 line 109, G-cap line 111, L6 line 85 (`grep -n -i -E '^\| (C2|G2|G-cap|L6) '` printed those four). `models_latest.json` line 23 `claude-sonnet-5-5`.
- Jira (GET): HPSMPOC-384 and -402 both Backlog, 0 comments; -384 AC, scope sentence and Files line quoted verbatim in the kit; -402 hand-off 3 and its Done-when quoted; -401 (Note) and -392 (gather) read whole.
- Design file sha256 `fb799db8...e8afeaa` re-checked; `revenue()` is at its line 203 and is a single page with five inputs and a 65%/55% rule: the kit adopts only the look.

## Sweep pointers: all correct, two refinements
- Row H10's YOURS list (three screens) is right. "Sibling test files" resolves to ONE file, `Revenue.test.tsx`, which does not follow the `X.*.test.*` naming the sweep's partition rule assumes (the program would not have pulled it in); no other open PR touches it (checked).
- "Move the RevenueResults tables onto ui/Table" is accurate but the lane has TWO tables (Comparison in RevenueResults, one-customer in OneCustomerEstimate); the -402 "page bars" part has no instance in these three files (see Q-2).

## D-decisions (mine, in the kit)
- D-1 base `7365165d`, nothing to merge; no rebase if main moves again; an optional later merge only on Tuesday's word.
- D-2 `Revenue.test.tsx` and all other tests byte-equal (0 class assertions).
- D-3 the one-customer scroll wrapper stays a plain `div` (a `TableScroll` swap would ADD a region role, tabindex and an accessible name = a word and behaviour addition). `Comparison`'s wrapper is already attribute-for-attribute a `TableScroll`, so that swap is DOM-identical and is proved by program.
- D-4 no breakpoint moves without a 1024/1280 screenshot reason (these pages already use `xl:` for their columns, unlike the lists).
- D-5 no new word; CSS uppercase on the table head is not a word change.
- D-6 figures are proved by program (harness at base and head, browser comparison, plants p1/p2), using `textContent` not `innerText`.
- D-7 no committed Playwright spec; scratch config under `.tools/b945/`.
- D-8 target READY 150 min, hard stop 240 (the proofs are the heavy part).

## Q-questions for Tuesday (each with a default)
- Q-1 (money words): if the restyle would need ANY change to a figure, label, caption or scenario text, the seat STOPs. Default: keep the text byte-equal; the seat's STOP is a question, never an edit. (Already the kit's default; say only if you want the opposite.)
- Q-2 (-402 "page bars"): the three files hold no score bar; the bars on these pages are `BarChart` and `KpiTile meter` in `partner/parts.tsx` (H3's, landed, deliberately not on `ui/Progress`). Default: the seat does nothing about bars and writes it in FOR TUESDAY; Tuesday records "ruling: the chart bars stay" against -402 (or leaves the clause to the lane that owns `results/ResultsView.tsx`, H16).
- Q-3 (one-customer table region): default NO, keep the plain `div` (D-3). If you answer YES, the kit's STOP-shaped words change: allow `TableScroll label="One customer, table"` (one new accessible name; axe `scrollable-region-focusable` is the argument for it).
- Q-4 gate round: default round 1 of 2 on the class "revenue restyle".
- Q-5 (post-landing order): the seat's base is `7365165d`; open PRs #245 to #252 land in some order and change no file of this lane, so the gate needs no merge. Default: no merge unless a landing touches the lane paths.

## UNMEASURED
Test counts at main (no suite run); Chromium; how the two-column calculator and results layouts read beside the 228 px sidebar at 1024/1280; widths of the two own tables against base (HPSMPOC-401); whether the extracted-text harness runs all states in jsdom (the `Blob` capture and `useId` values are the likely snags; the kit says to mask ids and say so); CodeQL and CI on the new head; whether the whole non-live e2e suite fits the hard stop under today's load.

## Outside-the-fences disclosure
1. No fence breached. Scratch only under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/bac710bd-bbd2-4bfc-92fb-a9e7c76b9ed8/scratchpad/drafters/b945/` (tarball of `7365165d`, PR file lists). The tarball is extracted data, never executed. I printed the `gh auth status` header once (it shows the masked token prefix only, no secret value). No file written in the project's Briefs folder.
2. **The Write tool decoded a typed backslash-u escape in the kit** (line 53, the typographic-quote instruction): found by a python scan (1 non-ASCII line), repaired with a python rewrite that replaces every code point above 127 by its six-character escape text; after repair non-ASCII lines = 0. The kit also tells the seat to check the same on its own writes.
3. The kit file changed on disk between my write and my check (a notice said so); I re-measured after it and the counts above are of the final file.
