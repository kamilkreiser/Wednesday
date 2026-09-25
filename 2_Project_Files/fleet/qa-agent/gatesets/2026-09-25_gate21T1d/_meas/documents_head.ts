/**
 * =============================================================================
 * DOCUMENT ROUTES
 * =============================================================================
 * API endpoints for document management, signing, and verification.
 * All persistence is delegated to documentRepo (DB + in-memory fallback).
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { body, param, validationResult } from 'express-validator';
import { v4 as uuidv4 } from 'uuid';
import crypto from 'crypto';

import {
  DocumentRecord,
  getDocument,
  listDocuments,
  saveDocument,
  updateDocument,
  getSigningRequest,
  saveSigningRequest,
  deleteSigningRequest,
  generateContentHash,
  seedDemoDocuments,
  assertNoCycle,
  getOrganizationExternalRef,
} from '../repositories/documentRepo';
import { logger } from '../utils/logger';
// KS-564: connector principals are not UUIDs; SQLSTATE mapping turns an
// unstorable-input failure into an honest 400 instead of a retryable 500.
import { toActorUuid } from '../utils/principalId';
import { extractPgCode } from '../utils/pgErrors';
import { publishEvent, EventTypes } from '../events';
import { authenticate } from '../middleware/auth';
import { isAllowedByRoleOrScope } from '../middleware/rbac';
import { normaliseOrgId } from '../services/orgId';
import { DOCUMENT_WRITE_ROLES } from '../middleware/documentWriteRoles';
import { sanitizeString } from '@secuura/shared/security';
import { verifyMessageSignature, hasNulByte, runWithTenantId } from '@secuura/shared';
import { mintAndRegisterThreadToken } from '../services/threadTokenClient';
import { pollAnchorUntilConfirmed, reconcileDocumentAnchorState } from '../services/anchorStateSync';
import { simulatedFieldsFromAnchor, composeHonestBlockchainBlob } from '../services/anchorHonesty';
import { createShare, type ShareType } from '../repositories/shareRepo';
import { createLifecycleEvent, setLifecycleEventAnchor, listLifecycleEvents } from '../repositories/lifecycleEventRepo';
import { LIFECYCLE_EVENT_ACTIONS, type LifecycleEventAction } from '../lifecycleActions';
import { SAFE_ID_PATTERN } from '../originate.openapi';
import {
  extractOnBehalfOf,
  resolveOnBehalfOf,
  recordActionProvenance,
  getCreationProvenance,
  wasCreatedByConnector,
  OnBehalfOfError,
  type OnBehalfOf,
} from '../services/provenance';

export const documentsRouter = Router();

/**
 * KS-480 §6 — handler-side onBehalfOf hook for the action endpoints
 * (version / share / transfer-custody / lifecycle-events; create has its own
 * inline flow because it also overrides owner_user_id). Validates the field
 * (connector-only, 400 on shape), resolves it against the key's org (403
 * cross-org), and appends the provenance row fire-and-forget.
 *
 * KS-564: also RETURNS the resolved user id. `/share` and `/lifecycle-events`
 * write an actor into a `UUID` column, and a connector principal
 * (`connector:<platform>:<id>`) is not a UUID — with a resolved same-org user
 * available, the row gets true per-user attribution instead of NULL.
 *
 * KS-1228: split in two, because recording the row as part of the check wrote it BEFORE the
 * refusals that follow in /version, /share and /transfer-custody. A refused request then left a
 * row for an action that never happened, and `action_provenance.document_id` is deliberately not a
 * foreign key (migrations/041), so nothing downstream rejects it. `checkOnBehalfOf` validates and
 * resolves where the handler always did, so a bad onBehalfOf still refuses first;
 * `recordOnBehalfOf` writes the row, and each handler calls it only once its action has happened.
 *
 * @returns `{ ok: true, obo, resolvedUserId }` to continue the handler
 *          (`resolvedUserId` is null when there was no onBehalfOf or it did not
 *          resolve); `{ ok: false }` when an error response was already sent.
 */
type CheckedOnBehalfOf = { ok: boolean; obo: OnBehalfOf | null; resolvedUserId: string | null };

async function checkOnBehalfOf(req: Request, res: Response): Promise<CheckedOnBehalfOf> {
  try {
    const obo = extractOnBehalfOf(req);
    const resolvedUserId = obo
      ? await resolveOnBehalfOf(obo, (req as any).user?.organizationId as string | undefined)
      : null;
    return { ok: true, obo, resolvedUserId };
  } catch (oboErr) {
    if (oboErr instanceof OnBehalfOfError) {
      res.status(oboErr.status).json({ success: false, error: { code: oboErr.code, message: oboErr.message } });
      return { ok: false, obo: null, resolvedUserId: null };
    }
    throw oboErr;
  }
}

/** Fire-and-forget: attribution must never fail the domain write. No row without an onBehalfOf. */
function recordOnBehalfOf(req: Request, documentId: string, action: string, checked: CheckedOnBehalfOf): void {
  if (!checked.obo) return;
  recordActionProvenance({
    documentId,
    action,
    tenantId: getReqTenantId(req),
    organizationId: (req as any).user?.organizationId as string | undefined,
    connectorId: (req as any).user?.userId as string | undefined,
    obo: checked.obo,
    resolvedUserId: checked.resolvedUserId,
  }).catch((provErr: Error) => logger.warn('provenance record failed', { documentId, action, error: provErr.message }));
}

/**
 * KS-566 — CONNECTOR-pattern provenance (Kam's G-1 ruling, 2026-08-05 /
 * KS-539): `anchor` and `lifecycle` attribute to the key that acted, never to
 * a caller-supplied principal.
 *
 * This exists because of what the 2026-08-22 measurement found, which the
 * ticket does not state: `handleOnBehalfOf` was the ONLY writer of an
 * `action_provenance` row and fired ONLY when the caller supplied
 * `onBehalfOf`. All 4,641 rows on demo carry the full triplet; zero
 * connector-only rows exist. So removing the field from lifecycle-events, as
 * the ticket asks, would have left the route writing NO provenance row at all
 * — trading a named actor for no actor on one of S's two highest-traffic
 * routes. One row per connector operation, attributed to the key.
 *
 * Interactive (JWT) callers write NO row, deliberately: their identity is the
 * JWT and it is already stored in the operation's own actor column. A
 * connector row for a human would be a false attribution.
 *
 * Fire-and-forget — attribution must never fail the domain write.
 */
function recordConnectorProvenance(req: Request, documentId: string, action: string): void {
  const user = (req as any).user;
  if (user?.role !== 'connector') return;
  recordActionProvenance({
    documentId,
    action,
    tenantId: getReqTenantId(req),
    organizationId: user?.organizationId as string | undefined,
    connectorId: user?.userId as string | undefined,
    obo: null,
  }).catch((provErr: Error) =>
    logger.warn('connector provenance record failed', { documentId, action, error: provErr.message }),
  );
}

// All routes here require an authenticated Bearer JWT. Audit A-09 + A-01:
// previously trusted client-supplied x-user-* headers via getUserFromRequest;
// the gateway now strips those (commit c796138f0) and this enforces real
// authentication as defense in depth.
documentsRouter.use(authenticate());

// KS-87: companion router for public `/api/documents/*` endpoints — currently
// only GET /:id/sig-json (the .sig.json envelope an offline verifier needs).
// Mounted in index.ts BEFORE documentsRouter so Express resolves the specific
// public route before falling through to the auth-gated catch-all. Keep this
// router minimal — any handler added here is reachable without a Bearer JWT.
export const publicDocumentsRouter = Router();

// =============================================================================
// KS-466 §8 — reject charset-illegal path ids before any DB work
// =============================================================================
// The published spec constrains every `{id}` path param to SAFE_ID_PATTERN
// (originate.openapi.ts idPathParams), but nothing enforced it at runtime, so
// a malformed id (e.g. the C1 control %C2%84) flowed into repo queries and
// surfaced as a raw 500. Same reject-before-cast pattern as KS-451/KS-367.
// router.param covers every current and future `:id` route on both routers.
const rejectMalformedIdParam = (
  _req: Request,
  res: Response,
  next: (err?: unknown) => void,
  value: string,
) => {
  if (!SAFE_ID_PATTERN.test(value)) {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message:
          'Invalid document id in path: expected 1-128 chars, alphanumeric plus `.`, `_`, `-`, starting alphanumeric',
      },
    });
  }
  next();
};
documentsRouter.param('id', rejectMalformedIdParam);
publicDocumentsRouter.param('id', rejectMalformedIdParam);


// =============================================================================
// SEED on module load (non-production only)
// =============================================================================

seedDemoDocuments().catch((err) =>
  logger.error('Failed to seed demo documents', { error: err instanceof Error ? err.message : String(err) }),
);

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function getUserFromRequest(req: Request): { id: string; walletAddress?: string } | null {
  // Pen-test F-04: read from authenticated req.user (set by authenticate()
  // middleware), NOT from raw headers. Direct header reads are spoofable
  // by anyone reaching the service directly.
  const user = (req as any).user;
  const userId = user?.userId;
  if (!userId) return null;

  return {
    id: userId,
    walletAddress: user?.walletAddress,
  };
}

/**
 * KS-4: every documentRepo call must be tenant-scoped. `req.tenantId` is
 * normally set by extractTenantContext from `x-tenant-id` — which the
 * gateway derives from the JWT (or, for super_admins, overrides via
 * X-Tenant-Override). The middleware is mounted only when
 * MULTI_TENANCY_ENABLED === 'true'; in single-tenancy mode it never runs
 * and req.tenantId stays undefined. In that case fall back to the same
 * default tenant id that extractTenantContext itself falls back to in
 * non-prod — the migration backfills all rows into this tenant when no
 * other source is available, so queries still match the right rows.
 */
const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';

// KS-199: issuerName (the on-chain organisation name) is optional. A user
// without an organisation (public tenant) uploads without one, and we anchor
// under this neutral, fixed, non-PII label rather than requiring a dummy org.
// Audit E-01 still holds: we never fall back to the user's email/name. Once a
// user has an organisation, the org name is supplied explicitly on later writes.
const DEFAULT_ISSUER_NAME = 'Individual';

function getReqTenantId(req: Request): string {
  const tid = (req as any).tenantId as string | undefined;
  return tid || DEFAULT_TENANT_ID;
}

// =============================================================================
// ROUTES
// =============================================================================

/**
 * GET /api/documents
 * List documents for the current user (admins can see all)
 */
documentsRouter.get(
  '/',
  async (req: Request, res: Response) => {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = Math.min(parseInt(req.query.limit as string) || 50, 100);
      const statusFilter = req.query.status as string | undefined;

      let result: { items: any[]; total: number };
      try {
        result = await listDocuments(getReqTenantId(req), { status: statusFilter, page, limit }, (req as any).db);
      } catch (dbErr: any) {
        // If the documents table doesn't exist in this context, return empty
        if (dbErr?.message?.includes('does not exist')) {
          result = { items: [], total: 0 };
        } else {
          throw dbErr;
        }
      }
      const { items } = result;

      // Filter by ownership unless user is admin
      // Pen-test F-04: read from authenticated req.user (set by authenticate()
      // middleware), NOT from raw headers.
      const user = (req as any).user;
      const userId = user?.userId as string | undefined;
      const userRole = user?.role as string | undefined;
      const isAdmin = userRole === 'system_admin' || userRole === 'SYSTEM_ADMIN' || userRole === 'super_admin';

      // F-HOLDER-01 + H22 (F-HOLDER-03 from 2026-04-28): the OWNER role
      // is "credential holder" — the person credentials are issued TO,
      // distinct from the creator. Three-way OR captures every legitimate
      // shape of "doc is mine":
      //   - owner.id === userId        — I created it
      //   - rightsHolderId === userId  — issuance populated rights_holder_id
      //                                  with my user-id (preferred long-term
      //                                  shape; needs auth-service lookup at
      //                                  POST time, not yet wired)
      //   - data.recipientEmail === me — issuance set my email at create
      //                                  time. The current shape until the
      //                                  email→user-id lookup lands.
      // H22 origin: Oxford registrar issued a degree with recipientEmail
      // set to alice@…; Alice's GET /api/documents returned 0 docs because
      // the filter only checked the first two paths and rights_holder_id
      // is empty on every current doc.
      const userEmail = String((user as any)?.email || '').toLowerCase();
      let filteredItems = items;
      if (userId && !isAdmin) {
        filteredItems = items.filter((d) => {
          if (d.owner?.id === userId) return true;
          if (d.rightsHolderId === userId) return true;
          const recipientEmail = String(
            (d.data as Record<string, unknown> | undefined)?.recipientEmail || '',
          ).toLowerCase();
          if (userEmail && recipientEmail && userEmail === recipientEmail) {
            return true;
          }
          return false;
        });
      }

      res.json({
        documents: filteredItems.map((d) => ({
          id: d.id,
          // KS-596 Phase B: canonical UUID alongside the legacy id on reads.
          documentUuid: d.documentUuid ?? null,
          title: (d.data?.title as string) || d.type || 'Untitled',
          documentType: (d.data?.documentType as string) || d.type,
          status: d.status,
          contentHash: d.contentHash,
          createdAt: d.createdAt,
          updatedAt: d.updatedAt,
        })),
        total: filteredItems.length,
        page,
        limit,
      });
    } catch (error) {
      logger.error('Failed to list documents', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list documents' } });
    }
  },
);

// KS-596: S-supplied identifier shapes. documentUuid is contractually v4
// (version nibble 4, variant 8/9/a/b); userUuid / organizationUuid accept any
// RFC 4122 version.
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const UUID_V4_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
// KS-596: hash equality for the idempotency rule must survive the P5 hygiene
// gap (`sha256:`-prefixed vs bare, mixed case both live in the DB today).
const normaliseHash = (h: unknown): string => String(h ?? '').replace(/^sha256:/i, '').toLowerCase();

/**
 * POST /api/documents
 * Create a new document.
 * Accepts two payload shapes for backward compatibility:
 *   Legacy:   { type, data: { ... } }
 *   Frontend: { title, documentType, contentHash, description }
 */
