/**
 * =============================================================================
 * GDPR COMPLIANCE ROUTES
 * =============================================================================
 * REST API for GDPR compliance operations:
 * - Consent management
 * - Data Subject Requests (DSR)
 * - Data retention policies
 * - Data export (portability)
 * - Right-to-be-forgotten (erasure)
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { z } from 'zod';
import * as gdpr from '../services/gdprService';
import { authenticate, requireRole, requireSelfOrRole, hasAnyRole, JwtPayload } from '../middleware/auth';
import { extractPgCode } from '../utils/pgErrors';

// KS-730: winston-only; see fail500's docblock for the measurement that licenses this.
import { logger } from '../utils/logger';
export const gdprRouter = Router();

// =============================================================================
// KS-445: write-path input guards for POST /consent and POST /dsr.
// Both handlers only truthy-checked their bodies, then bound the values into
// raw SQL (gdprService.recordConsent / createDSR, `${userId}::uuid` casts plus
// VARCHAR / CHECK / FK constraints). Fuzzer-shaped bodies therefore surfaced as
// raw Postgres failures → 500 INTERNAL_ERROR. Three layers fix that honestly:
//   1. a Zod schema mirroring the published request contract (spec-invalid
//      body → 400 VALIDATION_ERROR),
//   2. a UUID pre-check on userId — user_id is a uuid FK column, so a
//      non-UUID id cannot reference a real user → 404 (same reasoning as the
//      KS-431 export/download guard below),
//   3. SQLSTATE mapping on the DB error for values the spec permits but the
//      schema cannot store (unknown user via FK 23503 → 404; too-long /
//      not-allowed values 22001/23514 → 400).
// =============================================================================

/** Canonical UUID — users.id is a uuid column, so a non-UUID subject id is unresolvable. */
const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/** Largest millisecond value a JS Date can represent (ECMA-262 §21.4.1.1) — ±8.64e15. */
const MAX_JS_DATE_MS = 8_640_000_000_000_000;

/** Consent purposes — mirrors ConsentPurposeEnum in originate.openapi.ts (the published contract). */
const CONSENT_PURPOSES = [
  'marketing', 'analytics', 'profiling', 'data_processing',
  'third_party_sharing', 'cookies', 'communications', 'document_signing',
] as const;

/** DSR types — mirrors DSRTypeEnum in originate.openapi.ts and the data_subject_requests CHECK constraint. */
const DSR_TYPES = ['access', 'rectification', 'erasure', 'portability', 'restriction', 'objection'] as const;

/**
 * Runtime mirror of the published ConsentRecordRequest schema. `source` stays a
 * plain string (the spec does not constrain it); the DB CHECK constraint is
 * mapped to a 400 via SQLSTATE 23514 instead.
 */
