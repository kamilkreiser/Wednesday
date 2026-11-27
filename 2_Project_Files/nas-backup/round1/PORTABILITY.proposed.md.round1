# PROPOSED item for `PORTABILITY.md` (nothing here is applied)

Append as the next numbered section (the last one today is 30).

```
## 31. Nightly copy-only NAS backup — launchd job + NAS share + Homebrew rsync, per seat, machine-local (WED-170, 2026-11-27)
Kam 2026-11-27 12:03: each seat backs up its folder and working projects to the NAS in the middle of the night, about two hours apart; a missed night runs the next; no backup for 3 days is flagged to him.
- **Code (travels with the drive):** `2_Project_Files/nas-backup/` — `nas_backup.sh` (dry run by default), `nas_backup_nightly.sh` (what launchd calls), `nas_backup_watch.sh` (the three-day check), `nb_core.py`, `seats/<seat>.conf`, `tests/run.sh`. Run state is on the drive and gitignored: `nas-backup/state/`, `logs/`, `manifests/`.
- **Machine-local, per machine:**
  1. the launchd job `com.<seat>.nasbackup` (rendered from `scheduler/jobs/nasbackup.plist.template` by `install_all_jobs.sh`; Wednesday 00:30, Tuesday 02:30, Friday 04:30; logs `~/Library/Logs/<seat>_nasbackup.{out,err}`);
  2. the SMB share `//DotORG@192.168.20.154/DEV-Working` mounted at `/Volumes/DEV-Working` by Kam's login (item 27). The tool never mounts it and never creates the path;
  3. Homebrew rsync 3 at `/opt/homebrew/bin/rsync` (already required by `nas_push.sh`) and a `python3` (3.9 or newer; `/usr/bin/python3` is enough);
  4. **macOS privacy consent, twice:** the first launchd run reaches a network volume from `rsync` AND from `python3`. Expect a consent dialog for each on that Mac's screen (item 15a is the rsync one, 2026-10-05). Answer Allow, or grant both Full Disk Access. An unanswered dialog shows as exit 7 (STALLED) or as the whole-run watchdog in `state/<seat>.json`.
- **New Mac, or the drive's mount path changed:** run `install_all_jobs.sh` from the seat's own tree with `WED_AGENT` unset; check `seats/<seat>.conf` `source_volume` still names the drive as `mount` shows it; then `nas_backup.sh` (a dry run) and read its output.
- **Where the copy lives:** `/Volumes/DEV-Working/<Client>/<Seat>/nightly-backup/` (`current/`, `versions/<run stamp>/`, `manifests/`, `runs/`). Wednesday: `Secuura/Wednesday/` and `General/Wednesday/`. Nothing there is ever removed by the tool; clean-up is Kam's word.
- **Not in the backup, by design:** `4_Credentials/`, `3_Access_Keys/` and secret-shaped names (re-create by re-login on a new machine); `.git` directories (repos travel by git push: UNPUSHED commits are not on the NAS); `node_modules`, virtualenvs and caches; `_quarantine_*`; the brain-db `pgdata-*` directory; other seats' folders.
- **Degrades to:** no backup that night; the reason is in `nas-backup/state/<seat>.json` and `logs/<seat>/nightly.log`; after 72 hours `nas_backup_watch.sh` prints the one decision card for Kam at every boot until it is raised.
- **Verify:** `bash 2_Project_Files/nas-backup/tests/run.sh` (all PASS, fake NAS only), then `bash 2_Project_Files/nas-backup/nas_backup.sh` (dry run against the real share).
```

Rollback: remove the section.

Also proposed, one line in item 15a, so the next person meets both prompts: "The nightly copy-only backup (item 31) raises the same consent for `python3` as well as `rsync`."