documentsRouter.post(
  '/',
  async (req: Request, res: Response) => {
    try {
      const owner = getUserFromRequest(req);
      if (!owner) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      // RBAC: role allow-list OR scope-based grant (KS-71).
      // Pen-test F-04: read role from authenticated req.user, NOT raw headers.
      // KS-71: `sk_*` connector callers carry `role='connector'` (not in the
      // allow-list) but a `documents:write` scope validated by the gateway.
      // The helper accepts either path so scoped connectors aren't 403'd.
      const ALLOWED_CREATION_ROLES = DOCUMENT_WRITE_ROLES;
      if (!isAllowedByRoleOrScope(req, ALLOWED_CREATION_ROLES, 'documents:write')) {
        return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Forbidden: your role does not permit document creation' } });
      }

      // KS-480 §6: connector attribution — validate the optional onBehalfOf
      // triplet (connector-only; JWT callers 400) and resolve it tenant-scoped
      // against the key's own Organisation (same-org user → owner_user_id;
      // different org → 403; no user → verbatim provenance row).
      let onBehalfOf: OnBehalfOf | null = null;
      let oboResolvedUserId: string | null = null;
      try {
        onBehalfOf = extractOnBehalfOf(req);
        if (onBehalfOf) {
          oboResolvedUserId = await resolveOnBehalfOf(onBehalfOf, (req as any).user?.organizationId as string | undefined);
        }
      } catch (oboErr) {
        if (oboErr instanceof OnBehalfOfError) {
          return res.status(oboErr.status).json({ success: false, error: { code: oboErr.code, message: oboErr.message } });
        }
        throw oboErr;
      }

      const {
        type: rawType,
        data: rawData,
        title: rawTitle,
        documentType,
        contentHash: clientHash,
        description: rawDescription,
        requiresWalletSignature,
        recipientEmail,
        // KS-596 (architecture P1, Phase A): optional S-supplied identifiers.
        // documentUuid becomes the registration's external_id; userUuid /
        // organizationUuid are accepted + validated and preserved in metadata
        // (organizationUuid gains column semantics in KS-597).
        documentUuid: rawDocumentUuid,
        userUuid: rawUserUuid,
        organizationUuid: rawOrganizationUuid,
      } = req.body;

      // KS-129: validate negative inputs server-side instead of silently
      // dropping them (secuura-test-kit 2026-05-23 run-02, Phase-05 negatives).
      // Deprecated top-level `content` field is never read here — reject it
      // explicitly so callers fix the payload rather than lose data silently.
      if (req.body.content !== undefined) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: "The 'content' field is not supported; send 'contentHash' (sha256 hex) or 'data' instead" } });
      }
      // KS-444 (KS-440 validation hole): enforce the published
      // DocumentCreateRequest field types — title/documentType are strings and
      // data is an object in the spec, but the handler previously accepted any
      // shape (a fuzzer body with a non-string title or an array data blob
      // would be stored as-is).
      if (rawTitle !== undefined && typeof rawTitle !== 'string') {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'title must be a string' } });
      }
      if (documentType !== undefined && typeof documentType !== 'string') {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'documentType must be a string' } });
      }
      if (rawData !== undefined && (rawData === null || typeof rawData !== 'object' || Array.isArray(rawData))) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'data must be a JSON object' } });
      }
      // KS-451: a U+0000 (NUL) byte in any free-text field reaches Postgres
      // unfiltered (sanitizeString only HTML-escapes; it does not strip NUL) and
      // throws `invalid byte sequence for encoding "UTF8": 0x00` → a raw 500.
      // Reject it here → 400. Covers top-level title/description and the legacy
      // `data.{title,description}` shape this route still accepts.
      if (
        hasNulByte(rawTitle) ||
        hasNulByte(rawDescription) ||
        (rawData && typeof rawData === 'object' && (hasNulByte((rawData as Record<string, unknown>).title) || hasNulByte((rawData as Record<string, unknown>).description)))
      ) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Text fields must not contain a NUL (U+0000) byte' } });
      }

      // KS-596: validate the optional S-supplied identifiers. documentUuid is
      // contractually v4 (S generates it per registration — plan sheet P1);
      // userUuid / organizationUuid accept any RFC 4122 version so S can pass
      // through identifiers it did not mint. Reject malformed values with 400
      // rather than storing a corrupt identity key.
      if (rawDocumentUuid !== undefined && rawDocumentUuid !== null
          && (typeof rawDocumentUuid !== 'string' || !UUID_V4_RE.test(rawDocumentUuid))) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'documentUuid must be a UUID v4 string' } });
      }
      if (rawUserUuid !== undefined && rawUserUuid !== null
          && (typeof rawUserUuid !== 'string' || !UUID_RE.test(rawUserUuid))) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'userUuid must be a UUID string' } });
      }
      if (rawOrganizationUuid !== undefined && rawOrganizationUuid !== null
          && (typeof rawOrganizationUuid !== 'string' || !UUID_RE.test(rawOrganizationUuid))) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'organizationUuid must be a UUID string' } });
      }
      const documentUuid: string | null = typeof rawDocumentUuid === 'string' ? rawDocumentUuid.toLowerCase() : null;
      const sUserUuid: string | null = typeof rawUserUuid === 'string' ? rawUserUuid.toLowerCase() : null;
      const sOrganizationUuid: string | null = typeof rawOrganizationUuid === 'string' ? rawOrganizationUuid.toLowerCase() : null;

      // KS-597 (Kam's ruling, 2026-09-07 -- "bind the issuer to the actor"):
      // `organizationUuid` is attribution the CALLER supplies, so it is bound to
      // the caller's own Organisation and a mismatch is REFUSED rather than
      // quietly folded to NULL. A genuine delegation goes through the existing
      // `onBehalfOf` mechanism, not an unchecked field.
      //
      // This is deliberately the SAME rule `resolveOnBehalfOf` already enforces
      // (`services/provenance.ts:131`), and the same three cases it recognises:
      //   1. claim and caller both present, and the claim names NEITHER of the
      //      acting Organisation's identifiers -> 403 (option B, below).
      //   2. caller has NO Organisation -> no 403, and no attribution either.
      //      `provenance.ts:109` refuses to resolve for the same reason it
      //      gives there: an org-less caller "has no Organisation to validate
      //      against", so resolving "would attribute to ANY matching tenant
      //      user". (The separate phrase "not in a *different* org" belongs to
      //      `:136`, which is the org-less SUBJECT, not the org-less caller --
      //      an earlier revision of this comment borrowed that rationale for
      //      this branch and attributed it to `:109`, which does not say it.)
      //      Here the effect is: nothing can be bound, so the column folds to
      //      NULL and the caller's raw value survives in metadata.
      //      Reachable, not hypothetical -- migration 018 drops NOT NULL on
      //      `svc_api_keys.organization_id` outright (the originate admin
      //      endpoint issuing org-less keys is the migration's stated REASON,
      //      not a per-key condition -- a NOT NULL cannot be dropped
      //      selectively), and the gateway maps a missing connector org to ''
      //      (api-gateway `auth.ts:232`), which `normaliseOrgId` folds to null.
      //   3. no claim -> unchanged. This adds a refusal; it does not make the
      //      field required.
      //
      // Both sides go through the SHARED `normaliseOrgId`, never a private copy:
      // Peter Obeden's #795 review is quoted in `provenance.ts:126` observing
      // that two byte-identical private copies is the arrangement that produced
      // the last drift, and a third copy would re-open it. The normaliser also
      // does the work that makes case 2 correct -- it collapses '' to null.
      const callerOrgId = normaliseOrgId((req as any).user?.organizationId as string | undefined);
      const claimedOrgId = normaliseOrgId(sOrganizationUuid);
      // KS-597 option B (Kam's ruling, 2026-09-11 -- "K resolves S's externalRef,
      // then compares"): the claim may name the acting Organisation by EITHER of
      // its identifiers -- K's `organizations.id`, or the `externalRef` that
      // Organisation was registered with. register-connector stores Platform S's
      // Organisation GUID there (api-gateway `routes/platform.ts`), and S sends
      // that GUID here, so comparing the raw claim to K's id refused every S
      // originate (Stuart on KS-597, 2026-09-10: 144 refusals in 45 minutes).
      //
      // The read is CALLER-SCOPED -- the caller's own row, by id and request
      // tenant -- and never a lookup of the claim. `externalRef` has no unique
      // index and register-connector's idempotency is a lockless
      // check-then-insert, so resolving the CLAIM could pick one of two
      // Organisations sharing a ref by chance; resolving the CALLER cannot, and
      // it is the only resolution that could ever pass this comparison.
      //
      // It goes through `req.db`, the tenant-GUC client: `organizations` is under
      // fail-closed RLS (migration 039), and the same read with no tenant scope
      // returns nothing (`ks597-b-caller-org-externalref.integration.test.ts`). A
      // failed read throws to the handler's 500 -- never folded into an accept,
      // and never disguised as this refusal.
      if (claimedOrgId && callerOrgId && claimedOrgId !== callerOrgId) {
        const callerExternalRef = await getOrganizationExternalRef(callerOrgId, getReqTenantId(req), (req as any).db);
        if (normaliseOrgId(callerExternalRef) !== claimedOrgId) {
          return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'organizationUuid differs from the acting Organisation' } });
        }
      }
      // Only a claim bound to the acting Organisation reaches the column. The
      // repository still resolves it through a tenant-scoped SELECT (defence in
      // depth): there is no database backstop to fall back on, because the two
      // provisioning paths disagree -- `docker/init/01-schema.sql:125` declares
      // `issuer_organization_id UUID` with NO foreign key while
      // `migrations/001_initial-schema.sql:105` declares one, and no migration
      // ever adds it to an already-created table. MEASURED, not inferred: on a
      // database built from `docker/init` + `run-migrations.sh` (applied=48
      // failed=0) the column carries ZERO foreign-key constraints, against a
      // control showing `documents` does carry one elsewhere -- so the query
      // discriminates and the zero is real.
      // Under option B both accepted identifiers bind to the acting Organisation's
      // K id; S's GUID is never the column value and stays in `metadata.sIdentity`
      // as what the caller sent.
      const boundIssuerOrgId: string | null = claimedOrgId && callerOrgId ? callerOrgId : null;

      // Malformed contentHash — accept a bare hex digest or an optional
      // `sha256:` prefix (mirrors the version-create + verification paths via
      // CONTENT_HASH_RE); reject anything else with 400 rather than storing it.
      if (clientHash !== undefined && clientHash !== null) {
        const normalisedClientHash = String(clientHash).replace(/^sha256:/i, '').toLowerCase();
        if (!CONTENT_HASH_RE.test(normalisedClientHash)) {
          return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'contentHash must be a sha256 hex digest (64 lowercase hex chars, optional sha256: prefix)' } });
        }
      }

      // F-10 (audit 2026-05-15): defence-in-depth XSS escape on free-text
      // fields. The gateway's `sanitizeInput` middleware skips body parsing
      // for /api/documents (it's in `proxyPaths`, since the gateway proxies
      // the raw stream to originate). Without sanitisation here, raw
      // `<script>` / `<img onerror=...>` payloads land in the DB. React
      // text-encodes on render so live portals are safe today; this protects
      // PDF / CSV / mobile-native render paths and any future
      // `dangerouslySetInnerHTML` consumer.
      const title = typeof rawTitle === 'string' ? sanitizeString(rawTitle) : rawTitle;
      const description = typeof rawDescription === 'string' ? sanitizeString(rawDescription) : rawDescription;

      // Validate required fields.
      // KS-444 (closes the KS-440 hole): the published DocumentCreateRequest
      // declares `title` REQUIRED, but the handler accepted any body that
      // carried a `data` object — a fuzzer body with no title anywhere was
      // stored as an untitled document (negative_data_rejection 201). Require
      // a title: top-level `title` per the spec, or `data.title` for the
      // legacy `{type, data}` shape this route still supports.
      const docTitle = title || (typeof rawData?.title === 'string' && rawData.title ? rawData.title : undefined);
      if (!docTitle) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Document title is required (top-level `title`, or `data.title` in the legacy shape)' } });
      }

      const docType: string = documentType || rawType || 'DOCUMENT';

      // KS-1202: the type a document is SERVED as is `data.documentType || type`
      // (GET /:id and the list), but the type that was checked and stored is
      // docType. A caller could send an allowed type with a different
      // `data.documentType` and have the document served, and verified, as that
      // other type. A `data.documentType` that is present must equal docType.
      // Refused rather than overwritten: `data` is the caller's blob and the
      // content hash covers it.
      const dataDocumentType = rawData && typeof rawData === 'object' ? (rawData as Record<string, unknown>).documentType : undefined;
      if (dataDocumentType !== undefined && dataDocumentType !== docType) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'data.documentType must equal the document type (documentType, or type)' } });
      }

      const data: Record<string, unknown> =
        rawData && typeof rawData === 'object'
          ? { ...rawData, title: typeof rawData.title === 'string' ? sanitizeString(rawData.title) : rawData.title, description: typeof rawData.description === 'string' ? sanitizeString(rawData.description) : rawData.description }
          : { title, documentType: docType, contentHash: clientHash, description };

      if (title && !data.title) data.title = title;
      if (description && !data.description) data.description = description;
      if (documentType && !data.documentType) data.documentType = documentType;
      // H22: persist recipientEmail into the document's data blob if the
      // caller passed it at the top level. The list-side filter at line
      // ~111 reads d.data.recipientEmail to surface the doc on the named
      // holder's wallet view. Without this line, top-level recipientEmail
      // was being dropped before save, so holders never saw their own
      // credentials.
      if (recipientEmail && typeof recipientEmail === 'string' && !data.recipientEmail) {
        data.recipientEmail = recipientEmail;
      }

      // KS-549: persist a top-level issuerName into the data blob (same
      // top-level-field pattern as recipientEmail above). It was previously
      // only forwarded to the anchoring request body, so connector-originated
      // documents (S sends issuerName top-level per PS-496) resolved
      // `issuer: null` on every verify — all fallback sources were empty.
      // The E-01 no-emails guard below still 400s an "@"-carrying value; the
      // same condition here keeps an email out of the stored blob.
      const topLevelIssuerName =
        typeof req.body?.issuerName === 'string' ? req.body.issuerName.trim() : '';
      // KS-1265: refuse an "@"-carrying issuerName BEFORE the save below (it was refused at the anchoring
      // step, AFTER saveDocument and the provenance row) - a refused create must write nothing.
      if (topLevelIssuerName.includes('@')) {
        return res.status(400).json({
          success: false,
          error: { code: 'BAD_REQUEST', message: 'issuerName must not contain "@" - it should be the organisation name, not a user email (audit E-01)' },
        });
      }
      if (topLevelIssuerName && !topLevelIssuerName.includes('@') && !data.issuerName) {
        data.issuerName = topLevelIssuerName;
      }

      // KS-480 §6: `onBehalfOf` is a reserved provenance key — it must never
      // ride inside the content-addressed data blob (erasure would break the
      // content hash) and a caller must not be able to plant fake provenance.
      // It lives in action_provenance only.
      delete (data as Record<string, unknown>).onBehalfOf;

      // KS-596: an S-supplied documentUuid becomes the registration's
      // external_id (the column is UNIQUE); absent, K mints exactly as before.
      const id = documentUuid ?? `doc-${Date.now()}-${uuidv4().slice(0, 8)}`;
      const now = new Date().toISOString();
      const hash = clientHash || generateContentHash(data);

      // KS-4: tenantId is required for the tenant-scoped INSERT. Captured
      // here so the fire-and-forget closures below (anchor poll, thread
      // token, etc.) can reuse it from the request scope without the route
      // handler needing to stay alive.
      const tenantId = getReqTenantId(req);

      // KS-596 ruled idempotency (Kam 2026-08-10, ruling b): re-POST of a
      // seen documentUuid with the SAME content hash returns the existing
      // registration (a retry can never mint a phantom second document);
      // the same documentUuid with DIFFERENT bytes is 409 — surfacing an
      // S-side duplicate-UUID bug instead of masking it (S-pack §3.2).
      // Tenant-scoped by construction: external_id is unique per tenant DB.
      const respondForExisting = async (): Promise<boolean> => {
        if (!documentUuid) return false;
        const existing = await getDocument(documentUuid, tenantId, (req as any).db);
        if (!existing) return false;
        // getDocument also matches on the internal UUID pkey; a supplied
        // documentUuid that shadows ANOTHER document's pkey must refuse (it
        // is already a working lookup key for that document), same as a
        // byte mismatch. Only an external_id match can be idempotent.
        const matchedOnExternalId = existing.id.toLowerCase() === documentUuid;
        if (matchedOnExternalId && normaliseHash(existing.contentHash) === normaliseHash(hash)) {
          res.setHeader('Location', `/api/documents/${existing.id}`);
          res.status(200).json({
            id: existing.id,
            documentUuid: existing.documentUuid ?? documentUuid,
            type: existing.type,
            status: existing.status,
            contentHash: existing.contentHash,
            txHash: existing.blockchain?.txHash ?? null,
            createdAt: existing.createdAt,
            requiresWalletSignature: existing.status === 'pending_signature',
          });
          return true;
        }
        res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'documentUuid is already registered with different content' } });
        return true;
      };
      if (await respondForExisting()) return;

      const document: DocumentRecord = {
        id,
        type: docType,
        status: requiresWalletSignature ? 'pending_signature' : 'draft',
        owner,
        data,
        contentHash: hash,
        signatures: [],
        createdAt: now,
        updatedAt: now,
      };

      // KS-480 §6: a same-org resolved user becomes the document's
      // owner_user_id (true per-user attribution); the document stays
      // org-owned either way.
      // KS-596: with an S-supplied documentUuid the insert must NOT upsert —
      // a concurrent duplicate has to surface (inserted:false), not merge.
      const saved = await saveDocument(document, tenantId, (req as any).db, {
        ...(oboResolvedUserId ? { ownerUserIdOverride: oboResolvedUserId } : {}),
        ...(documentUuid ? { conflictMode: 'skip' as const } : {}),
        ...(sUserUuid || sOrganizationUuid
          ? { sIdentity: { ...(sUserUuid ? { userUuid: sUserUuid } : {}), ...(sOrganizationUuid ? { organizationUuid: sOrganizationUuid } : {}) } }
          : {}),
        // KS-597: the column carries only what the route could BIND to the
        // acting Organisation; `sIdentity` above still carries the caller's raw
        // claim for the metadata. They differ exactly when the claim could not
        // be bound, which is the distinction the column is for.
        issuerOrganizationId: boundIssuerOrgId,
      });
      if (documentUuid && !saved.inserted) {
        // A concurrent registration with the same documentUuid won the race
        // between the pre-check and the insert — apply the same rule to the
        // row that got there first.
        if (await respondForExisting()) return;
        // The conflicting row vanished between the two checks (deleted mid-
        // race); treat as a retryable conflict rather than inventing a state.
        return res.status(409).json({ success: false, error: { code: 'CONFLICT', message: 'documentUuid registration raced a concurrent request; retry' } });
      }
      const responseDocumentUuid = documentUuid ?? saved.dbId;

      if (onBehalfOf) {
        recordActionProvenance({
          documentId: id,
          action: 'create',
          tenantId,
          organizationId: (req as any).user?.organizationId as string | undefined,
          connectorId: owner.id,
          obo: onBehalfOf,
          resolvedUserId: oboResolvedUserId,
        }).catch((provErr: Error) => logger.warn('provenance record failed', { documentId: id, error: provErr.message }));
      }

      // Register in platform cross-tenant registry (fire-and-forget)
      // Pen-test F-04: tenant slug from req.user, NOT from raw headers.
      const { registerInPlatformRegistry } = require('./verification');
      registerInPlatformRegistry({
        documentId: id, contentHash: hash, tenantId,
        tenantSlug: (req as any).user?.tenantSlug as string | undefined,
        documentType: docType, title: title, status: document.status,
      }).catch(() => {});

      // Publish document.created event (fire-and-forget)
      publishEvent(EventTypes.DOCUMENT_CREATED, {
        documentId: id,
        documentType: docType,
        contentHash: hash,
        ownerId: owner.id,
        status: document.status,
      }).catch(() => {});

      // F6 Sprint 2 Phase 2 part B — fire-and-forget thread-token mint+lock.
      // Gated on STATE_THREAD_NFT_ENABLED to keep tADA spend opt-in until
      // the burn-watcher (Phase 2 part C) lands. When enabled, anchoring
      // mints a per-document thread NFT, locks the initial Draft datum at
      // the parameterised document_contract address, and persists the
      // (policy_id, script_address, mint_tx_hash, seed) into
      // state_thread_registry. Failures are logged but do NOT block document
      // creation — the legacy metadata-label anchor still happens below.
      if (
        process.env.STATE_THREAD_NFT_ENABLED === 'true' &&
        process.env.SIMULATE_ANCHORING !== 'true'
      ) {
        const bearerToken = (req.headers.authorization as string) || '';
        // Originator PKH: prefer the explicit field on the user; fall back
        // to a deterministic blake2b-derived bytes from owner.id so the
        // PKH is always 28 bytes hex even if not yet wired through auth.
        const originatorPkhHex =
          ((req as any).user?.pkh as string) ||
          crypto.createHash('sha256').update(owner.id).digest().toString('hex').slice(0, 56);
        const metadataHashHex = crypto
          .createHash('sha256')
          .update(JSON.stringify(data))
          .digest()
          .toString('hex');

        mintAndRegisterThreadToken({
          documentId: id,
          documentHashHex: hash.replace(/^sha256:/i, '').toLowerCase(),
          originatorPkhHex,
          documentType: docType,
          metadataHashHex,
          deploymentIdHex: '',
          createdAtMs: Date.now(),
          bearerToken,
        })
          .then((entry) => {
            logger.info('thread-token minted at document create', {
              documentId: id,
              policyId: entry.policyId,
              mintTxHash: entry.mintTxHash,
            });
            // Surface the thread-token info on the document record so
            // dashboards can show it without a separate lookup. The
            // canonical truth is state_thread_registry; this is a cache.
            updateDocument(id, tenantId, {
              blockchain: {
                ...(document.blockchain || {}),
                threadToken: {
                  policyId: entry.policyId,
                  scriptAddress: entry.scriptAddress,
                  mintTxHash: entry.mintTxHash,
                  network: entry.network,
                },
              },
            }).catch(() => {});
          })
          .catch((err: any) => {
            logger.warn('thread-token mint failed (document still created via legacy path)', {
              documentId: id,
              error: err?.message,
            });
          });
      }

      // Auto-anchor on blockchain (fire-and-forget — does not block the response)
      const anchoringBaseUrl = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
      const anchorUrl = `${anchoringBaseUrl}/api/anchors`;
      const simulateAnchoring = process.env.SIMULATE_ANCHORING === 'true';
      // F-CHAIN-VERIFY-AUTH-01 / -02 (2026-05-02): the anchoring service
      // mounts authenticate() on /api/* — every call from originate must
      // forward the caller's bearer or anchoring returns 500 "No token
      // provided". Capture once at the top of the auto-anchor scope so
      // every fetch below uses the same value (poll loop, anchor POST,
      // status GET).
      const anchoringAuth = (req.headers.authorization as string) || '';
      // KS-566: `x-emitter-internal` marks K's own hop so anchoring does not
      // write a second provenance row — POST /api/documents already wrote the
      // `create` row for this same user action. See emitLifecycleAnchor.
      const anchoringHeaders: Record<string, string> = {
        'x-emitter-internal': 'originate-create',
        ...(anchoringAuth ? { Authorization: anchoringAuth } : {}),
      };
      // KS-199: issuerName (the organisation name) is OPTIONAL — a user without
      // an organisation (public tenant) may upload without it, and we anchor
      // under the neutral DEFAULT_ISSUER_NAME rather than forcing a dummy org.
      // Audit E-01 still holds: we never fall back to the user's email/PII —
      // previously a missing org meant x-user-email could land verbatim on the
      // Cardano chain (immutable, public, forever). The gateway also strips x-*
      // trust headers (commit c796138f0). The default is a fixed non-PII label.
      const issuerOrgId = (req.body && (req.body.issuerOrgId || req.body.organizationId)) || owner.id;
      const suppliedIssuerName = req.body && typeof req.body.issuerName === 'string'
        ? req.body.issuerName.trim()
        : '';
      // Defensive: a *supplied* issuerName must not be an email (contains "@") —
      // the caller almost certainly mis-mapped a field, and the old email
      // fallback put PII on-chain (audit E-01). Empty is fine — it defaults below.
      if (suppliedIssuerName.includes('@')) {
        return res.status(400).json({
          success: false,
          error: { code: 'BAD_REQUEST', message: 'issuerName must not contain "@" — it should be the organisation name, not a user email. The previous fallback put emails on-chain (audit E-01); this guard exists to prevent the same mistake at the call site.' },
        });
      }
      const issuerName = suppliedIssuerName.length > 0 ? suppliedIssuerName : DEFAULT_ISSUER_NAME;

      const buildAnchorBody = () => JSON.stringify({
        documentId: id,
        contentHash: hash,
        network: process.env.CARDANO_NETWORK || 'preprod',
        environment: process.env.SECUURA_ENVIRONMENT || process.env.NODE_ENV || 'unknown',
        issuerOrgId,
        issuerName,
        certId: id,
      });

      // After anchoring accepts the request, poll the anchor resource until it's
      // confirmed on-chain (real txHash + blockHeight) or terminally failed
      // (KS-535: the fail-closed `anchor_failed` shape — previously a failed
      // anchor produced no write and the document claimed `anchored` forever).
      // Extracted to services/anchorStateSync.ts so the manual retry route
      // (POST /:id/anchor) shares it.

      if (simulateAnchoring) {
        const simData = {
          txHash: `tx_sim_${crypto.randomBytes(32).toString('hex')}`,
          blockHeight: 0,
          anchoredAt: new Date().toISOString(),
          simulated: true,
        };
        updateDocument(id, tenantId, { blockchain: simData, status: 'anchored' }).catch(() => {});
        logger.warn('SIMULATE_ANCHORING=true — simulated anchor applied immediately', { documentId: id });
      } else {
        // Cardano anchor — fire-and-forget relative to the HTTP response.
        fetch(anchorUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', ...anchoringHeaders },
          body: buildAnchorBody(),
        })
          .then(async (anchorResp) => {
            if (!anchorResp.ok) {
              throw new Error(`Anchoring service returned ${anchorResp.status}`);
            }
            const anchorResult = (await anchorResp.json()) as any;
            const anchorData = anchorResult.data || anchorResult;
            const anchorId = anchorData.id;
            const initial = {
              txHash: anchorData.txHash || null,
              blockHeight: anchorData.blockHeight || 0,
              anchoredAt: anchorData.anchoredAt || anchorData.createdAt || new Date().toISOString(),
              status: anchorData.status || 'pending',
              anchorId,
              // KS-587 (document-blob leg): carry the anchor's simulation
              // declaration onto the blob from the first write, so a caller
              // reading only the document can tell a mock anchor is not on
              // chain (KS-589 D1) and presentBlockchainHonestly has its input
              // (KS-589 D4). Empty for a real anchor.
              ...simulatedFieldsFromAnchor(anchorData),
            };
            // KS-521: same terminal-status guard as the poll below — this
            // write is fire-and-forget relative to the 201, so an immediate
            // revoke can race it.
            await updateDocument(id, tenantId, { blockchain: initial, status: 'anchored' }, undefined, { preserveTerminalStatuses: true });
            logger.info('Document anchor request accepted — awaiting on-chain confirmation', { documentId: id, anchorId });
            if (anchorId) pollAnchorUntilConfirmed({ anchorId, documentId: id, tenantId, authHeader: anchoringAuth });
          })
          .catch((err: any) => {
            // KS-520: fail CLOSED. Simulation is an explicit opt-in — the
            // SIMULATE_ANCHORING === 'true' branch above never reaches this
            // fetch — so an anchoring failure here must never fabricate a
            // tx_sim_ hash and mark the document anchored: the fabricated
            // hash corresponds to no Cardano transaction and a caller cannot
            // distinguish it from a genuine anchor. Record a retryable
            // failure state instead; the document stays un-anchored (and the
            // public verifier reports it unverified) until a real anchor
            // lands via POST /api/documents/:id/anchor or a recreate.
            logger.error('Auto-anchor failed — document saved without anchor (fail closed; retry via POST /api/documents/:id/anchor)', { documentId: id, error: err?.message });
            updateDocument(id, tenantId, {
              blockchain: {
                status: 'anchor_failed',
                txHash: null,
                blockHeight: 0,
                error: err?.message || 'anchoring unavailable',
                failedAt: new Date().toISOString(),
              },
            }, undefined, { preserveTerminalStatuses: true }).catch(() => {});
          });
      }

      // KS-154: emit RFC 7231 Location header on 201 — points at the
      // canonical resource URL so REST clients can follow without parsing
      // the body. The body still carries `id` for backward compatibility.
      res.setHeader('Location', `/api/documents/${document.id}`);
      res.status(201).json({
        id: document.id,
        // KS-596 Phase B: the canonical UUID rides on every registration
        // response next to the legacy id — the S-supplied documentUuid, or
        // the row's own UUID key (both already resolve via GET /:id).
        documentUuid: responseDocumentUuid,
        type: document.type,
        status: document.status,
        contentHash: document.contentHash,
        // F-DOC-RESP-SHAPE-01 (2026-05-02): always include txHash so the
        // client can distinguish "field absent / unsupported" from "anchor
        // queued, not yet on chain". Auto-anchor is fire-and-forget; the
        // tx hash arrives later (poll the doc by id, or subscribe to
        // events). For SIMULATE_ANCHORING the tx is set synchronously
        // below in updateDocument(); the client will see it on the next
        // GET. For real anchoring on demo, expect the field to remain
        // null until Cardano confirms (~30-60s typical on Preview).
        txHash: null,
        createdAt: document.createdAt,
        requiresWalletSignature: !!requiresWalletSignature,
      });
    } catch (error) {
      logger.error('Failed to create document', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create document' } });
    }
  },
);