const consentBodySchema = z.object({
  userId: z.string(),
  purpose: z.enum(CONSENT_PURPOSES),
  version: z.string().optional(),
  source: z.string().optional(),
  expiresInDays: z.number().int().positive().optional(),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

/** Runtime mirror of the published DSRCreateRequest schema (email carries `format: email` in the spec). */
const dsrBodySchema = z.object({
  type: z.enum(DSR_TYPES),
  userId: z.string(),
  email: z.string().email(),
  notes: z.string().optional(),
});

/**
 * KS-444: DSR statuses — mirrors DSRUpdateRequest in originate.openapi.ts, the
 * DataSubjectRequest type in services/gdprService.ts, and the
 * data_subject_requests CHECK constraint (migrations/001_initial-schema.sql).
 */
const DSR_STATUSES = ['pending', 'processing', 'completed', 'denied', 'extended'] as const;

/**
 * KS-444: runtime mirror of the published DSRUpdateRequest schema. The PATCH
 * handler only truthy-checked status/processedBy, so a spec-violating body
 * (e.g. `processedBy: {}` — the sweep's negative_data_rejection case) sailed
 * through to updateDSRStatus. Enforce exactly the published field types.
 */
const dsrUpdateBodySchema = z.object({
  status: z.enum(DSR_STATUSES),
  processedBy: z.string(),
  notes: z.string().optional(),
});

/**
 * KS-444: runtime mirror of the published ConsentWithdrawRequest schema. The
 * withdraw handler only truthy-checked userId/purpose, so a spec-violating
 * body (e.g. `userId: {}`) sailed through to the raw UPDATE.
 */
const consentWithdrawBodySchema = z.object({
  userId: z.string(),
  purpose: z.enum(CONSENT_PURPOSES),
});

/**
 * Emit a 400 VALIDATION_ERROR for a body that fails its published request
 * schema, flattening the Zod issues into one readable message.
 *
 * @param res - Express response the 400 is written to.
 * @param error - the ZodError from a failed safeParse of the request body.
 * @example
 * const parsed = consentBodySchema.safeParse(req.body ?? {});
 * if (!parsed.success) return sendBodyValidationError(res, parsed.error);
 */
function sendBodyValidationError(res: Response, error: z.ZodError): Response {
  const detail = error.issues.map((i) => `${i.path.join('.') || 'body'}: ${i.message}`).join('; ');
  return res.status(400).json({
    success: false,
    error: { code: 'VALIDATION_ERROR', message: `Invalid request body — ${detail}` },
  });
}

/**
 * Map a GDPR write-path DB failure to an honest 4xx where the SQLSTATE
 * identifies the cause. Sends the response itself and returns true when
 * mapped, so the caller writes `if (mapGdprWriteDbError(err, res)) return;`
 * and falls through to its 500 path otherwise.
 *
 * @param err - the caught error (wrapDbError wrapper carrying `pgCode`, or a
 *   raw pg/Prisma error from code outside the service's try block).
 * @param res - Express response used to emit the mapped 4xx.
 * @returns true when a 4xx response was sent; false when the error is not a
 *   recognised constraint/type failure (caller keeps its 500).
 * @example
 * if (mapGdprWriteDbError(err, res)) return;
 */
function mapGdprWriteDbError(err: unknown, res: Response): boolean {
  const pgCode = (err as { pgCode?: string } | null)?.pgCode ?? extractPgCode(err);
  // FK violation (user_id → users) or a uuid cast failure: the subject user
  // does not exist → 404, never a 500.
  if (pgCode === '23503' || pgCode === '22P02') {
    res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'User not found' } });
    return true;
  }
  // Value the spec permits but the schema can't store: too long (22001),
  // outside a CHECK-allowed set (23514), an unrepresentable datetime
  // (22007/22008), or a non-UTF-8 byte sequence in any text field (22021)
  // → the request is unprocessable as sent → 400.
  if (pgCode === '22001' || pgCode === '23514' || pgCode === '22007' || pgCode === '22008' || pgCode === '22021') {
    res.status(400).json({
      success: false,
      error: { code: 'VALIDATION_ERROR', message: 'One or more field values cannot be stored (too long or not an allowed value)' },
    });
    return true;
  }
  return false;
}

// KS-228: per-user GDPR reads/exports must be owner-or-admin, never any
// authenticated user. Admins who legitimately act on another user's data
// (e.g. processing an access DSR) hold one of these roles.
const GDPR_ADMIN_ROLES = ['SYSTEM_ADMIN', 'ORG_ADMIN'];

// All GDPR routes require authentication regardless of environment
gdprRouter.use(authenticate());

// KS-235: the consent record/withdraw/check routes take the subject userId from
// the request body/query (not a path param), so requireSelfOrRole can't gate
// them at the route level — apply the same owner-or-admin rule inline. Mirrors
// the /dsr/:dsrId post-load check. Returns true (and sends 403) when the caller
// is neither the subject nor a GDPR admin, so a non-admin cannot forge, withdraw
// or probe another user's legally-significant consent records.
function denyConsentIdor(req: Request, res: Response, targetUserId: string): boolean {
  const caller = (req as any).user as JwtPayload | undefined;
  if (targetUserId !== caller?.userId && !hasAnyRole(caller, GDPR_ADMIN_ROLES)) {
    res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'You may only act on your own consent records' } });
    return true;
  }
  return false;
}

