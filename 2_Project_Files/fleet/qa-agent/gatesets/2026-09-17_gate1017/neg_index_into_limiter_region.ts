/**
 * =============================================================================
 * SECUURA API GATEWAY — Orchestration Layer
 * =============================================================================
 * Thin entry point that wires together extracted modules:
 *   config/services, middleware/auth, middleware/security, middleware/csrf,
 *   routes/proxy, routes/admin, routes/verification, routes/platform,
 *   routes/system-status, services/health, services/enforcement,
 *   services/tokenisation, services/redis, utils/logger, db
 * Port: 8080
 * =============================================================================
 */

import { stripTrustHeaders } from './utils/trustHeaders';
import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';
import swaggerUi from 'swagger-ui-express';
import { readFileSync, existsSync, watch as fsWatch } from 'fs';
import { parse as parseYaml } from 'yaml';
import { resolve as resolvePath } from 'path';

import { services, SECURITY_CONFIG, UserPayload } from './config/services';
import { configureAuth, authenticateToken, parseTestToken, verifyRs256 } from './middleware/auth';
import { createAuditMiddleware } from './middleware/audit';
import { normaliseRepeatedSlashes } from './middleware/normalisePath';
import {
  sanitizeInput,
  createDetectSuspiciousRequests,
  createBruteForceProtection,
  requestFingerprint,
} from './middleware/security';
import { csrfMiddleware, enforceJsonContentType } from './middleware';
import { createProxyRoutes } from './routes/proxy';
import { createAdminRoutes } from './routes/admin';
import { createVerificationRoutes } from './routes/verification';
import { createPlatformRoutes } from './routes/platform';
import systemStatusRouter from './routes/system-status';
import healthDashboardRouter from './routes/health-dashboard';
import { versioningMiddleware } from './routes/versioning';
import batchRouter from './routes/batch';
import notificationsRouter from './routes/notifications';
import auditExportRouter from './routes/audit-export';
import { createHealthRoutes } from './services/health';
import { enforceDocumentTypeRules, createWorkflowInstanceIfRequired, meetsVerificationLevel } from './services/enforcement';
import { setTenantKey, getTenantKey, removeTenantKey } from './services/tokenisation';
import * as redisService from './services/redis';
import { logger as winstonLogger, validateEnv } from './utils/logger';
import { errorHandler, payloadTooLargeErrorHandler } from './middleware/errorHandler';
import { initDb, query, isDbAvailable } from './db';
import { buildSpecMethodMap, resolveSpecRoute } from './specRouteMap';
import { initErrorTracking, errorTrackingMiddleware, enforceProductionConfig, rejectNulBytes, resolveUnhandledRejectionMode, createUnhandledRejectionHandler } from '@secuura/shared';

dotenv.config();

// =============================================================================
// ENVIRONMENT VALIDATION
// =============================================================================

