/**
 * =============================================================================
 * HEALTH CHECK ROUTES
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { prisma } from '../db';
import { config } from '../config';

export const healthRouter = Router();

healthRouter.get('/', async (req: Request, res: Response) => {
  const health: {
    status: string;
    timestamp: string;
    service: string;
    version: string;
    checks: Record<string, string>;
  } = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'originate',
    version: '0.1.0',
    checks: {
      database: 'checking',
      redis: 'not_configured',
    },
  };

  // Database health check via Prisma
  try {
    await ((req as any).db || prisma).$queryRawUnsafe('SELECT 1');
    health.checks.database = 'healthy';
  } catch {
    health.checks.database = 'unhealthy';
    health.status = 'degraded';
  }

  const statusCode = health.status === 'healthy' ? 200 : 503;
  res.status(statusCode).json(health);
});

healthRouter.get('/ready', async (req: Request, res: Response) => {
  const CHECK_TIMEOUT = 3000;
  const checks: Record<string, { status: string; latencyMs: number; error?: string }> = {};

  async function timedCheck(name: string, fn: () => Promise<void>): Promise<void> {
    const start = Date.now();
    try {
      await Promise.race([
        fn(),
        new Promise<never>((_, reject) =>
          setTimeout(() => reject(new Error('timeout')), CHECK_TIMEOUT),
        ),
      ]);
      checks[name] = { status: 'up', latencyMs: Date.now() - start };
    } catch (err: any) {
      checks[name] = {
        status: 'down',
        latencyMs: Date.now() - start,
        error: err?.message || 'Unknown error',
      };
    }
  }

  await Promise.all([
    // PostgreSQL via Prisma
    timedCheck('postgres', async () => {
      await ((req as any).db || prisma).$queryRawUnsafe('SELECT 1');
    }),
    // Redis — lightweight ping via ioredis (lazy-loaded)
    timedCheck('redis', async () => {
      const Redis = (await import('ioredis')).default;
      const client = new Redis(config.redisUrl, {
        connectTimeout: CHECK_TIMEOUT,
        lazyConnect: true,
        maxRetriesPerRequest: 0,
      });
      try {
        await client.connect();
        await client.ping();
      } finally {
        client.disconnect();
      }
    }),
  ]);

  const allUp = Object.values(checks).every(c => c.status === 'up');

  res.status(allUp ? 200 : 503).json({
    ready: allUp,
    checks,
  });
});

healthRouter.get('/live', (_req: Request, res: Response) => {
  res.status(200).json({ live: true });
});
