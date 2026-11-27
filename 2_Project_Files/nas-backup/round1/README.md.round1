# nas-backup: nightly, staggered, copy-only backup of a seat to the NAS (WED-170)

Authority: Kam, live board 2026-11-27 12:03:29 (verbatim in `BRIEF.md`). Built 2026-11-27 by the WED build seat "nas-backup". **Nothing here is armed.** `HOLD_<seat>` files make every real run refuse; no launchd job exists; nothing has been written to the NAS.

## The pieces

| File | What it is |
|---|---|
| `nas_backup.sh` | The backup. **Dry run by default**; a real run needs `--run`. Seat resolved through `fleet/cockpit/seat_resolve.sh` |
| `nas_backup_nightly.sh` | What the scheduler calls. Runs when there is no good backup since the window opened; skips, with a logged reason, otherwise |
| `nas_backup_watch.sh` | The three-day check. Reads only the state file and the clock |
| `nb_core.py` | The engine behind all three (Python 3.9+, standard library). `nb_common.sh`: seat and python lookup |
| `seats/<seat>.conf` | Sources, schedule and added exclusions. `wednesday.conf` is confirmed; `tuesday.conf` and `friday.conf` are placeholders the tool refuses |
| `jobs/nasbackup.plist.template` | The launchd template. Kept OUT of `scheduler/jobs/` on purpose: the installer installs every template it finds there |
| `HOLD_wednesday`, `HOLD_tuesday`, `HOLD_friday` | While present, `--run` exits 3 |
| `proposed/` | Lines for `install_all_jobs.sh`, `doctor.sh`, `PORTABILITY.md`, the launcher (each with a rollback), and the instructions for the other seats |
| `tests/run.sh`, `tests/mutants.sh` | 167 checks on a fake NAS; 20 deliberate breakages the checks must catch |
| `state/`, `logs/`, `manifests/` | Run state on the drive, git-ignored. `state/<seat>.json` is the one file the catch-up and the flag read |

## Where the copy goes

```
/Volumes/DEV-Working/<Client>/<Seat>/nightly-backup/
    current/<set>/...            the latest copy
    versions/<run stamp>/<set>/  the PREVIOUS copy of every file that run replaced
    manifests/                   one manifest per run, and the symlink lists
    runs/                        RUN_<stamp>_STARTED.txt, and _COMPLETE.txt only when the run was counted good
    _tmp_incoming/               the engine's temp files (a killed run leaves them here, not scattered)
```
Wednesday writes to `Secuura/Wednesday/` and `General/Wednesday/`; Tuesday to `Datasec/Tuesday/`. The client list per seat is hard-coded in `nb_core.py` (`SEATS`); a configuration cannot add to it.

## How one run works

1. **Refusals first.** Unknown or disagreeing seat; `HOLD_<seat>`; source drive not a local mount, or a source not on it; NAS not in the mount table as `smbfs`; the client folder absent or spelled in a different case (real names from `os.listdir`); free space under 200 GiB; rsync not version 3; outside the window without `--out-of-sequence <card id>`; another run holding the lock. A stale lock is reported and left; `--clear-stale-lock` moves it into `state/_quarantine_<date>/`.
2. **List the source** under the exclusion rules (one implementation, in Python). Refuse a set above `max_files`.
3. **List the destination.** Decide per file: copy if it is absent, or its size differs, or the source's own (size, mtime, ctime) differs from the local index and the sha256 differs.
4. **Copy** exactly that list: `rsync -t -O -I --from0 --files-from=<list> --backup --backup-dir=<versions/stamp> --temp-dir=<_tmp_incoming>`. The argv is checked for deletion-capable flags before every call.
5. **Read the engine's log**: any `deleting` line fails the run (exit 9); any secret-shaped name in it fails the run.
6. **Observe the destination** for every file that was sent. A source file that is neither there with the same size nor proven changed or vanished at the source during the run fails the run. A sha256 sample (40 files per set) must agree.
7. **Write the manifest** (per top-level folder: files and bytes on both sides, destination-only files kept, exclusions, symlinks, case collisions) on the drive and on the NAS, the COMPLETE marker, and the state file.

