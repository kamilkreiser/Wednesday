# Secuura board audit — summary for Kam (2026-10-05, Wednesday)

## BLUF
- **529 open tickets. 64 are genuine product defects, 72 genuine hardening, 66 merged and waiting only on a live check, 55 need a human decision. 237 (45%) are the agents' own test/CI/tooling work filed on the product board. Only 13 are not genuine and 2 are duplicates; 12 are already fixed.**
- **Agents are no longer out-filing real problems:** agent filings fell 172 → 117 → 64 → 16 a week over the last four weeks (auditor C). The backlog is a stock problem, not a flow problem.
- **The path to "stable and ready by 31 Oct" is mostly DEPLOY + LIVE CHECK, not more code:** 32 of the 56 critical-path tickets are already fixed on develop but not deployed; kintsugi was last recorded on develop on 23 Sep (auditor A).
- **Archivable now: 38** (29 done-unarchived, plus 9 already-fixed/duplicate/process tickets proven at source). **44 more are Peter's or Stuart's** — listed for you, not archived.

## Counts (all 529 open; instrument: the three audit TSVs beside this file)
| class | n |
|---|---|
| TEST-OR-TOOLING | 237 |
| GENUINE-HARDENING | 72 |
| MERGED-AWAITING-SWEEP | 66 |
| GENUINE-DEFECT | 64 |
| NEEDS-HUMAN | 55 |
| NOT-GENUINE | 13 |
| ALREADY-FIXED | 12 |
| UNVERIFIED | 8 |
| DUPLICATE | 2 |

## Genuine defects most important for 31 Oct (each cited at develop 3ce8cd4026a6 by an auditor; ✔ = auditor re-read the line)
1. KS-1210 — any logged-in user can create an OAuth app or widen any app's scopes to `*` / `subjects:erase` (auth `oauth.ts:1148`, `:1245`). Tenant bound unmeasured.
2. KS-1401 / KS-1376 — tenant isolation gaps: `charge_events` RLS off on kintsugi; `certifications` has no `tenant_id` so its policy is skipped (migration 038a:72-89).
3. KS-1005 ✔ — nobody can change their password (404 for everyone).
4. KS-1256 / KS-1231 — connector allow-list fails OPEN on a missing/unreadable setting.
5. KS-1107 / KS-1116 — registration accepts any organisationId; any signed-in user can read any presentation by id.
6. KS-938 ✔ — disabling MFA keeps the TOTP seed and backup codes.
7. KS-1009 ✔ — unauthenticated wallet lookup returns user id, role, creation date.
8. KS-1384 / KS-1383 — repeat anchor request wipes a confirmed tx hash; credential verify checks no proof.
9. KS-801 / KS-806 / KS-695 — case-sensitive path checks; wallet email collision; missing connector org-erasure route.
10. KS-735 — verifier result page never shows title/issuer (Peter must pick the response shape).

## What an agent files that is not a real problem
Merge-process and PR-wording notes, board housekeeping, fleet/agent-host chores, tickets against unmerged or closed PRs, and one false premise. Separately, the 237 tooling tickets are REAL but they are about our harness, not the platform.

## Not verified
No live environment was checked (kintsugi RLS state, exposure, demo data). ~106 "merged but partial" residue claims come from agents' own comments, not re-read code. Ticket-level rows: `audit_A.tsv`, `audit_B.tsv`, `audit_C.tsv`; method + controls in each `audit_*.md`. One auditor claim discounted: the mobile exclusion lapses 2027-01-01 (re-dated by #1378 today), not 19 Oct.
