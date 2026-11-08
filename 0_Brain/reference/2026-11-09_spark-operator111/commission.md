# Spark operator 111 — commission (Wednesday, 2026-11-09, the 08:0x successor seat). Secuura only.

## BLUF
The Spark is IDLE again since 08:09 (KS-2134 PASS, held by Wednesday 08:1x as READY_KS-2134-...SOCIALTOKENPINS; routed to Seat T 19th as E3). Operator 110 (report /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator110/report.md) screened KS-2127..2138. Since then the board seat filed at least KS-2139 (F-2070-1 Medium), KS-2140 (F-2070-2 Low), KS-2141 (G243-F3+F4 Low) and possibly more. Kam, panel 2026-11-08 20:26: "please check that the spark is running flash 4 and keep it active as much as possible". Screen and feed the Spark.

## Read first (whole)
1. Operator 110's commission.md and report.md (folder above) and the 109/108 chain they name: instruments, exclusions, SPARK_WORK_ROOT on the boot volume, new_brief.sh (NOTE op 110: it writes the code_patch skeleton, not the test_only_input shape; brief_lint refuses '## Plant' with a golden_red.diff), hold_ready (--model-tag spark-dsv4flash; NEVER --title-from-brief alone), the counter (original + ONE rebrief, then a Claude seat).
2. /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md (the WIDENED predicate).

## Job
Screen every KS ticket numbered >= KS-2139, then op 110's 'not briefable' list again only where a lane has since freed files. Read each ticket at source (the project's Linear key sourced transiently from its own 4_Credentials/.env, never printed, read-only). Verdict per ticket (briefed / not briefable + the failing clause / taken). Brief, run, check. Do NOT hold: leave each PASS in its run dir and list it; Wednesday reads every PASS diff and holds it herself.
TAKEN NOW (files off limits): Seat B 109th merge queue (PRs 2103, 2105, 2106, 2107, 2109, 2104, 2108, 2110, 2092, 2073, 2066, 2075, 2052, 2095, 2096, 2093, 2094, 2097, 2098, 2101, 2102, 2099, 2100, A3 group 2067, 2080, 2081, 2085, 2059, 2079, 2087, 2089, 2090, 2064, 2088). Seat T 19th: KS-2109, KS-2120, KS-2055 half 1, KS-2123 (D4, after PR 2102), KS-2132, KS-2133, KS-2134 (E1-E3). Seat U 20th: KS-2059 governance. Owed to a Claude seat, not yours: api-gateway/src/index.ts 327-329, KS-2127, KS-2131. Check every open PR's file set (GitHub API) before queuing.

## Limits
- export SPARK_WORK_ROOT=/private/tmp/spark_work_o111 (boot volume) on EVERY call. SPARK_MIN_FREE_GB=8 for queue.sh. DevMASTER read 9 GiB free at 08:05 (a NAS move is freeing it now): STOP if df -g reads under 9 at any round and say so. Load1 under 8.
- Re-pin develop by ls-remote first and per round (425ea1d3df0f, the PR 2071 squash, by Seat B 108th's ls-remote 21:01Z).
- queue.sh per batch only; leave nothing running when you finish. No push, PR, ticket write, comment or mail. Never delete (quarantine = a move with a WHY row). Never cd.
- Stop at 4 PASSes, an exhausted pool (with counts), the disk line, or about 2 h.

## Deliverable
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator111/report.md (or the final message if the Write is refused): BLUF; every ticket read with verdict and reason; PASS run dirs; tickets for a Claude seat with reasons; disk before/after on both volumes; UNMEASURED. Final message: BLUF + counts + run dirs + done.md row times.
