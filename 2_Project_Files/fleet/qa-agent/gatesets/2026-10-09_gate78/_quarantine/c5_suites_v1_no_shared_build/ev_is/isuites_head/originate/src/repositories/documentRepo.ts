/**
 * =============================================================================
 * DOCUMENT REPOSITORY
 * =============================================================================
 * Persistence layer for documents using raw SQL that matches the actual
 * database column names. Database is the single source of truth.
 * =============================================================================
 */

import { prisma } from '../db';
import { runWithTenantId } from '@secuura/shared';

type DbClient = typeof prisma;
import { v4 as uuidv4 } from 'uuid';
import crypto from 'crypto';
import { logger } from '../utils/logger';

// =============================================================================
// TYPES
// =============================================================================

export interface DocumentRecord {
  id: string;
  // KS-596 (architecture P1, Phase B): the registration's canonical UUID —
  // the S-supplied documentUuid when registration carried one (stored as
  // external_id), else the row's own UUID primary key. Read paths surface it
  // alongside the legacy `id` so S can migrate reads independently of writes.
  // getDocument already resolves lookups by either value.
  documentUuid?: string;
  type: string;
  status: 'draft' | 'pending_signature' | 'signed' | 'anchored' | 'revoked';
  owner: {
    id: string;
    walletAddress?: string;
  };
  // Subject of the credential (the holder), separate from owner (the
  // creator/issuer). Empty on every existing row today — populated when
  // VC issuance lands. Surfaced here so the OWNER-role wallet view can
  // already include subject-scoped docs the moment they get populated,
  // without needing a second migration.
  rightsHolderId?: string;
  // KS-70: parent document in a lifecycle chain. Each certify / sign /
  // transfer-custody event produces a new linked document whose
  // `parent_document_id` points at its predecessor. Verify walks the
  // chain (up to MAX_LINEAGE_DEPTH) to surface provenance. Migration
  // 021 enforces the FK; the route layer enforces the no-cycles rule.
  // Undefined for documents created via the original (non-lifecycle)
  // POST /api/documents path.
  parentDocumentId?: string;
  data: Record<string, unknown>;
  contentHash: string;
  signatures: Array<{
    signerId: string;
    walletAddress: string;
    signature: string;
    signedAt: string;
  }>;
  blockchain?: {
    // Absent when the blob carries only a `threadToken` cache (minted at
    // document-create, before any anchor); null in the `pending-onchain` dev
    // state. A confirmed anchor carries a hash; a fresh 202 / fail-closed carries null.
    txHash?: string | null;
    // Absent in the threadToken-only state; null in `pending-onchain`. A
    // confirmed anchor carries a real number; a fresh 202 / fail-closed carries 0.
    blockHeight?: number | null;
    // Absent in the KS-520 fail-closed state — nothing was anchored, so
    // there is no anchor time to record. Null in the pending-onchain state.
    // Carried forward on a HASHED anchor_failed write (the tx reached the chain
    // before the write failed — anchorStateSync.ts's reconcile carry), so a
    // failed anchor with a real txHash keeps its time.
    anchoredAt?: string | null;
    network?: string;
    status?: string;
    anchorId?: string;
    simulated?: boolean;
    // KS-587: placeholder ref for a SIMULATED anchor — txHash stays null and
    // the placeholder rides here with `simulated: true` (never presented as
    // on-chain proof). Written via `simulatedFieldsFromAnchor` in documents.ts
    // and anchorStateSync.ts.
    simulatedTxRef?: string | null;
    // KS-1058: cache of the state-thread token so dashboards can show it
    // without a second lookup; the canonical truth is state_thread_registry.
    // Was written with `as any` (KS-1068) — declared here so a writer that
    // rebuilds the blob and drops it is at least visible to a reader of the type.
    threadToken?: {
      policyId: string;
      scriptAddress: string;
      // Null for a token minted but not yet confirmed on chain —
      // `StateThreadRegistryEntry.mintTxHash` is `string | null`. Was masked by
      // the `as any` (KS-1068); declared here so the null state is visible.
      mintTxHash: string | null;
      network?: string;
    };
    // Verifier-facing signal for the non-anchored dev-mode state. KS-1057
    // established it must NOT be carried onto a terminally-failed anchor, so it
    // is optional here — declaring it does not force it to be carried.
    confidence?: string;
    // KS-520 fail-closed state (`status: 'anchor_failed'`): the auto-anchor
    // call failed and simulation was not requested, so the document stays
    // un-anchored with the failure recorded for retry/diagnostics.
    error?: string;
    failedAt?: string;
  };
  createdAt: string;
  updatedAt: string;
}

/**
 * KS-70: soft cap on the verify-side lineage walk and the certify-side
 * cycle check. Real-world worst case (revoke → reissue → recertify cycles
 * over a long-lived document) sits around 6-8 levels; 12 gives ~50%
 * headroom. Env-var override so we can lift the cap without redeploy.
 */
export const MAX_LINEAGE_DEPTH = parseInt(process.env.MAX_LINEAGE_DEPTH || '12', 10);

export interface SigningRequest {
  documentId: string;
  walletAddress: string;
  hash: string;
  nonce: string;
  expiresAt: string;
}

// =============================================================================
// STATE
// =============================================================================

