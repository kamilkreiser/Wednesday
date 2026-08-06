---
client: Datasec
project: Lead_Bot
path: /Volumes/DevMASTER/!CODING/Datasec/Lead_Bot
status: active
updated: 2026-08-06
---

# Datasec / Lead Bot

**Last session (2026-08-06):** WED-75 closed. The LEAD_BOT_API_KEY Lead_Bot had
held since April was the key leaked in Vision's initial import (`96a5ff3b`) —
byte-identical, confirmed by hash — so this was leak remediation, not a config
sync, and the exposure ran about a month. Vision's current 64-hex key is now in
`4_Credentials/.env`, verified from disk on both sides; leaked value scanned for
and gone project-wide. First-ever `history.md` written, plus `BACKLOG.md` and a
root `.gitignore` (the credential folders were not covered by any ignore rule).

**Critical caveat:** the integration is **NOT live end-to-end.** `SALES_PORTAL_URL`
is still `http://localhost:4848` on Kam's explicit HOLD. Do not let this project
be reported as "handoff complete" — it is *credential fixed, wiring open*.

**Open / next:**
- [ ] WED-78 (b): confirm this project's Datasec tenant, then find any running
      instance — gates everything below
- [ ] WED-78 (a): decide the prod wiring (`SALES_PORTAL_URL`) — Kam-held 08-06
- [ ] Kam: `gh auth login` as `datasecau`, create the repo, generate deploy key
- [ ] Fix the `.env` location mismatch (code reads `2_Project_Files/.env`, which
      does not exist; canonical is `4_Credentials/.env`)

**Blockers:** tenant assignment TBD (workspace hard rule 4) blocks all `az` work.
`az` and `gh` are both unauthenticated for this project.

**Notes for Wednesday:** If a Lead_Bot instance is running on an Azure VM it still
holds the old leaked key and has been 401-ing every submission — silently, because
`salesPortalClient.js` falls back to a direct DB insert when the API fails. A
misconfigured instance therefore looks healthy while bypassing the API entirely.
That is the reason (b) is worth Kam's attention rather than being routine. Note
also: **this project has no git repo at all**, so nothing here is version
controlled and `history.md` is a single copy on one SSD.
