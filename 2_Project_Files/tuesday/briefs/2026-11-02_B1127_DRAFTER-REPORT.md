STARTABLE: YES (once stamped; no STOP found at drafting, 14:06 to 14:23 AEDT Mon 2 Nov 2026 by `date`)

# B1127 drafter report (kit B1127 / SEAT-G286, tier-1 Opus gate over `b1113/hpsmpoc-417-431-links-and-room` @ `d8a9456f`)

Kit `2026-11-02_B1127_SEAT-G286_hpsmpoc-417-431-gate-tier1.md`: 20,189 bytes (19.7 KiB; 20,000 is exceeded by 189 bytes, under 20 KiB; say if you read "20 KB" as 20,000 and I cut further), 8 lines with the four-underscore pattern (7 slots + last line; `.pre-stamp` control 8), 0 non-ASCII, 0 at-sign placeholders. Pane `Datasec/HPSM-POC-G286` (0 uses in any kit; control `G285` 9), ports 9530-9539, `BRIEF_SEAT_LEVEL=opus` inside the quotes.

## BLUF
One gate over both commits (head tree IS the landing tree while main stays `4b3cefae`). Gate re-derives the builder's 44 px census with its own instrument (19 widths, showcase UNSET as CI runs it, hit test and link-overlap added, "each link" mapped pointer by pointer to a reached state or NOT REACHED), the 17-width sentence figures including the loading state the builder did not test, no-word and accessibility-name equality, page-height and a defined "broken" list at 320 to 412, 7 own plants, both tickets, both open items, PRIOR WORK, landing files on GO. Round: the stamp wins over the READY line (Q-1).

