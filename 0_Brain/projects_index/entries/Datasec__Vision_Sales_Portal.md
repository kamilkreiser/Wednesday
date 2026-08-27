---
client: Datasec
project: Vision_Sales_Portal
path: /Volumes/DevMASTER/!CODING/Datasec/Vision_Sales_Portal
status: active
updated: 2026-08-27
---

# Datasec / Vision Sales Portal

**Session 3 (2026-08-27 09:06–10:47, QuickQuote, scored 1.0): PUBLISH HELD, correctly** — Kam's "publish QuickQuote" was `promptSource: suggestion_accepted` (an accepted rendered suggestion, my own wording), not typed; all three authority surfaces (DKIM · card tap · typed turn) empty. **Item 15 built + merged: whole-dollar amounts in Lines/Totals, RATES keep 2 dp** (Kam may flip); introduced-and-caught unmarked-equation defect → general print gate (13/13). **Height: decimals = 0px change (1002/1032)**; levers measured A −127 (deletes item-12 arithmetic) · B −27 · C −18 · D −17 · E −61 → card `quickquote-height-lever` (rec E). **Deploy target now `1796f9b`** (code == v2.26; delta BACKLOG only). Zero mail spent. Zero-OTP post-deploy proof = AppServicePlatformLogs "Creating container with image" (instrument proved); version tile needs one OTP.

**Open / next (refreshed 2026-08-27 10:5x):**
- 🔴 **Kam:** type `publish` → deploy 1796f9b (v2.26; carries the live Feedback-button fix, day 2) · height lever card (rec E) · rates whole-dollar too? · custom domain at go-live (ruled) · `gh auth login` datasecau on this seat (K2) · 1 HIGH dependabot (tracked BACKLOG:209, chromium path not used).
- **Next session:** deploy on his word → platform-log proof → one live feedback re-verify once /healthz shows a lastSuccessAt · `.dockerignore` (BACKLOG).

**Session 2 (2026-08-26 17:12–17:58, QuickQuote, scored 1.0):** Kam's rulings BUILT and MERGED, nothing deployed — main **424f049** (four merges): item 12 three-block layout (number diff ZERO across 8 shapes; equations that do not reproduce at 2 dp marked "rounded"), OTP resend cooldown (60 s/address, before generation, failing sends still start it), **item 14 HP Authentication Suite logo** (tool + printed quote + PDF; disclaimer kept; name in the version tile), and **a LIVE defect found by rendering: every emailed quote / hosted Ctrl+P since v0.4.1 carried the floating Feedback button on page 1** — fixed as a print-chrome rule. Caught its own 3-page regression pre-merge and built `stage3/test/print-fit.mjs` (CI job). Zero ACS sends; cap still failing at wrap. **Deploy = card `quickquote-publish-v225` (rec publish; default hold).**

**Session 1 (2026-08-26, QuickQuote, scored 0.85):** Kam's afternoon change round shipped LIVE in four deploys under his first-party word — v2.23 (main e39a10f): Register-deal checkbox beside Customer name · Workpath compatible-devices link · PoC gated at 10 on the deal count with his text · PoC+Workpath behind advanced mode (new ADVANCED SVC sentinel pair) · price-tile clipping · CSV beside the emailed PDF · WIL-54 currency chips · feedback box (Table Storage, server-side whitelist proven on a stored row). Four defects found beyond brief: the item-5 PoC drop on the PDF path (negative control) · a SECOND drop that reached prod for one test quote (E2E caught it; mismatch guard added) · stale-FX response pricing AUD at the EUR rate (money bug, pre-existing) · Express-4 async rejections exiting the process (every route + requireAuth). **Item 12 = PROPOSAL only** (`Quoting Tool/hpas-quoting-tool/docs/item12-bom-layout/PROPOSAL.md` + before/after PNGs) — Kam rules before code. 🔴 Its test volume exhausted the ACS send cap → sign-in blocked ~06:50–07:5xZ (time-only; disclosed first; backlogged as a SPOF).

**Open / next (as of 2026-08-26 — superseded above):**
- 🔴 **Kam:** PUBLISH v2.25 (card; carries the live feedback-button fix) · custom domain at go-live (ruled) · masthead disclaimer alignment (backlogged, pre-existing) · `gh auth login` datasecau on this seat (K2 — all merges local --no-ff) · 1 HIGH dependabot on QuickQuote's default branch.
- **Next session:** ONE live feedback re-verify once /healthz shows a lastSuccessAt (sign in, POST /api/feedback, read the row from Table Storage) · `.dockerignore` (BACKLOG) · item 12 build only on Kam's ruling.

**Prior session (2026-08-22):** Ran from this seat but the work was ATTIO's
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
