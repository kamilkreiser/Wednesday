/**
 * =============================================================================
 * SHARE REPOSITORY — KS-67 polymorphic shares
 * =============================================================================
 * Persistence for the new `shares` table that handles both document- and
 * certification-targeted shares behind a single discriminator column.
 *
 * Coexists with the legacy `share_records` table (which only holds
 * certification shares today). The existing `POST /api/certifications/:id/share`
 * route keeps writing to `share_records`; this repo backs the new
 * `POST /api/documents/:id/share` route and any future polymorphic readers.
 * A follow-up ticket will back-fill `share_records` rows into `shares`
 * and retire the legacy table.
 *
 * RLS on `shares` mirrors migration 022 (Phase-1 permissive shape with
 * app.current_tenant_id GUC); the route layer additionally passes
 * tenantId to every helper as defence-in-depth.
 * =============================================================================
 */

import { prisma, type TenantTx } from '../db';
import { v4 as uuidv4 } from 'uuid';
import { logger } from '../utils/logger';

type DbClient = typeof prisma;

export type ShareTargetType = 'document' | 'certification';
export type ShareType = 'view' | 'verify' | 'reshare';

export interface ShareRecordV2 {
  id: string;
  tenantId: string;
  targetType: ShareTargetType;
  /** External-facing target id. For documents we resolve to the documents.id
   *  UUID via a tenant-scoped subquery; for certifications we expect a UUID
   *  already (the existing certs flow uses uuidv4 ids end-to-end). */
  targetId: string;
  recipientUserId?: string | null;
  recipientEmail?: string | null;
  shareType: ShareType;
  /** KS-564: null for a connector (`sk_*`) caller with no onBehalfOf-resolved
   *  user — a connector principal (`connector:<platform>:<id>`) is not a UUID
   *  and the column is a UUID. Attribution lives on `action_provenance`. */
  sharedById: string | null;
  status: 'active' | 'revoked';
  expiresAt?: string | null;
  message?: string | null;
  createdAt: string;
  updatedAt: string;
  revokedAt?: string | null;
}

/**
 * Insert a new share row.
 *
 * - When `targetType === 'document'` and `targetId` is an external_id
 *   (the `doc-<ts>-<random>` shape), we resolve to the underlying
 *   `documents.id` UUID via a tenant-scoped subquery. This keeps the
 *   foreign-key story clean and prevents cross-tenant share leakage.
 * - When `targetType === 'certification'` we expect `targetId` to be a
 *   UUID already (the cert flow generates `uuidv4()` ids and stores
 *   them verbatim).
 *
 * Throws if neither `recipientUserId` nor `recipientEmail` is set
 * (matches the CHECK constraint in migration 022 — fail fast at the
 * app layer rather than waiting for the DB to reject).
 */