validateEnv();

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('api-gateway', {
  requiredEnvVars: ['DATABASE_URL', 'REDIS_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

// AUDIT B-4 + D-11: refuse to boot with auth-bypass / mock endpoints in any
// production-equivalent environment. Belt-and-braces: the existing
// ENABLE_MOCK_ENDPOINTS gate at line 572 is `NODE_ENV !== 'production' && ...`
// (correct) and ENABLE_TEST_TOKENS feeds parseTestToken which itself env-gates,
// but a misconfigured deploy that flips the flag to true would still log a
// warning and proceed. Make it FATAL.
{
  const env = process.env.NODE_ENV || 'development';
  const isProdLike = env === 'production' || env === 'staging' || env === 'demo';
  const testTokens = process.env.ENABLE_TEST_TOKENS === 'true';
  const mockEndpoints = process.env.ENABLE_MOCK_ENDPOINTS === 'true';
  if (isProdLike && (testTokens || mockEndpoints)) {
    console.error(
      `FATAL: NODE_ENV=${env} but ENABLE_TEST_TOKENS=${testTokens} ` +
      `ENABLE_MOCK_ENDPOINTS=${mockEndpoints}. Auth-bypass / mock endpoints ` +
      `MUST NOT be enabled in production-like environments.`
    );
    process.exit(1);
  }

  // AUDIT B-12: DATABASE_URL must not contain the documented dev-default
  // password in any production-like env. The `secuura_dev_password` literal
  // is only acceptable on a local docker-compose stack.
  const dbUrl = process.env.DATABASE_URL || '';
  if (isProdLike && dbUrl.includes('secuura_dev_password')) {
    console.error(`FATAL: DATABASE_URL contains the dev-default password 'secuura_dev_password' in NODE_ENV=${env}. Rotate via Key Vault.`);
    process.exit(1);
  }
}

// Initialise centralized error tracking (Sentry when SENTRY_DSN is set, structured JSON otherwise)
initErrorTracking('api-gateway');

const app = express();
const PORT = process.env.PORT || 8080;
app.set('trust proxy', 1);

const NODE_ENV = process.env.NODE_ENV || 'development';

// =============================================================================
// TYPE DECLARATIONS
// =============================================================================

declare global {
  namespace Express {
    interface Request {
      user?: UserPayload;
      requestId?: string;
    }
  }
}

// =============================================================================
// IN-MEMORY STORES & DB PERSISTENCE HELPERS
// =============================================================================

interface RejectionData {
  status: string;
  rejectionReason: string;
  rejectedAt: string;
  rejectedBy: string;
}

interface SignatureData {
  walletAddress: string;
  signature: string;
  nonce: string;
  signedAt: string;
}

const memWorkflowToDocumentMap = new Map<string, string>();
const memRejectedDocuments = new Map<string, RejectionData>();
const memDocumentSignatures = new Map<string, SignatureData>();

async function dbSaveRejection(docId: string, data: RejectionData): Promise<void> {
  // Write to Redis (also updates its internal in-memory fallback)
  try {
    await redisService.setRejectedDocument(docId, {
      status: data.status,
      rejectionReason: data.rejectionReason,
      rejectedAt: data.rejectedAt,
      rejectedBy: data.rejectedBy,
    });
  } catch { /* Redis write failed — in-memory fallback handled by redis service */ }

  // Keep gateway-level in-memory map as last-resort fallback
  memRejectedDocuments.set(docId, data);

  if (!isDbAvailable()) return;
  try {
    await query(
      `INSERT INTO svc_gateway_rejections (document_id, rejected_by, reason)
       VALUES ($1, $2, $3) ON CONFLICT (document_id) DO UPDATE SET rejected_by = EXCLUDED.rejected_by, reason = EXCLUDED.reason`,
      [docId, data.rejectedBy || 'unknown', data.rejectionReason || '']
    );
  } catch { /* fallback to in-memory */ }
}

async function loadFromDb(): Promise<void> {
  if (!isDbAvailable()) return;
  try {
    const wfRows = await query<{ document_id: string; workflow_id: string }>('SELECT document_id, workflow_id FROM svc_gateway_workflows');
    for (const r of wfRows.rows) {
      memWorkflowToDocumentMap.set(r.document_id, r.workflow_id);
      // Populate Redis from DB (fire-and-forget, errors are non-fatal)
      redisService.setWorkflowDocumentMapping(r.document_id, r.workflow_id).catch(() => {});
    }

    const rejRows = await query<{ document_id: string; reason: string; rejected_by: string }>('SELECT document_id, reason, rejected_by FROM svc_gateway_rejections');
    for (const r of rejRows.rows) {
      const rejData = { status: 'rejected', rejectionReason: r.reason, rejectedBy: r.rejected_by, rejectedAt: '' };
      memRejectedDocuments.set(r.document_id, rejData);
      redisService.setRejectedDocument(r.document_id, rejData).catch(() => {});
    }

    const sigRows = await query<{ document_id: string; wallet_address: string; signature: string }>('SELECT document_id, wallet_address, signature FROM svc_gateway_signatures');
    for (const r of sigRows.rows) {
      const sigData = { walletAddress: r.wallet_address, signature: r.signature, nonce: '', signedAt: '' };
      memDocumentSignatures.set(r.document_id, sigData);
      redisService.setDocumentSignature(r.document_id, sigData).catch(() => {});
    }

    log('info', 'Loaded gateway data from DB and populated Redis cache', { workflows: memWorkflowToDocumentMap.size, rejections: memRejectedDocuments.size, signatures: memDocumentSignatures.size });
  } catch (err: any) {
    log('warn', 'Failed to load gateway data from DB — starting empty', { error: err?.message });
  }
}

// =============================================================================
// LOGGING HELPERS
// =============================================================================

function log(level: 'info' | 'warn' | 'error', message: string, meta?: object) {
  winstonLogger.log(level, message, meta);
}

// =============================================================================
// CONFIGURE AUTH MODULE
// =============================================================================

configureAuth({
  enableTestTokens: process.env.ENABLE_TEST_TOKENS === 'true',
  defaultTenantId: process.env.DEFAULT_TENANT_ID || 'a0000000-0000-4000-8000-000000000001',
  securityServiceUrl: services.security?.url || 'http://localhost:6008',
  // KS-480: connector token exchange endpoint host (auth service)
  authServiceUrl: services.auth?.url || 'http://localhost:6003',
});

// =============================================================================
// MIDDLEWARE CHAIN
// =============================================================================

// KS-858 (carrying pen-test F5 / KS-946): collapse repeated `/` on the PATH,
// once, before ANY predicate — limiter mounts, scope gates, auth predicates and
// the proxy mounts alike. A route spelled `/api/auth//verify-email` missed all
// eight path-scoped rate limiters while the proxy still served the canonical
// handler; `/api/gdpr//erasures` did the same to a scope gate (KS-843, closed
// then by a `/api/gdpr`-scoped collapse that deferred the class here by name).
//
// MUST be unscoped and MUST be first. Measured against this repo's express
// 4.22.2: `app.use('/api', fn)` does not run for `//api/auth/login`, so a
// path-scoped normaliser is walked around by the same trick it exists to stop.
// Anything mounted above this line does not see canonical paths.
app.use(normaliseRepeatedSlashes());

// Helmet
// KS-245 (F-CSP-CLOUD-01): the gateway now sets its own CSP. It was previously
// disabled (Pen-test L9) on the assumption that the nginx-gateway in front is the
// authoritative CSP layer — true on local, but Dev/Demo Container Apps expose
// api-gateway directly with NO nginx in front, so no CSP was applied on cloud at
// all. The gateway serves mostly JSON plus two self-contained HTML pages
// (docs/extension-login.html — inline <script> + onclick; docs/developer-portal.html
// — inline <style>) and Swagger UI (/api/docs, same-origin bundle + inline styles),
// none of which load external resources — so 'unsafe-inline' for script/style (which
// the inline handlers + Swagger need) with everything else locked to 'self' fits all
// of them while still enforcing the meaningful directives (object-src 'none',
// base-uri 'self', frame-ancestors 'none' — matching the X-Frame-Options: DENY below,
// default-src 'self'). On local this layers with nginx's CSP on those two docs pages
// (browser enforces the intersection — harmless); picking a single authoritative CSP
// layer, and tightening these pages to nonces so 'unsafe-inline' can be dropped, are
// follow-ups. crossOriginResourcePolicy stays cross-origin for the public verify routes.
app.use(helmet({
  contentSecurityPolicy: {
    useDefaults: false,
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:'],
      fontSrc: ["'self'", 'data:'],
      connectSrc: ["'self'"],
      objectSrc: ["'none'"],
      baseUri: ["'self'"],
      frameAncestors: ["'none'"],
      formAction: ["'self'"],
    },
  },
  crossOriginResourcePolicy: { policy: 'cross-origin' },
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
}));

// Additional security headers
app.use((_req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
  res.removeHeader('X-Powered-By');
  next();
});

// HTTP method allowlist — KS-3 DRIFT-METHOD-405 fix.
// Without this, schemathesis (and any other unsupported-method probe) sees
// `TRACE` / `CONNECT` / arbitrary verbs proxied through to backend services,
// which reject them after the round-trip and the gateway returns 502 Bad
// Gateway instead of the documented 405 Method Not Allowed. This middleware
// rejects unsupported methods at the edge with a typed ErrorResponse + Allow
// header, before any proxy / auth / rate-limit processing.
const ALLOWED_HTTP_METHODS = new Set(['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']);
app.use((req: Request, res: Response, next: NextFunction) => {
  if (!ALLOWED_HTTP_METHODS.has(req.method.toUpperCase())) {
    res.set('Allow', [...ALLOWED_HTTP_METHODS].join(', '));
    res.status(405).json({
      success: false,
      error: {
        code: 'METHOD_NOT_ALLOWED',
        message: `HTTP method "${req.method}" is not supported by this API. ` +
                 `Allowed: ${[...ALLOWED_HTTP_METHODS].join(', ')}.`,
      },
    });
    return;
  }
  next();
});

// Strip identity / authorization-trust headers that the gateway is meant to
// SET based on a verified JWT — never to RECEIVE from clients. Without this
// strip, any caller can spoof their identity, tenant, organization, or role
// by sending the header (audit finding A-01, the keystone vulnerability that
// unblocks A-06, A-08, A-09 trivially). Applies to ALL inbound requests
// before any auth, CORS, or proxy logic runs.
//
// EXCEPTION: x-tenant-override is intentional super-admin functionality (the
// admin portal's tenant selector). It's a *request* — the auth middleware
// decides whether to honour it based on the verified JWT's role. The
// blanket strip pattern (added 2026-04-25 commit c796138f0) was matching
// it too, which broke the override path silently for two weeks (2026-04-25
// through 2026-05-09) and made KS-4 (BUG-ISOLATION-001) untestable. Auth
// middleware enforces SUPER_ADMIN_ROLES gating before honouring the value
// (services/api-gateway/src/middleware/auth.ts:380-382, the
// `SUPER_ADMIN_ROLES.includes(decoded.role)` check inside the post-jwt.verify
// block — grep that expression if the line moves), so letting it pass through
// the edge strip is safe.
app.use((req, _res, next) => {
  // The pattern, the allow-list and the reasons all live in
  // utils/trustHeaders.ts so the strip is testable against the real thing
  // rather than a re-declared copy. Applies to ALL inbound requests before any
  // auth, CORS, or proxy logic runs.
  stripTrustHeaders(req.headers as unknown as Record<string, unknown>);
  next();
});

// BUG-PLATFORM-AUTH-001 (2026-05-01): capture the raw Authorization header
// at request entry, BEFORE any other middleware can mutate or consume
// req.headers.authorization. Some downstream proxy paths (e.g.
// routes/platform.ts → tenant-provisioning) need to forward the original
// bearer token to internal services that JWT-verify directly. Symptom
// before this fix: GET /api/platform/tenants returned 502 because the
// inline proxy's `req.headers.authorization` read was empty by the time
// the handler ran, and tenant-prov returned `Error: No token provided`,
// which gateway's `r.json()` then failed to parse (HTML stack trace),
// producing an unhelpful 502.
app.use((req, _res, next) => {
  if (req.headers.authorization) {
    (req as any).rawAuthorization = req.headers.authorization;
  }
  next();
});

// AUDIT B-7 / D-2: refuse to start with wildcard origin in production-like
// environments. With credentials:true, `*` is spec-illegal AND a CSRF
// refresh-token exfil risk. Same rule for any wildcard-subdomain entry.
{
  const env = process.env.NODE_ENV || 'development';
  const isProdLike = env === 'production' || env === 'staging' || env === 'demo';
  const raw = process.env.CORS_ORIGINS;
  if (isProdLike && raw) {
    const origins = raw.split(',').map((s) => s.trim());
    const bad = origins.filter((o) => o === '*' || o.includes('//*.') || o.endsWith('://*'));
    if (bad.length > 0) {
      console.error(`FATAL: CORS_ORIGINS contains wildcard origin(s) ${JSON.stringify(bad)} in NODE_ENV=${env}. Replace with explicit allowlist.`);
      process.exit(1);
    }
  }
}

// CORS
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || [
    'http://localhost:6100', 'http://localhost:6101', 'http://localhost:6102',
    'http://localhost:6103', 'http://localhost:6882', 'http://localhost:6881',
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID', 'X-Api-Key', 'X-CSRF-Token'],
}));

