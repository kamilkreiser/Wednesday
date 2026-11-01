STARTABLE: YES
# B1113 DRAFTER REPORT (kit: `2026-11-02_B1113_SEAT-H100_hpsmpoc-417-431-links-and-room.md`, unstamped; reads 09:51:17 to 09:58:49 AEDT by `date`; routing row C8)

## BLUF
Builder kit for seat H100: HPSM-POC, branch `b1113/hpsmpoc-417-431-links-and-room` from main `4b3cefae71ca43f6f86d23c77dd75ae101a51fd3` (main MOVED from `c1457349`: pull request 274 landed, 8 files, 0 overlap with this lane), two commits on disjoint groups, Sonnet row C2 (`model-routing.md:92`), gate G1 tier 1 on Opus (`:108`), port block **9560-9569**. Commit 1 (417 residual): `ClientPacks.tsx`, `EngagementOverview.tsx`, `ServiceReport.tsx`, a new `residualLinks.targets.test.tsx`, and one literal in `ServiceReport.demo.test.tsx`. Commit 2 (431): `DocumentGeneration.tsx` (classes only) and a new `DocumentGeneration.room.test.tsx`. Layout classes only; any word needed is `STOPPED: NEEDS TUESDAY`. The header logo link is excluded. Both done-whens are quoted in full. The kit requires a real-browser census (chromium, own script, not committed) at base and head, red-first rows, 9 plants of the seat's own (5 link, 4 sentence), READY FOR QA with a PRIOR WORK section. **Size: 45.9 KB, over the 30 KB target** (Q-4).

## Facts re-measured (instrument, control)
- Main `4b3cefae...` by `gh api -X GET git/ref/heads/main` at 09:51:27 and again 09:58; open PRs 0 (pulls list printed no row); `matching-refs/heads/b1113` 0, control `b1097` 1. `compare c1457349...4b3cefae`: ahead 1, 8 files (all `feedback/`, `partner/`, `customer/CustomerManagement*`); the kit's main-moved pattern over it = 0, control (one-line file holding `customer/ServiceReport.tsx`) = 1.
- Pointers (all printed by `grep -n -F` or `awk NR==n` over raw files at main in scratch): ClientPacks `:201` link, `:184` candidate; EngagementOverview `:71` step link, `:241` activity link, `:192`, `:221`, `min-h-11` at `:49 :54 :139 :181`; ServiceReport `:169`/`:170`; DocumentGeneration `:144`, `:145`, `:156`, `:157`, `basis-60` at `:113`; tests `ClientPacks.test.tsx:153`, `ClientPacks.restyle.test.tsx:121`, `ServiceReport.demo.test.tsx:217`, `ServiceReport.withheld.test.tsx:61`; `ci.yml` `:371 :396 :409 :413 :426 :450 :478 :483 :515 :526`; routing `:92 :108 :109`; models `:23`; `brief_seat.sh:24`. Premise counts each 1, zero control `NOSUCH-zz-b1113` 0.
- Jira GET (jira.py, both tickets whole): 417 has 1 comment (03:05 records note), 431 has 0; done-whens quoted in the kit. The gate B1072 first line read: `GO WITH FINDINGS ... round 1 of 2 on class "customer-page text-link 44 px targets and the Home tile label"; NO GO 0 before`; its evidence gave the 11 census widths and the word table (3 states x 17 widths, 17 widths not enumerated).
- Landing: records `CLARIFICATIONS.md:3617` still reads "The landing form is a head-pinned squash" (5319 lines, analysis main `95735305`).
- **Port block 9560-9569:** `lsof` = 0 (control: a `python3 -I -B` listener on 9569 printed 2, then 0). Word scan `grep -l -w -E '956[0-9]'` over the 111 non-`.pre-` SEAT kits of 2026-11-01 and 11-02: 0; over every file of those dates in `tuesday/briefs/`: 0; control `972[0-9]`: 8 hits. One kit of 10-31 (finished gate B989) names 956x. Blocks 9500-9549, 9570-9599 all had hits or 10-31 hits; 9550-9559 is B1109's. After writing, this kit itself now names 956x (expected).
- REFUSE lines run live: stamp slots 11 lines (control: this is the unstamped copy, the REFUSE expects 0 after stamping); `@X@` 0; last line `READ-WHOLE-BY-TUESDAY: ____` (the line fires until stamped, as designed); main moved: 0 hits; `b1113` ref 0; `.tools/b1113` and `wt-b1113-*` absent, control `.tools/b1090` present; panes `^Datasec/HPSM-POC-H100$` 0, control `^Datasec/MPS-G[0-9]+$` 3; ports 0; project account logged in; node v24.21.0 at `.tools/node24`, `.tools/ms-playwright` holds chromium.
- Partition: kit-name scan of the 111 SEAT kits for the four component names finds only finished kits (B1059, B1072, B1073, B1079, B1090, B1102 and records seats); B1104, B1107, B1108, B1109 hold 0. `compare main...b1097/hpsmpoc-home-words-focus-ring` (pushed, ahead 2, behind 1): 7 files, pattern hits 0. No HPSM-POC pane live at 09:55.
- e2e specs naming the changed elements: by `grep -l -F` over the 57 files (listed in the kit); `toHaveScreenshot` in 0 files.

