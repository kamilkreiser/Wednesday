STARTABLE: YES (once stamped; no STOP found at drafting, 18:11 to 18:20 AEDT Mon 2 Nov 2026 by `date`)

# B1147 drafter report (kit B1147 / SEAT-G291, tier-1 Opus gate, ROUND 2 OF 2 on class "customer-page text-link 44 px targets", over `b1113/hpsmpoc-417-431-links-and-room` @ `d654fbb7`)

Kit `2026-11-02_B1147_SEAT-G291_hpsmpoc-417-431-links-gate-tier1-r2.md`: 32,539 bytes (about 31.8 KiB; B1127's was 21,239 and B1130's 22,171). 8 lines with the four-underscore pattern (7 slots + last line), 0 non-ASCII, 0 at-sign placeholders (programs, 18:19). Pane `Datasec/HPSM-POC-G291` (0 kits use G291; control G290 1), ports 9520-9529, `BRIEF_SEAT_LEVEL=opus` inside the quotes, model `claude-opus-5-5` (`models_latest.json:17`), row G1 `model-routing.md:108`, cap `:111`. The `.pre-stamp` copy was not left beside it (Tuesday makes it at stamping; I made one by mistake and moved it to the scratchpad).

## BLUF
Round 2 gate that re-measures B1127-1 (24 px link), B1127-2 (row alignment) and B1127-3 (count sentence) at the new head on the merge with main (head is 1 behind, main unmoved at `5f128fb`), with a census of 51-plus states x 19 widths derived from the render code, not from the builder's list, and a reconciliation of the builder's states against the gate's. Grades the title-to-detail gap by a number (expected growth = the 44 px box minus main's line box) and does not ask the product owner. NO GO is the cap and writes `residue.md` (closed instances, open instances one paragraph each, no ids); GO writes four landing files that must not repeat "none is under 44 px" (grep predicate with a control) and carry the corrected count with its frame, builder figures only where reproduced.

