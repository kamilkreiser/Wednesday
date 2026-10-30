## QA GATE - TIER 2, round 1: NO GO

PR #1829 (Secuura/Distributed_Secuura), head `63c149736a262c6fd4b7e85d4c8ff16c96faab11` (ls-remote at start and at end: unchanged), merge-base with develop `530f091120d5`. Ticket KS-1807. Gate 32, findings-only. Nothing under `!CODING/` was written. Clone: `0_Brain/reference/2026-10-30_gate32-1829/repo` (toplevel asserted before fetch); PR head checked out at `.../wt`.

Why NO GO: two Major findings, both sentences that tell Peter a connector/agent cannot do something it can. A systemTest written to them would assert a denial the code does not give. Both fixes are doc edits only (list the doors, or mark UNDECIDED and file a ticket). Everything else sampled held up and the work is unusually careful: of 35 table rows, 31 TRUE (3 with Minor omissions: rows 19, 27, 4), 1 OVERSTATED (row 32, a count), 2 FALSE (rows 33, 34 = F1, F2), 1 split with 3 UNVERIFIABLE sub-claims (row 35).

All citations are at PR head, paths relative to `Blockchain/Dev/`. "D:" = doc line.

## Scope checks requested

(c) Diff is docs only. `git diff --name-only develop...pr1829` lists exactly `docs/SCOPES.md`, `docs/security/AGENT-DOCUMENT-OPERATION-RULES.md`, `docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md` (all under `Blockchain/Dev/`); stat +358/-232 matches. No product, test, OpenAPI or html file changed.

(a) Existence re-check with my own instrument (`scratchpad/chk.py`, `ids.py`; python -I; `git ls-files` / `git grep -w` excluding `*.md`):
- Backticked paths and md link targets: 84 found (author says 77; mine also counts relative link targets). Planted control `services/originate/src/routes/NOPE_planted_control.ts` was reported missing (instrument discriminates). Real misses: only partial paths (`routes/verification.ts` -> api-gateway, `routes/certifications.ts` -> originate, `src/api-client.ts` -> mcp-server, `__tests__/ks480-provenance.test.ts` -> originate) and the URL `/api/admin/`. All resolve to a tracked file under a service dir. None is a dead path.
- Identifiers: 118 backticked identifiers (author: 145; different heuristic), 0 missing from non-doc source; control `zzPlantedNopeIdentifier9` absent, `hasScope` present. 23 bare filenames (tests, migrations), 0 missing (`ks566-connector-attribution.test.ts` is in `services/anchoring`, not originate; the doc does not say which).
- UNDECIDED count: 12 + 2 + 2 literal matches = 16, of which 1 in SCOPES.md (D:5) is the preamble naming the convention; 15 real, as claimed. SCOPES.md 11, RULES 2, INVENTORY 2.
- Scope table: `SCOPES` array has 32 members (counted, scopes.ts:37-142); SCOPES.md table has 32 rows. 9-scope S set matches `S_CONNECTOR_SCOPES` (api-gateway/src/routes/platform.ts:605-609). 17 services with no role gate: census reproduces (25 service dirs excluding `_PLANS`/`shared`; 8 gated; 17 listed; my role-pattern grep over the 17 found only non-gate hits).

(b) Removals: all 36 removed SCOPES.md lines and a 1-in-5 systematic sample (31 of 154) of the removed security-doc lines read. Every one is either rewritten in place with a corrected claim, rewrapped, or a line-number citation deliberately dropped (the preamble says so). Sample of 15 specifics: `certifications:sign` / `kyc:submit` / `kyc:read` rows (route does not exist: confirmed, certifications router has no /sign, certifications.ts routes listed below); `anchors:write` (old row named `POST /api/documents/{id}/anchor`, wrong: that route is gated by `documents:write`, documents.ts:1474); "Wildcards are validated at API-key issuance time" (wrong: security mint is `z.array(z.string()).default(['read'])`, security/src/index.ts:665, and the doc now says so); "KS-1116 RULED, NOT BUILT" -> BUILT (migration `054_ks1116_vc_store_creating_principal.sql` exists, `mayRead` at vc-issuer/src/ownership.ts:112); "Agent document ops are metered" narrowed (see claim 29); "Revoke ... not yet implemented" -> implemented (checkOnBehalfOf at documents.ts:2751); `auth ... authenticate.ts:125-139` row (requireRole in auth is now at authenticate.ts:183, mounted nowhere: confirmed). Nothing silently dropped; no removed rule lacks a successor.