// Cookie parsing & CSRF
app.use(cookieParser());
// Pen-test F-14 fix: enable CSRF in every environment except `test` (where
// the test runner needs to hit endpoints without juggling tokens). The
// previous gate of `NODE_ENV === 'production'` left dev / staging / demo
// without CSRF protection — and demo carries seeded credentials (F-05) +
// public URLs, so it absolutely needs CSRF.
if (NODE_ENV !== 'test') {
  app.use(csrfMiddleware.generateToken);
  app.use(csrfMiddleware.protect);
}

// KS-439: strict media-type enforcement — an /api/* request carrying a body
// must declare application/json (sole exception: the OAuth token endpoint's
// RFC 6749 form encoding). Mounted before the parsers AND the proxies so one
// choke point covers gateway-parsed and proxied paths alike; after CSRF so
// ambient-authority requests keep failing 403 first (auth posture).
app.use(enforceJsonContentType);

// Conditional body parsing — skip for proxied routes (they need raw body stream)
const proxyPaths = [
  '/api/credentials', '/api/status', '/api/presentations',
  '/api/auth', '/api/oauth', '/api/webhooks', '/api/documents', '/api/certifications',
  '/api/anchoring', '/api/prism', '/api/timestamp',
  '/api/wallet', '/api/security', '/api/m365',
  '/api/staking', '/api/referral', '/api/governance',
  '/api/analytics', '/api/billing', '/api/transfers',
  '/api/delegations', '/api/kyc',
  '/api/gdpr', '/api/verification', '/api/v2/verification', '/api/nft', '/webhooks',
  '/api/admin', '/api/signatories', '/api/system-errors',
  '/api/onedrive', '/api/teams',
  '/api/users', '/api/sessions', '/api/issuer-certs',
];
const shouldParseBody = (req: Request): boolean => !proxyPaths.some(p => req.path.startsWith(p));

// Default 1MB body limit; file upload routes get 10MB via their own middleware
app.use((req, res, next) => { if (shouldParseBody(req)) express.json({ limit: '1mb' })(req, res, next); else next(); });
app.use((req, res, next) => { if (shouldParseBody(req)) express.urlencoded({ extended: true, limit: '1mb' })(req, res, next); else next(); });

// 10MB limit for file upload paths
const uploadBodyParser = express.json({ limit: '10mb' });
app.use('/api/documents/upload', uploadBodyParser);
app.use('/api/nft/upload', uploadBodyParser);

// KS-471: no U+0000 may pass the boundary on any gateway-parsed body (raw-500 /
// persist class). No-op when req.body is unset, so mounting unconditionally
// after all parsers is safe.
//
// KS-818 F-06 — this comment used to say "proxied paths stream raw and are
// guarded by the same middleware inside each target service", full stop. True
// of paths that genuinely proxy, and FALSE of the gateway's own routes that
// sit on a `proxyPaths` prefix: `POST /api/documents/:id/verify` and
// `POST /api/certifications/:id/verify` have NO target service — they are
// answered here, by `verification.ts`. One sentence described the proxied case
// and quietly covered the non-proxied one, which is why KS-815 had to guard
// those two routes at their own mount rather than relying on this line.
//
// KS-833 Q-5 — and those two routes are an EXAMPLE, not the set. The paragraph
// above used to read as though `verification.ts` were the whole of the
// non-proxied case. It is not: `routes/admin.ts` carries its own mount-level
// guard for the same reason, covering the majority of the nineteen routes it
// mounts. The count lives in that file's own comment and is deliberately not
// repeated here — two copies of a number is how the claim above drifted in the
// first place.
//
// So, precisely, as a CLASS rather than a list:
//   · a path that PROXIES        — streams raw; the guard runs in the target service
//   · a path the GATEWAY answers — guarded HERE, either by this mount (when the
//     body was parsed above) or, for any router that parses its own body on a
//     `proxyPaths` prefix, at that router's own mount (KS-815). Today that is
//     `verification.ts` and `admin.ts`; a third such router would need the same
//     treatment, and nothing in this file would tell you so.
app.use(rejectNulBytes());

// Security middleware (only on parsed bodies)
const detectSuspiciousRequests = createDetectSuspiciousRequests(SECURITY_CONFIG);
const bruteForceProtection = createBruteForceProtection(SECURITY_CONFIG);

app.use((req, res, next) => { if (shouldParseBody(req)) sanitizeInput(req, res, next); else next(); });
app.use((req, res, next) => { if (shouldParseBody(req)) detectSuspiciousRequests(req, res, next); else next(); });
app.use(requestFingerprint);
app.use(bruteForceProtection);

// Request ID
app.use((req: Request, res, next) => {
  const requestId = req.headers['x-request-id'] as string || `req_${require('crypto').randomUUID()}`;
  req.requestId = requestId;
  res.setHeader('X-Request-ID', requestId);
  next();
});

// Request logging
app.use((req: Request, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    log('info', 'Request completed', {
      requestId: req.requestId, method: req.method, path: req.path,
      statusCode: res.statusCode, duration: `${Date.now() - start}ms`,
      ip: req.ip, userAgent: req.get('user-agent'),
    });
  });
  next();
});

// Global rate limiter — scoped: read-only and public endpoints exempt.
// Skip rules live in middleware/rateLimitSkip.ts so they're unit-testable
// without booting the server (pen-test C1 fix).
import { shouldSkipGlobalRateLimit } from './middleware/rateLimitSkip';
const isNonProd = ['development', 'dev', 'demo', 'test', 'staging'].includes(NODE_ENV);

app.use(rateLimit({
  windowMs: 60 * 1000,
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || (isNonProd ? '10000' : '301'), 10),
  message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many requests, please try again later.' } },
  standardHeaders: true,
  legacyHeaders: false,
  skip: (req) => shouldSkipGlobalRateLimit({
    authHeader: (req.headers.authorization as string) || '',
    path: req.path,
    nodeEnv: NODE_ENV,
    disableEnv: process.env.DISABLE_RATE_LIMIT,
  }),
}));

