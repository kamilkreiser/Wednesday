STARTABLE: YES (after your stamp; one size caveat in Q-1, one coordinator contradiction in C-1)

# B1132 drafter report (kit `2026-11-02_B1132_SEAT-H104_hpsmpoc-links-fix-round.md`, 18372 bytes, `wc -c` at 15:57:29 AEDT)

## BLUF
Builder fix round for row C2 on `b1113/hpsmpoc-417-431-links-and-room` @ `d8a9456`: one new commit, one plain push, no PR, no rebase. Three paths (`ClientPacks.tsx`, `EngagementOverview.tsx`, `residualLinks.targets.test.tsx`), class strings and tests only, NO WORD. B1127-1 is built from the gate's fix shape. B1127-2 is built as the BROWSER measures it from the gate's two proposals (negative block margin or `items-baseline`), with every candidate printed; proven by census, screenshot pair and class-pin rows. B1127-3 is a new commit message with the seat's own corrected count. Next gate: ROUND 2 OF 2 on the links class, NO GO 1 of 2 before, tier 1 Opus; a NO GO there is a card. Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes. Pane `Datasec/HPSM-POC-H104`, ports 9460-9469. Stamp slots are four underscores (11 lines, counted).

## Facts re-measured (each by a program; clock 15:43:44 to 15:57)
- Branch ref `d8a9456fa0fe251dd030b9afef67ec6480cc6139` (`gh api git/ref`), main `5f128fb890341e2b0d52b337fe527a59ceafd70a`; `compare main...branch` ahead 2, behind 1, 7 files; open PRs 0; `matching-refs/heads/b1132` 0 (control `b1113` 1). B1132 was unused by `ls` (B1130 and B1131 present, nothing above).
- Main moved from `4b3cefae` to `5f128fb`: 24 files, PR #275; `grep -c` of the kit's path pattern over them 0 (control 1).
- `web/package-lock.json` blob at the branch and at main: `81393fd77c36489b3e8b17a13bde28e225350fb4` both (`gh api contents`), so a node_modules reuse is safe.
- Panes `tmux list-panes -a -F '#{@cockpit_name}'` 15:49: `tuesday`, `Datasec/HPSM-POC-H102`, `fleet-monitor`. H102's kit B1124 declares one path, `web/src/server/auth/revocations.race.test.ts`; its kit holds 0 mentions of ClientPacks, EngagementOverview or residualLinks (`grep -c`). No H104 kit exists (`ls | grep -c` 0).
- Disjointness by `compare main...<branch>` lists and `grep -c -x -F -f` against the 7 paths of `b1113`: `b1095` @ `76116bc6` (4 files) 0, `b1097` @ `f9f1f490` (8 files) 0, `b1104` @ `f762cc7a` (24 files) 0, main-move list 0; control `b1113` against itself 7, against my 3 paths 3. `b1104`'s list equals the main-move list by `diff` (it landed as #275). B1126's and B1122's branches are `b1095` and `b1097`; both were PUSHED since their kits (new heads above).
- Ports: `lsof -nP -iTCP:9460-9469 -sTCP:LISTEN` 0 rows. Word-bounded `-w -E '946[0-9]'` over the 133 non-`.pre-` SEAT kits of 11-01 and 11-02: 0 files (control `9561`: 3 kits). A scan of the word-bounded numbers named in those kits (ranges expanded) left 9460 free; hits only in older drafter reports (B1012, B1017: a finished seat). B1130's block 9540-9549 and B1131's 9510-9519 read from their kits; 9530-9539, 9560-9589, 9720-9739 as you said.
- Disk: `df -k` available 27457228 KiB = 26.18 GiB (`df -g` prints 26, a floor). STOP line in the kit is `df -k` under 26214400 (25 GiB). Margin 1.18 GiB.
- Lines (printed by `awk NR==n` over `git show d8a9456:<path>`): `ClientPacks.tsx:182` container `flex flex-wrap items-center`, `:184` link `className="underline"`, `:201` pack link (44 already); `EngagementOverview.tsx:71`, `:83` `Row`, `:192`, `:212` `dl`, `:221` milestone link, `:238` activity `li`, `:239` icon `mt-0.5`, `:241` activity link, `:244` date; `residualLinks.targets.test.tsx:123` and `:157` pin `toEqual(TARGET)` exactly. `ci.yml` (679 lines) audit-dev `:395`, lint `:396`, typecheck `:409`, build `:413`, `--check-shards` `:426`, `npm test` `:478`. `model-routing.md:92, :108, :111`; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24`. Records `CLARIFICATIONS.md:3617` quoted from `gh api` raw.
- B1127 gate claims used (not re-measured): 25 own links under 44 at main, 1 at head; offsets 10/13/12 px; 931 readings per tree. All marked claims in the kit.

## D-decisions (mine, in the kit)
- D-1 Only `ClientPacks.tsx`, `EngagementOverview.tsx` and the builder's own test file are the property; `ServiceReport.tsx` joins only if the seat's census lists a link there. `Row` (`:83`) and `Panel` are NOT yours: a fix that needs them stops with a table. Reason: `Row` is shared by every summary row.
- D-2 B1127-2: the kit names both of the gate's proposals and orders them (negative margin first) but lets the browser decide; reason: negative margin also restores the old row heights (no growth), `items-baseline` on the `dl` touches every summary row. Neither is verified by me.
- D-3 No second install: `cp -Rc` APFS clone of `.tools/wt-b1113-fix/web/node_modules` (read-only source; `mount` reads apfs; lock blob equal). Three trees only, one merged tree built three times (main, head, fix). Estimated extra under 1 GiB (source 8.2 MB `src` per `du`; `.next` 175 MB measured in three other trees; clones about 0). The older trees stay: another seat (B1129) removes them.
- D-4 Existing rows `:123`, `:157` are edited (they pin the exact class set and would go red under any margin class); the kit says so, names them, and lists them as the only existing rows that may change.
- D-5 Alignment proof is census + screenshot pair + class-pin rows; jsdom cannot see layout (gate said so). No e2e file is touched.
- D-6 Gate-state gap: the builder's `pack3-service-withheld` state held no "Go to the executive report" (gate, not explained); the kit makes the seat print why or mark UNMEASURED, and census pack 3 withheld / none and pack 2 no-set, which the gate reached.

## Q-questions (each with a default)
- Q-1 The kit is 18372 bytes: under 18 KiB (18432), over 18000. Default: accept as 18 KB; say if you meant 18000 and I cut 400 more.
- Q-2 Should an e2e row (browser geometry) be allowed to pin alignment? Default NO: it adds a path under `web/e2e/` and a shard check; the census plus pinned classes is the proof.
- Q-3 `ServiceReport.tsx` conditional inclusion (D-1). Default as written.
- Q-4 Gate round count wording: the kit says "ROUND 2 OF 2 on the links class, NO GO 1 of 2 before (B1127)", read from the B1127 verdict line ("round 1 of 2 ... NO GO 0 before") and your brief. Default as written; the stamp slot carries it.
- Q-5 Ports 9460-9469. Default yes.

## Contradictions found
- C-1 The gate STATUS says Fix shape for B1127-1 is "the same class string as the other links on that line" (`inline-flex min-h-11 items-center underline`), but `ClientPacks.tsx:201`, the only other link on a related line, is `font-semibold underline` plus the three classes: no conflict, but the pack link is a different line (not the same container), so "same string" is the three classes plus `underline`, as the kit writes.
- C-2 B1127 says "round 1 of 2 on both classes" in its verdict tail but also "forward fix round, not the cap" and `model-routing.md:111` needs two NO GO rounds; the kit follows the first NO GO reading, next gate ROUND 2 OF 2, NO GO 1 before.
- C-3 The gate wrote "main 4b3cefae" in its REFUSE counts and "main 5f128fb" in its verdict; main moved during the gate; the kit uses 5f128fb everywhere.
- C-4 The builder's READY line said "round 2 of 2 (NO GO 0 before)"; the gate corrected it to round 1 of 2. The kit uses the gate's.
- C-5 The kit's line "tier 1 on Opus" comes from `model-routing.md:108` G1; B1126 does the same.

## UNMEASURED
Every height, offset, row outcome, hosted CI result and CodeQL state; whether a negative block margin on an `inline-flex` link restores main's offsets (the inline-level margin box should, but nobody ran it); whether the `:158` route is reachable; why the builder's withheld state never rendered the link; the byte size of three new trees and the real `.next` size after a build (estimates only); whether 1.18 GiB of margin is enough if Playwright output is large (the kit caps the PNGs at 12 and stops under 25 GiB).

## Outside-the-fences disclosure
Read-only throughout. Read: `DRAFTER_RULES.md`, B1127 and B1113 STATUS, B1113/B1126/B1122 kits, B1124 and B1130/B1131 kits for paths and ports, B1127 evidence names (`ls` and head of two files), `model-routing.md` three lines, `models_latest.json`, `brief_seat.sh` line 24, and `git show` of three source files and one test at `d8a9456` from the local worktree `.tools/wt-b1113-fix` (a read verb; its `HEAD` object type `commit`). `gh api -X GET` under the project's `gh-config` for refs, compare, branches, contents (raw `ci.yml`, package lock blob, records `CLARIFICATIONS.md:3617`). `lsof`, `tmux list-panes`, `df`, `mount`, `du -sh` on tree sizes. No card read, no decision_queue, no Jira, no Azure, no message. I listed branches via `matching-refs` prefixes b9..b14 (75 refs) and compared a subset. The scratch files (copies of three sources, `ci.yml`, branch and file lists) are in the session scratchpad only. One quirk: an early `cd` was refused by the hook; I did not retry it.
