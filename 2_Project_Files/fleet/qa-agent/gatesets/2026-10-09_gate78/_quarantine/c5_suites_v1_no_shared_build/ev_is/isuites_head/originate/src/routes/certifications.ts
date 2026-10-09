/**
 * =============================================================================
 * CERTIFICATION ROUTES
 * =============================================================================
 * API endpoints for issuing, managing, and revoking certifications
 * Certifications are verifiable credentials anchored on the Cardano blockchain
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { body, param, query, validationResult } from 'express-validator';
import {
  extractOnBehalfOf,
  resolveOnBehalfOf,
  recordActionProvenance,
  OnBehalfOfError,
  type OnBehalfOf,
} from '../services/provenance';
import { v4 as uuidv4 } from 'uuid';
import crypto from 'crypto';
import {
  getCertification,
  saveCertification,
  listCertifications,
  saveShare,
  getSharesByCertification,
  getLineageEvents,
  initRepo,
  type Certification,
  type ShareRecord,
} from '../repositories/certificationRepo';
import { prisma } from '../db';
import {
  createChargeEvent,
  getChargeEventsByCertification,
} from '../services/chargeEvents';
import {
  notifyDocumentCertified,
  notifyDocumentRevoked,
  notifyDocumentShared,
} from '../utils/notificationClient';
import { logger } from '../utils/logger';
import { publishEvent, EventTypes } from '../events';
import { authenticate } from '../middleware/auth';
import { isAllowedByRoleOrScope } from '../middleware/rbac';
import { DOCUMENT_WRITE_ROLES } from '../middleware/documentWriteRoles';
import {
  saveDocument as saveLineageDocument,
  assertNoCycle,
  generateContentHash as generateDocumentContentHash,
  type DocumentRecord,
} from '../repositories/documentRepo';
import { extractPgCode } from '../utils/pgErrors';

export const certificationsRouter = Router();
// All routes here require an authenticated Bearer JWT. Audit A-09 + A-01:
// previously trusted client-supplied x-user-* headers via getUserFromRequest;
// the gateway now strips those (commit c796138f0) and this enforces real
// authentication as defense in depth.
certificationsRouter.use(authenticate());


// Initialize repository on module load
initRepo().catch((err) => logger.error('Failed to init repo', { error: err instanceof Error ? err.message : String(err) }));

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function generateContentHash(data: Record<string, unknown>): string {
  const sorted = JSON.stringify(data, Object.keys(data).sort());
  return crypto.createHash('sha256').update(sorted).digest('hex');
}

function getUserFromRequest(req: Request): { id: string; did?: string; name?: string } | null {
  // Pen-test F-04: read from authenticated req.user (set by authenticate()
  // middleware), NOT from raw headers. Direct header reads are spoofable
  // by anyone reaching the service directly.
  const user = (req as any).user;
  const userId = user?.userId;
  const userEmail = user?.email as string | undefined;

  if (!userId) return null;

  return {
    id: userId,
    did: user?.did,
    name: userEmail?.split('@')[0],
  };
}

/**
 * KS-22 (KS-4 phase 5b): every certification call must be tenant-scoped.
 * Mirrors getReqTenantId in routes/documents.ts — req.tenantId is the
 * effective tenant after extractTenantContext resolves any X-Tenant-Override.
 * In single-tenancy mode the middleware doesn't run; fall back to the same
 * default tenant id that extractTenantContext itself uses in non-prod, so
 * queries match the rows the migration backfilled there.
 */
const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';

function getReqTenantId(req: Request): string {
  const tid = (req as any).tenantId as string | undefined;
  return tid || DEFAULT_TENANT_ID;
}

// =============================================================================
// ROUTES
// =============================================================================

/**
 * POST /api/certifications/issue
 * Issue a new certification
 */
