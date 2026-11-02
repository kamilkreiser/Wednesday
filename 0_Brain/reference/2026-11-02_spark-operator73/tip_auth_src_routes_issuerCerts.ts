/**
 * =============================================================================
 * ISSUER CERTS ROUTES — KS-83 PR 1
 * =============================================================================
 * Per-org X.509 cert lifecycle: upload, list, get one. Revoke + rotate
 * land in PR 2; sign-cert integration with /api/documents/{id}/version
 * (KS-86) lands in PR 3.
 *
 * RBAC:
 *   - POST   /api/issuer-certs   → ORG_ADMIN+ role  OR  `issuer-certs:write`
 *   - GET    /api/issuer-certs   → ORG_ADMIN+ role  OR  `issuer-certs:read`
 *   - GET    /api/issuer-certs/:id → same as list
 *
 * Tenant scoping: every read/write filters by `req.user.tenantId` (the JWT
 * tenant claim). RLS on the table is permissive defence-in-depth.
 *
 * Security notes:
 *   - The private-key PEM is encrypted before INSERT and never logged.
 *   - List/get responses use `toSummary()` which strips the encrypted blob
 *     so the ciphertext doesn't even leave the service.
 *   - Audit log captures upload + access events (uploaded_by_id is the
 *     authoritative actor; revoked_by_id will be in PR 2).
 * =============================================================================
 */

import { Router, Response } from 'express';
import { z } from 'zod';
import { AuthenticatedRequest } from '../types';
import { authenticate } from '../middleware/authenticate';
import { logger } from '../utils/logger';
import {
  parseCert,
  verifyKeyMatchesCert,
  encryptPrivateKeyPem,
  signContentHashWithCert,
  IssuerCertError,
} from '../services/issuerCert';
import {
  createIssuerCert,
  getIssuerCertById,
  findIssuerCertByFingerprint,
  findActiveIssuerCertForTenant,
  listIssuerCerts,
  revokeIssuerCert,
  rotateIssuerCert,
  toSummary,
  IssuerCertSummary,
  IssuerCertStatus,
} from '../repositories/issuerCertRepo';
import { publishEvent, EventTypes } from '../events';

export const issuerCertsRoutes = Router();

// =============================================================================
// HELPERS
// =============================================================================

/**
 * Roles that may manage issuer certs. Mirrors the admin gate used in
 * users.ts; if/when api-gateway adds scope-based gating for these
 * routes the scope check below complements (not replaces) it.
 */
const ADMIN_ROLES = ['ORG_ADMIN', 'SYSTEM_ADMIN', 'ISSUER_ADMIN', 'SUPER_ADMIN', 'admin', 'super_admin'];

/**
 * The one role test the four gates below share: the role claim, read as text, is in ADMIN_ROLES either as it is or upper-cased.
 * Behaviour-preserving extraction of the two lines that were copied into each gate.
 */
export function hasAdminRole(role: unknown): boolean {
  const text = String(role ?? '');
  return ADMIN_ROLES.includes(text) || ADMIN_ROLES.includes(text.toUpperCase());
}

function isAuthorisedForCertWrite(req: AuthenticatedRequest): boolean {
  const user = req.user as { role?: string; scopes?: string[] } | undefined;
  if (!user) return false;
  if (hasAdminRole(user.role)) return true;
  const scopes = Array.isArray(user.scopes) ? user.scopes : [];
  return scopes.includes('issuer-certs:write') || scopes.includes('issuer-certs:*') || scopes.includes('*');
}

function isAuthorisedForCertRead(req: AuthenticatedRequest): boolean {
  const user = req.user as { role?: string; scopes?: string[] } | undefined;
  if (!user) return false;
  if (hasAdminRole(user.role)) return true;
  const scopes = Array.isArray(user.scopes) ? user.scopes : [];
  return (
    scopes.includes('issuer-certs:read') ||
    scopes.includes('issuer-certs:write') ||  // write implies read
    scopes.includes('issuer-certs:*') ||
    scopes.includes('*')
  );
}

function isAuthorisedForCertRevoke(req: AuthenticatedRequest): boolean {
  const user = req.user as { role?: string; scopes?: string[] } | undefined;
  if (!user) return false;
  if (hasAdminRole(user.role)) return true;
  const scopes = Array.isArray(user.scopes) ? user.scopes : [];
  return (
    scopes.includes('issuer-certs:revoke') ||
    scopes.includes('issuer-certs:*') ||
    scopes.includes('*')
  );
}

