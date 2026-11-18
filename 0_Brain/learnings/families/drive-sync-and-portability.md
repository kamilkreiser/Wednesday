---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Drives, syncs and portability: what travels, what does not, and when a copy is really done

**The one idea.** The project must be able to wake up on another drive or another machine and work. A sync copies bytes, not intentions: absolute paths travel frozen, git carries only tracked files, a half-finished copy leaves folders that look complete, and conflict copies arrive already matching every file pattern. So everything lives on the drive, everything machine-local is listed and checked at boot, and no copy is called done until it has been counted on both sides.

## The rules

1. **When I add a tool, state or config:** keep it on the drive, under the project folder (tools under `2_Project_Files/tools/`), even if the machine has its own copy. Scripts and launchers locate themselves from their own path. Anything unavoidably machine-local (voice downloads, keychain items, installed daemons, the assistant software itself) must degrade gracefully elsewhere and be listed in `PORTABILITY.md` with a check in `doctor.sh`, added in the same session. The older half of this lesson ("the T9 drive is the master") is superseded: see rule 2. `2026-07-31_fully-portable-drive.md`

2. **Which drive is which:** DevMASTER is the master; the travel drive must carry everything; the T9 is a backup copy. No path to an old volume name may appear in a tracked file. `.git` does not travel by drive sync: the repository moves by git (pull, push); a `.git` that arrived by copy is a snapshot and needs a pull before use. The drive sync also drops file modes, so executable bits and key permissions need the additive copy that preserves them (and a recheck afterwards). Seats have since moved machines and drives; read the current home from the machine, do not assume it. `2026-08-25_one-drive-devmaster-is-master.md`, `2026-11-11_wednesday-lives-on-the-mac-mini.md`

3. **When both a master and a copy exist and I am about to launch:** sync first, verify content at the destination, THEN launch. A session launched from a stale copy writes a fork. `2026-08-25_one-drive-devmaster-is-master.md`

4. **After a drive sync, or at first boot on another machine:** expect every stored absolute path to be stale (the repo's ssh command pointing at a key on the old volume, launcher lists, hardcoded watch-lists, even a strict parser's assumptions). Heed the boot check's travel-pointer warnings and ROUTE them: the project's own launcher heals its pointer at its next launch, or its own agent repoints it; I never edit another project's repository. One client's launcher refreshes its pointer only conditionally, so flag that in the brief when launching it away from its home machine. When adding any mechanism, ask "what absolute path am I storing, and what happens when this wakes up on a different volume?"; prefer self-location, and add any unavoidable absolute to the boot sweep the same session. `2026-08-25_travel-drive-stale-pointers.md`

5. **When I launch agents on a laptop:** arm `caffeinate -dims` for the expected duration in the same action as the launch; a sleeping laptop kills turns mid-response. After a dead turn, re-verify what it wrote before resuming. `2026-08-25_travel-drive-stale-pointers.md`

6. **When I boot or run a tool on a machine that is new to the seat:** check the host alias, binary path and volume the tool names before trusting it. A return code 1 from a copy tool is read first as "wrong binary" (the system's stock copy tool lacks options the scripts use), not "nothing to copy". In zsh, `log` is a shell builtin; read system logs with `/usr/bin/log`. (Wednesday seat's lesson; the method holds for any seat.) `2026-11-11_wednesday-lives-on-the-mac-mini.md`

7. **When two seats on the same framework behave differently:** before diffing tracked files, enumerate what is NOT in git: ignored config files (hooks and guards live in one), machine-installed scheduled jobs, credential stores, anything installed rather than checked out, and habits. Then: anything that shapes behaviour goes into a tracked template plus a renderer the launcher runs at every boot (merging policy keys, keeping local ones); a missing guard is a boot-check FAIL, never a warning; a skipped step must print what it skipped and what that costs, as a number; and a habit is not a mechanism (test: if a cold seat replaced this one tonight, would it still happen? if not, put it in the launcher). When a system blames the agent, measure the environment first. `2026-09-16_what-keeps-a-seat-correct-is-not-all-in-git.md`

