STARTABLE: YES (after the stamp; 5 questions below, each with a default the kit already assumes)

# B1621 drafter report: MPS Commercial Calculator, lane M-G, the SDK pin guard's wording (seat M146)

Drafted 2026-11-16 from 15:44 to about 16:05 AEDT (`date` printed 15:44:44 to 15:53:46; the kit header lists ten of the reads). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1621_SEAT-M146_mps-lane-mg-sdk-pin-guard-wording.md` (87 lines, 12 stamp slots left as `____`) with sidecar `.measured` (104 lines, tags M00 to M15). `stamp_check.py <kit>` rc 0 (104 claims, 104 measured; about 45 of the rows are "INSTRUCTION to the seat" lines for names, paths and markers the seat writes). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s283/b1621/`.

## BLUF
- **Lane M-G fits one Sonnet seat in two parts, two commits, one branch `b1621/mps-lane-mg-sdk-pin-guard-wording`: A = MPSCALC-406 items 1 and 2 (guard docstring line 17 names "Pkcs or Xml pin"; csproj comment line 29 gains two lines tying `KeepPinnedXmlOutOfPackagePruning` to the Xml pin), B = items 3 and 4 at the sweep's question-4 default (four docstring lines naming the MSBuild reader's breadth and the unread global.json keys as accepted; no strictness change, no new row).** Model row C2 (`model-routing.md:92`), gate G3 (`:110`, as commissioned), pane `Datasec/MPS-M146`, READY at Step 0 + 60 minutes, Part A pushed by +30. Nothing deployed, no code line changed.
- **The exact words are frozen in the kit (FACT 5), and every claim the new sentences make was run.** Plant 1 (a `dotnet msbuild` line added after the one `dotnet build` line of `ci.yml`, line 42) gives `problems()` exactly one problem naming `msbuild`; plant 2 (an extra `msbuild-sdks` key in global.json) gives none; the control (`sdk.allowPrerelease`) fires. So the two "accepted" sentences are true of the code at main, and the kit makes the seat re-run them at head and STOP rather than bend a sentence.
- **Proofs the seat repeats (all measured on a scratch copy with both parts applied):** the guard file's code AST with the module docstring dropped is EQUAL to base; the project file parses as XML and its text outside comments is EQUAL to base; `numstat` is 1/1 and 2/1 for Part A and 4/0 for Part B; the two guard files stay rc 0 with 13 and 51 tests (the ticket's counts); `dotnet msbuild ... -getProperty:TargetFramework` prints `net10.0` rc 0. Each has a control that fires.
- **Two traps written into the kit:** (1) an XML comment may not contain `--` or end in `-`: MSBuild refuses the project (MSB4025, measured; the words of A2 avoid both and the seat checks it); (2) **the seat cannot restore or build the Api project**: the machine cache holds Xml 10.0.13 only and the project pins 10.0.15 (NU1102, measured), the kit forbids the registry, so the restore, build, `dotnet test` and `package.sh` are NOT RUN by the seat and are read from hosted CI by Tuesday. The one project-file proof that needs no restore is the MSBuild property evaluation.

