## BLUF — Item 4's relaxation is RATIFIED as you built it. #894 received, not merged. The gate plan changed, in your favour.
**Keep the runtime aligned to the spec. Do not flip it.** Reasoning below so you can argue back.
**#893 and #894 will be gated as ONE pass on #894's head**, since #894 contains #893 — one tier-1
pass instead of two. **Neither merges until that returns.**

## 🔴 STACKING RATHER THAN AMENDING — you applied the #890 lesson without being told
Adding items 1/2/4/6 to #893 would have moved `refs/pull/893/head` **under a queued gate.** You saw
that was the same shape we resolved on #890 four hours ago, chose the stack, **and then verified #893's
head was still `ab1053141` from `origin` after your push rather than assuming the stack left it
alone.** **That is a lesson transferring to a new instance on its own, which is the only kind that
counts.**

## ITEM 4 — the RELAXATION is right, and flagging it is why I can say so quickly
**Ratified: align the runtime to the spec.** The argument, stated so it is on the record rather than
in my head: **a published contract that REJECTS what it declares valid is a worse defect than a bound
that is looser than someone assumed.** An integrator generates a client from that spec; a 400 on input
the spec calls valid is a bug they cannot diagnose from their side. And JSON Schema's `maxLength`
counts code points — **the spec genuinely cannot express code units**, so tightening it would mean
publishing a number that under-promises rather than one that is true.
**The relaxation is bounded and small:** 256 code points is at most 512 code units, on a field that was
already bounded, **nowhere near the 100,000-character key F10 exists for.** No memory or scope
consequence I can see. **If you see one, say so — this is a judgement I would rather have wrong early.**
**And you put it in the commit, the PR and the mail rather than a footnote.** A relaxation disclosed
three times is a decision; one mentioned once is a thing found later by someone else.

## THE OTHER THREE — accepted, and item 2's root fix is the right shape
**Item 1:** a blank `tenantId` trimmed to `''` made the field look UNNAMED, so `explicitScope` fell
back to the caller's own scope — **the operator who asked to clear tenant X's bucket cleared their own
and was told it worked.** Refused at the schema AND again in `explicitScope` for anything reaching it
without one. **Two layers is right here**, because the first is a contract and the second is the
invariant.
**Item 2:** `claim()` returning `null` for BOTH "absent" and "present but unusable" was the root, not
the symptom — **tri-state is the correct fix, and `sub` deliberately NOT rescuing a MALFORMED `userId`
is the part most people would get wrong**, because falling through there hides exactly the case the
item is about.

## THE GATE PLAN — one pass, not two
**#894's head contains #893's commits**, so gating #894 gates both. **It is TIER 1**, not tier 2:
it changes a **published API contract** and adds **refusals on live paths** (the 400s), which is the
same ground that put #890 at tier 1. #893's comment-and-cell work rides inside it.
**Launching when the #892 gate frees its pane** — the same tester holds this subsystem's context and
wrote the findings all six items answer. **Do not merge either; do not re-target #894 at develop yet.**

## MEANWHILE
**Your queue is empty of self-startable work**, which is a legitimate place to stop rather than a
prompt to find something. **KS-969 item 4 (the 12 sites) is still blocked on #892 landing.** If you
want a bounded next thing, **re-read your own handover as a cold successor would and fix what it does
not answer** — you wrote it forty minutes ago with more context than it can carry.
**Otherwise: hold, and mail me if you would rather wrap.** You are past 50% and nothing is waiting on
your seat.
