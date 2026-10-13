From Friday (laptop seat), Datasec / MPS Commercial Calculator. B85 ADDENDUM-1: Friday's answer to your STOPPED: NEEDS FRIDAY ([B85-1], the importer parity proof).

## News first
**Kam ruled card `mpscalc-rental-parts-cents-rounding-1013` = a** (live board 2026-10-13 15:35:32, verbatim: "Decision mpscalc-rental-parts-cents-rounding-1013: a — Round the parts so they always add up (like purchase)"). Your branch is no longer HELD by the card. Your instructions do not change: push, stop at READY FOR GATE; Friday commissions the gate, then opens the PR and merges.

## Ruling on [B85-1]: YES, the STRICTER variant
Your partition is widened by exactly two files: `src/MpsCalc.Import/Parity/ParityProof.cs` and `tests/**/ParityTests.cs`.
1. In `CompareObjects`, a property whose name ends in `InCents` is compared equal-or-within **0.01 absolute** and counted **"within tolerance"** (so the report still shows it). Every other value stays exactly as today (1e-12 relative). No field is excluded and no property is moved out of the comparator's reach.
2. **And** for every object that carries the four parts in cents (line and portfolio), Σ of the four `…InCents` values must be **exactly equal** on both sides (decimal ==). A difference there is a DIFFER, never "within tolerance". This keeps the guard able to catch a wrong shown total.
3. One assertion in `ParityTests.cs` that the report shows the InCents rows as within-tolerance (not hidden) and that Σ-equality is checked.
4. Red-proofs: (a) a mutant that moves 2 cents between two parts → still within tolerance (expected; say so); (b) a mutant that changes ONE part by a cent without its pair (Σ broken) → DIFFER → RED; (c) a mutant that perturbs a non-InCents decimal by 1e-9 relative → RED (tolerance unchanged elsewhere).

## Why (quote it in STATUS)
The two reference sets differ by ~1e-16 in float-stored CPPs; rounding to cents is a step function, so a cent can legitimately move between base and mono while the shown charge is identical. A parity proof must not demand equality that the inputs cannot give, but it must still catch a wrong shown total: hence ±0.01 per part AND exact Σ. The change is to the GUARD's comparison rule for a new kind of value, not to any expected value; Friday authorises it, and the gate checks it.

Then finish your brief: suites, push (fast-forward), STATUS (record this ruling and the two-file partition widening), last line `READY FOR GATE: b85/rental-parts-cents <sha>`.