certificationsRouter.post(
  '/issue',
  [
    body('type')
      .isIn([
        'educational_degree',
        'employment_certificate',
        'professional_certification',
        'employment_reference',
        'identity_document',
        'certificate',
        'verification_certificate',
        // KS-66 (Kam, 2026-05-14): "Signed Document" — the SSD-side
        // recipient-attestation event ("sign"). `verification_certificate`
        // stays the issuer-side authoritative attestation ("certify").
        // Both produce new linked documents via KS-70's parent_document_id.
        'signed_document',
        'DOCUMENT',
      ])
      .withMessage('Invalid certification type. Allowed: educational_degree, employment_certificate, professional_certification, employment_reference, identity_document, certificate, verification_certificate, signed_document, DOCUMENT'),
    body('holderId').optional(),
    // KS-74: SSD-style flows can issue against an email when the holder
    // hasn't signed up yet. Mutually exclusive with holderId — the
    // handler returns 400 if both are set. When supplied, the email is
    // resolved (or an INVITED stub is created) via auth-service.
    body('holderEmail').optional().isEmail().withMessage('holderEmail must be a valid email'),
    body('data').isObject().withMessage('Data must be an object'),
    // KS-70: optional lifecycle parent. When set, certify creates a new
    // document linked to this one via parent_document_id and rejects
    // cycles in the proposed ancestor chain. Accepts the external-id
    // shape originate uses elsewhere (doc-<ts>-<random>) — the route
    // layer doesn't try to coerce to UUID.
    body('parentDocumentId').optional().isString().withMessage('parentDocumentId must be a string'),
    // KS-444: enforce the remaining published CertificationIssueRequest field
    // types. The sweep's negative_data_rejection sent `metadata: [null,null]`
    // (spec declares a JSON object) and it was accepted with a 201. isObject()
    // is strict by default — arrays and null are rejected.
    body('documentId').optional().isString().withMessage('documentId must be a string'),
    body('metadata').optional().isObject().withMessage('metadata must be an object'),
  ],
  async (req: Request, res: Response) => {
    try {
      // Check authentication first
      const issuer = getUserFromRequest(req);
      if (!issuer) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      // KS-547 (KS-540 F-2): certification issuance gates like every other
      // document-write verb — this was the one ungated write on the platform.
      // Human callers need a DOCUMENT_WRITE_ROLES role; `sk_*` connector
      // callers satisfy it via the `certifications:write` scope (KS-71 path),
      // so S's certify traffic is unaffected. Demo persona demo@secuura.io is
      // seeded ISSUER_ADMIN so the live demo certify flow keeps working.
      if (!isAllowedByRoleOrScope(req, DOCUMENT_WRITE_ROLES, 'certifications:write')) {
        return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Forbidden: your role does not permit issuing certifications' } });
      }

      // Then validate request body
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        // KS-39 #3: wrap express-validator output in the gateway's standard
        // envelope `{success, error: {code, message, details}}` so callers
        // can read `body.error.message` consistently. Previously we returned
        // raw `{errors: [...]}` which broke every consumer that doesn't
        // special-case it (including the e2e contract harness).
        const errArr = errors.array();
        const summary = errArr.map((e: { msg?: string }) => e.msg).filter(Boolean).join('; ');
        return res.status(400).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: summary || 'Invalid request body',
            details: errArr,
          },
        });
      }

      const { type, holderDid, data, expiresAt, privacySettings } = req.body;

      // KS-1213: with parentDocumentId, the derived document is stored as the certification type
      // (`type || 'verification_certificate'`) and the caller's `data` is spread into its `data`, while a
      // document is served as `data.documentType || type`. A `data.documentType` that differs from that
      // stored type would serve, and verify, the derived document as another type. Refused before any
      // write (the holder stub and the certification row come first); exact comparison, as KS-1202.
      const derivedDataDocumentType = data && typeof data === 'object' ? (data as Record<string, unknown>).documentType : undefined;
      if (req.body.parentDocumentId && derivedDataDocumentType !== undefined && derivedDataDocumentType !== (type || 'verification_certificate')) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'data.documentType must equal the certification type when parentDocumentId is set' } });
      }
      const holderEmail: string | undefined = req.body.holderEmail;

      // KS-74: holderId XOR holderEmail. Both = 400 (ambiguous which to use).
      if (req.body.holderId && holderEmail) {
        return res.status(400).json({
          success: false,
          error: {
            code: 'BAD_REQUEST',
            message: 'Supply either holderId or holderEmail, not both',
          },
        });
      }

      // Track whether the resolved holder was just-stubbed so the response
      // can tell SSD "you issued against a pending invite, status: INVITED".
      let holderStatus: 'ACTIVE' | 'INVITED' | string | undefined;
      let resolvedHolderEmail: string | undefined;

      // KS-74: when holderEmail is supplied, ask auth-service to either
      // resolve it to an existing user OR mint an INVITED stub. The stub
      // gets claimed on /api/auth/register later.
      //
      // KS-289: call auth-service DIRECTLY (server-to-server via
      // AUTH_SERVICE_URL), NOT via the public gateway. Two reasons the old
      // gateway route failed: (1) the gateway enforces CSRF on POST/PUT/etc.,
      // so a POST /api/users/stub through it is rejected with
      // CSRF_TOKEN_MISSING — a service call carries no browser CSRF token;
      // (2) GATEWAY_BASE_URL was unset, so it fell back to
      // http://localhost:6882, which inside the originate container is
      // originate itself → ECONNREFUSED → the reported 502 "Recipient lookup
      // service unavailable". auth's /stub self-gates on role/scope and reads
      // the tenant from the forwarded JWT, so the direct call is equivalent
      // for security and tenant-correct.
      let holderId: string;
      if (holderEmail) {
        const authHeader = (req.headers.authorization as string) || '';
        try {
          const authBase = process.env.AUTH_SERVICE_URL || 'http://localhost:6003';
          const stubRes = await fetch(`${authBase}/api/users/stub`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              ...(authHeader ? { Authorization: authHeader } : {}),
            },
            body: JSON.stringify({ email: holderEmail }),
            // KS-203: bound the upstream call so a hung users/stub can't keep
            // the request open until the gateway times out (empty-body 500).
            signal: AbortSignal.timeout(5000),
          });
          if (stubRes.status === 404) {
            // Cross-tenant block — the email is already a Platform K user
            // in another tenant. Auth-service deliberately returns 404 to
            // avoid cross-tenant disclosure. SSD treats this as "this
            // recipient cannot be issued to from this tenant".
            return res.status(404).json({
              success: false,
              error: {
                code: 'RECIPIENT_NOT_AVAILABLE',
                message:
                  'Email is not resolvable to a user in this tenant. ' +
                  'It may already belong to a different tenant.',
              },
            });
          }
          if (!stubRes.ok) {
            return res.status(502).json({
              success: false,
              error: { code: 'BAD_GATEWAY', message: 'Could not resolve recipient via users/stub' },
            });
          }
          const body = (await stubRes.json()) as {
            data?: { userId: string; status?: string; email?: string };
          };
          if (!body.data?.userId) {
            return res.status(502).json({
              success: false,
              error: { code: 'BAD_GATEWAY', message: 'users/stub returned no userId' },
            });
          }
          holderId = body.data.userId;
          holderStatus = body.data.status;
          resolvedHolderEmail = body.data.email;
        } catch (err: any) {
          // KS-203: a timeout/abort is a transient dependency failure (retryable
          // 503), distinct from a genuine bad-gateway response (502).
          const timedOut = err?.name === 'TimeoutError' || err?.name === 'AbortError';
          logger.warn('users/stub unreachable during certifications/issue', { error: err?.message, timedOut });
          return res.status(timedOut ? 503 : 502).json({
            success: false,
            error: timedOut
              ? { code: 'SERVICE_UNAVAILABLE', message: 'Recipient lookup timed out — please retry' }
              : { code: 'BAD_GATEWAY', message: 'Recipient lookup service unavailable' },
          });
        }
      } else {
        holderId = req.body.holderId || issuer.id; // Default to issuer's own ID
      }

      // Validate holderId references a real user if explicitly provided
      // (holderEmail flow skips this — auth-service already minted/resolved
      // a valid user id above).
      if (req.body.holderId) {
        // Quick format check before hitting DB
        const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
        if (!uuidRegex.test(holderId)) {
          return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid holderId — must be a valid UUID' } });
        }
        try {
          const db = (req as any).db || prisma;
          const holderCheck = await db.$queryRaw`SELECT id FROM users WHERE id = ${holderId}::uuid LIMIT 1`;
          if (!holderCheck || (Array.isArray(holderCheck) && holderCheck.length === 0)) {
            return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid holderId — user does not exist' } });
          }
        } catch (err: any) {
          const errMsg = err instanceof Error ? err.message : String(err);
          if (errMsg.includes('invalid input syntax') || errMsg.includes('uuid')) {
            return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid holderId — must be a valid UUID' } });
          }
          // For other DB errors (table missing, connection issues), log and return 400
          // rather than letting a bad holderId propagate to saveCertification
          logger.warn('holderId validation DB error — rejecting', { holderId, error: errMsg });
          return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid holderId — could not validate' } });
        }
      }

      const id = uuidv4();
      const now = new Date().toISOString();

      // KS-480 §6: connector attribution on the certify action. Validate +
      // resolve BEFORE any write (400 shape / 403 cross-org fail fast).
      // KS-1228: the row used to be recorded right here, "once the id exists",
      // which was still BEFORE the lineage 422, the production anchoring 503 and
      // the save-time 400/503s below — so a refused issue left a row for a
      // certification that was never issued. It is now recorded only once
      // saveCertification succeeds. Reserved key never rides in the
      // certification data blob (it is content-hashed below).
      let certObo: OnBehalfOf | null = null;
      let certOboResolved: string | null = null;
      try {
        certObo = extractOnBehalfOf(req);
        if (certObo) {
          certOboResolved = await resolveOnBehalfOf(certObo, (req as any).user?.organizationId as string | undefined);
        }
      } catch (oboErr) {
        if (oboErr instanceof OnBehalfOfError) {
          return res.status(oboErr.status).json({ success: false, error: { code: oboErr.code, message: oboErr.message } });
        }
        throw oboErr;
      }
      if (data && typeof data === 'object') {
        delete (data as Record<string, unknown>).onBehalfOf;
        // KS-543 (Stuart's KS-537 finding #3): the data blob is content-hashed
        // below, so any PII a caller puts in it becomes STRUCTURALLY
        // UNERASABLE — it can never be encrypted or pseudonymised post-hoc
        // without invalidating the certification's own hash. Boundary hygiene
        // is the only durable fix (the onBehalfOf delete above is the
        // precedent): strip the known identity keys BEFORE hashing so no
        // caller can hash them into permanence. S already dropped
        // data.actorName on their side (PS-472) — this enforces it
        // structurally instead of trusting each caller. Strip, not reject —
        // a 400 here would widen platform-wide 4xx behaviour (KS-472 rule:
        // bound the positive generator first).
        for (const identityKey of ['actorName', 'actorEmail']) {
          delete (data as Record<string, unknown>)[identityKey];
        }
      }

      const contentHash = generateContentHash(data);

      // KS-70: optional lifecycle parent. Walk the proposed parent's
      // ancestor chain to reject cycles BEFORE we anchor or write — the
      // anchoring call is expensive and an invalid lineage shouldn't be
      // visible on-chain. The walker is capped at MAX_LINEAGE_DEPTH; if
      // it would exceed the cap we still proceed (the chain is just deep,
      // not cyclic) but the verify endpoint will return truncated=true.
      const parentDocumentId: string | undefined = req.body.parentDocumentId;
      const lifecycleTenantId = getReqTenantId(req);
      if (parentDocumentId) {
        try {
          await assertNoCycle(id, parentDocumentId, lifecycleTenantId, {
            db: (req as any).db,
          });
        } catch (err: any) {
          if (err?.code === 'LINEAGE_CYCLE') {
            return res.status(422).json({
              success: false,
              error: {
                code: 'LINEAGE_CYCLE',
                message: `Refusing to certify: ${parentDocumentId} would form a cycle in the document lineage`,
              },
            });
          }
          throw err;
        }
      }

      // Pen-test F-03 LIVE: forward to services/anchoring which calls
      // Blockfrost. Returns 202 immediately with the upstream anchor id;
      // txHash + blockHeight populate once Cardano confirms (~20–60s).
      // Verifier endpoint reads the latest from anchoring on each verify
      // — so a successful response here does NOT imply on-chain confirmation,
      // only that the request was accepted by the anchoring service.
      const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
      const certUserToken = (req.headers.authorization as string) || '';
      let upstreamAnchorId: string | null = null;
      let anchoringStatus: 'submitted' | 'failed' = 'failed';
      try {
        const upstream = await fetch(`${anchoringBase}/api/anchors`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(certUserToken ? { Authorization: certUserToken } : {}),
          },
          body: JSON.stringify({
            documentId: id,
            certId: id,
            contentHash,
            network: process.env.CARDANO_NETWORK || 'preprod',
            issuerOrgId: issuer.id,
            issuerName: issuer.name,
          }),
          // KS-203: bound the anchoring call. On timeout the catch below logs +
          // leaves anchoringStatus='failed' (graceful; prod 503s, non-prod continues).
          signal: AbortSignal.timeout(10000),
        });
        if (upstream.ok) {
          const j = await upstream.json() as any;
          upstreamAnchorId = j?.data?.id || null;
          anchoringStatus = 'submitted';
          logger.info('Certification queued for anchoring', { certId: id, upstreamAnchorId });
        }
      } catch (err: any) {
        logger.warn('Anchoring service unreachable for certification', { certId: id, error: err?.message });
      }
      if (anchoringStatus === 'failed' && process.env.NODE_ENV === 'production') {
        return res.status(503).json({
          success: false,
          error: { code: 'SERVICE_UNAVAILABLE', message: 'Blockchain anchoring service is temporarily unavailable. Please try again later.', confidence: 'unavailable' },
        });
      }

      const certification: Certification = {
        id,
        type,
        status: 'issued',
        issuer,
        holder: {
          id: holderId,
          did: holderDid,
        },
        data,
        privacySettings,
        issuedAt: now,
        expiresAt,
        contentHash,
        createdAt: now,
        updatedAt: now,
        blockchain: {
          // Upstream anchor id (correlation), NOT a Cardano txHash.
          // The verifier endpoint reads the live txHash from the
          // anchoring service via /api/anchors/document/:documentId
          // once Cardano confirms.
          anchorId: upstreamAnchorId,
          txHash: null as any,
          blockHeight: null as any,
          anchoredAt: null as any,
          confidence: 'pending-onchain',
          anchoringStatus,
          // KS-1124 F4 (Kam ruled b, 2026-09-28): an issue whose anchoring failed saves status 'failed', which the
          // gateway maps to off-chain-only; a statusless 'pending-onchain' blob would show as pending forever.
          ...(anchoringStatus === 'failed' ? { status: 'failed' } : {}),
        } as any,
      };

      // KS-70: reuse lifecycleTenantId captured above so the cycle-check
      // and the cert persistence run against the same tenant. The alias
      // keeps the original variable name readable in the existing block.
      const tenantId = lifecycleTenantId;
      await saveCertification(certification, tenantId, (req as any).db);
      // KS-1228: the certification exists now, so its attribution row is recorded
      // here, after every refusal above (see the validation comment for why).
      if (certObo) {
        recordActionProvenance({
          documentId: id,
          action: 'certify',
          tenantId: getReqTenantId(req),
          organizationId: (req as any).user?.organizationId as string | undefined,
          connectorId: (req as any).user?.userId as string | undefined,
          obo: certObo,
          resolvedUserId: certOboResolved,
        }).catch((provErr: Error) => logger.warn('provenance record failed', { documentId: id, action: 'certify', error: provErr.message }));
      }

      // KS-70: when a parentDocumentId is supplied, create a NEW document
      // representing the post-certify state. The new document carries:
      //   - the cert's contentHash (new bytes, new hash),
      //   - parent_document_id pointing at the predecessor,
      //   - status='signed' (the chain anchor lands on this row, not the parent).
      // The parent doc is left UNTOUCHED — its history is preserved. This
      // is the divergence point between the lifecycle-event model and the
      // legacy "update the original to certified" path (the latter still
      // runs for callers who supply documentId without parentDocumentId).
      let derivedDocumentExternalId: string | undefined;
      if (parentDocumentId) {
        const derivedExternalId = `doc-${Date.now()}-${id.slice(0, 8)}`;
        const derivedDoc: DocumentRecord = {
          id: derivedExternalId,
          type: type || 'verification_certificate',
          status: 'signed',
          owner: { id: issuer.id },
          parentDocumentId,
          data: {
            title:
              (data?.title as string) ||
              `Certification ${type}`,
            certificationId: id,
            certifiedAt: now,
            parentDocumentId,
            ...data,
          },
          contentHash:
            (data as Record<string, unknown> | undefined)?.contentHash as string
            || generateDocumentContentHash(data || {})
            || contentHash,
          signatures: [],
          blockchain: certification.blockchain as DocumentRecord['blockchain'],
          createdAt: now,
          updatedAt: now,
        };
        try {
          await saveLineageDocument(derivedDoc, tenantId, (req as any).db);
          derivedDocumentExternalId = derivedExternalId;
        } catch (saveErr: any) {
          logger.error('KS-70: failed to write derived document for cert lineage', {
            certId: id,
            parentDocumentId,
            error: saveErr instanceof Error ? saveErr.message : String(saveErr),
          });
          // Fall through — the certification row already landed; the
          // derived doc can be back-filled later. We don't 500 the cert.
        }
      }

      // Update the original document's status + certification metadata.
      // KS-70: legacy path — only fires when the caller is in the
      // pre-lineage model (documentId set, parentDocumentId absent).
      if (req.body.documentId && !parentDocumentId) {
        const certDb = (req as any).db || prisma;
        const certMetaUpdate = JSON.stringify({
          issuerName: req.body.data?.issuedBy || issuer.name || undefined,
          issuerId: issuer.id,
          certificationId: id,
          certificationType: type,
          certifiedAt: new Date().toISOString(),
          certificationData: req.body.data || {},
          blockchain: certification.blockchain,
        });
        try {
          await certDb.$executeRaw`
            UPDATE documents SET
              status = 'certified',
              certified_at = NOW(),
              certification_metadata = ${certMetaUpdate}::jsonb,
              updated_at = NOW()
            WHERE external_id = ${req.body.documentId}
              AND tenant_id = ${tenantId}::uuid
              AND status IN ('draft', 'pending_signature', 'anchored', 'signed')
          `;
        } catch { /* best-effort */ }
      }

      // Publish certification.issued event (fire-and-forget)
      publishEvent(EventTypes.CERTIFICATION_ISSUED, {
        certificationId: id,
        type,
        holderId,
        issuerId: issuer.id,
        contentHash,
      }).catch(() => {});

      // Create charge events for certification signing + blockchain anchoring.
      // KS-216: metering is a billing side-effect — a failed charge write must
      // NOT 500 a certification that has already landed + been queued for
      // anchoring (the cert row + anchor exist by this point). Mirror the KS-70
      // lineage-write pattern above: log and fall through. Charge events can be
      // reconciled later; a 500 here makes clients retry and double-issue.
      let signCharge: Awaited<ReturnType<typeof createChargeEvent>> | null = null;
      let anchorCharge: Awaited<ReturnType<typeof createChargeEvent>> | null = null;
      try {
        signCharge = await createChargeEvent('certification_sign', id, issuer.id, tenantId, {
          metadata: { certificationType: type, holderId },
        });
        anchorCharge = await createChargeEvent('blockchain_anchor', id, issuer.id, tenantId, {
          metadata: { txHash: certification.blockchain?.txHash },
        });
      } catch (chargeErr: any) {
        logger.error('KS-216: failed to persist charge event(s) — continuing, certification already issued', {
          certId: id,
          tenantId,
          error: chargeErr instanceof Error ? chargeErr.message : String(chargeErr),
        });
      }

      // Fire lifecycle notification (non-blocking)
      // Pen-test F-04: fall back to authenticated req.user.email, NOT raw headers.
      // KS-74: also use resolvedHolderEmail from the stub flow when present.
      const notifyToEmail = resolvedHolderEmail || holderEmail || (req as any).user?.email;
      if (notifyToEmail) {
        // KS-203: fire-and-forget — an intermittent notification failure must
        // not surface as an unhandled rejection (matches publishEvent above).
        notifyDocumentCertified({
          toEmail: notifyToEmail as string,
          recipientName: req.body.holderName,
          documentTitle: (data.title as string) || (data.name as string) || type,
          certifierName: issuer.name || issuer.id,
          certificationId: id,
          certifiedAt: now,
        }).catch((err: any) =>
          logger.warn('certification notification failed', { certId: id, error: err?.message }),
        );
      }

      res.status(201).json({
        id: certification.id,
        type: certification.type,
        holderId: certification.holder.id,
        status: certification.status,
        data: certification.data,
        expiresAt: certification.expiresAt,
        issuedAt: certification.issuedAt,
        blockchainAnchor: certification.blockchain,
        chargeEvents: [signCharge?.id, anchorCharge?.id].filter(Boolean),
        // KS-70: when parentDocumentId was provided, the cert produced a
        // new document representing the post-certify state. Surface its
        // external id so callers can poll its anchor or feed it into the
        // next lifecycle event (e.g. sign-after-certify chains).
        ...(derivedDocumentExternalId
          ? { derivedDocumentId: derivedDocumentExternalId, parentDocumentId }
          : {}),
        // KS-74: when the holder was resolved via holderEmail, surface the
        // holder status. `INVITED` tells SSD it issued against a stub —
        // the recipient still needs to register. `ACTIVE` (or any other)
        // means an existing user.
        ...(holderEmail
          ? {
              holder: {
                id: certification.holder.id,
                status: holderStatus ?? 'UNKNOWN',
                email: resolvedHolderEmail ?? holderEmail,
              },
            }
          : {}),
      });
    } catch (error: any) {
      const msg = error instanceof Error ? error.message : String(error);
      // KS-203: log name + code + stack so the next concurrent-load failure is
      // diagnosable (the previous blanket 500 logged only the message).
      logger.error('Failed to issue certification', {
        error: msg,
        name: error?.name,
        code: error?.code,
        stack: error instanceof Error ? error.stack : undefined,
      });

      // Detect FK constraint violations and return helpful 400
      if (msg.includes('foreign key constraint') || msg.includes('violates foreign key')) {
        if (msg.includes('owner_user_id')) {
          return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid holderId — user does not exist' } });
        }
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid reference — a referenced record does not exist', detail: msg } });
      }

      // KS-203: transient dependency failures under concurrent load (DB pool
      // exhaustion, connection resets, upstream timeouts) are not internal bugs
      // — return a retryable 503 instead of a blanket 500 so callers/harnesses
      // back off and retry. Detected via Prisma's pool-timeout code (P2024),
      // pg connection-acquire timeouts, and Node socket/abort error codes.
      const code = error?.code as string | undefined;
      const isTransientDependency =
        code === 'P2024' ||                                   // Prisma: client connection-pool timeout
        code === '53300' || code === '53400' ||               // pg: too_many_connections / configuration_limit_exceeded
        code === '57P03' ||                                   // pg: cannot_connect_now (server starting/recovering)
        code === 'ECONNREFUSED' || code === 'ECONNRESET' ||   // socket dropped
        code === 'ETIMEDOUT' || code === 'EAI_AGAIN' ||       // network timeout / DNS
        error?.name === 'TimeoutError' || error?.name === 'AbortError' ||
        msg.includes('Timed out fetching a new connection from the connection pool') ||
        msg.includes('timeout exceeded when trying to connect') ||
        msg.includes('remaining connection slots are reserved') ||  // pg 53300, observed under load (KS-203)
        msg.includes('too many clients already') ||
        msg.includes('Connection terminated');
      if (isTransientDependency) {
        return res.status(503).json({
          success: false,
          error: { code: 'SERVICE_UNAVAILABLE', message: 'Certification service is temporarily overloaded — please retry', confidence: 'unavailable' },
        });
      }

      // KS-445: the spec's free-form `data`/metadata objects permit values
      // Postgres can't store (a \u0000 inside a jsonb string → 22P05, invalid
      // byte sequences → 22021, oversized varchar → 22001, bad casts → 22P02).
      // Unstorable input is the client's malformed payload, not a server fault.
      const pgCode = extractPgCode(error);
      if (pgCode && ['22P02', '22001', '22007', '22008', '22021', '22P05', '23502', '23514', '42804'].includes(pgCode)) {
        return res.status(400).json({
          success: false,
          error: { code: 'BAD_REQUEST', message: 'Certification payload contains values that cannot be stored' },
        });
      }

      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to issue certification' } });
    }
  }
);

