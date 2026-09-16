/**
 * =============================================================================
 * SYSTEM STATUS ROUTES
 * =============================================================================
 * Comprehensive system health, dependency, and version tracking
 * Accessible at /system/status
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { execSync } from 'child_process';
import { getRedisHealth } from '../services/redis';

const router = Router();

// =============================================================================
// CONFIGURATION
// =============================================================================

interface ServiceDefinition {
  name: string;
  description: string;
  port: number;
  url: string;
  healthPath: string;
  category: 'core' | 'blockchain' | 'integration' | 'frontend' | 'infrastructure';
  required: boolean;
  version?: string;
}

interface DependencyDefinition {
  name: string;
  type: 'database' | 'cache' | 'external' | 'blockchain';
  checkMethod: 'http' | 'tcp' | 'env';
  url?: string;
  envVar?: string;
  required: boolean;
}

// Helper to determine environment-appropriate URL
const getServiceUrl = (envVar: string, localPort: number, _azureServiceName?: string): string => {
  // Check for explicit environment variable first
  const envUrl = process.env[envVar];
  if (envUrl) return envUrl;
  
  // KS-864: the Azure staging estate is decommissioned — URLs come from the env var above or the localhost default.
  
  // Default to localhost for development
  return `http://localhost:${localPort}`;
};

// Service definitions - UPDATE THIS WHEN ENVIRONMENT CHANGES
const SERVICES: ServiceDefinition[] = [
  // Core Services
  {
    name: 'api-gateway',
    description: 'Central API routing and authentication',
    port: 8080,
    url: getServiceUrl('API_GATEWAY_URL', 8080, 'secuura-staging-api'),
    healthPath: '/health',
    category: 'core',
    required: true,
    version: '0.1.0',
  },
  {
    name: 'auth',
    description: 'Authentication and authorization service',
    port: 4003,
    url: getServiceUrl('AUTH_SERVICE_URL', 4003, 'secuura-staging-auth'),
    healthPath: '/health',
    category: 'core',
    required: true,
  },
  {
    name: 'originate',
    description: 'Document creation and management',
    port: 4000,
    url: getServiceUrl('ORIGINATE_SERVICE_URL', 4000, 'secuura-staging-originate'),
    healthPath: '/health',
    category: 'core',
    required: true,
  },
  {
    name: 'security',
    description: 'Security middleware and audit logging',
    port: 4008,
    url: getServiceUrl('SECURITY_SERVICE_URL', 4008, 'secuura-staging-security'),
    healthPath: '/health',
    category: 'core',
    required: true,
  },
  
  // Blockchain Services
  {
    name: 'anchoring',
    description: 'Cardano blockchain anchoring',
    port: 4005,
    url: getServiceUrl('ANCHORING_SERVICE_URL', 4005, 'secuura-staging-anchoring'),
    healthPath: '/health',
    category: 'blockchain',
    required: true,
  },
  {
    name: 'prism',
    description: 'Decentralized Identity (DID) management',
    port: 4001,
    url: getServiceUrl('PRISM_SERVICE_URL', 4001, 'secuura-staging-prism'),
    healthPath: '/health',
    category: 'blockchain',
    required: true,
  },
  {
    name: 'timestamping',
    description: 'RFC-3161 timestamp service',
    port: 4004,
    url: getServiceUrl('TIMESTAMPING_SERVICE_URL', 4004, 'secuura-staging-timestamp'),
    healthPath: '/health',
    category: 'blockchain',
    required: true,
  },
  {
    name: 'wallet-connector',
    description: 'CIP-30 wallet integration',
    port: 4002,
    url: getServiceUrl('WALLET_SERVICE_URL', 4002, 'secuura-staging-wallet'),
    healthPath: '/health',
    category: 'blockchain',
    required: true,
  },
  
  // Integration Services
  {
    name: 'vc-issuer',
    description: 'W3C Verifiable Credentials issuance',
    port: 4014,
    url: getServiceUrl('VC_ISSUER_SERVICE_URL', 4014),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  {
    name: 'billing',
    description: 'Stripe payment integration',
    port: 4019,
    url: getServiceUrl('BILLING_SERVICE_URL', 4019, 'secuura-staging-billing'),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  {
    name: 'analytics',
    description: 'Platform analytics and reporting',
    port: 4010,
    url: getServiceUrl('ANALYTICS_SERVICE_URL', 4010, 'secuura-staging-analytics'),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  {
    name: 'staking',
    description: 'Token staking and rewards',
    port: 4015,
    url: getServiceUrl('STAKING_SERVICE_URL', 4015, 'secuura-staging-staking'),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  {
    name: 'referral',
    description: 'Referral program management',
    port: 4016,
    url: getServiceUrl('REFERRAL_SERVICE_URL', 4016, 'secuura-staging-referral'),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  {
    name: 'governance',
    description: 'DAO governance and voting',
    port: 4017,
    url: getServiceUrl('GOVERNANCE_SERVICE_URL', 4017, 'secuura-staging-governance'),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  {
    name: 'kyc',
    description: 'Know Your Customer verification',
    port: 4011,
    url: getServiceUrl('KYC_SERVICE_URL', 4011, 'secuura-staging-kyc'),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  {
    name: 'nft-certificate',
    description: 'NFT certificate minting',
    port: 4018,
    url: getServiceUrl('NFT_SERVICE_URL', 4018, 'secuura-staging-nft'),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  {
    name: 'm365-integration',
    description: 'Microsoft 365 SharePoint integration',
    port: 4013,
    url: getServiceUrl('M365_SERVICE_URL', 4013, 'secuura-staging-m365'),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  {
    name: 'transfer',
    description: 'Ownership transfer workflows',
    port: 4020,
    url: getServiceUrl('TRANSFER_SERVICE_URL', 4020, 'secuura-staging-transfer'),
    healthPath: '/health',
    category: 'integration',
    required: false,
  },
  
  // Frontend Portals (public URLs)
  {
    name: 'issuer-portal',
    description: 'Document issuer web application',
    port: 8882,
    url: process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80',
    healthPath: '/',
    category: 'frontend',
    required: false,
  },
  {
    name: 'verifier-portal',
    description: 'Document verification web application',
    port: 8882,
    url: process.env.VERIFIER_PORTAL_URL || 'http://verifier-frontend:80',
    healthPath: '/verify/',
    category: 'frontend',
    required: false,
  },
  {
    name: 'admin-portal',
    description: 'Enterprise administration dashboard',
    port: 8882,
    url: process.env.ADMIN_PORTAL_URL || 'http://admin-frontend:80',
    healthPath: '/admin/',
    category: 'frontend',
    required: false,
  },
];

// Dependency definitions - UPDATE THIS WHEN ENVIRONMENT CHANGES
const DEPENDENCIES: DependencyDefinition[] = [
  {
    name: 'PostgreSQL',
    type: 'database',
    checkMethod: 'env',
    envVar: 'DATABASE_URL',
    required: true,
  },
  {
    name: 'Redis',
    type: 'cache',
    checkMethod: 'env',
    envVar: 'REDIS_URL',
    required: true,
  },
  {
    name: 'Blockfrost API',
    type: 'blockchain',
    checkMethod: 'env',
    envVar: 'BLOCKFROST_API_KEY',
    required: false,
  },
  {
    name: 'Stripe API',
    type: 'external',
    checkMethod: 'env',
    envVar: 'STRIPE_SECRET_KEY',
    required: false,
  },
  {
    name: 'WalletConnect',
    type: 'external',
    checkMethod: 'env',
    envVar: 'WALLETCONNECT_PROJECT_ID',
    required: false,
  },
];

// Expected package versions - UPDATE THIS WHEN DEPENDENCIES CHANGE
const EXPECTED_VERSIONS = {
  node: '>=18.0.0',
  npm: '>=9.0.0',
  typescript: '>=5.0.0',
  express: '>=4.18.0',
  prisma: '>=5.0.0',
  vite: '>=5.0.0',
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

async function checkServiceHealth(service: ServiceDefinition): Promise<{
  status: 'healthy' | 'unhealthy' | 'unreachable';
  latency?: number;
  version?: string;
  error?: string;
}> {
  const start = Date.now();
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    
    const response = await fetch(`${service.url}${service.healthPath}`, {
      signal: controller.signal,
    });
    
    clearTimeout(timeout);
    const latency = Date.now() - start;
    
    if (response.ok) {
      let version: string | undefined;
      try {
        const data = await response.json() as { version?: string };
        version = data.version;
      } catch {
        // Response may not be JSON (e.g., frontend health)
      }
      return { status: 'healthy', latency, version };
    }
    
    return { status: 'unhealthy', latency };
  } catch (error) {
    return {
      status: 'unreachable',
      latency: Date.now() - start,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

function checkDependency(dep: DependencyDefinition): {
  status: 'configured' | 'missing' | 'invalid';
  value?: string;
} {
  if (dep.checkMethod === 'env' && dep.envVar) {
    const value = process.env[dep.envVar];
    if (!value) {
      return { status: 'missing' };
    }
    // Mask sensitive values
    const masked = value.length > 8 
      ? `${value.substring(0, 4)}...${value.substring(value.length - 4)}`
      : '****';
    return { status: 'configured', value: masked };
  }
  return { status: 'missing' };
}

function getNodeVersion(): string {
  try {
    return process.version;
  } catch {
    return 'unknown';
  }
}

function getNpmVersion(): string {
  try {
    return execSync('npm --version', { encoding: 'utf-8' }).trim();
  } catch {
    return 'unknown';
  }
}

// =============================================================================
// ROUTES
// =============================================================================

/**
 * GET /system/status
 * Comprehensive system status dashboard data
 */
