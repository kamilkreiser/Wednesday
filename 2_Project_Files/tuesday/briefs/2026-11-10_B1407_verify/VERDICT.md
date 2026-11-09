GATE B1407: GO WITH FINDINGS @ f1a5283 on main 089a639

Tier G1 (kit S8: scripts change). Scope gated: MPSCALC-119, MPSCALC-201, MPSCALC-205. MPSCALC-203 is HELD (NEEDS-SHARED) and is not in this landing.
Re-read at 08:40:52 AEDT 2026-11-10 by `git ls-remote` (deploy key): branch = f1a52832216a10f1e45fcce6e9a8618e5216c119 (= READY), main = 089a63939c5b787168264862b35919e895b0211d.

## Findings

| # | Severity | Finding | Evidence (instrument) |
|---|---|---|---|
| 1 | Major (not a landing blocker; follow-up ticket) | The unchanged sibling script `infra/scripts/validate.sh` still offers `az bicep` as its third Bicep route (`:5`, `:13-14`) and `infra/README.md:22` documents it ("else `az bicep`"). Its build/lint steps use that route, then it calls `tests/test_infra.py` (`:29`) with `BICEP=""`, and the test no longer falls back to az. Result: on a machine whose only Bicep is `az bicep`, validate.sh is GREEN at main and RED at head. This is the behaviour the ticket asks for (never az) and CI is unaffected (`ci.yml:83` exports BICEP), but the out-of-lane script and README line now state a route that fails. Fix belongs to a lane owning `infra/scripts/**` and `infra/README.md` (e.g. validate.sh passes the compiler it found as BICEP, README:22 drops the az route for the tests). | Probe `probe_validate.sh` (scratchpad): fake `az` forwarding `az bicep <sub>` to the standalone 0.48.1 compiler, PATH without real az, BICEP unset: main rc 0 "== validate: OK" (6 fake-az calls); head rc 1 "no Bicep compiler: set BICEP ..." (4 calls). |
| 2 | Minor | `scripts/entra_apps.py`: at base the security-only check ran on the group whether found OR just created by the POST; at head `find_all_roles_group()` checks only a found group, and `ensure_all_roles_group(grp)` returns the POST response unchecked. The POST body sets mailEnabled false / securityEnabled true, so the practical risk is low, but one defensive read-back was dropped. No row pins it. | Source diff base..head, `entra_apps.py:167-183` (DERIVED, not run). |
| 3 | Minor | An added line carries an old brief number: `tempfile.mkdtemp(prefix="b14-nobicep-")` (`infra/tests/test_infra.py`, new class). It mirrors the existing `prefix="b14-bicep-"` in `compile_bicep`, so it is a naming convention, not a reference; the kit's (d) scan bans `B###` in added lines. | Case-insensitive `(^|[^a-z])b[0-9]{2,5}` over the 170 added lines: 1 hit (control `B1407` fires 1). |
| 4 | Minor | Claims not re-measured by the gate: CI `package` job exit 0 / 50 files at main and head, and the real-SDK 205 chain (base reproduces the ticket's refusal; head stops first; `dotnet clean` then package rc 0). | NOT RUN here: load1 8.84 (over the sweep's 7) and `.tools/.heavy-lock-1` held at 08:40. Replaced by the program proof in Probes below; hosted CI is the proof for the package job. |
| 5 | Info | My first parallel run of the CI `python` job showed `tools/demo/test/test_run_demo.py` C5 (2 ctrl-c rows) FAIL at main, head and merge alike. Cause: my harness ran the three trees as background `&` jobs, which ignore SIGINT. Re-run in the foreground: main 3 of 3, head, merge: 23/23 ok. Not the branch. | `out/rd-*.log` |

No blocker: 0 paths outside the lane, 0 secrets, 0 names, 0 reds at head/merge that are green at main in CI, 0 hosted touches, and a merge triggers no deploy (`ci.yml` is the only workflow; it has no deploy job, header `:1`; the package job only uploads a 7-day artifact on main).