// Pen-test M2 fix: /api/verification/* is exempt from the GLOBAL limiter
// because it's an unauthenticated public endpoint, but it still needs a
// limit. Without this an attacker could mass-verify documents to enumerate
// hashes or DoS the verification index. Per-IP, looser than the global
// limit but still bounded.
app.use(
  // KS-584 P3: the v2 verify-list contract is the same public surface —
  // same per-IP bound.
  ['/api/verification', '/api/v2/verification'],
  rateLimit({
    windowMs: 60 * 1000,
    max: parseInt(process.env.VERIFICATION_RATE_LIMIT_MAX || (isNonProd ? '600' : '60'), 10),
    message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many verification requests, slow down.' } },
    standardHeaders: true,
    legacyHeaders: false,
  }),
);

// Per-client rate limit enforcement (API keys + OAuth apps)
import { enforceClientRateLimit } from './middleware/rateLimitEnforce';
app.use(enforceClientRateLimit());

// =============================================================================
// API VERSIONING
// =============================================================================

app.use(versioningMiddleware());

const API_VERSION = 'v1';
// KS-584 P3: v2 currently carries only the verify-list contract
// (/api/v2/verification/*); v1 remains the default for everything else.
const SUPPORTED_VERSIONS = ['v1', 'v2'];

app.use((req: Request, res, next) => {
  const versionMatch = req.path.match(/^\/api\/(v\d+)\//);
  if (versionMatch) {
    const version = versionMatch[1];
    if (!SUPPORTED_VERSIONS.includes(version)) {
      res.status(400).json({
        success: false,
        error: {
          code: 'BAD_REQUEST',
          message: `Version '${version}' is not supported. Supported versions: ${SUPPORTED_VERSIONS.join(', ')}`,
          details: { currentVersion: API_VERSION },
        },
      });
      return;
    }
    (req as any).apiVersion = version;
  } else {
    (req as any).apiVersion = API_VERSION;
  }
  res.setHeader('X-API-Version', (req as any).apiVersion);
  res.setHeader('X-API-Supported-Versions', SUPPORTED_VERSIONS.join(', '));
  next();
});

app.use((req, _res, next) => {
  if (req.path.startsWith('/api/v1/')) req.url = req.url.replace('/api/v1/', '/api/');
  next();
});

// BACKLOG H1: audit-log middleware. Captures business events with actor
// identity. Wired AFTER api-version stripping (so audit `action` derives
// from canonical paths) and BEFORE route handlers (so res.on('finish') and
// res.json wrapping take effect).
app.use(createAuditMiddleware({
  query: query as unknown as (sql: string, params: unknown[]) => Promise<{ rows: any[] }>,
  isDbAvailable,
  log,
}));

// =============================================================================
// API DOCUMENTATION
// =============================================================================

const specPath = existsSync(resolvePath(__dirname, '../docs/openapi/secuura-api.yaml'))
  ? resolvePath(__dirname, '../docs/openapi/secuura-api.yaml')
  : resolvePath(__dirname, '../../../docs/openapi/secuura-api.yaml');

// ONE source of truth for every spec surface (KS-656). Both /api/docs routes
// serve from these two variables — never from a per-request disk read.
//
// The bug this replaces: `.json` served a boot-parsed object while `.yaml` did
// a fresh readFileSync on every request. When `generate-openapi` rewrote the
// file, the container's single-file bind-mount was left pointing at an inode
// that no longer existed — so `.yaml` returned 500 ENOENT while `.json` kept
// confidently serving the boot copy. The obvious check passed while its twin
// was down, which is exactly why it went unnoticed. Reading both from memory
// makes the failure mode "stale but CONSISTENT" instead of "half dead".
let openApiSpecRaw = readFileSync(specPath, 'utf8');
let openApiSpec = parseYaml(openApiSpecRaw);

// Spec-aware method allow-list (built in ./specRouteMap). Lets the gateway
// reject e.g. `PUT /api/governance/state` with 405 at the edge instead of
// proxying an unsupported method to a backend that 5xxs (KS-3
// DRIFT-METHOD-405-EXPANSION). `resolveSpecRoute` unions methods across spec
// paths that collapse to the same regex (KS-118).
let specMethodMap = buildSpecMethodMap(openApiSpec);

// Dev-only hot-reload: re-parse the spec when generate-openapi rewrites it
// so /api/docs picks up new routes without a gateway restart. Production
// stays static — no fs.watch surface, no per-request regeneration.
//
// ⚠ WHETHER THIS FIRES DEPENDS ON HOW THE SPEC IS WRITTEN (KS-659). The spec
// reaches the container as a SINGLE-FILE bind mount, so `/app/docs/openapi/` is
// the image's directory and only the one file inside it is bound. That splits
// the behaviour in two, and the split is the whole point — measured by Peter on
// 2026-08-31 on `node:22-alpine` with this mount shape, and corrected here:
//
//   - IN-PLACE rewrite (truncate + write the SAME inode): the FILE watch FIRES
//     and the container reads the new content. A directory watch scores zero.
//   - REPLACEMENT (`mv`, `rsync`): neither watch fires and the mountpoint's
//     inode is dead — the file reads ENOENT from inside, while `test -f` on the
//     host still says PRESENT. This is the 2026-08-17 measurement, and it is
//     real; it is just not the local-regeneration path.
//
// Local regeneration is IN-PLACE: `scripts/generate-openapi.ts:273` is a bare
// `fs.writeFileSync(OUT_PATH, …)` with no temp-file-and-rename, and it is the
// only writer of `docs/openapi/secuura-api.yaml` in the tree (the only other
// references are docstring examples in a Python test). So for
// `npm run generate-openapi` — the case this hot-reload exists for — the FILE
// watch is the one that works, and the directory watch is the one that does not.
//
// That is why the directory watch (KS-656) is reverted here rather than kept:
// not "both are equally dead", but the file watch observes the only write
// pattern the repo actually produces. A spec delivered by replacement — rsync
// to a VM, an image rebuild — still needs `docker compose restart api-gateway`.
// KS-659 tracks making the reload real. What is NOT affected is the docs
// surface staying up — both routes serve the in-memory copy above, so a dead
// mount now means "stale but consistent" rather than a 500 on one of them.
if (process.env.NODE_ENV !== 'production') {
  let reloadTimer: NodeJS.Timeout | null = null;
  fsWatch(specPath, { persistent: false }, () => {
    // Debounce — editors/generators often emit several events for one save.
    if (reloadTimer) clearTimeout(reloadTimer);
    reloadTimer = setTimeout(() => {
      try {
        const nextRaw = readFileSync(specPath, 'utf8');
        const nextSpec = parseYaml(nextRaw);
        const nextMap = buildSpecMethodMap(nextSpec);
        // Assign only after all three succeed, so a half-written file can
        // never leave raw and parsed disagreeing with each other.
        openApiSpecRaw = nextRaw;
        openApiSpec = nextSpec;
        specMethodMap = nextMap;
        log('info', 'OpenAPI spec hot-reloaded', {
          path: specPath,
          mappedRoutes: specMethodMap.length,
        });
      } catch (err) {
        log('error', 'OpenAPI spec hot-reload failed (keeping previous spec)', {
          err: (err as Error).message,
        });
      }
    }, 200);
  });
}

// Public exposure of API documentation is opt-in only. The Swagger UI + the
// raw OpenAPI spec advertise 342 endpoints, every parameter, and every
// authentication mechanism — that's a free attack-surface map for anyone
// (audit F-04). Set ENABLE_PUBLIC_API_DOCS=true on the dev portal Container
// App ONLY when actively developing against the docs; never in demo/prod.
const PUBLIC_API_DOCS_ENABLED = process.env.ENABLE_PUBLIC_API_DOCS === 'true';
const apiDocsGuard = (_req: Request, res: Response, next: () => void) => {
  if (PUBLIC_API_DOCS_ENABLED) return next();
  res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Not found' } });
};

app.get('/api/docs/openapi.json', apiDocsGuard, (_req: Request, res: Response) => { res.json(openApiSpec); });
// Raw YAML twin of the .json route above (same guard). Registered before the
// /api/docs UI mount below — the swaggerUi.setup handler answers every subpath
// with HTML, so a route added after it would be unreachable.
//
// Serves the in-memory copy captured alongside the parsed one (KS-656) — NOT a
// per-request disk read. The two routes are the same spec by construction, so
// they cannot disagree about what the gateway publishes.
app.get('/api/docs/openapi.yaml', apiDocsGuard, (_req: Request, res: Response) => {
  res.type('text/yaml').send(openApiSpecRaw);
});

// Connector downloads — static files
app.get('/api/downloads/secuura-verify.oxt', (_req: Request, res: Response) => {
  // Try multiple paths — dist/downloads in Docker, ../downloads in dev
  const paths = [
    resolvePath(__dirname, '..', 'downloads', 'secuura-verify.oxt'),
    resolvePath(__dirname, 'downloads', 'secuura-verify.oxt'),
    resolvePath(process.cwd(), 'downloads', 'secuura-verify.oxt'),
  ];
  const oxtPath = paths.find(p => existsSync(p)) || paths[0];
  if (existsSync(oxtPath)) {
    res.setHeader('Content-Disposition', 'attachment; filename="secuura-verify.oxt"');
    res.setHeader('Content-Type', 'application/octet-stream');
    res.sendFile(oxtPath);
  } else {
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Extension not found. Coming soon.' } });
  }
});

app.get('/api/downloads/Secuura-Verify.dmg', (_req: Request, res: Response) => {
  const paths = [
    resolvePath(__dirname, '..', 'downloads', 'Secuura-Verify.dmg'),
    resolvePath(__dirname, 'downloads', 'Secuura-Verify.dmg'),
    resolvePath(process.cwd(), 'downloads', 'Secuura-Verify.dmg'),
  ];
  const dmgPath = paths.find(p => existsSync(p)) || paths[0];
  if (existsSync(dmgPath)) {
    res.setHeader('Content-Disposition', 'attachment; filename="Secuura-Verify.dmg"');
    res.setHeader('Content-Type', 'application/x-apple-diskimage');
    res.sendFile(dmgPath);
  } else {
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Mac installer not found. Coming soon.' } });
  }
});

app.get('/api/downloads/Secuura-Verify-Setup.exe', (_req: Request, res: Response) => {
  const paths = [
    resolvePath(__dirname, '..', 'downloads', 'Secuura-Verify-Setup.exe'),
    resolvePath(__dirname, 'downloads', 'Secuura-Verify-Setup.exe'),
    resolvePath(process.cwd(), 'downloads', 'Secuura-Verify-Setup.exe'),
  ];
  const exePath = paths.find(p => existsSync(p)) || paths[0];
  if (existsSync(exePath)) {
    res.setHeader('Content-Disposition', 'attachment; filename="Secuura-Verify-Setup.exe"');
    res.setHeader('Content-Type', 'application/x-msdownload');
    res.sendFile(exePath);
  } else {
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Windows installer not found. Coming soon.' } });
  }
});

app.get('/api/downloads/secuura-verify.plugin', (_req: Request, res: Response) => {
  const paths = [
    resolvePath(__dirname, '..', 'downloads', 'secuura-verify.plugin'),
    resolvePath(__dirname, 'downloads', 'secuura-verify.plugin'),
    resolvePath(process.cwd(), 'downloads', 'secuura-verify.plugin'),
  ];
  const pluginPath = paths.find(p => existsSync(p)) || paths[0];
  if (existsSync(pluginPath)) {
    res.setHeader('Content-Disposition', 'attachment; filename="secuura-verify.plugin"');
    res.setHeader('Content-Type', 'application/octet-stream');
    res.sendFile(pluginPath);
  } else {
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Euro-Office plugin not found. Coming soon.' } });
  }
});

// Extension login page — browser-based auth for LibreOffice/desktop extensions
app.get('/api/auth/extension-login', (_req: Request, res: Response) => {
  const loginPath = resolvePath(__dirname, 'docs', 'extension-login.html');
  if (existsSync(loginPath)) {
    res.sendFile(loginPath);
  } else {
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Extension login page not found' } });
  }
});

// Developer portal — served as a static HTML page
app.get('/developers', (_req: Request, res: Response) => {
  const portalPath = resolvePath(__dirname, 'docs', 'developer-portal.html');
  if (existsSync(portalPath)) {
    res.sendFile(portalPath);
  } else {
    res.redirect('/api/docs');
  }
});

const swaggerUiOpts = {
  customCss: `.swagger-ui .topbar { display: none } .swagger-ui .info .title { color: #1976d2 } .swagger-ui .scheme-container { background: #fafafa; padding: 15px }`,
  customSiteTitle: 'Secuura API Documentation',
  customfavIcon: '/favicon.ico',
  swaggerOptions: { persistAuthorization: true, docExpansion: 'list', filter: true, showExtensions: true, showCommonExtensions: true, tryItOutEnabled: true },
};

if (process.env.NODE_ENV === 'production') {
  // Static mount — spec captured at boot. Fastest path, no hot-reload.
  app.use('/api/docs', apiDocsGuard, swaggerUi.serve, swaggerUi.setup(openApiSpec, swaggerUiOpts));
} else {
  // Dynamic mount — re-renders HTML per request from the (possibly
  // hot-reloaded) spec, so re-running `npm run generate-openapi` is
  // immediately visible at /api/docs without a gateway restart.
  app.use('/api/docs', apiDocsGuard, swaggerUi.serve, (_req: Request, res: Response) => {
    res.send(swaggerUi.generateHTML(openApiSpec, swaggerUiOpts));
  });
}

app.use('/system', systemStatusRouter);
app.use('/api/system/health', healthDashboardRouter);
// Frontends reach the gateway only through their nginx `/api` proxy, so the
// admin dashboard's `/api/system/status` call never resolved against the bare
// `/system` mount above (→ 404). Mount the same router under `/api/system` too.
// Registered AFTER `/api/system/health` so the more-specific health router wins
// `/api/system/health/*`; system-status only handles `/status` + `/status/simple`.
app.use('/api/system', systemStatusRouter);
app.use('/api/batch', batchRouter);
app.use('/api/notifications', notificationsRouter);
app.use('/api/admin/audit', auditExportRouter);

app.get(['/api', '/api/v1'], (_req: Request, res: Response) => {
  res.json({
    name: 'Secuura API Gateway', version: '1.0.0', apiVersion: API_VERSION,
    supportedVersions: SUPPORTED_VERSIONS,
    description: 'Central API gateway for the Secuura document authenticity platform',
    documentation: '/api/docs', openApiSpec: '/api/docs/openapi.json',
    endpoints: {
      gateway: { 'GET /health': 'Gateway health check', 'GET /health/services': 'All services health check', 'GET /api': 'API documentation', 'GET /api/docs': 'Swagger UI interactive documentation', 'GET /api/docs/openapi.json': 'OpenAPI 3.0 specification' },
      certifications: { 'POST /api/certifications/issue': 'Issue verifiable certification', 'GET /api/certifications': 'List certifications', 'GET /api/certifications/:id': 'Get certification by ID', 'POST /api/certifications/:id/revoke': 'Revoke certification' },
      auth: { 'POST /api/auth/register': 'Register new user', 'POST /api/auth/login': 'Login with credentials', 'POST /api/auth/logout': 'Logout (requires auth)', 'POST /api/auth/refresh': 'Refresh access token', 'GET /api/users/me': 'Get current user profile' },
      documents: { 'POST /api/documents': 'Create document (requires auth)', 'GET /api/documents': 'List documents (requires auth)', 'GET /api/documents/:id': 'Get document by ID (requires auth)', 'POST /api/documents/:id/verify': 'Verify document' },
      kyc: { 'POST /api/kyc/microsoft/start': 'Start KYC verification', 'GET /api/kyc/microsoft/session/:id': 'Get KYC session status', 'GET /api/kyc/microsoft/result/:id': 'Get KYC verification result' },
      governance: { 'GET /api/governance/state': 'Get governance state', 'POST /api/governance/proposals': 'Create proposal', 'GET /api/governance/proposals': 'List proposals', 'POST /api/governance/proposals/:id/vote': 'Vote on proposal' },
      nft: { 'POST /api/nft/record': 'Record client-side NFT mint result', 'POST /api/nft/estimate': 'Estimate minting cost', 'GET /api/nft/certificates': 'List user NFT certificates', 'GET /api/nft/certificates/:id': 'Get NFT certificate details', 'GET /api/nft/tiers': 'Get storage tier options', 'GET /api/nft/privacy-options': 'Get privacy configuration options', 'GET /api/nft/supported-chains': 'Get supported blockchain chains' },
      transfers: { 'POST /api/transfers/initiate': 'Initiate ownership transfer', 'GET /api/transfers': 'List transfers', 'POST /api/transfers/:id/approve': 'Approve/reject transfer' },
      delegations: { 'POST /api/delegations': 'Create delegation', 'GET /api/delegations': 'List delegations', 'POST /api/delegations/:id/revoke': 'Revoke delegation' },
    },
  });
});

// =============================================================================
// HEALTH ROUTES
// =============================================================================

app.use(createHealthRoutes(services, redisService));

// =============================================================================
// MOCK / DEV-ONLY ENDPOINTS (admin, verification, wallet mocks)
// =============================================================================

// Pen-test H1 fix: defence-in-depth — even if a guard bypass lets
// ENABLE_MOCK_ENDPOINTS=true through enforceProductionConfig in production,
// the second NODE_ENV check below ensures these mock auth/admin/verification
// routes are never wired into a production app. The mock wallet
// authenticate route returns a forgeable JWT (`mock_jwt_…`) — exposing it
// in production would let any caller mint admin tokens.
const ENABLE_MOCK_ENDPOINTS =
  NODE_ENV !== 'production' && process.env.ENABLE_MOCK_ENDPOINTS === 'true';
if (ENABLE_MOCK_ENDPOINTS) {
  log('warn', 'Mock endpoints enabled — disable in production by removing ENABLE_MOCK_ENDPOINTS');
  const mockBodyParser = express.json({ limit: '1mb' });

  // Mock wallet challenge
  app.post('/api/auth/wallet/challenge', mockBodyParser, (req: Request, res: Response) => {
    const { walletAddress } = req.body || {};
    if (!walletAddress) { res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'walletAddress is required' } }); return; }
    if (!walletAddress.startsWith('addr_test') && !walletAddress.startsWith('addr1')) { res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid wallet address format' } }); return; }
    // Audit C-06: never Math.random() for an auth-flow nonce — it's predictable
    // and lets an attacker pre-compute a challenge, sign it offline with a
    // stolen key, and replay later. crypto.randomBytes is the correct source.
    const cryptoMod = require('crypto') as typeof import('crypto');
    const nonce = `${Date.now()}-${cryptoMod.randomBytes(16).toString('hex')}`;
    res.json({ challengeId: nonce, nonce, challenge: `secuura-auth-${nonce}`, expiresAt: new Date(Date.now() + 300000).toISOString(), message: 'Sign this message with your wallet to authenticate', format: 'CIP-8' });
  });

  // Mock wallet authenticate
  app.post('/api/auth/wallet/authenticate', mockBodyParser, (req: Request, res: Response) => {
    const { walletAddress, signature, nonce } = req.body || {};
    if (!walletAddress || !signature) { res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Missing required fields: walletAddress and signature are required' } }); return; }
    if (!walletAddress.startsWith('addr_test') && !walletAddress.startsWith('addr1')) { res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid wallet address format' } }); return; }
    if (nonce && nonce.includes('expired')) { res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Challenge expired' } }); return; }
    const isValidSignature = signature.startsWith('mock_signature_') || signature.length > 50;
    if (!isValidSignature) { res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid signature' } }); return; }
    res.json({
      success: true,
      token: `mock_jwt_${Buffer.from(JSON.stringify({ sub: walletAddress, role: 'holder' })).toString('base64')}`,
      user: { walletAddress, did: `did:cardano:preview:${walletAddress.slice(0, 20)}`, verified: true },
    });
  });

  winstonLogger.info('Mock endpoints enabled via ENABLE_MOCK_ENDPOINTS=true');
}

// Admin + verification routers are NOT mock-gated. They carry real CRUD
// (organisations, users, document types, workflows, notification settings,
// privacy/enforcement, etc.) that the SPAs depend on. Previously they sat
// inside the ENABLE_MOCK_ENDPOINTS block which meant every dev deploy
// without that flag silently lost half the admin API — including
// /api/settings/notifications and /api/admin/document-types listing. Mock
// routes (mock wallet challenge/authenticate) are still gated above.
{
  const mockBodyParser = express.json({ limit: '1mb' });
  const ADMIN_ROLES = ['admin', 'ADMIN', 'SYSTEM_ADMIN', 'system_admin', 'super_admin', 'SUPER_ADMIN'];
  app.use(createAdminRoutes({
    authenticateToken, query: query as any, redisService, log,
    verifyToken: verifyRs256, parseTestToken, isDbAvailable,
    services: services as any,
  }));
  app.use(createVerificationRoutes({
    authenticateToken, mockBodyParser, query, isDbAvailable, redisService, services, log,
    memWorkflowToDocumentMap, memRejectedDocuments, dbSaveRejection, ADMIN_ROLES,
    enforceDocumentTypeRules, createWorkflowInstanceIfRequired, meetsVerificationLevel,
  }));
}

// Placeholder endpoints for features not yet deployed
app.all('/api/integrations', authenticateToken(true), (_req: Request, res: Response) => {
  res.json({ success: true, integrations: [], message: 'Integrations management coming soon. Configure M365 via the admin portal.' });
});
app.all('/api/integrations/*', authenticateToken(true), (_req: Request, res: Response) => {
  res.json({ success: true, integrations: [], message: 'Integrations management coming soon.' });
});

// Client-side logger sink. The issuer SPA's logger (`frontend/issuer/src/utils/logger.ts`)
// ships warn/error events as sendBeacon batches to /api/logs in production.
// Before this route existed, every batch 404'd and polluted the console.
// We don't yet ship these to a real log store (Sentry / OpenTelemetry); for
// now we accept them, log a compact summary into container stdout, and
// 204 back. Body shape is `{ logs: [{ level, message, data?, ts }] }`.
// No auth — the SPA's beacon fires regardless of session, and the data is
// already redacted by the client-side sanitizer.
app.post('/api/logs', (req: Request, res: Response) => {
  try {
    const body = req.body as { logs?: Array<{ level?: string; message?: string }> };
    const logs = Array.isArray(body?.logs) ? body.logs : [];
    for (const entry of logs.slice(0, 20)) {
      // eslint-disable-next-line no-console
      console.log(`[client-log] [${entry?.level ?? 'info'}] ${entry?.message ?? ''}`);
    }
  } catch { /* never block the SPA on logger ingest */ }
  res.status(204).end();
});

// GET /api/document-types is served by the public handler in routes/verification.ts
// (intended-public reference data — KS-144 marks it security:[]; getAllDocumentTypes
// is a global catalog, not tenant-scoped). A role-gated copy used to sit here, but it
// was mounted after createVerificationRoutes() so it never executed — removed to drop
// the shadowed duplicate (KS-357 review). Admin write paths stay behind
// /api/admin/document-types with requireAdmin.

// =============================================================================
// RATE LIMITERS (per-endpoint)
// =============================================================================

// Pen-test F-06 fix: the login limiter previously had an UNCONDITIONAL
// `Bearer test_token_` skip. That meant in production any caller could
// bypass the per-IP login throttle by prefixing their Authorization
// header — turning the F-05 seeded passwords into a credential-stuffing
// range. Now uses the same `isTestTokenBypassAllowed` helper as the
// global limiter: bypass requires NODE_ENV ∈ {development,test} AND
// ENABLE_TEST_TOKENS=true (mirroring the test-token PARSER's gating).
import { isTestTokenBypassAllowed, shouldSkipLoginLimiter } from './middleware/rateLimitSkip';
app.use('/api/auth/login', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: parseInt(process.env.LOGIN_RATE_LIMIT || (isNonProd ? '100' : '15'), 10),
  message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many login attempts. Please try again later.' } },
  standardHeaders: true, legacyHeaders: false,
  // KS-191: test-token bypass (dev/test) OR the operator's dev/CI login-limiter
  // override — both code-guarded to non-prod, never honoured in production.
  skip: (req) =>
    isTestTokenBypassAllowed((req.headers.authorization as string) || '', NODE_ENV) ||
    shouldSkipLoginLimiter({ nodeEnv: NODE_ENV, disableEnv: process.env.LOCAL_LOGIN_LIMITER_DISABLED }),
}));

app.use('/api/auth/register', rateLimit({
  windowMs: 60 * 60 * 1000,
  max: parseInt(process.env.REGISTER_RATE_LIMIT || (isNonProd ? '100' : '5'), 10),
  message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many registration attempts. Please try again later.' } },
  standardHeaders: true, legacyHeaders: false,
}));

app.use('/api/auth/forgot-password', rateLimit({
  windowMs: 60 * 60 * 1000,
  max: parseInt(process.env.PASSWORD_RESET_RATE_LIMIT || (isNonProd ? '50' : '5'), 10),
  message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many password reset attempts. Please try again later.' } },
  standardHeaders: true, legacyHeaders: false,
}));

app.use('/api/auth/refresh', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: parseInt(process.env.REFRESH_RATE_LIMIT || (isNonProd ? '200' : '30'), 10),
  message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many token refresh attempts. Please try again later.' } },
  standardHeaders: true, legacyHeaders: false,
}));

