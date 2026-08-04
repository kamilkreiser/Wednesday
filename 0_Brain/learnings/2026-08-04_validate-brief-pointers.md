---
date: 2026-08-04
type: correction
source: "w=2 ledger promotion: (1) Peter to-do type mis-asserted in the consent micro-brief; (2) Tokenomics brief pointed tenant verification at the stale client CLAUDE.md — a file that was itself under repair"
status: live
---

# Validate what a brief points AT, not just what it asserts

**The failure class (two occurrences, same day):** the delegation-protocol
rule "validate every fact in a brief against the live source" fired for facts
I *asserted* — but not for **pointers**: places I sent the agent to verify
things for themselves. Occurrence 2 was the sharp one: the Tokenomics
stale-tenant brief said "verify the current tenant from the client
CLAUDE.md's tenant section" — but that file was one of the two artifacts
being repaired *because its tenant section is stale*. Circular ground truth;
the agent had nowhere authoritative to stand.

**Why the existing rule didn't fire (w=2 diagnosis):** paths-over-content
(a good rule — paths stay fresh) made pointing feel inherently safe. It
isn't: a pointer is an implicit assertion that *the target is fit to answer
the question*.

**How to apply:**
1. For every "verify X from Y" in a brief: open Y first (read-only) and
   confirm Y actually answers X correctly TODAY. If I can't check Y, say so
   in the brief honestly ("Y may itself be stale — cross-check against Z").
2. **Repair-object rule:** if Y is part of what the brief asks the agent to
   fix, Y is disqualified as ground truth for that fix. Name an independent
   source (a sibling project's fixed artifact, live `az account show`,
   4_Credentials state).
3. Withholding facts from a brief (as I did with tenant IDs, rightly wary of
   asserting unverified ones) obliges me to ensure the verification path I
   name instead is sound — otherwise I've swapped a checkable wrong fact for
   an unfalsifiable dead end, which is worse.

**Related:** [[_ledger]], [[../skills/delegation-protocol]],
[[2026-08-03_mental-model-not-source-of-truth]]