## D-decisions (defaults apply if silent)
- D-1 Seat H100, B1113, Sonnet, G1 on Opus, ports 9560-9569; launch line copied from B1097/B1104 with `BRIEF_SEAT_LEVEL=sonnet` inside the quotes (the DRAFTER_RULES `cockpit.sh add` form is what `launch_when_cool.sh` runs).
- D-2 Precedent over invention: jsdom class-pin rows like `parts.targets.test.tsx` plus an uncommitted browser census, no e2e file (the sweep lane and PR 272 did the same).
- D-3 The extra under-44 links found in the property's own files are built; those in other files are listed, not fixed.
- D-4 Targets READY 180 min, hard stop 270 min (the census at 2 trees x 17 widths dominates).
- D-5 Sentence fix candidate `basis-60` on the `:145` column (seat measures; falls back to the next smallest class change; none passes = STOP with the table). Property: no word over the button or past the column at 17 widths, column at least 200 px or the button on its own line, rectangles within 1 px of main at 768 and wider where main had room.

## Q-questions for Tuesday (each with a default)
- Q-1 Round count: B1072 was GWF round 1 on class "customer-page text-link 44 px targets", so this gate is round 2 of 2 on that class (the cap row `:111`), NO GO 0. Default: as the kit says; tell me if you reckon the Home-tile half made it a different class.
- Q-2 The 17 widths of the gate's sentence table are not printed anywhere I could read. Default: the 11 plus 320, 340, 350, 375, 380, 400.
- Q-3 Row growth: `min-h-11` on the step link and activity link grows each `li` (they carry `py-2`) by up to about 16 px; the kit allows the growth, forbids reducing padding to hide it, and makes the seat report it. Default: allow, as PR 272 did for the crumbs.
- Q-4 Size 45.9 KB against the 30 KB target (B1104 was 42.6 KB, B1097 60 KB). Default accept. Cuts that remove checks, not prose: Step 10 (d) to (g) duplicates, plants PL5 and PD3.
- Q-5 Port block 9560-9569: default accept.
- Q-6 The kit names the demo test's `outerHTML` literal as a permitted edit to an existing row; default yes.

## Contradictions found
1. Main is `4b3cefae`, not `c1457349` (the sweep's pin): PR 274 landed; none of its 8 files is in this lane.
2. The sweep says the 417 residual's "Open the PDF" is at `ServiceReport.tsx:170`; the gate and Jira point at `:169`. Source: `:169` holds the `<a ... data-testid="report-open"` and `:170` the text. Both given.
3. The sweep's partition says only the finished B1102 names ClientPacks/EngagementOverview/DocumentGeneration; my name scan finds six more finished kits and several records kits (B1059, B1072, B1073, B1079, B1090, R-series). None is live. The kit lists no live collision.
4. The sweep calls the 17 to 42 px overview links one group; the gate's own table lists the activity links at 18 px and the step links separately. The kit's census measures each.
5. The 417 Jira comment's "five links that end a sentence" already landed in PR 272; `DocumentGeneration.tsx` links at `:149-:151` already carry `inline-flex min-h-11 items-center` (so the sentence column also holds 44 px links, relevant to the room measurement).
6. The 431 ticket says "the gate named no fix" and the sweep says "the coordinator decided build"; the kit carries the decision as Tuesday's, not the product owner's.
7. G280/G282 (HPSM-POC gates) and H99 are not in the live pane list at 09:55 although the commission says they may be live; the kit says "may be live" and tests nothing on their panes.

## UNMEASURED by the drafter
Every height, column width and shift; any build, test or browser run; the 17 widths; whether `basis-60` suffices; which e2e specs run without a live API; Jira text of any other ticket; hosted CI.

## Outside-the-fences disclosure
Read-only. `gh api -X GET` under the project `GH_CONFIG_DIR` on `datasecau/HPSM-POC` (refs, pulls, compare, commit 55e6063c, raw files at main, the file tree, ci.yml, 57 e2e files, HpLogo.tsx) and `datasecau/HPSM-POC-analysis` (CLARIFICATIONS.md raw into scratch). Jira GET via `.tools/b1007/jira.py` (HPSMPOC-417, -431, output to scratch). Read the B1104 and B1097 kits, B1109 report, DRAFTER_RULES, routing lines, the local B1072 STATUS lines and two evidence files. Ran `lsof`, `tmux list-panes`, `uptime` (load1 10.82 at 09:56), one 5 s loopback listener on 9569 (closed). No `decision_queue.sh`, no `list`. Scratch only in `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/1cb7b127-7345-4f65-b535-46453a034806/scratchpad/b1113/`. No `cd` typed (one attempt was refused by the hook before any other work). Only the kit and this report were written.