// Signing requests are intentionally in-memory — they are short-lived nonces
const memSigningRequests = new Map<string, SigningRequest>();

// =============================================================================
// DB READINESS CHECK
// =============================================================================

export async function verifyDbReady(db?: DbClient): Promise<void> {
  try {
    await (db || prisma).$queryRaw`SELECT 1`;
    logger.info('documentRepo: database connection verified');
  } catch (err: any) {
    logger.error('documentRepo: database connection FAILED — documents will not be available', {
      error: err instanceof Error ? err.message : String(err),
    });
    throw new Error('Database is required for document operations');
  }
}

// =============================================================================
// DB → DOMAIN CONVERTERS
// =============================================================================

/**
 * KS-550: keys in the metadata blob that are owned by the DocumentRecord's
 * top-level fields, never by `data`. fromDbRow spreads the stored metadata
 * into `data` on read, so without stripping these before a write, the stale
 * read-back copies clobber the fresh top-level values in saveDocument /
 * updateDocument's `...data` spread.
 */
function stripReservedMetadataKeys(data: Record<string, unknown>): Record<string, unknown> {
  const { blockchain: _blockchain, signatures: _signatures, walletAddress: _walletAddress, ...rest } =
    data || {};
  return rest;
}

function fromDbRow(row: any): DocumentRecord {
  const meta = row.metadata || {};
  const certMeta = row.certification_metadata || {};
  return {
    id: row.external_id || row.id,
    // KS-596: canonical UUID for the registration — a UUID-shaped external_id
    // is an S-supplied documentUuid; otherwise the pkey UUID serves (it is
    // already a working lookup key via getDocument's uuid fallback).
    documentUuid: isValidUuid(row.external_id) ? row.external_id : row.id,
    type: row.document_type || 'document',
    status: mapDbStatus(row.status),
    owner: {
      id: row.owner_user_id || row.issuer_user_id || '',
      walletAddress: meta.walletAddress,
    },
    rightsHolderId: row.rights_holder_id || undefined,
    // KS-70: lifecycle-event lineage. Empty for every doc created before
    // migration 021; populated by saveDocument when callers set it.
    parentDocumentId: row.parent_document_id || undefined,
    data: {
      title: row.title,
      documentType: row.document_type,
      description: row.description,
      contentHash: row.content_hash,
      ...meta,
    },
    contentHash: row.content_hash,
    signatures: certMeta.signatures || meta.signatures || [],
    blockchain: certMeta.blockchain || meta.blockchain,
    createdAt: row.created_at?.toISOString() || new Date().toISOString(),
    updatedAt: row.updated_at?.toISOString() || new Date().toISOString(),
  };
}

function mapDbStatus(s: string): DocumentRecord['status'] {
  const map: Record<string, DocumentRecord['status']> = {
    draft: 'draft',
    pending_signature: 'pending_signature',
    pending_certification: 'pending_signature',
    signed: 'signed',
    certified: 'signed',
    anchored: 'anchored',
    revoked: 'revoked',
  };
  return map[s?.toLowerCase()] || 'draft';
}

// =============================================================================
// HELPERS
// =============================================================================

export function generateContentHash(data: Record<string, unknown>): string {
  const sorted = JSON.stringify(data, Object.keys(data).sort());
  return crypto.createHash('sha256').update(sorted).digest('hex');
}

// =============================================================================
// CRUD OPERATIONS
// =============================================================================
//
// KS-4: every read/write filters by tenant_id. The caller is required to pass
// `tenantId` (the effective tenant after extractTenantContext resolves any
// X-Tenant-Override header — i.e. req.tenantId at the route layer). The
// `documents` table has a NOT NULL `tenant_id` column and an RLS policy
// (migration 011) so this WHERE is defence-in-depth on top of the DB-layer
// policy, not a substitute for it. It also closes the leak today on call
// paths whose connection has not yet been migrated to set
// `app.current_tenant_id`.

export async function getDocument(id: string, tenantId: string, db?: DbClient): Promise<DocumentRecord | null> {
  try {
    // Try external_id first, then uuid. Both lookups are tenant-scoped:
    // a doc that exists in another tenant must return null (= 404 at the
    // route layer), not the cross-tenant body.
    let rows: any[] = await (db || prisma).$queryRaw`
      SELECT * FROM documents
       WHERE external_id = ${id}
         AND tenant_id = ${tenantId}::uuid
       LIMIT 1
    `;
    if (rows.length === 0 && isValidUuid(id)) {
      try {
        rows = await (db || prisma).$queryRaw`
          SELECT * FROM documents
           WHERE id = ${id}::uuid
             AND tenant_id = ${tenantId}::uuid
           LIMIT 1
        `;
      } catch {
        // UUID lookup failed — not found
      }
    }
    if (rows.length > 0) return fromDbRow(rows[0]);
    return null;
  } catch (err: any) {
    if (!err?.message?.includes('invalid input syntax for type uuid')) {
      logger.warn('DB read failed', { error: err instanceof Error ? err.message : String(err) });
    }
    throw err;
  }
}

