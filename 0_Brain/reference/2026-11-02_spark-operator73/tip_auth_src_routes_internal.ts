/**
 * =============================================================================
 * INTERNAL ROUTES — service-to-service only (KS-480)
 * =============================================================================
 * Mounted at /internal — deliberately OUTSIDE /api so no gateway proxy mount
 * ever exposes it (the gateway proxies /api/auth and /api/users only). The
 * one route here is the connector token exchange: the api-gateway, having
 * received an `x-api-key: sk_…` request, posts the key here; auth validates
 * it against the security service (the same trust chain the gateway itself
 * uses) and mints a short-lived RS256 connector JWT. Authorisation IS the
 * possession of a valid sk_ key — no static service secret is introduced,
 * and even direct intra-cluster access yields nothing without a valid key.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { generateConnectorToken } from '../services/jwt';
import { logger } from '../utils/logger';

const SECURITY_SERVICE_URL = process.env.SECURITY_SERVICE_URL || 'http://security:4008';

export const internalRoutes = Router();

const connectorTokenSchema = z.object({
  apiKey: z.string().min(12).max(256).startsWith('sk_'),
});

/**
 * POST /internal/connector-token
 * Exchange a validated sk_ API key for a short-lived connector JWT (KS-480).
 */
internalRoutes.post('/connector-token', async (req: Request, res: Response) => {
  const parsed = connectorTokenSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({
      success: false,
      error: { code: 'VALIDATION_ERROR', message: 'apiKey (sk_…) required' },
    });
  }

  try {
    const upstream = await fetch(`${SECURITY_SERVICE_URL}/api/keys/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key: parsed.data.apiKey }),
    });
    if (!upstream.ok) {
      logger.warn('connector-token: security validate returned non-2xx', { status: upstream.status });
      return res.status(502).json({
        success: false,
        error: { code: 'BAD_GATEWAY', message: 'Key validation unavailable' },
      });
    }
    const body = (await upstream.json()) as {
      data?: {
        valid?: boolean;
        organizationId?: string;
        tenantId?: string;
        scopes?: string[];
        connectorId?: string | null;
      };
    };
    const data = body?.data;
    if (!data?.valid) {
      return res.status(401).json({
        success: false,
        error: { code: 'UNAUTHORIZED', message: 'Invalid API key' },
      });
    }

    const { token, expiresIn } = generateConnectorToken({
      connectorId: data.connectorId,
      organizationId: data.organizationId,
      tenantId: data.tenantId,
      scopes: data.scopes || [],
    });
    return res.json({ success: true, data: { token, expiresIn } });
  } catch (err) {
    logger.error('connector-token exchange failed', { error: (err as Error).message });
    return res.status(502).json({
      success: false,
      error: { code: 'BAD_GATEWAY', message: 'Key validation unavailable' },
    });
  }
});