/**
 * GET /api/certifications
 * List certifications with optional filtering
 */
certificationsRouter.get(
  '/',
  [
    query('type').optional().isString(),
    query('status').optional().isIn(['issued', 'pending', 'revoked', 'expired']),
    query('holderId').optional().isString(),
    query('issuerId').optional().isString(),
    query('limit').optional().isInt({ min: 1, max: 100 }),
    query('offset').optional().isInt({ min: 0 }),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { type, status, holderId, issuerId, limit = '20', offset = '0' } = req.query;
      const limitNum = parseInt(limit as string, 10);
      const offsetNum = parseInt(offset as string, 10);

      // Scope by authenticated user unless admin
      // Pen-test F-04: read from authenticated req.user (set by authenticate()
      // middleware), NOT from raw headers.
      const user = (req as any).user;
      const userId = user?.userId as string | undefined;
      const userRole = user?.role as string | undefined;
      const isAdmin = userRole === 'system_admin' || userRole === 'SYSTEM_ADMIN' || userRole === 'super_admin';

      const effectiveHolderId = isAdmin ? (holderId as string) : (userId || holderId as string);

      const { items: results } = await listCertifications(getReqTenantId(req), {
        issuerId: issuerId as string,
        holderId: effectiveHolderId,
        status: status as string,
        type: type as string,
        page: Math.floor(offsetNum / limitNum) + 1,
        limit: limitNum,
      });

      // Additional in-memory filtering for non-admin users
      let paginated = results;
      if (userId && !isAdmin) {
        paginated = results.filter(c =>
          c.holder?.id === userId || c.issuer?.id === userId
        );
      }

      res.json({
        certifications: paginated.map(c => ({
          id: c.id,
          type: c.type,
          status: c.status,
          holder: c.holder,
          issuer: c.issuer,
          issuedAt: c.issuedAt,
          expiresAt: c.expiresAt,
          revokedAt: c.revokedAt,
        })),
        pagination: {
          total: paginated.length,
          limit: limitNum,
          offset: offsetNum,
          hasMore: offsetNum + limitNum < paginated.length,
        },
      });
    } catch (error) {
      logger.error('Failed to list certifications', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list certifications' } });
    }
  }
);