export async function listDocuments(tenantId: string, filters?: {
  status?: string;
  page?: number;
  limit?: number;
}, db?: DbClient): Promise<{ items: DocumentRecord[]; total: number }> {
  try {
    const rows: any[] = await (db || prisma).$queryRaw`
      SELECT * FROM documents
       WHERE tenant_id = ${tenantId}::uuid
       ORDER BY created_at DESC
       LIMIT 200
    `;
    let all = rows.map(fromDbRow);

    if (filters?.status) {
      all = all.filter((d) => d.status === filters.status);
    }
    all.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());

    const page = filters?.page || 1;
    const limit = Math.min(filters?.limit || 50, 100);
    const offset = (page - 1) * limit;
    const paginated = all.slice(offset, offset + limit);

    return { items: paginated, total: all.length };
  } catch (err: any) {
    logger.warn('DB list failed', { error: err instanceof Error ? err.message : String(err) });
    throw err;
  }
}

/**
 * KS-597 option B: the Platform S `externalRef` the caller's OWN Organisation was
 * registered with (register-connector writes it to `organizations.metadata`), or
 * null when the Organisation has none or its row is not visible.
 *
 * Deliberately caller-scoped -- by id and request tenant -- and never a lookup by
 * ref: `metadata->>'externalRef'` carries no unique index, so a query keyed on the
 * ref could return either of two Organisations that share one.
 *
 * Pass the request's `req.db`. `organizations` is under FORCE fail-closed RLS
 * (migration 039), so with no tenant GUC this returns null for every caller. The
 * explicit `tenant_id` predicate stays for the paths RLS does not exclude (the
 * platform-admin bypass, a BYPASSRLS role), exactly as in `saveDocument` below.
 * Errors are NOT caught: the route turns them into a 500, never into an accept.
 */
export async function getOrganizationExternalRef(
  organizationId: string,
  tenantId: string,
  db?: DbClient,
): Promise<string | null> {
  if (!isValidUuid(organizationId) || !isValidUuid(tenantId)) return null;
  const rows = (await (db || prisma).$queryRaw`
    SELECT metadata->>'externalRef' AS external_ref
      FROM organizations
     WHERE id = ${organizationId}::uuid AND tenant_id = ${tenantId}::uuid
     LIMIT 1
  `) as Array<{ external_ref: string | null }>;
  return rows[0]?.external_ref ?? null;
}

