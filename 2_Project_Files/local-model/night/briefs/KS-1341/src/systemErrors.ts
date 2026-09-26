/**
 * =============================================================================
 * SYSTEM ERRORS ROUTES
 * =============================================================================
 * Admin API for viewing and managing system errors:
 * - List/filter errors
 * - Error statistics
 * - Resolve errors
 * - Ingest errors from other services and client-side
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { z } from 'zod';
import * as errorTracking from '../services/errorTrackingService';
// KS-730: an inline 500 logs err.message server-side and answers the constant text, in every NODE_ENV.
import { logger } from '../utils/logger';
import { authenticate, requireRole } from '../middleware/auth';

export const systemErrorsRouter = Router();

// KS-267: strict query validation for GET /api/system-errors — reject wrong-type
// / out-of-range / bad-enum with 400 instead of tolerating junk (the old handler
// coerced via parseInt and treated any non-'true' resolved as false). Mirrored
// in originate.openapi.ts so the generated spec matches. `severity` matches the
// SystemError union; `resolved` is the string enum the client sends; limit/offset
// are coerced + bounded.
const SystemErrorsQuerySchema = z
  .object({
    service: z.string().trim().min(1).optional(),
    severity: z.enum(['warning', 'error', 'critical']).optional(),
    resolved: z.enum(['true', 'false']).optional(),
    limit: z.coerce.number().int().positive().max(500).optional(),
    offset: z.coerce.number().int().min(0).optional(),
  })
  // KS-423: reject unknown query params with 400 (negative_data_rejection) —
  // a silently-stripped junk param would otherwise be accepted with 200.
  .strict();

// KS-444: the three write routes below truthy-checked (or didn't check) their
// bodies, so spec-violating shapes were accepted — ingest stored `metadata`
// sent as an array, client-errors stored `source: {}`, and resolve-by-service
// answered 200 to `service: {}` (verified live 2026-07-13). Validate against
// the published request schemas (originate.openapi.ts) and 400 with the
// KS-267-style envelope on violation. `severity` is the platform's real
// severity union (errorTrackingService + the GET /api/system-errors filter,
// KS-267) — the spec's stale debug/info/warn/error/fatal enum is corrected to
// match in the same change.
const IngestErrorBodySchema = z.object({
  service: z.string().min(1),
  errorType: z.string().optional(),
  message: z.string().min(1),
  stack: z.string().optional(),
  requestPath: z.string().optional(),
  requestMethod: z.string().optional(),
  userId: z.string().optional(),
  severity: z.enum(['warning', 'error', 'critical']).optional(),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

const ClientErrorBodySchema = z.object({
  error: z.string().optional(),
  componentStack: z.string().optional(),
  url: z.string().optional(),
  userAgent: z.string().optional(),
  source: z.string().optional(),
});

const ResolveByServiceBodySchema = z.object({
  service: z.string().min(1),
});

/** Ingest an error (from other services or client-side error boundaries) */
/**
 * KS-730: the only place in this router that turns a caught error into a 500.
 *
 * WHAT WAS WRONG. Four inline handlers returned `err.message` verbatim unless
 * `NODE_ENV === 'production'`, so every non-production environment — `development`, `demo`, `test`,
 * and an UNSET NODE_ENV — answered an admin route with the raw internal text. KS-727 fixed the two
 * SHARED handlers the same way; these are the per-route remainder it enumerated rather than folded in.
 *
 * WHY A HELPER RATHER THAN DELETING THE TERNARY IN PLACE. KS-727's fix was purely SUBTRACTIVE: the
 * shared handlers already logged `err.message` and `err.stack` at entry, so removing the ternary lost
 * nothing. That is NOT true here. Measured across the three originate files this ticket enumerates:
 * **0 of 65 sites log the error before returning it**, so deleting the ternary alone would destroy the
 * diagnostic at every one of them. The ticket asks for the log to be added in the same change, and a
 * helper is the only shape in which 65 such edits stay reviewable — it is the ticket's own suggestion
 * ("a small local helper rather than 67 edited ternaries").
 *
 * The log carries the message; the RESPONSE never does. `context` names the route, so a log line is
 * attributable without the caller having to be trusted about which handler it came from.
 */
