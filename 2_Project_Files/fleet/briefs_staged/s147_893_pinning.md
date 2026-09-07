## BLUF — #893 received, NOT ratified, NOT merged. Its gate is QUEUED behind #892's, deliberately.
**Continue with KS-970 items 1, 2, 4 and 6.** Splitting the comment defects from the behaviour and
published-contract changes was right, and **not folding them in silently is the part that matters** —
a PR that quietly grows past its stated scope is how a gated head stops meaning anything.

## 🔴 "I STOPPED REWORDING AND STARTED PINNING" — this is the best judgement call of your session
**Twice today a comment of yours claimed a property the code did not have** (the F3 mechanism on #888,
and this one). **You noticed that correcting the prose a third time would be the same move that had
already failed twice, and you changed the KIND of fix rather than repeating it.** That is the
difference between fixing an instance and fixing a class, and almost nobody makes that turn on their
own error.

**The corrected claim is now three CELLS, and the third one is why it works:** a control that two
ordinary tenants do **NOT** share a namespace — **without which the residual cell would pass on an
encoder that collapsed everything**, a far worse defect than the one it documents. **A cell asserting
a limitation, with no control proving the non-limited case still works, is a cell that cannot fail.**
You saw that and built the control in.

**And your stated limitation is a feature, not a caveat:** the residual cell asserts CURRENT behaviour,
so it **reds if someone later makes the encoder injective over surrogates**. **That is exactly right —
it forces the comment to be updated WITH the fix rather than left behind**, which is the failure this
whole item exists to correct. **Say that on the ticket in those words if it is not already there**, so
the next person who reds it understands they are being told to update the claim, not to delete the cell.

**Wednesday is carrying the general form fleet-wide: a comment that makes a claim about BEHAVIOUR
should be a test, not prose. Prose rots silently; a cell reds.** Your two wrong comments today are the
evidence, and your fix is the rule.

## ITEM 3's MEASUREMENT — accepted, and the honest framing is the right one
`\ud800`, `\ud801` and `�` all encode to `77-9` and collide, **with a control on two ordinary
tenants proving the instrument discriminates.** And the mechanism named at source: `explicitScope`
falls back to `principalScope(caller)` whenever the body names no scope, so **`/reset` reaches the
encoder through raw claims exactly as `/check` does** — `resetRateLimitSchema` guards BODY fields and
never sees a claim.
**"Close to unreachable is not refused, and that difference belongs in the comment rather than in a
reader's assumption"** — correct, and it is the sentence that distinguishes a documented residual from
a hidden one.

## WHY THE GATE IS QUEUED RATHER THAN LAUNCHED NOW
#893 is **tests and comments only — no executable line of `rateLimitScope.ts` touched** — so it is
**tier 2 through-code**, not tier 1. **It will be gated by the same tester that gated #890**, which
already holds this subsystem's context and wrote the findings #893 answers. **Running a third
concurrent pane to re-learn what that one already knows is waste**, and the change is not urgent:
nothing ships until #889's ruling and #892's verdict land anyway.
**So: #893 waits for #892's verdict, then gets its pass. Do not merge it, and do not treat this queuing
as an acceptance.**

## STILL HELD, unchanged
**#889** — Kam's trust-boundary ruling (carded). **#891** — Kam's click. **#892** — gate live, verdict
comes to Wednesday. **KS-968 control query** — carded, **default STOP**; nothing further on that box.
**Force-push narrow-allow** remains your standing rule.
