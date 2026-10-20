# PLAN — KS-1695: two same-tenant read gaps in `services/originate` (design only; nothing built, nothing pushed)

Planner seat for Wednesday, row C3 (auth read-path design). 2026-10-20.
Inputs read whole: `PLAN_BRIEF.md`, `KS-1695.md` (its last line: **comments fetched: 0**, first:50; `fetch.err` is 0 bytes), gate BX1 `verdict.md`, Seat C 30th's `HANDOVER.md`, `boot/plan-body.txt`, `mail/pr2-body.md`, `mail/ks1116-comment.md`, and the KS-1116 card record in `0_Brain/dashboard/data/decisions.json:41393-41437`.

**Source.** Every code citation is read at live develop **`7e3b9362e08b`** (`7e3b9362e08b1b5b2c418f43e05c9bd0616f896e`, "Refs KS-1682 … (#1662)", 2026-10-20 12:41 +1100) with `git -C …/local-model/spark/cache/src show <sha>:<path>`. Nothing was checked out or fetched. In that tree the service lives under **`Blockchain/Dev/services/`**. A citation written `S:originate/src/x.ts:N` means `7e3b9362e08b:Blockchain/Dev/services/originate/src/x.ts:N`.
Correction to the brief: `principalId.ts` is at `originate/src/utils/principalId.ts`. `originate/src/principalId.ts` does not exist at this SHA (`git show` rc 128).

---

## BLUF

1. **Gap 1 is the wider one and can be fixed without a new ruling or a migration.** `GET /api/certifications/:id` returns the row with no access check (`S:originate/src/routes/certifications.ts:956-994`). The certification record already holds the creating principal, **including a connector's raw id** (`S:originate/src/repositories/certificationRepo.ts:75`, `:80` fall back to `certification_metadata.issuerId` / `.holderId`, written raw at `:215`, `:218`). So a check that admits "issuer, holder or platform admin" keeps the issuing connector at 200 and needs **no provenance row**. That is the smallest PR.
2. **Gap 2 cannot be closed without stranding Platform S unless someone decides who may read an owner-less document.** For a bare-connector document **no record of the creator exists anywhere**. The code says so itself (`S:originate/src/utils/principalId.ts:19-22`), the insert stores no actor (`S:originate/src/repositories/documentRepo.ts:373-375`, `:361-367`), and the provenance row is written only with `onBehalfOf` (`S:originate/src/routes/documents.ts:758-768`). Any fail-closed cloak therefore needs a rule for who replaces the missing owner. **That is Kam's decision.**
3. **KS-1116's ruling does not extend automatically.** It was made for vc-issuer presentations and credentials, where the rows carry no organisation and it reached **0 existing rows**. On originate every document row has a tenant, and tenants hold several organisations (BX1's reader **a2** is one). The same words would let **an administrator of a different organisation in the same tenant** read the row. That consequence was not in front of Kam on 20 Oct, so this needs its own card (draft in §6).
4. Not in KS-1695, but the same class, read today: `GET /api/certifications/:id/lineage` (`S:originate/src/routes/certifications.ts:1416-1481`) and `GET /:id/evidence-bundle` (`:1497-1533`) do the same unbound lookup. Lineage also returns **share recipients' emails and names** (`:1459-1466`), and evidence-bundle **writes a billing charge event** for whoever reads it (`:1515-1516`). Neither is measured.

---

## 1. Audience table — copied from gate BX1's measured rows (via KS-1695.md, which reproduces the verdict's N1 and N2)

**a** = same-tenant `ISSUER_ADMIN`, same organisation · **a2** = same-tenant `ISSUER_ADMIN`, **another** organisation · **b** = another tenant · **c** = the issuing connector.