/**
 * GET /api/documents/:id
 * Get document details
 */
documentsRouter.get(
  '/:id',
  [param('id').notEmpty().withMessage('Document ID is required')],
  async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      let document: any = null;

      // KS-4: tenant-scoped lookup via req.tenantId (the effective tenant
      // after extractTenantContext resolves any X-Tenant-Override). A
      // super_admin asserting BUPA context will find 0 rows for an
      // Oxford-owned doc — the SELECT now has AND tenant_id = $BUPA.
      const tenantId = getReqTenantId(req);
      try {
        document = await getDocument(id, tenantId, (req as any).db);
      } catch (dbErr: any) {
        // If the table doesn't exist in this DB context, continue to fallback
        if (!dbErr?.message?.includes('does not exist')) throw dbErr;
      }

      // Cross-tenant fallback: only for admins — search the platform_document_registry
      // Pen-test F-04: read role from authenticated req.user, NOT raw headers.
      const userRole = (req as any).user?.role as string | undefined;
      const isAdmin = userRole === 'system_admin' || userRole === 'SYSTEM_ADMIN' || userRole === 'super_admin';
      // BUG-ISOLATION-001 fix (2026-05-02): if the admin explicitly set
      // X-Tenant-Override (i.e., effective tenant ≠ JWT tenant), they
      // are scoped to that override and the cross-tenant fallback MUST
      // NOT leak documents from other tenants.
      const userJwtTenant = (req as any).user?.tenantId as string | undefined;
      const adminUsingOverride = userJwtTenant && userJwtTenant !== tenantId;
      if (!document && isAdmin && !adminUsingOverride) {
        try {
          const { getTenantManager, createPoolProxy } = require('../db');
          const mgr = getTenantManager?.();
          if (mgr) {
            const platformPool = mgr.getPlatformPool?.();
            if (platformPool) {
              const regResult = await platformPool.query(
                'SELECT tenant_id FROM platform_document_registry WHERE document_id = $1 LIMIT 1',
                [id]
              ).catch(() => ({ rows: [] }));
              if (regResult.rows.length > 0) {
                const registryTenant = regResult.rows[0].tenant_id as string;
                const tenantPool = mgr.getPool(registryTenant);
                const tenantDb = createPoolProxy ? createPoolProxy(tenantPool) : tenantPool;
                // Pass the registry tenant id so the SELECT scopes to the
                // doc's actual home tenant, not the requesting admin's.
                // KS-458: the registry row's tenant must WIN over the request
                // ALS (the admin's own tenant) — run the lookup under the
                // registry tenant so createPoolProxy bundles THAT tenant's
                // GUC into the query's transaction (fail-closed RLS).
                document = await runWithTenantId(registryTenant, () => getDocument(id, registryTenant, tenantDb));
              }
            }
          }
        } catch {
          // Cross-tenant lookup not available — continue with 404
        }
      }

      if (!document) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found' } });
      }

      // Ownership check: the owner, an admin, or the designated recipient can view
      // Pen-test F-04: read from authenticated req.user, NOT raw headers.
      const authUser = (req as any).user;
      const userId = authUser?.userId as string | undefined;
      const userEmail = authUser?.email as string | undefined;
      const recipientEmail = (document.data as Record<string, unknown>)?.recipientEmail as string | undefined;
      const isRecipient = userEmail && recipientEmail && userEmail.toLowerCase() === recipientEmail.toLowerCase();
      if (userId && document.owner?.id && document.owner.id !== userId && !isAdmin && !isRecipient) {
        // KS-480 §6: onBehalfOf attribution sets owner_user_id, which would
        // 404-cloak the very connector key that created the document — and S
        // drives the whole lifecycle through this id. The CREATING connector
        // (matched via its creation provenance row) may read it back; any
        // other caller stays 404-cloaked like any non-owner.
        const isCreatingConnector = userRole === 'connector' && await wasCreatedByConnector(document.id, userId);
        if (!isCreatingConnector) {
          // Return 404 (not 403) to avoid leaking document existence to non-owners
          return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found' } });
        }
      }

      // KS-535: read-time self-healing for stale anchor claims. The in-process
      // confirmation poller dies with the service (restart) and its window is
      // shorter than anchoring's retry chain, so a document can sit claiming
      // an in-flight (or failed) anchor state that anchor_store has long since
      // resolved. Re-check stale rows against anchor_store and serve the truth.
      document = await reconcileDocumentAnchorState(document, tenantId, (req.headers.authorization as string) || '');

      const walletSignature = document.signatures.length > 0
        ? {
            address: document.signatures[0].walletAddress,
            signature: document.signatures[0].signature,
            signedAt: document.signatures[0].signedAt,
          }
        : undefined;

      // KS-480 §6: provenance is first-class — echo the creation attribution
      // (decrypted; pseudonymised rows echo externalRef only) so S and
      // auditors can see who acted. Null for non-connector documents.
      const createdOnBehalfOf = await getCreationProvenance(document.id);

      res.json({
        id: document.id,
        // KS-596 Phase B: canonical UUID alongside the legacy id on reads.
        documentUuid: document.documentUuid ?? null,
        type: document.type,
        title: (document.data as Record<string, unknown>)?.title || document.type || 'Untitled',
        documentType: (document.data as Record<string, unknown>)?.documentType || document.type,
        description: (document.data as Record<string, unknown>)?.description,
        status: document.status,
        owner: document.owner,
        data: document.data,
        contentHash: document.contentHash,
        signatures: document.signatures,
        walletSignature,
        blockchain: {
          // KS-520: `anchored` is status-derived, not presence-derived — the
          // fail-closed state records a blockchain object whose status is
          // 'anchor_failed', and that must not read as anchored.
          anchored: !!document.blockchain && document.blockchain.status !== 'anchor_failed',
          // KS-587 (document-blob leg): the KS-522 rules applied at the serve
          // boundary too, so blobs written BEFORE the writer fixes (e.g. the
          // SIMULATE_ANCHORING branch's stored tx_sim_ hash) still read
          // honestly — placeholder never presented as txHash, `simulated`
          // declared. No-op for real anchors and fail-closed states.
          ...(composeHonestBlockchainBlob(document.blockchain as Record<string, unknown> | null | undefined) || {}),
        },
        createdAt: document.createdAt,
        updatedAt: document.updatedAt,
        ...(createdOnBehalfOf ? { createdOnBehalfOf } : {}),
      });
    } catch (error) {
      logger.error('Failed to get document', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get document' } });
    }
  },
);

