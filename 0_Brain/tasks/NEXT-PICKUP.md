---
date: 2026-11-03
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 13:45 AEDT 2026-11-03 by the 13:3x rotation-successor seat. Previous kept as NEXT-PICKUP.md.pre-1103-1345 (its 11:2x / 10:24 / 09:41 blocks are history). Replace wholesale; never stack.
---

# NEXT PICKUP — Tue 3 Nov 2026, 13:45 AEDT (13:3x successor seat, ctx 56%)

## 🔴 FIRST WORK, in order (refreshed 14:3x at the 70% checkpoint)
0. **Seat B 84th %108 (Sonnet merge seat, plan CONFIRMED 03:28Z):** PR 1984 QUEUED 03:28:55Z (head 68897dda, gate 167 GO WITH NOTES; Wednesday ruled G167-F1 NOT a hold). It finishes ITEM 0a (3 declared helpers re-keying 27 tools), runs its 7 controls on merged PRs, then sends READY TO MERGE 1984. Read it WHOLE (Read tool), pre-GO checks, GO subject `GO: merge PR 1984 at 68897dda9410 on develop <pin12> (Seat B 84th)`. After the merge: the KS-1572 FLOW FRAGMENT still says "No fraud decision changes" -> a docs-only follow-up (F 26th's HANDOVER FIRST ACTION: `.../5_Project_History/2026-11-03_seatF-26th/HANDOVER.md`) for the next build seat.
1. **Seat S 15th %107 (Opus, KS-1961 then KS-1962 fail-closed):** plan CONFIRMED 03:10Z (13 rulings in Wednesday's ANSWER; incl. NEW negative rateLimitWindow + KS-616-fallback-throws in scope; not-connected fallback kept; registry missing table = not trusted). Building red-first. At each READY -> an Opus T1 gate (gate 168 PR 1, gate 169 PR 2) with `2_Project_Files/fleet/qa-agent/gate_common.md` pasted whole. Kam told the login-503-in-outage cost (panel bf-aaceb917338a). Cards 1970/1976 marked --delivered.
2. **PR 1982 (Peter's restore script) = gate 166 NO GO round 2 of 2 (the CAP).** Verdict `0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2/verdict.md`: all gate-165 items closed, 28 NEW forms slip (interpolation, TAB/CR/LF in host key, bare CR, BOM, NBSP). **KAM CARD `secuura-pr1982-restore-script-round2-nogo-1103`** (rec a: rebuild the check on the real readers, docker compose config + dotenv; default: nothing merges, E 30th wraps, Peter not told). E 30th told: no round 3, one KS-915 comment, HANDOVER, wrap. When E 30th wraps: verify, score, pane_close %103. If Kam = a: brief a fresh build seat from E 30th's HANDOVER + the verdict.
3. **Spark:** operator 95 (Sonnet subagent of THIS seat; workdir `0_Brain/reference/2026-11-03_spark-operator95/`, report.md at the end) refilling KS-1868 passes; if it dies at rotation, re-commission from its workdir + operator 94's. Operator 94's 4 last passes HELD and committed (29089d66).
4. **Lanes EMPTY:** R (raise seat owed for O91 x11, O92 x10, O93/O94 holds + R 78th ITEM 4a-c), F (KS-1572 fragment follow-up after 1984 merges), W. Launch at ROOM.
5. **DISK:** DevMASTER 26 GiB free (99%). KAM CARD `wed-gate-clones-fill-devmaster-1103` (rec a: remove merged-PR gates' ignored clones; default b: nothing removed, re-raise at 15 GiB). Re-measure `df -h /Volumes/DevMASTER` at every checkpoint. Never `du` over all gate dirs (423 dirs; it ran past 120 s).

## KAM
- Cards OPEN (5 = 4 Secuura + 1 WED, 14:3x): `secuura-pr1982-restore-script-round2-nogo-1103` (rec a, default nothing merges), `wed-gate-clones-fill-devmaster-1103` (rec a, default b), and the earlier three: `secuura-auth-lockout-failopen-redis-down-1103` (default a ~15:40: a seat files the ticket + queues the fail-closed fix AFTER KS-1961/1962 → add to S 15th's queue by ANSWER); `secuura-hibp-breach-check-never-runs-1103` (24 h: ticket, nothing built); `secuura-pr1979-ambassador-bonus-starts-paying-1103` (nothing merges). KS-1966 (gateway rotated:true) fail-closed remedy = REVISITING a Peter-reviewed design (KS-1152 R-880-1): bring to Kam with the other fail-closed rulings, not yet carded.
- Kam silent since 11:17:59. Panel status posted 13:3x (bf-15a14259a5b8).

## TODAY'S MERGES (Wednesday GOs, this afternoon chain): 1972-1977, 1970, 1980, 1978, 1981 = 10. develop 27fe5476526c (ls-remote 13:41:16). PR 1968 HELD. PR 1979 on Kam's card.

## RULES IN FORCE (today's ledger)
- Seat launch = its own call AFTER reading the dry run's CAPACITY line; FULL -> waiter, its armed line read in the next call.
- Never grep -r / find over the WEDNESDAY tree or local-model runs/ night/; a call auto-backgrounded at timeout is stopped or justified the same turn.
- Read every READY / mail body untruncated (Read tool or full sed), never through `cut`.
- A note is its own tool call, after the act's output is on screen; quote the act's own success line.
- No credential in argv (WED-155): headers via `curl -H @file` (0600, blanked after).

## OWED (not first-work)
- WED-155 (inbox_digest.sh lines 57/69 pass the AgentMail key in argv). gate_common.md now TRACKED at `2_Project_Files/fleet/qa-agent/gate_common.md` (claim OPEN in WED-OWNERSHIP: release after gate 166 uses it). board_count BOARD_COUNT_ZERO_OK accepts a refused control line (shared tooling, claim first). INDEX.md refresh. Ticket candidates for a board seat: G139-F1, G145-F3, G146-F2, G149-F4/F5, G154-F1, pool-listener C1 timeout. Regenerate BOTH digests at wrap if learnings/ changed.
