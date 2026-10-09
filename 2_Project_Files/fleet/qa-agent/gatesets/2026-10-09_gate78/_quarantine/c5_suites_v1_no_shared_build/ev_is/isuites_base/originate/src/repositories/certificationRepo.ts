/**
 * =============================================================================
 * CERTIFICATION REPOSITORY
 * =============================================================================
 * Persistence layer for certifications using raw SQL queries that match
 * the actual database column names. Database is the single source of truth.
 * =============================================================================
 */

import { prisma } from '../db';

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
    logger.error('certificationRepo: database connection FAILED — certifications will not be available', {
      error: err instanceof Error ? err.message : String(err),
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
    logger.warn('DB list failed', { error: err instanceof Error ? err.message : String(err) });
    throw err;
  }
}

export async function saveCertification(cert: Certification, tenantId: string, db?: DbClient): Promise<Certification> {
  try {
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
        ${cert.holder.id}::uuid,
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
    logger.warn('Failed to fetch shares from DB', { error: err instanceof Error ? err.message : String(err) });
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
