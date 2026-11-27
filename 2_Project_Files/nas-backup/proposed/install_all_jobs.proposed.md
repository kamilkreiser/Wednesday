# PROPOSED lines for `scheduler/install_all_jobs.sh` (nothing here is applied)

Applying these IS the arming step. It is the coordinator's, on Kam's word, after QA. The build seat edited no existing file.

## What must be true first
1. QA has passed this lane, and Kam has answered the scope questions in `STATUS.md`.
2. One real run has been made by hand and reported GOOD (`nas_backup.sh --run --out-of-sequence <card id>`), so the first scheduled night is not also the first real copy.
3. `HOLD_<seat>` in this lane has been moved aside (`mv -n HOLD_wednesday HOLD_wednesday.lifted-<date>`).

## Step 1: put the template where the installer looks
```
cp -n "2_Project_Files/nas-backup/jobs/nasbackup.plist.template" "2_Project_Files/scheduler/jobs/nasbackup.plist.template"
```
Rollback: `mv -n 2_Project_Files/scheduler/jobs/nasbackup.plist.template 2_Project_Files/scheduler/jobs/_quarantine_<date>/` (the installer then no longer sees it), then `launchctl bootout gui/$(id -u)/com.<seat>.nasbackup` and move `~/Library/LaunchAgents/com.<seat>.nasbackup.plist` aside.

## Step 2: three additions inside the `for t in "$JOBS"/*.plist.template` loop

(a) Beside the existing `nassync` hold line (after line 94), so a held backup is never (re)installed by a well-meaning re-run. This is the second independent lock the 2026-10-04 recurrence asks for:
```
  # nasbackup (WED-170, Kam 2026-11-27): the copy-only nightly backup. Held per seat by nas-backup/HOLD_<seat>; lifting it is the coordinator's word on Kam's instruction.
  if [ "$job" = "nasbackup" ] && [ -e "$PROJECT_DIR/2_Project_Files/nas-backup/HOLD_$SEAT" ]; then echo "skip $job — HELD (2_Project_Files/nas-backup/HOLD_$SEAT)"; continue; fi
  # ... and never for a seat whose configuration is not confirmed on its own machine.
  if [ "$job" = "nasbackup" ] && ! /usr/bin/grep -q '^status=confirmed$' "$PROJECT_DIR/2_Project_Files/nas-backup/seats/$SEAT.conf"; then echo "skip $job — seats/$SEAT.conf is not confirmed"; continue; fi
```
Rollback: remove the two lines (the installer keeps `install_all_jobs.sh.pre-<date>-nasbackup` beside itself, by this project's convention; take that copy first).

(b) Beside the `NASHOUR`/`NASMIN` case (after line 111), the per-seat fire times. A schedule is a per-seat fact (the 2026-09-21 lesson in that same block):
```
  case "$SEAT" in
    wednesday) NBH0=0; NBM0=30; NBH1=1; NBM1=40; NBH2=2; NBM2=50; NBH3=4; NBM3=0  ;;
    tuesday)   NBH0=2; NBM0=30; NBH1=3; NBM1=20; NBH2=4; NBM2=10; NBH3=5; NBM3=0  ;;
    friday)    NBH0=4; NBM0=30; NBH1=5; NBM1=40; NBH2=6; NBM2=50; NBH3=8; NBM3=10 ;;
  esac
```
and eight more `-e` expressions on the existing `sed` line 112:
```
 -e "s|@NBH0@|$NBH0|g" -e "s|@NBM0@|$NBM0|g" -e "s|@NBH1@|$NBH1|g" -e "s|@NBM1@|$NBM1|g" -e "s|@NBH2@|$NBH2|g" -e "s|@NBM2@|$NBM2|g" -e "s|@NBH3@|$NBH3|g" -e "s|@NBM3@|$NBM3|g"
```
The first fire time of each seat must equal `fire=` in `nas-backup/seats/<seat>.conf` (the script's window is computed from the conf, not from the plist). Rollback: remove the case block and the eight expressions.

(c) After a successful `launchctl load` of `nasbackup` (inside the `if launchctl load` branch), start the three-day clock, so a job that is installed and then never fires is still flagged:
```
    [ "$job" = "nasbackup" ] && bash "$PROJECT_DIR/2_Project_Files/nas-backup/nas_backup_watch.sh" --mark-armed
```
Rollback: remove the line. (The mark itself is one field, `armed_at`, in `nas-backup/state/<seat>.json`.)

## Step 3: Friday
`install_all_jobs.sh` exits at line 65 for the friday seat ("no scheduled jobs are installed on the laptop", Kam 2026-09-23). Kam's 2026-11-27 instruction says each agent backs up. Those two do not agree, and this proposal does NOT resolve it: Friday gets the job only if Kam says the laptop may carry this one scheduled job. If he does, the smallest change is to let the loop run for friday with every job except `nasbackup` skipped; that line is not written here on purpose.

## Step 4: verify the install (read-only)
```
launchctl print "gui/$(id -u)/com.<seat>.nasbackup" | /usr/bin/grep -i -E 'state|last exit|Hour|Minute'
bash 2_Project_Files/scheduler/install_all_jobs.sh --check
bash 2_Project_Files/nas-backup/nas_backup_nightly.sh --decide-only
```
The first morning after: read `nas-backup/logs/<seat>/nightly.log` and run `nas_backup_watch.sh`.
