/**
 * =============================================================================
 * GDPR COMPLIANCE SERVICE
 * =============================================================================
 * Persistent GDPR operations backed by PostgreSQL:
 * - Consent management (record, withdraw, query)
 * - Data Subject Requests (create, process, track)
 * - Data retention policy enforcement
 * - Right-to-be-forgotten (cascading deletion)
 * - Data export (portability)
 * =============================================================================
 */

import { prisma } from '../db';
import { logger } from '../utils/logger';
import {
  decryptField,
  encryptFieldWithDek,
  decryptFieldWithDek,
  isSubjectDekCiphertext,
  isEncryptedPii,
  runWithPlatformScope,
} from '@secuura/shared';
// publishEvent MUST come from originate's own initialised publisher
// (../events), NOT @secuura/shared: the shared singleton is never
// initEventBus()'d in this service, and its publishEvent SILENTLY NO-OPS
// when uninitialised — which meant the USER_ERASED fan-out (auth/kyc/
// wallet cascades) never actually fired despite the success log
// (found during KS-291 verification).
import { publishEvent, EventTypes } from '../events';
import { subjectDeks } from './subjectDeks';
import { extractPgCode } from '../utils/pgErrors';
import { ERASED_MARKER } from '../utils/erasureMarker';
import { normaliseOrgId } from './orgId';
import {
  encodeLifecyclePayload,
  decodeLifecyclePayload,
  eraseEmailDeep,
} from '../utils/lifecyclePayloadCodec';

/**
 * KS-445: the consent/DSR write paths re-throw a sanitised Error (no SQL, no
 * driver internals), which used to drop the Postgres SQLSTATE — so the route
 * could only answer a raw 500. Wrap-and-tag instead: same sanitised message,
 * plus the classified `pgCode` so the route can map constraint failures to an
 * honest 4xx (23503 unknown user → 404, 22001/23514 bad value → 400).
 *
 * @param message - sanitised, client-safe error message for the wrapper.
 * @param cause - the original error the DB layer threw (any shape).
 * @returns an Error carrying the extracted SQLSTATE as `pgCode` (undefined
 *   when the cause wasn't a recognisable Postgres error).
 * @example
 * throw wrapDbError('Failed to record consent', err);
 */
function wrapDbError(message: string, cause: unknown): Error & { pgCode?: string } {
  const wrapped: Error & { pgCode?: string } = new Error(message);
  wrapped.pgCode = extractPgCode(cause);
  return wrapped;
}

/**
 * Read PII column with backward-compat for the migration tail. Plaintext
 * rows (not encrypted-field ciphertext) are returned as-is so existing data
 * keeps round-tripping; the next write encrypts.
 *
 * KS-291 dual-format: `d1:` rows decrypt under the subject's DEK (resolved
 * via the in-process-cached provider); legacy `v<N>:` rows use the master
 * keyring. A missing/destroyed DEK reads as undefined — the crypto-shredded
 * state.
 */
async function readPii(
  stored: string | null | undefined,
  context: string,
  subjectId: string,
): Promise<string | undefined> {
  if (stored == null || stored === '') return undefined;
  if (!isEncryptedPii(stored)) return stored;
  try {
    if (isSubjectDekCiphertext(stored)) {
      const dek = await subjectDeks.getDek(subjectId);
      if (!dek) return undefined;
      return decryptFieldWithDek(stored, context, dek) ?? undefined;
    }
    return decryptField(stored, context) ?? undefined;
  } catch {
    return undefined;
  }
}

/**
 * Write PII column under the subject's DEK (KS-291). Returns null for
 * null/empty so absent values stay NULL. Throws SubjectKeyDestroyedError for
 * erased subjects — no new PII for a crypto-shredded user.
 */
async function writePii(
  value: string | null | undefined,
  context: string,
  subjectId: string,
): Promise<string | null> {
  if (value == null || value === '') return null;
  const dek = await subjectDeks.getOrCreateDek(subjectId);
  return encryptFieldWithDek(value, context, dek);
}

// =============================================================================
// TYPES
// =============================================================================

export interface ConsentRecord {
  id: string;
  userId: string;
  purpose: string;
  version: string;
  source: 'explicit' | 'implicit';
  givenAt: string;
  expiresAt?: string;
  withdrawnAt?: string;
  ipAddress?: string;
  metadata?: Record<string, unknown>;
}

export interface DataSubjectRequest {
  id: string;
  type: 'access' | 'rectification' | 'erasure' | 'portability' | 'restriction' | 'objection';
  userId: string;
  email: string;
  requestedAt: string;
  deadline: string;
  status: 'pending' | 'processing' | 'completed' | 'denied' | 'extended';
  completedAt?: string;
  processedBy?: string;
  notes?: string;
  auditTrail?: Array<{ action: string; timestamp: string; actor: string }>;
}

export interface RetentionPolicy {
  id: string;
  dataType: string;
  retentionPeriodDays: number;
  legalBasis: string;
  deletionMethod: 'hard' | 'soft' | 'anonymize';
  autoDelete: boolean;
  description?: string;
}

export interface DeletionLogEntry {
  id: string;
  userId?: string;
  dsrId?: string;
  dataType: string;
  recordsAffected: number;
  deletionMethod: string;
  reason: string;
  performedBy: string;
  createdAt: string;
}

// =============================================================================
// CONSENT MANAGEMENT
// =============================================================================

export async function recordConsent(
  userId: string,
  purpose: string,
  opts?: {
    version?: string;
    source?: 'explicit' | 'implicit';
    expiresInDays?: number;
    ipAddress?: string;
    userAgent?: string;
    metadata?: Record<string, unknown>;
  },
): Promise<ConsentRecord> {
  const version = opts?.version || '1.0';
  const source = opts?.source || 'explicit';
  const expiresAt = opts?.expiresInDays
    ? new Date(Date.now() + opts.expiresInDays * 86400000)
    : null;

  // Audit 1.3 phase 5: ip_address + user_agent are PII tied to a real
  // person's network identity. Encrypt at rest with AAD bound to
  // (userId, purpose) — that pair uniquely identifies a consent row, so
  // ciphertexts can't be ported to a different user's consent row. NB the
  // schema migration ALTERs ip_address from inet → text since AES-GCM
  // ciphertext isn't a valid inet literal.
  const ipCt = await writePii(opts?.ipAddress, `consent_records.ip_address.${userId}.${purpose}`, userId);
  const uaCt = await writePii(opts?.userAgent, `consent_records.user_agent.${userId}.${purpose}`, userId);

  try {
    const rows: any[] = await prisma.$queryRaw`
      INSERT INTO consent_records (user_id, purpose, version, source, given_at, expires_at, ip_address, user_agent, metadata)
      VALUES (
        ${userId}::uuid, ${purpose}, ${version}, ${source}, NOW(),
        ${expiresAt}, ${ipCt}, ${uaCt},
        ${JSON.stringify(opts?.metadata || {})}::jsonb
      )
      ON CONFLICT (user_id, purpose) DO UPDATE SET
        version = EXCLUDED.version,
        source = EXCLUDED.source,
        given_at = NOW(),
        expires_at = EXCLUDED.expires_at,
        withdrawn_at = NULL,
        ip_address = EXCLUDED.ip_address,
        user_agent = EXCLUDED.user_agent,
        metadata = EXCLUDED.metadata,
        updated_at = NOW()
      RETURNING *
    `;
    return await mapConsentRow(rows[0]);
  } catch (err: any) {
    logger.error('Failed to record consent', { error: err instanceof Error ? err.message : String(err) });
    // KS-445: keep the SQLSTATE on the sanitised wrapper so the route maps
    // unknown-user / bad-value failures to 404/400 instead of a raw 500.
    throw wrapDbError('Failed to record consent', err);
  }
}

export async function withdrawConsent(userId: string, purpose: string): Promise<boolean> {
  try {
    const result = await prisma.$executeRaw`
      UPDATE consent_records SET withdrawn_at = NOW(), updated_at = NOW()
      WHERE user_id = ${userId}::uuid AND purpose = ${purpose} AND withdrawn_at IS NULL
    `;
    return result > 0;
  } catch (err: any) {
    logger.error('Failed to withdraw consent', { error: err instanceof Error ? err.message : String(err) });
    return false;
  }
}

export async function hasValidConsent(userId: string, purpose: string): Promise<boolean> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT 1 FROM consent_records
      WHERE user_id = ${userId}::uuid AND purpose = ${purpose}
        AND withdrawn_at IS NULL
        AND (expires_at IS NULL OR expires_at > NOW())
      LIMIT 1
    `;
    return rows.length > 0;
  } catch {
    return false;
  }
}

export async function getUserConsents(userId: string): Promise<ConsentRecord[]> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT * FROM consent_records WHERE user_id = ${userId}::uuid ORDER BY given_at DESC
    `;
    // KS-291: row mapping is async (per-subject DEK resolve, cached in-process)
    return await Promise.all(rows.map((r) => mapConsentRow(r)));
  } catch {
    return [];
  }
}

