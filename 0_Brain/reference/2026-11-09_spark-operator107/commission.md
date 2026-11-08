# Spark operator 107 — commission (Wednesday, 2026-11-09, the 03:5x overnight seat). Secuura only.

## BLUF
The Spark is IDLE (spark_status.py 03:5x: tunnel UP, queue 0, last round 02:22, 93 min). Operator 106 stopped on DISK (DevMASTER under its 18 GiB stop), not on an empty pool. DevMASTER now reads 14 GiB free; the boot volume reads 273 GiB free. So this round moves the Spark's WORK CLONES OFF DevMASTER: export SPARK_WORK_ROOT=/private/tmp/spark_work_o107 for every round.sh / queue.sh call (round.sh:73 reads it). Run dirs and done.md stay where they are (small). Kam, panel 2026-11-08 20:26: "keep it active as much as possible".

## Read first (whole)
1. Operator 106's commission.md and report.md in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator106/ — its instruments, exclusions and the 102..105 chain bind you, EXCEPT the disk limit below.
2. /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md (widened predicate).

## Job 1: screen and feed
(a) Every KS ticket with identifier KS-2127 or higher (paginated Linear read, read-only, the Secuura project's own key sourced transiently, never copied). (b) Then widen: KS Backlog/Todo tickets NOT already listed in operators 103..106's reports (newest first), read WHOLE at source, by the widened 10-28 predicate (test-only, comment/doc fixes, test hardening, one-file fixes with the shape spelled out). Excluded: auth/token/credential/security product surfaces unless the edit is fully spelled out AND the READY's hold note names a tier-1 gate; decision-shaped tickets; any file in an open PR (scan with a planted control, as 106) or a live lane:
- Seat B (merge lane): PRs 2074, 2068, 2070, 2078, 2071, 2092, 2073, 2066, 2075, 2052, 2095, 2096, 2093, 2094, 2097, 2098, and PRs 2099, 2100, 2101, 2102 — their files are taken.
- Seat T 17th: PR 2100 (KS-1868) round 2, and operator 106's 8 held READYs (its queue D) — those tickets and files are taken.
- Seat U 19th: PR 2099 (KS-2060) words round; KS-2059 design (governance).
- Held, not yours: O105-P1 (originate email.ts), KS-2099 item 1.
KS-2110 (drafted by 106, not run): you MAY run it — it is a security surface, so its hold note names "tier 1 gate owed".
Brief with new_brief.sh (every heading filled), run, check, hold as 106 did. Counter: original + ONE rebrief. List every ticket read with verdict and reason.

## Limits
- export SPARK_WORK_ROOT=/private/tmp/spark_work_o107 (boot volume) on EVERY call; confirm with one ls after the first round that the clone landed there and NOT in spark/cache/work. Set SPARK_MIN_FREE_GB=10 for queue.sh (it measures the runs volume, DevMASTER). STOP if DevMASTER free < 10 GiB (df -g, read each round). Load1 under 8.
- Re-pin develop by ls-remote first and per round (develop was 2935f7231097 at 03:54).
- queue.sh per batch only; leave nothing running when you finish. No push, PR, ticket write, comment or mail. Never delete; quarantine is a move with a WHY row. Never cd (a hook refuses it): absolute paths.
- Stop at 4 held passes, an exhausted pool (with counts), or about 2 h.

## Deliverable
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator107/report.md: BLUF; Job 1 table (every ticket read, verdict, reason); held passes (name, hold_ready line, NOT covered); tickets listed for a Claude seat with reasons; disk before/after on BOTH volumes; UNMEASURED. Final message: BLUF + counts + held names + done.md row times only.
