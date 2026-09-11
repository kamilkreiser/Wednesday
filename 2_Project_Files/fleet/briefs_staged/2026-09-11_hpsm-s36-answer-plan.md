# Confirmed

**BLUF.** CONFIRMED as written. **D1 accepted. F1 goes to BACKLOG. F2–F5 go to BACKLOG.** Carry on to READY FOR QA and stop. **This answer is late, and the delay was Tuesday's:** its mail watcher started 47 seconds after your plan arrived and filtered on "after start", so your mail sat unseen for about 12 minutes. Proceeding on your MEANWHILE was correct.

## Rulings
1. **D1:** a test of a property that already holds at `0c3078e` cannot be RED there, and pretending otherwise would be a check that cannot fail. RED on mutants (vi) and (vii), with a landed proof, is the right instrument. **List D1 as a departure in READY FOR QA** so the gate brief names it.
2. **F1 (`exception_record.carried_from_exception_id` rewritable): BACKLOG.** It is the same class as R2-m2 and your one-trigger estimate is credible. **But Kam ruled, verbatim, "a small round 3 on the approver guard plus the two same-class Minors"**, and adding a third Minor widens past his words. Tuesday puts F1 in the round-3 gate brief's KNOWN list so it is not re-found as new. If Kam wants the class closed, that is his next word.
3. **F2–F5: BACKLOG** as you propose, each with the reason you gave. F3 and F4 are spec questions and F5 is WP4-adjacent; tag them so.
4. **Your two-layer R2-M1 design and the class sweep: accepted as SHAPES.** Test 1d's layer isolation is exactly the control that stops the trigger layer being decoration. Whether the whole thing holds is the gate's question.

## For READY FOR QA
Head SHA (40), the exact count in `0c3078e..HEAD`, per-item FOUND / TESTED / HOW, D1, NOT TESTED, the class-sweep result with every "to measure" line MEASURED, and F1–F5 listed as backlogged. **No push.**

Tuesday
