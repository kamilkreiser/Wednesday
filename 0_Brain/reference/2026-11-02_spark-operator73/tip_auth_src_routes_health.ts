/**
 * =============================================================================
 * HEALTH CHECK ROUTES
 * =============================================================================
 * Kubernetes-compatible health, readiness, and liveness probes
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { query, isDbAvailable } from '../db';

export const healthRoutes = Router();

// Track service start time
const startTime = Date.now();

interface HealthCheck {
  status: 'healthy' | 'degraded' | 'unhealthy';
  latency?: number;
  message?: string;
}

/**
 * Check Redis connection health
 */
async function checkRedis(): Promise<HealthCheck> {
  const { getRedisClient } = await import('../services/session');
  const client = getRedisClient();
  if (!client) {
    return { status: 'degraded', message: 'Redis not connected (using in-memory fallback)' };
  }

  try {
    const start = Date.now();
    await Promise.race([
      client.ping(),
      new Promise<never>((_, reject) => setTimeout(() => reject(new Error('timeout')), 3000)),
    ]);
    return { status: 'healthy', latency: Date.now() - start };
  } catch (error) {
    return { status: 'unhealthy', message: String(error) };
  }
}

/**
 * Check database connection health
 */
async function checkDatabase(): Promise<HealthCheck> {
  if (!isDbAvailable()) {
    return { status: 'degraded', message: 'Database not connected (using in-memory storage)' };
  }

  try {
    const start = Date.now();
    await Promise.race([
      query('SELECT 1'),
      new Promise<never>((_, reject) => setTimeout(() => reject(new Error('timeout')), 3000)),
    ]);
    return { status: 'healthy', latency: Date.now() - start };
  } catch (error) {
    return { status: 'unhealthy', message: String(error) };
  }
}

/**
 * GET /health
 * Basic health check
 */
healthRoutes.get('/', (_req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    service: 'auth',
    version: '0.2.0',
    timestamp: new Date().toISOString(),
    uptime: Math.floor((Date.now() - startTime) / 1000),
  });
});

/**
 * GET /health/ready
 * Readiness check - service is ready to handle requests
 */
healthRoutes.get('/ready', async (_req: Request, res: Response) => {
  const [dbCheck, redisCheck] = await Promise.all([
    checkDatabase(),
    checkRedis(),
  ]);
  
  const checks = {
    database: dbCheck,
    redis: redisCheck,
  };
  
  // Service is ready if no checks are unhealthy
  const isReady = !Object.values(checks).some(c => c.status === 'unhealthy');
  const overallStatus = Object.values(checks).some(c => c.status === 'degraded') 
    ? 'degraded' 
    : 'healthy';
  
  res.status(isReady ? 200 : 503).json({
    ready: isReady,
    status: overallStatus,
    checks,
  });
});

/**
 * GET /health/live
 * Liveness check - service is running (not deadlocked)
 */
healthRoutes.get('/live', (_req: Request, res: Response) => {
  // If we can respond, we're alive
  res.json({ 
    live: true,
    timestamp: new Date().toISOString(),
  });
});

/**
 * GET /health/details
 * Detailed health information (for debugging)
 */
healthRoutes.get('/details', async (_req: Request, res: Response) => {
  const [dbCheck, redisCheck] = await Promise.all([
    checkDatabase(),
    checkRedis(),
  ]);
  
  res.json({
    service: 'auth',
    version: '0.2.0',
    environment: process.env.NODE_ENV || 'development',
    uptime: Math.floor((Date.now() - startTime) / 1000),
    timestamp: new Date().toISOString(),
    memory: {
      heapUsed: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
      heapTotal: Math.round(process.memoryUsage().heapTotal / 1024 / 1024),
      rss: Math.round(process.memoryUsage().rss / 1024 / 1024),
    },
    dependencies: {
      database: dbCheck,
      redis: redisCheck,
    },
  });
});
