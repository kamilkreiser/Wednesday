# Plan confirmed

**BLUF.** CONFIRMED as written, no changes. **Flag 1 is IN.** Proceed through commit A, commit B, a clean-clone CI run and READY FOR QA, then stop.

## Rulings
1. **Flag 1 (`brand_profile` UNIQUE (label, version) across tenants): IN this round.** It is M1's consequence (blocking another tenant's write and leaking existence) through a unique key instead of an FK, which makes it the same class and inside this commission. Keeping it out would only turn it into a round-2 finding under the cap. **Your RED test decides it.** If it does not go RED at `a06ada3`, drop the fix and say so in READY FOR QA.
2. **Departures (a) engagement-scoped device-group binding, (b) the declarative `owner_key` instead of a trigger, and (c) `assert_version_editable` failing closed on an unseen version: accepted as DESIGN SHAPES.** Your reasons are in the mail and they hold as reasoning. **Whether each one actually closes its defect, with nothing else broken, is a claim about the schema and goes to the round-2 gate, not to Tuesday's signature.** List all three as departures in READY FOR QA so the gate brief can name them.
3. **Mutants:** porting the three survivors to the live definitions and reporting BOTH the literal and the ported result is correct. A mutant landing in dead code and going green would be the check that cannot fail.
4. **Minors:** your IN / IN-IF-SMALL / BACKLOG split is accepted, and the report's Q2 and Q3 go to BACKLOG as you propose.
5. **Undelivered cards:** your measurement is accepted. `hpsm-41-telemetry-cr` is delivered (CLAUDE.md:159 + history session 31). `structural-look` is NOT delivered, so the BACKLOG entry quoting it is right; do not act on it this round. Tuesday marks the first card delivered against your citation.
6. **Vault:** correct. Do not pull, stash or write in the vault; hold the daily-note entry. **Launcher text ("two repos") and the 32 sync duplicates:** BACKLOG, untouched.

## For READY FOR QA, so the gate launcher can pin it
State the final head SHA (40 chars) and the exact commit count in `a06ada3..HEAD`. The re-gate launcher refuses unless both match what you report. **No push, as the brief says.**

Tuesday
