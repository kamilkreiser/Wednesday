STARTABLE: YES

# B1128 DRAFTER REPORT (seat G287, MPS tier-2 gate of b1117, row C8)

## BLUF
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1128_SEAT-G287_mps-257-sites-warning-gate-tier2.md`, 17,990 bytes (`wc -c`), 8 four-underscore runs (S1-S7 plus the last line; `grep -c` = 8), 0 non-ASCII bytes. B1128 was free (highest in `briefs/` was B1127; `ls | grep B1128` found none before writing). Stamp slots left unfilled.
- The gate judges branch `b1117/mps-257-sites-warning-unless-stopped` @ `a9960f68` merged onto main `17fc0dbc` (MPS #143 landed since the builder's base `7104179f`; #143 touches `docs/IMPORTER.md` and two web tests; overlap with the branch's 3 paths: 0 by `comm`).
- The change IS reading B and only reading B, by my own read of the raw files at both shas: the diff of `PurchaseCalculator.cs` main vs head is exactly three hunks (call moved `:209` -> `:216`, doc sentence, 4-line guard deleted); the call now sits after the only stop that follows it, so the check runs exactly when the quote priced. Non-stopping Blocking codes found by grep: UNKNOWN ITEM (`:630`), MARKUP NOT SET (`:661`) and the two SOURCE codes (`QuoteCalculator.cs:191`, `:195`); stopping: all `:169` structure/quote-level codes, and the three line-check codes at the second stop. This is the kit's thesis, not a gate result: the seat re-derives it with its own cases.
- Not a money path by the builder's kit or either ticket (no figure; spec section 40). The kit still makes a price, total, status, hash, id or issue-order change on any case a Blocker, tested by comparing the whole serialized result head vs base for every case (Step 3).
- Rule L kept, narrowed: only restore, whole-solution build and whole-solution test wait for load1 under 7 (two reads two minutes apart, 120-minute cap); the Engine test project (probes, plants, filtered rows) takes a seat-local lock and no load wait.

## Facts re-measured (instrument; clock 14:25-14:34 AEDT)
- Refs: `git ls-remote origin` -> main `17fc0dbcf03a4dd48908882a1f36e7c6882b58f4`, b1117 head `a9960f688c1fd2058262174c601c3d2da5178bff` (equals the builder's READY line), b1093 `531c83be`. `gh api -X GET compare main...b1117/...`: diverged, ahead 2, behind 1, merge base `7104179f`, files: `docs/ENGINE.md` +1 -1, `PurchaseCalculator.cs` +3 -7, `PurchaseSiteAllocationTests.cs` +78 -11. `compare 7104179f...17fc0dbc`: 1 commit (#143), 3 files. `commits/17fc0dbc`: 1 parent. Actions runs for head_sha 17fc0dbc: "Push on main" and "ci" both completed success.
- Disjointness (`comm -12` of path lists printed by `gh api compare --jq`): vs #143 = 0, vs b1093 (14 paths) = 0, control `comm` of the list with itself = 3; M77's B1125 is not pushed (no b1125 ref), so only its stated property `web/src/api/contract[^/]*.test.ts` was tested: 0 hits on the 3 paths, control: a planted `web/src/api/contract.sync.test.ts` gives 1. Open PRs: #121, #120 (dependabot).
- Product file: raw fetches at main and at head (`gh api` raw accept) -> 1051 and 1047 lines; `diff` = 3 hunks; sha256 prefix of the head file `ad1c6d2e`, equal to the builder's STATUS. **Product diff is +3 -7 (net -4), not "net -4 +1"**: one call line moved (1 add, 1 delete), two doc-comment lines rewritten, the 4-line guard deleted. The coordinator's board remark (not literally one line) is borne out.
- Line pointers (`grep -n` on the raw files): main: structure stop `:169`, `CheckSourceValidity` `:173`, call `:209`, line-check stop `:212-216`, `var sectionResults` `:217`, Priced true return `:266`, method `:578`, guard `:580-583`. Head: call `:216`, stop's return `:214`, `var sectionResults` `:217`. Blocking raise sites in the file: 7 raise lines plus the two helpers' call sites; `IssueSeverity.Blocking` occurs 10 times at main.
- Api word: `Mapping.cs:69` `Status = r.Priced ? "Succeeded" : "Blocked"` (supports reading "blocked = did not price"; the kit left it out for size, the gate re-reads it in Step 2/7).
- Ruling: `CLARIFICATIONS.md:2203` entry C-82, words as relayed: "b -- Show it unless the calculator stopped"; the entry says it is RELAYED and the card was not queried (I did not read any card: fence). Landing rule lines `:758`, `:774` printed (squash with head pinned).
- Jira GET (`project = MPSCALC AND ( key = ... )`): MPSCALC-257 Backlog, labels include `tier-1`, 2 comments (40655, 40663); clause 2 waits for this build. MPSCALC-367 Backlog, label `tier-2`, comment 40664 restates the acceptance to the ruling; its description still asks for the opposite.
- Round count: the 14:27 count over `Briefs/*_STATUS.md`: 89 `^VERDICT:` lines, 35 contain ` NO GO ` project-wide; on this class (purchase site-allocation check) one verdict line: B1091 GO WITH FINDINGS round 1 of 2 -> "NO GO 0 before, round 1 of 2". (B1119, the previous G284 gate, already has its verdict: GO WITH FINDINGS.)
- Live panes (`tmux list-panes -a -F '#{@cockpit_name}'`, 14:25): tuesday, Datasec/HPSM-POC-H102, -H103, -H101, -G285, Datasec/MPS-G283, fleet-monitor. M76 closed. G287 not live; `.tools/b1128`, `wt-b1128-*` absent (`[ -e ]`); `.tools/b1119/clone` exists (not reused: foreign seat dir; the kit makes its own local clone).
- Disk `df -g`: 30 GiB free at 14:3x (the kit STOPs under 25, re-checked after each build). Load1 7.14 at 14:27. `lsof` listening: `:5000` only. Ports: none needed (Engine in-process; Api tests bind port 0, `ApiProcess.cs:35`), so no block assigned and no word-bounded kit scan was needed.
- CI: `ci.yml:42` build, `:43` test, `:58` node 24, `:61-63` web steps; `Directory.Build.props:6` TreatWarningsAsErrors (relayed by the builder kit; not re-read). Only comments in tests/src mention `docs/ENGINE.md`, so no test reads the register row.
- Model: `model-routing.md:109` row G2 (tier 2), `:92` row C2 for the builder; `models_latest.json:23` `claude-sonnet-5-5`. `brief_seat.sh:24` defaults to Opus; `BRIEF_SEAT_LEVEL=sonnet` is inside the quotes of the launch line.

## Cross-checks done on the kit (as asked)
- Every severity line against every step: Blocker "shown on stopped / hidden on priced" and "any figure/order difference" -> Step 3; "outside the 3 paths" -> Step 1; "new literal / changed message" -> Step 7; Rule S Blocker -> Step 8 (and Rule S); secret -> Step 8 gitleaks; head moved -> Step 0 REFUSE and Step 8 ls-remote. Major: done-when -> Step 5; builder row wrong -> Step 4; X-44 sentence -> Step 4; GP1/GP3 survive -> Step 6; landing sentence -> Step 9. Note items map to Steps 4, 6, 8. Every Step 0-9 has at least one severity line except Step 2 (it feeds Step 3's case list; no severity of its own).
- Every REFUSE against launch state today: four-underscore (stamp pending, correct to fire only on the unstamped copy), pane G287 (not live), branch head `a9960f68` (equals), class NO GO 0 (true), `.tools/b1128`/worktrees (absent), builder last line (prefix `READY FOR QA: B1117 ... @ a9960f688c1f` matches the STATUS last line), model id (`claude-sonnet-5-5`), free space 30 vs 25 (passes with 5 GiB margin; a heavy build plus three worktrees could cut it, hence the per-build `df`). None fires at launch.

## D-decisions (mine)
- D-1 Rule L split heavy/light (as asked). Heavy = restore, whole-solution build, whole-solution test; light = Engine test project work under `light.lock`.
- D-2 The core is a property oracle (Step 3): "Differs iff Priced" at head, "Differs iff Priced and no Blocking" at base, plus whole-result equality head vs base minus the one issue, over a closed list of cases stated as a property (one per Blocking raise site, each of the three line-check codes, combinations). It addresses the builder's gaps: no builder row for COLOUR VOLUME ON MONO, fixture 2 never separately red at the pin.
- D-3 Own plants GP1-GP6 (GP6 = "at most one Blocking issue" predicate, kills only if fixture 4 exists). GP1 and GP3 survivors are Majors; others Notes.
- D-4 One local clone of `2_Project_Files` (after one fetch under `.tools/.git-lock`), three worktrees (base, merged, mut); no second dotnet install (`T/dotnet/dotnet`, 10.0.401 per builder). Probes and plants only in base and mut.
- D-5 Web and python CI jobs NOT RUN locally with proof: base..merged diff in `web/ tools/ infra/ scripts/ .github/` is 0 lines (to be printed) and CI on main's push is success.
- D-6 Landing: squash, head pinned (`CLARIFICATIONS.md:758`, `:774`); landing files per the model B1119 (five files); keys only in title/subject; the builder's commit messages carry a key and a trailer, the squash replaces them.
- D-7 Launch line is the cockpit form (the template). Tuesday may wrap it in `launch_when_cool.sh` as the earlier stamps did.
- D-8 To fit 18 KB I removed, from the kit text, the "net -4 +1" quotation, the label detail of the tickets and the Api `Mapping.cs:69` line; they are in this report.

## Q-questions for Tuesday (each with a default)
- Q-1 Tier. MPSCALC-257 carries label `tier-1` (it is the feature; its first gate B1091 ran tier 1) and the edited file is the quote-calculation function, but the change adds a Review issue and moves no figure; a figure change is a Blocker. Default: tier 2 Sonnet (G2, as stamped for the builder's Q-1). If you read "inside the pricing function" as a quote-figure path, the default flips to tier 1 Opus (G1) and `BRIEF_SEAT_LEVEL=opus`; the kit needs only the level word and row line changed.
- Q-2 The gate writes untracked probe test files in its own scratch worktrees (never committed, never pushed) although "findings only: no code". Default: yes, same as B1119's mutants in `-mut`.
- Q-3 One fetch into `2_Project_Files` by the seat (a ref write in the project repo under `.tools/.git-lock`), as M76 and M77 did. Default: yes (S4).
- Q-4 Whether the 90-minute target is realistic with load1 above 7 for hours (the builder lost about 2 hours to it; the Engine suites are the heavy part). Default: keep 90/180, with only three heavy starts waiting.
- Q-5 Release wording: the squash body states "the warning sentence is unchanged" only if Step 7 proves no user reach. Default: as written.

## Contradictions found
- Builder kit: "one moved call, a removed 4-line guard, net -4 +1" vs measured product diff +3 -7.
- Builder kit Step 6 "B: 3 files" vs actual commit B 2 files (his Correction 3); the branch is 3 files.
- Builder kit: new rows "RED at the pin" for fixtures 1-7; fixture 3 is green at the pin by design and fixture 2 is not separately shown red (shares the changed row, which stops at its first assertion).
- MPSCALC-367's description (and original acceptance "green at the unedited product") says the opposite of the ruling; its comment 40664 restates it ("red at code main as it stands"). The kit uses the restated text and quotes the original in Step 5.
- Builder's STATUS base `7104179f` vs the kit's stated pin `f8f808c4` (his Correction 1); now main is a third sha, `17fc0dbc`.
- Builder STATUS says finished 14:24 and the Stamp window said launch until 20:00; no clash, but the builder missed its READY target by load.
- The builder's doc-comment line is about 160 characters against a 130-character neighbourhood; no analyser object (0 warnings), so only a Note.

## UNMEASURED
- No dotnet build, test or plant ran here. Every builder count (red 5 at the pin, 628/196/3167, P1-P5, 34->39 names, 0 literals, gitleaks) is RELAYED.
- The probe file does not exist; whether COLOUR VOLUME ON MONO and the quote-level codes are reachable from a group input (the kit makes unreachable a Note).
- `docs/ENGINE.md` X-44 new sentence was read only through the builder STATUS and truncated grep output, not the whole row at the branch; the gate reads it whole.
- `Directory.Build.props:6` not re-read by me. B1125 branch paths (unpushed). Whether any web or Api code reacts to an extra Review issue (builder says no code reads sites; I only confirmed `Mapping.cs:69` and `QuoteEndpoints.cs` Blocking counts at 7104179f).
- Free space after builds (30 GiB now, STOP at 25).

## Outside-the-fences disclosure
- Read-only git on `2_Project_Files`: `ls-remote`, `grep`, `cat-file`, `show`, `log` (no fetch, no ref write, no worktree). `gh api -X GET` only, under the project's `.gh-config` (compare, commits, contents raw, pulls, actions/runs).
- Jira: I ran my own scratch script (`python3 -I`, GET only, JQL `project = MPSCALC AND ( key = ... )`) that reads the project `.env` in-process and prints no secret, instead of the project's `.tools/b562/jira.py` whose `keys` mode writes logs into the project's `.tools`. Output only in the session scratchpad (`.../scratchpad/b1128/`: raw fetches, jira.txt, diff inputs).
- I read the headers of `.tools/b1116/heavy.sh` and `hb.sh` (listing and reading, not running), `ls` of `.tools`, and `rev-parse HEAD` of `.tools/b1119/clone` (read-only).
- Read: B1117 kit and STATUS, B1119 kit and its evidence files, B1125 kit (partition lines), B1091 STATUS lines 103-119 and 172-175, `CLARIFICATIONS.md` 758, 774, 2203-2224, `model-routing.md` lines 90-111, `brief_seat.sh` 22-26, `models_latest.json`, `ci.yml`. Not read: `decision_queue`, `fleet/briefs_staged/`, scoreboard, `_ledger.md`, any other tree.
- One command listed the scratchpad directory by an unquoted glob (names and line counts of other sessions' scratch files, no content read); one `cd` attempt was refused by the hook and had no effect. `tmux list-panes`, `lsof`, `df`, `uptime` run read-only. No message, decision_queue write, Jira write or Azure call.
- Files written: the kit and this report only (plus the scratchpad files above).

Clock at close: Mon 2 Nov 2026 14:3x AEDT (`date` printed 14:34:27 at the last check).