## Scope, key by key (the ticket read whole by Jira GET at 15:45)
| key | status | in slice? | reason |
|---|---|---|---|
| MPSCALC-406 item 1 | Backlog, 0 comments | IN, Part A | docstring `test_sdk_pin.py:17` says "raise the Pkcs pin in"; `PublishOutputTests.cs` guards both Pkcs and Xml |
| MPSCALC-406 item 2 | same | IN, Part A | csproj comment ends at `:29` and names no target; the target is `:37` with its own comment `:34-36` |
| MPSCALC-406 item 3 | same | IN, Part B, docstring only | the reader (`:85`, `:262`) flags a plain `dotnet msbuild` (measured); default: named as accepted |
| MPSCALC-406 item 4 | same | IN, Part B, docstring only | `problems()` reads only the `sdk` object (`:149`); default: named as accepted |
Held and dropped check: PRs naming `MPSCALC-406` (all 199, paginated; controls #72, #181, #199 present): 0 (control `MPSCALC-398`: 1). Pickup and today's note: `MPSCALC-406` is named by the records-created lines only (`NEXT-PICKUP-TUESDAY.md:147`, `daily_tuesday/2026-11-16.md:60`); `M-G` by the commission and "not commissioned" lines (pickup `:65`, `:73`, `:107`, `:123`): no hold, no DROPPED line.

## Facts re-measured with instruments (details in the sidecar)
- Main `5e80009525138879031c4b07a18436242dadf46c` at 15:47:00 and 15:53:46; open PRs 0; `heads/b1621` 0 rows (control `heads/b1593` 1).
- Source pointers at main, printed by `grep -n`: the ticket's `:17-18`, `:30`, `:85`, `:262`, csproj `:29` and `:37` are all still right (none moved). Guard file 441 lines, csproj 54.
- Baseline at main (scratch tree of the tarball): `test_sdk_pin.py` rc 0, 13 tests; `test_sdk_pin_routes.py` rc 0, 51 tests. The whole `scripts/tests` loop, each file alone: all 8 files rc 0 (8, 16, 44, 39, 19, 56, 51, 13 tests), about 4.5 minutes. With both parts applied the two guard files are rc 0 with 13 and 51.
- CI readers of these files: `python` job loop (`ci.yml:109-111`), `dotnet` job (`:42-43`), `package` job (`scripts/package.sh:50`). Only the guard and its routes file name `test_sdk_pin`; the publish rows publish the project and read no comment (DERIVED).
- Lanes: 24 of 222 origin branches name `sdk`, `pin`, `guard`, `xml`, `pkcs`, `package`, `csproj` or a b15xx/b16xx number; eight touch this lane's two paths and each is a merged-PR head (#42, #70, #119, #123, #177, #183, #188, #199); the one live branch there, `b1617/...`, changes `web/src/api/stub/` only. Live panes: `Datasec/MPS-R244` (records), `Datasec/NexusAI-N137`, `Datasec/HPSM-POC-H173`; no MPS code pane.
- Machine at 15:51: load 11.28 8.97 9.54; no lock folders (control `b1593` present); 1143 GiB free; ports 9980-9989 free (no port needed).

## Chain inputs (rule 4), in execution order
| step | inputs | produced by / exists at |
|---|---|---|
| 0 | the kit, the STATUS path | exists at launch / this step |
| 1 setup + baseline | clone, identity, deploy key, python3, `.tools/dotnet-10.0.404` | BASE and the machine (printed present above) |
| 2 predictions | baseline counts 13 and 51, `net10.0` | step 1 |
| 3 Part A | guard file line 17, csproj line 29, the FACT 5 words A1 and A2 | BASE; the kit |
| 3 property checks | base and head copies, the seat's own scratch script | steps 1 and 3 |
| 4 Part B | the guard file after Part A (line 32 unchanged), words B1 to B4, the two plants | step 3 (pushed); BASE `ci.yml` line 42 (the one `dotnet build` line) |
| 5 checks | each part's diff; gitleaks canary; the `scripts/tests` loop at base and at head | steps 3 and 4; the clone |
| 7 push | each part's diff | steps 3 to 5 |

## D-decisions the drafter took
- **D1** Two parts, two commits: A (the two wording fixes the ticket's acceptance names) first; B (the two "decide" items at the sweep's default) second, so Tuesday can drop B without touching A.
- **D2** The exact sentences are written into the kit and applied on a scratch copy, so every claim in them is run (plants) rather than left to the seat's reading. A seat that finds one false STOPs.
- **D3** The A2 sentence ties the target to the Xml pin using only the target's own words (it removes only Xml from the prune list; its comment `:34-36`); the ticket's "must go with the Xml pin" is rendered as "exists only for the Xml pin and must go with it: remove or change the two together, never one alone". The ticket's wording is the product owner's source; this phrasing is the coordinator's reading of it.
- **D4** No new guard row and no stricter reader: the ticket allows either "a row red on a plant" or "one sentence ... saying it is accepted", and Tuesday accepted the sentence at the sweep's question 4.
- **D5** "No code line changed" is a proof, not a promise: AST equality (docstring dropped) for the guard file, text-outside-comments equality plus XML parse for the project file, each with a control.
- **D6** The seat runs no restore, build or publish of the Api project (FACT 9). It runs the python loop over `scripts/tests` at base and at head (about 4.5 minutes each), because the CI `python` job runs it and the guard's docstring edit must not break any file in it.
- **D7** G3 is "no gate" in `model-routing.md:110`: Tuesday's completion check plus hosted CI replace it; Q1 offers G2 because the csproj is on the package surface.

## QUESTIONS FOR TUESDAY (each with a default)
1. **Gate tier:** the commission and the sweep say G3 (no separate gate kit). The csproj is the package's project file, but only an XML comment changes (proved by text-outside-comments equality). Default: G3, Tuesday reads the two-file diff at source and hosted CI. If you prefer a G2 read, say so at the stamp.
2. **Two parts or one commit:** default two (A then B), one branch.
3. **The words of FACT 5** (A1, A2, B1 to B4) are the drafter's rendering of the ticket's words. Default: accepted as written; edit them at the stamp if the product owner's reading differs (the seat copies them byte for byte; the plants for B1 to B4 run at the seat's head).
4. **No restore or build by the seat** (cache lacks Xml 10.0.15): default hosted CI's `dotnet` and `package` jobs are the first run of a restore and build on the edited comment. Say otherwise and the kit needs a registry exception for `dotnet restore`.
5. **The python loop** (about 4.5 minutes, light) at base and at head by the seat: default yes. Drop it and the seat runs only the two guard files.