/**
 * GET /api/certifications/:id
 * Get certification details by ID
 */
certificationsRouter.get(
  '/:id',
  [param('id').notEmpty().withMessage('Certification ID is required')],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { id } = req.params;
      const tenantId = getReqTenantId(req);
      const certification = await getCertification(id, tenantId);

      if (!certification) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Certification not found' } });
      }

      // Check if expired
      if (certification.expiresAt && new Date(certification.expiresAt) < new Date()) {
        certification.status = 'expired';
        await saveCertification(certification, tenantId, (req as any).db);
      }

      res.json({
        id: certification.id,
        type: certification.type,
        status: certification.status,
        issuer: certification.issuer,
        holder: certification.holder,
        data: certification.data,
        privacySettings: certification.privacySettings,
        issuedAt: certification.issuedAt,
        expiresAt: certification.expiresAt,
        revokedAt: certification.revokedAt,
        revocationReason: certification.revocationReason,
        blockchain: certification.blockchain,
        contentHash: certification.contentHash,
      });
    } catch (error) {
      // KS-210: a non-uuid :id (e.g. a coverage method-probe like "issue")
      // makes the `id::uuid` cast in getCertification throw pg 22P02
      // (invalid_text_representation) before the not-found check — treat it as
      // 404 (no such certification), not a 500 (KS-111 "500-on-bad-input" class).
      // KS-255: originate queries run through Prisma, which wraps the pg error
      // (code P2010, pg code only in meta/message) — so also match the wrapped
      // shape, not just the bare `code` the pg driver would set.
      const pgCode = (error as { code?: string })?.code ?? (error as { meta?: { code?: string } })?.meta?.code;
      if (pgCode === '22P02' || (error instanceof Error && error.message.includes('22P02'))) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Certification not found' } });
      }
      logger.error('Failed to get certification', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get certification' } });
    }
  }
);

