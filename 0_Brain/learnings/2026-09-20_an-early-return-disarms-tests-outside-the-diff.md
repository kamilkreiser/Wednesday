---
date: 2026-09-20
type: principle
source: Datasec/NexusAI S71's RD-549 gate finding (2026-09-20 05:41Z), adopted by Tuesday
status: live
tier: M
---

# An EARLY RETURN added to a shared function silently disarms existing tests — and by definition they are NOT in the diff

**The operative case, so the headline matches it:** a change adds a guard, a mode check or any other **early return** near the top of a function that other code already calls. **Before accepting it, enumerate the function's CALLERS and the existing cells that exercise them, and ask of each: does this cell still reach the check it is NAMED for?** A review scoped to the changed set cannot see this by construction — the weakened tests are in files the commit never touched, they still pass, and they keep their names.

**The case.** RD-549 added `if (o.mode !== 'admin' && o.mode !== 'open') return null;` at `backend/llm/index.js:43`, above the pre-existing `if (!o.endpoint || !o.apiKey) return null; // incomplete; ignore` at line 45. An untouched cell in `__tests__/security-fixes.test.js` — *"incomplete override (missing apiKey) is ignored"* — passes an override with **no apiKey and no mode**. It now returns at 43 for the missing MODE and never reaches 45. **The cell is green, its name is unchanged, and its own comment explaining why it passes is now false.** Line 45 could be deleted and the suite would stay green.

**The tell that it is systemic, not a slip:** the same author fixed the identical shape in `rd503-r2` **in the same commit** (adding `mode: 'admin'` with a comment saying why), because that file WAS in the changed set. One file got it, one did not. **Scope, not care, decided which.**

**How to apply:**
1. **The population to check is "callers of the mutated function", not "files the commit touched".** Enumerate them; do not sample.
2. **For each existing cell on that path, ask whether it still reaches the check it is named for** — and where it does not, the fix is usually one line in the FIXTURE (give it what the new guard demands), never a change to the policy ([[2026-09-20_a-closure-inherits-the-scope-of-its-measurement]]'s sibling rule: repair the fixture, not the guard).
3. **Prove the disarmament with a paired mutation:** delete the LATER check and expect the suspect cell GREEN plus a known-good cell RED. Both red means the diagnosis is wrong; both green means the instrument is dead and the run proved nothing.
4. **Severity: the product may be perfectly correct** — this is a COVERAGE defect, and saying both halves ("the product is right" and "the guard is now unexercised") stops the next reader over- or under-reading it.
5. **It generalises past early returns:** anything that short-circuits a shared path — a new cache, a feature flag checked first, a fail-fast validation, a middleware mounted earlier — can leave downstream assertions unreached while green.

**Family:** [[2026-08-07_a-check-that-cannot-fail]] (the parent: here the check exists, runs, passes, and no longer tests its subject) · [[2026-09-08_the-check-ran-and-was-not-checking-the-thing]] · [[2026-09-07_a-census-complete-over-a-frame-that-is-not]] (the diff is the frame) · [[2026-09-20_a-closure-inherits-the-scope-of-its-measurement]].