/**
 * POST /api/documents/:id/sign/request
 * Request document signing — returns hash and nonce for wallet signing
 */
documentsRouter.post(
  '/:id/sign/request',
  [param('id').notEmpty().withMessage('Document ID is required')],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { id } = req.params;
      const { walletAddress } = req.body;

      const document = await getDocument(id, getReqTenantId(req), (req as any).db);
      if (!document) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found' } });
      }

      const nonce = crypto.randomBytes(16).toString('hex');
      const hash = document.contentHash;
      const expiresAt = new Date(Date.now() + 5 * 60 * 1000).toISOString();

      saveSigningRequest(nonce, {
        documentId: id,
        walletAddress: walletAddress || user.walletAddress || '',
        hash,
        nonce,
        expiresAt,
      });

      res.json({
        hash,
        nonce,
        message: `Sign this document hash: ${hash}`,
        expiresAt,
        documentId: id,
      });
    } catch (error) {
      logger.error('Failed to create signing request', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create signing request' } });
    }
  },
);

/**
 * POST /api/documents/:id/sign
 * Submit wallet signature for document
 */
documentsRouter.post(
  '/:id/sign',
  [
    param('id').notEmpty().withMessage('Document ID is required'),
    body('signature').notEmpty().withMessage('Signature is required'),
    body('nonce').notEmpty().withMessage('Nonce is required'),
  ],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { id } = req.params;
      const { signature, nonce, walletAddress } = req.body;
      const tenantId = getReqTenantId(req);

      const document = await getDocument(id, tenantId, (req as any).db);
      if (!document) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found' } });
      }

      const signingRequest = getSigningRequest(nonce);
      if (!signingRequest) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid or expired signing request' } });
      }

      if (signingRequest.documentId !== id) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Signing request does not match document' } });
      }

      if (new Date(signingRequest.expiresAt) < new Date()) {
        deleteSigningRequest(nonce);
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Signing request has expired' } });
      }

      const isValidSignature = signature.startsWith('mock_signature_') || signature.length > 50;
      if (!isValidSignature) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid signature' } });
      }

      const now = new Date().toISOString();
      document.signatures.push({
        signerId: user.id,
        walletAddress: walletAddress || signingRequest.walletAddress,
        signature,
        signedAt: now,
      });

      await updateDocument(id, tenantId, {
        signatures: document.signatures,
        status: 'signed',
      });

      deleteSigningRequest(nonce);

      res.json({
        id: document.id,
        status: 'signed',
        signed: true,
        signature,
        signatureCount: document.signatures.length,
        signedAt: now,
      });
    } catch (error) {
      logger.error('Failed to sign document', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to sign document' } });
    }
  },
);

/**
 * Emit (or resolve) the on-chain anchor for a non-mutating lifecycle event
 * (share / transfer-custody / revoke) — KS-319. Anchoring is idempotent per
 * (document_id, network): re-anchoring an already-anchored document returns its
 * EXISTING anchor id, so the event is recorded against the existing document
 * (no new version / parent_document_id fork). Returns a resolvable anchor id
 * (GET /api/anchors/{id}) for the caller to surface, so Platform-S can persist
 * it as ExternalRef and its CardanoAnchorRefresher can upgrade it to a tx hash.
 * Shared so PS-123's generic lifecycle endpoint can reuse it (KS-274).
 *
 * Best-effort: the domain action (share/custody/revoke) has already committed by
 * the time this runs, so an anchoring outage degrades to {anchorId:null} + a
 * warning rather than failing the verb — S then falls back to POST /api/anchors
 * (its existing HTTP-failure path).
 */
async function emitLifecycleAnchor(params: {
  documentId: string;
  contentHash: string;
  authHeader?: string;
  // KS-387: widened beyond the three per-verb endpoints — the generic
  // /lifecycle-events route reuses this one shared emitter (the KS-319 note)
  // for its whole action vocabulary rather than growing a second implementation.
  eventType: 'share' | 'transfer-custody' | 'revoke' | LifecycleEventAction;
}): Promise<{ anchorId: string | null; txHash: string | null; status: string }> {
  const { documentId, contentHash, authHeader, eventType } = params;
  try {
    // Mirror POST /:id/anchor: forward the caller's bearer to anchoring's
    // authenticate() middleware; ANCHORING_SERVICE_URL is injected on Azure,
    // the service-name URL is the Docker Compose fallback.
    const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
    const resp = await fetch(`${anchoringBase}/api/anchors`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(authHeader ? { Authorization: authHeader } : {}),
        // KS-566: this is K's OWN hop, not Platform-S's flat-anchor fallback.
        // The calling verb (share / transfer-custody / revoke / lifecycle) has
        // already written its own action_provenance row, so anchoring must not
        // write a second one for the same user action. Non-spoofable: the
        // gateway strips `x-emitter-*` from every inbound client request
        // (api-gateway TRUST_HEADER_PATTERN), and this call bypasses it.
        'x-emitter-internal': 'originate-lifecycle',
      },
      body: JSON.stringify({
        documentId,
        // KS-282: anchoring requires a bare 64-hex digest; strip any sha256: prefix.
        contentHash: String(contentHash || '').replace(/^sha256:/i, '').toLowerCase(),
        network: process.env.CARDANO_NETWORK || 'preprod',
      }),
    });
    if (!resp.ok) {
      throw new Error(`Anchoring service returned ${resp.status}`);
    }
    const result = (await resp.json()) as any;
    const ad = result.data || result;
    logger.info('Lifecycle event anchored', { documentId, eventType, anchorId: ad.id, txHash: ad.txHash || null });
    return { anchorId: ad.id ?? null, txHash: ad.txHash ?? null, status: ad.status || 'submitted' };
  } catch (err: any) {
    logger.warn('Lifecycle anchor emission failed — event recorded without a resolvable anchor id (S falls back to /api/anchors)', {
      documentId,
      eventType,
      error: err instanceof Error ? err.message : String(err),
    });
    return { anchorId: null, txHash: null, status: 'pending' };
  }
}

/**
 * POST /api/documents/:id/anchor
 * Anchor document on blockchain via the anchoring service
 */
documentsRouter.post(
  '/:id/anchor',
  [param('id').notEmpty().withMessage('Document ID is required')],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { id } = req.params;
      const tenantId = getReqTenantId(req);
      const document = await getDocument(id, tenantId, (req as any).db);

      if (!document) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found' } });
      }

      // KS-520: a document whose auto-anchor FAILED (fail-closed state,
      // blockchain.status === 'anchor_failed') is not anchored — it must be
      // retryable through this route rather than 400ing as "already anchored".
      if (document.blockchain && document.blockchain.status !== 'anchor_failed') {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Document is already anchored' } });
      }

      const now = new Date().toISOString();
      let blockchainData: { txHash: string | null; blockHeight: number | null; anchoredAt: string | null; anchorId?: string; simulated?: boolean; simulatedTxRef?: string | null; confidence?: string };

      // Attempt to call the real anchoring service.
      // F-CHAIN-VERIFY-AUTH-01 / -02: forward bearer to anchoring's
      // authenticate() middleware (else 500 "No token provided"). Use
      // ANCHORING_SERVICE_URL when set (services.bicep injects the
      // internal Container Apps URL); the hard-coded service-name URL is
      // a Docker Compose fallback for local dev.
      try {
        const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
        const anchoringAuth = (req.headers.authorization as string) || '';
        const anchorResp = await fetch(`${anchoringBase}/api/anchors`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(anchoringAuth ? { Authorization: anchoringAuth } : {}),
          },
          body: JSON.stringify({
            documentId: id,
            // KS-282: the anchoring service requires a bare 64-hex digest, but a
            // document's stored contentHash may carry a `sha256:` prefix (every
            // version does — see the /version handler). Strip it so the version's
            // new hash actually anchors instead of 400'ing into the dev fallback.
            contentHash: String(document.contentHash || '').replace(/^sha256:/i, '').toLowerCase(),
            network: process.env.CARDANO_NETWORK || 'preprod',
          }),
        });

        if (anchorResp.ok) {
          const anchorResult = await anchorResp.json() as any;
          const ad = anchorResult.data || anchorResult;
          blockchainData = {
            // KS-281: capture the anchor id so the document's blockchain block
            // carries a resolvable anchorId (GET /api/anchors/{id}). The 202 body
            // has the id but not yet a txHash (the tx confirms asynchronously).
            anchorId: ad.id,
            txHash: ad.txHash || null,
            blockHeight: ad.blockHeight || 0,
            anchoredAt: ad.anchoredAt || ad.createdAt || now,
            // KS-587 (document-blob leg): same declaration as the create path.
            ...simulatedFieldsFromAnchor(ad),
          };
          logger.info('Document anchored via anchoring service', { documentId: id, anchorId: ad.id, txHash: blockchainData.txHash });
        } else {
          throw new Error(`Anchoring service returned ${anchorResp.status}`);
        }
      } catch (anchorErr: any) {
        if (process.env.NODE_ENV === 'production') {
          logger.error('Anchoring service unavailable in production', { documentId: id, error: anchorErr instanceof Error ? anchorErr.message : String(anchorErr) });
          return res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Blockchain anchoring service is temporarily unavailable. Please try again later.' } });
        }
        logger.warn('Anchoring service unavailable — recording pending-onchain state (dev mode)', { documentId: id, error: anchorErr instanceof Error ? anchorErr.message : String(anchorErr) });
        // Pen-test F-03: was generating a fake blockHeight via Math.random()
        // and persisting `simulated: true`. The simulated flag was easy to
        // miss downstream and the verifier UI didn't surface it. New shape
        // sets the chain-only fields to null and adds an explicit
        // `confidence: 'pending-onchain'` that the verifier UI must honour.
        blockchainData = {
          txHash: null,
          blockHeight: null,
          anchoredAt: null,
          confidence: 'pending-onchain',
        };
      }

      await updateDocument(id, tenantId, {
        blockchain: blockchainData,
        status: 'anchored',
      });

      // KS-535: this retry path previously never polled — a retried anchor
      // could neither gain its real txHash nor report a terminal on-chain
      // failure (the same permanent-'anchored' mislabel as the create path).
      // Same poller as create: confirms → txHash/blockHeight; terminal
      // failure → the KS-520 fail-closed shape.
      if (blockchainData.anchorId) {
        pollAnchorUntilConfirmed({
          anchorId: blockchainData.anchorId,
          documentId: id,
          tenantId,
          authHeader: (req.headers.authorization as string) || '',
        });
      }

      // KS-154: 202 Accepted — the anchor tx has been submitted (the
      // anchoring service returned a txHash) but on-chain confirmation
      // can take ~30-60s on Cardano. Convention for an async operation
      // whose work-of-record is still finalising. Clients poll
      // GET /api/documents/{id} or the verification endpoint for
      // confirmation. The dev-fallback path returns the same code with
      // `confidence: 'pending-onchain'` (txHash null) — still 202.
      res.status(202).json({
        id: document.id,
        status: 'anchored',
        transactionHash: blockchainData.txHash,
        blockchain: blockchainData,
      });
    } catch (error) {
      logger.error('Failed to anchor document', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to anchor document' } });
    }
  },
);

/**
 * POST /api/documents/:id/verify
 *
 * **DEPRECATED — KS-48 (option A).** Use `POST /api/verification/verify` instead.
 * This endpoint is owner-scoped (the doc must be in the caller's tenant);
 * the public `/api/verification/verify` resolves cross-tenant via the
 * platform document registry and is the canonical verify path used by
 * the verifier portal, the SSD connector (`SecuuraApi.verifyDocument`),
 * and any cross-environment workflow. RFC 8594 `Deprecation` + `Sunset` +
 * `Link: rel="successor-version"` headers are set on every response so
 * any remaining caller can spot the deprecation in logs / dev-tools.
 * Removal date: see `DEPRECATED_VERIFY_SUNSET` below.
 */

