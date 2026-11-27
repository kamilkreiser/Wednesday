# Nightly copy-only NAS backup: bring-up on the TUESDAY and FRIDAY seats

For: the Tuesday and Friday coordinator seats, each on its own machine and drive. Sent only after the Wednesday seat has run it for real and the coordinator says go. Until then this is a proposal.

Authority: Kam, live board 2026-11-27 12:03: "each agent backs up / syncs their folder and the working projects to the NAS ... about 2 hours apart ... If it does not happen one night, it should happen the next. Flag it with me if backup not done for 3 days so I can approve an out of sequence backup."

Your time: **Tuesday 02:30**, **Friday 04:30** (Wednesday is 00:30).

## What it does, in four lines
- Copies your seat's tree and your client's projects from YOUR drive to `/Volumes/DEV-Working/<your client>/<Seat>/nightly-backup/`. Tuesday: `Datasec/Tuesday/`.
- Copy only. Nothing is deleted on either side; a changed file's previous copy is kept under `versions/<run stamp>/`.
- Never copies `4_Credentials/`, `3_Access_Keys/`, secret-shaped names, `.git`, `node_modules`, `_quarantine_*`.
- A run is good only when every source file is counted at the destination. The result is in `2_Project_Files/nas-backup/state/<seat>.json`.

## What must be true first (check each, on your own machine)
1. The code is in your tree: `ls 2_Project_Files/nas-backup/nas_backup.sh` (it arrives by git pull).
2. The share is mounted as a network share: `mount | /usr/bin/grep -i 'DEV-Working'` shows `(smbfs`. If not, ask Kam to mount it (Finder > Go > Connect to Server). Never create `/Volumes/DEV-Working` by hand.
3. Your client folder exists on the share with exactly this spelling: `python3 -c "import os; print(sorted(os.listdir('/Volumes/DEV-Working')))"`. Tuesday needs `Datasec`. Do not list another client's folder.
4. Homebrew rsync 3: `/opt/homebrew/bin/rsync --version | head -1` says `version 3.` (else `brew install rsync`). A `python3` exists (`/usr/bin/python3` is enough).
5. Your seat's folder name is `TUESDAY` or `FRIDAY`, and `WED_AGENT` in your shell agrees with it (the tool refuses on a disagreement).
6. No other job of yours fires in your window. Tuesday: 02:30 to 05:30 (your shift change is 05:30; the last backup fire is 05:00). Check: `launchctl list | /usr/bin/grep -i 'com.tuesday'` and each plist's time.
7. **Friday only, before anything else:** two open questions are Kam's (see `STATUS.md` QUESTIONS): which client folder(s) Friday writes to (the tool allows `General` only for Friday today), and whether the laptop may carry a scheduled job at all (his 2026-09-23 ruling says none).

## Steps
1. **Run the tests** (fake NAS in a scratch folder, never the real share): `bash 2_Project_Files/nas-backup/tests/run.sh`. Every line PASS, `0 failed`. If one fails on your machine, stop and report it.
2. **Edit your configuration** `2_Project_Files/nas-backup/seats/<seat>.conf`:
   - `source_volume=` your working drive exactly as `mount` shows it;
   - each `set=<Client>|<name>|<absolute source>` line: your tree and your client's projects;
   - leave `status=unconfirmed` for now.
3. **Size your scope before the first dry run.** The Wednesday tree held 6.4 million files outside `reference/` (model weights, gate clones, verification clones). Yours will have its own. Set `status=confirmed`, then: `bash 2_Project_Files/nas-backup/nas_backup.sh --scan`. It only reads your drive. Add `exclude_path=<set name>|<path inside the set>` lines for regenerable bulk until each set is under `max_files` (400,000). Record what you excluded and why in your wrap.
4. **Dry run against the real share (reads only):** `bash 2_Project_Files/nas-backup/nas_backup.sh`. Read all of it. It must end `DRY RUN finished` with no PROBLEM line. Send the totals line to the coordinator.
5. **First real run: Kam's word.** It is outside the window and large, so it is an out-of-sequence backup: card it, and on his yes: `mv -n 2_Project_Files/nas-backup/HOLD_<seat> 2_Project_Files/nas-backup/HOLD_<seat>.lifted-<date>` then `bash 2_Project_Files/nas-backup/nas_backup.sh --run --out-of-sequence <card id>`. Watch the Mac's screen for a macOS privacy dialog for `rsync` or `python3` and answer Allow.
6. **Arm the schedule** only after step 5 printed `GOOD`: the lines in `proposed/install_all_jobs.proposed.md`, then `bash 2_Project_Files/scheduler/install_all_jobs.sh` from your own tree with `WED_AGENT` unset.

## How to prove the first run (send these five facts, with the commands' own output)
1. The run's last lines: `GOOD: every in-scope source file is at the destination and counted.` and the `--- totals:` line.
2. The per-folder table from the run log: for every top-level folder, `src files` equals `dst files` and `src bytes` equals `dst bytes` (2026-10-15 lesson: a copy is done only when it has been counted on both sides).
3. `deleting lines: 0` on every `engine result` line.
4. On the share: a `runs/RUN_<stamp>_COMPLETE.txt` beside the `RUN_<stamp>_STARTED.txt` (a STARTED without a COMPLETE is an unfinished copy).
5. A secrets check on the share: `find "/Volumes/DEV-Working/<Client>/<Seat>/nightly-backup" \( -name '4_Credentials' -o -name '3_Access_Keys' -o -name '.env' -o -name '*.pem' \) | wc -l` prints `0`, and the same `find` for a file you know is there prints 1 (the positive control).
Then the morning after the first scheduled night: `tail -5 2_Project_Files/nas-backup/logs/<seat>/nightly.log` and `bash 2_Project_Files/nas-backup/nas_backup_watch.sh`.

## If it refuses
Every refusal says why and writes nothing. The common ones: share not mounted; a folder on the share differs in case; outside the window without `--out-of-sequence`; `HOLD_<seat>` present; a stale lock after a reboot mid-run (`nas_backup.sh --clear-stale-lock` moves it aside; it is never removed for you); a set above `max_files`.

## What never to do
- Never add a deletion flag, a mirror mode, or `>/dev/null`.
- Never point a `set=` at another client's folder or another seat's tree (the tool refuses; do not work around it).
- Never run `--run` outside the window without Kam's card. After three days without a good backup the watch prints the one card to raise.
- Never delete anything under `nightly-backup/` on the share. Clean-up is Kam's word.