// =============================================================================
// CONSENT MANAGEMENT
// =============================================================================

/** Record or renew consent */
/**
 * KS-730: the only place in this router that turns a caught error into a 500.
 *
 * WHAT WAS WRONG. Fifteen inline handlers returned `err.message` verbatim unless
 * `NODE_ENV === 'production'`, so `development`, `demo`, `test` and an UNSET NODE_ENV all answered a
 * GDPR route — consent, DSRs, exports, erasure, retention, the deletion log — with raw internal text.
 * KS-727 fixed the two SHARED handlers the same way; these are the per-route remainder it enumerated.
 *
 * WHY A HELPER RATHER THAN DELETING THE TERNARY. KS-727's fix was SUBTRACTIVE: the shared handlers
 * already logged at entry, so removing the ternary lost nothing. Measured across the three originate
 * files this ticket enumerates, **0 of 65 sites log the error before returning it** — so deleting the
 * ternary alone would destroy the diagnostic everywhere. The log is added in the same change.
 *
 * ⚠ THE "NO LOGGER IMPORT IN THIS FILE" CONSTRAINT, AND WHY IT NO LONGER APPLIES. A comment further
 * down this file states that `utils/logger` pulls in `config.ts`, which throws at module load when
 * DATABASE_URL is unset, and that importing it kills suites before a single test runs. **The
 * constraint was real; its stated MECHANISM is not true at this commit.** Measured: `utils/logger.ts`
 * imports `winston` and nothing else, and importing it with DATABASE_URL and JWT_SECRET both deleted
 * SUCCEEDS. What does throw is importing `routes/gdpr` itself unmocked — its own graph reaches
 * `config.ts` by another path — and that is unchanged by adding a winston-only import here. All six
 * suites that import this router are run in the Test Evidence to prove exactly that.
 */
function fail500(res: Response, context: string, err: unknown): void {
  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
}

gdprRouter.post('/consent', async (req: Request, res: Response) => {
  try {
    const { userId, purpose, version, source, expiresInDays, metadata } = req.body ?? {};

    if (!userId || !purpose) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'userId and purpose are required' } });
    }
    // KS-445: enforce the published ConsentRecordRequest contract before any
    // value reaches the raw INSERT (wrong-typed fields / non-enum purpose
    // previously fell through to Postgres → raw 500).
    const parsed = consentBodySchema.safeParse(req.body);
    if (!parsed.success) return sendBodyValidationError(res, parsed.error);
    if (denyConsentIdor(req, res, userId)) return;
    // KS-445: consent_records.user_id is a uuid FK — a non-UUID userId cannot
    // reference a real user → 404 up front (never a 22P02 → 500).
    if (!UUID_PATTERN.test(userId)) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'User not found' } });
    }
    // KS-445: the spec allows any positive integer, but an expiry beyond the
    // JS Date range cannot be represented (Invalid Date → serialisation throw).
    if (expiresInDays !== undefined && Date.now() + expiresInDays * 86400000 > MAX_JS_DATE_MS) {
      return res.status(400).json({ success: false, error: { code: 'VALIDATION_ERROR', message: 'expiresInDays is too far in the future to be stored' } });
    }

    const consent = await gdpr.recordConsent(userId, purpose, {
      version,
      source,
      expiresInDays,
      ipAddress: req.ip || req.socket.remoteAddress,
      userAgent: req.headers['user-agent'],
      metadata,
    });

    res.status(201).json({ success: true, consent });
  } catch (err: any) {
    // KS-445: unknown user (FK) → 404; storable-limit violations → 400.
    if (mapGdprWriteDbError(err, res)) return;
    fail500(res, 'GDPR consent record failed (POST /api/gdpr/consent)', err);
  }
});