(d) Spark shadow NOT RUN: `spark_gate.sh` requires at least one repo-relative test file (`.py` pytest, or `.sh` / `*.test.ts` via shadow_facts.py) and diffs/executes product code at base vs head; a docs-only PR has no test file, so the runner exits 2 by its own usage rule. No Spark request was made.

## Claim table (35 rows)

| # | Claim | Doc | Code | Verdict |
|---|---|---|---|---|
| 1 | Gateway `requireScope` does not call `hasScope`; exact string match plus lone `*` | SCOPES:7,101 | api-gateway/src/middleware/scopes.ts:45,51 | TRUE |
| 2 | `requireScope` passes `jwt`/`email`/none callers without reading scopes | SCOPES:17 | scopes.ts:35-39 | TRUE |
| 3 | Eight `requireScope`/`requireScopeOrRole` mounts plus one inline create check, mount->scope table | SCOPES:23-35 | routes/proxy.ts:457,476,657,664,832,885,901,907; routes/verification.ts:669,749 | TRUE |
| 4 | Create check admits `documents:write`, `documents:*`, `*`, legacy `register`; 403 text | SCOPES:29,86 | verification.ts:749-751 | TRUE (applies only when `connectorMeta` is set, i.e. sk_ keys; see Note N2) |
| 5 | Erasure doors: scope passes; `connector` role passes while flag != `true` and logs `[KS-843]`; others (humans too) 403 `INSUFFICIENT_SCOPE`; flag read per request | SCOPES:65, RULES:46-48 | scopes.ts:152-192; proxy.ts:768-770,832,885 | TRUE |
| 6 | 403 body shapes differ between `requireScope` (flat) and `requireScopeOrRole` (envelope) | SCOPES:37 | scopes.ts:57-62 vs 184-192 | TRUE |
| 7 | `documents:*` key refused 403 on `GET /api/documents` (mount asks read-or-write exact) | SCOPES:101 | proxy.ts:657 + scopes.ts:51 | TRUE |
| 8 | `OWNER` carries default scope `documents:write` (only role with a default) | SCOPES:17, INV:2.2 | shared/src/security/scopes.ts:287-295; auth/src/services/jwt.ts:191,205 | TRUE |
| 9 | `DOCUMENT_WRITE_ROLES` = ISSUER_ADMIN, ORG_ADMIN, SYSTEM_ADMIN, SUPER_ADMIN; seven consumers in documents.ts plus `/issue` | SCOPES:46, INV:1.4 | originate/src/middleware/documentWriteRoles.ts; documents.ts:388,1474,1854,2330,2528,3004,3272; certifications.ts:246 | TRUE |
| 10 | `documents:write` gates version, anchor (then per-doc access: 404 cloak; revoked/deleted 400), sign-cert, sign-wallet | SCOPES:46 | documents.ts:1474-1503, 2330, 3004, 3272 | TRUE |
| 11 | `documents:share` / `transfer-custody` checked in originate; share-only key refused at gateway | SCOPES:47,49 | documents.ts:2528, 1854; proxy.ts:657 | TRUE |
| 12 | Share handler checks role-or-scope and tenant existence only; no owner/recipient/admin comparison (KS-1847) | RULES:87, matrix | documents.ts:2516-2570 | TRUE |
| 13 | Revoke owner-only, no admin bypass; 403 "Only the owner can revoke this document"; already revoked 400 | SCOPES:48, RULES:88, INV:2.3 | documents.ts:2728-2734 | TRUE; `documents:revoke` unread: TRUE (no `isAllowedByRoleOrScope` in revoke) |
| 14 | Read rule: owner/admin/recipient/creating connector, 404-cloaked; "admin" = system_admin, SYSTEM_ADMIN, super_admin only; skipped when no recorded owner | RULES:86, INV:2.3 | documents.ts:1102,1150-1160 | TRUE |
| 15 | List fan-in: admin unfiltered, else owner/rights-holder/recipient; no creating-connector arm | INV:2.3 | documents.ts:300-327 | TRUE |
| 16 | `/api/certifications` routes (issue, list, id, revoke, verify, share, recertify, lineage, evidence-bundle); no /sign | SCOPES:58 | certifications.ts route list | TRUE |
| 17 | `/issue`: DOCUMENT_WRITE_ROLES or `certifications:write`, else 403 with the quoted text | SCOPES:57, RULES matrix | certifications.ts:246-247 | TRUE |
| 18 | Certification revoke checks issuer identity, not a scope; share has no scope/role check | SCOPES:59-60 | certifications.ts:1116-1117, 1233-1260 | TRUE |
| 19 | `certifications:write` also admits `POST /api/users/stub` | SCOPES:57 | auth/src/routes/users.ts:247-259 | TRUE but INCOMPLETE: stub is also admitted by `users:read`, `users:create`, `users:*`, `*`, and `documents:transfer-custody` (KS-1653); the `users:read` and `documents:transfer-custody` rows say nothing of it (Minor M1) |
| 20 | Register-connector refuses any `scopes` field with 403 for a provisioning (connector) key; fixed nine-scope set | SCOPES:64, RULES:52 | platform.ts:605-609, 651-654 | TRUE (a platform admin may still pass `scopes`; doc scopes the sentence to the provisioning key) |
| 21 | Provisioning mint refuses `*`, `<resource>:*`, `organizations:register` | SCOPES:64, RULES:53 | security/src/provisioningPolicy.ts:52,63 | TRUE |
| 22 | Key-admin roles SYSTEM_ADMIN, SUPER_ADMIN, ORG_ADMIN, ISSUER_ADMIN, ADMIN; originate admin api-keys only SYSTEM_ADMIN/ORG_ADMIN; both default `['read']` | SCOPES:88,106,136 | security/src/index.ts:1099,665; originate adminConfig.ts:45,996-998 | TRUE |
| 23 | Issuer-certs gates: admin list passes all; write implies read; rotate needs write AND revoke; `issuer-certs:*`/`*` honoured inline | SCOPES:73-75,101 | auth/src/routes/issuerCerts.ts:63,74-120,539-545 | TRUE |
| 24 | OAuth: nine-member `AVAILABLE_SCOPES`; registration closed enum (400 for `*`); `admin:*` platform-admin only; default scopes; wildcard allow-list grants nothing, 400 `invalid_scope` | SCOPES:89,110 | auth/src/services/oauth.ts:57-67,96,353; routes/oauth.ts:1147-1200,415-440 | TRUE |
| 25 | OAuth token carries consenting user's role and `authMethod:'oauth'`, so downstream role checks can pass it | SCOPES:19, RULES:R1 | auth/src/services/jwt.ts:205,229 | TRUE |
| 26 | API-key validation cache: 60 s valid / 30 s rejected, not invalidated on revoke (KS-1847) | RULES:108 | api-gateway/src/middleware/auth.ts:299,308,320 | TRUE |
| 27 | `onBehalfOf` rules: connector-only 400 text; `null` 400; cross-org 403; org-less key/ no-user -> verbatim; accepted on create, version, share, transfer, revoke, certifications/issue; lifecycle ignores | RULES:R3 | originate/src/services/provenance.ts:96-106,112-160; documents.ts:399,1872,2349,2547,2751,2860-2866; certifications.ts:432 | TRUE (Minor: an org-less *user* also resolves verbatim with no 403; doc says only "no K user") |
| 28 | MCP client: non-`sk_` key goes out as Bearer; nine tools in four modules; no `onBehalfOf` anywhere | RULES:R1, register, G-2 | mcp-server/src/api-client.ts:23-29; tools/{hash,info,register,verify}.ts; grep onBehalfOf in mcp-server/src = 0 | TRUE |
| 29 | `charge_events` only for certification operations; create/version/share/revoke/transfer/anchor write none | RULES:R7 | originate/src/services/chargeEvents.ts called from routes/certifications.ts only (documents.ts has no call) | TRUE |
| 30 | R7: connector provenance rows for create, lifecycle, flat anchor; `POST /documents/{id}/anchor` writes none | RULES:R7 | documents.ts:776,2447,2888; anchoring/src/index.ts:556-563; anchor handler 1460-1700 has no record call | TRUE |
| 31 | Two inline "admin" gates admit `OWNER` (billing credits, NFT platform-fee) | INV:2.1 | billing/src/routes/billing.ts:621; nft-certificate/src/routes/nft.routes.ts:704 | TRUE (marked UNDECIDED, KS-1850) |
| 32 | `SUPER_ADMIN` "31 code sites in 18 files, counted by git grep on 2026-10-30" | INV:1.3 | `git grep -w SUPER_ADMIN`, non-md non-test: 60 lines/29 files under Blockchain/Dev; 42/21 under services/; 47/23 under services+packages | OVERSTATED as a reproducible number: I cannot reproduce 31/18 with any reasonable filter (Note N1) |
| 33 | R2 deny-by-default: "An operation with no scope in the vocabulary is not available to agents at all. Admin, user-management, platform and key-rotation routes have no document-op scopes - agents cannot reach them, by construction. Two doors are open to a connector by design" | RULES:43-48 | see F1 | FALSE as stated (Major F1) |
| 34 | Matrix: "Everything not in this table is not an agent operation (R2 deny-by-default)" | RULES:136 | documents.ts:1225-1345 | FALSE (Major F2) |
| 35 | Inventory 2.1 five ungated admin/reviewer routes | INV:2.1 | governance/src/routes/governance.ts:492 (no gate), staking/src/routes/stake.ts:448; kyc review and wallet sessions not read | governance, staking TRUE; kyc review, delegations, wallet sessions UNVERIFIABLE (not read) |

