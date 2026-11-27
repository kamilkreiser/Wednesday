# Nightly copy-only NAS backup: what the TUESDAY and FRIDAY seats do (round 3)

For: the Tuesday and Friday coordinator seats. Sent only when Wednesday says go. Until then it is a proposal.

Authority: Kam, live board 2026-11-27 12:03: "each agent backs up / syncs their folder and the working projects to the NAS ... about 2 hours apart ... If it does not happen one night, it should happen the next. Flag it with me if backup not done for 3 days so I can approve an out of sequence backup."

## Step 1: read this first. Today you can run NOTHING from this lane, on purpose.

The tool has a scope for the Wednesday seat only. From a TUESDAY or FRIDAY tree every command, a dry run included, exits 2 with "has no confirmed scope in this lane". That is the design after the independent check of 2026-11-27: a seat with no confirmed scope carried another client's folders (Friday: all of them).

**Your scope is yours to state, and Wednesday's to put into the lane.** You do not edit `nb_core.py`, `scheduler/install_all_jobs.sh`, `doctor.sh` or the launcher: those are shared files and Wednesday applies shared changes once, for all seats.

What you send Wednesday (a QUESTION mail, topic `nas-backup scope`), each item checked on your own machine:

1. **Your client folder on the share**, spelled exactly as the share spells it: `python3 -c "import os; print(sorted(os.listdir('/Volumes/DEV-Working')))"`. Tuesday expects `Datasec`. Do not list another client's folder.
2. **Your working drive** as `mount` shows it (it must be a local volume), and the absolute path of your seat tree and of each project folder you coordinate.
3. **What must never leave with your backup:** the other clients' names AND their project names as they appear on your drive (for Tuesday: Secuura, Blockchain, Platform K, Extranet, and the Wednesday seat's folders inside the shared tree such as `2_Project_Files/wednesday` and `0_Brain/daily_wednesday` if they exist on yours). This becomes your entry in the tool's seat table and your `seats/<seat>.tokens` file.
4. **Your other scheduled jobs and their times** (`launchctl list | /usr/bin/grep -i "com.<seat>"`, and each plist's time), so your window can be checked against them. Proposed: Tuesday 02:30 to 05:30, Friday 04:30 to 09:30.

**STOP HERE if any of these is open. Do not go to step 2.**

- **Friday: two rulings are missing and both are Kam's.** (a) Friday works both clients from the laptop; where does each client's material go on the share? (b) His ruling of 2026-09-23 says the laptop carries no scheduled job; his instruction of 2026-11-27 says each agent backs up. Until he has ruled on both, Friday stops at this line.
- **Tuesday:** stop here until Wednesday has answered your scope mail with a lane commit that adds your seat.

## Step 2: after Wednesday has added your seat (her commit, pulled into your tree)

1. **Run the tests** (fake NAS in a scratch folder, never the real share): `bash 2_Project_Files/nas-backup/tests/run.sh`. Every line PASS, `0 failed`. Then `bash 2_Project_Files/nas-backup/tests/mutants.sh` (long: one suite run per mutant, about an hour): `0 survived or broken`. If either fails on your machine, STOP and report it.
2. **Check the prerequisites:** the share is mounted as a network share (`mount | /usr/bin/grep -i 'DEV-Working'` shows `(smbfs`; if not, ask Kam to mount it, never create the path); `/opt/homebrew/bin/rsync --version | head -1` says `version 3.`; your tree's folder name is `TUESDAY` or `FRIDAY` and `WED_AGENT` agrees with it.
3. **Size your scope:** `bash 2_Project_Files/nas-backup/nas_backup.sh --scan` (reads your drive only). The Wednesday tree held 6.4 million files of caches and clones before it was narrowed. Propose `exclude_path=` lines for regenerable bulk to Wednesday until each set is under 400,000 files; say what and why. A path that does not exist is refused by name, and the conf's last line `END lines=<N>` must be recounted after every edit.
4. **Dry run against the real share (reads only):** `bash 2_Project_Files/nas-backup/nas_backup.sh`. Read all of it. It must end `DRY RUN finished` with no PROBLEM line. Send Wednesday the totals line, the "excluded as secret-shaped" line and the "another client's project name" line.

## Step 3: the first real copy is Kam's word, and it is long

It is outside the window and large, so it is an out-of-sequence backup. Card it. On his yes:
```
mv -n 2_Project_Files/nas-backup/HOLD_<seat> 2_Project_Files/nas-backup/HOLD_<seat>.lifted-<date>
bash 2_Project_Files/nas-backup/nas_backup.sh --run --out-of-sequence <card id> --max-seconds <seconds>
```
**`--max-seconds` matters:** without it the run stops at the nightly cap (3 to 5 hours) and is recorded as failed. Take the dry run's estimate in hours, double it, and give it in seconds. Watch the Mac's screen for a macOS privacy dialog for `rsync` or `python3` and answer Allow.

## Step 4: the schedule

You do nothing. Wednesday applies the one shared change (`proposed/install_all_jobs.proposed.md`); you then run `bash 2_Project_Files/scheduler/install_all_jobs.sh` from your own tree with `WED_AGENT` unset, as for any other job.

## How to prove the first run (send these, with the commands' own output)
1. The run's last lines: the line starting `GOOD: every in-scope source file is PROVEN at the destination with the source's content` and the `--- totals:` line. If the GOOD line names files DELETED at the source during the run, send those lines too.
2. The per-folder table: for every top-level folder `src files` equals `dst files` and `src bytes` equals `dst bytes`.
3. `deleting lines: 0` on every `engine pass` line, and `NOT PROVEN: 0` on every set.
4. On the share: a `runs/RUN_<stamp>_COMPLETE.txt` beside the `RUN_<stamp>_STARTED.txt`.
5. A secrets check on the share, with its positive control: `find "/Volumes/DEV-Working/<Client>/<Seat>/nightly-backup" \( -iname '*4_credentials*' -o -iname '*3_access_keys*' -o -iname '.env*' -o -iname '*.pem' -o -iname '*.key' \) | wc -l` prints `0`, and the same `find` for a file you know is there prints 1.
The morning after the first scheduled night: `tail -30 2_Project_Files/nas-backup/logs/<seat>/nightly.log` and `bash 2_Project_Files/nas-backup/nas_backup_watch.sh`.

## If it refuses or fails
Every refusal says why and writes nothing. A FAILED run names each file it could not prove at the destination (`NOT DELIVERED: ...`), in its last lines and in the watch's line. After a reboot mid-run: `nas_backup.sh --clear-stale-lock` moves the stale lock aside; it refuses while a copy engine of yours is still running.

## What never to do
- Never add a deletion flag, a mirror mode, or `>/dev/null`.
- Never point a `set=` at another client's folder or another seat's tree. The tool refuses; do not work around it.
- Never run `--run` outside the window without Kam's card. After three days without a good backup doctor prints a hard failure naming `nas_backup_watch.sh --card`: run it, add the one card it prints, then `--mark-raised <id>`.
- Never delete anything under `nightly-backup/` on the share. Clean-up is Kam's word.

Nothing in these instructions writes or deletes on the share except step 3's approved run.

## Round 3: what is different for you
- **One rule: a night is good only if every planned file is proven on the share.** A file that cannot be read fails the night and is named; so does a set whose plan holds no file at all (if one of your sets is really empty, say so in your scope mail: Wednesday adds an `allow_empty=` line, you do not).
- **A set= line cannot name a folder that holds another seat's tree or another client's folder.** Name your folders one by one. The tool refuses the wider line and says which forbidden folder it would have reached.
- **The copy goes in chunks of 200 files and saves its proofs as it goes.** If the first copy is interrupted (a closed terminal, a reboot, the cap), start the same command again: it sends only what is not proven.
- **If doctor says `NAS BACKUP STATE WAS FOUND DAMAGED`:** run `bash 2_Project_Files/nas-backup/nas_backup_watch.sh --check`, read what it says was damaged and where it was moved, tell Wednesday, then `nas_backup_watch.sh --ack-damage`.
- **More names stay out of the backup** (token and key files by their usual names, `.auth` and `.docker` folders, public certificates too). The list is in the lane's README, with the plain statement that a name rule cannot be complete.