/**
 * POST /api/certifications/:id/revoke
 * Revoke a certification
 */
certificationsRouter.post(
  '/:id/revoke',
  [
    param('id').notEmpty().withMessage('Certification ID is required'),
    body('reason').optional().isString().withMessage('Reason must be a string'),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const issuer = getUserFromRequest(req);
      if (!issuer) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { id } = req.params;
      const { reason } = req.body;
      const tenantId = getReqTenantId(req);

      const certification = await getCertification(id, tenantId);

      if (!certification) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Certification not found' } });
      }

      // Verify issuer has permission to revoke
      if (certification.issuer.id !== issuer.id) {
        return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Only the issuer can revoke this certification' } });
      }

      if (certification.status === 'revoked') {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Certification is already revoked' } });
      }

      const now = new Date().toISOString();
      certification.status = 'revoked';
      certification.revokedAt = now;
      certification.revocationReason = reason;
      certification.updatedAt = now;

      await saveCertification(certification, tenantId, (req as any).db);

      // Fire lifecycle notification (non-blocking)
      // Pen-test F-04: read from authenticated req.user, NOT raw headers.
      const holderEmail = (req as any).user?.email as string | undefined;
      if (holderEmail) {
        notifyDocumentRevoked({
          toEmail: holderEmail,
          documentTitle: (certification.data?.title as string) || (certification.data?.name as string) || certification.type,
          revokedBy: issuer.name || issuer.id,
          reason,
          revokedAt: now,
        });
      }

      res.json({
        id: certification.id,
        status: certification.status,
        revokedAt: certification.revokedAt,
        revocationReason: certification.revocationReason,
      });
    } catch (error) {
      logger.error('Failed to revoke certification', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to revoke certification' } });
    }
  }
);

