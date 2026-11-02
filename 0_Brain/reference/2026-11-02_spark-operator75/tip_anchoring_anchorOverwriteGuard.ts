/**
 * =============================================================================
 * KS-1385 — who may overwrite a stored anchor attestation
 * =============================================================================
 * Kam ruled card `secuura-ks1385-anchor-identity-needs-ps895-ruling-1013` = b,
 * verbatim: "Latest event's identity wins". Pull request 1549 implemented that
 * by adding `metadata_payload = EXCLUDED.metadata_payload` to the upsert's
 * `DO UPDATE SET` list — and that one line turned a write-once row into one
 * ANY authenticated caller, from ANY tenant, could rewrite, because
 * `POST /api/anchors` has never checked who owns `documentId` (KS-1603, the
 * pre-existing hole). The gate on head `aca6efb0` booted the real service and
 * demonstrated it: a tenant-B user rewrote tenant-A's anchor, and the public
 * verify-by-hash for the victim's bytes then answered `verified: true` carrying
 * the stranger's organisation and a "government / level 3" identity.
 *
 * THE RULED PRINCIPLE (Wednesday, 2026-10-13T11:22:45Z): the overwrite applies
 * only when the guard POSITIVELY confirms a legitimate event of this document.
 * Otherwise the row keeps its stored payload exactly as develop does.
 * #1549 could only REDUCE overwrites. KS-1612 deliberately ADDS some: it is what
 * lets Kam's rulings reach originate's anchors (external ids) and certifications
 * (no issuer, Kam's (b)). Each one added is a positively confirmed event of a
 * document in the caller's own tenant. The #1568 round-1 gate found that this
 * held only while no row's external_id could equal another tenant's primary key
 * (its MAJ-1); migration 050 makes that impossible database-wide, and the
 * resolution below relies on it — see readOwningDocument.
 *
 * WHY THE TENANT PREDICATE IS IN THE SQL AND NOT LEFT TO RLS. `documents` is
 * `relrowsecurity = t, relforcerowsecurity = t` with policy `tenant_isolation`
 * keyed on `app.current_tenant_id` — but (1) that policy carries an escape,
 * `OR current_setting('app.tenant_scope_bypass') = 'platform_admin'`, and
 * (2) a role with BYPASSRLS is not subject to it at all. Measured on the repo
 * schema: `secuura` is `rolsuper = t, rolbypassrls = t`; `secuura_app` is
 * neither. Anchoring runs as `secuura_app` (docker-compose.yml, the anchoring
 * block: `DATABASE_URL=…secuura_app…@pgbouncer:6432`), so RLS IS live in the
 * real deployment — but a guard whose correctness depends on which role is
 * configured is not a guard. The tenant bound is therefore an explicit
 * `tenant_id = $2::uuid` in the WHERE clause, and the GUC is set as well so
 * the read still works where the role IS subject to RLS. Belt and braces, and
 * the braces are the ones that hold.
 *
 * `set_config(..., true)` is SET LOCAL semantics, so it is scoped to the
 * transaction and safe through pgbouncer's transaction pooling.
 * `provenance.ts` is the in-service precedent for exactly this.
 *
 * KS-1612 — WHICH ID THE CALLER SENDS (the #1549 round-2 gate's MAJ-A). #1549 read
 * the document by `documents.id` only, and refused any id that was not uuid-shaped.
 * But originate's DOCUMENT anchors send the EXTERNAL id: `routes/documents.ts`
 * sends `documentId: id` with `id = documentUuid ?? 'doc-…'`, and
 * `documentRepo.ts` writes that value to `external_id` beside a fresh primary key.
 * So for every originate document anchor the guard found no row and kept the stored
 * payload, and neither of Kam's rulings took effect. CERTIFICATION anchors are the
 * other way round: `certificationRepo.ts` inserts `id = cert.id` and writes no
 * `external_id`, and their anchors send `cert.id`. The read therefore resolves the
 * id exactly as originate's own `getDocument` does — `external_id` first, then the
 * primary key, both bound to the caller's tenant — so the guard judges the same row
 * originate acts on.
 * =============================================================================
 */

