# KS-1814 / PR #1814: the four custody scenarios mapped onto the re-anchor predicate

Written 2026-10-30 for Wednesday. Read-only research: nothing was pushed, commented on or deployed. PR head `38de04f285b2` and develop `7152ac669d2d` were read by ls-remote at the start and again before writing, and were unchanged both times.

## BLUF

1. **Verdict: yes, with a follow-up.** #1814 only narrows access and fails closed. It refuses nobody who should keep access in scenarios 1, 2 and 4, and it closes a live hole that spends a fee.
2. **Scenario 3 (the company keeps the documents) is the gap.** A same-organisation ORG_ADMIN or ISSUER_ADMIN gets a 404. Kam already ruled the opposite for anchor *identity* (KS-1385 card (c): "Issuer, or anyone in the custodian's organisation"), and that rule ships in anchoring.
3. **The refusal can be bypassed today.** `POST /:id/transfer-custody` has no per-document check, so a refused same-tenant admin can transfer custody to itself and then re-anchor. The follow-up must cover that route too.
4. **Scenario 4 (central storage) has no data on K.** K is a hash-only registry with no custody or storage field. "Central" can only mean the platform-admin arm, which #1814 keeps.
5. **Lineage:** re-anchoring overwrites in place. Only `/version` (a new row with `parent_document_id`) creates lineage.

## The four scenarios

| Scenario | Modelled today? | #1814 outcome | Gap | Smallest fix |
|---|---|---|---|---|
| **1. The owner modifies a document; lineage is shown** | **Yes.** `/version`, `/sign-cert` and `/sign-wallet` each mint a new row with `parent_document_id` pointing at the source. Verify walks the chain both ways. | The child inherits `owner = source.owner`, so the original owner re-anchors it, as do a platform admin and the creating connector (`/version` children only). **Right for the owner.** | (i) A same-tenant non-owner that `/version` admits (KS-1688, open) mints a child it cannot anchor. This fails closed, but the two routes disagree. (ii) A connector cannot anchor a child it minted via `/sign-cert` or `/sign-wallet`, because no provenance is recorded for it (KS-1693). | Nothing in #1814. Follow-up: put the same predicate on `/version`'s source (KS-1688), and record provenance on sign-cert and sign-wallet (KS-1693). |
| **2. The owner keeps their own documents** | **Yes.** `documents.owner_user_id` (falling back to `issuer_user_id`); transfer-custody flips it and logs `custody_events`; revoke is owner-only. | The owner re-anchors, including an OWNER-role owner via its `documents:write` scope. **Right.** | Minor: an owner holding neither a write role nor `documents:write` (for example a VERIFIER who received custody) gets a 403 on its own document. | None needed to merge. If wanted later: let the owner arm run before the role gate. That is a policy change, not a fix. |
| **3. A company (organisation) keeps them** | **Partly.** The columns exist: `documents.issuer_organization_id`, `users.organization_id`, and `organizationId` on the JWT. But no document route checks an organisation, and the issuer org is NULL on most rows (see FOUND). S is person-owned today; org-owned documents are PS-690, still In Progress. | **ORG_ADMIN or ISSUER_ADMIN of the same organisation, not the owner: 404** (cells Q2 and Q3, which carry no organisation). The company keeps re-anchor only through S's creating connector key. | **GAP.** The company's own admin cannot re-anchor a K-native document of a member, and that is inconsistent with Kam's KS-1385 (c). Separately, the refusal can be bypassed through transfer-custody. | Add an **organisation arm**: role ∈ {ORG_ADMIN, ISSUER_ADMIN}, a non-empty token org, and that org equal to `issuer_organization_id` OR to the owner's `users.organization_id`. Read it with the same tenant-bound join anchoring uses; NULL never matches. Also add a per-document check to transfer-custody. **This is Kam's policy call (card below).** |
| **4. Stored centrally (platform custody)** | **No.** K stores hashes only, with no storage-location, custody-kind or custodian-org field. "Secuura-hosted versus organisation store" exists only on Platform S (PS-1075, PS-1391). | Platform admins (`system_admin`, `SYSTEM_ADMIN`, `super_admin`) and the creating connector. S's Secuura-hosted documents still anchor through S's connector key. **Right as far as K can tell.** | Upper-case `SUPER_ADMIN` is not an admin at the document check (Q12; tracked as KS-1701). Otherwise **the platform lacks the data to decide.** | None to merge. Catering for central custody needs a `documents.custody_kind` (person / organisation / platform) plus a named custodian principal, written at registration by S or K. Until then the admin arm is the only central actor. |

