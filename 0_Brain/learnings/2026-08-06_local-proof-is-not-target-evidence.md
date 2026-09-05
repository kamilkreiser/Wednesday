---
date: 2026-08-06
type: principle
source: "Secuura/Blockchain agent, KS-563 ship 2026-08-06 — their finding, propagated fleet-wide by me. Their words: 'Local could not have found this… a green local proof is not evidence about an env whose mode differs by design.'"
status: live
supersedes: ""
tier: M
---

# A green local proof is not evidence about an environment that differs by design

**The lesson:** when a target environment differs from local *deliberately* —
mocked externals, seeded data, disabled integrations, stub credentials, a
different provider mode — a passing local run is blind in exactly those places.
It is a necessary step, never a sufficient one, and the blind spots are usually
documented in the repo as intentional choices, which makes them findable in
advance.

**The case that taught it (not mine — worth remembering that):** KS-563 shipped
with a complete local receipt: unit tests green, full local matrix verified,
both pre-merge tiers passed. On demo, a genuinely confirmed on-chain anchor
reported `isAnchored: false` — a **false negative, the exact inverse of the
defect the ticket existed to fix.**

The root cause is the part that generalises. The fix required
`blockchain.anchored === true`. Real anchoring never writes that key; it writes
`{status, txHash, network, anchorId, anchoredAt, blockHeight}`. Only the
chain-first code paths build an `anchored:true` shape — and that was the shape
the unit tests used. **The tests were internally consistent, passed honestly,
and were tautological**: they asserted against a shape the author had invented
rather than one captured from the real system. Local runs mock anchoring by
design, so no local document could ever reach a confirmed real anchor.

**How to apply — mine, and in every brief:**
1. Before accepting a local receipt, ask what this environment fakes *on
   purpose*, and whether the change depends on data only the real one produces.
2. Prefer fixtures captured from the real system over hand-built ones. A
   hand-built fixture tests the design, not the data.
3. Require the verify matrix to run against the target **after** deploying, not
   only before — that is how this was caught.
4. Reward the honest form of the receipt: "unit-proven; the confirmed-anchor
   path cannot be exercised locally" beats a green tick that implies coverage
   it doesn't have.

**Meta-note worth keeping:** the agent found this, fixed it the same session,
and reported it unprompted with the methodological argument attached. Good
agents generate lessons for the fleet, not just completed tickets — my job is to
notice and propagate them rather than let them sit in one mailbox.

**Related:** [[2026-08-06_artifact-presence-is-not-execution]] (same family:
evidence that looks like proof and isn't), [[2026-08-06_exercise-mechanisms-before-arming]],
[[../skills/delegation-protocol]]
