STARTABLE: YES

# B1131 DRAFTER REPORT - SEAT-G289, HPSM-POC tier-1 gate, round 2 of 2 on class A (a NO GO is the cap)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1131_SEAT-G289_hpsmpoc-wake-close-gate-tier1-r2.md`, 18,421 bytes by `wc -c` (cap 18,432). B1131 was free (`ls` showed B1130 as the highest; `G289` appears in no other kit). Written 15:23-15:46 AEDT 2 Nov 2026.

## BLUF
The kit gates the 3-commit branch at `76116bc6` and judges the merged tree on main `5f128fb8`. Its nine steps follow the B1107 gate's. It first proves no product behaviour changed, with IL hashes of both modules at `2746b07` and at the head plus a comment-only diff of `SqlServerWakeRetry.cs`. It then re-makes a5 and all of a1-a7, PA2, PA2b, b2, b4, b5 with its own plants, and runs R1/R2 ten times each under a5 (red every run) and at the head (green). It asks whether R1/R2's event ordering could pass under four other shared-key shapes (s1-s4). It runs an independent b5 search that must fire under two known-different plants before a zero counts. It answers B1107 Notes -9 to -14, and runs suites (main + 16 Api and + 8 Reporting predicted, names lost 0 added 24) and CI placement. On a NO GO it writes `residue.md` in plain words and none of the four landing files. To fit 18 KB the kit hands clone, lock, IL-compare, hygiene, gitleaks and landing mechanics to the B1107 kit ("read WHOLE") and says this kit wins where it speaks.

## Facts re-measured (programs and clocks in brackets)
- Head `76116bc64a5c96bf72c51106a7b1a9ae0e3a1ac0` (`gh api git/ref`, 15:18, 15:22; tree `f171306d`; unsigned; 1 Sonnet trailer; message 3006 bytes). Main `5f128fb890341e2b0d52b337fe527a59ceafd70a`. `compare main...head`: diverged, ahead 3, behind 2, merge base `c1457349`, 4 paths (+68 -15, +3 -2, +626 -2, +119 -2). Commit order A `d1c9f47e` (tree `ac314526`), B `2746b073`, C `76116bc6`. Open PRs 0; `matching-refs/heads/b1131` 0 (control `b1095` 1).
- Main's two commits moved 24 paths, 6 under `api/` (`Endpoints/` x3, `Api.Tests/Assessment/` x2, `Contract/openapi.delta.json`). The B1107 REFUSE (main) pattern counts 0 over those 6 (controls: the product file 1, the retry test file 1). Branch list against itself = 4. Overlap with `b1113` 0 of 7, `b1097` 0 of 8; kits B1124 (one hit: its own planted control), B1127, B1129, B1130 name none of the 4.
- Product diff `2746b07` to head (`diff` of both raw files): one hunk, `SqlServerWakeRetry.cs:42` replaced by `:42-43` (comment only). Head file 124 lines. Retry test file 958 lines, 27 `[Fact]`. Guard test file 445 lines, 18 `[Fact]`. Pointers printed by `grep -n`: `OpenInProgress` `:48`, `OpenTimedOut` `:67` (reads `Opening` `:70`), `Mark` `:119-121`, R1 `:807`, R2 `:849`, R3 `:883`, R4 `:898`, R5 `:929`, `GateBound` `:426` (20 s), `ConnectionHold` `:432`, T17 `:419`, T18 `:432`, validator `:198`, `:295`, `:300`.
- `ci.yml` is byte-equal at main and head (hash prefix `ff8d727c9e67` both, 679 lines): `:87` job `api` test, `:165` shard, `:252`/`:255` filters, `:303` every outcome `Passed`, `:314` floors, `:353`. Ruleset `rules/branches/main`: deletion, non_fast_forward, code_scanning, required_status_checks.
- Records repo `CLARIFICATIONS.md` 5346 lines, "head-pinned squash" count 97 (control absent string 0); `:3617` reads as the landing form.
- `model-routing.md:108` G1, `:109` G2, `:111` cap; `models_latest.json:17` `claude-opus-5-5`. Builder STATUS last line begins `READY FOR QA: B1126 ... @ 76116bc...` (count 1, control 0); `## PRIOR WORK` count 1 (control 0).
- Panes (`tmux list-panes -a`, 15:21 and 15:46): `tuesday`, `Datasec/MPS-G287`, `Datasec/HPSM-POC-G286`, `Datasec/HPSM-POC-H102`, `Datasec/MPS-G283`, `fleet-monitor`. `-H103` 0, `-G286` 1, `-G289` 0 (it exists at launch; the kit says so).
- Ports: `lsof` on 9510-9519 0; word-bounded `\b951[0-9]\b` over the 132 non-`.pre-` SEAT kits of 11-01 and 11-02: 0 (control `957[0-9]` 3 kits). B1130 holds 9540-9549; 9530-9539, 9560-9589, 9720-9739 taken. Free in both checks at 15:2x: 9510, 9040, 9060, 9080, 9100, 9130, 9140, 9250, 9310-9390 (several), 9460. I chose 9510-9519, the nearest to the web gates' range. The kit's own text matches the scan pattern, so the scan sentence says "not this kit".
- Disk: `df -k` 26.79 GiB available at 15:22, 26.20 at 15:46 (other seats are building). Sizes by `du -sk`: `.tools/wt-b1107-base` 0.74, `-head` 0.74, `-mut` 0.45; `2_Project_Files/.git` 0.15. One clone (0.15) plus one built worktree (0.75) is about 0.9 GiB, leaving about 0.9 to 1.3 above the 25 floor. A second worktree would cross it, so the kit forbids the base/head/mut trio.
- Severity against steps, by program (python over the kit): steps carrying a severity tag 1-8; steps named by the severity paragraph 1-8; neither set has an extra member. Steps 0 and 9 carry none, and the severity heading says so.
- REFUSE against the launch state: panes and `.tools/b1131` are written for the pane existing at launch (G289 count 1) and the tree absent before Step 0. The kit's REFUSE lines were each run at 15:2x, none fires. Unstamped kit: four-underscore pattern 8, `@X@` pattern 0, non-ASCII 0, odd-backtick lines 0.

