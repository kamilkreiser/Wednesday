/**
 * =============================================================================
 * VERIFICATION ROUTES
 * =============================================================================
 * Extracted from the API gateway monolith. Contains:
 * - Document/certification verification endpoints
 * - Workflow instance management (approve/reject/query)
 * - Document creation with enforcement pipeline
 * - Document fetch interceptor (pending/rejected state)
 * - Workflow approval blockers for sign/anchor/share
 * - Notifications endpoint
 * - Governance fallback endpoints
 * - Public document types endpoint
 * =============================================================================
 */

import { Router, Request, Response, NextFunction, RequestHandler } from 'express';
import * as redisService from '../services/redis';
import { readPlatformSettings } from '../services/settingsStore';
import { rejectControlBytes } from '@secuura/shared';
import { DEFAULT_DOCUMENT_TYPE } from '@secuura/shared/documents/default-type';
// KS-1871: the scope arm of the document-create gate below; the deep path middleware/scopes.ts already imports.
import { hasScope } from '@secuura/shared/security/scopes';
// KS-955 P2a: the two originate forwards in this file bypass http-proxy-middleware, so they
// take the gateway vouch from the one reader in utils/originateForward.ts.
import { vouchHeaderFor } from '../utils/originateForward';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface UserPayload {
  userId: string;
  email: string;
  role: string;
  organizationId?: string;
  verificationLevel: string;
  authMethod?: string;
  mfaEnabled?: boolean;
  tenantId?: string;
  tenantSlug?: string;
}

interface RejectionData {
  status: string;
  rejectionReason: string;
  rejectedAt: string;
  rejectedBy: string;
}

interface ConnectorMeta {
  connectorId: string;
  scopes: string[];
  organizationId: string;
  rateLimit: number;
  rateLimitWindow: number;
}

interface ServiceConfig {
  name: string;
  url: string;
  healthPath: string;
  requiresAuth: boolean;
}

// Augment Express Request so TypeScript knows about .user and .connectorMeta
declare module 'express-serve-static-core' {
  interface Request {
    user?: UserPayload;
    connectorMeta?: ConnectorMeta;
    requestId?: string;
  }
}

// ---------------------------------------------------------------------------
// Dependencies injected from the main gateway
// ---------------------------------------------------------------------------

export interface VerificationRouteDeps {
  /** authenticateToken middleware factory (pass `true` for required, `false` for optional) */
  authenticateToken: (required: boolean) => RequestHandler;
  /** Express JSON body parser middleware */
  mockBodyParser: RequestHandler;
  /** Database query function from db.ts */
  query: <T extends Record<string, unknown> = Record<string, unknown>>(
    text: string,
    params?: unknown[],
  ) => Promise<{ rows: T[] }>;
  /** Is the database currently available? */
  isDbAvailable: () => boolean;
  /** Redis service (re-exported, but kept as dep for explicitness) */
  redisService: typeof redisService;
  /** Service URL config map */
  services: Record<string, ServiceConfig>;
  /** Structured logger */
  log: (level: 'info' | 'warn' | 'error', message: string, meta?: object) => void;
  /** In-memory workflow-to-document mapping */
  memWorkflowToDocumentMap: Map<string, string>;
  /** In-memory rejected documents map */
  memRejectedDocuments: Map<string, RejectionData>;
  /** Persist a rejection to memory + DB */
  dbSaveRejection: (docId: string, data: RejectionData) => Promise<void>;
  /** ADMIN_ROLES constant */
  ADMIN_ROLES: string[];

  // Enforcement helpers
  enforceDocumentTypeRules: (
    body: Record<string, unknown>,
    user: UserPayload | undefined,
  ) => Promise<
    | { ok: true; docType: Record<string, unknown> }
    | { ok: false; status: number; error: string; code: string }
  >;
  createWorkflowInstanceIfRequired: (
    docType: Record<string, unknown>,
    documentId: string,
    body: Record<string, unknown>,
    user: UserPayload | undefined,
  ) => Promise<{ gated: true; response: Record<string, unknown> } | { gated: false }>;
  /**
   * How long workflow approve waits for originate to answer the forward (default ORIGINATE_FORWARD_TIMEOUT_MS). Must be an integer
   * from 1 to 2147483647: createVerificationRoutes throws on anything else (KS-1185).
   */
  originateForwardTimeoutMs?: number;
}

/**
 * KS-1183: the longest POST /api/workflow-instances/:id/approve waits for originate
 * to answer the document forward. Without a bound, an originate that accepts the
 * connection and never answers holds the approve open indefinitely, and a 201 that
 * arrives after the caller gave up creates the document while the caller was told
 * nothing. The tightest proxy in front of the gateway stops waiting at 30 s
 * (`proxy_read_timeout 30s` in docker/nginx-gateway/nginx-production.conf), so the
 * route answers well inside that.
 *
 * KS-1185 F2: the bound is an IDLE timer, not a total one. It is armed with
 * http.ClientRequest#setTimeout, a socket-inactivity timeout, so every byte originate
 * sends restarts it, an informational 1xx (such as 102 Processing) included. "Well
 * inside 30 s" therefore holds for an originate that goes silent; one that keeps
 * sending 1xx holds the approve past the bound (the real originate sends none).
 * nginx's proxy_read_timeout is also measured between two reads, not over the whole
 * response, so the proxy would keep waiting too. Pinned by
 * ks1185-f2-f3-idle-bound-and-late-body-log.test.ts. (This comment used to imply a
 * total bound by saying only "answers well inside that".)
 */
export const ORIGINATE_FORWARD_TIMEOUT_MS = 15_000;

/**
 * KS-1185 F1: the longest timer Node honours. Above it Node truncates the timer to this value and only prints a TimeoutOverflowWarning,
 * so a larger bound would silently behave as "never" (about 24.8 days).
 */
const MAX_FORWARD_TIMEOUT_MS = 2_147_483_647;

/**
 * KS-1185 F1: the bound the forward to originate is armed with. `undefined` means the production default; anything else must be an
 * integer from 1 to MAX_FORWARD_TIMEOUT_MS, or the routes refuse to build. A destructuring default only replaces `undefined`, so before
 * this every other value reached http.ClientRequest#setTimeout: 0 meant never, -1 / NaN / Infinity / a string / null threw inside the
 * promise executor, and 1.5 fired after about 2 ms. Throwing here means a mis-wired bound (Number(process.env.X) with X unset is NaN)
 * fails when the gateway boots, not on the first approve while originate is down. Number.isInteger already refuses every non-number.
 */
