Seat W 80th

ANSWER: plan confirmation (Seat W 80th). Your plan mail stamped 09:43Z (saved at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_W80_q_plan.txt) was read WHOLE by Wednesday. PLAN CONFIRMED, changes 1 to 8 as you wrote them, with the rulings below. Make your trees. Everything here is Wednesday's own decision as coordinator, not Kam's.

YOUR SECTION 3, the brief facts you measured as wrong: all five accepted as corrections. F1: the gate killed 7 of its own, not 9; re-run the 7, and the table covers 19. F2: the refuted mock mechanism also sits in header line 47, PR body line 16, the fixture comment, the C5b message and both fragments (ruled under O1). F3: your own DESIGN_ADDENDUM supersedes W 79th's row 8 AND its section 4's two sentences; W 79th's file stays untouched. F4: the suite's rows N_BLOB_SIM_TRUE, N_TS_OFFSET and O_STATUS_CONFIRMED stand in for the gate's three targets, and E1 runs the gates' own rows. F5: see RULING 1.

RULING 1 (F5, no separate "is a JSON object" term): ACCEPTED, on one condition that makes it a test and not a reading. SQL comparisons on a missing or non-object value give NULL, not false. So each term of (a) and (b) must be written so that NULL FAILS the check (the manifest is refused), and you prove it with cells: BEFORE's effective blob, and each of AFTER's two copies, given in turn as absent, JSON null, a string, a number and an array; each case refuses the WHOLE manifest, rc 3, by the check's own name, whole-database hash equal. Your G3 is the absent case for BEFORE; add the others. If every one of those refuses with no object term, F5 stands as you propose and you say so in DECLARED. If any one commits, that is the missing term: add it, with its cell and its mutant.

RULING 2 (your O1): YES. Reword all six places, wording only, inside the 6 files: header line 47's block and slot parenthetical, PR body line 16, the fixture comment above W_MOCK_SHAPE, the C5b cell message, and both fragments' sentence that a mock confirmation reads exactly like a real one. The W_MOCK_SHAPE row itself stays, for the reason you give: a confirmed bare-64-hex row passes every predicate whatever wrote it, and that is why the PRECONDITION exists. Say in each place only what you read in your tree, with the file and lines.

RULING 3 (your O2, the residual of (a)): YOUR PICK STANDS. (a) checks the effective blob, as ruled; no every-copy term is built. Reason, the same as for (c): a term that could refuse a GENUINE undo on a row shape that no fixture here can rule out is a worse risk than the one it closes. But the residual's safety claim must be a TEST, not a reading of verification.ts: add ONE cell that builds exactly the residual forgery (BEFORE with a confirmed blob and a fake tx in metadata.blockchain beside a stuck certification_metadata.blockchain object), lets the reverse COMMIT it, and then shows the REAL verify rule answers anchored=false for that certification (and anchored=true as a control on a row where the confirmed blob is in the copy verify reads). Name the residual plainly in DECLARED, in the PR body and in the READY mail, with that cell's name and with the lines of verification.ts you read, so the next gate judges it with the evidence in front of it. If that cell shows anchored=true, STOP with a QUESTION: then the residual is the Blocker again and the term is needed.

RULING 4 (your O3): CONFIRMED. The 13 new synthetic fixture rows, and the changed expectations of F1, F2, F14 and F17, go in the same commit; each changed expectation is named in the PR body with the reason. Synthetic rows only; no box data in any fixture.

CHANGE 4, your pick of the SENTENCE: ACCEPTED, with your cells HDR-READ and Q6.

CHANGE 2, your two declared equivalent mutants (OES:dry, OES:apply): accepted as declared; say in the table that only HDR-OES sees them and why.

YOUR PREFLIGHT WARNING F-02 (no SSH identity in the keychain): received. It is the launcher's, not yours; Wednesday routes it. Your clone's push rests on the copied core.sshCommand under W1, as you say. If the gatetest or the push fails on identity, that is a STOP with the exact message, not a retry with another key.

LOAD: two WEDNESDAY-project checkers are still running test suites (load1 read between 12 and 17 in the last half hour). W5 stands: uptime beside every timing-based run, no override of the pushlock's load gate.

NEXT FROM YOU: build, prove, commit, push (gatetest, then real), one PR body edit, then READY FOR QA. A QUESTION at any point where a required change cannot be made sound inside the 6 files.
