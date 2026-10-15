---
date: 2026-10-16
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE at the 50% checkpoint of the 06:0x Wednesday seat (2026-10-16 ~06:4x). Replace wholesale again; never stack. The previous version is in git.
---

# NEXT PICKUP (Fri 16 Oct, refreshed at the ~06:4x 50% checkpoint)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says (digest ~609 KB in ~650-line chunks). Then `kam_rulings_today.sh`, `kam_msgs.sh 3`, `newmail.sh` (never piped), `fleet_ack.sh list`, `decision_queue.sh list open`, `fleet/usage_gate.sh --check`, and `fleet/cockpit/pane_prompt_check.sh %0` (NOTE the path: fleet/cockpit/, not tools/).
2. **Kam's two standing words (EXPIRING-GRANTS top rows, end = the quota reset ~Sun 18 Oct 1pm):** (a) Spark only for new ticket work, briefed by Wednesday by hand; (b) push/merge/deploy what is ready FIRST, Claude seats past the stop for those jobs only. Weekly gauge 98% (renews ~2d 6h at 06:05 Fri). **Wednesday's reading told to Kam on the panel 06:1x (bf-b32dea7d8d2f), uncorrected so far: no Claude launches at >=99%, because at 100% this seat stops too.**
3. **MONDAY 2026-10-19: WED-154**, the storage policy for old Blockchain files and old tests. Policy + dry-run + first measured report + a card; nothing removed before Kam sees it.

## 1. STATE (06:4x Fri; no Claude seat live; panes %0 + %1 only)
- **develop = 76698952a75717bbcbc35ace85d08d6758d8844f** (ls-remote 06:1x). Moved overnight by PETER's own merges #1557 (KS-1615, systemTest app roll) and #1559 (KS-1447, schemathesis) — measured by `git log` in the Spark cache clone; systemTest only, api-gateway untouched. Our five 10-15 merges sit under it. **Nothing deployed.**
- **HELD READYs, waiting for ONE batched raise seat:** KS-1543 part 2 (night/READY_KS-1543-UNUSEDBODY-2_..._2026-10-15.diff.md) + part 3 if its round passes (below). Plan told to Kam: raise them together under one batched tier-2 gate when 2-3 passes are held.
- **SPARK ROUND IN FLIGHT:** `ks_1543_p3` (site :1579, GET /api/document-types logs the error it 500s on; brief night/briefs/ks_1543_p3/, CONTROL-PASS 7/7 at 76698952a). Drainer pid 37609; result lands in local-model/spark/done.md. On PASS: source-read patch vs golden, `hold_ready.py`. On FAIL: classify (model/harness/brief), counter = original + ONE rebrief.
- **HARNESS FIX TODAY:** tasks/code_patch/checker.sh A6 re-runs each NEW red's file alone x2 with the patch (FLAKY-UNDER-LOAD vs real red); arms local-model/tests/a6_isolation_arms.sh 4/4; IMPROVEMENTS row 2026-10-16 06:36. The api-gateway health families (ks1101/1248/1258/1054/1246/864a/b) flake under full-suite load.
- **HELD, waiting for Kam:** PR #1555 (KS-1114) head c85cc28d, card secuura-ks1114-title-reply-leaks-details-fix-now-or-wait-1015 (default a: fix after the reset).
- **Waiting for the reset:** KS-1612 (needs real Postgres), KS-1613/1614, KS-1611.

## 2. KAM'S CARDS OPEN
secuura-ks724-locked-account-template-exclusion-1015 · secuura-ks1385-null-issuer-certifications-1015 · secuura-ks1114-title-reply-leaks-details-fix-now-or-wait-1015 (all rec a). Plus 3 Datasec cards (Tuesday's/Friday's). Unanswered panel question (bf-f955bd7b56aa959f): lean boots at >=95% weekly gauge? Not a rule until he answers.

## 3. NEXT SPARK CANDIDATES (screen of all 369 KS Backlog/Todo titles, first half read)
- **KS-1462** (p4): originate migrate-tenant-data logs a non-Error throw as [object Object]; one file, log shape — most promising, read the ticket + file next.
- Read and rejected at title level: KS-1105 (frontend, no test script per KS-1391), KS-1471 (auth middleware surface), KS-1132 (platform-admin login, auth), KS-1115 (needs Postgres).
- Second half of the title list (lines 190-370 of the screen) NOT read yet: re-pull with the Linear paginated query (the screen file was in a session scratchpad).

## 4. OWED BY WEDNESDAY (own tools, small)
1. Spark tunnel: doctor.sh WARN for SEAT=wednesday on 47788 + a `spark/tunnel.sh up|check`.
2. cockpit.sh say --mail: stamp the mail's own timestamp into the pointer.
3. INDEX.md refresh (newest block 2026-09-23).
4. Deploy round (Kintsugi) for what sits on develop: a READ-ONLY census seat first, ONLY once tasks/DEPLOY-BLOCKERS.md clears (GATEWAY_VOUCH_SECRET first). Not started; under the 99% reading above.
5. stash@{0} from 10-14 is KEPT, never dropped.
