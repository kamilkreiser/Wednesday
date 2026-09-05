---
date: 2026-08-13
type: principle
source: "Two independent instances the same night, from two different clients. Secuura/Blockchain s28: 'aligning a spec to a stub hardens the documentation around the stub' — KS-475 removed an unread optional `key` field to fix a spec/runtime mismatch, deleting the one field a correct implementation requires. Datasec/HPSM s17: SOW-01 §14's payment table was aligned to Delivery & Investment Plan v3 while §3 binds v2 — A$187,500 on signature against a bound plan that pays 10% on a deliverable."
status: live
supersedes: ""
tier: M
---

# When two artefacts disagree, establish which one is RIGHT before making them agree

**The failure shape.** Two things that should match do not. Someone notices, and
fixes the *mismatch* — which is a different job from fixing the *defect*. The
disagreement disappears, and with it the only signal that something was wrong.
Reconciliation is not neutral: **it destroys evidence.** Whichever side you edit
becomes retrospectively correct, and the next reader cannot tell that a question
was ever open.

**Two instances the same night, in domains with nothing in common:**

1. **A spec aligned to a stub (Secuura, KS-475).** The `wallet-connector` verify
   endpoint's schema carried an optional `key` field the runtime never read. The
   mismatch was real and the fix — remove the unread field — was reasonable. But
   the runtime ignored `key` *because the runtime verified nothing*; it was a
   stub. CIP-30 `signData` returns `{signature, key}`, and a Cardano public key
   cannot be derived from its blake2b address. So deleting that field made a
   correct implementation **contractually impossible as published**, and hardened
   the documentation around a stub that now looked like a specification. The
   agent's formulation: *aligning a spec to a stub hardens the documentation
   around the stub.*

2. **A contract aligned to a superseded plan (Datasec, SOW-01).** §3 ranks the
   *Delivery & Investment Plan v2* as binding. §14's payment table is **v3's**,
   verbatim, down to v3's own "reserves and mobilises" phrasing — 25% /
   A$187,500 on signature, where the bound plan pays 10% against a deliverable.
   Someone brought the money into line with the newer thinking and left the
   precedence clause pointing at the older document. **All six SOWs inherited
   it.** I re-derived every leg from the source files before believing it.

**Why these are one lesson.** In both, the two artefacts were *evidence of a
disagreement about what is true*. In both, the edit picked a winner implicitly —
by convenience, by recency, by whichever file was open — rather than by
establishing which one was authoritative. Neither editor was careless. The move
felt like tidying.

**How to apply:**
1. **Before reconciling, ask which side is authoritative and why.** Recency is
   not authority. Being the artefact you happen to be editing is not authority.
   In a contract, the precedence clause says. In code, the *intended behaviour*
   says — not the current behaviour.
2. **Aligning documentation to an implementation is safe only when the
   implementation is known correct.** Against a stub, an unfinished path or a
   mock, it converts "not built yet" into "not in the contract" — invisibly, and
   permanently, because the next reader sees agreement.
3. **When you cannot establish authority, record the disagreement instead of
   removing it.** A documented conflict is a finding. A silently resolved one is
   a deletion.
4. **Suspect any field, clause or check that exists but is unused.** That is the
   fingerprint of an intention that was never implemented — and the thing most
   likely to be tidied away by someone fixing a mismatch.
5. **Look for the class, not the instance.** Both cases above were found by
   reading two documents *against each other* rather than reading either one
   carefully. Where a system has a model and a contract, a spec and a runtime, a
   plan and an invoice — nobody is assigned to read the pair, so nobody does.

**Related:** [[2026-08-03_mental-model-not-source-of-truth]] (same discipline:
establish the source of truth before acting on the model),
[[2026-08-06_local-proof-is-not-target-evidence]],
[[2026-08-07_a-check-that-cannot-fail]] (a reconciled pair can no longer fail the
comparison), [[2026-08-13_headline-must-match-the-operative-case]] (tonight's
other structural-defect lesson), [[_ledger]]
