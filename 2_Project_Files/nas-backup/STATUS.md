READY FOR QA

Build seat "nas-backup" (WED-170), Fable 5.2. Nothing is armed, nothing was installed, nothing was written to the NAS, no existing file was edited. Full detail: `CENSUS.md` (facts with their instrument), `README.md` (design and the reason for each choice), `evidence/` (test, mutant, scan and dry-run output).

## Two things the coordinator should read before anything else

1. **Secrets are on the NAS already, put there by the job that is armed today.** `/Volumes/Backup/DevMASTER-mirror/!CODING/Secuura/Blockchain/4_Credentials` (23 entries) and `.../3_Access_Keys` (6 entries) exist on the Backup share. `scheduler/nas_push.sh` excludes neither name. I read existence and entry counts only, opened nothing, and touched nothing. This is workspace hard rule 3, and what happens next is Kam's.
2. **That same job (`com.wednesday.naspush`, 03:30) has not completed a run on this Mac.** STALLED on 11-12 and 11-13, then stopped by its 4-hour cap on all 13 nights from 11-14 to 11-26. It re-sends the same 128,000 files every night because the share does not keep the file times rsync sets. The mirror's `WEDNESDAY` folder is empty.

## Census headline

- **Exists:** `tools/nas_offload.sh` (by hand, dated offloads to DEV-Working); `scheduler/nas_sync.sh` (two-way unison, can delete); `scheduler/nas_push.sh` (one-way rsync, whole drive to the Backup share); `nas_staleness.sh`, `nas_sync_lib.sh`; doctor's NAS checks.
- **Held, and by whose word:** `nassync`, both seats. `NASSYNC_HOLD_wednesday`: "Re-arm ONLY on Kam's word" (2026-10-04, card `wed-nassync-rearm-shape-1004`). `NASSYNC_HOLD_tuesday`: "Lift: Kam's word only" (2026-10-16); `com.tuesday.nassync => disabled` on this Mac. PORTABILITY 20: "The NAS leg stays OFF until the case is fixed (Kam's card `nas-case-fold-datasec`)." This build does not re-arm it and does not use its engine.
- **Armed:** `naspush`, on Kam's cards `wed-nassync-rearm-shape-1004` = a and `wed-nightly-nas-mirror-old-nas-1111` = a. See the two points above.
- **The NAS:** `/Volumes/DEV-Working` is smbfs, 10.79 TiB free, top-level names `#recycle .DS_Store Datasec Friday General Personal Projects Secuura`. It is NOT case-sensitive (found without writing: `pathconf` and a read-only stat of the case-flipped names). The drive IS case-sensitive.
- **Recommendation: build beside, not extend.** New share, new folders, new label, own lock, state and hold. After its first good run, one card for Kam: hold `naspush`, and decide about the mirror and the secrets on it.
- **Scope:** as first written the backup was 8.9 million files (6,425,033 in the seat tree outside `reference/`, 2,464,442 in the Secuura folder). Narrowed in `seats/wednesday.conf` to **1,012,113 files, 67.83 GiB**. Every exclusion is listed with its measured size in the conf and in CENSUS section D.

## What I built (bytes)

| File | Size | What |
|---|---|---|
| `nas_backup.sh` | 2,695 | The backup. Dry run by default; `--run` for real. Seat via `fleet/cockpit/seat_resolve.sh`, plus two stricter checks |
| `nas_backup_nightly.sh` | 1,879 | What the scheduler calls: catch-up, skip-if-running, never outside the window |
| `nas_backup_watch.sh` | 2,263 | The three-day check; prints the one card command, never runs it |
| `nb_core.py` | 87,320 | The engine (Python 3.9+, standard library only) |
| `nb_common.sh` | 2,646 | Seat and python lookup, sourced by the three scripts |
| `seats/wednesday.conf` | 6,441 | Confirmed: 14 sets, schedule, exclusions |
| `seats/tuesday.conf`, `seats/friday.conf` | 1,111 / 986 | Placeholders, `status=unconfirmed`: the tool refuses them |
| `jobs/nasbackup.plist.template` | 2,689 | launchd template, four fire times per seat. Deliberately NOT in `scheduler/jobs/` |
| `HOLD_wednesday`, `HOLD_tuesday`, `HOLD_friday` | 474 / 468 / 465 | While present, `--run` exits 3 |
| `proposed/install_all_jobs.proposed.md` | 4,367 | Lines, each with a rollback |
| `proposed/doctor.proposed.md` | 3,527 | |
| `proposed/PORTABILITY.proposed.md` | 3,223 | |
| `proposed/launcher.proposed.md` | 2,116 | |
| `proposed/INSTRUCTIONS-for-other-seats.md` | 6,237 | Steps for Tuesday and Friday, what must be true first, how to prove the first run |
| `tests/run.sh` | 32,962 | 167 checks on a fake NAS |
| `tests/mutants.sh` | 7,017 | 20 deliberate breakages the suite must catch |
| `CENSUS.md`, `README.md` | 20,316 / 8,261 | |
| `.gitignore` | 143 | `state/ logs/ manifests/ __pycache__/` |
| `evidence/` | 124 KB | Outputs named below |

