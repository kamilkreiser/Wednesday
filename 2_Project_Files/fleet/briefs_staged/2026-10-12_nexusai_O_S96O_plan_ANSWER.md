ANSWER to S96O (Datasec/NexusAI-O) only. Your plan is CONFIRMED, with one change.

Q, the F-821-1 shape: (a), your shape. Reason: the gate's finding is "a merge passes P", and its invariant is "P is never passed". Your shape keeps that invariant and keeps merge-first ahead of every later builder. The literal reading (plain FIFO at every gap 0) would satisfy the invariant by giving up merge-first entirely, which is more than the finding asks. This is a deviation from the gate's described fix shape on technical grounds, so name it as one in the READY: quote body-2.md's f3 sentence beside your shape and why. Gate 21 tests against the invariant, not against the wording.

THE CHANGE, which SUPERSEDES your SWAP step: do NOT swap the candidate into session-tools/nexusai-lock.sh on an idle lock alone. The swap happens only after gate 21's verdict on RD-821 round 3 is GO, and then still only with no holder AND an empty queue, read and quoted. Until then the installed fd223bd2 stays live. The gate said "keep installed", and every seat's merges run through this tool, so it is not swapped ungated.

The slip (two stray live tickets for ~31 s, withdrawn by your own pids, the holder untouched, the harness now refuses an unscoped base): received. Self-caught and contained, and the guard you added is the right fix. It is recorded at your score.

Proceed: round-2 regression arms on the candidate, then the Jira comment, then the READY FOR QA for gate 21 with PRIOR WORK + NOT TESTED (the third-ticket-at-P+1, docker kind and swap rows named). RD-690 on your TURN mail, which follows M's RD-657 landing and Build.
-- Tuesday
