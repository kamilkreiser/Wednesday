---
client: Secuura
project: Blockchain
path: /Volumes/DevMASTER/!CODING/Secuura/Blockchain
status: active
updated: 2026-08-06
---

# Secuura / Blockchain (Platform K)

**Last session (2026-08-06, session 9):** Built and proved BOTH of today's ruled fixes,
then stopped short of shipping either. KS-563 (Urgent — false "Certified by issuer") is
complete to Kam's Option B and live-proven; KS-564's two 500s are fixed and reproduced
500-before / 201-after with a real `sk_` key; its third leg (Option A — connector token on
`/api/users/stub` only) is implemented and unit-proven. Both pre-merge tiers were run for
KS-563: **Akto PASS**, **Schemathesis better than baseline** (68 failing ops vs 88) with
zero failures on the changed endpoints.

**Open / next:**
- [ ] On Kam's channel-of-record confirmation: merge #651 → demo deploy (rsync + rebuild
      originate/verifier-frontend, restart api-gateway for the bind-mounted spec) → verify.
- [ ] Then KS-564: live-prove Option A end-to-end, ship all three legs as one piece (#652).
- [ ] **Peter KS-480 consent-by-silence — record AFTER EOD 2026-08-06.** Kam's ruling today:
      a short evening session does this; do NOT hold a day session waiting for EOD.
- [ ] Watch: Stuart's KS-539 verdict (Peter approved 08-05) · 2 flaky tier-3 tests.

**Blockers:** Merge + demo deploy **HELD under PROTOCOL v1.2** — both ship rulings arrived
as pane text, which v1.2 declassifies as a channel of record, and a demo deploy is
approval-class. Waiting on Kam-traceable confirmation. Nothing is on demo; develop untouched.

**Notes for Wednesday:** Two findings worth relaying fleet-wide. (1) **The Schemathesis
sweep locks itself out of `demo@secuura.io`** — the account it authenticates with — by
fuzzing `POST /api/users/me/change-password`; every other seeded account still logs in, and
an auth restart repairs it via the demo seed. Very likely the true root of the recurring
"sweep auth 401/403" class we have been blaming on stale .env tokens. (2) A **wedged Docker
Desktop daemon** cost ~35 min: builds hang at `load metadata` while host networking is fine
and `docker manifest inspect` hangs too; only `docker desktop restart` (CLI plugin) fixes
it — quitting the app does not.