/**
 * POST /api/certifications/:id/verify
 * Verify a certification's authenticity
 */
certificationsRouter.post(
  '/:id/verify',
  [param('id').notEmpty().withMessage('Certification ID is required')],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { id } = req.params;
      const certification = await getCertification(id, getReqTenantId(req));

      if (!certification) {
        return res.status(404).json({
          verified: false,
          error: 'Certification not found',
        });
      }

      // Check status
      const isValid = certification.status === 'issued';
      const isExpired = certification.expiresAt && new Date(certification.expiresAt) < new Date();
      const isRevoked = certification.status === 'revoked';

      // Verify content hash
      const currentHash = generateContentHash(certification.data);
      const hashValid = currentHash === certification.contentHash;

      // Create charge event for verification
      const verifier = getUserFromRequest(req);
      const verifyCharge = await createChargeEvent('verification', id, verifier?.id || 'anonymous', getReqTenantId(req), {
        metadata: { verified: isValid && !isExpired && hashValid },
      });

      res.json({
        verified: isValid && !isExpired && hashValid,
        certificationId: certification.id,
        status: certification.status,
        checks: {
          exists: true,
          notRevoked: !isRevoked,
          notExpired: !isExpired,
          hashValid,
          blockchainAnchored: !!certification.blockchain,
        },
        issuer: {
          id: certification.issuer.id,
          did: certification.issuer.did,
          verified: true,
        },
        blockchain: certification.blockchain,
        verifiedAt: new Date().toISOString(),
        chargeEventId: verifyCharge.id,
      });
    } catch (error) {
      logger.error('Failed to verify certification', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to verify certification' } });
    }
  }
);

// =============================================================================
// SHARE ENDPOINT (Phase 3 — Batch Sharing)
// =============================================================================