/** Withdraw consent */
gdprRouter.post('/consent/withdraw', async (req: Request, res: Response) => {
  try {
    const { userId, purpose } = req.body ?? {};
    if (!userId || !purpose) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'userId and purpose are required' } });
    }
    // KS-444: enforce the published ConsentWithdrawRequest contract — a
    // wrong-typed userId or non-enum purpose previously passed the truthy
    // check and reached the raw UPDATE.
    const parsed = consentWithdrawBodySchema.safeParse(req.body);
    if (!parsed.success) return sendBodyValidationError(res, parsed.error);
    if (denyConsentIdor(req, res, userId)) return;

    const withdrawn = await gdpr.withdrawConsent(userId, purpose);
    res.json({ success: withdrawn, message: withdrawn ? 'Consent withdrawn' : 'No active consent found' });
  } catch (err: any) {
    fail500(res, 'GDPR consent withdraw failed (POST /api/gdpr/consent/withdraw)', err);
  }
});

/** Check if user has valid consent for a purpose */
gdprRouter.get('/consent/check', async (req: Request, res: Response) => {
  try {
    const { userId, purpose } = req.query;
    if (!userId || !purpose) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'userId and purpose query params are required' } });
    }
    if (denyConsentIdor(req, res, userId as string)) return;

    const valid = await gdpr.hasValidConsent(userId as string, purpose as string);
    res.json({ success: true, hasConsent: valid });
  } catch (err: any) {
    fail500(res, 'GDPR consent check failed (GET /api/gdpr/consent/check)', err);
  }
});

/** Get all consents for a user */
gdprRouter.get('/consent/:userId', requireSelfOrRole(GDPR_ADMIN_ROLES), async (req: Request, res: Response) => {
  try {
    const consents = await gdpr.getUserConsents(req.params.userId);
    res.json({ success: true, consents });
  } catch (err: any) {
    fail500(res, 'GDPR consent read failed (GET /api/gdpr/consent/:userId)', err);
  }
});

// =============================================================================
// DATA SUBJECT REQUESTS
// =============================================================================

/** Create a new DSR */
gdprRouter.post('/dsr', async (req: Request, res: Response) => {
  try {
    const { type, userId, email, notes } = req.body ?? {};
    if (!type || !userId || !email) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'type, userId, and email are required' } });
    }

    if (!DSR_TYPES.includes(type)) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `type must be one of: ${DSR_TYPES.join(', ')}` } });
    }

    // KS-445: enforce the published DSRCreateRequest contract (email carries
    // `format: email`; userId/notes must be strings) before the raw INSERT.
    const parsed = dsrBodySchema.safeParse(req.body);
    if (!parsed.success) return sendBodyValidationError(res, parsed.error);
    // KS-445: data_subject_requests.user_id is a uuid FK — a non-UUID userId
    // cannot reference a real user → 404 up front (never a 22P02 → 500).
    if (!UUID_PATTERN.test(userId)) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'User not found' } });
    }

    const dsr = await gdpr.createDSR(type, userId, email, notes);
    res.status(201).json({ success: true, request: dsr });
  } catch (err: any) {
    // KS-445: unknown user (FK) → 404; storable-limit violations → 400.
    if (mapGdprWriteDbError(err, res)) return;
    fail500(res, 'GDPR DSR create failed (POST /api/gdpr/dsr)', err);
  }
});

/** Get pending DSRs (admin). KS-694: gated unconditionally — the old `isDev` spread
 *  contributed an EMPTY array off production, and nothing we deploy sets 'production'. */
gdprRouter.get('/dsr/pending', requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), async (_req: Request, res: Response) => {
  try {
    const pending = await gdpr.getPendingDSRs();
    res.json({ success: true, requests: pending });
  } catch (err: any) {
    fail500(res, 'GDPR pending DSR list failed (GET /api/gdpr/dsr/pending)', err);
  }
});

/** Get specific DSR */
gdprRouter.get('/dsr/:dsrId', async (req: Request, res: Response) => {
  try {
    const dsr = await gdpr.getDSR(req.params.dsrId);
    if (!dsr) return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'DSR not found' } });
    // KS-228: a DSR carries the subject's PII (email/notes) — only the subject
    // or an admin may read it. dsrId is not the caller's id, so check post-load.
    const caller = (req as any).user as JwtPayload | undefined;
    if (dsr.userId !== caller?.userId && !hasAnyRole(caller, GDPR_ADMIN_ROLES)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'You may only access your own data' } });
    }
    res.json({ success: true, request: dsr });
  } catch (err: any) {
    fail500(res, 'GDPR DSR read failed (GET /api/gdpr/dsr/:dsrId)', err);
  }
});

