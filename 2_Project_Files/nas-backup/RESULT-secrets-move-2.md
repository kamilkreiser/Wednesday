DONE

Task ANSWER-4 TASK 1, on Kam's ruling `wed-nas-mirror-37-more-secrets-folders-1127` = a (live board 2026-11-27 16:40:18: "Move all 37 aside, same method"). The 37 folders named `4_Credentials` or `3_Access_Keys` that the earlier sweep listed under `/Volumes/Backup/DevMASTER-mirror` are moved into the existing quarantine folder and counted equal. Nothing was opened, nothing was deleted, nothing else on any NAS mount was touched.

## FOUND

1. **The set was exactly the listed 37.** A fresh read-only sweep of the mirror (16:44:04 to 17:13:21, 1,757 s, 179,291 folders and 1,550,773 files seen, 0 read errors: the same totals as the earlier sweep) found 37 such folders, and every one is one of the 37 in `evidence/secrets-move/08_sweep_full.json`: 5 in the live mirror, 32 under `_nas_push_overwritten/<stamp>/`. No path outside the list, none of the list missing.
2. **All 37 are moved.** Each went by ONE same-share rename to `/Volumes/Backup/_quarantine_2026-11-27_secuura-secrets/more/<its path under DevMASTER-mirror>`, so two folders of the same name never meet. Each rename's exit code was 0 and was read before the next one started. For each folder the four figures at its new place equal the four figures before; each original path is gone; each original parent folder is still there.
3. **The first two folders in the quarantine were not touched.** The quarantine's top level holds exactly three entries: `3_Access_Keys`, `4_Credentials` (the two from ANSWER-1) and `more`.
4. **What the 37 held, in counts only:** 13,072 files, 2,498 folders, 791,587,477 bytes. Almost all of it is the four dated copies of Secuura Blockchain's `4_Credentials` (13,009 files, 791,571,101 bytes together). Three of the five live-mirror folders were empty.
5. **Files with secret-looking NAMES outside those folders are left where they are**, as ruled. Their counts are in the AFTER-SWEEP section for Kam's later card.

## Before and after, one row per folder

Counts by a program (`os.walk`, hidden names included, metadata only): top-level entries, files, folders, bytes. Walk errors: 0 in every count.