**Re-anchoring a modified document: overwrite, not lineage (measured from the code).**
- The anchor route never takes new bytes. It sends the row's stored `contentHash` (`documents.ts:1534` @38de04f2) and refuses any document that is already anchored (`:1506`). So modified bytes can never be re-anchored onto an existing id.
- A retry on a failed or absent anchor overwrites in place:
  - `updateDocument` *replaces* the `blockchain` blob, keeping only `threadToken` (`documentRepo.ts:579-582`).
  - Anchoring then upserts `ON CONFLICT (document_id, network) DO UPDATE` (`anchoring/src/index.ts:1462`; migration 031), which resets the same row (KS-1384).
- Lineage comes only from a modification, through `/version`:
  - It writes a new `documents` row with `parent_document_id` = the source, status `draft`, no anchor (`documents.ts:2414-2439`).
  - Anchoring that child writes a separate `anchor_store` row, because its `document_id` is new (031 header, lines 18-19).
- Kam's KS-1384 ruling (a), "one anchor per lifecycle event", would change the overwrite. It is not built.

## FOUND

All citations are at PR head `38de04f285b23eb5b5ea986c03c1adbfc2c0cabd` unless marked. At develop `7152ac669d2d`, `documentRepo.ts`, `documentWriteRoles.ts`, `anchorOverwriteGuard.ts` and `verification.ts` have identical blobs. Of the source files, only `documents.ts` differs between the two SHAs.

**The predicate.** `callerMayAnchorDocument` is at `documents.ts:1445-1453`. The route's checks run in this order:
- role or scope, 403: `:1474`;
- `getDocument`, 404: `:1480-1484`;
- per-document, 404: `:1489-1491`;
- revoked or deleted, 400: `:1498-1501`;
- the write with `preserveTerminalStatuses`: `:1585-1588`.

At develop the route is `documents.ts:1438-1571`, and its only state guard is `:1458`.

**Ownership (scenario 2).**
- `documents.owner_user_id`, `issuer_user_id` and `issuer_organization_id`: `migrations/001_initial-schema.sql:105-107`.
- The owner is mapped as `owner_user_id || issuer_user_id || ''`: `documentRepo.ts:176`.
- Transfer-custody flips `owner_user_id` inside one transaction with the `custody_events` insert: `documents.ts:2179-2211`. The table is created in migration `023`.
- Revoke is owner-only: `documents.ts:2728`.
- OWNER gets `documents:write`: `packages/shared/src/security/scopes.ts:287`; the reason is documented at `documentWriteRoles.ts:24-27`.

**Organisation (scenario 3).**
- The issuer org is written only when the create carries an organisation claim bound to the caller's org: `boundIssuerOrgId = claimedOrgId && callerOrgId ? callerOrgId : null` (`documents.ts:559`, passed at `:741`).
- `/version` (`:2439`), `/sign-cert` (`:3187`) and `/sign-wallet` (`:3381`) call `saveDocument` with no options, so every child gets `issuer_organization_id` NULL.
- `fromDbRow` does not map `issuer_organization_id` onto `DocumentRecord` (`documentRepo.ts:164-195`), so originate cannot see it today without a read change.
- `users.organization_id` is added at `001:531`. The JWT carries `organizationId` (`auth/src/services/jwt.ts:197`; originate `middleware/auth.ts:19`).
- `organization_members.role` is "never read for authorization" (`docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md` §1.6). KS-959 measured `organization_members` = 0 rows.
- KS-621 (Backlog): "Document reads are scoped by tenant and owner, never by organization".

**Kam's precedent for organisation-level custody.**
- `anchoring/src/anchorOverwriteGuard.ts:92-93` ships `CUSTODY_OPTION = 'c'`.
- `:203-221`: the issuer org, or the custodian's org, may overwrite the anchor's stored identity.
- `:262-275`: the custodian org comes from a tenant-bound LEFT JOIN of `documents.owner_user_id` to `users.organization_id`.
- Rulings:
  - card `secuura-ks1385-custodian-may-update-anchor-identity-1013` = **c** (2026-10-14);
  - card `secuura-ks1385-null-issuer-certifications-1015` = **b**: apply (c) to rows with no issuer too.

