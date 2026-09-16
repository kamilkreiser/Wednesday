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
import { rejectControlBytes } from '@secuura/shared';

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
  meetsVerificationLevel: (userLevel: string, requiredLevel: string) => boolean;
  /** How long workflow approve waits for originate to answer the forward (default ORIGINATE_FORWARD_TIMEOUT_MS) */
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
 */
export const ORIGINATE_FORWARD_TIMEOUT_MS = 15_000;

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

function makeFetchDocument(services: Record<string, ServiceConfig>) {
  // BACKLOG #5: same auth-forwarding rationale as makeCheckDocumentExists.
  return (docId: string, authHeader?: string): Promise<Record<string, any> | null> => {
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
                resolve(data && data.id ? data : null);
              } catch {
                resolve(null);
              }
            } else {
              resolve(null);
            }
          });
        },
      );
      req.on('error', () => resolve(null));
      req.on('timeout', () => { req.destroy(); resolve(null); });
    });
  };
}

/**
 * KS-1071: the ONE status→confidence mapping, shared by both lookup tiers.
 *
 * Before this the decision lived twice. Tier 2 (the blob synthesised from the
 * anchor store, below) mapped `confirmed`→on-chain, `failed`→off-chain-only and
 * EVERYTHING ELSE→pending-onchain — an OPEN default. Tier 1 (the persisted
 * document blob, in the verify handler) admitted only `confirmed`/null into
 * `persistedAnchored` and then let anything without its own
 * `confidence: 'pending-onchain'` fall to off-chain-only — a CLOSED default.
 * Measured at develop 721b333a6: a `pending`/`submitted` anchor answered
 * `pending-onchain` via tier 2 and `off-chain-only` via tier 1 (F8), and an
 * out-of-union value such as `expired` answered `pending-onchain` via tier 2
 * (F10) — "still coming", to the third-party verifier, with nothing red.
 * `anchor_store.status` is `TEXT NOT NULL DEFAULT 'pending'` with no CHECK
 * (migrations 001:714, 003:26), so a new terminal value lands there silently.
 *
 * The default is CLOSED: only anchoring's own union
 * ('pending' | 'submitted' | 'confirmed' | 'failed', anchoring/src/index.ts:112)
 * is mapped; anything else — including originate's own `anchor_failed`
 * vocabulary — is off-chain-only.
 *
 * `null`/absent is NOT this function's decision. The tier-1 `persistedAnchored`
 * carve-out (the seeded demo documents, KS-1057) and the statusless
 * `confidence: 'pending-onchain'` fallback (originate routes/documents.ts:1367-1372,
 * routes/certifications.ts:463-469 and :1184-1191) stay where they are.
 *
 * `on-chain` here means "the status alone would allow the claim". The tier-1
 * predicate still requires the hash, the height and `simulated` falsy
 * before it is made (KS-1057; KS-1069 and KS-1070 own those conjuncts).
 */
export function confidenceForAnchorStatus(
  status: unknown,
): 'on-chain' | 'pending-onchain' | 'off-chain-only' {
  switch (status) {
    case 'confirmed':
      return 'on-chain';
    case 'submitted':
    case 'pending':
      return 'pending-onchain';
    case 'failed':
      return 'off-chain-only';
    default:
      // KS-1071 F10: closed. Tier 2's prior behaviour here was 'pending-onchain'.
      return 'off-chain-only';
  }
}

/**
 * BACKLOG #G6 — verifier-role can't verify when they don't own the doc.
 * Originate's GET /api/documents/:id returns 404 to non-owners (sensible:
 * doc records can carry org-internal metadata). But the verifier portal
 * use case is "third party verifies a doc by id+hash", which doesn't need
 * the doc record at all — just the on-chain anchor.
 *
 * This helper hits anchoring's /api/anchors/document/:id which is auth'd
 * but NOT ownership-gated (the data it returns is on-chain public anyway).
 * If anchors exist for this docId, the doc is "anchored" for verification
 * purposes — we synthesise a minimal doc record from the anchor metadata
 * so the rest of the verify handler doesn't care about who owns it.
 *
 * Returns the latest (most recent) anchor's projected doc shape, or null
 * if anchoring has no record either.
 */
