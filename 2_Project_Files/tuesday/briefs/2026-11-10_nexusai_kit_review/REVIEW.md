ROUND 2: KITS STARTABLE: B1430, B1431, B1432, B1433, B1434 (each still needs Tuesday's stamp: 3 slots plus READ-WHOLE) | HOLD: none

# ROUND 2: re-review of the redrafted kits (06:27-06:30 AEDT 2026-11-10, by `date`)

**What I read in full:** the five kits as they stand now (B1430 194 lines, B1431 243, B1432 187, B1433 130, B1434 renamed `..._SEAT-R202_...`, 63 lines) and `REDRAFT.md` (190 lines). I compared the parts that changed against each `.pre-1110-review` copy.

**Fences:** same as round 1. `gh` was GET only. Jira was read only through a scratch copy of the helper, with its write verbs set to None. No git write verb was used, and no token was printed. The only file written is this one.

## R2-1. Every round-1 HOLD reason, at file:line

| Round-1 HOLD reason | Resolved? | Where now |
|---|---|---|
| Jira helper hard-codes `/Volumes/Laptop-DEV` (all five) | **RESOLVED** | Each seat copies the helper into its own `.tools/` folder, re-points only the 2 path lines, and proves the import: B1430:65, B1431:87, B1432:57, B1433:63, B1434:27 (and :26, :39). Reads go through the copy: B1430:169, B1431:218, B1432:162, B1433:81 (PRIOR WORK), B1434:26. **I replayed the kit's steps** on a scratch copy: `cmp` equal for both files; after `sed`, the diff shows 4 `^[<>]` lines and `Laptop-DEV` occurs 0 times; the import works; `( key = RD-798 )` returns 1 and the nonsense search returns 0. The path lines are 8 and 12 (`grep -n`). My round-1 "9 and 13" was off by one, and the kits have it right. The original file is untouched. |
| S/F kits did not own the existing test files their tickets name; feedback-attachments contradiction | **RESOLVED** | OWNS-S B1430:44-46 (feedback-attachments plus 2 more); OWNS-F B1432:32-39 (8 files); OWNS-T B1431:44-68 (25 files, neither of the two shared files); OWNS-B B1433:42-44 (rd486 plus 2). The rule text is at B1430:49 and the same line in each kit. |
| Cross-lane tickets contradicted THE PROPERTY; one-sided sequencing | **RESOLVED** | 19 tickets are dropped (B1430:58, B1431:81, B1432:51, B1433:57, B1434:36). Moved files are inside the receiving lane's OWNS block: 13 backend files plus 1 e2e test to S (B1430:30-43), riskAlertScheduler to F (B1432:30), with the matching `-` lines in B (B1433:28-41). Block 3 in S and F now holds only tickets whose files are all theirs (B1430:140-141, B1432:143-144). B has no Block 3 (B1433:89-90). No cross-lane wait remains. |
| The drafter's partition claim modelled a different partition | **RESOLVED** | Every kit now carries an explicit OWNS block, and the program reads it as written (see R2-2). |
| Copy-to folder `NexusAI/Briefs/` does not exist | **RESOLVED** | `1_Project_Definition/Briefs/`: B1430:65, B1431:87, B1432:57, B1433:63. `NexusAI/Briefs/` now occurs 0 times in all five. |
| B1431/B1432/B1433 on Opus where Sonnet is routed | **RESOLVED** | Level and model lines: B1431:4, B1432:4, B1433:4 (`claude-sonnet-5-5`, `models_latest.json:23`, row `model-routing.md:92`). Launch lines carry `BRIEF_SEAT_LEVEL=sonnet`: B1431:241, B1432:185, B1433:128. S stays opus (B1430:4, :192; row C3 :93). |
| B1431: no fence on `deploy-demo.yml` | **RESOLVED** | OWNS-T has a `-` line for it (B1431:43). HOLD 12 (B1431:84) bars any edit to `deploy-demo.yml` or any `CI_DEPLOY_ENABLED` line, as an item-level NEEDS-SHARED, and bars running the deploy scripts. Every builder kit says the file is owned by no lane (B1430:51, B1431:73, B1432:44, B1433:49). At source the `CI_DEPLOY_ENABLED` lines are 16, 53 and 91, as stated. |
| Person name in the B1431 and B1432 queue text | **RESOLVED** | B1431:145 and B1432:78 now say "the product owner's". HOLD 11 is in every builder kit (B1430:62, B1431:84, B1432:54, B1433:60). |
| B1432 index.js reserved now (13 tickets held) | **RESOLVED per ruling** | B1432:20, :54 (HOLD 12), :61. I ran its L3-branch filter (`rd-?937\|l3\|roles-?shell`) over all 442 origin branches: 0 hits, so no false positive today; the control `refs/heads/main$` returns 1. RD-937 reads To Do. |
| B1433 line 40 sent the seat to S-owned or unticketed alerts | **RESOLVED** | B1433:67 now names only RD-798's remainder, RD-804 and RD-805 (its five files). |
| B1434: seat R196 collision | **RESOLVED** | R202 at B1434:3, :5, :6, :39, :44. R196 occurs 0 times in the kit. R202 appears in no other brief's file name or content (`grep -l` over `briefs/*.md` found only this kit). |
| B1434: `pwd -P` is not `P` | **RESOLVED** | B1434:44 |
| B1434: name-scan library not underscore-aware | **RESOLVED** | B1434:20 replaces the `person` pattern with the underscore-aware form, with `_by_<name>_` controls and a printed diff. |
| B1434: false late-INSERT fact | **RESOLVED** | B1434:17 now says RD-219 only. Re-read now: `late INSERT` returns RD-219; `ROLLBACK` returns 61. |
| B1434: HISTORY entry for #182 | **RESOLVED per ruling** | B1434:3, :10 and :34 say no #182 entry. |
| B1434: "builders touch no 1_Project_Definition" | **RESOLVED** | B1434:9 |

## R2-2. Partition: my own program, over origin main's tree now

**Inputs:**
- `branches/main` read at 06:28:54 AEDT: `3929b7946e2de85ce2ea312ac70bb64134a767e6`.
- `git/trees/<sha>?recursive=1`: 985 blobs, `truncated` false.
- `scratchpad/prog/partition2.py` parses each kit's `OWNS-<L>` fence block exactly as written, including `-` and `+new`, plus each kit's queue table. It is my program, not the redrafter's.

**Result:**
- Files claimed by more than one lane: **0**. Per lane: T 248, F 114, B 81, S 24, R 1.
- Spot checks:
  - `scripts/verify-expected-counts.json`: no lane
  - `.github/workflows/deploy-demo.yml`: no lane
  - `static/js/index.js` and `static/index.html`: F
  - `__tests__/rd486-...`: B
  - `__tests__/feedback-attachments.test.js`: S
  - `docs/role-capabilities.json`: S
  - `backend/services/riskAlertScheduler.js`: F
  - `backend/services/emailService.js`: B
- New files: a synthetic `__tests__/rd<N>-zz.test.js` for each of the 259 queued keys is claimed by exactly its own lane (0 collisions). New non-test paths fall to exactly one lane each (backend B; static and e2e F; scripts, docs and .github T).
- Queues: S 74, T 96, F 75, B 14. No key appears in two kits, and none changed lane. 19 keys were dropped, exactly the 19 the kits list.
- Queued tickets naming a file outside their own lane: 6. All six are declared exceptions:
  - the counts file, which no lane owns (RD-908, RD-914, RD-458, RD-901)
  - `backend/server.js` as context only, behind NEEDS-SHARED (RD-980 at B1431:75, RD-798 at B1433:52).
- **Controls:**
  - Planting `static/js/index.js` into OWNS-B gives exactly 1 multi-claimed file, so the check can fail.
  - Removing T's `- .github/workflows/deploy-demo.yml` line makes T claim that file.
- **Open PRs:** 0 (control: the closed list returns #184 and #183). `b143*` or `records/b1434*` refs on origin: 0 of 442.

## R2-3. New problems introduced?

**None that holds a kit.** Checked across all five kits:

- **Holds:** No PR, no merge, no push to main, no deploy, no az, no mail, and no Jira write outside B1434.
- **CodeQL:** `refs/pull` appears only in the "never a landing condition" sentence (1 per builder kit, 0 in B1434).
- **Launch lines:** levels opus, sonnet, sonnet, sonnet, sonnet. `CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude` appears once in each.
- **Names:** the underscore-aware name scan (11 names) has 0 hits in all five (controls: `x_by_kam_y` and `_by_Peter_` fire, `kamera` does not).
- **Slots:** exactly 4 four-underscore lines per kit, and the last line is `READ-WHOLE-BY-TUESDAY: ____`.
- **Clocks and placeholders:** no `HH:Mx` placeholder clock; no `@X@` token.
- **Stale path:** `Laptop-DEV` occurs only inside the helper re-point instruction (4 per kit, all on that one line).

**Minor items, none a HOLD:**

- (a) `@MAIN@` is still absent. Main is a literal sha, once per kit at line 1. Tuesday's ruling keeps four slots, and the sha is still main at 06:28:54. If main moves before launch, the kits already say "REBUILD".
- (b) "CROSS-WAIT" still appears in the HANDOVER and STATUS sections of the builder kits (for example B1430:175, :178), although nothing produces one now. It is harmless leftover text.
- (c) B1434's STATUS first line differs between B1434:39 (`B1434 STATUS (placeholder, Step 0 running)`) and B1434:53 (`RECORDS B1434: RUNNING`). This was there before the redraft. The seat may ask about it; the default is to use :53 after Step 0.
- (d) The `l3` alternative in F's L3 filter (B1432:54) can false-positive on a future branch name containing "l3". It reads 0 today, and a false positive only stops the seat with a question, which fails safe.
- (e) B1431 RD-478 (Block 4, B1431:200-203) removes "VM/local-model code" across the tree, so it will likely need files outside OWNS-T and stop under the kit's own rules. This was there before the redraft and is placed last.

## R2-4. Facts re-read at source this round (2 or more per kit)

| Kit | Fact | Reading |
|---|---|---|
| all | origin main | `3929b7946e2de85ce2ea312ac70bb64134a767e6` (`branches/main`) |
| all | queue tickets To Do | 259 of 259 To Do (none missing). First tickets RD-929, RD-970, RD-962 and RD-798 all To Do. |
| B1430 | moved files exist at main; ITEMISED-CHANGES hash | `backend/routes/feedback.js`, `backend/routes/sustainability.js` and `__tests__/rd436-r4-enforce-stamp-and-status.test.js` are in the tree; `backend/services/capabilities.js` is not (it is new, as stated). The project copy's sha256 prefix is `6ba866d3e960fa9b`. |
| B1431 | `CI_DEPLOY_ENABLED` lines in deploy-demo.yml | 16, 53, 91 (B1431:84 is right) |
| B1431 | b774lib lines to re-point | 8 and 12 (the kit is right) |
| B1432 | L3 filter today; RD-937 | 0 of 442 branches match; RD-937 To Do |
| B1432 | `backend/services/riskAlertScheduler.js` | in the tree; claimed by F only |
| B1433 | alerts 152 and 153 | both open (learningManager); `__tests__/rd503-r2-...` and `security-fixes.test.js` are in the tree |
| B1434 | alerts 164 and 219 | fixed (the RD-799/RD-800 ranges, sampled at both ends) |
| B1434 | RD-936 comments; label `b1434-2026-11-10` | 0 and 0 (label control from round 1: `b1363-2026-11-07` = 8) |
| B1434 | late INSERT | RD-219 only; `ROLLBACK` = 61 |

**Environment at the time of these reads:**
- Ports: `lsof -nP -iTCP:9900-9939 -sTCP:LISTEN` printed nothing at 06:29:21 (rc 1); the control count of all listeners is 11.
- Load: load1 1.54 (`uptime` 06:29).

## R2-5. Stamp values each kit needs (for `stamp_brief.py`; every clock is `@NOW@`; Tuesday writes only reads Tuesday has done)

**Common to all five:**

- **Main sha:** re-read `branches/main` in the stamp action. The reviewer's read: `3929b7946e2de85ce2ea312ac70bb64134a767e6`. If it differs, add "main moved to <sha>; rebuild every pointer" to STAMP.
- **`STAMP:`** `STAMPED @NOW@ AEDT 2026-11-10 by Tuesday. Read whole by Tuesday: this kit. Tuesday's reads just before this stamp: main <sha40> (branches/main); open PRs 0; b143*/records refs 0; Deploy demo on main skipped; ports <block> free (lsof).` Then add the rulings applied:
  - helper copy
  - Sonnet for T, F and B
  - deploy-demo fence
  - test ownership
  - index.js released to F
  - R202, with no #182 entry
  - 19 dropped
  - Briefs folder
- **`LAUNCH WINDOW:`** `from @NOW@; load1 <read in the stamp action> (launch_when_cool waits below 7); live seats beside you: the other NexusAI lanes N114-N117 and R202 as launched; one waiter (launch_when_cool, GAP_MIN 120 s).`
- **`HARD STOP:`** an absolute AEDT clock that Tuesday prints with `date -v+4H '+%H:%M AEDT %Y-%m-%d'` in the stamp action for builders, and `date -v+2H` for B1434. This is the reviewer's suggestion. Never type it.
- **`READ-WHOLE`:** `DONE @NOW@`. Copy each kit to `.pre-stamp` first; there is none yet.

**Per kit:**

| Kit | Pane | Level and model | Port block | Kit-specific additions |
|---|---|---|---|---|
| B1430 | `Datasec/NexusAI-N114` | opus / `claude-opus-5-5` | 9900-9909 | none beyond the common values |
| B1431 | `Datasec/NexusAI-N115` | sonnet / `claude-sonnet-5-5` | 9910-9919 | STAMP: "HOLD 12 (deploy-demo / CI_DEPLOY_ENABLED) is item-level NEEDS-SHARED", which answers REDRAFT Q2 if Tuesday keeps the default |
| B1432 | `Datasec/NexusAI-N116` | sonnet / `claude-sonnet-5-5` | 9920-9929 | STAMP: "RD-937 read To Do by Tuesday at the stamp" |
| B1433 | `Datasec/NexusAI-N117` | sonnet / `claude-sonnet-5-5` | 9930-9939 | none beyond the common values |
| B1434 | `Datasec/NexusAI-R202` | sonnet / `claude-sonnet-5-5` | none | STAMP: "no HISTORY.md entry for #182 (Tuesday's 9 Nov answer stands)" and "STATUS first line: use `RECORDS B1434: RUNNING` after Step 0" (minor item c); HARD STOP: no Jira write from 20 minutes before it |

**Launch order:** these are suggestions.
- B1434 and B1430 first: S is the long Opus lane, and R holds the only Jira writes.
- Then T, F and B, one waiter at a time.

---

# ROUND 1 (06:02-06:12 AEDT, kept as written)

KITS STARTABLE: none | HOLD: B1430, B1431, B1432, B1433, B1434 - all five depend on the NexusAI Jira helper session-tools/b774/b774lib.py, which still hard-codes /Volumes/Laptop-DEV (lines 9 and 13; corrected in round 2: lines 8 and 12). Importing it on this drive fails with FileNotFoundError, so every seat hits REFUSE 4 ("Jira read is blind") at Step 0. Each kit also has its own items below: B1430 (S/F kits do not own the existing test files their tickets name; the cross-lane PROPERTY contradicts itself), B1431 (Opus where the routing table says Sonnet; no fence on deploy-demo.yml; a person name in the queue text), B1432 (Opus where Sonnet is routed; 14 tickets name test files no lane owns; 13 tickets held on the index.js reservation; a person name in the queue text), B1433 (Opus where Sonnet is routed; line 40 sends the seat to alerts whose tickets are lane S's or have no ticket), B1434 (seat R196 collides with B1386; the name-scan library it copies is not underscore-aware; `pwd -P` is not `P`; a false search fact)

# NexusAI lane kits B1430-B1434: independent review

Reviewer: a read-only Agent-tool reviewer for Tuesday. Clocks come from `date` in the same actions: start 06:02:26 AEDT 2026-11-10, ports read at 06:05:16 AEDT.
What I read in full, every line: the five kits, `2026-11-10_nexusai_sweep/lanes.md` (114 lines), `DRAFTER_RULES.md` (75 lines) and NexusAI `CLAUDE.md` (402 lines). I also read the cited CLARIFICATIONS entries, `disjoint_check.py` and its output, and the headers of `b774lib.py`, `launch_when_cool.sh`, `brief_seat.sh` and `stamp_brief.py`.
Instruments used:
- `gh api -X GET` under `GH_CONFIG_DIR=/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config`. The login contains "datasec": count 1, not quoted.
- Python programs in my scratchpad (`partition.py`, `seats.py`, `names.py`, `jira_read.py`).
- `lsof`.
- Jira, read-only. b774lib was loaded in memory with the stale drive name re-pointed. I disarmed its three write verbs (set to None) and called only `search`/`comments`. Controls: `( key = RD-798 )` returned 1; `( text ~ "zzqxnonexist" )` returned 0. No file was written outside this REVIEW.md, and no token was printed.

## Project rules, found by grep at source (not assumed)

- **Landing rule:** `NexusAI/1_Project_Definition/CLARIFICATIONS.md:2067` (C-190 item 2) says: "open a PR from the gated branch, wait for CodeQL ..., then land the SAME commit. Never squash, never rebase". The practice is a head-pinned merge commit, as in C-224 (`:2412`) and the PR #112 record (`:2397`). C-218 (`:2362`) records the one squash error.
- **Deploy rules:**
  - C-224 (`CLARIFICATIONS.md:2412`): no demo deploy until RD-876 part 2 lands.
  - C-127 (`:1358`): a demo redeploy waits for a Tuesday GO that quotes it.
  - C-220 (`:2378-2379`): `deploy-demo.yml` may be edited only on its two `azure/login` lines. The `if` tests on `CI_DEPLOY_ENABLED` (lines 53 and 91) and the switch are never touched.
  - At main, `deploy-demo.yml:26-32` triggers on push to main with paths-ignore `**.md`, `docs/**` and `tests/**`.
  - Run 42572360236 on 3929b794 concluded skipped, with jobs skipped,skipped. Repository variables: 0.
- **Ticket move rule:** `NexusAI/CLAUDE.md:302`: a code change moves to `Testing`.
- **CodeQL judgement:** C-240 (`CLARIFICATIONS.md:2542`): a fix is judged on main's analysis after landing.

## Cross-kit results (items 1-8)

| # | Item | Result | Evidence |
|---|---|---|---|
| 1a | Partition by file (the kits' own YOUR FILES globs, over origin main's tree) | **FINDING** | My `partition.py` ran over `git/trees/3929b794?recursive=1` (985 blobs, `truncated` false; identical to the drafter's `tree_at_3929b794.txt`, compared with cmp). Result: 1 file is claimed by two kits, `__tests__/rd486-ai-test-key-forwarding.test.js` (T's "existing __tests__ named by T tickets" at B1431:20 and B's at B1433:20); the text rule at B1430:30 etc. resolves it to B. Control: planting `static/js/index.js` into S's globs was caught as ['S','F']. Queue keys: S 86, T 98, F 78, B 16, no key in two kits, each equal to `final_assignment.json`. |
| 1b | Existing test files no lane owns | **FINDING (blocks tickets)** | The S and F YOUR FILES lines (B1430:20, B1432:20) include only *new* `__tests__/rd<N>-*`. The T and B lines (B1431:20, B1433:20) also include *existing* test files their tickets name. lanes.md:37 says an existing test file belongs to the lane whose ticket names it. Effect: S tickets RD-908, RD-855 and RD-691 name existing tests in no lane, and F has 23 such ticket-file pairs over 14 tickets (RD-349, 221, 151, 235, 512, 513, 514, 515, 540, 676, 677, 678, 679, 680, 704, 901). Building any of them breaks THE PROPERTY (1) and becomes a STOP. |
| 1c | `__tests__/feedback-attachments.test.js` | **FINDING** | B1430:30 says S keeps it (RD-366), but S's YOUR FILES (B1430:20) excludes it. T's YOUR FILES (B1431:20) claims it through RD-346. The two sides contradict each other. |
| 1d | Cross-lane (Block 3 and A6/A7) tickets against THE PROPERTY | **FINDING** | Block 3 says each ticket is "done wholly here" and edits another lane's file (S 22, F 4, B 2, T 1; e.g. B1430:117-138, B1432:125-128, B1433:66-67). THE PROPERTY (1) (B1430:17) and "the only files a branch of yours may touch" (B1430:20) forbid exactly that, and no carve-out is written. The sequencing check is also one-sided: the borrowing lane checks the owner's branches (B1430:114), but the owner's kit never checks the borrower's open branches on its own files. Example: B's RD-805 (B1433:45) and S's RD-768/RD-806 (B1430:120, :137) both edit `backend/services/emailService.js`. |
| 1e | The drafter's "MEASURED ... 0" partition claim (B1430:19 and the same line in each kit) | **FINDING** | `disjoint_check.py` does not encode D3: its S list lacks `docs/role-capabilities.json`, so it counts that file as T's. It also skips `__tests__/` entirely. Its "0" is about a different partition than the one the kits state. |
| 1f | The "other lanes" side of each partition | **FINDING (minor)** | B1430:21, B1432:21 and B1433:21 describe lane T as "scripts/**" only, leaving out `.github/**`, `docs/**`, `tests/**`, package*.json, jest.config.js, Dockerfile, bicep and azure-marketplace. B1430:21 also lists `scripts/**` as T's although S owns `scripts/role-capability-inventory.js`. |
| 1g | Open NexusAI PRs touching a lane file | **PASS** | `pulls?state=open` returned 0 (control: `state=closed` lists #184-#180 with merge shas). No `b143*` or `records/b1434*` ref exists among the 442 branches (control: `main` present). The four newest builder branches (b1344b, b1354, b1369, b1376) are 0 ahead of main. Branches other than these were not compared (UNMEASURED). |
| 2a | Deploy, merge, PR or push to main | **PASS** | S/T/F/B: "No pull request", push only `b143N/*`, "never main" (B1430:34, :156; the same in B1431-B1433). R: one plain push of `records/b1434-history`, no PR, no merge (B1434:10, :25). |
| 2b | Deploy-demo-on-merge trigger | **PASS** | No seat merges. The kits say a merge starts a Deploy demo run whose jobs must read skipped (B1430:34, :149). R's branch is `**.md`-only, so no run starts. |
| 2c | `deploy-demo.yml` edits | **FINDING (B1431)** | Lane T owns `.github/**` (B1431:20), and RD-605 (B1431:47, CI action versions) can reach `deploy-demo.yml`. HOLD 1 (B1431:34) forbids setting `CI_DEPLOY_ENABLED`, but nothing forbids editing the `if` lines 53/91 or the trigger. Add C-220's conditions verbatim: no edit to `deploy-demo.yml` beyond `uses:` pins, and such a branch is gated at G1. Also add "never execute `scripts/deploy-*.sh` or `setup-ci-oidc.sh`", because RD-328 and RD-634 edit `scripts/deploy-dev.sh`. |
| 2d | az, hosted host, Partner Center, mail to a human | **PASS** | All five forbid them (B1430:34 item 9; B1434:25). The IMDS address is stubbed for RD-968 (B1430:41). |
| 2e | Jira or Linear writes outside the records kit | **PASS** | Builder kits: GET verbs only, with `post_comment`/`create`/`do_transition` named as forbidden (B1430:153). Linear is mentioned 0 times in all five kits. |
| 3 | `refs/pull/N/head` as a landing condition | **PASS** | All four builder kits say never (B1430:146, B1431:163, B1432:136, B1433:75). B1434 reads alerts on current main (B1434:12); `refs/pull` appears 0 times in it. My read of main matches the kit facts: alerts 164-171 and 208-219 fixed; 152 and 153 open at `learningManager.js:125` and `:153`; 66 open; 0 dismissed. |
| 4 | Seat ids and ports | **FINDING (B1434)** | See "Seat ids and ports" below. |
| 5 | Model and tier | **FINDING (B1431, B1432, B1433)** | See the per-kit tables. All ids exist (`models_latest.json:17` claude-opus-5-5, `:23` claude-sonnet-5-5). All five launch lines put the level inside the quotes and carry `CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude` (the directory exists). `launch_when_cool.sh` usage `<name> <command>` matches. |
| 6 | Stale or false facts | Mostly PASS; FINDINGs listed per kit | 3 or more facts per kit re-read at source, below. |
| 7 | Name scans | **FINDING (B1431, B1432, B1434)** | My scan is underscore-aware: `(?<![A-Za-z])(kam\|kamil\|kreiser\|peter\|steve\|paul\|blanchard\|inch\|waite\|philip\|anupam)(?![a-z])` with re.I. Controls: `_by_kam_` and `_by_Kreiser_` fire, `kamera` does not. Hits: B1431:96 "Kam's 'investigate' ruling" and B1432:56 "Kam's commission", both in queue scope text a seat may paraphrase into a commit, plus B1430:41 (a path only: `fleet/state/kam_docs_1106/...`). B1434:20 tells the seat to copy the previous records scan library, but that library's person class uses `\bkam\b` and `\bpeter\b` (`session-tools/b1375/scanlib1114.py:20`), which is not underscore-aware, against DRAFTER_RULES:40-43. The builder kits ask for no name scan of their commit messages; add one that is underscore-aware. |
| 8 | Placeholders | **FINDING (all five)** | `@MAIN@` count 0 in all five (control: a planted line prints 1). The main sha is typed literally, once per kit (line 1, `3929b7946e2de85ce2ea312ac70bb64134a767e6`). Slot lines with four underscores: exactly 4 per kit (3 slots plus `READ-WHOLE-BY-TUESDAY: ____` as the last line), so they are countable and match each kit's own REFUSE 1 control. None has a `.pre-stamp` copy yet. Main is still 3929b794 at 06:02:26, so the literal sha is true today, but any move before launch makes line 1 stale. Put `@MAIN@` there, or add a MAIN slot. |

**The blocker shared by all five kits (6, MEASURED):** the kits name `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/b774/b774lib.py` for every Jira read and write (B1430:153, B1431:170, B1432:143, B1433:82, B1434:26).
- Its lines 9 and 13 hard-code `/Volumes/Laptop-DEV/...`, which does not exist (`ls`: No such file or directory).
- `python3 -I` importlib `exec_module` fails: `FileNotFoundError ... /Volumes/Laptop-DEV/.../jira-adf.py`.
- Fix inside each kit, without editing the project: at Step 1, `cp` `b774lib.py` and `jira-adf.py` into the seat's `.tools/bNNNN/`, re-point only the two path constants, show that `diff` changes exactly those two lines, and import the copy.
- The same stale prefix sits in every `session-tools/b13*/` tool B1434 copies (7 ENV lines). The tickets-by-lane copies and the lock tool are fine: `nexusai-lock.sh:84` defaults to Laptop-DEV, but the kits pass `NEXUSAI_LOCK_BASE` explicitly, and `locks-laptop-1017` exists on Datasec_DEV.

## B1430 - SEAT-N114 lane S (server)

| Check | Result | Where |
|---|---|---|
| Jira helper import | FINDING (blocker) | B1430:13, :153 |
| Step 0 copies the kit to `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/Briefs/` | FINDING: that folder does not exist (`ls`). The earlier N110-N113 kits were copied to `1_Project_Definition/Briefs/`, as B1434:34 does | B1430:37 |
| Existing test files (RD-908, RD-855, RD-691) and feedback-attachments (RD-366) | FINDING (1b, 1c) | B1430:20, :30 |
| Cross-lane PROPERTY contradiction (22 Block 3 tickets plus A6 RD-958, A7 RD-927) | FINDING (1d) | B1430:17, :20, :41, :114 |
| Itemised-document path is relative (`fleet/state/kam_docs_1106/...`) from a seat whose cwd is the project | FINDING (minor): write it absolute, `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_docs_1106/nexusai_roles_ui/ITEMISED-CHANGES.md` | B1430:41 |
| "the other three lanes S/T/F/B" lists four | cosmetic | B1430:11 |
| Model Opus, C3 row | PASS: L1 permission design and session revocation are row C3 (`model-routing.md:93`, O55 1st) | B1430:4 |
| Ports 9900-9909 | PASS (see below) | B1430:143 |
| Facts re-read at source | PASS: main `3929b794` (`branches/main`, 06:02:26). `server.js` has 22,431 lines; `:3508` is the `typeof jsonStorage.deleteSessionsForUser` guard; `jsonStorage.js` has 0 occurrences (control `createSession\|getSession` = 2). `conversationSessions` occurs once, at `:21828`. Counts file 5493/326. `ITEMISED-CHANGES.md` sha256 prefix `6ba866d3e960fa9b`, 542 lines, 136 I-rows, in both copies. Queue: 86 of 86 To Do, first RD-929 To Do. NOTE: the line numbers inside copied ticket titles are stale Jira text (e.g. RD-770 ":6049": the `includes('openai.com')` line is now `:6062`). The kit already says to re-derive them | B1430:1, :41, :64-65 |

## B1431 - SEAT-N115 lane T (tooling and tests)

| Check | Result | Where |
|---|---|---|
| Jira helper import | FINDING (blocker) | B1431:170 |
| Model: Opus, while the kit cites row C2, where `model-routing.md:92` puts S55 1st. lanes.md:84 says "Sonnet C2, G2". DRAFTER_RULES:60 says Sonnet first unless the table says Opus | FINDING: launch with `BRIEF_SEAT_LEVEL=sonnet`, model `claude-sonnet-5-5` (`models_latest.json:23`); a C3 surface already STOPs (B1431:4) | B1431:4, :193 |
| `deploy-demo.yml` and deploy scripts not fenced | FINDING (2c) | B1431:20, :34 |
| Person name in queue text: RD-458 "Kam's 'investigate' ruling" | FINDING (7): rephrase as "the product owner's ruling" | B1431:96 |
| feedback-attachments claimed by T's glob through RD-346, while S "keeps" it; rd486 claimed by both T and B | FINDING (1a, 1c): write "less `__tests__/rd486-...` and `__tests__/feedback-attachments.test.js`" into YOUR FILES | B1431:20, :31 |
| 57 of 98 tickets are keyword guesses, and each misplacement is a STOP-and-wait | FINDING (throughput): expect many round trips (RD-633, 635, 637 mail secrets; RD-389 static/js; RD-231 index.js). Prefer `MISPLACED <key> lane <X>`, then move on (lanes.md:113 Q3) | B1431:157 |
| Steps 0 Briefs path; branch slug example says "server-session-revocation" | FINDING (Briefs path, as B1430); cosmetic slug | B1431:37, :173 |
| Ports 9910-9919 | PASS | B1431:160 |
| Facts re-read | PASS: `package.json:27` lint placeholder; `build.yml:38/:41/:44` node -c, `:55` lint, `:84` `npm run verify -- --maxWorkers=2`; `jest.config.js` testPathIgnorePatterns includes `/tests/e2e/`; `verify-suite.sh:366` prints `VERDICT: PASS`; queue 98 of 98 To Do, first RD-970 To Do. RD-810's title says `:30`; the open alert 151 is at `tests/uat-run.js:43` (lanes.md:85 is right) | B1431:41, :46, :166 |

## B1432 - SEAT-N116 lane F (front end)

| Check | Result | Where |
|---|---|---|
| Jira helper import | FINDING (blocker) | B1432:143 |
| Model Opus where row C2 / lanes.md:79 say Sonnet C2, G2 | FINDING: `BRIEF_SEAT_LEVEL=sonnet`, `claude-sonnet-5-5` | B1432:4, :166 |
| 14 tickets name existing `__tests__` helpers, fixtures or tests that no lane owns | FINDING (1b): add "existing __tests__ files named by F tickets" to YOUR FILES | B1432:20 |
| `static/js/index.js` and `static/index.html` are reserved now ("NOT touched by this queue at all"), while lanes.md:33/:79 reserve them only "the day RD-937 starts" (RD-937 is held) | FINDING (scope): 13 of 78 F tickets name them (RD-146, 220, 349, 350, 439, 532, 613, 676, 677, 771, 835, 861, 901), including A12 RD-835 and A14 RD-771 from Block 1; all become HELD. Meanwhile S may edit index.js for RD-927/RD-892 (B1430:50, :125). Tuesday to choose | B1432:20, :39 |
| Person name: RD-262 "Kam's commission" | FINDING (7) | B1432:56 |
| Cross-lane C1-C4 contradict the PROPERTY | FINDING (1d) | B1432:121-128 |
| Steps 0 Briefs path | FINDING (as B1430) | B1432:35 |
| Ports 9920-9929 | PASS | B1432:133 |
| Facts re-read | PASS: `static/settings.html` and `tests/e2e/shell-layout.spec.js` in the tree; `static/js/first-run-setup.js:383` is the `.replace(/\/$/, '/')` line (RD-808); `deploy-demo.yml:29-32` paths-ignore as stated; queue 78 of 78 To Do, first RD-962 To Do | B1432:42, :44, :54, :139 |

## B1433 - SEAT-N117 lane B (backend periphery)

| Check | Result | Where |
|---|---|---|
| Jira helper import | FINDING (blocker) | B1433:82 |
| Model Opus where row C2 / lanes.md:73 say Sonnet C2 (G1 is a gate tier, not the builder) | FINDING: `BRIEF_SEAT_LEVEL=sonnet`, `claude-sonnet-5-5` | B1433:4, :105 |
| Line 40 sends the seat to "the open CodeQL alerts outside server.js ... (intentRouter, queryPreprocessor, ticketStore, marketplaceStore, validators, incidents, costCentreMap), each by its ticket" | FINDING: those alerts' tickets RD-765, 766, 767 and 769 are homed in S (B1430:117-121; B1433:24, "not yours"). `backend/incidents.js` (2 open alerts) is named by NO ticket in the sweep. lanes.md:74 says the opposite: the B half goes in B and merges first. One rule must win; delete or rewrite line 40 | B1433:40 |
| One-sided sequencing on `emailService.js` (RD-805 here vs S's RD-768/RD-806) and `azureLogAnalytics.js` (RD-804/RD-305 here vs S's RD-925/RD-792) | FINDING (1d): add a check of `b1430/*` branches on B-owned files before B starts a branch | B1433:44-45, :50 |
| Steps 0 Briefs path | FINDING (as B1430) | B1433:36 |
| Ports 9930-9939 | PASS | B1433:72 |
| Facts re-read | PASS: alerts 152/153 `js/log-injection` at `backend/learningManager.js:125` and `:153`; RD-805 names `entraGroupGate.js` (`tickets_paths.json`); 16 of 16 To Do, first RD-798 To Do; open backend alerts outside server.js and jsonStorage.js: 29 over 15 files | B1433:40, :43 |

## B1434 - SEAT-R196 records

| Check | Result | Where |
|---|---|---|
| Seat id R196 | FINDING: `2026-11-09_B1386_SEAT-R196_hpsmpoc-phase2-catalogue-tickets.md` already uses it. Rename to **R202** in the file name and at lines 3, 5, 6 and 39 (`Datasec/NexusAI-R196`) | B1434:3, :5, :6, :39 |
| `pwd -P` is not `P` | FINDING: an undefined template token. Write `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI` | B1434:39 |
| Jira helper import (this is the seat that WRITES Jira) | FINDING (blocker) | B1434:26 |
| Name-scan library not underscore-aware | FINDING (7): require `(?<![A-Za-z])<name>(?![a-z])` and a planted `_by_<name>_` control, per DRAFTER_RULES:40-43 | B1434:20 |
| `text ~ "late INSERT"` = RD-973 and RD-975 (also lanes.md:55) | FINDING (false today): it reads **RD-219** only (Release Ready, unrelated); control `text ~ "ROLLBACK"` = 61 holds; `text ~ "setQuickQuestions"` = RD-973 only. The conclusion (no cover, so create) is unchanged | B1434:17 |
| "builders touch no `1_Project_Definition/**`" | FINDING (minor): the builders write their STATUS (and should write their kit copies) into `1_Project_Definition/Briefs/`. The files are distinct, so there is no collision, but the sentence is false | B1434:9 |
| HISTORY entries for #180-#184 vs the B1375 stamp ("Answers ...: no HISTORY.md entry", `2026-11-09_B1375_slots.json`) | Q for Tuesday: this kit reverses yesterday's answer for #182 (lanes.md:52 calls it owed). Confirm at the stamp | B1434:10 |
| Records seat does not land its branch vs DRAFTER_RULES:59 ("Records seats land their own records branch") | Note: it is consistent with C-190 (a PR is needed, and the seat is `gh -X GET` only). DRAFTER_RULES:59 predates C-190 and should be reconciled | B1434:10 |
| Model Sonnet, G3 | PASS: `models_latest.json:23`, `model-routing.md:110` | B1434:4 |
| Facts re-read | PASS: HISTORY.md at main, head line 3 "Newest entries at the bottom"; last heading `:9916` B1363 (2026-11-07); `9926903f`/`763f0006`/`3929b794` 0 hits each, `33db7181` 2 hits (`:9990` says #180 "is not recor[ded]", so it is owed); RD-980 0 (control RD-970 3, G357 3). CLARIFICATIONS tail: section `## 82.` (`:2607`), C-246 (`:2609`). `B1377_STATUS.md:279-286` = B1377-1..-8 (the kit's "-2 to -8" is right; lanes.md:54 "-2 to -6" is wrong); `B1379_STATUS.md:158-166` = B1379-1..-9, -6 at `:163`. Alerts: 164-171 and 208-219 fixed, 152/153 open. RD-799/800/959/960/961/973/936/928 all To Do; RD-936 comments 0; label `b1434-2026-11-10` 0 (control label `b1363-2026-11-07` = 8) | B1434:10, :12-17 |

## Seat ids and ports (proposed)

| Kit | Seat now | Proposed | Port block | Status |
|---|---|---|---|---|
| B1430 | N114 | N114 (keep) | 9900-9909 | free |
| B1431 | N115 | N115 (keep) | 9910-9919 | free |
| B1432 | N116 | N116 (keep) | 9920-9929 | free |
| B1433 | N117 | N117 (keep) | 9930-9939 | free |
| B1434 | R196 | **R202** | none (no listener) | R196 is taken by B1386 |

How the seat ids were checked (`seats.py`), across every brief file name:
- N114-N117 occur once each.
- Whole-token, underscore-aware content hits: N115-N117 0; N114 only inside B1379's own zero-count scan line.
- The highest R used is 201 (B1444). R199 and R200 are unused gaps. R202 is above the maximum, so a counter-based assigner will not hand it out again. R197 is also already duplicated (B1397 and B1410; that is outside this review).

How the ports were checked:
- The blocks match the taken list. Every port and range in the non-`.pre-` SEAT kits of 9 and 10 Nov:
  - HPSM: 9630-9679, 9700-9739, 9940-9989
  - MPS: 9740-9849
  - Composer: 9850-9899
  - G375-G378: 9520-9529, 9570-9579, 9590-9699
  - None claims 9900-9939. "9939" appears only as a control string in B1440-B1442.
- `lsof -nP -iTCP:9900-9939 -sTCP:LISTEN` printed nothing (rc 1). Control: `lsof -nP -iTCP -sTCP:LISTEN | wc -l` = 11, and 9500-9999 has no listener.
- Live pane names: only `Datasec/HPSM-POC-R197` matches a NexusAI, R19x or N11x pattern.

## Stamp values each kit needs (Tuesday fills; reviewer's suggestions, not reads Tuesday has done)

**Common to all five, at stamp time:**
- **MAIN:** re-read `branches/main`. The reviewer read `3929b7946e2de85ce2ea312ac70bb64134a767e6` at 06:02:26 AEDT. If it has moved, line 1 of every kit is stale: replace it with `@MAIN@` or a MAIN slot.
- **STAMP:** `STAMPED @NOW@ AEDT 2026-11-10 by Tuesday`, plus what Tuesday read:
  - main sha
  - open PRs 0
  - `b143*` refs 0
  - Deploy demo on main skipped
  - the Jira-helper fix applied
  - the answers to the Qs above
- **LAUNCH WINDOW:**
  - load1 under 7, read inside `launch_when_cool.sh` (the reviewer's `uptime` read 1.32 during this review; no clock was printed with it)
  - one waiter, with GAP_MIN 120 s between launches
  - live seats beside: the other NexusAI lanes named
- **READ-WHOLE:** `DONE @NOW@`, written only after Tuesday reads the kit whole.

**Hard stops** (the reviewer's suggestions, as absolute AEDT clocks at launch):
- Builder lanes: launch + 4 h. Each kit already bans a new branch from 60 minutes before it.
- Records seat: launch + 2 h. Its kit already bans Jira writes from 20 minutes before it.

**Per kit, after the shared blocker is fixed:**
- **B1430:** Briefs path; YOUR FILES plus existing tests; the cross-lane carve-out in THE PROPERTY; the absolute itemised path.
- **B1431:** level sonnet; the deploy-demo and deploy-script fence; name rephrase; test-file exclusions.
- **B1432:** level sonnet; existing tests in YOUR FILES; a ruling on the index.js reservation (now vs L3 start); name rephrase.
- **B1433:** level sonnet; rewrite line 40; check S's open branches on B files.
- **B1434:** seat R202 (rename file, pane and launch line); `pwd -P` path; underscore-aware scan; the late-INSERT fact; the HISTORY #182 confirmation.

## UNMEASURED / disclosure

- Remote branches other than open PRs and the four newest builder branches were not compared for ahead-of-main work.
- No test, build or server was run.
- Hosted CodeQL on any PR head was not read, by design.
- Jira was read only through an in-memory re-point of b774lib, with its write verbs disarmed, using search, issue-in-search and comments GETs.
- No file was written except this REVIEW.md; scratch programs live in the reviewer's session scratchpad.