Engine in one sentence: the tool lists both sides itself, decides what changed (absent, size differs, or the source's own stat changed AND the sha256 differs), and hands rsync 3 an explicit list with `--backup --backup-dir=versions/<stamp>`, so a changed file's previous copy is kept and nothing is removed. It does not rely on file times on the NAS, because this NAS does not keep them.

Destination: `/Volumes/DEV-Working/<Client>/<Seat>/nightly-backup/{current,versions,manifests,runs}`. Wednesday: `Secuura/Wednesday/` and `General/Wednesday/`. The client list per seat is hard-coded; a conf cannot add to it.

## Tests

`bash tests/run.sh <dir under /private/tmp>`: fake NAS and fake source in the session scratchpad, never the real NAS (test mode is refused for any path outside `/private/tmp`).

```
T10 the oldest python on the target machines (/usr/bin/python3)
  PASS  T10 a real run under Python 3.9.6: exit 0 (= 0)
  PASS  T10 GOOD

T11 names that differ only in case: neither is copied, both are named (the scratch volume cannot hold such a pair, so the listing is supplied)
  PASS  T11 the planner ran (= 0)
  PASS  T11 only the non-colliding file is planned for copy
  PASS  T11 a folder pair that collides is not created; the clean folder is
  PASS  T11 four files under four colliding names are counted as not backed up, and it is not a failure

=== 167 passed, 0 failed
```
Full output: `evidence/tests_run_final.txt`. `grep -c '  PASS  '` is 167 and `grep -c '  FAIL  '` is 0 on it.

Covered: dry is the default and writes nothing (T1); a real run copies and counts both sides (T2); a changed file keeps its previous version, including a same-size change; a file removed at the source stays at the destination; a lost index re-copies nothing (T3); secrets, `.git`, `node_modules`, quarantine, `pgdata-*` and another seat's folder do not arrive while the ordinary file beside them does (T4); every refusal with its must-succeed neighbour: NAS not mounted, a local folder at the NAS path, client folder absent, top-level and seat-level names differing in case, free space, live lock, stale lock (reported, left, then moved by `--clear-stale-lock`), source not the seat's drive, another client's folder as destination and as source, seat disagreement, unknown tree, outside the window, hold file, unconfirmed conf, deletion-capable flags, a set over the file ceiling, an unlisted project folder (T5); a planted `*deleting` line fails the run at exit 9 although the engine exited 0; stall and cap (T6); catch-up with the clock supplied: first night, second fire the same night, missed one night, outside the window, a run in progress (T7); missed three nights: the card command appears exactly once per gap, and once again for a new gap (T8); the watch flags a job that was armed and never fired once, works with the NAS away, and stays quiet while held (T9).

**Each test shown able to fail.** `bash tests/mutants.sh`: copies the lane to scratch, breaks one property in the copy, runs the suite on it.
```
  CONTROL   the unmutated copy: exit 0 — === 167 passed, 0 failed
=== 20 mutants caught, 0 survived or broken
```
The first pass caught 18 of 20 (`evidence/mutants_first_pass_2_survivors.txt`). Both survivors were mutants that removed one of two guards: rsync 3 treats `--backup-dir` as implying `--backup`, and the allow-list is checked twice. The script now removes both guards for those two. Inside the suite, the additive and secret checks are also re-run against sabotaged engines ("CAN-FAIL" lines).

## The one real dry run (reads only), 12:59:26 to 13:06:28

`bash nas_backup.sh --dry`, exit 0. Output: `evidence/real_dry_run_2026-11-27.out`.

| | Files | Bytes |
|---|---|---|
| WEDNESDAY tree to `General/Wednesday` | 265,195 | 26.67 GiB |
| Secuura folder to `Secuura/Wednesday` | 587,085 | 30.95 GiB |
| Testing Agent MAIN | 151,723 | 9.38 GiB |
| Eleven smaller general projects | 8,110 | 0.82 GiB |
| **Would copy (everything is new: the destination does not exist)** | **1,012,113** | **67.83 GiB** |

Also in it: 982 symlinks recorded, not copied; 7,085 entries excluded; 14 files left out because 14 names differ only in case from a sibling; the engine's dry list agreed with the plan for all 14 sets; 0 deleting lines; no PROBLEM line.

NAS unchanged: top-level and own-client folder names, their mtimes, and `df` used blocks (117175864) are identical before and after (`evidence/nas_before_and_after_dry_run.txt`).

**Estimated duration.** I could not measure write speed read-only. The nearest measurement is the armed leg's own logs to the same NAS box: 8.9 files a second, three nights running. At that rate the first copy takes **about 32 hours**. That is an extrapolation from another job on another share, and that job also renames a previous copy for every file, which a first copy does not, so it may be up to twice as fast. After the first copy, a night's run lists about a million destination files at the 390 entries a second I measured (**about 43 minutes**) and copies only what changed.

## Proposed times, and collisions

| Seat | Fires | Window |
|---|---|---|
| Wednesday | 00:30, 01:40, 02:50, 04:00 | 00:30 to 05:30 |
| Tuesday | 02:30, 03:20, 04:10, 05:00 | 02:30 to 05:30 |
| Friday | 04:30, 05:40, 06:50, 08:10 | 04:30 to 09:30 |

No same-minute collision with any job found (01:15, 03:30, 05:30, 06:00, 06:45, 15:00, 23:00, 23:30, Monday 08:00). The known 23:00 collision on Tuesday's seat is untouched. Two overlaps on this Mac that are not collisions: `stalescreen` at 01:15 (model box, not the NAS), and `naspush` from 03:30 to 07:30 (same disk, same NAS box, different share). Later fires are not hourly at minute 30 because Wednesday's would land on 03:30 and Tuesday's on 05:30.

## Deviations, each with its reason

1. **The engine decides what changed; rsync only carries an explicit list.** The brief's example (`rsync --backup --backup-dir`) is kept, but plain rsync decides by size and time, and this NAS loses the time. On it that design re-copies and re-versions every file every night.
2. **One fixed `nightly-backup/` folder with dated `versions/` inside**, not a dated folder per night as the 2026-11-11 convention reads. A dated folder per night would add 68 GiB a night.
3. **More was excluded than the brief lists**: nine paths of caches, model weights and work clones in the seat tree, and eleven folder names plus one path inside the Secuura set. Without them the job is 8.9 million files. Precedent: Kam's `narrow-hard` ruling of 2026-09-11. All listed for him below.
4. **Four fire times in the template, not one.** One fire a night cannot serve "the NAS was away at 00:30".
5. **Three shell scripts over one Python engine** rather than three standalone shell scripts: the target Macs ship bash 3.2, and the counting, JSON state and clock logic are testable in Python and not in that shell.
6. **Names differing only in case are left out and reported, not refused.** A refusal would block the whole Secuura set.
7. **Symlinks are recorded in the manifest, not created on the NAS.**
8. **The watch says HELD and raises no card while `HOLD_<seat>` exists.** Otherwise a held, never-armed seat would raise a card after three days.
9. **I ran `nas_backup.sh --run` once in the real lane, to prove the hold.** It refused at exit 3 before touching the NAS. It left one `refused` record in `state/wednesday.json`.
10. **Friday's allow-list is `General` only**, a placeholder (question 5).
11. **`max_files` raised to 700,000 for this seat** (default 400,000): the Secuura set is 587,085 files, most of it session evidence.

## What I did NOT test

- **Any write to the real NAS.** So: whether DEV-Working accepts the engine's temp-folder rename and the move into `versions/`; whether it keeps file times; long paths and names SMB dislikes; Unicode names as the share returns them. The first real run is the first test of all of these.
- **Anything under launchd.** The job was never loaded. Expect a macOS privacy prompt for `python3` as well as `rsync` on the first scheduled run (PORTABILITY 15a is the rsync one).
- **The whole-run watchdog** (cap plus 15 minutes). The engine stall and cap were tested with stub engines only.
- **A signal or a reboot in the middle of a run.** The stale-lock path was tested with a dead process id, not a real interruption.
- **Scale beyond the dry run.** The whole dry run over a million files took 421 s. The real run's step of checking each sent file at the destination (a million stats over SMB), the index at a million rows, and memory use were not exercised.
- **A real case collision on disk.** The scratch volume folds case, so T11 supplies the listing.
- **The proposed lines** for doctor, the launcher and the installer: written, not run.
- **Tuesday's and Friday's configurations**: placeholders. Nothing was run for those seats.
- **`late_fire=run`**: its decision only, not a run. **Daylight-saving changeover** in the window arithmetic: not tested.
- **The 32-hour estimate**: an extrapolation, not a measurement.
- **Content isolation.** Exclusion is by NAME. A file in the Wednesday tree that mentions Datasec and is not named for it (a brief, a chat log, a ticket export) travels to `General/Wednesday/`.
- `0_Brain/reference` was not re-measured (279 GB and 5.9 million files is Wednesday's figure).

Housekeeping: the dry run left 240 MB in `logs/wednesday/` (the million-line file lists). A night's real run logs only what changed. Nothing in this lane prunes logs.

## QUESTIONS

The round is not blocked. These are for the coordinator and Kam before arming; where the brief contradicted itself I took the stricter reading.

1. **The brief contradicts itself on a late fire.** It says "a fire after a sleep still runs" and also "It never runs outside its window on its own". Stricter reading taken: a fire outside the window is logged and skipped, and the missed night is caught up when the next window opens. A fire after a sleep that lands inside the window does run (the windows are 3 to 5 hours and launchd fires once on wake). The other reading is one line: `late_fire=run` in the seat's conf.
2. **`0_Brain/reference`: in or out?** Out for now, as the brief asked. 279 GB and 5.9 million files. In would make the file count about seven times what it is now.
3. **Is the narrowing right?** Out: `local-model/spark/cache` (237.66 GiB), `local-model/spark-ab/work` (141.98 GiB), `tools/omlx/models` (198.18 GiB), `local-model/runs` (20.18 GiB), smaller caches; in Secuura, folders named `wt`, `quarantine*`, `*node_modules*`, `clone`, `deploy-clones`, the per-seat temp folders, `Blockchain/scratchpad`. Kept in: Secuura's session evidence (most of its 587,085 files), `fleet/qa-agent/gatesets` (193,238 files), `Testing Agent MAIN` (151,723 files). Each can be flipped by one line.
4. **The armed `naspush` job and the secrets on the Backup share** (top of this file). Not mine to act on. Suggested: one card to Kam now for the secrets, and after the new job's first good run, hold `naspush`.
5. **Friday.** Two rulings are missing: which client folder or folders Friday writes to (it works both clients), and whether the laptop may carry a scheduled job at all (Kam's 2026-09-23 ruling says none; his 2026-11-27 instruction says each agent).
6. **The first copy is about 32 hours, far outside a night.** It needs Kam's approval as an out-of-sequence run with a raised cap (`--run --out-of-sequence <card id> --max-seconds <n>`), or the scope cut further. Run night by night under the 5-hour cap instead, it would report "stopped by the cap" for several nights and raise the three-day flag.
7. **`.git` is excluded, so commits not yet pushed are not in the backup.** Accept that, or add a per-repository `git bundle` step in a later round?

## For the checker: where to look first

- The safety claims: header of `nb_core.py`; `SEATS`, `EXCLUDES`, `FORBIDDEN_RSYNC` near its top; `preflight()`, `plan_set()`, `cmd_backup()`.
- Re-run: `bash tests/run.sh /private/tmp/<dir>` then `bash tests/mutants.sh /private/tmp/<dir>`; then `bash nas_backup.sh --dry` (seven minutes, reads only).
- Not armed: `ls HOLD_*`; `launchctl list | grep -i -c nasbackup` is 0 (positive control: `naspush` counts 1); `ls scheduler/jobs | grep -i -c nasbackup` should be 0.

---
Last updated by the build seat: 2026-11-27 13:20:34 AEDT. Stopped at READY FOR QA.