**The bypass of #1814's refusal (source reading, not executed).**
- Transfer-custody gates only on `isAllowedByRoleOrScope(req, ALLOWED_TRANSFER_CUSTODY_ROLES, 'documents:transfer-custody')` (`:1854`), where `ALLOWED_TRANSFER_CUSTODY_ROLES = DOCUMENT_WRITE_ROLES` (`:1833`), which contains ORG_ADMIN and ISSUER_ADMIN.
- It then reads the document by tenant (`:2101`) and flips the owner to `newHolderId` (`:2203-2209`). Between `:1840` and `:2269` there is no check of owner, issuer or creator.
- So a same-tenant ORG_ADMIN refused at `:1489` can name itself as `newHolderId`, become the owner, and pass `:1451`.
- The board search below surfaced no ticket for the missing per-document check on transfer-custody. The search is fuzzy, so that is not proof that none exists.

**Lineage (scenario 1).**
- `parent_document_id` is added in migration `021`. The insert resolves it tenant-scoped (`documentRepo.ts:450`, `:476`).
- `/version` mints the child: `documents.ts:2383-2439`, with `owner: source.owner` at `:2418`, `blockchain: undefined` at `:2434`, and the creating connector recorded at `:2447`.
- Only create (`:776`) and `/version` (`:2447`) call `recordConnectorProvenance(…, CONNECTOR_CREATE_ACTION)`. Sign-cert and sign-wallet do not (KS-1693).
- Verify walks the chain: ancestors at `verification.ts:947`, descendants as `newerVersions` at `:979`.
- Non-mutating events go to `document_lifecycle_events` (migration `037`).
- The legacy `document_versions` table (`001:117`) has **zero** writers in `services/` (non-test). Its one hit is the CREATE in `api-gateway/src/startup-migrations.ts`.

**Central storage (scenario 4).**
- "Platform K is a hash-only registry; the bytes themselves live with the issuer (e.g. SSD)": `documents.ts:2277-2278`, and `originate.openapi.ts:1106-1107`.
- No service imports `@azure/storage-blob` or `BlobServiceClient` (0 files).
- In `services/` and `migrations/`, `custody_mode|custodian_type|storage_mode|escrow|central(ly) stor/custod|platform custod` gives 0 hits.
- On S: PS-1075 (Done) makes Secuura-hosted storage the default and lets an Account Admin choose an org store. PS-1391 (Done) is a deployment switch for "never Secuura storage". PS-690 holds S's ownership model: a single-user org is joint user+org; in a multi-user org, the org owns the documents.

**Platform S keeps working under #1814** (Stuart, KS-1688, 2026-10-19 23:36Z):
- S signs `/version` and the `POST /{newId}/anchor` that follows it with the owning organisation's connector key, so the creating-connector arm admits it.
- A cross-organisation rights-assign changes the holder, not the key.
- The one exception is the S organisation-merge edge (PS-984). Kam ruled card `secuura-ks1688-org-merge-edge-which-side-1020` = **a**: S adds a "transfer issuer" call.

**Card state.** `secuura-ks1814-owner-role-reanchor-1030` is **withdrawn** at 07:02:43. Its `withdrawn_reason` quotes Kam's 07:01:31 note verbatim and says the merge is HELD until this mapping is done.

## TESTED / HOW

- **SHAs:**
  - `git ls-remote origin refs/pull/1814/head refs/heads/develop` in `!CODING/Secuura/Blockchain/2_Project_Files`, read twice;
  - result: `38de04f285b23eb5b5ea986c03c1adbfc2c0cabd` and `7152ac669d2d6af08be5b9dcd35132818377155d`.
- **Code:**
  - `git clone --shared --no-checkout` into `…/scratchpad/ks1814map/repo`, a fresh path; `rev-parse --show-toplevel` equals it;
  - then `git show <sha>:<path>` and `git grep <sha>`;
  - `git diff 7152ac66 38de04f2` lists exactly 7 files (`documents.ts` 63 lines changed per `--stat`, 3 tests, the ks1293 manifest, 2 docs), matching the PR body.
- **Blob equality, as the control that develop citations hold at both SHAs:** `git rev-parse <sha>:<file>`:
  - `documentRepo.ts` `da8d409a3ca0` = `da8d409a3ca0`;
  - `documentWriteRoles.ts` `ba702d6e5657` =;
  - `anchorOverwriteGuard.ts` `f73ed2362dcd` =;
  - `verification.ts` `a870d955260e` =.