async function mapConsentRow(r: any): Promise<ConsentRecord> {
  return {
    id: r.id,
    userId: r.user_id,
    purpose: r.purpose,
    version: r.version,
    source: r.source,
    givenAt: r.given_at?.toISOString?.() || r.given_at,
    expiresAt: r.expires_at?.toISOString?.() || r.expires_at || undefined,
    withdrawnAt: r.withdrawn_at?.toISOString?.() || r.withdrawn_at || undefined,
    // Audit 1.3 phase 5: ip_address + user_agent stored encrypted at rest.
    ipAddress: await readPii(r.ip_address, `consent_records.ip_address.${r.user_id}.${r.purpose}`, r.user_id),
    metadata: r.metadata,
  };
}

// =============================================================================
// DATA SUBJECT REQUESTS
// =============================================================================

export async function createDSR(
  type: DataSubjectRequest['type'],
  userId: string,
  email: string,
  notes?: string,
): Promise<DataSubjectRequest> {
  try {
    const auditEntry = JSON.stringify([{ action: 'created', timestamp: new Date().toISOString(), actor: userId }]);
    // Audit 1.3 phase 5: email + notes are PII. AAD bound to (userId,
    // type) — a per-user-per-type DSR is unique enough to scope the
    // ciphertext.
    const emailCt = await writePii(email, `data_subject_requests.email.${userId}.${type}`, userId);
    const notesCt = await writePii(notes, `data_subject_requests.notes.${userId}.${type}`, userId);
    const rows: any[] = await prisma.$queryRaw`
      INSERT INTO data_subject_requests (type, user_id, email, notes, audit_trail)
      VALUES (${type}, ${userId}::uuid, ${emailCt}, ${notesCt}, ${auditEntry}::jsonb)
      RETURNING *
    `;
    return await mapDsrRow(rows[0]);
  } catch (err: any) {
    logger.error('Failed to create DSR', { error: err instanceof Error ? err.message : String(err) });
    // KS-445: same SQLSTATE preservation as recordConsent — see wrapDbError.
    throw wrapDbError('Failed to create data subject request', err);
  }
}

export async function getDSR(dsrId: string): Promise<DataSubjectRequest | null> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT * FROM data_subject_requests WHERE id = ${dsrId}::uuid LIMIT 1
    `;
    return rows.length > 0 ? await mapDsrRow(rows[0]) : null;
  } catch {
    return null;
  }
}

export async function getUserDSRs(userId: string): Promise<DataSubjectRequest[]> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT * FROM data_subject_requests WHERE user_id = ${userId}::uuid ORDER BY requested_at DESC
    `;
    return await Promise.all(rows.map((r) => mapDsrRow(r)));
  } catch {
    return [];
  }
}

export async function updateDSRStatus(
  dsrId: string,
  status: DataSubjectRequest['status'],
  processedBy: string,
  notes?: string,
): Promise<boolean> {
  try {
    const auditEntry = JSON.stringify({ action: `status_changed_to_${status}`, timestamp: new Date().toISOString(), actor: processedBy });
    const result = await prisma.$executeRaw`
      UPDATE data_subject_requests SET
        status = ${status},
        processed_by = ${processedBy},
        completed_at = ${status === 'completed' ? new Date() : null},
        notes = COALESCE(${notes}, notes),
        audit_trail = COALESCE(audit_trail, '[]'::jsonb) || jsonb_build_array(${auditEntry}::jsonb),
        updated_at = NOW()
      WHERE id = ${dsrId}::uuid
    `;
    return result > 0;
  } catch (err: any) {
    // KS-754: a failed write must NOT come back as an ordinary `false`.
    //
    // `false` is this function's "no such DSR" answer, and both callers read it
    // that way — routes/gdpr.ts:361 turns it into HTTP 200 with
    // `{ success: false, message: 'DSR not found' }`, and executeErasureImpl's
    // step 12 ignores it entirely. So a database error was reported to an API
    // caller as a successful request about a missing record, and to the erasure
    // path as nothing at all. That is what made this invisible.
    //
    // Same reasoning as KS-963: a DB error is not "no such row". Rethrowing
    // makes step 12 loud and turns the route's 200 into the 500 its own catch
    // already handles.
    logger.error('Failed to update DSR', {
      dsrId,
      status,
      error: err instanceof Error ? err.message : String(err),
      code: err?.code,
    });
    throw err;
  }
}

export async function getPendingDSRs(): Promise<DataSubjectRequest[]> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT * FROM data_subject_requests
      WHERE status IN ('pending', 'processing')
      ORDER BY deadline ASC
    `;
    return await Promise.all(rows.map((r) => mapDsrRow(r)));
  } catch {
    return [];
  }
}

async function mapDsrRow(r: any): Promise<DataSubjectRequest> {
  return {
    id: r.id,
    type: r.type,
    userId: r.user_id,
    email: (await readPii(r.email, `data_subject_requests.email.${r.user_id}.${r.type}`, r.user_id)) || '',
    requestedAt: r.requested_at?.toISOString?.() || r.requested_at,
    deadline: r.deadline?.toISOString?.() || r.deadline,
    status: r.status,
    completedAt: r.completed_at?.toISOString?.() || r.completed_at || undefined,
    processedBy: r.processed_by || undefined,
    notes: await readPii(r.notes, `data_subject_requests.notes.${r.user_id}.${r.type}`, r.user_id),
    auditTrail: r.audit_trail || [],
  };
}

// =============================================================================
// DATA RETENTION
// =============================================================================

export async function getRetentionPolicies(): Promise<RetentionPolicy[]> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT * FROM data_retention_policies ORDER BY data_type ASC
    `;
    return rows.map(mapRetentionRow);
  } catch {
    return [];
  }
}

export async function enforceRetention(): Promise<DeletionLogEntry[]> {
  // KS-458 (GDPR-mandated cross-tenant): retention enforcement is a
  // platform-wide sweep over every tenant's expired rows (audit_logs and
  // system_errors are fail-closed flip tables). It is invoked from the
  // background retentionScheduler (no request context at all) and from the
  // SYSTEM_ADMIN-only POST /api/gdpr/retention/enforce route — both are
  // reviewed platform paths, so run the whole sweep under the platform scope.
  return runWithPlatformScope(() => enforceRetentionImpl());
}

async function enforceRetentionImpl(): Promise<DeletionLogEntry[]> {
  const logs: DeletionLogEntry[] = [];

  try {
    const policies: any[] = await prisma.$queryRaw`
      SELECT * FROM data_retention_policies WHERE auto_delete = true
    `;

    for (const policy of policies) {
      const cutoff = new Date(Date.now() - policy.retention_period_days * 86400000);
      let affected = 0;

      try {
        if (policy.data_type === 'user_sessions') {
          const result = await prisma.$executeRaw`
            DELETE FROM user_sessions WHERE created_at < ${cutoff}
          `;
          affected = result;
        } else if (policy.data_type === 'audit_logs' && policy.deletion_method === 'anonymize') {
          const result = await prisma.$executeRaw`
            UPDATE audit_logs SET
              user_id = NULL, ip_address = NULL, user_agent = NULL,
              details = '{"anonymized": true}'::jsonb
            WHERE created_at < ${cutoff} AND user_id IS NOT NULL
          `;
          affected = result;
        } else if (policy.data_type === 'verification_requests') {
          const result = await prisma.$executeRaw`
            DELETE FROM verification_requests WHERE created_at < ${cutoff}
          `;
          affected = result;
        } else if (policy.data_type === 'system_errors' && policy.deletion_method === 'anonymize') {
          const result = await prisma.$executeRaw`
            UPDATE system_errors SET
              user_id = NULL, ip_address = NULL, stack = NULL,
              metadata = '{"anonymized": true}'::jsonb
            WHERE created_at < ${cutoff} AND user_id IS NOT NULL
          `;
          affected = result;
        } else if (policy.data_type === 'share_records') {
          const result = await prisma.$executeRaw`
            DELETE FROM share_records WHERE created_at < ${cutoff}
          `;
          affected = result;
        }

        if (affected > 0) {
          const logRows: any[] = await prisma.$queryRaw`
            INSERT INTO data_deletion_log (data_type, records_affected, deletion_method, reason, performed_by)
            VALUES (${policy.data_type}, ${affected}, ${policy.deletion_method}, ${'Retention policy enforcement'}, ${'system'})
            RETURNING *
          `;
          if (logRows[0]) logs.push(mapDeletionLogRow(logRows[0]));
        }

        // Update last enforcement timestamp
        await prisma.$executeRaw`
          UPDATE data_retention_policies SET last_enforcement_at = NOW(), updated_at = NOW()
          WHERE id = ${policy.id}::uuid
        `;
      } catch (err: any) {
        logger.error('Retention enforcement failed', { dataType: policy.data_type, error: err instanceof Error ? err.message : String(err) });
      }
    }
  } catch (err: any) {
    logger.error('Retention enforcement error', { error: err instanceof Error ? err.message : String(err) });
  }

  return logs;
}