function isAuthorisedForCertSign(req: AuthenticatedRequest): boolean {
  const user = req.user as { role?: string; scopes?: string[] } | undefined;
  if (!user) return false;
  // Signing is a sensitive op — the role gate stays the same admin
  // allow-list, plus a dedicated `issuer-certs:sign` scope for the
  // SSD connector path (originate calls this on behalf of the caller,
  // forwarding the Bearer token, so the caller's scopes apply).
  if (hasAdminRole(user.role)) return true;
  const scopes = Array.isArray(user.scopes) ? user.scopes : [];
  return (
    scopes.includes('issuer-certs:sign') ||
    scopes.includes('issuer-certs:*') ||
    scopes.includes('*')
  );
}

function getReqTenantId(req: AuthenticatedRequest): string | null {
  const user = req.user as { tenantId?: string } | undefined;
  return user?.tenantId || null;
}

function publicResponse(summary: IssuerCertSummary): Record<string, unknown> {
  return {
    id: summary.id,
    name: summary.name,
    organizationId: summary.organizationId,
    fingerprintSha256: summary.fingerprintSha256,
    subject: summary.subject,
    issuer: summary.issuer,
    serialNumber: summary.serialNumber,
    validFrom: summary.validFrom.toISOString(),
    validUntil: summary.validUntil.toISOString(),
    keyAlgorithm: summary.keyAlgorithm,
    keySizeBits: summary.keySizeBits,
    trustLevel: summary.trustLevel,
    status: summary.status,
    uploadedAt: summary.uploadedAt.toISOString(),
    uploadedById: summary.uploadedById,
    revokedAt: summary.revokedAt ? summary.revokedAt.toISOString() : null,
    revokedById: summary.revokedById,
    revocationReason: summary.revocationReason,
    previousCertId: summary.previousCertId,
    // certPem is included so consumers can ship the public cert with
    // signatures (offline verifiers need it). Never includes the
    // encrypted private key — that's repo-level only.
    certPem: summary.certPem,
  };
}

function mapCertErrorStatus(code: string): number {
  switch (code) {
    case 'INVALID_CERT_PEM':
    case 'MULTI_CERT_PEM':
    case 'KEY_PARSE_ERROR':
    case 'INVALID_CONTENT_HASH':
      return 400;
    case 'CERT_EXPIRED':
    case 'CERT_NOT_YET_VALID':
    case 'KEY_MISMATCH':
    case 'UNSUPPORTED_KEY_ALGORITHM':
      return 422;
    case 'SIGN_FAILED':
    case 'DECRYPTION_FAILED':
      return 500;
    default:
      return 500;
  }
}

// =============================================================================
// VALIDATION
// =============================================================================

const uploadSchema = z
  .object({
    name: z.string().trim().min(1).max(200),
    certPem: z.string().min(1),
    privateKeyPem: z.string().min(1),
    privateKeyPassword: z.string().optional(),
    organizationId: z.string().uuid().optional(),
  })
  .strict();

