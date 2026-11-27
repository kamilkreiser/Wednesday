# CENSUS: what exists for the NAS on the WEDNESDAY seat (read-only, 2026-11-27)

Build seat "nas-backup", WED-170. Every fact below names its instrument. Times are from `date` on this Mac (Kamil's Mac mini, `scutil --get ComputerName`), AEDT. Nothing was written to the NAS and no existing script was run.

## Headline

1. **A nightly NAS job is already armed on this Mac, and it has not finished once since it was repointed.** `com.wednesday.naspush` (03:30, `scheduler/nas_push.sh`, whole drive to `/Volumes/Backup/DevMASTER-mirror`) is loaded. Its log shows STALLED on 11-12 and 11-13, then KILLED by its 4-hour cap on every night from 11-14 to 11-26 (13 nights), and no "DONE" line at all.
2. **Why it never finishes: the share does not keep the file times rsync sets.** Every one of the 128,421 lines of the 11-26 run is `>f..t......` (same size, time differs), so it re-sends the same files every night, at 8.9 files a second, and is cut off before it reaches new ones. The mirror's `WEDNESDAY` folder is empty.
3. **That job has put two secrets folders on the NAS.** `/Volumes/Backup/DevMASTER-mirror/!CODING/Secuura/Blockchain/4_Credentials` (23 entries) and `.../3_Access_Keys` (6 entries) exist on the Backup share. `nas_push.sh` has no exclusion for either name and Kam's sync profile has none. This is against workspace hard rule 3. Existence and entry counts only were read; no file in them was opened. Nothing was touched: what to do about it is Kam's.
4. **The two-way sync job is held on Kam's word and stays held.** `nas_sync.sh` (unison, can delete in both directions) has hold files for both seats; this design does not re-arm it and does not use its engine.
5. **Recommendation: build beside, not extend.** The new copy-only job goes to the DEV-Working share in per-client, per-seat folders. Once it has one good run, ask Kam whether to retire `naspush` (one card). Until then the two overlap from 03:30 on this Mac.
6. **The scope as first written was 100 times too big.** The seat's tree outside `reference/` is 6.4 million files and 627 GiB; the Secuura folder is 2.5 million in-scope files after the standard exclusions (and 44 million more under `worktrees`). After the narrowing in `seats/wednesday.conf` the backup is 1,012,113 files and 67.83 GiB.

## A. Every existing NAS job and tool

Instrument: the files read whole (`Read`), unless a row says otherwise.

| Tool | Copies what, where | Engine and flags | When, which seat | Can it delete? |
|---|---|---|---|---|
| `tools/nas_offload.sh` | Named sources to `/Volumes/DEV-Working/{Secuura,General}/Wednesday/<date>_<topic>/` with `MANIFEST.txt`, sha256 of every file, REVIEW-AFTER +30 days | `rsync -a` (whichever rsync is first on PATH) | By hand, Wednesday seat. Not scheduled | No deletion flag. It does `rm -f` its own stderr temp file inside the new folder (line 71). Refuses an existing target folder |
| `scheduler/nas_sync.sh` + `jobs/nassync.plist.template` | Two-way: the whole drive against `/Volumes/Development` (the old NAS), through Kam's `!SYNC FILES/devnas-sync.sh` and `devnas.prf`. Tuesday's branch: one-way, three paths | unison 2.54 (`/opt/homebrew/bin/unison`), `batch = true`; a retry pass for failed paths | Wednesday 03:30, Tuesday 23:00 (`install_all_jobs.sh` lines 107 to 111) | **YES, in both directions.** Its header says it cannot PREVENT a mass deletion, only detect one afterwards. `confirmbigdel = true` covers a whole-replica delete only |
| `scheduler/nas_push.sh` + `jobs/naspush.plist.template` | One-way: all of `/Volumes/DevMASTER` to `/Volumes/Backup/DevMASTER-mirror`, minus the profile's ignores and `Datasec TUESDAY node_modules worktrees .venv __pycache__ .next .turbo .pytest_cache .git` | Homebrew rsync 3.5.2: `-rlt --timeout=1800 --modify-window=2 --backup --backup-dir=<mirror>/_nas_push_overwritten/<stamp> --itemize-changes --stats`; 4-hour cap; 15-minute stall watchdog | 03:30, Wednesday seat only | No. It checks its own argv for `--delete*`. A replaced file is moved to the backup dir |
| `scheduler/nas_staleness.sh` | Nothing. Compares six key files by sha256 against `/Volumes/Development` | `stat`, `shasum` | Called by `nas_sync.sh` and `doctor.sh` | No (read-only). It prints SKIP today: that volume is not mounted |
| `scheduler/nas_sync_lib.sh` | Nothing. Log parser for the retry pass | awk, sed | Sourced by `nas_sync.sh` | No |
| `doctor.sh` lines 485 to 547, 1433 to 1439 | Nothing. Per-job sweep (reports `nassync` as HELD while its hold file exists; includes `naspush` for Wednesday); NAS staleness; "DEV-Working NAS mounted" | `launchctl print` | Every boot | No |

Other seats' NAS tools exist and were not read (their files): `2_Project_Files/tuesday/tools/nas_offload.sh` (named in PORTABILITY 27), and whatever wrote `General/Friday/2026-11-19_nas-backup-selftest` and `-selftest-v2` on the share (folder names only, from `os.listdir`).

## B. Installed, loaded or held on THIS Mac now

Instrument: `launchctl list` filtered, `launchctl print-disabled gui/501`, `ls ~/Library/LaunchAgents`, at 12:05:58.

| Job | State | By whose word |
|---|---|---|
| `com.wednesday.naspush` | **LOADED and armed.** `launchctl list` row `- 0 com.wednesday.naspush`; plist in `~/Library/LaunchAgents` dated 11 Nov 10:11, Hour 3 Minute 30. No hold file: `ls scheduler/ \| grep -i -c NASPUSH_HOLD` is 0 (positive control: `NASSYNC_HOLD` counts 2) | Kam, card `wed-nassync-rearm-shape-1004` = a ("go with a — rebuild it one-way", quoted in the script header), then card `wed-nightly-nas-mirror-old-nas-1111` = a ("Repoint to the new NAS's Backup share"; that card reads `ruled` in the decision store) |
| `com.wednesday.nassync` | **Not loaded, no plist installed, HELD.** No row in `launchctl list`; `scheduler/NASSYNC_HOLD_wednesday` exists | The hold file, verbatim: "Re-arm ONLY on Kam's word: delete this file AND `launchctl enable gui/501/com.wednesday.nassync`." Set 2026-10-04 after the deletion incident. Lesson 2026-08-26 (recurrence section): "A scheduled mechanism that can destroy data and cannot PREVENT that is held, not armed." Card `wed-nassync-rearm-shape-1004` |
| `com.tuesday.nassync` | **Disabled** on this Mac: `"com.tuesday.nassync" => disabled`. `scheduler/NASSYNC_HOLD_tuesday` exists | That hold file: "Lift: Kam's word only." Set 2026-10-16 by the Tuesday seat. PORTABILITY 20: "The NAS leg stays OFF until the case is fixed (Kam's card `nas-case-fold-datasec`)." |
| A `nasbackup` job | **Does not exist.** `launchctl list \| grep -i -c nasbackup` is 0 (positive control: `naspush` counts 1); no such plist | Nothing installed by this seat |

Other loaded jobs with a clock (for the schedule check): `close` 23:00, `dailysweep` 15:00, `shiftchange` 05:30, `wake` 06:00, `stalescreen` 01:15 (its script keeps a 01:00 to 05:00 window), `stuartweekly` Monday 08:00, `chatsync` every 60 s, `trmnlpush` every 900 s, `dmlinkwatch` (running, pid 874; it has no template in `scheduler/jobs/`).

### The armed `naspush` leg, measured
- Outcomes (`~/Library/Logs/wednesday_naspush.log`): STALLED 11-12 and 11-13 (the macOS privacy prompt of PORTABILITY 15a); KILLED-CAP after 14,400 s on each of 11-14 to 11-26. `grep -i -c 'DONE in'` on that log is 0 (positive control: 15 STALLED or KILLED lines in the same file).
- What it moves (`scheduler/state/naspush_run_*.log`, source sizes by `stat`): 11-24: 128,619 files, 12.21 GiB; 11-25: 130,164 files, 10.09 GiB; 11-26: 128,421 files, 9.11 GiB. That is 8.9 to 9.0 files a second and under 1 MiB a second, three nights running.
- Why the same files each night: `awk '{print substr($0,1,11)}'` on the 11-26 log gives 128,421 lines of `>f..t......` and nothing else but 2 folder lines and the kill. Source `/Volumes/DevMASTER/CLAUDE.md` has mtime 2026-09-10 10:08:58; the mirror's copy has mtime 2026-11-26 03:30:17 (python `os.stat`). The share keeps the time of the copy, not the time rsync sets (`grep -i -c 'set times'` on that log is 0: rsync reported no error doing it).
- What is on the mirror: `os.listdir` of its `WEDNESDAY` folder returns `[]`. The top level has 25 names; `TUESDAY`, `SYSTEM`, `NEW STRUCTURE` are not among them.
- **Secrets on the mirror** (`os.path.isdir` and a top-level entry count; nothing opened): `!CODING/Secuura/Blockchain/4_Credentials` 23 entries, `!CODING/Secuura/Blockchain/3_Access_Keys` 6 entries. Cause: `nas_push.sh` line 108 lists no secrets name, and `grep -i -c -E '^ignore = .*(4_Credentials|3_Access_Keys)'` on `!SYNC FILES/devnas.prf` is 0 (positive control: 23 `ignore =` lines in it). `nas_sync.sh` line 93 states the rule this breaks: "4_Credentials + 3_Access_Keys: NEVER replicated to the NAS (workspace hard rule 3)".

## C. The NAS as mounted now

Instrument: `mount`, `df -k`, python `os.listdir`, `os.pathconf`, `os.stat`, `smbutil statshares -m`, at 12:05 to 12:06.

```
//DotORG@192.168.20.154/DEV-Working on /Volumes/DEV-Working (smbfs, nodev, nosuid, mounted by kamil)
//DotORG@192.168.20.154/Backup on /Volumes/Backup (smbfs, nodev, nosuid, mounted by kamil)
//DotORG@192.168.20.154/Seagate%20Hub on /Volumes/Seagate Hub (smbfs, nodev, nosuid, mounted by kamil)
/dev/disk7s1 on /Volumes/DevMASTER (apfs, local, nodev, nosuid, journaled, noowners)

Filesystem                          1024-blocks       Used   Available Capacity
//DotORG@192.168.20.154/DEV-Working 11702751232  117175864 11585575368     2%
//DotORG@192.168.20.154/Backup       4867637248 1854892408  3012744840    39%
```
- **DEV-Working top-level names as the filesystem returns them:** `['#recycle', '.DS_Store', 'Datasec', 'Friday', 'General', 'Personal Projects', 'Secuura']`. `Datasec/` was not entered.
- This seat's client folders: `Secuura` holds `['Blockchain']` (and `Blockchain` holds `['WIP']`); `General` holds `['Friday', 'Wednesday']`; `General/Wednesday` holds `['2026-11-11_workflow-selftest']`. **`Secuura/Wednesday` does not exist yet**; the first real run would create it.
- **Free space:** 11,863,629,176,832 bytes (10.79 TiB) of 11,983,617,261,568 (`os.statvfs`).
- **Case sensitivity, found without writing:** NOT case-sensitive, case-preserving. `os.pathconf(root, 11)` (`_PC_CASE_SENSITIVE`) is 0 and `os.pathconf(root, 12)` (`_PC_CASE_PRESERVING`) is 1; and a read-only `os.stat` of the case-flipped name of each top-level folder resolves to the same inode (`Secuura` and `sECUURA`, same for `Datasec`, `General`, `Friday`). This is the 2026-08-25 shape.
- **The drive is the opposite:** `os.pathconf('/Volumes/DevMASTER', 11)` is 1. The drive is case-SENSITIVE, so it can hold two names the NAS cannot. Seven such pairs are in scope today (section D).
- SMB 3.1.1, signing on, encryption off on the wire (`SMB_CURR_ENCRYPT_ALGORITHM OFF`).
- Speed, read-only samples on the same NAS box (Backup share): listing 15,687 entries in 40.2 s, 390 entries a second; reading 40 MiB in 0.2 s (too small a sample to mean much). Write speed was not measured: it needs a write.

## D. What a backup of this seat would cover

Instrument: `nas_backup.sh --scan --measure-excluded` (12:19 to 12:53), `nas_backup.sh --scan` (12:56), and the real dry run (12:59 to 13:06). All read the drive only.

### Before narrowing
| Source | In scope after the fixed exclusions | Largest parts |
|---|---|---|
| `/Volumes/DevMASTER/WEDNESDAY` without `0_Brain/reference` | **6,425,033 files, 627.42 GiB** | `local-model/spark/cache` 237.66 GiB, 3,898,595 files; `tools/omlx/models` 198.18 GiB, 237 files; `local-model/spark-ab/work` 141.98 GiB, 2,006,459 files; `local-model/runs` 20.18 GiB, 229,507 files; `fleet/qa-agent/gatesets` 10.56 GiB, 193,238 files |
| `0_Brain/reference` | Not walked here. 279 GB and 5.9 million files by `current_structure_census.md` section B1 (Wednesday's figure, not re-measured). 19,309 of its files are tracked in git (`git ls-files`) | Asked in STATUS |
| `/Volumes/DevMASTER/!CODING/Secuura` | **2,464,442 files, 93.59 GiB** | `Blockchain/5_Project_History` 2,098,046 files, 59.91 GiB in 1,045 dated session folders; `Blockchain/deploy-clones` 142,368 files; `Blockchain/scratchpad` 73,847 files |
| The same folder, already excluded by the fixed rules | `worktrees` 44,203,120 files, 474.46 GiB; `node_modules` 22,593,291 files, 157.12 GiB; `_quarantine_*` 8,644,477 files, 75.64 GiB; `.git` 87,719 files, 66.89 GiB | |
| Other `!CODING` folders | `Testing Agent MAIN` 151,707 files, 9.38 GiB; `Paperclip` 4,557 files, 401 MiB; `Agentic Coding` 3,205 files; `Claude to Claude` 149 files, 346 MiB; seven more, under 200 files each | |

`!CODING` has no `Datasec` folder on this drive (python `os.listdir`: 16 names, none of them Datasec).

### After narrowing (what `seats/wednesday.conf` now says, and what the dry run counted)
| Set | Goes to | Files | Bytes |
|---|---|---|---|
| WEDNESDAY tree | `General/Wednesday/nightly-backup/current/WEDNESDAY` | 265,195 | 26.67 GiB |
| Secuura client folder | `Secuura/Wednesday/nightly-backup/current/Secuura` | 587,085 | 30.95 GiB |
| Testing Agent MAIN | `General/Wednesday/nightly-backup/current/CODING/Testing Agent MAIN` | 151,723 | 9.38 GiB |
| Eleven smaller general projects | `General/Wednesday/nightly-backup/current/CODING/<name>` | 8,110 | 0.82 GiB |
| **Total** | | **1,012,113** | **67.83 GiB** |

### What is excluded, and why
Fixed in `nb_core.py`; no configuration can remove these:
- **Secrets, never copied:** `4_Credentials`, `3_Access_Keys`, `.env`, `.env.*`, `*.env`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.keystore`, `*.jks`, `*.kdbx`, `id_rsa*`, `id_ed25519*`, `id_ecdsa*`, `id_dsa*`, `.azure`, `.gh-config`, `.aws`, `.ssh`, `.gnupg`, `.netrc`, `.npmrc`, `.pypirc`, `.pgpass`, `service_principal_entries.json`, `msal_token_cache*`, `credentials.json`, `secrets.json`. In the seat tree alone that is 874 entries (30,509 of the unnarrowed tree's files were `.env.*`).
- **`.git` directories: excluded.** A live object store copied file by file is not a consistent repository, and its pack files are rewritten whole, which would put a new multi-hundred-megabyte version on the NAS on many nights. Committed work travels by `git push`. **What this leaves out: commits not yet pushed, stashes and local-only branches are NOT in the backup.** The working tree, including uncommitted edits, is. (The armed `naspush` leg excludes `.git` the same way.)
- **`node_modules`, `worktrees`, `qa-worktrees*`, `deploy-worktrees`, `wt-*`, `.venv`, `venv`, `__pycache__`, `.next`, `.turbo`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.hypothesis`, `.pnpm-store`:** regenerable (Kam's `narrow-hard` ruling of 2026-09-11, quoted in `nas_sync.sh`).
- **Build output named `dist`, `build` or `coverage` is NOT excluded.** `nas_sync.sh` records that those names hold real source in some trees.
- **Anything under a `_quarantine_*` folder.**
- **`pgdata-*`** (the brain-db lane's live Postgres directory, `2_Project_Files/brain-db/pgdata-<seat>/`): a live database copied file by file is not a usable copy, and it is a rebuildable index. One such folder exists today: 1,342 files, 172 MiB.
- **System litter:** `.DS_Store`, `._*`, `.Spotlight-V100`, `.fseventsd`, `.Trashes`, `.TemporaryItems`, `.smbdelete*`, `.unison*`, `#recycle`.
- **Other seats, inside the seat's own tree only:** names matching `*tuesday*` or `*friday*` (358 entries; e.g. `2_Project_Files/tuesday`, `0_Brain/daily_tuesday`). The brief: those files belong to other seats.
- **Another client, in every set:** names matching `*datasec*` (1,113 entries in the seat tree, 8 in Testing Agent MAIN, 2 in Secuura).

Added for this seat in `seats/wednesday.conf` (each line carries its measured size; all are git-ignored paths of caches, model weights or throw-away clones): `0_Brain/reference`; `local-model/spark/cache`; `local-model/spark-ab/work`; `tools/omlx/models`, `uv-cache`, `cache`; `local-model/runs`; `local-model/hosted/work`; `tools/media/models`; `tools/ollama`; and, inside the Secuura set only, folders named `wt`, `wt_*`, `quarantine`, `_quarantine`, `quarantine_*`, `*node_modules*`, `node-compile-cache`, `clone`, `deploy-clones`, the per-seat temp folders `.a23t`-style, and `Blockchain/scratchpad`.

Not copied and not excluded by a rule, each counted in every manifest:
- **982 symlinks**: recorded (path and target) in the manifest folder, not created on the NAS.
- **14 files under 14 names that differ only in case** from a sibling (the NAS can hold one of each pair, so neither is copied). Five pairs in Secuura, e.g. `Blockchain/2_Project_Files/logs` and `.../Logs`, `mergetree_ks-1614.out` and `mergetree_KS-1614.out`; two pairs in Testing Agent MAIN.

## E. The overlap, plainly

- `naspush` already tries to do the first half of Kam's instruction for this seat (its folder and projects, nightly, copy-only) and does not manage it: wrong shape for the instruction (whole drive, one seat, one flat mirror, no per-client folder, no catch-up record, no three-day flag), no secrets exclusion, and an engine decision (size plus time) that this NAS defeats.
- `nassync` is the held two-way job. Nothing here re-arms it or calls its engine.
- **Recommendation: build beside.** Extending `nas_push.sh` would mean editing an armed script in place, changing its destination under a running schedule, and inheriting the size-plus-time decision. The new job shares nothing with either: different share (DEV-Working), different folders, different launchd label (`com.<seat>.nasbackup`), its own lock, state and hold file.
- **How the two relate after arming:** the new 00:30 window overlaps `naspush` from 03:30 on the same Mac and the same NAS box. They cannot corrupt each other (different shares and folders), but they share the disk and the network. Proposed for Kam, one card, after the new job's first good run: hold `naspush` (and decide what happens to the mirror and the secrets folders on it). This seat changed nothing about `naspush`.

## F. Proposed times against every scheduled job found

| Seat | Fires (first is the scheduled time) | Window | Same-minute collision? |
|---|---|---|---|
| Wednesday | 00:30, 01:40, 02:50, 04:00 | 00:30 to 05:30 | None with 01:15, 03:30, 05:30, 06:00, 06:45, 15:00, 23:00, 23:30. **Overlap, not collision:** `stalescreen` runs 01:15 inside the window (it uses the model box, not the NAS); `naspush` starts 03:30 and runs to 07:30 |
| Tuesday | 02:30, 03:20, 04:10, 05:00 | 02:30 to 05:30 | None with her templates (05:30, 06:00, 23:00, the hourly `escalate48h`, which has no fixed minute). The window stops at her 05:30 shift change. To be confirmed on her machine |
| Friday | 04:30, 05:40, 06:50, 08:10 | 04:30 to 09:30 | The laptop has no scheduled jobs (`install_all_jobs.sh` line 65). See STATUS QUESTIONS |

The collision PORTABILITY names (`com.tuesday.close` and `com.tuesday.nassync` both at 23:00, "unresolved and Kam's") is not touched: no proposed time is 23:00, and `nassync` is held. The 05:30 shift change is the reason the Wednesday and Tuesday windows close at 05:30 and no fire is placed at 05:30. An hourly retry at minute 30 was rejected because Wednesday's would land on 03:30 (`naspush`) and Tuesday's on 05:30.

## G. Conflict copies (listed as asked, not read)

`scheduler/`: `close_wednesday (conflict_on_2026-09-17).sh`, `install_all_jobs (conflict_on_2026-09-17).sh`.
`scheduler/jobs/`: `chatsync.plist`, `close.plist`, `dailysweep.plist`, `nassync.plist`, `ornith-loop.plist`, `ornith-night.plist`, `ornith-receipt.plist`, `shiftchange.plist`, `wake.plist`, each with ` (conflict_on_2026-09-17).template`.
`2_Project_Files/`: `doctor (conflict_on_2026-09-04).sh`, `doctor (conflict_on_2026-09-17).sh`. Workspace root: `CLAUDE (conflict_on_2026-09-17).md`.
Note for whoever arms: `install_all_jobs.sh` globs `*.plist.template`; the conflict copies end in `.template` but not `.plist.template`, so it skips them.

## H. Limits of this census

- Not read: `4_Credentials/`, `3_Access_Keys/` (contents), Tuesday's and Friday's tools, `Datasec/` on the share, Kam's `devnas-sync.sh` (only two `grep -c` counts were taken from `devnas.prf`).
- `0_Brain/reference` was not re-measured.
- Write speed to DEV-Working, whether DEV-Working keeps file times, and whether it accepts symlinks: unknown, because each needs a write. The design does not depend on any of the three.
- The sizes are today's. The seat tree's regenerable folders grow daily.
