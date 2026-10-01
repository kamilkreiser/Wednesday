# Can more than one Platform S use kintsugi? — answer for Stuart

Read-only research, 2026-10-01. Code facts were read at develop `c56dd7c32edf` (Secuura/Distributed_Secuura). Ticket states come from Linear (KS team), read the same day. Nothing on kintsugi was called, measured or changed.

## BLUF

**Yes, with conditions.** K has no notion of "one Platform S". It identifies S **per Organisation**: each Organisation gets its own `sk_` key, minted at runtime by `register-connector`. A second S system just registers its own Organisations and gets its own keys, with no deploy and no env change. The one hard condition is that the temp system must use **Organisation GUIDs (externalRef) that differ from the existing S's**. A cloned S database with the same GUIDs would get back the existing Organisations with **no key**, or share them.

## Draft reply to Stuart

> Yes. Kintsugi doesn't limit you to one Platform S. It issues keys per Organisation, not per system, so your temp system can have its own keys alongside the current one.
> There's one condition: the temp system's Organisations need their own GUIDs. If you clone your current database, re-key the Organisation GUIDs first. Kintsugi treats the GUID as the identity, so a GUID it already knows returns the existing Organisation with no new key.
> Two ways to get keys. (a) We register the temp system's Organisations for you with the admin login and send you each key. (b) We mint the temp system its own provisioning key, and it registers its Organisations itself at creation, the same way the current one does.
> Nothing on kintsugi needs redeploying or reconfiguring. It's an admin action. Calls are server-to-server, so we don't need your temp system's URL.
> Send us the temp system's Organisation GUIDs (or tell us you want option b) and we'll issue the keys.

## How to register another environment

All of these are runtime admin actions on kintsugi through the public gateway (`https://kintsugi.secuura.net`). None needs a redeploy, a restart or an env change.

1. **Choose fresh Organisation GUIDs on the temp S.** `externalRef` = S's OrganisationGuid is the identity K matches on. The lookup is `SELECT … FROM organizations WHERE metadata->>'externalRef' = $1 LIMIT 1` under platform scope, so it runs **across all tenants** (`services/api-gateway/src/routes/platform.ts:606-609`). A GUID K already knows → `alreadyRegistered: true` and **no key** (`platform.ts:654-660`). So a clone must re-key its Organisation GUIDs first.
2. **Option A — admin registers each Organisation (works today, no S-side change).**
   - The caller needs a platform-admin bearer: role in `super_admin | SUPER_ADMIN | platform_admin | SYSTEM_ADMIN` (`platform.ts:64`, gate `platform.ts:91-114`).
   - `POST /api/platform/organizations/register-connector` with body `{ "externalRef": "<temp-S Org GUID>", "organizationName": "<optional>" }`. Optionally add `tenantSlug`. If it is absent, the Organisation goes into the canonical default tenant `a0000000-0000-4000-8000-000000000001` (`platform.ts:490, 558-578`).
   - The response, **once only**, is `{ organizationId, tenantId, tenantSlug, organizationSlug, keyId, key, scopes, rotated }` (`platform.ts:746-759`). The `key` is plaintext `sk_…`; K keeps only a sha256 hash (`services/security/src/index.ts:1088-1089`).
   - Default scopes are `documents:write/read/share/revoke/transfer-custody, certifications:write, anchors:read/write, subjects:erase` (`platform.ts:485-489`).
   - Hand each key to Stuart out-of-band. The temp S stores it and sends it as `x-api-key`.