// KS-48: deprecation horizon. 2026-08-14 = 90 days from the deprecation
// commit (2026-05-14). Adjust here if the call says shorter/longer.
const DEPRECATED_VERIFY_SUNSET = 'Thu, 14 Aug 2026 00:00:00 GMT';
const DEPRECATED_VERIFY_SUCCESSOR = '/api/verification/verify';

documentsRouter.post(
  '/:id/verify',
  [param('id').notEmpty().withMessage('Document ID is required')],
  async (req: Request, res: Response) => {
    // KS-48: stamp the deprecation headers on every response, success or
    // failure. setHeader before any res.json() / res.status() — Express
    // serialises headers at the first body chunk, so calling it here
    // covers all six early-return paths below.
    res.setHeader('Deprecation', 'true');
    res.setHeader('Sunset', DEPRECATED_VERIFY_SUNSET);
    res.setHeader(
      'Link',
      `<${DEPRECATED_VERIFY_SUCCESSOR}>; rel="successor-version"`,
    );
    try {
      const { id } = req.params;
      const document = await getDocument(id, getReqTenantId(req), (req as any).db);
      if (!document) {
        return res.status(404).json({
          verified: false,
          error: 'Document not found',
        });
      }

      const providedHash = req.body?.contentHash || req.body?.providedHash;
      const isRevoked = document.status === 'revoked';
      const isAnchored = document.status === 'signed' || document.status === 'anchored';

      if (!providedHash) {
        return res.json({
          verified: false,
          documentId: document.id,
          status: document.status,
          reason: 'No contentHash provided for comparison. Provide contentHash in the request body to verify document integrity.',
          checks: {
            exists: true,
            notRevoked: !isRevoked,
            hashValid: false,
            hasSignatures: document.signatures.length > 0,
            blockchainAnchored: !!document.blockchain,
          },
          verifiedAt: new Date().toISOString(),
        });
      }

      const hashValid = providedHash === document.contentHash;

      res.json({
        verified: isAnchored && hashValid && !isRevoked,
        documentId: document.id,
        status: document.status,
        hash: document.contentHash,
        checks: {
          exists: true,
          notRevoked: !isRevoked,
          hashValid,
          hasSignatures: document.signatures.length > 0,
          blockchainAnchored: !!document.blockchain,
        },
        issuer: {
          id: document.owner.id,
          verified: true,
        },
        blockchain: document.blockchain
          // KS-520: same status-derived `anchored` as GET /:id — an
          // anchor_failed record is not an anchor.
          ? { ...document.blockchain, anchored: document.blockchain.status !== 'anchor_failed' }
          : { anchored: false },
        verifiedAt: new Date().toISOString(),
      });
    } catch (error) {
      logger.error('Failed to verify document', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to verify document' } });
    }
  },
);

/**
 * POST /api/documents/:id/transfer-custody — KS-68
 *
 * Explicit custodian-transfer endpoint. The rights-holder changes from
 * A to B without the document bytes changing. Distinct from KS-70 lineage
 * (which creates new linked documents for content-changing events like
 * certify / sign) — transfer-custody is metadata-only, hence its own
 * lightweight `custody_events` table.
 *
 * Body: `{newHolderId | newHolderEmail, reason?, effectiveAt?}`. One of
 * `newHolderId` / `newHolderEmail` is required. The email path needs a
 * follow-up resolver to a real userId — for now it's stored as-is on
 * the event row's `to_holder_id` is the resolved userId; email-only
 * recipients require a KS-69 lookup hit upstream.
 *
 * Behaviour:
 *   1. RBAC gate: any document-write role (ISSUER_ADMIN / ORG_ADMIN /
 *      SYSTEM_ADMIN / SUPER_ADMIN) OR the `documents:transfer-custody` scope.
 *      KS-290: the original KS-68 spec omitted ISSUER_ADMIN, which 403'd a
 *      document's own issuer/owner on their own document even though they
 *      could create / version / share it. ISSUER_ADMIN is now included via
 *      the shared `DOCUMENT_WRITE_ROLES` base so this verb can't drift from
 *      its siblings again. (Public-signup OWNER stays excluded — it carries
 *      only `documents:write`, not `documents:transfer-custody`.)
 *   2. Confirm document exists in tenant.
 *   2a. KS-697: confirm the NEW HOLDER exists in this tenant. `newHolderId` is
 *      format-checked at the boundary (400) and then existence-checked against
 *      `users` (404 RECIPIENT_NOT_FOUND) — the same answer the `newHolderEmail`
 *      path has always given via auth's /api/users/lookup. Before this, an
 *      arbitrary invented uuid returned 201 and minted an anchor for a custody
 *      chain pointing at nobody; `custody_events.to_holder_id` carries no FK,
 *      so the database was never going to catch it.
 *   3. Insert custody_events row (from = current owner, to = new holder).
 *   4. Update documents.owner_user_id to the new holder.
 *   5. Return 201 with the event id.
 *
 * Anchoring on Cardano is deferred to a follow-up — the chain metadata
 * shape needs alignment with anchoring service. For now the event is
 * tenant-DB-only; the chain anchor will arrive in a separate PR.
 */
const ALLOWED_TRANSFER_CUSTODY_ROLES = DOCUMENT_WRITE_ROLES;

documentsRouter.post(
  '/:id/transfer-custody',
  [
    param('id').notEmpty().withMessage('Document ID is required'),
    body('reason').optional().isString(),
    body('effectiveAt').optional().isISO8601().withMessage('effectiveAt must be an ISO-8601 timestamp'),
  ],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      if (!isAllowedByRoleOrScope(req, ALLOWED_TRANSFER_CUSTODY_ROLES, 'documents:transfer-custody')) {
        return res.status(403).json({
          success: false,
          error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit custody transfer on this document' },
        });
      }

      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Invalid request body', details: errors.array() },
        });
      }

      const { id } = req.params;
      // KS-480 §6: connector attribution on the transfer action. KS-1228: validated here, and
      // recorded only once the custody event and the owner flip are written (below).
      const transferObo = await checkOnBehalfOf(req, res);
      if (!transferObo.ok) return;
      const { newHolderId, newHolderEmail, reason, effectiveAt } = req.body as {
        newHolderId?: string;
        newHolderEmail?: string;
        reason?: string;
        effectiveAt?: string;
      };

      if (!newHolderId && !newHolderEmail) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'One of newHolderId or newHolderEmail is required' },
        });
      }
      if (newHolderId && newHolderEmail) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Supply either newHolderId or newHolderEmail, not both' },
        });
      }

      // KS-697: `newHolderId` flows into a `::uuid` cast in the INSERT below.
      // A non-UUID threw Postgres 22P02 there, got swallowed by this handler's
      // outer catch and surfaced as a raw 500 — the not_a_server_error class,
      // and the same boundary gap KS-497/KS-536 closed for tenant ids and
      // `recipients[].userId`. Reject before the cast.
      //
      // ⚠ The KS-536 comment on /share asserted "/transfer-custody already
      // format-checks its holder id before touching the DB". It did not — no
      // such guard existed on this route until this line. The claim is
      // corrected there too; a comment that says a guard exists is worse than
      // no comment, because it stops the next reader looking.
      if (newHolderId !== undefined && !UUID_RE.test(String(newHolderId))) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'newHolderId must be a valid UUID' },
        });
      }

      // Resolve the email-only path via the /api/users/lookup helper SSD
      // uses (KS-69). KS-289: call auth-service DIRECTLY (AUTH_SERVICE_URL),
      // not via the gateway — the gateway default (http://localhost:6882) is
      // unreachable from inside the originate container (→ 502), and auth's
      // /lookup self-gates on role/scope + reads the tenant from the
      // forwarded JWT. If the lookup misses we return 404 — the recipient
      // should be invited first (KS-74).
      let resolvedHolderId = newHolderId;
      if (!resolvedHolderId && newHolderEmail) {
        const authHeader = (req.headers.authorization as string) || '';
        try {
          const authBase = process.env.AUTH_SERVICE_URL || 'http://localhost:6003';
          const lookupRes = await fetch(
            `${authBase}/api/users/lookup?email=${encodeURIComponent(newHolderEmail)}`,
            { headers: authHeader ? { Authorization: authHeader } : {} },
          );
          if (lookupRes.status === 404) {
            return res.status(404).json({
              success: false,
              error: {
                code: 'RECIPIENT_NOT_FOUND',
                message: 'No user with that email in this tenant. Invite them first (KS-74 pending-invite UX).',
              },
            });
          }
          // KS-536 sweep: a MALFORMED newHolderEmail made auth's lookup answer
          // 400, and mapping every non-404 to 502 turned bad client input into a
          // server error (the not_a_server_error class). A 4xx from the lookup
          // is the caller's fault and must surface as 400; only a genuine
          // upstream failure (5xx / unreachable) is a 502.
          if (lookupRes.status === 400 || lookupRes.status === 422) {
            return res.status(400).json({
              success: false,
              error: { code: 'VALIDATION_ERROR', message: 'newHolderEmail is not a valid email address' },
            });
          }
          // KS-739: the comment above states a rule about the whole 4xx CLASS,
          // and KS-536 implemented it for two codes. 401 and 403 are 4xx by the
          // same reasoning and were still becoming 502 — which is what Platform S
          // saw: a caller-credential refusal presented as an upstream outage, and
          // a 5xx is not something a caller can branch on. Enumerating 401/403
          // would leave 405/409/410/429 to re-create this ticket on the next code
          // auth grows, so this handles the class instead. `/sign-cert` in this
          // same file already does exactly that (search CERT_SIGN_ERROR) —
          // transfer-custody's enumeration was the outlier, not the norm.
          //
          // 404 and 400/422 keep their specific typed answers ABOVE this line;
          // they are contract and more useful than a pass-through. 5xx and an
          // unreachable auth service stay 502 below — those are the only genuine
          // upstream failures.
          if (lookupRes.status >= 400 && lookupRes.status < 500) {
            const upstream = (await lookupRes.json().catch(() => ({}))) as {
              error?: { code?: string; message?: string };
            };
            // The lookup is called with the CALLER'S Authorization (above), and
            // auth's /lookup self-gates on role/scope — so a 401/403 here is the
            // caller's own credential failing, not ours. Name what is missing:
            // auth accepts `users:read`, `users:*` or `*` (auth users.ts,
            // hasUsersReadScope), which is what KS-739 ruled S provisions.
            const hint =
              lookupRes.status === 401
                ? 'The credential on this request was rejected by the user lookup. Re-authenticate and retry.'
                : lookupRes.status === 403
                  ? 'The credential on this request may not resolve users by email. Grant it the `users:read` scope (or `users:*` / `*`).'
                  : null;
            const upstreamMessage = upstream?.error?.message;
            return res.status(lookupRes.status).json({
              success: false,
              error: {
                code: upstream?.error?.code || 'RECIPIENT_LOOKUP_FAILED',
                message: hint
                  ? upstreamMessage
                    ? `${hint} Upstream said: ${upstreamMessage}`
                    : hint
                  : upstreamMessage || `Recipient lookup failed with status ${lookupRes.status}`,
              },
            });
          }
          if (!lookupRes.ok) {
            return res.status(502).json({
              success: false,
              error: { code: 'BAD_GATEWAY', message: 'Could not resolve recipient email via users/lookup' },
            });
          }
          const body = await lookupRes.json() as { data?: { userId: string } };
          resolvedHolderId = body.data?.userId;
        } catch (err: any) {
          logger.warn('users/lookup unreachable during transfer-custody', { error: err?.message });
          return res.status(502).json({
            success: false,
            error: { code: 'BAD_GATEWAY', message: 'Recipient lookup service unavailable' },
          });
        }
      }

      if (!resolvedHolderId) {
        return res.status(500).json({
          success: false,
          error: { code: 'INTERNAL_ERROR', message: 'Resolved holder id missing after lookup' },
        });
      }

      const tenantId = getReqTenantId(req);
      const doc = await getDocument(id, tenantId, (req as any).db);
      if (!doc) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found in this tenant' } });
      }

      const fromHolderId = doc.owner.id || null;
      const eventEffectiveAt = effectiveAt ? new Date(effectiveAt) : new Date();
      // Use the existing db reference from the request (per-tenant if
      // multi-tenancy is on, default prisma otherwise — same pattern as
      // every other write route in this file).
      const { prisma: defaultPrisma, withTenant } = await import('../db');
      const db = (req as any).db || defaultPrisma;

      // KS-697: the id path never checked that the holder EXISTS. `custody_events`
      // has an FK on `document_id` but NOT on `to_holder_id`, so any well-formed
      // uuid inserted happily: an arbitrary invented holder returned 201 AND minted
      // an anchor, while `newHolderEmail` for the same operation correctly 404s.
      // The document's chain of custody could be pointed at nobody, and anchored.
      //
      // Mirror the email path exactly: unknown holder → 404 RECIPIENT_NOT_FOUND.
      // Only the id path needs this — the email path has already resolved through
      // auth's /api/users/lookup, which does its own existence + tenant check.
      //
      // Scoping: since KS-458 this `$queryRaw` carries the request's RLS tenant
      // GUC, and `users` is FORCE RLS fail-closed — so a holder in another tenant
      // is simply invisible here and falls out as the same 404. That matches auth's
      // deliberate stance on /lookup, where "no such user" and "exists in another
      // tenant" are made indistinguishable so the negative response cannot be read
      // as cross-tenant existence disclosure. The explicit tenant_id predicate is
      // belt-and-braces for any deployment where the GUC is not carried (tenant RLS
      // has been inert before now — KS-160/KS-458); `tenant_id IS NULL` is tolerated
      // because auth's own lookup only enforces tenancy when both sides are known.
      if (newHolderId !== undefined) {
        const holderRows: Array<{ ok: number }> = await db.$queryRaw`
          SELECT 1 AS ok
            FROM users
           WHERE id = ${resolvedHolderId}::uuid
             AND (tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)
           LIMIT 1
        `;
        if (holderRows.length === 0) {
          return res.status(404).json({
            success: false,
            error: {
              code: 'RECIPIENT_NOT_FOUND',
              message: 'No user with that id in this tenant. Invite them first (KS-74 pending-invite UX).',
            },
          });
        }
      }

      // KS-1263: the custody event and the owner flip are ONE transaction. They used to be two
      // statements, and the comment here accepted the window between them ("Prisma's $executeRaw
      // doesn't compose nicely ... we accept a small window where the event row exists without the
      // doc-owner update"). A throw in that window left a custody event for a transfer that did not
      // happen, and since KS-1228 no action_provenance row either.
      // KS-1263: withTenant() is used UNCONDITIONALLY here, never `(req as any).db`. On a
      // multi-tenant deployment (index.ts:225, gated on MULTI_TENANCY_ENABLED, which
      // deployment/azure/services.bicep:798 sets to 'true') that reference is
      // createPoolProxy(pool), which wraps BEGIN + set_config + COMMIT around EACH statement
      // (db.ts:24-26) — two transactions again, which is the defect this ticket removes.
      // withTenant checks out ONE client, runs BEGIN + both set_config GUCs + the callback on
      // that client, then COMMIT, or ROLLBACK on a throw (db.ts:302-336); handed that open
      // client, createPoolProxy queries it directly rather than re-bundling (db.ts:24-26,
      // pinned by ks458-db-tenant-guc.test.ts:111).
      let eventId: string;
      try {
        eventId = await withTenant(tenantId, async (tx) => {
          const eventRows: Array<{ id: string }> = await tx.$queryRaw`
        INSERT INTO custody_events (
          tenant_id, document_id, from_holder_id, to_holder_id,
          transferred_by_id, reason, effective_at
        ) VALUES (
          ${tenantId}::uuid,
          (SELECT id FROM documents WHERE external_id = ${id} AND tenant_id = ${tenantId}::uuid LIMIT 1),
          ${fromHolderId}::uuid,
          ${resolvedHolderId}::uuid,
          ${user.id}::uuid,
          ${reason ?? null},
          ${eventEffectiveAt}
        )
            RETURNING id::text AS id
          `;
          const written = eventRows[0]?.id;
          if (!written) {
            // Throw, never return: a `return res.json(...)` inside the callback resolves it
            // normally and COMMITS. Throwing rolls the INSERT back; the 500 is mapped below.
            throw Object.assign(new Error('custody event not written'), { code: 'CUSTODY_EVENT_NOT_WRITTEN' });
          }
          // Flip the owner. Use external_id as the lookup key to match
          // the rest of the originate-route convention.
          await tx.$executeRaw`
            UPDATE documents
               SET owner_user_id = ${resolvedHolderId}::uuid,
                   updated_at = NOW()
             WHERE external_id = ${id}
               AND tenant_id = ${tenantId}::uuid
          `;
          return written;
        });
      } catch (err: any) {
        if (err?.code === 'CUSTODY_EVENT_NOT_WRITTEN') {
          return res.status(500).json({
            success: false,
            error: { code: 'INTERNAL_ERROR', message: 'Failed to write custody event' },
          });
        }
        throw err;
      }
      recordOnBehalfOf(req, id, 'transfer-custody', transferObo);

      logger.info('Custody transferred', {
        documentId: id,
        fromHolderId,
        toHolderId: resolvedHolderId,
        eventId,
      });

      // EventTypes doesn't yet have an OWNERSHIP_TRANSFERRED const —
      // pass the literal string. When events.ts grows the const, swap
      // to EventTypes.DOCUMENT_OWNERSHIP_TRANSFERRED.
      publishEvent('document.ownership_transferred' as never, {
        documentId: id,
        fromHolderId,
        toHolderId: resolvedHolderId,
        transferredById: user.id,
        eventId,
      }).catch(() => {});

      // KS-319: emit the on-chain anchor for the custody-transfer event and
      // return a resolvable anchor id (idempotent — reuses the document's
      // existing anchor). Replaces the previously-deferred anchoredTxHash:null.
      const custodyAnchor = await emitLifecycleAnchor({
        documentId: id,
        contentHash: doc.contentHash,
        authHeader: req.headers.authorization as string,
        eventType: 'transfer-custody',
      });

      return res.status(201).json({
        transfer: {
          id: eventId,
          documentId: id,
          fromHolderId,
          toHolderId: resolvedHolderId,
          effectiveAt: eventEffectiveAt.toISOString(),
          anchoredTxHash: custodyAnchor.txHash,
          anchorId: custodyAnchor.anchorId,
          anchor: { id: custodyAnchor.anchorId, txHash: custodyAnchor.txHash, status: custodyAnchor.status },
        },
      });
    } catch (error) {
      logger.error('Failed to transfer custody', { error: error instanceof Error ? error.message : String(error) });
      return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to transfer custody' } });
    }
  },
);

