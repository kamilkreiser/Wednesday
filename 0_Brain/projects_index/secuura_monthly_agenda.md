---
date: 2026-10-30
type: agenda
scope: Secuura — items for Kam and Stuart's MONTHLY long-term development meeting (Kam, live board 2026-10-30 12:55:54)
status: live
---

# Secuura — monthly Kam/Stuart agenda (long-term development decisions)

Rule: learnings/2026-10-30_kam-and-stuart-meet-monthly-on-long-term-development.md. Near-term fixes never wait
for this meeting. Each item: BLUF, the measurement it rests on, and who found it. Next meeting date: UNMEASURED
(ask Kam once).

1. **KS-1384 per-event anchor date for Stuart** — card `secuura-ks1384-stuart-asks-a-date-1030`. Kam ruled the
   outline (posted, 616db2a5) instead of a date; whether the date question moves here is Kam's word.
2. **Provisioning-key DIRECT mint breadth (2026-10-30, Seat V 11th, KS-1807 docs pass).** A provisioning key
   holding `organizations:register` may mint any scope set except `*`, `<resource>:*` and
   `organizations:register` (stated policy in `decideMint`'s header: "deliberately NOT a copy of the contract's
   section 8 scope list"). Effect: a leaked provisioning key can mint a document-capable key in its own tenant;
   the org-less per-instance key Platform S holds is bounded by its tenant only. Read from code, not probed.
   Recorded UNDECIDED in AGENT-DOCUMENT-OPERATION-RULES.md (PR #1829). No ticket (design, not a defect).
3. **KS-1410 class: three decision-shaped 500-body sites** (Spark operator 23): api-gateway proxy.ts:430 502
   `details.reason` (KS-41 diagnostic in front of auth); demo-service reset.ts:69 (operator needs the text);
   timestamping :245 typed 503. Each is "keep the diagnostic or make it constant".

- **(added 2026-10-30 18:1x, Wednesday) KYC approval and the verification level — KS-1807 PR-2 UNDECIDED line.** Question for Kam + Stuart: should approving a KYC verification raise the user's verification level? Raised by Seat V 11th writing the docs (#1836). Evidence of what the code does TODAY: gate 39's answer 5 at 0_Brain/reference/2026-10-30_gate39-1836/verdict.md (pending at the time of this line). Not blocking any PR.

- **(added 2026-10-31 11:1x, Wednesday) Should a TENANT admin ever run the workflow escalation sweep for their own tenant?** KS-1881 (Seat S 9th, PR 1) restricts `POST /api/workflows/escalate` (transfer) to platform admins only, gate-only, no widening. Facts (S 9th, read at develop cb2320368ae4, unverified by Wednesday): processEscalations has one caller, the route; no timer or cron in transfer; the route is reachable only in-network (the gateway serves /api/workflows/* itself). Question for Kam + Stuart: does any tenant need to trigger its own escalations, or is it platform-operations only? Default if never discussed: platform-only, as built.

- **KS-2071, is a staker rewards product planned? (added 2026-11-06, Kam's card `secuura-ks2071-is-a-staker-rewards-product-planned-1106` = a.)** By Seat C 36th's code read at develop, not run on any box: the staking reward-claim routes have failed on every database built from the repo since 2026-03-20, because their table was never written; past login they read no role and no owner; nothing credits a balance; the one route that credits is a mock. Routes stay off behind the flag until this is decided. Options on the card: remove the routes, or build it properly with an owner check.

- **(added 2026-11-09 03:3x, Wednesday) Retire the governance stake path that names a WALLET?** Kam's card `secuura-ks2059-design-tenant-scope-named-route-1106` = a added a named stake route that "names a user and never a wallet". KS-2059's accepted design (Seat U 19th, design/ks2059_design.md, ruled by Wednesday 03:3x, default Q-d) KEEPS the old admin-by-wallet stake path, now scoped to the caller's tenant, because removing a live path was not in the card. Question for Kam and Stuart: retire the wallet-naming path (callers move to the user-named route), or keep both. Measured: unmeasured who calls the old path today.

- **(added 2026-11-09 17:2x, Wednesday) KS-1807: three K-side scope choices Stuart says cost S nothing (Kam's card `secuura-ks1807-undecided-k-side-1109` = a, 17:20:43: "Docs record today's behaviour now").** The docs now record today's behaviour; these three are the decisions left. By Seat S 45th's code read at develop 204e62acdc35 (drafts/ks1807_undecided_answers.md in its record, sha256 2f8e0ee4c79e7884), not probed: (1) `documents:revoke` is minted in the nine-scope set but read by no gate: keep minting it, or stop? (2) anchor reads are ungated by scope (gateway proxy.ts 913-916 has no requireScope on GET /api/anchors): gate them on `anchors:read`, or leave and stop minting the scope? S reads only GET /api/anchors/{id} and /tx/{hash} under keys that carry it. (3) a provisioning key may still mint keys directly (POST /api/keys) with any scope set except organizations:register, * and <resource>:* (provisioningPolicy.ts): limit it to the nine-scope set, or refuse direct mints? S uses only register-connector. Stuart's ruling on line 1 (no connector revoke with onBehalfOf) is already settled and goes into the docs.