| # | Path under `DevMASTER-mirror/` | Entries before / after | Files before / after | Folders before / after | Bytes before / after | Equal |
|---|---|---|---|---|---|---|
| 1 | `!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 2 | `!CODING/DESIGN_AGENT/3_Access_Keys` | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | yes |
| 3 | `!CODING/DESIGN_AGENT/4_Credentials` | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | yes |
| 4 | `!CODING/Personal Projects/Visualiser/3_Access_Keys` | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | yes |
| 5 | `!CODING/Personal Projects/Visualiser/4_Credentials` | 3 / 3 | 1 / 1 | 2 / 2 | 218 / 218 | yes |
| 6 | `_nas_push_overwritten/20261115-033002/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 7 | `_nas_push_overwritten/20261115-033002/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 8 | `_nas_push_overwritten/20261116-033004/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 9 | `_nas_push_overwritten/20261116-033004/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 10 | `_nas_push_overwritten/20261116-033004/!CODING/Secuura/Blockchain/3_Access_Keys` | 6 / 6 | 6 / 6 | 0 / 0 | 1,533 / 1,533 | yes |
| 11 | `_nas_push_overwritten/20261116-033004/!CODING/Secuura/Blockchain/4_Credentials` | 20 / 20 | 3,550 / 3,550 | 721 / 721 | 216,699,205 / 216,699,205 | yes |
| 12 | `_nas_push_overwritten/20261117-033005/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 13 | `_nas_push_overwritten/20261117-033005/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 14 | `_nas_push_overwritten/20261117-033005/!CODING/Secuura/Blockchain/3_Access_Keys` | 6 / 6 | 6 / 6 | 0 / 0 | 1,533 / 1,533 | yes |
| 15 | `_nas_push_overwritten/20261117-033005/!CODING/Secuura/Blockchain/4_Credentials` | 22 / 22 | 3,563 / 3,563 | 732 / 732 | 217,559,380 / 217,559,380 | yes |
| 16 | `_nas_push_overwritten/20261118-033002/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 17 | `_nas_push_overwritten/20261118-033002/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 18 | `_nas_push_overwritten/20261118-033002/!CODING/Secuura/Blockchain/3_Access_Keys` | 6 / 6 | 6 / 6 | 0 / 0 | 1,533 / 1,533 | yes |
| 19 | `_nas_push_overwritten/20261118-033002/!CODING/Secuura/Blockchain/4_Credentials` | 22 / 22 | 3,578 / 3,578 | 747 / 747 | 218,237,357 / 218,237,357 | yes |
| 20 | `_nas_push_overwritten/20261119-033005/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 21 | `_nas_push_overwritten/20261119-033005/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 22 | `_nas_push_overwritten/20261119-033005/!CODING/Secuura/Blockchain/3_Access_Keys` | 6 / 6 | 6 / 6 | 0 / 0 | 1,533 / 1,533 | yes |
| 23 | `_nas_push_overwritten/20261119-033005/!CODING/Secuura/Blockchain/4_Credentials` | 18 / 18 | 2,318 / 2,318 | 296 / 296 | 139,075,159 / 139,075,159 | yes |
| 24 | `_nas_push_overwritten/20261120-033004/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 25 | `_nas_push_overwritten/20261120-033004/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 26 | `_nas_push_overwritten/20261121-033004/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 27 | `_nas_push_overwritten/20261121-033004/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 28 | `_nas_push_overwritten/20261122-033005/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 29 | `_nas_push_overwritten/20261122-033005/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 30 | `_nas_push_overwritten/20261123-033002/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 31 | `_nas_push_overwritten/20261123-033002/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 32 | `_nas_push_overwritten/20261124-033004/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 33 | `_nas_push_overwritten/20261124-033004/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 34 | `_nas_push_overwritten/20261125-033002/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 35 | `_nas_push_overwritten/20261125-033002/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| 36 | `_nas_push_overwritten/20261126-033002/!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 2 / 2 | 2 / 2 | 0 / 0 | 570 / 570 | yes |
| 37 | `_nas_push_overwritten/20261126-033002/!CODING/Personal Projects/Visualiser/4_Credentials` | 1 / 1 | 1 / 1 | 0 / 0 | 218 / 218 | yes |
| | **Totals, 37 folders** | **147 / 147** | **13,072 / 13,072** | **2,498 / 2,498** | **791,587,477 / 791,587,477** | **37 of 37** |

By group (before the move):

