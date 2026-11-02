/**
 * =============================================================================
 * LIFECYCLE EVENT REPOSITORY — KS-387 generic non-mutating lifecycle rows
 * =============================================================================
 * Persistence for `document_lifecycle_events` (migration 037): one row per
 * lifecycle verb performed against a document that has NO dedicated endpoint.
 * KS-1275: the accepted set is LIFECYCLE_EVENT_ACTIONS in
 * services/originate/src/lifecycleActions.ts, and the vocabulary contract is
 * docs/VOCABULARY.md. An inline list of the verbs stood here and had drifted
 * from both — it named neither the KS-534 share-attach-consent verb, the KS-556
 * protect/unprotect pair, nor the KS-1172/KS-1173 additions — so it is replaced
 * by these pointers rather than re-synchronised. Rows are NON-MUTATING — they attach to the
 * current document via `parent_document_id` (no version fork), mirroring
 * Platform-S's PreviousChainId chain in K's lineage.
 *
 * Mirrors shareRepo's conventions: routes pass the document's external_id and
 * the INSERT resolves it to the internal documents.id UUID in a tenant-scoped
 * subquery; a NULL resolution (document not in this tenant) surfaces as a typed
 * LIFECYCLE_TARGET_NOT_FOUND error the route maps to 404.
 * =============================================================================
 */

import { prisma } from '../db';
import { v4 as uuidv4 } from 'uuid';
import { logger } from '../utils/logger';
import { encodeLifecyclePayload, decodeLifecyclePayload } from '../utils/lifecyclePayloadCodec';

type DbClient = typeof prisma;

/** One recorded lifecycle event, as the API returns it. */
export interface LifecycleEventRecord {
  id: string;
  tenantId: string;
  /** External id of the document the event attaches to (as the caller supplied it). */
  documentId: string;
  action: string;
  payload: Record<string, unknown>;
  actorUserId: string | null;
  anchorId: string | null;
  createdAt: string;
}

/**
 * Insert one lifecycle event row for a document (resolved by external_id within
 * the tenant). Returns the stored record; throws LIFECYCLE_TARGET_NOT_FOUND when
 * the document does not exist in this tenant (NULL subquery → NOT NULL violation,
 * same detection shareRepo uses).
 */
export async function createLifecycleEvent(
  input: {
    tenantId: string;
    documentId: string;
    action: string;
    payload?: Record<string, unknown> | null;
    actorUserId?: string | null;
    anchorId?: string | null;
  },
  db?: DbClient,
): Promise<LifecycleEventRecord> {
  const id = uuidv4();
  const now = new Date();
  const payload = input.payload ?? {};
  // KS-537: caller-supplied payloads are PII-bearing (the old spec example
  // even recommended an email) — encrypt at rest, AAD bound to this row.
  const storedPayload = encodeLifecyclePayload(payload, id);
  try {
    await (db || prisma).$executeRaw`
      INSERT INTO document_lifecycle_events (
        id, tenant_id, parent_document_id, action, payload, actor_user_id, anchor_id, created_at
      ) VALUES (
        ${id}::uuid,
        ${input.tenantId}::uuid,
        (SELECT id FROM documents WHERE external_id = ${input.documentId} AND tenant_id = ${input.tenantId}::uuid LIMIT 1),
        ${input.action},
        ${storedPayload}::jsonb,
        ${input.actorUserId ?? null}::uuid,
        ${input.anchorId ?? null},
        ${now}
      )
    `;
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    if (msg.includes('null value in column "parent_document_id"')) {
      // Subquery returned no row — document not in this tenant.
      const friendlyErr: Error & { code?: string } = new Error(
        `Lifecycle target ${input.documentId} not found in tenant ${input.tenantId}`,
      );
      friendlyErr.code = 'LIFECYCLE_TARGET_NOT_FOUND';
      throw friendlyErr;
    }
    logger.error('createLifecycleEvent failed', { documentId: input.documentId, action: input.action, error: msg });
    throw err;
  }
  return {
    id,
    tenantId: input.tenantId,
    documentId: input.documentId,
    action: input.action,
    payload,
    actorUserId: input.actorUserId ?? null,
    anchorId: input.anchorId ?? null,
    createdAt: now.toISOString(),
  };
}

/**
 * Record the anchor id emitted for an already-inserted event (anchor emission
 * runs AFTER the row commit so an anchoring outage never loses the event).
 */
export async function setLifecycleEventAnchor(id: string, anchorId: string, db?: DbClient): Promise<void> {
  await (db || prisma).$executeRaw`
    UPDATE document_lifecycle_events SET anchor_id = ${anchorId} WHERE id = ${id}::uuid
  `;
}

/**
 * List a document's lifecycle events (tenant-scoped, newest first). The document
 * is matched by external_id, mirroring how routes address documents everywhere.
 */
export async function listLifecycleEvents(
  documentId: string,
  tenantId: string,
  db?: DbClient,
): Promise<LifecycleEventRecord[]> {
  const rows = (await (db || prisma).$queryRaw`
    SELECT e.id, e.tenant_id, e.action, e.payload, e.actor_user_id, e.anchor_id, e.created_at
    FROM document_lifecycle_events e
    JOIN documents d ON d.id = e.parent_document_id
    WHERE d.external_id = ${documentId} AND e.tenant_id = ${tenantId}::uuid
    ORDER BY e.created_at DESC
  `) as Array<Record<string, unknown>>;
  return rows.map((r) => ({
    id: String(r.id),
    tenantId: String(r.tenant_id),
    documentId,
    action: String(r.action),
    // KS-537: encrypted rows decode here; legacy plaintext objects pass through.
    payload: decodeLifecyclePayload(r.payload, String(r.id)),
    actorUserId: r.actor_user_id ? String(r.actor_user_id) : null,
    anchorId: r.anchor_id ? String(r.anchor_id) : null,
    createdAt: r.created_at instanceof Date ? r.created_at.toISOString() : String(r.created_at),
  }));
}
