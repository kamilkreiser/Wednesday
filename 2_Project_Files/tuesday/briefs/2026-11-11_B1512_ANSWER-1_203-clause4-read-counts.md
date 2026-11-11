# B1512 ANSWER-1 (SEAT-M119): MPSCALC-203 clause 4 may change exactly the two read-count expectations

From Tuesday (s268), 2026-11-11, answering your QUESTION mail of 07:26Z ("B1512 203 clause 4 changes two existing read-count assertions"). This file amends your kit; where they differ, this file wins.

**ANSWER: YES, build clause 4, under these limits.**

1. You may change exactly two existing expectations in `scripts/tests/test_deploy_pre1.py`, and nothing else in any existing test:
   - `:206` in `test_an_absent_overlay_is_0_entries_and_deploys`: `1` -> `2`
   - `:341` in `test_203_vi_two_runs_in_one_second_...`: `2` -> `3`
   Each changed line carries a short comment: one PRE-1 read plus one re-read before `az webapp deploy`. Test names are unchanged. Re-print both line numbers at your base before editing: if either moved or reads differently, STOP.
2. **Why this is allowed:** these two lines pin the old behaviour that clause 4 is commissioned to change (S4 Q-L5-5 = build). An exact count raised by design is not a weakened assertion. The kit's "removed test lines 0" still holds: the old lines are modified, not removed. List both in STATUS with before/after, under a heading `CHANGED EXPECTATIONS (ANSWER-1)`.
3. **The new behaviour must be pinned positively, not only through the changed counts:** your clause-4 rows must show (a) an equal second read deploys and leaves no second copy; (b) a changed second read stops with rc 1, deploys nothing, and keeps the second copy at 0600; (c) `probe` and `check` still make 0 overlay reads. The mutant that removes the re-read must turn at least one of those rows red, and must also turn the two changed counts red.
4. Everything else in the kit and its Stamp stands, including the 126 stdout condition, the tier-1 gate for 126 and 203, and HARD STOP 22:30.
5. In FOR TUESDAY, write one line: "ANSWER-1 used: two read-count expectations changed (:206 1->2, :341 2->3)".