- **Board (read-only GraphQL):**
  - Read in full: KS-1814, KS-1688, KS-1384, KS-621, KS-959, PS-690, PS-1075 and PS-1391.
  - Fetched but read by title only: KS-1829, KS-1385, KS-597, KS-70, KS-68, KS-1116, KS-539, KS-1693, KS-602, KS-1695, PS-984 and KS-1701.
  - `searchIssues` over "central storage", "custodial", "platform custody", "organisation owns documents", "org-owned", "issuer_organization_id", "document lineage", "owner_user_id", "custody model" and "callerMayCertifyDocument".
  - **Control failed to discriminate:** a random token `zzqxv-control-token` also returned 25 hits. The search is fuzzy, so hits were read by title and **absence of a ticket is not established** by it.
- **Cards:** `0_Brain/dashboard/data/decisions.json`, read by id.
- **Raw outputs:** `…/scratchpad/ks1814map/lin/*.json` and `…/head/*.ts`.
- **Not run:** no test, no request against any box, no database query.

## UNMEASURED (each with the instrument that would close it)

- **What share of documents has `issuer_organization_id` set, and what share of owners have `users.organization_id` set,** on kintsugi and demo. This decides whether an organisation arm would admit anyone. Instrument: a read-only count as `secuura_app` with the tenant GUC, plus a control count of `documents`. KS-959 measured 0 of 59 issuer orgs locally; KS-597's title says 0 of 100 on demo before its fix.
- **Whether the transfer-custody bypass works end to end.** Instrument: a cell in the #1814 test style. An ORG_ADMIN calls `transfer-custody` with `newHolderId=self`, then `POST /anchor` on the same document; expect 201 then 202 today. Control: the same anchor call without the transfer returns 404.
- **Whether anchoring's `POST /api/anchors` would itself refuse a same-org admin forwarded by an organisation arm.** Instrument: the KS-1603 integration file with an org-matched non-owner caller.
- **What Kam means by "stored centrally":** Secuura-hosted bytes (S's PS-1075 default), a Secuura operations principal acting as custodian, or ownerless rows. Only Kam can close this; the card below asks it.
- **Who pays the anchoring fee on each box.** It is still unmeasured on KS-1814 itself. Instrument: the anchoring wallet configuration per environment.
- **How many K-native (non-S) documents exist whose owner belongs to a multi-member organisation.** That is the population scenario 3 affects. Instrument: a read-only count joining `documents.owner_user_id` → `users.organization_id`, grouped by member count.

## Draft card for Kam (the decision is genuinely his: product policy)

**Title:** KS-1814: may a company's admin re-anchor a document owned by one of its people?

**BLUF:** Your note asked #1814 to cater for four scenarios. Three are covered:
- An owner re-anchors its own documents and its modified versions; modifications create linked versions, and lineage is shown.
- Platform admins remain the "central" actor. K stores only hashes, so it has no record of where documents are stored.
- Platform S keeps working through its organisation key.

The one scenario #1814 does not cover is **"a company keeps them"**. An ORG_ADMIN or ISSUER_ADMIN of the *same* organisation, who is not the owner, is refused. That is narrower than your KS-1385 (c) ruling, "Issuer, or anyone in the custodian's organisation".

Separately, that refusal can be bypassed today: an admin can transfer custody of the document to itself first. That route has no per-document check, and it needs one whichever option you choose.

#1814 only narrows access, so merging it now refuses no one the other three scenarios need.

**Options:**
- **(a) Merge #1814 now; follow-up adds the organisation arm** (recommended). Same-organisation admins re-anchor, matched on the issuer organisation or the owner's organisation, as anchoring already does. The follow-up also adds the per-document check to transfer-custody, after a count of how many documents carry an organisation at all.
- **(b) Add the organisation arm to #1814 before merging.** One more round on the PR. The anchor route stays open to every tenant user until it lands.
- **(c) Merge #1814 as the final rule: owner, platform admin and creating connector only.** A company's admin never re-anchors a member's document. Transfer-custody is still closed separately.

**Recommendation: (a).** It closes the fee-spending hole today and matches your earlier organisation-level ruling. It builds the organisation arm only once the data that would feed it has been counted.

**Default if unanswered: (a).**

Scenario 4 (central storage) needs no tap now. If you want K to know where a document is held, that becomes a new field, and its own card.
