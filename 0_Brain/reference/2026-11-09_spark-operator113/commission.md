# Spark operator 113 — commission (Wednesday, 2026-11-09, the 10:01 successor seat). Secuura only.

## BLUF
The Spark is IDLE since 09:34 (spark_status.py at 10:03: tunnel UP, queue 0, no drainer). Operator 112 (report in its final message; Wednesday's summary in today's note 09:36) held KS-2129 + KS-2130 on the new test_only_bash tier, spent KS-2141's counter (now a Claude seat's), and judged KS-1218, KS-1982, KS-2040, KS-2142, KS-2143 not briefable. Kam, panel 2026-11-08 20:26: "please check that the spark is running flash 4 and keep it active as much as possible". Screen and feed it.

## Read first (whole)
1. Operator 112's commission (0_Brain/reference/2026-11-09_spark-operator112/commission.md) and operator 110's commission.md + report.md (0_Brain/reference/2026-11-09_spark-operator110/): instruments, SPARK_WORK_ROOT on the boot volume, new_brief.sh caveats, brief_lint, the counter (original + ONE rebrief, then a Claude seat).
2. /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md (the WIDENED predicate) and local-model/spark/README.md (tiers incl. test_only_bash).
3. Seat S 41st's buildable list: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatS-41st/drafts/buildable.md (read-only).

## Job, in this order (read each ticket at source first: the project's Linear key sourced transiently from its own 4_Credentials/.env, never printed, read-only)
1. KS-1902 — scripts/check-akto-container-names.sh line 82: let the pattern skip one value token after a flag; S says "one file, an existing suite".
2. KS-1794 — deployment/azure/RUNBOOK.md line 142 wording + scripts/smoke-test.sh line 17 (print the smoke target with URL credentials stripped). Docs + one line. NOTE: Kam holds RUNNING the smoke test against a live box (KS-1250 scope); editing the script is not paused, and NOTHING may execute smoke-test.sh against a real host.
3. KS-918 — services/auth/package.json: move vite to devDependencies and regenerate the lock (only if the harness can regenerate a lock deterministically; else not briefable, say why).
4. KS-1718 — systemTest/fixtures/provision.ts redactSecrets (line ~271): the COMMENT variant only (say the redaction is cosmetic) is Spark-sized; systemTest is Peter's harness, so a PASS is held, never raised, until Wednesday rules.
5. Then re-screen the rest of buildable.md for anything a lane has since freed or that a tier now fits.
Verdict per ticket: briefed / not briefable + the failing clause / taken. Brief, run, check. Do NOT hold: leave each PASS in its run dir and list it; Wednesday reads every PASS diff and holds it herself.

TAKEN NOW (files off limits; check every open PR's file set via the GitHub API before queuing): Seat B 111th merge queue (PRs 2106, 2109, 2104, 2108, 2110, 2111, 2112, then 2092, 2073, 2066, 2075, 2052, 2095, 2096, 2093, 2094, 2097, 2098, 2101, 2102, 2099, 2100 and the A3 group). PR 2113 (KS-2055 half 1, at gate 276). Seat T 19th/T 20th: KS-2055, KS-2123 (after PR 2102), KS-2132, KS-2133, KS-2134, KS-2138 item 1, KS-2129, KS-2130. Seat U 20th: KS-2059. Owed to a Claude seat, not yours: KS-2141, KS-2127, KS-2131, api-gateway/src/index.ts 327-329.

## Limits
- export SPARK_WORK_ROOT=/private/tmp/spark_work_o113 (boot volume) on EVERY call; SPARK_MIN_FREE_GB=15 for queue.sh. DevMASTER 108 GiB free at 10:04.
- Re-pin develop by ls-remote first and per round (4e529633d0a1, PR 2107 squash, Wednesday's ls-remote 10:05:52).
- queue.sh per batch only; leave nothing running when you finish. No push, PR, ticket write, comment or mail. Never delete (quarantine = a move with a WHY row). Never cd.
- Stop at 4 PASSes, an exhausted pool (with counts), or about 2 h.

## Deliverable
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator113/report.md (or the final message if the Write is refused): BLUF; every ticket read with verdict and reason; PASS run dirs; tickets for a Claude seat with reasons; disk before/after; UNMEASURED. Final message: BLUF + counts + run dirs + done.md row times.