// =============================================================================
// POST /api/issuer-certs — upload a cert + private key
// =============================================================================
issuerCertsRoutes.post('/', authenticate(), async (req: AuthenticatedRequest, res: Response) => {
  try {
    if (!isAuthorisedForCertWrite(req)) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit issuer-cert upload' },
      });
    }

    const tenantId = getReqTenantId(req);
    if (!tenantId) {
      return res.status(400).json({
        success: false,
        error: { code: 'TENANT_REQUIRED', message: 'Authenticated user has no tenantId claim' },
      });
    }

    const parsed = uploadSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: parsed.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('; '),
          details: parsed.error.issues,
        },
      });
    }

    const { name, certPem, privateKeyPem, privateKeyPassword, organizationId } = parsed.data;

    // 1. Parse the cert (catches malformed PEM, expired, multi-cert chain)
    let parsedCert;
    try {
      parsedCert = parseCert(certPem);
    } catch (err) {
      if (err instanceof IssuerCertError) {
        return res.status(mapCertErrorStatus(err.code)).json({
          success: false,
          error: { code: err.code, message: err.message },
        });
      }
      throw err;
    }

    // 2. Verify the private key matches the cert (sign + verify roundtrip)
    try {
      verifyKeyMatchesCert(parsedCert.certPem, privateKeyPem, privateKeyPassword);
    } catch (err) {
      if (err instanceof IssuerCertError) {
        return res.status(mapCertErrorStatus(err.code)).json({
          success: false,
          error: { code: err.code, message: err.message },
        });
      }
      throw err;
    }

    // 3. Idempotent upload — same fingerprint within a tenant returns the
    //    existing row instead of creating a duplicate.
    const existing = await findIssuerCertByFingerprint(parsedCert.fingerprintSha256, tenantId);
    if (existing) {
      logger.info('Issuer cert upload: returning existing row (idempotent)', {
        id: existing.id,
        tenantId,
        fingerprint: parsedCert.fingerprintSha256.slice(0, 16),
      });
      return res.status(200).json({
        success: true,
        cert: publicResponse(toSummary(existing)),
        idempotent: true,
      });
    }

    // 4. Pre-mint the row id so we can encrypt the private key with the
    //    correct AAD context in a single write. The AAD binds the
    //    ciphertext to the row id — a swap between rows fails AES-GCM
    //    verification rather than silently decrypting to the wrong key.
    const certId = (await import('crypto')).randomUUID();
    const encryptedPrivateKey = encryptPrivateKeyPem(privateKeyPem, certId);

    const created = await createIssuerCert({
      id: certId,
      tenantId,
      organizationId: organizationId ?? null,
      name,
      fingerprintSha256: parsedCert.fingerprintSha256,
      subject: parsedCert.subject,
      issuer: parsedCert.issuer,
      serialNumber: parsedCert.serialNumber,
      validFrom: parsedCert.validFrom,
      validUntil: parsedCert.validUntil,
      keyAlgorithm: parsedCert.keyAlgorithm,
      keySizeBits: parsedCert.keySizeBits,
      trustLevel: parsedCert.trustLevel,
      certPem: parsedCert.certPem,
      encryptedPrivateKey,
      uploadedById: req.user!.userId as string,
    });

    logger.info('Issuer cert uploaded', {
      id: created.id,
      tenantId,
      fingerprint: parsedCert.fingerprintSha256.slice(0, 16),
      subject: parsedCert.subject,
      trustLevel: parsedCert.trustLevel,
      validUntil: parsedCert.validUntil.toISOString(),
      uploadedById: req.user!.userId,
    });

    publishEvent(EventTypes.ISSUER_CERT_UPLOADED, {
      certId: created.id,
      tenantId,
      fingerprintSha256: parsedCert.fingerprintSha256,
      subject: parsedCert.subject,
      trustLevel: parsedCert.trustLevel,
      validUntil: parsedCert.validUntil.toISOString(),
      uploadedById: req.user!.userId as string,
    }).catch(() => {});

    return res.status(201).json({
      success: true,
      cert: publicResponse(toSummary(created)),
    });
  } catch (err) {
    logger.error('Issuer cert upload failed', {
      error: err instanceof Error ? err.message : String(err),
    });
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to upload issuer cert' },
    });
  }
});

// =============================================================================
// GET /api/issuer-certs — list certs for the caller's tenant
// =============================================================================
issuerCertsRoutes.get('/', authenticate(), async (req: AuthenticatedRequest, res: Response) => {
  try {
    if (!isAuthorisedForCertRead(req)) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit issuer-cert read' },
      });
    }

    const tenantId = getReqTenantId(req);
    if (!tenantId) {
      return res.status(400).json({
        success: false,
        error: { code: 'TENANT_REQUIRED', message: 'Authenticated user has no tenantId claim' },
      });
    }

    const limit = Math.min(parseInt((req.query.limit as string) || '50', 10), 200);
    const offset = Math.max(parseInt((req.query.offset as string) || '0', 10), 0);
    const statusParam = req.query.status as string | undefined;
    const validStatuses: IssuerCertStatus[] = ['active', 'revoked', 'expired'];
    const status =
      statusParam && validStatuses.includes(statusParam as IssuerCertStatus)
        ? (statusParam as IssuerCertStatus)
        : undefined;

    const { certs, total } = await listIssuerCerts({ tenantId, status, limit, offset });

    return res.status(200).json({
      success: true,
      certs: certs.map((c) => publicResponse(toSummary(c))),
      pagination: { total, limit, offset },
    });
  } catch (err) {
    logger.error('Issuer cert list failed', {
      error: err instanceof Error ? err.message : String(err),
    });
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to list issuer certs' },
    });
  }
});

