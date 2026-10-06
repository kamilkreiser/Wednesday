---
date: 2026-10-07
type: preference
source: Kam, live board 2026-10-07 08:53:04 (view=wednesday)
status: live
tier: W
---

# Disk running out? ARCHIVE old builds and other unneeded bulk to G-DRIVE first, and clear the archive after about a month

**The operative case, so the headline matches it:** a drive is filling (a box, DevMASTER, a deploy host), or a round is about to free space, and the plan says *delete* or *prune* old builds, rollback images, scratch clones or other bulk that is not needed now. **Before any deletion, ask whether it can be MOVED to G-DRIVE instead**, dated, and cleared there after about a month.

**His words, verbatim (08:53:04):**
> *"Also, with regards to running out of hard disk space, don't forget about G-Drive. You can put the old builds on there and then clear them after a month or so. This goes for other things that are taking up space but not necessary."*

**What G-DRIVE is (measured 2026-10-07 08:5x, `df -h`):** `/Volumes/G-DRIVE`, 11 TiB, 3.6 TiB free, mounted on the Studio.

**How to apply:**
1. **Archive before delete.** A space-freeing plan lists what can go to G-DRIVE first; deletion is for what cannot be moved (or is regenerable and Kam's 2026-09-29 rule already covers it). This narrows, never widens, what a seat may delete.
2. **Dated, findable, and sized.** Archive under a dated folder naming the project and the source (`/Volumes/G-DRIVE/<Client>/<Project>/archive/<YYYY-MM-DD>_<what>/`), with a manifest (what, from where, sizes, sha256 where practical) beside it. One client per folder (hard rule 2).
3. **"Clear after a month or so"** is a review, not an automatic delete: at the monthly check, archives older than ~30 days are listed to Kam (or cleared under his standing word, stated as Wednesday's reading). Never a silent sweep.
4. **Remote boxes:** for images on a VM (demo, kintsugi), the archive route is `docker save` streamed to G-DRIVE over SSH; measure its size and time before relying on it. A secret never goes into an archive (no `.env`, no keys).
5. **Briefs carry it:** any disk-freeing brief names the G-DRIVE option and its path before any deletion step.

**The case it arrived with:** the same morning, Seat D 14th deleted demo's five old rollback sets (31 images, ~11.8 GB) under Kam's card `secuura-demo-disk-retire-old-rollback-sets-1007` = a. That was authorised and is done; this rule applies from now on.

**Family:** [[2026-08-26_never-delete-cleanup-means-quarantine]] (quarantine over delete — G-DRIVE is the quarantine with room) · [[2026-09-29_regenerable-build-leftovers-are-not-kept]] (regenerable leftovers are removed; this covers what is not regenerable or worth keeping a month) · [[2026-09-10_a-sync-conflict-copy-is-an-input-to-every-glob]] · [[2026-08-03_role-beyond-code-three-priorities]] (one client per archive folder).