function resolveOriginateForwardTimeoutMs(value: unknown): number {
  if (value === undefined) return ORIGINATE_FORWARD_TIMEOUT_MS;
  if (Number.isInteger(value) && (value as number) > 0 && (value as number) <= MAX_FORWARD_TIMEOUT_MS) return value as number;
  // String() flattens 1n to "1" and -0 to "0", which read as the valid 1 and the refused 0 (KS-1518): show the type for those two.
  // KS-1542: it also flattens [1] to "1" (the valid bound), [] to "" and {} to "[object Object]": an object prints as JSON, or as its
  // type tag when JSON.stringify throws (a cycle, a BigInt inside).
  let shown = typeof value === 'string' ? JSON.stringify(value) : typeof value === 'bigint' ? `${value}n` : Object.is(value, -0) ? '-0' : String(value);
  if (typeof value === 'object' && value !== null) {
    try {
      shown = JSON.stringify(value);
    } catch {
      shown = Object.prototype.toString.call(value);
    }
  }
  throw new Error(
    `originateForwardTimeoutMs must be an integer from 1 to ${MAX_FORWARD_TIMEOUT_MS} milliseconds (got ${shown}); omit it for the ${ORIGINATE_FORWARD_TIMEOUT_MS} ms default`,
  );
}

// ---------------------------------------------------------------------------
// Helper: check if a document/certification exists on the originate service
// ---------------------------------------------------------------------------

function makeCheckDocumentExists(services: Record<string, ServiceConfig>) {
  // BACKLOG #5: originate requires auth on /api/documents/:id (F-04
  // trust-header middleware). Without forwarding the caller's bearer
  // token, originate returns 401 and verify() treats every existing
  // document as "not found". The optional `authHeader` is the raw
  // value of req.headers.authorization (e.g. "Bearer eyJ…") from the
  // verify route.
  return (docId: string, authHeader?: string): Promise<boolean> => {
    return new Promise((resolve) => {
      const originateUrl = services.originate?.url || 'http://localhost:6000';
      const url = new URL(`${originateUrl}/api/documents/${docId}`);
      const http = originateUrl.startsWith('https') ? require('https') : require('http');
      const req = http.get(
        {
          hostname: url.hostname,
          port: url.port,
          path: url.pathname,
          timeout: 3000,
          headers: authHeader ? { Authorization: authHeader } : {},
        },
        (proxyRes: any) => {
          let body = '';
          proxyRes.on('data', (chunk: string) => { body += chunk; });
          proxyRes.on('end', () => {
            if (proxyRes.statusCode === 200) {
              try {
                const data = JSON.parse(body);
                resolve(!!data && !!data.id);
              } catch {
                resolve(false);
              }
            } else {
              resolve(false);
            }
          });
        },
      );
      req.on('error', () => resolve(false));
      req.on('timeout', () => { req.destroy(); resolve(false); });
    });
  };
}

/**
 * KS-529 / KS-1432: the POST /api/documents body guard. `JSON.parse` returns whatever the document was (a
 * literal null, a number, a string, an array); only a non-null, non-array object is an acceptable body.
 * Exported so the unit test exercises THIS predicate rather than a copy of it.
 */
export function isAcceptableDocumentBody(parsed: unknown): boolean {
  return !(parsed === null || typeof parsed !== 'object' || Array.isArray(parsed));
}

/**
 * KS-1871: the roles that may create a document, copied from originate's DOCUMENT_WRITE_ROLES
 * (services/originate/src/middleware/documentWriteRoles.ts). The gateway does not import from a service, so this is
 * a copy; ks1871-document-create-requires-a-write-role-or-scope.test.ts reads both files and fails if they differ.
 */
const GATEWAY_DOCUMENT_WRITE_ROLES = ['ISSUER_ADMIN', 'ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN'];

/**
 * KS-1871: may this principal create a document? Originate's create rule (routes/documents.ts, isAllowedByRoleOrScope
 * with DOCUMENT_WRITE_ROLES and 'documents:write'): a document-write role, or the documents:write scope. An OWNER
 * login token carries that scope (KS 151) and a connector key carries its own. Stricter than originate on two shapes
 * no real mint produces: a role that is not a string is refused, and only a-z is case-folded (originate's
 * String(role).toUpperCase() also folds U+0131 and U+017F, the KS 1591 class).
 */
function canCreateDocument(user: { role?: unknown; scopes?: unknown } | undefined): boolean {
  if (!user) return false;
  if (typeof user.role === 'string' && GATEWAY_DOCUMENT_WRITE_ROLES.includes(user.role.replace(/[a-z]/g, (ch) => ch.toUpperCase()))) {
    return true;
  }
  const scopes = Array.isArray(user.scopes) ? user.scopes.filter((s): s is string => typeof s === 'string') : [];
  return hasScope(scopes, 'documents:write');
}

// ---------------------------------------------------------------------------
// Middleware: block sign/anchor/share on documents pending workflow approval
// ---------------------------------------------------------------------------

function makeBlockPendingApproval(deps: Pick<VerificationRouteDeps, 'redisService'>): RequestHandler {
  return async (req: Request, res: Response, next: NextFunction) => {
    const docId = req.params.id;
    if (docId) {
      const pending = await deps.redisService.getPendingDocument(docId);
      if (pending) {
        res.status(403).json({
          success: false,
          error: {
            code: 'PENDING_APPROVAL',
            message: 'Document is pending workflow approval and cannot be modified until approved',
            details: { documentId: docId },
          },
        });
        return;
      }
    }
    next();
  };
}

// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------

