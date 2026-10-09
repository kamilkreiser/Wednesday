/**
 * =============================================================================
 * HEALTH CHECK ROUTES
 * =============================================================================
 */

import { Router, Request, Response } from 'express';

const router = Router();

router.get('/', (_req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    service: 'vc-issuer',
    version: '0.1.0',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
});

router.get('/ready', async (_req: Request, res: Response) => {
  // Add checks for database, redis, etc.
  res.json({
    status: 'ready',
    checks: {
      service: 'ok',
      // database: 'ok',
      // redis: 'ok',
    },
  });
});

router.get('/live', (_req: Request, res: Response) => {
  res.json({ status: 'live' });
});

export { router as healthRoutes };