/**
 * POST /api/documents/:id/version — KS-86 (Option B sub-task of KS-84)
 *
 * Issuer-side lifecycle action endpoint. Records a new versioned document
 * (with `parent_document_id` pointing at the source) for any byte-changing
 * action the caller has already performed externally — typically a
 * watermark or an X.509 sign-and-sidecar. Platform K is a hash-only
 * registry; the bytes themselves live with the issuer (e.g. SSD).
 *
 * Body: `{action, newContentHash, metadata?, title?}`
 *   - `action`: 'watermark' | 'sign-cert'  (enum locked here; future
 *     verbs land via a deliberate ticket so we don't grow drift).
 *   - `newContentHash`: sha256 hex digest of the new bytes. Optional
 *     `sha256:` prefix accepted (and stripped); 64 lowercase hex chars
 *     required after the prefix.
 *   - `metadata`: free-form issuer metadata folded into the new doc's
 *     `data` blob (e.g. `{watermarkText, watermarkPosition}` for
 *     watermark, `{signedBy, certThumbprint, sidecarUrl}` for sign-cert).
 *   - `title`: override the new version's title; defaults to
 *     "<source title> (watermarked)" / "<source title> (signed)".
 *
 * Behaviour:
 *   1. RBAC gate — same role allow-list as transfer-custody, plus
 *      `documents:write` scope (versioning is a write op; we don't
 *      carve a `documents:version` scope until a connector needs it).
 *   2. Resolve source doc in tenant. 404 if missing.
 *   3. Mint new external_id `doc-<ts>-<rand>`.
 *   4. KS-70 cycle check on the new id against the source. Should always
 *      pass for fresh ids but defence-in-depth keeps the invariant solid.
 *   5. Save derived doc with `parent_document_id` = source.
 *   6. Audit log + DOCUMENT_VERSIONED event.
 *   7. Return 201 with the new doc shape.
 *
 * Anchoring is intentionally NOT triggered here — the existing
 * `POST /api/documents/{id}/anchor` endpoint can be called against the
 * new id when the issuer is ready. Keeps Cardano cost decisions in the
 * issuer's hands per the KS-70 model.
 */
const ALLOWED_VERSION_ROLES = DOCUMENT_WRITE_ROLES;
const ALLOWED_VERSION_ACTIONS = ['watermark', 'sign-cert'] as const;
type VersionAction = (typeof ALLOWED_VERSION_ACTIONS)[number];
const CONTENT_HASH_RE = /^([a-f0-9]{64})$/;

documentsRouter.post(
  '/:id/version',
  [
    param('id').notEmpty().withMessage('Document ID is required'),
    body('action').isString().isIn(ALLOWED_VERSION_ACTIONS as unknown as string[]).withMessage(`action must be one of: ${ALLOWED_VERSION_ACTIONS.join(', ')}`),
    body('newContentHash').isString().notEmpty().withMessage('newContentHash is required'),
    body('metadata').optional().isObject().withMessage('metadata must be an object'),
    body('title').optional().isString(),
  ],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      if (!isAllowedByRoleOrScope(req, ALLOWED_VERSION_ROLES, 'documents:write')) {
        return res.status(403).json({
          success: false,
          error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit creating a new version of this document' },
        });
      }

      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Invalid request body', details: errors.array() },
        });
      }

      const { id } = req.params;
      const action = req.body.action as VersionAction;
      // KS-480 §6: connector attribution on the version action (watermark/sign). KS-1228: validated
      // here, and recorded only once the new version is saved (below), after every refusal.
      const versionObo = await checkOnBehalfOf(req, res);
      if (!versionObo.ok) return;
      const rawHash = String(req.body.newContentHash || '');
      const metadata = (req.body.metadata && typeof req.body.metadata === 'object') ? req.body.metadata as Record<string, unknown> : {};
      // KS-480 §6: reserved provenance key — lives in action_provenance only,
      // never in a row's plain metadata blob (it would be unencrypted PII).
      delete metadata.onBehalfOf;
      const overrideTitle = typeof req.body.title === 'string' ? req.body.title.trim() : '';

      // Normalise hash: accept both `sha256:hex` and `hex`. Reject anything
      // that isn't 64 lowercase hex chars after the optional prefix — every
      // store path downstream expects the bare digest.
      const normalisedHash = rawHash.replace(/^sha256:/i, '').toLowerCase();
      if (!CONTENT_HASH_RE.test(normalisedHash)) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'newContentHash must be a sha256 hex digest (64 lowercase hex chars, optional sha256: prefix)' },
        });
      }
      const newContentHash = `sha256:${normalisedHash}`;

      const tenantId = getReqTenantId(req);
      const source = await getDocument(id, tenantId, (req as any).db);
      if (!source) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found in this tenant' } });
      }
      // KS-1213: this row is stored as `source.type` but served as `data.documentType || type`, and
      // the caller's `metadata` is spread into `data`. A `metadata.documentType` that differs from the
      // stored type would serve, and verify, the new row as another type. Same rule as the KS-1202
      // create guard: refused, never overwritten; exact comparison, and a non-string never matches.
      if (metadata.documentType !== undefined && metadata.documentType !== source.type) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      const newExternalId = `doc-${Date.now()}-${uuidv4().slice(0, 8)}`;

      try {
        await assertNoCycle(newExternalId, id, tenantId, { db: (req as any).db });
      } catch (cycleErr: any) {
        if (cycleErr?.code === 'LINEAGE_CYCLE') {
          return res.status(422).json({
            success: false,
            error: {
              code: 'LINEAGE_CYCLE',
              message: `Refusing to version: source ${id} would form a cycle in the lineage chain (corrupted parent chain?)`,
            },
          });
        }
        throw cycleErr;
      }

      const now = new Date().toISOString();
      const sourceTitle = (source.data?.title as string) || source.type || 'Untitled';
      const titleSuffix = action === 'watermark' ? ' (watermarked)' : ' (signed)';
      const derivedTitle = overrideTitle || `${sourceTitle}${titleSuffix}`;

      // KS-282: a version is a fresh document with its OWN content hash; it must
      // NOT inherit the parent's anchor. The parent's `blockchain` block rides in
      // via `...source.data` (mapRow spreads metadata into `data`, and blockchain
      // is read back from metadata) — strip it so the version reads as
      // un-anchored and POST /{versionId}/anchor anchors the version's new hash
      // (its document_id is new, so it gets its own anchor row).
      const { blockchain: _parentBlockchain, ...sourceDataSansChain } =
        (source.data || {}) as Record<string, unknown>;

      const derivedDoc: DocumentRecord = {
        id: newExternalId,
        type: source.type,
        status: 'draft',
        owner: source.owner,
        rightsHolderId: source.rightsHolderId,
        parentDocumentId: id,
        data: {
          ...sourceDataSansChain,
          title: derivedTitle,
          versionAction: action,
          versionedAt: now,
          versionedById: user.id,
          parentDocumentId: id,
          ...metadata,
        },
        contentHash: newContentHash,
        signatures: [],
        blockchain: undefined,
        createdAt: now,
        updatedAt: now,
      };

      await saveDocument(derivedDoc, tenantId, (req as any).db);
      recordOnBehalfOf(req, id, `version:${action}`, versionObo);

      logger.info('Document versioned', {
        sourceId: id,
        newId: newExternalId,
        action,
        tenantId,
        userId: user.id,
      });

      // EventTypes doesn't yet have a DOCUMENT_VERSIONED const — pass
      // the literal string. When events.ts grows the const, swap to
      // EventTypes.DOCUMENT_VERSIONED.
      publishEvent('document.versioned' as never, {
        sourceId: id,
        newId: newExternalId,
        action,
        contentHash: newContentHash,
        userId: user.id,
      }).catch(() => {});

      return res.status(201).json({
        document: {
          id: newExternalId,
          parentDocumentId: id,
          type: source.type,
          status: 'draft',
          contentHash: newContentHash,
          action,
          title: derivedTitle,
          versionedAt: now,
          // Anchoring intentionally not auto-triggered — caller hits
          // POST /api/documents/{newId}/anchor when ready.
          anchored: false,
        },
      });
    } catch (error) {
      logger.error('Failed to version document', { error: error instanceof Error ? error.message : String(error) });
      return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create new document version' } });
    }
  },
);

/**
 * POST /api/documents/:id/share — KS-67
 *
 * Share an uploaded document (with or without a prior certification) to
 * one or more recipients. Writes to the polymorphic `shares` table from
 * migration 022; the existing `/api/certifications/:id/share` route is
 * unchanged and still writes to the legacy `share_records` table (a
 * follow-up ticket consolidates the two).
 *
 * Body: `{recipients: [{email | userId, name?, shareType: 'view'|'verify'|'reshare'}], message?, expiresAt?}`
 *
 * Per recipient an `email` OR a `userId` is required. The `userId` form
 * is used by SSD after a `/api/users/lookup` hit (KS-69); the `email`
 * form covers the unregistered-recipient case (the share row carries
 * the email and is claimed if the user signs up later, per KS-74).
 *
 * RBAC: ISSUER_ADMIN / ORG_ADMIN / SYSTEM_ADMIN / SUPER_ADMIN role OR
 * `documents:share` scope (KS-71 helper).
 */
const ALLOWED_DOCUMENT_SHARE_ROLES = DOCUMENT_WRITE_ROLES;
const ALLOWED_SHARE_TYPES: ShareType[] = ['view', 'verify', 'reshare'];
// KS-536: recipients[].userId is used in a `::uuid` cast downstream, so it must
// be format-checked at the boundary (mirrors the transfer-custody guard).
const SHARE_RECIPIENT_UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