function mapRetentionRow(r: any): RetentionPolicy {
  return {
    id: r.id,
    dataType: r.data_type,
    retentionPeriodDays: r.retention_period_days,
    legalBasis: r.legal_basis,
    deletionMethod: r.deletion_method,
    autoDelete: r.auto_delete,
    description: r.description || undefined,
  };
}

function mapDeletionLogRow(r: any): DeletionLogEntry {
  return {
    id: r.id,
    userId: r.user_id || undefined,
    dsrId: r.dsr_id || undefined,
    dataType: r.data_type,
    recordsAffected: r.records_affected,
    deletionMethod: r.deletion_method,
    reason: r.reason,
    performedBy: r.performed_by,
    createdAt: r.created_at?.toISOString?.() || r.created_at,
  };
}

// =============================================================================
// RIGHT TO BE FORGOTTEN — CASCADING DELETION
// =============================================================================

export async function executeErasure(
  userId: string,
  dsrId: string,
  performedBy: string,
): Promise<{ success: boolean; deletionLog: DeletionLogEntry[] }> {
  // KS-458 (GDPR-mandated cross-tenant): Art. 17 erasure must reach every row
  // belonging to the subject — users/documents/audit_logs/charge_events are
  // fail-closed flip tables and the subject may live in a tenant the calling
  // admin's request context doesn't match. Invoked only from the
  // SYSTEM_ADMIN-gated POST /api/gdpr/erasure/:userId route (routes/gdpr.ts),
  // so the platform scope is a reviewed admin path, not an open bypass.
  //
  // KS-695 ask 1: there is now a SECOND caller — executeErasureByExternalRef
  // below, reached by a connector (`x-api-key` -> connector JWT) rather than a
  // SYSTEM_ADMIN. The platform scope is still not an open bypass, but the
  // reason has moved: that path resolves external_ref -> users.id **scoped to
  // the caller's own tenant_id** BEFORE it gets here, so a connector can only
  // ever name a subject inside its own tenant. The tenancy gate is the
  // resolution step, not this function.
  return runWithPlatformScope(() => executeErasureImpl(userId, dsrId, performedBy));
}

