---
date: 2026-10-15
type: correction
tier: W
source: Kam, terminal to Friday 2026-10-15 ~13:2x AEDT
status: live
---

# A sync is not done until every folder is counted on both sides; never delete or "clean space" on the strength of a folder existing

**Kam's words (verbatim):** *"so at some point these directories got deleted and lost. Not good. please make sure this never
happens again especially through syncs or cleaning of space."*

## What happened (measured 2026-10-15)
On the Laptop-DEV drive, `Family`, `Meeting Notes and Transcripts`, `!SYNC FILES` (plus `Setup and System`, `QA_AGENT`, `SYSTEM`,
`_handover`, `.app-source`, `.scripts`, `!CODING/_New_Project`, …) existed but held **0 files**. The T9 still held them: Family 31 files
/ 71 MB, Meeting Notes 3, !SYNC FILES 9. Every empty folder is stamped `2026-09-25 11:41:12`. That day at 11:42 Kam had formatted
the drive and Wednesday started a one-way DevMASTER → Laptop-DEV rsync (daily/2026-09-25.md 11:42, 12:56: ≈7.5 MiB/s, ≈39 h ETA).
rsync creates the directory tree first, so the drive moved to the laptop (2026-09-28) before the copy reached those folders.
**Not a deletion: an unfinished copy that looked finished because the folders were there.** Nobody counted files at the
destination against the source, and two later syncs and three weeks of work treated the drive as complete.

## The rules (every seat, every sync, every space clean-up)
1. **A copy or sync is DONE only when it has been counted.** For each top-level folder (and each project folder), compare
   file count and bytes, source against destination. "rsync exited 0" is not the proof. A copy that was never allowed to finish
   is not done, whatever its exit code.
2. **Empty on one side, full on the other, is an ALARM.** Report it before anything else touches either side. Never resolve it
   by deleting, and never by assuming the empty side is right.
3. **Syncs never delete.** No `--delete`, no unison deletion propagation, no "mirror". Files that would be replaced go to a
   dated backup folder (`--backup --backup-dir`), never to oblivion.
4. **Cleaning space is quarantine first, always with Kam's yes.** List candidates with sizes; Kam picks; move them to a
   `_quarantine_<date>` folder (or confirm a second copy exists elsewhere, counted) before any removal. Nothing is removed because
   it "looks old", "looks rebuildable" or "is empty on this side".
5. **Before removing anything, prove a second copy exists, by count, not by name.** A folder of the same name is not a copy.
6. **Interrupted copies leave a marker.** If a long copy must be interrupted, write `_INCOMPLETE_COPY_<date>.txt` at the
   destination root naming what was not copied. The next seat reads it before trusting the drive.
7. **Removing truly empty folders (Kam asked, 2026-10-15):** only after the copy that could refill them has finished; never
   inside `.git`, `node_modules`, virtualenvs, hidden tool folders or project templates; every removed path is recorded in a
   file with a one-command re-create script beside it.

## How to apply
Any seat asked to sync, move, copy, mirror, migrate or free space runs rules 1–5 as its checklist. It reports the per-folder
count table to Kam BEFORE saying "done".
