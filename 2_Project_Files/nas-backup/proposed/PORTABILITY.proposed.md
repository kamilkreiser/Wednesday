# PROPOSED item for `PORTABILITY.md` (round 3). Nothing here is applied.

The section number is **NN**: Wednesday numbers it (the brain-db lane proposes an item too). Round 1 said "the last one today is 30" and proposed 31; section 31 already exists (the Monday Stuart list, line 566). My slip: I read the list of sections from an earlier grep that stopped at 30.

```
## NN. Nightly copy-only NAS backup — launchd job + NAS share + Homebrew rsync, per seat, machine-local (WED-170, 2026-11-27)
Kam 2026-11-27 12:03: each seat backs up its folder and working projects to the NAS in the middle of the night, about two hours apart; a missed night runs the next; no backup for 3 days is flagged to him.
- **Code (travels with the drive):** `2_Project_Files/nas-backup/` — `nas_backup.sh` (dry run by default), `nas_backup_nightly.sh` (what launchd calls), `nas_backup_watch.sh` (the three-day check), `nb_core.py`, `seats/<seat>.conf` and `seats/<seat>.tokens`, `tests/`. Run state is on the drive and gitignored: `nas-backup/state/`, `logs/`, `manifests/`.
- **Which seats:** Wednesday only, today. Tuesday and Friday have no scope in the lane and the tool refuses them until each coordinator confirms her own.
- **Machine-local, per machine:**
  1. the launchd job `com.<seat>.nasbackup` (from `scheduler/jobs/nasbackup.plist.template`; it fires at minute 30 of every hour and the script keeps the seat's window from `seats/<seat>.conf`: Wednesday 00:30 to 05:30; logs `~/Library/Logs/<seat>_nasbackup.{out,err}`);
  2. the SMB share `//DotORG@192.168.20.154/DEV-Working` mounted at `/Volumes/DEV-Working` by Kam's login (item 27). The tool never mounts it and never creates the path;
  3. Homebrew rsync 3 at `/opt/homebrew/bin/rsync` (already required by `nas_push.sh`) and a `python3` (3.9 or newer; `/usr/bin/python3` is enough);
  4. **macOS privacy consent, twice:** the first launchd run reaches a network volume from `rsync` AND from `python3`. Expect a consent dialog for each on that Mac's screen (item 15a is the rsync one). Answer Allow, or grant both Full Disk Access. An unanswered dialog shows as exit 7 (STALLED) or as the whole-run watchdog in `state/<seat>.json`;
  5. no wake is scheduled. A Mac asleep through its whole window does not back up that night. A wake schedule (`pmset repeat`) is a machine setting and Kam's.
- **New Mac, or the drive's mount path changed:** run `install_all_jobs.sh` from the seat's own tree with `WED_AGENT` unset; check `source_volume` and every `set=` and `exclude_path=` in `seats/<seat>.conf` still name real folders (a path that names nothing is refused, by name); then `nas_backup.sh` (a dry run) and read its output.
- **Editing `seats/<seat>.conf`:** its last line is `END lines=<N>`. Recount after any edit; a file whose count is wrong is refused.
- **Where the copy lives:** `/Volumes/DEV-Working/<Client>/<Seat>/nightly-backup/` (`current/`, `versions/<run stamp>/`, `manifests/`, `runs/`). Wednesday: `Secuura/Wednesday/` and `General/Wednesday/`. Nothing there is ever removed by the tool; clean-up is Kam's word.
- **Not in the backup, by design:** anything secret-shaped by NAME, in any case (`4_Credentials`, `3_Access_Keys` and decorated copies of them, `.env*`, `*.env`, key and certificate files, deploy keys, `.ssh`, `.aws`, `.azure`, `.gh-config`, `.npmrc`, terraform state): re-create by re-login on a new machine. This over-excludes on purpose (`.envrc`, `.env.example`, a Keynote `.key` file). Also: files with more than one hard link; `.git` directories (repos travel by git push: UNPUSHED commits are not on the NAS); `node_modules`, virtualenvs and caches; `_quarantine_*`; the brain-db `pgdata-*` directory; names containing another client's name; other seats' folders inside the shared tree.
- **Degrades to:** no backup that night; the reason is in `nas-backup/state/<seat>.json` and `logs/<seat>/nightly.log`; after 72 hours doctor prints a hard failure naming `nas_backup_watch.sh --card` until a seat has raised the one card for Kam. A damaged state file or index is moved aside and doctor prints `NAS BACKUP STATE WAS FOUND DAMAGED` at every boot until a seat runs `nas_backup_watch.sh --ack-damage`.
- **Verify:** `bash 2_Project_Files/nas-backup/tests/run.sh` (all PASS, fake NAS only), then `bash 2_Project_Files/nas-backup/nas_backup.sh` (a dry run; it lists the real share and writes nothing to it).
```

Rollback: remove the section.

Also proposed, one line in item 15a: "The nightly copy-only backup (item NN) raises the same consent for `python3` as well as `rsync`."