export async function saveDocument(
  doc: DocumentRecord,
  tenantId: string,
  db?: DbClient,
  // KS-480 §6: a connector's onBehalfOf that resolved to a same-org K user
  // becomes the owner_user_id (true per-user attribution) — the connector's
  // own non-UUID `connector:<id>` would otherwise fold to NULL.
  opts?: {
    ownerUserIdOverride?: string;
    // KS-596: S-supplied identity fields, kept in the metadata JSON (NOT the
    // content-addressed data blob — that would change server-computed hashes).
    // KS-597: organizationUuid now ALSO gains column semantics — it is resolved
    // onto documents.issuer_organization_id below. It stays in the metadata too:
    // the column records what we could resolve, the metadata records what the
    // caller actually sent, and those differ whenever the org is unknown here.
    sIdentity?: { userUuid?: string; organizationUuid?: string };
    // KS-597: the issuing organisation the ROUTE resolved and bound to the
    // acting Organisation, or null when it could not be bound. Deliberately
    // separate from `sIdentity.organizationUuid` above: that is the caller's
    // raw claim and belongs in the metadata, this is what the row may assert.
    issuerOrganizationId?: string | null;
    // KS-596: 'skip' turns the legacy ON CONFLICT (external_id) DO UPDATE
    // into DO NOTHING. The upsert is safe for K-minted `doc-<ts>-<rand>` ids
    // (collisions don't occur in practice) but for an S-supplied documentUuid
    // it would silently MERGE a re-POST into the existing row — the ruled
    // semantics require 200-idempotent (same bytes) or 409 (different bytes),
    // decided by the caller. `inserted: false` signals the conflict raced in
    // between the caller's pre-check and this insert.
    conflictMode?: 'upsert' | 'skip';
  },
): Promise<{ dbId: string; inserted: boolean }> {
  try {
    const dbId = uuidv4();
    const skipOnConflict = opts?.conflictMode === 'skip';
    const metadata = JSON.stringify({
      ...stripReservedMetadataKeys(doc.data),
      walletAddress: doc.owner.walletAddress,
      signatures: doc.signatures,
      blockchain: doc.blockchain,
      ...(opts?.sIdentity ? { sIdentity: opts.sIdentity } : {}),
    });
    const certMeta = JSON.stringify({
      signatures: doc.signatures,
      blockchain: doc.blockchain,
    });

    const ownerUuid = opts?.ownerUserIdOverride && isValidUuid(opts.ownerUserIdOverride)
      ? opts.ownerUserIdOverride
      : (isValidUuid(doc.owner.id) ? doc.owner.id : null);

    // KS-597: resolve the issuing organisation onto its own column.
    //
    // The value arrives ALREADY BOUND to the acting Organisation -- the route
    // 403s a claim belonging to a different org and passes null when it could
    // not bind one (`routes/documents.ts`, Kam's "bind the issuer to the actor"
    // ruling of 2026-09-07). This function therefore never sees an unbound
    // claim, and the caller's raw value still reaches `metadata.sIdentity`
    // regardless, so a NULL column is recoverable rather than a data loss.
    //
    // The tenant-scoped SELECT below is kept as defence in depth rather than
    // as the only check, for three reasons -- worth stating because the live
    // column has NO foreign key to fall back on. The two provisioning paths
    // disagree: `docker/init/01-schema.sql:125` declares
    // `issuer_organization_id UUID` with no reference, while
    // `migrations/001_initial-schema.sql:105` declares
    // `REFERENCES organizations(id)`; 001's CREATE TABLE does not re-create an
    // existing table and no later migration adds the constraint, so a database
    // built the way ours are built has none. A bare insert of any 128-bit value
    // would be accepted and attributed.
    //   1. an unknown org id folds to NULL instead of writing a dangling
    //      reference that later reporting would read as attribution;
    //   2. ANOTHER TENANT's org id folds to NULL -- the `tenant_id` predicate is
    //      explicit rather than left to RLS. RLS is forced on `organizations`
    //      and the request pool does set `app.current_tenant_id`, so the policy
    //      would also exclude it; but this arm has been fail-open before now,
    //      and a cross-tenant attribution is not a thing to protect with only
    //      one mechanism whose history is what it is;
    //   3. a registration never fails HERE. Note what changed: refusing a
    //      mismatched claim is now the ROUTE's job and it is a deliberate 403,
    //      so this field CAN fail a registration -- it is authorisation, not
    //      merely attribution. What stays true is that the failure is an
    //      explicit 403 decided before the write, never a 500 out of this
    //      statement. An earlier revision of this comment said a registration
    //      "NEVER fails because of this field"; that sentence is left corrected
    //      rather than deleted, because it described the behaviour this code
    //      had before the ruling and a reader who remembers it should see why
    //      it no longer holds.
    const issuerOrgUuid = opts?.issuerOrganizationId
      && isValidUuid(opts.issuerOrganizationId)
      ? opts.issuerOrganizationId
      : null;

    // KS-70: resolve parent_document_id from the external_id callers pass.
    // The subquery returns NULL when parentExtId is null OR the parent
    // isn't in this tenant — both fold to NULL on the column, which is
    // the right shape (no FK violation, no cross-tenant lineage).
    const parentExtId = doc.parentDocumentId ?? null;

    // KS-596: one insert body, two conflict tails. `${null}::uuid` binds SQL
    // NULL, so the FK-fallback retry reuses the same statement with a null
    // owner instead of duplicating it.
    const insertOnce = async (ownerVal: string | null): Promise<number> => {
      const client = db || prisma;
      if (skipOnConflict) {
        return client.$executeRaw`
          INSERT INTO documents (
            id, external_id, tenant_id, title, description, document_type, content_hash,
            content_hash_algorithm, status, owner_user_id, issuer_organization_id, metadata,
            certification_metadata, parent_document_id, created_at, updated_at
          ) VALUES (
            ${dbId}::uuid,
            ${doc.id},
            ${tenantId}::uuid,
            ${(doc.data?.title as string) || doc.type || 'Untitled'},
            ${(doc.data?.description as string) || null},
            ${doc.type || 'document'},
            ${doc.contentHash},
            'sha256',
            ${doc.status},
            ${ownerVal}::uuid,
            (SELECT id FROM organizations WHERE id = ${issuerOrgUuid}::uuid AND tenant_id = ${tenantId}::uuid LIMIT 1),
            ${metadata}::jsonb,
            ${certMeta}::jsonb,
            (SELECT id FROM documents WHERE external_id = ${parentExtId} AND tenant_id = ${tenantId}::uuid LIMIT 1),
            NOW(),
            NOW()
          )
          ON CONFLICT (external_id) DO NOTHING
        `;
      }
      return client.$executeRaw`
        INSERT INTO documents (
          id, external_id, tenant_id, title, description, document_type, content_hash,
          content_hash_algorithm, status, owner_user_id, issuer_organization_id, metadata,
          certification_metadata, parent_document_id, created_at, updated_at
        ) VALUES (
          ${dbId}::uuid,
          ${doc.id},
          ${tenantId}::uuid,
          ${(doc.data?.title as string) || doc.type || 'Untitled'},
          ${(doc.data?.description as string) || null},
          ${doc.type || 'document'},
          ${doc.contentHash},
          'sha256',
          ${doc.status},
          ${ownerVal}::uuid,
          (SELECT id FROM organizations WHERE id = ${issuerOrgUuid}::uuid AND tenant_id = ${tenantId}::uuid LIMIT 1),
          ${metadata}::jsonb,
          ${certMeta}::jsonb,
          (SELECT id FROM documents WHERE external_id = ${parentExtId} AND tenant_id = ${tenantId}::uuid LIMIT 1),
          NOW(),
          NOW()
        )
        ON CONFLICT (external_id) DO UPDATE SET
          -- KS-597: issuer_organization_id is deliberately NOT in this list.
          -- The upsert tail exists to refresh mutable state on a re-POST; the
          -- issuing organisation is attribution fixed at registration, and
          -- tenant_id and owner_user_id are already excluded for the same
          -- reason. Re-POSTing must not let a later caller re-attribute a
          -- document that is already on the record.
          status = EXCLUDED.status,
          metadata = EXCLUDED.metadata,
          certification_metadata = EXCLUDED.certification_metadata,
          updated_at = NOW()
      `;
    };

    let affected: number;
    try {
      affected = await insertOnce(ownerUuid);
    } catch (fkErr: any) {
      const fkMsg = fkErr instanceof Error ? fkErr.message : String(fkErr);
      // If the owner user doesn't exist in this tenant's users table, retry without the FK
      if (ownerUuid && (fkMsg.includes('foreign key') || fkMsg.includes('violates') || fkMsg.includes('not present in table'))) {
        logger.warn('Owner user not in tenant DB — inserting document with null owner_user_id', { id: doc.id, ownerId: ownerUuid });
        affected = await insertOnce(null);
      } else {
        throw fkErr;
      }
    }
    // `inserted` is only meaningful in skip mode (DO UPDATE also reports 1
    // affected row); skip-mode callers use it to detect a conflict that raced
    // in between their pre-check and this insert.
    return { dbId, inserted: affected > 0 };
  } catch (err: any) {
    logger.error('DB write failed for document', { id: doc.id, error: err instanceof Error ? err.message : String(err) });
    throw err;
  }
}

