/**
 * =============================================================================
 * KS-480 §6 — on-behalf-of provenance (connector attribution)
 * =============================================================================
 * A connector (sk_) caller acts for a real Platform-S user. The optional
 * body-level `onBehalfOf {email, displayName?, externalRef?}` carries that
 * user; this module owns its whole lifecycle:
 *
 *   validate  — connector-only (JWT callers 400), KS-202-trimmed shapes.
 *   resolve   — tenant-scoped email→user lookup (the KS-69 HMAC-hash
 *               mechanism). Same-org user → resolvedUserId (true per-user
 *               attribution); DIFFERENT org → 403 (a key attributes only
 *               within its own Organisation); no user → verbatim provenance.
 *               Never creates an account, never grants auth.
 *   record    — one row per attributed action in action_provenance
 *               (migration 041): email/displayName encrypted with the
 *               platform PII keyring, deterministic email_hash for erasure
 *               lookup, external_ref (S PersonGuid) plain — it survives
 *               pseudonymisation as the stable attribution id.
 *   echo      — document reads decrypt the creation row (first-class
 *               provenance, Peter §6-3 / Stuart).
 *   erasure   — pseudonymise: blank email/displayName/email_hash, KEEP
 *               external_ref + resolved_user_id (Peter §6-2).
 *
 * ON-CHAIN GUARANTEE (Peter §6-1): nothing this module stores is ever
 * anchored. The anchor payload builders are fixed-field whitelists
 * (documents.ts buildAnchorBody; anchoring metadataPayload, KS-240) and the
 * flat-anchor schema strips unknown keys. __tests__/ks480-provenance.test.ts
 * pins the structural exclusion.
 * =============================================================================
 */

import type { Request } from 'express';
import { z } from 'zod';
import { encryptField, decryptField, lookupHash } from '@secuura/shared';
import { prisma } from '../db';
import { logger } from '../utils/logger';
import { normaliseOrgId } from './orgId';

// KS-202: trim before content checks so '   ' fails min(1).
export const onBehalfOfSchema = z.object({
  email: z.string().trim().min(3).max(255).email(),
  displayName: z.string().trim().min(1).max(255).optional(),
  externalRef: z.string().trim().min(1).max(128).optional(),
});

export type OnBehalfOf = z.infer<typeof onBehalfOfSchema>;

/** Encryption contexts — stable strings, never derived from row data. */
const CTX_EMAIL = 'action_provenance.email';
const CTX_DISPLAY_NAME = 'action_provenance.display_name';

export class OnBehalfOfError extends Error {
  constructor(
    public status: 400 | 403,
    public code: 'BAD_REQUEST' | 'FORBIDDEN',
    message: string,
  ) {
    super(message);
  }
}

/**
 * Extract + validate `onBehalfOf` from a request body.
 *
 * @returns the validated triplet, or null when the body carries none.
 * @throws OnBehalfOfError 400 when a non-connector caller sends it (it is
 *         connector-only attribution, not an impersonation surface) or the
 *         shape is invalid.
 */
export function extractOnBehalfOf(req: Request): OnBehalfOf | null {
  const raw = (req.body as Record<string, unknown> | undefined)?.onBehalfOf;
  if (raw === undefined) return null;
  // KS-480 sweep follow-up: `null` is a spec violation (the published field is
  // object-or-absent), and anchoring's zod path already rejects it — treating
  // it as "absent" here made the two services diverge and let a
  // schema-violating body through with a 2xx.
  if (raw === null) {
    throw new OnBehalfOfError(400, 'BAD_REQUEST', 'onBehalfOf must be an object when provided (omit the field entirely for no attribution)');
  }

  const role = String((req as any).user?.role ?? '');
  if (role !== 'connector') {
    throw new OnBehalfOfError(400, 'BAD_REQUEST', 'onBehalfOf is connector-only — interactive callers act as themselves');
  }
  const parsed = onBehalfOfSchema.safeParse(raw);
  if (!parsed.success) {
    throw new OnBehalfOfError(400, 'BAD_REQUEST', 'onBehalfOf must be { email, displayName?, externalRef? } (valid email, non-empty strings)');
  }
  return parsed.data;
}

/**
 * Resolve the attributed email to a K user, tenant-scoped (KS-69 semantics).
 * The query runs under the request's tenant GUC (fail-closed RLS applies).
 *
 * @returns the same-org user's id, or null when no K user matches.
 * @throws OnBehalfOfError 403 when the email resolves to a DIFFERENT org —
 *         a key can only attribute within its own Organisation.
 */
