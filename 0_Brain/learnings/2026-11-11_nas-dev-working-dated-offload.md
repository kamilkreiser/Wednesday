---
date: 2026-11-11
type: preference
source: Kam, Tuesday terminal, 2026-11-11 ~09:00 AEDT
status: live
tier: W
---

# Backups and offloads go to the DEV-Working NAS, in a dated, named folder, so they can be cleaned up

**Kam's words, verbatim:** *"there is a new NAS on the network with a folder called DEV-Working. If you need to backup or offload anything there you can use that drive. Put it in a logical folder and with a date so we can periodically clean this up. please save this as an ongoing workflow"*

**The rule:**
1. Whenever this seat needs to back up or offload anything (large evidence, old worktrees, a copy before a risky change, files crowding a drive), it goes to `/Volumes/DEV-Working/Datasec/Tuesday/<YYYY-MM-DD>_<topic-kebab>/` through **`2_Project_Files/tuesday/tools/nas_offload.sh <topic> "<why>" <source...>`**. That tool makes the dated folder, copies with rsync, verifies every file by sha256, and writes `MANIFEST.txt` (date, why, sources, per-file hashes, **REVIEW-AFTER = +30 days**). Do not hand-copy: the manifest is what makes the clean-up possible.
2. **Client isolation:** this seat writes only under `DEV-Working/Datasec/`. The share also holds `Secuura/` (the Wednesday seat's): never read, list or write it. A folder per client is hard rule #2 applied to a shared drive.
3. **Copy, never move.** The tool never deletes the source. Removing a source after an offload is a separate step, done only after `VERIFIED`, and only where deletion is otherwise allowed (inside this seat's own tree; never in a project folder, which is read-only to this seat; quarantine rules still apply).
4. **No secrets on the NAS:** nothing from `4_Credentials/` or `3_Access_Keys/`, no `.env`, keys or certificates (the tool refuses them).
5. **Clean-up:** a folder past its REVIEW-AFTER date is listed for Kam at a weekly consolidation (or when he asks), and deleted only on his word. Kam's purpose is periodic clean-up, so the dates and manifests are the point, not decoration.
6. **Mount is a floating pointer:** the share is SMB from the NAS (`//DotORG@192.168.20.154/DEV-Working`, mounted by Kam's login). Before an offload, the tool checks the share is really mounted (smbfs), because an unmounted `/Volumes/DEV-Working` path would quietly write onto the local disk. If it is absent, say so and ask Kam to mount it; never create the path by hand.

**Measured at setup (2026-11-11 09:00):** mounted smbfs, 11 TiB, 1% used, writable (probe written and read back, filed at `Datasec/Tuesday/_probes/`). Tool exercised before use: one verified copy (`2026-11-11_workflow-selftest`, 4 files incl. nested and spaced names, manifest checked) and four refusals (existing folder, `.env` inside a source, a non-kebab topic, a `4_Credentials` path). Not exercised: the sha256-mismatch path (it would need a file changed mid-copy).

Related: [[2026-07-31_fully-portable-drive]] (the NAS is a machine/network dependency: PORTABILITY + doctor), [[2026-08-13_shared-bus-tag-filter-or-leak]] (client isolation on shared things), [[2026-08-07_a-check-that-cannot-fail]] (the mount check).