(Counts: rows 1-31 TRUE, 32 OVERSTATED, 33 and 34 FALSE, 35 split.)

## Findings

### Major (fix before merge)

**F1. R2's "agents cannot reach admin, user-management, platform and key-rotation routes, by construction; two doors open by design" is false, and the PR's own SCOPES.md contradicts it.** (RULES:43-48)
Reachable by a connector today, per the same PR: (i) the security service's `POST /api/keys` (key minting) for a connector holding `organizations:register`, within the provisioning limits (SCOPES:64,136; security/src/index.ts, provisioningPolicy.ts) - a third door, and a key-minting one; (ii) `POST /api/users/stub` (creates an INVITED user row) for any connector key holding `certifications:write` (every Platform S org key), `users:read`, `documents:transfer-custody` or `*` (auth/src/routes/users.ts:247-259); the gateway authenticates `/api/users` with no scope (proxy.ts:550-552); (iii) `/api/issuer-certs` (upload a certificate and private key, sign, revoke, rotate) for `issuer-certs:*` scopes (issuerCerts.ts:74-120; proxy.ts:558-560, auth only at gateway); (iv) `/api/webhooks` for `webhooks:manage`. `/api/admin/` is the one family that is role-gated against connectors (proxy.ts:1252-1265). Fix: replace "by construction ... two doors" with the actual list, or mark the intent UNDECIDED and ticket it. This is a place where intended (deny by default, R2's whole premise) differs from current and is not marked.

