# Spark operator round 8 (o121). Commissioned 2026-11-09 22:2x by the 22:20 Wednesday seat.
WHY: spark_status.py at 22:2x read 'IDLE since last round 39 min ago — queue EMPTY'. Kam, live board 2026-11-08 20:26, "please check that the spark is running flash 4 and keep it active as much as possible"; 15:58 today "spark is also back online. please use it as much as possible"; 20:21:56 "lets prioritise closing off priority secuura tasks and working with the spark on as many others as possible". Rule file: /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md.

METHOD: read WHOLE and follow the o120 commission and report, and the round-5 and round-6 commissions and reports they point to (method, tools, checker, hold steps, every exclusion, what was already rejected):
- /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_priority-triage-and-spark-o120/commission.md (PART B only — do NOT redo Part A's triage) + report.md + triage.md
- /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds-5/
- /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds-6/

POOL, in this order:
1. KS-1984 FIRST (named by o120's report): nft-certificate minting.service.ts JSON.parse on already-parsed JSONB, lines 123/505/592/678; no open PR at 20:5x; code_patch2 with a new vitest file. Re-verify those lines and 'no open PR touches the file' at source before briefing.
2. Then High-priority Backlog tickets that fit the Spark predicate, then any other.
EXCLUDE: everything o114-o120 held or rejected (incl. KS-716 and KS-1413, held o120); everything a live lane owns — R 92nd (raise: KS-2144, KS-2147, KS-2148, KS-2142, KS-2146, KS-2066, KS-2123, KS-2027, KS-2089, KS-2150, KS-2153, KS-2138), S board seat, G (KS-590, PR 2138); and every file an open PR touches (re-read the open PRs' file lists through the PR files API, with a planted control).

Brief, run and HOLD every PASS (clean --dry-run, then real). Report each READY path and rc. ROWIDs use o121. Keep at least one task above doc_only, and state the rung tried. Stop after 5 rounds or 90 minutes, whichever first. Leave the queue NON-EMPTY at the end if any honest piece remains (one queued task beyond your stop is fine — say which).

HARD LIMITS: never cd; never rm. In a /Volumes/DevMASTER/!CODING/ checkout use only ls-remote, show, log, diff, ls-tree, cat-file and grep: never fetch, never any git write verb. Linear and GitHub are READ-ONLY (keys in-process, never printed). Raise nothing, push nothing, post nothing, mail nothing. Touch no file under Blockchain/Dev/docs/. Keep load1 under 8 (a Sonnet gate subagent is running beside you).

OUTPUT: final message line 1 'Spark rounds o121: <n> briefed, <p> PASS (<h> held), <f> FAIL, <q> still queued'. Then a per-ticket report. Save it to /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-o121/report.md if your Write is accepted (else put it all in the final message). If the queue ends empty, carry a measured WHY line.
