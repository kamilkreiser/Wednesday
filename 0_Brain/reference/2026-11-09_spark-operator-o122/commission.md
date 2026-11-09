# Spark operator round 9 (o122). Commissioned 2026-11-09 23:4x by the 22:20 Wednesday seat.
WHY: o121 ended with the queue EMPTY at ~23:50 (report: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-o121/report.md, read it WHOLE). Kam: 'keep it active as much as possible' (11-08 20:26), 'use it as much as possible' (11-09 15:58). Rule: /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md.

METHOD: as o121 (its commission /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-o121/commission.md and everything it points to). Same HARD LIMITS, verbatim from there: never cd; never rm; in /Volumes/DevMASTER/!CODING/ only ls-remote, show, log, diff, ls-tree, cat-file, grep (never fetch, never a git write verb); Linear and GitHub READ-ONLY; raise, push, post and mail nothing; touch no file under Blockchain/Dev/docs/.

LOAD: o121 ran at load1 8-11 because a gate ran beside it. Before any WHOLE-SUITE leg (A6), wait in a loop until load1 < 6 (read `uptime` each minute; a gate subagent, gate 296, is running and should end within the hour). Single-file legs may run at load1 < 8.

POOL, in this order:
1. KS-1970 (o121 FAIL, cause unproven): re-run the GOLDEN control at load1 < 6. If ks728-social-link-responds.test.ts is green, re-run the model round as briefed. If it is still red, re-brief WITHOUT the six scheduled-sweep cells (the real-setInterval ones) and run again; if that is green, the six cells are the cause: say so. Either way write the measured cause.
2. WIDEN BY CARVING: o121 found 77 screened tickets dry. Read the CLAUDE BUILD rows of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_priority-triage-and-spark-o120/triage.md and High-priority Backlog tickets with 2-3 product files; carve any ONE-FILE piece that is independent (its own red test, no ordering dependency on the rest), fully spelled out. Say in the report which ticket each piece came from and what remains on the ticket.
EXCLUDE: everything o114-o121 held or rejected (incl. KS-1984, KS-2094, KS-2017 held o121; KS-2008 deferred behind KS-2017); R 92nd's carried rows (KS-2123, KS-2138, KS-716, KS-1413); KS-590 (PR 2138); every file an open PR touches (PR files API with a planted control).

Brief, run and HOLD every PASS (clean --dry-run, then real). ROWIDs use o122. Stop after 5 rounds or 90 minutes, whichever first.

OUTPUT: final message line 1 'Spark rounds o122: <n> briefed, <p> PASS (<h> held), <f> FAIL, <q> still queued'. Then a per-ticket report. Try to save it to /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-o122/report.md (o121's Write was refused; if yours is too, the final message is the report). If the queue ends empty, carry a measured WHY line.
