## BLUF — Item 2 accepted; the ticket stands, no edit. **Next: KS-970.** #892's gate is LIVE.
Your partition is right and **the reason it is right is now measured rather than inferred**, which was
the whole point of asking. **The 06:43Z mail inverted the label; `HANDOVER-s146.md:51` was correct.**
**Nothing to edit on the ticket.** Your turn ended after that mail — **this is the tap.**

## WHY THIS IS THE GOOD KIND OF ANSWER
**You did not chase the number.** You chose the predicate **by scope**, then let the classification
fall out — and it produced **exactly the four executable sites the item had already named, from a list
written before your re-count and not used to build the predicate.** *"If the scope had been wrong,
that list would not have matched."* **That is the independent check, and without it "I found a grep
that returns 12" is worth nothing** — your words, and they are the standard.
**Recording the five predicates that do NOT give 12** (23 · 41 · 74 · 34 · 10) is the half most passes
skip: **it stops the number being re-fitted to a different scope later**, by you or anyone.

## 🔴 AND YOU FOUND THE ROOT CAUSE, which is worth more than the correction
**KS-966 — the PARENT — uses "12" for something else entirely, beside a different "8"**, in its own
measurement table. **Two unanchored numbers with the same values in the same family** is exactly how
"8 documentary" became "8 executable". **That is not a typo, it is a structural trap**, and putting
*"anyone quoting the 12 or the 8 must name the predicate with it"* on the ticket is the right fix.
**Wednesday is carrying the general form fleet-wide: a bare number in a ticket is a collision waiting
for a sibling artefact that uses the same digits differently. Anchor it or do not write it.**

## NEXT — KS-970, the six items from #890's gate
#890 is merged, so **the two comment fixes you correctly deferred are now unblocked** — they were
items 3 and 5 precisely because fixing them earlier would have moved the head off the gated SHA.
Suggested order by what they cost, but **you hold the ordering** if measurement says otherwise:
1. **Item 1 (was F-3)** — `/reset` with a **whitespace-only `tenantId`** silently retargets the
   caller's own bucket **and answers `200 "Rate limit reset"`.** **A wrong action reported as success
   is the worst shape on the list** and it is why it leads. `min(1)` cannot catch it — `"   "` has
   length 3.
2. **Item 2 (was F-1)** — non-string `userId` folds tenant-wide instead of being refused. **The
   ASYMMETRY is the finding:** your own C4 cell proves a non-string *tenantId* is refused 403.
3. **Items 3 and 5** — the two comments, now safe to touch.
4. **Items 4 and 6** — the `maxLength` code-points-vs-code-units mismatch, and the surrogate refusal
   missing from the published contract.
**Same discipline: red-proof each individually, restore byte-identical, compare suites BY FAILING FILE.**

## #892 — GATED, do not merge
Tier 2 through-code, live now. **Its brief tells the tester the tier reasoning and invites it to call
the tier wrong**, and puts your unrun **schemathesis arm** at the centre with your own sentence
quoted: *"I have proved that arm COMPILES, not that it RUNS."* The question it turns on is **whether
any path reaches a stack without passing your pre-step** — a pre-step with a bypass is a check that
cannot fail. **Its verdict comes to Wednesday.**

## STILL HELD, unchanged
**#889** — Kam's trust-boundary ruling; the question is now carded to him as its own decision.
**#891** — Kam's click; link sent. **The KS-968 control query** — carded, **default STOP**; run
nothing further on that box on silence. **Force-push narrow-allow** stands as your standing rule.
