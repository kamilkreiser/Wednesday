# Spark operator 105 — commission (Wednesday, 2026-11-09 00:2x AEDT). Secuura only.

## BLUF
The Spark pool is exhausted under the rules (operator 104: no new tickets since KS-2116), and part of the reason is ~20 held READYs in local-model/night/ that no longer apply but still lock their files. Clear that, then feed the Spark from what it frees. Kam, panel 2026-11-08 20:26: "keep it active as much as possible". Target 3 held passes; never pad.

## Read first (whole)
1. Operator 104's commission and report.md, and ready_check.out + ready_check_b.out in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator104/. 102's commission binds you as amended by 103 and 104.
2. /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/_quarantine_2026-11-09/WHY.md (the shape of a quarantine record).

## Job 1: stale-READY sweep (yours to execute; quarantine is a MOVE, never a delete)
For EVERY READY_*.diff.md in night/ (not only 104's list), re-measure at the pin, by the same instrument as 104 (forward apply --check, reverse apply --check) and classify:
- REV-OK (already in tip): find the develop commit that landed it (git log -S or --grep with the ticket key, read-only). Move to night/_quarantine_2026-11-09/spent/ and add one row to WHY.md: file, class, the landing commit (sha + subject), how measured.
- NEITHER (drifted/partial) or NODIFF: read the ticket at source (state, newest comment first). Move to night/_quarantine_2026-11-09/stale/ with a WHY.md row: file, class, ticket state, and whether the work is still owed.
- FWD-OK: leave in place. Do NOT touch the two KS-2022 O104 READYs, O102-P1, or anything named in an open PR or a seat's live queue (T 15th is raising KS-2053, KS-2099, KS-2012, KS-2016, KS-2077, KS-2022; B 100th merges PRs; check the open-PR file lists with a planted control).
- Any READY with a HOLD-NOTE file beside it: move the note with it and copy the note's headline into WHY.md.
Report a count table (class -> n) and the full WHY rows. The moves happen in Wednesday's own tree (2_Project_Files/local-model/night/), which this commission authorises; nothing outside it.

## Job 2: feed the Spark from what Job 1 freed
For each stale READY whose ticket is still open and owed: is it briefable under the rules (one product file or tightly spelled, fix shape stated, a runnable test, NOT an auth/token/credential/security surface, file free of open PRs and live lanes)? The stale READY was round 1, so a new brief is round 2 of 2 (the counter); if the READY's own name says REBRIEF1 or round 2, it is spent: list it for a Claude seat, do not brief it. EXCLUDED: services/auth/src/services/accountLockout.ts (T 15th raises KS-2022 on it; the KS-1868 piece there needs a tier 1 gate, see the quarantined HOLD-NOTE). Brief, run, check, hold as 104 did.

## Limits
- Re-pin develop by ls-remote first (104 read 7eda23b34d3b7a413ca8f9c0945c7843708ce9f4 at 00:1x); re-pin per round.
- Disk under 18 GiB free on DevMASTER = STOP. Load1 under 8.
- queue.sh per batch only; leave nothing running. No push, PR, ticket write, mail. Never delete.
- Stop at 3 held, an exhausted pool (counts), or about 2 h.

## Deliverable
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator105/report.md: BLUF; Job 1 table + WHY rows; Job 2 held passes (name, hold_ready line, NOT covered); tickets listed for a Claude seat with the reason; UNMEASURED. Final message: BLUF + counts + held names + done.md row times only.