export async function updateDocument(
  id: string,
  tenantId: string,
  updates: Partial<DocumentRecord>,
  db?: DbClient,
  opts?: {
    /**
     * KS-521: guard the status write against resurrecting a terminal document.
     * The async anchor pipeline (the accept-time update and the confirmation
     * poll, which runs up to 10 minutes after creation) used to write
     * `status: 'anchored'` unconditionally — stomping a `revoked` set by the
     * owner in between, so a revoked document verified again. The guard lives
     * IN the UPDATE statement (CASE), so it is atomic: a revoke landing
     * between the read above and this write still wins. Anchor/blockchain
     * metadata is still recorded either way — the anchor is factual; the
     * terminal status stays authoritative for verification.
     */
    preserveTerminalStatuses?: boolean;
    /**
     * KS-1278: refuse the write IN the UPDATE when the row's status already equals this value, so of two
     * overlapping writers exactly one changes the row. A guarded write that changed no row returns null.
     */
    ifStatusIsNot?: string;
  },
): Promise<DocumentRecord | null> {
  const doc = await getDocument(id, tenantId, db);
  if (!doc) return null;

  const updated: DocumentRecord = {
    ...doc,
    ...updates,
    updatedAt: new Date().toISOString(),
  };

  try {
    // KS-550: the reserved keys must come AFTER the data spread. fromDbRow
    // spreads the whole metadata blob into `data`, so `updated.data` carries
    // the PREVIOUS blockchain/signatures/walletAddress — spreading it last
    // clobbered every fresh `blockchain` write (the KS-535 poll/reconcile
    // updates landed in certification_metadata but were silently lost in
    // metadata, and the two blobs diverged per reader).
    const metadata = JSON.stringify({
      ...stripReservedMetadataKeys(updated.data),
      walletAddress: updated.owner.walletAddress,
      signatures: updated.signatures,
      blockchain: updated.blockchain,
    });
    const certMeta = JSON.stringify({
      signatures: updated.signatures,
      blockchain: updated.blockchain,
    });

    // Tenant-scoped UPDATE — a cross-tenant id passes through getDocument
    // above (returns null → early exit), but we still scope the UPDATE so a
    // racing tenant change can't slip a write through. Defence-in-depth.
    const preserveTerminal = opts?.preserveTerminalStatuses === true;
    // KS-1278: `ifStatusIsNot` opts exactly ONE caller into the guarded write below
    // (routes/documents.ts:2398, POST /:id/revoke). PRIOR BEHAVIOUR, and why the key moved:
    // getDocument above resolves `id` by external_id or, when `id` is UUID-shaped, by the
    // primary key (:244-:251) -- and the API hands clients that primary key as `documentUuid`
    // (:172). This UPDATE keyed on `external_id = ${id}`, so a sequential, NON-race revoke of
    // a live owned document addressed by its documentUuid matched 0 rows, `affected` was 0,
    // this returned null, and the route answered 400 "Document is already revoked" for a
    // document that was never revoked (gate65 N-1393-1, PROBED). The other 12 production
    // callers pass no `ifStatusIsNot`, take the byte-identical statement below, and do not
    // change. Their own pre-existing silent no-op on a UUID-addressed id is tracked
    // separately -- see KS-TICKET.
    const guardStatus = opts?.ifStatusIsNot ?? null;
    // KS-1278: cast ONLY when `id` really is UUID-shaped, mirroring getDocument's isValidUuid
    // guard at :244. `${x}::uuid` on a non-UUID string RAISES (22P02), which is why the read
    // wraps its uuid lookup in try/catch (:252-:254); binding null instead keeps the resolver
    // below reducible to the external_id arm, so a non-UUID external id behaves exactly as it
    // did before this change. Wednesday's ANSWER 2026-10-05T22:14:59Z made this a condition.
    const idAsUuid = isValidUuid(id) ? id : null;
    const affected = guardStatus === null
      ? await (db || prisma).$executeRaw`
      UPDATE documents SET
        status = CASE
          WHEN ${preserveTerminal}::boolean AND status IN ('revoked', 'deleted')
          THEN status
          ELSE ${updated.status}
        END,
        metadata = ${metadata}::jsonb,
        certification_metadata = ${certMeta}::jsonb,
        updated_at = NOW()
      WHERE external_id = ${id}
        AND tenant_id = ${tenantId}::uuid
        AND (${guardStatus}::text IS NULL OR status IS DISTINCT FROM ${guardStatus}::text)
    `
      : await (db || prisma).$executeRaw`
      UPDATE documents SET
        status = CASE
          WHEN ${preserveTerminal}::boolean AND status IN ('revoked', 'deleted')
          THEN status
          ELSE ${updated.status}
        END,
        metadata = ${metadata}::jsonb,
        certification_metadata = ${certMeta}::jsonb,
        updated_at = NOW()
      WHERE id = COALESCE(
              (SELECT d.id FROM documents d
                WHERE d.external_id = ${id}
                  AND d.tenant_id = ${tenantId}::uuid
                LIMIT 1),
              (SELECT d2.id FROM documents d2
                WHERE d2.id = ${idAsUuid}::uuid
                  AND d2.tenant_id = ${tenantId}::uuid
                LIMIT 1)
            )
        AND tenant_id = ${tenantId}::uuid
        AND (${guardStatus}::text IS NULL OR status IS DISTINCT FROM ${guardStatus}::text)
    `;
    // KS-1278: a guarded write that changed no row means the row's status already equalled
    // guardStatus, decided IN the UPDATE -- so of two overlapping writers exactly one changes
    // the row. PRIOR BEHAVIOUR: the already-revoked decision was taken only on the read above,
    // so both writers could pass it and both recorded a revocation.
    if (guardStatus !== null && affected === 0) return null;
  } catch (err: any) {
    logger.error('DB update failed for document', { id, error: err instanceof Error ? err.message : String(err) });
    throw err;
  }

  return updated;
}