export async function resolveOnBehalfOf(
  obo: OnBehalfOf,
  connectorOrgId: string | undefined,
): Promise<string | null> {
  // An org-less key (legacy / admin-minted without organizationId) has no
  // Organisation to validate against — resolving would attribute to ANY
  // matching tenant user. Store verbatim instead; only org-bound keys (§4
  // registration mints these) get per-user attribution.
  if (!connectorOrgId) return null;
  const hash = lookupHash(obo.email.toLowerCase());
  try {
    const rows = (await prisma.$queryRaw`
      SELECT id, organization_id FROM users WHERE email_lookup_hash = ${hash} LIMIT 1
    `) as Array<{ id: string; organization_id: string | null }>;
    if (rows.length === 0) return null;
    const user = rows[0];

    // QA F-4: these two comparisons were RAW string compares of a PG-canonical
    // column against a connector-supplied claim that nothing normalises — the
    // same defect the sibling resolver fixed at `gdprService.ts:1249` and the
    // identical class, on the identical relationship. A differently-cased or
    // space-padded claim read as a DIFFERENT Organisation, which on this path
    // means a same-org user silently loses per-user attribution (and, one line
    // up, a same-org caller can be 403'd). Both sides go through the SAME
    // `normaliseOrgId` as the sibling resolver — one implementation, so the two
    // cannot drift apart again (Peter Obeden's #795 review: two byte-identical
    // private copies is the arrangement that produced the drift).
    const subjectOrg = normaliseOrgId(user.organization_id);
    const callerOrg = normaliseOrgId(connectorOrgId);

    if (subjectOrg && subjectOrg !== callerOrg) {
      throw new OnBehalfOfError(403, 'FORBIDDEN', 'onBehalfOf user belongs to a different Organisation than this key');
    }
    // Same-org user → true per-user attribution. An org-LESS user is not in
    // the key's Organisation either — verbatim provenance, no resolution
    // (and no 403: they are not in a *different* org).
    return subjectOrg !== null && subjectOrg === callerOrg ? user.id : null;
  } catch (err) {
    if (err instanceof OnBehalfOfError) throw err;
    // Lookup infrastructure failure → attribute verbatim rather than fail the
    // write; the provenance row still records who acted.
    logger.warn('onBehalfOf resolution failed — storing verbatim provenance', { error: (err as Error).message });
    return null;
  }
}

export interface ProvenanceRecord {
  documentId: string;
  action: string;
  tenantId: string;
  organizationId?: string;
  connectorId?: string;
  /**
   * KS-566: OPTIONAL since the G-1 split. `null`/absent is the CONNECTOR
   * pattern (anchor / lifecycle) — the operation is attributed to the key
   * itself and carries no principal. Present is the onBehalfOf pattern
   * (share / revoke / transfer-custody).
   */
  obo?: OnBehalfOf | null;
  resolvedUserId?: string | null;
}

/** The ten column values of one `action_provenance` row (migration 041). */
export interface ProvenanceRow {
  tenantId: string;
  organizationId: string | null;
  documentId: string;
  action: string;
  connectorId: string | null;
  emailEnc: string | null;
  displayNameEnc: string | null;
  emailHash: string | null;
  externalRef: string | null;
  resolvedUserId: string | null;
}

/**
 * KS-566 — THE single row-construction path, extracted so the two attribution
 * patterns are one function rather than two remembered field lists (same
 * reasoning as anchoring's buildFlatAnchorMetadataPayload whitelist).
 *
 * With `obo`   → the attributed row: email/displayName encrypted, deterministic
 *                email_hash for erasure lookup, external_ref plain (it is the
 *                pseudonym that survives erasure — Peter §6-2).
 * Without      → the CONNECTOR-ONLY row: connector_id is the actor and every
 *                identity column is NULL. Notably `email_hash` too — it is the
 *                GDPR lookup key, and a row with no subject must not carry one
 *                or erasure would claim a subject it cannot name.
 *
 * Pure: no I/O, so the shape is unit-testable without a database
 * (__tests__/ks566-g1-split.test.ts).
 */