## Design choices, one line each

- **Engine: Homebrew rsync 3 as transport only, with `--backup --backup-dir=versions/<stamp>`.** It is already a dependency of this project, writes each file under a temp name and renames it, and moves a replaced file aside instead of overwriting it; there is no mode in the argv that removes anything.
- **The decision "has this file changed" is made here, not by rsync.** The NAS does not keep the file times rsync sets (measured on the Backup share: all 128,421 files re-sent nightly), so size-plus-time would copy, and version, everything every night.
- **A local index (`state/<seat>.index.sqlite`) is a cache, not a record.** Lose it and the next run compares the overlap by sha256 once; correctness never rests on it.
- **One fixed folder with dated versions inside, not a dated folder per night.** The 2026-11-11 convention is `<Client>/<Seat>/<date>_<topic>/`; a nightly copy in that shape would duplicate 68 GiB a night. The dates Kam asked for (so things can be cleaned up) are on `versions/<stamp>/` and the manifests.
- **Nothing is ever pruned.** `versions/` grows by what changed each night; clean-up is Kam's word (2026-11-11 lesson, rule 5).
- **`.git` is excluded**, as in the existing leg: a live object store copied file by file is not a repository. Unpushed commits are therefore NOT in the backup; this is said in the census, the PORTABILITY text and STATUS.
- **Symlinks are recorded, not created**, so a run cannot fail on what the share supports, and a link can never pull in a file from outside the scope.
- **Names that differ only in case are left out, both of them, and named at every run.** The drive is case-sensitive and the NAS is not. Blocking would have meant no Secuura backup at all (five such pairs exist today).
- **"Good" means counted, not exit 0.** rsync's exit 23 or 24 (a listed file went away mid-run) is neither trusted nor fatal: every listed file is accounted for one by one afterwards.
- **A backup is "as of the start of the run".** A file that changes while the run is going is counted as such and copied again the next night, so the busiest files do not fail every run.
- **Four fires per window; the script allows one backup per window.** A late wake or a late NAS still gets its run that night; a second fire is a logged skip.
- **Outside the window the nightly script does not run (`late_fire=refuse`)**, the stricter reading; `late_fire=run` in the seat's conf is the other reading, one line.
- **The three-day check is a separate script** called from the launcher, doctor and the nightly job, and its clock starts at arming (`--mark-armed`), so a job that never fires is still flagged.
- **The card command is printed, once per gap, and never run by the tool.** Later checks print one reminder line and keep exiting 3 until `--mark-raised` is recorded.
- **Three independent holds for arming:** the `HOLD_<seat>` file, the template living outside `scheduler/jobs/`, and `status=` in the seat conf. Any one of them alone gets undone by a well-meaning successor (2026-08-26 lesson, recurrence).
- **A released lock is moved, not removed** (`state/released_locks/`): no delete verb anywhere in this lane.
- **A whole-run watchdog** (cap plus 15 minutes) stops a run blocked in a system call, which is what a macOS privacy prompt on a network volume looks like from inside.

## Commands

```
bash nas_backup.sh                         dry run (reads both sides, writes nothing to the NAS)
bash nas_backup.sh --scan                  what is in scope, per set (reads the drive only)
bash nas_backup.sh --run                   real run, inside the window, hold lifted
bash nas_backup.sh --run --out-of-sequence <card id>     real run outside the window, on Kam's approval
bash nas_backup_nightly.sh --decide-only   what tonight's fire would decide
bash nas_backup_watch.sh                   one status line; exit 3 when overdue
bash tests/run.sh [/private/tmp/dir]       the suite, fake NAS only
bash tests/mutants.sh [/private/tmp/dir]   prove the suite can fail
```
Exit codes of `nas_backup.sh`: 0 good or dry run done · 2 refused · 3 held · 4 run-time cap · 5 engine error · 6 locked · 7 stalled · 8 not counted equal · 9 a deleting line in the engine's log.
