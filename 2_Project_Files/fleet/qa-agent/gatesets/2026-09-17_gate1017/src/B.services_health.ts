/**
 * =============================================================================
 * HEALTH CHECK ROUTES
 * =============================================================================
 * Extracted from api-gateway/src/index.ts
 * Provides connector info, gateway health, and aggregated service health.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { ServiceConfig } from '../config/services';
import { ConnectorMeta } from '../middleware/auth';
import { authenticateToken } from '../middleware/auth';
import { query } from '../db';

// The redisService parameter mirrors `import * as redisService from './services/redis'`
// We only require the subset of methods used by these routes.
interface RedisServiceLike {
  getNotificationSettings(key: string): Promise<object | null>;
  getRedisClient(): import('ioredis').default | null;
}

/**
 * Creates an Express Router containing the health-check routes.
 *
 * @param services  – the services record keyed by service name
 * @param redisService – redis service (or compatible object) that exposes `getNotificationSettings`
 */
export function createHealthRoutes(
  services: Record<string, ServiceConfig>,
  redisService: RedisServiceLike,
): Router {
  const router = Router();

  // ---------------------------------------------------------------------------
  // Connector info endpoint for MCP / AI agent connectors
  // ---------------------------------------------------------------------------
  router.get('/api/connector/info', authenticateToken(true), async (req: Request, res: Response) => {
    const meta = (req as any).connectorMeta as ConnectorMeta | undefined;
    if (!meta || req.user?.role !== 'connector') {
      res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'This endpoint is only available for API-key authenticated connectors' } });
      return;
    }

    let connectorConfig: Record<string, unknown> = {};
    try {
      const settingsRaw = await redisService.getNotificationSettings('platform-settings');
      const settings = (settingsRaw || {}) as Record<string, unknown>;
      const integrations = ((settings as any)?.integrations || []) as Array<Record<string, unknown>>;
      const found = integrations.find((i: any) => i.id === meta.connectorId);
      if (found?.config) connectorConfig = found.config as Record<string, unknown>;
    } catch { /* swallow – non-critical */ }

    res.json({
      id: meta.connectorId,
      name: connectorConfig.name || `Connector ${meta.connectorId}`,
      scopes: meta.scopes,
      allowedDocumentTypes: connectorConfig.allowedDocumentTypes || [],
      workflowPolicy: connectorConfig.workflowPolicy || 'enforce',
      rateLimit: meta.rateLimit,
    });
  });

  // ---------------------------------------------------------------------------
  // Gateway health
  // ---------------------------------------------------------------------------
  router.get('/health', (_req: Request, res: Response) => {
    res.json({
      status: 'healthy',
      service: 'api-gateway',
      version: '0.1.0',
      timestamp: new Date().toISOString(),
    });
  });

  // ---------------------------------------------------------------------------
  // Deep readiness check — verifies critical dependencies are reachable.
  //
  // BACKLOG H6: Gateway `/health` was reporting "healthy" even when
  // downstream services were returning 502. That's correct ACA-style
  // semantics (liveness = "the gateway process is running") but operators
  // expected one health endpoint to reflect the platform-as-a-whole state.
  // This endpoint probes the 5 services without which the platform can't
  // serve a single user-facing flow:
  //
  //   - postgres   — every authed read/write
  //   - redis      — sessions, rate limits, settings, audit cache
  //   - auth       — every login + token refresh
  //   - originate  — document CRUD + verify lookup
  //   - anchoring  — chain-first verify path (BACKLOG H6: previously absent
  //                  from the readiness check; verify flows depend on it)
  //
  // Mounted at both `/health/ready` (k8s convention) and `/health/deep`
  // (the name the user-simulated test report referenced).
  // ---------------------------------------------------------------------------
  const deepHealthHandler = async (_req: Request, res: Response): Promise<void> => {
    const CHECK_TIMEOUT = 3000;
    const checks: Record<string, { status: string; latencyMs: number; error?: string }> = {};

    // Helper: run a check with a timeout
    async function timedCheck(
      name: string,
      fn: () => Promise<void>,
    ): Promise<void> {
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

    // Helper: probe a downstream service's /health
    async function probeService(name: string, key: string): Promise<void> {
      await timedCheck(name, async () => {
        const url = services[key]?.url;
        if (!url) throw new Error(`${key} service URL not configured`);
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), CHECK_TIMEOUT);
        try {
          const resp = await fetch(`${url}/health`, { signal: controller.signal });
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        } finally {
          clearTimeout(timeout);
        }
      });
    }

    await Promise.all([
      timedCheck('postgres', async () => { await query('SELECT 1'); }),
      timedCheck('redis', async () => {
        const client = redisService.getRedisClient();
        if (!client) throw new Error('Redis client not initialised');
        await client.ping();
      }),
      probeService('auth', 'auth'),
      probeService('originate', 'originate'),
      probeService('anchoring', 'anchoring'),
    ]);

    const allUp = Object.values(checks).every(c => c.status === 'up');
    const downCount = Object.values(checks).filter(c => c.status === 'down').length;

    res.status(allUp ? 200 : 503).json({
      ready: allUp,
      status: allUp ? 'healthy' : 'degraded',
      checks,
      summary: {
        total: Object.keys(checks).length,
        up: Object.keys(checks).length - downCount,
        down: downCount,
      },
      timestamp: new Date().toISOString(),
    });
  };
  router.get('/health/ready', deepHealthHandler);
  router.get('/health/deep', deepHealthHandler);

  // ---------------------------------------------------------------------------
  // Aggregated health check across all services
  //
  // Public exposure of this endpoint is opt-in. The response enumerates every
  // internal service (~20) and their up/down state — it's a free reconnaissance
  // map for an attacker (audit F-04). Set ENABLE_PUBLIC_HEALTH_SERVICES=true
  // ONLY for active platform monitoring; never in production-equivalent envs.
  // The basic /health endpoint above remains public for ACA liveness probes.
  // ---------------------------------------------------------------------------
  router.get('/health/services', async (_req: Request, res: Response) => {
    if (process.env.ENABLE_PUBLIC_HEALTH_SERVICES !== 'true') {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Not found' } });
    }
    const serviceHealth: Record<string, { status: string; latency?: number; error?: string }> = {};

    await Promise.all(
      Object.entries(services).map(async ([key, service]) => {
        const start = Date.now();
        try {
          const controller = new AbortController();
          const timeout = setTimeout(() => controller.abort(), 5000);

          const response = await fetch(`${service.url}${service.healthPath}`, {
            signal: controller.signal,
          });

          clearTimeout(timeout);

          serviceHealth[key] = {
            status: response.ok ? 'healthy' : 'unhealthy',
            latency: Date.now() - start,
          };
        } catch (error) {
          serviceHealth[key] = {
            status: 'unreachable',
            latency: Date.now() - start,
            error: error instanceof Error ? error.message : 'Unknown error',
          };
        }
      }),
    );

    const allHealthy = Object.values(serviceHealth).every(s => s.status === 'healthy');

    res.status(allHealthy ? 200 : 503).json({
      status: allHealthy ? 'healthy' : 'degraded',
      gateway: 'healthy',
      services: serviceHealth,
      timestamp: new Date().toISOString(),
    });
  });

  return router;
}