async function executeErasureImpl(
  userId: string,
  dsrId: string,
  performedBy: string,
): Promise<{ success: boolean; deletionLog: DeletionLogEntry[] }> {
  const logs: DeletionLogEntry[] = [];

  try {
    // 1. Delete share records (shared_by_id is varchar)
    const shareCount = await prisma.$executeRaw`
      DELETE FROM share_records WHERE shared_by_id = ${userId}
    `;
    if (shareCount > 0) logs.push(await logDeletion(userId, dsrId, 'share_records', shareCount, 'hard', 'GDPR erasure request', performedBy));

    // 2. Delete charge events (initiated_by is varchar)
    const chargeCount = await prisma.$executeRaw`
      DELETE FROM charge_events WHERE initiated_by = ${userId}
    `;
    if (chargeCount > 0) logs.push(await logDeletion(userId, dsrId, 'charge_events', chargeCount, 'hard', 'GDPR erasure request', performedBy));

    // 3. Anonymize certification events (keep for audit but remove PII).
    // KS-543 (Stuart's KS-537 finding #1): the old step only NULLed the FK
    // and STAMPED `anonymized: true` while leaving every value in `details`
    // in place — "reads as compliant in a DSR log and isn't". Now the
    // details are rebuilt from a non-identifying ALLOW-LIST ({status,
    // blockchain, shareType} — the keys K's own writers use for event/chain
    // state; anything else, known or unknown, is dropped). Event type, hash
    // and chain linkage survive; identity does not.
    const certEventCount = await prisma.$executeRaw`
      UPDATE certification_events SET
        actor_user_id = NULL,
        details = (
          SELECT COALESCE(jsonb_object_agg(e.key, e.value), '{}'::jsonb)
          FROM jsonb_each(COALESCE(certification_events.details, '{}'::jsonb)) AS e(key, value)
          WHERE e.key IN ('status', 'blockchain', 'shareType')
        ) || '{"anonymized": true}'::jsonb
      WHERE actor_user_id = ${userId}::uuid
    `;
    if (certEventCount > 0) logs.push(await logDeletion(userId, dsrId, 'certification_events', certEventCount, 'anonymize', 'GDPR erasure request (details allow-list stripped)', performedBy));

    // 4. Anonymize audit logs
    const auditCount = await prisma.$executeRaw`
      UPDATE audit_logs SET
        user_id = NULL, ip_address = NULL, user_agent = NULL,
        details = '{"anonymized": true, "reason": "GDPR erasure"}'::jsonb
      WHERE user_id = ${userId}::uuid
    `;
    if (auditCount > 0) logs.push(await logDeletion(userId, dsrId, 'audit_logs', auditCount, 'anonymize', 'GDPR erasure request', performedBy));

    // 5. Delete document access grants
    const accessCount = await prisma.$executeRaw`
      DELETE FROM document_access WHERE granted_by = ${userId}::uuid OR granted_to_user_id = ${userId}::uuid
    `;
    if (accessCount > 0) logs.push(await logDeletion(userId, dsrId, 'document_access', accessCount, 'hard', 'GDPR erasure request', performedBy));

    // 5b. KS-480 §6 — PSEUDONYMISE connector provenance (Peter's erasure rule:
    // blank identity, keep attribution). email/display_name (encrypted) and
    // the derived email_hash are blanked; external_ref (S PersonGuid) and
    // resolved_user_id survive as the stable non-identifying attribution —
    // deleting them would destroy the only attribution record and reinstate
    // the anonymous-blob problem KS-480 exists to fix. Matched by the
    // resolved user id OR the subject's own email hash (rows recorded before
    // any K account existed carry only the hash).
    const provenanceCount = await prisma.$executeRaw`
      UPDATE action_provenance SET
        email_enc = NULL, display_name_enc = NULL, email_hash = NULL
      WHERE resolved_user_id = ${userId}::uuid
         OR (email_hash IS NOT NULL AND email_hash IN (
              SELECT email_lookup_hash FROM users WHERE id = ${userId}::uuid AND email_lookup_hash IS NOT NULL
            ))
    `;
    if (provenanceCount > 0) logs.push(await logDeletion(userId, dsrId, 'action_provenance', provenanceCount, 'anonymize', 'GDPR erasure request (pseudonymised — attribution retained)', performedBy));

    // 5c. KS-537 — resolve the subject's plaintext email while the user row
    // is still intact (anonymisation happens at step 10). Needed for content
    // matching inside lifecycle payloads and the shares recipient column —
    // both store the address itself, not a user id. A failed resolution
    // leaves the email undefined and the uuid-matched clauses still run.
    let subjectEmail: string | undefined;
    try {
      const uRows: any[] = await prisma.$queryRaw`
        SELECT email FROM users WHERE id = ${userId}::uuid
      `;
      subjectEmail = await readPii(uRows?.[0]?.email, `users.email.${userId}`, userId);
    } catch (err) {
      logger.warn('Erasure: subject email resolution failed — email-matched steps will be uuid-only', {
        error: err instanceof Error ? err.message : String(err),
      });
    }

    // 5d. KS-537 — pseudonymise lifecycle payloads. The column is caller-
    // supplied free-form JSON (encrypted at rest since KS-537; legacy rows
    // plaintext), so the subject's PII can sit under any key. Decode every
    // row, deep-replace the subject's email, re-encrypt. The row and its
    // attribution (actor_user_id, action, anchor linkage) survive — KS-480 §6
    // posture: identity blanked, attribution retained. actor_user_id is a
    // bare uuid whose user row step 10 anonymises, so it is not PII here.
    let lifecycleCount = 0;
    if (subjectEmail) {
      const evRows: any[] = await prisma.$queryRaw`
        SELECT id, payload FROM document_lifecycle_events
      `;
      for (const row of evRows ?? []) {
        const eventId = String(row.id);
        const decoded = decodeLifecyclePayload(row.payload, eventId);
        if (!decoded || Object.keys(decoded).length === 0) continue;
        if ((decoded as Record<string, unknown>).payloadUnavailable === true) continue;
        const { value, changed } = eraseEmailDeep(decoded, subjectEmail);
        if (!changed) continue;
        const scrubbed = { ...(value as Record<string, unknown>), piiErased: true };
        const stored = encodeLifecyclePayload(scrubbed, eventId);
        await prisma.$executeRaw`
          UPDATE document_lifecycle_events SET payload = ${stored}::jsonb WHERE id = ${row.id}::uuid
        `;
        lifecycleCount++;
      }
    }
    if (lifecycleCount > 0) logs.push(await logDeletion(userId, dsrId, 'document_lifecycle_events', lifecycleCount, 'anonymize', 'GDPR erasure request (payload pseudonymised — event + attribution retained)', performedBy));

    // 5e. KS-537 — the `shares` table (the live /share path, published
    // KS-536) was outside erasure entirely: recipient_email is stored in
    // plaintext and only the OLDER share_records table was covered. Sharer
    // rows are hard-deleted (mirrors the share_records posture at step 1);
    // rows where the subject is the RECIPIENT keep the share record but
    // blank the identifying address (recipient_user_id, a uuid, survives as
    // attribution like everywhere else).
    const sharesDeleted = await prisma.$executeRaw`
      DELETE FROM shares WHERE shared_by_id = ${userId}::uuid
    `;
    if (sharesDeleted > 0) logs.push(await logDeletion(userId, dsrId, 'shares', sharesDeleted, 'hard', 'GDPR erasure request (subject was sharer)', performedBy));
    // shares_recipient_chk requires at least one recipient identifier, so an
    // email-only row can't just lose its address — it gets the subject's uuid
    // instead (we matched their email, so it IS their share; the uuid points
    // at the anonymised user row, same attribution-retained shape as
    // everywhere else).
    const sharesRecipient = await prisma.$executeRaw`
      UPDATE shares SET
        recipient_email = NULL,
        recipient_user_id = COALESCE(recipient_user_id, ${userId}::uuid)
      WHERE recipient_user_id = ${userId}::uuid
         OR (recipient_email IS NOT NULL AND ${subjectEmail ?? null}::text IS NOT NULL
             AND lower(recipient_email) = lower(${subjectEmail ?? null}::text))
    `;
    if (sharesRecipient > 0) logs.push(await logDeletion(userId, dsrId, 'shares', sharesRecipient, 'anonymize', 'GDPR erasure request (recipient email blanked — share record retained)', performedBy));

    // 5f. KS-543 — certification_events SHARE rows carry the RECIPIENT's
    // identity ({toEmail, toName}); step 3 only matches actor rows, so a
    // subject who was shared WITH kept their email in other users' events.
    // Same posture as the shares table at 5e: identity keys removed, the
    // event and its shareType retained. (to_email is matched on the resolved
    // plaintext; rows for a subject with no resolvable email are untouched —
    // there is nothing to match them by.)
    if (subjectEmail) {
      const certEventRecipient = await prisma.$executeRaw`
        UPDATE certification_events SET
          details = (details - 'toEmail' - 'toName') || '{"anonymized": true}'::jsonb
        WHERE details->>'toEmail' IS NOT NULL
          AND lower(details->>'toEmail') = lower(${subjectEmail})
      `;
      if (certEventRecipient > 0) logs.push(await logDeletion(userId, dsrId, 'certification_events', certEventRecipient, 'anonymize', 'GDPR erasure request (subject was share recipient — toEmail/toName removed)', performedBy));

      // 5g. KS-543 (adjacent gap, same family) — the legacy share_records
      // table stores the recipient in plaintext (to_email NOT NULL /
      // to_name); step 1 only deletes rows the subject SENT. Blank the
      // identifying columns where the subject was the recipient (sentinel,
      // not NULL — the column is NOT NULL).
      const shareRecordsRecipient = await prisma.$executeRaw`
        UPDATE share_records SET to_email = ${ERASED_MARKER}, to_name = NULL
        WHERE lower(to_email) = lower(${subjectEmail})
      `;
      if (shareRecordsRecipient > 0) logs.push(await logDeletion(userId, dsrId, 'share_records', shareRecordsRecipient, 'anonymize', 'GDPR erasure request (subject was recipient — to_email/to_name blanked)', performedBy));
    }

    // 6. Anonymize documents (keep structure, remove personal metadata)
    // KS-695 ask 2: `title` carries the real filename — Platform S sends it as
    // `Title` on originate (platform-s CardanoAnchorService.cs:407) — so before
    // this it survived erasure verbatim on the subject's own documents.
    //
    // `description` is the same class one column below (caller-supplied free
    // text, `routes/documents.ts:471`) and was still standing after ask 2 —
    // QA F-2. The two are erased DIFFERENTLY on purpose, and the difference is
    // the live schema, not a style choice: `title` is `character varying NOT
    // NULL`, so it must hold something and gets ERASED_MARKER; `description` is
    // nullable `text`, so it gets NULL, because storing nothing erases more
    // than storing a marker.
    //
    // Scope is unchanged: the subject's OWN documents. Non-owned documents are
    // step 6b's surgical pass and keep their titles — those belong to someone
    // else.
    const docCount = await prisma.$executeRaw`
      UPDATE documents SET
        metadata = '{"anonymized": true}'::jsonb,
        certification_metadata = '{"anonymized": true}'::jsonb,
        title = ${ERASED_MARKER},
        description = NULL,
        document_type = ${ERASED_MARKER},
        owner_did = NULL
      WHERE owner_user_id = ${userId}::uuid
    `;
    if (docCount > 0) logs.push(await logDeletion(userId, dsrId, 'documents', docCount, 'anonymize', 'GDPR erasure request', performedBy));

    // 6b. KS-543 (Stuart's KS-537 finding #2) — certification_metadata on
    // documents the subject does NOT own. Certifications are documents rows
    // with holder = owner_user_id, so step 6 covers holder-subjects; but a
    // subject who was the ISSUER (or whose identity landed in the verbatim
    // certificationData blob — S sent `actorName: "First Last (email)"`
    // until PS-472) survives on documents owned by someone else. Those rows
    // must NOT be blanked wholesale — the blob also carries the holder's
    // blockchain/signature linkage, which is the holder's data, not the
    // subject's. Surgical pass instead: blank the issuer identity fields
    // (issuerId, a uuid pointing at the anonymised user row, survives as
    // attribution) and deep-erase the subject's email everywhere in the
    // blob (containment match — covers "Name (email)" shapes; a bare name
    // with no address has nothing durable to match it by).
    {
      const linked: any[] = await prisma.$queryRaw`
        SELECT id, certification_metadata FROM documents
        WHERE certification_metadata IS NOT NULL
          AND (owner_user_id IS NULL OR owner_user_id <> ${userId}::uuid)
          AND (
            issuer_user_id = ${userId}::uuid
            OR certification_metadata->>'issuerId' = ${userId}
            OR (${subjectEmail ?? null}::text IS NOT NULL
                AND certification_metadata::text ILIKE '%' || ${subjectEmail ?? null}::text || '%')
          )
      `;
      let certMetaCount = 0;
      for (const row of linked ?? []) {
        const meta = ((typeof row.certification_metadata === 'string'
          ? JSON.parse(row.certification_metadata)
          : row.certification_metadata) ?? {}) as Record<string, unknown>;
        const isSubjectIssuer = String(meta.issuerId ?? '') === userId;
        const base: Record<string, unknown> = { ...meta };
        if (isSubjectIssuer) {
          if ('issuerName' in base) base.issuerName = ERASED_MARKER;
          if ('issuerDid' in base) base.issuerDid = null;
        }
        const { value, changed } = eraseEmailDeep(base, subjectEmail);
        if (!changed && !isSubjectIssuer) continue;
        const scrubbed = { ...(value as Record<string, unknown>), piiErased: true };
        await prisma.$executeRaw`
          UPDATE documents SET certification_metadata = ${JSON.stringify(scrubbed)}::jsonb, updated_at = NOW()
          WHERE id = ${row.id}::uuid
        `;
        certMetaCount++;
      }
      if (certMetaCount > 0) logs.push(await logDeletion(userId, dsrId, 'documents.certification_metadata', certMetaCount, 'anonymize', 'GDPR erasure request (non-owned docs — issuer identity blanked, subject email deep-erased; holder chain linkage retained)', performedBy));
    }

    // 7. Delete user sessions
    const sessionCount = await prisma.$executeRaw`
      DELETE FROM user_sessions WHERE user_id = ${userId}::uuid
    `;
    if (sessionCount > 0) logs.push(await logDeletion(userId, dsrId, 'user_sessions', sessionCount, 'hard', 'GDPR erasure request', performedBy));

    // 8. Delete refresh tokens (KS-293). The FK to users is ON DELETE CASCADE,
    // but erasure anonymises the user row (UPDATE at step 10) instead of
    // deleting it, so the cascade never fires. Left in place, an orphaned
    // refresh token would still mint fresh access tokens for the anonymised
    // account after erasure — delete them explicitly, as we do for sessions.
    const refreshTokenCount = await prisma.$executeRaw`
      DELETE FROM refresh_tokens WHERE user_id = ${userId}::uuid
    `;
    if (refreshTokenCount > 0) logs.push(await logDeletion(userId, dsrId, 'refresh_tokens', refreshTokenCount, 'hard', 'GDPR erasure request', performedBy));

    // 9. Delete consent records (they're being withdrawn by erasure)
    const consentCount = await prisma.$executeRaw`
      DELETE FROM consent_records WHERE user_id = ${userId}::uuid
    `;
    if (consentCount > 0) logs.push(await logDeletion(userId, dsrId, 'consent_records', consentCount, 'hard', 'GDPR erasure request', performedBy));

    // 10. Anonymize the user record (soft delete — keep UUID for referential integrity)
    // NB the ::text cast on erasedAt inside jsonb_build_object is load-bearing:
    // when MULTI_TENANCY_ENABLED=true (demo/prod) `prisma` is the pg-pool
    // proxy, which sends parameters untyped, and Postgres cannot infer a
    // parameter's type inside variadic jsonb_build_object — the whole erasure
    // aborted with `could not determine data type of parameter $1` (found in
    // the KS-291 demo verification; the real Prisma client used locally
    // masked it).
    const erasedAt = new Date().toISOString();
    // first_name / last_name / password_hash go to NULL, not plaintext
    // sentinels ('Deleted'/'User'/'DELETED'): the name columns are encrypted
    // at rest, so a plaintext sentinel trips auth's B-10 plaintext-cutoff
    // hard-fail in prod-like envs (login for the erased row 500'd on demo
    // until the auth cascade happened to overwrite it — KS-291 verification),
    // and a non-hash sentinel in password_hash makes verify throw rather
    // than reject. NULLs express exactly what erasure means.
    const userCount = await prisma.$executeRaw`
      UPDATE users SET
        email = 'deleted_' || id || '@anonymized.local',
        password_hash = NULL,
        first_name = NULL,
        last_name = NULL,
        mfa_secret = NULL,
        status = 'deleted',
        metadata = jsonb_build_object('anonymized', true, 'erasedAt', ${erasedAt}::text),
        updated_at = NOW()
      WHERE id = ${userId}::uuid
    `;
    if (userCount > 0) logs.push(await logDeletion(userId, dsrId, 'users', userCount, 'anonymize', 'GDPR erasure request', performedBy));

    // 11. CRYPTO-SHRED (KS-291): destroy the subject's DEK. Every d1: PII
    // ciphertext for this user — live rows already NULLed/deleted above, plus
    // every copy in every database backup — becomes permanently unrecoverable
    // once the pii_subject_keys backups age out of the retention window. The
    // row is kept as a tombstone (destroyed_at) so the destruction is
    // auditable and a DEK can never be re-minted for the erased subject.
    // (Predecessor history: the pre-KS-292 code here DELETEd from tables that
    // never existed and swallowed the error — see KS-292.)
    // Runs LAST among the data steps: nothing after it needs to decrypt.
    const shredResult = await subjectDeks.destroyDek(userId);
    logs.push(await logDeletion(userId, dsrId, 'pii_subject_keys', 1, 'crypto-shred', `GDPR erasure request (${shredResult})`, performedBy));

    // 12. Mark DSR as completed
    // KS-1028: a step-12 throw must not skip the step-13 fan-out below - captured here, re-raised after it.
    const step12Error: unknown = await updateDSRStatus(dsrId, 'completed', performedBy, 'Erasure completed. ' + logs.length + ' data types processed.')
      .then(() => undefined, (err: unknown) => err ?? new Error('KS-1028: step 12 rejected'));
    // KS-1028: the fan-out (step 13) runs next; the captured error is thrown after it, before the completed log.
    // 13. Audit 2.2: fan out to other services. Originate's executeErasure
    // only touches originate's own DB; downstream services (auth, kyc, m365,
    // wallet-connector, security audit) hold user-scoped data of their own
    // and need to react to this event. The publish is fire-and-forget; we
    // don't block the DSR response on subscriber processing because GDPR's
    // 30-day SLA is well above what async processing takes, and the event
    // bus's consumer-group semantics make it idempotent on retry.
    //
    // We capture the user's wallet_address pre-anonymisation so the
    // wallet-connector subscriber can find sessions to drop (it has no
    // user_id column — wallets are keyed by address).
    let walletAddress: string | undefined;
    try {
      const wRows: any[] = await prisma.$queryRaw`
        SELECT wallet_address FROM users WHERE id = ${userId}::uuid
      `;
      walletAddress = wRows?.[0]?.wallet_address || undefined;
    } catch {
      // If lookup fails, walletAddress stays undefined and wallet-connector
      // subscriber simply has nothing to act on. Not fatal.
    }

    try {
      await publishEvent(EventTypes.USER_ERASED, {
        userId,
        dsrId,
        performedBy,
        erasedAt: new Date().toISOString(),
        ...(walletAddress ? { walletAddress } : {}),
      });
      logger.info('user.erased event published — downstream services will cascade', { userId });
    } catch (err: any) {
      logger.warn('Failed to publish user.erased event (cascade may be incomplete)', { userId, error: err?.message });
    }
    if (step12Error) throw step12Error; // KS-1028: re-raised only AFTER the fan-out; the outer catch below still answers success false
    logger.info('Erasure completed', { userId, dataTypesProcessed: logs.length, totalRecordsAffected: logs.reduce((sum, l) => sum + l.recordsAffected, 0) });
    return { success: true, deletionLog: logs };
  } catch (err: any) {
    logger.error('Erasure failed', { error: err instanceof Error ? err.message : String(err) });
    return { success: false, deletionLog: logs };
  }
}

