/**
 * =============================================================================
 * KS-695 ask 3 - POST/GET /api/platform/organizations/erase-connector
 * =============================================================================
 * Connector-scoped ORGANISATION erasure, for dissolution. Platform S calls it with the
 * organisation's operational `sk_` key; the gateway validates that key, exchanges it for a
 * connector JWT and forwards a Bearer, so `authenticate()` populates `req.user` with role
 * `connector` and the verified `tenantId` / `organizationId` claims.
 *
 * The wire contract is Platform S's, implemented as its client already sends it (KS-695,
 * 2026-08-28): the paths below, and the envelope `{ success, data: { status, alreadyErased } }`.
 * S stops on `completed`, retries anything else without bound, and takes a 403 as terminal.
 * Shape ruled by Kam, 2026-09-02: ONE TERMINAL SYNCHRONOUS POST.
 *
 * PR (i) landed the mount and every refusal; PR (ii), here, is the erasure: a request that passes
 * every check erases inside ONE transaction and answers `completed` in the same response. The
 * route itself never writes: all writes are in the service, inside `withTenant`.
 *
 * ⚠ LIMITATION, in plain words: a document created with no `organizationUuid` claim and no
 * `onBehalfOf` is unattributable and is NOT reached by this erasure. See the service header.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { authenticate, requireRole, JwtPayload } from '../middleware/auth';
import { prisma } from '../db';
import { logger } from '../utils/logger';
import {
  ConnectorOrganisationContext,
  OrganisationErasureForbiddenError,
  OrganisationErasureConnectorSharedError,
  OrganisationErasureFallbackPrincipalError,
  OrganisationErasureOrgLessError,
  OrganisationTooLargeError,
  eraseConnectorOrganisation,
  isOrganisationErased,
  resolveCallerOrganisation,
  resolveOrganisationErasureTarget,
} from '../services/connectorOrganisationErasure';

export const platformOrganizationsRouter = Router();
platformOrganizationsRouter.use(authenticate());

const CONNECTOR_ROLES = ['connector'] as const;

// Same bounds as ask 1's `externalRef` (the stored column is VARCHAR(128)); `keyId` is a TEXT id.
const Ref = z.string().trim().min(1).max(128);
const EraseBody = z.object({ externalRef: Ref, keyId: Ref });

/** Tenant + connector id + Organisation from the VERIFIED claims, never from a header. */
function connectorContext(req: Request): ConnectorOrganisationContext | null {
  const user = (req as unknown as { user?: JwtPayload }).user;
  const tenantId = user?.tenantId;
  if (!user || !tenantId) return null;
  return { connectorId: String(user.userId).replace(/^connector:/, ''), tenantId, organizationId: user.organizationId };
}

/** The request's tenant-scoped db when the app provided one, else the default client. */
function requestDb(req: Request): typeof prisma {
  return ((req as unknown as { db?: typeof prisma }).db || prisma) as typeof prisma;
}

/**
 * M-2: a refusal of the fallback principal is logged with the VERIFIED claims only (tenant and organisation). The request's own
 * `keyId` is caller input and the organisation's name is what is being erased, so neither is logged.
 */
function logFallbackRefusal(ctx: ConnectorOrganisationContext): void {
  logger.warn('erase-connector: refused 403, the calling principal is the fallback label shared by every key without a connector id', {
    tenantId: ctx.tenantId,
    organizationId: ctx.organizationId,
  });
}

/**
 * One mapping for both handlers. A crossing is terminal and a caller fault (403); an org-less key
 * is terminal but not a refusal of authority (200 `unresolvable`). Neither is a 5xx: a refusal that
 * reaches S as a 5xx is a retry loop, not a refusal. Anything else is left to the caller.
 */
function sendRefusal(res: Response, err: unknown): Response | null {
  if (err instanceof OrganisationErasureOrgLessError) {
    return res.json({ success: true, data: { status: 'unresolvable', alreadyErased: false, reason: 'org_less_key' } });
  }
  if (err instanceof OrganisationErasureForbiddenError) {
    return res.status(403).json({
      success: false,
      error: { code: 'FORBIDDEN', message: "the request names an organisation or key outside this connector's Organisation" },
    });
  }
  return null;
}

