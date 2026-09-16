# [Secuura/Blockchain -> Wednesday] READY FOR QA: #1007 KS-864 @b28ed490ada70df2056763f4512c98443285a694
# from: secuura-blockchain <secuura-blockchain@agentmail.to> · timestamp: 2026-09-16T14:17:53.000Z · message_id: <010001a0aa94cc04-dccf9f93-70e6-483f-bad3-0bc6026d05be-000000@email.amazonses.com>
# authentication_results: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
PR #1007 (KS-864, parts A+B) is READY FOR QA at head b28ed490ada70df2056763f4512c98443285a694. system-status.ts no longer resolves service or portal URLs to the dead secuura-staging / ashypond...westeurope estate under NODE_ENV=staging. "Part of KS-864" (link: contributes, only KS-864); the ticket stays open. The dead-estate grep measures 18, not the brief's 17 (details below).

## Recommendation
Launch its QA gate at b28ed490ada70df2056763f4512c98443285a694. My read is tier 2: no response-shape change outside NODE_ENV=staging, and staging's estate is gone. Your call. One thing for the gate to weigh: :527 is a /system/status remediation hint still naming secuura-staging-*. It is left for the open ticket, not touched here.

## Detail
PR: https://github.com/Secuura/Distributed_Secuura/pull/1007
Branch: feature/ks-864-ornith-dead-estate-pointers, one commit on develop 40fe4db69. 3 files, all services/api-gateway: system-status.ts (19 -/+ lines), ks864a-dead-estate-helper.test.ts, ks864b-dead-estate-portals.test.ts.
Ticket: KS-864. Facts comment 861c86e2-849d-478b-9663-d1c8bb375849 lists the remaining four items.

What the PR says (brief A10):
- Part A: the helper's staging branch is removed and the parameter renamed _azureServiceName. The model's extra comment above the const was dropped (brief: keep or drop); the brief's body comment was kept.
- Part B: three portal ternaries become env-or-compose-default.
- grep -c 'ashypond|westeurope|secuura-staging-' measured 22 on develop -> 18 after A+B = the 17 untouched call-site arguments + :527's  hint.
- Not closed: item 2 (:80 vs :8080; B's default stays :80), item 3 (headline ignores red panels), the 17 call-site arguments, the :527 hint.
- Test files renamed ks864a / ks864b (the collision); each is byte-identical to its READY + lines.
- git apply --3way fell back to a direct apply for both product hunks, rc 0.

Test Evidence summary:
- Red before green:
  - Both test files on the untouched product: 6 ran, 4 red (2 per file), controls green.
  - After A only: A 3/3, B 2 red.
  - After A+B: 6/6.
- Tampers (system-status.ts restored to its sha each row; AssertionErrors only):
  - A's staging branch restored: A's two red cells only.
  - The issuer staging ternary restored: B's two red cells only.
  - getServiceUrl ignores its env var: both controls.
  - T0 and T0-after green.
- api-gateway 44 files / 388 tests pass (baseline 42 / 382). shared 842/842. tsc rc 0 (the renamed parameter satisfies noUnusedParameters). eslint clean (develop's system-status.ts clean too).
- Pre-push (14:11:15Z -> 14:16:08Z): PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (3, 4, 8). Nothing failed. PROTOCOL-CLEAN, first push.

NOT done / NOT covered:
- Platform suites (Schemathesis scoped to A7/A11; no stack).
- Live /system/status against a running stack.
- Preflight legs 3/4/8.

Seat A open PRs: #1005 (KS-1073, T1, gate drafting), #1006 (KS-844, T1; head moving by one comment-only commit per your 14:10 ruling, HEAD MOVED line to follow), #1007. That is 3, at the limit. Next when a slot frees: A11 KS-1101 (system-status.ts chain 2 of 2; waits for #1007's merge anyway).

