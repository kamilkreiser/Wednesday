# Spark operator 106 — commission (Wednesday, 2026-11-09, overnight seat). Secuura only.

## BLUF
The Spark has been idle since 00:41 (spark_status.py at 01:56: tunnel UP, queue 0, IDLE 74 min). Operator 105 left the pool "exhausted under the rules", but new tickets have been filed since (S 37th filed KS-2109..KS-2116, S 38th filed KS-2117..KS-2126 overnight), and the gate-pilot rule (2026-10-26) makes Spark SHADOW reviews of tier-2 gates count as Spark work. Kam, panel 2026-11-08 20:26: "keep it active as much as possible". Two jobs, in order. Target: 3 held passes from Job 1 and every shadow row Job 2 can produce; never pad.

## Read first (whole)
1. Operator 105's commission.md and report.md in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator105/ — its instruments (including the --unidiff-zero retry) and exclusions bind you. 102's commission binds as amended by 103, 104 and 105.
2. /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md (the widened predicate) and 2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice.md (the shadow method and its calibration rows).
3. /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/gate/REVIEW_CHECKLIST.md and the header of spark_gate.sh.

## Job 1: screen the tickets filed since the last screen, and feed the Spark
Enumerate every KS ticket with identifier KS-2105 or higher (paginated read, state and newest comment first; Linear read-only, the Secuura project's own key sourced transiently, never copied). For each, read it WHOLE at source and decide by the widened 10-28 predicate: test-only work, comment and doc fixes, test hardening, single-file fixes with the shape spelled out. Excluded: auth/token/credential/security product surfaces (a fully spelled-out edit there is allowed only with a tier-1 gate named in the READY's hold note), anything decision-shaped, and any file in an open PR (check the open-PR file lists with a planted control) or a live lane:
- B 102nd merges PRs (2076, 2082..2071, 2092, 2073, 2066, 2075, 2052, 2095, 2096, 2093, 2094, 2097, 2098): their files are taken.
- X 9th: pre-run side-by-side on PR 2095's change, local branch only.
- U 18th: KS-2060 (governance), waiting on PR 2076.
- Held, not yours: O105-P1 (originate email.ts), KS-2099 item 1 (waits on PR 2094).
Brief (new_brief.sh, every heading filled), run, check, hold as 105 did. Round 1 for a fresh ticket; the counter is original + ONE rebrief. List every ticket you read with its verdict (briefed / why not) so the next screen starts where you stopped.

## Job 2: Spark shadow reviews of tonight's tier-2 gates (calibration)
For gate 264 (PRs 2093, 2094, 2097, 2098; verdict /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate264-tier2-t15-batch/verdict.md) and gate 265 (PRs 2095, 2096; /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate265-tier2-pr2095-pr2096/): run local-model/gate/spark_gate.sh per PR at the head the gate verdict names (re-read the head by ls-remote; if it moved, say so and use the gate's head). Do NOT read the Claude verdict until the Spark review for that PR is written, then compare: findings recalled, false positives (checked at source), verdict match, facts match. One calibration row per PR in the 10-26 lesson's CALIBRATION shape, in your report (Wednesday files them).
Job 2 runs one request at a time on the Spark, interleaved with Job 1 as the queue allows (MAX_NUM_SEQS=1).

## Limits
- Re-pin develop by ls-remote first and per round. Disk under 18 GiB free on DevMASTER = STOP. Load1 under 8.
- queue.sh per batch only; leave nothing running when you finish. No push, PR, ticket write, comment or mail. Never delete; quarantine is a move with a WHY row.
- Stop at 3 held + all six shadow rows, an exhausted pool (with counts), or about 2 h.

## Deliverable
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator106/report.md: BLUF; Job 1 table (every ticket read, verdict, reason); held passes (name, hold_ready line, NOT covered); Job 2 calibration rows; tickets listed for a Claude seat with the reason; UNMEASURED. Final message: BLUF + counts + held names + done.md row times only.
