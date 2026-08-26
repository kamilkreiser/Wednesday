---
date: 2026-08-26
type: correction
source: "Kam, 2026-08-26 10:51 (dashboard chat, verbatim): 'Do not delete any files, especially files that we are working on. Better cleanup is worthwhile.' — minutes after the restore of the six folders the NAS sync leg had deleted, and after my panel line calling 15 HPSM conflict copies 'safe to delete when you like'."
status: live
supersedes: ""
---

# Never delete files — especially files we are working on. Cleanup means quarantine, not removal

**The rule (Kam's words, twice in one message):** *"Do not delete any files,
especially files that we are working on. Better cleanup is worthwhile."* A
deletion is the one file operation that cannot be undone from inside the
system; every other outcome (a duplicate, a stale copy, a conflict file, a
folder in the wrong place) is a tidiness cost that can be paid later with full
information. Kam prefers the tidiness cost. So do I from now on.

**What triggered it, honestly:** the 2026-08-25 NAS unison leg deleted six
`!CODING/` folders from the master drive
([[2026-08-26_a-sync-that-cannot-refuse-a-deletion]]); the same morning I told
Kam the HPSM `(conflict_on_2026-08-25)` copies on the travel drive were "safe to
delete when you like", and at boot I discarded this drive's local dashboard-data
churn (`git checkout` + `stash drop`) to get a clean fast-forward. None of those
lost anything that mattered — and that is not the standard. The standard is
that nothing I run, recommend, or configure removes a file.

**How to apply:**
1. **No delete verbs from my hands:** no `rm`, no `git stash drop`/`checkout --`
   over uncommitted work, no `rsync --delete`, no unison leg that can propagate
   a deletion without a human confirming it. When a task seems to need one,
   the move is **quarantine**: rename or move the file into a dated
   `_quarantine_YYYY-MM-DD/` folder next to it (or `Archive/`, which the sync
   engine already ignores), and record where it went. Deleting the quarantine
   is Kam's, later, with full information.
2. **Sync engines are covered by the rule.** Recommend to Kam (his profile):
   `confirmbigdel = true` back on, and ideally a no-delete posture for the
   NAS/travel legs (unison has no `--no-delete`; the equivalent is quarantining
   what a dry run reports as deletions before the real run). Until then: dry
   run first, read `Deleting` lines, and refuse the leg if any name a working
   folder.
3. **Conflict copies, stale duplicates, `._` AppleDouble files, old logs:**
   report them, never remove them, never call them "safe to delete". If Kam
   wants them gone, he says so per set.
4. **Briefs to agents carry the rule:** an agent tidying its own tree moves
   files into an archive path; it does not `rm`. A "cleanup" ticket is a
   quarantine ticket.
5. **"Files we are working on" is the sharpest half:** anything with a mtime
   in the last days, anything an agent pane has open, anything in a branch's
   working tree — those are never even quarantined without the owner's word.

**Related:** [[2026-08-26_a-sync-that-cannot-refuse-a-deletion]] (the event),
[[2026-08-15_a-gui-open-is-a-write]] (my writes into others' folders),
[[2026-07-31_manage-dont-do]], [[2026-08-03_contemplation-the-cockroach]] (don't
destroy gratuitously; under uncertainty, the cheap mercy wins — the same shape
pointed at files), [[../people/kam]]