app.use('/api/auth/password-reset', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: isNonProd ? 50 : 5,
  message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many password reset requests. Please try again later.' } },
  standardHeaders: true, legacyHeaders: false,
}));

app.use('/api/auth/verify-email', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: isNonProd ? 100 : 10,
  message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many email verification requests. Please try again later.' } },
  standardHeaders: true, legacyHeaders: false,
}));

app.use('/api/auth/mfa', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: isNonProd ? 100 : 10,
  message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many MFA requests. Please try again later.' } },
  standardHeaders: true, legacyHeaders: false,
}));

// KS-733 — the SAME TOTP secret is verifiable through a second surface. The
// self-service trio (/api/users/me/mfa/{enable,verify,disable}, declared in
// auth.openapi.ts and served by userRoutes) carried NO path-scoped limiter, so
// in production it fell through to the global 300/min: 4,500 attempts per 15
// minutes against the identical secret that /api/auth/mfa caps at 10. The
// window and max are deliberately the SAME VALUES as the block above rather
// than a reference to it — two express-rate-limit instances must not share one
// store, or the two surfaces would consume a single budget and a caller on one
// could lock out the other.
//
// This is an AUTHENTICATED surface: all three routes carry authenticate(), so
// the exposure is post-credential — the stolen-session case, which is the one
// MFA exists for, and /me/mfa/disable can switch it off.
//
// BOUND: the gateway is the only enforcement point. services/auth carries no
// limiter of its own (measured: zero rateLimit/express-rate-limit occurrences
// in services/auth/src/index.ts and routes/users.ts), so any path reaching the
// auth service directly is unaffected by this mount.
app.use('/api/users/me/mfa', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: isNonProd ? 100 : 10,
  message: { success: false, error: { code: 'RATE_LIMIT_EXCEEDED', message: 'Too many MFA requests. Please try again later.' } },
  standardHeaders: true, legacyHeaders: false,
}));

