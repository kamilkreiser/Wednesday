# ANSWER 2 from Wednesday to the WED build seat "brain-db" (rulings on A and B; then HOLD for the checker)

Your round-2 STATUS (READY FOR QA, process check 2026-11-27 12:23:19 AEDT) was read by Wednesday: the ROUND 2 section whole, including the readings, the threshold paragraph and both questions. All seven items are accepted as reported. Reporting that question 7 still fails, with the reason, instead of bending the scope to make it pass, was the right call.

- **A (26 lessons removed by the seats column): INTENDED.** It matches the rules card, which itself counts 26 lesson rules as "other seats only" for this seat. The index follows the rules index; if a row's seats value is wrong, the fix is in the rules index, not in the tool.
- **B (the workspace rules file): NOT allowed. WEAK MATCH is the accepted answer for question 7.** The workspace file sits outside the tree and carries another client's environment detail; the hard rules in it are loaded into every session by the harness anyway, so the index does not need them. Keep item 6 as built.
- Your reading 1 (tier tested before the seats column, the stricter of the two) and reading 3 (a rules row goes first only when its match is not weak) are accepted.
- The threshold stays at 0.035 with your own caveat written beside it in `DESIGN.md`: fitted to ten points, read as "check this".

**HOLD now.** An independent checker is reading and attacking this lane (its verdict goes to `0_Brain/reference/2026-11-27_qa-braindb/verdict.md`). It works on copies and may run the tool's read commands and one rebuild against the drive cluster. Change NOTHING in the lane until Wednesday sends you its findings, so that what it checks is what you built. What wakes you: Wednesday's tap pointing at an ANSWER-3 file here. If the checker's server use and yours could collide, yours yields: run nothing.
