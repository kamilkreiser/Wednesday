DONE

Task ANSWER-1, on Kam's ruling `wed-nas-backup-share-holds-secuura-credentials-1127` = a (live board 2026-11-27 13:36:06). The two named folders are moved and counted equal. **The sweep found 37 more secrets folders on the same mirror, eight of them further copies of the two just moved. I touched none of them: the ruling covers the two named folders only.**

## FOUND

1. **The two named folders are out of the mirror.** Both now sit in `/Volumes/Backup/_quarantine_2026-11-27_secuura-secrets/`, at the share's root, outside `DevMASTER-mirror`. All four figures match for each.
2. **Older copies of the same two folders are still inside the mirror.** `nas_push.sh` keeps what it replaces in `_nas_push_overwritten/<run stamp>/`. Four of those run folders (20261116, 20261117, 20261118, 20261119) each hold `!CODING/Secuura/Blockchain/4_Credentials` and `.../3_Access_Keys`: 8 folders.
3. **Five secrets folders of other projects are in the live mirror**, and 24 more copies of two of them are in the run folders (table below).
4. **Secret-shaped file names outside those folders:** 160 in the live mirror and 1,318 in the run folders (counts only, table below).
5. **The quarantine does not make the contents private** (limit, at the end).

## Before and after

| Folder | Where | Top-level entries | Files | Folders | Bytes |
|---|---|---|---|---|---|
| `4_Credentials` | before: `DevMASTER-mirror/!CODING/Secuura/Blockchain/` | 23 | 3,729 | 755 | 218,615,015 |
| | after: `_quarantine_2026-11-27_secuura-secrets/` | 23 | 3,729 | 755 | 218,615,015 |
| `3_Access_Keys` | before: same parent | 6 | 6 | 0 | 1,533 |
| | after: same quarantine | 6 | 6 | 0 | 1,533 |

Walk errors: 0 in all four counts. Both original paths: `os.path.exists` and `os.path.lexists` False. Positive control: the `Blockchain` parent still exists, with 113 entries (115 before). The quarantine folder holds exactly 2 entries. Re-checked at 14:09:54 after the sweep: unchanged.

## Sweep of the mirror (read-only, 13:39:37 to 14:09:49, 1,812.7 s)

179,291 folders and 1,550,773 files seen, 0 read errors. The walk records a secrets folder's own path and never enters it, so nothing inside any of them is counted below.

### Directories named `4_Credentials` or `3_Access_Keys` (case-insensitive): 37

| Where | Path under `DevMASTER-mirror/` | How many |
|---|---|---|
| Live mirror | `!CODING/Claude to Claude/claude-bridge/3_Access_Keys` | 1 |
| Live mirror | `!CODING/DESIGN_AGENT/3_Access_Keys` and `!CODING/DESIGN_AGENT/4_Credentials` | 2 |
| Live mirror | `!CODING/Personal Projects/Visualiser/3_Access_Keys` and `.../Visualiser/4_Credentials` | 2 |
| Run folders | `_nas_push_overwritten/<stamp>/!CODING/Secuura/Blockchain/4_Credentials` and `.../3_Access_Keys`, stamps 20261116, 20261117, 20261118, 20261119 | 8 |
| Run folders | `_nas_push_overwritten/<stamp>/!CODING/Claude to Claude/claude-bridge/3_Access_Keys`, every stamp from 20261115 to 20261126 | 12 |
| Run folders | `_nas_push_overwritten/<stamp>/!CODING/Personal Projects/Visualiser/4_Credentials`, every stamp from 20261115 to 20261126 | 12 |

The full list of 37 paths is in `evidence/secrets-move/08_sweep_full.json`. Positive control, run BEFORE the move with the same program on one level of the `Blockchain` parent: it found both known folders (`02_sweep_control_before_move.txt`). The full sweep ran after the move and, as it should, no longer lists them in the live mirror.

### Secret-shaped file names outside those folders (counts only)

| Top two levels under the mirror | `.env` / `.env.*` | `*.pem` | `*.key` | `*.p12` / `*.pfx` | `id_rsa` / `id_ed25519` | the `.pub` halves |
|---|---|---|---|---|---|---|
| `!CODING/Agentic Coding` | 39 | 0 | 0 | 0 | 0 | 0 |
| `!CODING/Claude to Claude` | 1 | 0 | 0 | 0 | 0 | 0 |
| `!CODING/Paperclip` | 5 | 0 | 1 | 0 | 0 | 0 |
| `!CODING/Secuura` | 111 | 3 | 0 | 0 | 0 | 0 |
| **Live mirror total** | **156** | **3** | **1** | **0** | **0** | **0** |
| `_nas_push_overwritten/20261115-033002` | 106 | 0 | 1 | 0 | 0 | 0 |
| `_nas_push_overwritten/20261116-033004` | 131 | 2 | 1 | 0 | 0 | 0 |
| `_nas_push_overwritten/20261117-033005`, `20261118-033002`, `20261119-033005` (each) | 106 | 2 | 1 | 0 | 0 | 0 |
| `_nas_push_overwritten/20261120-033004` | 106 | 1 | 1 | 0 | 0 | 0 |
| `_nas_push_overwritten/20261121-033004` to `20261126-033002` (six, each) | 106 | 0 | 1 | 0 | 0 | 0 |
| **Run folders total** | **1,297** | **9** | **12** | **0** | **0** | **0** |

