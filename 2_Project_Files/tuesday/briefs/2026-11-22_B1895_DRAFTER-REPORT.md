STARTABLE: YES - the kit for seat M173 (MPSCALC-430, 431, 432 in `infra/tests/test_infra.py` and MPSCALC-433 in `infra/scripts/validate.sh`) is written, its sidecar is complete (`stamp_check.py` exits 0, 121 claims), every edit was prototyped on a copy of main and run green and red, and the seat is not startable until Tuesday stamps the ten slots.

# DRAFTER REPORT B1895 (lane M-I + M-S, one seat) - drafted 2026-11-22 15:13 to about 15:40 AEDT (clocks by `date`) by a read-only drafter for Tuesday

## BLUF
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1895_SEAT-M173_mps-infra-tests-and-validate-comment.md` (72395 bytes, 508 lines), sidecar `...md.measured` (121 lines: 58 measured, 63 "unmeasured by design" command or word literals), this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s308/d1895/` (tarball of main, base tree `tb/`, prototype `proto2/` and `proto3/`, `red_full/` with the 31 red and green runs, `ci_final/`, the GET-only Jira helper `jget.py`).
- Base: code main `9c9a72199dca98026b5acab7020c409ae47db39f` (read 15:13:36 and 15:24:12 and 15:35:03, equal), 0 open pull requests, `matching-refs/heads/b1895` 0 rows (control `heads/b1790` 1 row), 225 pull requests of all states name none of the four keys (control `MPSCALC-418` finds #224). The tickets cite lines at `28d8d31b`; the blob of `test_infra.py` is unchanged (`c0e6a272`), so every cited line still prints what the ticket says.
- The build is fully frozen in one tool, `apply_edits.py` (8 edits to `test_infra.py`, 1 to `validate.sh`; it asserts each `old_string` occurs once, writes whole new content to a temp file and `os.replace`s it). Applied, the blobs are `6486350d718c6c720b2989602cccd6d9df9f9d6a` (`test_infra.py`) and `22322327ddc2dcb13f57b28b71a2c27187a4d80c` (`validate.sh`); two independent applications gave the same bytes. `git diff --no-index --numstat`: `106 9` and `1 1`.
- Test counts (MEASURED): `test_infra.py` 43 at base, 49 at head (+5 table tests, +1 site-plants test with 7 sub-tests); `test_validate_script.py` 6 before and after. The CI python loop at head: 15 files, rc 0 each (table in the kit).
- Red proof (MEASURED, `red.py`, 31 labels, `DIFF 0`): every new cell is red under the ticket's own planted defect and green without it; the ticket claims were reproduced at base first (430: pinned literals emptied reads 4 failing sub-tests, plants list emptied reads OK 43; 431: one real defect fails 34, a removed setting gives the bare `KeyError`, ids swap 16; 432: each of the seven properties planted in the template source leaves the whole file OK at base).
- The kit's seat read load is about 120.6 kB (below the 300 kB Sonnet bar; breakdown below).

## The tickets as drafted (the four checks, each quoted verbatim in the kit) and their red/green results
| Ticket | The check the kit builds | Red (defect planted) | Green |
|---|---|---|---|
| MPSCALC-430 | `TheTablesAndPlantListsAreNotEmpty` (5 tests): key sets of `COMPUTED_SETTINGS` (6), `PINNED_LITERALS` (4), `SITE_EXPECT` (13 after 432), the setting plants (13) and the site plants (7) | `h430-pinned` 5 failing (the new test + 4 plant sub-tests), `h430-computed` 7, `h430-site` 12, `h430-plants` 1, `h430-siteplants` 1: each table or list emptied turns the new test red; at base `b430-pinned` 4 failing and `b430-plants` OK 43 (the ticket's own claims) | `head0`: Ran 49 tests, OK |
| MPSCALC-431 | `new_problems(before, after)` helper; `one_setting_problem`, the id-swap test and the planted-source test compare with the unmutated template and assert exactly one new problem naming the key; a removed setting not in the template fails with `setting <KEY> is not in the unmutated template, so there is nothing to remove` | base with one real defect: `b431-defect` 34 failing, `b431-ids` 16, `b431-removed` 37 failures + 1 bare `KeyError`; head: `h431-defect` 2, `h431-ids` 4, `h431-removed` 6 (the removal test now carries the named-key message); control `h431-two` (a checker that reports two problems per change) fires 34 | `head0` |
| MPSCALC-432 | seven rows added to `SITE_EXPECT` (alwaysOn True, http20Enabled True, remoteDebuggingEnabled False, use32BitWorkerProcess False, appCommandLine "dotnet MpsCalc.Api.dll", clientAffinityEnabled False, publicNetworkAccess "Enabled"; all seven are written literally by the template at `showcase.bicep:42,46,47,48,52,38,39`) and `TheSitePropertyGuardsFireOnPlantedSource` (7 plants of the template SOURCE, each exactly one new site problem naming the property) | `b432-1..7`: each property planted in the source leaves the base file OK, 43 tests ("a changed value stays green"); `h432-1..7`: each pin removed makes its plant sub-test the one failure | `h432-control` (selector alone): Ran 1 test, OK; `head0` |
| MPSCALC-433 | line 4 of `validate.sh`: `step 3` becomes `step 2` (README numbers the what-if as step 2 at `:59`, the create as step 3 at `:65`); `check433.py` reads the step number from the README | base `check433.py` exit 1 (`header names: ['3']`), planted step 4 exit 1; `README.md step 3` counts 1 in `infra/scripts` at base | head `check433.py` exit 0 (`['2']`); `README.md step 3` counts 0; `test_validate_script.py` Ran 6 tests, OK; `bash -n` rc 0; mode 755 kept |

## Facts re-measured with instruments (details and controls in the sidecar and the kit)
- Jira (GET, own helper, token never printed): the four tickets read whole at 15:13:49; each Backlog, 0 comments, 0 links; `key = MPSCALC-361` reads Done (control for the helper).
- Compiler `Bicep CLI version 0.48.1 (cec7951cf6)` at the project's `.tools/bicep-v0.48.1/bicep`; `Python 3.14.10`. Machine at 15:14: 995 GiB free, load 2.34 1.76 1.63; no `Datasec/MPS-` pane at 15:14, 15:34 or 15:35 (3 panes; control: one named `tuesday`). No `.git-lock` and no `b1895` entry in the project's `.tools`. No port block is needed.
- Readers of the two changed files (CENSUS in the kit): only `test_validate_script.py` reads `test_infra.py` (a sentence the edits do not touch, `:87`) and runs and reads `validate.sh` (no test reads the comment; `README.md step` finds 0 lines of both test files, control 1 line of `validate.sh`); dotnet and web frames name no path under `infra/` (0; control `docs/` 69).
- Identity: project repo's configured email is 29 bytes, name 12; the repo's `core.sshCommand` is stale (names `/Volumes/Laptop-DEV/`, 1 occurrence); the deploy key file exists.

## The checks of the kit that the seat runs: STOP-severity ones run once on the prototype with their control
- Blobs after `apply_edits.py` equal the prototype's: PASS (twice, from two copies; the kit's code blocks were extracted from the final kit and compared byte for byte to the tested files: equal).
- `red.py` 31 labels all MATCH: PASS (one full run, `red_full.log`: `labels 31 | DIFF 0`); control: a mutated checker (`h431-two`) FIRES; the `Ran 0 tests` guard is in the script and was not triggered.
- `scans.py` over the 107 added lines: 0 non-ASCII (control U+200B fires), 0 Cf (control fires), 0 GUID (control fires), 0 host words (control: `app-mpscalc` is on 1 line at base), underscore-aware name scan 12 names quiet and 12 controls `_by_<name>_` fired, 0 tabs.
- `check433.py`: base exit 1, head exit 0, planted step 4 exit 1.
- gitleaks (8.30.1): `dir` on a folder with a random `ghp_` canary rc 1; on a folder with the two changed files rc 0.
- The CI python loop at head, run from the kit's own `ciloop.sh` block on a fresh copy (`proto3`, edits applied by the kit's `apply_edits.py`): `files=15 nonzero=0`, every rc 0, the `Ran` figures equal the kit's CENSUS table (log `ci_final.log`).
- NEVER RUN (marked in the kit and the sidecar): `git diff --name-only <base>` and `git diff --numstat` on a real commit (equivalents run: `cmp` over both trees found exactly 2 of 734 files differ; `git diff --no-index --numstat` printed `106 9` and `1 1`), `gitleaks git` over a commit range, `git log --format='%h %ae | %ce'` (no commit exists), the clone, push and read-back steps, hosted CI, CodeQL, the dotnet and web jobs.

