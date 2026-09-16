/**
 * =============================================================================
 * RESET ROUTE — DEMO SERVICE
 * =============================================================================
 * POST /reset endpoint that orchestrates a full demo reset: restores the
 * PostgreSQL database from a pg_dump snapshot and flushes Redis. Returns
 * structured progress with per-step timing.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';

import { logger } from '../utils/logger';
import { resetDatabase, resetRedis } from '../services/resetService';

export const resetRouter = Router();

// =============================================================================
// CONSTANTS
// =============================================================================

const SNAPSHOT_PATH = '/seed/demo-snapshot.dump';

// =============================================================================
// POST /demo-api/reset
// =============================================================================

/**
 * Orchestrate full demo reset: pg_restore + Redis FLUSHALL.
 * Requires X-Demo-Reset header to prevent accidental triggers.
 */
resetRouter.post('/reset', async (req: Request, res: Response) => {
  // Guard: require X-Demo-Reset header
  if (!req.headers['x-demo-reset']) {
    return res.status(400).json({
      success: false,
      error: { code: 'BAD_REQUEST', message: 'Missing X-Demo-Reset header. Use the demo toolbar to trigger reset.' },
    });
  }

  const overallStart = Date.now();
  logger.info('Demo reset initiated');

  try {
    // Step 1: Restore database
    const dbResult = await resetDatabase(SNAPSHOT_PATH);

    // Step 2: Flush Redis
    const redisResult = await resetRedis();

    const totalDurationMs = Date.now() - overallStart;
    logger.info('Demo reset complete', { totalDurationMs });

    return res.json({
      success: true,
      steps: [
        { name: 'database', status: 'complete', durationMs: dbResult.durationMs },
        { name: 'redis', status: 'complete', keysCleared: redisResult.keysCleared },
      ],
      totalDurationMs,
    });
  } catch (err: unknown) {
    const totalDurationMs = Date.now() - overallStart;
    const message = err instanceof Error ? err.message : 'Unknown error';
    const failedStep = message.includes('pg_restore') ? 'database' : 'redis';

    logger.error('Demo reset failed', { error: message, failedStep, totalDurationMs });

    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: message, failedStep },
    });
  }
});
