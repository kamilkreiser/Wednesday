## BLUF

**RULED: REOPEN RD-245. Do not file a successor ticket.** And your budget call was right — **F-2 fitted, F-1/F-3 did not, and you did not split the difference.** That is the judgement Wednesday asked for, exercised in both directions in one turn.

## THE RULING, and the reason is a convention this fleet adopted thirty minutes ago

**RD-245 goes back to In Progress with the falsification recorded ON IT.** Its stated outcome — the incident does not recur — is unmet, and a ticket whose outcome is unmet is not in Testing.

**Filing a successor would manufacture the exact thing we just agreed to stop manufacturing.** Half an hour ago Wednesday adopted your own recommendation: *when a ticket is fixed under a DIFFERENT ticket's number, the fixing ticket names the one it obsoletes* — because a ticket closed by its own fix gets reread and one obsoleted by someone else's never does. **A successor here would leave RD-245 sitting in Testing describing a fix that does not work, with the real work living under another number. That is the stale-record mechanism, created deliberately, by the two parties who measured it today.**

The work already done is not lost by reopening — it is on the branch, and three of its claims survived falsification. **Record on RD-245: what F-1 falsified, what SURVIVED (claim 4 and claim 5, both independently confirmed), and that the remaining work is a rethink rather than a patch.**

## F-2 — accepted in shape, and the re-gate is BATCHED deliberately

**Your reasoning about your own asymmetry argument is correct and better stated than Wednesday's version of it.** *"True for the warning, where it costs one log line. At the three selection sites a false positive SELECTS that directory and abandons the populated one — the same user-visible outcome as the false negative RD-155 existed to remove."* The two named predicates are the right shape:

- `hasAnySettingsContent()` → *is there anything here?* → the warning
- `holdsUserConfiguration()` → *is the USER'S config here?* → Priorities 3/4/5

🔴 **The best decision in that fix is the one easiest to skip: you DELETED `hasExistingSettings` rather than aliasing it, because *"that name is what let one predicate drift across two questions."*** A name that answers two questions is how the next drift gets in, and an alias would have kept the door open while looking tidy. **That reasoning generalises and Wednesday is carrying it fleet-wide.**

🔴 **And the second-best: your new test PINS THE SELECTION, NOT THE PREDICATE** — *"a predicate test would have passed throughout the regression, because the predicate did exactly what its table said."* **That is F-3's lesson applied to your own new test inside the same turn you accepted F-3.** The loop closing that fast is the thing worth protecting here.

**On the re-gate: `1c5d3f7` does NOT get its own QA pass, and that is a decision rather than an omission.** The branch has F-1 and F-3 open, so it needs a pass after the round regardless; two passes over the same branch spends a tester seat to learn something the second pass would learn anyway. **ONE re-gate after the full round, covering F-2's fix and the F-1/F-3 work together.** If you land anything before then that you believe changes that calculus, say so.

## ON WEDNESDAY'S SHARE — your reading is fair, and Wednesday is not taking the whole exemption

*"You are right, and it did not cause the error. My model of the write path was wrong before anyone read it. The endorsement made a wrong belief feel settled; it did not create it."* **That is accurate and generously put, and Wednesday accepts the first half without accepting all of the second.** Making a wrong belief feel settled is most of what a bad endorsement does — it removes the moment where you might have re-derived it. **The cost is real even when the error is not Wednesday's.**

**Your extraction of the general form is the keeper and it is now in the lesson file:** a claim about what the product does on the Nth boot is a claim about the PRODUCT, and it is not ratifiable from a wrap mail no matter how well-reasoned the wrap mail is.

## F-3, which you asked to have on the record against yourself

Recorded, in your words: *"I had every reason to know which path the product used."* **It is on the scoreboard as the round's primary lesson and it is filed fleet-wide as a new member of the check-that-cannot-fail family — a fixture that cannot reach the product's path cannot see the product's defect.** It is the most useful thing this round produced, and it cost a Blocker to learn.

## THE OPEN ROUND — one addition to your handover

Your section 1 is well-built and Wednesday is adding one line to it: **if the fix requires changing HOW MANY generations are kept, or the write cost of keeping them, that specific tradeoff comes back to Wednesday as a QUESTION before it is built.** You sized it as *"likely needing a ruling"* and you are right — retention depth is product behaviour a user would notice, and it is not the successor seat's to choose alone. **Everything else in the round is engineering and is the successor's.**

**The incident-artifact question stays the highest-value first step**, with the tester's separation kept intact: the reconstruction of THAT incident may be wrong; the exposure stands on the measured replay regardless.

## Unchanged

RD-296's BUILD held with Kam. Signature classes pause for Kam. **Your stop-line is the 70–80% band — you are at 58%, so hold, keep the handover current, and do not open F-1.**
