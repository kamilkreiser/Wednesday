STARTABLE: YES (conditional on Q-1: an existing refusal sentence fits; if you reject it the ticket is BLOCKED-ON-WORDS and the kit must not launch)

# B711 DRAFTER-REPORT: SEAT-M28, MPS lane M-PARITY, MPSCALC-302 (drafted 2026-10-26 07:50-08:1x AEDT, clock from `date`)

## BLUF
- An existing sentence fits: `ParityProof.cs:192` ("'<sheet>': N option records of colour panels in the store, but its panel heading block, its mapped devices and the pairs the catalogue map already holds give M: a per-device panel record is missing or extra."), reused byte for byte. Only wart: for a count-preserving swap N equals M ("4 ... give 4"). No new word, so not BLOCKED-ON-WORDS unless you rule the wart unacceptable (Q-1).
- PRIOR-WORK CHECK: the fix is NOT on main. `ParityProof.cs` at `f5a27af0` still reads `if (mine.Count != expected)` at line 190; the file has 4 commits, none after PR #84 (`acfcf5de`); 0 comments on the ticket; 0 hits for duplicate/multiset/swap in the three parity test files.
- Kit: 2 paths (`src/MpsCalc.Import/Parity/ParityProof.cs` edit of `CheckPanels` lines 188-193; NEW `tests/MpsCalc.Import.Tests/PanelParityMultisetTests.cs`, 4 `[Fact]`s), Sonnet (line 92), gate tier 1 Opus (line 108), ports 9780-9789 unused, branch `b711/mps-parity-multiset`, pane `Datasec/MPS-M28`. 8 stamp slots left blank.
- Open PRs: #112 (4 paths) and #117 (the B686 branch, 1 Api test path): 0 shared with either.
- Main is `f5a27af0a4994a884c739e7892181b71ae0e4b72` (matches the sweep).

