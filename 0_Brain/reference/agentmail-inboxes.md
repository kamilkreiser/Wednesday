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

## API-key revocation semantics (AgentMail support, authoritative, 2026-08-25 mail <f335a081-34a5-4076-a56f-54324dd8edf6@mtasv.net>)
- Authorization decisions are CACHED up to 300s. DELETE removes the key from the
  source of truth immediately; already-cached decisions stay valid until expiry.
  (Our 08-13 measurement of ~299s flip is exactly this.)
- **No supported way to force immediate invalidation of a single key.**
- **Leak response:** delete the key + rotate the secret immediately, and treat
  the old key as potentially USABLE for up to 5 more minutes.
- Delay materially beyond 5 min after DELETE = unexpected → report timestamps +
  request IDs to support.
- Not documented on their side (their admission); this note is the record.
- Closes the 08-13 QUESTION thread (our correction mail + their reply). No
  further reply owed; any future mail to support is Kam's class.
- **Second support reply (Harry Du, 19:36Z):** frames the same delay as DELIBERATE
  ("some customers accidentally delete keys so we add this for them") vs Shaban's
  cache-expiry framing. The two explanations differ on WHY; the operational facts
  agree and are what we act on (≤5 min window, no forced invalidation, delete +
  rotate + assume 5-min tail). Support invites future findings. No reply owed.
