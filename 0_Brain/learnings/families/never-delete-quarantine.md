---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Never delete: cleanup means quarantine, and removal is Kam's word

**The one idea.** Deletion is the one file operation that cannot be undone from inside the system; a duplicate, a stale copy or a folder in the wrong place is only a tidiness cost that can be paid later with full information. Kam prefers the tidiness cost ("Do not delete any files, especially files that we are working on"). So nothing I run, recommend, configure or schedule removes a file; what needs to go is moved somewhere dated and findable, and the few narrow classes that may really be deleted are deleted on Kam's word by the seat that owns them.

## The rules

1. **When a task seems to need a delete:** I use no delete verbs. No `rm`, no `git stash drop`, no `git checkout --` over uncommitted work, no `rsync --delete`, no two-way sync leg that can propagate a deletion without a human confirming it. The move is quarantine: move the file into a dated `_quarantine_YYYY-MM-DD/` folder (or an `Archive/` folder), and record where it went. Deleting the quarantine is Kam's, later. Session scratchpad files are exempt (per the index and the hook). `2026-08-26_never-delete-cleanup-means-quarantine.md`

2. **When I find conflict copies, stale duplicates, `._` files or old logs:** report them; never remove them and never call them "safe to delete". If Kam wants a set gone he says so per set. `2026-08-26_never-delete-cleanup-means-quarantine.md`

3. **When the file is one we are working on** (changed in the last few days, open in an agent's pane, in a branch's working tree): it is not even quarantined without its owner's word. `2026-08-26_never-delete-cleanup-means-quarantine.md`

4. **When I brief an agent to tidy:** the brief carries the rule. An agent tidying its own tree moves files to an archive path; a "cleanup" ticket is a quarantine ticket. `2026-08-26_never-delete-cleanup-means-quarantine.md`

5. **When I quarantine a file inside a tree that is synced to other copies:** do not rename it in place. A rename is a delete plus a create; a sync that never propagates deletions copies the new name and keeps the old one, so every replica still holds the original under its ordinary name and the next restore ships it. Move the file into a directory the sync ignores. Then verify at EVERY replica that the original name is absent, and fix the source (the bundle, template or image that ships it), not only the machine in front of me. The same question applies wherever "removed" is a rename or a status flag inside a set that is copied wholesale: what copies this set, and does it copy intentions or only bytes? Where the 2026-08-26 lesson says "rename or move", this newer lesson wins: move, not rename. `2026-09-09_quarantine-by-rename-is-not-removal-on-an-additive-sync.md` (over `2026-08-26_never-delete-cleanup-means-quarantine.md`)

6. **When I report a quarantine that failed or a dangerous leftover:** state severity by what is reachable, not by what is named (an inert profile with no token is a directional risk, not an active one), so the owner can size it. `2026-09-09_quarantine-by-rename-is-not-removal-on-an-additive-sync.md`

7. **Before any two-way sync leg between drives Kam depends on:** (a) dry run first and refuse the leg if any `Deleting` line names a working folder; (b) prove the replicas agree on top-level NAMES including letter case, using a real directory listing (`python3 -c 'import os; print(os.listdir(root))'`), because `ls` on a case-insensitive mount shows two different spellings as the same and the engine then deletes both sides; (c) after the leg, read the log for `Deleting` before reading it for `finished`. Exit code 0 and "finished" are true of a run that deleted hundreds of megabytes; a cut run writes no summary, and that absence is itself the signal to read the body. A leg I do not need can still delete from the drive I do. `2026-08-26_a-sync-that-cannot-refuse-a-deletion.md`

8. **When I hand a running sync leg to a successor:** say what to search the log for (`Deleting`, `conflict`, no `Sync finished`). A shutdown in the middle of a run is an incident, not a skipped step. `2026-08-26_a-sync-that-cannot-refuse-a-deletion.md`

9. **When a scheduled, unattended job can destroy data and cannot PREVENT that:** it is held, not armed. Detecting the damage afterwards in a log is a post-mortem, not a guard. Card it to Kam naming the missing prevention; re-arm only on his word. Hold it with several independent locks (the scheduler entry disabled in a way that survives login, a hold file the script refuses on, the installer skipping it, the boot check reporting HELD), because one lock alone is undone by a helpful successor. Kam hears about every unattended job that could destroy data at least once, with what it can and cannot prevent. `2026-08-26_a-sync-that-cannot-refuse-a-deletion.md`

10. **When restoring after a wrongful deletion:** find every copy; restore additively (no delete flag); verify by file count and a hash sample, not by disk-usage totals; run only the legs proven case-consistent; card the unsafe leg with its root cause. A restore is a write into someone else's folders and happens on Kam's ruling. `2026-08-26_a-sync-that-cannot-refuse-a-deletion.md`