import { transaction } from './db';

/**
 * CUSTODY — Kam ruled card `secuura-ks1385-custodian-may-update-anchor-identity-1013`
 * = c, verbatim: "Issuer, or anyone in the custodian's organisation"
 * (2026-10-14 11:15:54, live board). Round 1 shipped (a), issuer only, while the
 * card was still open.
 *
 * Measured on the repo schema: custody is recorded as a **USER**, not an
 * organisation — `documents.owner_user_id` (transfer-custody flips it) and
 * `custody_events.to_holder_id`. There is NO custodian-organisation column;
 * the custodian's organisation is derivable in one join via
 * `users.organization_id`.
 *
 * (a), (b) and (c) are each ONE condition in `decideMetadataOverwrite` — see
 * the marked block there — and the option is a parameter of that function, so
 * the cells exercise all three for real. Delivering the ruling was this one
 * constant.
 *
 * NO-ISSUER ROWS — Kam ruled card `secuura-ks1385-null-issuer-certifications-1015`
 * = b, "Apply (c) to them too" (2026-10-18 19:00:28, live board). Its detail,
 * verbatim: "A follow-up ticket and round reorders the guard so the custodian's
 * organisation can update these rows. This gives a certificate holder's
 * organisation a new write." He chose that knowingly. It is not an exotic shape:
 * originate's certification INSERT (`certificationRepo.ts`) writes no
 * `issuer_organization_id` and sets `owner_user_id` to the HOLDER, so every
 * certification row is one. So a NULL issuer is no longer refused before the
 * custody block: the block runs for every row, and a no-issuer row is refused only
 * when no custody rule admits the caller. #1549 kept these rows as develop does,
 * on Wednesday's interim ruling (2026-10-15T02:17:54Z); cell C-f, which pinned that
 * limit, now pins the new write.
 */
export type CustodyOption = 'a' | 'b' | 'c';
export const CUSTODY_OPTION: CustodyOption = 'c';

/** The caller fields `POST /api/anchors` has on `req.user` (index.ts:520-530). */
export interface AnchorCaller {
  role?: string;
  userId?: string;
  organizationId?: string;
  tenantId?: string;
}

/** What the decision reads about the owning document, all as text. */
export interface OwningDocument {
  tenantId: string;
  issuerOrganizationId: string | null;
  /** `documents.owner_user_id` — the CURRENT custodian, as a user. */
  ownerUserId: string | null;
  /**
   * `users.organization_id` for that custodian, resolved in the same
   * tenant-scoped read, so custody option (c) — which ships — is a comparison
   * rather than a second query.
   */
  ownerOrganizationId: string | null;
}

export type OverwriteRefusal =
  | 'caller-has-no-tenant'
  | 'caller-has-no-organisation'
  | 'caller-organisation-not-a-uuid'
  | 'document-not-in-callers-tenant'
  | 'document-has-no-issuer-organisation'
  | 'caller-is-not-the-issuer-organisation';

export type OverwriteDecision =
  | { allow: true; reason: 'caller-is-issuer-organisation' | 'caller-is-custodian-user' | 'caller-shares-custodian-organisation' }
  | { allow: false; reason: OverwriteRefusal };

/**
 * A uuid in the one shape Postgres' `uuid` type accepts from us here. It is a
 * SHAPE test, not a validity test: its job is to stop a non-uuid reaching a
 * `::uuid` cast, which raises 22P02 and would turn a guarded keep into a 5xx.
 * A `doc-…` id is the ordinary case, not the exotic one: it is originate's own
 * external-id form and Platform S's flat form.
 */
const UUID_SHAPE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/**
 * KS-1385 (b) — THE ISSUER FIELDS. Kam ruled card `secuura-ks1385-cert-holder-can-rewrite-issuer-fields-1018` = b,
 * "Holder may update, but not the issuer fields", option detail verbatim: "A follow-up keeps issuerOrgId, orgDid,
 * orgTrust and orgVerified as first anchored, and lets the holder change only the rest."
 *
 * These are four keys of `metadata_payload.secuura` (anchorSchema.ts builds them flat there). Whenever an overwrite is
 * admitted for anyone OTHER than the issuer's organisation — today the custodian's organisation, Kam's (c) — the
 * upsert keeps each of these keys exactly as stored, absent stays absent, and applies the rest of the payload.
 * The issuer's own events are unchanged: "latest event's identity wins" still applies to them.
 */