export function buildProvenanceRow(rec: ProvenanceRecord): ProvenanceRow {
  const obo = rec.obo ?? null;
  return {
    tenantId: rec.tenantId,
    organizationId: rec.organizationId || null,
    documentId: rec.documentId,
    action: rec.action,
    connectorId: rec.connectorId || null,
    emailEnc: obo ? encryptField(obo.email, CTX_EMAIL) : null,
    displayNameEnc: obo?.displayName ? encryptField(obo.displayName, CTX_DISPLAY_NAME) : null,
    emailHash: obo ? lookupHash(obo.email.toLowerCase()) : null,
    externalRef: obo?.externalRef || null,
    resolvedUserId: rec.resolvedUserId || null,
  };
}

/**
 * Append one provenance row (fire-and-forget safe — callers may .catch(log)).
 * email/displayName encrypted; email_hash deterministic for erasure lookup.
 * KS-566: one row per attributed operation on EITHER pattern — the connector
 * path no longer writes nothing.
 */
export async function recordActionProvenance(rec: ProvenanceRecord): Promise<void> {
  const row = buildProvenanceRow(rec);
  await prisma.$executeRaw`
    INSERT INTO action_provenance (
      tenant_id, organization_id, document_id, action, connector_id,
      email_enc, display_name_enc, email_hash, external_ref, resolved_user_id
    ) VALUES (
      ${row.tenantId}::uuid,
      ${row.organizationId}::uuid,
      ${row.documentId},
      ${row.action},
      ${row.connectorId},
      ${row.emailEnc},
      ${row.displayNameEnc},
      ${row.emailHash},
      ${row.externalRef},
      ${row.resolvedUserId}::uuid
    )
  `;
}

export interface EchoedProvenance {
  email: string | null;
  displayName: string | null;
  externalRef: string | null;
  resolvedUserId: string | null;
  /** True once erasure has pseudonymised the row (email/displayName gone). */
  pseudonymised: boolean;
}

/**
 * The creation-action provenance for a document, decrypted for echo in reads.
 * Returns null when the document has none (non-connector creation).
 */
export async function getCreationProvenance(documentId: string): Promise<EchoedProvenance | null> {
  try {
    const rows = (await prisma.$queryRaw`
      SELECT email_enc, display_name_enc, external_ref, resolved_user_id
      FROM action_provenance
      WHERE document_id = ${documentId} AND action = 'create'
      ORDER BY created_at ASC LIMIT 1
    `) as Array<{
      email_enc: string | null;
      display_name_enc: string | null;
      external_ref: string | null;
      resolved_user_id: string | null;
    }>;
    if (rows.length === 0) return null;
    const r = rows[0];
    return {
      email: r.email_enc ? decryptField(r.email_enc, CTX_EMAIL) : null,
      displayName: r.display_name_enc ? decryptField(r.display_name_enc, CTX_DISPLAY_NAME) : null,
      externalRef: r.external_ref,
      resolvedUserId: r.resolved_user_id,
      pseudonymised: !r.email_enc,
    };
  } catch (err) {
    // Table missing (pre-migration boot) or decrypt failure — reads must not
    // break over provenance.
    logger.warn('getCreationProvenance failed', { documentId, error: (err as Error).message });
    return null;
  }
}

/**
 * True when this connector recorded the document's creation provenance.
 * Read-back guard: attributing a document to a resolved user sets
 * owner_user_id, which would otherwise 404-cloak the very key that created
 * it — S drives the document's whole lifecycle through this id.
 */
export async function wasCreatedByConnector(documentId: string, connectorUserId: string): Promise<boolean> {
  try {
    const rows = (await prisma.$queryRaw`
      SELECT 1 AS ok FROM action_provenance
      WHERE document_id = ${documentId} AND action = 'create' AND connector_id = ${connectorUserId}
      LIMIT 1
    `) as Array<{ ok: number }>;
    return rows.length > 0;
  } catch {
    return false;
  }
}

/**
 * GDPR erasure (Peter §6-2): pseudonymise every provenance row for a subject
 * email — blank the encrypted identity fields AND the derived email_hash,
 * keep external_ref + resolved_user_id as the stable non-identifying
 * attribution. Returns the number of rows pseudonymised.
 */
export async function pseudonymiseProvenanceByEmail(email: string): Promise<number> {
  const hash = lookupHash(email.toLowerCase().trim());
  const n = await prisma.$executeRaw`
    UPDATE action_provenance
    SET email_enc = NULL, display_name_enc = NULL, email_hash = NULL
    WHERE email_hash = ${hash}
  `;
  return Number(n);
}