/**
 * POST /api/certifications/:id/share
 * Share a certification with one or more recipients (batch)
 */
certificationsRouter.post(
  '/:id/share',
  [
    param('id').notEmpty().withMessage('Certification ID is required'),
    body('recipients').isArray({ min: 1 }).withMessage('At least one recipient is required'),
    body('recipients.*.email').isEmail().withMessage('Valid email is required for each recipient'),
    body('recipients.*.shareType')
      .isIn(['view', 'verify', 'reshare'])
      .withMessage('Share type must be view, verify, or reshare'),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { id } = req.params;
      const certification = await getCertification(id, getReqTenantId(req));

      if (!certification) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Certification not found' } });
      }

      if (certification.status === 'revoked') {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Cannot share a revoked certification' } });
      }

      const { recipients } = req.body;
      const now = new Date().toISOString();
      const created: ShareRecord[] = [];

      for (const recipient of recipients) {
        const shareId = uuidv4();
        const record: ShareRecord = {
          id: shareId,
          certificationId: id,
          toEmail: recipient.email,
          toName: recipient.name || undefined,
          shareType: recipient.shareType,
          sharedBy: user.id,
          timestamp: now,
          status: 'active',
        };

        await saveShare(record);
        created.push(record);

        // Fire lifecycle notification (non-blocking)
        notifyDocumentShared({
          toEmail: recipient.email,
          recipientName: recipient.name,
          documentTitle: (certification.data?.title as string) || (certification.data?.name as string) || certification.type,
          sharedByName: user.name || user.id,
          shareType: recipient.shareType,
        });

        logger.info('Certification shared', { certificationId: id, recipientEmail: recipient.email, shareType: recipient.shareType });
      }

      // Create charge event for sharing (currently free, tracked for audit)
      const shareCharge = await createChargeEvent('share', id, user.id, getReqTenantId(req), {
        feeStatus: 'free',
        metadata: { recipientCount: created.length, recipients: recipients.map((r: any) => r.email) },
      });

      res.status(201).json({
        certificationId: id,
        sharesCreated: created.length,
        shares: created.map((s) => ({
          id: s.id,
          toEmail: s.toEmail,
          toName: s.toName,
          shareType: s.shareType,
          status: s.status,
          timestamp: s.timestamp,
        })),
        chargeEventId: shareCharge.id,
      });
    } catch (error) {
      logger.error('Failed to share certification', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to share certification' } });
    }
  }
);

// =============================================================================
// RECERTIFY ENDPOINT (Phase 2 — Verifier → Certifier)
// =============================================================================

/**
 * POST /api/certifications/:id/recertify
 * Issue a verification certificate — a secondary credential that wraps the
 * original, attesting that a Verifier has verified it.
 * The Verifier transitions to Certifier role for this lineage.
 */
certificationsRouter.post(
  '/:id/recertify',
  [
    param('id').notEmpty().withMessage('Certification ID is required'),
    body('note').optional().isString(),
  ],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { id } = req.params;
      const { note } = req.body;
      const tenantId = getReqTenantId(req);

      const originalCert = await getCertification(id, tenantId);

      if (!originalCert) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Original certification not found' } });
      }

      if (originalCert.status === 'revoked') {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Cannot re-certify a revoked certification' } });
      }

      const now = new Date().toISOString();
      const newCertId = uuidv4();
      const verificationContentHash = generateContentHash({
        originalCertificationId: id,
        verifierId: user.id,
        verifiedAt: now,
      });

      // Pen-test F-03 LIVE: queue with anchoring service.
      const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
      const verifyCertUserToken = (req.headers.authorization as string) || '';
      let upstreamAnchorId: string | null = null;
      let anchoringStatus: 'submitted' | 'failed' = 'failed';
      try {
        const upstream = await fetch(`${anchoringBase}/api/anchors`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(verifyCertUserToken ? { Authorization: verifyCertUserToken } : {}),
          },
          body: JSON.stringify({
            documentId: newCertId,
            certId: newCertId,
            contentHash: verificationContentHash,
            network: process.env.CARDANO_NETWORK || 'preprod',
          }),
        });
        if (upstream.ok) {
          const j = await upstream.json() as any;
          upstreamAnchorId = j?.data?.id || null;
          anchoringStatus = 'submitted';
        }
      } catch (err: any) {
        logger.warn('Anchoring service unreachable for verification cert', { error: err?.message });
      }
      if (anchoringStatus === 'failed' && process.env.NODE_ENV === 'production') {
        return res.status(503).json({
          success: false,
          error: { code: 'SERVICE_UNAVAILABLE', message: 'Blockchain anchoring service is temporarily unavailable. Please try again later.', confidence: 'unavailable' },
        });
      }

      // Create the verification certificate
      const verificationCert: Certification = {
        id: newCertId,
        type: 'verification_certificate',
        status: 'issued',
        issuer: {
          id: user.id,
          did: user.did,
          name: user.name,
        },
        holder: originalCert.holder,
        data: {
          originalCertificationId: id,
          originalType: originalCert.type,
          originalIssuer: originalCert.issuer,
          verifierNote: note || null,
          verifiedAt: now,
          roleTransition: { from: 'verifier', to: 'certifier' },
        },
        issuedAt: now,
        contentHash: verificationContentHash,
        createdAt: now,
        updatedAt: now,
        blockchain: {
          anchorId: upstreamAnchorId,
          txHash: null as any,
          blockHeight: null as any,
          anchoredAt: null as any,
          confidence: 'pending-onchain',
          anchoringStatus,
          // KS-1124 F4 (Kam ruled b, 2026-09-28): a recertify whose anchoring failed saves status 'failed', the same
          // rule as the issue route: the gateway maps it to off-chain-only instead of pending forever.
          ...(anchoringStatus === 'failed' ? { status: 'failed' } : {}),
        } as any,
      };

      await saveCertification(verificationCert, tenantId, (req as any).db);

      // Create charge event for verification certificate (free_in_context for recruitment)
      const recertCharge = await createChargeEvent('verification_certificate', id, user.id, tenantId, {
        feeStatus: 'free_in_context',
        metadata: {
          verificationCertificateId: newCertId,
          roleTransition: { from: 'verifier', to: 'certifier' },
          parentCertificationId: id,
        },
      });

      logger.info('Verification certificate issued', { verificationCertId: newCertId, originalCertId: id, userId: user.id });

      res.status(201).json({
        certificationId: newCertId,
        type: 'verification_certificate',
        parentCertificationId: id,
        status: 'issued',
        issuer: verificationCert.issuer,
        roleTransition: { from: 'verifier', to: 'certifier' },
        blockchain: verificationCert.blockchain,
        issuedAt: now,
        chargeEventId: recertCharge.id,
      });
    } catch (error) {
      logger.error('Failed to issue verification certificate', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to issue verification certificate' } });
    }
  }
);

