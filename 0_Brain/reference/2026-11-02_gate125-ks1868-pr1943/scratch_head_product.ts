/**
 * =============================================================================
 * CERTIFICATION REPOSITORY
 * =============================================================================
 * Persistence layer for certifications using raw SQL queries that match
 * the actual database column names. Database is the single source of truth.
 * =============================================================================
 */

import { prisma, withTenant} from '../db';

type DbClient = typeof prisma;
import { v4 as uuidv4 } from 'uuid';
import { logger } from '../utils/logger';
import { toActorUuid } from '../utils/principalId';

// The route-level interface (kept for backward-compatibility)
export interface Certification {
  id: string;
  type: string;
  status: 'issued' | 'pending' | 'revoked' | 'expired';
  issuer: { id: string; did?: string; name?: string };
  holder: { id: string; did?: string; name?: string };
  data: Record<string, unknown>;
  privacySettings?: {
    defaultVisibility: 'public' | 'authenticated' | 'authorized' | 'private' | 'zkp_only';
    fieldOverrides?: Array<{ field: string; visibility: string }>;
  };
  issuedAt: string;
  expiresAt?: string;
  revokedAt?: string;
  revocationReason?: string;
  blockchain?: { txHash: string; blockHeight: number; anchoredAt: string };
  contentHash: string;
  createdAt: string;
  updatedAt: string;
}

export interface ShareRecord {
  id: string;
  certificationId: string;
  toEmail: string;
  toName?: string;
  shareType: string;
  sharedBy: string;
  timestamp: string;
  status: string;
}

// =============================================================================
// DB READINESS CHECK
// =============================================================================

export async function verifyDbReady(db?: DbClient): Promise<void> {
  try {
    await (db || prisma).$queryRaw`SELECT 1`;
    logger.info('certificationRepo: database connection verified');
  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('certificationRepo: database connection FAILED — certifications will not be available', {
      error: reason,
    });
    throw new Error('Database is required for certification operations');
  }
}

// Convert DB row → Certification interface
function fromDbRow(row: any): Certification {
  const meta = row.metadata || {};
  const certMeta = row.certification_metadata || {};
  return {
    id: row.id,
    type: certMeta.certificationType || meta.certificationType || row.document_type || 'certificate',
    status: mapDbStatus(row.status),
    issuer: {
      id: row.issuer_user_id || certMeta.issuerId || '',
      name: certMeta.issuerName || meta.issuerName,
      did: certMeta.issuerDid || meta.issuerDid,
    },
    holder: {
      id: row.owner_user_id || certMeta.holderId || '',
      name: certMeta.holderName || meta.holderName,
      did: row.owner_did || certMeta.holderDid || meta.holderDid,
    },
    data: certMeta.certificationData || meta.certificationData || {},
    privacySettings: certMeta.privacySettings || meta.privacySettings,
    issuedAt: row.certified_at?.toISOString() || row.created_at?.toISOString() || new Date().toISOString(),
    expiresAt: row.expires_at?.toISOString(),
    revokedAt: certMeta.revokedAt,
    revocationReason: certMeta.revocationReason,
    blockchain: certMeta.blockchain || meta.blockchain,
    contentHash: row.content_hash,
    createdAt: row.created_at?.toISOString() || new Date().toISOString(),
    updatedAt: row.updated_at?.toISOString() || new Date().toISOString(),
  };
}

function mapDbStatus(s: string): Certification['status'] {
  const map: Record<string, Certification['status']> = {
    draft: 'pending',
    pending_certification: 'pending',
    certified: 'issued',
    revoked: 'revoked',
    expired: 'expired',
  };
  return map[s?.toLowerCase()] || 'pending';
}

function toDbStatus(s: Certification['status']): string {
  const map: Record<string, string> = {
    issued: 'certified',
    pending: 'pending_certification',
    revoked: 'revoked',
    expired: 'expired',
  };
  return map[s] || 'draft';
}