| row | tree | endpoint | a | a2 | b | c |
| -- | -- | -- | -- | -- | -- | -- |
| connector certification, no holder | landing | `GET /api/documents/:id` | **200** | **200** | 404 | **200** |
| **bare-connector** `POST /api/documents` (owner NULL, issuer NULL) | **develop AND landing** | `GET /api/documents/:id` | **200** | **200** | 404 | **200** |
| human-issued certification, no holder (owner = issuer = a UUID) | both | `GET /api/documents/:id` | 404 | 404 | 404 | 404 |
| **human-issued certification** | **develop AND landing** | `GET /api/certifications/:id` | **200** | **200** | 404 | — |
| connector certification, no holder | landing | `GET /api/certifications/:id` | **200** | **200** | 404 | **200** |

- Positive control (BX1): the human certification is 404 on the documents path, so the cloak works when an owner exists.
- "Landing" for the holder-less connector certification is now develop: `3cc46ae41fed` ("Refs KS-1659: fold the holder principal…") is an ancestor of `7e3b9362e08b` (`git merge-base --is-ancestor`, rc 0). That row type exists on develop today.
- **What "same tenant, any organisation" means:** both 200 columns are **a and a2**. Do not shorten this to "the same organisation". The ledger records that exact narrowing once already today (`_ledger.md:27`).
- **Measured readers were `ISSUER_ADMIN` only.** BX1 states the audience as "all roles". That is an inference from source, and I re-read both lines that support it. `documents.ts:1124` has no role term except `!isAdmin`, and `isAdmin` is only `system_admin` / `SYSTEM_ADMIN` / `super_admin` (`S:originate/src/routes/documents.ts:1076`). `certifications.ts:956-994` has no role term at all. **A plain end-user (`OWNER`) reader was not measured.**
- **Gateway: does not narrow it for humans, from source only.** The gateway mounts both paths behind `requireScope(...)` (`S:api-gateway/src/routes/proxy.ts:635-647`), but `requireScope` passes every `jwt` or `email` principal without a scope check (`S:api-gateway/src/middleware/scopes.ts:33-36`). I believe the gateway therefore does not narrow the human audience. **Not measured through a real gateway** (BX1 NOT RUN).

## 2. What the code does today (each line re-read at `7e3b9362e08b`)

**Gap 1: `GET /api/certifications/:id`**
- `S:originate/src/routes/certifications.ts:966-968`: `getCertification(id, tenantId)`. `:980-994` returns issuer, holder, data, privacySettings, blockchain and contentHash. No caller term at all.
- `S:originate/src/repositories/certificationRepo.ts:166-171`: `SELECT * FROM documents WHERE id = $1::uuid AND tenant_id = $2::uuid`. **No `document_type` filter.** I believe this route serves **any** row in the tenant's `documents` table by primary-key UUID, plain documents included, with `data` = `{}` for a plain document (`:84`). I have not measured a plain document through this path. If it holds, gap 1 also lets anyone in the tenant read the contentHash, blockchain and owner of documents that the documents GET cloaks.
- **A read that writes:** `certifications.ts:975-978`. If the row is expired, it calls `saveCertification(...)` for **whoever** is reading. Any check must come **before** this write.
- Comparators already in the file: the list (`:906`, `:921-924`) admits platform admins plus `holder.id === userId || issuer.id === userId`. Revoke (`:1046`) admits the issuer only.
- **The connector is identifiable on this route.** On a certify call, `holderId = req.body.holderId || issuer.id` (`:335`), and the record is built with `holder: { id: holderId }` (`:483-484`). The repo writes the raw principals into `certification_metadata` (`certificationRepo.ts:215`, `:218`) while the UUID columns fold to NULL (`:232`, `:250-251`). On read, `issuer.id` and `holder.id` fall back to that metadata (`:75`, `:80`). So a holder-less connector certification reads back with `issuer.id = holder.id = 'connector:…'`.