## Steps and results

1. **Refs.** ls-remote branch = READY sha. Changed paths base `31234f5f`..head: 5 of 5 inside OWNS (`infra/tests/test_infra.py`, `scripts/entra_apps.py`, `scripts/package.sh`, `scripts/tests/test_entra_all_roles.py`, `scripts/tests/test_scripts.py`). Open PRs 0 (`gh api -X GET pulls?state=open`, control closed `per_page=5` = 5). Sibling kits B1400..B1409: their "Your paths" rows name 0 `infra/` or `scripts/` paths (control: this kit's row names 4). Live sibling branches b1402, b1404, b1405, b1406: 0 file overlap with this branch (control self-overlap 5). Branch is 3 ahead, 2 behind main (main moved only `docs/IMPORTER.md`, `tests/MpsCalc.Api.Tests/TemplateIsolationTests.cs`).
   **203 hold:** `scripts/deploy-from-ci.sh` blob `a7ba4ee1` is identical at base, head and main; `git diff base head -- scripts/deploy-from-ci.sh` = 0 lines; commits touching it in base..head = 0 (control: package.sh = 1).
2. **Merge.** Own clone in the session scratchpad, push URL `INVALID-NO-PUSH`, never pushed. `git merge-tree --write-tree main head` rc 0, tree `7d099946`. Merge vs main differs in exactly the 5 lane files, each equal to the head blob; main's 2 moved files equal the main blobs.
3. **CI.** Only workflow: `.github/workflows/ci.yml`. Jobs reading changed files: `python` (runs every `infra/tests` and `scripts/tests` file) and `package` (runs `scripts/package.sh`). `dotnet` and `web` read none of the 5 files.
   - `python` job (every file `python3 -I`, BICEP = project-local 0.48.1, Python 3.9.6): main 190 rows, head 200, merge 200; lost 0 (main->head and main->merge); status changes on kept rows 0; head rows == merge rows; gained exactly 10 = the builder's 10 new rows (3 `TheCompilerIsNeverAz`, 4 `AllRolesGroup`, 3 `PackageStaleReleaseBuild`). Per file at head: infra 28, entra_all_roles 15, scripts 44, others unchanged.
   - `package` job: NOT RUN (finding 4).
   - Repo-wide hidden-character walk over tracked files: main, head and merge each 680 text files, the same 6 files with Cf characters (pre-existing test fixtures), delta 0 (control: a planted U+200B file is found).
   - `bash -n scripts/package.sh` rc 0 at main, head, merge (control: a broken script rc 2). `py_compile scripts/entra_apps.py` rc 0 at all three. shellcheck: not on this machine, NOT RUN.
4. **Red without the fix** (copies of head with ONLY the product change taken back):
   - 119 (az branch restored in `bicep_command`): `..._the_command_is_none_even_with_az_on_path` FAIL, `..._compile_fails_naming_bicep_and_never_runs_az` ERROR; `test_bicep_on_path_is_used_when_the_env_is_unset` stays ok (a control by design).
   - 201 (base `entra_apps.py`): all 4 new rows FAIL.
   - 205 (base `package.sh`): `..._refused_before_publish_naming_the_fix` FAIL; the 2 controls stay ok by design. Mutation check on the controls (guard widened to every file in obj/Release): `test_a_release_build_without_symbols_reaches_the_publish` FAILS, so the controls bite. No vacuous test.
5. **Closed lines.** No ALREADY-ON-MAIN lines. The HELD 203 lines were re-printed at main 089a6393: `deploy-from-ci.sh:97` ("One Kudu VFS GET"), `:110` (`--retry 2`), `:116` and `:160` (`mkdir -p "$DIR.live"`), `:118`/`:120` (`umask 077` on the copy only), `:137` (`pre1_hosted`), `:143` (`az webapp deploy ... --clean true`): all as the STATUS states.
6. **Probes.**
   - package.sh guard (lines 43-44 of head, run in isolation under `set -euo pipefail`): fresh merge tree (0 `obj/` dirs under src) passes; `.pdb` in `src/*/obj/Release` STOPs naming the dir and the `dotnet clean` fix; `.pdb` only in obj/Debug, only in bin/Release, only under `tests/`, or obj/Release without a .pdb: passes; no `src/` at all: passes (`|| true` holds under pipefail); two projects, three pdbs: one STOP listing both dirs once; a space in a project dir: listed intact.
   - **No change alters what a deploy does:** the package.sh diff is 5 added lines, 0 removed (`@@ -39,0 +40,5 @@`), before the publish; on a fresh checkout (CI, and the runbook's "clean checkout of that exact sha") the guard evaluates to empty and every following line is byte-identical, so the package is built exactly as at main. `deploy-from-ci.sh` and `deploy-package.py` are untouched. `entra_apps.py` is never run in CI or deploy; its write sequence for a normal run is unchanged (the group GET moved earlier; the POST and assignments are at the old place).
   - 119 with BICEP unset and PATH=/usr/bin:/bin: rc 1, "no Bicep compiler: set BICEP ...", 0 skipped.
   - Doc sentences checked at source: test_infra docstring "as CI does" (`ci.yml:83` exports BICEP): true. entra docstring/help "without it the read-back ... exits 1": true for both flags (`entra_apps.py:339` empties `groups` without the flag so `:350` fails; without `--approver-only-user` the named account's assignment counts as a 5th user at `:340`). STATUS "without flags the keys equal the pre-MPSCALC-136 set and order": true (`a6813d7^` summary keys api, spa, seed, kam, seedAssignmentIds, azureCliPreauthorized).
7. **Scans** over the 170 added lines and the 3 commit messages: ban list (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, plus Friday, Tuesday, Wednesday) with `(?<![A-Za-z])<name>(?![a-z])`, case-insensitive: 0 (planted `_by_Kam_` fires). Upper-case B-numbers 0; lower-case 1 (finding 3). GUIDs, tenant/subscription ids, hosts 0; emails: only synthetic `t@example.test` and the attribution trailer. Non-ASCII / Cf 0 (control fires). gitleaks 8.30.1: `ghp_` canary rc 1, range base..head rc 0.
8. **Claims** (builder STATUS):
   - Branch head and read-back = f1a52832: TRUE.
   - Files = exactly the 5 allowed: TRUE.
   - python job main 190 -> head 200, lost 0, new red 0, gained the 10 rows written: TRUE (re-measured at main 089a6393 as well).
   - 119 red-first (2 red, 1 control ok): TRUE. 201 all 4 rows red at base: TRUE. 205 1 red + 2 controls ok: TRUE.
   - gitleaks canary rc 1, range rc 0: TRUE. Property scans 0 hits: TRUE for its pattern set; finding 3 is outside it.
   - Ahead 3, behind 2, merge base 31234f5f: TRUE.
   - HELD 203 file:lines and blob a7ba4ee1 at main: TRUE.
   - Summary keys without flags equal the pre-MPSCALC-136 set and order: TRUE.
   - package job exit 0 / 50 files at main and head; real-SDK 205 chain: NOT SHOWN (finding 4).
9. **Tier.** G1 followed: scripts checked line by line at source, syntax-checked, probed; no security-shaped issue beyond finding 2 (Minor, defensive check dropped on a just-created group).

## NOT RUN
- CI `package` job (dotnet publish + npm ci + deploy-package.py): load1 8.84 over the sweep ceiling and a heavy lock held; hosted CI is the proof.
- CI `dotnet` and `web` jobs: they read none of the changed files.
- shellcheck: not installed on this machine.
- Hosted CI, CodeQL, any hosted site, `az`, Entra: never (fences). `entra_apps.py` was exercised only through the repo's fake az.
- Node 24 (CI) vs local: not relevant to the run jobs (python only).
