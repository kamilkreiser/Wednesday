STARTABLE: NO until B1288 pushes W3 (kit B1288 file does not exist yet; the HEAD slot and the path list are Tuesday's to stamp); the kit itself is complete and has no open defect.

**BLUF.** Kit B1289 (seat G343, round 2 of 2, the cap) is 50 long lines (dense; the 80-line target met in lines, not in width). It judges the W3 delta in full (B1280-1 PDF brand tokens, B1280-2/-3 A24/A30 figures, B1280-6 spec sleeps and the 673 pin) and carries every other round-1 result by proving tree equality (n of 117 blobs equal, plus `git diff --name-only 9061c291 HEAD -- web ':!web/e2e'` empty), re-running only a smoke set. Cap handling: NO GO writes `residue.md` + `card-input.txt` only; GO writes the four landing files. Seven slots: STAMP, HEAD, ROUTE, CLOCK, LAUNCH AUTHORITY, MODEL, plus the last-line READ-WHOLE.

## Facts re-measured (instrument; control)
- Round count: loop over `Briefs/*STATUS.md` first lines filtered `GATE VERDICT` + `visual round` printed ONE file, B1280, "NO GO ... round 1 of 2" (the hit is its own positive control; the kit tells the seat to re-run with the B1269 control). So the class is NO GO 1 of 2; this is the cap.
- Refs at 23:32 (`gh api -X GET`): branch `9061c291...` (W3 not pushed), main `fc2bc2fc...`, open PRs 0.
- Pointers at `9061c291` (raw blob, `grep -n`/`awk NR`): BrandTokens.cs `:26` `--ds-fg`, `:29` `--ds-border`, accessors `:55-58`; IntegrationTests.cs (path `api/tests/HpsmPoc.Modules.Reporting.Tests/Integration/IntegrationTests.cs`) test name at `:102` (round 1 cited `:112`; the brief asks the seat to print both); mock-rows.spec.ts `:24` and `:72` `waitForTimeout(500)`, `:74` `toBe(673)`. My awk count of token rows in `:22-52` gave 23, not 25: the kit says "N by program, round 1 says 25 (RELAYED)" rather than asserting 25.
- CI (`ci.yml` at main, `grep -n`): api `:32` (25 min `:35`), sqlserver shard `:165`, web-build `:371`, web-unit `:450`, web-e2e `:483` (20 min `:487`, shard line `:491`).
- Landing `awk NR==3617` of HPSM-POC-analysis CLARIFICATIONS.md: head-pinned squash text, as in round 1. `model-routing.md:108` G1, `:111` G-cap; `models_latest.json:17` `claude-opus-5-5`.
- Ports 9750-9759: 0 listeners (`lsof`); word-bounded scan hits B1221, B1234, B1275, B1279, B1280, B1281, B1282 (all closed or prose/other block; B1282's own block is 9200-9209); `G343`/`B1289` words: 0 hits. Panes: `%0 tuesday`, `%1 fleet-monitor`. Disk 164831980 KiB free.
- Round-1 tools present (`ls`): `.tools/b1280/g/rows2.cjs rows3.cjs`, `ring/ring1269.cjs ring1280.cjs b1269_*.json`, `scripts/`; `wt-b1280-*` trees exist.
- Kit checks: `grep -c` four-underscore = 7 (six slots + last line), at-sign-capital tokens 0, slots.json parses with 7 keys.

## D-decisions
- D-1: the carried/judged split rests on ONE program claim, "web outside e2e equals 9061c291". If W3 touches any other web path the seat must judge it by the round-1 steps (kit text says so); it does not silently carry.
- D-2: plant set cut to P0, PC, PB (revert one BrandTokens value), PM (break the property the replaced 673 pin asserts), PN, PS (PS as a Note only: round 1 found unit rows do not see it).
- D-3: smoke set = audit-dev, lint, typecheck, build, check-shards, unit (names lost 0), all five shards, header 72 in 24 cells, page-end 72 cells vs ref. No browser re-measure of menu/colour/width/logo/words/ledgers.
- D-4: ports reuse 9750-9759 (G340 closed, 0 listeners); 9751/9752 spare.
- D-5: clock = Step 0 + 120 min, latest 03:45 AEDT 2026-11-05 (as asked); heavy shards may not fit in 120 min if the load is high; the kit orders the work so the W3 steps (1-5) come first and a shard not run is NOT TESTED by name.
- D-6: Minors B1280-4,-5,-7,-8,-9,-10 are explicitly carried to the product owner, not re-judged; the PR body copies the questions from round 1's `card-input.txt`.

## Q for Tuesday (each with a default)
- Q-1: what does the B1288 kit name as W3's path list beyond BrandTokens.cs and mock-rows.spec.ts (e.g. does it reword `IntegrationTests.cs`)? Default: only those two; Step 1's property makes any other path a Blocker candidate, so the kit needs no edit unless B1288 names more (then add the path to Step 1's "at least").
- Q-2: the HEAD slot value: slots.json carries the token `@HEAD@` (new; the B1287 file has only `@NOW@`/`@SEAT@`). Default: substitute it at the stamp with the sha40 you read.
- Q-3: the kit tells the seat the compare `fc2bc2fc...HEAD` should read ahead 10 (9 + W3), DERIVED, not measured. Default: leave; the seat measures it.
- Q-4: launch ordering: after B1288's READY and the HEAD stamp (kit says so). Default accepted.

## UNMEASURED
- The B1288 kit, W3's content and its path list; the actual HEAD sha.
- Whether `IntegrationTests.cs` assertion is at `:112` at the HEAD (only `:102` test name measured at `9061c291`).
- The count of token pairs in BrandTokens.cs (23 by my crude awk over `:22-52`, 25 by round 1's STATUS); the seat counts by program.
- Names of the Reporting PDF-contrast tests (the kit tells the seat to find them by `grep -n -i contrast`).
- Whether round 1's `rows2.cjs/rows3.cjs` still run unchanged (read as text only by me? No: I only listed them; not opened).
- Round-1 smoke figures (4038 tests, 275 files, shard counts) are RELAYED from the B1280 STATUS, not re-measured.

## Outside-the-fences disclosure
Read only: DRAFTER_RULES.md, the B1280 kit and ADDENDUM-1, B1287 kit and slots (shape), the B1280 STATUS (lines 1-3, 150-204), `card-input.txt` of round 1, `model-routing.md` lines 108/111, `models_latest.json:17`, `gh api -X GET` reads on `datasecau/HPSM-POC` and HPSM-POC-analysis, `lsof`, `tmux list-panes`, `ls` of `.tools/b1280`. No `cd`, no Tuesday attestations in slots, no decision_queue, no fetch in the project repo, nothing written but these three files. B1279's kit (cap text model) was not on disk; I used B1287's cap text and `model-routing.md:111` instead. The card-input.txt of round 1 was opened (it is in the evidence folder; it names no card id).
