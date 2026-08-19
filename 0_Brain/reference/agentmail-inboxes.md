# AgentMail inbox registry (account: Kam's, via AGENTMAIL_API_KEY holders)

Date-stamped 2026-08-20. Source: live `GET /v0/inboxes` + Kam's identifications.
No secrets here — inbox addresses only.

| Inbox | Role | Status |
|---|---|---|
| `wednesday-agent@agentmail.to` | Wednesday's own inbox (live 2026-08-04) | active |
| `coagent@agentmail.to` | Legacy shared fleet bus; holds the original 2026-08-07 v1.3 grant. Migrated projects' scoped keys 404 here BY DESIGN | active, being retired |
| `secuura-blockchain@agentmail.to` | Secuura/Blockchain per-project inbox (scoped key) | active |
| `datasec-hpsm@agentmail.to` | Datasec/HPSM per-project inbox (scoped key) | active |
| `datasec-nexusai@agentmail.to` | Datasec/NexusAI per-project inbox | active |
| `datasec-vision@agentmail.to` | Datasec/Vision per-project inbox | active |
| `secure_abacus@agentmail.to` | **Old test inbox — IGNORE** (Kam, 2026-08-20, verbatim: "secure_abacus was an old test inbox, ignore it"). Never a grant recipient, never fleet routing | ignore |

The re-issued v1.3 grant (2026-08-19T22:08:45Z) sits in the six active inboxes:
Message-ID `<096604C5-237F-4467-9ECF-B79F975FCB11@me.com>`, subject reads
"Team collaboration" — **retrieve by Message-ID, never by subject.**