function fail500(res: Response, context: string, err: unknown): void {
    logger.error(context, { error: err instanceof Error ? err.message : String(err) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
}

systemErrorsRouter.post('/ingest', async (req: Request, res: Response) => {
  try {
    const parsed = IngestErrorBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'service and message are required', details: parsed.error.errors } });
    }
    const { service, errorType, message, stack, requestPath, requestMethod, userId, severity, metadata } = parsed.data;

    await errorTracking.trackError({
      service,
      errorType: errorType || 'unhandled',
      message,
      stack,
      requestPath,
      requestMethod,
      userId,
      ipAddress: req.ip || req.socket.remoteAddress,
      severity: severity || 'error',
      metadata,
    });

    res.status(201).json({ success: true });
  } catch (err: any) {
    logger.error('System error ingest failed', { error: err instanceof Error ? err.message : String(err) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
  }
});

/** Client-side error ingestion (from React Error Boundaries) */
systemErrorsRouter.post('/client-errors', async (req: Request, res: Response) => {
  try {
    // KS-444: every declared field is optional, but a present field must match
    // its published type (the sweep's `source: {}` was stored verbatim).
    // Non-strict, so the ErrorBoundary's extra fields (type, message, …) pass.
    const parsed = ClientErrorBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request body', details: parsed.error.errors } });
    }
    const { error, componentStack, url, userAgent, source } = parsed.data;

    await errorTracking.trackError({
      service: source || 'frontend',
      errorType: 'client_render_error',
      message: error || 'Unknown client error',
      stack: componentStack,
      requestPath: url,
      requestMethod: 'GET',
      ipAddress: req.ip || req.socket.remoteAddress,
      severity: 'error',
      metadata: { userAgent, source },
    });

    res.status(201).json({ success: true });
  } catch (err: any) {
    logger.error('Client error ingest failed', { error: err instanceof Error ? err.message : String(err) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
  }
});


/** Get error statistics (dashboard widget data) — admin only (dev: open) */
systemErrorsRouter.get('/stats', authenticate(), requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), async (_req: Request, res: Response) => {
  try {
    const stats = await errorTracking.getErrorStats();
    res.json({ success: true, stats });
  } catch (err: any) {
    fail500(res, 'Error statistics read failed (GET /api/system-errors/stats)', err);
  }
});

/** List errors with optional filters — admin only (dev: open) */
systemErrorsRouter.get('/', authenticate(), requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), async (req: Request, res: Response) => {
  try {
    const { service, severity, resolved, limit, offset } = SystemErrorsQuerySchema.parse(req.query);

    const result = await errorTracking.getRecentErrors({
      service,
      severity,
      resolved: resolved !== undefined ? resolved === 'true' : undefined,
      limit,
      offset,
    });

    res.json({ success: true, ...result });
  } catch (err: any) {
    if (err instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid query parameters', details: err.errors } });
    }
    fail500(res, 'Error list read failed (GET /api/system-errors)', err);
  }
});

/** Mark an error as resolved — admin only */
systemErrorsRouter.patch('/:errorId/resolve', authenticate(), requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), async (req: Request, res: Response) => {
  try {
    const resolved = await errorTracking.resolveError(req.params.errorId);
    res.json({ success: resolved, message: resolved ? 'Error resolved' : 'Error not found' });
  } catch (err: any) {
    fail500(res, 'Error resolve failed (PATCH /api/system-errors/:errorId/resolve)', err);
  }
});

/** Bulk resolve errors by service — admin only */
systemErrorsRouter.post('/resolve-by-service', authenticate(), requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), async (req: Request, res: Response) => {
  try {
    // KS-444: truthy check let a wrong-typed `service` (object/number) through → 200.
    const parsed = ResolveByServiceBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'service is required', details: parsed.error.errors } });
    }

    const count = await errorTracking.resolveErrorsByService(parsed.data.service);
    res.json({ success: true, resolved: count });
  } catch (err: any) {
    fail500(res, 'Bulk error resolve failed (POST /api/system-errors/resolve-by-service)', err);
  }
});