// =============================================================================
// SPEC-AWARE METHOD + AUTH ALLOW-LIST
// =============================================================================
// Two checks driven by the OpenAPI spec, applied at the gateway edge BEFORE
// any proxy:
//
//   1. METHOD GATE — reject methods not declared for the matched spec path.
//      Without this, fuzzed methods (PUT to GET-only routes etc.) get
//      proxied to backends that crash with 5xx instead of the proper 405.
//
//   2. AUTH GATE — for ops whose spec declares `security: [{ bearerAuth: [] }]`,
//      reject requests with no Authorization header / no API key with 401
//      BEFORE the proxy. Without this, unauth requests for authed routes
//      (where the gateway uses `authenticateToken(false)` for mixed public/
//      authed proxies) reach the backend and 502/500 because the backend
//      can't auth without a token.
//
// Both checks only apply when the request path matches a spec entry. Paths
// that aren't in the spec (`/api/downloads/*`, `/demo-api/*`, etc.) fall
// through unchanged.
app.use((req: Request, res: Response, next: NextFunction) => {
  if (!req.path.startsWith('/api/')) return next();

  // Union allowed/authed methods across EVERY spec entry whose regex matches
  // this path — distinct spec paths can collapse to one regex (e.g.
  // /api/referrals/{code} GET + /api/referrals/{codeId} DELETE). Gating on the
  // first match alone 405'd a method a sibling path legitimately allows
  // (KS-118).
  const { matched, methods, authedMethods, specPath } = resolveSpecRoute(specMethodMap, req.path);
  if (!matched) return next();

  const upperMethod = req.method.toUpperCase();

  // (1) Method gate
  if (!methods.has(upperMethod)) {
    res.set('Allow', [...methods].join(', '));
    res.status(405).json({
      success: false,
      error: {
        code: 'METHOD_NOT_ALLOWED',
        message: `Method ${req.method} not allowed for ${specPath}.`,
        details: { allowed: [...methods] },
      },
    });
    return;
  }

  // (2) Auth gate — only for ops the spec marks `security: bearerAuth`.
  if (authedMethods.has(upperMethod)) {
    const hasBearer = req.headers.authorization?.startsWith('Bearer ');
    const hasApiKey = typeof req.headers['x-api-key'] === 'string'
      && (req.headers['x-api-key'] as string).startsWith('sk_');
    if (!hasBearer && !hasApiKey) {
      res.status(401).json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: 'Authentication required',
        },
      });
      return;
    }
  }

  next();
});

