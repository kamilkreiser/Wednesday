---
client: Datasec
project: NexusAI
path: /Volumes/DevMASTER/!CODING/Datasec/NexusAI
status: active
updated: 2026-08-04
---

# Datasec / NexusAI

**Last session (2026-08-04):** Fixed Kam's Settings-page bug (RD-64): 403 on
quick-question / risk-criteria AI actions was a CSRF token-rotation race, not
an AI failure. Server no longer rotates the token per fetch; clients read the
cookie at request time. Deployed to Container Apps revision 69 and verified
signed-in end-to-end (all 200s, test artifacts cleaned up). Side find RD-65
(Low): bare /api/settings 404 behind the Appearance tab.

**Open / next:**
- Kam to confirm RD-64 in his own session and close (Tested - Release Ready)
- RD-62: surface data-freshness on /api/health + status page
- RD-61: dead ABTDEMO printer feed since 1 June — needs the fleet owner, not code
- Release Ready pile awaiting Kam: RD-59/60/63, RD-45, RD-41, RD-23

**Blockers:** RD-61 needs the external ABTDEMO/HPAM fleet owner; RD-18 waits on
Kam's legal decision.

**Notes for Wednesday:** demo env is Container Apps only (4.x VM decommissioned;
RD-49 residue: Azure-side deallocate needs the dev-tenant admin). If Kam reports
any Settings 403 again after a hard refresh, reopen RD-64.
