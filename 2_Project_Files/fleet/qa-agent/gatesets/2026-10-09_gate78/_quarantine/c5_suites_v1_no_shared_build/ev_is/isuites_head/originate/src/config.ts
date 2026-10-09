/**
 * =============================================================================
 * CONFIGURATION
 * =============================================================================
 * Service configuration loaded from environment variables
 * =============================================================================
 */

import dotenv from 'dotenv';

dotenv.config();

export const config = {
  // Server
  nodeEnv: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '4000', 10),

  // Database — append pgbouncer=true when connecting through PgBouncer to avoid
  // "prepared statement does not exist" errors (Prisma uses prepared statements
  // by default, which PgBouncer's transaction pooling mode does not support).
  databaseUrl: (() => {
    const url = process.env.DATABASE_URL;
    if (!url) throw new Error('DATABASE_URL environment variable is required');
    if (url.includes('pgbouncer') && !url.includes('pgbouncer=true')) {
      const sep = url.includes('?') ? '&' : '?';
      return `${url}${sep}pgbouncer=true&connection_limit=1`;
    }
    return url;
  })(),

  // Redis
  redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',

  // JWT — auth signs RS256; originate only verifies via JWT_PUBLIC_KEY, so no secret here.
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '1d',

  // Cardano — network drives explorer URL selection
  cardanoNodeUrl: process.env.CARDANO_NODE_URL || 'http://localhost:6092',
  cardanoNetwork: (process.env.CARDANO_NETWORK || 'preview') as 'preview' | 'preprod' | 'mainnet' | 'devnet',

  // Rate limiting
  rateLimitWindowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000', 10),
  rateLimitMaxRequests: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '100', 10),

  // CORS — include all frontend dev ports and the nginx gateway
  corsOrigins: (process.env.CORS_ORIGINS || 'http://localhost:6100,http://localhost:6101,http://localhost:6102,http://localhost:6882').split(','),

  // Feature flags
  features: {
    documentCertification: process.env.FEATURE_DOCUMENT_CERTIFICATION === 'true',
    walletIntegration: process.env.FEATURE_WALLET_INTEGRATION === 'true',
    basicDid: process.env.FEATURE_BASIC_DID === 'true',
  },
};

// Validate required configuration in production and staging
const requiredEnvVars = ['DATABASE_URL'];
const isProdOrStaging = config.nodeEnv === 'production' || config.nodeEnv === 'staging';
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar] && isProdOrStaging) {
    throw new Error(`FATAL: Missing required environment variable: ${envVar}`);
  }
}
