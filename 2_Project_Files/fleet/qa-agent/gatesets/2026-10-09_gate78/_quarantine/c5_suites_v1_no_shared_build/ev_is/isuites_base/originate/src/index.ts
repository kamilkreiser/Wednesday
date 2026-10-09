/**
 * =============================================================================
 * SECUURA ORIGINATE SERVICE
 * =============================================================================
 * Document Authenticity Service - Handles document creation, certification,
 * and verification workflows
 * =============================================================================
 */

import express, { Express, Request, Response, NextFunction } from 'express';
// KS-1041 Step 2: gateway-provenance middleware. Uses only node builtins, so
// it adds nothing to the lockfile.
import {
  createGatewayProvenanceMiddleware,
  describeState,
} from './utils/gatewayProvenance';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { certificationsRouter } from './routes/certifications';
import { documentsRouter, publicDocumentsRouter } from './routes/documents';
import { verificationRouter } from './routes/verification';
import { verificationV2Router } from './routes/verificationV2';
import { anchorsRouter } from './routes/anchors';
import { meteringRouter } from './routes/metering';
import { gdprRouter } from './routes/gdpr';
import { systemErrorsRouter } from './routes/systemErrors';
import { adminConfigRouter } from './routes/adminConfig';
import { signatoriesRouter } from './routes/signatories';
import { thirdPartyVerifiersRouter } from './routes/thirdPartyVerifiers';
import { webhooksRouter } from './routes/webhooks';
import { disconnectDb, initDb, getTenantManager, getRequestPrisma, prisma } from './db';
import { extractTenantContext, tenantGucContext, rejectNulBytes } from '@secuura/shared';
import { healthRouter } from './routes/health';
// KS-298: overload protection now lives in @secuura/shared (was the inline
// originate-only KS-294 middleware). The default instance is env-configured via
// OVERLOAD_MAX_INFLIGHT / OVERLOAD_MAX_EVENT_LOOP_LAG_MS — same knobs as before.
import { overloadProtection, startOverloadMonitor, stopOverloadMonitor } from '@secuura/shared';
import { startRetentionScheduler, stopRetentionScheduler } from './services/retentionScheduler';
import { trackError } from './services/errorTrackingService';
import { loadPricing, verifyDbReady as verifyChargeEventsDb } from './services/chargeEvents';
import { verifyDbReady as verifyDocumentsDb } from './repositories/documentRepo';
import { verifyDbReady as verifyCertificationsDb } from './repositories/certificationRepo';
import { verifyAnchorsDbReady } from './routes/anchors';
import { logger, validateEnv } from './utils/logger';
import { errorHandler } from './middleware/errorHandler';
import { config } from './config';
import { initEventBus, shutdownEventBus } from './events';
import { initErrorTracking, enforceProductionConfig } from '@secuura/shared';

dotenv.config();