## UNMEASURED
CI's `ubuntu-latest` python version (the box has 3.14.10; the files use the standard library only); hosted CI's `dotnet`, `package` and `python` jobs on the edited files; whether MSBuild's evaluation proof would also catch a comment placed outside the project element (not planted); the `infra/tests` and `tools/demo/test` files of the CI python loop (the first needs the bicep compiler; not run, and the edit cannot reach them: DERIVED from `grep -rn` of `test_sdk_pin` and the csproj path); the behaviour of the dotnet host on a global.json key other than `sdk` (the new sentence says only what the guard reads).

## Outside the fences (disclosure)
Read: the commission, DRAFTER_RULES, SWEEP-1450 (lines 78-112 and 162-172), the B1617 kit, sidecar, report and STATUS (template), `model-routing.md` rows (grep -n), `models_latest.json:23`, `brief_seat.sh:31`, the pickup and today's note (grep for the key and `M-G`), the B1611 kit (grep for this lane's paths: 0 hits; its `src/MpsCalc.Api` hits are a reading table), `GATE-VERIFIER-STANDARD.md` step 7 (ban list; no name copied into the kit). At main, by `gh api -X GET` (ref, pulls paginated, branches paginated, compare, tarball, contents): the guard file, the project file, `ci.yml`, `package.sh`, `Directory.Build.props`, `global.json`, `test_sdk_pin_routes.py`, `PublishOutputTests.cs`. Jira: GET only through my own helper `fleet/state/s283/b1621/jget.py` (project `.env` read in-process, token never printed): MPSCALC-406 and MPSCALC-361. **Ran, beyond reads, in my scratch folder only:** python property and plant scripts (`plant406.py`, `props406.py`, `mkedit.py`, `fill.py`) over scratch copies; the two guard test files and the whole `scripts/tests` loop (about 4.5 minutes) on a scratch tarball of main and, partially, on a partial copy of it (`treeA`, which lacks `infra` and `tools`, so its `test_deploy_pre1` rc 1 there is the missing tree, not a finding; the full-tree loop is all rc 0); `dotnet restore src/MpsCalc.Api/MpsCalc.Api.csproj --source ~/.nuget/packages` (rc 1, NU1102; it named the machine cache as its only source, so no registry call, but it wrote `obj` folders in my scratch tree), and `dotnet msbuild ... -getProperty` (several times, one with a planted `--` on a scratch copy, restored with `cp` and `cmp`). No push, no PR, no Jira write, no mail, no board, no `az`, no `cd`, no deploy; I did not read `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, or any `decision_queue.sh` output, and used no Artifact or Docs tool. The scratch folder holds a 104-line `measured.skeleton1` (the first `--init`, superseded; ids identical to the final sidecar's).

DRAFTED B1621: kit 87 lines, sidecar rc 0, questions 5