// =============================================================================
// GET /api/issuer-certs/:id — get one cert
// =============================================================================
issuerCertsRoutes.get('/:id', authenticate(), async (req: AuthenticatedRequest, res: Response) => {
  try {
    if (!isAuthorisedForCertRead(req)) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit issuer-cert read' },
      });
    }

    const tenantId = getReqTenantId(req);
    if (!tenantId) {
      return res.status(400).json({
        success: false,
        error: { code: 'TENANT_REQUIRED', message: 'Authenticated user has no tenantId claim' },
      });
    }

    const cert = await getIssuerCertById(req.params.id, tenantId);
    if (!cert) {
      return res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'Issuer cert not found in this tenant' },
      });
    }

    return res.status(200).json({
      success: true,
      cert: publicResponse(toSummary(cert)),
    });
  } catch (err) {
    // KS-210: a non-uuid :id (e.g. "0") makes the `id::uuid` cast in
    // getIssuerCertById throw pg 22P02 (invalid_text_representation) before the
    // not-found check — treat it as 404 (no such issuer cert), not a 500
    // (KS-111 "500-on-bad-input" class).
    if ((err as { code?: string })?.code === '22P02') {
      return res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'Issuer cert not found in this tenant' },
      });
    }
    logger.error('Issuer cert get failed', {
      error: err instanceof Error ? err.message : String(err),
    });
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to get issuer cert' },
    });
  }
});

// =============================================================================
// POST /api/issuer-certs/:id/revoke — KS-83 PR 2
// =============================================================================
const revokeSchema = z.object({ reason: z.string().trim().max(500).optional() }).strict();

issuerCertsRoutes.post('/:id/revoke', authenticate(), async (req: AuthenticatedRequest, res: Response) => {
  try {
    if (!isAuthorisedForCertRevoke(req)) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit issuer-cert revoke' },
      });
    }

    const tenantId = getReqTenantId(req);
    if (!tenantId) {
      return res.status(400).json({
        success: false,
        error: { code: 'TENANT_REQUIRED', message: 'Authenticated user has no tenantId claim' },
      });
    }

    const parsed = revokeSchema.safeParse(req.body || {});
    if (!parsed.success) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: parsed.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('; '),
          details: parsed.error.issues,
        },
      });
    }

    // Snapshot pre-state so we can distinguish first-revoke (200) from
    // already-revoked (409) without race conditions on the UPDATE.
    const existing = await getIssuerCertById(req.params.id, tenantId);
    if (!existing) {
      return res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'Issuer cert not found in this tenant' },
      });
    }

    if (existing.status === 'revoked') {
      return res.status(409).json({
        success: false,
        error: {
          code: 'ALREADY_REVOKED',
          message: `Cert was already revoked at ${existing.revokedAt?.toISOString()}`,
        },
        cert: publicResponse(toSummary(existing)),
      });
    }

    const updated = await revokeIssuerCert({
      id: req.params.id,
      tenantId,
      revokedById: req.user!.userId as string,
      reason: parsed.data.reason,
    });
    if (!updated) {
      // Lost a race to a concurrent revoke / delete — surface as 404.
      return res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'Issuer cert vanished between read and update' },
      });
    }

    publishEvent(EventTypes.ISSUER_CERT_REVOKED, {
      certId: updated.id,
      tenantId,
      fingerprintSha256: updated.fingerprintSha256,
      revokedById: req.user!.userId as string,
      reason: parsed.data.reason ?? null,
    }).catch(() => {});

    return res.status(200).json({
      success: true,
      cert: publicResponse(toSummary(updated)),
    });
  } catch (err) {
    logger.error('Issuer cert revoke failed', {
      error: err instanceof Error ? err.message : String(err),
    });
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to revoke issuer cert' },
    });
  }
});

// =============================================================================
// POST /api/issuer-certs/:id/rotate — KS-83 PR 2
// =============================================================================
// Atomic rotate: validate the new cert+key, revoke the old row, insert
// the new row with previous_cert_id linked. Either both succeed or
// neither does (single transaction in the repo). Historical signatures
// stay valid forever — they reference the OLD cert by fingerprint, which
// is preserved as a row in status=revoked.
const rotateSchema = z
  .object({
    name: z.string().trim().min(1).max(200).optional(),
    certPem: z.string().min(1),
    privateKeyPem: z.string().min(1),
    privateKeyPassword: z.string().optional(),
    organizationId: z.string().uuid().optional(),
    reason: z.string().trim().max(500).optional(),
  })
  .strict();

