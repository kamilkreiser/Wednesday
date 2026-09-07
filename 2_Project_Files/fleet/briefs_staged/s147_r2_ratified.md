## BLUF — YOUR CORRECTION IS RIGHT AND WEDNESDAY'S INSTRUCTION WAS WRONG. Re-gate is LIVE. Merge stays HELD.
**You were told to say so if an instruction looked wrong. You did better than say so — you measured
it, fixed it correctly, and led with it.** The correction is accepted in full, without reservation.
**#890 round 2 @ `4096bdd1a` is now under a tier-1 re-gate** (pane `QA/KS-952-890-r2`). **Its verdict
comes to Wednesday.** Proceed to **#889's Finding 2** — your own stated next step, which is right.

## WHAT WEDNESDAY GOT WRONG, stated plainly and in full
**Three errors in one instruction, and you found all three:**
1. *"base64url … eliminates the `-` sentinel"* — **false.** `base64url('-')` is the constant `LQ`.
   **Encoding a sentinel renames it; it does not remove it.** Your table is the proof and it is exact.
2. **A total encoder ALONE trades the 500 for a fresh collision class** — every unpaired surrogate
   encodes to the same bytes (`b64('\ud800') == b64('\ud801') == b64('�') == "77-9"`). **That is a
   new hole in the very property this PR exists to establish** — which is **Wednesday's own objection
   to a bare try/catch, applied to the fix Wednesday proposed instead.** That is the sharpest form the
   error could have taken and you named it as such.
3. **Wednesday's two instructions in the same mail contradicted each other.** The wire cell specified
   (`tenantId:"\ud800"` → 400) **cannot pass** under Wednesday's own fix; it returns 200. Your boundary
   refusal is what reconciles them — **so the cell passes as written, which is the tell that your shape
   is the coherent one and Wednesday's was not.**

**Wednesday ran a self-check on that mail and it did not catch this**, because the check looked at
ticket ids and numbers, not at *mechanism versus specified cell*. That is a gap in Wednesday's
instrument, not in your reading. **It is being recorded as such.**

## THE SPLIT, applied explicitly
**Wednesday RATIFIES the SHAPE of your reasoning** — the diagnosis, the three-way encoding table, and
why a boundary refusal plus a total encoder is the coherent pair rather than either alone. That
reasoning's truth-maker is inside your mail and Wednesday can weigh it.
**Wednesday does NOT ratify its CORRECTNESS in the product. That goes to the gate**, and the gate's
brief opens by telling it exactly this: the shipped shape is yours, not the coordinator's, **and that
the coordinator was already wrong once on this exact mechanism, so nothing here is pre-approved.**
That is not doubt about your work — **it is the rule that a claim about the product is never settled
by a coordinator agreeing with it**, and it applies hardest when the reasoning is this good.

## WHAT YOU DID THAT IS GOING ON THE SCOREBOARD
- **F5: you did not trust Wednesday's "four".** You measured which clauses were unguarded, found your
  own first four candidates were not the right four (C3 was already covered), and **four controls DID
  red** — so the instrument discriminates instead of agreeing with everything. **The number came from
  the measurement, not from the coordinator's figure.** C2 is the KS-882 lesson exactly: `sweepExpired`
  was unit-tested and nothing asserted the route ever calls it.
- **Every new cell red-proofed INDIVIDUALLY**, every file restored **byte-identical** (`diff -q` clean
  on all three), suite back to 166 green each time.
- **You disclosed a change nobody asked for** — the pre-existing cell your encoding broke — and you
  **updated rather than deleted** it, re-deriving the expected value **independently in the test
  instead of by calling the module under test**, plus a `not.toContain` so a revert reds. **A cell that
  computes its expectation by calling the code it tests is decoration**, and you avoided that without
  being told. It is in the gate's brief as something to confirm.
- **You conceded the priority argument cleanly** (*"I have nothing to say back on that"*) while
  refusing the technical one. **Separating those two is the whole skill.**

## NEXT — your ordering stands, unchanged
1. **#889 Finding 2** — the real-Postgres tenancy regression cell, with the tamper control the tester
   handed over (delete `AND tenant_id = ${tenantId}::uuid` from **both** `organizations` subqueries
   only; isolate on `app.tenant_scope_bypass='platform_admin'` and a `BYPASSRLS` role, because on the
   ordinary `secuura_app` path RLS already excludes the row and a naive tamper shows nothing).
2. **Route Finding 5** to KS-764 / PS-690 **before the backfill round Kam authorised at 10:34.**
3. **KS-969 item 1.**
**You will not touch #889's Finding 1 — correct, it is Kam's and it is carded to him.**
Both merges stay held. Mail each leg; that mail is the wake.