export const ISSUER_FIELDS = ['issuerOrgId', 'orgDid', 'orgTrust', 'orgVerified'] as const;

/** True exactly when an admitted overwrite must keep the stored issuer fields (KS-1385 (b)). */
export function holdsIssuerFields(decision: OverwriteDecision): boolean {
  return decision.allow && decision.reason !== 'caller-is-issuer-organisation';
}

export function isUuidShaped(value: unknown): boolean {
  return typeof value === 'string' && UUID_SHAPE.test(value.trim());
}

/**
 * uuids are case-insensitive by definition and Postgres renders them
 * lower-case, so a caller's claim that differs only in case is the SAME
 * organisation and must not be refused on spelling.
 */
function sameUuid(a: string | null | undefined, b: string | null | undefined): boolean {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  const left = a.trim().toLowerCase();
  const right = b.trim().toLowerCase();
  if (left.length === 0 || right.length === 0) return false;
  return left === right;
}

/**
 * THE DECISION. Pure: no database, no clock, no environment — so it is
 * unit-testable per branch and a mutant on any single condition lands on a
 * named cell.
 *
 * `doc === null` means "the document is not in the caller's tenant", which
 * covers both a document that does not exist (Platform S's flat anchors) and
 * one that belongs to somebody else. Both keep the payload, which is develop's
 * behaviour — as ruled for the flat-anchor case.
 */
export function decideMetadataOverwrite(
  caller: AnchorCaller | undefined,
  doc: OwningDocument | null,
  /**
   * Which custody option to apply. Defaults to the shipped `CUSTODY_OPTION`, so
   * every product call reads (c).
   *
   * It is a PARAMETER rather than only a module constant for one reason: the
   * pull request claims the options are each one condition apart, and a
   * claim like that is worth nothing unless a cell can exercise it. With this
   * argument the pending cells for Kam's card run for real today, instead of
   * sitting skipped — which the workspace never-skip rule forbids — or behind
   * an `if` arm that cannot be taken until the constant flips.
   */
  custodyOption: CustodyOption = CUSTODY_OPTION,
): OverwriteDecision {
  if (!caller?.tenantId || caller.tenantId.trim().length === 0) return { allow: false, reason: 'caller-has-no-tenant' };
  if (!caller.organizationId || caller.organizationId.trim().length === 0) return { allow: false, reason: 'caller-has-no-organisation' };
  if (!isUuidShaped(caller.organizationId)) return { allow: false, reason: 'caller-organisation-not-a-uuid' };
  if (doc === null) return { allow: false, reason: 'document-not-in-callers-tenant' };

  // THE ISSUER — admitted under every option. `issuer_organization_id` is NULLABLE
  // on `documents` (measured), and every certification row has none.
  const hasIssuer = doc.issuerOrganizationId !== null && doc.issuerOrganizationId.trim().length > 0;
  if (hasIssuer && sameUuid(doc.issuerOrganizationId, caller.organizationId)) {
    return { allow: true, reason: 'caller-is-issuer-organisation' };
  }

  // ---- CUSTODY EXTENSION POINT (Kam's card) ---------------------------------
  // Option (b): the custodian USER may update.
  if (custodyOption === 'b' && sameUuid(doc.ownerUserId, caller.userId)) {
    return { allow: true, reason: 'caller-is-custodian-user' };
  }
  // Option (c) — SHIPS: anyone in the custodian's ORGANISATION may update. The
  // custodian's organisation is `users.organization_id` for
  // `documents.owner_user_id`, resolved by `readOwningDocument` in the same
  // tenant-scoped read, so this is a comparison and not a second query.
  if (custodyOption === 'c' && sameUuid(doc.ownerOrganizationId, caller.organizationId)) {
    return { allow: true, reason: 'caller-shares-custodian-organisation' };
  }
  // ---------------------------------------------------------------------------

  // A NULL issuer can never equal a caller's organisation, so it is named rather than
  // compared: the refusal reason is the useful half.
  return { allow: false, reason: hasIssuer ? 'caller-is-not-the-issuer-organisation' : 'document-has-no-issuer-organisation' };
}

