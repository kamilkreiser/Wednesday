---
date: 2026-11-04
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 03:19 AEDT 2026-11-04 by the 01:5x seat at its 65% checkpoint. Previous kept as NEXT-PICKUP.md.pre-1104-0319. Replace wholesale; never stack.
---

# NEXT PICKUP — Wed 4 Nov 2026 (the 01:5x seat's checkpoint handover)

## STATE
- **develop = 79145a312f0150ca9adaf5a36bb3dea93d108cff** (ls-remote 03:18). Unmoved since PR 1991 merged 01:20.
- **Live floor (both Sonnet 5.5, Secuura/Blockchain):**
  - **Seat R 81st** (lane R, pane %117) — brief `2_Project_Files/fleet/briefs_staged/2026-11-04_seatR81_raise_notes_pr16_docs.md`. DONE: NOTES PATCHED PR 1992 (twice; the 15:47Z correction is the live body, sha256 bbe4b5c1) and PR 1993 (sha256 f03ab92a); KS-902 comment cce55d45 (premise false as measured; O101-P1 NOT raised by Wednesday's 16:14Z ruling). IN FLIGHT: PR 16 (nft.routes.ts, O98-P2..P9) push, driver pid 56169 since 16:10:02Z. NEXT for it: PR 16 READY FOR GATE -> two doc PRs (KS-1320; KS-1343 P2B+P3B, single-key titles) -> ITEM 5 tickets 4a/4b -> ITEM 6 gate ticket candidates -> ITEM 7 QUESTION. It wraps at 80-85% (watcher read 66% ~03:1x).
  - **Seat B 87th** (lane B, pane %118) — brief `.../2026-11-04_seatB87_merge_queue.md`. Plan CONFIRMED 16:02Z, QUEUE PR 1992 sent 16:03Z (head 651f25b0d0e2, develop pin 79145a312f01, expected merge tree 70bbceb1bf16: its early look reproduced it). All 37 tools re-keyed + checked, merged-PR controls 7/7. NEXT: its READY TO MERGE for 1992.
- Gauge 7d 94% (renews ~4d 11h from 01:59). Usage is a guide (Kam 10-22, 10-29: "minimal but used when necessary"): raise / gate / merge seats only.
- Disk DevMASTER 23-24 GiB free (99%); seats STOP under 15.

## FIRST WORK, in order
1. **B 87th READY TO MERGE PR 1992** -> completion check (tree = 70bbceb1bf16, shared paths 0, 9 files, Gate 176 notes present at bbe4b5c1, GO_GATE CONTROLS on top) -> gate_stray_check -> re-pin by ls-remote IN THE SAME ACTION -> GO, subject copied from the previous GO's: `GO: merge PR 1992 at 651f25b0d0e2 on develop 79145a312f01 (Seat B 87th)`, body labels `Head pin:`, `develop pin:`, `Expected merge tree on the pin:`. No other GO outstanding.
2. On its MERGED mail: verify by ls-remote (develop = the squash; refs/pull/1992/merge gone with a control), then **QUEUE PR 1993** (head 8712cb115e0a; expected tree on develop+1992 = ce7a5d0d1a99 per gate 177; notes at f03ab92a). Then its READY -> GO -> MERGED. B 87th wraps after.
3. **R 81st's READY FOR GATE: PR 16** -> commission a TIER-1 Opus gate (Agent subagent; commission file under 0_Brain/reference/2026-11-04_gate178-ks1868-pr<N>/; copy gate 176's commission + gate_common.md). Note for the gate: app.ts:48 lists POST /nft/verify/asset and /verify/transaction as publicOps, so the 500-vs-left-open reading matters on PUBLIC routes. The two doc PRs: ONE tier-2 Sonnet gate as a batch.
4. **Kam's card `secuura-pr1989-gate174-cap-nogo-pgbouncer-1104`** (open; default HOLD). On (a): brief E 33rd from `!CODING/Secuura/Blockchain/5_Project_History/2026-11-03_seatE-32nd/HANDOVER.md` (Opus, SEAT_MODEL_ENV=claude-opus-5-5), then a narrow round-3 gate. PR 1982 untouched until 1989 resolves.
5. **Waiter template:** `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d2036c3a-7e9b-4208-9997-bf43c65bf373/scratchpad/r81_waiter.sh` (rc on its own line; asserts its own paths). Launch confirmed only by `pane ... added (%N)` + the pane list.

