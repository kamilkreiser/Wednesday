---
date: 2026-10-16
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE at the 50% checkpoint of the 06:0x Wednesday seat (2026-10-16 ~06:4x); section 1 refreshed at the 65% checkpoint (~08:3x). Replace wholesale again; never stack. The previous version is in git.
---

# NEXT PICKUP (Fri 16 Oct, refreshed at the ~06:4x 50% checkpoint)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says (digest ~609 KB in ~650-line chunks). Then `kam_rulings_today.sh`, `kam_msgs.sh 3`, `newmail.sh` (never piped), `fleet_ack.sh list`, `decision_queue.sh list open`, `fleet/usage_gate.sh --check`, and `fleet/cockpit/pane_prompt_check.sh %0` (NOTE the path: fleet/cockpit/, not tools/).
2. **Kam's two standing words (EXPIRING-GRANTS top rows, end = the quota reset ~Sun 18 Oct 1pm):** (a) Spark only for new ticket work, briefed by Wednesday by hand; (b) push/merge/deploy what is ready FIRST, Claude seats past the stop for those jobs only. Weekly gauge 98% (renews ~2d 6h at 06:05 Fri). **Wednesday's reading told to Kam on the panel 06:1x (bf-b32dea7d8d2f), uncorrected so far: no Claude launches at >=99%, because at 100% this seat stops too.**
3. **MONDAY 2026-10-19: WED-154**, the storage policy for old Blockchain files and old tests. Policy + dry-run + first measured report + a card; nothing removed before Kam sees it.

## 1. STATE (09:1x Fri) — NO Claude seat live (R 46th WRAPPED 22:12Z, pane closed, scored 0.95; handover Blockchain/5_Project_History/2026-10-16_seatR-46th/HANDOVER.md)
- **develop = 76698952a75717bbcbc35ace85d08d6758d8844f** (Peter's #1557/#1559 on top of our 10-15 merges). **Nothing deployed.**
- **R 46th raises the three held Spark passes as TWO PRs** (brief fleet/briefs_staged/2026-10-16_seatR46_raise_spark_1543p2p3_1462.md):
  - **PR A = #1560 (KS-1543 parts 2+3), head 180c7c822b571b8ff8b5ea15d4286277948c66c0**, base 76698952a, ESLint verification.ts 0/0, api-gateway full-suite reds identical to the tip's (0 new), KS-1543 linked contributes, stays In Progress.
  - **PR B = #1561 (KS-1462 item 1), head ba8c18794beddd47e7704891e6cbd4efda7664f6**, base 76698952a; KS-1462 moved to In Progress by the GitHub integration on PR open. Both PRs READY FOR GATE (batched; overlap 0; merge-tree clean either order).
  - Push transport: per-command `-c core.sshCommand` WITH ServerAliveInterval (the F-02 launcher branch leaves a keepalive-less config; STANDING_LINES has the full line). Wednesday's plan answer item 1 was SUPERSEDED for omitting it (ledger).
  - Ruled by Wednesday: gate on 13/16 legs (3/4/8 need the local stack; no route/spec change). The 35 api-gateway tsconfig.test errors are leg 16's baseline (no ticket).
- **THE GATE WAITS ON KAM'S CARD `secuura-gate-at-99pct-two-spark-prs-1016`** (weekly gauge 99%). UNRULED at 09:10, so default b applied: R wrapped. NEXT: one batched Opus gate for #1560 + #1561 after Sunday's reset (~12:30) or at once if Kam /logins another account; the merging seat follows R 46th's HANDOVER section 1 (re-read develop, head == GO sha, one at a time, restore Linear to In Progress/contributes after each merge).
- **Harness changes today:** checker.sh A6 isolation re-check (load-flakes vs real reds; arms tests/a6_isolation_arms.sh 4/4) and hold_ready.py honouring it (backup .pre-1016-a6flaky; the subset-refusal branch NOT yet exercised).
- **HELD, waiting for Kam:** PR #1555 (KS-1114) head c85cc28d, card secuura-ks1114-title-reply-leaks-details-fix-now-or-wait-1015.
- **Waiting for the reset:** KS-1612 (needs real Postgres), KS-1613/1614, KS-1611.
- **HELD for the NEXT raise round (not R 46th's):** night/READY_KS-1541-REFUSALNOTE-1_spark-dsv4flash_BRIEFED-CODEPATCH-INFO-PASS-7of7_2026-10-16.diff.md (mcp-server tools/info.ts + a new test; disjoint from R 46th's files).
- **Spark queue EMPTY** after KS-1541 (3 briefed by hand today, 3 PASS first round, 0 rebriefs). Next: section 3; second half of the title screen read; KS-1526 skipped as decision-shaped.

## 2. KAM'S CARDS OPEN
secuura-ks724-locked-account-template-exclusion-1015 · secuura-ks1385-null-issuer-certifications-1015 · secuura-ks1114-title-reply-leaks-details-fix-now-or-wait-1015 (all rec a) · secuura-gate-at-99pct-two-spark-prs-1016 (rec a switch account; default b wait). Plus 3 Datasec cards (Tuesday's/Friday's). Unanswered panel question (bf-f955bd7b56aa959f): lean boots at >=95% weekly gauge? Not a rule until he answers.

## 3. NEXT SPARK CANDIDATES (screen of all 369 KS Backlog/Todo titles, first half read)
- KS-1462 item 1 DONE (Spark PASS, raised as PR B). Item 2 (TENANT_COPY_FAILED shape) is an either/or for a decision; the shared-helper extraction cannot go to the Spark (blank context line).
- Read and rejected at title level: KS-1105 (frontend, no test script per KS-1391), KS-1471 (auth middleware surface), KS-1132 (platform-admin login, auth), KS-1115 (needs Postgres).
- Second half of the title list (lines 190-370 of the screen) NOT read yet: re-pull with the Linear paginated query (the screen file was in a session scratchpad).

## 4. OWED BY WEDNESDAY (own tools, small)
1. Spark tunnel: doctor.sh WARN for SEAT=wednesday on 47788 + a `spark/tunnel.sh up|check`.
2. cockpit.sh say --mail: stamp the mail's own timestamp into the pointer. ALSO: `say %4 ...` (a pane id instead of the lane name) was a SILENT no-op on 10-16; make an unknown name fail loudly.
6. Proposal for Kam (not urgent): Secuura launches default SECUURA_ALLOW_ONDISK_KEY=1 (or seed the keychain) so F-02 stops leaving a keepalive-less core.sshCommand.
3. INDEX.md refresh (newest block 2026-09-23).
4. Deploy round (Kintsugi) for what sits on develop: a READ-ONLY census seat first, ONLY once tasks/DEPLOY-BLOCKERS.md clears (GATEWAY_VOUCH_SECRET first). Not started; under the 99% reading above.
5. stash@{0} from 10-14 is KEPT, never dropped.
