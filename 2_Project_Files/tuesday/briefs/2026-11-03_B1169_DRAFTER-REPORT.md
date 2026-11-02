STARTABLE: YES

# B1169 drafter report (Sonnet drafter) - kit `2026-11-03_B1169_SEAT-M83_mps-375-template-isolation-killing-rows.md`

## BLUF
MPSCALC-375 is a one-file, test-only lane: `tests/MpsCalc.Api.Tests/TemplateIsolationTests.cs` (blob `6f7788ec`, 297 lines, ASCII). New branch `b1169/mps-375-template-isolation-killing-rows` from main `62fd49c74d092784e232799fea7e080b16718817` (PR #149; one parent). The kit adds three shape guards (raw string, preprocessor line, format-spec hole) over the real Templates files plus a detector-control fact, four killing rows for the named branches (`:113` depth, `:162` verbatim, `:169` backslash, `:100` char literal) using the gate's measured cases, and rewrites the three inexact comments. The `}}` branch (`:177`) is equivalent to the fall-through: the kit has the seat run a plant, report it, and stop on that item (no row, no removal). Gate G2 (`model-routing.md:109`), round 1 of 2 on this class, NO GO 0 before. Builder C2 (`:92`), `claude-sonnet-5-5` (`models_latest.json:23`). Nothing was built or run; all red/green claims are hand derivations from the gate's tables.

## Facts re-measured (instrument; control)
- main = `62fd49c7` by `gh api -X GET git/ref/heads/main` and `git ls-remote` (03:01 and 03:05 AEDT); `compare b7eebb47...62fd49c7` = ahead 1, 2 files, both `web/src/screens/bom/*`. Test file blob equals `gh api` contents sha at both b7eebb47 and the pin (`6f7788ec...`).
- **The pin's object is not in the local checkout** (`git cat-file -t` fatal; local HEAD `7f6ca4c0`), so the kit's Step 2 carries one fetch of main by URL under `.tools/.git-lock`.
- Line pointers (`:68 :100 :113 :162 :169 :173 :177 :229 :270 :284`, comments `:63 :66 :258`) printed by `cat -n`/`awk NR` over the raw bytes fetched with `gh api`. Control: the ticket's own pointers agree.
- Shape census over the four Templates files (`gh api` raw, 836 lines in all): three-quote 0, line-start `#` 0, format-colon hole 0, each with a positive control printing 1. Matches the gate (`B1150_STATUS.md:66`).
- Jira MPSCALC-375: Backlog, 0 comments, done-when quoted verbatim (own in-process GET into scratch; control MPSCALC-363 returned 1 row, Done).
- `B1150_STATUS.md:67, :81-:86, :135, :137, :163` re-printed; the dead-branch finding is `:85` (M7: 0 of 88 probe rows change).
- Partition: `compare main...b1146/mps-358-quantity-rule-api` = 12 files, none is the test file (0; planted control 1). Open PRs #121/#120 list only `web/package-lock.json`. Branch census `^b1[01][0-9][0-9]/` (17): only `b1093` and `b1142` list the file, both landed (#145, #148). 2026-11-03 non-`.pre-` SEAT kits naming the path: B1162 (4), B1164 (1), B1165 (2), all "not on your paths" sentences about landed #148 (control `Dtos.cs`: 16/3/9).
- Panes (tmux, 03:0x): `%0 tuesday`, `%112 Datasec/MPS-G301`, `%113 Datasec/NexusAI-N92`, `%114 Datasec/HPSM-POC-R146`, `%1 fleet-monitor`; no M83 (control G301 = 1). The kit's REFUSE line expects exactly 1 M83 pane at launch (the seat's own) and names "no OTHER M83 pane"; the other-builder scan is by prefix `Datasec/MPS-M` with the own `-M83` line excluded after printing.
- Locks: `.tools/*/heavy.lock` and `.tools/.git-lock` absent at 03:0x (`ls`, read only). G301's tooling dir is `.tools/b1165` (its scripts use `b1165/heavy.lock` and `light.lock`); the kit makes the seat's `heavy.sh` also wait while any other seat's `heavy.lock`/`light.lock` exists.
- CI predicate: `ci.yml:42` `dotnet build MpsCalc.slnx -c Release`, `:43` `dotnet test ... --no-build`; `Directory.Build.props:6` TreatWarningsAsErrors true. SDK `.tools/dotnet/dotnet --version` prints 10.0.401.
- Ports: none assigned; listeners at drafting `44760 44761 49152 5000 59869 7000 49166 49168 49171`, none ours.
- Machine: load1 2.82 (03:01), 3.82 (03:05); 251 GiB free. Gate round: B1150 GO WITH FINDINGS round 1 of 2 (`B1150_STATUS.md:163`); B1105/B1118 NO GO 2 of 2 are the template-store class, not this one.
- Slot count: the kit reads 9 four-underscore lines (8 slots plus the last line), `/usr/bin/grep -c`.