/**
 * Read the owning document, bound to the caller's tenant two ways (see the
 * module header). Returns null when there is no such document IN THAT TENANT,
 * including when the tenant id is not uuid-shaped.
 *
 * KS-1612: `documentId` is resolved as originate's `getDocument` resolves it —
 * `external_id` first, then the primary key — so the guard judges the row
 * originate acts on. ⚠ That is safe only because migration 050 keeps the two
 * namespaces disjoint across ALL tenants. `anchor_store` is one global text
 * namespace with no tenant column, so if tenant B's external_id could equal
 * tenant A's primary key, "this id names a document in my tenant" would no
 * longer imply "this anchor row is my document's" (the #1568 gate's MAJ-1). The external id is matched exactly as sent, as getDocument
 * does. The primary-key arm takes a uuid PARAMETER that is NULL unless the id is
 * uuid-shaped: a `doc-…` id must never reach a `::uuid` cast (22P02), and Postgres
 * does not promise to evaluate the arms of an OR in order, so the guard is in the
 * parameter rather than in the SQL.
 *
 * `documents` and `anchor_store` live in the same database — anchoring and
 * originate share `pgbouncer:6432/${POSTGRES_DB:-secuura}` — so this needs no
 * migration and no cross-service call.
 */
export async function readOwningDocument(documentId: string, tenantId: string): Promise<OwningDocument | null> {
  if (typeof documentId !== 'string' || documentId.length === 0 || !isUuidShaped(tenantId)) return null;
  const asPrimaryKey = isUuidShaped(documentId) ? documentId.trim() : null;
  return transaction(async (client) => {
    await client.query("SELECT set_config('app.current_tenant_id', $1, true)", [tenantId.trim()]);
    // The LEFT JOIN carries its OWN `u.tenant_id = $2::uuid`, and that is not
    // belt-and-braces duplication of the one on `documents`. `users` has a
    // SECOND, permissive policy — `users_auth_lookup`, whose qual is literally
    // `true` — and Postgres ORs permissive policies together, so tenant
    // isolation on `users` is open for SELECT by construction. Measured on the
    // repo schema. A join without its own bound would read a custodian row
    // from ANY tenant.
    //
    // LEFT, not INNER: a document whose custodian user has been deleted must
    // still yield the document row, with a null custodian organisation, rather
    // than vanish and read as "not in the caller's tenant".
    const r = await client.query(
      `SELECT d.tenant_id::text AS tenant_id,
              d.issuer_organization_id::text AS issuer_organization_id,
              d.owner_user_id::text AS owner_user_id,
              u.organization_id::text AS owner_organization_id
         FROM documents d
         LEFT JOIN users u
                ON u.id = d.owner_user_id
               AND u.tenant_id = $2::uuid
        WHERE d.tenant_id = $2::uuid
          AND (d.external_id = $1 OR d.id = $3::uuid)
        ORDER BY (d.external_id = $1) DESC NULLS LAST
        LIMIT 1`,
      [documentId, tenantId.trim(), asPrimaryKey],
    );
    if (r.rowCount !== 1) return null;
    const row = r.rows[0] as {
      tenant_id: string;
      issuer_organization_id: string | null;
      owner_user_id: string | null;
      owner_organization_id: string | null;
    };
    return {
      tenantId: row.tenant_id,
      issuerOrganizationId: row.issuer_organization_id,
      ownerUserId: row.owner_user_id,
      ownerOrganizationId: row.owner_organization_id,
    };
  });
}