router.get('/status', async (_req: Request, res: Response) => {
  const startTime = Date.now();
  
  // Check all services
  const serviceChecks = await Promise.all(
    SERVICES.map(async (service) => {
      const health = await checkServiceHealth(service);
      return {
        ...service,
        ...health,
      };
    })
  );
  
  // Check all dependencies
  const dependencyChecks = DEPENDENCIES.map((dep) => ({
    ...dep,
    ...checkDependency(dep),
  }));
  
  // Calculate summary
  const healthyServices = serviceChecks.filter(s => s.status === 'healthy').length;
  const requiredHealthy = serviceChecks.filter(s => s.required && s.status === 'healthy').length;
  const requiredTotal = serviceChecks.filter(s => s.required).length;
  const configuredDeps = dependencyChecks.filter(d => d.status === 'configured').length;
  const requiredDepsConfigured = dependencyChecks.filter(d => d.required && d.status === 'configured').length;
  const requiredDepsTotal = dependencyChecks.filter(d => d.required).length;
  
  // Overall status
  const allRequiredHealthy = requiredHealthy === requiredTotal;
  const allRequiredDepsConfigured = requiredDepsConfigured === requiredDepsTotal;
  const overallStatus = allRequiredHealthy && allRequiredDepsConfigured ? 'operational' : 'degraded';
  
  // Group services by category
  const servicesByCategory = {
    core: serviceChecks.filter(s => s.category === 'core'),
    blockchain: serviceChecks.filter(s => s.category === 'blockchain'),
    integration: serviceChecks.filter(s => s.category === 'integration'),
    frontend: serviceChecks.filter(s => s.category === 'frontend'),
  };
  
  // Redis health check
  const redisHealth = await getRedisHealth();
  
  // Environment info
  const environment = {
    nodeVersion: getNodeVersion(),
    npmVersion: getNpmVersion(),
    platform: process.platform,
    arch: process.arch,
    env: process.env.NODE_ENV || 'development',
    uptime: process.uptime(),
    memoryUsage: process.memoryUsage(),
    redis: redisHealth,
  };
  
  res.json({
    status: overallStatus,
    timestamp: new Date().toISOString(),
    responseTime: Date.now() - startTime,
    summary: {
      services: {
        total: serviceChecks.length,
        healthy: healthyServices,
        required: {
          total: requiredTotal,
          healthy: requiredHealthy,
        },
      },
      dependencies: {
        total: dependencyChecks.length,
        configured: configuredDeps,
        required: {
          total: requiredDepsTotal,
          configured: requiredDepsConfigured,
        },
      },
    },
    services: servicesByCategory,
    dependencies: dependencyChecks,
    environment,
    expectedVersions: EXPECTED_VERSIONS,
    troubleshooting: generateTroubleshooting(serviceChecks, dependencyChecks),
  });
});

