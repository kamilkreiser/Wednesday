---
date: 2026-10-19
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 08:4x Wednesday seat at its 70% checkpoint, 2026-10-19 ~11:5x. Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1019-1150 + git.
---

# NEXT PICKUP (Mon 19 Oct, midday)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh (the WHOLE day, never a count from a wake), reconcile_rulings.py, `tools/newmail.sh` (to a file; if it FAILS LOUDLY on a JSON decode, re-run once), fleet_ack.sh list, decision_queue.sh list open, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`.
2. **In force:** Kam 10-18 "new account: tickets, backlog, routing definition, Spark as many as it can handle" (EXPIRING-GRANTS top row). Routing v1.0 (every launch receipt names its row). Gauge 25% at 11:47.
3. Commit your own files by pathspec before any tool that pulls (wed_claim now refuses on a dirty tree, rc 9).

## 1. LIVE WORK (11:5x)
- **develop = 78cb3c3939e319332e387ffecb075a169edd4a39** (tree 1ca89b2b5b72; #1589 merged). 27 Secuura merges since 19:00 Sun. Nothing deployed.
- **GATE O1 (Opus, tier 1, background sub-agent of THIS seat):** #1597 KS-1634 8ec96bbac643 · #1590 68270e124aac · #1596 83b5758bc779 · #1598 35a5fcb93c53 · #1599 73101f01c32e. Brief + verdict: 0_Brain/reference/2026-10-19_gate-O1-tier1-five/. **GATE O2 (Sonnet, tier 2):** #1591 a992894cdbf7 · #1592 ac758817103c · #1593 587fe9dbf0a7 · #1594 2cda8fe5243f · #1595 46795487b69c · #1600 6499cce63ab9 · #1601 c08b786603c3. 0_Brain/reference/2026-10-19_gate-O2-tier2-seven/. On each verdict: re-hash its sha (line 6 / line 8 deleted, plus a control), ls-remote the heads, then GO per PR to the R LANE (head-pinned, re-predict onto live develop). **#1597 is NOT merged until its author force-push is done** (item below).
  - **If this seat rotated before the verdicts landed:** the sub-agents die with the seat. Read whether the verdict files exist. If not, re-launch from the same briefs (and say so).
- **Seat R 51st** (%10, launched 11:47, brief fleet/briefs_staged/2026-10-19_seatR51_successor.md): plan confirmation owed (rung 5/6). Switch it to Opus 5.5 at its first idle (launcher pins "Opus 5"). Queue: the O1/O2 GOs → the SCREEN_11 batch (KS-1377, KS-1617 x2, KS-1507; prepared by R 50th, overlap 0/35) → ONE batched READY → KS-1638 (the hook fix, tier 1) → the #1597 author-only force-push (ALLOW_FORCE=1, tree b64be7e50092, amended commit 8f3310c6ed85, recipe in R 50th's HANDOVER) → KS-1622's widened scope.
- **Seat J 13th** (%6, Opus 5.5): Kam ruled KS-1612 round 4 = a (narrow, the LAST). J was told to mail its DESIGN first. Wednesday rules it on the deciding question (does dropping 051's pk arm reopen any of MAJ-A's four minters; MAJ-B on a real PG; MIN-A via real Prisma; KS-1633 out), then J builds, then ONE full Opus gate.
- **Drive clean-up (b) sub-agent (Opus, background):** gatesets older than 14 d removed; Qwen3.8-Flash + Qwen3.5-122B oMLX and the unreferenced Ollama models MOVED to `/Volumes/G-DRIVE/WED/models-archive/2026-10-19_*` (Ornith 1.5 kept). Report `0_Brain/reference/2026-10-19_dev-drive-survey/CLEANUP_B.md`. Verify: df on both drives, `ollama list` + `ollama show` on the kept models, the oMLX Ornith folder present; then tell Kam the GB.
- **OWED, not started:** Testing Agent MAIN's ~285 GiB of Secuura QA scratch (Kam's (b); survey row 1; `!CODING/Testing Agent MAIN/projects/secuura/reports/*/{wt*,work*,clone*,scratch*,tmp*}`). It is THAT project's files: Wednesday may not remove them, and there is no cockpit lane. Launch a Claude session in that project folder with a brief citing card `wed-devmaster-drive-cleanup-1019` = b (liveness, counts, df, quarantine nothing, remove regenerable only).
- **Storage done today:** round 1 304.51 GiB (D 20th), round 2 42.85 GiB (D 21st, 16 removed / 11 kept). DevMASTER 73%. Not raised (under 85%): the 11 KEEPs need a named amendment; the 8 deploy clones are unruled. Next weekly dry run: the W class is larger under the stricter predicate (D 21st's note).
- **Spark:** queue empty ON PURPOSE with a measured why line (SCREEN_10 + 11 exhausted the lane-free pool; 18 PASSes held today). Next screen when R's batches merge (that frees files). KS-1546 is a Claude-seat candidate (the builder does not run check.cjs).

## 1b. RULED BY WEDNESDAY TODAY, STILL OPERATIVE (Secuura)
- KS-1628 L1/L6 = (iii) → KS-1634 (High; census 0/0). N1: no in-repo caller moves.
- #1597's force-push: (iii) now, then (i). KS-1638 first; `ALLOW_FORCE=1` accepted (the hook's own opt-in); `--no-verify` refused. Kam's card b is DEFERRED, not withdrawn.
- KS-805 Closes (with the spec half). KS-1471 Closes. KS-1544 Refs (no behaviour cell in that PR). KS-1525 Refs (measured G7/G8 posted). KS-1622's widened scope = R's Claude build.
- KS-1624 F1 = (a) (done). F2/F3 and KS-1623 N2 UNRULED, not queued. KS-1625 (Node floor) filed, no fix.

## 2. KAM'S CARDS
All of today's Secuura/WED cards are RULED. To deliver (`decision_queue.sh --delivered`): `secuura-datasec-author-on-two-branch-commits-1019` (after the force-push), `secuura-ks1612-round3-nogo-1019` (after round 4's verdict), `wed-devmaster-drive-cleanup-1019` (after CLEANUP_B + the QA-scratch session). `wed-secuura-storage-27-held-worktrees-1019` is DELIVERED. Datasec's `composer-l05-setup-card-too-1014` is Tuesday's.

## 3. OWED BY WEDNESDAY (own tools, small)
1. cockpit.sh say --mail: stamp the mail's timestamp into the pointer; `say %4` (pane id) is a silent no-op: fail loudly.
2. pretooluse_no_cd.sh: allow a variable path that resolves inside WEDNESDAY or the session scratchpad.
3. Deploy round (Kintsugi): READ-ONLY census seat first, once tasks/DEPLOY-BLOCKERS.md clears.
4. Fable 5.1 coordinator-task trial (routing decision 7).
5. The 95 `t <t@e.com>`-authored commits on develop (R 50th's flag): check whether they are tracked.
6. Keep stash@{0} and older stashes; never drop them.
7. From the 10-19 consolidation: cockpit `say` "queued" case; the "next-up" stall; `stamp.sh`; a DKIM helper. PROMOTION OWED: a send_brief.sh --kind answer advisory for a RULED code shape with no `read <path>`/`unread` clause (arms first).
