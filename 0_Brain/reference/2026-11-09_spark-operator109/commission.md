# Spark operator 109 — commission (Wednesday, 2026-11-09, the 05:3x morning seat, 06:0x). Secuura only.

## BLUF
The Spark is IDLE since 04:24 (spark_status.py 05:4x: tunnel UP, queue 0) with operator 108's written reason (pool exhausted under the rules). Two things changed: (1) Seat T 17th's wrap names a concrete leftover: api-gateway/src/index.ts lines 327 and 329 still say SUPER_ADMIN_ROLES and are NOT in D5's (KS-2109) held READY; Wednesday ruled 06:0x that they stay out of D5 and go to the Spark as their own task; (2) new tickets may have been filed since 108. Kam, panel 2026-11-08 20:26: "keep it active as much as possible".

## Read first (whole)
1. Operator 108's commission.md and report.md in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator108/ (and the 106/107 chain it names): instruments, exclusions, SPARK_WORK_ROOT on the boot volume, hold_ready, the counter.
2. /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md (widened predicate).
3. For Job 1: T 17th's HANDOVER /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-17th/HANDOVER.md (the D5 lines), ticket KS-2109 (read-only, the project's Linear key sourced transiently, never printed), and D5's held READY in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/ (READY_KS-2109-*).

## Job 1: the two SUPER_ADMIN_ROLES lines (api-gateway/src/index.ts:327, :329 at develop)
Read the two lines at develop (git show, by ref, in your own clone on the boot volume) and KS-2109's words. Brief it ONLY if the ticket or D5's held change spells out exactly what those two lines become (the same replacement D5 makes elsewhere). Then: brief with new_brief.sh, every heading filled, the exact line text at develop and the new text; run, check, hold. It is an auth/role surface: its hold note says "tier 1 gate owed; raise AFTER D5's PR (KS-2109) merges or in the same tier-1 gate, file-disjoint check first" (routing v1.0 rule 4: the Spark may take a fully spelled-out edit inside an auth file; the PR gets a tier-1 Opus gate). If the fix is NOT spelled out (any 'decide whether'), do NOT brief: list it for a Claude seat with the reason.

## Job 2: screen and feed
Every KS ticket with identifier above the highest operator 108 read, and any ticket whose files were taken at 108 and are now free. TAKEN NOW (not yours):
- Seat B 106th (merge lane): PRs 2070, 2078, 2071, 2092, 2073, 2066, 2075, 2052, 2095, 2096, 2093, 2094, 2097, 2098, 2101, 2102, 2099, 2100, and the A3 group 2067, 2080, 2081, 2085, 2059, 2079, 2087, 2089, 2090, 2064, 2088: their files are taken.
- Gate 271 (running): PRs 2103 (KS-2107), 2104 (KS-1972), 2105 (KS-1974), 2106 (KS-2117).
- Seat G 30th: KS-1971 (ssrf-guard.ts), KS-1973 (vc/verifier.ts), KS-2110.
- Seat T 18th (being briefed): KS-2121, KS-2109, KS-2120, KS-2123 (after PR 2102), C1/C2 held.
- Seat U 20th: KS-2059 governance files.
- Held, not yours: O105-P1 (originate email.ts), KS-2099 item 1.
Brief with new_brief.sh (every heading filled), run, check, hold as 106/108 did. Counter: original + ONE rebrief. List every ticket read with verdict and reason.

## Limits
- export SPARK_WORK_ROOT=/private/tmp/spark_work_o109 (boot volume) on EVERY call; confirm with one ls after the first round. SPARK_MIN_FREE_GB=10 for queue.sh. DevMASTER read 10.6 GiB free at 05:4x: STOP if it reads under 10 GiB (df -g, every round), and say so. Load1 under 8.
- Re-pin develop by ls-remote first and per round (6c9a593df4abf746db612946a87839111ec5b7a9 at 06:01).
- queue.sh per batch only; leave nothing running when you finish. No push, PR, ticket write, comment or mail. Never delete; quarantine is a move with a WHY row. Never cd: absolute paths.
- Stop at 4 held passes, an exhausted pool (with counts), DevMASTER under 10 GiB, or about 2 h.

## Deliverable
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator109/report.md: BLUF; Job 1 verdict (briefed and held / listed for Claude, with the lines quoted at develop); Job 2 table (every ticket read, verdict, reason); held passes (name, hold_ready line, NOT covered); tickets for a Claude seat with reasons; disk before/after on BOTH volumes; UNMEASURED. Final message: BLUF + counts + held names + done.md row times only.