platformOrganizationsRouter.post('/erase-connector', requireRole(...CONNECTOR_ROLES), async (req: Request, res: Response) => {
  // The request clock for the erasure's time budget (a MONOTONIC reading, taken before anything else this handler does, so the
  // two pre-transaction reads below and any wait for a connection count against the budget the proxy is timing).
  const startedAtMs = performance.now();
  const parsed = EraseBody.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'externalRef and keyId are required (1-128 characters each)' } });
  }
  const ctx = connectorContext(req);
  if (!ctx) {
    return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector token carries no tenant' } });
  }
  let target;
  try {
    target = await resolveOrganisationErasureTarget(ctx, parsed.data, requestDb(req));
  } catch (err) {
    if (err instanceof OrganisationErasureFallbackPrincipalError) logFallbackRefusal(ctx);
    const refused = sendRefusal(res, err);
    if (refused) return refused;
    logger.error('erase-connector: resolving the erasure target failed', { tenantId: ctx.tenantId, error: err instanceof Error ? err.message : String(err) });
    return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Organisation erasure check failed' } });
  }
  try {
    const result = await eraseConnectorOrganisation(target, { startedAtMs });
    return res.json({ success: true, data: result });
  } catch (err) {
    // A refusal raised INSIDE the transaction (the named key's row is gone, or the shared revoke policy
    // refused it) is the same terminal answer as one raised before it, and nothing was written.
    if (err instanceof OrganisationErasureConnectorSharedError) {
      logger.warn("erase-connector: refused 403, another key in the tenant carries this key's connector id", { tenantId: target.tenantId, organizationId: target.organizationId, keyId: target.keyId });
    }
    const refused = sendRefusal(res, err);
    if (refused) return refused;
    // Non-terminal on purpose. S retries a 5xx without bound and the transaction rolled back, so the retry
    // finds a clean slate. Never `completed` after a failure.
    if (err instanceof OrganisationTooLargeError) {
      logger.warn('erase-connector: refused, the organisation is too large for one synchronous request', {
        organizationId: target.organizationId,
        tenantId: ctx.tenantId,
        documents: err.documents,
        max: err.max,
      });
      return res.status(503).json({
        success: false,
        error: { code: 'ORGANISATION_TOO_LARGE', message: 'This organisation is too large to erase in one synchronous request. Nothing was erased.' },
      });
    }
    // Logged because S retries a 5xx without bound: without this line a failing erasure is an invisible loop.
    // Ids and the error only: the organisation's name and the documents' titles are what is being erased.
    logger.error('erase-connector: the erasure failed and was rolled back', {
      organizationId: target.organizationId,
      tenantId: ctx.tenantId,
      error: err instanceof Error ? err.message : String(err),
    });
    return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Organisation erasure failed. Nothing was erased.' } });
  }
});

platformOrganizationsRouter.get('/erase-connector/:organisationGuid', requireRole(...CONNECTOR_ROLES), async (req: Request, res: Response) => {
  const parsedRef = Ref.safeParse(req.params.organisationGuid);
  if (!parsedRef.success) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'organisationGuid must be 1-128 characters' } });
  }
  const ctx = connectorContext(req);
  if (!ctx) {
    return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector token carries no tenant' } });
  }
  try {
    const { organizationId } = await resolveCallerOrganisation(ctx, parsedRef.data, requestDb(req));
    if (await isOrganisationErased(organizationId, ctx.tenantId, requestDb(req))) {
      return res.json({ success: true, data: { status: 'completed', alreadyErased: true } });
    }
  } catch (err) {
    const refused = sendRefusal(res, err);
    if (refused) return refused;
    logger.error('erase-connector: the status read failed', { tenantId: ctx.tenantId, error: err instanceof Error ? err.message : String(err) });
    return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Status read failed' } });
  }
  // Not yet erased. A non-terminal status: S re-asks later.
  return res.json({ success: true, data: { status: 'pending', alreadyErased: false } });
});