// =============================================================================
// CERTIFICATION CRUD
// =============================================================================
//
// KS-22 (KS-4 phase 5b): every read/write filters by tenant_id. Originate's
// "certifications" are persisted as rows in the `documents` table (with
// `document_type` markers + certification-specific metadata), so the tenant
// scope is enforced via documents.tenant_id (added in migration 011). The
// caller passes the effective tenant after extractTenantContext resolves any
// X-Tenant-Override (i.e. req.tenantId at the route layer).

/**
 * KS-1633: remove a certification this request wrote moments ago, tenant-scoped.
 *
 * Used for ONE purpose: the certify route now writes its `documents` row BEFORE it anchors, so that a failure of
 * that write can never leave an `anchor_store` row naming no document. The one refusal that sits between the two
 * steps — production with anchoring unavailable — must keep its "nothing was written" contract, so the row is
 * compensated away before the 503. Every child of a fresh certification row cascades (`certification_events`,
 * `share_records`, `verification_requests` are all ON DELETE CASCADE; measured), so one DELETE is enough.
 *
 * It is deliberately NOT a general certification delete: it is keyed by id AND tenant, it returns the row count so
 * the caller can tell a miss from a removal, and it does not touch `anchor_store` (the anchor is the other
 * service's row). `verifiable_credentials.document_id` is ON DELETE NO ACTION, so a certification that has since
 * grown a credential would refuse here rather than cascade — the caller handles a throw, it does not swallow it.
 */
export async function deleteCertification(id: string, tenantId: string, pool?: { connect: () => Promise<any> }): Promise<number> {
  // Through `withTenant`, not a bare client: `documents` is FORCE RLS under the `tenant_isolation` policy, whose
  // USING clause reads the TRANSACTION-LOCAL GUC `app.current_tenant_id` (set_config(..., true)). A DELETE issued
  // outside that transaction matches **0 rows and raises nothing** — measured on a migrated scratch database as
  // `secuura_app`: `DELETE 0` with the row still present, and `DELETE 1` with the GUC set. So a compensating
  // delete written the obvious way would silently remove nothing and still look like success. `withTenant` sets
  // both `app.tenant_id` and `app.current_tenant_id` in one transaction (KS-458), which is what the policy needs.
  //
  // The row COUNT is returned rather than discarded so the caller can tell a removal from a no-op; the caller
  // treats anything but 1 as a failed compensation. Every child of a fresh certification cascades
  // (`certification_events`, `share_records`, `verification_requests`; measured), so one DELETE is enough, while
  // `verifiable_credentials.document_id` is ON DELETE NO ACTION — a certification that has since grown a
  // credential throws here rather than cascading, and the caller handles the throw instead of swallowing it.
  // The REQUEST's pool, when it has one (gate AI1 note N4): under multi-tenancy with a separate database per
  // tenant the default pool is a different database from the one the write went to, so the delete would look for
  // the row in the wrong place and remove nothing. Without a pool this is exactly the previous behaviour.
  return withTenant(tenantId, async (tx) => Number(await tx.$executeRaw`
    DELETE FROM documents WHERE id = ${id}::uuid AND tenant_id = ${tenantId}::uuid
  `), pool ? { pool } : undefined);
}

export async function getCertification(id: string, tenantId: string, db?: DbClient): Promise<Certification | null> {
  try {
    const rows: any[] = await (db || prisma).$queryRaw`
      SELECT * FROM documents
       WHERE id = ${id}::uuid
         AND tenant_id = ${tenantId}::uuid
       LIMIT 1
    `;
    if (rows.length > 0) return fromDbRow(rows[0]);
    return null;
  } catch (err: any) {
    if (!err?.message?.includes('invalid input syntax for type uuid')) {
      logger.warn('DB read failed', { error: err instanceof Error ? err.message : String(err) });
    }
    throw err;
  }
}