// Validate environment variables at startup
validateEnv();

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('originate', {
  requiredEnvVars: ['DATABASE_URL', 'REDIS_URL', 'ANCHORING_SERVICE_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

// Initialise centralized error tracking (Sentry when SENTRY_DSN is set, structured JSON otherwise)
initErrorTracking('originate-service');

// KS-294: last-resort safety net. Overload protection (below) sheds load before
// the process is driven to a crash, but a stray unhandled rejection/exception
// must never silently kill the service without a trace — the original KS-294
// crash left no stack in originate's own logs. Log + persist both; on an
// uncaughtException the process state is undefined, so exit and let the restart
// policy bring back a clean process.
process.on('unhandledRejection', (reason: unknown) => {
  const message = reason instanceof Error ? reason.message : String(reason);
  const stack = reason instanceof Error ? reason.stack : undefined;
  logger.error('Unhandled promise rejection', { message, stack });
  trackError({ service: 'originate', errorType: 'UnhandledRejection', message, stack, severity: 'error' }).catch(() => {});
});

process.on('uncaughtException', (err: Error) => {
  logger.error('Uncaught exception — exiting for a clean restart', { message: err.message, stack: err.stack });
  trackError({ service: 'originate', errorType: err.name || 'UncaughtException', message: err.message, stack: err.stack, severity: 'error' }).catch(() => {});
  // Give the logger/tracker a brief moment to flush, then exit. unref() so this
  // timer never holds the process open on its own.
  setTimeout(() => process.exit(1), 100).unref();
});

const app: Express = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(helmet());
app.use(cors({
  origin: config.corsOrigins,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
}));
// KS-294: shed load with 503 before an OOM kill under write pressure. Mounted
// ahead of express.json so an overloaded process rejects a request before
// buffering up to 10 MB of body.
app.use(overloadProtection);

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
// KS-471: no U+0000 may pass the boundary (raw-500 / persist class).
// KS-781 P3-3 — this MUST be mounted after EVERY body parser, not between them. The guard
// inspects `req.body`; on a form-encoded request `express.json()` leaves `req.body` as `{}`
// and skips parsing, so a guard sitting between the two parsers runs against an empty object
// and never sees the form body. Measured before this fix: the same NUL was a 400 as JSON and
// a 200 as a form. The api-gateway (index.ts) has always mounted it after both parsers.
app.use(rejectNulBytes());

// Health check (liveness + readiness via routes/health.ts)
app.use('/health', healthRouter);

// API Documentation
app.get('/api', (_req: Request, res: Response) => {
  res.json({
    service: 'Secuura Originate Service',
    version: '0.2.0',
    status: 'active',
    endpoints: {
      certifications: {
        'POST /api/certifications/issue': 'Issue a new certification',
        'GET /api/certifications': 'List certifications',
        'GET /api/certifications/:id': 'Get certification details',
        'POST /api/certifications/:id/revoke': 'Revoke a certification',
        'POST /api/certifications/:id/verify': 'Verify a certification',
        'POST /api/certifications/:id/share': 'Share certification with recipients (batch)',
        'POST /api/certifications/:id/recertify': 'Issue verification certificate (Verifier → Certifier)',
        'GET /api/certifications/:id/lineage': 'Get full document lineage data',
        'GET /api/certifications/:id/evidence-bundle': 'Download evidence bundle',
      },
      documents: {
        'POST /api/documents': 'Create new document',
        'GET /api/documents/:id': 'Get document details',
        'POST /api/documents/:id/sign': 'Add digital signature',
        'POST /api/documents/:id/anchor': 'Anchor document on blockchain',
        'GET /api/documents/:id/qr': 'Generate QR code for verification',
      },
      verification: {
        'POST /api/verification/verify': 'Verify document integrity',
        'POST /api/verification/hash': 'Generate document hash',
      },
      gdpr: {
        'POST /api/gdpr/consent': 'Record user consent',
        'POST /api/gdpr/consent/withdraw': 'Withdraw consent',
        'GET /api/gdpr/consent/check?userId&purpose': 'Check valid consent',
        'GET /api/gdpr/consent/:userId': 'Get all user consents',
        'POST /api/gdpr/dsr': 'Create Data Subject Request',
        'GET /api/gdpr/dsr/pending': 'List pending DSRs (admin)',
        'PATCH /api/gdpr/dsr/:dsrId': 'Update DSR status',
        'GET /api/gdpr/export/:userId': 'Export user data (Article 20)',
        'GET /api/gdpr/export/:userId/download': 'Download user data as file',
        'POST /api/gdpr/erasure/:userId': 'Execute right-to-be-forgotten',
        'GET /api/gdpr/retention': 'List retention policies',
        'POST /api/gdpr/retention/enforce': 'Trigger retention enforcement',
        'GET /api/gdpr/deletion-log': 'View deletion audit trail',
      },
      systemErrors: {
        'POST /api/system-errors/ingest': 'Ingest error from service/client',
        'POST /api/system-errors/client-errors': 'Ingest client-side error',
        'GET /api/system-errors/stats': 'Get error statistics',
        'GET /api/system-errors': 'List errors (with filters)',
        'PATCH /api/system-errors/:errorId/resolve': 'Resolve an error',
        'POST /api/system-errors/resolve-by-service': 'Bulk resolve by service',
      },
      signatories: {
        'POST /api/signatories': 'Nominate an authorised signatory',
        'GET /api/signatories?organizationId=': 'List signatories for organisation',
        'GET /api/signatories/:id': 'Get signatory details',
        'PATCH /api/signatories/:id': 'Update signatory',
        'POST /api/signatories/:id/revoke': 'Revoke signatory authorisation',
        'POST /api/signatories/:id/reinstate': 'Reinstate revoked signatory',
        'GET /api/signatories/check?organizationId&userId': 'Check signatory authorisation',
      },
      thirdPartyVerifiers: {
        'POST /api/third-party-verifiers/register': 'Register a third-party verifier',
        'GET /api/third-party-verifiers': 'List all verifiers (admin)',
        'POST /api/third-party-verifiers/:id/approve': 'Approve a pending verifier (admin)',
        'POST /api/third-party-verifiers/:id/suspend': 'Suspend an active verifier',
        'POST /api/third-party-verifiers/:id/reinstate': 'Reinstate a suspended verifier',
        'POST /api/third-party-verifiers/verify': 'Perform third-party verification (API key auth)',
        'GET /api/third-party-verifiers/:id/records': 'Get verification records',
      },
      admin: {
        'GET /api/admin/pricing': 'Get pricing table',
        'PATCH /api/admin/pricing/:eventType': 'Update pricing for event type',
        'POST /api/admin/pricing/refresh': 'Refresh pricing cache',
        'GET /api/admin/document-types': 'List document types',
        'POST /api/admin/document-types': 'Create document type',
        'PUT /api/admin/document-types/:id': 'Update document type',
        'DELETE /api/admin/document-types/:id': 'Delete document type',
        'GET /api/admin/workflows': 'List workflows',
        'POST /api/admin/workflows': 'Create workflow',
        'PUT /api/admin/workflows/:id': 'Update workflow',
        'DELETE /api/admin/workflows/:id': 'Delete workflow',
      },
    },
  });
});

// =============================================================================
// KS-1041 Step 2: gateway provenance — establish WHERE a request came from
// before any trust header is honoured
// =============================================================================
// Mounted ahead of extractTenantContext and the KS-458 tenant block, both of
// which read `x-tenant-id`, and ahead of routes/metering.ts:42, which promotes
// `x-user-role: connector` into req.user without consulting a JWT. The full
// rationale — including why this STRIPS rather than REFUSES, and why an unset
// secret is fail-open but loud — lives in utils/gatewayProvenance.ts.
const GATEWAY_VOUCH_SECRET = process.env.GATEWAY_VOUCH_SECRET || '';
const provenanceState = describeState(GATEWAY_VOUCH_SECRET);
logger[provenanceState.level](provenanceState.message);
app.use(createGatewayProvenanceMiddleware(GATEWAY_VOUCH_SECRET));

// Multi-tenancy: attach tenant database pool + Prisma-compatible db to each request
if (process.env.MULTI_TENANCY_ENABLED === 'true') {
  app.use((req, res, next) => {
    const mgr = getTenantManager();
    if (mgr) {
      extractTenantContext(mgr)(req, res, () => {
        // Also create a Prisma-compatible client from the tenant pool
        if (req.tenantPool) {
          (req as any).db = getRequestPrisma(req);
        }
        next();
      });
      return;
    }
    next();
  });
  logger.info('Multi-tenancy middleware registered — will activate after initDb()');
}

// =============================================================================
// KS-458: request tenant context for fail-closed RLS (migration 039)
// =============================================================================
// UNCONDITIONAL — runs in single-tenant mode too (the live config), where the
// extractTenantContext block above never mounts and req.tenantId would stay
// undefined. Resolution mirrors getReqTenantId in the routes: an upstream
// middleware's req.tenantId wins (multi-tenant mode / X-Tenant-Override),
// else the gateway-derived `x-tenant-id` header, else the same default
// tenant the single-tenant migration backfills all rows into. The follow-up
// tenantGucContext() seeds AsyncLocalStorage from req.tenantId so the db.ts
// chokepoints bundle the RLS GUC into every statement's transaction.
const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';
app.use((req: Request, _res: Response, next: NextFunction) => {
  const attached = (req as any).tenantId;
  const header = req.headers['x-tenant-id'];
  (req as any).tenantId =
    (typeof attached === 'string' && attached.length > 0 ? attached : undefined) ||
    (typeof header === 'string' && header.length > 0 ? header : undefined) ||
    DEFAULT_TENANT_ID;
  next();
});
app.use(tenantGucContext());

// Certification routes
app.use('/api/certifications', certificationsRouter);

// Document routes
//
// KS-87: publicDocumentsRouter handles the no-auth subset (currently only
// GET /:id/sig-json). Must be mounted BEFORE the auth-gated documentsRouter
// so Express matches the specific public route first; anything not matched
// here falls through to documentsRouter, which enforces a Bearer JWT for
// every other /api/documents/* route.
app.use('/api/documents', publicDocumentsRouter);
app.use('/api/documents', documentsRouter);

// Verification routes
app.use('/api/verification', verificationRouter);
// KS-584 P3: the versioned verify-list contract. v1 above stays untouched
// until the coordinated cutover (Kam's word); consumers migrate per
// docs/design/2026-08-11_p3-verify-list-design.md.
app.use('/api/v2/verification', verificationV2Router);

// Anchor routes
app.use('/api/anchors', anchorsRouter);
app.use('/api/anchoring', anchorsRouter); // Alias for anchoring endpoints

// Metering / usage routes (KS-320) — partner-facing, tenant-scoped read API
// over charge_events for Platform-S (Option 2).
app.use('/api/metering', meteringRouter);

// GDPR compliance routes
app.use('/api/gdpr', gdprRouter);

// System error tracking routes (admin + client error ingestion)
app.use('/api/system-errors', systemErrorsRouter);
app.use('/api/client-errors', systemErrorsRouter); // Alias for error boundary POSTs

// Admin configuration routes (pricing, document types, workflows)
app.use('/api/admin', adminConfigRouter);

// Authorised signatory management
app.use('/api/signatories', signatoriesRouter);

// Third-party verifier management
app.use('/api/third-party-verifiers', thirdPartyVerifiersRouter);
app.use('/api/webhooks', webhooksRouter);

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Not Found', path: req.path } });
});

// KS-727: the global handler now lives in `./middleware/errorHandler` as an
// EXPORTED symbol. It was inline here, which put it outside the class guard's
// corpus by construction. Its `message` was already redacted at >= 500, but a
// `details: err.message` spread still returned the thrown text on every
// non-production environment — the value the demo VM runs (KS-658). Extracted
// and closed; see that file's header.
app.use(errorHandler);

// =============================================================================
// GRACEFUL SHUTDOWN
// =============================================================================

let isShuttingDown = false;

const gracefulShutdown = (signal: string) => {
  if (isShuttingDown) return;
  isShuttingDown = true;
  
  logger.info(`Received ${signal}. Starting graceful shutdown...`);
  
  server.close((err) => {
    if (err) {
      logger.error('Error during shutdown', { error: err.message });
      process.exit(1);
    }
    logger.info('HTTP server closed.');
    stopRetentionScheduler();
    stopOverloadMonitor();
    shutdownEventBus().catch(() => {});
    disconnectDb().finally(() => process.exit(0));
  });
  
  // Force exit after 30 seconds
  setTimeout(() => {
    logger.error('Graceful shutdown timeout. Forcing exit.');
    process.exit(1);
  }, 30000);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Start server
const server = app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                  SECUURA ORIGINATE SERVICE                    ║
╠═══════════════════════════════════════════════════════════════╣
║  Status:    Running                                           ║
║  Port:      ${PORT}                                              ║
║  Health:    http://localhost:${PORT}/health                      ║
║  GDPR:      /api/gdpr/* endpoints active                      ║
║  Retention: Scheduler active (daily enforcement)              ║
║  Shutdown:  Graceful (SIGTERM/SIGINT)                         ║
╚═══════════════════════════════════════════════════════════════╝
  `);

  // Audit 1.3: PII keyring init. Originate now reads/writes encrypted
  // ip_address + user_agent on consent_records and email + notes on
  // data_subject_requests, so the keyring must be loaded before any GDPR
  // route is hit.
  if (process.env.PII_ENCRYPTION_KEY) {
    try {
      const { initFromEnv } = require('@secuura/shared');
      initFromEnv();
      logger.info('PII encryption keyring initialised');
    } catch (err: any) {
      logger.warn('PII encryption init failed (consent/DSR will store plaintext)', { error: err?.message });
    }
  } else if (process.env.NODE_ENV === 'production') {
    logger.error('FATAL: PII_ENCRYPTION_KEY missing in production — refusing to start');
    process.exit(1);
  } else {
    logger.warn('PII_ENCRYPTION_KEY not set — consent/DSR PII will store plaintext');
  }

  // Initialize database (multi-tenancy pool manager if enabled, Prisma otherwise)
  initDb().then(() => {
    logger.info('Database initialized');
  }).catch((err) => {
    logger.error('Database initialization failed', { error: err?.message });
  });

  // Load pricing from database (awaited to ensure pricing is ready before serving requests)
  loadPricing().then(() => {
    logger.info('Pricing loaded successfully');
  }).catch((err) => {
    logger.warn('Pricing failed to load from database — using defaults', { error: err?.message });
  });

  // Verify all database connections are ready (DB is the single source of truth)
  Promise.all([
    verifyDocumentsDb(),
    verifyCertificationsDb(),
    verifyChargeEventsDb(),
    verifyAnchorsDbReady(),
  ]).then(async () => {
    logger.info('All database connections verified — DB is single source of truth');

    // Startup migrations — idempotent, safe to run on every boot
    try {
      // KS-92: the DDL below is owned by the superuser migration path
      // (api-gateway CORE_MIGRATIONS + migrations/). The runtime role
      // (secuura_app) is least-privilege and lacks CREATE/ALTER on schema
      // public, so executing it here only throws 42501 (permission denied for
      // schema public) — and because it fails on the first statement, the rest
      // never ran anyway. When the migration path has already created the
      // canonical schema, skip the redundant runtime DDL entirely.
      // KS-236: cast to_regclass to text — Prisma cannot deserialize a bare
      // `regclass` column ("Failed to deserialize column of type 'regclass'"),
      // which threw here on every boot and aborted the whole startup block
      // (the rights_holders skip, charge_events create, retention seed all
      // silently skipped). `::text` returns the qualified name or NULL.
      const rhExists: any = await prisma.$queryRawUnsafe(`SELECT to_regclass('public.rights_holders')::text AS t`);
      if (rhExists?.[0]?.t || rhExists?.rows?.[0]?.t) {
        logger.info('Startup migrations: schema owned by migration path — skipping runtime DDL (KS-92)');
        return;
      }
      // Create rights_holders table if missing
      await prisma.$executeRawUnsafe(`
        CREATE TABLE IF NOT EXISTS rights_holders (
          id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
          email VARCHAR(255), first_name VARCHAR(100), last_name VARCHAR(100),
          display_name VARCHAR(200), external_id VARCHAR(255),
          organization_id UUID, user_id UUID,
          status VARCHAR(20) DEFAULT 'active',
          invite_sent BOOLEAN DEFAULT FALSE, invite_sent_at TIMESTAMPTZ,
          invite_token VARCHAR(255), metadata JSONB DEFAULT '{}',
          created_at TIMESTAMPTZ DEFAULT NOW(), updated_at TIMESTAMPTZ DEFAULT NOW()
        )
      `);
      await prisma.$executeRawUnsafe(`CREATE INDEX IF NOT EXISTS idx_rh_email ON rights_holders(email)`);
      await prisma.$executeRawUnsafe(`CREATE INDEX IF NOT EXISTS idx_rh_org ON rights_holders(organization_id)`);
      await prisma.$executeRawUnsafe(`CREATE INDEX IF NOT EXISTS idx_rh_user ON rights_holders(user_id)`);

      // Add rights_holder columns to documents if missing
      await prisma.$executeRawUnsafe(`
        DO $$ BEGIN
          IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='documents' AND column_name='rights_holder_id') THEN
            ALTER TABLE documents ADD COLUMN rights_holder_id UUID;
          END IF;
          IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='documents' AND column_name='certification_scope') THEN
            ALTER TABLE documents ADD COLUMN certification_scope VARCHAR(20) DEFAULT 'generic';
          END IF;
        END $$
      `);

      // Create charge_events table if missing (needed for certification flow)
      await prisma.$executeRawUnsafe(`
        CREATE TABLE IF NOT EXISTS charge_events (
          id TEXT PRIMARY KEY,
          event_type TEXT NOT NULL,
          certification_id TEXT,
          initiated_by TEXT,
          amount NUMERIC NOT NULL DEFAULT 0,
          currency TEXT DEFAULT 'ADA',
          status TEXT DEFAULT 'pending',
          fee_status TEXT DEFAULT 'unpaid',
          typical_payer TEXT,
          metadata JSONB DEFAULT '{}',
          created_at TIMESTAMPTZ DEFAULT NOW()
        )
      `);

      // KS-236: the consent_records.ip_address inet→text widening moved to the
      // canonical migration path (migrations/032_widen_consent_ip_address_to_text.sql)
      // so it applies as the migration owner on dev/demo too — the runtime
      // secuura_app role can't ALTER schema public. It was dead here anyway:
      // gated behind the skip-return above and never reached past the (now-fixed)
      // to_regclass deserialize abort.

      // Audit 2.3: seed default retention policies if missing. The
      // retentionScheduler runs daily but does nothing without policies;
      // this seed unblocks enforcement on every fresh dev DB.
      await prisma.$executeRawUnsafe(`
        INSERT INTO data_retention_policies
          (data_type, retention_period_days, legal_basis, deletion_method, auto_delete, description)
        VALUES
          ('user_sessions',         90,    'GDPR Art 5(1)(e) data minimisation', 'hard',      true,
              'Idle session records — kept long enough to support investigation, then deleted.'),
          ('verification_requests', 365,   'GDPR Art 5(1)(e) data minimisation', 'hard',      true,
              'Closed verification requests retained 1 year for dispute window, then deleted.'),
          ('share_records',         365,   'GDPR Art 5(1)(e) data minimisation', 'hard',      true,
              'Document share events — useful for audit but lose value after 1 year.'),
          ('system_errors',         90,    'Operational diagnostics',            'anonymize', true,
              'System error rows older than 90 days have user_id, IP, and stack stripped.'),
          ('audit_logs',            2555,  'AU APP 11.2 / ISO 27001 A.18.1.3',  'anonymize', true,
              'Audit log entries kept 7 years (compliance requirement) but PII fields stripped after retention window.')
        ON CONFLICT (data_type) DO NOTHING
      `);

      logger.info('Startup migrations complete');
    } catch (err: any) {
      logger.warn('Startup migration issue (non-fatal)', { error: err?.message });
    }
  }).catch((err) => {
    logger.warn('Some database connections failed — service may have degraded functionality', { error: err?.message });
  });

  // Start daily retention enforcement scheduler
  startRetentionScheduler();

  // Initialise event bus for async event publishing (non-blocking)
  initEventBus();
});
// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;

// KS-294: begin sampling event-loop lag so overload protection can shed load.
startOverloadMonitor();

export default app;
