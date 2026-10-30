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
