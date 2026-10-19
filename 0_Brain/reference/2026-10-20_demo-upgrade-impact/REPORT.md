# Demo-pk upgrade d75bfe2deb80 -> develop 11af03696c9b: impact on existing users and accounts
Produced 2026-10-20 ~10:45 AEDT by an Opus analysis sub-agent for Wednesday (code reading only, no box access). Saved here by Wednesday from the agent's returned text (the harness refused the sub-agent's own write). Appendix A (254 first-parent commits by service): APPENDIX_A_commits_by_service.md.

## BLUF
1. No existing data is deleted or rewritten. Migrations 049-054 only add tables, columns and triggers (plus one DROP NOT NULL). KS-1557's 055 only ADDS provenance rows. Token lifetimes and claims unchanged. KS-1407 (sign-out on password change) is NOT in develop.
2. What existing accounts lose: tenant-level ADMIN users can no longer mint or revoke organisation-bound API keys until a platform admin grants them a scope (the scope table, migration 049, starts empty). Non-platform admins cannot mint provisioning keys that name no organisation. Stored credentials and presentations open only for their creator (KS-1116), so demo's one older presentation becomes unreadable to everyone. Admins certify only documents they own or receive.
3. What Platform S sees: x-api-key calls behave as before. Certify is refused (403) on documents S did not create. Develop alone also refuses S's routine certify of a document's current version; C 31st's KS-1557 fix (#1654) plus migration 055 restores it for the 31 existing version-minted documents, but NOT for older documents S originated without onBehalfOf. Transfer-custody now succeeds where it answered 404/500 (and mints INVITED stub users for unknown holders). erase-connector goes from 404 to actually erasing.
4. One change to existing rows when auth starts: the demo-user seeder (KS-968) can SUSPEND the account holding admin@secuura.com, only if both seed rows exist and ADMIN_USER_PASSWORD is unset. UNMEASURED on demo.
5. Test first: S certify on a current version and on an older S-originated document; an ADMIN operator minting and revoking an org key in Admin Dashboard -> API Keys; sign-in as admin@secuura.com after auth boots; demo edge logs for S erase-connector retries BEFORE the deploy; re-run the 050/051 censuses.
6. UNMEASURED: live demo row counts and user role counts; Platform S's own code; the September images (demo-service, demo-overlay). The 31 / 1 / 0 figures are earlier seats' read-only measurements quoted in source or handover.

## Inputs
- Demo runs d75bfe2deb80 (Seat D 23rd HANDOVER §7, §12); demo-service (09-10) and demo-overlay (09-07) run older images: their delta starts earlier, UNMEASURED.
- develop 11af03696c9b (ls-remote); pin is an ancestor. Delta: 254 first-parent commits, 969 files, +103,892/-23,563; 105 tooling/tests/docs only.
- KS-1557 fix NOT merged (#1654, branch db9bca740df0, merges cleanly onto develop). KS-1407 NOT merged (#1655).

## Migrations (each read in full; demo highest applied = 048)
- 049 admin_organisation_scopes: new table, FORCE RLS, starts EMPTY (the §2 behaviour change).
- 050/051 (KS-1612): SECURITY DEFINER triggers on documents; refuse unless superuser/BYPASSRLS; RAISE on existing violations. Demo census 0/0 (H§7): re-run on deploy day.
- 052: custody_events.transferred_by_id DROP NOT NULL.
- 053 svc_m365_oauth_states: new table (also created by api-gateway startup-migrations).
- 054: nullable created_by_* on vc_credentials_store / vc_presentations_store, no backfill.
- 055 (#1654 only): INSERT of action_provenance 'create:connector' rows, marker external_ref='ks1557-055-backfill', reversible; 31/31 on demo per its header. Children whose parent has NO version:* row are neither inserted nor reported (inner join): they stay 403.
- No new start-up refusal found. GATEWAY_VOUCH_SECRET now fail-closed when unset (demo already armed).

## Existing users and accounts
- KS-1116: GET credentials/:id and presentations/:id 404 unless creator (same userId AND tenantId); owner-less rows readable only by ORG_ADMIN/SYSTEM_ADMIN of the row's tenant, and that column is NULL on every old row, so no old row is readable. Not bound: list, by-hash, public revocation lookup, POST revoke (credentials.ts:286-297).
- API keys (KS-1570/1584/1533/1594/1564): ADMIN needs an admin scope to mint/revoke org-bound keys; every existing ADMIN starts unscoped; only platform-only PUT /api/keys/admin-scopes/:userId grants one. Admin Dashboard now sends a real org id. Non-platform callers: 403 on org-less provisioning keys, foreign org ids, connectorId without platform/provisioner role. No key rewritten or revoked. KS-1553: padded/upper-case keys listable again.
- Certify (KS-1538/1557): callerMayCertifyDocument now applies on both paths (at the pin neither checked). ISSUER_ADMIN/ORG_ADMIN not creator/recipient: 201 -> 403; upper-case SUPER_ADMIN on others' docs 201 -> 403; unknown documentId 201 -> 403. Verify presentation: certifications without data.contentHash = parent hash no longer shown certified; erased holders / transferred custody stop counting; certifierOrganizationId null. Count of affected demo certifications UNMEASURED.
- Auth: no token lifetime/claim change. Connector JWT as Bearer -> 401; x-api-key + connector Bearer -> 401. KS-968 seeder may SUSPEND admin@secuura.com (UNMEASURED). KS-1009 wallet status minimal. KS-806 wallet emails hashed for new accounts; client-supplied @wallet.local refused. MFA/verification edges fail closed. Rate-limit buckets renamed for non-key machine principals (counters reset); new S connectors minted at 3,000/h.
- m365/Teams: demo has 0 rows and no ENTRA env: not exercisable.

## Platform S status-code changes
| Call | Pin | develop | develop + #1654/055 |
|---|---|---|---|
| Lineage certify, S doc originated WITH onBehalfOf | 201 | 201 | 201 |
| Certify from a /version-minted document | 201 | 403 | 201 (new + the 31 backfilled) |
| Certify from an S doc originated WITHOUT onBehalfOf, pre-upgrade | 201 | 403 | still 403 |
| Certify a doc S did not create | 201 | 403 | 403 |
| Legacy certify unknown/foreign doc | 201 | 403 | 403 |
Other: untyped create without DOCUMENT in the connector allow-list 201 -> 403; anchor write naming another tenant's K document 202 -> 403; registering a document id an anchor already holds 201 -> 409; /api/connector/info failures 200 [] -> 503/403; public POST /documents/:id/verify retired; audit-log limit>200 -> 400; mock-TSA timestamps verified:false; several malformed inputs 500 -> 400. The other way: transfer-custody 500/404 -> success (mints INVITED stub users); erase-connector 404 -> live and destructive (blanks titles/descriptions, renames the organisation, revokes the key; S retries without bound); audit export 401 -> works.

## Deploy caveats
- KS-695: erase-connector should reach demo-pk only after uat-ps has it; check demo edge logs for erase-connector retries first.
- :latest != running on 5 containers; builds need --profile phase2 (H§4-5).
- Without #1654, develop breaks S's routine certify (403 + flat-anchor fallback).

## UNMEASURED
Every live demo count (users by role, org-bound provisioning keys, S documents without onBehalfOf, certifications without the parent hash, the KS-968 state, mock-TSA usage, anchors since the 050/051 census); Platform S's code; the September images; no tests or builds were run.
