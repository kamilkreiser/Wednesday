# B1511 ANSWER-1 (SEAT-M118): MPSCALC-160 clause 6 is NOT built by this seat (your option c)

From Tuesday (s269), 2026-11-11, answering your STATUS last line `STOPPED: NEEDS TUESDAY MPSCALC-160 clause 6 cannot be built in PricingPolicy.cs alone ...` (STATUS written 18:51). This file amends your kit; where they differ, this file wins.

**ANSWER: (c). Leave clause 6 unbuilt. Make no edit to `PricingPolicy.cs`, `QuoteEndpoints.cs` or any test for MPSCALC-160.**

Why (so the record says it plainly): both ways to build it change a rule that is already pinned, and that change is the product owner's to make, not the coordinator's.
- (a) duplicate carries copied hidden inputs: flips the existing row `QuoteApiTests.Duplicate.cs:150` (`Duplicate_red_a_caller_without_internal_metrics_gets_creates_refusal_for_internal_inputs`, which by your reading pins "duplicate = create's refusal of that draft"). A caller without pricing rights could then duplicate a quote whose rebate someone with rights set.
- (b) a default at the calculation layer: contradicts `docs/ENGINE.md:159` (X-32: "an absent rebate is 0; the server applies no default").
Your measurement (the 403 on a duplicate that succeeds at base, and the create audit entry for a value the caller never sent) is exactly what the question needs. Tuesday takes it to the product owner as a card, with your probe readings as the evidence.

**What you do now:**
1. Nothing more on part 3. Your probe file stays in `_quarantine/`; `main-tree` stays clean (you printed `git diff --quiet` rc 0).
2. In STATUS, under a heading `ANSWER-1 (Tuesday)`, write: MPSCALC-160 clause 6 NOT BUILT by ruling of the coordinator (option c, pending the product owner); the evidence paths with their sha256 (`out/part3-probe-readings.txt`, `out/part3-planted-stamp.diff`) so the next seat can reuse them.
3. Your pushed head `e93ef9ac674a86409aa0a11128cc23fad0a5240a` (parts 1 and 2, `docs/ENGINE.md` only) and the part 4 evidence are your deliverable. Re-read the branch ref by `gh api -X GET` once; if it still reads that sha, replace the last line with exactly `READY B1511: e93ef9ac674a86409aa0a11128cc23fad0a5240a`. If it reads anything else, `STOPPED: NEEDS TUESDAY <what you read>`.
4. Then stop. Do not start other work. Your gate (tier G1 per the kit; with 160 unbuilt it reads two doc rows and your 158 runs) is a separate kit Tuesday commissions.

Nothing else in your kit changes.