/**
 * Whether a KEPT payload is the ordinary case that `dbPersistAnchor` deliberately does
 * not log. Develop refused every non-uuid `documentId` unread, right after the tenant
 * check, so EVERY keep on one from a caller with a tenant was silent — whatever the
 * caller's organisation. Platform S's flat anchors take that path by design, and logging
 * it would bury the anomalies. Quiet here, as on develop: a non-uuid id from a caller
 * with a tenant whose organisation is unusable (missing, as on a connector token minted
 * with none — auth's jwt.ts — or not a uuid), or that names no document in the caller's
 * tenant. What now LOGS that develop kept silent, both on purpose: a non-uuid id that
 * names a document in the caller's tenant and is refused (a real refusal, newly
 * reachable), and an allowed caller whose payload the upsert kept anyway (a hash or
 * anchor-type mismatch). Pure, so a cell pins it without booting the service.
 */
const DEVELOP_QUIET_REASONS: ReadonlySet<OverwriteRefusal> = new Set<OverwriteRefusal>([
  'document-not-in-callers-tenant',
  'caller-has-no-organisation',
  'caller-organisation-not-a-uuid',
]);
export function isQuietKeep(decision: OverwriteDecision, documentId: string): boolean {
  return !decision.allow && DEVELOP_QUIET_REASONS.has(decision.reason) && !isUuidShaped(documentId);
}

/**
 * KS-1385 (b) round 2 (the T1 gate's MIN-2): which server line a persisted anchor earns, decided from the upsert's
 * own RETURNING flags. It is a pure function so that a cell can run it on the REAL row the REAL statement returns;
 * before, the split lived inline in dbPersistAnchor and was pinned by source text alone.
 *   'held-issuer-fields' an admitted non-issuer's update APPLIED, with the stored issuer fields kept: the info line.
 *   'kept'               the stored payload was kept (a refused caller, or a hash or anchor-type mismatch): the warn line.
 *   'kept-quietly'       kept, on Platform S's by-design repeat path (isQuietKeep): no line, as on develop.
 *   'stored-as-sent'     the stored payload is the one sent, or the comparison was NULL: no line, as on develop.
 */
export type PersistOutcome = 'stored-as-sent' | 'held-issuer-fields' | 'kept' | 'kept-quietly';

export function classifyPersistOutcome(
  decision: OverwriteDecision,
  row: { payload_is_incoming?: boolean | null; rest_is_incoming?: boolean | null } | null | undefined,
  documentId: string,
): PersistOutcome {
  if (!row || row.payload_is_incoming !== false) return 'stored-as-sent';
  if (holdsIssuerFields(decision) && row.rest_is_incoming === true) return 'held-issuer-fields';
  return isQuietKeep(decision, documentId) ? 'kept-quietly' : 'kept';
}

/**
 * The one call site's worth of glue: read, then decide. Separated from the
 * decision so the decision stays pure, and separated from `dbPersistAnchor` so
 * a refusal is one named value rather than an inline boolean.
 *
 * It never throws outward: a database fault here must not turn an anchor into a
 * 5xx, and the fail-closed answer is "keep the stored payload", which is
 * develop's behaviour.
 */
export async function mayOverwriteStoredMetadata(
  documentId: string,
  caller: AnchorCaller | undefined,
  log?: (level: 'warn', message: string, meta?: Record<string, unknown>) => void,
): Promise<OverwriteDecision> {
  if (!caller?.tenantId || caller.tenantId.trim().length === 0) return { allow: false, reason: 'caller-has-no-tenant' };
  try {
    const doc = await readOwningDocument(documentId, caller.tenantId);
    return decideMetadataOverwrite(caller, doc);
  } catch (err: unknown) {
    log?.('warn', 'KS-1385: the anchor-overwrite guard could not read the owning document — keeping the stored payload', {
      documentId,
      error: (err as { message?: string })?.message,
    });
    return { allow: false, reason: 'document-not-in-callers-tenant' };
  }
}


