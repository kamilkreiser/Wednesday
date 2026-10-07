---
date: 2026-10-08
type: grant
source: Kam, live board 2026-10-08 09:17:17 view=wednesday (card secuura-usage-89pct-raise-backlog-1008 = a)
status: live
tier: W
---

# Grant: this seat may spend to 100% of the weekly allowance, for raise, gate and merge seats only, until the renewal

**The operative case, so the headline matches it:** the weekly gauge is between 90% and 100% and Wednesday is about to launch a Secuura seat. **If it raises, QA-gates or merges PRs (or deploys, at most two at once, per the card's option text), launch it with `WED_USAGE_STOP=100` and name this file and the EXPIRING-GRANTS row as the authority.** Any other kind of Claude seat still stops at 90%.

**His words, verbatim (tap):** *"Decision secuura-usage-89pct-raise-backlog-1008: a — Lift the stop to 100% for raise, gate and merge seats only"*. The card's option (a) detail, which he chose: *"Same shape as your 10-06 grant: Spark on every briefable ticket, at most two deploy seats, raises partitioned by file. Ends at the renewal or when you switch accounts."*

**How to apply:**
1. Every launch past 90% names this file, the card id, and which clause it falls under (raise / gate / merge / deploy).
2. The Spark takes every ticket it can be briefed for; Claude seats only raise, gate, merge or deploy (≤ 2 deploy seats).
3. **Expiry is an EVENT:** the weekly allowance renews (~Sun 11 Oct, statusline `renews`) or Kam switches accounts or says stop. Do not renew by inference.
4. Unchanged: the v1.3 signature classes, the QA gate before every merge, KS-535, Phase 0, one client per Spark task, and leg 14 (KS-1450) still refuses any push touching `Blockchain/Dev/`, so this grant does not by itself unblock the raise backlog.

**Family:** [[2026-10-06_use-to-100pct-spark-all-tickets-one-or-two-deployers]] (the same shape, expired at the 10-07 /login) · [[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]] · [[2026-09-06_a-scoped-override-carries-its-own-expiry]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5).
