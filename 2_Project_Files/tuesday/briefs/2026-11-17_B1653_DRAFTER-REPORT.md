STARTABLE: YES (after the stamp; 5 questions below, each with a default the kit already assumes; no MPS pane is live, no MPS branch `b1653*` exists)

# B1653 drafter report: MPS Commercial Calculator, lane M-D2 (seat M154)

Drafted 2026-11-17 from 05:55 to about 06:10 AEDT (`date` printed 05:55:30, 05:56:14, 06:00:52, 06:01:06, 06:01:37, 06:03:15, 06:03:54, 06:08:02, 06:08:30). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-17_B1653_SEAT-M154_mps-lane-md2-docs-and-comment.md` (81 lines, 8 stamp slots left as four underscores: S0 to S6 and the last line) with sidecar `.measured` (stamp_check rc 0: 99 claims, 99 measured; plus 53 extra `srcNN` lines that print the source line behind each frozen sentence). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s285/b1653/` (Jira dumps, tarball of main, `measure.sh`, `facts.txt`, build and test logs).

## BLUF
- **The lane builds ONE comment line and nothing else.** MPSCALC-390 item 3: `tests/MpsCalc.Engine.Tests/PurchasePageEstimate.cs:10` still reads "X-33 (docs/ENGINE.md row text in the seat's STATUS)". The register row now exists (`docs/ENGINE.md:160`), so the kit replaces that one phrase with "X-33 (the row of that id in docs/ENGINE.md):". No identifier, no code, no test row changes; the file's other 13 neighbours that mention a STATUS record are reported, not edited.
- **MPSCALC-195 is NOT closable by this lane and builds nothing.** Re-read at main `c74e2ecf`: clauses 1, 2, 4, 5, 6, 7 read MET (lines in the kit's FACT 7 and the sidecar). Clause 3 (the rate-limit parenthesis, `docs/API.md:768`) and the accepted engine-target sentence are NOT BUILDABLE: no words are given, and the sentence's text is in none of the ticket's six comments (comment 41070 says only "the drafted engine-target sentence is accepted") nor in the two records kits that name it. So Part B is a seat-written clause table, no commit; ticket stays open for the product owner's words. The commission's "records-only close" does not apply (two clauses open).
- Model row C2 (`model-routing.md:92`), `claude-sonnet-5-5` (`models_latest.json:23`), gate G2 (`:109`) per the sweep; pane `Datasec/MPS-M154`; branch `b1653/mps-lane-md2-test-comment`. READY at Step 0 + 60 minutes. No port, no listener (block 9970-9979 had 0 listeners).
- Measured by running it (in a tarball of main in my scratch, never in the project): `dotnet build MpsCalc.slnx -c Release` rc 0, `0 Warning(s)`; `dotnet test tests/MpsCalc.Engine.Tests` 743 passed; the frozen edit planted: build 0 warnings, 743 passed again. Each job took seconds. Hosted CI runs the whole `MpsCalc.slnx` test (`ci.yml:43`); no test reads this file (the name occurs in 1 file in the repository).

## Facts re-measured (instrument; control)
| Fact | Reading | Instrument / control |
|---|---|---|
| MPS main | `c74e2ecf24898220d9d2ab3c1262fcc63ecfcd55`, 0 open PRs, 0 `b1653` refs | `gh api -X GET` 06:03; control `heads/b1622` 1 row |
| Between #202 (`efe6cdd5`) and main | 11 files, 0 under `docs/`, 0 the test file | `compare` files; control 5 under `web/` |
| Jira 390 | Backlog, updated 11-16 21:30, 1 comment (41301) | own GET reader; control MPSCALC-361 Done |
| Jira 195 | Backlog, updated 11-16 21:31, 6 comments (newest 41304) | same |
| Test file line 10 | the stale phrase, once; 129 chars | `awk NR==10`, `grep -c -F` |
| `ENGINE.md:160` | the only `| X-33 |` line, 5 cells, holds the margin-order sentence | `awk -F'|'`, `grep -c -F` |
| 195 clause lines | API.md `:86-89`, `:91`, `:768`, `:262-266`, `:587`, `:590`; ENGINE.md `:157`, `:179`; SOURCE.txt blob = `openapi.json` blob `e03ee073` | `awk NR==`, `git hash-object` |
| Generated header commit `fd56438e` | exists, `diverged` from main (a PR head), same contract blob | `gh api commits/`, `compare` |
| CI predicate | `ci.yml:42` build, `:43` test; `Directory.Build.props:6` warnings are errors; `global.json` 10.0.404 `rollForward` disable | `awk NR==` |
| Toolchain | `<project>/.tools/dotnet-10.0.404/dotnet --version` 10.0.404 | run |
| Panes, locks, ports | 0 `Datasec/MPS-` panes, 0 lock dirs under `.tools`, 0 listeners on 9970-9979 | tmux, `ls`, `lsof`; controls fire |

## Chain inputs (rule 4)
Step 0 (copy of kit) -> Setup (clone, base, identity) -> Predictions (needs the clone) -> Step 3 base measures (needs clone and toolchain, makes BASE COUNT) -> Part A edit (needs the clone) -> rebuild (HEAD COUNT, compared with BASE COUNT) -> checks -> commit -> push -> Part B table (reads `git show <base>:<path>`; needs only the clone). Every input is produced by an earlier step or exists at base.

## D-decisions (the drafter's, so Tuesday can overrule)
- D1: new pointer phrase "the row of that id in docs/ENGINE.md" (ASCII, no `<`, `>`, `&`, no B-number); only the phrase changes, the description sentence after the colon is not reworded (the ticket asks for the pointer only).
- D2: no docs edit at all, although `docs/API.md` and `docs/ENGINE.md` are in the sweep's owned-path table: nothing in 195 is buildable without the product owner's words, and the 707 clause is out of the commission.
- D3: clause 6 judged by blob equality and a `commits/<sha>` GET; the generator `sync-contract.mjs` is not run (needs node; not needed: blobs equal).
- D4: the kit keeps the project's heavy-lock convention for the dotnet jobs although they take seconds (the project rule says any dotnet build or test is heavy); Tuesday may waive.
- D5: a comment on 195 newer than 41304 that carries the exact sentence is a STOP with the quote, not a build (placing words is a separate, reviewed kit).

## Questions for Tuesday (each with the default the kit assumes)
- **Q1** (S4): the frozen new phrase "the row of that id in docs/ENGINE.md". Default: as frozen.
- **Q2**: fix the false clause at `docs/API.md:707` ("across every governed version that did not fail"; code `SourceDocumentChecks.cs:406` counts only Validating, Active, Superseded) in this lane? It is a Minor BACKLOG row with no ticket, outside the commission. Default: NO, reported in FOR TUESDAY; a later docs lane or records pass owns it.
- **Q3**: gate tier. The sweep says G2 (a non-doc file). Row G3 (`model-routing.md:110`) lists "comment corrections" and has no gate (the completion check only). Default: G2, as the sweep.
- **Q4**: 195 stays open and builds nothing. Do you hold the accepted engine-target sentence's text (or the rate-limit words)? If yes, a separate small docs kit places them; default: no text, no kit.
- **Q5**: the full-solution test (`dotnet test MpsCalc.slnx`, the Api tests) is left to hosted CI; the seat runs the solution build and the Engine tests only. Default: as stated.

Before stamping, Tuesday decides nothing else; the stamp slots S0 to S6 are Tuesday's (commission, base re-read, state at stamp, answers, window, hard stop).

## UNMEASURED
- The text of the accepted engine-target sentence (not found anywhere readable).
- Whether any other field reaches the engine negative (195 clause 1's tail; RELAYED from #202's builder).
- The Api test suite against the edit (the hosted job does it; no test reads the file).
- Hosted state of the MPS site (nothing here touches it).

## Outside-the-fences disclosure
- I ran `dotnet build` and `dotnet test` (project toolchain by path, `DOTNET_CLI_HOME` in my scratch) on a tarball of main extracted into my scratch folder, and planted then restored the frozen edit there. The restore read the existing NuGet cache (no download in the logs: 0 http lines; 0 new package directories). Nothing in `!CODING` was written; no heavy lock taken (a lock is a write there); the machine load stayed 6 to 9. I also read project files outside the code repo (`BACKLOG.md`, `CLARIFICATIONS.md`, records and STATUS briefs under the project's `1_Project_Definition/`), read-only, and printed one long grep hit (a CLARIFICATIONS entry) by accident while searching for the sentence's text. No `.local`, no price book, no ledger, no `decision_queue.sh`, no Artifact, Docs, mail or board.
- My shell hit a hook refusal once (an unquoted `======` word) and one `grep -rl` over the Tuesday brain timed out at 120 s and was stopped (`TaskStop`); nothing was written by either.

DRAFTED B1653: kit 81 lines, sidecar rc 0, questions 5