11. **When a drive is filling and the plan says delete or prune bulk that is NOT regenerable or is worth keeping a while** (old builds, rollback images) (Wednesday seat, which has the archive drive mounted): first ask whether it can be MOVED to the archive drive (`/Volumes/G-DRIVE/<Client>/<Project>/archive/<YYYY-MM-DD>_<what>/`), one client per folder, with a manifest (what, from where, sizes, checksums where practical), no secrets (no `.env`, no keys). Any disk-freeing brief names this option before any deletion step. "Clear after a month or so" means a monthly review that lists archives older than about 30 days to Kam; never a silent sweep. This narrows what a seat may delete; it never widens it. `2026-10-07_archive-bulky-leftovers-to-g-drive-clear-after-a-month.md`

12. **When a build seat records real tool output as a test fixture** (a search, a listing, a log): generate it from a scratch tree made for the purpose, with invented names and a scratch home; a recording made against the real drive is never committed, and committed paths are relative or scrubbed. Every brief that allows recorded output says so. Before any repository changes visibility or leaves its project, sweep EVERY branch and the WHOLE history (secrets, personal data, other clients' and projects' names, drive layout, commit identities), with a positive control for each search that returns nothing; confirm the main findings at source myself; give Kam the visibility link only with the sweep result beside it. `2026-11-17_recorded-fixtures-come-from-a-scratch-tree-never-the-real-drive.md`

## What a tool already enforces

- `2_Project_Files/fleet/hooks/pretooluse_no_rm.sh` refuses delete verbs from a seat's shell (rule 1). It does not cover what I recommend, brief or configure for others, nor a sync engine's own deletions.
- `2_Project_Files/scheduler/nas_sync.sh` refuses to run while its hold is in place (rule 9). By its own header it could only detect a mass deletion after a run, not prevent one; that gap is why it is held.

## Grants and their limits

- **Regenerable build leftovers may be deleted** (Kam, 2026-09-29): stale dependency folders (such as `node_modules` in untouched worktrees), scratch clones a QA or CI run made for one use, install caches, once no longer in use. The project's OWN seat deletes them and re-measures free space before and after; I still delete nothing by my own hand. A deletion brief names the exact class, the staleness test, the exclusions, a count before and after, and free space before and after. If it touches other seats' trees or more than one project it goes to Kam as a card.
- **Not covered by that grant:** records (QA reports, evidence, handovers, history, briefs, logs a successor reads) and anything in use (a worktree touched in the last 3 days, one registered to a live seat, anything a pane has open). For these, cleanup is still quarantine. `2026-09-29_regenerable-build-leftovers-are-not-kept.md`
- **Stays Kam's:** deleting any quarantine or archive; re-arming a held destructive-capable job; turning the sync engine's own big-deletion guard back on (his file); fixing leaked content in a repository's history, whether by a fresh repository or an irreversible history rewrite.

## The mistakes this family keeps catching

- "Safe to delete" said about something that merely looks redundant.
- A sync's green exit read as "nothing was lost".
- A rename counted as a removal in a tree that is copied additively.
- A job that can destroy data left running because "we would see it in the log".
- A narrow permission to delete build leftovers stretched to cover records or work in progress.
- Real drive contents committed as test data, where history keeps them after the file is gone.

## Members

- `2026-08-26_a-sync-that-cannot-refuse-a-deletion.md` — Before any two-way sync leg: dry run, prove replica top-level names match in case (os.listdir, not ls), and read the log for 'Deleting' before 'finished'. A scheduled job that can destroy data but not prevent it is HELD; re-arm only on Kam's word.
- `2026-08-26_never-delete-cleanup-means-quarantine.md` — Never delete files or run delete verbs (rm, git stash drop, checkout -- over work, rsync --delete). Cleanup means move to a dated _quarantine folder and say where. Report conflict copies and duplicates; never call them safe to delete. Scratchpad files exempt.
- `2026-09-09_quarantine-by-rename-is-not-removal-on-an-additive-sync.md` — When quarantining a file in a synced tree: do not rename in place (an additive sync keeps both names); move it into a directory the sync ignores. Verify the original name is absent at every replica and fix the source bundle, not just this machine.
- `2026-09-29_regenerable-build-leftovers-are-not-kept.md` — Regenerable build leftovers (stale node_modules, old CI/QA scratch clones) not in use go once used, deleted by the project's own seat with df before/after. Records, anything touched in 3 days or a live seat's tree stay.
- `2026-10-07_archive-bulky-leftovers-to-g-drive-clear-after-a-month.md` — When a drive is filling and the plan says delete old builds or bulk: first MOVE it to /Volumes/G-DRIVE dated, per client, with a manifest, no secrets. 'Clear after a month' is a listed review to Kam, not a silent sweep.
- `2026-11-17_recorded-fixtures-come-from-a-scratch-tree-never-the-real-drive.md` — When a build seat records tool output as fixtures: generate from a scratch tree, never the real drive. Before a repo goes public or leaves its project, sweep every branch and all history (positive controls); fixing history is Kam's call.