3. **Option B — give the temp S its own provisioning key (self-service, the "one per S instance" design).**
   - An admin mints a key with scope `organizations:register` only: `POST /api/security/keys` (the gateway proxies `/api/security` → security `/api`, `services/api-gateway/src/routes/proxy.ts:1168-1171`; mint route `services/security/src/index.ts:1083`).
   - The body is e.g. `{ "name": "Platform S provisioning — temp UX", "scopes": ["organizations:register"], "tenantId": "<tenant>" }` (schema at `index.ts:599-613`; `organizationId` is optional).
   - The temp S then calls `register-connector` itself at Organisation creation (`platform.ts:102`).
   - Guardrails: it is pinned to its own tenant, it cannot widen scopes, it cannot rotate, and it cannot mint `organizations:register` or wildcards (`platform.ts:515-535, 585-601, 621-627`; `services/security/src/provisioningPolicy.ts:95-126`).
   - The design names this tier "one key per S instance (uat-ps → K demo; ps → K prod)" (`Blockchain/Dev/docs/S-K-OWNERSHIP-CONTRACT.md:106-110`, `docs/SCOPES.md:45`). That makes a third instance the intended pattern, not a workaround.
4. **(Optional) A separate tenant for hard isolation.**
   - `POST /api/platform/tenants` (super-admin, `platform.ts:236-256`). It also auto-mints a per-tenant Platform-S `metering:read` key (`services/tenant-provisioning/src/index.ts:295`, `meteringKey.ts:38-53`, KS-336).
   - Then pass `tenantSlug` in step 2, or `tenantId` in step 3.
   - **Not recommended for a UX demo.** Whether kintsugi runs with `MULTI_TENANCY_ENABLED` is UNMEASURED: compose defaults it to `false` (`docker-compose.yml:196`), and the box's `.env` was not read. Several multi-tenant defects are open (KS-1119, KS-598, KS-1235, KS-1055). The default tenant plus distinct Organisations is the well-trodden path.
5. **S-side config for the temp system:**
   - K base URL `https://kintsugi.secuura.net`.
   - The stored per-Organisation `sk_` key(s), sent as `x-api-key`.
   - **Do not send `x-tenant-slug`.** K overwrites tenancy from the key (`S-K-OWNERSHIP-CONTRACT.md:238-246`; gateway `services/api-gateway/src/middleware/auth.ts:334-336`).
   - No callback/webhook URL is registered in K for S. No grep hit on the S path; the webhook tables found belong to Teams/Stripe.
   - CORS (`CORS_ORIGINS`, `api-gateway/src/index.ts:340-353`) only matters if the temp S's **browser** calls K directly. The contract's integration is server-to-server, so it should need no change. UNMEASURED for Steve's UI specifically.
6. **Teardown when the demo ends.** Revoke each key: `DELETE /api/security/keys/:id` (admin, `security/src/index.ts:1285`). The Organisation rows stay. No unregister endpoint was found.

## EVIDENCE

**How K authenticates S**
- `x-api-key: sk_…` is validated by the security service.
- The principal becomes `role: 'connector'`, with `organizationId`, `tenantId` and `scopes` taken from the verified key, and inbound tenancy headers overwritten: `services/api-gateway/src/middleware/auth.ts:273-342`. The validate call is at `auth.ts:223`.
- The key is exchanged for a short-lived connector JWT at `auth.ts:327-330`.

**Identity is per Organisation, not per S instance**
- `S-K-OWNERSHIP-CONTRACT.md:56-63`: "per SSD Organisation … K-minted `sk_` connector key".
- `:71`: "One key per Organisation".
- `:100-102`: "never one per S instance".
- `docs/DR-RESTORE-RUNBOOK.md:99-102`.

**Registration code**
- `register-connector` handler: `services/api-gateway/src/routes/platform.ts:492-760`.
- Key minted with `connectorId: platform-s:<externalRef>` at `:690-709`.
- The Organisation row is inserted with `metadata {externalRef, connectorSource:'platform-s'}` at `:670-675`.

**No hard limit to one S**
- Key store `svc_api_keys` has `id` as primary key, and its only indexes are non-unique ones on `organization_id` and `key_prefix` (`migrations/002_verification-tiers.sql:553-569`).
- No migration declares a unique constraint on `connector_id` or `externalRef`. A grep of `migrations/` found none.
- `externalRef` "has no unique index" (`services/originate/src/routes/documents.ts:512-514`). Uniqueness is a **convention** enforced by the lockless check-then-insert in `register-connector`, not a DB constraint.
- No env var names a single S instance. A grep for `PLATFORM_S_*` returned nothing.