/**
 * GET /system/status/simple
 * Simplified status for quick checks
 */
router.get('/status/simple', async (_req: Request, res: Response) => {
  const coreServices = SERVICES.filter(s => s.required);
  const checks = await Promise.all(
    coreServices.map(async (service) => {
      const health = await checkServiceHealth(service);
      return { name: service.name, status: health.status };
    })
  );
  
  const allHealthy = checks.every(c => c.status === 'healthy');
  
  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? 'ok' : 'degraded',
    services: checks,
  });
});

// =============================================================================
// TROUBLESHOOTING GENERATOR
// =============================================================================

interface TroubleshootingItem {
  issue: string;
  severity: 'critical' | 'warning' | 'info';
  component: string;
  resolution: string;
  commands?: string[];
}

function generateTroubleshooting(
  services: Array<ServiceDefinition & { status: string; error?: string }>,
  dependencies: Array<DependencyDefinition & { status: string }>
): TroubleshootingItem[] {
  const items: TroubleshootingItem[] = [];
  
  // Check for unhealthy required services
  services
    .filter(s => s.required && s.status !== 'healthy')
    .forEach(service => {
      items.push({
        issue: `${service.name} service is ${service.status}`,
        severity: 'critical',
        component: service.name,
        resolution: `Check if the ${service.name} service is running and accessible`,
        commands: [
          `# Check service logs`,
          `docker logs secuura-${service.name}`,
          `# Restart service`,
          `docker restart secuura-${service.name}`,
          `# For Azure Container Apps:`,
          `az containerapp revision restart --name secuura-staging-${service.name} --resource-group secuura-staging-rg`,
        ],
      });
    });
  
  // Check for missing required dependencies
  dependencies
    .filter(d => d.required && d.status !== 'configured')
    .forEach(dep => {
      items.push({
        issue: `${dep.name} is not configured`,
        severity: 'critical',
        component: dep.name,
        resolution: `Set the ${dep.envVar} environment variable`,
        commands: [
          `# Set environment variable`,
          `export ${dep.envVar}="your-value-here"`,
          `# Or add to .env.local file`,
          `echo '${dep.envVar}=your-value' >> .env.local`,
        ],
      });
    });
  
  // Check for unhealthy optional services
  services
    .filter(s => !s.required && s.status !== 'healthy')
    .forEach(service => {
      items.push({
        issue: `${service.name} service is ${service.status} (optional)`,
        severity: 'warning',
        component: service.name,
        resolution: `The ${service.name} service is optional but recommended for full functionality`,
        commands: [
          `# Start the service locally`,
          `cd services/${service.name} && npm run dev`,
        ],
      });
    });
  
  // Check for missing optional dependencies
  dependencies
    .filter(d => !d.required && d.status !== 'configured')
    .forEach(dep => {
      items.push({
        issue: `${dep.name} is not configured (optional)`,
        severity: 'info',
        component: dep.name,
        resolution: `Configure ${dep.envVar} to enable ${dep.name} integration`,
        commands: [],
      });
    });
  
  return items;
}

export default router;