8. **When I sync, copy, move, migrate or free space:** I do not say "done" until every top-level folder (and each project folder) has been counted, files and bytes, on both sides, and the table has gone to Kam. A clean exit code is not proof; a copy that was interrupted is not done. Empty on one side and full on the other is an alarm: report it before anything else touches either side, and never resolve it by deleting or by assuming the empty side is right. Syncs never delete: no `--delete`, no deletion propagation, no mirror; replaced files go to a dated backup folder. An interrupted long copy leaves `_INCOMPLETE_COPY_<date>.txt` at the destination root naming what is missing. Where the 2026-08-25 lesson describes the travel sync as a two-way engine, this newer rule governs its deletions. `2026-10-15_a-sync-is-not-done-until-every-folder-is-counted-on-both-sides.md` (over `2026-08-25_one-drive-devmaster-is-master.md`)

9. **When freeing space:** quarantine first, always with Kam's yes. List candidates with sizes; he picks; move them to `_quarantine_<date>` or prove a second copy exists by count (a folder of the same name is not a copy). Nothing goes because it "looks old", "looks rebuildable" or "is empty here". Truly empty folders are removed only after the copy that could refill them has finished, never inside `.git`, dependency folders, virtual environments, hidden tool folders or templates, and every removed path is recorded with a one-command re-create script. `2026-10-15_a-sync-is-not-done-until-every-folder-is-counted-on-both-sides.md`

10. **When I write a file pattern (glob) over a synced brain folder:** exclude `(conflict_on_` files; a bare date glob there is a defect on sight, because the sync creates conflict copies that match it and readers then serve stale duplicates. Never delete the conflict copies and do not rename them either; leave them on disk and exclude them from readers. Diff a conflict copy before assuming it is junk (it may be a lost edit). `2026-09-10_a-sync-conflict-copy-is-an-input-to-every-glob.md`

11. **When a rule is withdrawn, superseded or narrowed:** amend the HEADING in the same edit, not only the body. Digests carry headings only, so a retraction left in the body is still served as the live rule. `2026-09-10_a-sync-conflict-copy-is-an-input-to-every-glob.md`

12. **When I write, copy or move any file:** name its folder before its filename. The project root holds only `CLAUDE.md`, `PORTABILITY.md`, `.gitignore` and the `Launch_*.command` launchers (a `.pre-*` backup of a root script may sit beside it). Screenshots and renders go to `0_Brain/reference/<date>_<topic>/`, session artefacts to `5_Project_History/`, scratch to the session scratchpad. A file for Kam to open still goes in its folder; the pointer goes in the message. Misfiled files are moved, never deleted. `2026-09-05_root-folder-holds-only-rules-and-launchers.md`

13. **When a seat backs up or offloads (large evidence, old worktrees, a copy before a risky change):** use that seat's offload tool into the NAS share `DEV-Working`, in a dated, named folder under its own client: Tuesday uses `2_Project_Files/tuesday/tools/nas_offload.sh` into `Datasec/Tuesday/<date>_<topic>/`; Wednesday uses `2_Project_Files/tools/nas_offload.sh --client secuura|general` into `<Client>/Wednesday/<date>_<topic>/`. Never hand-copy (the manifest is what makes clean-up possible). One client per offload, and never read, list or write the other client's folder. Copy, never move: removing a source afterwards is a separate step, only after VERIFIED, only inside the seat's own tree, and quarantine rules still apply. No secrets. If the share is not mounted, say so and ask Kam; never create the mount path by hand (it would write to the local disk). Do not confuse this new NAS with the old one used by the nightly mirror. `2026-11-11_nas-dev-working-dated-offload.md` (Tuesday), `2026-11-11_wednesday-offloads-to-dev-working-nas.md` (Wednesday)

## What a tool already enforces