documentsRouter.post(
  '/:id/share',
  [
    param('id').notEmpty().withMessage('Document ID is required'),
    body('recipients').isArray({ min: 1 }).withMessage('At least one recipient is required'),
  ],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      if (!isAllowedByRoleOrScope(req, ALLOWED_DOCUMENT_SHARE_ROLES, 'documents:share')) {
        return res.status(403).json({
          success: false,
          error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit sharing this document' },
        });
      }

      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Invalid request body', details: errors.array() },
        });
      }

      const { id } = req.params;
      // KS-480 §6: connector attribution on the share action. KS-1228: validated and resolved here
      // (the resolved person is the sharer below), and recorded only once every share row is
      // written, because createShare itself can still refuse (404, and the SQLSTATE 400s).
      const shareObo = await checkOnBehalfOf(req, res);
      if (!shareObo.ok) return;
      const { recipients, message, expiresAt } = req.body as {
        recipients: Array<{ email?: string; userId?: string; shareType?: ShareType; name?: string }>;
        message?: string;
        expiresAt?: string;
      };

      const tenantId = getReqTenantId(req);

      // Confirm the document exists in this tenant before we write any
      // share rows. Otherwise the shareRepo.createShare subquery would
      // silently fail with SHARE_TARGET_NOT_FOUND on the FIRST recipient
      // and we'd respond mid-flight.
      const doc = await getDocument(id, tenantId, (req as any).db);
      if (!doc) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found in this tenant' } });
      }

      // Validate recipient shape up-front so we don't half-write.
      for (const r of recipients) {
        if (!r.email && !r.userId) {
          return res.status(400).json({
            success: false,
            error: { code: 'VALIDATION_ERROR', message: 'Each recipient must have either an email or a userId' },
          });
        }
        // KS-536 sweep: a non-UUID `userId` reached a `::uuid` cast in the share
        // repo and threw Postgres 22P02 ("invalid input syntax for type uuid"),
        // surfacing as a raw 500 — the not_a_server_error class, and the same
        // boundary gap KS-497 closed for tenant ids.
        // ⚠ KS-697 correction: this comment used to end "/transfer-custody
        // already format-checks its holder id before touching the DB; /share
        // did not." That was false — /transfer-custody had NO such guard, and
        // 500'd on a non-uuid holder for as long as this comment claimed
        // otherwise. It does now. Left as a correction rather than a silent
        // deletion, because the wrong half is why nobody went and looked.
        if (r.userId !== undefined && !SHARE_RECIPIENT_UUID_RE.test(String(r.userId))) {
          return res.status(400).json({
            success: false,
            error: { code: 'VALIDATION_ERROR', message: 'recipients[].userId must be a valid UUID' },
          });
        }
        const st = (r.shareType ?? 'view') as ShareType;
        if (!ALLOWED_SHARE_TYPES.includes(st)) {
          return res.status(400).json({
            success: false,
            error: { code: 'VALIDATION_ERROR', message: `Invalid shareType '${st}'. Allowed: ${ALLOWED_SHARE_TYPES.join(', ')}` },
          });
        }
      }

      // KS-564: `shares.shared_by_id` is a UUID column, but a connector
      // principal is `connector:<platform>:<id>` — writing it hit the ::uuid
      // cast and 22P02'd into a raw 500 on every Platform S share. Prefer the
      // onBehalfOf-resolved human; otherwise store NULL (same treatment
      // POST /api/documents has always given owner_user_id). A provenance row
      // carries the connector only when onBehalfOf was supplied — see
      // utils/principalId and BACKLOG.md for the bare-connector gap.
      const sharedByUuid = toActorUuid(user.id, shareObo.resolvedUserId);

      const created: Array<{ id: string; recipientEmail?: string | null; recipientUserId?: string | null; shareType: ShareType }> = [];
      // KS-1263: every recipient's row is written in ONE transaction, so a refusal at recipient
      // k > 1 rolls the earlier rows back rather than leaving them behind with no
      // action_provenance row (which is what develop did after KS-1228).
      // KS-1263: withTenant() is used UNCONDITIONALLY here, never `(req as any).db`. On a
      // multi-tenant deployment (index.ts:225, gated on MULTI_TENANCY_ENABLED, which
      // deployment/azure/services.bicep:798 sets to 'true') that reference is
      // createPoolProxy(pool), which wraps BEGIN + set_config + COMMIT around EACH statement
      // (db.ts:24-26) — two transactions again, which is the defect this ticket removes.
      // withTenant checks out ONE client, runs BEGIN + both set_config GUCs + the callback on
      // that client, then COMMIT, or ROLLBACK on a throw (db.ts:302-336); handed that open
      // client, createPoolProxy queries it directly rather than re-bundling (db.ts:24-26,
      // pinned by ks458-db-tenant-guc.test.ts:111).
      const { withTenant } = await import('../db');
      try {
        await withTenant(tenantId, async (tx) => {
          for (const r of recipients) {
            const share = await createShare(
              {
                tenantId,
                targetType: 'document',
                targetId: id,
                recipientUserId: r.userId ?? null,
                recipientEmail: r.email ?? null,
                shareType: (r.shareType ?? 'view') as ShareType,
                sharedById: sharedByUuid,
                expiresAt: expiresAt ?? null,
                message: message ?? null,
              },
              tx,
            );
            created.push({
              id: share.id,
              recipientEmail: share.recipientEmail,
              recipientUserId: share.recipientUserId,
              shareType: share.shareType,
            });
          }
        });
      } catch (err: any) {
        // The rollback has already happened; `created` describes rows that no longer exist, and
        // nothing below this point reads it on an error path.
        if (err?.code === 'SHARE_TARGET_NOT_FOUND') {
          return res.status(404).json({
            success: false,
            error: { code: 'NOT_FOUND', message: 'Document not found in this tenant (resolution failed at share time)' },
          });
        }
        throw err;
      }
      recordOnBehalfOf(req, id, 'share', shareObo);

      // KS-319: emit the on-chain anchor for the share event + return a
      // resolvable anchor id (idempotent — reuses the document's existing anchor).
      const shareAnchor = await emitLifecycleAnchor({
        documentId: id,
        contentHash: doc.contentHash,
        authHeader: req.headers.authorization as string,
        eventType: 'share',
      });

      return res.status(201).json({
        documentId: id,
        sharesCreated: created.length,
        shares: created,
        anchorId: shareAnchor.anchorId,
        anchor: { id: shareAnchor.anchorId, txHash: shareAnchor.txHash, status: shareAnchor.status },
      });
    } catch (error) {
      // KS-564 (Stuart's ask 2): a bad-input constraint failure is the
      // caller's to fix — answering INTERNAL_ERROR made S retry it forever on
      // every refresher tick. Map the storable-input SQLSTATEs to a 400 so S
      // can tell "will never work" from "retry later".
      const pgCode = extractPgCode(error);
      if (pgCode && ['22P02', '22001', '22007', '22008', '23502', '23503', '23514', '42804'].includes(pgCode)) {
        logger.warn('Share rejected on unstorable input', { pgCode });
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Share could not be stored: one or more fields are not storable (check recipients[].userId and expiresAt)' },
        });
      }
      logger.error('Failed to share document', { error: error instanceof Error ? error.message : String(error) });
      return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to share document' } });
    }
  },
);

/**
 * POST /api/documents/:id/revoke
 * Revoke a document
 */
documentsRouter.post(
  '/:id/revoke',
  [param('id').notEmpty().withMessage('Document ID is required')],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { id } = req.params;
      const { reason } = req.body;
      const tenantId = getReqTenantId(req);

      let document: any;
      try {
        document = await getDocument(id, tenantId, (req as any).db);
      } catch (dbErr: any) {
        if (dbErr?.message?.includes('does not exist')) {
          return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found' } });
        }
        throw dbErr;
      }
      if (!document) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found' } });
      }

      if (document.owner?.id !== user.id) {
        return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Only the owner can revoke this document' } });
      }

      if (document.status === 'revoked') {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Document is already revoked' } });
      }

      // KS-566 (G-1 ruling, KS-539): revoke is on the onBehalfOf pattern — share /
      // revoke / transfer-custody attribute to the real person behind a connector call.
      //
      // PLACEMENT (#742 review): deliberately AFTER the 404, the ownership 403 and the
      // already-revoked 400, and NOT at the top of the handler where /share and
      // /transfer-custody put it. handleOnBehalfOf writes an action_provenance row
      // carrying email_enc, display_name_enc and email_hash. At the top of the handler a
      // connector could POST /api/documents/<any-string>/revoke and persist that PII
      // against a document id that need not exist or belong to its tenant —
      // migrations/041_action_provenance.sql:33-36 makes document_id deliberately NOT a
      // foreign key and no later migration adds one, so nothing downstream rejects it.
      // Writing it here means a row exists only for a call that was going to succeed.
      // /share and /transfer-custody kept the top-of-handler shape until KS-1228, which
      // moved their row (and /version's) after the action; see checkOnBehalfOf.
      const revokeObo = await checkOnBehalfOf(req, res);
      if (!revokeObo.ok) return;
      const now = new Date().toISOString();
      await updateDocument(id, tenantId, { status: 'revoked' });

      // KS-1264: the row is recorded only now, after updateDocument, so a revoke that throws writes none.
      recordOnBehalfOf(req, id, 'revoke', revokeObo);
      // KS-319: emit the on-chain anchor for the revoke event + return a
      // resolvable anchor id (idempotent — reuses the document's existing anchor).
      // K `revoke` = global invalidation of the document (status:'revoked'); S's
      // owner-local soft-delete routes here per PS-124 (semantics noted) — the
      // anchor records the revoke against the existing document, not a derived one.
      const revokeAnchor = await emitLifecycleAnchor({
        documentId: id,
        contentHash: document.contentHash,
        authHeader: req.headers.authorization as string,
        eventType: 'revoke',
      });

      res.json({
        id: document.id,
        status: 'revoked',
        revokedAt: now,
        reason,
        anchorId: revokeAnchor.anchorId,
        anchor: { id: revokeAnchor.anchorId, txHash: revokeAnchor.txHash, status: revokeAnchor.status },
      });
    } catch (error) {
      logger.error('Failed to revoke document', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to revoke document' } });
    }
  },
);

// =============================================================================
// POST /api/documents/:id/lifecycle-events — KS-387 generic non-mutating verbs
// =============================================================================
//
// The KS-134 verbs with NO dedicated endpoint (rights-unassign / share-revoke /
// share-permission-change / rename, the KS-389 delete/restore mapping, plus the
// KS-415/PS-235 share-edit four: share-recipient-change / share-expiry-change /
// share-token-rotate / share-resend)
// previously anchored via the flat POST /api/anchors fallback and carried no
// lineage. This one extensible route (generic over per-verb — KS-274) records
// each as a NON-MUTATING lifecycle row (bytes unchanged → attaches to the
// CURRENT document via parent_document_id, no version fork) and emits a
// resolvable anchor via KS-319's shared emitLifecycleAnchor, exactly like
// /share, /transfer-custody and /revoke do — so Platform-S gets a top-level
// anchorId its CardanoAnchorRefresher can upgrade to a Cardano tx.
documentsRouter.post(
  '/:id/lifecycle-events',
  [param('id').notEmpty().withMessage('Document ID is required')],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { id } = req.params;
      const { action, payload } = (req.body ?? {}) as { action?: unknown; payload?: unknown };
      // KS-566 (G-1 ruling, KS-539): lifecycle is on the CONNECTOR pattern, so
      // `onBehalfOf` no longer applies here. A sent field is IGNORED, not 400'd
      // — Platform S is live sending it (PS-616, UAT since 2026-08-21T10:07Z)
      // and a rejection would turn this deploy into an S outage. Tightening to
      // a 400 stays available under its own ticket once S stops sending it.
      // The reserved key still never rides in payload.
      if (payload && typeof payload === 'object') {
        delete (payload as Record<string, unknown>).onBehalfOf;
      }

      // Strict vocabulary enforcement (KS-387 acceptance): unknown verbs 400 with
      // the accepted list, mirroring the flat-anchor enum (KS-388). Verbs with a
      // dedicated endpoint are rejected here too — S routes those to their own
      // endpoints; accepting them twice would double-record lifecycle rows.
      if (typeof action !== 'string' || !LIFECYCLE_EVENT_ACTIONS.includes(action as LifecycleEventAction)) {
        return res.status(400).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: `Invalid lifecycle action '${String(action ?? '')}'. Accepted: ${LIFECYCLE_EVENT_ACTIONS.join(', ')}`,
          },
        });
      }
      if (payload !== undefined && (payload === null || typeof payload !== 'object' || Array.isArray(payload))) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'payload, when supplied, must be a JSON object' },
        });
      }

      const tenantId = getReqTenantId(req);
      const doc = await getDocument(id, tenantId, (req as any).db);
      if (!doc) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found in this tenant' } });
      }

      // Record the event FIRST — the domain fact is the row; anchoring is
      // best-effort enrichment (an anchoring outage must not lose the event).
      let event;
      try {
        event = await createLifecycleEvent(
          {
            tenantId,
            documentId: id,
            action,
            payload: (payload ?? {}) as Record<string, unknown>,
            // KS-564: same ::uuid trap as /share — `actor_user_id` is a UUID
            // column and a connector principal is not a UUID. KS-566: there is
            // no onBehalfOf-resolved user on this route any more, so a
            // connector write stores NULL here and its attribution lives on the
            // connector-only action_provenance row recorded below.
            actorUserId: toActorUuid(user.id, null),
          },
          (req as any).db,
        );
      } catch (err: any) {
        if (err?.code === 'LIFECYCLE_TARGET_NOT_FOUND') {
          return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found in this tenant (resolution failed at event time)' } });
        }
        throw err;
      }

      // KS-566: one connector-only provenance row per RECORDED event. Placed
      // after the vocabulary gate and after the event row exists, so a 400'd
      // verb leaves no provenance behind and the count stays 1:1 with the
      // events it describes — which is what the pre-KS-566 comment here always
      // claimed ("recorded with the verb once it validates below") but the code
      // did not do: it recorded before validation, with an `unknown` fallback.
      recordConnectorProvenance(req, id, `lifecycle:${action}`);

      // KS-319 shared emitter: idempotent per (document, network) — the event
      // anchors against the document's existing anchor, returning a resolvable
      // anchor id (GET /api/anchors/{id}); null when anchoring is down (S falls
      // back to POST /api/anchors, its existing HTTP-failure path).
      const eventAnchor = await emitLifecycleAnchor({
        documentId: id,
        contentHash: doc.contentHash,
        authHeader: req.headers.authorization as string,
        eventType: action as LifecycleEventAction,
      });
      if (eventAnchor.anchorId) {
        await setLifecycleEventAnchor(event.id, eventAnchor.anchorId, (req as any).db);
      }

      return res.status(201).json({
        documentId: id,
        eventId: event.id,
        action,
        recordedAt: event.createdAt,
        anchorId: eventAnchor.anchorId,
        anchor: { id: eventAnchor.anchorId, txHash: eventAnchor.txHash, status: eventAnchor.status },
      });
    } catch (error) {
      // KS-564 (Stuart's ask 2): same mapping as /share — an unstorable field
      // is a 400 the caller can act on, not an opaque retryable 500.
      const pgCode = extractPgCode(error);
      if (pgCode && ['22P02', '22001', '22007', '22008', '23502', '23503', '23514', '42804'].includes(pgCode)) {
        logger.warn('Lifecycle event rejected on unstorable input', { pgCode });
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Lifecycle event could not be stored: one or more payload fields are not storable' },
        });
      }
      logger.error('Failed to record lifecycle event', { error: error instanceof Error ? error.message : String(error) });
      return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to record lifecycle event' } });
    }
  },
);

/**
 * GET /api/documents/:id/lifecycle-events
 * List a document's recorded lifecycle events (tenant-scoped, newest first) —
 * the read side of KS-387, so S (and the portals) can confirm lineage without
 * walking anchors.
 */
documentsRouter.get(
  '/:id/lifecycle-events',
  [param('id').notEmpty().withMessage('Document ID is required')],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }
      const { id } = req.params;
      const tenantId = getReqTenantId(req);
      const doc = await getDocument(id, tenantId, (req as any).db);
      if (!doc) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found in this tenant' } });
      }
      const events = await listLifecycleEvents(id, tenantId, (req as any).db);
      return res.json({ documentId: id, count: events.length, events });
    } catch (error) {
      logger.error('Failed to list lifecycle events', { error: error instanceof Error ? error.message : String(error) });
      return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to list lifecycle events' } });
    }
  },
);

