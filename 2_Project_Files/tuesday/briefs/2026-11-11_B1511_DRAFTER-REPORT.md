STARTABLE: YES (after Tuesday fills the 11 Stamp slots; two things to read first: Q-L4-1 and Q-L4-6 below)

# B1511 drafter report: SEAT-M118, MPS lane L4 "engine and docs"

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1511_SEAT-M118_mps-lane-l4-engine-docs.md` (84 lines, ASCII, 11 unfilled `____` lines, matching the kit's own "reads 11 such lines"). Modelled on B1494 (L2) and B1502 (L1): every standing line, refuse, fence, identity, heavy-lock, PRIOR-WORK, context-band and stamp-slot convention kept. Drafted 17:54 to 18:10 AEDT 2026-11-11.

## BLUF
Of the five L4 tickets, four are buildable now and one is held. None is met at main.
- MPSCALC-196: only clause (d) is open: the register row X-33 was never written into `docs/ENGINE.md`. Doc row, text already exists in the build records. BUILD.
- MPSCALC-147: only clause 2b is open: no Customisation row in `docs/ENGINE.md`. Doc row, text proposed in the records. BUILD.
- MPSCALC-160: clause 6 (server half of the 7% rebate default for callers without per-quote pricing rights) is the one real code change, in `PricingPolicy.cs`. BUILD, with a hazard written into the kit as a STOP (see D3).
- MPSCALC-158: no code to write; clause 5 is "no gate re-ran the two follow-up tests". The seat runs them under the gate's two mutants and records it; commits only if a mutant survives. Clause 4 (browser never computes it) cannot be built: no target-click screen exists at main and a screen needs product words.
- MPSCALC-200: HELD. Clauses 2 and 3 need counts from the real price-book store, which every MPS kit forbids; the other way out is a coordinator ruling that the "Read" definition suffices. Neither exists.
Seat model: Opus (model-routing row C3, line 93), because 160 changes pricing policy on an authorization surface. Gate after: tier G1.

## Facts re-measured (instrument; control)
1. Main `54ed76273cf5e7eb804315635c413034f28b3372` at 17:55:23 and 18:04:48 (`gh api -X GET .../git/ref/heads/main`). Open PRs: #176 (`b1494/mps-api-stores`, ahead 5, 15 files, all Feedback/Sources/their tests) and #177 (`b1508/mps-pkcs-pin`, one csproj). Neither touches an L4 path (`compare main...<branch> --jq .files[].filename`; control: the listing names 15 / 1 files). `matching-refs/heads/b1511` 0 rows, control `heads/b1405` 1.
2. Tickets: Jira GET 17:55:16, `project = MPSCALC AND ( key in (...) )`, all five Backlog, comment counts 147:4, 158:5, 160:3, 196:2, 200:1, newest comment 200's 2026-11-10 15:48:53; control 361 reads Done. Reader written into my scratch folder, reads the project `.env` in-process, nothing printed.
3. Register: `/usr/bin/grep -c -E "MPSCALC-<k>\b"` over the decision register: 0 for 147, 196, 160, 158, 200; control MPSCALC-77 = 1. Same count over `CLARIFICATIONS.md` from line 2653 (C-102) to the end (2912, C-130 last): 0 for all five; control 77 = 2. So none of the 29 accepted recommendations answers these tickets. **C-109 (`CLARIFICATIONS.md:2716`) does govern the doc rows**: developer-only docs are left out of the product owner's word review, so `docs/ENGINE.md` rows need no word card.
4. `docs/ENGINE.md` at main: `| X-33 |` 0 hits (control `| X-34 |` 1), `customis` 0 hits; X-32 at :159, X-34 at :160, X-30 at :157, X-23 at :149. Code cites X-33 at `PurchaseCalculator.cs:52,55,58,209,510`. Row texts exist in the project's own records (`B518_STATUS.md:36`, `B104_STATUS.md:231-232`), local files; the kit tells the seat to prove every clause against code before writing and to strip names, seat ids and card candidates from the text.
5. 160 at main: the 7% default is web-only (`bomModel.ts:45,53`); `PricingPolicy.cs:48` refuses a non-rights caller any rebate; `:176` keeps stored hidden values by section id; `Apply` is called at `QuoteEndpoints.cs:78` (create), `:162` (update), `:538` (duplicate). `docs/ENGINE.md:159` (X-32) states the server applies no default today.
6. 158 at main: both follow-up tests exist (`SuppliesIssueTextApiTests.cs:140` B163_1..., `DealUsageAuditApiTests.cs:112` B163_2...), X-30 is in the register (:157), mutant site `Mapping.cs:213` still matches the gate's pointer; the gate's `PriceAudit.cs:75` pointer is stale (comparison now at :35, field row at :89, `SameAmount` :236). No target screen: grep for `target|marginNeeded` over `DealUsage.tsx` and `DealUsageResultView.tsx` printed only two DOM-event hits (weak control: the files hit their own two lines).
7. PRs naming the keys (177 PRs, paginated, regex covers short `-<n>` inside lists; control: #102 hits both 196 and 217): 147 -> #69, 196 -> #102, 160 -> #97, 158 -> #73 and #77, 200 -> none. Branches: 198 compared (all but main); 9 branches touch L4-ish paths with no PR at all, last commits 2026-10-11 to 2026-10-16, all superseded stacks; no branch is newer than that on these paths.
8. CI readers: of 12 python test files, 0 mention `ENGINE.md|IMPORTER.md|docs/` in 11 and 1 in `test_demo_doc.py` (control, reads DEMO.md); of 14 files returned by a GitHub code search for ENGINE.md, none opens the real file (`OutputGuardTests.cs` writes a synthetic IMPORTER.md). The search is approximate (UNMEASURED as a census), so the kit makes the seat re-run it.
9. Ports 9610-9619: `lsof` 0 listeners (control: the 9600-9699 listing printed 7, the unfiltered one 17); `/usr/bin/grep -c -w -E '961[0-9]'` over 79 non-`.pre-` SEAT kits of 10-11 Nov: 0 hits (control: `969[0-9]` hit 3 kits). Live panes 18:00: tuesday, Security-Composer-R215, HPSM-POC-H156, NexusAI-N122, MPS-M114, fleet-monitor, ten unnamed. Load 18:00 14.89, 18:03 41.33 (not a refuse). Disk 1304 GiB free. No heavy-lock dirs.
10. Toolchain: project `.tools/dotnet/dotnet --version` 10.0.401; `global.json` 10.0.100 rollForward latestFeature; the two NuGet packages are in the machine cache. Hosted-only red RELAYED from the M116 kit: two `PublishOutputTests` fail on every PR at this main until #177 lands; the kit names it so the seat does not mistake it for its own.
Model line numbers: `model-routing.md:93` (C3), `:108` (G1), `models_latest.json:17` (claude-opus-5-5), `brief_seat.sh:24` (default opus).

## D-decisions (mine)
- D1 One Opus seat, ordered 196, 147, 160, 158 (both doc rows first because 160 edits the same `ENGINE.md`; one commit per ticket). 200 held.
- D2 158 is a measurement, not a build, mirroring how the L2 kit treated the overlay-mutant ticket. A commit happens only if a mutant survives, in a new `LaneL4*.cs` file.
- D3 160 stamps only NEW sections (create: all; update: ids not in stored) and never duplicates, stored sections, reads or rights-holders. **The hazard I found and wrote in as a STOP:** `QuoteEndpoints.cs:183-186` answers 400 `PRICE_REASON_REQUIRED` whenever `PriceAudit.Diff(stored, next)` is non-empty. A stamped rebate on a non-rights caller's new section may make that diff non-empty, so a save that works today would start to be refused for a reason the caller cannot know (or add an audit entry for a value they never sent). I did not run it (read-only), so it is DERIVED. If it bites, the seat STOPs with both readings; the fix is a design choice (hide from the diff, require a reason, or another layer), not the seat's. I judge this likely enough that Tuesday may prefer to hold 160 until it has chosen; see Q-L4-1.
- D4 Paths: `docs/ENGINE.md`, `PricingPolicy.cs`, new `LaneL4*.cs`, and listed existing rows that pin the reversed behaviour (expected value changed, name unchanged, each listed). I excluded `QuoteEndpoints.cs` and `PurchaseValidation.cs` from the seat even though they sit in the sweep's `Quotes/*`: L3's 333/325/338/339 rows pin their order and walks. `PriceAudit.cs` is excluded (170's contract question was dropped from L1 for you to decide); the seat only plants a mutant there in `main-tree`. `docs/IMPORTER.md` excluded because 200 is held.
- D5 READY target 22:00, HARD STOP 22:30 as given; the kit leaves the latest Step 0 to S9. With about 3 hours of work (baseline dotnet build/test, three doc/code parts, ten mutant runs) I would stamp a latest start of 19:00.
- D6 The kit says `docs/ENGINE.md` is not read by any CI test (Fact 8), so rule 8 (a gate runs the jobs whose tests read the changed files) is satisfied by the census plus the full dotnet job and `package` once at head.
- D7 Name hygiene: the proposed doc rows name the reviewer, build seats and card candidates (K-06, K-13, B104, B518); the kit has the seat strip them and runs the underscore-aware name scan with a planted control.

## Q-questions for Tuesday (each with a default)
- Q-L4-1 Build 160 clause 6 now, with the audit/reason hazard as a STOP? Default: yes (the ruling exists in the ticket and X-32; the seat proves or stops). Alternative: drop part 3 and let the seat do the other three; the kit's parts are independent, so deleting part 3 is a clean edit.
- Q-L4-2 200: stay held? Default: yes. To release it Tuesday needs either authority for counts-only reads of the local store (every MPS kit forbids `.local/` and `Source_Documents/`, so this is an access grant, approval-class) or a coordinator ruling that `docs/IMPORTER.md:115-116` already explains the gaps.
- Q-L4-3 158: accept measurement-only, clause 4 open (screen unbuilt, needs words)? Default: yes.
- Q-L4-4 Doc rows from the records' proposed rows, no word review (C-109)? Default: yes.
- Q-L4-5 One Opus seat for all parts (C3), G1 gate after? Default: yes.
- Q-L4-6 Landing order: the hosted `dotnet` job reds on the two `PublishOutputTests` until #177 lands. Default: land #177 first, then open the L4 PR; S8 carries that sentence.
- Q-L4-7 Latest Step 0 for S9? Default 19:00 AEDT.

## UNMEASURED
- Whether stamping changes `PriceAudit.Diff` for a non-rights update (D3): derived from reading `:183-186`, not run.
- Whether any existing test pins "a non-rights new section has no rebate" (I did not search the test files for `rebatePercent`; the kit makes the seat do it and list them).
- The sweep's claim that the local store holds both books (200).
- Duration of the full dotnet suite at the present load; the Pkcs reds' local reproduction.
- That every clause of the two proposed ENGINE.md rows still matches the code (the kit makes the seat prove each; I checked the constant names, line numbers, class names and the Option-in-hardware group only).
- Code-search census of readers of ENGINE.md (search is approximate).
- Whether 9 stale no-PR branches carry anything unmerged that matters; only their paths, dates and absence of a PR were read.

## Outside-the-fences disclosure
- Read only: the rules file, SWEEP-1326, the B1502/B1494/B1505/B1508 kits and B1502 report, the decision register (the file the task named), `model-routing.md`, `models_latest.json`, `brief_seat.sh` line 24. I never ran `decision_queue.sh`, never read `briefs_staged`, `scoreboard.md`, either ledger, or any non-Datasec tree.
- Project-local files read (not git, not an `az`/host call): `CLAUDE.md`, `CLARIFICATIONS.md` (lines 2216, 2653-2912 and greps), and the build-seat records `B104_STATUS.md`, `B518_STATUS.md`, `B163_STATUS.md`. Not read: `.local/`, `Source_Documents/`, any price store. No `.tools/b15xx` of another seat opened (I listed `.tools` names only).
- Jira: one reader script `jget1511.py` in my scratch folder, GET only, project `.env` read in-process; 1 query of 6 keys.
- GitHub: `gh api -X GET` only, under the project `GH_CONFIG_DIR`, including `pulls`, `branches`, 198 `compare` calls, `contents` raw reads, `git/trees`, and 2 `search/code` queries (GitHub API, not a hosted site). No clone, fetch, worktree or git write.
- Executed tools: `.tools/dotnet/dotnet --version` (as the L2 drafter did), `lsof`, `tmux list-panes`, `uptime`, `df`, `sysctl` not run (relayed). One background shell for the branch scan; it finished.
- Scratch: all intermediates in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s268/draft1511/` (`tickets.txt`, `raw/`, `raw2/`, `prs.jsonl`, `branch-scan.txt`, `tree.txt`, `jget1511.py`). No port used. The only other writes are the kit and this report.
- One hook refusal (an unquoted `=====` in a command) and one zsh glob error on an unquoted `?` URL, both harmless and retried. The rules file names `/Volumes/Laptop-DEV`; this drive is `/Volumes/Datasec_DEV` as the task said, so paths were taken from the task.
