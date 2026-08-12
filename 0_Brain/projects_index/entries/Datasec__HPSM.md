---
client: Datasec
project: HPSM
path: /Volumes/DevMASTER/!CODING/Datasec/HPSM
status: active
updated: 2026-08-12
---

# Datasec / HPSM

**Last session (2026-08-12, session 4):** Azure step 6 done with Kam on the
login — `hpsm-dev-rg` (australiaeast, empty, no billing) + SP
`hpsm-claude-deploy` Contributor-scoped to the RG only; boundary proven by
logging in as the SP (AuthorizationFailed on Vision prod RG). Creds in
`4_Credentials/.env`. HPSM-7 Done with receipts; SETUP_RUNBOOK fully closed —
no Kam-gated setup remains.

**Open / next:**
- Kam's ~08-17 refinement session consumes the pack (HPSM-13) → D01 fill → build epics per ratified order
- In-session lookups: hosted-agents AU-East (portal), External ID Go-Local rate (pricing calculator)
- Nothing HP-facing without Kam's explicit send; architecture summary INPUT-ONLY until ratified

**Blockers:** none — setup complete; build work waits on the refinement session by design.

**Notes for Wednesday:** Azure now agent-actionable (SP in .env, scoped to
hpsm-dev-rg); anything billable still flags to you/Kam BEFORE creation. Board:
HPSM-6/7/10/11/14 Done (5 of 20). Gotcha: fresh SP needed ~30s AAD propagation
before first login.
