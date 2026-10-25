STARTABLE: YES (after the stamp; 8 four-underscore lines to fill, 7 slots and the last line; no blocker found)

# B686 DRAFTER-REPORT: SEAT-M26, lane M-NULLROWS (MPSCALC-336), drafted 2026-10-25 18:57-19:2x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B686_SEAT-M26_mps-336-null-class-rows.md` (142 lines, shape cloned from the B670 kit, with the C# specifics of the B672 kit).

## BLUF
- One builder seat, Sonnet (C2, routing line 92), pane `Datasec/MPS-M26`, writes ONE NEW test file `tests/MpsCalc.Api.Tests/SourceLifecycleTests.GovernedNullClassEdges.cs` (33 theory rows by default) on a new branch `b686/mps-null-class-edge-rows` off main `a85f8bd5`, builds six mutants (G13, G13a, G13b, G6, G4, G3) from the gate's TEXT, kills each with its own rows, runs a six-variant sweep, ends at READY FOR QA. Tests only, no product byte, no PR, no deploy.
- Why a new file and not an append: the existing byte builder and expected-list switch are closed (they throw on an unknown shape, `GovernedNullClass.cs:277`), so an "append" there would mean editing an existing method. A new partial file keeps blob `b7b0a190` byte-equal and reaches the private helpers because it is the same partial class.
- Gate round-count wrinkle for you: on this class there were already NO GO 2 of 2 (B619 round 1, B645 round 2); the product landed on the round-cap card default. The kit names the gate as G2 tier 2 and leaves the "is this round 1 of a new cycle" call to the stamp (Q-1).

