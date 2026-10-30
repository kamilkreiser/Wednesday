## QA GATE - TIER 2, round 2: NO GO (one Major, a two-sentence doc edit; everything else can ship)

PR #1829, head `4c9b4ee18f1cf9f5f0ee238121c394840a15a331` (ls-remote at start = same; fetched into the round-1 clone `repo`, toplevel asserted equal to `.../2026-10-30_gate32-1829/repo`). Round-2 commit on `63c149736a26`: `git diff --name-only` = exactly `docs/SCOPES.md`, `docs/security/AGENT-DOCUMENT-OPERATION-RULES.md`, `docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md` (36 ins / 22 del). Docs only. Code was read from the head via `git show 4c9b4ee18f1c:<path>` (I could not move the round-1 `wt` checkout: the hook refuses git write verbs on it, and the code is identical because only docs changed). Paths relative to `Blockchain/Dev/`.

### Disclosure: the one remaining defect traces to MY round-1 F1
Round-1 F1 item (iii) said a connector can reach `/api/issuer-certs`. I read the scope gates in `auth/src/routes/issuerCerts.ts:63-120` but not the middleware above them. Every route there is mounted with plain `authenticate()` (issuerCerts.ts:193,331,378,433,539,708), and `authenticate()` calls `verifyAccessToken`, which throws unless `payload.type === 'access'` (auth/src/services/jwt.ts:337-343). The gateway turns an `sk_` key into a `type: 'connector'` JWT (jwt.ts:259-261, 280-290; gateway middleware/auth.ts:219-255). auth's own comment says `authenticate()` rejects connector tokens "by design" and that only `/users/stub` and `/users/lookup` use `authenticateAccessOrConnector` (middleware/authenticate.ts:66-93; users.ts:361-366). So an `sk_` connector key holding `issuer-certs:*` is refused at auth; the author followed my finding and wrote a door that, by this reading, is shut. (Human/OAuth `access` tokens with the role or scope do pass; those are not "keys".) Read from code, not probed.

## Q1 - round-1 findings

| Finding | New line | Verdict |
|---|---|---|
| F1 (R2 "agents cannot reach admin... by construction") | RULES:43-58 | Headline reframed ("intent, not what the code does") TRUE. Door list: register-connector + erasure TRUE; key minting TRUE; user creation TRUE; webhooks TRUE; signing TRUE; admin role-gated TRUE (proxy.ts:1252-1265). **Issuer-certs bullet FALSE for `sk_` keys (above) = still Major, see fix list.** |
| F1 UNDECIDED line | RULES:58 | TRUE as a statement of status; "stub scopes recorded in KS-1402 and KS-1653 as built" is consistent with users.ts:361,257. KS-1831/1832 contents not checkable (Linear) |
| F1 line 59 narrowed | RULES:61 | "touches no document itself but can cause a key that does to be minted" TRUE (security/src/index.ts:1144-1345; decideMint accepts any non-escalating scopes, provisioningPolicy.ts:106-116) |
| F2 matrix signing rows | RULES:145 | TRUE: `/sign/request` + `/sign` (documents.ts:1225-1345) check auth + tenant only; read-only key passes gateway (proxy.ts:657); returns hash+nonce (1252-1260); sets `signed`, accepts `mock_signature_*` or length>50 (1312-1330), no status check. Omits that `/sign` also needs a live nonce from `/sign/request` (1303-1309): incomplete, not false. "KS-1831 ... revoked document is written back to `signed`": ticket text unverified; code is consistent with it |
| F2 sign-cert/sign-wallet row | RULES:146 | TRUE (documents.ts:3004, 3272; ALLOWED_VERSION_ROLES = DOCUMENT_WRITE_ROLES :2309; issuer-certs:sign message :3086-3091). Note: for an `sk_` caller the downstream `issuer-certs/sign` call has the same connector-token problem as above, so "also needs `issuer-certs:sign` at auth" is true for access tokens only; harmless to the row |
| F2 closing sentence | RULES:149 | TRUE and honest ("not a list of everything a connector key can do") |
| F2 SCOPES rows | SCOPES:45,46 | TRUE; "originate then refuses it, except on the two signing routes" is incomplete (lifecycle events are also unrefused, matrix row 144) but not false for share/version |
| M1 users/stub admission | SCOPES:49, 66, 37 | TRUE (users.ts:247-259; mintInvitedStubHolder documents.ts:1670-1717 for transfer; gateway `/api/users` authenticates only, proxy.ts:550-553, lookup exception :473-478). CLOSED |
| M2 OAuth create | SCOPES:19 | TRUE: create check reads connectorMeta (round-1 verification.ts:746-751); originate applies `isAllowedByRoleOrScope(...'documents:write')` (documents.ts:388). CLOSED |
| M3 org-less existing user | RULES:79 | TRUE (provenance.ts:154-155, round 1). CLOSED |
| M4 preamble | unchanged | still open, by design; not re-litigated |
| N1 count | INV:47, 261 | CLOSED: I re-ran the quoted `git grep` at both `530f09112` and the head: 47 lines / 23 files, matches. No "31 code sites" text remains in docs |

## Q2 - new behavioural claims in the round-2 diff

