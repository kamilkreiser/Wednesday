/**
 * =============================================================================
 * METERING / USAGE API (KS-320, Option 2)
 * =============================================================================
 * Partner-facing, tenant-scoped read API over the metering Platform-K already
 * records (charge_events). Platform-S stays the subscriber-facing biller (Stripe
 * + tiers) and consumes this to meter / reconcile / display blockchain usage
 * against a subscription.
 *
 * Auth (tenant-scoped) — two caller types:
 *   - Human / service-account → Bearer JWT, re-verified by authenticate().
 *   - Partner machine (Platform-S) → an sk_ API key. The gateway validates the
 *     key and forwards a `connector` identity + the key's authoritative
 *     x-tenant-id. The gateway STRIPS any client-supplied x-user / x-tenant
 *     trust headers before auth (anti-spoof, audit A-01) and originate is internal-only
 *     ingress, so a `connector` identity reaching this route can ONLY have been
 *     set by the gateway from a validated key — safe to accept without a JWT.
 * Either way the tenant comes from the AUTHENTICATED context, never the caller's
 * body — a partner can only read its OWN tenant's usage.
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';
import { authenticate } from '../middleware/auth';
import { logger } from '../utils/logger';
import { getUsageSummary } from '../services/chargeEvents';

// Same default tenant the documents/certifications routes fall back to when
// MULTI_TENANCY_ENABLED is off (extractTenantContext never runs → req.tenantId
// undefined). Migration 013 backfills all charge_events into this tenant.
const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';

export const meteringRouter = Router();

// Accept either a human/service-account Bearer JWT (authenticate()) or a
// gateway-validated partner API key. For an sk_ key the gateway sets
// x-user-role: connector + the key's x-tenant-id; it strips any client-supplied
// trust headers first (audit A-01) and originate is internal-only, so that
// connector identity is gateway-vouched. A partner machine has no JWT, so
// requiring one would lock out the very caller this endpoint exists for.
meteringRouter.use((req: Request, res: Response, next: NextFunction) => {
  if (req.headers['x-user-role'] === 'connector' && req.headers['x-tenant-id']) {
    (req as any).user = { userId: String(req.headers['x-user-id'] || 'connector'), role: 'connector' };
    if (!(req as any).tenantId) {
      (req as any).tenantId = String(req.headers['x-tenant-id']);
    }
    return next();
  }
  return authenticate()(req, res, next);
});

function reqTenantId(req: Request): string {
  return ((req as any).tenantId as string | undefined) || DEFAULT_TENANT_ID;
}

// Permissive ISO-8601-ish guard so we never hand junk to ::timestamptz (which
// would 500 inside the query). Accepts a date or a full timestamp.
const ISO_DATE = /^\d{4}-\d{2}-\d{2}([T ][0-9:.+Zz-]*)?$/;

/**
 * GET /api/metering/usage?from=<ISO>&to=<ISO>
 *
 * Per-event-type counts + ADA/USD totals of this tenant's recorded blockchain
 * metering (charge_events), over an optional inclusive [from, to] window.
 *
 * Response: { success, data: { tenantId, from, to, byEventType:[{eventType,
 * count, adaTotal, usdTotal}], totals:{count, adaTotal, usdTotal} } }. ADA is in
 * whole ADA (lovelace ÷ 1e6); USD is in whole dollars (cents ÷ 100).
 */
meteringRouter.get('/usage', async (req: Request, res: Response) => {
  try {
    const user = (req as any).user;
    if (!user?.userId) {
      return res
        .status(401)
        .json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
    }

    const from = typeof req.query.from === 'string' ? req.query.from : undefined;
    const to = typeof req.query.to === 'string' ? req.query.to : undefined;
    if ((from && !ISO_DATE.test(from)) || (to && !ISO_DATE.test(to))) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'from/to must be ISO-8601 dates (e.g. 2026-06-01 or 2026-06-01T00:00:00Z)' },
      });
    }

    const summary = await getUsageSummary(reqTenantId(req), from, to);
    return res.json({ success: true, data: summary });
  } catch (error) {
    logger.error('Failed to read metering usage', { error: error instanceof Error ? error.message : String(error) });
    return res
      .status(500)
      .json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to read usage' } });
  }
});
