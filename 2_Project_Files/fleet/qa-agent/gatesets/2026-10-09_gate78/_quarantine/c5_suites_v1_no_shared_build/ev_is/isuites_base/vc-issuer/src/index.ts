/**
 * =============================================================================
 * SECUURA VC ISSUER SERVICE
 * =============================================================================
 * W3C Verifiable Credential issuance, management, and verification
 * Port: 4014
 * =============================================================================
 */

import express, { Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';

dotenv.config();

import { createLogger } from './utils/logger';
import { initDb, closeDb } from './db';
import { healthRoutes } from './routes/health';
import { credentialRoutes } from './routes/credentials';
import { statusRoutes } from './routes/status';
import { presentationRoutes, loadPresentationsFromDb } from './routes/presentations';
import { identityCredentialRoutes } from './routes/identity-credentials';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/requestLogger';
import { loadFromDb as loadCredentialsFromDb } from './repositories/credentialRepo';
import { authenticate as jwtAuthenticate, enforceProductionConfig, rejectNulBytes } from '@secuura/shared';

const logger = createLogger('vc-issuer-service');

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('vc-issuer', {
  requiredEnvVars: ['DATABASE_URL', 'PRISM_AGENT_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

const app = express();
const PORT = process.env.PORT || 4014;

// =============================================================================
// MIDDLEWARE
// =============================================================================

// Security headers
app.use(helmet());

// CORS
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:6100', 'http://localhost:6101'],
  credentials: true,
}));

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
// KS-471: no U+0000 may pass the boundary (raw-500 / persist class).
// KS-781 P3-3 — this MUST be mounted after EVERY body parser, not between them. The guard
// inspects `req.body`; on a form-encoded request `express.json()` leaves `req.body` as `{}`
// and skips parsing, so a guard sitting between the two parsers runs against an empty object
// and never sees the form body. Measured before this fix: the same NUL was a 400 as JSON and
// a 200 as a form. The api-gateway (index.ts) has always mounted it after both parsers.
app.use(rejectNulBytes());

// Request logging
app.use(requestLogger);

// =============================================================================
// ROUTES
// =============================================================================

app.use('/health', healthRoutes);

// Pen-test H2 — every /api/* route below this point JWT-verifies the
// bearer token via @secuura/shared's `authenticate()`. Without this,
// downstream services trusted the gateway-injected x-user-* headers,
// which an attacker reaching a service directly (intra-cluster, leaked
// internal endpoint, etc.) could forge.
// KS-442: the two verify ops are public by contract (spec `security: []`) —
// tokenless verification is the verifier story. Paths are relative to the
// /api mount.
// KS-476: the identity-credential type catalog is public by contract too
// (spec `security: []`) — now that the gateway proxies the prefix, the
// service-side gate needs the matching exemption. /issue stays bearer-gated
// (enforced at the gateway AND here).
app.use('/api', jwtAuthenticate({
  publicOps: [
    'POST /credentials/verify',
    'POST /presentations/verify',
    'GET /identity-credentials/types',
  ],
}));

app.use('/api/credentials', credentialRoutes);
app.use('/api/status', statusRoutes);
app.use('/api/presentations', presentationRoutes);
app.use('/api/identity-credentials', identityCredentialRoutes);

// API info endpoint
app.get('/api', (_req: Request, res: Response) => {
  res.json({
    service: 'Secuura VC Issuer Service',
    version: '0.1.0',
    description: 'W3C Verifiable Credential issuance and management',
    endpoints: {
      credentials: {
        'POST /api/credentials': 'Issue a new verifiable credential',
        'GET /api/credentials': 'List credentials',
        'GET /api/credentials/:id': 'Get credential by ID',
        'POST /api/credentials/:id/revoke': 'Revoke a credential',
        'POST /api/credentials/verify': 'Verify a credential',
      },
      status: {
        'GET /api/status/:id': 'Get status list credential',
        'GET /api/status/:id/check/:index': 'Check if index is revoked',
      },
      presentations: {
        'POST /api/presentations': 'Create a verifiable presentation',
        'POST /api/presentations/verify': 'Verify a presentation',
      },
    },
    standards: {
      'W3C VC Data Model': '1.1',
      'Status List': 'StatusList2021',
      'DID Methods': ['did:prism'],
    },
  });
});

// =============================================================================
// ERROR HANDLING
// =============================================================================

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    error: { code: 'NOT_FOUND', message: `Cannot ${req.method} ${req.path}` },
  });
});

// Error handler
app.use(errorHandler);

// =============================================================================
// START SERVER
// =============================================================================

/**
 * One-shot DB boot work: warm the in-memory credential/presentation stores.
 * Passed to initDb as its onReady hook so it runs on the boot success path
 * AND again when the DB only comes up after a lost start race (KS-377
 * background retry) — recovery re-runs it instead of silently skipping it
 * (KS-382).
 */
async function runDbBootTasks(): Promise<void> {
  await Promise.all([
    loadCredentialsFromDb(),
    loadPresentationsFromDb(),
  ]);
  logger.info('All in-memory stores loaded from DB');
}

async function start() {
  const dbReady = await initDb(runDbBootTasks);
  logger.info(dbReady ? 'PostgreSQL connected' : 'Running with in-memory storage only');

  const server = app.listen(PORT, () => {
    logger.info(`VC Issuer Service running on port ${PORT}`, {
      environment: process.env.NODE_ENV || 'development',
    });

    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                SECUURA VC ISSUER SERVICE                      ║
╠═══════════════════════════════════════════════════════════════╣
║  Status:    Running                                           ║
║  Port:      ${String(PORT).padEnd(47)}║
║  Env:       ${(process.env.NODE_ENV || 'development').padEnd(47)}║
║  Database:  ${(dbReady ? 'PostgreSQL' : 'In-memory fallback').padEnd(47)}║
╠═══════════════════════════════════════════════════════════════╣
║  W3C VC Data Model: 1.1                                       ║
║  Status List:       StatusList2021                            ║
╚═══════════════════════════════════════════════════════════════╝
    `);
  });
  // KS-252: hold keep-alive sockets longer than any upstream proxy's idle
  // window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
  // sockets; Node's 5 s default close races their reuse -> ECONNRESET and
  // 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
  server.keepAliveTimeout = 65_000;
  server.headersTimeout = 66_000;

  // Graceful shutdown
  const shutdown = async (signal: string) => {
    logger.info(`${signal} received — shutting down`);
    server.close(async () => {
      await closeDb();
      process.exit(0);
    });
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));
}

start().catch((err) => {
  logger.error('Failed to start VC Issuer Service', { error: err.message });
  process.exit(1);
});

export default app;
