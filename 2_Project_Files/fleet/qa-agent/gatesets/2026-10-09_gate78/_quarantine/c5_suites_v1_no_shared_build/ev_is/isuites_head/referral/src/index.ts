/**
 * =============================================================================
 * SECUURA REFERRAL SERVICE
 * =============================================================================
 * Referral codes, milestone tracking, and growth rewards
 * Port: 4016
 * =============================================================================
 */

import express, { Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';

dotenv.config();

import { createLogger } from './utils/logger';
import { healthRoutes } from './routes/health';
import { referralRoutes } from './routes/referrals';
import { milestonesRoutes } from './routes/milestones';
import { rewardsRoutes } from './routes/rewards';
import { leaderboardRoutes } from './routes/leaderboard';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/requestLogger';
import { initDb } from './db';
import { referralService } from './services/referralService';
import { milestoneService } from './services/milestoneService';
import { fraudDetectionService } from './services/fraudDetection';
import { authenticate as jwtAuthenticate, enforceProductionConfig, rejectNulBytes } from '@secuura/shared';

const logger = createLogger('referral-service');

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('referral', {
  requiredEnvVars: ['DATABASE_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

const app = express();
const PORT = process.env.PORT || 4016;

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
app.use('/api', jwtAuthenticate());

app.use('/api/referrals', referralRoutes);
app.use('/api/milestones', milestonesRoutes);
app.use('/api/rewards', rewardsRoutes);
app.use('/api/leaderboard', leaderboardRoutes);

// API info endpoint
app.get('/api', (_req: Request, res: Response) => {
  res.json({
    service: 'Secuura Referral Service',
    version: '0.1.0',
    description: 'Referral codes, milestone tracking, and growth rewards',
    endpoints: {
      referrals: {
        'POST /api/referrals/generate': 'Generate referral code',
        'GET /api/referrals/:code': 'Get referral code details',
        'POST /api/referrals/apply': 'Apply referral code',
        'GET /api/referrals/user/:userId': 'Get user referral stats',
        'GET /api/referrals/user/:userId/referred': 'Get referred users',
      },
      milestones: {
        'GET /api/milestones': 'Get all milestone definitions',
        'GET /api/milestones/user/:userId': 'Get user milestone progress',
        'POST /api/milestones/check/:userId': 'Check and award milestones',
      },
      rewards: {
        'GET /api/rewards/user/:userId': 'Get user rewards',
        'POST /api/rewards/claim': 'Claim pending rewards',
        'GET /api/rewards/history/:userId': 'Get reward history',
      },
      leaderboard: {
        'GET /api/leaderboard': 'Get referral leaderboard',
        'GET /api/leaderboard/monthly': 'Get monthly leaderboard',
      },
    },
    milestones: {
      firstReferral: '1 referral - 100 SECURA',
      bronze: '5 referrals - 500 SECURA',
      silver: '25 referrals - 2,500 SECURA + Silver badge',
      gold: '100 referrals - 10,000 SECURA + Gold badge',
      platinum: '500 referrals - 50,000 SECURA + Platinum badge',
      ambassador: '1,000 referrals - Ambassador status + ongoing bonus',
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
 * One-shot DB boot work: verify the referral/milestone tables and warm the
 * in-memory fraud caches. Passed to initDb as its onReady hook so it
 * runs on the boot success path AND again when the DB only comes up after a
 * lost start race (KS-377 background retry) — recovery re-runs it instead of
 * silently skipping it (KS-382). (Each callee re-checks isDbAvailable().)
 */
async function runDbBootTasks(): Promise<void> {
  await referralService.verifyDbReady();
  await milestoneService.verifyDbReady();
  await fraudDetectionService.loadFromDb();
}

initDb(runDbBootTasks).then((available) => {
  logger.info('Database initialization', { available });
}).catch(err => {
  logger.warn('Database initialization failed', { error: err.message });
});

const server = app.listen(PORT, () => {
  logger.info(`Referral Service running on port ${PORT}`, {
    environment: process.env.NODE_ENV || 'development',
  });

  logger.info('Secuura Referral Service banner displayed', {
    milestones: ['firstReferral', 'bronze', 'silver', 'gold', 'platinum', 'ambassador'],
  });
});
// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;

export default app;
