STARTABLE: YES

# B2135 drafter report: ADDENDUM-1 to B2133 (seat N181's CodeQL stop)

## BLUF
Addendum `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2133_ADDENDUM-1_k8-file-system-race.md` (94 lines, sha256 `f8ffff1e9bec8debfb99a0671b4edc265d0eae2378b27a616d1a34ddf03c3fa8`, sidecar `.measured` 73 of 73, `stamp_check.py` rc 0). Shape: a new commit E after K, one path (the RD-745 test file), `1 1` numstat, no cell added so K stays valid.

**Tuesday's default fix did NOT pass CodeQL; the fix shipped is different.** The file-descriptor read (openSync, fstatSync, closeSync in a finally) was built and run through the same tool: rc 1, the same alert (`fp=791124dbb925fcd7:1`, HIGH+ 7.7) moved from line 202 to line 207, its related location now the `openSync` line (the tool counts `openSync` as the check). Proved instead: the unchanged assertion `expect(fs.lstatSync(store).nlink).toBe(2);` moved from before the try to after the two reads inside it (line 196 to line 203, one line moved). **CodeQL on that fix: MEASURED, rc 0, `results head 29 base 29`, KEPT 0, NEW 0** (scratch git repository, base = BASE tarball tree, head = BASE plus four hunks plus four new files with the re-frozen file plus the turned RD-838 file). Control that can fail: the OLD file in the same scratch repo read rc 1 with the seat's own fingerprint and line (202:20).

## Facts re-measured (instrument)
- Frozen artefacts (folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s332/d2135/frozen/`, sha256 by `shasum -a 256`): re-frozen rd745 file `f3dc1338c54996af55b2283c03dba3c6946f2cc990de5bfd21a711054284708c` (blob `e45efcb650034fa5f45cbf4cef399830451fd6d4`, 13125 bytes, 285 lines, 14 cells by `^[[:space:]]+test\(`); `static2133e.py` `f9783525a4e5df57376e3eb533eb74307445b72003bc676fdf28b312e1a08560` (diff from the kit's: three hunks 2c2, 14a15, 16c17); `msg-E.txt` `3c776e762933ef72f5b2a30884dd552ac90e8d25ed6dc91c3fe0abf0685139b8`; `lane2133e.sh` `a72d7134be71bd748e183d0b287983080f7caa25269680db07e68bd147eda0d5`; `run2133e.sh` `438c58012bd9d297a8356769ccef9b447135f457b35cd21fa7e998bbd872b0a4`.
- Jest under the NexusAI lock (header read first; lock base listed no holder before or after; tags `d2135-lane-e`, two acquisitions, the first discarded because I pointed `FR` at the wrong folder and every judge read rc 2): RD-745 file 14 of 14 in the Linux and own shapes; six mutations judged on five files, 32 judge lines all rc 0; `745-inside-true` reddens K8 exactly; `745-inside-false` also reddens R8 of the RD-744 file; the equivalent mutant stays green. Reverted blob `6a88926cb35456368ec13986958cef25634701ef` each time. Load averages 4.77 3.92 3.65 at 04:21 (an earlier, concurrent CodeQL run had just ended).
- `static2133e.py E`: 15 OK lines, `STATIC E PASS`, controls fired; gitleaks no leaks, planted control found 2.
- Other cells (heuristic, read by program): same check-then-use shapes found in RD-744 lines 252 and 274 (stat then unlink) and RD-750 (exists then a later write); CodeQL flagged K8 only, nothing else changed.

## D-decisions
- D1: the fix differs from Tuesday's default (above); the addendum says so and why, with the three heads measured.
- D2: added two frozen helpers beyond the commission's list (`lane2133e.sh`, `run2133e.sh`) so the seat's one acquisition is a frozen script; the new folder for the seat is `.tools/b2133/frozen-e/` (the kit's `frozen/` holds the old rd745 file of the same name).
- D3: the seat's work folders for E are new (`logs-e`, `cq2`) so the first run's evidence stays.
- D4: HOLD 64 now reads three kit acquisitions plus one of the addendum.

## Questions for Tuesday (each with a default)
- Q1: shape E after K (default) versus a rebuild from C (holds lifted by name; repeats the lane, both whole-suite runs and CodeQL). Default: E.
- Q2: accept the changed fix (assertion moved after the reads, so K8 no longer asserts the two-name precondition BEFORE the purge; it asserts it after, and `linkSync` throws if the second name was not made). Alternative if you want a before-purge precondition: none passed the tool (descriptor variants read rc 1). Default: accept.
- Q3: the addendum has no Tuesday-clock for the HARD STOP slot or the STAMP slot (left `____`; you stamp).
- Q4: whether the seat's hosted-CI risk is acceptable: the same CodeQL rule runs on the hosted pull request; the local tool is an approximation (the scratch result and the seat's STEP CQ at E are the only proofs; the hosted result is UNMEASURED).

## UNMEASURED
The plain verify at E (predicted PASS 6588 / 415; no cell changes; the seat's K verify read PASS 6588/415, relayed), the verify leg of `run2133e.sh` (only `bash -n`), the real E commit and the seat's trees (the drafter's scratch trees are copies), real Linux, hosted CodeQL. The CodeQL scratch repo has a `.git` and a scratch base; the real run is the seat's.

## Outside-the-fences disclosure
Wrote only the addendum, its `.measured` sidecar, this report, and files under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s332/d2135/` (scratch repo `repo/`, trees `w/run` and `w/mut`, `cq/`, `logs/`, `cand/`, `frorig/` a copy of the kit's frozen folder, `frozen/`). Two jest-lock acquisitions (both released). Read-only reads of the NexusAI project (`.tools/b2133/wt` git log and rev-parse, cq1 outputs, STATUS tail, verify-plain.log). `git init`/`commit` ran only inside my scratch repo. No `gh`, no Jira, no card store, no mail. No alert dismissed or commented. `cd` never typed. Nothing deleted. A zsh hook refused one command (an unquoted `======` separator); a second was refused because a `$S` variable sat in a `git -C` write path; both re-issued with typed paths.

Drafting window: first `date` Fri 27 Nov 2026 04:17:07 AEDT; last `date` Fri 27 Nov 2026 04:26:17 AEDT.