| Where it was | Folder | How many | Files in all | Bytes in all |
|---|---|---|---|---|
| Live mirror | `!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 1 | 2 | 570 |
| Live mirror | `!CODING/DESIGN_AGENT/3_Access_Keys` and `.../4_Credentials` | 2 | 0 | 0 |
| Live mirror | `!CODING/Personal Projects/Visualiser/3_Access_Keys` | 1 | 0 | 0 |
| Live mirror | `!CODING/Personal Projects/Visualiser/4_Credentials` | 1 | 1 | 218 |
| Run folders, 12 stamps (20261115 to 20261126) | `.../Claude to Claude/claude-bridge/3_Access_Keys` | 12 | 24 | 6,840 |
| Run folders, 12 stamps (20261115 to 20261126) | `.../Personal Projects/Visualiser/4_Credentials` | 12 | 12 | 2,616 |
| Run folders, 4 stamps (20261116 to 20261119) | `.../Secuura/Blockchain/3_Access_Keys` | 4 | 24 | 6,132 |
| Run folders, 4 stamps (20261116 to 20261119) | `.../Secuura/Blockchain/4_Credentials` | 4 | 13,009 | 791,571,101 |
| **All** | | **37** | **13,072** | **791,587,477** |

## AFTER-SWEEP (read-only, 17:17:42 to 17:38:46, 1,263.9 s)

**0 folders named `4_Credentials` or `3_Access_Keys` (any case) are left under `/Volumes/Backup/DevMASTER-mirror`.**

- The sweep saw 179,254 folders and 1,550,773 files with 0 read errors. Before the move it saw 179,291 folders and 1,550,773 files: exactly 37 folders fewer, and the same number of files (the sweep never enters a secrets folder, so the files inside them were in neither count).
- **Positive control, outside the NAS:** the same program on a scratch folder holding one folder named `4_Credentials` and one named `3_access_keys` (lower case, two levels down) beside an ordinary file found both (2 of 2). So a zero from it is a zero it could have failed to give.
- **The quarantine's own count:** the same program on `/Volumes/Backup/_quarantine_2026-11-27_secuura-secrets` found 39 such folders: 2 at its top level (the two from ANSWER-1) and 37 under `more/`. 0 read errors. It saw no file outside those 39 folders.

### Files with secret-looking names, left where they are (counts only, for Kam's later card)

By name only; no file was opened. Identical before and after the move, as expected: none of these files was inside a moved folder.

| Where under the mirror | `.env` / `.env.*` | `*.pem` | `*.key` | `*.p12` / `*.pfx` | `id_rsa` / `id_ed25519` (and `.pub`) | All |
|---|---|---|---|---|---|---|
| `!CODING/Agentic Coding` | 39 | 0 | 0 | 0 | 0 | 39 |
| `!CODING/Claude to Claude` | 1 | 0 | 0 | 0 | 0 | 1 |
| `!CODING/Paperclip` | 5 | 0 | 1 | 0 | 0 | 6 |
| `!CODING/Secuura` | 111 | 3 | 0 | 0 | 0 | 114 |
| **Live mirror** | **156** | **3** | **1** | **0** | **0** | **160** |
| `_nas_push_overwritten/20261115-033002` | 106 | 0 | 1 | 0 | 0 | 107 |
| `_nas_push_overwritten/20261116-033004` | 131 | 2 | 1 | 0 | 0 | 134 |
| `_nas_push_overwritten/20261117-033005`, `20261118-033002`, `20261119-033005` (each) | 106 | 2 | 1 | 0 | 0 | 109 |
| `_nas_push_overwritten/20261120-033004` | 106 | 1 | 1 | 0 | 0 | 108 |
| `_nas_push_overwritten/20261121-033004` to `20261126-033002` (six, each) | 106 | 0 | 1 | 0 | 0 | 107 |
| **Run folders, 12 stamps** | **1,297** | **9** | **12** | **0** | **0** | **1,318** |
| **All** | **1,453** | **12** | **13** | **0** | **0** | **1,478** |

A name of this shape is not proof of a secret (`.env.example` counts as `.env.*`; a `.key` can be a presentation). The thirteenth run folder on the share, `_nas_push_overwritten/20261114-033005`, holds none of these names and none of the 37 folders.

## TESTED

- `/Volumes/Backup` is the smbfs mount (`//DotORG@192.168.20.154/Backup on /Volumes/Backup (smbfs, ...)`), read at 16:43:57 and again at 17:15:16, and checked by the program before every step.
- No copy job was running against the mirror at 17:15:16, 50 seconds before the first rename: `pgrep -fl nas_push` rc 1 (nothing); `pgrep -fl unison` rc 1; `pgrep -fl rsync` rc 0 with five rows, none of them rsync (the pattern matches inside `colorsync`, `postersyncd`, `appplaceholdersyncd`); `launchctl list` shows `com.wednesday.naspush` loaded with no pid. `pgrep -fl nb_core` showed one row: my own shell running a name scan of a file list in the scratchpad, which reads no NAS path. Tonight's 03:30 `naspush` run had not happened.
- The set check, by a program: 37 found, 37 listed, 0 not on the list, 0 of the list missing, 37 distinct destinations, 0 destinations already existing (`03_check.txt`, rc 0).
- Each of the 37 renames: rc 0, `os.rename` only. Before each one the program counted the folder again and compared with the list step's counts (a change would have stopped it); after each one it counted the folder at its new place. 37 lines read `equal: True | original path gone: True | its parent still present: True`; 0 lines carry STOP or Traceback (control: 37 lines carry MOVED). First rename 17:16:06, last 17:16:59.
- The count after, as its own step: 37 of 37 equal, 37 original paths absent, totals equal (`07_after.txt`, rc 0). Positive control: the mirror folder itself still exists.
- The program was rehearsed first on a scratch copy of a made-up share (three folders, one of them under a run folder): moves, a refused second move of the same folder (rc 14, "destination already exists"), counts and sweeps behaved as written. That rehearsal touched nothing on the NAS.

