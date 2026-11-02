/**
 * =============================================================================
 * SECUURA DAO GOVERNANCE SERVICE
 * =============================================================================
 * Decentralized governance with token-weighted voting
 * Port: 4018
 * =============================================================================
 */

import express from 'express';
import { initDb } from './db';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { governanceRoutes } from './routes/governance';
import * as governanceService from './services/governanceService';
import { VOTE_MULTIPLIERS, TIER_THRESHOLDS, DEFAULT_GOVERNANCE_CONFIG } from './types/governance.types';
import { logger, validateEnv } from './utils/logger';
import { authenticate as jwtAuthenticate, enforceProductionConfig, errorHandler, rejectNulBytes } from '@secuura/shared';

dotenv.config();

// Validate environment variables at startup
validateEnv();

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('governance', {
  requiredEnvVars: ['DATABASE_URL', 'REDIS_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

const app = express();
const PORT = process.env.PORT || 4018;

// =============================================================================
// MIDDLEWARE
// =============================================================================

app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || (process.env.NODE_ENV === 'production' ? [] : ['http://localhost:6100', 'http://localhost:6101', 'http://localhost:6102']),
  credentials: true,
}));
app.use(express.json());
app.use(rejectNulBytes()); // KS-471: no U+0000 may pass the boundary (raw-500 / persist class)

// Request logging
app.use((req, _res, next) => {
  logger.info('Request received', { method: req.method, path: req.path });
  next();
});

// =============================================================================
// HEALTH & INFO
// =============================================================================

app.get('/health', async (_req, res) => {
  const stats = await governanceService.getGovernanceStats();

  res.json({
    status: 'healthy',
    service: 'governance',
    timestamp: new Date().toISOString(),
    stats,
  });
});

app.get('/api', (_req, res) => {
  res.json({
    service: 'Secuura DAO Governance Service',
    version: '1.0.0',
    description: 'Decentralized governance with token-weighted voting',
    features: {
      tokenWeightedVoting: 'Vote power based on stake amount and tier',
      voteMultipliers: VOTE_MULTIPLIERS,
      tierThresholds: TIER_THRESHOLDS,
      proposalCategories: [
        'parameter_change', 'fee_adjustment', 'treasury_spend',
        'upgrade', 'emergency', 'governance_change', 'whitelist', 'general'
      ],
      timelockExecution: 'Passed proposals have configurable delay before execution',
      delegation: 'Delegate vote power to other participants',
    },
    endpoints: {
      participants: {
        'POST /api/governance/participants/register': 'Register as governance participant',
        'GET /api/governance/participants': 'Get all participants',
        'GET /api/governance/participants/:id': 'Get participant details',
      },
      proposals: {
        'POST /api/governance/proposals': 'Create new proposal (draft)',
        'GET /api/governance/proposals': 'Get all proposals',
        'GET /api/governance/proposals/active': 'Get active proposals',
        'GET /api/governance/proposals/:id': 'Get proposal details',
        'POST /api/governance/proposals/:id/submit': 'Submit proposal to start voting',
        'POST /api/governance/proposals/:id/cancel': 'Cancel a proposal',
        'POST /api/governance/proposals/:id/execute': 'Execute a queued proposal',
      },
      voting: {
        'POST /api/governance/proposals/:id/vote': 'Cast a vote',
        'GET /api/governance/proposals/:id/votes': 'Get votes for proposal',
      },
      delegation: {
        'POST /api/governance/delegate': 'Delegate vote power',
        'DELETE /api/governance/delegate': 'Revoke delegation',
      },
      config: {
        'GET /api/governance/config': 'Get governance configuration',
        'GET /api/governance/stats': 'Get governance statistics',
      },
    },
    defaultConfig: {
      approvalThreshold: `${DEFAULT_GOVERNANCE_CONFIG.defaultApprovalThresholdBps / 100}%`,
      quorumThreshold: `${DEFAULT_GOVERNANCE_CONFIG.defaultQuorumThresholdBps / 100}%`,
      votingPeriod: `${DEFAULT_GOVERNANCE_CONFIG.defaultVotingPeriodHours} hours`,
      timelockPeriod: `${DEFAULT_GOVERNANCE_CONFIG.defaultTimelockPeriodHours} hours`,
      minProposalStake: `${DEFAULT_GOVERNANCE_CONFIG.minProposalStake} SECURA`,
    },
  });
});

// =============================================================================
// ROUTES
// =============================================================================

// Pen-test H2 — every /api/* route below this point JWT-verifies the
// bearer token via @secuura/shared's `authenticate()`. Without this,
// downstream services trusted the gateway-injected x-user-* headers,
// which an attacker reaching a service directly (intra-cluster, leaked
// internal endpoint, etc.) could forge.
app.use('/api', jwtAuthenticate());

app.use('/api/governance', governanceRoutes);

// =============================================================================
// ERROR HANDLING
// =============================================================================

app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: { code: 'NOT_FOUND', message: `Route ${req.method} ${req.path} not found`, documentation: '/api' },
  });
});

// KS-103: route through the shared AppError-aware handler so typed errors
// (e.g. UnauthorizedError from authenticate()) map to their HTTP status —
// 401 for a missing/invalid token — instead of a blanket 500. The shared
// handler emits the canonical { success, error: { code, message } } shape;
// the request logger above already records method+path for each request.
app.use(errorHandler);

// =============================================================================
// SCHEDULED TASKS
// =============================================================================

// Process expired proposals every minute
setInterval(async () => {
  const processed = await governanceService.processExpiredProposals();
  if (processed > 0) {
    logger.info('Processed expired proposals', { count: processed });
  }
}, 60 * 1000);

// =============================================================================
// START SERVER
// =============================================================================

// verifyDbReady (the proposal-counter seed) is initDb's onReady boot work: it
// runs when the boot probe succeeds AND again when the DB only comes up after
// a lost start race (KS-377 background retry) — otherwise recovery would
// leave the counter unseeded and proposal numbers would restart from zero
// (KS-382).
initDb(() => governanceService.verifyDbReady()).then((connected) => {
  logger.info('DB init', { connected });
});

const server = app.listen(PORT, () => {
  logger.info('Secuura DAO Governance Service started', {
    port: PORT,
    environment: process.env.NODE_ENV || 'development',
    endpoints: {
      api: `http://localhost:${PORT}/api`,
      health: `http://localhost:${PORT}/health`,
      stats: `http://localhost:${PORT}/api/governance/stats`,
    },
  });
});

// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;
