# Agent Document-Operation Rules — Platform K (KS-539)

**Status:** signed off by Kam 2026-08-05 (WED-65 sitting) **with the G-1 split ruled**
(`onBehalfOf` = share / revoke / transfer-custody · connector attribution = anchor /
lifecycle — see the matrix and G-1 below). Stuart + Peter sign-off verdicts were still open
when this was written; the board state is not readable from the repository and was not re-checked.
**Scope:** every non-human caller performing document operations on Platform K: the
Platform-S connector, MCP-fronted AI agents (`services/mcp-server`), and any future
OAuth app or automation. "Document operations" = create / read / version / share /
revoke / transfer-custody / anchor / certify / lifecycle-event.
**Grounding:** written against the KS-540 inventory
(`docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md`), the KS-480 ownership contract
(`docs/S-K-OWNERSHIP-CONTRACT.md` §6/§8), and `docs/SCOPES.md`. Compiled from
`develop`.
**Out of scope:** smart-contract cascading governance (KS-541, tracked separately).
Which humans may certify (KS-547) was decided and built on 2026-08-03: see the *Certify* row.

> **Re-verified 2026-10-30 against `develop` `530f09112` (KS-1807).** Every rule, matrix row and gap below was read against the code and the tests at that commit; the earlier wording is in git history. Citations are a file path plus the function, constant or route that carries the claim, with **no line numbers** (the old ones had drifted). Where the code does not follow a rule that a ruling or the spec makes clear, the passage says "known deviation" with the ticket. Where nobody has ruled which side is right, it carries a line starting `UNDECIDED (KS-1807`; do not assert either behaviour for those until they are ruled. Not re-checked: deployment state, and the Linear state of any ticket named here.

---

## The rules

### R1 — Agents are connectors, never humans

A machine caller authenticates with an `sk_` API key and is minted
`role: 'connector'` at the gateway (`services/api-gateway/src/middleware/auth.ts`),
exchanged for a 10-minute RS256 connector JWT (`services/auth/src/routes/internal.ts`, `POST /connector-token`;
`CONNECTOR_TOKEN_TTL_SECONDS = 600` in `services/auth/src/services/jwt.ts`; the algorithm is `JWT_SIGNING_ALG`, default and only registered value RS256).
An agent must never hold a human JWT, a seeded persona, or any human role. There is no
"agent role" — the connector role plus scopes IS the agent identity model.
**An OAuth client is not minted `connector`.** An OAuth token carries the consenting user's role plus the granted
`scopes` and `authMethod: 'oauth'` (`services/auth/src/services/jwt.ts`), so a downstream role check can pass it on that role before the scope is read.
The rule is operational, not enforced by code: the MCP client sends whatever `SECUURA_API_KEY` holds, and a value that does not start with `sk_` goes out as a Bearer token
(`services/mcp-server/src/api-client.ts`, `authHeaders`).

### R2 — Authority = scopes, deny by default, least privilege

What an agent may do is meant to be defined **solely by its key's scope set**, drawn from the
canonical vocabulary — the `SCOPES` array in `packages/shared/src/security/scopes.ts` (KS-843: the literal count and line range that used to be quoted here are gone on purpose; both were stale within one commit of being written, and neither is derivable by a reader),
mirrored in `docs/SCOPES.md`). The vocabulary has drifted: gates and mints also use strings outside it (see `docs/SCOPES.md`, *Scopes in use that are not in the vocabulary*). Consequences:

- **Deny by default is the rule's intent, not what the code does.** The intent is that an operation with no scope in the vocabulary is not available
  to agents. The code does not hold that line: the gateway only authenticates most mounts, and several services admit a connector key on a scope or role check of their own.
  Read from code on 2026-10-30 (not probed on a running stack), a connector key can reach these routes; apart from the signing routes, which the matrix lists, none of them is in the operation matrix below:
  - **`register-connector`** (the `organizations:register` provisioning key) and **GDPR erasure** (`subjects:erase`, KS-843) are open to a connector by design.
    Until `SUBJECTS_ERASE_SCOPE_ENFORCED` is set to `true` (it is not set in the repository's compose files or `env.example`), any caller with role `connector` passes the erasure doors without the scope,
    and the gateway logs `[KS-843] erasure allowed by ROLE without the required scope`.
  - **Key minting.** A connector key holding `organizations:register` can call the security service's key mint (`POST /api/security/keys`) directly. The gateway mount authenticates only; the decision is `decideMint` in `services/security/src/provisioningPolicy.ts`.
    It refuses `*`, any `<resource>:*` and `organizations:register`, and a mint outside the key's own tenant. A provisioning key that carries an organisation may not name a different one; the org-less per-instance key Platform S holds is bounded by its tenant only (`decideTenantAccess` in `packages/shared/src/security/keyRevokePolicy.ts`). Any other scope set is accepted. So a key it mints can carry scopes outside the nine that `register-connector` mints.
  - **User creation.** `POST /api/users/stub` creates an INVITED user row. `hasUsersStubScope` in `services/auth/src/routes/users.ts` admits `certifications:write` (every Platform S org key), `documents:transfer-custody` (KS-1653), `users:read`, `users:create`, `users:*` and `*`; the gateway's `/api/users` mount authenticates only.
  - **Webhooks.** `/api/webhooks` is open to a key holding `webhooks:manage` (the gateway's `requireScope`).
  - **Signing.** `POST /api/documents/{id}/sign/request` and `POST /api/documents/{id}/sign` check no scope or role in originate (see the matrix, *Request / submit a signature*).

  `/api/admin/` is role-gated against connectors at the gateway (`enforceAdminProxy` with `PROXY_ADMIN_ROLES` in `services/api-gateway/src/routes/proxy.ts`, which lists human roles only). Other mounts carry gates of their own (for example `requireOrgProvisioner` on register-connector in `services/api-gateway/src/routes/platform.ts`); this page does not census them.

  **A route family that looks like a door and is not: `/api/issuer-certs`** (upload a certificate and its private key, sign, revoke, rotate). Every route there uses auth's plain `authenticate()` (`services/auth/src/routes/issuerCerts.ts`), which accepts an access token only and refuses a connector token (`type: 'connector'`) by design (`services/auth/src/middleware/authenticate.ts`; `verifyAccessToken` in `services/auth/src/services/jwt.ts`). So an `sk_` key holding an `issuer-certs:*` scope is refused there. An interactive or OAuth access token reaches it on an admin role, or on an `issuer-certs:*` scope if it carries one; no path that gives an access token such a scope was found (the role-default scope set is `documents:write` for `OWNER` only, and the OAuth registrable set has no `issuer-certs` entry). Read from code, not probed on a running stack.

  > UNDECIDED (KS-1807, 2026-10-30): which of these routes are meant to be open to an agent. Only `register-connector` and erasure were ruled open; the stub scopes are recorded in KS-1402 and KS-1653 as built, and signing is tracked in KS-1831 and KS-1832. Do not assert either behaviour for the others until ruled.
- **Least privilege at mint.** Keys are minted with the minimal set for their purpose
  (the §8 document set for S org keys, nine scopes; `organizations:register` alone for the
  provisioning key, which touches **no** document itself but can cause a key that does to be minted, as the *Key minting* item above says). The provisioning path may not
  name its own scope set: register-connector refuses any `scopes` field with `403`
  (`services/api-gateway/src/routes/platform.ts`), and the security service refuses a provisioning key `*`, any `<resource>:*` and `organizations:register`
  (`services/security/src/provisioningPolicy.ts`, `decideMint`).
- **Keys are org-bound when minted by register-connector.** A key minted by an admin through the security service may carry no organisation (`organizationId` is optional, KS-33); then the tenant verdict applies, which KS-764 (below, R4) rules is the intended behaviour.
  Tenancy rides the verified key's metadata, never a caller-supplied header: the edge strips the trust headers (`stripTrustHeaders` in `services/api-gateway/src/utils/trustHeaders.ts`)
  and the gateway seeds the tenant from the verified credential. (`x-tenant-override`, honoured for the super-admin list only, is the documented exception; one originate admin route reads it raw — known deviation, KS-1847.)

### R3 — Acting for a person requires `onBehalfOf` provenance

When an agent performs a document operation **for a real user**, it must carry the
`onBehalfOf {email, displayName?, externalRef?}` triplet (KS-480 §6). The field is
connector-only — a human JWT sending it gets 400, "onBehalfOf is connector-only — interactive callers act as themselves"
(`extractOnBehalfOf` in `services/originate/src/services/provenance.ts`); a `null` value gets 400 for any caller. It is accepted on
create, version, share, transfer-custody, revoke and `certifications/issue`; lifecycle events and the flat anchor ignore or strip it for every caller (G-1). Semantics:

- Tenant-scoped resolution: same-org K user → true per-user attribution; different
  org → **403** (`{ success: false, error: { code: 'FORBIDDEN' } }`: a key attributes only within its own Organisation); no K user →
  verbatim provenance. So does an org-less key (it has no Organisation to resolve against), and so does an existing user who has no
  organisation: that user is not in a *different* organisation, so there is no 403 (`resolveOnBehalfOf` in `services/originate/src/services/provenance.ts`). Never creates an account, never grants auth — attribution,
  not identity.
- Stored encrypted in `action_provenance` (migration 041; PII keyring, deterministic
  `email_hash` for erasure), echoed on `GET /api/documents/{id}` (the `create` row only), pseudonymised on Art.17
  erasure (external_ref survives as the stable attribution id).
- An agent operating autonomously (no human principal — e.g. a scheduled
  re-verification) omits the field; the op attributes to `connector:<id>`, which is
  the honest answer.

### R4 — Consent chains through the Organisation

An agent's authority to touch a document comes from the **org that owns its key**,
which consented at provisioning time (register-connector, KS-480 §4). An agent
cannot borrow a user's consent to escape its org: cross-org attribution 403s (R3; KS-764 (2026-09-03): *"Refuse only a real cross-org mismatch (as built) — org-less keys keep the tenant verdict"*),
tenant isolation pins the data plane (RLS + GUC from the verified credential,
`services/api-gateway/src/middleware/auth.ts`), and the document rules are:

- **Read:** owner, admin, designated recipient or the creating connector, 404-cloaked (`GET /:id` in `services/originate/src/routes/documents.ts`). Known deviation, KS-1847: the check is skipped for a document with no recorded owner.
- **Share:** the handler checks the role-or-scope gate and that the document exists in the tenant; it compares the caller with no owner, recipient or admin. This rule used to say ownership checks "still apply on read/share/revoke". Known deviation, KS-1847 (same class: KS-1688 for the version source; KS-1833 and KS-1834 for lifecycle events).
- **Revoke:** owner-only, no admin bypass (403 "Only the owner can revoke this document"). A connector principal (`connector:<id>`) is never a persisted document's owner, so a connector cannot revoke today (the KS-566 finding of 2026-08-26; tracked in KS-1433).

> UNDECIDED (KS-1807, 2026-10-30): whether a connector, acting for a person with `onBehalfOf`, should be able to revoke at all (KS-566, PS-616; as quoted in KS-1433, the 2026-08-26 ruling was to ask Stuart to reconcile PS-616 first). Do not assert either behaviour until ruled.

### R5 — Provenance never reaches the chain

Nothing from `onBehalfOf` / `action_provenance` is ever anchored. Anchor payload
builders are fixed-field whitelists (`buildAnchorBody` in `documents.ts`, which spreads only the `identity` field from the request; anchoring `metadataPayload`, KS-240) and the flat-anchor schema (`anchorDocumentSchema` in `services/anchoring/src/anchorSchema.ts`) strips unknown keys;
the structural exclusion is pinned by `services/anchoring/src/__tests__/ks480-provenance-exclusion.test.ts`
(originate's `__tests__/ks480-provenance.test.ts` pins `extractOnBehalfOf` validation only, and says so). Any new
anchor-payload field must preserve this.

### R6 — Enforcement is server-side, layered, and revocable

No rule in this document depends on agent good behaviour. The layers:

1. Gateway `requireScope` on eight mounts of `services/api-gateway/src/routes/proxy.ts` plus the gateway's own document-create handler (`docs/SCOPES.md` lists them; it matches scopes by exact string, passes human logins without reading scopes, and honours a lone `*` but not `<resource>:*`).
2. Downstream `isAllowedByRoleOrScope` in originate (`services/originate/src/middleware/rbac.ts`; role arm first, then the shared `hasScope`, which does honour wildcards).
3. Ownership + tenant checks (§R4).
4. Connector JWTs expire in 10 minutes; keys are revocable (`DELETE /api/keys/:id` in the security service, revoke-then-rotate on compromise — contract §5) and
   support `expiresAt` for forced rotation. **Known deviation, KS-1847:** the revoke is immediate in the security service, but the gateway caches a validated key for 60 seconds (a rejection for 30) and nothing invalidates the cache on revoke, so a revoked key can still be accepted for up to 60 seconds. Contract §5 says revocation "takes effect on next validate".

### R7 — Every agent operation is observable

Person-attributed ops leave `action_provenance` rows, and so do connector-only ones now (`create:connector`, `lifecycle:<verb>`, the flat anchor — KS-566, KS-1557); `POST /api/documents/{id}/anchor` writes none. A reviewer must be able to
answer "which agent, whose authority, which document, when" from stored data alone.
Metering (KS-320 — K is the metering source S bills from) is narrower than this rule used to say: `charge_events` rows are written only for certification operations
(`services/originate/src/services/chargeEvents.ts`, called from `routes/certifications.ts`). Create, version, share, revoke, transfer-custody and anchor write none. Tracked: KS-1847.

> UNDECIDED (KS-1807, 2026-10-30): which agent operations are to be metered. Do not assert either behaviour until ruled.

---

## Operation matrix (agent-permitted document ops)

| Operation | Scope | `onBehalfOf` | Notes |
|---|---|---|---|
| Create document | `documents:write` | yes, when for a person | contract §6 home surface. The gateway's create handler accepts `documents:write`, `documents:*`, `*` or the legacy `register` |
| Read / list | `documents:read` **or** `documents:write` at the gateway | n/a (read) | RLS + ownership fan-in apply; originate has no `documents:read` check, so `documents:write` also admits reads |
| New version | `documents:write` | yes, when for a person | KS-86 — no separate scope until a connector needs it |
| Share | `documents:share` | yes, when for a person | G-1 ruling 2026-08-05. The gateway mount also requires `documents:read` or `documents:write`, so a key holding only `documents:share` is refused. No per-document access check (R4; KS-1847) |
| Revoke | `documents:revoke` is **minted but not checked** | yes, when for a person (implemented: KS-566, 2026-09-01) | G-1 ruling 2026-08-05. Service-side revoke is owner-only and a connector is never an owner, so a connector cannot revoke today (R4). Tracked: KS-1433 |
| Transfer custody | `documents:transfer-custody` | yes, when for a person | G-1 ruling 2026-08-05. A recipient email with no K user in the tenant creates an INVITED stub user (KS-1402, 2026-10-19, contract §11), so the address persists as a users row; this replaces the earlier PS-498 answer that the recipient email is never stored. Whether custody events also store it was not checked |
| Anchor (explicit) | `anchors:write` for `POST /api/anchors` and `/api/anchors/batch`; `POST /api/documents/{id}/anchor` needs `documents:write` (KS-1814) | **no — connector attribution** | G-1 ruling 2026-08-05 · supersedes the contract §6 flat-anchor coverage line; `anchors:read` is minted but no route checks it (KS-1433); auto-anchor on create covers most callers |
| Certify | `certifications:write` on `POST /issue`; no scope is checked on the other certification routes | yes — honoured on `/issue` per contract §6 | **Decided and built: KS-547 (2026-08-03)** — a `DOCUMENT_WRITE_ROLES` role or `certifications:write`, otherwise 403 `FORBIDDEN`. Connector traffic unchanged. `certifications:sign` names no route; `:share` and `:revoke` are unread (`docs/SCOPES.md`) |
| Lifecycle events | document scopes at the gateway (`documents:read` or `documents:write`); no role or scope check in originate | **no — connector attribution** | G-1 ruling 2026-08-05 · supersedes the contract §6 lifecycle coverage line. A sent `onBehalfOf` is ignored (KS-566; Platform S was still sending it). Any tenant caller who passes the gateway can record an event on any document in the tenant: tracked KS-1833 and KS-1834 |
| Request / submit a signature | **none checked in originate**: `POST /api/documents/{id}/sign/request` and `POST /api/documents/{id}/sign` | no (the handlers do not read it) | **Known deviation, not a design.** Both check authentication and that the document is in the caller's tenant, and nothing else: no role, no scope, no owner, recipient or creating-connector check. At the gateway they pass on `documents:read` or `documents:write` (the `/api/documents` mount admits either for every method but create), so a key holding only `documents:read` reaches them. `/sign/request` returns the document's content hash and a signing nonce. `/sign` appends a signature and sets the status to `signed`; it accepts any signature string that starts `mock_signature_` or is longer than 50 characters, and checks nothing about the document's current status (KS-1831 records that a revoked document is written back to `signed`). Read from code, not probed on a running stack. UNDECIDED (KS-1807, 2026-10-30): who may request and submit a signature. Tracked: KS-1832 (`/sign/request`), KS-1831 (`/sign`, High). Do not assert either behaviour until ruled. |
| Sign with a certificate or a wallet | `documents:write` on `POST /api/documents/{id}/sign-cert` and `POST /api/documents/{id}/sign-wallet`; `sign-cert` also calls auth's `issuer-certs/sign` with the caller's Bearer, which accepts an access token only (the connector token an `sk_` caller carries is refused there; read from code, not probed) | no (the handlers do not read it) | Checked in originate by `isAllowedByRoleOrScope`: a `DOCUMENT_WRITE_ROLES` role or `documents:write` (the handlers pass it as `ALLOWED_VERSION_ROLES`, the same set); see `docs/SCOPES.md`. These two routes are not the `/sign` pair above |
| upload / download / assign / unassign / rename / delete | vocabulary-only (KS-85/134) | — | **not issued today**; wiring one up requires revisiting this matrix, not just minting |

This table lists the operations the agent contract covers (contract §6, G-1). It is **not** a list of everything a connector key can do: the routes under R2 and the signing routes above are reachable too, and R2's deny-by-default is the intent, not the behaviour.

---

## Agent-surface register

- **Platform-S connector** — per-org keys minted via register-connector; §8 scope set (nine scopes, `docs/SCOPES.md`).
- **MCP server** (`services/mcp-server`) — fronts AI-agent tools (hash / register /
  verify / info; nine tools in four modules: `secuura_hash_document`, `secuura_register_document(s)`, `secuura_verify_by_id`, `secuura_verify_by_file`, `secuura_verify_documents`,
  `secuura_list_documents`, `secuura_check_workflow`, `secuura_get_connector_info`) and calls the platform with the `SECUURA_API_KEY` env key
  (`src/api-client.ts`). **Rule application:** each MCP deployment holds ONE
  org-bound key scoped to its tools' needs — never a platform-wide or human credential.
  MCP tool calls acting for a person must pass `onBehalfOf` through (today the tools
  don't — gap G-2 below).
- **Future OAuth apps** — not the same model today: an OAuth token carries the user's role plus granted scopes (R1), not `role: 'connector'`.

---

## Gaps / follow-ups (not blockers to sign-off)

- **G-1: `onBehalfOf` coverage beyond `POST /api/documents` — RESOLVED and IMPLEMENTED (Kam ruling
  2026-08-05, WED-65 sitting):** `onBehalfOf` pattern applies to **share / revoke /
  transfer-custody**; **connector** pattern applies to **anchor / lifecycle** (the op
  attributes to `connector:<id>`, no person attribution). Same shape, no variants.
  Consequences flagged, not silently merged:
  - The contract §6 coverage list (accepted 2026-07-29) included **lifecycle-events**
    and **flat `POST /api/anchors`** in the honoured set — **superseded** by this
    ruling; both drop to connector attribution. (The contract at this commit leaves those two lines "for sign-off"; the honoured-set list itself was not located.)
  - **Revoke** was absent from the §6 list; the ruling adds it.
  - **Certify** (`/api/certifications/issue`) is NOT named by the ruling — its §6
    coverage stands as accepted; KS-547 changed who may certify, not the connector path.
  The implementation alignment (add revoke extraction; remove lifecycle + flat-anchor
  extraction) was KS-566 and landed on 2026-09-01 (#742, `bb3bc5e78`), pinned by `ks566-g1-split.test.ts` and `ks566-connector-attribution.test.ts`.
- **G-2: MCP register tool carries no `onBehalfOf`** — an MCP agent registering a
  document for a user today attributes to the connector only. G-1 is ruled
  (2026-08-05), so this is actionable: wire the field through the register tool. Still open (the MCP client contains no `onBehalfOf`).
- **G-3: scope-vocabulary drift (KS-540 F-3/F-4/F-5)** — gateway wildcard handling,
  unvalidated mints, and out-of-vocabulary literals (`metering:read`,
  `webhooks:manage`) weaken R2's "vocabulary = authority" claim; consolidation
  sequenced in the inventory §6. Still open; tracked KS-1846.
- **G-4: seventeen services mount no role gate** (inventory §2.1; the list there was corrected on 2026-10-30) — they rely on
  gateway auth + ownership/tenant checks; fine under this model, but any NEW
  document-op route in those services must mount `isAllowedByRoleOrScope` from day one. Five routes in five of them are labelled admin or reviewer and are ungated (KS-1845).

---

*KS-539 · drafted 2026-08-03 from develop · re-verified 2026-10-30 (KS-1807) · linked: KS-480 (contract), KS-540
(inventory), KS-547 (certify gate, closed), KS-541 (smart-contract governance),
KS-320 (metering).*
