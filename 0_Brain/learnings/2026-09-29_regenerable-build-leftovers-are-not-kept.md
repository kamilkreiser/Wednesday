---
date: 2026-09-29
type: preference
source: Kam, live board 2026-09-29 08:05:14 (view=wednesday), ruling (b) on card wed-devmaster-full-secuura-worktree-node-modules
status: live
tier: W
---

# Regenerable build leftovers (stale node_modules, old CI/QA scratch clones) are NOT kept once used — but only Kam's word authorises a deletion, and records are never in scope

**The operative case, so the headline matches it:** a drive is filling, or a round has finished, and there are regenerable build artefacts lying around: `node_modules` in worktrees nobody has touched for days, repo clones a QA gate made for one run, install caches. **Kam does not want them kept.** They are removed by the project's own seat once they are no longer in use, and the space is re-measured.

**His words, verbatim (08:05:14):**
> *"Decision wed-devmaster-full-secuura-worktree-node-modules: b — Delete those node_modules | note: there is no need to keep historical CI files. these seem to be very hungry in terms of storage so limit storing what has been used and no longer needed"*

**What it narrows, and what it does not:**
1. It narrows [[2026-08-26_never-delete-cleanup-means-quarantine]] for ONE class: **regenerable build artefacts that are no longer in use.** `npm ci` rebuilds node_modules; a gate's clone is re-made by the next gate. Quarantining 300 GB of them onto another volume (my recommendation (a)) is what he declined.
2. **It does NOT cover records:** QA reports, evidence folders, handovers, history, briefs, READY diffs, logs a successor reads, anything a human or seat may need to read again. Those stay, and "cleanup" of them is still quarantine.
3. **It does NOT cover anything in use:** a worktree touched in the last 3 days, a worktree registered to a live seat, anything a pane has open. The 2026-08-26 "files we are working on" half stands in full.
4. **Wednesday still deletes nothing by her own hand** (the no-delete hook, and hard rule 1 for another project's tree). The project's own seat executes, on Kam's ruling, and re-measures `df` as the proof.
5. **Reading, stated to him on the board 08:0x:** "historical CI files" = old CI/QA scratch clones and install caches, not the reports. If he meant more, his word widens it.

**How to apply:**
- At the end of a round, a seat's handover names the regenerable leftovers it created and removes them (its own only), stating what was removed and the free space after.
- When a drive runs low, the first proposal is removing stale regenerable artefacts, not moving them; it still goes to Kam as a card if it touches other seats' trees or more than one project.
- A deletion brief names the exact class (directory name), the staleness predicate, the exclusions (live seats' worktrees), a count before and after, and `df` before and after.

**Family:** [[2026-08-26_never-delete-cleanup-means-quarantine]] (narrowed, not retired) · [[2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit]] (read the scope of the ruling) · [[2026-08-16_classification-is-the-field-that-grants-authority]] ("regenerable" and "no longer used" are scope words and each needs its measurement).
