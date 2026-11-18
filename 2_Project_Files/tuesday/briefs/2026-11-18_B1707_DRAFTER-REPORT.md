STARTABLE: YES (at main 8ae5db6ea4ea1fb99a7e306d90e36111b6128d9d; no wait: the lane takes no heavy-lock slot, runs no dotnet; one condition the seat checks first, Step 3(b): the production audit must still read 0 at base)

Drafter: Sonnet 5.5 Agent-tool drafter for Tuesday. Clock: `date` reads 11:23:49, 11:25:13, 11:26:21, 11:29:23 AEDT. Files written: the kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1707_SEAT-M160_mps-lane-ci-production-audit-step.md`, its sidecar `.measured` (107 lines, all filled; `stamp_check.py <kit>` exits 0), this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s289/d1707/`. The Stamp has 8 lines of four underscores (S0 to S6 and the last line), unfilled.

## BLUF
- Lane CI-AUDIT (MPSCALC-413) is ONE new step in the `web` job of `.github/workflows/ci.yml`, right after `npm ci` (`ci.yml:61` at main): ONE commit, ONE path, ONE branch `b1707/mps-lane-ci-production-audit-step`, no PR. Four added lines (`@@ -61,0 +62,4 @@`, `1 file changed, 4 insertions(+)`).
- Ruling verified by the READ verb: `decision_queue.sh show mps-413-web-audit-instrument-1118` printed `status: ruled (Datasec/MPS)` and `ruling: choice='a'` at 2026-11-18T11:22:03+11:00; option a detail "Passes today with 0; developer tools updated at the next routine round". client_project is MPS. Nothing added, ruled, amended, withdrawn or delivered.
- Model row C2 (`model-routing.md:92`), gate tier G2 (`:109`: config/CI), model id `claude-sonnet-5-5`, launch carries `BRIEF_SEAT_LEVEL=sonnet`. Note on the row: the task is one file, one hunk, spelled out, which is row L1 shape (`:80`), but check P4 (`:50`) gives Datasec no local tier, so C2 is the nearest Claude row (DERIVED).

## THE FROZEN STEP (exact; the first and last lines are the two unchanged context lines)
```
      - run: npm ci
      # Production dependencies only: the advisories that reach what ships (MPSCALC-413). Passes at 0 today; the development
      # toolchain is not audited here (its high findings are a separate, later dependency round).
      - name: npm audit, production dependencies (blocks on high/critical)
        run: npm audit --omit=dev --audit-level=high
      - run: npm run lint
```

## Why level high (D1)
HPSM-POC's step (`ci.yml:389-390`, read by `gh api -X GET` raw) is `npm audit --omit=dev --audit-level=high` with the same step name, inside the existing web job after `npm ci`. NexusAI's `npm-audit.yml` is a separate workflow (job `audit-production-deps`) at `--audit-level=moderate`. I followed HPSM-POC: a step inside the existing job adds no check name; and `high` is the level the ticket counts. At main the production audit reads 0 at every level (low, moderate, high, critical all rc 0), so the level changes nothing today; `high` means a future moderate-only advisory does not turn main red alone. Q1 below.

## Facts re-measured with instruments
- Main `8ae5db6ea4ea1fb99a7e306d90e36111b6128d9d` (expected value matched; `gh api -X GET git/ref/heads/main`, 11:23 and 11:26); open PRs 0; `matching-refs/heads/b1707` 0 rows. Subject "Correct the source version id uniqueness clause in the API document and contract (#213)". #213 and #212 (the MPSCALC-410 and MPSCALC-207 lanes) have landed.
- `ci.yml` at main: blob `8e96096c...` (contents API `.sha` equals `git hash-object` of the raw file), 146 lines; `audit` on 0 lines (control `npm` 8). Web job `:45-89`, `npm ci` `:61`, `npm run lint` `:62`, `defaults.run.working-directory: web` `:49-51`.
- Production audit at main (scratch extract of the tarball; `npm ci --no-audit --no-fund --ignore-scripts` `added 273 packages`; node v26.13.0, npm 11.20.0): `npm audit --omit=dev --audit-level=high` rc 0, `found 0 vulnerabilities`; `--json` metadata all severities 0, total 0. CONTROL that the zero can fail: the full audit `npm audit --audit-level=high` rc 1, `12 high severity vulnerabilities` (matches the ticket). Lockfile blob `610a0767...` and `package.json` blob `b7ceb57f...` match the ticket's.
- Planted production advisory (scratch copy of the two package files with `minimist` 1.2.5 added by hand as a production dependency, never pushed): the step's command exits 1, prints `1 critical severity vulnerability` and `Prototype Pollution in minimist`. Same package as a dev dependency (lock entry `"dev": true`): `--omit=dev` rc 0 `found 0 vulnerabilities`, full audit rc 1. So the step fails on a production advisory and ignores a development one.
- YAML parse: Ruby `psych` (no `actionlint`, no python `yaml` module on this machine): base and edited both parse; four job keys and `name:` values equal; web steps 9 -> 10, added exactly `npm audit, production dependencies (blocks on high/critical)`, removed none; the other three jobs equal as parsed; all non-jobs keys equal. Controls: a renamed job name compares false; a planted `a: [` raises (rc 1).
- Repo CI text tests on the edited tree (scratch copy of the main extract with the edited file): `scripts/tests/test_ci_workflow.py`, `test_sdk_pin.py`, `test_sdk_pin_routes.py` each print `OK`; control: a planted `- uses: x/y@v1` makes `test_ci_workflow.py` exit 1. No other `.md`, `.yml`, `.py`, `.sh` file of the repo names `npm audit`.
- Job/step names: the diff is exactly one added step. Required checks: the merged PR #213 head `c72ba442...` has 9 check-run names (`package ...`, `CodeQL`, `web (npm ci, lint, test, production build)`, `dotnet (build Release, 0 warnings; test)`, `python (demo harness, infra static tests, deploy tooling)`, `Analyze (python|csharp|actions|javascript-typescript)`); main's own head has the same 8 workflow-side names. A check-run is named by its JOB, so a new step adds and renames none. NOTE: the repository ruleset 24139430 ("Security scan rule") has an EMPTY `required_status_checks` list and branch protection reads 404; so no name is enforced by the ruleset today. The kit keeps all 9 anyway.
- Hygiene instruments on scratch: `git diff --check` rc 0 (planted trailing space rc 2); ASCII scan of added lines 0 (planted U+200B 1); gitleaks 8.30.1 `dir` canary rc 1, clean rc 0.
- Disjoint from the MPSCALC-412 lane (`src/MpsCalc.Import/PriceBookImporter.cs` plus one Import test, per the commission; I did not read its kit): this lane touches only `.github/workflows/ci.yml`. No live `Datasec/MPS-` pane (`tmux list-panes`: 0; control `tuesday` listed). load 5.42, free 1078 GiB.