/**
 * =============================================================================
 * KS-1603 — WHO MAY WRITE AN ANCHOR ROW AT ALL (the interim ownership check)
 * =============================================================================
 * Everything above decides who may REPLACE a stored attestation. It is silent on
 * who may write the row in the first place, and `index.ts` says so at the `$23`
 * parameter: "a first anchor is never gated: the guard decides who may REPLACE an
 * attestation, not who may make one. That question is KS-1603."
 *
 * THE GAP. `dbPersistAnchor`'s `ON CONFLICT (document_id, network) DO UPDATE SET`
 * list gates `metadata_payload` alone. The other twelve columns — `status`,
 * `transaction_hash`, `block_hash`, `block_number`, `slot`, `fee`,
 * `confirmations`, `confirmed_at`, `error_message`, `retry_count`, `simulated`,
 * `updated_at` — are unconditional, for any authenticated caller from any tenant.
 * `transaction_hash` and `content_hash` are not cosmetic: `content_hash` is the
 * key public verify-by-hash resolves on, so rewriting it changes which bytes
 * verify.
 *
 * WHY THE RESOLVER ABOVE CANNOT BE THIS GATE. `readOwningDocument` is bound to the
 * caller's own tenant, so it answers `null` — and `decideMetadataOverwrite` reports
 * `document-not-in-callers-tenant` — for TWO different situations:
 *   * the id names no document in ANY tenant. That is the whole of Platform S's
 *     flat-anchor traffic: S sends `documentId = ToHyphenatedGuid(tx.ChainId)`, its
 *     own ledger chain id, one fresh value per event and never a K document id, so
 *     every S flat anchor is its own `anchor_store` row (Stuart, KS-1603, 2026-10-15,
 *     read from `CardanoAnchorService.PerVerb.cs`);
 *   * the id names ANOTHER TENANT'S document. That is the attack this ticket is
 *     about, demonstrated end to end by the pull request 1549 gate on the real
 *     service.
 * Refusing on `allow: false` would therefore refuse S's live integration. Telling
 * the two apart needs a read of `documents` that is NOT bound to the caller's
 * tenant.
 *
 * WHY THAT READ NEEDS THE PLATFORM-ADMIN GUC, AND WHY THAT IS NOT A HOLE.
 * Anchoring runs as `secuura_app` — neither superuser nor BYPASSRLS
 * (docker-compose.yml, the anchoring block) — and `documents` is FORCE RLS. Under
 * migration 039 the `tenant_isolation` policy is fail-CLOSED with exactly one
 * escape, `current_setting('app.tenant_scope_bypass', true) = 'platform_admin'`
 * (039_rls_fail_closed.sql:124), so an unbound read returns ZERO rows. Under the
 * older 011 policy the same read is fail-OPEN on an unset GUC and returns
 * EVERYTHING (011_documents_tenant_id.sql:160-171; KS-1054 — a fresh database is
 * fail-open until the second boot). A probe that answers differently by migration
 * level is not a probe, so the escape is set DELIBERATELY and the answer is the
 * same on both. Measured on a migrated scratch database as `secuura_app`: without
 * the GUC the read sees 0 rows while the owner sees 1; with it, 1 row and the
 * owning tenant; after the transaction, 0 again and the GUC back to unset.
 *
 * `set_config(..., true)` is SET LOCAL semantics — scoped to the transaction and
 * safe through pgbouncer's transaction pooling, for the same reason
 * `readOwningDocument` relies on it. It reads ONE column of at most one row per
 * requested id and never writes. Seat J 13th's migration 051 needed SECURITY
 * DEFINER for the same visibility, "for CORRECTNESS and not only to see a foreign
 * row" (051:62-66); that is the alternative shape, and it was ruled out for this
 * interim because it would add a second `052_` migration beside the one KS-1402
 * is already taking.
 *
 * THIS IS A PURE NARROWING — Wednesday's ruling of 2026-10-19T05:55:40Z, confirming
 * the predicate proposed at 05:54Z. The ONLY new refusal is "this id names a
 * `documents` row whose `tenant_id` is not the caller's". Everything else behaves
 * exactly as develop:
 *   * no document holds the id, in any tenant   -> ALLOW (S's flat anchors, and
 *     their retries: one event's ChainId is fixed, so a retry repeats the id and
 *     must not newly fail — the registrar retries every non-2xx each tick, KS-1584);
 *   * the document is in the caller's own tenant -> ALLOW, whoever the caller is
 *     inside it. The issuer / custodian test above is deliberately NOT the write
 *     gate: it would newly refuse an in-tenant caller who is neither — an admin on
 *     a lifecycle event, say — on the seven originate sites that forward the end
 *     user's own bearer. That is not this ticket's scope;
 *   * the caller carries no usable tenant claim -> ALLOW with a warn. `tenantId` is
 *     genuinely optional: auth signs it conditionally
 *     (`services/auth/src/services/jwt.ts:263`);
 *   * the probe itself throws                   -> ALLOW with a warn (fail-OPEN).
 *     Failing closed would turn a transient database fault into refused anchoring
 *     for Platform S. Fail-open makes this interim's worst case exactly develop,
 *     which is the honest bound for an interim and the same argument `index.ts`
 *     makes for the KS-1385 conditions.
 *
 * WHAT IT DOES NOT CLOSE. An `anchor_store` row whose `document_id` names no
 * document records no owner anywhere, so nothing here can say who may rewrite it;
 * that needs the tenant column, which is the KS-1384 structural project on Kam's
 * card `secuura-ks1384-schedule-per-event-anchors-1019` and is deliberately
 * untouched.
 * =============================================================================
 */