**Gap 2: the documents cloak**
- `S:originate/src/repositories/documentRepo.ts:176`: `id: row.owner_user_id || row.issuer_user_id || ''`. Unlike the certification mapper, there is **no metadata fallback**.
- `S:originate/src/routes/documents.ts:1124`: `if (userId && document.owner?.id && … )`. An empty owner makes the conjunction false, so the cloak never runs. `:1130` admits the creating connector only through `wasCreatedByConnector`.
- `S:originate/src/services/provenance.ts:285-296`: that function needs an `action_provenance` row with `action = 'create'` and a matching `connector_id`, and it returns false on any error.
- `S:originate/src/routes/documents.ts:758-768`: the create provenance row is written **only `if (onBehalfOf)`**. BX1 measured 0 such rows against 12 documents.
- `S:originate/src/repositories/documentRepo.ts:373-375`: the owner is either the `onBehalfOf` override or the caller id if it is a UUID, otherwise NULL. Metadata (`:361-367`) holds data, wallet, signatures, blockchain and `sIdentity`. **The connector's id is not recorded.**
- **A third owner-less population that BX1 did not name:** `documentRepo.ts:497-502`. If a **human's** UUID trips a foreign key ("Owner user not in tenant DB"), the insert is retried with owner NULL. The creator then survives only in a log line. Count unmeasured.
- `issuer_organization_id` is written (`documentRepo.ts:447`, `:473`), but only when the caller claimed an organisation and it bound (`S:originate/src/routes/documents.ts:558`). `fromDbRow` (`documentRepo.ts:164-196`) **does not map it**, so the route cannot read it today. An "organisation matches the row's" admit needs the mapper extended, and it still finds NULL on unclaimed rows.
- Tenant source for any tenant-admin arm: `getReqTenantId` falls back to a fixed default tenant when `req.tenantId` is unset (`S:originate/src/routes/documents.ts:250`, `:259-262`). Any "tenant on the token" check must read `req.user.tenantId` and fail closed when it is absent, **never** use the defaulted value. This is the same lesson as C 30th's (`plan-body.txt:87-90`).

## 3. Callers (who could legitimately break)

| caller | route | file:line | effect of a bound |
|---|---|---|---|
| **Platform S connector** | both | not readable: `Secuura/platform-s` is 404 to the project token (C 30th HANDOVER §5) | **UNMEASURED.** Gap 1 fix: the issuing connector keeps 200 (it is `issuer.id`). A *different* S key reading a cert it did not issue would go to 404; whether S does that is unknown. Gap 2: see options. |
| Human UI (issuer app) | `GET /certifications/:id` | `S:../../frontend/issuer/src/services/api.ts:470-473` defines `certificationApi.get` | **0 call sites** in `frontend/`. Positive control: the same search finds `certificationApi.getLineage` at `frontend/issuer/src/components/lineage/LineageViewer.tsx:108` and `getEvidenceBundle` at `:353`. So the UI does use the sibling routes (§BLUF 4). |
| Human UI | `GET /documents/:id` | list filter `S:originate/src/routes/documents.ts:319-330` | Owner-less rows never appear in a human's list (`:321`), so a human reaches them only by a known id. No UI flow found that depends on reading another person's owner-less document. Not exhaustively traced. |
| Gateway | `GET /documents/:id` as an existence check | `S:api-gateway/src/routes/verification.ts:183-224`, used by the mock `POST /api/certifications/:id/verify` at `:332-337` (header: "for E2E tests", `:327-328`) | Forwards the **caller's** bearer. Under a fail-closed cloak an owner-less doc answers "not found" to a non-owner verifier, exactly as an owned doc already does. |
| nft-certificate | `GET /certifications/:id` | `S:nft-certificate/src/services/minting.service.ts:148`, `:173`. `fetch` with **no Authorization header** | originate's `authenticate()` returns 401 on a missing bearer (`S:originate/src/middleware/auth.ts:87-89`, router-wide at `certifications.ts:65`). I believe this caller already fails today, so a bound changes nothing for it. Not measured. |
| vc-issuer | either | `git grep -i -E "originate\|/api/documents/"` over `vc-issuer/src` (non-test): **0 hits**. Controls: 13 vc-issuer files match `express`; 67 gateway files match `originate` | Not a caller. |
| SDK | `GET /api/certifications/:id` | `S:../../sdk/javascript/src/modules/certifications.ts:122` | Public client surface. A non-party SDK user goes to 404. |
| E2E suite | `GET /api/certifications/:id` as the **verifier after an ownership transfer** | `S:../../tests/e2e/tests/integration/full-certification-flow.api.spec.ts:178-183` (transfer at `:122-170`) | **Could go red under an issuer/holder-only check.** I have not read the transfer service, so whether an accepted transfer rewrites `owner_user_id` is unread. Whether this suite runs in any gate is unmeasured. |