## Chain inputs table (every input exists at BASE or is made by an EARLIER step)
| Step | Inputs | Source |
|---|---|---|
| 1 Setup | origin main, deploy key, project config email | BASE / project folder |
| 2 Predictions | the kit | BASE |
| 3 Base measures | clone at base, `web/node_modules` (made by step 1 `npm ci`), registry | step 1 |
| 4 Edit | `.github/workflows/ci.yml` at base | BASE |
| 4(d) YAML | base copy from `git show <base>:...` | BASE |
| 4(e) tests | `scripts/tests/*.py` of the clone | BASE |
| 5 Checks | the edit, the ban list file | step 4, BASE |
| 6 Commit/push | the edit | step 4 |

## D-decisions
- D1: level `high`, one step inside the existing web job (HPSM shape), not a new workflow (NexusAI shape). See above.
- D2: ONE commit (no generated copy exists for CI config; unlike B1698).
- D3: no `dotnet`, `npm run lint` or `npm test` in the lane (no code or test file changes; they would add 10+ minutes and a heavy slot and prove nothing about the one path). They are listed NOT RUN; the PR's hosted run is the arbiter. Say if you want `npm test` anyway.
- D4: the comment in the step text names the ticket key MPSCALC-413 (a ticket key, not a B-number, name or card id); it also says the dev toolchain is not audited, so a reader of ci.yml sees the reason for "production only".

## Q-questions for Tuesday (each with a default)
- Q1: level `high` or `moderate`? Default `high` (HPSM-POC's level; 0 at every level today so no behavioural difference now).
- Q2: gate tier. Default G2 (config/CI). Hand to G1 only if the gate finds a security-shaped issue.
- Q3: other stale text found is reported, not edited. Default yes.
- Q4: `npm ci` and `npm audit` registry calls in the seat's own clone and scratch allowed (the kit names them as the only registry exceptions). Default yes.
- Q5 (for the PR, not the seat): the step reaches the npm registry at CI time, so a newly published high advisory on any of the 4 production dependencies turns every PR's `web` job red with no code change. That is the instrument doing its job, but say so to the product owner when you land it. Default: land, and read the first hosted log line of the step (`found 0 vulnerabilities`).
- Q6: the ticket's other halves (which instrument the project follows; what happens to the 12 dev highs) are Tuesday's Jira record after landing, not this lane. Default: the kit says so and the seat writes no Jira.

## UNMEASURED
- A Node 24 reading (the machine's node is 26.13.0; the project has no drive-local node; HPSM-POC has a `node24` which the kit forbids using). The audit depends on the lockfile and the registry's advisory data, not on the Node version (DERIVED).
- The first hosted run of the new step (the PR's own run).
- Whether the registry's advisory set will still read 0 when the seat starts (the seat's Step 3(b) STOPS if not).
- The `.local`-style cross-lane read of the MPSCALC-412 kit.
- Why `ruleset required_status_checks` is empty while the project treats the 9 names as required: not investigated (the kit preserves the names regardless).

## Outside-the-fences disclosure
- I read HPSM-POC's `ci.yml` and NexusAI's `npm-audit.yml` by `gh api -X GET` raw, as asked. The HPSM-POC read ran under HPSM-POC's own `GH_CONFIG_DIR` and the NexusAI read under NexusAI's own, as commissioned. I then repeated the HPSM-POC raw read ONCE under the MPS project's `GH_CONFIG_DIR` (output discarded) to learn whether the seat can do it: rc 0, so the MPS token can read that repo (the kit's Step 3(e) uses the project's own config only). All GET only.
- I listed (`ls`) `HPSM-POC/.tools` to learn whether a `node24` exists (it does); nothing was run or read from it.
- The decision card was read once with `show` into a scratch file under the scratch folder; the card text was read in full (the card is for this very ticket; no other card read; `list` never run).
- Scratch writes: npm registry reached by `npm ci` and `npm audit` only, in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s289/d1707/{main,mainnew,mainplant,plant,plantdev}`; a scratch `git init` repo at `.../d1707/repo` (inside the Tuesday folder) for `git diff --check`; one `sed -i.bak` on my own scratch file `added.txt` (a stream edit of scratch, not a project file; a `.bak` copy remains). No project file, repo ref, Jira row, board, mail, or hosted site was written or probed.
- The Jira helper `jget.py` in scratch reads `.env` in-process and never printed a token; three GETs (MPSCALC-413 whole, a text JQL for `npm audit` / `dev toolchain` that found only the ticket and three unrelated Done keys, MPSCALC-412 and MPSCALC-361 summaries).
