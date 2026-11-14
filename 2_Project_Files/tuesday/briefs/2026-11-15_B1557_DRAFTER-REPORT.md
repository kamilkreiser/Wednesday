STARTABLE: YES (round 2 of 2 on the B1554 branch; four asks only; read Q-1 and Q-2 before stamping)

# B1557 drafter report (SEAT-M133, MPS round-2 FIX kit), drafted 2026-11-15 07:20 to about 07:33 AEDT (`date` printed 07:20:47 first and 07:31:52 last)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1557_SEAT-M133_mps-round2-token-xtrace-pre1-time.md` (85 lines, 12 lines with four underscores = S0 to S10 and the last line, ASCII only: `LC_ALL=C grep -c -v -x -E '[ -~]*'` printed 0; person-name scan underscore-aware printed 0 for 11 names, control `x_by_kam_y` printed 1). Sidecar `...md.measured` (134 lines). `stamp_check.py <kit>` exit 0: `101 claims, 101 measured, 0 not measured`.

## BLUF
- The kit asks for F1, F2, F3 and F8 and nothing else; F4 to F7 and N1 to N5 are named as the records pass's and the seat may not touch them. One forward commit on the same branch, fast-forward push of `355fe9e81fe8aa68a3699c8975e92dcf89ed2233`, ends `READY B1557: <sha40>`.
- **Both fixes were trialled by the drafter in a scratch copy of head's `scripts/`** (the repo untouched): F1 with `kudu_get` taking its own token after `{ set +x; }` and the `rf_token` lines removed: the gate's probe went from `token lines 2` to `token lines 0` at count 0 and above 0, rc unchanged (0 and 1); F2 with `[0-9]` and `\Z`: the 5 forms turn from red to green and the other forms stay green. So the shape the kit names meets its own property.
- **The 5 F3 forms are NOT in the round-1 fixture** (they were the gate's own extra probes, idx 242 to 349 of the gate's list; the fixture has 242 forms, 5 already `knownDifference`). So F3 is "add 5 entries", and F2 is "add 5 entries"; the fixture goes to 252. Red-first for F2 is real (drafter's trial: the two property rows list exactly the 5 names); for F3 there is no red (they pin PRE-1's current stop), and the kit says so.
- F1 and F2 red-first in the seat's clone is measured here only in the scratch copy; the seat measures it in its own.
- The kit adds NO test method (F1 cases go inside the existing `test_xtrace_never_prints_the_token`, F2 and F3 are data), so the seat's checks are `Ran N` equal for every file and `comm -23`/`comm -13` against base both printing 0 lines.