A name of this shape is not proof of a secret (`.env.example` counts as `.env.*`; a `.key` can be a presentation). These are counts by name; no file was opened.

## TESTED

- `/Volumes/Backup` is the smbfs mount (`mount`: `//DotORG@192.168.20.154/Backup on /Volumes/Backup (smbfs, ...)`), checked at the start of every step.
- No copy job was running against the mirror at 13:39:17: `pgrep -fl nas_push` rc 1 (nothing); `pgrep -fl unison` rc 1; `pgrep -fl rsync` rc 0 with five rows, none of them rsync (the pattern matches inside `colorsync`, `postersyncd`, `appplaceholdersyncd`); `launchctl list` shows `com.wednesday.naspush` loaded with no pid.
- The quarantine folder did not exist before; `os.mkdir` rc 0.
- Each rename rc 0, read before the next step: `4_Credentials` at 13:39:23, `3_Access_Keys` at 13:39:27. `os.rename` only; the program has no copy path and no delete verb.
- Counts after equal counts before, for both folders, all four figures.

## NOT tested

- **Content.** By instruction no file was opened or hashed, so "the same files" rests on entry, file and folder counts and total bytes, not on a content comparison.
- **Wednesday's edit to `nas_push.sh`** (the two new excludes). Not mine and not exercised. Tonight's 03:30 run is its first test.
- **Whether those excludes cover everything the sweep found.** An exclude stops new copies; it removes nothing already on the share, and it does not cover `.env`, `*.pem` or `*.key` names.
- **Anything inside the 37 folders the sweep found**, including whether the eight Secuura copies in the run folders are complete copies.
- **Other shares.** Only `DevMASTER-mirror` on the Backup share was swept.

## HOW

Two programs, written for this task, both under `evidence/secrets-move/`: `secrets_move.py` (`list`, `mkquar`, `move <name>`, `after`) and `sweep.py`. Each step was one command, its exit code written into its own evidence file.

| Step | Command | rc | Evidence |
|---|---|---|---|
| List first | `secrets_move.py list before.json` | 0 | `01_list.txt`, `before.json` |
| Sweep control, before the move | `sweep.py <Blockchain parent> 1 ...` | 0 | `02_sweep_control_before_move.txt` |
| Process check | `pgrep -fl` three patterns, `launchctl list` | as above | `03_process_check.txt` |
| Create the quarantine | `secrets_move.py mkquar` | 0 | `04_mkquar.txt` |
| Move 1 | `secrets_move.py move 4_Credentials` | 0 | `05_move_4_Credentials.txt` |
| Move 2 | `secrets_move.py move 3_Access_Keys` | 0 | `06_move_3_Access_Keys.txt` |
| Count after | `secrets_move.py after before.json after.json` | 0 | `07_after.txt`, `after.json` |
| Full sweep, background | `sweep.py /Volumes/Backup/DevMASTER-mirror 0 ...` | 0 | `08_sweep_full.txt`, `08_sweep_full.json` (stderr file empty) |

The first command's exit code did not print on screen (a shell variable that is empty in zsh); its evidence is the two `BEFORE` lines and the `before.json` it wrote, which the program only writes on its success path. Every later step records its rc.

## Noticed

- **The quarantine is half the job.** Eight more copies of the same two Secuura folders remain on the share in the run folders of 16 to 19 November. Moving them is the same kind of action as the one Kam approved, but they are not the two folders his ruling names, so they are reported, not moved.
- **Three other projects' secrets folders are in the live mirror** (`claude-bridge`, `DESIGN_AGENT`, `Visualiser`), with twelve nightly copies each of two of them. Those are general projects, not Secuura.
- **The run folders show which nights the job rewrote which secrets folders**: the Secuura pair on four nights only, the other two every night from 15 to 26 November.
- `_nas_push_overwritten` is inside `DevMASTER-mirror`, and `nas_push.sh` excludes that name from its own copy, so the job does not re-read it. It also never prunes it.

## Limit, said plainly

The quarantine folder is on the same share. Whoever can read the Backup share can still read everything in it, exactly as before: the move changed where the folders are, not who can see them. Whether the keys and credentials in it should be rotated, and whether the folder (and the other 37) should be removed from the NAS, is Kam's next decision. It is not mine and not Wednesday's.

Nothing committed, nothing pushed. No lane code, test, proposal, STATUS.md, README.md or CENSUS.md was edited for this task.
