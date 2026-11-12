STARTABLE: YES (after the Stamp; every slot is left as four underscores and every default is HOLD)

# B1539 drafter report (SEAT-R222, HPSM-POC records: ticket the held messaging-map rows)

Drafter session s272, 2026-11-12, started 11:3x AEDT, kit written 11:4x (end clocks by `date` at the foot). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1539_SEAT-R222_hpsmpoc-messaging-held-tickets.md` (472 lines, 87588 bytes).

## BLUF
- **16 held items in 9 tickets.** The map holds **15 rows** (13 C rows + the 2 D rows K2 and K3); the coordinator's list of 16 names differs by exactly one: **`H6b` is not a row of the map** (see "Difference" below). It is the held half of map row H6, held out of the text pass by the builder's kit. Ticket T9 covers it conditionally (my recommendation: slot HOLD until the builder's result shows it still unbuilt).
- 9 tickets: T1 landing copy + hero block (C-landing, H-hero); T2 journey rename + Training labels (C-rename, C-training); T3 customer report introduction + Next Engagement section (R6, R7); T4 operating modes + Phase 3 naming (C-modes, C-phase3); T5 Good/Better/Best packages page (C-gbb); T6 commercial stages + success metrics (C-stages, C-metrics); T7 coach opener (C-coach); T8 deck sentences + firmware question + deck voice (C-deck, K2, K3); T9 Illustrative tag title attribute (H6b).
- **Search-before-create found one expected duplicate target: T5 should become ONE comment on the open HPSMPOC-392** ("Good / Better / Best: packages page, pricing reading of the words ...", Backlog, needs input). Everything else is nearby tickets only (listed as "related" in each body).
- Each ticket: summary printed length (202, 231, 186, 192, 211, 195, 158, 208, 211; all under 255), BLUF/Recommendation/Detail body that quotes the map row(s) verbatim, the source-document lines verbatim, the D-item, the hold reason, the map's question and default, a marker, labels, phrase searches and a HIT rule. At most 9 writes, one per ticket, create OR comment. Nothing moved, closed, built or re-labelled. C-entry (expected C-366) records the 11:21 ruling.
- Stamp slots (JIRA, T1-T9, RECORDS, REC-MERGE, RULING-1121 and the rest) are four underscores. Nothing in the kit is written as Tuesday's read.

## Difference from the coordinator's list (stated, not trusted)
The list: C-landing, H-hero, C-rename, C-training, R6, R7, C-modes, C-phase3, C-gbb, C-stages, C-metrics, C-coach, C-deck; K2, K3; H6b. Against the map: the 13 C rows are exactly these 13 (instrument below); K2 and K3 are the only D rows the map holds (the other 9 D rows ship in qualified form); **`H6b` has no row in the map** (`grep -c 'H6b'` over the map = 0; control `grep -c 'H6'` = 5). It appears in the builder's kit (B1535, line 12 and line 169: "H6a (the tile sub line) is built; H6b (the title attribute) is HELD `NEEDS-SHARED web/src/components/partner/parts.tsx`"). So: 15 map HOLD rows, plus 1 builder-held half-row = 16 items.

## Facts re-measured (instrument, control)
| Fact | Instrument | Control |
|---|---|---|
| Map class counts A 22, B 13, C 13, D 11, total 59 | `awk -F'|'` over the map's table rows (last cell trimmed); printed per row | the map's own BLUF prints the same four numbers |
| HOLD rows = 13 C + K2, K3 = 15 | same awk listing, C rows and D rows named | 13 C ids listed = the coordinator's 13; D ids: K2 K3 P4 P6 R1 W10 W5 W6 W8 W9 W17 = 11, of which the map says 9 ship (P4 P6 R1 W5 W6 W8 W9 W10 W17) |
| Board 470 issues, highest key HPSMPOC-470, Done 347 / Backlog 120 / In Progress 3 | own GET-only helper, `search/jql` `project = HPSMPOC AND (key >= HPSMPOC-1)`, paginated | earlier drafter's 11:25 export also 470; board has not moved |
| Labels on board: `messaging-2026-11-12` 0, `next-phase` 3, `gather` 7, `awaiting-hp` 9, `follow-up` 6, `needs-kam` 16, `catalogue-2026-11-09` 13 | Python Counter over the export | export includes labels field for all 470 |
| Jira text index: `qqzzxx9` 0; `REC-LAND4-461-11NOV` = HPSMPOC-461 | helper phrase search | both fired as expected |
| The 11:21 words not on any ticket | phrase searches "ticket anything left for later" / "messaging mapping looks good" / "deploy based on this": 0, 0, 0 | positive control 461 above. So the ruling is RELAYED only; it lives on the board chat, not in Jira |
| Code main `c717ba1a945191ffa31f13320c19967a6cf7f15a` | `gh api -X GET repos/datasecau/HPSM-POC/commits/main` under the project GH_CONFIG_DIR | equals the map's sha |
| Records main `75ae17d5b0bf438f5855527626c0a22a51da07c7`; CLARIFICATIONS.md 6276 lines, 2060302 bytes, 365 headings, newest C-365 at 6263; `### C-263 ` at 5114; open analysis PRs 0 | `gh api -X GET` raw read, awk/grep | C-263 found once; R219's STATUS last line names the same sha as its merge of #198 |
| Expected entry number C-366 | highest heading + 1 | stated "derive again by program" |
| Phase decision document: `grep -i -c -E 'landing|hero'` = 0 | /usr/bin/grep -i -c | same pattern over the map = 10; `talk track` over the document = 3 |
| File sizes: map 267 lines, source text 302, decision document 1872 | `wc -l` | n/a |
| Panes at 11:38: `Datasec/HPSM-POC-H161`, `Datasec/HPSM-H160` live; both kits say no Jira write, CLARIFICATIONS named once | `tmux list-panes -a -F`, `grep` of the two kits | control: the same list prints the named panes |
| Disk free 1271 GiB; no B1539 file before mine | `df -g`, `ls | grep -c B1539` = 0 | n/a |
| Every quoted `CODE:` fragment in the nine bodies is a substring of the map or the source text; body sha256 and summary re-extracted from the written kit equal the generator's | Python substring check over the kit as written | all 9 True; not-substring count 0 for each; a one-character mutant is not tested (UNMEASURED for the control, see below) |
| Ban scan over the nine bodies and summaries: 0 problems, 0 prose `HP` outside the exemptions | `gen.py` regexes, underscore-aware | planted `entry C-9999`, `B170`, `Tuesday`, `gate`, `_by_Kam_`, `C-347`, `.NET`, prose `HP`: all fired |
| Non-ASCII in the bodies: U+2014, U+201C, U+201D, U+2192 only (from the source lines). The source text's `&amp;` (lines 3, 282) is shown as `&` in the one affected quote (line 282, T6) and the body says so | Python census | n/a |

Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s272/d1539/` (`jira_get.py` GET-only copy, `gen.py`, `kitgen.py`, `board.json`, `tickets_block.json`, `clar_now.md`, `pull.py`, `srch.py`, `show.py`, `s2.py`).

## D-decisions (mine, reversible at the stamp)
- D1 Grouping 9, not 16, by the creation rule in the brief (one ticket per logical path; group what one test pass proves; split only separate workloads). The two least obvious: T4 groups C-modes with C-phase3 (same pair of partner-showcase JSON files, one content version) and T6 groups C-stages with C-metrics (the metrics count the stages). T8 groups C-deck with K2/K3 (same hash-pinned deck file, one new content version).
- D2 Labels from board practice, because JIRA.md and CLAUDE.md hold NO label or creation rule (checked, they hold only the key, the issue types, the board id and the BLUF format): every create gets `messaging-2026-11-12` (new, modelled on `catalogue-2026-11-09`); `next-phase` where the phase document's D-item is Next phase or none; `gather` (needs input) on T1 and T3; `awaiting-hp` on T8; `follow-up` on T9. Type Task, no parent/link/priority/assignee.
- D3 T5 is a comment on HPSMPOC-392, not a new ticket. Reason: 392 is open, decides the same page (the packages page), and the board's catalogue ticket HPSMPOC-456 also carries it as item P2-070. The kit makes two hits a STOP for that ticket, so the seat never chooses.
- D4 Verbatim quoting beats the "no HP as a word" scan: the earlier records kits ban `HP` in Jira prose. The task needs rows quoted verbatim, and the map's rows and the source lines contain HP. Resolution in the kit: `HP` is exempt on `CODE:` lines and in the exact product names; banned in summaries and prose; the drafter's scan passed with 0 hits. (The board's own Phase 2 catalogue tickets 449, 452, 456 carry the word in descriptions, never in summaries, measured 0 in all 31 summaries from key 440 to 470.)
- D5 The phase decision document is named, never ticketed: each ticket names the D-item beside its held row. The existing partner-pages catalogue (HPSMPOC-448 to -460) is not touched unless it is the single T5 hit.
- D6 Three absence claims are RELAYED from the map (no landing/about/marketing page, no report introduction, no coach slot); the kit makes the seat re-measure each at its code main with a control, and drops the sentence if it fails. The fourth (phase document has no landing/hero item) I measured (0, control 10 and 3).

## Q-questions for Tuesday (each with a default)
- Q1 Grouping: nine tickets as drafted, or sixteen, or something between? Default: nine (D1). A different grouping changes the frozen texts, so it needs a re-draft, not a seat decision.
- Q2 Labels (D2): confirm `messaging-2026-11-12` and the `next-phase` / `gather` / `awaiting-hp` / `follow-up` mix. Default: as drafted.
- Q3 T9 / H6b: file it now or wait for the builder? Default: slot HOLD; the kit already refuses to write it unless the builder's `## HELD` still shows H6b unbuilt. Note H6b is the only item whose existence depends on a pane still running (the minimatch pane H161 is unrelated).
- Q4 R7 is D-019, which the phase document recommends THIS PHASE (a ruling, not work), and K2/K3 ride with D-004 to D-006 (THIS PHASE, needs an HP SME). The product owner's 11:21 words say "ticket anything left for later". Default: ticket them as held, and say plainly in the ticket that the phase document recommended this phase and the 11:21 instruction puts it later. If Tuesday would rather ask the product owner whether the this-phase recommendation stands, T3 and T8 should be HOLD at the stamp.
- Q5 D-item links in the map are loose in two places and I wrote the true readings into the tickets: D-064 as the phase document reads is the rail heading/numbering/Metrics-apart item (cosmetic), not the Discover/Assess/Recommend/Engage rename; D-059 is "Automation metrics: add four summary tiles", not the document's success metrics (MA 281-287). Default: keep my wording ("the map links ...; neither names the rename itself"). Should the map's link be corrected?
- Q6 Items left that are NOT map rows: the document's off-site assets the map says are "not on the site, so not mapped" (EDM sequence, executive overview, seller talk-track document, Appendix A variants, MA 180-191, 290-303); the approval of "HP-aligned, product-validated recommendations" (map question 9); P6's "SIEM integration if available" (question 11); and questions 12-13 (Home lead, snapshot vs assessment naming). Default: NOT ticketed (the brief says "every HELD row"). If "anything left" should include them, say so and I will add a tenth ticket to the kit.
- Q7 Records: C-entry numbered C-366 for the ruling, written through a records PR by B1523's route (REC-MERGE FF). The tickets carry no entry citation, so RECORDS HOLD leaves the tickets unchanged. Default: RECORDS WRITE, REC-MERGE FF. Is a separate entry warranted, given R219's pattern, or should the ruling be folded into the builder's later records pass? Default: separate.
- Q8 The kit includes a `RULING-1121` slot for the exact words and clock as Tuesday read them (the drafter was relayed them and could not find them in Jira). Default: Tuesday fills it from the board.