async function logDeletion(
  userId: string,
  dsrId: string,
  dataType: string,
  recordsAffected: number,
  deletionMethod: string,
  reason: string,
  performedBy: string,
): Promise<DeletionLogEntry> {
  const rows: any[] = await prisma.$queryRaw`
    INSERT INTO data_deletion_log (user_id, dsr_id, data_type, records_affected, deletion_method, reason, performed_by)
    VALUES (${userId}::uuid, ${dsrId}::uuid, ${dataType}, ${recordsAffected}, ${deletionMethod}, ${reason}, ${performedBy})
    RETURNING *
  `;
  return mapDeletionLogRow(rows[0]);
}

// =============================================================================
// DATA EXPORT (PORTABILITY)
// =============================================================================

export async function exportUserData(userId: string): Promise<Record<string, unknown>> {
  // KS-458 (GDPR-mandated cross-tenant): the Art. 20 export must be complete
  // regardless of tenant boundary — users/documents/charge_events are
  // fail-closed flip tables and an admin processing an access/portability DSR
  // may export a subject outside their own tenant. Invoked only from the
  // self-or-admin gated GET /api/gdpr/export/:userId(+/download) routes.
  return runWithPlatformScope(() => exportUserDataImpl(userId));
}

async function exportUserDataImpl(userId: string): Promise<Record<string, unknown>> {
  const exported: Record<string, unknown> = {
    exportedAt: new Date().toISOString(),
    userId,
    format: 'GDPR Article 20 — Data Portability',
  };

  try {
    // User profile. email / first_name / last_name are encrypted at rest —
    // decrypt for the export (Art. 20 requires the data in intelligible
    // form; the raw columns are ciphertext). Fixed alongside KS-291: the
    // previous version exported the ciphertext blobs verbatim.
    const users: any[] = await prisma.$queryRaw`
      SELECT id, email, first_name, last_name, role, verification_level, created_at
      FROM users WHERE id = ${userId}::uuid
    `;
    const u = users[0];
    exported.profile = u
      ? {
          ...u,
          email: await readPii(u.email, `users.email.${userId}`, userId),
          first_name: await readPii(u.first_name, `users.first_name.${userId}`, userId),
          last_name: await readPii(u.last_name, `users.last_name.${userId}`, userId),
        }
      : null;
  } catch (err: any) {
    logger.warn('User profile export failed', { error: err instanceof Error ? err.message : String(err) });
  }

  try {
    // Consent records
    const consents: any[] = await prisma.$queryRaw`
      SELECT purpose, version, source, given_at, expires_at, withdrawn_at FROM consent_records WHERE user_id = ${userId}::uuid
    `;
    exported.consents = consents;
  } catch (err: any) {
    logger.warn('Consent export failed', { error: err instanceof Error ? err.message : String(err) });
  }

  try {
    // Documents
    const docs: any[] = await prisma.$queryRaw`
      SELECT id, title, document_type, status, created_at, updated_at FROM documents WHERE owner_user_id = ${userId}::uuid
    `;
    exported.documents = docs;
  } catch (err: any) {
    logger.warn('Documents export failed', { error: err instanceof Error ? err.message : String(err) });
  }

  try {
    // Share records (shared_by_id is varchar, not uuid)
    const shares: any[] = await prisma.$queryRaw`
      SELECT id, document_id, to_email, share_type, timestamp FROM share_records WHERE shared_by_id = ${userId}
    `;
    exported.shares = shares;
  } catch (err: any) {
    logger.warn('Shares export failed', { error: err instanceof Error ? err.message : String(err) });
  }

  try {
    // Charge events (initiated_by is varchar, not uuid)
    const charges: any[] = await prisma.$queryRaw`
      SELECT id, event_type, certification_id, amount, currency, fee_status, created_at FROM charge_events WHERE initiated_by = ${userId}
    `;
    exported.chargeEvents = charges;
  } catch (err: any) {
    logger.warn('Charge events export failed', { error: err instanceof Error ? err.message : String(err) });
  }

  try {
    // DSR history
    const dsrs: any[] = await prisma.$queryRaw`
      SELECT id, type, requested_at, deadline, status, completed_at FROM data_subject_requests WHERE user_id = ${userId}::uuid
    `;
    exported.dataSubjectRequests = dsrs;
  } catch (err: any) {
    logger.warn('DSR export failed', { error: err instanceof Error ? err.message : String(err) });
  }

  return exported;
}