export async function listCertifications(tenantId: string, _filters?: {
  issuerId?: string;
  holderId?: string;
  status?: string;
  type?: string;
  page?: number;
  limit?: number;
}, db?: DbClient): Promise<{ items: Certification[]; total: number }> {
  try {
    const rows: any[] = await (db || prisma).$queryRaw`
      SELECT * FROM documents
       WHERE tenant_id = ${tenantId}::uuid
       ORDER BY created_at DESC
       LIMIT 100
    `;
    const all = rows.map(fromDbRow);
    return { items: all, total: all.length };
  } catch (err: any) {
    let reason: string;
    try {
      reason = String(err instanceof Error ? err.message : err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('DB list failed', { error: reason });
    throw err;
  }
}

/**
 * The ROW half of a certification write — the single `INSERT INTO documents` for a certification, shared so that
 * nothing can drift. `saveCertification` calls it and then writes the certification_events row; KS-1633's
 * `reserveCertificationRow` calls it and writes no event. There is exactly ONE statement in this file that
 * inserts a certification's document row, and both callers go through it.
 */
async function insertCertificationRow(cert: Certification, tenantId: string, db?: DbClient): Promise<void> {
  const certMeta = JSON.stringify({
    certificationType: cert.type,
    certificationData: cert.data,
    issuerId: cert.issuer.id,
    issuerName: cert.issuer.name,
    issuerDid: cert.issuer.did,
    holderId: cert.holder.id,
    holderName: cert.holder.name,
    holderDid: cert.holder.did,
    privacySettings: cert.privacySettings,
    blockchain: cert.blockchain,
    revokedAt: cert.revokedAt,
    revocationReason: cert.revocationReason,
  });

  // KS-564: the issuer may be a connector principal (`connector:platform-s:<ref>`),
  // which is not a UUID and cannot go in `issuer_user_id` / `actor_user_id`.
  // Fold it exactly as the /share and /lifecycle-events paths do; the raw
  // principal is still carried in `certification_metadata.issuerId` above, so
  // connector attribution survives the fold.
  const issuerUserId = toActorUuid(cert.issuer.id);

  // Upsert using raw SQL — tenant_id is the security boundary (migration
  // 011 made it NOT NULL). The ON CONFLICT branch intentionally does NOT
  // update tenant_id: a doc's home tenant is fixed at creation, and a
  // racing cross-tenant write would silently change ownership otherwise.
  await (db || prisma).$executeRaw`
    INSERT INTO documents (id, tenant_id, title, document_type, content_hash, content_hash_algorithm, status,
                           issuer_user_id, owner_user_id, owner_did, metadata, certification_metadata,
                           certified_at, expires_at, created_at, updated_at)
    VALUES (
      ${cert.id}::uuid,
      ${tenantId}::uuid,
      ${(cert.data as any).title || `Certification ${cert.id.slice(0, 8)}`},
      ${cert.type},
      ${cert.contentHash},
      ${'SHA-256'},
      ${toDbStatus(cert.status)},
      ${issuerUserId}::uuid,
      ${toActorUuid(cert.holder.id)}::uuid,
      ${cert.holder.did || null},
      ${JSON.stringify({})}::jsonb,
      ${certMeta}::jsonb,
      ${cert.issuedAt ? new Date(cert.issuedAt) : new Date()},
      ${cert.expiresAt ? new Date(cert.expiresAt) : null},
      ${new Date()},
      ${new Date()}
    )
    ON CONFLICT (id) DO UPDATE SET
      status = EXCLUDED.status,
      certification_metadata = EXCLUDED.certification_metadata,
      updated_at = NOW()
    WHERE documents.tenant_id = ${tenantId}::uuid
  `;
}

/**
 * KS-1633: write a certification's `documents` row WITHOUT its certification_events row.
 *
 * The certify route writes the row BEFORE it anchors, so that a failure of the write can never leave an
 * `anchor_store` row naming no document. Only the AUTHORITATIVE save afterwards writes the event, so an accepted
 * certification still ends with exactly ONE ISSUE event, as it does without this reservation — which is why this
 * is a separate entry point rather than a flag on `saveCertification`, whose contract is unchanged.
 *
 * It shares `insertCertificationRow` with `saveCertification`, so the reservation and the authoritative write
 * cannot disagree about columns, casts or the ON CONFLICT tail.
 */
export async function reserveCertificationRow(cert: Certification, tenantId: string, db?: DbClient): Promise<void> {
  await insertCertificationRow(cert, tenantId, db);
}

export async function saveCertification(cert: Certification, tenantId: string, db?: DbClient): Promise<Certification> {
  try {
    await insertCertificationRow(cert, tenantId, db);

    // KS-564 fold, recomputed here for the event row: see insertCertificationRow for why.
    const issuerUserId = toActorUuid(cert.issuer.id);

    // Record certification event in provenance chain
    const eventId = uuidv4();
    const eventType = cert.status === 'revoked' ? 'REVOKE_DOCUMENT' : 'ISSUE';
    await (db || prisma).$executeRaw`
      INSERT INTO certification_events (id, document_id, event_type, event_hash, actor_user_id, details, created_at)
      VALUES (
        ${eventId}::uuid,
        ${cert.id}::uuid,
        ${eventType},
        ${cert.contentHash},
        ${issuerUserId}::uuid,
        ${JSON.stringify({ status: cert.status, blockchain: cert.blockchain })}::jsonb,
        ${new Date()}
      )
    `;
  } catch (err: any) {
    // If IDs aren't valid UUIDs (e.g., "cert-1234..."), log and re-throw
    if (!err?.message?.includes('invalid input syntax for type uuid')) {
      logger.error('Failed to persist certification to DB', { error: err instanceof Error ? err.message : String(err) });
    }
    throw err;
  }

  return cert;
}

// =============================================================================
// SHARE RECORDS
// =============================================================================

export async function saveShare(share: ShareRecord, db?: DbClient): Promise<ShareRecord> {
  try {
    await (db || prisma).$executeRaw`
      INSERT INTO share_records (id, document_id, to_email, to_name, share_type, shared_by_id, status, timestamp, created_at, updated_at)
      VALUES (
        ${share.id}::uuid,
        ${share.certificationId}::uuid,
        ${share.toEmail},
        ${share.toName || null},
        ${share.shareType},
        ${share.sharedBy},
        ${share.status},
        ${new Date(share.timestamp)},
        ${new Date()},
        ${new Date()}
      )
    `;

    // Also record a certification event
    const eventId = uuidv4();
    await (db || prisma).$executeRaw`
      INSERT INTO certification_events (id, document_id, event_type, event_hash, actor_user_id, details, created_at)
      VALUES (
        ${eventId}::uuid,
        ${share.certificationId}::uuid,
        ${'SHARE'},
        ${'share_' + share.id},
        ${share.sharedBy}::uuid,
        ${JSON.stringify({ toEmail: share.toEmail, toName: share.toName, shareType: share.shareType })}::jsonb,
        ${new Date(share.timestamp)}
      )
    `;
  } catch (err: any) {
    if (!err?.message?.includes('invalid input syntax for type uuid')) {
      logger.error('Failed to persist share to DB', { error: err instanceof Error ? err.message : String(err) });
    }
    throw err;
  }

  return share;
}

export async function getSharesByCertification(certificationId: string, db?: DbClient): Promise<ShareRecord[]> {
  try {
    const rows: any[] = await (db || prisma).$queryRaw`
      SELECT * FROM share_records WHERE document_id = ${certificationId}::uuid ORDER BY timestamp ASC
    `;
    return rows.map((r) => ({
      id: r.id,
      certificationId: r.document_id,
      toEmail: r.to_email,
      toName: r.to_name,
      shareType: r.share_type,
      sharedBy: r.shared_by_id,
      timestamp: r.timestamp?.toISOString() || r.created_at?.toISOString(),
      status: r.status,
    }));
  } catch (err: any) {
    let reason: string;
    try {
      reason = String(err instanceof Error ? err.message : err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('Failed to fetch shares from DB', { error: reason });
    throw err;
  }
}

export async function getLineageEvents(certificationId: string, db?: DbClient): Promise<any[]> {
  try {
    return await (db || prisma).$queryRaw`
      SELECT * FROM certification_events WHERE document_id = ${certificationId}::uuid ORDER BY created_at ASC
    `;
  } catch {
    return [];
  }
}

// =============================================================================
// INITIALIZE
// =============================================================================

export async function initRepo(): Promise<void> {
  await verifyDbReady();
  logger.info('certificationRepo initialized — database is source of truth');
}