/** Get all DSRs for a user */
gdprRouter.get('/dsr/user/:userId', requireSelfOrRole(GDPR_ADMIN_ROLES), async (req: Request, res: Response) => {
  try {
    const dsrs = await gdpr.getUserDSRs(req.params.userId);
    res.json({ success: true, requests: dsrs });
  } catch (err: any) {
    fail500(res, 'GDPR DSR list by user failed (GET /api/gdpr/dsr/user/:userId)', err);
  }
});

/** Update DSR status (admin) */
gdprRouter.patch('/dsr/:dsrId', requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), async (req: Request, res: Response) => {
  try {
    const { status, processedBy, notes } = req.body ?? {};
    if (!status || !processedBy) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'status and processedBy are required' } });
    }
    // KS-444: enforce the published DSRUpdateRequest contract — a wrong-typed
    // processedBy (the sweep sent `{}`) or a non-vocabulary status previously
    // passed the truthy check and reached updateDSRStatus.
    const parsed = dsrUpdateBodySchema.safeParse(req.body);
    if (!parsed.success) return sendBodyValidationError(res, parsed.error);
    // KS-1029: reject a non-canonical dsrId before the lookup. data_subject_requests.id is a
    // uuid, so updateDSRStatus's `::uuid` cast raised 22P02 for a malformed id and, since
    // KS-754's rethrow, this route answered 500 INTERNAL_ERROR (previously no id check here).
    // 404 'DSR not found' is what GET /dsr/:dsrId answers on the same path and a status the
    // spec declares; it sits after the body checks, as in POST /consent and POST /dsr.
    // UUID_PATTERN is canonical-only, so the hyphenless and braced forms PostgreSQL also
    // accepts now answer 404 too — a deliberate narrowing.
    if (!UUID_PATTERN.test(req.params.dsrId)) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'DSR not found' } });
    }

    const updated = await gdpr.updateDSRStatus(req.params.dsrId, status, processedBy, notes);
    res.json({ success: updated, message: updated ? 'DSR updated' : 'DSR not found' });
  } catch (err: any) {
    fail500(res, 'GDPR DSR update failed (PATCH /api/gdpr/dsr/:dsrId)', err);
  }
});

// =============================================================================
// DATA EXPORT (PORTABILITY — GDPR Article 20)
// =============================================================================

/** Export all user data */
gdprRouter.get('/export/:userId', requireSelfOrRole(GDPR_ADMIN_ROLES), async (req: Request, res: Response) => {
  try {
    const data = await gdpr.exportUserData(req.params.userId);
    res.json({ success: true, data });
  } catch (err: any) {
    fail500(res, 'GDPR export build failed (GET /api/gdpr/export/:userId)', err);
  }
});

/** Export user data as downloadable file */
gdprRouter.get('/export/:userId/download', requireSelfOrRole(GDPR_ADMIN_ROLES), async (req: Request, res: Response) => {
  try {
    // KS-431: userId is a uuid. A malformed value (the sweep sent non-UTF-8 bytes
    // `%23%F2%B5%92%9B`) reached the query and made Postgres throw (22P02 / 22021),
    // which fell through to a raw 500. Reject a non-UUID id up front — it cannot
    // reference a real user → 404 (never a 500).
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(req.params.userId)) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'User not found' } });
    }
    const data = await gdpr.exportUserData(req.params.userId);
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Content-Disposition', `attachment; filename="gdpr-export-${req.params.userId}.json"`);
    res.send(JSON.stringify(data, null, 2));
  } catch (err: any) {
    fail500(res, 'GDPR export download failed (GET /api/gdpr/export/:userId/download)', err);
  }
});

// =============================================================================
// RIGHT TO BE FORGOTTEN (ERASURE)
// =============================================================================