// =============================================================================
// DELETION LOG
// =============================================================================

export async function getDeletionLog(userId?: string): Promise<DeletionLogEntry[]> {
  try {
    if (userId) {
      const rows: any[] = await prisma.$queryRaw`
        SELECT * FROM data_deletion_log WHERE user_id = ${userId}::uuid ORDER BY created_at DESC
      `;
      return rows.map(mapDeletionLogRow);
    }
    const rows: any[] = await prisma.$queryRaw`
      SELECT * FROM data_deletion_log ORDER BY created_at DESC LIMIT 100
    `;
    return rows.map(mapDeletionLogRow);
  } catch {
    return [];
  }
}

// =============================================================================
// KS-695 ask 1 — ERASURE ADDRESSABLE BY `external_ref` (connector-driven)
// =============================================================================
// Platform S holds no K `users.id` — the per-user credential tier was removed
// in PS-465. The only per-user link it has is `Person.PersonGuid`, which K
// already receives as `onBehalfOf.externalRef` on every attributed write and
// which erasure deliberately RETAINS (see step 5 above) as the stable
// non-identifying attribution.
//
// S retries WITHOUT BOUND — a parked erasure silently strands a legal
// obligation — so every path below must be idempotent and must TERMINATE.
// There is deliberately no 404: an `external_ref` K cannot resolve is not a
// not-found, it is a subject K holds nothing erasable for, and answering
// anything non-terminal would strand the retry forever.

/**
 * The five statuses `data_subject_requests.status` admits, ENUMERATED FROM THE
 * SCHEMA rather than from memory — `docker/init/01-schema.sql:490`:
 *
 *   CHECK (status IN ('pending', 'processing', 'completed', 'denied', 'extended'))
 *
 * Confirmed against the live constraint with
 * `pg_get_constraintdef` on `data_subject_requests`, which returns the same
 * five. Of them exactly two are TERMINAL:
 *
 *   - `completed` — the erasure ran and discharged the obligation.
 *   - `denied`    — a human REFUSED it, e.g. under one of the Art. 17(3)
 *                   exemptions. It is a decision, not a pending state.
 *
 * `pending` and `processing` are obviously non-terminal. `extended` is too, and
 * that is the one worth stating: it is an Art. 12(3) extension of the RESPONSE
 * DEADLINE, not a conclusion — the request is still live and must still be
 * driven.
 *
 * QA F-1: the re-drive predicate was `status <> 'completed'`, which makes
 * `denied` non-terminal. A denied erasure was therefore re-driven, executed
 * irreversibly (crypto-shred included), and the human's denial overwritten with
 * `completed`. Anything reading this table for terminality must use the set,
 * never the single literal.
 */
export const TERMINAL_DSR_STATUSES = ['completed', 'denied'] as const;
export type TerminalDsrStatus = (typeof TERMINAL_DSR_STATUSES)[number];

/**
 * The CONNECTOR-FACING terminal vocabulary. Deliberately NOT `TerminalDsrStatus`:
 * that type is the `data_subject_requests` CHECK vocabulary, and `unresolvable`
 * is never written to that table — there is no user row to file it against. The
 * two were the same type only by coincidence, and widening the DSR vocabulary to
 * express a response would have been a schema change to describe an API answer.
 *
 * `unresolvable` is TERMINAL: S must stop retrying. It is answered 200, not 5xx,
 * for the same reason `denied` is — a refusal S retries forever is the failure
 * mode this whole path exists to avoid.
 */
export const CONNECTOR_ERASURE_STATUSES = ['completed', 'denied', 'unresolvable'] as const;
export type ConnectorErasureStatus = (typeof CONNECTOR_ERASURE_STATUSES)[number];

/** Why an erasure was refused. Sent to S in the body so a human can act on it. */
export type ConnectorErasureRefusalReason =
  | 'org_less_key'
  | 'subject_outside_connector_organisation'
  | 'ambiguous_subject';

export interface ConnectorErasureResult {
  /**
   * `denied` is terminal for S in exactly the way `completed` is: stop
   * retrying. It is NOT an error — K is reporting a decision it holds, and a
   * 5xx here would put S back into the unbounded retry this whole path exists
   * to avoid.
   */
  status: ConnectorErasureStatus;
  alreadyErased: boolean;
  /** Present only on `unresolvable`. */
  reason?: ConnectorErasureRefusalReason;
}

/**
 * Thrown when the erasure ran but did not complete.
 *
 * The only non-terminal answer this path can give. It is deliberate: S retries
 * without bound, and a retryable failure MUST be retried — the alternative is
 * reporting an Art. 17 obligation discharged when it was not. The route turns
 * this into a 500; the DSR is left non-terminal so the next attempt re-drives
 * the same row rather than filing another.
 */
/**
 * Thrown when an `external_ref` hash-resolves to a user in a DIFFERENT
 * Organisation from the caller's key. Terminal and a caller fault — the route
 * answers 403, not a 5xx, so S stops rather than retrying a request it can
 * never make succeed.
 *
 * QA Blocker 2. This was TENANT-scoped, and a tenant holds many organisations:
 * a connector minted for org A could erase a subject in org B of the same
 * tenant and be answered `completed`. The write-side sibling
 * `resolveOnBehalfOf` (`provenance.ts:104-122`) has always been
 * ORGANISATION-scoped and 403s that exact crossing, naming the hazard in its
 * own comment — "would attribute to ANY matching tenant user". Erasure is the
 * more destructive direction of the same relationship, so it is now scoped the
 * same way. The tenant compare is not lost: the provenance query that feeds
 * this resolver is still `tenant_id`-filtered, so the tenant is a floor and the
 * organisation is the gate.
 */
export class ConnectorErasureCrossOrgError extends Error {
  constructor(externalRef: string) {
    super(`external_ref ${externalRef} resolves to a subject outside this connector's Organisation`);
    this.name = 'ConnectorErasureCrossOrgError';
  }
}

/**
 * Thrown when the subject CANNOT be resolved safely and erasing anyway would be
 * a guess. Terminal, answered 200 with `status: 'unresolvable'` and a reason, so
 * S stops retrying — and, critically, never `completed`, because reporting an
 * Art. 17 obligation discharged that was not is the failure this path exists to
 * prevent.
 */
export class ConnectorErasureUnresolvableError extends Error {
  constructor(externalRef: string, public readonly reason: ConnectorErasureRefusalReason) {
    super(`external_ref ${externalRef} could not be resolved safely: ${reason}`);
    this.name = 'ConnectorErasureUnresolvableError';
  }
}

export class ConnectorErasureIncompleteError extends Error {
  constructor(externalRef: string) {
    super(`Erasure for external_ref ${externalRef} did not complete — not marking it done`);
    this.name = 'ConnectorErasureIncompleteError';
  }
}

/**
 * Resolve an S `PersonGuid` to a K user id, **scoped to the caller's tenant**.
 *
 * This is the tenancy gate for the whole connector erasure path: a connector
 * can only ever name a subject that appears in its own tenant's provenance.
 * Returns the resolved user id (or null) plus whether K holds any provenance
 * for that ref at all — the two are different answers and the caller needs
 * both.
 */