// =============================================================================
// POST /api/documents/:id/sign-cert — KS-83 PR 3
// =============================================================================
//
// Active X.509 signing path. The source document's bytes stay untouched
// (KS-21 Q3 v1: out-of-band JSON envelope, not embedded). The endpoint:
//
//   1. Looks up the source doc in the caller's tenant.
//   2. Forwards a sign request to auth-service's POST /api/issuer-certs/sign
//      with the source's contentHash. Caller's Bearer token rides along so
//      auth applies the same RBAC; auth picks the tenant's active cert.
//   3. Mints a new versioned document row (parent_document_id = source)
//      carrying the signature envelope in its `data` blob. The new row's
//      contentHash equals the source's — the bytes didn't change, the
//      signature lives out-of-band in the data blob (and is served via
//      GET /api/documents/{id}/sig-json).
//   4. Returns the new doc shape + the envelope inline (so callers don't
//      need a second round-trip for the sidecar bytes).
//
// Anchoring is intentionally NOT auto-triggered (consistent with KS-86's
// /version path — caller hits POST /api/documents/{newId}/anchor when ready).
//
// Why a dedicated endpoint and not just /version action='sign-cert' with
// the caller supplying a hash they already signed somewhere else: this
// path is the one where Platform K actively uses the stored cert to sign.
// The /version endpoint is for "the issuer did something externally, please
// register it" (watermark, future PAdES). Different concern; cleaner API.
documentsRouter.post(
  '/:id/sign-cert',
  [
    param('id').notEmpty().withMessage('Document ID is required'),
    body('metadata').optional().isObject().withMessage('metadata must be an object'),
    body('title').optional().isString(),
    // Optional cert id override — when omitted, auth picks the tenant's
    // most-recently-uploaded active cert (KS-83 PR 3 v1 selection rule).
    body('certId').optional().isString().withMessage('certId must be a string'),
  ],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      if (!isAllowedByRoleOrScope(req, ALLOWED_VERSION_ROLES, 'documents:write')) {
        return res.status(403).json({
          success: false,
          error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit signing this document' },
        });
      }

      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Invalid request body', details: errors.array() },
        });
      }

      const { id } = req.params;
      const metadata = (req.body?.metadata && typeof req.body.metadata === 'object')
        ? (req.body.metadata as Record<string, unknown>)
        : {};
      const overrideTitle = typeof req.body?.title === 'string' ? req.body.title.trim() : '';
      const certIdOverride = typeof req.body?.certId === 'string' ? req.body.certId : undefined;

      // 1. Resolve source doc + tenant scope.
      const tenantId = getReqTenantId(req);
      const source = await getDocument(id, tenantId, (req as any).db);
      if (!source) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found in this tenant' } });
      }
      // KS-1213: stored as `source.type`, served as `data.documentType || type`; same refusal as /version.
      if (metadata.documentType !== undefined && metadata.documentType !== source.type) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      // 2. Call auth-service DIRECTLY (AUTH_SERVICE_URL) to sign
      // source.contentHash. KS-289: same fix as the holder-lookup paths —
      // routing this POST through the gateway both hit the gateway's CSRF
      // gate (no browser token on a service call) and fell back to an
      // unreachable http://localhost:6882 inside the container. auth's
      // /issuer-certs/sign self-authenticates from the forwarded JWT.
      const authHeader = (req.headers.authorization as string) || '';
      const authBase = process.env.AUTH_SERVICE_URL || 'http://localhost:6003';

      let envelope: {
        signature: string;
        signatureAlgorithm: string;
        signedContentHash: string;
        signedAt: string;
        cert: {
          id: string;
          fingerprintSha256: string;
          subject: string;
          issuer: string;
          certPem: string;
          validFrom: string;
          validUntil: string;
          trustLevel: string;
        };
      };
      try {
        const signRes = await fetch(`${authBase}/api/issuer-certs/sign`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(authHeader ? { Authorization: authHeader } : {}),
          },
          body: JSON.stringify({
            contentHash: source.contentHash,
            ...(certIdOverride ? { certId: certIdOverride } : {}),
          }),
        });
        if (signRes.status === 404) {
          // NO_ACTIVE_CERT — no cert uploaded for this tenant.
          const body = await signRes.json().catch(() => ({})) as { error?: { code?: string; message?: string } };
          return res.status(409).json({
            success: false,
            error: {
              code: body?.error?.code || 'NO_ACTIVE_CERT',
              message: body?.error?.message || 'No active issuer cert for this tenant. Upload one via POST /api/issuer-certs first.',
            },
          });
        }
        if (signRes.status === 403) {
          // Caller has documents:write but not issuer-certs:sign. Surface clearly.
          return res.status(403).json({
            success: false,
            error: {
              code: 'CERT_SIGN_FORBIDDEN',
              message: 'Caller has documents:write but is not authorised to use issuer-certs:sign. Request the scope from your admin.',
            },
          });
        }
        if (!signRes.ok) {
          const body = await signRes.json().catch(() => ({})) as { error?: { code?: string; message?: string } };
          // Propagate the upstream error code/status so e.g. 422 KEY_MISMATCH
          // surfaces accurately to the caller instead of being flattened to 502.
          if (signRes.status >= 400 && signRes.status < 500) {
            return res.status(signRes.status).json({
              success: false,
              error: {
                code: body?.error?.code || 'CERT_SIGN_ERROR',
                message: body?.error?.message || `Cert sign failed with status ${signRes.status}`,
              },
            });
          }
          return res.status(502).json({
            success: false,
            error: { code: 'BAD_GATEWAY', message: `Cert sign upstream returned ${signRes.status}` },
          });
        }
        envelope = await signRes.json() as typeof envelope & { success: true };
      } catch (err: any) {
        logger.warn('issuer-certs/sign unreachable during /sign-cert', { error: err?.message });
        return res.status(502).json({
          success: false,
          error: { code: 'BAD_GATEWAY', message: 'Cert sign service unavailable' },
        });
      }

      // 3. Mint the new versioned document row. contentHash matches the
      //    source (bytes unchanged); the signature lives in data blob.
      const newExternalId = `doc-${Date.now()}-${uuidv4().slice(0, 8)}`;
      try {
        await assertNoCycle(newExternalId, id, tenantId, { db: (req as any).db });
      } catch (cycleErr: any) {
        if (cycleErr?.code === 'LINEAGE_CYCLE') {
          return res.status(422).json({
            success: false,
            error: {
              code: 'LINEAGE_CYCLE',
              message: `Refusing to sign: source ${id} would form a cycle in the lineage chain (corrupted parent chain?)`,
            },
          });
        }
        throw cycleErr;
      }

      const now = new Date().toISOString();
      const sourceTitle = (source.data?.title as string) || source.type || 'Untitled';
      const derivedTitle = overrideTitle || `${sourceTitle} (signed)`;

      const sigJsonEnvelope = {
        version: 1,
        documentId: newExternalId,
        parentDocumentId: id,
        signedContentHash: envelope.signedContentHash,
        signature: envelope.signature,
        signatureAlgorithm: envelope.signatureAlgorithm,
        certFingerprintSha256: envelope.cert.fingerprintSha256,
        certPem: envelope.cert.certPem,
        subject: envelope.cert.subject,
        issuer: envelope.cert.issuer,
        trustLevel: envelope.cert.trustLevel,
        signedAt: envelope.signedAt,
        signedById: user.id,
      };

      const derivedDoc: DocumentRecord = {
        id: newExternalId,
        type: source.type,
        status: 'signed',
        owner: source.owner,
        rightsHolderId: source.rightsHolderId,
        parentDocumentId: id,
        data: {
          ...source.data,
          title: derivedTitle,
          versionAction: 'sign-cert',
          versionedAt: now,
          versionedById: user.id,
          parentDocumentId: id,
          ...metadata,
          // Signature envelope — stored alongside the versioned doc so
          // GET /sig-json can serve it without a second auth round trip.
          sigJson: sigJsonEnvelope,
        },
        contentHash: source.contentHash, // unchanged — OOB envelope per Q3
        signatures: [],
        blockchain: undefined,
        createdAt: now,
        updatedAt: now,
      };

      await saveDocument(derivedDoc, tenantId, (req as any).db);

      logger.info('Document signed via issuer cert', {
        sourceId: id,
        newId: newExternalId,
        certId: envelope.cert.id,
        certFingerprint: envelope.cert.fingerprintSha256.slice(0, 16),
        algorithm: envelope.signatureAlgorithm,
        tenantId,
        userId: user.id,
      });

      publishEvent('document.versioned' as never, {
        sourceId: id,
        newId: newExternalId,
        action: 'sign-cert',
        contentHash: source.contentHash,
        certId: envelope.cert.id,
        userId: user.id,
      }).catch(() => {});

      return res.status(201).json({
        document: {
          id: newExternalId,
          parentDocumentId: id,
          type: source.type,
          status: 'signed',
          contentHash: source.contentHash,
          action: 'sign-cert',
          title: derivedTitle,
          versionedAt: now,
          anchored: false,
        },
        sigJson: sigJsonEnvelope,
        // Convenience URL — callers can also fetch via GET /sig-json later.
        sigJsonUrl: `/api/documents/${newExternalId}/sig-json`,
      });
    } catch (error) {
      logger.error('Failed to sign document via issuer cert', {
        error: error instanceof Error ? error.message : String(error),
      });
      return res.status(500).json({
        success: false,
        error: { code: 'INTERNAL_ERROR', message: 'Failed to sign document' },
      });
    }
  },
);

// =============================================================================
// POST /api/documents/:id/sign-wallet — KS-278 (KS-274 decision)
// =============================================================================
//
// Dedicated endpoint for a DETACHED Cardano wallet signature, mirroring
// /sign-cert. The caller signs the source document's contentHash with their
// wallet (CIP-30 signData) and submits {walletAddress, signature, key}. The
// signature is out-of-band — the bytes don't change — so this mints a new
// lineage row whose contentHash EQUALS the source's, carrying the wallet
// signature envelope in data.sigWallet.
//
// Per KS-274, K verifies the signature SERVER-SIDE (Ed25519 over the COSE
// Sig_structure1, via @secuura/shared verifyMessageSignature) against the
// source's contentHash BEFORE minting — a bogus signature is rejected, never
// recorded or anchored. Anchoring is NOT auto-triggered (call .../anchor).
//
// Why a dedicated endpoint and not a /version action: a wallet signature is
// detached (no new bytes), so it doesn't fit /version's newContentHash model —
// same reasoning as /sign-cert.
documentsRouter.post(
  '/:id/sign-wallet',
  [
    param('id').notEmpty().withMessage('Document ID is required'),
    body('walletAddress').isString().notEmpty().withMessage('walletAddress is required'),
    body('signature').isString().notEmpty().withMessage('signature (hex COSESign1) is required'),
    body('key').isString().notEmpty().withMessage('key (hex COSEKey) is required'),
    body('metadata').optional().isObject().withMessage('metadata must be an object'),
    body('title').optional().isString(),
  ],
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      if (!isAllowedByRoleOrScope(req, ALLOWED_VERSION_ROLES, 'documents:write')) {
        return res.status(403).json({
          success: false,
          error: { code: 'FORBIDDEN', message: 'Your role / scope does not permit signing this document' },
        });
      }

      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          error: { code: 'VALIDATION_ERROR', message: 'Invalid request body', details: errors.array() },
        });
      }

      const { id } = req.params;
      const walletAddress = String(req.body.walletAddress).trim();
      const signature = String(req.body.signature).trim();
      const key = String(req.body.key).trim();
      const metadata = (req.body?.metadata && typeof req.body.metadata === 'object')
        ? (req.body.metadata as Record<string, unknown>)
        : {};
      const overrideTitle = typeof req.body?.title === 'string' ? req.body.title.trim() : '';

      // 1. Resolve source doc + tenant scope.
      const tenantId = getReqTenantId(req);
      const source = await getDocument(id, tenantId, (req as any).db);
      if (!source) {
        return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document not found in this tenant' } });
      }
      // KS-1213: stored as `source.type`, served as `data.documentType || type`; same refusal as /version.
      if (metadata.documentType !== undefined && metadata.documentType !== source.type) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      // 2. Verify the wallet signature SERVER-SIDE (KS-274): the wallet must
      //    have signed THIS document's contentHash. Reject before minting.
      const signatureValid = verifyMessageSignature(walletAddress, source.contentHash, signature, key);
      if (!signatureValid) {
        return res.status(400).json({
          success: false,
          error: {
            code: 'INVALID_WALLET_SIGNATURE',
            message: 'The wallet signature did not verify against this document\'s content hash. Ensure the wallet signed the document contentHash with the submitted address/key.',
          },
        });
      }

      // 3. Mint the new versioned document row. contentHash matches the source
      //    (bytes unchanged); the wallet signature lives in the data blob.
      const newExternalId = `doc-${Date.now()}-${uuidv4().slice(0, 8)}`;
      try {
        await assertNoCycle(newExternalId, id, tenantId, { db: (req as any).db });
      } catch (cycleErr: any) {
        if (cycleErr?.code === 'LINEAGE_CYCLE') {
          return res.status(422).json({
            success: false,
            error: {
              code: 'LINEAGE_CYCLE',
              message: `Refusing to sign: source ${id} would form a cycle in the lineage chain (corrupted parent chain?)`,
            },
          });
        }
        throw cycleErr;
      }

      const now = new Date().toISOString();
      const sourceTitle = (source.data?.title as string) || source.type || 'Untitled';
      const derivedTitle = overrideTitle || `${sourceTitle} (wallet-signed)`;

      const sigWalletEnvelope = {
        version: 1,
        documentId: newExternalId,
        parentDocumentId: id,
        signedContentHash: source.contentHash,
        signature,
        key,
        walletAddress,
        signatureAlgorithm: 'CIP-8/Ed25519',
        signedAt: now,
        signedById: user.id,
      };

      const derivedDoc: DocumentRecord = {
        id: newExternalId,
        type: source.type,
        status: 'signed',
        owner: source.owner,
        rightsHolderId: source.rightsHolderId,
        parentDocumentId: id,
        data: {
          ...source.data,
          title: derivedTitle,
          versionAction: 'sign-wallet',
          versionedAt: now,
          versionedById: user.id,
          parentDocumentId: id,
          ...metadata,
          // Wallet-signature envelope — stored alongside the versioned doc.
          sigWallet: sigWalletEnvelope,
        },
        contentHash: source.contentHash, // unchanged — detached wallet signature
        signatures: [],
        blockchain: undefined,
        createdAt: now,
        updatedAt: now,
      };

      await saveDocument(derivedDoc, tenantId, (req as any).db);

      logger.info('Document signed via wallet', {
        sourceId: id,
        newId: newExternalId,
        walletAddress: walletAddress.slice(0, 16),
        tenantId,
        userId: user.id,
      });

      publishEvent('document.versioned' as never, {
        sourceId: id,
        newId: newExternalId,
        action: 'sign-wallet',
        contentHash: source.contentHash,
        userId: user.id,
      }).catch(() => {});

      return res.status(201).json({
        document: {
          id: newExternalId,
          parentDocumentId: id,
          type: source.type,
          status: 'signed',
          contentHash: source.contentHash,
          action: 'sign-wallet',
          title: derivedTitle,
          versionedAt: now,
          anchored: false,
        },
        sigWallet: sigWalletEnvelope,
      });
    } catch (error) {
      logger.error('Failed to sign document via wallet', {
        error: error instanceof Error ? error.message : String(error),
      });
      return res.status(500).json({
        success: false,
        error: { code: 'INTERNAL_ERROR', message: 'Failed to wallet-sign document' },
      });
    }
  },
);

// =============================================================================
// GET /api/documents/:id/sig-json — KS-83 PR 3 (public, see KS-87)
// =============================================================================
//
// Returns the out-of-band signature envelope for a doc that was signed
// via POST /sign-cert. Per KS-21 Q3 v1 decision: the envelope is a
// separate companion artifact, NOT embedded in the file. Offline verifiers
// download both the original bytes and this envelope.
//
// No auth on this endpoint — same as the public verifier. The envelope
// only contains data that's already meant for offline distribution
// (signature, public cert, content hash). Revoked-cert state is NOT
// inferred here — the verifier checks current cert status against
// /api/issuer-certs/{id} or via the published CRL (future).
//
// KS-87: registered on publicDocumentsRouter (not documentsRouter) so the
// blanket `authenticate()` on documentsRouter doesn't fire. Mounted before
// documentsRouter in index.ts so Express matches this specific path first.
publicDocumentsRouter.get(
  '/:id/sig-json',
  [param('id').notEmpty().withMessage('Document ID is required')],
  async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const tenantId = getReqTenantId(req);
      const doc = await getDocument(id, tenantId, (req as any).db);
      if (!doc) {
        return res.status(404).json({
          success: false,
          error: { code: 'NOT_FOUND', message: 'Document not found' },
        });
      }

      const sigJson = (doc.data as Record<string, unknown>)?.sigJson;
      if (!sigJson || typeof sigJson !== 'object') {
        return res.status(404).json({
          success: false,
          error: {
            code: 'NO_SIG_JSON',
            message: 'This document does not have an X.509 signature envelope. Was it created via POST /api/documents/{id}/sign-cert?',
          },
        });
      }

      // Content-Disposition so the response can be saved straight to disk
      // as `<id>.sig.json` — convenient for SSD-side download flows.
      res.setHeader('Content-Type', 'application/json');
      res.setHeader('Content-Disposition', `inline; filename="${id}.sig.json"`);
      return res.status(200).json(sigJson);
    } catch (error) {
      logger.error('Failed to get sig-json', {
        error: error instanceof Error ? error.message : String(error),
      });
      return res.status(500).json({
        success: false,
        error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch sig-json' },
      });
    }
  },
);

export default documentsRouter;