/** The one refusal this gate adds. */
export type AnchorWriteRefusal = 'document-belongs-to-another-tenant';

export type AnchorWriteAllowReason =
  /** No `documents` row in any tenant holds this id — Platform S's flat anchors. */
  | 'no-document-holds-these-ids'
  /** Every id resolved, and to the caller's own tenant. */
  | 'documents-are-in-callers-tenant'
  /** No usable tenant claim on the caller, so there is nothing to compare. */
  | 'caller-has-no-usable-tenant'
  /** The probe faulted. Fail-open, as ruled. */
  | 'ownership-probe-unavailable';

export type AnchorWriteDecision =
  | { allow: true; reason: AnchorWriteAllowReason }
  | { allow: false; reason: AnchorWriteRefusal; documentId: string; ownerTenantId: string };

/** One row of the cross-tenant probe: an id, and the tenant whose document holds it. */
export interface IdOwner {
  documentId: string;
  ownerTenantId: string;
}

/**
 * Which of these ids are held by a `documents` row, and by which tenant — read
 * ACROSS tenants, in ONE statement for the whole request (the batch route accepts
 * up to 100 ids, `index.ts:281`, and 100 round trips for one decision is not a
 * design).
 *
 * The id is resolved exactly as `readOwningDocument` resolves it, `external_id`
 * first and then the primary key, so this gate judges the same row the overwrite
 * guard and originate's own `getDocument` judge. ⚠ Safe only because migration 050
 * keeps the two id namespaces disjoint across ALL tenants.
 *
 * The primary-key arm takes its OWN array, carrying only the uuid-shaped ids: a
 * `doc-…` id must never reach a `::uuid` cast (22P02), and Postgres does not
 * promise to evaluate the arms of an OR in order — so, as above, the guard is in
 * the parameter and not in the SQL. An empty array is a valid `uuid[]`.
 */
export async function readIdOwners(documentIds: readonly string[]): Promise<IdOwner[]> {
  const ids = documentIds.filter((d): d is string => typeof d === 'string' && d.length > 0);
  if (ids.length === 0) return [];
  const asPrimaryKeys = ids.filter((d) => isUuidShaped(d)).map((d) => d.trim());
  return transaction(async (client) => {
    // 039's single escape, SET LOCAL. See the module block above for why it is here
    // and what it costs. One column, at most one row per id, never a write.
    await client.query("SELECT set_config('app.tenant_scope_bypass', 'platform_admin', true)");
    const r = await client.query(
      `SELECT d.external_id AS external_id,
              d.id::text    AS primary_key,
              d.tenant_id::text AS tenant_id
         FROM documents d
        WHERE d.external_id = ANY($1::text[])
           OR d.id = ANY($2::uuid[])`,
      [ids, asPrimaryKeys],
    );
    const byExternal = new Map<string, string>();
    const byPrimaryKey = new Map<string, string>();
    for (const row of r.rows as Array<{ external_id: string | null; primary_key: string; tenant_id: string | null }>) {
      if (typeof row.tenant_id !== 'string' || row.tenant_id.length === 0) continue;
      if (typeof row.external_id === 'string' && row.external_id.length > 0) byExternal.set(row.external_id, row.tenant_id);
      byPrimaryKey.set(row.primary_key.toLowerCase(), row.tenant_id);
    }
    const owners: IdOwner[] = [];
    for (const documentId of ids) {
      // external_id first, then the primary key — the same precedence as
      // readOwningDocument's `ORDER BY (d.external_id = $1) DESC`.
      const ownerTenantId = byExternal.get(documentId) ?? byPrimaryKey.get(documentId.trim().toLowerCase());
      if (typeof ownerTenantId === 'string') owners.push({ documentId, ownerTenantId });
    }
    return owners;
  });
}