## Facts re-measured (instrument, time)
- `gh api -X GET`: main `4b3cefae71ca43f6f86d23c77dd75ae101a51fd3` (tree `457b2a69`); head `d8a9456f...`; `compare` ahead 2, behind 0, merge base = main; commits `bb6619d1` (tree `0fde84c6`, parent main) and `d8a9456f` (tree `4d195136`, parent `bb6619d1`); 7 paths (5 + 2) = the builder's list; open PRs 0 (14:06).
- Round count, 14:08: 140 gate STATUS files with first line `GATE VERDICT`; "text-link 44 px" in 1 (B1072, GO WITH FINDINGS, NO GO 0 before); control "wake" 8. Builder READY line says "round 2 of 2"; B1113 stamp GATE-ROUND says NO GO 0, a NO GO here is the FIRST NO GO (not the cap, `model-routing.md:111`). Sentence class: new.
- Builder STATUS (113 lines): last line begins `READY FOR QA: B1113 ... @ d8a9456f...` (grep -c 1, control 0); `## PRIOR WORK` 1 (control 0). Builder numstat from `compare`: ClientPacks 1/1, EngagementOverview 4/4, ServiceReport 1/1, demo test 1/1, DocumentGeneration 1/1, new tests 221 and 91. Patch read: all 7 product lines are class-string additions; the one test edit is `ServiceReport.demo.test.tsx:217`.
- In-flight path sets (`comm -12` against the 7 paths from `compare` lists): `b1104` (24) 0, `b1097` (7) 0, `b1095` (4) 0; controls 7 and 24. Kits B1121/B1122/B1124/B1125/B1126: `grep -c -i -E 'ClientPacks|EngagementOverview|ServiceReport|DocumentGeneration|residualLinks'` = 0 each (control B1113 kit 12). Panes 14:23: `tuesday`, `HPSM-POC-H102`, `-H103`, `-H101`, `-G285`, `Datasec/MPS-G283`, `Datasec/MPS-M76`, `fleet-monitor`. G285 (B1121) lands 24 paths on the same main: if it lands first, main moves and the kit's MAIN-MOVE rule applies (property, not a path list).
- Ports: `lsof -nP -iTCP:9500-9999` listeners at 14:07 were 9571-9573 only (H101); 9530-9539 lsof 0 at 14:11 and 14:23 (control 9570-9579 4 rows). Word-bounded scan (`-w -E '953[0-9]'`, B1122's method) over the 128 non-`.pre-` SEAT kits of 11-01/-02: 0 before my kit existed, 1 after (my own kit only, checked by name); control `957[0-9]` 2 then 3. 9510 and 9540 were also free; I took 9530 because a parallel drafter would likely pick the first free block (9510). Taken per your note: 9560-9589, 9720-9739.
- Tickets read by Jira GET through `.tools/b1007/jira.py` (`importlib` from a scratch script; token never printed), 14:08: 417 "Done when: each link is at least 44 px high at the sizes the gates measured, or the item is recorded as declined. Which links are built is a scope call that is not made here." 431 "Done when: the sentence has room beside the button at 360 and 375 px and no word runs over it, or the item is recorded as declined. ..." (both Backlog).
- Landing rule: `CLARIFICATIONS.md:3617` in `datasecau/HPSM-POC-analysis` (5346 lines now; 5319 at B1107; line 3617 unchanged) reads "The landing form is a head-pinned squash".
- CI: `ci.yml` at main 679 lines; web jobs at `:371 :396 :409 :413 :426 :395 :450 :478 :483 :526`; SHOWCASE grep 1 hit, a comment about `showcase.sh` (the builder's census ran `HPSM_SHOWCASE=on`, CI and the e2e specs do not); `audit-dev.mjs` runs at `:395` under `working-directory: web` (`:377`).
- Model: `models_latest.json:17` `claude-opus-5-5`; `model-routing.md:108` G1, `:111` cap. Drive 30 GiB free; load1 14.50 (14:06), 6.92 (14:09), 13.31 (14:23).
- Severity lines were put against every step (2 words/names, 3 census/hit/overlap/pointers, 4 sentence/guard/loading, 5 broken list, 6 tests, 7 plants, 8 tickets/items, 9 landing text, 1 paths). REFUSE lines were each run against the live state at 14:11 (G286 pane absent, H100 absent with `-G285` control 1, head unmoved, READY line 1/0, PRIOR WORK 1/0, `.tools/b1127` and `wt-b1127-*` absent with `.tools/b1113` control present, 9530 block free, model line); none fires.

## D-decisions (mine, for you to accept or strike)
- D-1 Own instrument runs with showcase UNSET (CI's setting), because the builder ran `on` and Home vs Customers sign-in differs; the gate says whether any state needs `on`.
- D-2 Census adds two things the builder did not do: a hit test (top+2, middle, bottom-2) and link-box overlap, and two extra widths (600, 1920): an `inline-flex min-h-11` link inside a row could be 44 px high and still be covered.
- D-3 "Broken" for step 5 is defined as a list NEW against base (scroll, past-edge, overlap, clipped text, unreachable action, misaligned row, Generate button separated from its reason, screenshots read). Plain growth is a Note.
- D-4 417's done-when is graded against the pointer table (every `<Link>`/`<a>` of the four files to a state or NOT REACHED); a pointer with no state bars a GO. 431 is graded MET-ON-A-READING because the head puts the button BELOW the sentence at 412 and narrower, not beside it (builder FOR TUESDAY says so; the done-when says "beside"). Never a finding.
- D-5 Loading state tested (builder NOT TESTED list): `not-empty:basis-60` gives the column a basis while the loading line renders, so the button can jump when it resolves; graded Minor only if jarring.
- D-6 Plants p1 to p7 are chosen to attack what the builder's rows might not pin (p1 `items-center`, p5 `basis-56`, p6 `min-w-0`); p2 and p4 also rebuilt through the census; builder's PL/PD plants are not remade.
- D-7 Showcase and audit-cwd items: drafter read says neither matters to this landing (CI has no showcase; CI runs `audit-dev` in `web`); the gate re-derives.
- D-8 Load discipline: B1121's RULE L (heavy-slot dirs, two reads two minutes apart, 120-minute wait cap, red re-run ALONE 3 times) plus: census one context and one page at a time, never beside a build.

## Q-questions (each with a default)
- Q-1 The builder READY line says "round 2 of 2"; your stamp says NO GO 0, round 1 of 2 counting NO GO rounds. Default: stamp wins, said so in the kit; a NO GO is a forward fix round, not the cap, and the sentence class is separate.
- Q-2 Port block: 9530-9539. Default yes (9510 and 9540 spare).
- Q-3 Size 20,189 bytes (under 20 KiB, over 20,000). Default accept; otherwise I cut the COUNT FLOOR line and step 9's PR-text detail.
- Q-4 The 431 reading ("beside" not built). Default: MET-ON-A-READING, you rule scope; no code change asked of anyone.
- Q-5 df 30 GiB with the STOP at 25 GiB leaves about 5 GiB for two installs and builds. Default: the seat stops at 25; the builder's trees (2.4 GB, `.tools/wt-b1113-*`) stay until you say.
- Q-6 If G285 lands first the merged tree changes. Default: the gate follows MAIN-MOVE (property), not the path list.

## Contradictions found
1. READY line "round 2 of 2 ... (NO GO 0 before)" vs stamp "NO GO 0, first NO GO would not be the cap" (Q-1).
2. Builder: "Open the PDF (two places)" in its census vs one `<a>` for it in `ServiceReport.tsx` (`:169`; `:159` is the download link): the gate settles it.
3. Builder census ran `HPSM_SHOWCASE=on`; CI does not.
4. 431 "room beside the button" vs button below the sentence at 412 and narrower.
5. Builder says drive 37 GiB free at its last read; 30 GiB now.
6. Builder BLUF "7 changed lines, 6 + 1": numstat gives 7 product lines (4 + 1 + 1 + 1) plus one test line; consistent, no conflict.

## UNMEASURED by me
No build, browser, test or plant was run. Not measured: every height, column, hit-test and overlap; whether `not-empty` renders as the builder says in the production CSS; the loading jump; whether the 29 states cover every pointer; the 3826 and 3811 counts; the 5 specs' result; hosted CI and CodeQL; Jira ticket state beyond Backlog; the live-API specs. The builder's tables are claims.

## Outside the fences
None. Reads only: DRAFTER_RULES, the B1113 kit, the B1113 STATUS (113 lines), B1107 and B1121 kits (whole), B1122/B1124/B1126 kits (head lines and port/branch greps), `gh api -X GET` (compare, refs, commits, raw files at head and main, the records `CLARIFICATIONS.md`), two Jira GETs through the project's helper (output to scratch, only "Done when" and status lines read), `tmux list-panes`, `lsof`, `uptime`, `df`. Scratch files only in the session scratchpad. No decision_queue, no Azure, no mail, no write outside the two files.
