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
