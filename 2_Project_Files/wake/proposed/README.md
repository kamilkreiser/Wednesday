# proposed/ — changes to shared files, as PROPOSALS ONLY

Nothing here has been applied. Every target is a file outside this lane; the build seat edited none of them.

| # | Target | Proposal file | Form |
|---|---|---|---|
| 1 | `Launch_Wednesday.command` | `01_launcher_boot_prompt.md` + `01_launcher_boot_prompt.diff` (made from `launcher_hunk_A.sh`, `launcher_hunk_B.sh` by `build_launcher_diff.py`) | unified diff, additive only |
| 2 | `CLAUDE.md` (tree root) | `02_root_CLAUDE_md.md` | exact old text and replacement |
| 3 | `0_Brain/CLAUDE.md` | `03_brain_CLAUDE_md.md` | exact old text and replacement |
| 4 | `2_Project_Files/doctor.sh` | `04_doctor_check.md` + `doctor_check_snippet.sh` | block to insert |
| 5 | `.gitignore` | `05_gitignore.md` | lines to append |
| 6 | `CLAUDE.md` session end | `06_wrap_step.md` | exact old text and replacement |
| 7 | `2_Project_Files/doctor.sh` | `07_doctor_pickup_warning.md` | exact old text and replacement (round 2) |
| 8 | `2_Project_Files/scheduler/nas_staleness.sh` | `08_nas_staleness.md` | one line (round 2) |
| 9 | `Launch_Wednesday.command` | `09_prompt_backtick.md` | one line. **ALL SEATS: needs Tuesday's and Friday's agreement; not part of this round's Wednesday-only change** |
| - | `CLAUDE.md`, `0_Brain/CLAUDE.md` | `FOR-KAM_lesson-load-ruling.md` | a question for Kam, not a change to apply: the "full lesson load STAYS" sentence |

## Order to apply (each step leaves a working boot)

1. **`.gitignore` (5)** first: the pack is a generated, untracked file; the rotation script refuses on a stray untracked file.
2. **First STATE block**: `2_Project_Files/wake/handover.sh seed --from-legacy` prints it from the legacy pickup's newest block plus the file's standing `## OWED` and `## STANDING` sections, and reports what it took by line number (dry; nothing written); the coordinator reads it, then either adds `--run` or edits the printed block and pipes it to `handover.sh write --stdin`, and commits `0_Brain/tasks/STATE-wednesday.md`. Until this exists the pack carries only the legacy pickup's newest block and says so.
3. **Launcher (1)**, claimed with Tuesday and Friday first (it is the shared launcher). From the next Wednesday launch the read list is the pack.
4. **Doctor (4 and 7)** together.
5. **Rules files and wrap step (2, 3, 6)** in one commit, so the rules files and the launcher never disagree again.
6. **NAS staleness (8)** once the state file has reached the NAS.

Not in this order, because they are not part of the Wednesday-only change: **proposal 9** (the backtick pair) changes all three seats' prompt text and needs Tuesday's and Friday's agreement; **`FOR-KAM_lesson-load-ruling.md`** is Kam's to rule. Proposals 4 and 7 change doctor's output on the other seats' machines in one respect each (stated in those files), so they are claimed with them like the launcher.

`NEXT-PICKUP.md` is not touched by any step: it simply stops growing. Folding it away is the coordinator's later step.

## Rollback of everything

`patch -R Launch_Wednesday.command < 2_Project_Files/wake/proposed/01_launcher_boot_prompt.diff`, then `git revert` the commits of steps 1, 4 and 5. The STATE files and the pack are inert without the launcher change: the legacy prompt names neither. No data moves in any step, so nothing needs restoring.

## Things the cut-over touches that are NOT proposed here (found while reading; the coordinator's call)

- (Now proposals 7, 8 and 9: doctor's stacked-pickup warning, the NAS staleness list, the backtick pair.)
- The 14 grant rows that lead with no seat name are the coordinator's to label in the grants file at cut-over; the pack keeps them until then. `out/WAKE-<seat>.dropped.txt` lists every row the pack left out, with the proof.
- The launcher's shared STANDING BEHAVIOUR text still says "write + push the handover block" without naming a tool. For the Wednesday seat the new step 2 names the tool; the shared sentence is left byte-identical for the other seats.
- Census A7's "which machine a seat is on" contradiction lives in Tuesday's and Friday's scope text ("WEDNESDAY on the Studio"). Those seats' text is not changed in this round, so it stands.
- The launcher's banner prints `Voice: Moira (en_IE)` for all three seats while `voice/speak.sh` prefers Matilda (Premium). Shared line, not changed.