// =============================================================================
// LINEAGE — KS-70 parent_document_id walks
// =============================================================================
//
// Verify endpoint walks `parent_document_id` recursively to surface the full
// provenance trail. Certify-with-parent walks the same chain to detect cycles
// before insert. Both share the same walker, capped at `MAX_LINEAGE_DEPTH`
// (env-configurable, default 12).
//
// The walk runs in originate's prisma context — the tenant filter on every
// step is defence-in-depth on top of the RLS policy from migration 011.

export interface LineageEntry {
  /** External-facing id (matches the `id` field on DocumentRecord). */
  id: string;
  /** Internal Postgres UUID — useful for the verify response so callers
   *  can correlate with anchoring/chain rows. */
  dbId: string;
  contentHash: string;
  documentType: string;
  status: string;
  createdAt: string;
}

/**
 * KS-70: walk a document's ancestor chain via `parent_document_id`.
 *
 * Returns the chain INCLUDING the starting document, oldest entry last.
 * Stops at the root (`parent_document_id IS NULL`) OR at
 * `MAX_LINEAGE_DEPTH` steps — at which point `truncated` is true and the
 * caller can re-query the tail with `walkAncestors(lineage[lineage.length-1].id, ...)`.
 *
 * Tenant-scoped: a parent in a different tenant is treated as a chain
 * boundary (we don't follow the FK across tenants). This shouldn't
 * happen in practice — the certify-side cycle check resolves parents
 * within the caller's tenant only — but it's defence-in-depth against
 * a future bug or a direct DB write that bypasses the route layer.
 */
export async function walkAncestors(
  startExternalId: string,
  tenantId: string,
  options?: { maxDepth?: number; db?: DbClient },
): Promise<{ lineage: LineageEntry[]; truncated: boolean }> {
  const maxDepth = options?.maxDepth ?? MAX_LINEAGE_DEPTH;
  const db = options?.db || prisma;
  const lineage: LineageEntry[] = [];
  let cursor: string | null = startExternalId;
  // Belt-and-braces cycle guard: even though insert-time `assertNoCycle`
  // prevents loops, a corrupt row written outside the route layer could
  // produce one. Stop on revisit.
  const seen = new Set<string>();

  for (let step = 0; step < maxDepth && cursor; step++) {
    if (seen.has(cursor)) break;
    seen.add(cursor);

    const rows: Array<{
      id: string;
      external_id: string | null;
      content_hash: string;
      document_type: string;
      status: string;
      created_at: Date;
      parent_external_id: string | null;
    }> = await db.$queryRaw`
      SELECT
        d.id::text AS id,
        d.external_id,
        d.content_hash,
        d.document_type,
        d.status,
        d.created_at,
        p.external_id AS parent_external_id
       FROM documents d
       LEFT JOIN documents p ON p.id = d.parent_document_id AND p.tenant_id = ${tenantId}::uuid
       WHERE d.external_id = ${cursor}
         AND d.tenant_id = ${tenantId}::uuid
       LIMIT 1
    `;
    if (rows.length === 0) break;

    const row = rows[0];
    lineage.push({
      id: row.external_id || row.id,
      dbId: row.id,
      contentHash: row.content_hash,
      documentType: row.document_type,
      status: row.status,
      createdAt: row.created_at?.toISOString?.() || String(row.created_at),
    });

    cursor = row.parent_external_id ?? null;
  }

  // truncated is true if we hit the cap with a non-null cursor still
  // pending (i.e. there's at least one more ancestor we didn't walk).
  return { lineage, truncated: cursor !== null && lineage.length >= maxDepth };
}