// =============================================================================
// PROXY ROUTES (all service proxying)
// =============================================================================

app.use(createProxyRoutes({ services, authenticateToken, log }));

// =============================================================================
// PLATFORM / MULTI-TENANCY ROUTES
// =============================================================================

app.use(createPlatformRoutes({
  authenticateToken,
  tenantProvisioningUrl: process.env.TENANT_PROVISIONING_URL || 'http://tenant-provisioning:4022',
  // KS-480: register-connector mints the per-org sk_ key via the security service
  securityServiceUrl: services.security?.url || 'http://localhost:6008',
  setTenantKey, getTenantKey, removeTenantKey,
  query: query as unknown as (sql: string, params?: unknown[]) => Promise<{ rows: any[] }>,
}));

// =============================================================================
// ERROR HANDLING
// =============================================================================

app.use((req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    error: {
      code: 'NOT_FOUND',
      message: `Route ${req.method} ${req.path} not found`,
      details: { documentation: '/api' },
    },
  });
});

// Handle body-parser payload size errors before generic error tracking.
// KS-727 (ask 2): this was inline here, which the class guard's corpus-2 rule
// classified FILTER — exempt — on the presence of a `next(err)`, even though it
// answers `entity.too.large` itself and owns the response body on that path.
// Extracted to an exported symbol so corpus 1 drives it for real; see that
// file's header.
app.use(payloadTooLargeErrorHandler);