## MORNING CARD (11-04, boot step 10a) must carry
- Overnight: merges 1990 + 1991 (+1992/1993 if done); gates 175/176/177 GO WITH NOTES; gate 174 NO GO at the cap (his card); G-DRIVE move DONE (13/13, counts equal, FAILS=0); Spark: operator 100 3 doc passes held, operator 101 built the test_only_input hold kind + held KS-902 (NOT raised: false premise; KS-902 comment instead); PR 16 raised and gated (if so).
- FYI G177-F7 (pre-existing, both trees): with no DID resolver and VC_SIGNING_KEY unset, a credential signed with the source's default dev key verifies even under NODE_ENV=production. Module-measured; **whether any deployed vc-issuer runs with the key unset is UNMEASURED**. R 81st files it at ITEM 6.
- The 94% gauge reading, read under 10-22 + 10-29.
- Candidate machine setting (his): exclude the G-DRIVE archive from Spotlight (mds_stores drove load1 to 9-17 for an hour after the move).
- Counts awaiting him: 1 Secuura card (the 1104 cap card).

## OWED (Wednesday's)
- Ticket candidates NOT given to R 81st (route via the next Secuura seat): G175-F2/F3/F4 + the connection-pool.ts:279 survivor, G174-F4/F5 (after Kam rules 1989), R 80th's board candidates (KS-1329 count 10 vs 24, KS-1737, originate webhooks.ts:553, KS-1727 title, Node-26 threadToken self-skip). Auth follow-ups G171-F1/F2, KS-1968 B2, G172 F1/F2/F3/F6. DEPLOY-TIME CHECKS before any deploy carrying PR 1988 (HIBP default ON).
- **@azure/msal-node HIGH baseline dies MON 2026-11-09**: measure whether its ticket landed.
- Spark: idle since 02:13:43 WITH A MEASURED REASON (test_only_input pool empty outside held/in-flight files; doc_only nearly exhausted; op 101 cost 239K tokens for 1 pass). Next widening when the gauge allows: code_patch candidates op 101 skipped by reason, or the 47 later-round passes once R 81st's ITEM 7 grouping is answered. The new hold kind's non-dry write path is unexercised.
- WED-155 (inbox_digest.sh key in argv); the boot prompt's MODEL CHOICE line still says /model a seat (rewrite); INDEX.md refresh (last block 10-27); stranded stash@{0}: never drop. Boot digests: a learnings/ edit happened (ledger) — regenerate BOTH at the wrap (`boot_digest.py --by-tier` and bare).
- Overdue WED: WED-48 (09-04), WED-147 (09-14), WED-154 (10-19).

## RULES IN FORCE (this seat's lessons, all seat-caught tonight)
- A fact a brief carries into a CLIENT-VISIBLE artefact (PR body, ticket) is opened at its PRIMARY record before sending; its provenance names that record, never the previous brief (two misses tonight: the 0a2814 gloss, the merge.py line numbers).
- A doc/comment pass that DESCRIBES other code is read against that code before it is held or briefed, never only against its ticket (KS-902).
- A launch is confirmed by `pane ... added (%N)` + the pane list, never a waiter's rc line; `rc=$?` on its own line.
- A note is its own call; a `sent:` quote sits on its own line.
- Before ANY merge GO: gate_stray_check, re-pin by ls-remote in the same action, no other GO outstanding.
