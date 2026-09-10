---
date: 2026-09-10
type: correction
source: found while building the family-weight index — both boot digests were serving a rule Kam had withdrawn
status: live
tier: W
---

# An additive sync does not just fail to DELETE — it CREATES files, and every glob in the system treats them as input

**The lesson:** Unison resolves a conflict by keeping both sides and renaming one
`<name> (conflict_on_<date>).<ext>`. That new file **sits in the same folder, with the same
extension, and matches the same glob as the real one.** `boot_digest.py` globbed
`learnings/2026-*.md` — and `2026-09-02_coo-actionable-tickets-never-wait-for-kam
(conflict_on_2026-09-04).md` matched it.

**So both boot digests were serving a stale duplicate of that lesson at every boot**, a copy
predating six extensions — including **Kam's 2026-09-06 09:45 withdrawal of the ticket-aggregation
rule.** A seat reading the digest could have applied a rule he had explicitly taken back three
minutes after giving it. **Nobody wrote a bug; the glob was simply never asked what else could match
it.** There are **33 such conflict artefacts** under `0_Brain/` right now.

**The second half, and it is the more dangerous one:** removing the duplicate was not enough. The
digest carries *headings*, and that lesson's heading still read
*"…rather than three or five separate tickets, create one larger ticket."* **The withdrawal lived in
the body, which the digest does not carry.** The digest was still serving the withdrawn rule — from
the live file this time. Fixed by putting the retraction **in the heading**, because
[[2026-08-13_headline-must-match-the-operative-case]]: the first line IS the retrieval handle, and a
retraction that does not travel with the handle has not been recorded, only stored.

## How to apply

1. **Every glob over a synced folder gets an exclusion for `(conflict_on_`.** Treat a bare
   `glob("2026-*.md")` on any brain folder as a defect on sight.
2. **When a rule is withdrawn, superseded or narrowed, amend the HEADING**, not just the body —
   in the same edit. Whatever the digest carries is what a cold seat will act on.
3. **Never delete the conflict copies** ([[2026-08-31_never-delete-files]]) and do not rename them
   either ([[2026-09-09_quarantine-by-rename-is-not-removal-on-an-additive-sync]] — the replica
   keeps both names). **Exclude them from readers; leave them on disk.**
4. **Diff a conflict copy before assuming it is junk.** This one was a strict subset, so nothing had
   diverged — but that was measured, not hoped, and the answer decides whether it is noise or a lost
   edit.
5. This is the twin of the quarantine lesson: that one says a sync **cannot remove**; this one says a
   sync **adds**, and additions arrive already matching your selectors.

Related: [[2026-09-09_quarantine-by-rename-is-not-removal-on-an-additive-sync]] ·
[[2026-08-13_headline-must-match-the-operative-case]] ·
[[2026-09-09_a-guard-whose-exclusion-list-contains-its-own-subject]] ·
[[2026-09-02_coo-actionable-tickets-never-wait-for-kam]]
