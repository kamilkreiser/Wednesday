---
client: Datasec
project: Vision_Sales_Portal
path: /Volumes/DevMASTER/!CODING/Datasec/Vision_Sales_Portal
status: active
updated: 2026-08-22
---

# Datasec / Vision Sales Portal

**Last session (2026-08-22):** Ran from this seat but the work was ATTIO's
(coupled pair). One change to Vision PRODUCTION: a least-privilege read-only
Postgres role (`attio_bridge_ro`, SELECT on 4 tables only) for the ATTIO bridge,
proven by 15 probes with real 42501 refusals. Vision's code was read, not
modified. Prod measured for the first time.

**Open / next:**
- Production has **1 quote**, status "generated", `lead_id` NULL — no lead has a
  quote. ATTIO-19's cutover criterion depends on data that does not exist. No
  ticket owns this.
- **Leads table frozen since 2026-07-02** (newest lead 2026-06-24) while 149 of
  153 rows carry a `monday:*` source — Monday sync or upstream board stalled.
  With Kam.
- Portal rate card is exactly **1.4x below** QuickQuote's on every line
  (1000/1500/200 · 30d vs 1400/2100/280 · 45d). Flagged on ATTIO-9, not resolved.

**Blockers:** none at this seat.

**Notes for Wednesday:** Prod Postgres is unreachable from dev machines; the only
firewall rule is AllowAllAzureServices, so DB work runs from inside Azure via
Kudu on `datasec-attio-bridge` with an Entra bearer. The prod admin credential in
`datasec-sales-kv/DATABASE-URL` IS the server admin — treat any task needing it as
prod-class. Do not "fix" the portal rate card by pasting QuickQuote's numbers: the
1.4x may be a deliberate cost-vs-sell split, and it is Kam's call.
