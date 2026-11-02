---
date: 2026-11-03
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE ~08:18 AEDT 2026-11-03 by the morning seat (respawned 05:34; ctx 70% checkpoint). Previous kept as NEXT-PICKUP.md.pre-1103-0818. Replace wholesale; never stack.
---

# NEXT PICKUP — Tue 3 Nov 2026, ~08:18 AEDT (morning seat, 70% checkpoint)

## SUBAGENTS OF THIS SEAT (they DIE at its rotation; re-launch from the workdir + today's note if no output)
- **Gate 151** (Sonnet T2, PR 1967 demo-service state.ts, head 118cf6d9): workdir `0_Brain/reference/2026-11-03_gate151-ks1868-pr1967/`. ANSWER goes to **Seat W 21st** (not yet launched).
- **Spark operator 92** (Sonnet): workdir `0_Brain/reference/2026-11-03_spark-operator92/`; supply = G149-F4 documentRepo.ts + GET /:id, referralService.ts :257/:68 (raise after the referral PR merges), G150-F3 probeDb prism/timestamping.
- ~~W 21st brief drafter~~ DONE: brief read whole, **Seat W 21st LAUNCHED 08:26** by the waiter at the first ROOM (pane %100, Sonnet 5.5). Its plan confirmation is owed; gate 151's ANSWER goes to it.
- **Rotation note (08:2x):** this seat rotated at ~78% ctx at a clean boundary. Live: R 77th %98, B 81st %99, W 21st %100. PR 1965 head fb0a2bee is up (probably R 77th's PR 7; READY not yet received -> gate 148 Opus -> Kam card).

## 🔴 UPDATE 09:0x (READ FIRST — supersedes below where it differs)
- develop **ddd770cab4aa** (PR 1967). Merged by this seat's GOs today: 1957-1963, 1966, 1967 (9).
- **PR 1969 (referral, T1, head 15c17034): gate 153 GO WITH NOTES. KAM CARD `secuura-pr1969-referral-rewards-reaward-1103` POSTED ~08:58 (rec a; default a after 4 h = not before ~13:00).** Pre-existing HIGH: progress save always fails (BigInt) -> milestones re-awarded even with a healthy DB; failed read -> duplicate awards; /milestones/check/:userId no owner check. W 21st asked to FILE 2 High tickets + PATCH notes. QUEUE to B 81st only at NOTES PATCHED; GO only after Kam rules or the default fires.
- **PR 1968 (vc-issuer, head 6e58db56): gate 152 GO WITH NOTES + FIX-BEFORE-MERGE wording (G152-F2). HELD BY WEDNESDAY (decided inside Kam's KS-1352 = a "a revoked credential fails"): a revoked credential verifies TRUE on a stale memory copy + failed DB read, and this PR extends it to hostile values. Do NOT queue 1968 until a fix makes the verify path refuse to answer from memory on a failed read (a fix seat; ticket being filed by W 21st). Kam told by FYI 09:0x (no card).** W 21st also files revoke()-swallows-failed-UPDATE (High) and patches notes incl. the F2 wording.
- **Next QUEUE to B 81st: PR 1964** at R 77th's NOTES PATCHED (gate 149; G149-F1/F2 ticket owed from R 77th).
- Subagents of this seat at rotation: Spark operator 92 only (gates 151/152/153 DONE). If no report.md after rotation: check spark/done.md + night/ READY_*O92*.
- Kam cards still owed after their Opus gates: R 77th PR 7 (fail-open), R 77th PR 10 (isPasswordBreached fail-open). Fix-seat candidates now: KS-1953/KS-1955 (erasure), the referral re-award + owner-check tickets, the vc-issuer revocation tickets (blocks 1968).
- W 21st %100 at ctx ~50% (items 5-8 drivers pushing; item 9 to re-verify + push). B 81st %99 idle (queue empty). R 77th %98.

## OWED FIRST (merge chain; every GO after: no un-MERGED GO outstanding, push_queue list, gate_stray_check rc 0, ls-remote pin + head; subject `GO: merge PR <n> at <head12> on develop <pin12> (Seat B 81st)`)
1. **PR 1964** (originate documents routes, T1, head 25c437f4): gate 149 GO WITH NOTES. R 77th asked to FILE a High ticket (G149-F1/F2 sign retry duplicates; F7 = existing KS-1831) + PATCH notes. QUEUE to B 81st at its NOTES PATCHED.
2. **PR 1967**: at gate 151's verdict -> ANSWER W 21st (notes) -> QUEUE.
3. **KAM CARDS BEFORE MERGE** (after each Opus gate measures): R 77th's **PR 7** (api-gateway brute-force guard + limiter header-write: fail-closed -> fail-open for a hostile value; precedent KS-1256 = fail closed; gate 148 at its READY), W 21st's **item 4 referral** (re-awards milestones / fraud boots empty on a failed read), R 77th's **PR 10** (isPasswordBreached -> false).
4. **Gates to commission at READY:** W items 3 vc-issuer, 5 m365, 6 originate (T2 Sonnet; item 6 = tests-included tsc 0 -> 82, measure it), 4 referral + 7 governance + 8 billing (T1 Opus), 9 transfer delegation (T2 unless a changed outcome); R 77th PR 8 anchoring (T1; amend + test-only `vi` commit RULED; two-commit merge shape), PR 9 auth session (T1), PR 11 security rotate (T1; it tells me before building).
5. **Operator 91's 11 held passes** (mostly T1: billing chargeable-events, m365 tokenCrypto, tokenisation vault, anchoring/timestamping init, auth userErasedSubscriber) -> W 21st raises them if context remains (grouping told first), else the next raise seat.

## STATE (08:18)
- develop **b85b7b6786fa** (PR 1966). Merged by this seat's GOs: 1957-1963 + 1966 (8).
- **Live seats (Sonnet 5.5):** R 77th %98 (raise: PR 7 READY at driver VERIFY, PR 1964 notes + ticket, PR 8 amend, PRs 9-11), B 81st %99 (merge; plan CONFIRMED; queue empty). W lane: W 20th WRAPPED; its six drivers (items 3-8: 45786, 56304, 51082, 77887, 51568, 6118) are detached, ppid 1.
- Scored + closed this seat: W 19th 0.94, B 79th 0.95, R 76th 0.93, B 80th 0.96, W 20th 0.94.
- **High tickets filed today (pre-existing, read back):** KS-1952, KS-1953, KS-1954, KS-1955 (+ G149-F1/F2 pending). Kam told once (combined FYI 07:06).
- **Kam ruled today:** wed-morning-plan-1103 = a; secuura-pr1961-erasure-skip-not-shredded-1103 = a. Nothing else from him since.
- **11-09 baseline fuse: FULLY RETIRED** (zod row gone with 1953; at develop b85b7b67 no row expires 2026-11-09 and no msal package row — measured by the B 81st drafter).
- Spark harness fixed 06:03 (deps store + LOCK KEY check). Gauge 7d ~62%.

## RULES IN FORCE
- Seat launch = its own call AFTER reading the dry run's CAPACITY line; FULL -> waiter (ledger 11-03).
- Pre-existing High finding from a gate: board search first; file via the PR's own seat on my word; read back.
- Read every drafted brief WHOLE; send-gate format rules (PROVENANCE `| read YYYY-MM-DD`, no unsourced scope words, git refs as words, fresh SELF-CHECK).

## OWED (not first-work)
- wed_claim release (Spark deps fix) once operator 90/91/92 loop logs are committed. WED-155 (curl argv keys). gate_common.md cwd/logs note. INDEX.md refresh. EXPIRING-GRANTS: mark the msal half retired too. Ticket candidates for a board seat: G139-F1 family, G145-F3, G146-F2, G149-F5, fragment follow-ups. Regenerate BOTH digests at wrap (ledger got 2 rows today).
