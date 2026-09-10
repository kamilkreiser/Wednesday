---
date: 2026-09-10
type: preference
source: Kam, email 2026-09-10 15:24
status: live
expires: 2026-09-14
tier: W
---

# Deploy freely to kintsugi AND demo until end of Sunday 14 Sep — and "everything possible" means what has MERGED

**His words, verbatim (email, 2026-09-10 15:24):**
> *"Ruling given. Please deploy everything possible to kintsugi. Also deploy everything possible to
> demo. This rule stands until the end of the week."*

**This lifts the demo-affecting pause for the week.** All day until this email, demo was his
signature class and every demo action stopped for him.

## The three precisions that keep this from being read too wide

1. **"Everything possible" = what has MERGED to develop.** It does **not** authorise merging the
   66 open unapproved PRs, bypassing a gate, or `--no-verify`. Those are not *possible* — they are
   blocked on a review nobody can give, which is the agent-identity problem and is untouched by
   this grant.
2. **Kintsugi first, then demo.** His 13:22 ruling the same day made kintsugi the dev box things
   land on first. **A four-hour-old rule is not silently reversed by a later one that does not
   mention it.**
3. **It EXPIRES.** Recorded in [[../tasks/EXPIRING-GRANTS]] with a date, because a time-scoped
   instruction with no expiry mechanism becomes a permanent change nobody decided to make.
   ⚠ *"End of the week"* read as **end of Sunday 14 September**, flagged to him as an assumption.

## What it does NOT change

**Production is untouched and does not exist** — measured 2026-09-10: the hostname does not
resolve and its config is deployed nowhere. **This grant is about two dev/demo boxes and nothing
else.**

The safety practices stay, because they are how a deploy is done rather than permission to do one:
**Phase 0 re-tag before building** (neither box has any rollback — 31/31 bare `:latest`, zero
dangling), **build everything before swapping anything**, **migrations in the middle** (046/047 add
CHECK constraints old code demonstrably violates), and **re-verify KS-535's wallet AFTER a redeploy,
not before**, because the risk is a redeploy overwriting it.

**Family:** [[2026-09-10_kintsugi-first-then-demo-behind-gates]] ·
[[2026-08-29_a-time-scoped-instruction-needs-a-mechanism-that-expires-it]] ·
[[2026-09-05_never-update-prod-and-demo-is-kams-class]] (suspended for this week only, by this file).