## Facts re-measured (instrument; control)
- Main: `git --no-optional-locks ls-remote origin refs/heads/main` = `f5a27af0...`; `compare/f5a27af0...main` ahead_by 0. Also #115 is the head commit.
- File: `gh -X GET api contents/src/MpsCalc.Import/Parity/ParityProof.cs?ref=f5a27af0` .sha `16d2af67...`, .size 27856 (matches the sweep's 27,856), 500 lines by `wc -l` of the raw read. Lines 189-190 as the ticket cites (control: the same lines read by `cat -n` show the `int expected` sum and `if (mine.Count != expected)`).
- Commits touching it: 4 (`commits?path=`), last `acfcf5de` #84.
- Open PRs: `pulls?state=open` printed #117 and #112; `pulls/<n>/files --paginate` lists as in the kit. Control: 117's one file is the new GovernedNullClassEdges test, so the listing does return files.
- Ticket: Jira GET through the project `.env` in process, MPSCALC-302 Backlog, Medium, tier-1, 0 comments, 0 links; recommendation and acceptance quoted. Cross-checked with `B305_STATUS.md:343-348`.
- Existing tests: `PanelParityRecordsTests.cs` 159 lines / 7 tests, `PanelParityDeviceSourcesTests.cs` 151 / 3, `ParityTests.cs` 115 / 6 (`-c '\[(Fact|Theory)'`). `grep -c -i -E 'duplicate|multiset|swap'` over all three = 0, 0, 0 (control: a search for `missing or extra` hit `PanelParityDeviceSourcesTests.cs:130`, so the file contents were searchable; GitHub code search for `zzznosuchstring7f3a` printed 0).
- Sentence uses: `missing or extra` lives in `ParityProof.cs`, `PanelParityDeviceSourcesTests.cs` (exact assert, line 130) and `docs/IMPORTER.md` (line 90) only. Reusing it changes none.
- Ports: `lsof -nP -iTCP:9780-9789 -sTCP:LISTEN` empty, rc 1; positive control (python socket on 9780) listed 1 line, then empty rc 1 after. Word-boundary scan of 98 non-`.pre-` SEAT kits of 10-25 and 10-26 for `978[0-9]`: claimants B628 (H18, HPSM-POC, other repo) and B685 (M25, MPS, "tentative", in-process); live panes at 07:5x: `tuesday`, `Datasec/NexusAI-M13`, `Datasec/Security-Composer-G133`, `fleet-monitor`, so neither is live. Kits written today (B705, B706, B707) are not in the hit list. `SEAT-M28` count in kits 0 (control: `SEAT-M25` 1).
- Branches: `matching-refs/heads/b711` length 0 (control: `heads/b685` length 1). No `.tools/b711`, no `wt-b711-*` (control: `.tools/b686` lists).
- Routing: `grep -n -i -E '^\| (C2|G1|G-cap) '` = lines 92, 108, 111. Model id `claude-sonnet-5-5` (`models_latest.json` line 23, checked 07:42:13). `brief_seat.sh:24` defaults Opus; launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- CI: `ci.yml` build then test of `MpsCalc.slnx` (Release, no filter), `TreatWarningsAsErrors>true` count 1, `global.json` 10.0.100.
- Landing rule: `CLARIFICATIONS.md:809` (squash, head pinned) and project `CLAUDE.md:50-52` (CodeQL), read.
- Load at 07:54: 8.15 / 7.37 / 6.54 (the launch waiter will hold until below 7).
- Kit text: 8 lines hold four underscores (slots 7 + last line); 0 non-ASCII bytes (`LC_ALL=C grep -c '[^ -~]'` = 0, rc 1 as it should).

## D-decisions (override at the stamp)
- D1 reuse sentence (d) verbatim; STOP if it cannot express the fix (no new word).
- D2 one NEW Import test file, existing three parity files stay byte-equal.
- D3 multiset replaces the count test in the same `if`; one refusal per sheet.
- D4 base `f5a27af0`; D5 one commit, branch `b711/mps-parity-multiset`; D6 own mutants P1-P6; D7 no provider matrix, no Api/web.
- D8 closed-list property for the sweep (stated as property first, then "at least P1-P6", then "prove or STOP").
- Rows: control, cross-device duplicate (the acceptance row), same-device duplicate, extra duplicate (5 records). Cap 4 extra rows.

## Q-questions for Tuesday (each with a default)
- Q-1: Is sentence (d) acceptable when N equals M ("4 option records ... give 4: a per-device panel record is missing or extra")? Default: YES, accept. It is true (one pair missing and one extra), adds no word and keeps every existing assert green. If NO, the ticket is BLOCKED-ON-WORDS (a new sentence goes to the product owner's words gate) and the kit must not launch.
- Q-2: Ports 9780-9789 kept although B628 (H18) and B685 (M25) claim the block on paper? Default: YES, the lane listens on nothing; no live pane holds either.
- Q-3: Round count: stamp as "NO GO 0 of 2 on class 'count-preserving panel tamper says AGREE'", Opus gate at tier 1 per line 108 because this edits the parity tool. Default: YES.
- Q-4: Test location: a new file in `tests/MpsCalc.Import.Tests/` (the sweep's fence), not appended to `PanelParityRecordsTests.cs`. Default: new file (appending edits an existing file the lane should leave byte-equal).

## UNMEASURED
Nothing built, run or compiled. Not measured: the unfixed answers for the same-device shape (reasoned from lines 177-190; the cross-device shape is the gate's measured probe); the exact fixed-head sentences (expected 4/4, 4/4, 5/4); that a `with`-copied `StoredOption` stays in the `excluded` set; mutants P5 and P6 killers (least sure; the kit tells the seat to build a row inside the 4-row cap or prove equivalence); Import test count at main; CodeQL on the new head; load at launch.

## Outside-the-fences disclosure
Read-only only. Read: DRAFTER_RULES.md, the B686 template kit, the sweep (grep of its MPS/LANES lines), routing lines, `models_latest.json`, `brief_seat.sh` line 24, SEAT kit file names and port-scan lines (kits of 10-25/10-26), project `CLAUDE.md` lines 50-52, `CLARIFICATIONS.md` line 809, `BACKLOG.md` grep hits for the finding, `B305_STATUS.md` lines 335-352, raw files from GitHub at `f5a27af0` (ParityProof.cs, three test files, docs/IMPORTER.md, ci.yml, Directory.Build.props, global.json). Network: `gh -X GET api` under the project's `GH_CONFIG_DIR` (including two `search/code` GETs), one Jira GET from the project `.env` in process (token not printed), one `git ls-remote`. A `tmux list-panes` and `lsof` plus a 6-second loopback python socket for the port control (freed). Scratch copies of raw files in the session scratchpad. No decision card read, no `decision_queue.sh`, no `fleet/briefs_staged/`, no scoreboard or `_ledger.md`, no WEDNESDAY/FRIDAY tree. Wrote only the kit and this report. The Jira helper: the project has no read helper script, so I used an in-process python GET (stdlib only).