**F2. The operation matrix's closing line "Everything not in this table is not an agent operation (R2 deny-by-default)" is false for at least two document routes, and the code gap is unrecorded.** (RULES:136)
`POST /api/documents/{id}/sign/request` and `POST /api/documents/{id}/sign` (originate/src/routes/documents.ts:1225-1345) have no role check, no scope check and no per-document access check; the router only does `authenticate()` (documents.ts:175). The gateway admits `documents:read` or `documents:write` on every non-create method (proxy.ts:657), so a key holding only `documents:read` reaches them. `/sign` pushes a signature onto the document and sets `status: 'signed'` (documents.ts:1320-1330) and accepts any signature string starting `mock_signature_` or longer than 50 characters (documents.ts:1312). Neither route appears in any of the three docs (grep: no match for `/sign/request` or `{id}/sign` as a route), and the matrix also omits `sign-cert` / `sign-wallet`, which SCOPES.md does gate. Not probed on a running stack (read from code). Fix: add both routes to SCOPES.md/matrix as "no gate" with a KS finding (same class as KS-1847/1833), and drop or qualify the closing sentence. Also worth its own product ticket; this gate files none.

### Minor

- **M1. `POST /api/users/stub` admission is under-documented.** SCOPES `users:read` row (D:66) and `documents:transfer-custody` row (D:49) omit that those scopes admit the stub route; only `certifications:write` (D:57) and `users:create` (D:85) mention it. A test author deriving "what does users:read allow" gets an incomplete answer. (users.ts:247-259)
- **M2. Gateway create handler gates sk_ keys only.** An OAuth token has no `connectorMeta` (auth.ts:490), so the inline create check (verification.ts:746-751) does not run for it and `requireScope` is not mounted on `POST /api/documents` (verification.ts:669). SCOPES:19 says OAuth callers are checked by `requireScope` "on the same mounts"; for create they are not checked at the gateway at all, only in originate. The table row says "an API-key caller", which is right; D:19 reads as broader than the code. Cross-referencing sentence needed.
- **M3. R3 resolution wording:** "no K user -> verbatim" omits that an org-less existing user is also verbatim without a 403 (provenance.ts:154-155).
- **M4. Preamble honesty:** SCOPES.md preamble lists three sentences "not re-checked"; the RLS sentence, AES-256-GCM/AAD sentence and the `subjects:erase` dates are therefore not covered by this gate either. I did not verify them.

