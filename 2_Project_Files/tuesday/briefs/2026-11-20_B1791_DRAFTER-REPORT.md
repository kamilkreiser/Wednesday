STARTABLE: YES - a kit for one file (`infra/tests/test_infra.py`) on main debb5e28, the project's own bicep 0.48.1 is on the machine, every literal measured; two readings of the ticket (Q1, Q2) are Tuesday's to confirm at the stamp.

# B1791 drafter report (lane M-3, seat M170, MPSCALC-418), drafted 2026-11-20 17:53 to 18:03 AEDT

## BLUF
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1791_SEAT-M170_mps-infra-setting-values.md` (57,465 bytes), sidecar `...values.md.measured` (92 claims, `stamp_check.py` exit 0: "92 measured, 0 not measured"), this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/d1791/` (prototype scripts in `proto/`, tarball in `tar/` and `full/`, none of it run as a project test).
- The change: 8 new tests (35 -> 43, DERIVED), +145 lines, 0 removed, 3 hunks, in `infra/tests/test_infra.py` only. It pins the compiled ARM expression string of six computed settings, a shape for `AllowedHosts`, the four app-setting literals no check pins, and the two ids as the module call passes them. 13 source plants prove each row.
- Every plant was MEASURED at function level: 13 of 13 compile rc 0, the existing six checks (`all_problems`) read 0 problems on all 13, the new functions read exactly 1 problem naming the row on all 13, and the base template reads 0 new problems.

