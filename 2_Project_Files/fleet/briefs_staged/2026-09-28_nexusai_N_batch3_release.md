# BLUF — Datasec/NexusAI-N (lane 2): BATCH 3 IS BACK and you are its MERGE AUTHOR. RELEASE FOUR of the five: RD-324, RD-684, RD-685, RD-314, one at a time, in that order, under the merge-turn rule (my 09:2x ANSWER). **RD-424 is HELD** for a composition fix (D-F2, ruled below) before it merges. This SUPERSEDES the order of your current queue (RD-656 install, RD-591/648 greens, RD-609): merges take their turns first; the rest continues between turns.

Verdict: QA/NexusAI-batch3, 23:22Z, report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch3/report.md` (read whole by Tuesday). Read §0, §3, §9b (C-57), §10 and §17 before the first merge.

## THE RELEASE (the gate's order without RD-424)
1. RD-324 `rd-324-ledger-union-s84n` @ `168d850` — GO WITH FINDINGS (tier 1)
2. RD-684 `rd-684-redrive-carries-surviving-target-s84n` @ `7085ee7` — GO WITH FINDINGS (tier 1)
3. RD-685 `rd-685-hardlinked-store-s84n` @ `9d7076b` — GO WITH FINDINGS (tier 1)
4. RD-314 `rd-314-law-window-after-source-s84n` @ `ce148d5` — GO WITH FINDINGS (tier 1)
Main at the gate's end = `3ee790f` (moved from M0 1904765; shares only the counts file with the deltas, per the gate). Re-read ls-remote before each merge.
- **The RD-684 × RD-685 hunk (C-57 narrow exception of 2026-09-27, carried VERBATIM):** resolve `backend/dataErasure.js` as the CANONICAL union — RD-684's block, `}`, a blank line, `/**`, RD-685's block — and repeat the three proofs: `node --check` rc 0; each side's diff = the other ticket's own diff over 1904765; the blob equals the gate's **`1f708e2`** (with RD-324 in). A different blob = STOP, mail Tuesday.
- **RD-314's merge meets the C-57 stop on the rd409-410 renamed id** ("…RD-410 O2 … CONTROL — choosing a DIFFERENT mode still clears a generated token (unchanged)"): ACCOUNTED under C-133's ADDENDUM case 1 (stale parent), exactly as the gate did. Any OTHER missing id = STOP.
- Per merge, the batch-1/4 pattern: forward merge (never rebase, C-68), the gate's C-68 sets by name, counts regenerated once, C-57 superset, full verify through the lock with SESSION_SECRET unset, push, deploy-demo SKIPPED (read it), CI Build green before the next. MERGED mail each: ticket, main sha, parents, counts, C-57, demo run id, Build run id.
- **Merge-turn rule** (09:2x ANSWER to P, O and M, same text): forward merge + queue only when no other seat's MERGE ticket is queued or holding; a CI wait does not hold the turn.

## D-F2 — RULED (Tuesday; C-164 was Tuesday's ruling, so this is its owner amending it)
The composition: while an erasure is honestly `purged_incomplete` (RD-684/685 make that indefinite), C-164 condition 1's R-1 freeze skips EVERY store's backups, so a tear boots to an EMPTY store (r8). **Ruling: the freeze covers ONLY the stores (and their recovery copies) named in the erasure's failed ledger. Every other store backs up normally during `purged_incomplete`.** Rationale: R-1 exists so pre-erasure bytes are never fanned into new copies; a store the erasure already purged holds only post-erasure data, and the stores still holding erased bytes are exactly the named ones. Build it on `rd-424-backup-after-write-s84n` (forward-merge main first, never rebase) as RD-424 round 2, tier 1, with cells: r8 as a cell (merged-shape: a symlink AND a hard-link incomplete erasure, five writes, tear, boot → the store restores W5, not empty), the named store's pre-erasure bytes still NOT fanned (R4's property kept), and a control that the freeze still applies to the named store. Record this as a C-164 ADDENDUM (Tuesday's amendment of its own ruling). READY FOR QA when done; it goes to a gate before RD-424 merges.

## TICKETS (after your merges, one ticket per fix one test pass proves; report §10 has fix shapes and red cells)
- **C-F1 (Major, RD-685/684):** a hard-link refusal is not carried; a changed/missing inode lets the re-drive certify `purged`. **Shape RULED:** carry the refusal forward keyed by DATA_DIR name + refused inode (dev:ino); resolve only when that SAME inode is ours with nlink 1; a changed or missing inode keeps `purged_incomplete` with a text that asks for an operator confirmation (C-169 already prefers a dead end to a guess). Cells k12a/k12b, control k5. Priority: next erasure work.
- C-F2 (Major, low likelihood): `path.resolve(DATA_DIR)` once in the census; k15a/b cells; M-C6/M-C7 cells (C-F3).
- E-F1 (Major, RD-314): triple-backtick literal state in the scanner; q11c/d/g/h + E-F2's before-the-first-pipe cells.
- D-F1 (Major, pre-existing, RD-424 class): a clearing write reverted on restart. D-F3 (Minor): stranded backups/*.tmp.* survives an erasure.
- Minors: A-F1/A-F2 (RD-324), B-F1 (RD-684 cells), B-P1, D-P1.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- rd104-gh-identity-acceptance-false-premise: "You check the two settings pages yourself - two clicks, links below (recommended)" (2026-09-07) -> Kam's own action; nothing for N to land.
- t9-nas-leg-direction: "Make this drive's backup ONE-WAY, drive to NAS, additive" (2026-09-21) -> not N's work.

## HOLDS
No deploy, no demo, no Partner Center, no `.github` change. Ticket comments only for anything client-facing. PRIOR-WORK CHECK; never delete (quarantine); never fetch into the stale clone's working tree (C-28 and my 09-28 reading).

PROVENANCE:
- batch-3 verdicts, order, blob 1f708e2, C-57 accounting, findings | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch3/report.md | read 2026-09-28 09:3x
- C-164 is Tuesday's ruling | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md:1683 | read 2026-09-28 09:3x
- N's previous queue | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-28_nexusai_N_rd656_launcher.md | read 2026-09-28 09:3x
Self-check note: four merges; RD-424 held for a round-2 fix of D-F2 under Tuesday's amendment of its own C-164; C-F1 shape ruled; queue superseded by name.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 09:24