## NOT tested

- **Content.** By instruction no file was opened or hashed. "The same files" rests on entry, file and folder counts and total bytes for each folder, not on a content comparison.
- **Whether tonight's 03:30 `naspush` run re-creates any of them.** Wednesday's edit of 13:36 added both names to that job's excludes; it has not run since. If it does re-create one, the next sweep would show it.
- **Whether the left-behind parent folders in the run folders are now empty or still hold other files.** I counted the moved folders, not their neighbours.
- **Anything on the other shares.** Only `DevMASTER-mirror` on the Backup share was swept. `/Volumes/DEV-Working` and `/Volumes/Seagate Hub` were not looked at for this task.
- **The files with secret-looking names** (below): not opened, not moved, only counted by name.

## HOW

One program written for this task, `evidence/secrets-move-2/secrets_move_2.py` (verbs: `check`, `before`, `move <n>`, `after`), and the earlier seat's `evidence/secrets-move/sweep.py` run from where it lies. The program has no copy path and no delete verb; its only writes are `os.makedirs` for the parents of a destination inside the quarantine and one `os.rename` per call.

| Step | Command | rc | Evidence (`evidence/secrets-move-2/`) |
|---|---|---|---|
| Mount, processes, share's top level | `mount`, `pgrep -fl` four patterns, `launchctl list`, `os.listdir` | as above | `01_precheck.txt` |
| Fresh sweep, background | `sweep.py /Volumes/Backup/DevMASTER-mirror 0 ...` | 0 | `02_sweep_before.json`, `.txt`, `.err` (empty) |
| Is the set exactly the 37 | `secrets_move_2.py check <old sweep> <fresh sweep> plan.json` | 0 | `03_check.txt`, `plan.json` |
| Process check again | as the first row | as above | `04_process_check.txt` |
| Count before | `secrets_move_2.py before plan.json before.json` | 0 | `05_before.txt`, `before.json` |
| 37 moves, one call each, stop at the first non-zero rc | `secrets_move_2.py move plan.json before.json <n>` | 0, 37 times | `06_moves.txt` |
| Count after | `secrets_move_2.py after plan.json before.json after.json` | 0 | `07_after.txt`, `after.json` |
| Sweep control outside the NAS | `sweep.py <scratch folder with two planted names> 0 ...` | 0 | `08_sweep_control_outside_the_nas.*` |
| The quarantine's own count | `sweep.py /Volumes/Backup/_quarantine_2026-11-27_secuura-secrets 0 ...` | 0 | `09_sweep_quarantine.*` |
| Second sweep of the mirror, background | `sweep.py /Volumes/Backup/DevMASTER-mirror 0 ...` | 0 | `10_sweep_after.*` |

## Limit, said plainly, again

The quarantine folder is on the same share. Whoever can read the Backup share can still read everything in it, exactly as before: the move changed where these 39 folders are, not who can see them. The keys and credentials in them are as exposed as they were this morning. Whether they should be rotated, and whether the quarantine should be removed from the NAS, is Kam's next decision. It is not mine and not Wednesday's.

Nothing committed, nothing pushed.