// Centralized error tracking (structured JSON + optional Sentry)
app.use(errorTrackingMiddleware('api-gateway'));

// KS-727: the global handler now lives in `./middleware/errorHandler` as an
// EXPORTED symbol. It was inline here, which put it outside the class guard's
// corpus by construction — the guard walks for exported `errorHandler` symbols
// — while it returned `err.message` to the caller on both `message` and
// `details` for every NODE_ENV that was not exactly `production`. That is the
// value the demo VM actually runs (KS-658), on the one service the internet
// talks to. Extracted and redacted; see that file's header.
app.use(errorHandler);

// =============================================================================
// GRACEFUL SHUTDOWN
// =============================================================================

let server: ReturnType<typeof app.listen>;
let isShuttingDown = false;

const gracefulShutdown = async (signal: string) => {
  if (isShuttingDown) return;
  isShuttingDown = true;
  log('info', `Received ${signal}. Starting graceful shutdown...`);
  if (server) {
    server.close((err) => {
      if (err) log('error', 'Error closing HTTP server', { error: err.message });
      else log('info', 'HTTP server closed.');
    });
  }
  const redisClient = redisService.getRedisClient();
  if (redisClient) {
    try { await redisClient.quit(); log('info', 'Redis connection closed.'); }
    catch (err) { log('error', 'Error closing Redis', { error: String(err) }); }
  }
  setTimeout(() => { log('error', 'Graceful shutdown timeout. Forcing exit.'); process.exit(1); }, 30000);
  log('info', 'Graceful shutdown complete.');
  process.exit(0);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
process.on('uncaughtException', (error) => { log('error', 'Uncaught exception', { error: error.message, stack: error.stack }); gracefulShutdown('uncaughtException'); });
// KS-546 (Kam, 2026-07-31): the gateway SURVIVES unhandled rejections
// (UNHANDLED_REJECTION_MODE=survive in compose/bicep) — KS-529 proved one
// unguarded async path here is a platform-wide, any-authed-user-repeatable
// outage. Every other service keeps fail-fast (originate's own handler, or
// Node 20's fatal default), and uncaughtException above still exits here too.
const rejectionMode = resolveUnhandledRejectionMode();
process.on(
  'unhandledRejection',
  createUnhandledRejectionHandler({
    serviceName: 'api-gateway',
    mode: rejectionMode,
    logger: (message) => log('error', message),
    shutdown: (signal) => void gracefulShutdown(signal),
  }),
);
log('info', `unhandledRejection mode: ${rejectionMode}`);

// =============================================================================
// START SERVER
// =============================================================================

/**
 * One-shot DB boot work: warm the gateway caches from the DB, then run the
 * idempotent startup migrations. Passed to initDb as its onReady hook so it
 * runs on the boot success path AND again when the DB only comes up after a
 * lost start race (KS-377 background retry) — recovery re-runs it instead of
 * silently skipping it (KS-382).
 */
async function runDbBootTasks(): Promise<void> {
  await loadFromDb();

  // Run startup database migrations (creates missing tables — idempotent)
  try {
    const { runStartupMigrations } = require('./startup-migrations');
    await runStartupMigrations();
  } catch (err: any) {
    log('warn', 'Startup migrations skipped', { error: err?.message });
  }
}

async function startServer() {
  const redisConnected = await redisService.initRedis();
  const redisMode = redisConnected ? 'Redis' : 'In-Memory (fallback)';
  const dbConnected = await initDb(runDbBootTasks);
  const dbMode = dbConnected ? 'PostgreSQL' : 'In-Memory (fallback)';
  console.log(`[API Gateway] DB init: ${dbConnected ? 'connected' : 'in-memory fallback'}`);

  server = app.listen(PORT, () => {
    log('info', 'API Gateway started', { port: PORT, environment: NODE_ENV, redis: redisMode, database: dbMode });
    console.log(`
\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557
\u2551                    SECUURA API GATEWAY                        \u2551
\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563
\u2551  Status:    Running                                           \u2551
\u2551  Port:      ${PORT}                                              \u2551
\u2551  Env:       ${(NODE_ENV).padEnd(43)}\u2551
\u2551  Storage:   ${redisMode.padEnd(43)}\u2551
\u2551  Shutdown:  Graceful (SIGTERM/SIGINT)                         \u2551
\u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563
\u2551  Endpoints:                                                   \u2551
\u2551    \u2022 API Docs:     http://localhost:${PORT}/api                   \u2551
\u2551    \u2022 Health:       http://localhost:${PORT}/health                \u2551
\u2551    \u2022 Services:     http://localhost:${PORT}/health/services       \u2551
\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d
`);
  });

  // KS-252: hold keep-alive sockets longer than any upstream proxy's idle
  // window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
  // sockets; Node's 5 s default close races their reuse -> ECONNRESET and
  // 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
  server.keepAliveTimeout = 65_000;
  server.headersTimeout = 66_000;
}

// KS-858 round 2 (gate finding F-QA-2): listen ONLY when this module is the
// process entry point.
//
// WHY THIS EXISTS. The whole of KS-858 rests on one line — `app.use(
// normaliseRepeatedSlashes())` above every predicate — and NOTHING could see
// it. Zero tests imported this file, because importing it started a server,
// so the gate deleted that line by exact string replacement and the entire
// api-gateway suite stayed green at 27 files / 277 tests. The nine cells the
// change shipped with pin the FUNCTION and a synthetic express app the test
// builds itself; they cannot pin the wiring. This guard is what makes the real
// chain observable, and `ks858-edge-path-normalisation.test.ts` now asserts
// against `app` itself: the normaliser is present, and it is the FIRST layer.
//
// WHY IT IS SAFE. `require.main === module` is true exactly when node was
// pointed at this file. Measured in all four contexts that matter:
//   node dist/index.js   (the container's CMD)          -> true, boots
//   tsx src/index.ts     (`npm run dev`)                -> true, boots
//   imported by vitest                                  -> false, does not
//   require()d from another module                      -> false, does not
// The `typeof` tests keep it from throwing if this file is ever emitted as a
// real ES module, where neither binding exists; there it evaluates false, which
// would stop the gateway booting — so a change of module target must re-measure
// this line rather than assume it. `tsconfig.json` pins `"module": "commonjs"`.
if (typeof require !== 'undefined' && typeof module !== 'undefined' && require.main === module) {
  startServer().catch((error) => {
    log('error', 'Failed to start server', { error: error.message });
    process.exit(1);
  });
}

export default app;