issuerCertsRoutes.post('/:id/rotate', authenticate(), async (req: AuthenticatedRequest, res: Response) => {
  try {
    // Rotate is essentially "revoke + upload" — gate on BOTH scopes so a
    // caller that only has revoke can't sneak through an upload.
    if (!isAuthorisedForCertWrite(req) || !isAuthorisedForCertRevoke(req)) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit issuer-cert rotate (needs both write + revoke)' },
      });
    }

    const tenantId = getReqTenantId(req);
    if (!tenantId) {
      return res.status(400).json({
        success: false,
        error: { code: 'TENANT_REQUIRED', message: 'Authenticated user has no tenantId claim' },
      });
    }

    const parsed = rotateSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: parsed.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('; '),
          details: parsed.error.issues,
        },
      });
    }

    const { name, certPem, privateKeyPem, privateKeyPassword, organizationId, reason } = parsed.data;

    // 1. Confirm the old cert exists and is currently active.
    const oldCert = await getIssuerCertById(req.params.id, tenantId);
    if (!oldCert) {
      return res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'Old issuer cert not found in this tenant' },
      });
    }
    if (oldCert.status !== 'active') {
      return res.status(409).json({
        success: false,
        error: {
          code: 'NOT_ACTIVE',
          message: `Cannot rotate cert in status '${oldCert.status}'. Only active certs can be rotated.`,
        },
      });
    }

    // 2. Parse + verify the NEW cert (same logic as upload).
    let parsedCert;
    try {
      parsedCert = parseCert(certPem);
    } catch (err) {
      if (err instanceof IssuerCertError) {
        return res.status(mapCertErrorStatus(err.code)).json({
          success: false,
          error: { code: err.code, message: err.message },
        });
      }
      throw err;
    }

    // Reject same-fingerprint rotation — that's a no-op masquerading as
    // a rotation and would create a self-referencing previous_cert_id
    // confusion (FK technically allows it but semantically meaningless).
    if (parsedCert.fingerprintSha256 === oldCert.fingerprintSha256) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'SAME_FINGERPRINT',
          message: 'New cert fingerprint matches the old cert — rotation requires a different cert',
        },
      });
    }

    try {
      verifyKeyMatchesCert(parsedCert.certPem, privateKeyPem, privateKeyPassword);
    } catch (err) {
      if (err instanceof IssuerCertError) {
        return res.status(mapCertErrorStatus(err.code)).json({
          success: false,
          error: { code: err.code, message: err.message },
        });
      }
      throw err;
    }

    // 3. Pre-mint UUID + encrypt private key with the AAD context bound
    //    to that id (same invariant as upload).
    const newCertId = (await import('crypto')).randomUUID();
    const encryptedPrivateKey = encryptPrivateKeyPem(privateKeyPem, newCertId);

    // 4. Atomic rotation: revoke old + insert new in one transaction.
    const result = await rotateIssuerCert({
      oldCertId: oldCert.id,
      tenantId,
      rotatedById: req.user!.userId as string,
      reason: reason ?? 'rotated',
      newCert: {
        id: newCertId,
        tenantId,
        organizationId: organizationId ?? oldCert.organizationId ?? null,
        name: name ?? oldCert.name,
        fingerprintSha256: parsedCert.fingerprintSha256,
        subject: parsedCert.subject,
        issuer: parsedCert.issuer,
        serialNumber: parsedCert.serialNumber,
        validFrom: parsedCert.validFrom,
        validUntil: parsedCert.validUntil,
        keyAlgorithm: parsedCert.keyAlgorithm,
        keySizeBits: parsedCert.keySizeBits,
        trustLevel: parsedCert.trustLevel,
        certPem: parsedCert.certPem,
        encryptedPrivateKey,
        uploadedById: req.user!.userId as string,
      },
    });

    publishEvent(EventTypes.ISSUER_CERT_ROTATED, {
      oldCertId: result.oldCert.id,
      newCertId: result.newCert.id,
      tenantId,
      newFingerprintSha256: result.newCert.fingerprintSha256,
      rotatedById: req.user!.userId as string,
      reason: reason ?? 'rotated',
    }).catch(() => {});

    return res.status(201).json({
      success: true,
      newCert: publicResponse(toSummary(result.newCert)),
      revokedCert: publicResponse(toSummary(result.oldCert)),
    });
  } catch (err) {
    logger.error('Issuer cert rotate failed', {
      error: err instanceof Error ? err.message : String(err),
    });
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to rotate issuer cert' },
    });
  }
});