/**
 * KS-280: walk a document's DESCENDANT tree via `parent_document_id` (the
 * inverse of walkAncestors). Given a document, finds every newer/derived
 * version whose parent chain leads back to it, so the verify endpoint can
 * flag — when presenting an older version — that a newer (and possibly
 * certified) version exists. Lineage branches (one source can spawn several
 * versions), so this is a breadth-first tree walk, not a linear chain.
 *
 * Bounded by `maxNodes` (total descendants collected) to keep the verify
 * path cheap; `truncated` signals the tree was larger than the cap. Tenant-
 * scoped and revisit-guarded like walkAncestors.
 */
export async function walkDescendants(
  startExternalId: string,
  tenantId: string,
  options?: { maxNodes?: number; db?: DbClient },
): Promise<{ descendants: LineageEntry[]; truncated: boolean }> {
  const maxNodes = options?.maxNodes ?? MAX_LINEAGE_DEPTH * 8;
  const db = options?.db || prisma;
  const descendants: LineageEntry[] = [];

  // Children reference the parent via its internal UUID (`parent_document_id`),
  // not its external_id — resolve the start doc's internal id first.
  const startRows: Array<{ id: string }> = await db.$queryRaw`
    SELECT id::text AS id FROM documents
     WHERE external_id = ${startExternalId} AND tenant_id = ${tenantId}::uuid
     LIMIT 1
  `;
  if (startRows.length === 0) return { descendants: [], truncated: false };

  const seen = new Set<string>([startRows[0].id]);
  const queue: string[] = [startRows[0].id];
  let truncated = false;

  while (queue.length > 0) {
    const parentDbId = queue.shift() as string;
    const children: Array<{
      id: string;
      external_id: string | null;
      content_hash: string;
      document_type: string;
      status: string;
      created_at: Date;
    }> = await db.$queryRaw`
      SELECT d.id::text AS id, d.external_id, d.content_hash,
             d.document_type, d.status, d.created_at
        FROM documents d
       WHERE d.parent_document_id = ${parentDbId}::uuid
         AND d.tenant_id = ${tenantId}::uuid
       ORDER BY d.created_at ASC
    `;
    for (const row of children) {
      if (seen.has(row.id)) continue;
      seen.add(row.id);
      if (descendants.length >= maxNodes) {
        truncated = true;
        break;
      }
      descendants.push({
        id: row.external_id || row.id,
        dbId: row.id,
        contentHash: row.content_hash,
        documentType: row.document_type,
        status: row.status,
        createdAt: row.created_at?.toISOString?.() || String(row.created_at),
      });
      queue.push(row.id);
    }
    if (truncated) break;
  }

  return { descendants, truncated };
}

/**
 * KS-70: assert that adopting `proposedParentExternalId` as the parent of
 * `newExternalId` would NOT create a cycle (i.e. `newExternalId` does not
 * appear in the proposed parent's ancestor chain within `MAX_LINEAGE_DEPTH`
 * steps).
 *
 * Throws an error tagged `LINEAGE_CYCLE` for the route layer to catch and
 * translate to a 422 response.
 *
 * Returns the resolved ancestor chain on success — saves the route handler
 * from a second walk if it wants to log lineage depth.
 */
export async function assertNoCycle(
  newExternalId: string,
  proposedParentExternalId: string,
  tenantId: string,
  options?: { maxDepth?: number; db?: DbClient },
): Promise<LineageEntry[]> {
  const { lineage } = await walkAncestors(proposedParentExternalId, tenantId, options);
  for (const entry of lineage) {
    if (entry.id === newExternalId) {
      const err = new Error(
        `LINEAGE_CYCLE: ${newExternalId} appears in the ancestor chain of ${proposedParentExternalId}`,
      );
      (err as { code?: string }).code = 'LINEAGE_CYCLE';
      throw err;
    }
  }
  return lineage;
}

// =============================================================================
// SIGNING REQUESTS (in-memory only — these are short-lived nonces)
// =============================================================================

export function getSigningRequest(nonce: string): SigningRequest | undefined {
  return memSigningRequests.get(nonce);
}

export function saveSigningRequest(nonce: string, req: SigningRequest): void {
  memSigningRequests.set(nonce, req);
}

export function deleteSigningRequest(nonce: string): void {
  memSigningRequests.delete(nonce);
}

// =============================================================================
// SEED DATA
// =============================================================================