export async function createShare(
  input: Omit<ShareRecordV2, 'id' | 'createdAt' | 'updatedAt' | 'status'> & {
    status?: ShareRecordV2['status'];
  },
  // KS-1263: `/share` now runs the per-recipient loop inside withTenant(), whose client is a
  // TenantTx — the four raw methods without `$disconnect`. This function only ever calls
  // `$executeRaw` (twice), so TenantTx satisfies everything it uses. Widened here only;
  // the other two signatures in this file are untouched.
  db?: DbClient | TenantTx,
): Promise<ShareRecordV2> {
  if (!input.recipientUserId && !input.recipientEmail) {
    throw new Error('createShare: at least one of recipientUserId or recipientEmail is required');
  }

  const id = uuidv4();
  const now = new Date();
  const status: ShareRecordV2['status'] = input.status ?? 'active';

  const expires = input.expiresAt ? new Date(input.expiresAt) : null;

  // For document targets the INSERT below resolves the external_id →
  // documents.id UUID in a tenant-scoped subquery. For certification
  // targets it writes the supplied UUID verbatim.
  try {
    if (input.targetType === 'document') {
      await (db || prisma).$executeRaw`
        INSERT INTO shares (
          id, tenant_id, target_type, target_id,
          recipient_user_id, recipient_email, share_type,
          shared_by_id, status, expires_at, message,
          created_at, updated_at
        ) VALUES (
          ${id}::uuid,
          ${input.tenantId}::uuid,
          ${input.targetType},
          (SELECT id FROM documents WHERE external_id = ${input.targetId} AND tenant_id = ${input.tenantId}::uuid LIMIT 1),
          ${input.recipientUserId ?? null}::uuid,
          ${input.recipientEmail ?? null},
          ${input.shareType},
          ${input.sharedById ?? null}::uuid,
          ${status},
          ${expires},
          ${input.message ?? null},
          ${now},
          ${now}
        )
      `;
    } else {
      await (db || prisma).$executeRaw`
        INSERT INTO shares (
          id, tenant_id, target_type, target_id,
          recipient_user_id, recipient_email, share_type,
          shared_by_id, status, expires_at, message,
          created_at, updated_at
        ) VALUES (
          ${id}::uuid,
          ${input.tenantId}::uuid,
          ${input.targetType},
          ${input.targetId}::uuid,
          ${input.recipientUserId ?? null}::uuid,
          ${input.recipientEmail ?? null},
          ${input.shareType},
          ${input.sharedById ?? null}::uuid,
          ${status},
          ${expires},
          ${input.message ?? null},
          ${now},
          ${now}
        )
      `;
    }
  } catch (err: any) {
    const msg = err instanceof Error ? err.message : String(err);
    if (msg.includes('null value in column "target_id"')) {
      // Subquery returned no row — document not in this tenant.
      const friendlyErr: Error & { code?: string } = new Error(
        `Share target ${input.targetId} not found in tenant ${input.tenantId}`,
      );
      friendlyErr.code = 'SHARE_TARGET_NOT_FOUND';
      throw friendlyErr;
    }
    logger.error('createShare failed', { targetType: input.targetType, error: msg });
    throw err;
  }

  return {
    id,
    tenantId: input.tenantId,
    targetType: input.targetType,
    targetId: input.targetId,
    recipientUserId: input.recipientUserId ?? null,
    recipientEmail: input.recipientEmail ?? null,
    shareType: input.shareType,
    sharedById: input.sharedById,
    status,
    expiresAt: input.expiresAt ?? null,
    message: input.message ?? null,
    createdAt: now.toISOString(),
    updatedAt: now.toISOString(),
    revokedAt: null,
  };
}

/**
 * Convenience wrapper for keeping the cleanup path readable. Sets
 * status='revoked' + revoked_at=NOW(). No-op (returns false) if the
 * row doesn't exist or is already revoked.
 */
export async function revokeShare(
  shareId: string,
  tenantId: string,
  db?: DbClient,
): Promise<boolean> {
  const result = await (db || prisma).$executeRaw`
    UPDATE shares
       SET status = 'revoked', revoked_at = NOW(), updated_at = NOW()
     WHERE id = ${shareId}::uuid
       AND tenant_id = ${tenantId}::uuid
       AND status <> 'revoked'
  `;
  return result > 0;
}

/**
 * List shares for a given (target_type, target_id) pair within a
 * tenant. The `target_id` lookup honours the same external-id →
 * UUID resolution used in `createShare`. Returns newest first.
 */
export async function listSharesForTarget(
  targetType: ShareTargetType,
  targetId: string,
  tenantId: string,
  db?: DbClient,
): Promise<ShareRecordV2[]> {
  const rows: any[] = await (db || prisma).$queryRaw`
    SELECT
      s.id::text AS id,
      s.tenant_id::text AS tenant_id,
      s.target_type,
      s.target_id::text AS target_id,
      s.recipient_user_id::text AS recipient_user_id,
      s.recipient_email,
      s.share_type,
      s.shared_by_id::text AS shared_by_id,
      s.status,
      s.expires_at,
      s.message,
      s.created_at,
      s.updated_at,
      s.revoked_at
     FROM shares s
     WHERE s.target_type = ${targetType}
       AND s.tenant_id = ${tenantId}::uuid
       AND (
         s.target_id::text = ${targetId}
         OR s.target_id IN (
           SELECT id FROM documents
            WHERE external_id = ${targetId}
              AND tenant_id = ${tenantId}::uuid
         )
       )
     ORDER BY s.created_at DESC
  `;
  return rows.map(fromDbRow);
}

function fromDbRow(row: any): ShareRecordV2 {
  return {
    id: row.id,
    tenantId: row.tenant_id,
    targetType: row.target_type,
    targetId: row.target_id,
    recipientUserId: row.recipient_user_id || null,
    recipientEmail: row.recipient_email || null,
    shareType: row.share_type,
    sharedById: row.shared_by_id,
    status: row.status,
    expiresAt: row.expires_at?.toISOString?.() ?? row.expires_at ?? null,
    message: row.message || null,
    createdAt: row.created_at?.toISOString?.() ?? String(row.created_at),
    updatedAt: row.updated_at?.toISOString?.() ?? String(row.updated_at),
    revokedAt: row.revoked_at?.toISOString?.() ?? row.revoked_at ?? null,
  };
}
