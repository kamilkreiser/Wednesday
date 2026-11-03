---
date: 2026-11-04
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 01:52 AEDT 2026-11-04 by the 22:16 seat at its ~80% rotation. Previous kept as NEXT-PICKUP.md.pre-1104-0152. Replace wholesale; never stack.
---

# NEXT PICKUP — Wed 4 Nov 2026, 01:52 AEDT (the 22:16 seat's rotation handover)

## STATE AT HANDOVER
- **develop = 79145a312f0150ca9adaf5a36bb3dea93d108cff** (ls-remote 01:2x). Merged tonight, each on a head-pinned GO and verified at source: **PR 1990 -> 137b4026c89f**, **PR 1991 -> 79145a312f01** (KS-1868 PRs 13 + 12, gate 175). Merge seat B 86th WRAPPED, scored 0.95, pane %116 closed.
- **Live floor: Seat E 32nd only** (%115, Opus), ordered to WRAP at 14:50:54Z (see item 1). Raise lane R and merge lane B are EMPTY.
- Gauge 7d 94% (renews ~4d 11h). Usage is a guide (Kam 10-22); launches are "necessary" only (raise / gate / merge, which need repo rights).

## FIRST WORK, in order
1. **E 32nd's wrap mail** (due): verify at source (history entry, HANDOVER first action = the F1/F2/F3 fix design, nothing running), score, pane_close %115.
2. **Kam's card `secuura-pr1989-gate174-cap-nogo-pgbouncer-1104`** (posted 01:4x, HTTP 201). Gate 174 = round 2 of 2 on PR 1989 (KS-915 restore script) = **NO GO (G174-F1, HIGH)**: the five PGBOUNCER_* pool keys are judged by no reader, and a crafted newline value renders a remote host line in pgbouncer.ini. Verdict `0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2/verdict.md`. Rec (a): one narrow round 3 for F1 + G174-F2 (PATH lock) + F3 (census pin 8/8); default HOLD, nothing merges. **On (a): brief E 33rd from E 32nd's HANDOVER** (Opus, SEAT_MODEL_ENV=claude-opus-5-5), then a narrow round-3 gate. On (b): QUEUE 1989 to a merge seat with F1 ticketed High. On (c): close it via a seat. PR 1982 stays OPEN and untouched until 1989 resolves.
3. **R 81st raise seat — BRIEF NOT WRITTEN; write it first** from R 80th's HANDOVER (`!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatR-80th/HANDOVER.md`, FINAL block) with the R 80th brief (`2_Project_Files/fleet/briefs_staged/2026-11-03_seatR80_raise_continue_r79.md`) as the template, re-keyed section by section; NEW SEAT step 1 quotes card 1030. Its queue:
   (a) **notes patch PR 1992** from gate 176 (`0_Brain/reference/2026-11-03_gate176-ks1868-pr1992/verdict.md`: GO WITH NOTES; Wednesday's rulings: F1 not a hold (webhook = machine POST); F2/F3 ticket candidates; F4 note; F5 = state what the group tree 0a2814d535d7 was computed over);
   (b) **notes patch PR 1993** from gate 177 (`0_Brain/reference/2026-11-03_gate177-ks1868-pr1993/verdict.md`: GO WITH NOTES; F1/F4/F6 READY corrections; F2/F3 ticket candidates; F5 a follow-up cell (H5 survives); F7 below);
   (c) PR 16 (O98-P2..P9, nft.routes.ts; patches sha-proven in R 80th's drafts/patches/);
   (d) ITEM 4a/4b (two Low tickets) and ITEM 5;
   (e) **a raise PR for the three Spark doc_only passes** (KS-1320 P1B; KS-1343 P2B + P3B, PARTIAL: notes 4/7/8 of 3-10; READY files in `local-model/night/`), tier 2.
   Launch via a waiter at CAPACITY ROOM. **Use `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/32f399aa-9ead-45db-bd67-469960bf8bbe/scratchpad/b86_waiter2.sh` as the waiter template**: the older r80/e32/b85/b86 waiters log a false "LAUNCH rc=0" ($? read after $(date)); ledger 2026-11-04. A brief staged before midnight is re-read and re-stamped before it launches after midnight.
4. **Merge seat B 87th** after R 81st's two NOTES PATCHED: QUEUE 1992 (head 651f25b0d0e2) then 1993 (head 8712cb115e0a), one GO at a time, each recomputed on the REAL develop (gate predictions: develop+1990+1991+1992 = 70bbceb1bf16, the 4-PR tree = ce7a5d0d1a99). Brief: re-key `fleet/briefs_staged/2026-11-03_seatB86_merge_queue.md` from B 86th's HANDOVER (`!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatB-86th/HANDOVER.md`; it lists 7 new tool defects, incl. vault_commit_mine:64 with no --add for a new note).
5. **G-DRIVE move** (6 remaining gate clones): `2_Project_Files/tools/archive_gate_clones_20261103_remaining.sh --run`, detached pid 22247, log `/Volumes/G-DRIVE/Secuura/Blockchain/archive/2026-11-03_gate-clones/run_remaining_2226.log`. On finish: read FAILS and the manifest (13 MOVED rows), `df -g`, then `decision_queue.sh --delivered wed-gate-clones-hook-blocks-removal-1103 "/Volumes/G-DRIVE/Secuura/Blockchain/archive/2026-11-03_gate-clones"`. NEVER re-run the original script (the empty repo/ skeletons would write false MISMATCH rows).

## MORNING CARD (11-04, boot step 10a) must carry
- Overnight: merges 1990 + 1991; gates 175/176/177 GO WITH NOTES; gate 174 NO GO at the cap (his card); Spark operator 100: 3 doc_only passes held; G-DRIVE move result.
- **FYI G177-F7 (pre-existing, both trees):** with no DID resolver and VC_SIGNING_KEY unset, a credential signed with the source's default dev key ('secuura-dev-signing-key', verifier.ts:356) verifies even under NODE_ENV=production. Module-measured, route not driven; **whether any deployed vc-issuer runs with the key unset is UNMEASURED**. Disposition: a ticket via a Secuura seat (board search first).
- **The 90%+ gauge reading** (the 11-02 'continue with tickets' row says re-read at 90%): read as continuing under 10-22 + 10-29 (minimal, necessary Claude agents).
- Candidate machine setting (his): exclude the G-DRIVE archive from Spotlight (Avast + mds drove load1 to 17 during the move).
- Counts awaiting him: 1 Secuura card (the 1104 cap card).

## OWED (Wednesday's)
- Ticket candidates to route via a Secuura seat: G175-F2/F3/F4, G176-F2/F3 (F3: the indexer re-reads one block forever), G177-F2/F3/F5/F7, G174-F4/F5; R 80th's board findings (KS-1329 count 10 vs 24, KS-1737, originate webhooks.ts:553, KS-1727). Auth follow-ups G171-F1/F2, KS-1968 B2, G172 F1/F2/F3/F6. DEPLOY-TIME CHECKS before any deploy carrying PR 1988 (HIBP default ON).
- **@azure/msal-node HIGH baseline dies MON 2026-11-09**: measure whether its ticket landed.
- Spark: idle with a measured reason (doc_only class nearly exhausted; test_only_input has no hold kind: build it next).
- WED-155 (inbox_digest.sh key in argv); the boot prompt's MODEL CHOICE line still says /model a seat (rewrite); INDEX.md refresh (last block 10-27); stranded stash@{0}: never drop.

## RULES IN FORCE (this seat's lessons)
- A launch is confirmed by `pane ... added (%N)` + the pane list, never a waiter's rc line; capture `rc=$?` on its own line.
- A note is its own call; a `sent:` quote sits on its own line.
- SELF-CHECK stamps are generated by `date`, and re-done after midnight.
- Before ANY merge GO: gate_stray_check, re-pin by ls-remote in the same action, no other GO outstanding.
- At a cap NO GO with a HIGH open, card Kam (default HOLD) rather than ship.