// =============================================================================
// LINEAGE ENDPOINT (Phase 1 — Lineage Data)
// =============================================================================

/**
 * GET /api/certifications/:id/lineage
 * Get the full lineage data for a certification, including all shares,
 * verification certificates, and delegation chains.
 */
certificationsRouter.get(
  '/:id/lineage',
  [param('id').notEmpty().withMessage('Certification ID is required')],
  async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const certification = await getCertification(id, getReqTenantId(req));

      if (!certification) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Certification not found' } });
      }

      // Collect all related shares from database
      const shares = await getSharesByCertification(id);

      // Collect lineage events from provenance chain
      const events = await getLineageEvents(id);

      // Verification certificates are certifications with type='verification_certificate'
      // referencing this original via data.originalCertificationId
      const verificationCerts = events
        .filter((e: any) => e.eventType === 'RECERTIFY')
        .map((e: any) => ({
          id: e.id,
          issuer: (e.eventData as any)?.issuer || { id: e.actorId },
          issuedAt: e.occurredAt?.toISOString?.() || e.occurredAt,
          roleTransition: (e.eventData as any)?.roleTransition,
        }));

      // Gather charge events for this certification
      const chargeEvents = await getChargeEventsByCertification(id, getReqTenantId(req));

      res.json({
        certificationId: id,
        originalCertification: {
          id: certification.id,
          type: certification.type,
          status: certification.status,
          issuer: certification.issuer,
          holder: certification.holder,
          issuedAt: certification.issuedAt,
          blockchain: certification.blockchain,
        },
        shares: shares.map((s) => ({
          id: s.id,
          toEmail: s.toEmail,
          toName: s.toName,
          shareType: s.shareType,
          status: s.status,
          timestamp: s.timestamp,
        })),
        verificationCertificates: verificationCerts,
        totalShares: shares.length,
        totalVerificationCerts: verificationCerts.length,
        chargeEvents: chargeEvents.map((ce) => ({
          id: ce.id,
          eventType: ce.eventType,
          amount: ce.amount,
          currency: ce.currency,
          feeStatus: ce.feeStatus,
          typicalPayer: ce.typicalPayer,
          status: ce.status,
          createdAt: ce.createdAt,
          metadata: ce.metadata,
        })),
      });
    } catch (error) {
      logger.error('Failed to get lineage', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get lineage data' } });
    }
  }
);

// =============================================================================
// EVIDENCE BUNDLE ENDPOINT (Phase 7)
// =============================================================================

/**
 * GET /api/certifications/:id/evidence-bundle
 * Assemble and return a complete evidence bundle for a certification.
 */
certificationsRouter.get(
  '/:id/evidence-bundle',
  [param('id').notEmpty().withMessage('Certification ID is required')],
  async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const certification = await getCertification(id, getReqTenantId(req));

      if (!certification) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Certification not found' } });
      }

      const tenantId = getReqTenantId(req);
      const shares = await getSharesByCertification(id);
      const events = await getLineageEvents(id);
      const chargeEvents = await getChargeEventsByCertification(id, tenantId);

      // Create charge event for evidence export
      const exporter = getUserFromRequest(req);
      const exportCharge = await createChargeEvent('evidence_export', id, exporter?.id || 'anonymous', tenantId);

      const bundle = {
        bundleVersion: '1.0.0',
        generatedAt: new Date().toISOString(),
        certification: {
          id: certification.id,
          type: certification.type,
          status: certification.status,
          issuer: certification.issuer,
          holder: certification.holder,
          contentHash: certification.contentHash,
          issuedAt: certification.issuedAt,
          expiresAt: certification.expiresAt,
          revokedAt: certification.revokedAt,
          revocationReason: certification.revocationReason,
          blockchain: certification.blockchain,
        },
        provenanceChain: [
          {
            action: 'created',
            actor: certification.issuer.id,
            timestamp: certification.createdAt,
            details: { type: certification.type },
          },
          {
            action: 'issued',
            actor: certification.issuer.id,
            timestamp: certification.issuedAt,
            txHash: certification.blockchain?.txHash,
          },
          ...shares.map((s) => ({
            action: 'shared',
            actor: s.sharedBy,
            recipient: s.toEmail,
            timestamp: s.timestamp,
            shareType: s.shareType,
          })),
          ...events
            .filter((e: any) => e.eventType === 'RECERTIFY')
            .map((e: any) => ({
              action: 'recertified',
              actor: e.actorId,
              timestamp: e.occurredAt?.toISOString?.() || e.occurredAt,
              verificationCertificateId: e.id,
            })),
        ],
        shares: shares.length,
        verificationCertificates: events.filter((e: any) => e.eventType === 'RECERTIFY').length,
        chargeEvents: [...chargeEvents, exportCharge].map((ce) => ({
          id: ce.id,
          eventType: ce.eventType,
          amount: ce.amount,
          currency: ce.currency,
          feeStatus: ce.feeStatus,
          typicalPayer: ce.typicalPayer,
          status: ce.status,
          createdAt: ce.createdAt,
        })),
        exportChargeEventId: exportCharge.id,
      };

      res.setHeader('Content-Type', 'application/json');
      res.setHeader(
        'Content-Disposition',
        `attachment; filename="evidence-bundle-${id}.json"`
      );
      res.json(bundle);
    } catch (error) {
      logger.error('Failed to generate evidence bundle', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to generate evidence bundle' } });
    }
  }
);

export default certificationsRouter;
