STARTABLE: YES

# B665 drafter report - SEAT-M22, lane M-STORE332 (MPSCALC-332), Datasec / MPS Commercial Calculator
Drafted 2026-10-25 12:40-13:05 AEDT. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B665_SEAT-M22_mps-332-store-first-use-absent.md` (137 lines, ASCII, 8 four-underscore lines: 7 slots plus the last line; `grep -c` printed 8).

## BLUF
1. One new test file, `tests/MpsCalc.Api.Tests/StoreFirstUseAbsent.cs`, 5 cases (F1 absent-at-first-use x2 hosts, F2 vanished-file pin x2 hosts, F3 unit-level exact line x1). No source byte changes (the product owner's ruling is "accept as written").
2. Base main `dd0ce36dc1083266bf89c55d9ddab4aa9efb4c85`; open PRs are #112 (B654, now open, under gate B663) and #110; the one path is in neither list, nor are the helpers it calls.
3. CI judges the Api tests with `dotnet build MpsCalc.slnx -c Release` then `dotnet test MpsCalc.slnx -c Release --no-build` (ci.yml lines 42-43; exit 0 of both; TreatWarningsAsErrors). No SQL Server shard in the MPS workflow.
4. Model: Sonnet C2 (routing line 92), `BRIEF_SEAT_LEVEL=sonnet` inside the quotes. Recommend gate tier 2 (Q-1).
5. Ports 9610-9619 free; one old finished kit (B609, other repository) names the block.

## Facts re-measured at source (instrument, control)
- Main: `git --no-optional-locks ls-remote origin refs/heads/main` at 12:45:02 = `dd0ce36d...`; no `refs/heads/b665*` (control: `matching-refs/heads/b6` lists seven refs including b654).
- Open PRs (`gh -X GET api 'pulls?state=open'`, project GH_CONFIG_DIR): #112 head `6618f119c807a68cbf06c6ba8306c21420247247` (4 files: docs/API.md, PurchaseValidation.cs, QuoteEndpoints.cs, QuoteWalkCaps.cs); #110 head `650ddfb7...` (5 files). `StoreFirstUseAbsent.cs` shared with neither (control: files of both lists printed). Note the B654 seat has already pushed and #112 is open, so the kit names it as the live neighbour, gate seat `Datasec/MPS-G114`, B663.
- Ticket: Jira GET, `project = MPSCALC AND ( key = MPSCALC-332 )`: Backlog, labels mpscalc-b610, plan-b610-b594-1-2, tier-1; one comment (the ruling relay). Acceptance quoted in the kit.
- Ruling record: C-66 at `1_Project_Definition/CLARIFICATIONS.md:1327` in the project root (root HEAD 87e4cf1, read with sed). Cited in the kit; the card id is not.
- Source at main (raw `contents?ref`): `ActiveSources.cs` 249 lines, blob `8942fe8a...`; `if (!File.Exists(full))` line 172 (count 1), no-store sentence line 238 (1), cannot-open sentence line 244 (1), `reportCannotOpen: false` line 233 (1); control string `zzz-no-such-string-7f3a` = 0. Existing rows: `StoreReopen*.cs` hold zero matches for "No reference store at" (case-insensitive; control: `StoreLoadFaultMapping.cs` has "cannot be opened" 1). This is the ticket's survivor.
- Helpers (`StoreProbe`, `TempWorkTree`, `ListLoggerProvider`, `ApiHost`, `EntraApiHost`) are `internal` in the same assembly and in no open PR's file list. `Hold` in `StoreReopen.cs` is `private static` to its class: the kit tells the seat to write its own helper (a trap I would otherwise have left).
- CI: `.github/workflows/ci.yml` at main is 123 lines; `dotnet` job lines 30-43; `grep -c -i sql` = 0 (control: `dotnet` count 22 in the earlier contaminated copy is not used; on the clean 123-line copy `-i -E 'sql|hpsm'` printed 2, both comment lines naming HPSM). `Directory.Build.props` TreatWarningsAsErrors true (count 1).
- Landing rule: `CLARIFICATIONS.md:809` ("squash with the head pinned (--match-head-commit, the MPS convention...)"), project `CLAUDE.md:50-52` CodeQL rule; both quoted in the kit.
- Model: routing rows C2 line 92, G1 line 108, G2 line 109, G-cap line 111 (grep -n); model id `claude-sonnet-5-5` at `models_latest.json` line 23, checked 12:39:27.
- Ports: `lsof -nP -iTCP:9610-9619 -sTCP:LISTEN` empty, rc 1 (no positive control by me). Word-boundary scan of non-`.pre-` SEAT kits of 10-24 and 10-25 for `961[0-9]`: one hit, B609 (HPSM-POC gate, finished, own old block; the scan fires on it so it works). Kits B650 9200-9209, B659 9950-9959, B660 9570-9579, B661 9570-9579/9580-9589, B662 9020-9029, B663 9060-9069: none overlaps. Panes: tuesday, MPS-G114, NexusAI-G113, HPSM-POC-G111, Security-Composer-G110, NexusAI-M9, fleet-monitor; no `MPS-M22`. `M22` appears in four Composer/NexusAI kits as a mutant id only.
- Load: `uptime` 4.13 then 4.12 (4 s apart); no `.tools/heavy-slot-*` directory and no `.tools/.git-lock` existed at 12:47.

## D-decisions (override at the stamp)
- D1 one file, class `StoreFirstUseAbsentTests`, shape of `StoreReopenTests`.
- D2 five cases: F1 (absent file at first use: 503 triple, the typed no-store sentence once, still refused after the file is written, no Loaded line), F2 (the vanished-file answer: held at first use, then moved away: still 503, still one warning, no no-store line, served when the file returns), F3 (unit-level exact line). Sketches are marked UNMEASURED; the seat measures and types.
- D3 names added exactly 5. D4 base main, not a PR branch. D5 branch `b665/mps-store-first-use-absent-row`. D6 no provider matrix, no SQL Server shard.
- Mutants S1-S6 (S1 is the ticket's acceptance mutant: first-use check disabled, predicted red F1 x2 and F3), plus controls c0/c1/c2 and cw-weak; non-warning forms of the mutants are required (TreatWarningsAsErrors).

## Questions for Tuesday
- Q-1 Gate tier. Ticket label says tier 1; sweep says G1; I recommend **tier 2 (Sonnet gate), routing row G2** because the diff is one new test file, no `src`, no answer or word changes, no deploy, no client tester, and the mechanism was measured by the gate that found it. Rows: line 108 `G1 | Tier 1: security surfaces, data destruction, anything deploying, anything handed to a client tester` (none applies); line 109 `G2 | Tier 2: tests-only, spec-only, docs, config/CI, tooling, and follow-ups whose mechanism a prior gate already measured`; line 92 `C2 | Multi-file build or feature that fails the local predicate, not decision-shaped, not auth-design and not a destroying path` (Sonnet first); line 111 G-cap two NO GO rounds. Default: tier 2. The kit says the gate tier is "Q-1, drafter recommends tier 2" and the READY marker takes the tier from the stamp.
- Q-2 Branch name `b665/mps-store-first-use-absent-row` follows the `bNNN/...` convention but carries a brief number (standing line 4 forbids it in code/commits only). Default: keep.
- Q-3 Launch order: M22 is independent of #112 and #110, so it can launch beside the B663 gate. Default: launch through the cool-load waiter after the queue ahead.

## UNMEASURED
No build, test or mutant was run; no C# compiled. Not measured: that F1-F3 are green at main; the exact `Warning:` line shape and when the `IActiveSources` singleton is resolved for an absent path; that a moved-away file raises the exception the cannot-open catch takes (the ruling calls this the card's reading, not a run); Linux CI behaviour of the file hold (existing rows rely on it); test-count baselines; CodeQL; the gauge.

## Outside-the-fences disclosure
- Wrote only the kit and this report under `2_Project_Files/tuesday/briefs/`. Read: DRAFTER_RULES.md, the template kit, the sweep file, the project root records (CLARIFICATIONS.md, CLAUDE.md), the routing file, models_latest.json, tuesday kits' port lines. No `decision_queue.sh`, no staged briefs, no scoreboard, no ledger, no WEDNESDAY/FRIDAY tree. Git in the project repo: `ls-remote` only. `gh` only `-X GET api` under the project's GH_CONFIG_DIR. Jira: one GET search with parentheses, through an in-process script reading the project `.env` (token never printed). No HTTP to any app host.
- **Shared-scratchpad hazard (needs your attention):** the session scratchpad is shared between concurrent drafters. I first wrote scratch files into its root (`jget.py`, `ActiveSources.cs`, `ci.yml`, `tree.txt`, directory `t/`). My first `ci.yml` read back as 679 lines of HPSM-POC content: another drafter had overwritten that name. I discarded it and re-fetched every fact I used into my own subdirectory `scratchpad/b665/` (ci.yml now 123 lines of MPS content). The same hazard may have bitten that other drafter's `ci.yml`/`tree.txt` reads if they used the same names after mine: if a sibling kit quotes CI or tree facts from this scratchpad root, re-check them. The kit's standing line 6 now tells the seat to keep scratch in a seat-named directory.
- Two files of mine remain in the scratchpad root (`jget.py`, `t/`) and four others; none is in the project.
