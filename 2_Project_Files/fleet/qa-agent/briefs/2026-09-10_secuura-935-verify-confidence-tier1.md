# QA GATE BRIEF — Secuura/Blockchain PR #935 (KS-1057) — TIER 1

## TIER AND WHY

**Tier 1.** This change alters what a **public verification endpoint tells a user about whether a
document is anchored**. That is the product's core claim, and the change is keyed on a field
(`blockchain.status`) whose absence in legacy rows is handled by an explicit carve-out. **The
carve-out is the risk, not the fix.**

## WHAT CHANGED, as the builder reports it — RE-DERIVE IT, DO NOT INHERIT IT

The builder (Secuura seat s164) states: api-gateway verify was **presence-keyed** — `confidence`
read `txHash && blockHeight` and never `blockchain.status` — so a **failed** anchor that carries a
hash could report as confident. The fix keys on status, with a **carve-out for rows that have no
status key at all**.

**Everything in this section is the builder's account, relayed by Wednesday, which holds no client
identity and re-derived none of it. Treat every sentence as a claim to test.**

- Branch: `feature/ks-1057-api-gateway-verify-is-presence-keyed-confidence-reads-txhash`
- PR head as reported: **`0b5ad9ac2`** — this is a MERGE of the KS-1067 lock branch into the fix.
- The fix commit as reported: **`1cc021a44`**. Two files: the fix and its test.
- Base as reported: `origin/develop` at `d4cf7e3cf`.

**FIRST: verify the head yourself from the PR, and if it has moved, gate the head you find and say
so.** A gate pinned to a SHA someone told you about is a gate on a claim.

## THE FOUR QUESTIONS THIS GATE EXISTS TO ANSWER

**1. Does the fix actually change the verdict for a failed-anchor-with-hash?**
Drive it. A code read proves the code; only a render or a response proves the artefact. Construct
or find a document whose anchor row is **failed AND carries a txHash/blockHeight**, call the verify
endpoint, and read what `confidence` comes back as — before and after.

**2. DOES THE CARVE-OUT HOLD, AND CAN IT FAIL?** The builder reports that **four seeded demo
documents — including the canonical OpenAPI example document (KS-481) — store `{txHash,
blockHeight, anchoredAt}` with NO status key**, and that a strict `status === 'confirmed'`
allowlist would flip all four to unverified. **Exercise this, do not read it.** Drive verify against
a statusless legacy row and observe the response. **Then red-proof the carve-out itself**: remove
it and prove those four go dark. A carve-out nobody has seen fail is a carve-out nobody has tested.

**3. Is the new test a test?** The builder reports a red proof of **2 failed / 4 passed / 6 total,
exit 1**, with the two being the defect cells and four controls green, restored byte-identical by
sha256. **Re-run it and check the red is BEHAVIOURAL — six tests RAN, not a compile break** — and
check the assertion reads the value the product WRITES, not one the harness supplies.

**4. What does the KS-1067 merge bring in, and is it separable?** The head is a merge. Confirm the
lockfile change and the fix change are distinguishable in the diff, and that the fix's own commit
touches only the two files claimed.

## WHAT IS NOT A REQUIRED LEG, AND WHY IT IS SAID OUT LOUD

**Schemathesis is NOT a required leg on this PR and must not be run as one.** On 2026-09-09
Wednesday made it a required leg on #930, it executed cleanly, and across 100 generated cases it
never reached the changed code — a green that measured nothing. **This change alters the VALUE of a
response field, not its schema, and a schema sweep is structurally blind to that.** If you believe
a contract leg can say something here, say what it would measure before running it.

**This instruction exists because Wednesday got it wrong nine hours ago and the retraction is
carried by name rather than left in a report.**

## HOW TO REPORT

- **Findings only. You never fix.** Severity per the charter.
- **State what you did NOT test**, in the same breath as what you did.
- **Every zero, empty or no-match gets a control that would have produced a non-zero, run in the
  same action** — and the control must be able to fail independently of the failure it tests for.
- **A green from a check aimed at the wrong property is worse than no check.** Say which property
  each green establishes.
- If a claim above is false, **that is a finding about Wednesday's brief and it is Wednesday's
  error, not the builder's.** Report it as such.

## BOUNDS

- **Demo and UAT are HELD.** Do not probe either; Kam has not picked an instrument. Local only,
  disposable containers, and say so.
- **Nothing merges.** `develop` is merge-frozen repo-wide (55 of 56 PRs read `blocked`) — a
  `blocked` state on #935 tells you nothing about #935.
- **No contact with Peter or Stuart. No `--no-verify`. Never delete — quarantine.**
- Do not touch the advisory baseline or branch protection.

## VERDICT DESTINATION

**Mail your verdict to `wednesday-agent@agentmail.to` when the pass is complete**, subject
`[QA -> Wednesday] TIER 1 GATE #935 (KS-1057) <head> — GO / GO WITH FINDINGS / NO GO`.
A gate that cannot report is decoration: on 2026-09-09 a 16-minute tier-1 verdict with a Blocker in
it sat unread in a folder because nobody told the gate where to send it.
