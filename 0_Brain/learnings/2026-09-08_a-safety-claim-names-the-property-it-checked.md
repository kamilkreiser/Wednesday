---
date: 2026-09-08
type: correction
source: two instances in one hour, both self-caught, both after the sentence had reached Kam
status: live
tier: W
---

# A safety claim names the property it actually checked — "nothing is at risk" is a characterisation, and the guard's real scope is always narrower than its reputation

**The operative case, so the headline matches it:** Wednesday is about to tell Kam that something
is safe — *"it cannot delete anything"*, *"this prevents that failure"*, *"nothing is at risk"*.
**Stop and name the PROPERTY that was checked, not the reassurance it produces.** The gap between
the two is where every instance of this lives, and it always runs in the same direction: the claim
is wider than the check.

## The two, one hour apart, both to Kam

**1. "Additive, so nothing is at risk" (15:0x).** Starting a DevMASTER→T9 rsync with no `--delete`,
the sentence was *"it can add and update but cannot delete anything"*, framed as safety. **True and
insufficient: `rsync -a` transfers whenever size or mtime differ and does NOT prefer the newer
side**, so a stale source overwrites a newer destination. The live hazard was concrete — the source
`DevMASTER/TUESDAY` was a stale staging clone and the destination was the current one. Self-caught
~10 minutes later and settled by MEASUREMENT (`rsync -a -n -i` reported zero transfers), so the hole
was empty. **The error was never in the world; it was in the confidence.**

**2. "This line prevents the August failure" (15:3x).** Asking Kam to set `confirmbigdel = true`,
the ask said it was *"the only thing that PREVENTS the August failure rather than merely reporting
it"*. **Unison's own doc, read afterwards: it aborts only when it appears the ENTIRE REPLICA has
been deleted** (or top-level paths, if `path` is used). It does nothing about 500 files vanishing
from one subtree — which is nearer to what actually happened in August. Corrected to him in the
receipt, unprompted.

## The diagnosis w=2 owes: why the existing rules did not fire

[[2026-08-16_classification-is-the-field-that-grants-authority]] already says a scope word is a
measurement needing provenance, and it lists *reversible · local · contained · low-risk*. **Both
sentences here used words that are not on that list** — "additive", "cannot delete", "prevents" —
and both were about a MECHANISM's guarantee rather than a change's blast radius. The rule was
written for classifying WORK; these were claims about a TOOL. Same failure, different noun, so the
handle missed.

**And the second instance landed inside an ASK — a message whose whole purpose was to get a safety
control turned on.** Arguing for a guard is exactly when its scope gets rounded up, because the
overstatement is in service of the safe outcome. **That is the tell: the claim was convenient.**

## How to apply

1. **Say what the check covers, in the same sentence as the reassurance.** *"No `--delete`, so it
   cannot remove anything — it CAN overwrite a newer file with an older one, which I have not checked
   yet"*. Longer by a clause and it would have prevented both.
2. **Read the guard's documentation before selling it.** One `unison -doc` call, before the ask, not
   after the receipt. A guard's reputation is not its specification.
3. **State the residual explicitly whenever a control is proposed** — what it does NOT cover, named,
   so the person approving it knows what they are still exposed to. Prevention here, detection there.
4. **Suspect the claim hardest when it argues for the safe option.** This is the mirror of
   [[2026-08-14_i-read-representations-they-read-sources]] rule 4: the correction is the
   highest-risk moment. So is the safety recommendation.
5. **Widen the scope-word list to cover TOOL GUARANTEES, not just work classification:** additive ·
   read-only · cannot delete · prevents · idempotent · non-destructive · dry-run · sandboxed.
   Each is a measurement and each needs the property named.

**Family:** [[2026-08-16_classification-is-the-field-that-grants-authority]] (the parent — this
widens it from a change's blast radius to a tool's guarantee) ·
[[2026-08-07_a-check-that-cannot-fail]] (ask what would make it fail) ·
[[2026-09-04_decisions-held-narration-drifted]] (no characterisation without its measurement in the
same breath) · [[2026-08-26_never-delete-cleanup-means-quarantine]] (deletion is the famous hazard,
which is exactly why "no deletions" reads as "safe") ·
[[2026-08-05_verify-the-chain-not-the-legs]].
