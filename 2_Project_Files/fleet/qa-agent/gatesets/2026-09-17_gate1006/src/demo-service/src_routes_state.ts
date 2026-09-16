/**
 * =============================================================================
 * STATE ROUTE — DEMO SERVICE
 * =============================================================================
 * Manages demo state (current persona, presenter mode) via Redis with an
 * in-memory fallback when Redis is unavailable. Lightweight key-value storage.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import Redis from 'ioredis';

import { logger } from '../utils/logger';
import { DemoState } from '../types';

export const stateRouter = Router();

// =============================================================================
// REDIS / IN-MEMORY STATE
// =============================================================================

let redis: Redis | null = null;

const inMemoryState: DemoState = {
  currentPersona: null,
  presenterMode: false,
  scenarioStep: 0,
};

/** Initialise Redis connection (non-blocking — falls back to in-memory). */
function getRedis(): Redis | null {
  if (redis) return redis;

  const redisUrl = process.env.REDIS_URL;
  if (!redisUrl) return null;

  try {
    redis = new Redis(redisUrl, {
      maxRetriesPerRequest: 1,
      retryStrategy: () => null, // Do not retry — fall back to in-memory
    });

    redis.on('error', (err) => {
      logger.warn('Redis unavailable, using in-memory state', { error: err.message });
      redis = null;
    });

    return redis;
  } catch {
    return null;
  }
}

// =============================================================================
// GET /demo-api/state
// =============================================================================

/**
 * Returns the current demo state from Redis or in-memory fallback.
 */
stateRouter.get('/state', async (_req: Request, res: Response) => {
  try {
    const client = getRedis();

    if (client) {
      const [currentPersona, presenterMode, scenarioStep] = await Promise.all([
        client.get('demo:currentPersona'),
        client.get('demo:presenterMode'),
        client.get('demo:scenarioStep'),
      ]);

      return res.json({
        currentPersona: currentPersona || null,
        presenterMode: presenterMode === 'true',
        scenarioStep: parseInt(scenarioStep || '0', 10),
      });
    }

    return res.json(inMemoryState);
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Failed to read demo state', { error: message });
    return res.json(inMemoryState);
  }
});

// =============================================================================
// POST /demo-api/presenter-mode
// =============================================================================

/**
 * Toggles presenter mode flag.
 */
stateRouter.post('/presenter-mode', async (req: Request, res: Response) => {
  try {
    const { enabled } = req.body;
    const value = Boolean(enabled);

    const client = getRedis();

    if (client) {
      await client.set('demo:presenterMode', String(value));
    } else {
      inMemoryState.presenterMode = value;
    }

    logger.info('Presenter mode toggled', { enabled: value });
    return res.json({ success: true, presenterMode: value });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Failed to toggle presenter mode', { error: message });
    return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
  }
});