| # | Claim | Where | Code | Verdict |
|---|---|---|---|---|
| 1 | provisioning key's direct mint reachable as `POST /api/security/keys`, gateway authenticates only | SCOPES:64, RULES:49 | proxy.ts:1214-1217 (`^/api/security`->`/api`) | TRUE |
| 2 | provisioning key carrying an org may not name another; org-less per-instance key bounded by tenant only | SCOPES:64, RULES:50 | shared keyRevokePolicy.ts:`decideTenantAccess` provisioner arm ("outside provisioning key organisation", "unbounded provisioning key"); index.ts:1269-1295 | TRUE |
| 3 | any other scope set accepted; nine-scope limit is register-connector's, `decideMint` says so on purpose | SCOPES:64 | provisioningPolicy.ts:29-33,106-116 | TRUE |
| 4 | leaked provisioning key cannot read/write a document with its own calls, but can mint a key that can | SCOPES:64 | same | TRUE |
| 5 | `/api/security` and `/api/users` (except lookup) authenticated only at gateway | SCOPES:37 | proxy.ts:550-553,1214 | TRUE |
| 6 | stub row detail: "INVITED user row for the email in the caller's tenant" | SCOPES:66 | users.ts:396-399 | TRUE |
| 7 | transfer to an email with no K user mints the stub first | SCOPES:49 | documents.ts:1670 | TRUE |
| 8 | webhooks open to `webhooks:manage` via `requireScope` | RULES:55 | proxy.ts:454-458; originate webhooks.ts:143 | TRUE |
| 9 | **`/api/issuer-certs` (upload cert+key, sign, revoke, rotate) is open to a key holding the matching `issuer-certs:*` scope; "a key can also reach ... `/api/issuer-certs`"** | RULES:53; SCOPES:135 | issuerCerts.ts plain `authenticate()`; jwt.ts:337-343; authenticate.ts:66-93 | **FALSE for `sk_` keys (Major)** |
| 10 | "a connector key can reach these routes, none of which is in the operation matrix below" | RULES:45 | matrix rows 145-146 list signing; the signing bullet itself points at the matrix | OVERSTATED (self-contradicting; Minor, fix with #9) |
| 11 | `/api/admin/` is "the one route family the gateway role-gates against connectors" | RULES:56 | proxy.ts:1252-1265 true; "the one" not exhaustively checked across other gateway mounts (platform.ts `requireOrgProvisioner` is another connector-aware gate) | UNVERIFIED as "the one"; Minor |
| 12 | analytics export routes store no caller/tenant, filter nothing by either; one caller's list returns every caller's exports, files included; KS-1856 | INV:119 | analytics.ts:305-380; exportService.ts:36-48 (no caller/tenant column), 96-99 (`listExports` returns the map, no filter), 149-153 (download URL) | TRUE for the list (note: also `GET /exports/:id`, same absence). POST "filters nothing" is odd wording but not false. Analytics data-query tenancy not read |
| 13 | "five routes, one in each of five services" (was "five in four") | INV:115 | governance.ts:492, stake.ts:448 (round 1); the other three not read | consistent now; 3 of 5 still unverified (as round 1) |
| 14 | SUPER_ADMIN count + exact command | INV:47 | re-run | TRUE |

## Q3 - docs only, nothing true removed
Docs only: confirmed (3 files). I read all 22 removed lines (-U0). Every removal is a rewrite with a successor or a deliberate retraction: "agents cannot reach ... by construction", "Everything not in this table is not an agent operation", "Grants no ... access" (now qualified), "31 code sites" (now command + count), "four of them". The round-1-TRUE claims touched by the diff (rows 20/21 provisioning guardrails, row 27 onBehalfOf) were narrowed, not dropped; the register-connector `scopes` refusal, wildcard/`organizations:register` refusal and own-tenant limit are all still stated.

## Fix before merge (exact sentences)
1. RULES bullet **"Issuer certificates. `/api/issuer-certs` (upload a certificate and its private key, sign, revoke, rotate) is open to a key holding the matching `issuer-certs:*` scope; the gateway authenticates and auth decides."** Replace with something true, e.g. "reachable by an interactive or OAuth access token holding the role or scope; an `sk_` connector key's token is refused at auth's `authenticate()` (the connector token's `type` is not `access`)", or move it to UNDECIDED if the author wants a running-stack probe first. Also drop it from SCOPES:135's list ("`/api/issuer-certs`") and fix the same-sentence overclaim "none of which is in the operation matrix" (RULES:45) by saying "except the signing routes".
2. Optional: qualify "the one route family" (RULES:56) as "among gateway mounts in proxy.ts".

## Can the rest ship?
Yes. With item 1 corrected the PR is a GO; every other round-2 sentence read TRUE or a Minor omission. If the cap forces a decision without another edit, the residue is one false door in a list that is otherwise right and carries an UNDECIDED line; I would ticket it rather than hold, but it is a Major by the stated rule, so I mark it fix-before-merge.

## What I did NOT test
No running stack, no request sent (the issuer-certs refusal is inferred from code: connector JWT `type` vs `verifyAccessToken`, not exercised). Linear contents of KS-1831/1832/1856/1402/1653/1807 not checked. KS-1845 routes 3-5 (kyc review, delegations, wallet sessions) still unread. Analytics data tenancy beyond the export list not read. Whether other gateway mounts role-gate connectors (RULES:56 "the one") not swept. Round-1 TRUE claims not re-read. Spark shadow not run (docs only, as round 1).
