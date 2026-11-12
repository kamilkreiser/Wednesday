GATE B1530: GO WITH FINDINGS @ 184cb81 on main 1515a71 (round 1 of 2)

Gate G2 (tests, tooling and CI-reader change), round 1 of 2, 2026-11-12 11:33-13:53 AEDT. Project MPS Calculator, tickets MPSCALC-389 and MPSCALC-391, branch b1530/mps-389-391-sdk-guard-picker-spec @ 184cb810422073d2afdc5bb4a49c7c4468a0a270 (184cb81), two commits over base 793d0a9c52c961852b4a1f04bb826ffff752ce74. Gate session s272; it replaces the s271 gate that died with its coordinator (nothing of its folder is counted; I reused no clone).

Findings by class: Blocker 0, Major 0, Minor 3, Note 4. No security-shaped issue found (no input, URL, regex-from-variable, HTML sink, file mode or subprocess added). Both guards turn red on the planted defects they claim to catch and green on the real files; the 391 spec runs in the stub step only and fails if the page-estimate sub-row is counted as a line row.

## Refs and merge (measured)
- `git ls-remote` at 12:50: branch = 184cb810422073d2afdc5bb4a49c7c4468a0a270 (one b1530 ref), main = 1515a71dc5a5f28eaf6c13ac129cc600f8d10b02. Main was 5239020 when the builder pushed and moved again during this gate (one squash for MPSCALC-160). Open PRs 0 (`pulls?state=open --jq length` printed 0).
- Head vs current main: `rev-list --left-right --count` 2 2 (head 2 ahead, 2 behind: #186 and the MPSCALC-160 squash). merge-base = 793d0a9 (the base).
- Changed paths: 4 of 4 inside the lane (test_sdk_pin.py M, test_sdk_pin_routes.py A, b100-picker-many.spec.ts M, playwright.config.ts M). Diff +425 -4 (`--numstat`: test_sdk_pin.py 193/1, test_sdk_pin_routes.py 223/0, b100-picker-many.spec.ts 9/2, playwright.config.ts 0/1). Removed lines, printed whole: the old step-key `re.match` line, `const rows = ...`, `toHaveCount(6)`, the LEFT_OUT entry; nothing else.
- Held byte-identical base = head = main (`rev-parse <sha>:<path>`): global.json 89ddff24, .github/workflows/ci.yml de0ac3b5, scripts/package.sh 51ff3fb2, web/package.json f74032cf, web/package-lock.json 7c7d4608. Changes under web/src 0.
- Main gained since the builder's base: 793d0a9 -> 5239020 (#186, four web files: print.spec.ts, proposal-buttons.spec.ts, ProposalPage.tsx, ProposalPage.test.tsx) and 5239020 -> 1515a71 (MPSCALC-160: docs/API.md, docs/ENGINE.md, docs/api/openapi.json, PricingPolicy.cs, QuoteEndpoints.cs, three tests/MpsCalc.Api.Tests files, web/src/api/generated/{SOURCE.txt,openapi.snapshot.json,schema.ts}). `comm -12` of main-gained and head paths: empty (overlap 0, with the positive control that main-gained lists 15 paths and head lists 4).
- `git merge-tree --write-tree 1515a71 184cb81` rc 0, tree 3abf25b3. `diff-tree -r --name-only main merge-tree` lists exactly the 4 head paths and their blobs equal the head blobs (4d36d69b, 5bd807f3, 26046ae3, 88386e3f). Control: a synthetic commit editing the same LEFT_OUT line merged against head gives merge-tree rc 1 (conflict detected). Earlier merge at 5239020 (tree 53a1d036) was also rc 0 and equal main + head blobs; the results below say which main each ran on.
- Commit identity: both commits `kamil.kreiser@datasec.com.au | kamil.kreiser@datasec.com.au`, equal to the project repo's own `user.email`. Each message ends with the attribution line once; each subject ends with its ticket key; no key in the body.
- Landing: ci.yml is the only workflow; a merge triggers no deploy. Org CodeQL ruleset applies (CLAUDE.md:50).

## Both guards: red first, then green (my own mutations)
Method: copies of the head files under `fleet/state/s272/g1530/mutwork/Mxx`, one defect planted per copy in the REAL guard code, the 34 new rows and 13 old rows run with `python3 -I -B`, copy rebuilt from head for the next plant. Python 3.9.6.
| Plant (guard feature removed) | new rows red | old 13 |
|---|---|---|
| M01 quoted-key alternative out of STEP_KEY | 3: double-quoted dotnet-version, single-quoted dotnet-version, quoted global-json-file naming global.json | green |
| M02 DOTNET_ allow-list loop disabled | 6: workflow-level, any-case, job-level DOTNET_ROOT, step-level ON_NO_CANDIDATE_FX, GITHUB_ENV write, package.sh copy | green |
| M03 DOTNET_ read case-sensitive | 1: any-case row | green |
| M04 install routes disabled | 4: dotnet-install + dot.net/v1, --roll-forward, RollForward, install route in script | green |
| M05 uses_problems unhooked | 1: third action naming dotnet | green |
| M06 unreadable_forms unhooked | 6: flow with, flow step, repeated key, anchor, alias/merge, block scalar | green |
| M07 flow read / M08 anchor read / M09 block-scalar read / M10 repeated-key read disabled singly | 2 / 2 / 1 / 1 matching rows | green |
| M11 CI script-set check disabled | 2: other.sh, bare scripts/other.sh | green |
| M12 script text not read for routes | 2: DOTNET_ name and install route in the script | green |
| M13 nested walk ignores non-root / M16 name compare case-sensitive | 1 / 1: nested global.json row (src, tests/Sub, lib/Global.JSON) | green |
| M14 SKIP_DIRS not applied | 3: nested row + both skip-directory controls | green |
| M15 symlinks followed | 1: symlinked-directory control | green |
| M17 pin_note constant | 1: pin_note literal row | green |
| M19 comment lines not ignored in route_problems | 2: comment control and clean-script control | green |
| M20 repeated-key counter removed | 1 | green |
| **M18 all_problems drops script_problems and nested_problems** | **0 (all 34 stay green)** | green |
Every plant but M18 turns at least one new row red; the old 13 rows stay green in all 20 plants (a row that cannot fail would show here). Restored = green: real files at head, 13 + 34 tests, rc 0 (`test_sdk_pin.py` Ran 13 OK, `test_sdk_pin_routes.py` Ran 34 OK).
- The 13 original methods: AST compare of the base blob and head blob, per method source: 13 base, 13 head, 13 identical, 0 changed, 0 removed (control: one body altered in a copy is detected). The only changed original line is the old `m = re.match(...)` in `setup_dotnet_steps`, now `m = STEP_KEY.match(l)` (test_sdk_pin.py, diff -1).
- The kit's "15 existing rows" is wrong; the source has 13 at base. Builder was right to follow the source.
- My own adversarial probes on copies of the real files (`probe.py`, `probe2.py`, `probe3.py`; real-files control returns 0 problems every time): step env DOTNET_ROLL_FORWARD 1; quoted env key 1; `${{ env.DOTNET_ROOT }}` in a run 1; script with dotnet-install 2; nested src/global.json 1; quoted extra `uses: 'evil/setup-dotnet@v1'` 1; one-line flow `with:` 2; flow mapping on the next line 2 (the builder listed that as not closed: it is closed); YAML tag `!!str` on dotnet-version 1 (builder listed as not closed: closed); `docker://mcr.microsoft.com/dotnet/sdk:9.0` 1; mixed-case `Actions/Setup-DotNet@v1` 1; CRLF file with a planted quoted dotnet-version or DOTNET_ROLL_FORWARD 1 each; inline `# DOTNET_ROOT` after code 1 (conservative); a run line `echo rollforward` 1 and `echo dotnet_format` 1 (conservative over-trigger by design). Not closed, confirmed: `$GITHUB_PATH` write 0, `shell: pwsh` step 0, `MSBuildSDKsPath` env 0, `uses: ./local` 0, as the builder listed.
- ReDoS timing of the new patterns (STEP_KEY, SH_PATH, ANCHOR) on 200000-token adversarial lines: under 0.02 s each; no nested overlapping unbounded quantifier.

## 391 spec
- `--list`, CI stub shape (env of ci.yml:67-73 at my ports) at main 1515a71 -> merge: **gained exactly the 2 test names of this spec (b100-picker-many.spec.ts:41:1 and :74:1), lost 0**; 202 -> 204 tests, 17 -> 18 files. Api-off `--list`: main 51 = merge 51, lost 0, gained 0; the spec is absent from api-off (testMatch, playwright.config.ts) with print.spec.ts present there as control. The printed left-out list shrinks from 8 names to 7 (spec gone). Head vs base-shaped main (5239020 list): stub 197 + 2 = 199 files 18, api-off 46 = 46.
- Measured sub-row literal: the spec passes 3 of 3 with `deviceLines = 1`, `PICKABLE.length` = 6, whole table 6 + 1 (head tree, stub CI shape, ports 9947; 2 passed each run, rc 0). It is a measured literal read from the stub's rendering, per the kit.
- Fails when the sub-row is counted as a line row (plants in a copy `plant/`, one spec file per run, restored and compared equal to head after):
| Plant | Result |
|---|---|
| product: `PageEstimateRow.tsx:30` `<tr className="bom-subline">` loses its class | test 1 RED, `toHaveCount(6)`: Expected 6, Received 7; test 2 green |
| spec: line rows read with plain `tbody tr` (sub-row counted) | test 1 RED, Expected 6, Received 7 |
| spec: `deviceLines` = 2 | test 1 RED, Expected 2, Received 1 |
| spec: `deviceLines` = 0 | test 1 RED |
| spec: line-row locator filtered to match none | test 1 RED |
| spec: wrong line-number expectation (runner control) | test 1 RED, toEqual |
| unmodified head spec x3 | 2 passed each, rc 0 |
- Stub off, mode unset: 2 skipped, rc 0 (the `test.skip` at spec :37). With `MPSCALC_E2E_MODE=api-off` the spec argument matches no test ("No tests found", rc 1): not run in api-off, as testMatch requires.
- Not loosened: `expect(` 10 -> 12, `test.skip(` 1 -> 1; added lines carry no `.only`, `fixme`, `waitForTimeout`, `ts-ignore`, `eslint-disable` (each pattern fires on a planted line). Two lines removed, nine added; the new lines are stricter (three counts and the two column reads scoped to line rows).
- Lint control: `npm run lint` rc 0 at main, head, merge; a copy with `var`, `debugger` and an assignment in a condition gives rc 1 (5 problems), so lint reads this spec.

## CI by program (my clones; Node v24.22.2; Playwright installed Chrome; ports 9941-9949)
| Check | main (1515a71) | head (184cb81) | merge (head on 1515a71) |
|---|---|---|---|
| python job loop (`python3 -I -B`, ci.yml:102-107) | 9 files rc 0 at 5239020 and again at 1515a71 (run_demo not re-run there); run_demo env-red; 2 infra files NOT RUN (no bicep) | 10 files rc 0 incl. both guard files; run_demo env-red; 2 NOT RUN | at 1515a71: 10 files rc 0 incl. both guard files; run_demo not re-run (same red at the older merge tree); 2 NOT RUN |
| `test_sdk_pin.py` / `test_sdk_pin_routes.py` / `test_ci_workflow.py` | 13 OK / absent / OK | 13 OK / 34 OK / OK | 13 OK / 34 OK / OK |
| `npm run lint` | rc 0 | rc 0 | rc 0 |
| vitest, sorted `path :: fullName` lists | 1541 passed, 0 failed, 145 files, 1541 unique | 1531 passed, 0 failed, 145 files, 1531 unique | 1541 passed, 0 failed, 145 files, 1541 unique |
| list diffs | - | main -> head lost 10 (the 10 ProposalPage rows main gained from #186; head's base predates them), gained 0 | **main -> merge lost 0, gained 0**; head -> merge gained the same 10, lost 0 |
| stub-step Playwright (whole `npx playwright test`, ci.yml:67-73 shape) | not re-run at 1515a71 (see NOT RUN) | 194 passed, 5 skipped, 0 failed (6.3 min); both picker-many rows in it | 194 passed, 10 skipped, 0 failed, rc 0 at 1515a71 + head (6.0 min; the earlier merge tree 5239020 + head gave the same 194 / 10 / 0 in 7.9 min); the 5 skips beyond head's are the print.spec rows that skip in the stub step by design; both picker-many rows passed in it |
| api-off step (whole) | - | `--list` identical to base, 46 | `--list` main = merge (51), lost 0 gained 0; whole step NOT RUN (see below) |
| `VITE_MPSCALC_AUTH=entra npm run build` + `check-bundle.mjs dist` | - | not run (web/src, package files and the lock are byte-identical to the base; the merge run covers it) | rc 0; 8 files, 1109118 bytes, markers 0/57 |
Vitest note: hosted-like timeouts are 5 s per test. While other seats loaded this machine (load1 30-45) three whole-suite runs of head at the default timeout failed 3, 12 and 5 tests, a different set each time, all `Test timed out in 5000ms` or a DOM query that had not rendered yet, in files this change does not touch. The same 3 first-run files passed 17 of 17 alone at head and at main (load 44). The final three runs (head, merge, main) used `--maxWorkers=3 --testTimeout=60000` and are the numbers in the table; the three red runs are kept in `out/vitest-head-run{1,2,3}-*.json`. Hosted CI is the 5 s judge. The suite does not read the changed files except `web/src/test/pdftotextTimeout.test.ts:17,74`, which reads only the `timeout` value of playwright.config.ts (green in the table).
Controls: the sorted-name comparer prints `lost 1` when one name is removed from a copy; a planted `sys.exit(1)` file reads rc 1; a planted failing assertion fails the spec (rc 1, above).
Python job, the two reds that are not this change: `tools/demo/test/test_run_demo.py` fails the same three tests at main, head and the earlier merge tree (`C5StopsExactlyWhatItStarted`: `test_ctrl_c_is_never_reported_as_an_unexpected_stop`, `test_ctrl_c_stops_api_and_web_and_leaves_a_bystander_in_the_same_dir`, `test_sighup_closing_the_terminal_also_stops_both`; md5 of the sorted FAIL/ERROR lines equal in all three). The script prints "Ctrl-C cannot reach this script (it was started with SIGINT ignored, e.g. in the background)": my runs were background jobs, so it is the environment, and a hosted runner is not backgrounded. Named, not mine.
Other jobs whose tests read the changed paths: `grep -rn -i -E "test_sdk_pin|b100-picker-many|LEFT_OUT|playwright\.config|global\.json"` over tests scripts infra tools web/src web/e2e .github (excluding the two guard files) prints: ci.yml:40,64,120 (setup-dotnet inputs and a comment), four `.cs` test METHOD names containing `left_out`, `web/e2e/b83-feedback-attachments.spec.ts:6` (comment) and `web/src/test/pdftotextTimeout.test.ts:17,74` (a Vitest that reads playwright.config.ts: ran green). Control: the same grep with `ci\.yml` prints test_ci_workflow.py and both guard files, and test_ci_workflow.py ran rc 0 at head and merge. dotnet and package jobs read no changed path (no .cs, csproj, global.json, script or workflow byte changes). Repo-wide tracked-file scans: this repo has no `infra/tests/test_hidden_characters.py` (`ls infra/tests`: test_infra.py, test_validate_script.py; no tracked file matches hidden|ascii|charact); the added lines and messages are ASCII (0 non-ASCII; control U+200B reads 1) and Cf 0 (control U+202E reads 1).

## Scans (added lines 425, messages 2; every pattern has a planted control that fires)
- Names, underscore-aware `(?<![A-Za-z])<name>(?![a-z])`, planted `x_by_<name>_y` reads 1 for each: Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, Friday, Tuesday, Wednesday, Thursday, Monday, Jarvis: 0 in added lines and in both messages. B-numbers and seat ids 0 (control fires). Ticket keys: 0 in added lines; one in each commit, at the end of the subject only. Decision-card id 0; GUID/tenant id 0; secrets (ghp_, AKIA, BEGIN PRIVATE, eyJ, password=, api_key=) 0; hosts: the only hits are `dot.net/v1` strings inside test plants and one escaped pattern (no URL is fetched); emails 0 in code (the attribution line in messages is the noreply address).
- gitleaks: random `ghp_` canary rc 1; `base..head` rc 0 ("2 commits scanned, no leaks found").
- CodeQL JS/TS pre-scan over the 9 added web lines: `new RegExp(`, `eval(`, `Function(`, `innerHTML`/`dangerouslySetInnerHTML`, `child_process`, `.replace(/[` hand-escape, nested quantifier: 0 each (control 1 each).
- CodeQL Python pre-scan over the 416 added py lines: any `chmod`/`umask`/`mode=`/`0o` literal/`stat.S_I*`/`os.open(`/`makedirs(..., mode)`: **0** (case-sensitive; a first case-insensitive pass flagged `LACKS_INPUT` and `ci_runs_is_missing` as S_I... false positives, retracted; control `os.chmod(p, 0o755)` reads 2); `tempfile.mktemp` 0; `subprocess`/`os.system`/`exec`/`eval` 0; bare `except` 0; `open(` without `with` 0 (all 7 are `with open`); `re.<fn>(` with a non-literal first argument 0 (every pattern is a raw string literal; no `re.escape` constant); host-like dot in a pattern is escaped (`dot\.net/v1`); pickle/yaml.load/marshal 0. `tempfile.TemporaryDirectory` is used 7 times (no mode). `os.symlink` appears once in a test, creating a link inside a temp directory (not a permission change). Module-level names never read: only `ROOT` in test_sdk_pin.py, which the sibling file reads as `guard.ROOT` (a quality note at most).

## Findings
| # | Sev | Finding |
|---|---|---|
| F1 | Minor | `scripts/tests/test_sdk_pin.py:303-308` `all_problems(root)` (the function that chains `problems`, `script_problems` and `nested_problems` for the real-files row at `test_sdk_pin_routes.py:72-74`) has no row that plants a defect through it. Mutation M18 (drop `script_problems` and `nested_problems` from the return) leaves all 47 rows green, so a mistake in that wiring would not be seen: each reader is proved alone on a planted tree, and the real-files row only proves a clean tree reads clean. Suggested follow-up: one row that builds a temp root with a copy of ci.yml, a script with a DOTNET_ name and a nested global.json and asserts `all_problems(root)` equals the three expected lines. |
| F2 | Minor | Builder STATUS "CHECKS: Other readers of my paths ... the only hits are four `.cs` TEST METHOD NAMES" is false at source. The same grep also prints `web/src/test/pdftotextTimeout.test.ts:17,74` (a Vitest that reads `playwright.config.ts`), `web/e2e/b83-feedback-attachments.spec.ts:6` and `.github/workflows/ci.yml:40,64,120`. Harmless: that Vitest reads only the Playwright `timeout` value and is green at head and merge. |
| F3 | Minor | Builder STATUS FOR TUESDAY lists as "NOT closed" a multi-line flow mapping and YAML tags; at head both ARE reported (flow mapping on the line after `with:` -> 2 problems; `dotnet-version: !!str 9.x` -> the dotnet-version problem), and a `docker://...dotnet...` action is reported too. The list understates the guard. The routes it lists that I confirmed open (0 problems on a plant): `$GITHUB_PATH` write, `shell: pwsh`, `MSBuildSDKsPath` env, `uses: ./local`, plus the `allowPrerelease` and `paths` keys of global.json and a second workflow file (docstring test_sdk_pin.py:26-28 says so). Recorded as follow-ups below, not as findings against this commission. |
| F4 | Note | Kit says "15 existing rows"; source has 13 at base and head, all unedited (AST compare). Kit wrong, build right. |
| F5 | Note | Conservative over-triggers by design: `RollForward` matches any code-line word containing `rollforward` in any case (an `echo rollforward` fires) and any `dotnet_<anything>` fires. A harmless new name costs one deliberate edit of the allow-list, which the docstring names as the policy. |
| F6 | Note | Builder STATUS records two heavy-slot slips of its own (a premature release, a release while its job still ran). No job of mine ran with both slots held by others; mine are in `heavy-events.txt` with the load reads (pairs 120 s apart, not independent). |
| F7 | Note | Builder STATUS says the guard file "passed 450 lines with the rows in it (581)"; the head guard file is 387 lines and the sibling 223. The split is allowed by kit D-8 with a sentence (STATUS gives it). |

## Claims graded (builder STATUS)
- Two commits, four allowed files, nothing held changed: true. 13 original rows green and unedited: true. 34 new rows: true (34 methods; Ran 34 OK).
- Each guard red-proved on a plant, two mutations of the real code turn the matching rows red: true (and 19 more mutations of mine do).
- 391: line rows 6, sub-rows 1, whole 6 + 1; `LEFT_OUT` entry removed (one line removed, none added); stub `--list` +2 tests +1 file, api-off unchanged; 3 of 3 passes; stub off 2 skipped rc 0; whole stub step 194 passed, 5 skipped, 0 failed: true on all counts (my whole-step run: 194 / 5 / 0 on head).
- Vitest 1531 -> 1531, lost 0 gained 0: true against base (head 1531 unique names, equal count; I did not run base itself, main and merge give 1541 = 1531 + the 10 main gained).
- Python loop: same rc as base for all files, new file rc 0: true (apart from the environment-red run_demo, equal at all trees).
- gitleaks, name scans, ASCII scan, identity: true (re-run by me).
- "Other readers of my paths ... only .cs test method names": false (F2).
- Main moved by one commit after the pre-push read, disjoint: true; main has moved a second time since (MPSCALC-160), also disjoint.
- Kit-vs-source count (15 vs 13): true, 13.

## Follow-ups (not findings against this commission)
Routes the builder left open, confirmed open: `$GITHUB_PATH` writes and PATH edits, PowerShell steps, MSBuild SDK variables, local actions, `allowPrerelease`/`paths` in global.json, a second workflow file, runtime-built names, the runtime setup-dotnet installs before the pinned SDK. Plus F1's wiring row, and the builder's note that `setup_dotnet_steps` could call `step_blocks` (two step walks live in one file now).

## NOT RUN
- Hosted CI and CodeQL (they decide; the CodeQL pre-scan is by pattern only; codeql is not installed here).
- `infra/tests/test_infra.py` and `test_validate_script.py` (no Bicep compiler at `$HOME/.azure/bin/bicep`); the dotnet and package jobs (no .cs, csproj, global.json, script or workflow byte changed); Linux/ubuntu Python (3.9.6 only).
- `tools/demo/test/test_run_demo.py` at the final merge tree 1515a71 (ran at main 5239020, head and the earlier merge; same three environment reds).
- The whole stub step at main 1515a71 (baseline taken from the builder's base run and my head/merge runs).
- The api-off whole step (51 tests expected at merge) and a build at head: queued behind other seats' heavy jobs and cancelled at the hard-stop approach. The api-off `--list` is identical at main and merge and the spec cannot run in api-off, so only print.spec (main's #186 rows, untouched here) would run there. Hosted CI is the proof.
- Three-run repeats of every Playwright spec other than the picker-many spec (3 runs on head; 1 whole-step run per tree).
- No push, no PR, no Jira, no mail, no az, no hosted HTTP except `git ls-remote`/clone/fetch over SSH and `gh -X GET`. Both heavy slots I used were released (holder files moved into `logs/`); no listener of mine remains in 9940-9949 (`lsof -nP -iTCP:9940-9949 -sTCP:LISTEN` printed 0 at the end; no lock dir of mine held); the plant tree, mutation copies and `dist` output are in my folder, nothing deleted.

## FOR TUESDAY
- Land head-pinned squash: the exact command is in `landing.txt` (N left as `<N>`). Texts: `pr-title.txt`, `pr-body.txt`, `squash-subject.txt`, `squash-body.txt`. The squash body ends with the Opus attribution line the gate standard requires; this gate ran on Sonnet.
- CodeQL / hosted CI to watch: the `python` job (new test_sdk_pin_routes.py runs under the `scripts/tests/test_*.py` glob; Python 3.9-clean here), the web job stub step (now 199 tests; the picker-many spec adds about 5 s), and `py/overly-permissive-file`, which my pre-scan finds 0 of.
- Main has moved twice since the builder's push; none of it touches the lane (merge-tree clean at 1515a71). If main moves again before landing, `--match-head-commit` is on the branch head, which is unaffected.
- Hosted-runner risk for the 391 spec is small (it is the stub step, 6 rows, one device line); if it fails there, the literal `deviceLines` (b100-picker-many.spec.ts:60) is the first suspect.
