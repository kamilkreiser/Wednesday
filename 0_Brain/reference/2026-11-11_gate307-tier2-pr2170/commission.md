# Gate 307, TIER 2 (Sonnet): R 94th round 3: PR 2170 (KS-1954, transfer escalation sweep). ONE PR, one verdict. Commissioned 2026-11-11 ~10:2x AEDT by the Mac mini Wednesday seat (owed from the 11-10 wrap handover).

Common rules: the tier-2 shape of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-10_gate306-tier2-pr2166-2169/commission.md (read whole; its common-rules pointer and its Constraints apply unchanged). Calibration of what a finding looks like: that folder's verdict.md.

Pins (Wednesday's ls-remote at 10:24:49 AEDT 2026-11-11; RE-READ at start and end, say whether each moved):
- develop 0b55401ad5dcb748f9dc47189f9896209567eb75 (PR 2156 squash; the PR was built on it or earlier: say which, and what develop's move since its base changed on its paths)
- PR 2170 head 52f482a8343635965f439193401bdbcfa087fc47 (KS-1954: transfer service, PRODUCT bytes change + tests, by the READY)

READY (read whole; reproduce, do not trust): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-10_seatR-94th/mail/ready_round3.md (if absent, out_ready_round3.txt beside it). Its stated facts: whole transfer suite 466/466 on develop, 471/471 with the patch; red-first 3 of 5; tsc with tests clean (planted control fires); and the PR says a step with NO workflow at all now also stays pending on every sweep (UNMEASURED how many exist).
Wednesday's rulings to the seat (read whole): /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-10_seatR94_raise.md (RULED sections; tier-2 stamp wording for product rows) and _R94_answer_gate305.md, _R94_answer_wrap.md in the same folder.
The held Spark pass: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1954-KS-1954-O131-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-APPROVALWORKFLOWSERVICE-PASS-7of7_2026-11-10.diff.md: compare the PR's diff with it per file and name every difference.

Questions:
1. File set exactly as stated; prove by the PR files API and a diff read.
2. Red proof: the new cells fail with the product reverted and the tests kept, and pass at the head. Your own mutant reddens a NAMED cell. Cells are pins and labelled honestly; say which 2 of 5 were not red-first and whether that is honest.
3. The change does what KS-1954's scope sentence asks, and no more (read KS-1954 at Linear read-only).
4. BEHAVIOUR CHANGE, the one that matters: a step with NO workflow now stays pending on every sweep. Measure what you can: which code paths create a step without a workflow (search with a control that hits), whether any existing data or test fixture has one, and whether 'stays pending forever' could block a real transfer that previously escalated or completed. If it can strand a real transfer, that is a NO GO unless the PR body names it AND a follow-up exists; say which.
5. Whole transfer suite (vitest) before and after, counts; tsc with tests. Whole-suite legs only when load1 < 8 (three long drive copies are running on this Mac mini: say if you could not, and what you ran instead).
6. Merge tree onto today's develop alone, and against each queued PR 2163-2169 (pins in gate 306's commission and 305's): any shared path, with a planted control.
7. No closing word in closing form in title, body, commit or comments.

SPARK SHADOW (rule 2026-10-26): after your verdict is written, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/gate/spark_gate.sh on PR 2170 exactly as /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-shadow-pr2127/commission.md did (read it whole; check the tunnel with python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/spark_status.py first; the tunnel was opened at 09:5x via the mini's alias hp-loan-spark). KNOWN TOOL GAP: a fresh spark_gate worktree has no built packages/shared/dist; record it as the tool gap, not a PR finding. Append a calibration row to this folder's calibration.md. Tunnel DOWN or a refusal: say so with exit code and output; never skip silently.

Verdict path: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate307-tier2-pr2170/verdict.md. Line 1 exactly: 'PR 2170: <GO | GO WITH NOTES | NO GO>'. Then FOUND / TESTED / HOW, NOT TESTED, findings G307-2170-<n> with severities. Return the whole verdict in your final message as well.
