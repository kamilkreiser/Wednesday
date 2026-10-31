From Tuesday (the Datasec coordinator seat) to SEAT-M52, Datasec / MPS Commercial Calculator. ADDENDUM-2 to BRIEF B974. Binding. This is your ONE build round after the round-1 gate.

**The gate's verdict:** B980 = NO GO, round 1 of 2, on class "V4 engine: page basis and rental projection", at your head 1d49328 on main 1a2a029. Read it whole first: `1_Project_Definition/Briefs/2026-10-31_B980_STATUS.md` (FINDINGS B980-1 and B980-3, and FOR TUESDAY). Your context was compacted while idle, so read your own `2026-10-31_B974_STATUS.md` and the brief again before you change anything.

**Ruling: fix B980-1. ADDENDUM-1 point 4 stands as written: the purchase result must not change at all.** An additive key carrying no figure is still a change. Every new purchase snapshot the Api stores would carry it, and the property "new members are omitted from JSON when unset" says no.

What to do (one round, on your existing branch, new commits on top, NO force-push, NO rebase):
1. **B980-1 (Blocker).** `src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs:482` sets `VolumeBasis = l.VolumeBasis` on every purchase line result, and `src/MpsCalc.Engine/Results/PurchaseResult.cs:59` serialises it. Change it so an UNSET purchase quote's result serialises byte-equal to base, under BOTH InputHash's serialiser options and the Api's `ApiJson`. The property: the member is present only when the line was stated as a fleet total, and absent otherwise. One way is to set it only for `FleetTotal` (null at the default) and omit it when null. Pick the smallest change that meets the property, and prove it under both serialisers.
2. **Regression row for B980-1:** serialise an unset purchase result with InputHash's options and require no `VolumeBasis` key, plus a FleetTotal purchase line showing the key present. Show it red at 1d49328 and green at your new head.
3. **B980-3 (Minor):** add a row pinning the X-34 quantity-0 purchase rule that the register states: a quantity-0 fleet-total purchase line counts its pages and adds no shortfall. The gate's mutant N8 (a quantity-0 total line adds a shortfall) must turn your row red. Show that.
4. **Out of scope, do NOT touch:** the rental line result's basis member (the gate's strip list allows it), the B980-2/4/5/6/7/8/9 Notes, the reconciliation module (HOLD), and every word text.
5. **Re-measure with your own instruments:** byte-equal over the 20 suites with the purchase result NOT stripped (the gate's 12 of 13 differing caller files must read 0 differing), InputHash equal on the 20 inputs, MU1-MU6 still red as predicted, and the full local CI line (Release build at 0 warnings, then Engine, Import and Api tests). **Run the tests with TMPDIR outside any git work tree:** `QuotePersistenceTests.A_path_outside_any_git_work_tree_is_refused` goes red under a TMPDIR inside the project (the gate measured this at base and head; see its Check 6).
6. **Push your branch once** and read it back with `ls-remote`. Leave the PR's title and body alone: Tuesday edits them.

Clocks for this round: target READY 16:30 AEDT, hard stop 18:00 AEDT. Your locks, heavy slots and load gate are unchanged.

Append a `## ROUND 2 (ADDENDUM-2)` section to your STATUS. End it with ONE final line in your round-1 shape, `READY FOR QA: B974 <branch> @ <new head sha40> on <base sha40> - gate tier 1, round 2 - ...`, or `STOPPED: NEEDS TUESDAY - <one question>` if the property cannot be met without changing a figure or a word.

Every other line of the brief and of ADDENDUM-1 stands.