export async function seedDemoDocuments(): Promise<void> {
  if (process.env.NODE_ENV === 'production') return;

  // Seed documents belong to the default tenant (the same id that
  // extractTenantContext falls back to in non-prod when no x-tenant-id
  // header is present). Keep these in sync.
  const SEED_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';

  const pastDate = (daysAgo: number) =>
    new Date(Date.now() - daysAgo * 86_400_000).toISOString();

  const demoOwner = {
    id: 'a0000000-0000-4000-8000-000000000010',
    walletAddress: undefined as string | undefined,
  };

  const seeds: DocumentRecord[] = [
    {
      id: 'doc-demo-degree-001',
      type: 'degree',
      status: 'anchored',
      owner: demoOwner,
      data: {
        title: '[Demo] BSc Computer Science — University of Oxford',
        documentType: 'degree',
        description: 'Sample seed document — undergraduate degree certificate',
        contentHash: 'sha256:4f7a8c2e9b1d3f5a7c9e1b3d5f7a9c1e3b5d7f9a1c3e5b7d9f1a3c5e7b9d1f',
      },
      contentHash: 'sha256:4f7a8c2e9b1d3f5a7c9e1b3d5f7a9c1e3b5d7f9a1c3e5b7d9f1a3c5e7b9d1f',
      signatures: [
        {
          signerId: demoOwner.id,
          walletAddress: 'addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj83ws8lhrn648jjxtwq2ytjqp',
          signature: 'ed25519_sig_demo_1',
          signedAt: pastDate(5),
        },
      ],
      blockchain: {
        txHash: '8f3b2c1a4e5d6f7089ab1cd2ef3456789012abcdef3456789012abcdef345678',
        blockHeight: 1024576,
        anchoredAt: pastDate(4),
      },
      createdAt: pastDate(7),
      updatedAt: pastDate(4),
    },
    {
      id: 'doc-demo-transcript-002',
      type: 'transcript',
      status: 'anchored',
      owner: demoOwner,
      data: {
        title: '[Demo] Academic Transcript — 2022-2025',
        documentType: 'transcript',
        description: 'Sample seed document — academic transcript with module grades',
        contentHash: 'sha256:a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1',
      },
      contentHash: 'sha256:a2b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1',
      signatures: [
        {
          signerId: demoOwner.id,
          walletAddress: 'addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj83ws8lhrn648jjxtwq2ytjqp',
          signature: 'ed25519_sig_demo_2',
          signedAt: pastDate(3),
        },
      ],
      blockchain: {
        txHash: 'b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1',
        blockHeight: 1024590,
        anchoredAt: pastDate(2),
      },
      createdAt: pastDate(5),
      updatedAt: pastDate(2),
    },
    {
      id: 'doc-demo-certificate-003',
      type: 'certificate',
      status: 'anchored',
      owner: demoOwner,
      data: {
        title: '[Demo] Professional Certification — AWS Solutions Architect',
        documentType: 'certificate',
        description: 'Sample seed document — cloud computing professional certification',
        contentHash: 'sha256:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a',
      },
      contentHash: 'sha256:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a',
      signatures: [
        {
          signerId: demoOwner.id,
          walletAddress: 'addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj83ws8lhrn648jjxtwq2ytjqp',
          signature: 'ed25519_sig_demo_3',
          signedAt: pastDate(1),
        },
      ],
      blockchain: {
        txHash: 'c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2',
        blockHeight: 1024605,
        anchoredAt: pastDate(1),
      },
      createdAt: pastDate(1),
      updatedAt: pastDate(1),
    },
    {
      // KS-481: the CANONICAL OpenAPI example document. Every document-id
      // example in the published spec (formerly the volatile
      // doc-1777346021120-1e528170, which 404'd after any DB reset) points at
      // this id, so exampled routes resolve on a fresh stack and partners can
      // copy examples out of Swagger UI that actually work. The id is
      // format-shaped (doc-<ms>-<8hex>) but honestly synthetic: a 13-zero
      // "timestamp" (epoch 0 — no real id can carry it) and hexspeak
      // "5eeded0c" (~"seeded"). Keep in sync with the spec examples and, once
      // KS-256 lands, with FX.document.id in
      // packages/shared/src/openapi/example-fixtures.ts. contentHash =
      // sha256('secuura-canonical-openapi-example-document').
      id: 'doc-0000000000000-5eeded0c',
      type: 'document',
      status: 'anchored',
      owner: demoOwner,
      data: {
        title: '[Spec] Canonical OpenAPI example document',
        documentType: 'document',
        description:
          'Deterministic seed document referenced by the published OpenAPI examples (KS-481). Do not delete — spec runnability depends on it.',
        contentHash: 'sha256:19b24e77f70f6ea2fe18f8e9ee00859e64f65c95e5abae6086c01f9cec1a0730',
      },
      contentHash: 'sha256:19b24e77f70f6ea2fe18f8e9ee00859e64f65c95e5abae6086c01f9cec1a0730',
      signatures: [
        {
          signerId: demoOwner.id,
          walletAddress: 'addr_test1qz2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj83ws8lhrn648jjxtwq2ytjqp',
          signature: 'ed25519_sig_demo_canonical',
          signedAt: pastDate(2),
        },
      ],
      blockchain: {
        txHash: 'd4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4',
        blockHeight: 1024610,
        anchoredAt: pastDate(1),
      },
      createdAt: pastDate(2),
      updatedAt: pastDate(1),
    },
  ];

  // KS-458 residual: the boot-time seed runs outside any request scope, so
  // the tenant-GUC proxy passed the INSERT through bare and fail-closed RLS
  // (migration 039) rejected it with 42501 on every boot. Wrap the writes in
  // an explicit tenant scope so a fresh database seeds correctly.
  await runWithTenantId(SEED_TENANT_ID, async () => {
    for (const doc of seeds) {
      await saveDocument(doc, SEED_TENANT_ID);
    }
  });

  logger.info('Demo documents loaded', { count: seeds.length, tenantId: SEED_TENANT_ID, note: 'non-production only, titles prefixed with [Demo]' });
}

// =============================================================================
// UTILS
// =============================================================================

function isValidUuid(s: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(s);
}
