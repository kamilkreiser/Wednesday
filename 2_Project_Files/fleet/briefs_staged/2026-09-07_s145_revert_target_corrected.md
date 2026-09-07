## 🔴 BLUF — STOP. Wednesday's revert target was WRONG and it would have put Kam's real address back into the repository. You are right; the target is ROUND-1 HEAD, not base.
**Do not revert that file to base. Your drift guard caught Wednesday's error and it was the correct
call to stop on it.**

## THE ERROR, owned precisely
Wednesday's `split` brief said:
> *"`git diff <base> <reverted-head> -- …/startup-migrations.ts` — if that is EMPTY, the file is
> byte-identical to base, F1 is fully gone."*

**That is wrong, and the reason is the whole point of this ticket.** The file's history on this branch:
- **base (develop `61df129e9`)** — old conflict handling **AND KAM'S REAL ADDRESS**, unredacted.
- **round-1 head (`a98df6b11`)** — the address **REDACTED**, conflict handling still the old broken
  `ON CONFLICT (email)`. (The round-1 gate said exactly this: *"the PR redacted the address on line
  960 but did not change the conflict handling."*)
- **round-2 head (`6dbe63cae`)** — redaction kept, **plus** F1's conflict-target change.

**So "revert F1" = restore that file to its ROUND-1 state.** Reverting to base would have undone the
redaction too and **re-introduced the real address into the tree** — the exact thing this ticket
exists to remove, put back by the instruction meant to make things safer.

**CORRECTED PROOF — this is the check to run:**
```
git diff a98df6b11 <reverted-head> -- Blockchain/Dev/services/api-gateway/src/startup-migrations.ts
```
**EMPTY = F1 reverted and the redaction intact.** Keep the control from the original brief (a file you
DID change must show a NON-empty diff in the same command shape), **and add a second, decisive one:
grep the reverted file for the fictional address and require a HIT** — a positive control that the
redaction survived, rather than inferring it from an empty diff.

## WHAT CAUGHT IT — and this is worth more than the error cost
**F4's drift guard.** The guard you built this round — the one that enumerates seed sites from the
tree instead of a hand-written list — **fired on Wednesday's own instruction** and told you the real
address was back in that file. **A guard written this morning caught the coordinator's mistake this
afternoon, on the very file it was written to protect.** That is the strongest possible argument for
building guards into the path rather than keeping rules in briefs, and it is going on the scoreboard
in those terms.

**And you did the right thing twice over:** you noticed your own diff had run from the wrong directory
and printed nothing, **re-measured from the repo root rather than trusting a zero**, and only then read
the guard's finding. **A zero from a wrong path is the check-that-cannot-fail wearing a shell's
clothes**, and you have now caught that exact shape twice today.

## UNCHANGED
`split` stands. Revert F1 **and its suite** (`ks949_main_seed_idempotence.test.sh` asserts the fixed
behaviour and will fail once F1 is gone). Re-run leg 12 so the tracked-suite count moving 15 → 14 is
measured. Push one head; Wednesday's completion check; then you merge on the GO.

**The `NODE_ENV` read stays authorised** under Kam's Secuura production grant — one value,
pre-registered, nothing else read.

## WHAT WEDNESDAY IS DOING WITH THIS
Telling Kam, leading with it, in the next message. **The honest version is that Wednesday wrote an
instruction that would have re-published his address, and a guard the fleet built this morning is
what stopped it.** Filed as a correction — Wednesday specified a target without asking what that file
CONTAINS at that target, which is the same root cause as the F1 ratification two hours ago: **a fact
about the artefact's CONTENT not carried into a decision about the artefact.**

## PROVENANCE
- The file's three states | your measurement this action, plus the round-1 gate's verdict quoted above.
- The drift-guard hit | **yours**, quoted, not re-derived by Wednesday.
- Kam's `split` ruling | panel 12:13:21. His production grant | 12:07:38, Secuura-only 12:10:40.
