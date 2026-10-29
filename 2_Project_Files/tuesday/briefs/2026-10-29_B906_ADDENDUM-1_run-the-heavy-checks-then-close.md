From Tuesday (the Datasec coordinator seat), to SEAT-G205 (B906, NexusAI PR #143 gate), 2026-10-29. This answers your STOP of 20:44 and is part of your commission.

# ADDENDUM-1 to B906: run the remaining heavy checks in THIS seat, then close the gate

**Answer: run the remaining heavy checks first, then write the verdict.** B906-1 (Blocker) and B906-2 / B906-4 (Majors) stand as reproduced; the verdict will be NO GO round 1 of 2. Round 2 of 2 is the cap on this class (`model-routing.md:111`), so the ONE fix round that follows must see the COMPLETE residue: a finding first discovered at round 2 would cost the product owner a third round. A verdict with C5/C8/C9/C10 unrun would leave exactly that gap.

Do, in your kit's priority order and under its LOAD and lock rules (nothing else changes):
1. **C5** the nine mutants (ML, MO, MN, MC, MS, MP, MK, MW, MR) against the new test file (+ rd856/857/863 where named). Report in particular whether ANY of the 26 new cells turns red for the shapes of B906-1 (two rostered users, earlier one preempts), B906-2 (strict hit unfindable, collateral found) and B906-4 (one-word possessive after "show me"). A finding that NO cell can see is itself a G-3 Major ("the pinning row cannot fail"): name it per finding, so the fix lane knows which cells to add.
2. **C9** the new file at base (red/green by name) and at the gate tree x3; the answer differential on your corpus.
3. **C8** the 15 neighbour suites at base and gate.
4. **C10** the plain verify on your merge tree (5250/311), M4-only red = Note.
5. **C3** the hosted `build` job log of #143 once complete (the rd869 PASS/FAIL line, Tests, VERDICT), and say which merge ref it judged (main moved to `4f662c49` by #139 at about 19:55; the hosted merge ref was still `7620ebac` over `be13993a` at the stamp).
6. Then C11-C14 as written, and the verdict line.

**FOR TUESDAY must carry, for the fix lane (one forward commit or a few on the same branch, no rebase):** every Blocker and Major with its fix shape in prose (you have written B906-1/-2/-4 well already), the exact regression cells to add (question, roster, expected user), the CLOSED list (every shape you proved safe), and which Notes (B906-3, B906-5, others) you recommend folding into the same fix versus ticketing. If a heavy check would push you past your HARD STOP or ~80% context, stop it, write PROGRESS/RESUME, and close the verdict as NO GO round 1 of 2 with the unrun checks named as NOT TESTED; never stretch past the hard stop.

You may write `VERDICT:` as your last line only when the above is done (or cut off by the hard-stop rule).

READ-BY-TUESDAY: written by Tuesday s204 after reading B906_STATUS lines 53-55, 84-85, 105, 135-139.
