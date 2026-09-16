# [Secuura/Blockchain -> Wednesday] READY FOR QA: #1008 KS-1087 @dd7086d5aa574285beffc515f9371a438621f25d
# from: secuura-blockchain <secuura-blockchain@agentmail.to> · timestamp: 2026-09-16T14:53:04.000Z · message_id: <010001a0aab501f8-1405d95c-40f9-447c-8803-c67a6e706a2b-000000@email.amazonses.com>
# authentication_results: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
PR #1008 (KS-1087, item 1 only) is READY FOR QA at head dd7086d5aa574285beffc515f9371a438621f25d. POST /api/workflow-instances/:id/approve now answers 502 ORIGINATE_FORWARD_FAILED and KEEPS the pending document when originate refuses the forward; only a 2xx deletes it. "Part of KS-1087" (link: contributes KS-1087); the ticket stays open for item 2.

## Recommendation
Launch its QA gate at dd7086d5aa574285beffc515f9371a438621f25d. My read is tier 1: a behaviour change (a new 502) on an authenticated workflow route. Your call. Two things to weigh:
(1) the route is not in the published OpenAPI spec (0 matches for "workflow-instances" in secuura-api.yaml, control 3), so no contract documents the 502 and Schemathesis never reaches it;
(2) resolveStatus fires on the response headers, not on 'end'.

## Detail
PR: https://github.com/Secuura/Distributed_Secuura/pull/1008
Branch: feature/ks-1087-ornith-workflow-approve-keeps-pending, one commit on develop 93629700c (after #1005). 2 files, both services/api-gateway.
Ticket: KS-1087, facts comment af51e52a-e8d3-4f5d-a3b7-969e042daba3 (no mentions).

Deviations from the READY, deliberate:
- The READY's 401 cell is titled "…and the pending document survives" but never asserted it: its deleteCount was local to beforeAll and never read. I hoisted the counter. The 401 cell now asserts it unchanged; the 201 control asserts exactly one deletion.
- Two dead locals are _-prefixed (eslint).
- The product hunk is as held: git apply --recount, direct-apply fallback. patch(1) rejects the READY as malformed (miscounted header). The applied -/+ lines equal the READY's apart from one identical delete line git shows as context. Indentation inside the new Promise wrapper is ragged, kept as the READY's bytes.

Test Evidence summary:
- Red before green: READY test alone 2/3 red (expected 200 not to be 200 x2), control green; after the product hunk 3/3.
- Tampers (verification.ts restored to its sha each row; AssertionErrors only):
  - status check removed: 401 + unreachable cells red.
  - delete moved before the check: 401 cell red by the NEW survival assertion only; unreachable red by uDeleteCount.
  - delete removed: control red by the NEW deletion assertion only.
  - T0 and T0-after green.
- api-gateway 44 files / 388 tests pass (baseline 43 / 385 at 93629700c). shared 842/842. tsc rc 0. eslint: test file clean; verification.ts 5 warnings = develop's.
- Pre-push (14:46:42Z -> 14:52:00Z): PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (3, 4, 8). Nothing failed. PROTOCOL-CLEAN, first push.

NOT done / NOT covered:
- Item 2.
- A live approve against a running originate.
- Platform suites (the route is not in the spec; no stack).
- Preflight legs 3/4/8.
- A type-check including the test file.

Seat A open PRs: #1006 (KS-844, T1 @86fe59e6b), #1007 (KS-864, T2 @b28ed490a), #1008. That is 3, at the limit. Next when a slot frees: A9 KS-1072 (verification.ts chain 3 of 3; waits for #1008's merge anyway), or a file-disjoint one: A12 KS-871 / A13 KS-745 / A14 KS-999.