## Facts re-measured (instrument, time)
- `gh api -X GET`, 18:11: branch ref `d654fbb7...` (tree `707e21f4`); main `5f128fb8...`; `compare main...branch` ahead 3, behind 1, base `4b3cefae`; commit 3 = 3 paths; open PRs 0; `compare 5f128fb...main` 0 commits. The other 4 paths' blobs are not compared by me (the kit makes the gate do it).
- Round count: 143 gate STATUS files with first line `GATE VERDICT` (program, first line only); "text-link 44 px" in 2 (B1072 GO WITH FINDINGS, B1127 NO GO); control "wake" 8. B1127 last line read: `NO GO (round 1 of 2 on both classes)`. So links class: NO GO 1 of 2 before; sentence class: 0 of 2. The builder's own READY line says "ROUND 2 OF 2 ... NO GO 1 of 2 before: B1127"; it agrees.
- Pointers: every `file:line` in the kit printed by `grep -n` over the raw files fetched at `d654fbb7` (ClientPacks, EngagementOverview, ServiceReport, DocumentGeneration, the new test file) between 18:13 and 18:17, then pasted. Not re-printed: `EngagementOverview.tsx:204` (B1127's table has it; my grep pattern did not show it), so the kit does not cite it.
- Panes 18:1x: tuesday, NexusAI-N90, MPS-M78, MPS-M79, Security-Composer-C80, HPSM-POC-G289, HPSM-POC-G288, fleet-monitor (H104 and G286 absent). Live HPSM seats: G288 (`b1097`, `f9f1f490`, 8 paths) and G289 (`b1095/hpsmpoc-wake-close-path-and-narrative-pins`, `76116bc6`, 4 api paths). Disjointness by `comm -12` of `compare main...<branch>` file lists vs the 7 paths: b1097 0 of 8, b1095 0 of 4, control self 7.
- Ports: `lsof -nP -iTCP:9520-9529 -sTCP:LISTEN` 0 rows (control 9540-9549: 4 rows). Word-bounded perl scan `(?<![\w-])952[0-9](?![\w-])` over 147 non-`.pre-` SEAT kits of 11-01/-02: 0 (control `957[0-9]` 1). A first, unbounded `grep -w` scan read hash noise (6 lines of commit ids and a 9650-9669 fallback in an old MPS kit that says "Ports: NONE"); ranges such as `9470-9529` and `9490-9599` appear in older kits as scan ranges, not reservations. 9510-9519 (G289) and 9530-9549 (G288) are named taken in the kit. After the kit existed the bounded scan reads 3 hits of `952x` (9520, 9521, 9522: my own kit; the pre-existing count was 0).
- CI: `ci.yml` at main, 679 lines; `:371 :377 :395 :396 :409 :413 :426 :450 :478 :483 :526` printed by grep. Landing rule: `CLARIFICATIONS.md:3617` in `datasecau/HPSM-POC-analysis` `1_Project_Definition/` (5371 lines), line read by `awk NR==3617`: "The landing form is a head-pinned squash".
- `df -g /Volumes/Laptop-DEV` 273 GiB available; load1 8.35 / 9.45 / 10.49 at 18:15.
- Builder STATUS read whole (B1132, 115 lines) and B1127 STATUS whole (177 lines). Every builder count in the kit is marked RELAYED.

## D-decisions (mine, accept or strike)
- D-1 Three builds are REQUIRED (main, `d8a9456` merged, landing tree), because the landing text must carry a corrected count "from YOUR runs" and the 4-state, 76-reading figure at `d8a9456` is the builder's. Costs one extra build.
- D-2 Step 3 reconciles the builder's state list (a claim) against the gate's derived list and demands "states you opened that the builder did not". It names new axes: wrapped activity titles at 320, no activity, the `/playbook` branch B1127 left untested, report-list loading and failed, the menu open.
- D-3 The gap is graded by a number, not by taste: expected growth = 44 px box minus main's line box; a row differing from that by over 2 px is Major; a closer or overlapping detail line, or a part-covered link, is Blocker; growth equal to expected is Note, or Minor if the screenshot pair reads as a visible "two rhythms". The declined shapes are not built; optional re-run of the builder's 620 and 244 figures stays out of the verdict.
- D-4 The builder's own limit "the pack's no-report link sits 10 px lower than its line in 42 of 76 readings" is a NEW difference caused by the fix (0 of 76 at the previous head). The kit makes the gate decide whether it is an offset (neighbour on the row, B1127-2 rule) or a gap growth (own line), and say which.
- D-5 Sentence class: NO GO 0 of 2, not re-judged, blobs proved equal to `d8a9456`; its figures are re-measured only for the landing text. A finding there is that class's first NO GO, not the cap.
- D-6 Hard stop 150 / 210 minutes (B1127 was 180 / 240) because the work is a re-measure on a known instrument; outer bound is the stamp's slot, not 20:00.
- D-7 q-plants q1-q7 attack the three fix lines (`ClientPacks.tsx:184`, `EngagementOverview.tsx:221`, `:241`); q1, q3, q4 also built and censused so the alignment measures are shown to move.

## Q-questions for Tuesday (each with a default)
- Q-1 Size 32,539 bytes, over the 20 KiB convention the B1127 drafter followed. Default: accept (two jobs: a re-measure of three findings and a landing/residue fork). Otherwise I cut step 7 and the optional shapes.
- Q-2 Port block 9520-9529. Default yes (spare 9660-9669 was my second pick).
- Q-3 Outer bound clock for S5. Default: your call at the stamp; the launch is after 18:20 and load1 is 8 to 10, so 21:00 or 21:30 as for G288/G290.
- Q-4 The `:158` route is reachable only by a crafted held session per the builder; the kit has the gate read the code and call it a Note either way, a link under 44 px in it is Major. Default yes.
- Q-5 Three tree builds with a shared `node_modules` clone: if B1132's trees were removed by R136 before launch, the gate needs its own `npm ci` (about 600 MB). Default: it takes the install under RULE L.

## Contradictions found
1. Builder "main 39 distinct own links under 44 px" vs B1127 "25 distinct" (different state sets and keys); the kit has the gate print both keys.
2. Builder "`:158` REACHED" (crafted session) vs B1127 "NOT REACHED"; kit step 3.
3. Builder says `pk-a-3-withheld` renders the link; its own `pack3-service-withheld` row did not (UNMEASURED by the builder why); the gate's reconcile in step 3.
4. Builder commit 3 message ends "Rows: 8 new ... 3826 to 3834"; B1127 said the older head had 15 new rows; 15 + 8 = 23 added names against main (kit step 8).

## UNMEASURED by me
No build, browser, test or plant was run. Not measured: any height, offset, gap or hit test; the 3834 and 3848 counts; the four blobs equal to `d8a9456`; whether `:158` is reachable by a normal flow; the Jira text of 417 and 431 (relayed from B1127); hosted CI and CodeQL; the builder's trees' presence on disk.

## Outside the fences
None. Reads only: DRAFTER_RULES, the B1127 and B1130 kits and B1127 report, B1127 and B1132 STATUS, `brief_seat.sh` line 24 (by `awk`), `gh api -X GET` (refs, compare, commits, org repo list, raw file contents of five source files, `ci.yml`, the records `CLARIFICATIONS.md`), `tmux list-panes`, `lsof`, `df`, `uptime`. One failed `gh api -X GET` (404 on a wrong records path) and one hook refusal on a `cd` in my first call (no effect). Scratch files only in the session scratchpad. No decision_queue, no Azure, no mail, no write outside the two files.
