# PROPOSED change for arming the schedule (round 2). Nothing here is applied.

Arming is Wednesday's, on Kam's word, after a GO from QA. It is **ONE change, applied once for all seats, by Wednesday**. No other seat edits the shared installer (QA minor: round 1 told Tuesday and Friday to apply the edits themselves).

## Why the order no longer matters (QA finding 11)

Round 1's template carried eight placeholders that only an edited installer rendered, and the hold lived only in the installer edit. Copy the template first and the unedited installer walked past the hold and loaded a broken plist.

Round 2 removes both dependencies:

1. **The template uses only the three placeholders the installer already renders** (`PROJECT_DIR`, `SEAT`, `HOME`). An unedited installer writes a valid plist from it. Tested: `tests/run.sh` T20 renders it with the installer's own five `sed` expressions, `plutil -lint` passes, no placeholder is left.
2. **The schedule is not in the template.** It fires at minute 30 of every hour. `nas_backup_nightly.sh` reads the seat's window from `seats/<seat>.conf` and does nothing outside it but log one line.
3. **The hold is enforced by the script launchd calls**, not by the installer. Under `HOLD_<seat>` the nightly script exits 3 and writes one line to `logs/<seat>/nightly.log` (T20). A seat with no confirmed scope (Tuesday, Friday today) is refused by the engine itself (T14).

So whichever file lands first, a held or unconfirmed seat copies nothing.

## The one change

Apply together, in one commit, from the WEDNESDAY tree:

**(a) the template**
```
cp -n "2_Project_Files/nas-backup/jobs/nasbackup.plist.template" "2_Project_Files/scheduler/jobs/nasbackup.plist.template"
```

**(b) two lines in `scheduler/install_all_jobs.sh`**, beside the existing `nassync` hold line (line 94). They are tidiness, not safety: without them a held or unconfirmed seat gets a loaded job that refuses every hour.
```
  # nasbackup (WED-170, Kam 2026-11-27): the copy-only nightly backup. Held per seat by nas-backup/HOLD_<seat>; only seats with a confirmed scope file get the job.
  if [ "$job" = "nasbackup" ] && [ -e "$PROJECT_DIR/2_Project_Files/nas-backup/HOLD_$SEAT" ]; then echo "skip $job — HELD (2_Project_Files/nas-backup/HOLD_$SEAT)"; continue; fi
  if [ "$job" = "nasbackup" ] && ! /usr/bin/grep -q '^status=confirmed$' "$PROJECT_DIR/2_Project_Files/nas-backup/seats/$SEAT.conf" 2>/dev/null; then echo "skip $job — no confirmed nas-backup/seats/$SEAT.conf"; continue; fi
```
(The one `2>/dev/null` hides only grep's "no such file" for a seat that has no conf; the `echo` beside it says the same thing in words.)

**(c) the doctor block** (`proposed/doctor.proposed.md`): one sourced line.

Rollback of the whole change: `launchctl bootout gui/$(id -u)/com.<seat>.nasbackup`; move `~/Library/LaunchAgents/com.<seat>.nasbackup.plist` and `scheduler/jobs/nasbackup.plist.template` aside into a `_quarantine_<date>/` folder; remove the two installer lines and the doctor line (take the `.pre-<date>-nasbackup` copies first, by this project's convention).

## What must be true before it is applied
1. QA has returned GO on round 2.
2. One real run has been made by hand and printed GOOD (`nas_backup.sh --run --out-of-sequence <card id> --max-seconds <n>`): Kam approved a first full copy "after it passes its check" (13:35:50), and it is Wednesday who runs it.
3. `HOLD_wednesday` has been moved aside (`mv -n HOLD_wednesday HOLD_wednesday.lifted-<date>`), never deleted.

## Times, and what they sit beside
The job fires at hh:30, every hour, on each seat's own machine. Inside its window a seat runs at most one backup; every other fire is one log line.

| Seat | Window (from the seat's conf) | Fires that can start a backup |
|---|---|---|
| Wednesday | 00:30 to 05:30 | 00:30, 01:30, 02:30, 03:30, 04:30 |
| Tuesday (not runnable yet) | 02:30 to 05:30 | 02:30, 03:30, 04:30 |
| Friday (not runnable yet) | 04:30 to 09:30 | 04:30 to 08:30 |

- First fires are two hours apart, as Kam asked.
- On Wednesday's Mac the 03:30 fire shares its minute with `com.wednesday.naspush`. It only starts a backup if 00:30, 01:30 and 02:30 all could not (Mac asleep, NAS away). Tuesday's 05:30 fire falls on her shift change but is outside her window (it closes at 05:30), so it is a log line.
- Limits, not fixed in code this round (Wednesday's ruling 9): the seats run on different machines and the lock is per seat, so two seats can copy to the NAS at the same hour when one is catching up or running long; and no wake is scheduled, so a Mac asleep through its whole window does not back up that night (launchd fires once on wake; outside the window that fire is a log line). A wake schedule is a machine setting and Kam's.

## Verify after applying (read-only)
```
plutil -lint ~/Library/LaunchAgents/com.wednesday.nasbackup.plist
launchctl print "gui/$(id -u)/com.wednesday.nasbackup" | /usr/bin/grep -i -E 'state|last exit'
bash 2_Project_Files/scheduler/install_all_jobs.sh --check
bash 2_Project_Files/nas-backup/nas_backup_nightly.sh --decide-only
```
The morning after: `tail -30 2_Project_Files/nas-backup/logs/wednesday/nightly.log` (24 lines a day is the job's heartbeat), then `bash 2_Project_Files/nas-backup/nas_backup_watch.sh`.

Not tested: the installer with these two lines in it, and any `launchctl` verb. Nothing was loaded.
