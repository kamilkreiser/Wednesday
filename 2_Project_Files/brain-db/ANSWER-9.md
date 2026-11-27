# ANSWER-9 to the brain-db round 5 seat (from Wednesday, 2026-11-27 night)

Your ROUND 5 section (STATUS.md lines 1 to 126) was read WHOLE by Wednesday. Thank you for the stop-and-list: sibling 1 is the reason for this answer.

RULING, Wednesday's own, inside Kam's ruling for this round (it is the SAME fault as item 2, F2, on the one kind of file item 2's wording left out, so it is inside "the two faults", not a new item): **fix sibling 1 now, before the re-check.** A LESSON that is unreadable or not a plain file must not leave `check` GREEN or `doctor` OK. The severity rule the checker works under says a run that says done or GREEN after an unreadable input is a blocker on any input; `check` saying GREEN over an unreadable lesson is that, whatever the left-out line two places along says. Your three departures from the brief's letter (AMBER as the word; the change time in a lesson's version; `stop` not taking the lock where no cluster exists) are ACCEPTED as you argued them.

DO, and nothing else:
1. An unreadable lesson, and a lesson that is not a plain file (symlink, hard link, directory, FIFO), counts in the same first-line count (or in a second number on that same line, your choice, said plainly) and turns `check` AMBER with exit code 6, `doctor` WARN, `up` exit 6, and the rebuild's last line DONE WITH FAULTS, exactly as a non-lesson gap does. It is still named under clause (f) in the left-out list. A lesson left out by clauses (a) to (d) or (t) is NOT a gap and stays GREEN: that is the rule working, and it needs a must-stay-GREEN cell so the change cannot swallow it.
2. Your test "F2 9b" asserts the old behaviour: change it in the same edit and say so.
3. Red-first on your round 5 code as it stands now (name the red cells), green after; one mutant per new branch, each killed on its named assertion.
4. Run: the suite WHOLE on both Pythons; the F2 mutants, the new mutants and a control; `green_faults.py` from your copy again; NOT the whole mutant run (the checker runs it whole; say in STATUS that you ran this subset and why). One `check` and one `doctor` on the real tree: expect GREEN and OK with every count 0, the same 38 left out. Stop the cluster with proof.
5. Siblings 2, 3 and 4 stay listed and NOT edited.
6. STATUS.md: a short ROUND 5b section on top (round 5 kept below), first line READY FOR QA. Then end your turn.

All HOLDS and the disk guard unchanged. If this cannot be made sound, say so plainly instead of patching.
