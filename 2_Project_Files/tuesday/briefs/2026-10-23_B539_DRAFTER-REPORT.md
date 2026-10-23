From Tuesday's brief drafter (Sonnet 5.5, routing row C8), Datasec / MPS Commercial Calculator. Drafted 2026-10-23 16:05-16:40 AEDT. Read-only: nothing fetched, built, run, stamped or launched.

# B539 drafter report: SEAT-M3R, fix round for PR #99 (b519, gate B533 NO GO round 1 of 2)

**Kit:** `2026-10-23_B539_SEAT-M3R_mps-b519-fix-round-2.md` (124 lines) and a byte-identical `.pre-stamp` (`cmp` OK, sha256 `b561c1e5b6b8bcd79912ed4205712f2c79a0e401a6fd66eb850b62eb33d87e12`). B539 was free (`ls | grep -E 'B539|B54[0-9]'` printed nothing).

**Stamp sentence:** the unstamped copy reads **8 lines** with the four-underscore pattern: seven slot lines (STAMP, LAUNCH WINDOW, Stamped by, Launch authority, Hard stop, Head and main at launch, Model receipt) plus the last line `READ-WHOLE-BY-TUESDAY: ____`. All 8 end in four underscores (program: 8 lines contain the pattern, 8 end with `: ` plus it; the body holds no other). Open slots: **8**.

**Port block:** 8800-8809 (the briefs allot up to 8790-8799 for B538; `lsof` on 8800-8900 empty; no bind control run by the drafter: the builder runs one). Pane `Datasec/MPS-M3R`. Model Opus (row C3), `BRIEF_SEAT_LEVEL=opus`. Hard stop suggestion 4.5 h, target READY 3 h.

**Measured at 16:05:** branch `b519/...` = `refs/pull/99/head` = `25cb36574ae3cd9c4d51ac79f90a4a7409d151c8`; main `4c593517dfa0febc7833c17579817d60ccc6d812`. Panes: tuesday, fleet-monitor, HPSM-POC-G58, MPS-G60, MPS-G61, HPSM-POC-G62. The gate pane G59 is gone and G63 is not yet a pane. Heavy slot-2 held by another seat; load1 8.98.

## Four things for your stamp read
1. **The 11 generated cases are not in the evidence folder.** Ruling 1 says each of the gate's 11 cases becomes a committed row, but the case file lives in the gate's own tree (`.tools/b533/`, read-forbidden to the builder). The brief tells the builder to read `B533_evidence/c6-unreachable-11-cases.json` if it exists, else derive the shapes from the Findings, `c6-reachability-per-case.json` (ids and classes only) and `c5-attack-rows.tsv` lines 6-8 / 68-70, and say so in Corrections. If you want the exact 11, copy them into the evidence folder before launch (I could not: my fence is three files).
2. **Rates reading.** Ruling 1's words say "per-number first-line check". The gate says base also judges the first rates entry of each section. The brief applies the ruling's stated principle ("never reach an end state base cannot reach") to rates too, red-first, but only if the builder's program finds a rates shape the head allows and base refuses; otherwise it builds nothing. It also tells the builder to flag in STATUS if it thinks this exceeds the ruling. Strike the rates paragraph at the stamp if you want lines only.
3. **Withdrawn widening can turn other committed rows red.** The brief authorises changing only the expectation of rows that pinned the widening (the `Boundary_a_repeated_number_sent_back...` moved half named by you, and any other found), with every changed line printed and the reason; a red row that is not that is a regression and a STOP. This is the one carve-out from "existing rows never edited".
4. **Finding 4 (Minor) is "as the gate states".** The gate gives two options joined by "or" (fixture with quantity per device other than 1; or drop names a row cannot justify). The brief builds the fixture first, then drops only names no row can justify after it, with a per-name mutant. Fixture file ownership is UNMEASURED; the brief stops if it is outside Yours.

## Other design choices
- **Commits:** one per finding, four, in the order 1 to 4 (finding 1 first because it moves the only `src` file). No rebase, no force, no merge of main; branch stays on `e027ebd0`; push is a plain fast-forward; the round-2 gate pins the new head.
- **New in the kit beyond the B519 shape:** a seeded 4,000-case differential (base tree vs fix, program not committed) that makes ruling 1 true by measurement (head-allowed/base-refused must be 0); a test-local transcription of base's first-line rule as the oracle of the committed property row, cross-checked against a real base tree; the list of 12 gate mutants to rebuild (`f`, `e1`, `e3`-`e6`, `e8`-`e10`, `e11`, `e13`, `e14`) plus controls c0/c1/c2; the check "a row no mutant turns red = 0" which the gate applies; the fence that `Apply`'s signature stays (gate G63 pins #102, which calls it).
- **Words:** none expected; any new string is a WORDS-DRAFT and a STOP.
- **Fences written in:** G60 (#100) and G61 (#101) files, trees and ports; queued G63 (#102) files; `.tools/b533/**`; the earlier builder's `.tools/b519/**` and `wt-b519-*`; main's docs/web; serial lanes; records files.
- **Out of scope as ruled (5):** the gate's Notes B533-5, -6, -7 and its whole FACT list.
- **REFUSE changes from round 1:** the b519 ref must exist at exactly `25cb365` (opposite of before); new tree names `wt-b539-*`; `Datasec/MPS-M3` (old builder pane) also blocks.

## Not done / UNMEASURED
No Jira read and no `gh` call by me (the builder's Step 0 does them); no bind control on the new ports; I did not run the base's first-line rule against the committed rows, so which existing rows turn red is for the builder; open PRs beyond #99-#102 not listed.