async function resolveExternalRef(
  externalRef: string,
  tenantId: string,
  connectorOrgId: string | undefined,
): Promise<{ userId: string | null; provenanceRows: number }> {
  // Peter F12: ORDER BY + an explicit first row, not `.find()` on an unordered
  // unlimited SELECT. Rows carrying a resolved id sort first, so the pick is
  // deterministic instead of dependent on Postgres's scan order.
  const rows: Array<{ resolved_user_id: string | null; email_hash: string | null }> =
    await prisma.$queryRaw`
      SELECT resolved_user_id, email_hash FROM action_provenance
      WHERE external_ref = ${externalRef} AND tenant_id = ${tenantId}::uuid
      ORDER BY (resolved_user_id IS NULL), created_at ASC
    `;
  const direct = rows.find((r) => r.resolved_user_id);
  if (direct?.resolved_user_id) {
    return { userId: direct.resolved_user_id, provenanceRows: rows.length };
  }

  // Peter F1. `resolveOnBehalfOf` opens with `if (!connectorOrgId) return null`
  // (provenance.ts:108), so a connector key minted WITHOUT an organizationId
  // never sets `resolved_user_id` on ANY row — whether or not a matching K user
  // exists. Resolving on `resolved_user_id` alone therefore sent a real user's
  // erasure down the unresolvable branch, which blanks three provenance columns
  // and answers `completed`: no users row, no documents, no crypto-shred, and S
  // records the obligation discharged. Measured on this database: 8 of 22
  // action_provenance rows carry a hash with no resolved_user_id, and only 1 is
  // resolved — the degraded branch is the common case here, not a corner.
  //
  // The fallback is step 5b's own clause (`:590`), run in the resolution
  // direction.
  //
  // WHY AN ASSERTION AND NOT A `WHERE u.tenant_id = $2` FILTER — this is the
  // part of Peter's fix shape I changed after measuring the schema.
  // `users_email_lookup_hash_uniq` is a UNIQUE index on `email_lookup_hash`
  // (partial, WHERE NOT NULL), so a hash names AT MOST ONE user row globally.
  // Uniqueness removes ambiguity but not cross-org REACH: the single row it
  // finds may belong to another Organisation. Filtering would turn that case
  // into "no rows" — i.e. back to the unresolvable branch, which is exactly the
  // silent under-erasure F1 is about. So: match on the hash, then CHECK, and
  // refuse loudly.
  //
  // QA Blocker 2 — WHY THE ORGANISATION AND NOT THE TENANT. The assertion was
  // `candidate.tenant_id !== tenantId`, and a tenant contains many
  // organisations, so a connector minted for org A could erase a subject in
  // org B of the same tenant. The write-side sibling `resolveOnBehalfOf`
  // (`provenance.ts:104-122`) is ORGANISATION-scoped for this same
  // relationship and 403s that crossing. Erasure is the more destructive
  // direction, so it mirrors the sibling. The tenant is still a floor: the
  // provenance SELECT above is `tenant_id`-filtered, so a hash can only be
  // reached through a ref this tenant actually holds.
  const hashes = rows.map((r) => r.email_hash).filter((h): h is string => !!h);
  if (hashes.length === 0) return { userId: null, provenanceRows: rows.length };

  // An ORG-LESS KEY does not fall back to the hash at all. The sibling returns
  // null here and stores verbatim provenance, which is harmless on a write. On
  // an erasure, "null" means the unresolvable branch: blank three provenance
  // columns and answer `completed` — a silent partial erasure reported as a
  // discharged obligation. So this path refuses instead, terminally.
  if (!connectorOrgId) {
    logger.warn('Connector erasure: key carries no organizationId — refusing to resolve by hash', {
      externalRef, callerTenantId: tenantId,
    });
    throw new ConnectorErasureUnresolvableError(externalRef, 'org_less_key');
  }

  // LIMIT 2, not 1. QA finding 4: `= ANY(hashes) … LIMIT 1` with no ORDER BY
  // picks an arbitrary row, and the uniqueness argument above does NOT hold for
  // a SET-valued match — `hashes` may carry several distinct hashes (the
  // address-change population), each naming a different user. Reading two rows
  // is what makes "more than one" observable at all; erasing one of them
  // arbitrarily is the irreversible version of guessing.
  const byHash: Array<{ id: string; tenant_id: string | null; organization_id: string | null }> =
    await prisma.$queryRaw`
      SELECT id, tenant_id, organization_id FROM users
      WHERE email_lookup_hash IS NOT NULL AND email_lookup_hash = ANY(${hashes}::text[])
      ORDER BY id ASC
      LIMIT 2
    `;
  if (byHash.length === 0) return { userId: null, provenanceRows: rows.length };
  if (byHash.length > 1) {
    logger.warn('Connector erasure: external_ref hash-resolves to MORE THAN ONE user — refusing', {
      externalRef, callerTenantId: tenantId, matched: byHash.length,
    });
    throw new ConnectorErasureUnresolvableError(externalRef, 'ambiguous_subject');
  }
  const candidate = byHash[0];

  // uuid comparison. QA finding 11: the SQL one statement earlier casts to
  // ::uuid and compares canonically; this is a JS string compare of a
  // PG-canonical value against a JWT claim that nothing normalises. Both sides
  // are normalised through the SAME `normaliseOrgId` as the sibling resolver in
  // provenance.ts, so a differently-cased claim cannot read as a different
  // Organisation and the two cannot drift apart.
  const subjectOrg = normaliseOrgId(candidate.organization_id);
  const callerOrg = normaliseOrgId(connectorOrgId);

  // An ORG-LESS USER cannot be shown to belong to the caller's Organisation.
  // The sibling returns null (verbatim provenance, no 403: they are not in a
  // *different* org). Erasure cannot borrow that answer, because null here is
  // the silent-completion branch. Refused explicitly instead — and it is a
  // distinct reason from the cross-org case, because the caller is not at fault
  // and a human may need to attach the user to an Organisation.
  if (!subjectOrg) {
    logger.warn('Connector erasure: matched user has no organization_id — refusing to attribute', {
      externalRef, callerTenantId: tenantId, subjectTenantId: candidate.tenant_id,
    });
    throw new ConnectorErasureUnresolvableError(externalRef, 'subject_outside_connector_organisation');
  }
  if (subjectOrg !== callerOrg) {
    // Never silently downgrade to "unresolvable" — that is the F1 failure mode
    // wearing a different hat. A connector naming a subject outside its own
    // Organisation is a tenancy fault and must be visible.
    logger.warn('Connector erasure: external_ref hash-resolves to a user in ANOTHER Organisation — refusing', {
      externalRef, callerTenantId: tenantId, resolvedTenantId: candidate.tenant_id,
    });
    throw new ConnectorErasureCrossOrgError(externalRef);
  }

  // QA finding 5 — the NULL-TENANT user, decided explicitly rather than left to
  // fall out of a comparison. `users.tenant_id` is NULLABLE
  // (`docker/init/01-schema.sql:42`), and the old assertion `null !== tenantId`
  // refused such a user terminally with no branch and no case covering it. With
  // the ORGANISATION as the gate the tenant compare is secondary, so the rule
  // is stated: a user whose `organization_id` matches the caller's key RESOLVES
  // even when `tenant_id` is NULL. The organisation is the stronger claim — it
  // is what the key was minted against — and the ref was already proved to sit
  // in this tenant's provenance by the SELECT above.
  return { userId: candidate.id, provenanceRows: rows.length };
}

/**
 * Erase everything K holds for an S subject, addressed by `external_ref`.
 *
 * Two shapes, because K may hold a full user row for the subject or only
 * provenance rows:
 *
 *  - **Resolvable** — delegate to the existing `executeErasure`, with a DSR row
 *    synthesised here (K creates its own; S has no DSR to supply). That row is
 *    the idempotency record, so no new table is needed.
 *  - **Unresolvable** — `resolved_user_id` is null everywhere. There is no
 *    `users` row to erase, but there ARE `action_provenance` rows carrying that
 *    ref with identity columns in them. Blank those. **The post-erasure state
 *    of those rows is itself the idempotency record** — a repeat finds zero
 *    rows with a non-null identity column and returns without writing.
 *    (`data_subject_requests` cannot record this case: `user_id` and `email`
 *    are both NOT NULL and there is neither.)
 */
