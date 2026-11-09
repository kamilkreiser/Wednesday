# Priority triage + Spark operator round 7 (o120). Commissioned 2026-11-09 ~20:2x by the 18:46 Wednesday seat.
WHY: Kam, live board 20:21:56 (view=wednesday), verbatim: "as you are at 70% now. lets prioritise closing off priority secuura tasks and working with the spark on as many others as possible". The weekly gauge reads 69-70%. Rule files: /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-22_usage-is-a-guide-outcomes-over-rules-route-by-learnings.md and 2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md.

Measured by Wednesday at 20:2x (fleet/board_count.sh, real counts, team KS): Urgent (priority 1): backlog 1, todo 1, in progress 8. High (priority 2): backlog 87, todo 20, in progress 57.

PART A: PRIORITY TRIAGE (read-only; you change nothing on the board).
For every URGENT ticket (10) and every HIGH ticket in Todo (20), read the ticket at Linear (description and newest comments; key from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env, in-process, never printed) and classify it into exactly ONE class, with the evidence named:
  1. ALREADY DONE: the fix is merged on develop. Name the squash, read by git log --grep or the PR API.
  2. DUPLICATE: give the survivor's id, and say why it is the same defect.
  3. OWNED: an open PR or a live lane has it (the PR number, read through the PR files API or the open-PR list). Live lanes now: B 122nd (merge queue), R 92nd (raise: KS-2144, KS-2147, KS-2148, KS-2142, KS-2146, KS-2066, KS-2123, KS-2027, KS-2089, KS-2150, KS-2153, KS-2138), S 45th (board), G 32nd (KS-590, PR 2138).
  4. SPARK: briefable under the Spark predicate: one product file, the fix shape spelled out, a runnable test nearby, not an auth/credential/security surface (or a FULLY spelled-out edit inside one, which routing v1.0 allows with a tier-1 gate after), and not touching any file an open PR changes.
  5. CLAUDE BUILD: real work no local tier can do. Name the files, a size estimate, and whether it is disjoint from every live lane's files.
  6. NEEDS KAM OR A CLIENT HUMAN: a decision, or Peter's or Stuart's word. Quote the line that makes it so.
Do the URGENT ones first. Write the table to /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_priority-triage-and-spark-o120/triage.md (if your Write is refused, put it in your final message).

PART B: SPARK ROUND o120 (the Spark is idle; tunnel UP by spark_status.py at 20:1x).
Read whole and follow the round-5 and round-6 commissions and reports: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds-5/ and /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds-6/ (the method, tools, checker, hold steps, every exclusion and what was already rejected).
Pool, in this order: the class-4 SPARK rows from Part A first, then High-priority Backlog tickets (87) that fit the predicate, then any other. Exclude everything o114-o119 held or rejected, everything a live lane owns, and every file an open PR touches (re-read the open PRs' file lists through the PR files API, with a planted control).
Brief, run and HOLD every PASS (clean --dry-run, then real). Report each READY path and rc. ROWIDs use o120. Keep at least one task above doc_only, and state the rung tried. Stop after 5 rounds or 90 minutes, whichever comes first.

HARD LIMITS: never cd; never rm. In a /Volumes/DevMASTER/!CODING/ checkout use only ls-remote, show, log, diff, ls-tree, cat-file and grep: never fetch or any git write verb. Linear and GitHub are READ-ONLY. Raise nothing, push nothing, post nothing, mail nothing. Touch no file under Blockchain/Dev/docs/.

Output: final message line 1 'Triage: <u> Urgent, <h> High read; classes 1:<n> 2:<n> 3:<n> 4:<n> 5:<n> 6:<n> | Spark rounds o120: <n> briefed, <p> PASS (<h> held), <f> FAIL, <q> still queued'. Then the triage table, then the Spark per-ticket report. Save the Spark report to /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_priority-triage-and-spark-o120/report.md if your Write is accepted. If the Spark queue ends empty, the report carries a measured WHY line.