### Notes

- **N1. Counts that are hard to reproduce:** "31 code sites in 18 files" for `SUPER_ADMIN` (INV:1.3) - I get 47/23 (services+packages, non-test, non-md), 60/29 (all of Blockchain/Dev). The doc itself argues numbers a reader cannot derive drift; give the exact `git grep` command or drop the number. Seed-persona counts (17/15) were not recounted.
- **N2. Instrument caution:** several of my first-pass greps were case-sensitive multi-word patterns; claims above were each confirmed by reading the cited lines, not by a zero count.
- **N3. Positives worth keeping:** every UNDECIDED passage I checked (`documents:revoke`, `certifications:share/revoke`, `anchors:read`, out-of-vocabulary scopes, `<resource>:*` at the gateway, `*` mint rights, `validateScopes`, OWNER on two admin routes, credential revoke) matches a real code-vs-intent gap, and the code behaviour stated beside each is TRUE. Citations are by path + function, so they will not drift.

## What I did NOT test

- No running stack: no request was sent anywhere; every behaviour claim is read from code at the PR head, not probed. Gateway-plus-originate composition (e.g. that the sign routes are reachable end to end by a `documents:read` key) is inferred from the middleware chain, not exercised.
- Not checked: deployment state, Linear ticket state/priority (KS-1845/1846/1847/1850/1851 existence and content), dates and rulings quoted from tickets (KS-843, KS-1116, KS-1570, KS-1157, KS-566 dates), `S-K-OWNERSHIP-CONTRACT.md` content, the RLS sentence, the AES-GCM/AAD sentence, seed counts, `x-tenant-override` raw read in `GET /api/admin/dashboard` beyond adminConfig.ts:597-605, KYC review/delegations/wallet-sessions ungated routes, Art.17 pseudonymisation of provenance, frontend claims (F-1, F-17), the diagram PNG, and the OpenAPI "not in published spec" statements beyond a count-zero grep for the batch/share/revoke certification paths.
- Of the ~210 behavioural statements in the three files I read about 35 against code (table). Weighting was roles/scopes/who-may-do-what as asked.
- Spark shadow not run (above).

## Instrument errors

- First cd attempts were refused by the workspace hook and a `$G` multi-word variable was refused by the zsh hook; re-run under `bash` with absolute paths, no result affected.
- `wc -l` of `docs/security/*.md` failed on the wrong base path (docs live under `Blockchain/Dev/docs/security`); re-read correctly.
- My path-existence script reports partial paths as "missing"; I resolved the four by hand (all exist). My identifier extractor yields 118 against the author's 145; heuristics differ, no disagreement on any identifier.
- The `SUPER_ADMIN` counts depend on my filter; I could not find one giving 31/18.
- The `ks566-connector-attribution.test.ts` not-found in originate (my guess of location) was a wrong assumption; it exists in anchoring.

Repo state: `repo` worktree `wt` left in place under the gate folder (nothing deleted). Remote head re-read at end: `63c149736a262c6fd4b7e85d4c8ff16c96faab11`.