## UNMEASURED
- The 11:21 words themselves (only relayed; not in Jira).
- The `+1 character mutant` control for the substring check (my substring check printed all True; I did not plant a mutant). The kit makes the seat run it.
- The three absence claims (D6) at the code tree: relayed from the map, not re-measured.
- Whether `labels` accepts the new label `messaging-2026-11-12` on create without a project label whitelist (not tested; a create is a write). The kit's read-back and the stop-at-first-non-2xx rule cover it.
- The T5 outcome until the seat reads HPSMPOC-392 whole (I read its summary and first 1200 characters only).
- Whether the builder (B1535, still `PROGRESS ... HOLD` at 11:18, 11 lines) will hold any further row: the kit has the seat read its `## HELD` and name differences.

## Outside-the-fences disclosure
- Read: the drafter rules, the map, the source text (via numbered print and Python), the decision document (D-item table rows and the sections of D-004/005/006/019/023/024/027/043/047/056/058/059/064/069 only; two `grep`s), the two template kits, `JIRA.md`, `CLAUDE.md`, the builder kits B1535 and B1538 (grep and sed excerpts only), B1535 STATUS (11 lines) and B1523 STATUS (last lines), `model-routing.md` lines 97 and 110 (grep), `models_latest.json` (grep), `brief_seat.sh` (grep), the previous drafter's `jira_get.py` (read whole, GET only; copied to my work folder) and head of its `clar.md`.
- Jira: GET only through my own copy of the helper (JQL always `project = HPSMPOC AND (...)`), credentials read in-process, never printed. No write of any kind.
- GitHub: `gh api -X GET` only, under the project `GH_CONFIG_DIR`: code `commits/main` (sha), analysis `commits/main` (sha), analysis `pulls?state=open` (count 0), and one raw read of `CLARIFICATIONS.md` into my work folder (`clar_now.md`).
- `tmux list-panes` (read). No decision-queue command, no card, no `briefs_staged`, no scoreboard, no ledger, no WEDNESDAY/FRIDAY tree, no other project. No project file edited. No mail, chat or publish tool used. Two files written under the briefs folder (this report and the kit) plus scratch files in `fleet/state/s272/d1539/`.
- One slip, caught: I ran a `cd`-containing command once early (the hook refused it, nothing ran).

End clock: Thu Nov 12 11:44:50 AEDT 2026 (by `date`).