/** Execute erasure (cascading delete) — admin only */
// -----------------------------------------------------------------------------
// KS-695 ask 1 — connector-driven erasure, addressed by external_ref
// -----------------------------------------------------------------------------
// Platform S calls these with `x-api-key: sk_…`. The gateway validates that key,
// exchanges it for a connector JWT at auth's POST /internal/connector-token and
// forwards it as a Bearer, so `authenticate()` below populates req.user with
// role `connector`, `userId: "connector:<connectorId>"` and the verified
// `tenantId` claim. No new transport is needed — the gate is the role.
//
// The wire contract is Stuart's, implemented as his client already sends it
// (his KS-695 comment, 2026-08-28): the paths below, and the envelope
// { success, data: { status, alreadyErased } }. S stops on status `completed`
// or `alreadyErased: true`, and retries anything else without bound — which is
// why neither handler can 404 or 500 its way out of a subject it cannot
// resolve.

const CONNECTOR_ROLES = ['connector'] as const;

/**
 * Tenant + connector id + Organisation from the VERIFIED claims, never from a
 * header. `organizationId` is read exactly where the write-side sibling reads
 * it (`routes/documents.ts:84`) so the two directions of the same relationship
 * cannot disagree about which Organisation a key belongs to.
 */
function connectorContext(
  req: Request,
): { connectorId: string; tenantId: string; organizationId?: string } | null {
  const user = (req as unknown as { user?: JwtPayload }).user;
  const claims = user as unknown as { tenantId?: string; organizationId?: string } | undefined;
  const tenantId = claims?.tenantId;
  if (!user || !tenantId) return null;
  return {
    connectorId: String(user.userId).replace(/^connector:/, ''),
    tenantId,
    organizationId: claims?.organizationId,
  };
}

/**
 * One mapping for both connector erasure handlers.
 *
 * QA finding 3: the GET mapped every refusal to 500, which puts S back into the
 * unbounded retry the POST's own comment says this path exists to avoid — and
 * the spec already declared 403 on that operation, so the declared code was
 * unreachable. A refusal that reaches the caller as a 5xx is a retry loop, not
 * a refusal.
 */
function sendConnectorRefusal(res: Response, err: unknown, fallbackMessage: string): Response {
  if (err instanceof gdpr.ConnectorErasureCrossOrgError) {
    return res.status(403).json({
      success: false,
      error: { code: 'FORBIDDEN', message: "externalRef resolves to a subject outside this connector's Organisation" },
    });
  }
  // Terminal, but not the caller's fault and not a refusal of authority: 200
  // with a terminal status and a reason, so S stops sweeping and a human has
  // something to act on. Never `completed` — K did not erase anything.
  if (err instanceof gdpr.ConnectorErasureUnresolvableError) {
    return res.json({
      success: true,
      data: { status: 'unresolvable', alreadyErased: false, reason: err.reason },
    });
  }
  return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: fallbackMessage } });
}

// Peter F4. The column is VARCHAR(128) (`041_action_provenance.sql:50`) and the
// WRITE validator is `.trim().min(1).max(128)` (`originate.openapi.ts:228`).
// Accepting 255, untrimmed, meant a 129–255 char ref — or one with surrounding
// whitespace — was accepted, matched no row, and was answered
// `{"status":"completed","alreadyErased":true}`: a discharged obligation, to S.
const ExternalRefSchema = z.object({ externalRef: z.string().trim().min(1).max(128) });

