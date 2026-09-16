/**
 * =============================================================================
 * SECUURA DEMO SERVICE
 * =============================================================================
 * Handles demo-mode persona switching, state management, and presenter mode.
 * Provides real JWT tokens by authenticating against the auth service internally.
 * Port: 4030
 *
 * State persistence: Redis when available, in-memory fallback.
 *
 * The app itself is built by ./app (KS-641) so the middleware wiring can be
 * exercised in tests; this file is the process entry point only.
 * =============================================================================
 */

import dotenv from 'dotenv';

dotenv.config();

import { createApp } from './app';
import { createLogger } from './utils/logger';
import { assertDemoServiceEnabled } from './middleware/demoGuard';

const logger = createLogger('demo-service');

// =============================================================================
// FAIL-CLOSED BOOT GATE (KS-641)
// =============================================================================
// demo-service mints real Platform Admin tokens without asking the caller for
// a credential, and /demo-api/reset runs a pg_restore + Redis FLUSHALL. It
// must refuse to run in production at all, refuse to run without an explicit
// opt-in, and refuse to run without a usable shared key — rather than run
// open. Same shape as the PII_ENCRYPTION_KEY guards in auth / kyc / security /
// m365-integration. Runs BEFORE the app is built, so a misconfigured
// deployment never gets as far as binding a port.

try {
  assertDemoServiceEnabled();
} catch (err) {
  const message = err instanceof Error ? err.message : String(err);
  logger.error(`FATAL: ${message}`);
  process.exit(1);
}

const app = createApp();
const PORT = process.env.PORT || 4030;

// =============================================================================
// GRACEFUL SHUTDOWN
// =============================================================================

let isShuttingDown = false;
let server: ReturnType<typeof app.listen>;

const gracefulShutdown = (signal: string) => {
  if (isShuttingDown) return;
  isShuttingDown = true;

  logger.info(`Received ${signal}. Starting graceful shutdown...`);

  server.close((err?: Error) => {
    if (err) {
      logger.error('Error during shutdown', { error: err.message });
      process.exit(1);
    }
    logger.info('HTTP server closed.');
    process.exit(0);
  });

  setTimeout(() => {
    logger.error('Graceful shutdown timeout. Forcing exit.');
    process.exit(1);
  }, 30000);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// =============================================================================
// START
// =============================================================================

server = app.listen(PORT, () => {
  logger.info(`Demo Service running on port ${PORT}`, {
    environment: process.env.NODE_ENV || 'development',
    gracefulShutdown: 'enabled',
  });
});

// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;

export default app;
