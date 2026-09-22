# Why the Ornith queue is empty — 2026-09-20 17:0x

Written because "I didn't find anything" is not an artefact and a silent empty queue
breaks Kam's 2026-09-18 09:16 standing rule without saying so.

**The queue is empty by a DELIBERATE pacing decision, not for want of candidates.**
`night/candidates.md` holds 386 rows and the pool is not dry.

**The reason: the weekly Claude allowance.** Measured with `fleet/usage_gate.sh --check`:
**83% at 16:45, 85% at 17:05** — ~2 points in twenty minutes, against the ~1.3 points/HOUR
the card `wed-allowance-pace-before-week-away` assumed. Kam's cut is 90% (2026-09-14 19:14:
at 90% no new agents or gates; in-flight finishes; Wednesday works with Ornith only), and
the allowance renews **Fri 25 Sep 8am AEST**. He is away from **Monday night 2026-09-21**.

**Feeding Ornith is not free: the brief IS the cost** (2026-09-18 lesson). Each brief is a
Claude subagent, and its tokens come from the same allowance as the QA gate now running on
#1100/#1101 — which is the main line and is time-boxed by tonight's 23:00 merge cut-off.

**So the ordering is deliberate:** the gate, the GO and the merges first; the next Ornith
brief after the gate returns, if the allowance still allows it. **This is a routing decision
and it is Wednesday's** (Kam's 2026-09-16 grant makes routing hers, and the misroutes hers
to own).

**Two fixes are already HELD and cost nothing to raise later:**
- `READY_KS-1275-ORDER-1_…PASS-8of8-REBRIEF1_2026-09-20.diff.md` — raise as `Refs KS-1275`.
- `READY_KS-1203-UNTYPED-1_…PASS-8of8_2026-09-20.diff.md` — raise as `Refs KS-1203`, and it
  applies with `--recount`, NOT strict.

**What the next seat does:** if the gate has returned and the allowance is under 90%, brief
the next candidate immediately. If it is at or over 90%, do NOT — that is Kam's rule, and
the two held fixes are the work that is already banked.

---

## AMENDMENT 17:1x — the pause was BROKEN and then RESTORED, by Wednesday, and the record should say so

Minutes after this file was written, **Wednesday resumed the brief-writer anyway** — reasoning that Kam's pace card is ruled `spend-to-90`, that 85% is under the cut, and that resuming a loaded agent is cheaper than a fresh one. **That reasoning was not wrong, but it was not MEASURED against the thing that matters, and it contradicted a decision already written into this file.**

Re-derived properly, which is what should have happened first:
- The banked fixes (KS-1275, KS-1203) **have no route to a PR tonight**. The one raise seat is occupied holding for its GO; after the merges there is no room for another raise round before the **23:00 merge cut-off**.
- So a THIRD banked fix has **low marginal value tonight** and a **real cost** against the gate now running on #1100/#1101, which is the main line and the thing Kam actually asked for ("close, archive merge and deploy anything that's ready").

**Both agents were stopped and the pause stands.** `spend-to-90` is a ceiling, not an instruction to spend; under it the ordering rule is still Kam's own — **the cheapest closes first**, and merging work that is already gated is cheaper than manufacturing new work to gate later.

**The lesson, which is the point of writing this down:** a pacing decision recorded in an artefact is a decision, and re-opening it needs a measurement, not a recollection of a grant. The grant said what the ceiling is; it never said what the priority is.

## 2026-09-22 04:44 — queue EMPTY after FEED 4 (the 03:45 seat)
**Why empty:** FEED 4's drafter read the whole pool at develop 64ab10513 — T5 multi-file 30/30 (1 briefable → KS-1231 split A/B, both PASS + HELD), headline-named 23/23 (0 briefable: 15 not on the open board, 3 In Progress with PRs, 4 own a READY, 1 shipped), the FEED 3 easy-tier skips 11 re-read (0 lapsed). FEED 3 had already found 2 briefable of 38 at T1–T3. The rebriefs the seats' typechecks produced (KS-1171 ×2, KS-1123 F3b, KS-1192) all ran round 2 and PASSED. **Every tier is thin by measurement, not by feel** (`briefs_staged/2026-09-22_ornith_feed3.REPORT.md` §0.1, `…_feed4_queue_proposal.md` §disposition).
**What refills it next (in order):** (1) the gates' NOT-PINNED rows from gate16B / gate16C when their verdicts land (each is a test_only brief); (2) the nightly `derive_candidates.py` re-derivation after the 16th round MERGES (closed/archived tickets fall out, new ones in — the KS board moved 17 tickets overnight); (3) a fresh board search commission (the 09-18 rule: widening = a search commission, not hand-sampling). **Not a refill:** the 68 older content-absent READYs and the FEED T product rows — those are a RAISE pool for a Claude seat (the 17th round), not Ornith work.
**Held pool at this line:** the 00:05 seat's handover said 31 R15 READYs; this seat HELD 8 R16 READYs (`ls night/READY_*R16*2026-09-22.diff.md | grep -c`), three of which supersede R15 rows (KS-1171 ×2, KS-1123 F3b) and one a 09-17 row (KS-1192) — so the raise pool is 31 − 4 + 8 = 35 by arithmetic on those two reads, unmeasured as a single listing; the seats' briefs and the pickup are the authority per round.

## 2026-09-22 07:57 — the 07:2x seat: FEED 6 drained (KS-1188 MFASIBLINGS PASS 8/8, HELD; 12 R16 READYs today), queue EMPTY again — reason
- `derive_candidates.py` re-run at 07:57 after the twenty merges: 312 KS Backlog/Todo rows (was 314 at 04:57; T1 25 · T2 0 · T2b 5 · T3 4 · T4 1 · T5 29 · held 57 · set-aside 30 · excluded 161). The tier lists are the same rows FEED 3/4/5 already read: the easy tiers are thin by measurement (FEED 3: 2 briefable / 36 skipped; FEED 4: T5 30/30 read → 1; FEED 5: 194/194 → 3). The two gates' NOT-PINNED rows are spent (KS-1188 briefed + passed; KS-910 LEG12ZEROCELLS already pinned at the tip — the gate's row was over a narrow read).
- The honest next widening is a RAISE pool for Claude seats (the 12 R16 READYs + the un-raised older READYs — the round-18 raise-brief drafter is running), not more Ornith briefs. Ornith idles until (a) the 18th round's gate produces NOT-PINNED rows, (b) a ticket is filed that fits the contract, or (c) a search commission over the 161 excluded rows with a NEW predicate (the FEED 5 predicate is exhausted).

## 2026-09-22 12:53 — the 11:0x seat: FEED 10 drained (5/5 PASS, all HELD — 18 R16B READYs today), queue EMPTY since 12:22 — reason
- The FEED 11 brief-writer drafter is RUNNING in this seat (`fleet/briefs_staged/2026-09-22_ornith_feed11.COMMISSION.md`; precheck dir `runs/2026-09-22_feed11-drafter-precheck/` growing at 12:53): its §0 fixes the FEED 10 build defect (`suggested_test_file` == the brief's `File:`) before briefing KS-1028, KS-730-A, KS-1160, KS-1121, KS-976-B, KS-1097-A/Db. A brief-less input is a wasted round (09-18 rule), so the queue waits for briefs, not the other way round.
- Wake for the refill: the drafter's report (this seat) → Wednesday's checks → queue + kick. Bound ~60 min from 12:2x. If this seat rotated first: the successor re-commissions from the COMMISSION file if no proposal is on disk.
