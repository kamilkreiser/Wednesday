---
date: 2026-11-02
type: plan
source: Kam live 12:06:10 ("look at the current tickets, specifically the high priority and Dependency ones ... use as many agents as possible and let me know when you think you will get through these"); three read-only triage agents (A, B1, B2), counts summed by command
status: live
---

# Secuura KS board: Urgent + High + dependency tickets, plan and ETA (12:2x AEDT)

## What is on the board (232 tickets: 18 Urgent, 206 High, 8 more with "depend" in the title)
| Bucket | Count | What it needs |
|---|---|---|
| DONE, not closed (merged AND deployed to kintsugi) | 100 | a live check + close with an evidence comment |
| Agent-buildable | 91 | ~176 seat-hours of build (S=0.5, M=2, L=5), then gate + merge |
| Needs Kam | 21 | a decision each (list below) |
| Blocked | 8 | upstream (Prisma, postgres image CVE) or another ticket |
| Stale / duplicate / tracker | 7 | close with a pointer |
| Needs client (Stuart/Peter) | 4 | waiting |
| PR open | 1 | KS-1594 (PR #1794): gate + merge |

The "In Progress" picture: of the 129 tickets marked In Progress or In Review, most are actually merged and deployed. The board lags the code.

## The plan (agents, in parallel, as load allows)
1. **Close-out seats (start now):** verify each of the 100 DONE tickets on kintsugi or in the deployed code, post a facts-only evidence comment, close. Tickets whose acceptance needs a person to observe stay open and are listed. Two seats, split by file family.
2. **Dependency first:** the audit-baseline rows for zod (KS-1724) and @azure/msal-node (KS-1725) expire 2026-11-09 and would freeze every push again: fixed this week, first in the build queue.
3. **Build seats:** the 91 buildable tickets in batches by service, Urgent first (KS-1785, 1413, 1076, 1712, 1226, 1025, 785, 562, 918), then High. Every PR gets a QA gate (Opus for security/money/data, Sonnet otherwise) and a merge seat. Spark takes the mechanical subset.
4. **Kam's 21 decisions:** posted as cards with a recommended default each.

## ETA (estimate; measured inputs stated)
- Close-outs: ~1.5-2 days (100 x ~0.4 h, two seats).
- Builds: ~176 seat-h. The machine runs ~3-4 Claude seats at once (load gate); each PR also needs a 15-25 min push (measured today: 947 s, 1047 s, 1382 s, one at a time) plus a gate. Realistic: ~4-5 days of round-the-clock fleet time for everything agents can do.
- Today's measured pace: 23 PRs merged since last night (~15 h).
- Risks: the weekly allowance (12% now; last week reached 99%), machine load, and the 21 decisions (blocked items wait for you).

## Needs Kam (21)
- KS-1669 Renovate vs Dependabot for systemTest pins (07-04 ruling)
- KS-1389 slot-target.sh / preflight leg 13 change
- KS-1044 VM liveness signal + who is paged
- KS-869 accept or rework #880's Platform S choice (KS-843 grace overlap)
- KS-968 per-environment first-boot outcome without ADMIN_USER_PASSWORD
- KS-1012 branch protection (ruleset: 7 dead required checks, 0 approvals, admin bypass) — a GitHub admin change
- KS-1516 what an unverified timestamp may claim (today: verified true; /verify accepts a forged proof)
- KS-491 WAF / CAPTCHA product and spend
- KS-590 Peter's four disclosure questions (verify-by-hash cross-tenant fields)
- KS-602 / KS-603 product rulings BM-1, BM-2
- KS-624 prism random-byte proof: remove or fix
- KS-655 fleet-wide fix to the KS-78 drift check
- KS-889 re-mint or accept (5 of 32 keys recoverable; Stuart-facing)
- KS-1087 workflow-approve credential forwarding (item 2)
- KS-1336 downgrade from High or keep parked
- KS-1561 which registrant verify presents as certifier
- KS-229 close the 06-10 assurance umbrella or keep
- KS-256 your sign-off pass, then close
- KS-601 confirm the kintsugi dev/demo split is restored
- KS-762 confirm the 09-05 APP_DB_PASSWORD rotation happened

Evidence per ticket: triage_A.md, triage_B1.md, triage_B2.md in this folder.
