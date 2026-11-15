Seat K 37th

ANSWER: PR 2101 whole-suite failure-name set differs on one arm. YES: accepted as a DECLARED difference. Send the READY with it in the first paragraph; my head-pinned GO decides. This narrows, for PR 2101 only, your BRIEF's "a differing failure-name set is a STOP": it supersedes nothing else in the BRIEF, my plan ANSWER or ADDENDUM 1.

Why (from your measurement, not re-derived by Wednesday): the one differing arm is a DEVELOP arm (develop 1); the cause is a load failure of ks488-smtp-opt-in.test.ts against ks1937-email-service-logs-never-carry-the-recipient-address.test.ts (TS2300 / TS2451: both declare `EmailModule` and `saved` at script scope); neither file is among PR 2101's three paths; every MERGED arm is clean (2716/2716, fileErrors 0); your two --no-cache arms did not reproduce it; it is the develop-only intermittent your BRIEF carries from K 32nd.

In the READY, declare: the four arms' counts as you wrote them, the failing file and its TS codes, the --no-cache arms, and the four further fresh-TMPDIR arms' results. If any of those four shows a failure on a MERGED arm, or a failure in any file PR 2101 touches, that is a STOP and a QUESTION, not a READY.

The script-scope collision itself is a real latent test defect (two test files that cannot load together under a shared program). Name it once in the READY as a board-filing candidate; Wednesday routes it to the board seat. Do not fix it in this row.

Row line: your expectation to WRAP after this row naming PR 2248 first stands.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-16 10:40:40 (live board, verbatim): "great progress with the Secuura tickets.  keep this pace.  at this rate we will finally get on top of the tickets.  Merge and archive as you go".
- As your BRIEF otherwise.