export async function executeErasureByExternalRef(
  externalRef: string,
  connectorId: string,
  tenantId: string,
  connectorOrgId?: string,
): Promise<ConnectorErasureResult> {
  return runWithPlatformScope(async () => {
    const { userId, provenanceRows } = await resolveExternalRef(externalRef, tenantId, connectorOrgId);

    if (userId) {
      // Read every TERMINAL erasure DSR for this subject, not just 'completed'.
      // Ordering puts 'denied' first so a refusal outranks an older completion:
      // if a human has denied an erasure, that decision governs the answer.
      const priorRows: Array<{ id: string; status: string }> = await prisma.$queryRaw`
        SELECT id, status FROM data_subject_requests
        WHERE user_id = ${userId}::uuid AND type = 'erasure'
          AND status IN ('completed', 'denied')
        ORDER BY CASE status WHEN 'denied' THEN 0 ELSE 1 END, requested_at DESC
        LIMIT 1
      `;
      if (priorRows.length > 0) {
        if (priorRows[0].status === 'denied') {
          // QA F-1. A denied DSR is terminal. Re-driving it would execute an
          // irreversible erasure a human refused and then overwrite the denial
          // with 'completed' — the audit trail of the refusal destroyed by the
          // act it forbade. Answer the refusal; never re-drive.
          logger.warn('Connector erasure refused — a denied erasure DSR is terminal', {
            externalRef, connectorId, dsrId: priorRows[0].id,
          });
          return { status: 'denied' as const, alreadyErased: false };
        }
        logger.info('Connector erasure is a repeat — not re-executing', { externalRef, connectorId });
        return { status: 'completed' as const, alreadyErased: true };
      }

      const performedBy = `connector:${connectorId}`;

      // Reuse an existing NON-TERMINAL erasure DSR instead of filing a fresh one
      // per attempt. S retries without bound, so a failing subject would
      // otherwise accumulate one orphan DSR row per retry — and from the second
      // attempt on, the `email` recorded on it is the post-anonymisation
      // sentinel rather than the subject's address.
      // NOT `status <> 'completed'` (QA F-1): that admits 'denied'. Terminal is
      // the SET above — the schema's CHECK enumerates five statuses and exactly
      // two of them conclude a request.
      const openRows: Array<{ id: string }> = await prisma.$queryRaw`
        SELECT id FROM data_subject_requests
        WHERE user_id = ${userId}::uuid AND type = 'erasure'
          AND status NOT IN ('completed', 'denied')
        ORDER BY requested_at ASC
        LIMIT 1
      `;
      let dsrId: string;
      if (openRows.length > 0) {
        dsrId = openRows[0].id;
        logger.info('Connector erasure is re-driving an existing non-terminal DSR', { externalRef, connectorId, dsrId });
      } else {
        // Peter F3. `users.email` is encrypted at rest — which is why
        // `email_lookup_hash` exists at all — and `createDSR` runs `writePii`
        // over whatever it is handed. Passing the stored value straight through
        // stored ciphertext-of-ciphertext, and `mapDsrRow` then decrypted once
        // to an unusable blob. Step 5c forty lines above already wraps the
        // identical query in `readPii`; this is the same read, so it does too.
        // The unit suite stubs PII encryption to the identity function, which
        // is precisely why nothing caught it.
        const subject: Array<{ email: string | null }> = await prisma.$queryRaw`
          SELECT email FROM users WHERE id = ${userId}::uuid LIMIT 1
        `;
        const subjectEmail = await readPii(subject[0]?.email, `users.email.${userId}`, userId);
        const dsr = await createDSR('erasure', userId, subjectEmail || '[unknown]', `KS-695: erasure requested by ${performedBy} for external_ref ${externalRef}`);
        dsrId = dsr.id;
      }

      // `executeErasureImpl` NEVER THROWS — its catch returns
      // `{ success: false, deletionLog }`. Discarding that and marking the DSR
      // completed anyway turned a FAILED Art. 17 erasure into a permanent
      // `alreadyErased: true`: S stops retrying, K's record says done, and the
      // step that failed is left standing with no retry path. Propagate it, the
      // way the admin route already does (`routes/gdpr.ts` — `result.success`).
      const result = await executeErasureImpl(userId, dsrId, performedBy);
      if (!result.success) {
        // Leave the DSR non-terminal so the block above re-drives THIS row on
        // S's next retry, and so the GET keeps answering `alreadyErased: false`.
        logger.error('Connector erasure did not complete — DSR left non-terminal for retry', {
          externalRef, connectorId, dsrId, dataTypesProcessed: result.deletionLog.length,
        });
        throw new ConnectorErasureIncompleteError(externalRef);
      }

      // NOT redundant on this path, despite step 12 of `executeErasureImpl`
      // calling `updateDSRStatus(dsrId, 'completed', performedBy)`: that write
      // sets `processed_by = ${performedBy}::uuid`, and `performedBy` here is
      // `connector:<id>`.
      //
      // ⚠ KS-754 IS FIXED AND THIS PARAGRAPH DESCRIBES THE OLD WORLD. It read:
      // `processed_by` is `uuid`, `SELECT 'connector:abc'::uuid` errors 22P02,
      // `updateDSRStatus` swallows that as a `false` nobody reads. Migration
      // 048 widened the column to TEXT and `updateDSRStatus` now rethrows, so
      // step 12 CAN write on this path and a failure is no longer silent.
      //
      // This raw UPDATE is therefore REDUNDANT rather than load-bearing. It is
      // left in place deliberately: removing a writer from a GDPR Art. 17
      // completion path is its own change with its own blast radius, and it
      // does not belong in the same PR as a schema migration. Ticketed.
      // Peter F2. `executeErasureImpl` matches provenance by
      // `resolved_user_id = userId` OR the subject's own email hash (step 5b).
      // A row written for the SAME PersonGuid under a DIFFERENT address — an
      // ordinary address change on S — satisfies neither, and the ref-scoped
      // blank previously ran only on the unresolvable branch, so those siblings
      // survived with `email_enc` and `display_name_enc` intact while the
      // caller was told `completed`. Run the ref-scoped blank here too: it is
      // idempotent, and it is the only clause that addresses rows BY REF.
      const siblings = await prisma.$executeRaw`
        UPDATE action_provenance SET
          email_enc = NULL, display_name_enc = NULL, email_hash = NULL
        WHERE external_ref = ${externalRef} AND tenant_id = ${tenantId}::uuid
          AND (email_enc IS NOT NULL OR display_name_enc IS NOT NULL OR email_hash IS NOT NULL)
      `;
      if (siblings > 0) {
        logger.info('Connector erasure blanked sibling provenance rows under the same ref', {
          externalRef, connectorId, rows: siblings,
        });
      }

      // Peter F8. The raw UPDATE substituted for step 12's `updateDSRStatus`,
      // which COULD NOT write on this path before KS-754 was fixed
      // (`processed_by` was uuid; `performedBy` is `connector:<id>`). It
      // recorded strictly less than the call it replaces: no audit-trail entry,
      // so the DSR that IS the accountability record for a connector Art. 17
      // erasure ended with a trail containing only `created`.
      //
      // ⚠ The sentence that used to close this comment — "`processed_by` still
      // cannot be written here" — is NO LONGER TRUE. Migration 048 widened the
      // column to TEXT, so the actor string this trail was added to preserve
      // can now live in the column it was always meant to occupy.
      const auditEntry = JSON.stringify({
        action: 'completed', timestamp: new Date().toISOString(), actor: performedBy,
      });
      await prisma.$executeRaw`
        UPDATE data_subject_requests SET
          status = 'completed', completed_at = NOW(), updated_at = NOW(),
          audit_trail = coalesce(audit_trail, '[]'::jsonb) || ${auditEntry}::jsonb
        WHERE id = ${dsrId}::uuid
      `;
      return { status: 'completed' as const, alreadyErased: false };
    }

    // Unresolvable. Erase what IS addressable by external_ref, then terminate.
    const remaining = await countUnerasedProvenance(externalRef, tenantId);
    if (provenanceRows === 0 || remaining === 0) {
      // Either K has never seen this ref, or it was erased already. Both are
      // terminal and both are honestly 'completed' — K holds nothing for the
      // subject either way.
      return { status: 'completed' as const, alreadyErased: true };
    }
    const blanked = await prisma.$executeRaw`
      UPDATE action_provenance SET
        email_enc = NULL, display_name_enc = NULL, email_hash = NULL
      WHERE external_ref = ${externalRef} AND tenant_id = ${tenantId}::uuid
    `;
    logger.info('Connector erasure blanked provenance identity for an unresolved subject', {
      externalRef, connectorId, rows: blanked,
    });
    return { status: 'completed' as const, alreadyErased: false };
  });
}

/** Rows for this ref, in this tenant, that still carry any identity column. */
async function countUnerasedProvenance(externalRef: string, tenantId: string): Promise<number> {
  const rows: Array<{ n: bigint }> = await prisma.$queryRaw`
    SELECT COUNT(*)::bigint AS n FROM action_provenance
    WHERE external_ref = ${externalRef} AND tenant_id = ${tenantId}::uuid
      AND (email_enc IS NOT NULL OR display_name_enc IS NOT NULL OR email_hash IS NOT NULL)
  `;
  return Number(rows[0]?.n ?? 0);
}

/**
 * Status read for S's convergence sweep. Never writes, and never 404s — same
 * reasoning as the POST.
 */
export async function getErasureStatusByExternalRef(
  externalRef: string,
  tenantId: string,
  connectorOrgId?: string,
): Promise<ConnectorErasureResult> {
  return runWithPlatformScope(async () => {
    const { userId } = await resolveExternalRef(externalRef, tenantId, connectorOrgId);
    if (userId) {
      // QA F-1, the read side. Reading only 'completed' made a DENIED erasure
      // report `alreadyErased: false`, so S's convergence sweep kept finding
      // outstanding work and kept POSTing — which is what drove the re-drive
      // in the first place. The GET has to be terminal wherever the POST is.
      const prior: Array<{ id: string; status: string }> = await prisma.$queryRaw`
        SELECT id, status FROM data_subject_requests
        WHERE user_id = ${userId}::uuid AND type = 'erasure'
          AND status IN ('completed', 'denied')
        ORDER BY CASE status WHEN 'denied' THEN 0 ELSE 1 END, requested_at DESC
        LIMIT 1
      `;
      if (prior.length > 0 && prior[0].status === 'denied') {
        return { status: 'denied' as const, alreadyErased: false };
      }
      // Peter F2, read side. Answering from the DSR row alone reported
      // `alreadyErased: true` while sibling provenance rows under the same ref
      // still carried identity columns, so S's convergence sweep terminated on
      // a subject K had only partly erased. Both have to be true.
      const refRemaining = await countUnerasedProvenance(externalRef, tenantId);
      return {
        status: 'completed' as const,
        alreadyErased: prior.length > 0 && refRemaining === 0,
      };
    }
    const remaining = await countUnerasedProvenance(externalRef, tenantId);
    return { status: 'completed' as const, alreadyErased: remaining === 0 };
  });
}