## D-decisions
- D1 Mechanics by reference to the B1107 kit, read whole (C3 plants, C5 patterns, C6, C7, C8 gitleaks, C9 landing, P4 IL compare, the main-moved pattern). That is how the 18 KB fits; the kit states it wins on conflict. The B1107 REFUSE (main) pattern is not copied: it is cited verbatim, and I counted it 0 on #275's 6 paths with two controls.
- D2 One clone, one worktree, one restore, states switched by `git checkout --detach <sha>` only with a clean `status --porcelain`; plants restored by `cp`. B1107 forbade `checkout --`/`reset` (file restore), not this; I flag it as Q2.
- D3 Suite subject is the merged tree, base is main `5f128fb8`. Predicted merged = base + 16 Api (11 + 5) and + 8 Reporting (6 + 2), lost 0, added 24. The builder's branch-tree figures (2183/0/13, 850/0/0) are checked last. Arithmetic: 2167 + 16 = 2183, 842 + 8 = 850, which matches the builder's own numbers on c1457349.
- D4 Shared-key shapes s1-s4 (my predictions, unrun): s1 last-opener slot probably leaves R1 green (B's opening replaces A's slot) but R2 red; s2 unclamped counter probably leaves R1 green, R2 red; s3 thread id and s4 `GetType()` unclear (s4 equals a5 for two state-only connections). A shape green on both rows with W5 moved is a Minor pin gap; only a5 itself is Major. This is my call (Q3).
- D5 The b5 search is the gate's own, with controls that can fail (b4 and a lookbehind-removed plant must each give at least 1 differing cell; 0 = blind). My reading: b5 is likely equivalent (the claim regex's `(?<![\w.])` forbids a word character or dot before, the lookahead needs white space after, so a removed claim leaves white space before the next token). Unrun; the kit makes the seat prove it before reading the builder's search.
- D6 `residue.md` only on NO GO (B1130's shape: one plain-words paragraph per residue, no finding ids or ticket key). On GO or GO WITH FINDINGS the four landing files, figures from its own runs.
- D7 PA2, PA2b, a3, b2, b4 surviving is Minor, not Major (the builder says each new row is red; a Minor cannot block, as your stamp ruled for the last round). a1, a2, a4, a5, a6, a7 surviving, or a5 green in R1 or R2 on any run, is Major and the cap.
- D8 Steps cut for room: the W-cell re-run is replaced by IL equality plus one cell each of W4-B, W3 and W6; A-only and B-only commit builds are not asked (C is not a separable commit pair); the `.tools/b1107` W-cell scratch is a READ pattern only.
- D9 The class B line says NO GO 0 before and gives it no cap text (a NO GO there would be its first).

## Q-questions for Tuesday (each with a default)
- Q1 Disk margin is about 1 GiB over the floor with other seats building (26.20 GiB at 15:46). Launch B1129 (old lane-tree removal) first? Default: launch the gate anyway; its REFUSE stops it cleanly under 25 GiB (`STOPPED: NEEDS TUESDAY disk <n> GiB`).
- Q2 Allow `git checkout --detach <sha>` for state switches inside the seat's own clone? Default: yes (the kit says so).
- Q3 s-shape pin gap, Minor or Major? Default: Minor, because R1/R2 are the builder's ask for a5 and the gap goes to `residue.md`.
- Q4 Judge the merged tree (kit) or the branch tree? Default: merged; the branch tree last.
- Q5 B1129 may move `.tools/b1107` scripts (a "lane-worktree/build-output" removal). The kit tells the seat to copy first and rewrite a missing script. Default: accept.

## Contradictions
- The B1126 brief said R2's held open "throws a login timeout"; the builder used the pool wait form (its STATUS Corrections 1; its commit message says so). The kit does not re-open this; the sentence table in step 8 covers it if the gate finds it matters.
- The B1126 brief says the branch was "2 ahead, 1 behind main"; measured now ahead 3, behind 2 (main's 4b3cefa web-only commit and 5f128fb), matching the builder's final PINS.
- Builder STATUS "G3: 58,950 generated, 58,890 distinct" versus your "0 of 58,890": same figure, distinct count.
- B1107 and the B1126 brief gave `models_latest.json` lines 17 and 23; the opus line is still 17 (printed by grep).
- B1107's REFUSE listed `Datasec/HPSM-POC-G276` as the pane control; that pane ended. The kit uses `-G286` (count 1 now).

## UNMEASURED
Every row's outcome, every plant, the IL equality, the b5 search result, the merged tree id, any suite count on the merged tree, the SQL Server leg, hosted CI, CodeQL, a real SqlClient close or pool wait, whether a real -2 ends after login, B1129's effect on `.tools/b1107`, and whether disk holds above 25 GiB through the first build. The s1-s4 predictions and the b5 equivalence reading are unrun reasoning.

## Outside the fences
Nothing read outside the allowed set. Read-only: the two kits and two STATUS files named, `gh api -X GET` (ref, compare, commits, contents of the 6 raw files at the head and `2746b07`, rules, the records CLAIMS file), `lsof`, `tmux`, `df`, `du`, `ls` of `.tools/` and `Briefs/` names, the B1124, B1127, B1129, B1130 kits for ports and paths. No `decision_queue`, Jira, Azure, mail or message to anyone; no `cd`. Scratch files only under the session scratchpad (the kit was edited there and copied over). No git verb ran in any project repo. The only files written under the project tree are the two named.