(`S:../../` = `7e3b9362e08b:Blockchain/Dev/`.)

## 4. Remedy options

### Gap 1: `GET /api/certifications/:id`

**1-A (recommended): bind the route on the record.** After `getCertification` and **before** the expiry write at `:975`, return the existing 404 body **byte-identical** to an unknown id (`:971`) unless one of these holds:
- the role is a platform admin (the same set as `:906`);
- the caller's `userId` is non-empty and `=== certification.issuer.id`;
- the caller's `userId` is non-empty and `=== certification.holder.id`.

| | |
|---|---|
| **Blocks** | a and a2 on human certifications (BX1 row 4) and on holder-less connector certifications (row 5). Any same-tenant reader of a plain document's pkey through this path, because a bare-connector document has `issuer.id = holder.id = ''` (`certificationRepo.ts:75`, `:80`) and an empty id never matches. |
| **Keeps** | b stays 404. **c stays 200** (it is `issuer.id` via metadata). Issuer, holder and platform admins keep access. |
| **Who loses access** | A normal user, or an `ISSUER_ADMIN` / `ORG_ADMIN`, of any organisation in the tenant who is neither the issuer nor the holder. This matches what the list already shows them (`:921-924`). |
| **Legitimately breaks** | Possibly the post-transfer verifier (E2E above). Possibly a Platform S key other than the issuer (unmeasured). Share recipients reading by id (unmeasured: whether shares expect `/:id` access; recipients are in `share_records`, `getSharesByCertification`). |
| **Migration / backfill** | **None.** No column or data change. |
| **KS-1685 caveat** | Every API key without a connector id is the single principal `connector:api-key` in its tenant (C 30th's KS-1685), so "issuer matches" admits **all** such keys in that tenant to certs any one of them issued. 1-A is still strictly narrower than today. |

**1-B: copy the documents predicate literally** (owner, platform admin, `recipientEmail`, `wasCreatedByConnector`). This inherits gap 2's empty-owner hole and the provenance dependency, and certifications carry no `recipientEmail` in their `data` shape. **Not recommended.**

**1-C: also bind `/:id/lineage` and `/:id/evidence-bundle` in the same PR with the same helper.** These are not in KS-1695's text and not measured. Lineage leaks share-recipient emails (`:1459-1466`); evidence-bundle bills a charge to any reader (`:1515-1516`). The human UI calls both (LineageViewer `:108`, `:353`), so the issuer must keep access, which 1-A's rule does. C 30th's precedent is to widen to the sibling reads rather than ship "a bound that the next route steps around" (`plan-body.txt:253-256`). Recommended as **the same PR if Wednesday accepts the scope**, otherwise one follow-up ticket.

### Gap 2: the documents cloak on an empty owner (all need Kam's audience decision except 2-E)

| option | edit | blocks | who loses | breaks | backfill |
|---|---|---|---|---|---|
| **2-A: fail closed** (drop `document.owner?.id &&`, `documents.ts:1124`) | 1 line | a, a2 on both owner-less row types | everyone except platform admins and recipients, **including c** | **Platform S loses its own bare documents and holder-less certifications** (BX1 N4; `:1125-1129` says S drives the lifecycle through that id) | impossible for bare rows: no creator recorded |
| **2-B: KS-1116 shape plus connector**: owner-less readable by platform admins, plus `ORG_ADMIN`/`SYSTEM_ADMIN` whose **token** tenant equals the lookup tenant, plus `role === 'connector'` in that tenant | about 10 lines | a and a2 when they are not tenant admins (BX1's a and a2 were `ISSUER_ADMIN`, so both go to 404) | normal users and issuer-admins of every organisation | **an `ORG_ADMIN` of another organisation in the tenant still reads it**; any connector key in the tenant (not only the creator) still reads it | none needed; reaches **all** existing owner-less rows, unlike vc-issuer's 0 |
| **2-C: connector-only**: platform admins, plus `role === 'connector'` in the tenant | about 6 lines | all human non-admins, incl. tenant admins | as 2-B, plus tenant admins | another org's connector key still reads; c keeps 200 | none |
| **2-D: record the creator going forward** (write a `create` provenance row for every bare connector create and certify, then 2-A) | write path plus read | as 2-A for **new** rows | as 2-A | **existing** bare rows strand c unless combined with 2-B or 2-C for legacy rows | not possible for legacy bare rows; connector certs could be backfilled from `certification_metadata.issuerId` |
| **2-E: no change** | — | nothing | nobody | nothing | — |

Two narrower variants, both noted and not recommended as the first move:
- **For connector certifications only**, give `documentRepo.ts:176` the same metadata fallback as `certificationRepo.ts:75`. The cloak would then run with owner = the connector principal: a and a2 → 404, c → 200, no provenance needed. But it changes `DocumentRecord.owner.id` for every downstream reader (list `:321`, `:2016`, `:2631`), so it needs its own read-through. It does nothing for bare documents.
- **Org-matched connector** (admit a connector whose `organizationId` equals the row's `issuer_organization_id`): `fromDbRow` must map the column first, and unclaimed rows hold NULL (`documents.ts:558`). It cannot reach legacy rows reliably.

**Counts of existing owner-less rows on demo and kintsugi: UNMEASURED.** No report I found holds them. The only figures in hand are C 30th's control totals for `documents` (207 demo, 31 kintsugi, read-only, 2026-10-20), and they are totals, not the owner-less subset. The measurement to take (read-only, by the D lane): `SELECT COUNT(*) FILTER (WHERE owner_user_id IS NULL AND issuer_user_id IS NULL), COUNT(*) FROM documents GROUP BY tenant_id`, split by `certification_metadata ? 'issuerId'`, with the documents total as the in-statement control.

## 5. Recommendation

**PR 1 (smallest, closes gap 1, tier 1, needs no new ruling): 1-A.** It applies the rule the certification list already uses (`certifications.ts:921-924`) to the by-id read. Ideally it includes 1-C's two siblings with the same helper.

| | |
|---|---|
| Files | `routes/certifications.ts` plus one new test file |
| Cells that go red on develop | a → 404 and a2 → 404 on a human cert. a → 404 on a holder-less connector cert. Foreign-id 404 **byte-identical** to unknown-id 404. A plain owner-less document's pkey → 404 for a. **No expiry write for a refused reader** (an expired foreign cert: assert no update and no `certification_events` row). |
| Controls that must stay green | issuer 200, holder 200, platform admin 200, **c 200 on its own holder-less cert**, b 404 |
| Mutants | drop the holder arm; drop the non-empty guard (`'' === ''`); move the check after the expiry write; widen the role set to `ORG_ADMIN` |
| Before READY | Run, or at least read, the E2E transfer cell. Ask Platform S (Kam or Stuart; our token cannot see S) whether S reads certifications by id with a key other than the issuer. That is the same open question as KS-1683. |

**Then gap 2, after Kam's card.** It follows the rule he picks. My recommendation to him is **2-B without the "any connector" breadth where avoidable**: tenant administrators of the row's tenant plus connectors, combined with 2-D for new rows so the creator is recorded from now on. The connector admit for legacy rows stays until the owner-less count is measured and S confirms which keys read what.

**KS-1116 extension: needs its own decision.** The ruling's words ("tenant administrators, ORG_ADMIN / SYSTEM_ADMIN with a tenant on the token") would build here, but its consequence differs:
- On vc-issuer it reached 0 rows and the rows carried no organisation.
- On originate it reaches every owner-less row, and it admits an administrator of *another organisation* in the tenant (an a2 with `ORG_ADMIN`).
- It is also silent on the connector, which here is the creator.

A remedy matching it would inherit his authority only for the human-admin half; the connector half is new.

## 6. Card draft for Kam (Wednesday posts; I do not)

**Title:** Records with no named owner: who in the tenant should be able to open them?

**BLUF:**
- Two gaps, both found by testing, neither new.
  - **(1)** Any signed-in user in a tenant, **in any organisation in that tenant**, can open any certification there by its id. That includes certifications the documents page already hides from them.
  - **(2)** Documents that Platform S's connector creates without naming a person have no recorded owner. Anyone in the tenant, any organisation, can open those too.
- We will fix (1) by applying the rule the certification list already uses (issuer, holder, platform admin). The issuing connector keeps access.
- (2) needs your word. Nothing records which connector created those documents, so "only the creator" cannot be built for them. Someone has to stand in for the missing owner.
- Your 20 Oct answer for presentations and credentials ("tenant administrators") is the nearest precedent. Here it would also let **an administrator of a different organisation in the same tenant** open them, which was not true there.
- How many such records exist on demo and kintsugi is **not yet counted**.

**Options:**
- **(a) Tenant administrators and Platform S's connectors (recommended).**
  - A normal user in another organisation can no longer open these records. Neither can an issuer-admin.
  - An organisation administrator anywhere in that tenant still can.
  - Platform S keeps working.
  - From now on we also record which connector created each record, so new ones can later be limited to their creator.
- **(b) Platform S's connectors only, plus platform administrators.**
  - No person in the tenant can open these records, administrators included, unless they are a platform administrator.
  - Platform S keeps working.
  - Another organisation's connector in the same tenant could still open them.
- **(c) Leave them as they are for now.**
  - Every signed-in user in the tenant, in every organisation, can still open these records.
  - Only the certification fix ships.
- **(d) Nobody except platform administrators.**
  - Tightest. **Platform S loses access to the documents it created and can no longer manage them.**

**Recommended:** (a).
**If you don't answer:** (c). The certification fix ships, because it applies a rule we already use. Owner-less records stay as they are, because tightening them without your word could cut off Platform S.

## 7. What I could not establish (unmeasured)

- Owner-less row counts per tenant on demo and kintsugi, and how they split between bare-connector rows, connector certifications and FK-fallback human rows (`documentRepo.ts:497-502`).
- Whether Platform S reads either route with a key other than the creating one. Our token cannot see S's repo.
- Any gateway or real-JWT behaviour. The gateway reading in §1 is source only.
- A plain end-user (`OWNER`) reader, `MULTI_TENANCY_ENABLED=true`, a recipient reader, and an `onBehalfOf` connector certification (all also BX1 NOT RUN).
- That `GET /api/certifications/:id` serves plain (non-certification) documents. I believe it does from `certificationRepo.ts:166-171`; I have not run it.
- Whether an accepted ownership transfer rewrites `owner_user_id` (transfer service unread), so whether the E2E verifier cell survives 1-A.
- Whether share recipients are expected to read `/:id`.
- Whether nft-certificate's tokenless fetch is live anywhere. I believe it 401s today.
- The `/:id/lineage` and `/:id/evidence-bundle` exposure. Source read only, not measured.
- How many connector keys share a tenant. This decides how wide "connectors in the tenant" is in options (a) and (b).
- No remedy was built, and no suite or red-proof was run.