- `2_Project_Files/doctor.sh` sweeps each project repository's stored ssh command at boot and warns on a path that does not exist on this machine (rule 4). It warns only; the repair is routed to the owning project.
- `2_Project_Files/doctor.sh` checks the machine-local, untracked layers found missing in rule 7 (the hook and guard config). It sees only what has been given a check: "if the boot check does not check it, it does not exist".
- `2_Project_Files/tools/boot_digest.py` excludes conflict copies from its glob (rule 10). It does not protect other globs, and it cannot fix a heading that still states a withdrawn rule.
- `2_Project_Files/tuesday/tools/nas_offload.sh` and `2_Project_Files/tools/nas_offload.sh` make the dated folder, verify every file by checksum, write the manifest with a review date 30 days on, and refuse secrets, an existing folder, an unmounted share and (Wednesday's) the other client's sources. The checksum-mismatch path was not exercised. Neither tool deletes anything.

## Grants and their limits

- Seats may offload to the NAS without asking, through the tool, within their own client folder.
- Deleting an offload folder past its review date, removing quarantined material, choosing what is cleared to free space, and repointing the old nightly mirror stay Kam's.

## The mistakes this family keeps catching

- A folder exists at the destination, so the copy is assumed complete.
- "The logins were not copied" diagnosed, when the truth is that a pointer came along frozen.
- Two seats compared by diffing tracked files while the real difference is in what git never carries.
- A file pattern written without asking what else could match it.
- A step that silently skips, with a hint instead of a measurement.
- A file dropped in the root because it was the shortest path to something openable.

## Members

- `2026-07-31_fully-portable-drive.md` — When I add a tool, state or config: keep it on the drive (2_Project_Files/tools/), keep scripts self-locating, list anything machine-local in PORTABILITY.md and doctor.sh. (The 'T9 is master' half is superseded: DevMASTER is master.)
- `2026-08-25_one-drive-devmaster-is-master.md` — DevMASTER is the master drive; the T9 and travel drive are sync copies. Sync, verify content at the destination, THEN launch (a stale copy writes a fork). .git travels by git, not drive sync. No old-volume absolute paths in tracked files.
- `2026-08-25_travel-drive-stale-pointers.md` — After a drive sync or first boot on another machine: absolute paths (core.sshCommand, launcher confs, hardcoded lists) travel frozen; heed doctor's travel-pointers warnings and route them to the project launcher. Arm caffeinate when launching on a laptop.
- `2026-09-05_root-folder-holds-only-rules-and-launchers.md` — When writing or moving any file: name its folder first. The root holds only CLAUDE.md, PORTABILITY.md, .gitignore and Launch_*.command. Screenshots go to 0_Brain/reference/<date>_<topic>/, artefacts to 5_Project_History/, scratch to scratchpad. Never delete.
- `2026-09-10_a-sync-conflict-copy-is-an-input-to-every-glob.md` — When writing a glob over a synced brain folder: exclude '(conflict_on_' files, never delete or rename them. When a rule is withdrawn or narrowed, amend the HEADING in the same edit, since digests carry only headings.
- `2026-09-16_what-keeps-a-seat-correct-is-not-all-in-git.md` — When two seats on one framework behave differently: enumerate what is NOT in git first (gitignored config, machine daemons, habits). Behaviour-shaping config goes in a tracked template plus renderer; a guard missing is a doctor FAIL; a skip prints its cost.
- `2026-10-15_a-sync-is-not-done-until-every-folder-is-counted-on-both-sides.md` — When I sync, copy, move or free space: never say done until every top-level folder is counted (files, bytes) on both sides; empty-here/full-there is an alarm; no --delete, quarantine with Kam's yes, prove a second copy by count.
- `2026-11-11_nas-dev-working-dated-offload.md` — When Tuesday backs up or offloads: use tuesday/tools/nas_offload.sh into DEV-Working/Datasec/Tuesday/<date>_<topic>/ (verified, MANIFEST, REVIEW-AFTER +30d). Copy never move, no secrets, never touch Secuura/, delete past review only on Kam's word.
- `2026-11-11_wednesday-lives-on-the-mac-mini.md` — When booting or running a tool on a new machine: check the host alias, binary path and volume it names before trusting it. rc 1 from a copy tool means wrong binary first; in zsh use /usr/bin/log. Spark alias part is dead; seat home may have moved since.
- `2026-11-11_wednesday-offloads-to-dev-working-nas.md` — When Wednesday backs up or offloads: use tools/nas_offload.sh --client secuura|general into DEV-Working/<Client>/Wednesday/<date>_<topic>/. One client per offload, never Datasec, no secrets, copy never move, delete past REVIEW-AFTER only on Kam's word.
