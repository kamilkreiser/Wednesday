# QA GATE BRIEF — Secuura #892 ROUND 5 @ `d2aa11fd1`, TIER 2 (through-code)

## WHAT THIS ROUND IS, AND WHY IT IS THE LAST ONE
**Kam authorised it himself** (panel 2026-09-08 07:08:30, verbatim): *"ONE more narrow round — F-1
and F-2 only, F-2 first."* **F-3 is NOT in this round. THERE IS NO ROUND 6** — a NO GO goes back to
Kam, not into a merge and not into another round. The two-NO-GO cap on this class was already spent
once (round 3 NO GO, round 4 GO-with-findings).

**Round 4 closed the original BLOCKER and introduced the two Majors this round fixes.** The tester's
sentence on F-2 is why round 4 did not merge: *"it REINTRODUCES KS-969's OWN FAILURE CLASS FROM
INSIDE KS-969's OWN TEST SUITE."*

## SUBJECT
`#892`, head **`d2aa11fd1`** (`1e31c80b9..d2aa11fd1`, two commits, F-2 then F-1 in Kam's order).
Base `develop` **`4f337be83`**. **Nothing is merged and nothing is deployed from this branch.**

## F-2 — the manifest quarantine
`pre_suite.test.sh` drove `pre-suite.ts` for real without protecting `generated/`, so it silently
quarantined a developer's live manifest **and still reported a clean pass.** Fixed with the
stash/restore + `trap … EXIT` pattern taken from `quarantine_call_sites.test.sh:40-56`.

**THE BINDING CONDITION FOR F-2 — the builder's own red-proof, and you must reproduce it:**
commenting out **ONLY** `trap restore EXIT` destroys the manifest again **while the suite still
reports a clean pass.** **That is the point: the suite's own report is PROVABLY BLIND to this
defect, which is why it could not have been closed by adding a cell.** A gate that only re-runs the
suite green has verified nothing here.

## F-1 — the no-throw contract, and a real TOCTOU
`quarantineManifest()` sat INSIDE the catch at `pre-suite.ts:157`, so a throw from it had nothing
above to catch it and `runPreSuite` threw — against its own docstring at `:90-91`, *"Never throws:
classifying the failure IS this function's job."* `manifest.ts:107-114` is `existsSync` then
`renameSync`: a genuine TOCTOU, and `run-in-slot.sh` documents that slots run in parallel.

**Builder's measurement to reproduce or refute:** two concurrent runs in one checkout crashed
**9 of 12**; parent-commit control **0 of 12**.
**The fix must REPORT the failure, not swallow it.** Swallowing is the worse outcome here: a
surviving stale manifest outranks the seeded accounts in every consumer, so a swallowed error is
exactly the case where a suite runs on stale actors while believing it is degraded.

## 🔴 THE DISCRIMINATOR RULE FOR THIS SUITE — corrected, and do NOT inherit the old one
Wednesday's round-4 brief said *"a cell that reds by failing to BUILD proves nothing — plant a syntax
error first."* **The builder did exactly that and MEASURED that it does not behave that way here:**

    syntax error appended  ->  all cells STILL RAN, trailer STILL printed a clean pass,
                               only rc=2 and one stderr line differed
    inert comment appended ->  clean pass, rc 0

**bash executes line-by-line, so a trailing syntax error does not prevent execution.** The rule that
transfers is *read the COUNT, not the verdict* — and **for this bash suite the count to read is the
TRAILER'S FAILED NUMBER. `rc` alone tells you nothing.** Any red-proof you run must report the
trailer's failed count, not just an exit code.

## ALSO: A NUMBER IN A BRIEF IS NOT A FIXTURE
Wednesday's brief said the suite has **24** cells. **It has 29.** The builder flagged it rather than
matching the number. **Report the count you measure; do not reconcile to any number written here.**

## WHAT A GO REQUIRES
1. **F-2 closed AND its blindness demonstrated** — the trap removed, manifest destroyed, suite still
   reporting a clean pass. Both tampers restored byte-identical.
2. **F-1 closed with a REAL throw**, not a simulated one — the builder used `chmod 555` on
   `generated/` so `renameSync` throws `EACCES` genuinely. With the fix: rc 0, DEGRADED reported,
   the EACCES named, **0 uncaught exceptions.** Tampered: rc 1.
3. **Your OWN controls, both directions** — a positive control proving your instrument fires and a
   negative control proving a zero is real.
4. **F-3 explicitly OUT of scope.** If you find it, note it; do not gate on it.

## VERDICT FORM
**GO · GO WITH FINDINGS · NO GO**, with the terminating classification. **State what you did NOT
test.** A NO GO returns to Kam — say so plainly rather than proposing round 6.
