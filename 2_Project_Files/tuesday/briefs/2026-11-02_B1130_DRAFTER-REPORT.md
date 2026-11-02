STARTABLE: YES (with the disk caveat in Q-1)

# B1130 DRAFTER REPORT - SEAT-G288, HPSM-POC tier-1 QA gate, round 2 of 2 on class R
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1130_SEAT-G288_hpsmpoc-focus-ring-gate-tier1-r2.md`, 20470 bytes (`wc -c`, limit 20480). B1130 was unused (`ls | grep B1130` 0 before writing). Stamp slots: 7 plus the last line = 8 lines with the four-underscore pattern (`grep -c` 8), at-sign placeholders 0, non-ASCII 0. Stamp slots unfilled.

## BLUF
One Opus gate over `b1097/hpsmpoc-home-words-focus-ring` @ `f9f1f490`, judged on the merge into main (the head tree is not the landing tree: head is 2 behind main). Its own census (real Tab/Shift+Tab, in-process two-screenshot diff) against the product owner's words, every role, both menus, six widths, two heights, both directions, plus a drawer height sweep. Questions (a)-(e) are Steps 3.5, 4, 5, 7, 2. A NO GO on class R is the cap: the kit requires `residue.md` (one plain paragraph per residue) and no landing files. Class W is checked by blob only.
**Main moved while I drafted:** PR #275 landed; main is now `5f128fb890341e2b0d52b337fe527a59ceafd70a` (was `4b3cefae` at 14:53). Head is ahead 3, behind 2, 8 paths, 0 overlap with #275's 24. I updated the kit (rev-list expectation `2 3`, MAIN-MOVE baseline `5f128fb8`).

## Facts re-measured (instrument; clock)
- Head `f9f1f490d20b7ba89b9f4145ae5d3582e3083bb9` (`gh api git/ref`, 14:53 and 15:04); tree `b1c9e649`; commits A `4f59c83e` (tree `50a765ef`), B `dcc5ca03` (tree `9060e9ad`), C `f9f1f490` (parent `dcc5ca03`, unsigned, one Sonnet trailer). `compare main...head` (15:04): diverged, ahead 3, behind 2, 8 paths. Commit C = 4 paths (`globals.css` +4 -1, spec +59, `AppShell.sidebar.test.tsx` +15 -13, new `PartnerDashboard.text.test.tsx` +136).
- Class W by blob: `contents` sha of the four commit-A paths at `dcc5ca03` equals at `f9f1f490` (4 of 4, `gh api`).
- `globals.css` at the head (`grep -n` over the raw file): `:82` link rule, `:91` current-item rule, `:92` offset 2px, `:93` `revert-layer`, `:94` `scroll-margin-block: 6px`, `:96` `[data-nav-ring]`.
- Open PRs 0 (`gh api pulls`, 15:04). #275: closed, merged, merge commit `5f128fb8`. `compare 4b3cefae...main`: ahead 1, 24 files; the MAIN-MOVE regex over them counts 0 (control `web/src/app/globals.css` counts 1); `CustomerShell` paths 3; overlap with the 8 paths 0.
- Disjointness (`comm -12` of `compare main...<branch>` lists vs the 8 paths): `b1113` (7) 0, `b1095` (4) 0, `b1104` (24) 0; control self 8. `b1124` (H102) is not pushed (compare 404); its kit names `web/src/server/auth/revocations.race.test.ts` and `api/`: not mine.
- Live panes (`tmux list-panes -a -F '#{@cockpit_name}'` 15:04): `tuesday`, `Datasec/MPS-G287`, `Datasec/HPSM-POC-G286`, `-H102`, `-H103`, `Datasec/MPS-G283`, `fleet-monitor`. `-H101` count 0 (control `-G286` 1); `-G288` not yet live.
- Ports: `lsof -nP -iTCP:9540-9549 -sTCP:LISTEN` 0 (also 9530-9539, 9570-9579, 9590-9599, 9560-9599: 0). Word-bounded scan of 131 non-`.pre-` SEAT kits of 11-01/-02: `954[0-9]` 0, `959[0-9]` 1, `955[0-9]` 2, control `957[0-9]` 3. Across all 278 B-files of the two days (reports included), `954[0-9]` has 4 prose hits (B1017 "blocks seen", B1113/B1122/B1127 reports; B1127 says "9540 spare"): none a claim. The listener control on 9549 was not run by me (read-only rule); the kit has the seat run it.
- Builder STATUS: last line starts `READY FOR QA: B1122 b1097/hpsmpoc-home-words-focus-ring @ f9f1f490...` (1; control 0), `## PRIOR WORK` 1. `.tools/b1130` absent, `wt-b1130-*` absent (`ls -d`), control `.tools/b1122` exists. B1109 STATUS line 1 matches `NO GO @ dcc5ca0 ... round 1 of 2 on class R` (1).
- Model: `model-routing.md:108` row G1 (Opus, tier 1), `:111` row G-cap (two NO GO rounds on one class: STOP; a third needs Kam's word on a card); `models_latest.json:17` `claude-opus-5-5`. Launch line carries `BRIEF_SEAT_LEVEL=opus` inside the quotes.
- CI (`ci.yml` at main, 679 lines): `web-build` `:371`, `audit-dev` `:395`, lint `:396`, typecheck `:409`, build `:413`, `--check-shards` `:426`, `web-unit` `:450`, `npm test` `:478`, `web-e2e` `:483`, `web` `:526`.
- Disk: `df -g` 27 GiB at 14:53, **26 GiB at 15:05**. Load1 15.11 at 14:53, 6.55 at 15:05 (`uptime`). Shared checkout `du -sk`: `node_modules` 473632, `.git` 161996, `.next` 37208 (the basis of the disk plan).
- Builder's 73/10 cells: from its STATUS (claim): 73 short, all under the Menu toggle, 63 short at main, 10 new (partner 768x420 My readiness; partner, consultant, demo 390x420 Engagements; consultant, demo 768x420 Training & playbooks and Revenue; admin 390x420 Training & playbooks and Delivery phases). The kit sends the seat to its own census, not the builder's list.

## D-decisions (mine, for Tuesday to accept or change)
- D-1 **RULE T, "the gate's reading" of a toggle-covered ring**, from B1109's grading: C2 (a) clipped or missing edge in a reachable cell = Blocker, (b) drawer cell failing while the 1280 main menu passes = Major, (d) frame no product ships = Note; B1109's table split "REGRESSION" (whole at main) from "both trees" (B1109-7, Note). My reading: the words fail in ANY cell with an edge not clear (3 ring pixels on the middle line, each at 3:1+), whoever covers it; attribution then grades. T-a (cut at main too, rows not fewer) = Note. T-b (clear at main, not at head): 0 rows or under 3:1 in a shipped frame = Blocker; 1-2 rows in a drawer cell = Major; a frame no device ships = Note with the frame stated. Shipped frames: widths 390, 768, 844, 1024+, heights 390+. So the 10 new cells are at least Major unless a sweep shows they occur only at heights no device ships (all 10 are at 420 tall in the builder's claim).
- D-2 **"Worse than main" is a number:** E = clear edges per cell. Main's left edge is 1.911 (never clear), so main's E is at most 3; a head cell with the toggle covering one edge also has E = 3. The kit prints cells with E_head <, =, > E_main plus rows lost on an edge main had at 3, and asks better/worse/mixed. This matters: by E alone the 10 may read "equal"; by rows lost they read worse. The kit makes the seat report both.
- D-3 **Question (b), scroll margin:** the seat measures per press rail `scrollTop` and document `scrollY` at main and the landing tree (800, every 2 px 420-900, longest customer menu both directions), and counts six "broken" properties (item not fully visible, scroll against travel, over-scroll beyond item height + 6, document scrolls where main's does not, round trip not returning, spurious scroll for an item already 6 px inside). Control: a 40 px margin plant must read broken.
- D-4 **Question (c):** the margin cannot change paint; the seat proves it and re-measures hovered next AND previous. Same 2 rows = the same Minor carried (as B1109-2); 0-1 rows or under 3:1 = Major.
- D-5 **Question (d):** R4' property stated; b1-b11 re-made as defined in B1109 C3 (not retyped, for size). b5 and b11 must leave R4' green. **b6 is taken as R4' red by design** (see contradictions). Added margin plants m1-m5 and T1 plants t1-t5 (t5 equivalent).
- D-6 **Question (e):** the seat reads the rendered Home text in a browser (4 roles x 390/1280 x B1109's 8 states) at the landing tree and at `dcc5ca03`'s, then compares T1's literal and construction against it; "T1 must be fed by the page" is a Major if not.
- D-7 **Disk:** one clone, one `npm ci` (head worktree), base and plant worktrees symlink `web/node_modules`, screenshots in process, `df -g` before every heavy start and in the heartbeat, STOP under 25 GiB, `du -sk` after each build. Nothing deleted (a `mv` frees nothing on one volume).
- D-8 **MAIN-MOVE** is a path-property regex (counts 0 over #275's files), `shell/CustomerShell*` explicitly not a stop: name, re-derive the merged tree, re-run the customer-menu cells, Note with the delta.
- D-9 The kit does not copy B1109's hygiene/landing mechanics; it points to B1109 (step 1, C5, C7, C8) and B1127, to stay under 20 KB. The seat must read both whole.
- D-10 COUNT FLOOR was dropped to stay under the size limit; under load the only cut rules are RULE L (a wait is not a finding; NOT RUN bars a GO).

## Q-questions for Tuesday (each with a default)
- Q-1 Disk is 26 GiB at 15:05 and falling (27 at 14:53) with STOP at 25. Default: launch anyway; the seat stops itself under 25 and says so plainly; plan needs under ~1.5 GiB. If you want headroom, free space first (not mine to do).
- Q-2 Is a ring covered by the Menu toggle a failure of the product owner's words (D-1)? Default: yes, per D-1; the kit grades T-b new cells Major/Blocker and T-a Note.
- Q-3 Are widths 390/768/844 at heights as low as 390 "shipped frames"? Default: yes (landscape phone is 844x390). If you rule 420-tall drawer cells are not shipped, the 10 new cells become Notes and the gate can reach GO WITH FINDINGS.
- Q-4 Stamp S1-S7 and the launch window are yours. Default: launch via `launch_when_cool.sh` as the kit's launch line, load1 under 7.
- Q-5 Residue card text goes to the product owner via Tuesday. Default: `residue.md` in the evidence folder, plain paragraphs, no ids.

## Contradictions found
- B1122 brief says R4' is green on b6 and red on PR4, but b6 and PR4 are one edit (the builder's Corrections 1 says so). Kit: b6 red under R4' is a Note, not a finding.
- B1109 C3 called b6 "equivalent on behaviour"; the B1122 brief decision 2 pins placement by a row. Both stand; the kit follows decision 2.
- Builder's numbers do not match the gate's (120/193 vs 115/160) and the builder did not reconcile its brief's "232" (builder Corrections 4). The kit tells the seat to treat all of them as claims.
- Builder's census is at the fix tree (dcc5ca03 + C), not the landing tree; the landing tree got lint, typecheck, unit and a build only. The kit puts the whole census on the merged tree.
- The kit's disk figure of 27 GiB is already stale (26 at 15:05); noted in Q-1.
- The kit header says "Open PR #275" nowhere now; the facts line says it landed. B1122's brief said open PR 275 belonged to b1104 (still true; landed).

## UNMEASURED
- Whether a listener on 9549 is seen by `lsof` (control not run: read-only rule); the seat runs it.
- Whether H102's branch will touch any of the 8 paths (unpushed; its kit names one `web/src/server/` test file and `api/`).
- Whether the 10 NEW cells exist at any shipped height, whether the margin changes scroll behaviour, the 7 px oddity: all the gate's job.
- Hosted CI, CodeQL, other engines, screen reader, real touch.
- The `.pre-stamp` copy: I made one and moved it to the session scratchpad (`.../scratchpad/...pre-stamp`) to respect the two-file rule; Tuesday must make its own before filling slots (unstamped copy reads 8 four-underscore lines).
- I did not run the kit's shell lines as written (only the equivalent reads).

## Outside-the-fences disclosure
Reads only: the rules file, kits B1109/B1122/B1127, B1109 and B1122 STATUS files, `model-routing.md`, `models_latest.json`, `ls`/`wc`/`du`/`df`/`lsof`/`tmux` reads, `gh api -X GET` under the project's `.gh-config` (refs, compares, contents, pulls), raw reads of `globals.css` and `ci.yml` into the session scratchpad. Scratchpad helper scripts (`cut*.py`, `upd*.py`) edited only the kit. No decision_queue, Jira, Azure, mail, message, `cd`, git write, or project-folder write. The one stray file (`.pre-stamp`) is in the scratchpad.
