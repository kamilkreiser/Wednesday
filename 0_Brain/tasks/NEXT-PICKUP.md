---
date: 2026-10-23
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the Opus 5.5 Wednesday morning seat of 23 Oct at its 67% checkpoint (2026-10-23 08:05 AEDT). Replace wholesale again; never stack. Previous version: NEXT-PICKUP.md.pre-1023-0806 and git history.
---

# NEXT PICKUP (Fri 23 Oct, written 2026-10-23 08:05 AEDT; ctx 67%, weekly 7d 96%)

## 00. LIVE STATE AT 08:05
- **Floor: %0 wednesday, %1 fleet-monitor, %30 Seat D 30th (Secuura/Blockchain-D, Opus 5.5, DEMO deploy), %31 Seat G 15th (Secuura/Blockchain-G, Sonnet 5.5, raise + KS-1707).** Both switched by Wednesday with `/model` at their plan prompts (the Secuura launcher pins `claude-opus-5`; fixing it is the project's file: a brief item, never edited from here).
- **D 30th:** demo build of develop `bcc51903d893` running detached on the box, 16 batches, ~6/16 at 20:51Z, projected end ~22:00Z (09:00 AEDT). Rollback set `pre-20261023d1` (33, idfp 4b52bd0652edd836). Its wake: `evidence/tools/autobeat_d30.sh` mails Wednesday a heartbeat every 20 min ('STATUS build (auto heartbeat)') and wakes the seat on done / fail / stall. **Pre-swap rule (Wednesday's mail 07:12): if its statusline reads >= 98% at the first swap, NO swap, STATUS "built, not swapped", wait.** Once swaps start it finishes them. Part D (post K1c to Stuart) ONLY on Wednesday's mail after Kam's tap.
- **G 15th:** PR #1679 (freeze, PR D) MERGED at 4caeec5fee78 (tree e128f13c9d55, verified at source by Wednesday). PR #1680 (KS-1709, head ebf294c37a84, landing f8981fe78807) and PR #1681 (KS-1622, head b5cc01ddcb2a, landing bf5482565b07) READY; **gate DA2 (Sonnet, Agent tool, background) running on both**: `0_Brain/reference/2026-10-23_gate-DA2-pr1680-1681/verdict.md` when done. PR C (KS-1707) building under ruling (B): three re-dates (react-router x2, braces), 16 stale removals (15 + sprintf-js, withdrawn upstream 19:21Z), contract edits, vacuity bound > 3, tier 2; NO prisma move.
- **Spark:** KS-1705 p1 HELD (`night/READY_KS-1705-KS-1705-REQBODY1705-1_...`, security.openapi.ts, needs a tier-1 gate and an openapi.yaml regen at raise). ks_1705_p2 CONTROL-FAIL by harness: asn1js/pkijs not installed in the Spark cache checkout (npm ci owed there). Screen 23 report: `0_Brain/reference/2026-10-18_spark-screen/SCREEN_23.md` (Q2-Q4 need rulings: KS-1683, KS-1703, the audit op).

## 0. NEXT ACTIONS, IN ORDER
1. **DA2 verdict lands** -> recompute the trailer (`sed '1,2d;$d' verdict.md | shasum -a 256`), ls-remote both heads + develop, completion check, then GO each merge by head sha to G 15th (one at a time, develop re-read after each). Verify each merge at source (tree == landing tree).
2. **PR C READY** -> its own tier-2 gate (Sonnet) -> GO -> verify. Then mark card `secuura-ks1707-redate-four-unfixable-audit-rows-1022` DELIVERED on the merged PR (`decision_queue.sh rule/--delivered`).
3. **D 30th DEPLOYED or "built, not swapped"** -> outside sweep (/, /verify/, /admin/, /health/deep, /api/zzz 404), then score + `pane_close.sh` in ONE action after its wrap.
4. **Kam's taps to act on:** `secuura-kintsugi-deploy-notice-1022` (a = D 30th posts K1c, 1,114 B ec613ad4d1ac897b, verified by Wednesday) · `secuura-ks485-answer-peter-vouch-secret-1023` (a = D 30th posts its 2,730 B draft) · `secuura-ks1707-fifth-row-postcss-no-fix-1023` (a = re-date postcss AND deepmerge-ts, mail G 15th before its PR C push) · `secuura-ks1709-keep-unanchored-certification-1023` (product decision). Every tap: rule it, act, mark delivered.
5. **Fresh login asked of Kam 07:12** (gauge 93 -> 95 in an hour). If the gauge nears 99% with no switch, say so on the panel.
6. Fleet flags: `fleet_ack.sh answered` lags the collector; re-run for any open G 15th QUESTION before the wrap.

## 1. IN FORCE (read the files, not this list)
- Usage is a GUIDE (Kam 2026-10-22 15:34); `fleet/USAGE_STOP.wednesday` = 100. Routing v1.0. October deploy grant until further notice (kintsugi first, then demo; KS-535). TESTED merge grant; merge-and-archive grant. The freeze pattern (lock refresh in range, nothing baselined) is Kam's three-time ruling: reported as a receipt.

## 2. OWED
1. **Follow-up ticket: the prisma-family move** (deepmerge-ts fix + valibot clear) needs `scripts/prisma-generate.cjs` to derive the client path from where @prisma/client resolved, plus a hoisted-layout cell (G 15th's evidence/prC/ E2 lock and its 3-line fix). Not in PR C.
2. **KS-1705 p1 raise** (tier-1 gate) and **ks_1705_p2** after an npm ci in the Spark cache.
3. STANDING_LINES additions (claim first): "a lock refresh is proven by parsing the locks, never by npm's rc"; the earlier owed lines from 22 Oct (searchIssues control; send_brief 'sent:' is not delivery; a waiter is a background job whose exit wakes the seat).
4. Secuura launcher: model pin `claude-opus-5` -> the newest Opus, and the box-reachability preflight leg: brief items for a Secuura seat (project file).
5. From yesterday, still owed: C 33rd (KS-1695 gap 2, Opus C3), KS-1692 PR 2, KS-1688 org-merge; Fable 5.1 trial gate.
6. Datasec/ATTIO digest mails keep arriving at wednesday-agent@ (third day): subject only; Tuesday's routing.

## 3. BOARD
KS open 689 at 06:07 (Backlog 354, Todo 26, In Progress 266, In Review 40, Blocked 3); completed since 06:00 22 Oct: 2. The 31 Oct target is off track.
