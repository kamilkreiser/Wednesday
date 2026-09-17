// =============================================================================
// SERVICE CONFIGURATION MODULE
// Extracted from api-gateway/src/index.ts
// =============================================================================

// =============================================================================
// TYPE DEFINITIONS
// =============================================================================

export interface ServiceConfig {
  name: string;
  url: string;
  healthPath: string;
  requiresAuth: boolean;
}

export interface UserPayload {
  userId: string;
  email: string;
  role: string;
  organizationId?: string;
  verificationLevel: string;
  authMethod?: string;
  mfaEnabled?: boolean;
  tenantId?: string;
  tenantSlug?: string;
  // KS-164: per-client rate-limit allowance for machine callers (API key /
  // OAuth app), copied from the connector record so enforceClientRateLimit can
  // apply the per-key ceiling. Absent for interactive users (global limiter).
  connectorId?: string;
  rateLimit?: number;
  rateLimitWindow?: number;
}

// =============================================================================
// ENVIRONMENT
// =============================================================================

const NODE_ENV = process.env.NODE_ENV || 'development';
export const IS_PROD = NODE_ENV === 'production';

// =============================================================================
// SECURITY CONFIGURATION
// =============================================================================

export const SECURITY_CONFIG = {
  // Rate limiting per endpoint type — stricter in production
  rateLimits: {
    auth: {
      windowMs: 15 * 60 * 1000,
      max: IS_PROD ? 5 : 10, // 5 login attempts per 15 min in production
    },
    api: {
      windowMs: 60 * 1000,
      max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || (IS_PROD ? '60' : '100'), 10),
    },
    verification: {
      windowMs: 60 * 1000,
      max: IS_PROD ? 100 : 200, // Public verification — still generous
    },
  },
  // Brute force protection
  bruteForce: {
    freeRetries: 5,
    minWait: 500,
    maxWait: 30000,
    lifetime: 300000, // 5 minutes
  },
  // Suspicious patterns for logging
  suspiciousPatterns: [
    /(\.\.\/)/, // Path traversal
    /<script/i, // XSS attempts
    /union\s+select/i, // SQL injection
    /exec\s*\(/i, // Command injection
  ],
};

// =============================================================================
// SERVICE CONFIGURATION
// =============================================================================

export const services: Record<string, ServiceConfig> = {
  originate: {
    name: 'Originate Service',
    url: process.env.ORIGINATE_SERVICE_URL || 'http://localhost:6000',
    healthPath: '/health',
    requiresAuth: true,
  },
  wallet: {
    name: 'Wallet Connector',
    url: process.env.WALLET_SERVICE_URL || 'http://localhost:6002',
    healthPath: '/health',
    requiresAuth: true,
  },
  auth: {
    name: 'Auth Service',
    url: process.env.AUTH_SERVICE_URL || 'http://localhost:6003',
    healthPath: '/health',
    requiresAuth: false,
  },
  security: {
    name: 'Security Service',
    url: process.env.SECURITY_SERVICE_URL || 'http://localhost:6008',
    healthPath: '/health',
    requiresAuth: true,
  },
  anchoring: {
    name: 'Anchoring Service',
    url: process.env.ANCHORING_SERVICE_URL || 'http://localhost:6005',
    healthPath: '/health',
    requiresAuth: true,
  },
  timestamping: {
    name: 'Timestamping Service',
    url: process.env.TIMESTAMPING_SERVICE_URL || 'http://localhost:6004',
    healthPath: '/health',
    requiresAuth: true,
  },
  prism: {
    name: 'PRISM Service',
    url: process.env.PRISM_SERVICE_URL || 'http://localhost:6001',
    healthPath: '/health',
    requiresAuth: true,
  },
  m365: {
    name: 'M365 Integration',
    url: process.env.M365_SERVICE_URL || 'http://localhost:6013',
    healthPath: '/health',
    requiresAuth: true,
  },
  vcIssuer: {
    name: 'VC Issuer Service',
    url: process.env.VC_ISSUER_SERVICE_URL || 'http://localhost:6014',
    healthPath: '/health',
    requiresAuth: true,
  },
  staking: {
    name: 'Staking Service',
    url: process.env.STAKING_SERVICE_URL || 'http://localhost:6015',
    healthPath: '/health',
    requiresAuth: true,
  },
  referral: {
    name: 'Referral Service',
    url: process.env.REFERRAL_SERVICE_URL || 'http://localhost:6016',
    healthPath: '/health',
    requiresAuth: true,
  },
  transfer: {
    name: 'Transfer Service',
    url: process.env.TRANSFER_SERVICE_URL || 'http://localhost:6020',
    healthPath: '/health',
    requiresAuth: true,
  },
  kyc: {
    name: 'KYC Service',
    url: process.env.KYC_SERVICE_URL || 'http://localhost:6011',
    healthPath: '/health',
    requiresAuth: true,
  },
  governance: {
    name: 'DAO Governance Service',
    url: process.env.GOVERNANCE_SERVICE_URL || 'http://localhost:6017',
    healthPath: '/health',
    requiresAuth: true,
  },
  nft: {
    name: 'NFT Certificate Service',
    url: process.env.NFT_SERVICE_URL || 'http://localhost:6018',
    healthPath: '/health',
    requiresAuth: true,
  },
  billing: {
    name: 'Billing Service',
    url: process.env.BILLING_SERVICE_URL || 'http://localhost:6019',
    healthPath: '/health',
    requiresAuth: false, // Some routes public (pricing)
  },
  analytics: {
    name: 'Analytics Service',
    url: process.env.ANALYTICS_SERVICE_URL || 'http://localhost:6010',
    healthPath: '/health',
    requiresAuth: true,
  },
  dashboard: {
    name: 'Dashboard Service',
    url: process.env.ANALYTICS_SERVICE_URL || 'http://localhost:6010',
    healthPath: '/health',
    requiresAuth: true,
  },
  notification: {
    name: 'Notification Service',
    url: process.env.NOTIFICATION_SERVICE_URL || 'http://localhost:6021',
    healthPath: '/health',
    requiresAuth: true,
  },
};
