# Spark operator 110 — commission (Wednesday, 2026-11-09, the 06:3x morning seat). Secuura only.

## BLUF
The Spark is IDLE since its last round at 06:21 (spark_status.py 06:37: tunnel UP, queue 0, drainer not running). Operator 109 found no tickets at KS-2127 or above at its read; since then Seat S 39th has filed KS-2127 .. KS-2138 (rows of its GO, gate 249/263/260 findings, KS-2136 SDK test command, KS-2137 ks488/ks1937 global names, KS-2138 the PR 2091 group). Kam, panel 2026-11-08 20:26: "please check that the spark is running flash 4 and keep it active as much as possible". Screen the new filings and feed the Spark.

## Read first (whole)
1. Operator 109's commission.md and report.md in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator109/ and the 108/106/107 chain they name: instruments, exclusions, SPARK_WORK_ROOT on the boot volume, new_brief.sh, hold_ready, the counter (original + ONE rebrief, then a Claude seat).
2. /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md (the WIDENED predicate: multi-file test-only work, comment and doc fixes, test hardening, filing-list items are all allowed; a failed round is data).

## Job: screen KS-2127 .. KS-2138, then anything else newly free
Read each ticket at source (the project's Linear key sourced transiently from the project's own 4_Credentials/.env, never printed, read-only). For each: verdict (briefed / not briefable + the clause that fails / taken). Brief with new_brief.sh (every heading filled, the exact line text at develop and the new text), run, check, hold as 109 did.
TAKEN NOW (not yours; files of these are off limits):
- Seat B 107th (merge lane): PRs 2078, 2071, 2103, 2105, 2092, 2073, 2066, 2075, 2052, 2095, 2096, 2093, 2094, 2097, 2098, 2101, 2102, 2099, 2100, and the A3 group 2067, 2080, 2081, 2085, 2059, 2079, 2087, 2089, 2090, 2064, 2088.
- Seat G 30th: PR 2107 (KS-1971, ssrf-guard.ts), PR 2108 (KS-1973, packages/shared/src/vc/verifier.ts), KS-2110 (row 5, pushing now), PR 2104 (KS-1972 event-indexer.ts).
- Seat T 18th: PR 2106 (KS-2117 + KS-2086 README), KS-2121, KS-2109, KS-2120, KS-2123, KS-2055 half 1, D4 after PR 2102.
- Seat U 20th: KS-2059 governance files. Seat D 60th: kintsugi deploy (no repo files).
- Seat S 39th: board only (no files), but tickets it is mid-way on (KS-2086, KS-2138 group) are not yours to brief until you have read whether a seat already holds a fix.
- Held, not yours: O105-P1 (originate email.ts), KS-2099 item 1; api-gateway/src/index.ts lines 327-329 (owed to a Claude seat).
Check the open PRs' file sets before queuing anything (109's prscan shape).

## Limits
- export SPARK_WORK_ROOT=/private/tmp/spark_work_o110 (boot volume) on EVERY call; confirm with one ls after the first round. SPARK_MIN_FREE_GB=10 for queue.sh. DevMASTER read 10.30 GiB free at 06:37: STOP if it reads under 10 GiB (df -g, every round), and say so. Load1 under 8.
- Re-pin develop by ls-remote first and per round (5d6a95c552fd131a166776076d951666b6de7329 at 06:37:09, Wednesday's ls-remote).
- queue.sh per batch only; leave nothing running when you finish. No push, PR, ticket write, comment or mail. Never delete; quarantine is a move with a WHY row. Never cd: absolute paths.
- Stop at 4 held passes, an exhausted pool (with counts), DevMASTER under 10 GiB, or about 2 h.

## Deliverable
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator110/report.md (if your Write is refused, put the whole report in your final message instead): BLUF; table (every ticket read, verdict, reason); held passes (name, hold_ready line, NOT covered, tier owed); tickets for a Claude seat with reasons; disk before/after on BOTH volumes; UNMEASURED. Final message: BLUF + counts + held names + done.md row times.