## D-decisions (all Tuesday's as coordinator, each sourced in the kit)
D1 key sets, not counts, for 430, and five things pinned, not three (Q1). D2 pin the template's own value for all seven properties; none is left at a platform default (Q2). D3 `new_problems` is a multiset difference, defined once. D4 the older class `EachGuardFiresOnItsOwnTerm` is left alone (431's own note). D5 the site plants are a new class mirroring the 418 plants test, not an edit of it. D6 one docstring line (E1) is extended so the module's own check list stays true. D7 edits go in by `apply_edits.py`, not the Edit tool, because the file holds a non-ASCII line and the new text is 106 lines; the script refuses to change the non-ASCII line count.

## Questions for Tuesday (each with the default the kit assumes; none blocks the start)
- Q1 what 430 pins: default five key sets. Alternative: the three tables only, or row counts (a swapped row would pass).
- Q2 432: default pin the template's value for all seven. Alternative: leave `publicNetworkAccess` and `clientAffinityEnabled` as "platform defaults" (the template sets both explicitly).
- Q3 431 "first failure names the key": with one real defect the first failure printed is the planted-source sub-test of that key; its label names the key but its message is the bare `unique anchor` (MEASURED, `h431-defect`). Default: leave it. Alternative: a ninth edit naming the plant in the anchor message of the two plant tests (needs a longer `old_string`: the `unique anchor` text is on 2 lines at base inside plant tests and 1 in an older test).
- Q4 one commit (default) or two. Q5 433 rides with the tests (default). Q6 gate G2, one Sonnet reader. Q7 branch `b1895/mps-infra-430-433`, subject of 101 characters. Q8 level sonnet (routing row C2, `model-routing.md:92`; G2 at `:109`). Q9 the seat prints its counts.