gdprRouter.post('/erasures', requireRole(...CONNECTOR_ROLES), async (req: Request, res: Response) => {
  const parsed = ExternalRefSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'externalRef is required' } });
  }
  const ctx = connectorContext(req);
  if (!ctx) {
    return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector token carries no tenant' } });
  }
  try {
    const result = await gdpr.executeErasureByExternalRef(
      parsed.data.externalRef, ctx.connectorId, ctx.tenantId, ctx.organizationId,
    );
    return res.json({ success: true, data: result });
  } catch (err) {
    // Deliberately no logger import in this file: `utils/logger` pulls in
    // `config.ts`, which THROWS at module load when DATABASE_URL is unset, and
    // that kills three unit suites that import this router before a single test
    // runs — an import-throw reads as a clean zero. (The BACKLOG entry that
    // recorded this was closed by #791 once the four suites were shown to run;
    // the import hazard it describes is still real, which is why the constraint
    // stays here rather than following the entry out.)
    //
    // Peter F7: the old comment claimed "the pg code is still classified so the
    // response shape stays right". It was not — `extractPgCode` is pure and its
    // return was discarded, and both handlers answer a fixed 500 either way. His
    // reading of how it got here is correct: `mapGdprWriteDbError` maps 22P02 to
    // 404 and this operation must never 404, so it was rightly abandoned and the
    // vestigial call came along for the ride. Removed rather than re-described.
    // Peter F1's tenancy case is TERMINAL and a caller fault: answer 403 so S
    // stops, rather than a 5xx it would retry without bound forever.
    return sendConnectorRefusal(res, err, 'Erasure failed');
  }
});

gdprRouter.get('/erasures/:externalRef', requireRole(...CONNECTOR_ROLES), async (req: Request, res: Response) => {
  const ctx = connectorContext(req);
  if (!ctx) {
    return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Connector token carries no tenant' } });
  }
  // Peter F10. The spec declared 400 on this operation and nothing could
  // produce one — while the POST validated the identical value. Same schema on
  // both, so the declared status code is now reachable and the two ops agree on
  // what an external_ref is.
  const parsedRef = ExternalRefSchema.shape.externalRef.safeParse(req.params.externalRef);
  if (!parsedRef.success) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'externalRef must be 1-128 characters' } });
  }
  try {
    const result = await gdpr.getErasureStatusByExternalRef(parsedRef.data, ctx.tenantId, ctx.organizationId);
    return res.json({ success: true, data: result });
  } catch (err) {
    return sendConnectorRefusal(res, err, 'Status read failed');
  }
});

gdprRouter.post('/erasure/:userId', requireRole('SYSTEM_ADMIN'), async (req: Request, res: Response) => {
  try {
    const { dsrId, performedBy } = req.body;
    if (!dsrId || !performedBy) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'dsrId and performedBy are required' } });
    }

    const result = await gdpr.executeErasure(req.params.userId, dsrId, performedBy);
    res.json({
      success: result.success,
      message: result.success ? 'User data erased successfully' : 'Erasure partially failed',
      deletionLog: result.deletionLog,
    });
  } catch (err: any) {
    fail500(res, 'GDPR erasure failed (POST /api/gdpr/erasure/:userId)', err);
  }
});

// =============================================================================
// DATA RETENTION POLICIES
// =============================================================================

/** Get all retention policies */
gdprRouter.get('/retention', async (_req: Request, res: Response) => {
  try {
    const policies = await gdpr.getRetentionPolicies();
    res.json({ success: true, policies });
  } catch (err: any) {
    fail500(res, 'GDPR retention policy read failed (GET /api/gdpr/retention)', err);
  }
});

/** Trigger manual retention enforcement (admin) */
gdprRouter.post('/retention/enforce', requireRole('SYSTEM_ADMIN'), async (_req: Request, res: Response) => {
  try {
    const logs = await gdpr.enforceRetention();
    res.json({
      success: true,
      message: `Retention enforcement complete. ${logs.length} data types processed.`,
      deletionLog: logs,
    });
  } catch (err: any) {
    fail500(res, 'GDPR retention enforce failed (POST /api/gdpr/retention/enforce)', err);
  }
});

// =============================================================================
// DELETION LOG
// =============================================================================

/** Get deletion audit trail (admin). KS-694: gated unconditionally — see /dsr/pending. */
gdprRouter.get('/deletion-log', requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), async (req: Request, res: Response) => {
  try {
    const { userId } = req.query;
    const logs = await gdpr.getDeletionLog(userId as string | undefined);
    res.json({ success: true, logs });
  } catch (err: any) {
    fail500(res, 'GDPR deletion log read failed (GET /api/gdpr/deletion-log)', err);
  }
});
