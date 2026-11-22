STARTABLE: YES

# B1917 DRAFTER REPORT: lane T (owed items 47 and 48), seat Datasec/OXPd2-X31, kit `2026-11-22_B1917_SEAT-X31_oxpd2-t-held-test-cells.md`

Drafter: Opus, in-session, read-only toward OXPd_2, Jira and GitHub. Drafted 2026-11-22 20:15 to 20:35 AEDT (the clock reads are in the sidecar's first entry).

## BLUF
- **The W02 cell's full text IS held whole.** It is the third-round kit's `2-w02-body.diff`: +64 -0, sha256 `ca79627a…48330`. Three copies are byte-equal: `fleet/state/s306/d1872/new/`, `…/d1872/gate/` and `<project>/.tools/b1872/gate/`. They also match the sha that the B1872 kit printed. The diff's `index a849adf..` line is exactly the blob of `ReceiverTests.cs` on main `bf6b441e`. The kit freezes it byte for byte as `1-w02-body.diff`.
- **The K8 row is new text** that I wrote (+22 -0, one file). It walks every client model that has an optional root property, sends that property as null, and asserts the answer is refused `WrongType` at `$.<name>`. It asserts the count is above 0 and adds no test case.
- **Red first, by mutant, is proved for both cells. A survivor control shows that only the new cells kill each mutant:**
  - `mReasonDisposed` turns the W02 `ObjectDisposedException` row red (Jobs 122/1 failed, `Expected: JobNotFound`, `Actual:   ScanRefused`). With main's tests it stays green (Jobs 120/0).
  - `mNullStrictToo` turns K8 red (Contracts 148/1 failed). With main's tests it stays green (148/0). This mutant edits the generated `Oxpd2Json.cs:431` and the generator `Oxpd2RuntimeText.cs:808` the same way, because the Contracts test project compiles the generator.
- Whole solution at green: 1580 total, 0 failed, 1576 succeeded, 4 skipped (main 1578 + 2). Exactly two files change. No `src/` or `contracts/` change, no lock or project file, no slnx line.
- `stamp_check.py <kit>` exits 0: 131 claims, all 131 measured.

## Facts re-measured (instrument; control)
| Fact | Instrument | Result | Control |
|---|---|---|---|
| origin main | `gh api -X GET …/git/ref/heads/main` 20:18:48 | `bf6b441e…`, 0 open PRs, 19 branches (incl. `b1912/f13-test-race`), no `b1917*` | `.private true`, `.permissions.push true` |
| held W02 diff | `shasum -a 256` on all 3 copies | all `ca79627a…` | the B1872 kit's THE TOOLS line holds the same sha |
| W02/K8 absent on main | `git grep -c -F` at bf6b441e | `W02_a_body_whose_read_throws` 0, `ThrowingBody` 0, `did not refuse an optional null` 0 | `W02_a_wipe_during` 1; `did not refuse an unlisted value` 1 |
| patches apply byte for byte | `git apply` in a 2nd fresh clone, then `cmp` | rc 0, cmp 0 for both files | a second `apply --check` rc 1 |
| green | heavy.py, test executables whole | Jobs `Total: 122 … Failed: 0`, Contracts `Total: 148 … Failed: 0` | `[FAIL]` count 0 in the green Jobs log |
| red | the same, under each mutant | 1 `[FAIL]` each, the expected cell | survivor runs at main's tests: green |
| mutant undo | proto.py sha compare; `git diff --quiet -- src contracts` | `sha equal True` x4; rc 0 | none |
| chain (partial) | unittest; repo_rules without `--source-documents`; gitleaks | `Ran 111` OK; `RULES: clean (500 files)` rc 0; `no leaks found` rc 0 | gitleaks plant rc 1 (my first, low-entropy plant gave rc 0 and was discarded as a control; the kit warns about this) |
| words | `words.py` | `WORDS: clean` over the added lines (86) and the message; the control fired 13 of 13 | `3-mutants.txt` gives 1 hit (its B-number, never committed) |
| cells | `grep -c -E` indented and column-1 | Theory 5→6, InlineData 16→18, Fact unchanged; column 1 count 0 | none |
| toolchain | `--version` | dotnet 10.0.404, gitleaks 8.30.1 | none |
| ports / panes | `tmux list-panes -a` 20:29 | no OXPd2 pane, no X31; this lane uses no port | `Datasec/NexusAI-N162` pane seen |

Evidence: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1917/logs/` (`proto.out`, the per-job logs, `rules.log`, `unittest.log`, `gate.log`). Programs: `…/d1917/tools/proto.py` and `fill.py`.

## D-decisions (all the coordinator's defaults; none is the product owner's)
D1: the K8 row covers every client model (Q1). D2: W02 is frozen from the held diff. D3: the mutant edits both the generated file and the generator. D4: one commit for both cells. D5: the K8 count goes out as a diagnostic message only.

## Q-questions for Tuesday (each with a default)
- **Q1 (STOP-class, S4 in words):** the K8 row over every client model (default) or over the first one only. The first-only form is about 8 lines shorter (DERIVED, not built). It kills the mutant the same way.
- Q2: one commit (default) or a T1/T2 split.
- Q3: the held W02 text byte for byte (default).
- Q4: Opus, by project CLAUDE.md:7 (default).
- Q5: READY within 120 min, push within 90, pane `Datasec/OXPd2-X31`, gate G2 on Opus (default).
- The commission asked which of the W02 forms applies: it is held whole, so the kit freezes it rather than specifying new text.

## UNMEASURED / NOT RUN by the drafter
- Both `dotnet publish` runs and `release_guard.py`. The GUARD counts 10 and 11 are RELAYED from B1912 at the same main.
- The locked restore with `--force` and its lock-file compare.
- `run_step.py`'s neutral-object scan. Its wordings are re-counted from B1912's saved `hosted-base.txt`.
- `clone.py seat`, any commit, push or hosted run. `hosted2.py` was not run by me; BASE's FAIL-on-F13 is RELAYED from B1912.
- The K8 count (716 is RELAYED from the B1885 reader's G05 probe; my row does not print it to the console).
- The U+200B plant control of check 6(b).

## Risks the kit handles
- F13 can still race on the linux leg until seat X27 lands. The kit records a local F13 red and reruns the solution once. A second local red, or a hosted F13 red, is `STOPPED: NEEDS TUESDAY`, never a rerun.
- If X27 lands first, the expected total becomes 1581 under the rebase rule. The partition is disjoint (B1913: 0 overlaps).
- My prototype heavy jobs waited up to 103 s on the shared lock at load1 up to 11.8.

## Outside-the-fences disclosure
- I wrote only inside my scratch folder `fleet/state/s310/d1917/` and wrote the kit, its sidecar and this report. There is also one `.measured.tmp` file, replaced in place by `os.replace`.
- **Project reads (read-only):** `BACKLOG.md` lines 304-325, `CLAUDE.md` single lines, `CLARIFICATIONS.md` lines 682-690, and `.tools/b1872/gate/2-w02-body.diff` (sha only, plus the `ls` of `.tools`).
- **Git:** `git clone` from B1912's scratch clone (inside TUESDAY) into my scratch, and git read verbs. Write verbs ran only in my scratch clones. Push URL `invalid://no-push`.
- **GitHub:** `gh api -X GET` only (main ref, open PRs, repo flags, branches).
- **Heavy lock:** 15 jobs through the unchanged `heavy.py` and the wave lock, one at a time. I broke no lock. The lock folder held by another lane at 20:29 was left alone.
- **Never touched:** Jira, `Source_Documents/`, any key folder, any other lane's files or X27's files. No message to anyone. Nothing deleted: the two gitleaks control folders were moved to `d1917/_quarantine/ctl/`.
- **Card ids:** none used.