## Facts re-measured with instruments
- main `debb5e28f7bbd4e0f641a829eb353ac356afdd81` at 17:53:49 and 17:56:44 (`gh api -X GET`); 0 open PRs; `matching-refs/heads/b1791` 0 rows (control `b1767` 1 row); search for MPSCALC-418 total 0 (control MPSCALC-278: 3).
- Ticket MPSCALC-418 read whole by my own Jira GET helper (`proto`-free, in scratch `jget.py`): Backlog, 0 comments, 0 links, updated 2026-11-20 10:18 AEDT. Scope sentence and acceptance check are quoted in the kit.
- `test_infra.py` blob `34ebbeda76155d3336579c744eef11cb64510f27` (equals the sweep's `34ebbeda`), 494 lines, 35 tests by program (12 + 16 + 2 + 2 + 3), 1 non-ASCII line (line 3).
- Compiled template (project bicep, my copy in scratch): the 18 app settings are 11 literals and 7 expressions; the seven expression strings are printed in the kit.
- CI predicate read at `ci.yml:104-118` (bicep v0.48.1 via `az bicep install`, then the loop over 15 test files, rc 0 each).

## Bicep in the seat (the commission's question)
Found: `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/bicep-v0.48.1/bicep` (Mach-O arm64, 116,883,328 bytes; `--version` prints `Bicep CLI version 0.48.1 (cec7951cf6)`, the same version CI installs). Not on PATH, `$BICEP` unset, not under brew. The file finds the compiler as `$BICEP`, then `bicep` on PATH, nothing else (`test_infra.py:57`). The kit tells the seat to run `env -C <clone> BICEP=<that path> python3 -I infra/tests/test_infra.py` and to install nothing. I ran the binary only for `--version` and `build` of copies in scratch.

## Questions for Tuesday (each with its default in the kit)
- Q1 what "compiled value" means: default = pin the exact expression string (`bicep build` never substitutes an id, so "build with two synthetic ids" has nothing to fill). Alternative: an evaluator or `bicep snapshot`; whether 0.48.1 supports it here is UNMEASURED.
- Q2 which "remaining literals": default = the 4 unpinned app-setting literals (the ticket's "Where" is `showcase.bicep` 60-91). Alternative: also the 7 unpinned site properties (`alwaysOn`, `http20Enabled`, `remoteDebuggingEnabled`, `use32BitWorkerProcess`, `appCommandLine`, `clientAffinityEnabled`, `publicNetworkAccess`).
- Q3 the new guards stay outside `ALL_CHECKS` (inside, 2 existing tests would flip from 1 problem to 2); Q4 the module-call pin is IN; Q5 gate G2; Q6 level sonnet (row C2, `model-routing.md:92`); Q7 branch `b1791/mps-infra-setting-values-418`; Q8 seat prints counts.

## Census of tests that pin the old behaviour (by program, frame = `test_infra.py` at main, 35 tests)
No existing expectation changes: 35 of 35 stay untouched (1 + 11 + 16 + 2 + 2 + 3). The only ones that WOULD change if the new check were folded into `ALL_CHECKS` are `test_secret_shaped_azuread_value` (`:387`) and `test_secret_shaped_spa_value` (`:391`) (one problem becomes two): that is why it is not folded in. `infra/tests/test_validate_script.py:86-91` reads `test_infra.py`'s text (the missing-compiler sentence at `:69`): the kit forbids touching it (D7).

## Corrections to the commission and to the sweep's row
- The sweep row's gate guess, size M and "`bicep` on PATH or `$BICEP`" are right; its "needs a working standalone bicep in the builder's seat" is satisfied: the project already holds one (above).
- The sweep says `test_infra.py` "contains `bicep` 21 times"; I did not re-count it (not needed).
- The ticket's "build the template with two synthetic ids, read the compiled value" does not match the compiler: the compiled value is an expression string. The ticket's "10 shared literals" does not match the template's 11 literals (the deploy record may exclude one); the kit pins by the template.
- The ticket says the old file is blind; MEASURED partly wrong: 3 of the 13 plants (the Spa client id swap and both module-call swaps) leave a parameter unused and bicep prints a `no-unused-params` warning, which the existing `test_build_has_no_warning` should catch (DERIVED, not run). The other 10 are fully blind.
- The commission says "run no test"; I read that as no project test. I did call the new reference functions from a scratch script over real compiles (~30 builds, ~0.6 s each) and `ast.parse`d the patched copy; I did not run any unittest class.
- Template kit had a stale `core.sshCommand` note; it holds here too (the project repo's config names `/Volumes/Laptop-DEV`, count 1): kit FACT 7.

## Reading load (bytes, by program)
kit 57,465 + `test_infra.py` 23,184 + `showcase.bicep` 6,994 + `main.bicep` 3,225 + names list 698 + `test_validate_script.py` lines 80-91 691 + gate-standard line 31 3,038 + project `CLAUDE.md` 8,103 = **103,398 bytes**, under the 300 kB aim. Tuesday's own stamped kits are not on the list.

## Chain inputs (rule 4)
Each step's input exists at main or is made by an earlier step: Step 2 baseline (main files) -> Step 4 blind proof (needs the clone, bicep path, unedited test file) -> Step 5 code (the reference diff) -> Step 6 red proof (needs the code of Step 5) -> Step 7 checks (needs the diff) -> Step 8 commit -> Step 9 push. No step needs a file a later step makes.

## UNMEASURED
All test totals (`Ran 35 tests`, `Ran 43 tests`), every RED set of a TEST class and of the six mutants MT1-MT6, whether the existing `test_build_has_no_warning` goes red on the 3 warning plants, the whole-file run time, the CI runner's python version, the bicep `snapshot` question, the 10 other CI python files' state at base, hosted CI and CodeQL (the kit lists the Python CodeQL rows for the gate).

## D-decisions
D1 expression strings plus a version-free shape for `AllowedHosts`; D2 literals = the four app-setting ones; D3 guards outside `ALL_CHECKS`; D4 module-call pin; D5 three red-proof layers; D6 no id in the file; D7 do not touch `:69`. Each is written in the kit as Tuesday's choice as coordinator; none is put in the product owner's mouth.

## Outside-the-fences disclosure
Read: the commission, `DRAFTER_RULES.md`, the template kit B1775, the sweep file (JOB 2 rows only), the project `CLAUDE.md`, `model-routing.md` rows C2 and C8 (one grep), `models_latest.json` (one grep), `brief_seat.sh` (grep), `GATE-VERIFIER-STANDARD.md` line 31, `stamp_check.py` header (first 45 lines). Listed `.tools/` of the project (names only; it showed old build folders) and one `find` of the home folder at depth 3 for bicep files. Did not open `decision_queue`, `.local/`, `Source_Documents/`, `fleet/briefs_staged/`, the ledger, any HPSM or other client file. Wrote only: the kit, its sidecar, this report, and the scratch folder `fleet/state/s299/d1791/`. Used `tmux list-panes` read-only. No git write, no Jira write, no `az`, no mail, no Artifact or Docs tool. Never printed a credential; the `.env` was read in-process by `jget.py` for names `JIRA_*` only. One `Read` of the sweep file used offset and limit; one earlier bash listing was too long (260 `.tools` folder names) and was my own mistake, not a policy breach.
