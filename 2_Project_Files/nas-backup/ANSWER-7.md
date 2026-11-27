# ANSWER-7 to the nas-backup round 4 seat (from Wednesday, 2026-11-28, just after midnight)

Your ROUND 4 section (STATUS.md lines 1 to 190) was read WHOLE by Wednesday. TASK 1 is recorded as done and Kam has been told, with the limits you named. Thank you for the stop-and-list and for slip 1: both change what Wednesday does.

RULING, Wednesday's own, inside Kam's ruling for this round: **fix sibling 1 (the link at `README.txt`) now, before the re-check.** It is the SAME fault as item 2 (a link in the destination makes the tool write outside the seat's folder and say GOOD), on the one write the brief's wording left out, so it is inside "the four points", not a new item. A re-check that fails ends this lane with no further card, and you say yourself that a checker who tries file-level links will find it. Your five departures from the brief's letter ("differ" 1 to 5) are ACCEPTED as you argued them, each with its cell and mutant.

DO, and nothing else:
1. `README.txt`: `os.path.lexists`, as you say; and refuse (exit 2, nothing written, named) when a link is found at that name, in the same way a linked level is refused. Then look ONCE at every other place where the tool creates or opens a file BY A FIXED OR PREDICTABLE NAME at the destination (the COMPLETE marker, the manifest, the run file, anything else `open(..., 'w')` or `os.replace` writes there) and say for each, from the code, whether a link planted at that name could carry a write outside: fix those that can in the same way, list those that cannot with the reason. That is the whole class of this sibling; siblings 2, 3 and 4 stay listed and NOT edited.
2. Red-first on your round 4 code as it stands (name the red cells), green after; one mutant per new guard, each killed by its named cell. Your probe `probe_sibling_readme_file_symlink_NOT_FIXED` becomes a cell.
3. Run, from a snapshot outside the repo as you now do: the suite WHOLE; the F mutants, the new mutants and a control (NOT the whole 143: the checker runs it whole; say in STATUS that you ran this subset and why); `tests/claims_check.py`. No second real dry run.
4. STATUS.md: a short ROUND 4b section on top (round 4 kept below), first line READY FOR QA. Then end your turn.

ON YOUR SLIP 1 (a commit by Wednesday's session swapped your uncommitted files under a running suite): your reading is right. Wednesday's push tool pulls with an autostash, which sets uncommitted tracked changes aside and puts them back. From this answer on Wednesday commits both live lanes' files as they stand in the same push, so there is nothing of yours to set aside; keep running from a snapshot all the same. Your point 1 "commit this lane before any real run" is taken.

All HOLDS and the disk guard unchanged. If the fix cannot be made sound, say so plainly instead of patching.
