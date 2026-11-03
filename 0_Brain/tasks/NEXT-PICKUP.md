---
date: 2026-11-04
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 03:19 AEDT 2026-11-04 by the 01:5x seat at its 65% checkpoint. Previous kept as NEXT-PICKUP.md.pre-1104-0319. Replace wholesale; never stack.
---

# NEXT PICKUP — Wed 4 Nov 2026 (the 01:5x seat's checkpoint handover)

## STATE (REFRESHED 03:4x at the 71% checkpoint — this block supersedes FIRST WORK items 1-3 below where they differ)
- **develop = ea5134d6b98c470615c59fca5d3ec30356adfbd7** (ls-remote 16:41:39Z) = **PR 1992 MERGED** by B 87th 16:27:08Z (squash tree 70bbceb1bf16 = the GO's; verified at source). **PR 1993 GO SENT 16:41:39Z** (head 8712cb115e0a, pin ea5134d6b98c, expected tree ce7a5d0d1a99a2f734011df3799b0d597ff4df11): on its MERGED mail verify at source (develop = squash, its tree = ce7a5d0d1a99, refs/pull/1993/merge gone + a control), then B 87th WRAPS (no further queue) -> score it, pane_close.
- **PR 1994** (= R 81st's PR 16, nft.routes.ts, head 74dc459edbb6, 1 commit on 79145a312f01, 11 files) is under **GATE 178** (Opus Agent subagent, background, tier 1; commission `0_Brain/reference/2026-11-04_gate178-ks1868-pr1994/commission.md`; verdict.md will land there). Two interim notices so far, no verdict. **A rotation KILLS it**: if this seat must rotate before the verdict, re-commission from the same file (round 1 restarts). On its verdict: GO (WITH NOTES) -> notes patch by an R seat, then QUEUE to a NEW merge seat B 88th (B 87th will have wrapped); HOLD-FOR-KAM -> card him with the cells.
- **Seat R 81st** (lane R, %117): after PR 1994 READY it is on the two doc PRs (KS-1320; KS-1343 P2B+P3B; single-key titles; ONE tier-2 Sonnet gate as a batch when both READYs land), then tickets 4a/4b, then ITEM 6 gate ticket candidates (G176-F2/F3, G177-F2/F3/F5/F7), ITEM 7 QUESTION. It wraps at 80-85% (watcher read 70% at ~03:3x): its successor R 82nd is briefed from its HANDOVER.
- **Seat B 87th** (lane B, %118): ctx 67% at 16:41Z; wraps after 1993.
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