function makeFetchDocFromAnchorStore(services: Record<string, ServiceConfig>) {
  return (docId: string, authHeader?: string): Promise<Record<string, any> | null> => {
    return new Promise((resolve) => {
      const anchoringUrl = services.anchoring?.url || 'http://anchoring:4005';
      const url = new URL(`${anchoringUrl}/api/anchors/document/${docId}`);
      const http = anchoringUrl.startsWith('https') ? require('https') : require('http');
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
            if (proxyRes.statusCode !== 200) { resolve(null); return; }
            try {
              const data = JSON.parse(body);
              const anchors = data?.data?.anchors;
              if (!Array.isArray(anchors) || anchors.length === 0) { resolve(null); return; }
              // Latest = highest blockNumber, fall back to most-recent confirmedAt. (QA fixture: a move outside both regions)
              // KS-1072: implement the tiebreak the line above promises. Before this, equal blockNumbers kept
              // anchoring's response order, and since KS-1057 the selected anchor's status decides the verdict.
              const latest = anchors.slice().sort((a: any, b: any) => {
                const byBlock = (b.blockNumber || 0) - (a.blockNumber || 0);
                if (byBlock !== 0) return byBlock;
                return (Date.parse(b.confirmedAt) || 0) - (Date.parse(a.confirmedAt) || 0);
              })[0];
              resolve({
                id: docId,
                // We can't know revocation status without the doc record;
                // assume non-revoked. If the doc IS revoked the owner can
                // still see it via the originate path (above). Documenting
                // limitation: a revoked doc still verifies as on-chain
                // anchored to a non-owner — they need a separate revocation
                // check (e.g. a public revocation list endpoint).
                status: 'anchored',
                contentHash: latest.contentHash || latest.content_hash,
                blockchain: {
                  txHash: latest.transactionHash || latest.transaction_hash,
                  blockHeight: latest.blockNumber || latest.block_number || 0,
                  // KS-1057 F1: carry the anchor's REAL status. It was already
                  // being read on the next line for `confidence` and then
                  // dropped, which left this synthesised blob statusless — and
                  // a statusless blob takes the legacy carve-out below, so this
                  // tier stayed keyed on presence alone while tier 1 became
                  // status-aware. One endpoint answering two ways for the same
                  // anchor state, decided by which lookup tier resolved the
                  // document, and THIS is the tier a third party reaches
                  // (authenticated but not ownership-gated — BACKLOG #G6).
                  status: latest.status,
                  // KS-1070: carry the anchor's `simulated` flag the same way
                  // `status` is carried above. Prior behaviour: this key was
                  // absent, so the handler's `persistedSimulated !== true`
                  // guard read `undefined !== true` on every tier-2 blob — a
                  // confirmed row with a real hash and `simulated: true`
                  // reported on-chain through this tier (measured) while the
                  // same blob via tier 1 reported off-chain-only. It was not
                  // live only because anchoring nulls the hash on a simulated
                  // row (KS-587 `honestTxView`) — an accident of a response
                  // shape, not a guard. The value is carried as-is, not
                  // coerced; the handler reads it with `Boolean()` (widened by
                  // KS-1069: any truthy value is a declaration).
                  simulated: latest.simulated,
                  // Found by running the F1 cells: this mapped EVERY
                  // non-confirmed status to 'pending-onchain', including
                  // 'failed' — so a terminally failed anchor reached via this
                  // tier reported itself as still coming. That is the same
                  // unearned claim as the on-chain one, one value over, and it
                  // is the exact shape KS-1058 refused to carry through the
                  // fail-closed writer. 'failed' is terminal, so it is
                  // off-chain-only; 'submitted'/'pending' are genuinely still
                  // in flight and keep 'pending-onchain'.
                  // KS-1071: this blob carried its OWN `confidence`, decided
                  // by an inline ternary — `confirmed`→on-chain,
                  // `failed`→off-chain-only, everything else→pending-onchain,
                  // an OPEN default that reported an out-of-union status (F10)
                  // as "still coming". The decision is made ONCE now, in the
                  // verify handler, from `status` above through
                  // `confidenceForAnchorStatus`. This blob therefore carries
                  // no `confidence`. Anchoring's `formatAnchorResponse` emits
                  // `status` unconditionally (anchoring/src/index.ts:1596)
                  // over a `TEXT NOT NULL` column, so a tier-2 record without
                  // `status` is not producible today. If one arrives, the
                  // handler answers off-chain-only (closed): the statusless
                  // `confidence` fallback finds nothing to read, and the
                  // statusless on-chain carve-out is tier-1 only — it
                  // excludes `_source: 'anchor_store'` (KS-1073), so a real
                  // hash and height do not earn the claim on this tier.
                  anchoredAt: latest.confirmedAt || latest.createdAt,
                },
                _source: 'anchor_store',  // marker for downstream telemetry
              });
            } catch {
              resolve(null);
            }
          });
        },
      );
      req.on('error', () => resolve(null));
      req.on('timeout', () => { req.destroy(); resolve(null); });
    });
  };
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
    meetsVerificationLevel,
    originateForwardTimeoutMs = ORIGINATE_FORWARD_TIMEOUT_MS,
  } = deps;

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
  const fetchDocument = makeFetchDocument(services);
  const fetchDocFromAnchorStore = makeFetchDocFromAnchorStore(services);
  const blockPendingApproval = makeBlockPendingApproval({ redisService });

  // ==========================================================================
  // MOCK DOCUMENT/CERTIFICATION VERIFY ENDPOINTS (for E2E tests)
  // ==========================================================================

  // Document verify endpoint (with verification level enforcement).
  // KS-375: auth is required — the spec (originate.openapi.ts) documents
  // bearerAuth + 401 on this deprecated, owner-scoped route, and the lookup
  // tiers below all need the forwarded bearer anyway; public verification
  // lives at POST /api/verification/verify.
  router.post('/api/documents/:id/verify', authenticateToken(true), mockBodyParser, async (req: Request, res: Response) => {
    const { id } = req.params;
    const { contentHash, requestedFields, purpose } = req.body || {};

    // Check for pending_approval documents
    const pendingDoc = await redisService.getPendingDocument(id);
    if (pendingDoc) {
      res.status(403).json({
        verified: false,
        documentId: id,
        error: 'Document is pending workflow approval and cannot be verified yet',
        code: 'PENDING_APPROVAL',
      });
      return;
    }

    // Three-tier lookup:
    //   1. Originate's docs route — works for owners; gives full info
    //      including revocation status. (BACKLOG #5: forwards bearer.)
    //   2. Anchoring's /api/anchors/document/:id — works for any authed
    //      caller; gives txHash + contentHash + blockHeight, NO ownership
    //      check. This is the verifier-portal path. (BACKLOG #G6.)
    //   3. Gateway-side mock store — last-resort dev fallback.
    //
    // Only step 1 returns 'revoked' status; for non-owners (verifier
    // path) we treat documents as non-revoked because we have no way to
    // check. Tracked as a follow-up (would need a public revocation list
    // endpoint or on-chain revocation event).
    const authHeader = req.headers.authorization as string | undefined;
    let doc = await fetchDocument(id, authHeader);
    let lookupSource: 'originate' | 'anchor_store' | 'mock' | null = doc ? 'originate' : null;

    if (!doc) {
      doc = await fetchDocFromAnchorStore(id, authHeader);
      if (doc) lookupSource = 'anchor_store';
    }

    if (!doc) {
      const exists = await checkDocumentExists(id, authHeader);
      if (!exists) {
        res.status(404).json({
          verified: false,
          documentId: id,
          error: 'Document not found',
          checks: {
            exists: false,
            notRevoked: false,
            hashValid: false,
            hasSignatures: false,
            blockchainAnchored: false,
          },
          verifiedAt: new Date().toISOString(),
        });
        return;
      }
      // Document exists in mock store but not in originate or anchoring
      doc = { id, status: 'anchored' };
      lookupSource = 'mock';
    }
    // expose for response telemetry
    (doc as any)._lookupSource = lookupSource;

    // Enforce verifierVerificationLevel from the document's specific type config
    const docTypeName = (doc.documentType || doc.type || '').toLowerCase();
    if (docTypeName) {
      const allDocTypes = await redisService.getAllDocumentTypes() as Array<Record<string, unknown>>;
      const matchingType = allDocTypes.find(
        (dt) => ((dt.code as string) || '').toLowerCase() === docTypeName ||
                ((dt.name as string) || '').toLowerCase() === docTypeName,
      );
      if (matchingType) {
        const verifierLevel = (matchingType.verifierVerificationLevel as string || 'none').toLowerCase();
        if (verifierLevel !== 'none') {
          const userLevel = req.user?.verificationLevel || 'none';
          if (!meetsVerificationLevel(userLevel, verifierLevel)) {
            res.status(403).json({
              verified: false,
              documentId: id,
              error: `Verification requires ${verifierLevel.toUpperCase()} identity verification level. Your current level is ${userLevel.toUpperCase()}.`,
              code: 'INSUFFICIENT_VERIFICATION_LEVEL',
              requiredLevel: verifierLevel,
              currentLevel: userLevel,
            });
            return;
          }
        }
      }
    }

    const isRevoked = doc.status === 'revoked';
    const hashValid = contentHash ? contentHash === doc.contentHash : true;

    // Pen-test F-03 LIVE: query the anchoring service's chain-first
    // verifier with the content hash. If Blockfrost has the tx, we get
    // a real txHash + blockHeight back. If not, fall through to the
    // persisted state. Cached via the anchoring service (60s) so this
    // is cheap to call on every verify.
    const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
    let liveTxHash: string | null = null;
    let liveBlockHeight: number | null = null;
    let liveConfirmedAt: string | null = null;
    if (doc.contentHash) {
      try {
        // Forward the caller's bearer token — anchoring mounts global
        // authenticate() on /api/* so /api/anchors/verify/:hash returns
        // 500 "No token provided" without it. (Verify endpoint cosmetic
        // bug from BACKLOG: blockchainAnchored stayed false because this
        // call always failed.)
        const r = await fetch(`${anchoringBase}/api/anchors/verify/${doc.contentHash}`, {
          signal: AbortSignal.timeout(2_500),
          headers: authHeader ? { Authorization: authHeader } : {},
        });
        if (r.ok) {
          const j = await r.json() as any;
          // Anchoring returns a flat shape: { verified, txHash, blockNumber,
          // confirmedAt, ... }. Older code expected j.anchor.* (nested) which
          // never matched, so liveTxHash stayed null and the response always
          // fell through to the persisted document.blockchain stub.
          if (j.verified) {
            liveTxHash = j.txHash || j.transactionHash || (j.anchor && j.anchor.txHash) || null;
            const blockNum = j.blockNumber ?? j.blockHeight ?? (j.anchor && j.anchor.blockHeight);
            liveBlockHeight = blockNum != null ? Number(blockNum) : null;
            liveConfirmedAt = j.confirmedAt || j.anchoredAt || (j.anchor && j.anchor.confirmedAt) || null;
          }
        }
      } catch (_err) {
        // Network/timeout — fall through to persisted state. Verification
        // remains honest because we still report 'pending-onchain' rather
        // than fabricating.
      }
    }

    // Persisted state from originate's document record.
    const persistedTxHash = (doc as any).blockchain?.txHash ?? null;
    const persistedBlockHeight = (doc as any).blockchain?.blockHeight ?? null;
    const persistedConfidence = (doc as any).blockchain?.confidence;
    const persistedStatus = (doc as any).blockchain?.status ?? null;
    const persistedSimulated = (doc as any).blockchain?.simulated;

    // KS-1069: `persistedAnchored` below used to trust the SHAPE of these three
    // values — `persistedTxHash &&` and `persistedBlockHeight &&` were
    // truthiness tests, and `persistedSimulated !== true` was strict in the
    // unsafe direction. Measured before the change, each of these reported
    // on-chain with `verified: true`: a `tx_sim_`/`mock_tx_`/`tx_` placeholder
    // hash; a height of '0' (string), -1, 4242.5 or '4242' (string);
    // `simulated: 'true'` or `1`. The predicate now reads the three validated
    // booleans below; the echoed `blockchain.txHash` / `blockHeight` values are
    // NOT rewritten here (the claim is what this closes, not the presentation).
    //
    // Hash: a string that is not a KS-522 placeholder. Local mirror of the
    // rule anchoring applies at anchoring/src/index.ts:595 and originate at
    // its serve boundary (`presentBlockchainHonestly`, originate
    // routes/verification.ts:53 — another service, not importable here).
    const persistedTxHashIsReal =
      typeof persistedTxHash === 'string' &&
      persistedTxHash.length > 0 &&
      !/^(tx_sim_|mock_tx_|tx_)/.test(persistedTxHash);
    // Height: a positive integer, not merely truthy. Strict, not coerced (ruled
    // 2026-09-13): a numeric string reaching this read is a shape defect the
    // guard refuses. A string CAN reach it: originate's KS-584 heal path
    // (originate routes/verification.ts:338, written back by
    // `persistHealedAnchor` :359-366) carries anchoring's raw pg BIGINT
    // (anchoring/src/index.ts:622, `row?.block_number`). The root fix belongs
    // there (KS-1129), not in a coercion here. What a JSONB round-trip returns
    // is still unmeasured.
    // The `typeof … === 'number'` clause is documentation of intent, not a
    // live guard: `Number.isInteger` already refuses every non-number, so no
    // cell can redden that clause alone. Kept on purpose (KS-1130 P3).
    const persistedBlockHeightIsHeight =
      typeof persistedBlockHeight === 'number' &&
      Number.isInteger(persistedBlockHeight) &&
      persistedBlockHeight > 0;
    // Simulated: any truthy value is a declaration, not only boolean `true`.
    const persistedDeclaredSimulated = Boolean(persistedSimulated);

    // Live data wins when available; persisted is the fallback.
    const txHash = liveTxHash || persistedTxHash;
    const blockHeight = liveBlockHeight || persistedBlockHeight;

    // KS-1057: `confidence` used to be keyed on PRESENCE alone — `txHash &&
    // blockHeight`. That was safe only by accident: `status === 'anchor_failed'`
    // USED to imply `txHash === null`, and KS-1004 (#912) deliberately and
    // correctly retired that invariant so a failed transaction keeps its hash
    // as a forensic trail. A hash proves a transaction was BUILT, not that it
    // succeeded, so presence can no longer stand in for success.
    //
    // Live chain evidence is judged on its own and stays authoritative: a tx
    // observed in a block IS on chain whatever a stale persisted status says.
    // That is the whole point of the scan above and it must still be able to
    // heal a document whose blob went `anchor_failed` on a raced signal — so
    // this deliberately does NOT consult `persistedStatus`.
    const liveAnchored = Boolean(liveTxHash && liveBlockHeight);

    // Persisted evidence is only as good as the status stored beside it. This
    // mirrors originate's `isAnchoredHonestly` (services/originate/src/routes/
    // verification.ts): only `confirmed` earns the claim — 'submitted' means
    // the tx is in flight and may still fail, the KS-535 class — and a
    // declared-simulated blob never earns it (KS-522/587).
    //
    // `status == null` covers the statusless blob shape `{txHash, blockHeight,
    // anchoredAt}`. ⚠ It is NOT legacy-only — that wording was wrong when this
    // was written and it licensed exactly the future writer this guard worries
    // about. Producers, counted from source:
    //   * the four seeded demo documents (documentRepo.ts:790/818/846/886),
    //     including the canonical OpenAPI example (KS-481) — these are why the
    //     carve-out exists, and the cell below pins them;
    //   * the CURRENT retry route `POST /api/documents/:id/anchor`
    //     (originate routes/documents.ts:1313-1322), whose create-path sibling
    //     at :836 DOES write a status. It is inert today only because
    //     anchoring's 202 body carries neither a txHash nor a blockHeight —
    //     an accident of a response shape, not a guard.
    // This branch is fail-OPEN by construction: a writer that omits `status`
    // while setting a height is treated as on-chain, and it is the weakest part
    // of this predicate — narrowing it needs the statusless producers closed
    // first.
    //
    // ⚠ IT IS TIER 1 ONLY, and since KS-1073 the predicate enforces that: the
    // `_source !== 'anchor_store'` conjunct keeps a statusless tier-2 blob out
    // even if one were produced. An earlier version of this comment said the
    // tier-2 verifier path depends on the carve-out. That was true of the code
    // it was written against and the F1 fix in the same commit made it false: tier 2 now
    // synthesises its blob with `status: latest.status` (in
    // `makeFetchDocFromAnchorStore`) from anchoring's `formatAnchorResponse`,
    // which emits `status: anchor.status` unconditionally
    // (anchoring/src/index.ts:1596) over a column declared
    // `TEXT NOT NULL DEFAULT 'pending'` (migrations 001:714, 003:26). So a
    // tier-2 blob ALWAYS carries a status today and does not reach `== null`.
    // Measured before KS-1073 (#1002's QA gate, G4): deleting this carve-out
    // reddened exactly ONE cell — the tier-1 `REGRESSION: a legacy statusless
    // blob`. Its only producers are the two counted above, and both are tier 1.
    const persistedAnchored = Boolean(
      persistedTxHashIsReal &&           // KS-1069: was `persistedTxHash &&`
      persistedBlockHeightIsHeight &&    // KS-1069: was `persistedBlockHeight &&`
      !persistedDeclaredSimulated &&     // KS-1069: was `persistedSimulated !== true`
      (persistedStatus === 'confirmed' || (persistedStatus == null && (doc as any)._source !== 'anchor_store')), // KS-1073: carve-out tier-1 only; anchor-store rows are never statusless
    );

    // KS-1071: the in-flight decision is made HERE, once, for BOTH tiers —
    // a tier-2 blob arrives with `status` and no `confidence` of its own (see
    // makeFetchDocFromAnchorStore). Keyed on the persisted status through the
    // one exported mapping. Prior behaviour: this read only
    // `persistedConfidence === 'pending-onchain'`, a field originate's
    // status-writers never set (anchorStateSync.ts:212/247/348 write
    // `status: 'submitted'`/`'pending'`/`'confirmed'` and no `confidence`), so
    // a tier-1 blob in flight answered `off-chain-only` while the same anchor
    // via tier 2 answered `pending-onchain` (F8). The `persistedConfidence`
    // fallback stays, for STATUSLESS blobs only: originate writes
    // `{txHash: null, blockHeight: null, confidence: 'pending-onchain'}` with no
    // status key when anchoring is unavailable (routes/documents.ts:1367-1372)
    // and at certification create (routes/certifications.ts:463-469,
    // :1184-1191) — "the verifier UI must honour" it. A blob never carries
    // both, so the two arms cannot disagree. The mapping's `on-chain` is never
    // emitted from here: `persistedAnchored` above owns that claim.
    const confidence: 'on-chain' | 'pending-onchain' | 'off-chain-only' =
      liveAnchored || persistedAnchored
        ? 'on-chain'
        : confidenceForAnchorStatus(persistedStatus) === 'pending-onchain'
        ? 'pending-onchain'
        : persistedStatus == null && persistedConfidence === 'pending-onchain'
        ? 'pending-onchain'
        : 'off-chain-only';
    const blockchainAnchored = confidence === 'on-chain';

    res.json({
      verified: !isRevoked && hashValid && blockchainAnchored,
      documentId: id,
      certificationId: id,
      status: doc.status || 'anchored',
      revoked: isRevoked,
      checks: {
        exists: true,
        notRevoked: !isRevoked,
        hashValid,
        hasSignatures: true,
        blockchainAnchored,
      },
      issuer: {
        id: doc.owner?.id || 'test-issuer',
        verified: true,
      },
      blockchain: {
        anchored: blockchainAnchored,
        txHash,
        blockHeight,
        confidence,
        confirmedAt: liveConfirmedAt,
        source: liveTxHash ? 'cardano-live' : (persistedTxHash ? 'persisted' : 'none'),
      },
      verificationConfidence: confidence,
      requestedFields: requestedFields || [],
      purpose: purpose || 'verification',
      verifiedAt: new Date().toISOString(),
    });
  });

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
  // The /api/documents/:id/verify and /api/certifications/:id/verify mock
  // routes ABOVE this block remain — they implement test-only flows that
  // originate doesn't expose (verification-level enforcement, three-tier
  // lookup including anchor_store fallback).
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

        // The status line decides: originate persists the document before it writes a 2xx
        // (services/originate/src/routes/documents.ts), so a 2xx header means it exists.
        // The promise settles once; later resolveStatus calls are no-ops.
        const forwardStatus: number = await new Promise<number>((resolveStatus) => {
          const proxyReq = http.request(
            { hostname: url.hostname, port: url.port, path: url.pathname, method: 'POST', headers: forwardHeaders },
            (proxyRes: any) => {
              let body = '';
              proxyRes.on('data', (chunk: string) => { body += chunk; });
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
            log('error', 'Failed to forward approved document to originate', { error: err.message });
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
      let body: Record<string, unknown> = {};
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
        if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) {
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
        try {
          const sRaw = await redisService.getNotificationSettings('platform-settings');
          const sAll = (sRaw || {}) as Record<string, unknown>;
          const ints = ((sAll as any)?.integrations || []) as Array<Record<string, unknown>>;
          const found = ints.find((i: any) => i.id === connectorMeta.connectorId);
          if (found?.config) connectorConfig = found.config as Record<string, unknown>;
        } catch {}
        const allowedTypes = (connectorConfig.allowedDocumentTypes || []) as string[];
        if (allowedTypes.length > 0 && body.documentType && !allowedTypes.includes(body.documentType as string)) {
          res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: `Connector is not permitted to register document type "${body.documentType}"` } });
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
      } catch (err: any) {
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
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch document types' } });
    }
  });

  return router;
}