## Facts re-measured (instrument, control)
- Refs 07:21 AEDT: branch `355fe9e81fe8aa68a3699c8975e92dcf89ed2233`, main `0bb3ed12808d72d3187c51d56852b7ecd2174666` (`gh api -X GET .../git/ref/heads/<ref> --jq .object.sha` under the project `GH_CONFIG_DIR`); open PRs 0 (`pulls?state=open --jq length`); `matching-refs/heads/b1554` length 1; `compare main...355fe9e8` ahead 2 behind 0, 7 files.
- Head files fetched by `gh api ... -H 'Accept: application/vnd.github.raw'` into `d_mps2/head/` and a scratch tree `d_mps2/tree/` (22 paths of `scripts/` and `global.json`). Every `file:line` in the kit was printed by `grep -n` or `sed -n` over those files: `deploy-from-ci.sh` 325 lines (`:195` `rf_token=""`, `:196` `kudu_get`, `:197` `{ set +x; }`, `:198-199` the global token read, `:206-207` the leak, `:209`/`:214` callers, `:236-238` call order, `:109-115` `read_overlay`, `:281-288` `download_wwwroot`, `:280` comment); `deploy-package.py` 846 lines (`:448` `PRE1_TIME`, `:539` `pre1_time_ok`, `:541` `.match`, `:444` limit); `test_scripts.py` 737 lines (`:464` the method, `:215` its class, `:22` the token constant, `:466` `SHELLOPTS`).
- **F1 reproduced** with the gate's probe `probe_xtrace.py` over head's scripts, `PATH=/usr/bin:/bin`, `/usr/bin/python3` 3.9.6: count 0 `rc 0 token lines 2`, count above 0 `rc 1 token lines 2`, lines `+ rf_token=<TOKEN>` and `+ [[ -n <TOKEN> ]]` (the token is the fake constant; the gate's probe masks it in its print).
- **F2 and F3 reproduced**: head's `pre1` on the gate's `345.bin` to `349.bin` printed `PRE-1 count: 0 {} info: {}` rc 0 each; on `242 244 271 280 341` printed `PRE-1 count: 1 {...}` rc 1 each. The gate's oracle TSV (350 rows) rows 345-349 REFUSED/REFUSED, 242 244 271 280 341 OPENED/OPENED (sidecar K11); the full sha256 of each of the 10 `.bin` and of the 5 gate files the seat copies are in the sidecar (K9, K10) so the seat can compare its own bytes.
- F8: the gate's log `.../g1554/out/red-test_deploy_pre1_forms.py.log` tail `Ran 16 tests` / `FAILED (failures=20, errors=2)`; `grep -c -E '^(FAIL|ERROR):'` on it printed 22.
- CI predicate: `ci.yml` at head 139 lines, python step `:96-107`, loop `:102-104` (`python3 -I "$t" || rc=1`, `exit $rc`); `.github` not in the branch's 7 files. Gate's loop at head (`g1554/out/head.loop.txt`): test_scripts rc 0 Ran 56; forms rc 0 Ran 16; rollforward rc 0 Ran 22; test_run_demo rc 1 and test_infra rc 1 (the two environmental reds, in the kit).
- Ports 9760-9769: `lsof -nP -iTCP:9760-9769 -sTCP:LISTEN | wc -l` printed 0 (control: unfiltered 16); the word-boundary scan of the 5 non-`.pre-` 14/15-Nov SEAT kits printed 0 each (control `x 9763 y` printed 1); no pane with `MPS` in its name (0 lines of 7).
- Model: `model-routing.md:92` row C2 (Sonnet 1st) read with `:67` (credential-surface rule: a fully spelled-out mechanical edit may go below Opus, its gate then always tier 1); `:93` row C3 is the DESIGN surface and does not apply; gate G1 `:108`. Id `claude-sonnet-5-5` at `models_latest.json:23`. `brief_seat.sh:31` defaults to opus, so the launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
- Landing rule: project `CLAUDE.md:50` printed "Seats push a branch only;" (`grep -c` 1).

## Chain input table (every step's inputs exist at base or come from an earlier step)
| Step | Inputs | Source |
|---|---|---|
| 0 | gate copy files (probe, gen, oracle .cs and .sh, TSV, 10 bins) | exist in the gate folder now; sha256 in sidecar K9, K10 |
| 1 | clone, base-tree at `355fe9e8`, loop files | base |
| 2 | the 10 forms as fixture entries, oracle .cs, forms folder, dotnet 10.0.404 | entries from step 3a's recipes (the kit orders: 2a builds them; 3a writes them to the fixture) |
| 3 | fixture entries, edited `test_scripts.py` method | step 2a; base |
| 4 | red lists of step 3 | step 3 |
| 5-9 | the fix, the loop at base | steps 1, 4 |
| 6 (F8) | round-1 forms test and fixture at `355fe9e8`, main's `scripts/` | base, main |

Note: step 2 and step 3 both name the entries; the kit says 2a builds the byte strings and compares them with the gate's, 3a writes the entries into the fixture. If the seat finds the order awkward it may write the entries first; the oracle needs only the byte strings. This is the one place a seat could stumble; Q-3.

## D-decisions (mine)
- D-1: BASE is the branch head `355fe9e8`, not main, for the baseline loop and the oracle tree; the branch changed no `src/`, so the app's reader is the same. The cumulative count against main (2 lost, 40 gained) is restated, not rebuilt.
- D-2: F3 default is LIST (the ask's "prefer listing"); making PRE-1 pass a form is named as outside the kit.
- D-3: F1's shape is the gate's and `read_overlay`'s own (take the token in the subshell per call); other shapes allowed if they meet the property and the kit's by-program check (every `az account get-access-token` line sits in a subshell function whose first line is `{ set +x; } 2> /dev/null`; at head 355fe9e8 that table is `:111` yes, `:206` NO, `:283` yes).
- D-4: the new fixture entries are inserted after line 4 (`"forms": [`) so no existing line changes; the removed-line allowance is then about the F1 and F2 lines only.
- D-5: `test_scripts.py` is allowed for ONE method only; the kit says the F1 cases go inside the existing method (name unchanged, lost and gained 0) with an assertion that the run really went through `kudu_get`, so the test cannot pass vacuously.
- D-6: clocks: READY target Step 0 + 75, no new step after +100, hard stop +120 and never later than S9 (the user's proposal: 2 hours).
- D-7: the oracle gets the same HEAVY rule as round 1 (load gate under 24, two reads).
- D-8: the gate's `oracle.sh` and `.cs` are copied and renamed by the seat; if the seat's oracle row differs from the gate's for the same bytes: STOP with both.

## Q-questions for Tuesday (each with a default)
- **Q-1: Sonnet or Opus for the seat?** F1 is a credential surface. Default: Sonnet (row C2 with the `:67` rule: the edit is spelled out, the design is the gate's; row C3 `:93` is for the design decision); the gate after is G1 Opus anyway. If you prefer Opus, change `BRIEF_SEAT_LEVEL` in the launch line and S7.
- **Q-2: base for the baseline loop = the round-1 head (D-1)**; default yes.
- **Q-3: order of steps 2 and 3** (above); default: leave as written; the seat may reorder.
- **Q-4: the same `$`-anchor shape sits at `deploy-package.py:50` (`SHA`) and `:671-672` (`NEWTYPE_FILES`)** (Python's `$` also matches before a trailing newline). Not in the gate's findings and not reachable in practice by the drafter's reading (the names come from lines split on newlines); the kit names them under FOR TUESDAY and changes nothing. Default: leave to the records pass.
- **Q-5: the round-1 STATUS file stays as it is**; the F8 correction lives in the round-2 STATUS (default as asked).

## UNMEASURED
- The seat's own oracle run of the 10 forms (the kit makes it a step; the gate's TSV is RELAYED).
- Hosted CI and CodeQL; any real `az`, Kudu or host run.
- The runner's own Python and bash.
- Whether any other test file counts `az account get-access-token` calls (the drafter grepped `tests/*.py` in the 22 fetched paths: 0 hits; the seat's loop is the proof). The fix makes `az` be asked once per Kudu read, a few more fake calls, none to a host.
- Whether a form added at the top of the fixture changes any row that indexes by position: `test_deploy_pre1_forms.py` looks forms up by name (`BY_NAME`, `:43`) and writes files by position only in `setUpClass`; the drafter's scratch run with 10 entries added at the top printed no such effect.
- Final state at 07:3x: kit 85 lines, sidecar 134 lines, `stamp_check.py <kit>` exit 0.

## Outside-the-fences disclosure
- Read-only reads: the gate's folder `fleet/state/s275/g1554/` (probes, TSVs, logs, `tmp/forms/*.bin`), the VERDICT, the round-1 kit and STATUS, the project `CLAUDE.md:50`, `.env` NAMES only (`grep -c -E '^JIRA_(BASE_URL|EMAIL|API_TOKEN)='` printed 3; no value printed), `model-routing.md`, `models_latest.json`, `brief_seat.sh`, `DRAFTER_RULES.md`.
- Wrote only: the kit, its `.measured`, this report, and scratch files in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s275/d_mps2/` (`head/`, `tree/`, `forms/`, `gen_sidecar.py`, `paths.txt`, `red_f2.txt`, `o.txt`). The scratch `tree/` was edited by me (fixture entries, the two fixes) to run the trials; it is a copy, not a repo.
- Ran: the gate's `probe_xtrace.py` and `gen.py` (read-only inputs, outputs in my folder), head's `deploy-package.py pre1` on 10 bins, the forms and rollforward tests in the scratch tree, `bash -n`, `dotnet --version` (the project's own 10.0.404 SDK, no build). No git write verb, no clone, no fetch, no `az`, no docker, no ssh, no HTTP beyond `gh api -X GET`. No Jira call (the kit makes the seat read it). No WEDNESDAY, FRIDAY, Secuura or non-Datasec tree opened. The fake token constant `fake-token-6b1f0c` was printed once in my tool output by an assertion message (a synthetic test constant, not a credential).
- One hook refused an `rm` (I had meant to remove a stale sidecar skeleton); nothing was deleted: the skeleton was overwritten by the real sidecar.