## D-decisions (kit makes; Tuesday stamps)
- D-1 Shape rows are guards over the real Templates files (the gate's own cheapest killing rows), green on clean code, red under a planted instance; the scanner is not made to read those shapes.
- D-2 Guards read raw text (stricter than the scan). 
- D-3 One killing row per named branch, gate cases, hand-written expectations.
- D-4 `:177` is reported, not pinned or removed (the sweep's "report and stop on that item"). Plant P7 expects 0 red; any red means it is not dead, STOP.
- D-5 Three comments rewritten from the seat's own probe printout.
- D-6 G2, becomes G1 only if the scanner or a product file changes (forbidden).
- D-7 Shape plants live in `-mut` product files as comment/directive lines, never committed.

## Q-questions for Tuesday (each with a default)
- Q-1 Remove the four dead lines at `:177-:180`? Default no: report only; a separate test-only follow-up if the owner wants.
- Q-2 Guards on raw text (a shape in a comment trips them) vs code-only text? Default raw text, because the scan cannot be trusted to strip a shape that misaligns it.
- Q-3 The seat needs the offline NuGet cache copied from `.tools/b1146/nuget-home` (about 320 MB; B1162 did the same). Default yes; a restore that wants the network stops the seat.
- Q-4 Pane count: the kit expects exactly 1 `Datasec/MPS-M83` line at launch (the seat's own). Default as written.
- Q-5 Heavy-lock courtesy: the seat waits for G301's `b1165` locks too (kit Step 2). Default yes.

## UNMEASURED
- Whether each row is green at the head and red under each plant (hand-derived from the gate's mutant table, not run); P7's 0-red is the gate's claim, not re-run.
- Exact wording the seat will give the three comments (it derives them from its probe).
- Whether `dotnet test` of the whole solution is clean at the pin (baseline is Step 3).
- Whether any ticket besides MPSCALC-269/-370/-375 owns these rows (the seat re-runs the text search).

## Outside-the-fences disclosure
- Wrote only the two named files, plus scratch in the session scratchpad (a copy of the Jira reader with its out path re-pointed, the fetched test file, the four Templates files, a branch list).
- Jira: read-only GETs (JQL with parentheses; token never printed). `gh api -X GET` only, under the project's `GH_CONFIG_DIR`, including `search/code` (one query) and raw contents. git: `rev-parse`, `cat-file -t`, `ls-remote`, `for-each-ref` with `--no-optional-locks`; no fetch.
- Ran `.tools/dotnet/dotnet --version` (read-only). Read `.tools/b1125` and `.tools/b1146` scripts (heavy/hb/env/ci-dotnet/mutate/plant headers), `.tools/b1162/env.sh` and `ci-dotnet.sh`, `.tools/b1165/{light,dn,ci_dotnet}.sh` as templates; `ls` of lock names only. Read `B1150_STATUS.md` and its evidence probe outputs (read only). Did not read `fleet/briefs_staged/`, scoreboard, `_ledger.md`, any Wednesday/Friday tree, or run `decision_queue.sh`.
- One Bash call was refused by a hook (an unquoted `=====`) and re-issued; one `grep -P` call failed on macOS grep and was redone with a character class.