// =============================================================================
// POST /api/issuer-certs/sign — KS-83 PR 3
// =============================================================================
// Sign a content hash with the tenant's active issuer cert. Produces the
// signature + public cert + algorithm metadata that callers can wrap into
// a `.sig.json` companion file (per KS-21 Q3: out-of-band sidecar, not
// embedded in the document).
//
// Originate's POST /api/documents/{id}/sign-cert calls this internally
// (forwarding the caller's Bearer token so this route's RBAC applies).
// Public-API-callable too — connectors can sign hashes directly.
//
// RBAC: ORG_ADMIN+ role OR `issuer-certs:sign` scope.
const signSchema = z
  .object({
    contentHash: z.string().min(1),
    // Optional: caller can target a specific cert by id (e.g. for replaying
    // an old signature). When omitted, we pick the most recently uploaded
    // active cert via findActiveIssuerCertForTenant.
    certId: z.string().uuid().optional(),
  })
  .strict();

issuerCertsRoutes.post('/sign', authenticate(), async (req: AuthenticatedRequest, res: Response) => {
  try {
    if (!isAuthorisedForCertSign(req)) {
      return res.status(403).json({
        success: false,
        error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit issuer-cert sign' },
      });
    }

    const tenantId = getReqTenantId(req);
    if (!tenantId) {
      return res.status(400).json({
        success: false,
        error: { code: 'TENANT_REQUIRED', message: 'Authenticated user has no tenantId claim' },
      });
    }

    const parsed = signSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: parsed.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('; '),
          details: parsed.error.issues,
        },
      });
    }

    // 1. Find the cert to sign with.
    let cert = parsed.data.certId
      ? await getIssuerCertById(parsed.data.certId, tenantId)
      : await findActiveIssuerCertForTenant(tenantId);

    if (!cert) {
      return res.status(404).json({
        success: false,
        error: {
          code: 'NO_ACTIVE_CERT',
          message:
            parsed.data.certId
              ? `Cert ${parsed.data.certId} not found in this tenant`
              : 'No active issuer cert found for this tenant. Upload one via POST /api/issuer-certs first.',
        },
      });
    }

    // 2. Refuse to sign with non-active certs. PR 2's background sweep
    //    flips expired certs automatically; revoked is operator-driven.
    //    Either way the route MUST refuse — historical sigs stay valid
    //    forever, but new sigs only come from an active cert.
    if (cert.status !== 'active') {
      return res.status(409).json({
        success: false,
        error: {
          code: 'CERT_NOT_ACTIVE',
          message: `Cannot sign with cert in status '${cert.status}'. Rotate or upload a new active cert.`,
        },
      });
    }

    // Belt-and-braces: validUntil < now should never happen on an active
    // cert (the sweep flips it to expired), but in the gap between sweeps
    // the row stays 'active' so this catches it.
    if (cert.validUntil.getTime() < Date.now()) {
      return res.status(409).json({
        success: false,
        error: {
          code: 'CERT_EXPIRED',
          message: `Cert validUntil (${cert.validUntil.toISOString()}) has passed. Awaiting next sweep tick to flip status=expired.`,
        },
      });
    }

    // 3. Sign.
    let envelope;
    try {
      envelope = signContentHashWithCert({
        encryptedPrivateKey: cert.encryptedPrivateKey,
        certId: cert.id,
        keyAlgorithm: cert.keyAlgorithm,
        contentHash: parsed.data.contentHash,
      });
    } catch (err) {
      if (err instanceof IssuerCertError) {
        return res.status(mapCertErrorStatus(err.code)).json({
          success: false,
          error: { code: err.code, message: err.message },
        });
      }
      throw err;
    }

    logger.info('Issuer cert signed content hash', {
      certId: cert.id,
      tenantId,
      fingerprint: cert.fingerprintSha256.slice(0, 16),
      contentHash: envelope.signedContentHash.slice(0, 32),
      algorithm: envelope.signatureAlgorithm,
      signedById: req.user!.userId,
    });

    return res.status(200).json({
      success: true,
      signature: envelope.signature,
      signatureAlgorithm: envelope.signatureAlgorithm,
      signedContentHash: envelope.signedContentHash,
      signedAt: envelope.signedAt,
      cert: {
        id: cert.id,
        fingerprintSha256: cert.fingerprintSha256,
        subject: cert.subject,
        issuer: cert.issuer,
        certPem: cert.certPem,
        validFrom: cert.validFrom.toISOString(),
        validUntil: cert.validUntil.toISOString(),
        trustLevel: cert.trustLevel,
      },
    });
  } catch (err) {
    logger.error('Issuer cert sign failed', {
      error: err instanceof Error ? err.message : String(err),
    });
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'Failed to sign content hash' },
    });
  }
});