## UNMEASURED (named so nobody reads them as measured)
- `git`-based checks on a real commit, the push, the read-back, hosted CI, CodeQL (the new code uses temp-folder and file-open idioms already in the file), the dotnet and web jobs.
- Whether the CI python loop's demo-harness tests (`tools/demo/test/*`) open loopback listeners while they run: they ran in the scratch copy and passed; their ports were not inspected.
- The seat's own timing (the kit sets READY = Step 0 + 75 minutes; the drafter's whole loop plus red runs took about 4 and 7 minutes of compute).
- Any `Ran` figure of the 13 CI files the lane does not change at the seat's own run (the kit says: the same or the difference is named).

## Reading load of the seat, by program (bytes)
kit 72395 + project `CLAUDE.md` 8103 + `test_infra.py` 32313 + `showcase.bicep` lines 30-55 838 and 57-92 2740 + `validate.sh` 1655 + `README.md` lines 56-66 1159 + `test_validate_script.py` lines 84-90 422 + `ci.yml` lines 96-118 1000 = **120625** (sidecar 13.6 kB not read by the seat; the code blocks inside the kit are counted in the kit).

## Chain-step inputs (each produced by an earlier step or present at base)
| Step | Inputs | Where they come from |
|---|---|---|
| 0 | the stamped kit, `.tools/.git-lock` | the kit; the lock dir is made in Step 1 |
| 1 | S2, project repo identity, deploy key, `BICEP` binary | stamp slot S2; `config --local` of the project repo; `3_Access_Keys/github_deploy_rw`; `.tools/bicep-v0.48.1/bicep` (present at drafting) |
| 2 | the clone at base | Step 1 |
| 3 | Step 2's counts | Step 2 |
| 4 | the clone files, `showcase.bicep` | Step 1 |
| 5 | `apply_edits.py`, `red.py` (code blocks of the kit), the base tree | the kit; `git archive` of the base made in Step 1 |
| 6 | `check433.py`, `scans.py`, `ciloop.sh` (kit blocks), the edited files, the base tree | the kit; Step 5; Step 1 |
| 7, 8 | Step 6's green checks, the ssh key | Steps 5-6; FACT 6 |

## Outside the fences, disclosed
Read-only reads beyond the commission's list: the project `CLAUDE.md`, the sweep, the form kit B1876 and its sidecar and report, `DRAFTER_RULES.md`, `model-routing.md` lines 92, 98 and 109, `brief_seat.sh:31`, `models_latest.json`, `stamp_check.py` header. Jira GET of MPSCALC-430, 431, 432, 433 and MPSCALC-361 (control) by my own helper `jget.py` (reads the project `.env` in-process, prints nothing of it). `gh api -X GET` only: main ref, pulls (open and all states), matching refs, repo settings, one commit. The tests ran ONLY in my scratch copies under `fleet/state/s308/d1895/` (never inside the project), including the other 13 files of the CI python loop, which execute demo-harness and deploy-tooling tests against fakes. Two Bash calls that carried an accidental `rm` line (one on a scratch path that did not exist, one on `/dev/null`) were refused by the hook; nothing was deleted or moved, and `proto`, `proto2` and `proto3` all remain in the scratch folder. No write to any project, Jira or GitHub; no message to any human; no `az`; no hosted call.