/**
 * THE GATE. Refuses exactly one thing: an id held by a document in a tenant that
 * is not the caller's. Everything else allows, with the reason named so the log
 * line and the cells can tell the four allow-paths apart.
 *
 * It never throws outward — a probe fault must not turn an anchor into a 5xx, and
 * the ruled fail-open answer is "allow", which is develop's behaviour.
 */
export async function mayWriteAnchorRows(
  documentIds: readonly string[],
  caller: AnchorCaller | undefined,
  log?: (level: 'warn', message: string, meta?: Record<string, unknown>) => void,
): Promise<AnchorWriteDecision> {
  const callerTenantId = typeof caller?.tenantId === 'string' ? caller.tenantId.trim() : '';
  // A tenant claim that is absent, blank, or not uuid-shaped is not something a
  // Postgres-rendered uuid can ever equal, so comparing it would refuse rather
  // than compare. Develop allows these, and this gate is a narrowing.
  if (!isUuidShaped(callerTenantId)) {
    log?.('warn', 'KS-1603: the anchor caller carries no usable tenant claim — allowing the write, as develop does', {
      documentIds: documentIds.slice(0, 8),
      callerTenantIdPresent: callerTenantId.length > 0,
    });
    return { allow: true, reason: 'caller-has-no-usable-tenant' };
  }
  let owners: IdOwner[];
  try {
    owners = await readIdOwners(documentIds);
  } catch (err: unknown) {
    log?.('warn', 'KS-1603: the anchor ownership probe could not read the owning document — allowing the write (fail-open), as develop does', {
      documentIds: documentIds.slice(0, 8),
      error: (err as { message?: string })?.message,
    });
    return { allow: true, reason: 'ownership-probe-unavailable' };
  }
  // The first foreign id in the REQUEST'S order, so the refusal is deterministic.
  const foreign = owners.find((o) => !sameUuid(o.ownerTenantId, callerTenantId));
  if (foreign) {
    return {
      allow: false,
      reason: 'document-belongs-to-another-tenant',
      documentId: foreign.documentId,
      ownerTenantId: foreign.ownerTenantId,
    };
  }
  return {
    allow: true,
    reason: owners.length === 0 ? 'no-document-holds-these-ids' : 'documents-are-in-callers-tenant',
  };
}

/**
 * The refusal, as a TYPE rather than a status code, so the gate can live at the one
 * site both routes persist through (`dbPersistAnchor`) while each handler decides
 * its own response. Without a distinguishable error the flat route's `next(error)`
 * would turn a deliberate 403 into a 500.
 *
 * `ownerTenantId` is carried for the SERVER log only. The response must not name
 * another tenant's id: the caller has just been told it does not own the document,
 * and telling it who does would answer a question it is not entitled to ask.
 */
export class AnchorOwnershipError extends Error {
  readonly reason: AnchorWriteRefusal;
  readonly documentId: string;
  readonly ownerTenantId: string;
  constructor(decision: Extract<AnchorWriteDecision, { allow: false }>) {
    super('caller does not own this document');
    this.name = 'AnchorOwnershipError';
    this.reason = decision.reason;
    this.documentId = decision.documentId;
    this.ownerTenantId = decision.ownerTenantId;
  }
}

/** True for the KS-1603 refusal, without an `instanceof` that a second module registry breaks. */
export function isAnchorOwnershipError(err: unknown): err is AnchorOwnershipError {
  return err instanceof Error && (err as { name?: string }).name === 'AnchorOwnershipError';
}