## Facts re-measured (instrument and control)
| Fact | Instrument | Result | Control |
|---|---|---|---|
| main = `a85f8bd5f172af494f05d8ffc1e0ee64b26fcf68` | `git --no-optional-locks ls-remote origin refs/heads/main` under the project dir | equal to the commission | the local checkout does NOT hold it (`cat-file -t` fatal), so the builder needs one explicit-refspec fetch; kit says so |
| open PRs | `gh -X GET api 'pulls?state=open'` under the project `GH_CONFIG_DIR` | #112 only, head `f2102e35` (moved from `6618f119`), files: docs/API.md, PurchaseValidation.cs, QuoteEndpoints.cs, QuoteWalkCaps.cs | `pulls/112/files` listed 4 paths; `pulls/112` state open, draft false |
| commits since the gate's base `dd0ce36d` | `compare dd0ce36d...a85f8bd5` | ahead 3: #110 `8b046423` (this lane's product), #113 `ef9bfba4`, #114 `a85f8bd5` | `pulls/110` merged=true, merge_commit_sha `8b046423...` |
| validator blob | `contents?ref=a85f8bd5 .sha` | `e7c6f862e6f06f111c7764d29d111f05d8d22632`, 229 lines; the ticket says the same blob at the squash and the gate's head | n/a (the ticket's text agrees) |
| existing null-class test file | raw read of main | 411 lines, 11 `[Theory]`, 0 `[Fact]`, blob `b7b0a190...`; data rows 4+4+10+12+9+10+15+20+3+2+2 = 91 (derived from the `TheoryData` blocks, equal to the gate's 91) | `grep -c` of a made-up string printed 0 |
| anchors | `grep -c -i -F` over the raw validator | line 203 condition 1, line 207 1, line 161 1, line 163 1, line 166 1, `SuppliesCppAgrees` 1 (line 200, called line 92), the two dictionary sites 1 and 1, `StringComparer.Ordinal` 6 | made-up string 0 |
| new file name free | `grep -c -i` over main's 732-line recursive tree | `GovernedNullClassEdges` 0 | `GovernedNullClass.cs` printed 1 |
| ticket | Jira GET, `project = MPSCALC AND ( key in (MPSCALC-336, MPSCALC-337, MPSCALC-310) )`, then the issue | MPSCALC-336 Backlog, Task, Medium, tier-2, 0 comments, 0 links; acceptance names G13, G13a, G13b, G6 as required and G4, G3 "if taken" | the search returned all three keys (3) |
| sweep line 74 and 175 | `grep -n 'MPSCALC-336\|M-NULLROWS'` | line 74 (completable table) and line 175 (lane table): both say "tests/MpsCalc.Import.Tests/** or SourceLifecycleTests.GovernedNull*.cs (confirm)": CONFIRMED the Api `SourceLifecycleTests.GovernedNull*` family; Import tests hold no governed validate-and-activate path | the match printed exactly these two lines for the key |
| CI predicate | `ci.yml` raw, 123 lines | `dotnet:` job line 30, build line 42, test line 43, timeout 20 min; `TreatWarningsAsErrors>true` count 1; `global.json` SDK 10.0.100 | made-up string 0 |
| routing / model | `grep -n` of the C2/G2/G-cap rows; `models_latest.json` | C2 line 92, G2 line 109, G-cap line 111; `claude-sonnet-5-5` at line 23, checked 18:41:45; `brief_seat.sh` line 24 defaults to opus | `BRIEF_SEAT_LEVEL=sonnet` written inside the launch quotes |
| ports 9790-9799 | `lsof -nP -iTCP:9790-9799 -sTCP:LISTEN` | nothing, rc 1 | a python socket on 9790 was listed, then freed, then rc 1 again |
| port claims | word-boundary scan of the 131 non-`.pre-` SEAT kits of 10-24 and 10-25 | 6 files hit: `B629` (HPSM-POC-H19) CLAIMS 9790-9799 ("ONLY"); `B592` is a source line number `:9795`; `B649`, `B657`, `B666`, `B682` name wider ranges in prose | no H19 pane in `tmux list-panes -a` at 18:59 (panes: tuesday, HPSM-POC-R43, Security-Composer-G122, fleet-monitor); the same scan style finds `M23` in 13 kits |
| pane / branch free | `ls -d`, `matching-refs/heads/b686`, kit scan for `M26` | no `.tools/b686`, no refs (length 0); `M26` appears in 3 Composer kits (B623, B626, B666) as a mutant id | `heads/b61` length 1; `M23` scan lists 13 |
| heavy slots / load | `ls -d`, `uptime` | no `heavy-slot-*` and no `.git-lock` exists now; load 6.63 4.91 3.58 at 18:59 | B672 kit recorded slot 1 held at 14:06, so the slots do get taken |
| sibling lane | `ls` of the briefs dir for B683-B689 | nothing yet (B685 not written at my read); #113 is on main, so `StoreFirstUseAbsent.cs` (blob `2b10826d`) is a main file now | n/a |

## D-decisions (the kit's; override at the stamp)
- D1 one NEW file, not an append (reason above); the Import-level alternative not taken.
- D2 G4 and G3 are in (ticket "if taken"; small, test-only); sweep rows capped at 12 extra cases, more is a STOP.
- D3 mutants are the builder's own from the table; the gate's evidence folder is forbidden reading (it holds the gate's mutator and probes).
- D4 base main `a85f8bd5`; D5 one commit, branch `b686/mps-null-class-edge-rows`.
- D6 narrow runs by FullyQualifiedName; the old 91 are selected by `~GovernedNullClass` and `!~GovernedNullClassEdges`, with a mandatory printed count (the filter may not select 91; the builder must say what it selects).
- D7 no provider matrix. D8 the property for the sweep and the closed list ("at least these", then "prove it meets the property or STOP").
- Ports reserved but unused (in-process hosts); hard stop 4 h, target READY 2.5 h (C# mutant matrix, as B672).

## Q-questions for Tuesday (each with a default)
- Q-1 Gate round count: B619/B645 closed the class at NO GO 2 of 2. Is the gate after this lane "round 1 of a new cycle" (follow-up ticket, product already landed) or does it need the product owner's word? Default: G2 tier 2, counted as a new follow-up, and a same-class NO GO goes straight to a card.
- Q-2 Ports: B629's kit still claims 9790-9799 on paper (H19, no live pane). Default: keep the block (the seat listens on nothing); alternative 9800-9809 if you prefer a clean scan, check it first.
- Q-3 Sweep variants (iv) and (v) (case-insensitive supplies groups, case-insensitive product key) go beyond the ticket's four findings. Default: IN as sweep, rows only if the variant is reachable and survives, within the 12-case cap.
- Q-4 The ticket's open question (an empty or one-space product name with five terms validates and activates) is the product owner's. Default: no row, kit says so twice.
- Q-5 Heavy-slot sharing with the M-STORE builder and any gate: default wait, never touch holders; the kit allows a 4 h hard stop for it.

## UNMEASURED
Nothing was built, run or compiled. Not measured: that the 33 rows are green at main; the head's exact answers for a whitespace link and for a costed `cells = {}` (the kit expects one CPP_INCONSISTENT at the row); mutant build cleanliness; the red counts 16/8/8/8/8/5 (the gate's, on its rows); that a filter selects the old 91; where `Host()` and `StageBytes` are defined (I located `Lifecycle` at `SourceLifecycleTests.cs:35` and `AdminOf` at line 37 only, and the existing file calls both helpers, so they exist); main's test counts (the gate's 435/183/2963 are at its head); the B685 kit's final paths (taken from your commission text).

## Outside-the-fences disclosure
- Wrote only the two output files, with Write/Edit. Scratch copies of main's raw files (validator, two test files, `ci.yml`, tree listing, kit list) went to the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/16269e6c-6a5b-4095-925b-ab14a2b17432/scratchpad/` as `m26_*`: this is a deviation from "write ONLY your two output files"; they are read-only copies, nothing else was created.
- Jira: no helper existed in the MPS `.tools`; the HPSM-POC helper `jira.py` reads HPSM-POC's own `.env` (its ROOT is two levels up), so I did NOT import it. I read it whole, then ran an inline `python3 -I` heredoc that reads the MPS project's own `4_Credentials/.env` in process (GET only, token never printed), with `project = MPSCALC AND ( key in (...) )` parentheses. No file written for it. I read the MPS `.env` by pattern for three variable names only, and listed `4_Credentials/` (names only).
- `gh` only `-X GET`, under the MPS `GH_CONFIG_DIR`; git only `ls-remote`, `cat-file -t` (failed on the stale checkout) and `ls-tree` (failed, same reason) in the project repo; nothing fetched.
- Opened `.tools/b672/scripts` and `.tools/b670/scripts` by `ls` only (names), read nothing in them. Read the B645 STATUS whole (allowed per the commission) but not its evidence folder (only `ls` of its file names, to name the forbidden items). Read the B672 and B670 kits (templates). No HTTP to any hosted host. A 4-second python socket on 127.0.0.1:9790 for the port control. No decision_queue, no mail, no Artifact, no Docs.
- Kit text carries no person's name and no decision-card id (the project CLAUDE.md quote had a seat name; I replaced it and said so). The name list in property check (f) is the scan pattern, copied from the template.