**Precision**
- **Hard behaviour:** a reused `externalRef` returns the existing Organisation and no key (`platform.ts:654-660`). A provisioning key naming another tenant's `externalRef` gets 404 (`platform.ts:621-627`).
- **Not a hard limit:** the number of Organisations, keys or provisioning keys.
- **Rate limit:** each key has a default rate limit of 1000 per 3600 s (`security/src/index.ts:610-611`).

**Mint permissions**
- The security service also accepts `ORG_ADMIN / ISSUER_ADMIN / ADMIN` for `/keys`, own-tenant only (`security/src/index.ts:1043-1051, 1139-1151`).
- `register-connector` itself is super-admin or provisioning key only (`platform.ts:91-114`). KS-1283 pins that this stays so.

**The "Platform tenant seed" log line is unrelated to S registration.** It seeds platform-DB tenants (`api-gateway/src/startup-migrations.ts:1206`).

**Tickets (Linear, read 2026-10-01)**

| Ticket | State | What it covers |
|---|---|---|
| **KS-480** | Deployed to UAT | Option A per-Organisation connector identity; this is where `register-connector` was built |
| **KS-772** | Todo | Stuart's S↔K review stream; its test pass is run from Platform S: register-connector → originate → anchor → verify → erasure → re-key |
| **KS-601** | In Progress | The kintsugi dev server itself |
| **KS-1283** | In Progress | Test coverage that tenant ADMIN stays refused on `register-connector` |
| **KS-579** | Todo | Platform-admin is a shared seeded account, so there is no per-person attribution on registrations |
| **KS-581** | Todo | Volume alerting and rate limit on `register-connector` |
| **KS-576** | Todo | Bulk re-key |
| **KS-583** | Todo | DR lose-a-key rehearsal |
| **KS-621** | Backlog | Document reads are scoped by tenant and owner, not by Organisation, so cross-org denial is emergent |
| **KS-748** | Backlog | `svc_api_keys.organization_id` is not a tenancy boundary |
| **KS-336** | Done | Per-tenant metering key |
| **KS-320** | Done | Metering API |

- **No KS ticket was found about multiple S environments, a staging S, or registering a second S.** Searches covered the terms "register-connector", "provisioning key", "organizations:register", "uat-ps", "second Platform S", "multiple Platform S", "staging", "S instance", "client key", "S↔K", "PS-" and "tenant".
- These are search results, not counts, so `board_count.sh` was not needed.

## UNMEASURED

- **Live state on kintsugi.** It is not known whether the existing S already holds a provisioning key there, which Organisations and externalRefs are already registered, or whether `/api/platform/organizations/register-connector` and `/api/security/keys` are reachable through kintsugi's front proxy. No live call was made.
- **`MULTI_TENANCY_ENABLED` on kintsugi**, and therefore whether option 4 (a new tenant) behaves.
- **Whether a platform-admin login on kintsugi works today.** The shared seeded admin is noted in KS-579; it was not tested.
- **Whether the temp system is a clone of S's DB** (shared Organisation GUIDs) or fresh. This decides whether step 1 is needed.
- **Whether Steve's UI calls K from the browser.** If it does, kintsugi's `CORS_ORIGINS` would need the temp origin, and that is an env change plus a restart, i.e. a deploy-class action. Not checked on the S side.
- **Isolation between the two S systems inside one tenant.** It rests on per-owner checks (KS-621), not an Organisation boundary. A demo with distinct Organisations should not see the other's documents, but that was not tested here.
- **S-side code (platform-s repo).** It was not read; how S stores per-org keys and whether its provisioning key is configurable per environment are assumed from the contract only.
