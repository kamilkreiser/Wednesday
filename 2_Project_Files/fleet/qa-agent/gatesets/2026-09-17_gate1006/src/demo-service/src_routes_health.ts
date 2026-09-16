/**
 * =============================================================================
 * HEALTH ROUTE — DEMO SERVICE
 * =============================================================================
 * Simple health check endpoint for container orchestration and monitoring.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';

export const healthRouter = Router();

/**
 * GET /demo-api/health
 * Returns service health status.
 */
healthRouter.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok', service: 'demo-service' });
});