export function createVerificationRoutes(deps: VerificationRouteDeps): Router {
  const router = Router();
  const {
    authenticateToken,
    mockBodyParser: injectedBodyParser,
    query,
    isDbAvailable,
    redisService,
    services,
    log,
    memWorkflowToDocumentMap,
    memRejectedDocuments,
    dbSaveRejection,
    ADMIN_ROLES,
    enforceDocumentTypeRules,
    createWorkflowInstanceIfRequired,
    originateForwardTimeoutMs: originateForwardTimeoutOverride,
  } = deps;
  const originateForwardTimeoutMs = resolveOriginateForwardTimeoutMs(originateForwardTimeoutOverride);

  // ==========================================================================
  // KS-815 — THIS ROUTER GUARDS THE BODY IT PARSES ITSELF.
  //
  // The gateway's global control-byte guard cannot cover these routes, and that
  // is not a bug in the guard. In `index.ts`: `shouldParseBody()` returns false
  // for every `proxyPaths` prefix, and `/api/documents` and `/api/certifications`
  // are both on that list, so the global `express.json()` is skipped and
  // `req.body` is still unset when `rejectNulBytes()` runs. The guard then
  // no-ops — correctly, by its own documented contract ("No-op when req.body is
  // unset"). This router is mounted later and parses with the parser it is
  // handed, AFTER the guard has already gone by.
  //
  // Measured over a real socket by the KS-800 re-gate: a NUL in the body of
  // POST /api/documents/:id/verify and POST /api/certifications/:id/verify
  // returned 200 with the NUL present in `req.body`, against a control
  // (POST /api/workflows/:id/reject) that returned 400 — that route is NOT on
  // `proxyPaths`, so the global parser and guard both cover it. The control
  // discriminating is what made this a finding rather than a broken probe.
  //
  // GUARDING HERE RATHER THAN AT THE CALL SITE IS THE POINT. Composing the
  // parser in `index.ts` would leave this router safe only for callers that
  // remember to do it — precisely the "per-service convention" that KS-800's
  // own `mountBodyParsers` doc comment calls "the class of guard that
  // eventually fails". Wrapping the injected parser here makes the router safe
  // by construction for every caller, and lets a test prove it against this
  // module instead of against a replica of index.ts's wiring.
  //
  // The four `/api/workflows*` routes are now guarded twice. That is a no-op
  // and it is deliberate: the outer coverage is an accident of them not being
  // on `proxyPaths`, and a future addition to that list would silently remove
  // it.
  // ==========================================================================
  const controlByteGuard = rejectControlBytes();
  const mockBodyParser: RequestHandler = (req, res, next) => {
    injectedBodyParser(req, res, (err?: unknown) => {
      if (err) { next(err as Error); return; }
      controlByteGuard(req, res, next);
    });
  };

  const checkDocumentExists = makeCheckDocumentExists(services);
  const blockPendingApproval = makeBlockPendingApproval({ redisService });

  // ==========================================================================
  // MOCK DOCUMENT/CERTIFICATION VERIFY ENDPOINTS (for E2E tests)
  // ==========================================================================

  // Certification verify endpoint (for test compatibility)
  router.post('/api/certifications/:id/verify', mockBodyParser, async (req: Request, res: Response) => {
    const { id } = req.params;
    const { requestedFields, purpose } = req.body || {};

    const authHeader = req.headers.authorization as string | undefined;
    const exists = await checkDocumentExists(id, authHeader);
    if (!exists) {
      res.status(404).json({
        verified: false,
        certificationId: id,
        error: 'Certification not found',
        checks: {
          exists: false,
        },
        verifiedAt: new Date().toISOString(),
      });
      return;
    }

    // Pen-test F-03: certifications/:id/verify previously fabricated chain
    // metadata for every request. Until the originate→anchoring rewire
    // lands, this endpoint can no longer claim `anchored: true` —
    // certifications without real on-chain confirmation get
    // `confidence: 'pending-onchain'` and `verified: false`.
    res.json({
      verified: false,
      certificationId: id,
      status: 'issued',
      issuer: {
        id: 'test-issuer',
        verified: true,
      },
      blockchain: {
        anchored: false,
        txHash: null,
        blockHeight: null,
        confidence: 'pending-onchain',
        confirmedAt: null,
      },
      verificationConfidence: 'pending-onchain',
      requestedFields: requestedFields || [],
      purpose: purpose || 'verification',
      verifiedAt: new Date().toISOString(),
    });
  });

  // ============================================================================
  // /api/verification/verify — REMOVED 2026-04-29 (verifier consolidation)
  // ============================================================================
  // The mock /api/verification/verify route was a Local-only duplicate of
  // services/originate/src/routes/verification.ts that emitted a different
  // checks schema (exists/hashValid/notRevoked/hasSignatures/blockchainAnchored)
  // than production (documentExists/hashValid/isCertified/isRevoked/
  // integrityVerified). The cross-env audit on 2026-04-28 surfaced the
  // divergence as F-DEMO-VERIFY-01: an H11 "fix" was applied to this mock
  // and never to originate, so Local appeared correct while production
  // (Dev + Demo) ran the original (also-buggy) chain-first path.
  //
  // The fix landed in originate at d215b4d85 (chain-first now downgrades
  // drafts). Removing this duplicate makes originate the SINGLE source
  // of truth for /api/verification/verify across all envs:
  //   - the gateway proxyPaths list (gateway/src/index.ts:330) routes
  //     /api/verification/* to originate by default
  //   - the verifier portal UI iterates Object.entries(checks) so it
  //     handles either schema (no UI change needed)
  //   - frontend/shared/src/schemas/verify.ts ChecksSchema is updated
  //     in the same commit to model originate's actual fields
  //
  // The /api/certifications/:id/verify mock route ABOVE this block remains — it
  // implements a test-only flow that originate doesn't expose. The
  // /api/documents/:id/verify mock beside it (verification-level enforcement,
  // three-tier lookup including anchor_store fallback) was retired in KS-1628:
  // nothing called it (0 calls at the edge on kintsugi and demo, 2026-10-19), and
  // its honesty rules were ported to originate's isAnchoredHonestly first.
  // ============================================================================

  // ==========================================================================
  // WORKFLOW REJECTION & INSTANCE MANAGEMENT
  // ==========================================================================

  // Workflow rejection endpoint
  router.post('/api/workflows/:workflowId/reject', authenticateToken(true), mockBodyParser, async (req: Request, res: Response) => {
    const { workflowId } = req.params;
    const { reason, comments, documentId: bodyDocumentId } = req.body || {};

    const rejectionReason = reason || 'Document verification failed';
    const rejectedAt = new Date().toISOString();
    const rejectedBy = req.user?.userId || 'admin';

    // Try Redis first, then fall back to in-memory map
    let mappedDocumentId: string | null = null;
    try {
      mappedDocumentId = await redisService.getWorkflowDocumentMapping(workflowId);
    } catch { /* Redis unavailable — fall through */ }
    if (!mappedDocumentId) {
      mappedDocumentId = memWorkflowToDocumentMap.get(workflowId) || null;
    }
    const docId = bodyDocumentId || mappedDocumentId || workflowId;

    const rejectionData: RejectionData = {
      status: 'rejected',
      rejectionReason,
      rejectedAt,
      rejectedBy,
    };

    await dbSaveRejection(docId, rejectionData);

    if (mappedDocumentId && mappedDocumentId !== docId) {
      await dbSaveRejection(mappedDocumentId, rejectionData);
    }

    await dbSaveRejection('mock-document-id', rejectionData);

    log('info', 'Workflow rejected', { workflowId, documentId: docId, mappedDocumentId });

    res.json({
      success: true,
      workflowId,
      documentId: docId,
      status: 'rejected',
      rejectedBy,
      rejectionReason,
      comments: comments || '',
      rejectedAt,
    });
  });

  // =========================================================================
  // WORKFLOW INSTANCE MANAGEMENT (approve / reject / query)
  // =========================================================================

  router.get('/api/workflow-instances/:id', authenticateToken(true), async (req: Request, res: Response) => {
    const instance = await redisService.getWorkflowInstance(req.params.id) as Record<string, unknown> | null;
    if (!instance) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Workflow instance not found' } });
      return;
    }
    res.json(instance);
  });

  router.get('/api/workflow-instances', authenticateToken(true), async (_req: Request, res: Response) => {
    const instances = await redisService.getAllWorkflowInstances();
    res.json(instances);
  });

  router.post('/api/workflow-instances/:id/approve', authenticateToken(true), mockBodyParser, async (req: Request, res: Response) => {
    const instance = await redisService.getWorkflowInstance(req.params.id) as Record<string, unknown> | null;
    if (!instance) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Workflow instance not found' } });
      return;
    }

    if (instance.status === 'approved' || instance.status === 'completed') {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Workflow already completed' } });
      return;
    }
    if (instance.status === 'rejected') {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Workflow was rejected and cannot be approved' } });
      return;
    }

    const steps = (instance.steps || []) as Array<Record<string, unknown>>;
    const currentIdx = (instance.currentStepIndex as number) || 0;
    const currentStep = steps[currentIdx];

    if (currentStep) {
      const approverValue = (currentStep.approverValue || '') as string;
      const approverType = (currentStep.approverType || 'role') as string;
      const userRole = req.user?.role || '';
      const userId = req.user?.userId || '';

      if (approverType === 'role' && approverValue) {
        const allowedRoles = typeof approverValue === 'string' ? approverValue.split(',').map(r => r.trim().toLowerCase()) : [];
        if (allowedRoles.length > 0 && !allowedRoles.includes(userRole.toLowerCase()) && !ADMIN_ROLES.includes(userRole)) {
          res.status(403).json({ error: `Not authorized to approve this step. Required role: ${approverValue}` });
          return;
        }
      } else if (approverType === 'user' && approverValue) {
        if (approverValue !== userId && !ADMIN_ROLES.includes(userRole)) {
          res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Not authorized to approve this step' } });
          return;
        }
      }

      currentStep.status = 'approved';
      currentStep.approvedBy = userId;
      currentStep.approvedAt = new Date().toISOString();
      currentStep.comments = (req.body || {}).comments || '';
    }

    const nextIdx = currentIdx + 1;
    if (nextIdx < steps.length) {
      instance.currentStepIndex = nextIdx;
      steps[nextIdx].status = 'pending';
      instance.status = 'pending_approval';
      await redisService.setWorkflowInstance(req.params.id, instance);

      res.json({
        success: true,
        instanceId: req.params.id,
        status: 'pending_approval',
        message: `Step ${currentIdx + 1} approved. Awaiting step ${nextIdx + 1}: ${steps[nextIdx].name}`,
        currentStep: steps[nextIdx],
        approvedBy: req.user?.userId,
      });
    } else {
      instance.status = 'approved';
      instance.completedAt = new Date().toISOString();
      await redisService.setWorkflowInstance(req.params.id, instance);

      const documentId = instance.documentId as string;
      const pendingDoc = await redisService.getPendingDocument(documentId) as Record<string, unknown> | null;

      if (pendingDoc) {
        const originateUrl = services.originate?.url || 'http://localhost:6000';
        const http = originateUrl.startsWith('https') ? require('https') : require('http');
        const url = new URL(`${originateUrl}/api/documents`);
        const payload = JSON.stringify({
          title: pendingDoc.title,
          documentType: pendingDoc.documentType || pendingDoc.type,
          description: pendingDoc.description,
          contentHash: pendingDoc.contentHash,
          data: pendingDoc.data,
        });
        const forwardHeaders: Record<string, string> = {
          'Content-Type': 'application/json',
          'Content-Length': String(Buffer.byteLength(payload)),
        };
        if (pendingDoc.createdBy) forwardHeaders['x-user-id'] = pendingDoc.createdBy as string;
        // KS-955 P2a: vouch, so a provisioned originate does not drop x-user-id as unvouched.
        // This forward still carries no Bearer and originate answers 401 — that is KS-1087,
        // not changed here.
        Object.assign(forwardHeaders, vouchHeaderFor('originate'));

        // The status line decides: originate persists the document before it writes a 2xx
        // (services/originate/src/routes/documents.ts), so a 2xx header means it exists.
        // The promise settles once; later resolveStatus calls are no-ops.
        const forwardStatus: number = await new Promise<number>((resolveStatus) => {
          // KS-1185 F3: the status line that decided this forward, once it arrived (0 = none yet). A later request
          // error is then about the reply BODY, not the forward, and is logged as such below.
          let decidedByStatus = 0;
          const proxyReq = http.request(
            { hostname: url.hostname, port: url.port, path: url.pathname, method: 'POST', headers: forwardHeaders },
            (proxyRes: any) => {
              decidedByStatus = proxyRes.statusCode || 0;
              proxyRes.on('data', () => { /* drain only: the reply body is not read (KS-1543) */ });
              proxyRes.on('end', () => {
                log('info', 'Workflow approved — document forwarded to originate', { documentId });
              });
              // KS-1183: a response that fails mid-body settles as a transport failure, so
              // moving the resolve into 'end' can never leave the route unanswered.
              proxyRes.on('error', () => resolveStatus(0));
              proxyRes.on('aborted', () => resolveStatus(0));
              proxyRes.on('close', () => resolveStatus(0));
              resolveStatus(proxyRes.statusCode || 0);
            },
          );
          // KS-1183: an originate that never answers is a failed forward at the bound.
          // Destroying the request also stops a late 201 reaching this handler.
          proxyReq.setTimeout(originateForwardTimeoutMs, () => {
            proxyReq.destroy(new Error(`originate did not answer within ${originateForwardTimeoutMs} ms`));
          });
          proxyReq.on('error', (err: Error) => {
            if (decidedByStatus) {
              // KS-1185 F3: the status line already settled the forward (a 2xx means originate persisted the document and the
              // caller was told so), so an error now, e.g. the idle bound firing on a body that never ends, is about the reply
              // body only. It used to log 'Failed to forward approved document to originate' at error level here, which
              // contradicted the 200 the caller had already been given.
              log('warn', 'Approved-document forward: originate\'s reply body did not finish after its status line had decided the forward', { status: decidedByStatus, error: err.message });
            } else {
              log('error', 'Failed to forward approved document to originate', { error: err.message });
            }
            resolveStatus(0);
          });
          proxyReq.write(payload);
          proxyReq.end();
        });
        if (forwardStatus < 200 || forwardStatus >= 300) {
          res.status(502).json({ success: false, error: { code: 'ORIGINATE_FORWARD_FAILED', message: 'Approved, but the document could not be created in originate; the pending document was kept', status: forwardStatus } });
          return;
        }
        await redisService.deletePendingDocument(documentId);
      }

      res.json({
        success: true,
        instanceId: req.params.id,
        status: 'approved',
        documentId,
        message: 'All workflow steps approved. Document has been created.',
        approvedBy: req.user?.userId,
        completedAt: instance.completedAt,
      });
    }
  });

  router.post('/api/workflow-instances/:id/reject', authenticateToken(true), mockBodyParser, async (req: Request, res: Response) => {
    const instance = await redisService.getWorkflowInstance(req.params.id) as Record<string, unknown> | null;
    if (!instance) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Workflow instance not found' } });
      return;
    }

    if (instance.status === 'approved' || instance.status === 'completed') {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Workflow already completed and cannot be rejected' } });
      return;
    }
    if (instance.status === 'rejected') {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Workflow already rejected' } });
      return;
    }

    const { reason, comments } = req.body || {};
    instance.status = 'rejected';
    instance.rejectedBy = req.user?.userId;
    instance.rejectedAt = new Date().toISOString();
    instance.rejectionReason = reason || 'Rejected by approver';
    await redisService.setWorkflowInstance(req.params.id, instance);

    const documentId = instance.documentId as string;
    if (documentId) {
      await dbSaveRejection(documentId, {
        status: 'rejected',
        rejectionReason: instance.rejectionReason as string,
        rejectedAt: instance.rejectedAt as string,
        rejectedBy: instance.rejectedBy as string,
      });
      await redisService.deletePendingDocument(documentId);
    }

    res.json({
      success: true,
      instanceId: req.params.id,
      documentId,
      status: 'rejected',
      rejectedBy: req.user?.userId,
      reason: instance.rejectionReason,
      comments: comments || '',
      rejectedAt: instance.rejectedAt,
    });
  });

  // Legacy workflow approve/reject endpoints (backward compatibility)
  router.post('/api/workflows/:workflowId/approve', authenticateToken(true), mockBodyParser, (req: Request, res: Response) => {
    const { workflowId } = req.params;
    const { comments } = req.body || {};
    res.json({
      success: true,
      workflowId,
      status: 'approved',
      approvedBy: req.user?.userId || 'admin',
      comments: comments || '',
      approvedAt: new Date().toISOString(),
    });
  });

  // =========================================================================
  // DOCUMENT CREATION with Enforcement Pipeline
  // =========================================================================

  router.post('/api/documents', authenticateToken(true), (req: Request, res: Response, _next: NextFunction) => {
    const chunks: Buffer[] = [];
    req.on('data', (chunk: Buffer) => { chunks.push(chunk); });

    // KS-529: an `async` event-listener's rejection has nowhere to go — it
    // surfaces as an unhandledRejection, which this service treats as fatal
    // (index.ts installs a gracefulShutdown handler). So ANY unguarded throw in
    // the body below took the entire gateway offline for every tenant. The
    // wrapper below converts that into a 500 for the one request instead.
    req.on('end', () => { void (async () => {
      const rawBody = Buffer.concat(chunks);
      let body: Record<string, unknown>;
      try {
        const parsed = rawBody.length ? JSON.parse(rawBody.toString()) : {};
        // KS-529: `JSON.parse` returns whatever the document was — a literal
        // `null`, a number, a string, an array — not necessarily an object.
        // A body of `null` therefore made `body.documentType` throw
        // "Cannot read properties of null" downstream in enforceDocumentTypeRules,
        // and because that throw happened inside THIS async 'end' callback it
        // escaped as an unhandledRejection and took the whole gateway down
        // (one authenticated request = platform-wide outage). Same family as
        // KS-501, which fixed the non-string case but not the non-object one.
        // KS-1432: this is the exported isAcceptableDocumentBody, the predicate ks529-non-object-body-guard.test.ts calls.
        if (!isAcceptableDocumentBody(parsed)) {
          res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Request body must be a JSON object' } });
          return;
        }
        body = parsed as Record<string, unknown>;
      } catch {
        res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid JSON body' } });
        return;
      }

      // ---------------------------------------------------------------------
      // KS-815 F-02 — GUARD THE BODY THIS ROUTE PARSED BY HAND.
      //
      // The wrapper above guards whatever parser the router is HANDED. This
      // route takes no parser middleware at all — it reads `req.on('data')`
      // and calls `JSON.parse` itself — so there is no parser for the wrapper
      // to wrap, and nothing for the guard to have inspected. `/api/documents`
      // is on `proxyPaths`, so the global guard no-oped for it too: the same
      // mechanism as the two verify routes, reached by a different road.
      //
      // Measured over a raw socket before this line existed: a NUL in the body
      // was NOT refused (502 here, 201 with the byte persisted and echoed
      // against a real originate). Authenticated, any role, production-live.
      //
      // AFTER the parse, deliberately. The route already answers its own 400s
      // for unparseable JSON and for a non-object body (KS-529); guarding
      // before the parse would take those answers over. Two controls pin that.
      //
      // `req.body` is set because the shared guard reads it — reusing the
      // platform middleware is what keeps this refusal byte-identical to every
      // other one (`400 VALIDATION_ERROR` naming the path) instead of a second
      // hand-rolled refusal that drifts from it. The assignment is otherwise
      // inert: the forward below writes `rawBody`, not `req.body`.
      // ---------------------------------------------------------------------
      req.body = body;
      let guardPassed = false;
      controlByteGuard(req, res, () => { guardPassed = true; });
      if (!guardPassed) {
        // The guard refused and has already written its 400. The headersSent
        // check is not defensive noise: `rejectControlBytes` is synchronous
        // today, and if it ever stopped being, `guardPassed` would be false
        // with nothing written and this request would hang silently inside an
        // async handler. A loud 500 beats a hang, and this is the one place
        // that can tell the two apart.
        if (!res.headersSent) {
          res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create document' } });
        }
        return;
      }

      // --- Connector scope and document type enforcement ---
      const connectorMeta = (req as any).connectorMeta as ConnectorMeta | undefined;
      if (connectorMeta) {
        // KS-480: the canonical KS-71 scope for document creation is
        // `documents:write` — the pre-KS-71 literal `register` blocked every
        // canonically-scoped key from this route. `register` stays accepted
        // for keys minted before the vocabulary existed.
        const canCreate = connectorMeta.scopes.some(s => s === 'documents:write' || s === 'register' || s === '*' || s === 'documents:*');
        if (!canCreate) {
          res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector does not have "documents:write" scope' } });
          return;
        }
        let connectorConfig: Record<string, unknown> = {};
        // KS-1231 (#1035 gate N-1): the stored container is read FAIL CLOSED for the calling connector.
        // A non-array integrations, a non-object entry, a second entry with this connector id, or a
        // non-object config on this connector entry refuses the create instead of reading as no
        // restriction (the parse used to leave connectorConfig = {} on any throw or miss).
        let containerBad = false;
        // KS-1256: the allow-list read FAILS CLOSED when the configuration cannot be read.
        // Prior behaviour: an unreadable platform-settings left connectorConfig = {} and so EVERY
        // restricted connector read as UNRESTRICTED -- the same fail-open class KS-1233 closed for
        // the TTL trigger only. Measured on this branch: when Redis is unavailable
        // getNotificationSettings resolves null out of an empty in-memory store WITHOUT throwing
        // (services/redis.ts:671-678), and `fallbackMode` is set on a sustained runtime outage by
        // retryStrategy at services/redis.ts:78, which carries NO NODE_ENV guard -- so production
        // reaches this state too, despite refusing to START without Redis. A catch cannot observe a
        // resolved null, which is why this is an explicit availability test BEFORE the read rather
        // than part of the catch below.
        if (!redisService.isRedisAvailable()) {
          res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Connector allow-list configuration is currently unreadable; refusing until it can be read' } });
          return;
        }
        // KS-1256 (option C): a MISSING key with Redis up used to read as "no restriction" (null -> {} -> no
        // integrations), so after an allkeys-lru eviction every restricted connector was unrestricted. The key is now
        // read through the settings store: a miss reads the stored record (svc_gateway_settings) and refills Redis;
        // a miss with no readable record refuses below with the Redis-down 503. A thrown Redis read still reaches
        // the catch.
        let settingsUnreadable = false;
        try {
          const read = await readPlatformSettings(redisService, { query, isDbAvailable }, (message, meta) => log('warn', message, { route: 'POST /api/documents', ...meta }));
          if (read.kind === 'unreadable') settingsUnreadable = true;
          const sRaw = read.kind === 'present' ? read.settings : null;
          const sAll = (sRaw || {}) as Record<string, unknown>;
          const ints: unknown = (sAll as any)?.integrations === undefined ? [] : (sAll as any).integrations;
          if (!Array.isArray(ints)) {
            containerBad = true;
          } else {
            let matched = 0;
            for (const entry of ints) {
              if (entry === null || typeof entry !== 'object' || Array.isArray(entry)) { containerBad = true; break; }
              const e = entry as Record<string, unknown>;
              if (e.id !== connectorMeta.connectorId) continue;
              matched += 1;
              const cfg = e.config;
              if (matched > 1 || (cfg !== undefined && cfg !== null && (typeof cfg !== 'object' || Array.isArray(cfg)))) { containerBad = true; break; }
              if (cfg) connectorConfig = cfg as Record<string, unknown>;
            }
          }
        } catch {
          // KS-1256: a THROWN read refuses the create instead of granting everything. Shapes that
          // reach here: the client's MaxRetriesPerRequestError, and the SyntaxError raised by
          // JSON.parse at services/redis.ts:675 on malformed stored bytes. Prior behaviour: a bare
          // `} catch {}` swallowed both and left connectorConfig = {} -- no restriction.
          res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Connector allow-list configuration could not be read; refusing until it can be read' } });
          return;
        }
        if (settingsUnreadable) {
          res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Connector allow-list configuration is currently unreadable; refusing until it can be read' } });
          return;
        }
        if (containerBad) {
          res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector allow-list container is malformed; refusing until it is corrected' } });
          return;
        }
        // KS-1204 (#1014 gate N-2): the allow-list is stored by PUT /api/admin/settings,
        // which merges the body verbatim, so it is not guaranteed to be an array. Cast
        // to string[], a STRING made `.includes` a substring match ("SSD_DOCUMENT"
        // admitted DOCUMENT). A configured allow-list that is not an array now refuses
        // every create (fail closed). Absent or null still means no restriction.
        const rawAllowedTypes = connectorConfig.allowedDocumentTypes;
        if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !Array.isArray(rawAllowedTypes)) {
          res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector document-type allow-list is not a list; refusing until it is corrected' } });
          return;
        }
        // gate 210 planted at the insertion point
        const allowedTypes = (rawAllowedTypes || []) as string[];
        // KS-1176 (QA gate F-1): read the key enforcement reads (enforcement.ts `body.documentType || body.type`).
        // This checked `body.documentType` only, so a restricted connector could name any type via `type`;
        // the verification-level check used to stop the none-rank ones by accident.
        // KS-1203 (#1014 gate N-4): a body that names no type is stored by originate as the DEFAULT type, so the
        // allow-list applies to that resolved type. The check used to be skipped when `requestedType` was falsy,
        // and a connector restricted to ['SSD_DOCUMENT'] could still register a DOCUMENT by sending none (untyped,
        // an empty type, an ignored key, an own __proto__.type, or an untyped data carrier). 403 unless the list
        // contains the default. The default is the shared constant originate stores, not a second literal.
        const requestedType = body.documentType || body.type || DEFAULT_DOCUMENT_TYPE;
        if (allowedTypes.length > 0 && !allowedTypes.includes(requestedType as string)) {
          res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: `Connector is not permitted to register document type "${requestedType}"` } });
          return;
        }
      }

      // --- Enforcement: validate document type rules ---
      const enforcement = await enforceDocumentTypeRules(body, req.user);
      if (!enforcement.ok) {
        const fail = enforcement as { ok: false; status: number; error: string; code: string };
        // KS-466 §7b: this was the one path answering the FLAT
        // `{error, code}` shape — every sibling response here (and the spec)
        // uses the standard `{success:false, error:{code,message}}` envelope.
        res.status(fail.status).json({ success: false, error: { code: fail.code, message: fail.error } });
        return;
      }

      // --- Workflow gate: check if approval workflow is required ---
      const documentId = `doc-${require('crypto').randomUUID()}`;

      // Connectors with bypass policy skip the workflow gate
      let bypassWorkflow = false;
      if (connectorMeta) {
        let connectorConfig: Record<string, unknown> = {};
        try {
          const sRaw = await redisService.getNotificationSettings('platform-settings');
          const sAll = (sRaw || {}) as Record<string, unknown>;
          const ints = ((sAll as any)?.integrations || []) as Array<Record<string, unknown>>;
          const found = ints.find((i: any) => i.id === connectorMeta.connectorId);
          if (found?.config) connectorConfig = found.config as Record<string, unknown>;
        } catch {}
        bypassWorkflow = connectorConfig.workflowPolicy === 'bypass';
      }

      if (!bypassWorkflow) {
        // KS-1871: refuse a caller with neither a document-write role nor the documents:write scope BEFORE the
        // workflow gate writes anything. Before, an approval-gated type stored a workflow instance and the pending
        // document and answered 201 pending_approval for any authenticated caller, while the same caller on a
        // non-gated type got originate's 403. The refusal is originate's own (routes/documents.ts), so both paths
        // answer alike; on a non-gated type the caller now gets it here rather than from originate.
        if (!canCreateDocument((req as any).user)) {
          res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Forbidden: your role does not permit document creation' } });
          return;
        }
        const workflowResult = await createWorkflowInstanceIfRequired(
          enforcement.docType,
          documentId,
          body,
          req.user,
        );

        if (workflowResult.gated) {
          res.status(201).json(workflowResult.response);
          return;
        }
      }

      // --- No workflow needed: forward to originate service ---
      const originateUrl = services.originate?.url || 'http://localhost:6000';
      const http = originateUrl.startsWith('https') ? require('https') : require('http');
      const url = new URL(`${originateUrl}/api/documents`);
      const forwardHeaders: Record<string, string> = {
        'Content-Type': 'application/json',
        'Content-Length': String(rawBody.length),
      };
      // Pen-test F-04: forward identity from authenticated req.user (set by
      // gateway authenticate() middleware), NOT by echoing inbound headers
      // (which would be spoofable on routes that bypass authenticate()).
      const fwdUserId = (req as any).user?.userId as string | undefined;
      if (fwdUserId) forwardHeaders['x-user-id'] = fwdUserId;
      if (req.headers['x-wallet-address']) forwardHeaders['x-wallet-address'] = req.headers['x-wallet-address'] as string;
      if (req.headers['authorization']) forwardHeaders['authorization'] = req.headers['authorization'] as string;
      if ((req as any).requestId) forwardHeaders['x-request-id'] = (req as any).requestId;
      // KS-39 #4: forward tenant context so originate's extractTenantContext
      // doesn't fall back to DEFAULT_TENANT_ID (`a0000000-...`). Without this,
      // POST writes to the fallback tenant while subsequent GET / revoke
      // (which DO carry x-tenant-id through the http-proxy-middleware chain)
      // read from the JWT tenant — and the fresh doc looks invisible / 404s.
      if (req.headers['x-tenant-id']) forwardHeaders['x-tenant-id'] = req.headers['x-tenant-id'] as string;
      if (req.headers['x-tenant-slug']) forwardHeaders['x-tenant-slug'] = req.headers['x-tenant-slug'] as string;
      // KS-955 P2a (KS-1083 R2-1): without the vouch, a provisioned originate drops x-tenant-id
      // and x-user-id as unvouched and saves the document under DEFAULT_TENANT_ID — a 201 with
      // the document in the wrong tenant, no error anywhere.
      Object.assign(forwardHeaders, vouchHeaderFor('originate'));

      const proxyReq = http.request(
        { hostname: url.hostname, port: url.port, path: url.pathname, method: 'POST', headers: forwardHeaders },
        (proxyRes: any) => {
          res.status(proxyRes.statusCode || 500);
          Object.entries(proxyRes.headers).forEach(([k, v]) => { if (v) res.setHeader(k, v as string); });
          proxyRes.pipe(res);
        },
      );
      proxyReq.on('error', (err: Error) => {
        log('error', 'Failed to forward document creation to originate', { error: err.message });
        res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Originate service unavailable' } });
      });
      proxyReq.write(rawBody);
      proxyReq.end();
    })().catch((err: unknown) => {
      // KS-529: last line of defence. Without this the rejection escapes to
      // process.on('unhandledRejection') → gracefulShutdown → the whole gateway
      // exits, turning one malformed request into a platform-wide 502 cascade.
      log('error', 'Document-create pipeline threw', { error: err instanceof Error ? err.message : String(err) });
      if (!res.headersSent) {
        res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create document' } });
      }
    }); });
  });

  // =========================================================================
  // Document fetch interceptor for GET /api/documents/:id
  // Handles documents in pending_approval or rejected state.
  // =========================================================================

  router.get('/api/documents/:id', authenticateToken(true), async (req: Request, res: Response, next: NextFunction) => {
    const { id } = req.params;

    // Check for pending_approval documents (held by workflow gate)
    const pendingDoc = await redisService.getPendingDocument(id) as Record<string, unknown> | null;
    if (pendingDoc) {
      const wfiId = pendingDoc.workflowInstanceId as string;
      const wfi = wfiId ? await redisService.getWorkflowInstance(wfiId) as Record<string, unknown> | null : null;
      res.json({
        id,
        title: pendingDoc.title,
        status: 'pending_approval',
        documentType: pendingDoc.documentType || pendingDoc.type,
        contentHash: pendingDoc.contentHash,
        createdBy: pendingDoc.createdBy,
        createdAt: pendingDoc.createdAt,
        workflowInstance: wfi ? {
          id: wfiId,
          status: wfi.status,
          currentStepIndex: wfi.currentStepIndex,
          steps: wfi.steps,
          workflowName: wfi.workflowName,
        } : undefined,
      });
      return;
    }

    // Check if this document was rejected via workflow
    // Priority: Redis → in-memory Map → DB query
    let rejection: RejectionData | undefined;

    // Try Redis first
    try {
      const redisRejection = await redisService.getRejectedDocument(id);
      if (redisRejection) {
        rejection = {
          status: redisRejection.status,
          rejectionReason: redisRejection.rejectionReason,
          rejectedAt: redisRejection.rejectedAt,
          rejectedBy: redisRejection.rejectedBy,
        };
      }
    } catch { /* Redis unavailable — fall through */ }

    // Fall back to in-memory map
    if (!rejection) {
      rejection = memRejectedDocuments.get(id);
    }

    // Try database if not found in Redis or memory
    if (!rejection && isDbAvailable()) {
      try {
        const result = await query<{
          document_id: string;
          rejected_by: string;
          reason: string;
        }>('SELECT * FROM svc_gateway_rejections WHERE document_id = $1', [id]);

        if (result.rows.length > 0) {
          const row = result.rows[0] as any;
          rejection = {
            status: 'rejected',
            rejectionReason: row.reason,
            rejectedAt: new Date().toISOString(),
            rejectedBy: row.rejected_by,
          };
          memRejectedDocuments.set(id, rejection);
          // Back-fill Redis from DB result (fire-and-forget)
          redisService.setRejectedDocument(id, rejection).catch(() => {});
        }
      } catch {
        // Ignore DB errors - fallback to in-memory only
      }
    }

    if (rejection) {
      res.json({
        id,
        status: rejection.status,
        rejectionReason: rejection.rejectionReason,
        rejectedAt: rejection.rejectedAt,
        rejectedBy: rejection.rejectedBy,
        type: 'DEGREE',
        data: {},
      });
      return;
    }

    // Pass through to originate service via proxy
    next();
  });

  // =========================================================================
  // Block sign/anchor/share on documents pending workflow approval
  // =========================================================================

  router.post('/api/documents/:id/sign', authenticateToken(true), blockPendingApproval);
  router.post('/api/documents/:id/sign/request', authenticateToken(true), blockPendingApproval);
  router.post('/api/documents/:id/anchor', authenticateToken(true), blockPendingApproval);
  router.post('/api/documents/:id/share', authenticateToken(true), blockPendingApproval);

  // KS-375: the mock GET /api/notifications that lived here was dead code —
  // routes/notifications.ts is mounted first (index.ts) and always won the
  // route match, so this handler could never run. Removed.

  // ==========================================================================
  // GOVERNANCE — no handlers here (KS-450)
  // ==========================================================================
  // The governance mock that lived here (GET /api/governance/state, GET+POST
  // /api/governance/proposals, POST /api/governance/proposals/{id}/vote) was
  // labelled a "fallback" but was mounted BEFORE the governance proxy, so it
  // ALWAYS shadowed the real service: proposals created through the public API
  // existed only in the mock's memory and could never be listed, submitted,
  // cancelled, executed or voted through the real governance service. Removed
  // in KS-450 — all /api/governance/* traffic now flows through the catch-all
  // proxy in routes/proxy.ts to the governance microservice, which enforces
  // its own JWT auth and the published request schemas (CreateProposalSchema,
  // CastVoteSchema — pinned by that service's unit tests).

  // =========================================================================
  // PUBLIC DOCUMENT TYPES ENDPOINT (no admin auth required)
  // =========================================================================

  router.get('/api/document-types', async (_req: Request, res: Response) => {
    try {
      const allTypes = await redisService.getAllDocumentTypes();
      const active = (allTypes as Array<Record<string, unknown>>)
        .filter(dt => dt.isActive !== false)
        .map(dt => ({
          id: dt.id,
          name: dt.name,
          code: dt.code,
          description: dt.description,
          category: dt.category,
          creatorVerificationLevel: dt.creatorVerificationLevel || 'none',
          ownerVerificationLevel: dt.ownerVerificationLevel || 'none',
          viewerVerificationLevel: dt.viewerVerificationLevel || 'none',
          verifierVerificationLevel: dt.verifierVerificationLevel || 'none',
          requireMFA: dt.requireMFA || false,
          requireWalletSignature: dt.requireWalletSignature || false,
          requireKYC: dt.requireKYC || false,
          allowedAuthProviders: dt.allowedAuthProviders || [],
          requiresApproval: dt.requiresApproval || false,
          metadataSchema: dt.metadataSchema || [],
        }));
      res.json(active);
    } catch (err) {
      // KS-1619 (gate C INFO-1560-2): fail500's describer (routes/batch.ts, KS-1346), so a thrown plain object logs its TYPE and FIELD NAMES, not [object Object].
      // KS-1771: describing the thrown value and writing the log line can themselves throw (a message getter, a Proxy trap, a revoked Proxy, a logger that fails). Nothing here caught that, so it rejected
      // the async handler from inside this catch and the request got no answer at all, where this route promises the constant 500 below. Describe the value in its own try and log in another (the shape
      // PR 1754 gave platform.ts, KS-1524 a). The line is unchanged for every value that could be described before.
      let described: string;
      try {
        described = err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err;
      } catch {
        described = 'thrown value that could not be described';
      }
      try {
        log('error', 'Failed to fetch document types', { error: described });
      } catch {
        // Nothing more can be said if the logger itself fails; the caller still gets the 500 below.
      }
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch document types' } });
    }
  });

  return router;
}
