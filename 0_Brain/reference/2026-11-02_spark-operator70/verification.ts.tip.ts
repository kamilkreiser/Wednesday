/**
 * =============================================================================
 * VERIFICATION ROUTES
 * =============================================================================
 * API endpoints for document verification, hash validation, and integrity checks
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { body, validationResult } from 'express-validator';
import crypto from 'crypto';
import { logger } from '../utils/logger';
import { ERASED_MARKER } from '../utils/erasureMarker';
import { prisma, getTenantManager } from '../db';
// KS-458: fail-closed RLS — cross-tenant registry lookups must query the
// resolved tenant's rows under THAT tenant's GUC (bundled in-transaction),
// not the request's (public verify has no auth → default-tenant ALS).
import { runWithTenantId, queryWithTenantGuc } from '@secuura/shared';
import {
  walkAncestors as walkDocumentAncestors,
  walkDescendants as walkDocumentDescendants,
  MAX_LINEAGE_DEPTH,
  type LineageEntry,
} from '../repositories/documentRepo';

export const verificationRouter = Router();

// KS-252: ceiling on the chain-first lookup to the anchoring service. Without
// it, anchoring's wallet-history chain scan (~20-30 s for a hash that is not
// anchored yet) stalls the public verify endpoint for its full duration —
// 39% of verifies timed out client-side under the KS-194 load baseline. On
// abort we fall through to the local-DB verify path, which both call sites
// already do for any chain-lookup error. Must stay ABOVE anchoring's
// VERIFY_CHAIN_SCAN_BUDGET_MS (default 4 s) so bounded cross-env chain hits
// still arrive.
export const CHAIN_VERIFY_TIMEOUT_MS = parseInt(process.env.CHAIN_VERIFY_TIMEOUT_MS || '5000', 10);

// =============================================================================
// KS-522 — honest labelling of simulated anchors
// =============================================================================
// A `tx_sim_…`/`mock_tx_`/`mock_batch_tx_`/`tx_…` transaction hash corresponds to NO Cardano
// transaction (SIMULATE_ANCHORING or the legacy dev mock wrote it). Simulation
// is legitimate for local/demo use — presenting its output as on-chain proof
// is not, because the verify response is the artefact a relying party acts on.
// Every verify response passes its blockchain blob through this presenter:
// a simulated anchor keeps document-level verification (content integrity +
// certification status are real) but makes NO on-chain claim — `txHash` is
// nulled (the placeholder moves to `simulatedTxRef`), `anchored` flips false,
// and a machine-readable `simulated: true` marker is set (also surfaced
// top-level by the response builders).
const FABRICATED_TXHASH_RE = /^(tx_sim_|mock_tx_|mock_batch_tx_|tx_)/;

export function presentBlockchainHonestly(blob: unknown): unknown {
  if (!blob || typeof blob !== 'object') return blob;
  const b = blob as Record<string, unknown>;
  const tx = typeof b.txHash === 'string' ? b.txHash : undefined;
  // KS-1628: any TRUTHY `simulated` counts ('true', 1), not only `=== true` — the rule the retired
  // gateway handler applied (`Boolean(persistedSimulated)`, KS-1069). Absent or false still does not.
  const simulated = Boolean(b.simulated) || (tx !== undefined && FABRICATED_TXHASH_RE.test(tx));
  if (!simulated) return blob;
  return {
    ...b,
    simulated: true,
    anchored: false,
    txHash: null,
    ...(tx ? { simulatedTxRef: tx } : {}),
    // A scan URL for a non-existent tx is itself a false claim.
    cardanoScanUrl: undefined,
  };
}

// =============================================================================
// KS-563 — certified is not anchored
// =============================================================================
// `checks.isCertified` used to be true for `certified | anchored | signed`, so a
// document that was merely originated and auto-anchored (every Platform S
// upload) reported certification nobody performed — a live false "Certified by
// issuer" in front of end users. Certification is now the narrow claim it
// names: an issuer certified this document. Anchoring gets its own honest
// flag, and the certification act — who/when/which certification — is
// surfaced as an object that is ABSENT when no certification happened.
//
// `verified` / `integrityVerified` deliberately keep the OLD broad set
// (VERIFIABLE_STATUSES): their meaning is "in the registry, hash intact, not
// revoked", which is unchanged by this fix. Narrowing them would flip every
// upload-only document to `verified: false` and break consumers for a defect
// that lives in the certification flag alone.
const CERTIFIED_STATUS = 'certified';
const VERIFIABLE_STATUSES = new Set([CERTIFIED_STATUS, 'anchored', 'signed']);

// KS-584 P3: exported for the /v2 list contract (routes/verificationV2.ts),
// which presents every same-hash registration through the SAME honesty rules
// v1 applies to its selected row. Pure predicates/builders only — exporting
// them changes no v1 behaviour.
export const isCertifiedStatus = (status: unknown): boolean => status === CERTIFIED_STATUS;
export const isVerifiableStatus = (status: unknown): boolean => VERIFIABLE_STATUSES.has(String(status));

/** KS-1628: anchoring's terminal failure ('failed') and originate's own 'anchor_failed'. */
const FAILED_ANCHOR_STATUSES: ReadonlySet<string> = new Set(['failed', 'anchor_failed']);

/**
 * KS-1628: a positive integer NUMBER, or a positive-integer digit STRING. The retired gateway handler
 * took numbers only (KS-1069 item 1); Wednesday ruled (b) on 2026-10-19 to accept the digit string too,
 * because it is a real stored shape - originate's heal path writes anchoring's raw pg BIGINT (KS-1129),
 * and one live demo anchor carries it. -1, 0, '0', '04', '4.2', 4.2 and non-numeric text are refused.
 */
const DIGIT_HEIGHT_RE = /^[1-9][0-9]*$/;
function isAnchorHeight(value: unknown): boolean {
  if (typeof value === 'number') return Number.isInteger(value) && value > 0;
  return typeof value === 'string' && DIGIT_HEIGHT_RE.test(value);
}

/**
 * True only for a real, non-simulated on-chain anchor. KS-522 rules apply: a placeholder
 * (`tx_sim_`/`mock_tx_`/`mock_batch_tx_`/`tx_…`, KS-1628) is not an anchor; never sets this.
 * Takes the blob ALREADY passed through presentBlockchainHonestly (which flips
 * `anchored` false and nulls `txHash` on simulated rows).
 */
export function isAnchoredHonestly(honestChain: unknown, status?: unknown): boolean {
  if (honestChain && typeof honestChain === 'object') {
    // A chain blob is the authoritative answer — do NOT fall back to the
    // document status when one exists. `documents.status` flips to 'anchored'
    // when the anchor is SUBMITTED, so a still-pending anchor (status
    // 'pending', txHash null) would otherwise report isAnchored: true — the
    // same unearned claim this ticket exists to remove, one field over.
    const c = honestChain as Record<string, unknown>;
    // KS-1628: truthy, not `=== true` — see presentBlockchainHonestly.
    if (c.simulated) return false;
    // KS-1628: a failed anchor is not an anchor, whatever else the blob says. The chain-first blobs
    // carry `anchored: true` and no status, so they are unaffected; a stored blob that pairs
    // `anchored: true` with a failed status was on-chain before this line.
    if (FAILED_ANCHOR_STATUSES.has(String(c.status))) return false;
    // The stored blob is `{status, txHash, network, anchorId, anchoredAt,
    // blockHeight}` — anchoring's vocabulary is pending | submitted |
    // confirmed | failed (services/anchoring/src/index.ts) and there is NO
    // `anchored` boolean on a real row. The chain-first branches DO build a
    // blob with `anchored: true`, so accept either shape. Only 'confirmed'
    // counts: 'submitted' means the tx is in flight and may still fail — the
    // KS-535 class — so it has not earned the claim yet.
    const settled = c.anchored === true || c.status === 'confirmed';
    // KS-1628: a real hash is 64 hex characters (REAL_TXHASH_RE), not merely a non-empty string, and a
    // height that IS reported must be a real one (isAnchorHeight). A height that is not reported at all
    // (undefined, or the null anchoring's toBlockNumber returns when it has none) keeps today's answer:
    // the chain-first branches build their blob from that value, and ks563 pins that shape as on-chain.
    const heightOk = c.blockHeight === undefined || c.blockHeight === null || isAnchorHeight(c.blockHeight);
    return settled && typeof c.txHash === 'string' && REAL_TXHASH_RE.test(c.txHash) && heightOk;
  }
  // No chain blob at all — the document's own status is all we have.
  return status === 'anchored';
}

/**
 * The certification act, or undefined when the document was never certified.
 * Built from `certification_metadata`, which `POST /api/certifications/issue`
 * already writes (issuerName / certificationId / certificationType /
 * certifiedAt) alongside `status='certified'` — no new persistence needed.
 * Absent (not null) so a consumer's `if (res.certification)` is the honest test.
 */
export function buildCertification(doc: any): Record<string, unknown> | undefined {
  if (!isCertifiedStatus(doc?.status)) return undefined;
  const certMeta = (doc?.certification_metadata || {}) as Record<string, any>;
  const certifiedAt = certMeta.certifiedAt || doc?.certified_at || undefined;
  const certifiedBy =
    certMeta.issuerName
    || certMeta.certificationData?.issuedBy
    || doc?.organization_name
    || undefined;
  return {
    certificationId: certMeta.certificationId ?? null,
    certificationType: certMeta.certificationType ?? null,
    certifiedAt: certifiedAt ? new Date(certifiedAt).toISOString() : null,
    certifiedBy: certifiedBy ?? null,
    certifierOrganizationId: certMeta.issuerId ?? null,
  };
}

// =============================================================================
// KS-584 (interim) — select the registration that evidences its claims
// =============================================================================
// Verify-by-hash used to resolve a content hash to ONE arbitrary row
// (`ORDER BY certified_at DESC NULLS LAST LIMIT 1`) — but the normal certify
// flow creates a SECOND row for the same bytes (the certification's
// signed_document, which carries no chain data), and `certified_at` is NULL on
// whole row-sets in production, so the pick was effectively arbitrary. Live
// consequence (UAT, 2026-08-07): a certified document with three confirmed
// on-chain anchors verified as neither certified nor anchored. The full fix is
// the P3 lookup contract (UUID primary key; verify-by-hash returns a list);
// this interim keeps LIMIT 1 semantics for consumers but picks the row that
// can actually support the answer, and reads certification evidence from the
// same-hash registration set rather than only the selected row.
export const REAL_TXHASH_RE = /^[0-9a-f]{64}$/i;

export function chainBlobOfRow(row: any): Record<string, unknown> | null {
  const certMeta = row?.certification_metadata || {};
  const meta = row?.metadata || {};
  const blob = certMeta.blockchain || meta.blockchain;
  return blob && typeof blob === 'object' ? (blob as Record<string, unknown>) : null;
}

export function rowHasRealTx(row: any): boolean {
  const b = chainBlobOfRow(row);
  if (!b || b.simulated === true) return false;
  return typeof b.txHash === 'string' && REAL_TXHASH_RE.test(b.txHash);
}

export const rowCreatedMs = (row: any): number => {
  const t = row?.created_at instanceof Date ? row.created_at.getTime() : Date.parse(String(row?.created_at ?? ''));
  return Number.isFinite(t) ? t : Number.MAX_SAFE_INTEGER;
};

/**
 * Pick the row that best evidences the platform's claims for these bytes:
 *   1. a `certified` row (the legacy certify path writes one);
 *   2. else a row with a REAL on-chain tx (KS-522, KS-1628: no FABRICATED_TX_PREFIX
 *      placeholder counts) — 'confirmed' chain state first, then the ORIGINAL registration
 *      (created_at ASC), since derived signed_document rows are later copies;
 *   3. else the oldest row — deterministic, where the legacy NULLS LAST order
 *      was arbitrary.
 * Input rows keep the query's certified_at DESC pre-sort, so within rule 1 the
 * most recent certification still wins.
 */
function selectVerifiableRow(rows: any[]): any | undefined {
  if (!rows || rows.length === 0) return undefined;
  if (rows.length === 1) return rows[0];
  const certified = rows.filter((r) => isCertifiedStatus(r?.status));
  if (certified.length > 0) return certified[0];
  const anchored = rows.filter(rowHasRealTx).sort((a, b) => {
    const aConfirmed = chainBlobOfRow(a)?.status === 'confirmed' ? 0 : 1;
    const bConfirmed = chainBlobOfRow(b)?.status === 'confirmed' ? 0 : 1;
    if (aConfirmed !== bConfirmed) return aConfirmed - bConfirmed;
    return rowCreatedMs(a) - rowCreatedMs(b);
  });
  if (anchored.length > 0) return anchored[0];
  return [...rows].sort((a, b) => rowCreatedMs(a) - rowCreatedMs(b))[0];
}

/**
 * KS-1557 (read side). Which derived 'signed' rows may testify to a certification act?
 *
 * The lineage certify path (`POST /api/certifications/issue` with parentDocumentId) records the act on a DERIVED row (status 'signed',
 * `metadata.certificationId`) and leaves the parent untouched. The derived row's `metadata` is filled from the CALLER'S `data` (the
 * caller's keys are spread AFTER the server's), so everything in it - certificationId, certifiedAt, certificationType, issuerId - is
 * caller-chosen. Reading the evidence from there let a caller choose what verify presented, and let a row whose hash is not its
 * parent's count. The rule now: a derived row counts only when ALL of these hold, and the presented id, type and time come from the
 * real certification row, never from the derived row's metadata:
 *   1. status 'signed', and `metadata.certificationId` is a UUID;
 *   2. its parent link is set, and the parent's hash equals its own (the parent is read from the same-hash set, else one lookup);
 *   3. its external id carries the first 8 hex characters of that certification id (the route generates doc-<ms>-<certId8>), so a row
 *      cannot cite someone else's genuine certification;
 *   4. that certification id RESOLVES, in the row's own tenant, to a real certification row (a `documents` row written by
 *      saveCertification: certification_metadata carries certificationType and holderId);
 *   5. the derived row's owner is the certification's issuer (owner_user_id equals issuer_user_id; both NULL for a connector principal).
 * `certifiedBy` stays the caller-asserted display string it always was (ruled); `certifierOrganizationId` is null here because the
 * certification row stores the issuer's USER id, not an organisation id (the organisation-id fix is the write side).
 */
export const MAX_EVIDENCE_LOOKUPS = 8;
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const DERIVED_EXTERNAL_ID_RE = /^doc-\d+-([0-9a-f]{8})$/i;
const normaliseRowHash = (h: unknown): string => String(h ?? '').replace(/^sha256:/i, '').toLowerCase();

export interface CertificationEvidenceContext { db?: any }
export type TrustedEvidence = ReadonlyMap<unknown, Record<string, unknown>>;

/** The certification id a derived row CLAIMS, when it is shaped like a certify-lineage child. No I/O. */
function claimedCertificationId(row: any): string | null {
  if (row?.status !== 'signed' || !row?.parent_document_id) return null;
  const certId = (row?.metadata as Record<string, unknown> | undefined)?.certificationId;
  if (typeof certId !== 'string' || !UUID_RE.test(certId)) return null;
  const m = DERIVED_EXTERNAL_ID_RE.exec(String(row?.external_id ?? ''));
  if (!m || m[1].toLowerCase() !== certId.slice(0, 8).toLowerCase()) return null;
  return certId.toLowerCase();
}

/** Run one tenant-scoped read for a row: the row's own tenant pool when it came from another tenant, else the request's db. */
async function readForRow(row: any, ctx: CertificationEvidenceContext, sql: string, params: unknown[], tagged: (db: any) => Promise<any[]>): Promise<any[]> {
  if (row?._tenantId) {
    const mgr = getTenantManager();
    if (!mgr) return [];
    const tenant = String(row._tenantId);
    const out = await runWithTenantId(tenant, () => queryWithTenantGuc(mgr.getPool(tenant), sql, params));
    return out.rows;
  }
  return tagged(ctx.db || prisma);
}

async function fetchParentHash(row: any, tenant: string, ctx: CertificationEvidenceContext): Promise<string | null> {
  const parent = String(row.parent_document_id);
  if (!UUID_RE.test(parent)) return null;
  const rows = await readForRow(row, ctx, 'SELECT content_hash FROM documents WHERE id = $1::uuid AND tenant_id = $2::uuid LIMIT 1', [parent, tenant],
    (db) => db.$queryRaw`SELECT content_hash FROM documents WHERE id = ${parent}::uuid AND tenant_id = ${tenant}::uuid LIMIT 1`);
  return rows.length > 0 ? normaliseRowHash(rows[0].content_hash) : null;
}

async function fetchCertificationRow(row: any, certId: string, tenant: string, ctx: CertificationEvidenceContext): Promise<any | null> {
  const rows = await readForRow(row, ctx,
    'SELECT id, status, document_type, certified_at, created_at, issuer_user_id, certification_metadata FROM documents WHERE id = $1::uuid AND tenant_id = $2::uuid LIMIT 1', [certId, tenant],
    (db) => db.$queryRaw`SELECT id, status, document_type, certified_at, created_at, issuer_user_id, certification_metadata FROM documents WHERE id = ${certId}::uuid AND tenant_id = ${tenant}::uuid LIMIT 1`);
  return rows[0] ?? null;
}

/** A real certification row is one saveCertification wrote: it carries certificationType and holderId in certification_metadata. */
function isCertificationRow(cert: any, certId: string, derived: any): boolean {
  if (!cert || String(cert.id).toLowerCase() !== certId || String(cert.id) === String(derived?.id)) return false;
  const cm = (cert.certification_metadata || {}) as Record<string, unknown>;
  return typeof cm.certificationType === 'string' && cm.certificationType.length > 0 && cm.holderId !== undefined && cm.holderId !== null;
}

/**
 * Resolve, for every row of the set that claims to be a certify-lineage child, whether it is a GENUINE act, and the evidence to
 * present. Fail closed: any miss, mismatch or error leaves the row out. At most MAX_EVIDENCE_LOOKUPS claimed rows are examined.
 * The result is keyed by the row OBJECT, so callers pass it to siblingCertification / ownRowCertification with the same rows.
 */
export async function resolveTrustedCertificationEvidence(rows: any[], ctx: CertificationEvidenceContext): Promise<TrustedEvidence> {
  const trusted = new Map<unknown, Record<string, unknown>>();
  let examined = 0;
  for (const r of rows || []) {
    const claimed = claimedCertificationId(r);
    if (!claimed) continue;
    if (examined >= MAX_EVIDENCE_LOOKUPS) break;
    examined += 1;
    try {
      const tenant = String(r?._tenantId ?? r?.tenant_id ?? '');
      if (!UUID_RE.test(tenant)) continue;
      const own = normaliseRowHash(r.content_hash);
      const inSet = rows.find((p: any) => p !== r && String(p?.id) === String(r.parent_document_id));
      const parentHash = inSet ? normaliseRowHash(inSet.content_hash) : await fetchParentHash(r, tenant, ctx);
      if (parentHash === null || parentHash !== own) continue;
      const cert = await fetchCertificationRow(r, claimed, tenant, ctx);
      if (!isCertificationRow(cert, claimed, r)) continue;
      // The certify route saves the derived row owned by the ISSUER and the certification row with the same issuer, so the two agree (both a
      // UUID for a person, both NULL for a connector principal). A sign-cert / sign-wallet row is owned by the SOURCE's owner, so it cannot cite
      // an actor's certification unless that actor owns the source.
      if (String(r.owner_user_id ?? '') !== String(cert.issuer_user_id ?? '')) continue;
      const meta = (r?.metadata || {}) as Record<string, any>;
      const cm = (cert.certification_metadata || {}) as Record<string, any>;
      const at = cert.certified_at ?? cert.created_at ?? null;
      trusted.set(r, {
        certificationId: String(cert.id),
        certificationType: cm.certificationType,
        certifiedAt: at ? new Date(at).toISOString() : null,
        certifiedBy: meta.issuerName ?? meta.issuedBy ?? r?.organization_name ?? null,
        certifierOrganizationId: null,
      });
    } catch (err: any) {
      logger.warn('KS-1557: certification evidence lookup failed - the row is not counted', { rowId: r?.id, error: err?.message });
    }
  }
  return trusted;
}

/**
 * The certification act evidenced elsewhere in the same-hash registration set: a 'certified' sibling (the legacy path writes one), else a
 * derived 'signed' row that resolveTrustedCertificationEvidence accepted. `trusted` is REQUIRED (no default): a call site that forgot to
 * resolve would otherwise fail open.
 */
function siblingCertification(rows: any[], selected: any, trusted: TrustedEvidence): Record<string, unknown> | undefined {
  if (!rows || rows.length < 2) return undefined;
  for (const r of rows) {
    if (r === selected) continue;
    if (isCertifiedStatus(r?.status)) return buildCertification(r);
    const evidence = trusted.get(r);
    if (evidence) return evidence;
  }
  return undefined;
}

// =============================================================================
// KS-584 (interim) — tenant-owned fields do not cross the tenant boundary
// =============================================================================
// Verify is reachable without authentication, and (in multi-tenant mode) the
// row that answers can belong to a DIFFERENT tenant than the caller. The row's
// existence + integrity + anchor facts are the service; the tenant-owned
// naming (title, issuer/organisation) is a disclosure — possession of widely
// shared bytes (a template, a statutory form) must not reveal which named
// organisation registered them. Lineage walks are skipped entirely for scoped
// responses (they enumerate tenant-owned document chains).
function callerTenantOf(req: Request): string | null {
  const user = (req as any).user as Record<string, unknown> | undefined;
  const fromUser = user?.tenantId;
  const fromReq = (req as any).tenantId;
  const v = (typeof fromUser === 'string' && fromUser) || (typeof fromReq === 'string' && fromReq) || null;
  return v ? String(v).toLowerCase() : null;
}

export function isCrossTenantResponse(req: Request, row: any): boolean {
  const rowTenant = row?._tenantId ?? row?.tenant_id ?? null;
  if (!rowTenant) return false; // no tenancy info on the row — nothing to scope by
  const caller = callerTenantOf(req);
  return !caller || String(rowTenant).toLowerCase() !== caller;
}

export function scopeTenantFields<T extends Record<string, unknown>>(response: T, scoped: boolean): T {
  if (!scoped) return response;
  return {
    ...response,
    title: null,
    issuer: null,
    // The certification act stays, minus the tenant-owned naming.
    ...(response.certification && typeof response.certification === 'object'
      ? { certification: { ...(response.certification as Record<string, unknown>), certifiedBy: null } }
      : {}),
  };
}

// KS-584 (interim): bounded rowset for the same-hash registration scan. Far
// above the real duplicate counts (max observed: 5 rows per hash) while
// keeping a pathological hash from dragging the whole set through JS.
export const VERIFY_ROWSET_LIMIT = 24;

// Moved to utils/blockHeight.ts (KS-1333) so the anchorStateSync service can use the same shaping without importing a route
// module; re-exported here so every existing importer, and the KS-1129 cells, keep working unchanged.
import { toBlockHeight } from '../utils/blockHeight';
export { toBlockHeight };
// KS-1384 R2b part 5: the verify heals' one shared path (see healVerifyRow below).
import { healAnchorForVerify } from '../services/anchorStateSync';

/**
 * KS-1384 R2b part 5 (D3): the v1 and v2 verify heals are ONE shared path, anchorStateSync healAnchorForVerify, for one stored
 * row. It reads the blob's own anchor row with the caller's bearer and lets the one resolver decide; only a `confirmed`
 * decision is presented and written (through the conditional blob write, never over a confirmed blob). Before R2b this file
 * held confirmStalePendingAnchor, which healed from verify-by-hash's chain answer on the same tx OR sameDoc, and
 * persistHealedAnchor, which wrote that through updateDocument; both are gone. A cross-tenant row (`_tenantId`) came from another
 * tenant's pool, so it is presented and never written here.
 */
export async function healVerifyRow(row: any, blob: Record<string, unknown> | null, authHeader: string): Promise<Record<string, unknown> | null> {
  return healAnchorForVerify({
    documentId: String(row?.external_id || row?.id || ''),
    documentPk: row?.id ? String(row.id) : null,
    tenantId: row?.tenant_id ? String(row.tenant_id) : null,
    blob,
    contentHash: String(row?.content_hash || ''),
    updatedAt: row?.updated_at ?? null,
    authHeader,
    write: !row?._tenantId,
  });
}

// =============================================================================
// CROSS-TENANT DOCUMENT LOOKUP
// =============================================================================

/**
 * Register a document in the platform cross-tenant registry.
 * Called when a document is created or certified.
 */
export async function registerInPlatformRegistry(doc: {
  documentId: string;
  contentHash: string;
  tenantId?: string;
  tenantSlug?: string;
  documentType?: string;
  title?: string;
  status?: string;
}): Promise<void> {
  const mgr = getTenantManager();
  if (!mgr) return; // Not in multi-tenant mode

  try {
    const platformPool = mgr.getPlatformPool();
    await platformPool.query(
      `INSERT INTO platform_document_registry (content_hash, document_id, tenant_id, tenant_slug, document_type, title, status)
       VALUES ($1, $2, $3::uuid, $4, $5, $6, $7)
       ON CONFLICT (content_hash, tenant_id) DO UPDATE SET
         document_id = EXCLUDED.document_id, title = EXCLUDED.title, status = EXCLUDED.status, updated_at = NOW()`,
      [doc.contentHash, doc.documentId, doc.tenantId, doc.tenantSlug, doc.documentType, doc.title, doc.status || 'active'],
    );
  } catch (err: any) {
    logger.warn('Failed to register document in platform registry', { error: err?.message });
  }
}

/**
 * Look up a document across all tenants when it can't be found in the current DB.
 * Queries the platform_document_registry, then the specific tenant DB.
 */
async function crossTenantLookup(documentId: string, hashToVerify?: string): Promise<any | null> {
  const mgr = getTenantManager();
  if (!mgr) return null;

  try {
    const platformPool = mgr.getPlatformPool();

    // Search registry by documentId or hash
    let registryRows;
    if (documentId) {
      registryRows = await platformPool.query(
        'SELECT * FROM platform_document_registry WHERE document_id = $1 LIMIT 1',
        [documentId],
      );
    }
    if ((!registryRows || registryRows.rows.length === 0) && hashToVerify) {
      registryRows = await platformPool.query(
        'SELECT * FROM platform_document_registry WHERE content_hash = $1 LIMIT 1',
        [hashToVerify],
      );
    }

    if (!registryRows || registryRows.rows.length === 0) return null;

    const reg = registryRows.rows[0];
    const tenantPool = mgr.getPool(reg.tenant_id);

    // Query the tenant's DB for full document details — search by hash first, then ID.
    // KS-458: documents/organizations are fail-closed flip tables; the registry
    // row's tenant must WIN over the request context, so scope explicitly to
    // reg.tenant_id and bundle the GUC in the same transaction as each query.
    const searchHash = hashToVerify ? hashToVerify.replace(/^sha256:/, '') : null;
    let docRows;
    if (searchHash) {
      // KS-584 (interim): fetch the same-hash SET and select the row that
      // evidences its claims, instead of an arbitrary LIMIT 1.
      docRows = await runWithTenantId(reg.tenant_id, () => queryWithTenantGuc(
        tenantPool,
        `SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
                d.certification_metadata, d.metadata, d.created_at, d.certified_at,
                d.tenant_id, d.parent_document_id, d.owner_user_id, o.name AS organization_name
         FROM documents d
         LEFT JOIN organizations o ON d.issuer_organization_id = o.id
         WHERE d.content_hash = $1 OR d.content_hash = $2 OR d.content_hash = $3
         ORDER BY d.certified_at DESC NULLS LAST LIMIT ${VERIFY_ROWSET_LIMIT}`,
        [hashToVerify, searchHash, `sha256:${searchHash}`],
      ));
    }
    // KS-1119: the id lookup says which document an id names; it says nothing about a hash. It runs only when NO hash
    // was supplied (the documentId-only strategy, which never claims integrity). When a hash was supplied and the hash
    // query above found nothing, the answer is "not found": falling back to the id made strategy 1 present an
    // uncompared row as a hash match, and made verify-file (documentId '') match any row with an empty external_id.
    if ((!docRows || docRows.rows.length === 0) && !hashToVerify) {
      docRows = await runWithTenantId(reg.tenant_id, () => queryWithTenantGuc(
        tenantPool,
        `SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
                d.certification_metadata, d.metadata, d.created_at, d.certified_at,
                d.tenant_id, o.name AS organization_name
         FROM documents d
         LEFT JOIN organizations o ON d.issuer_organization_id = o.id
         WHERE d.external_id = $1 LIMIT 1`,
        [documentId],
      ));
    }

    if (!docRows || docRows.rows.length === 0) return null;

    const selected = selectVerifiableRow(docRows.rows);
    // KS-1557: the rows were read from THIS tenant's pool, so the evidence lookups run there too (readForRow keys on _tenantId).
    for (const r of docRows.rows) r._tenantId = reg.tenant_id;
    const trusted = await resolveTrustedCertificationEvidence(docRows.rows, {});
    return {
      ...selected,
      _tenantId: reg.tenant_id,
      _tenantSlug: reg.tenant_slug,
      // KS-584 (interim): certification evidence can live on a same-hash
      // sibling (the certify lineage path); carry it so response builders
      // don't lose it when the anchored row wins selection.
      _siblingCertification: siblingCertification(docRows.rows, selected, trusted),
    };
  } catch (err: any) {
    logger.warn('Cross-tenant lookup failed', { documentId, error: err?.message });
    return null;
  }
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

export function generateHash(data: Record<string, unknown> | string): string {
  const content = typeof data === 'string' ? data : JSON.stringify(data, Object.keys(data).sort());
  return `sha256:${crypto.createHash('sha256').update(content).digest('hex')}`;
}

// =============================================================================
// ROUTES
// =============================================================================

/**
 * POST /api/verification/verify-file
 * Upload a document file → server hashes it → looks up hash in registry.
 * This is the strongest verification — the server computes the hash from
 * the raw file bytes, so a client cannot lie about the hash.
 *
 * If the hash matches a certified document: VERIFIED (authentic)
 * If the hash is not found: NOT VERIFIED (document was never certified,
 * or has been modified — even a single byte change fails verification)
 */
verificationRouter.post('/verify-file', async (req: Request, res: Response) => {
  try {
    // Read raw body and hash it
    const chunks: Buffer[] = [];
    await new Promise<void>((resolve, reject) => {
      req.on('data', (chunk: Buffer) => chunks.push(chunk));
      req.on('end', resolve);
      req.on('error', reject);
    });

    const fileBuffer = Buffer.concat(chunks);
    if (fileBuffer.length === 0) {
      return res.status(400).json({
        verified: false,
        error: 'No file content received. Upload the document file as the request body.',
      });
    }

    const fileHash = `sha256:${crypto.createHash('sha256').update(fileBuffer).digest('hex')}`;
    const hashNorm = fileHash.replace('sha256:', '');

    logger.info('File verification request', { size: fileBuffer.length, hash: fileHash.substring(0, 30) + '...' });

    const db = (req as any).db || prisma;

    // Search for this hash in current tenant DB.
    // KS-584 (interim): fetch the same-hash SET (bounded) — selection happens
    // in selectVerifiableRow, not in an arbitrary LIMIT 1.
    let rows: any[] = await db.$queryRaw`
      SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
             d.certification_metadata, d.metadata, d.created_at, d.certified_at,
             d.tenant_id, d.parent_document_id, d.owner_user_id, o.name AS organization_name
      FROM documents d
      LEFT JOIN organizations o ON d.issuer_organization_id = o.id
      WHERE d.content_hash = ${fileHash} OR d.content_hash = ${hashNorm} OR d.content_hash = ${'sha256:' + hashNorm}
      ORDER BY d.certified_at DESC NULLS LAST
      LIMIT ${VERIFY_ROWSET_LIMIT}
    `;

    // Cross-tenant lookup if not found locally
    if (rows.length === 0) {
      const crossDoc = await crossTenantLookup('', fileHash);
      if (crossDoc) {
        rows = [crossDoc];
        logger.info('File hash found via cross-tenant lookup', { tenant: crossDoc._tenantSlug });
      }
    }

    // Chain-first fallback — ask the anchoring service if this hash was anchored
    // on-chain in any environment. Source of truth is the chain, not our DB.
    if (rows.length === 0) {
      try {
        const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
        const resp = await fetch(`${anchoringBase}/api/anchors/verify/${encodeURIComponent(hashNorm)}`, {
          signal: AbortSignal.timeout(CHAIN_VERIFY_TIMEOUT_MS), // KS-252
        });
        if (resp.ok) {
          const chain: any = await resp.json();
          if (chain?.verified === true) {
            logger.info('File hash verified via chain-first lookup', { hash: hashNorm.substring(0, 16), source: chain.source });
            // KS-522: legacy mock rows can surface via the chain index —
            // never present a fabricated hash as an on-chain claim.
            const honestChain = presentBlockchainHonestly({
              anchored: true,
              network: chain.network,
              txHash: chain.txHash,
              blockHeight: chain.blockNumber,
              cardanoScanUrl: chain.cardanoScanUrl,
              confirmedAt: chain.confirmedAt,
              simulated: chain.simulated,
            });
            // KS-563: this branch found the hash ON CHAIN and nothing else. It
            // must claim only what it performed: the hash matched an anchor.
            // Certification is a separate act with no evidence here unless the
            // on-chain metadata carries a certification id.
            const chainCertId = chain.metadata?.certId || chain.metadata?.certificationId || null;
            const chainIsCertified = Boolean(chainCertId);
            return res.json({
              verified: true,
              fileHash,
              fileSize: fileBuffer.length,
              source: chain.source === 'chain' ? 'blockchain' : 'blockchain-indexed',
              documentId: chain.metadata?.documentId || chain.metadata?.certId,
              title: null,
              documentType: chain.metadata?.documentType || null,
              status: 'anchored',
              certifiedAt: chain.confirmedAt,
              issuer: chain.metadata?.issuerName || chain.metadata?.issuerOrgId || null,
              blockchain: honestChain,
              ...(chainIsCertified
                ? {
                    certification: {
                      certificationId: chainCertId,
                      certificationType: chain.metadata?.certificationType ?? null,
                      certifiedAt: chain.confirmedAt ?? null,
                      certifiedBy: chain.metadata?.issuerName ?? null,
                      certifierOrganizationId: chain.metadata?.issuerOrgId ?? null,
                    },
                  }
                : {}),
              onChainMetadata: chain.metadata,
              checks: {
                documentExists: true,
                hashValid: true,
                isCertified: chainIsCertified,
                isAnchored: isAnchoredHonestly(honestChain, 'anchored'),
                isRevoked: false,
                integrityVerified: true,
              },
              verifiedAt: new Date().toISOString(),
            });
          }
        }
      } catch (chainErr: any) {
        logger.warn('Chain-first verify-file lookup failed', { error: chainErr?.message });
      }
    }

    if (rows.length === 0) {
      return res.json({
        verified: false,
        fileHash,
        fileSize: fileBuffer.length,
        error: 'This document is NOT in the Secuura registry. It may have been modified, or was never certified on this platform.',
        checks: { documentExists: false, hashValid: false, integrityVerified: false },
      });
    }

    // KS-584 (interim): select the row that evidences its claims; read
    // certification evidence from the whole same-hash set; confirm a stale
    // 'pending' chain state against the chain index before presenting it.
    const doc = selectVerifiableRow(rows);
    const isRevoked = doc.status === 'revoked';
    const isVerifiable = isVerifiableStatus(doc.status);
    const certMeta = doc.certification_metadata || {};
    const meta = doc.metadata || {};

    const certification = buildCertification(doc)
      ?? doc._siblingCertification
      ?? siblingCertification(rows, doc, await resolveTrustedCertificationEvidence(rows, { db }));
    // KS-563: `isCertified` stays the narrow claim — an issuer certified these
    // bytes — now read from the registration set's evidence (KS-584), not just
    // the selected row's status.
    const isCertified = isCertifiedStatus(doc.status) || Boolean(certification);

    // KS-522: honest labelling — simulated anchors make no on-chain claim.
    const preHealBlob = chainBlobOfRow(doc);
    const healedBlob = await healVerifyRow(doc, preHealBlob, (req.headers.authorization as string) || '');
    const fileVerifyChain = presentBlockchainHonestly(healedBlob ?? certMeta.blockchain);
    const scoped = isCrossTenantResponse(req, doc);
    res.json(scopeTenantFields({
      verified: isVerifiable && !isRevoked,
      fileHash,
      fileSize: fileBuffer.length,
      documentId: doc.external_id || doc.id,
      title: doc.title,
      documentType: doc.document_type,
      status: doc.status,
      certifiedAt: (certification as Record<string, unknown> | undefined)?.certifiedAt || doc.certified_at || doc.created_at,
      issuer: certMeta.issuerName || certMeta.certificationData?.issuedBy || meta.issuedBy || meta.certifiedBy || meta.issuerName || doc.organization_name || null,
      blockchain: fileVerifyChain,
      ...(fileVerifyChain && (fileVerifyChain as Record<string, unknown>).simulated === true ? { simulated: true } : {}),
      ...(certification ? { certification } : {}),
      checks: {
        documentExists: true,
        hashValid: true,
        isCertified,
        isAnchored: isAnchoredHonestly(fileVerifyChain, doc.status),
        isRevoked,
        integrityVerified: isVerifiable && !isRevoked,
      },
      verifiedAt: new Date().toISOString(),
    }, scoped));
  } catch (error) {
    logger.error('File verification error', { error: error instanceof Error ? error.message : String(error) });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'File verification failed' } });
  }
});

/**
 * POST /api/verification/verify
 * Verify by hash or documentId (JSON body).
 * For strongest verification, use /verify-file with the actual document.
 */
verificationRouter.post(
  '/verify',
  [
    // KS-222: validate every field in the VerifyRequest spec schema
    // (documentId, hash, title, contentHash — all strings) plus the extra hash
    // aliases this handler also reads (providedHash, documentHash) and
    // documentData, so a non-string (e.g. {}) is rejected with 400 rather than
    // slipping through to a lookup miss that returns 200.
    body('documentId').optional().isString(),
    body('hash').optional().isString(),
    body('title').optional().isString(),
    body('contentHash').optional().isString(),
    body('providedHash').optional().isString(),
    body('documentHash').optional().isString(),
    body('documentData').optional().isObject(),
  ],
  async (req: Request, res: Response) => {
    try {
      // KS-222: enforce the declared body validators. Previously no
      // validationResult check existed, so the rules above were dormant and a
      // wrong-type hash reached the lookup and returned 200 instead of a 400.
      const validationErrors = validationResult(req);
      if (!validationErrors.isEmpty()) {
        return res.status(400).json({
          verified: false,
          // KS-1103: the message names every field the chain above checks. It used to
          // name only documentId, providedHash, contentHash and documentHash, so a
          // caller refused for a non-string `hash` or `title` was told about fields it
          // had not sent.
          error: 'Invalid request body: documentId, hash, title, contentHash, providedHash and documentHash must be strings; documentData must be an object.',
        });
      }

      // Verification is a public endpoint — auth is optional
      // (used for audit logging if available, but not required)

      // KS-1103: read the published `hash` field. KS-222 added it to the validator
      // chain, but the handler never destructured it, so a spec-valid body carrying
      // only `hash` fell through to the 400 below while the same value as
      // `contentHash` answered 200.
      const { documentId, providedHash, documentData, contentHash, documentHash, hash, title } = req.body;
      const db = (req as any).db || prisma;

      // Resolve the hash to verify against — accept multiple field names
      // KS-1103: `hash` is read LAST, so every body carrying a pre-existing alias keeps
      // its lookup value — when an alias and `hash` are both present the lookup still
      // sees the alias. Before this change the chain stopped at documentHash.
      // KS-1118 F-3: NOT "every body that worked before keeps its answer", which is what
      // this said and is wrong. A body pairing `hash` with `documentId` or `documentData`
      // now takes the hash strategy where it used to take the id / data one, as v2
      // already does. documentId-only, documentData-only and alias-only bodies are
      // unchanged. No caller in the repo sends that pairing (measured: 73-file census).
      const hashToVerify = providedHash || contentHash || documentHash || hash;

      // KS-1114: the title strategy. Kam's ruling, verbatim: "Title lookup open to anyone, one
      // tenant". An empty or whitespace-only title is treated as ABSENT, so `''` cannot match a
      // row and a body carrying only `{title: ''}` keeps today's 400. A present title is matched
      // EXACTLY as sent (case and surrounding spaces included).
      const titleToFind: string | undefined =
        typeof title === 'string' && title.trim().length > 0 ? title : undefined;

      if (!documentId && !hashToVerify && !documentData && !titleToFind) {
        return res.status(400).json({
          verified: false,
          // KS-1103: name every field this handler accepts. The previous text said
          // "a content hash (from the document file) or a documentId", which was also
          // what a caller saw after sending the published `hash` field.
          // KS-1114: `title` is now one of them.
          error: 'Please provide a documentId, a content hash (hash, contentHash, providedHash or documentHash), documentData, or a title.',
        });
      }

      // If documentData (raw content) is provided, hash it first
      let computedHash = hashToVerify;
      if (documentData && !computedHash) {
        computedHash = generateHash(documentData);
      }

      // =================================================================
      // HASH-FIRST VERIFICATION (security model)
      // =================================================================
      // The hash IS the integrity proof. We look up by hash to confirm
      // this exact file content was certified. Looking up by ID alone
      // cannot prove integrity — a bad actor could swap the file.
      // =================================================================

      /**
       * KS-70: best-effort lineage walk from a resolved document row.
       *
       * Walks `parent_document_id` up to MAX_LINEAGE_DEPTH and returns
       * the chain (newest first) plus a `truncated` flag. The walk is
       * tenant-scoped to the doc's own tenant — cross-tenant walks
       * would expose lineage information across the isolation
       * boundary, so we stop at the first cross-tenant parent.
       *
       * Public verify is unauthenticated; if the walk fails (FK miss,
       * DB hiccup, parent_document_id column not yet in this env)
       * we return an empty lineage rather than fail the whole verify.
       */
      const walkLineageForDoc = async (
        doc: { external_id?: string; id?: string; tenant_id?: string },
      ): Promise<{ lineage: LineageEntry[]; truncated: boolean }> => {
        const externalId = doc.external_id || doc.id;
        if (!externalId || !doc.tenant_id) {
          return { lineage: [], truncated: false };
        }
        try {
          return await walkDocumentAncestors(externalId, doc.tenant_id, { db });
        } catch (err: any) {
          logger.warn('KS-70 lineage walk failed; returning empty lineage', {
            externalId,
            error: err instanceof Error ? err.message : String(err),
          });
          return { lineage: [], truncated: false };
        }
      };

      // KS-280: statuses that count as "certified" for the forward-lineage
      // flag — mirrors `isCertified` in buildResponse below.
      // KS-563: narrowed with it. `hasNewerCertifiedVersion` drives a
      // "superseded by a newer CERTIFIED version" warning, so a merely-anchored
      // descendant must not raise it — that was the same false claim.
      const CERTIFIED_STATUSES = new Set([CERTIFIED_STATUS]);

      /**
       * KS-280: forward (descendant) lineage. Given a resolved doc, find any
       * newer/derived versions and whether any of them is certified, so the
       * verifier can flag "this version has been superseded by a newer
       * certified version" (e.g. will v1 once v2 is certified). Best-effort
       * like walkLineageForDoc — never fails the verify.
       */
      const walkNewerVersionsForDoc = async (
        doc: { external_id?: string; id?: string; tenant_id?: string },
      ): Promise<{ newerVersions: LineageEntry[]; truncated: boolean; hasNewerCertifiedVersion: boolean }> => {
        const externalId = doc.external_id || doc.id;
        if (!externalId || !doc.tenant_id) {
          return { newerVersions: [], truncated: false, hasNewerCertifiedVersion: false };
        }
        try {
          const { descendants, truncated } = await walkDocumentDescendants(externalId, doc.tenant_id, { db });
          return {
            newerVersions: descendants,
            truncated,
            hasNewerCertifiedVersion: descendants.some((d) => CERTIFIED_STATUSES.has(d.status)),
          };
        } catch (err: any) {
          logger.warn('KS-280 forward-lineage walk failed; returning none', {
            externalId,
            error: err instanceof Error ? err.message : String(err),
          });
          return { newerVersions: [], truncated: false, hasNewerCertifiedVersion: false };
        }
      };

      // Helper: build verification response from a document row.
      // KS-584 (interim): `extras` carries what the selected row alone cannot
      // know — certification evidence from a same-hash sibling, and a chain
      // blob whose stale 'pending' state was confirmed against the chain index.
      const buildResponse = (doc: any, hashMatch: boolean, extras?: { siblingCert?: Record<string, unknown>; healedChain?: Record<string, unknown> | null }) => {
        const isRevoked = doc.status === 'revoked';
        const isVerifiable = isVerifiableStatus(doc.status);
        const certMeta = doc.certification_metadata || {};
        const meta = doc.metadata || {};
        // Resolve issuer name from all possible sources
        const issuerName = certMeta.issuerName || certMeta.certificationData?.issuedBy || meta.issuedBy || meta.certifiedBy || meta.issuerName || doc.issuer_name || doc.organization_name || null;
        // KS-522: honest labelling — a simulated anchor never presents an
        // on-chain claim (see presentBlockchainHonestly above).
        const chain = presentBlockchainHonestly(extras?.healedChain ?? certMeta.blockchain);
        const certification = buildCertification(doc) ?? doc._siblingCertification ?? extras?.siblingCert;
        // KS-563: narrow claim — an issuer certified these bytes; KS-584 reads
        // the evidence from the registration set, not only the selected row.
        const isCertified = isCertifiedStatus(doc.status) || Boolean(certification);
        return {
          verified: hashMatch && isVerifiable && !isRevoked,
          documentId: doc.external_id || doc.id,
          title: doc.title,
          documentType: doc.document_type,
          status: doc.status,
          contentHash: doc.content_hash,
          certifiedAt: (certification as Record<string, unknown> | undefined)?.certifiedAt || doc.certified_at || doc.created_at,
          issuer: issuerName,
          blockchain: chain,
          // KS-522: top-level machine-readable marker so a relying party
          // cannot mistake a simulated anchor for on-chain proof.
          ...(chain && (chain as Record<string, unknown>).simulated === true ? { simulated: true } : {}),
          // KS-563: present ONLY when an issuer actually certified — its
          // absence is the honest signal that no certification happened.
          ...(certification ? { certification } : {}),
          checks: {
            documentExists: true,
            hashValid: hashMatch,
            isCertified,
            isAnchored: isAnchoredHonestly(chain, doc.status),
            isRevoked,
            integrityVerified: hashMatch && isVerifiable && !isRevoked,
          },
          verifiedAt: new Date().toISOString(),
        };
      };

      // Normalise hash for comparison (strip or add sha256: prefix)
      const normaliseHash = (h: string) => h.replace(/^sha256:/, '');

      /**
       * The by-id answer: strategy 2 (by documentId). It does not prove integrity, so `verified` is
       * false and `hashValid` / `integrityVerified` are false — never an integrity claim on an id match.
       * Hoisted from strategy 2 VERBATIM (only the warning became a parameter); KS-1114's
       * byte-identity cell T9 pins the documentId answer against develop's.
       * KS-1114 round 2: the title strategy deliberately does NOT use this. This answer carries the
       * contentHash, issuer, certification and lineage, and on a title match that turned a guessed
       * title into a full `verified:true` answer through `{hash}` (gate F1, 2026-10-15).
       */
      const respondExistenceOnly = async (doc: any, warning: string) => {
        // KS-563: narrow certification claim (this strategy never proves
        // integrity anyway — `verified` is hardcoded false below).
        const isCertified = isCertifiedStatus(doc.status);
        const isRevoked = doc.status === 'revoked';
        const certMeta = doc.certification_metadata || {};
        const meta = doc.metadata || {};
        // KS-584 (interim): by-id answers cross the tenant boundary via
        // crossTenantLookup too — scope tenant-owned fields and skip the
        // lineage walks for scoped responses.
        const byIdScoped = isCrossTenantResponse(req, doc);
        // KS-70: surface lineage even on the by-ID strategy. Same
        // re-fetch pattern as strategy-1 — the cross-tenant lookup
        // doesn't always return tenant_id directly.
        let lineagePayload: { lineage: LineageEntry[]; truncated: boolean } = {
          lineage: [],
          truncated: false,
        };
        let fwdPayload: { newerVersions: LineageEntry[]; truncated: boolean; hasNewerCertifiedVersion: boolean } = {
          newerVersions: [],
          truncated: false,
          hasNewerCertifiedVersion: false,
        };
        try {
          if (!byIdScoped) {
            const tenantLookup: any[] = await db.$queryRaw`
              SELECT external_id, tenant_id FROM documents
               WHERE id = ${doc.id}::uuid LIMIT 1
            `;
            if (tenantLookup.length > 0) {
              lineagePayload = await walkLineageForDoc(tenantLookup[0]);
              fwdPayload = await walkNewerVersionsForDoc(tenantLookup[0]);
            }
          }
        } catch (lineageErr: any) {
          logger.warn('KS-70 verify (by-id) lineage attach failed', {
            error: lineageErr instanceof Error ? lineageErr.message : String(lineageErr),
          });
        }
        return res.json(scopeTenantFields({
          verified: false,
          warning,
          documentId: doc.external_id || doc.id,
          title: doc.title,
          status: doc.status,
          contentHash: doc.content_hash,
          issuer: certMeta.issuerName || certMeta.certificationData?.issuedBy || meta.issuedBy || meta.certifiedBy || meta.issuerName || doc.organization_name || null,
          ...(buildCertification(doc) ? { certification: buildCertification(doc) } : {}),
          checks: {
            documentExists: true,
            hashValid: false,
            isCertified,
            isAnchored: isAnchoredHonestly(presentBlockchainHonestly(certMeta.blockchain), doc.status),
            isRevoked,
            integrityVerified: false,
          },
          ...(lineagePayload.lineage.length > 0
            ? {
                lineage: lineagePayload.lineage,
                lineageTruncated: lineagePayload.truncated,
                lineageDepthAtTruncation: lineagePayload.truncated ? MAX_LINEAGE_DEPTH : undefined,
              }
            : {}),
          ...(fwdPayload.newerVersions.length > 0
            ? {
                newerVersions: fwdPayload.newerVersions,
                newerVersionsTruncated: fwdPayload.truncated,
                hasNewerCertifiedVersion: fwdPayload.hasNewerCertifiedVersion,
              }
            : {}),
          verifiedAt: new Date().toISOString(),
        }, byIdScoped));
      };

      try {
        // STRATEGY 1: Look up by hash (strongest verification — proves file integrity)
        if (computedHash) {
          const hashNorm = normaliseHash(computedHash);

          // Local tenant DB first (KS-252) — same-env documents answer in
          // milliseconds and their local status is authoritative anyway
          // (F-DEMO-VERIFY-01: local draft/revoked overrides chain presence).
          // KS-584 (interim): fetch the same-hash SET (bounded); selection
          // happens in selectVerifiableRow, not in an arbitrary LIMIT 1.
          let rows: any[] = await db.$queryRaw`
            SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
                   d.certification_metadata, d.metadata, d.created_at, d.certified_at,
                   d.tenant_id, d.parent_document_id, d.owner_user_id, o.name AS organization_name
            FROM documents d
            LEFT JOIN organizations o ON d.issuer_organization_id = o.id
            WHERE d.content_hash = ${computedHash}
               OR d.content_hash = ${hashNorm}
               OR d.content_hash = ${'sha256:' + hashNorm}
            ORDER BY d.certified_at DESC NULLS LAST
            LIMIT ${VERIFY_ROWSET_LIMIT}
          `;

          // If not found locally, search cross-tenant via platform registry
          if (rows.length === 0) {
            const crossDoc = await crossTenantLookup(documentId || '', computedHash);
            if (crossDoc) {
              rows = [crossDoc];
              logger.info('Hash found via cross-tenant lookup', { hash: hashNorm.substring(0, 16) });
            }
          }

          if (rows.length === 0) {
            // CHAIN FALLBACK for cross-env certs: the chain is shared, so any
            // environment can verify a cert issued by any other environment even
            // though that cert is absent from our tenant registry.
            //
            // KS-252 (2026-06-10): this used to run BEFORE the local DB, but the
            // anchoring chain scan costs seconds for any hash not anchored yet —
            // the common case when a verify races a fresh anchor — and stalled
            // 39% of verifies to client timeout under the KS-194 load baseline.
            // Local + registry hits don't need the chain: F-DEMO-VERIFY-01
            // (2026-04-29) established that the local status (draft/revoked)
            // OVERRIDES chain presence, so for any locally-known document the
            // local answer is both faster and more precise. Only a full miss
            // falls through to the chain scan (preserving the cross-env
            // guarantee in CREDENTIALS-AND-PORTALS §8). The inner local-doc
            // downgrade check stays as belt-and-braces for docs created
            // between the lookups.
            try {
              // F-CHAIN-VERIFY-AUTH-01 (2026-05-02): the anchoring service
              // mounts authenticate() on /api/* (T1-A trust-header migration).
              // Calling /api/anchors/verify without the caller's bearer token
              // returned 500 "No token provided", silently breaking chain-
              // first lookup — and therefore breaking the cross-env shared-
              // chain verify guarantee documented in CREDENTIALS-AND-PORTALS
              // §8. Forwarding Authorization here is the same pattern used
              // by services/api-gateway/src/routes/platform.ts after the
              // BUG-PLATFORM-AUTH-001 fix.
              const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
              const callerAuth = (req.headers.authorization as string) || '';
              const resp = await fetch(`${anchoringBase}/api/anchors/verify/${encodeURIComponent(hashNorm)}`, {
                headers: callerAuth ? { Authorization: callerAuth } : {},
                signal: AbortSignal.timeout(CHAIN_VERIFY_TIMEOUT_MS), // KS-252
              });
              if (resp.ok) {
                const chain: any = await resp.json();
                if (chain?.verified === true) {
                  // F-DEMO-VERIFY-01: check the local tenant DB for a doc with
                  // this hash. If found and status is draft/deleted/revoked,
                  // downgrade — the chain's confirmation is about a different
                  // (prior) document that happened to share the same content.
                  let localDoc: any = null;
                  try {
                    // KS-584 (interim): the downgrade decision must be made on
                    // the row selection would pick — a draft sibling of an
                    // anchored/certified row must not downgrade the verify.
                    const localRows = await db.$queryRaw`
                      SELECT external_id, id, status, title, document_type,
                             certification_metadata, metadata, created_at, certified_at
                      FROM documents
                      WHERE content_hash = ${computedHash}
                         OR content_hash = ${hashNorm}
                         OR content_hash = ${'sha256:' + hashNorm}
                      ORDER BY certified_at DESC NULLS LAST
                      LIMIT ${VERIFY_ROWSET_LIMIT}
                    ` as any[];
                    if (localRows.length > 0) localDoc = selectVerifiableRow(localRows);
                  } catch (lookupErr: any) {
                    logger.warn('Local-doc draft check in chain-first path failed', { error: lookupErr?.message });
                  }

                  if (localDoc) {
                    const status = localDoc.status;
                    // KS-563: the gate below is "is this document presentable
                    // as verified", which is the BROAD set — narrowing it here
                    // would 'draft'-reject every anchored document. Only the
                    // reported `checks.isCertified` narrows.
                    const isCertified = isCertifiedStatus(status);
                    const isVerifiable = isVerifiableStatus(status);
                    const isRevoked = status === 'revoked';
                    if (!isVerifiable || isRevoked) {
                      return res.json({
                        verified: false,
                        documentId: localDoc.external_id || localDoc.id,
                        title: localDoc.title,
                        documentType: localDoc.document_type,
                        status,
                        contentHash: computedHash,
                        error: isRevoked
                          ? 'This document was anchored on chain but has since been revoked.'
                          : 'The content hash was anchored on chain previously, but this document is still in draft and has not been certified by the issuer.',
                        chain: {
                          anchored: true,
                          network: chain.network,
                          txHash: chain.txHash,
                          note: 'A different document with the same content was anchored at this txHash; this is not it.',
                        },
                        checks: {
                          documentExists: true,
                          hashValid: true,
                          isCertified,
                          isAnchored: true,
                          isRevoked,
                          integrityVerified: false,
                        },
                        verifiedAt: new Date().toISOString(),
                      });
                    }
                  }

                  logger.info('Hash verified via chain-first lookup', { hash: hashNorm.substring(0, 16), source: chain.source });
                  // KS-522: legacy mock rows can surface via the chain
                  // index — never present a fabricated hash as on-chain.
                  const honestChain = presentBlockchainHonestly({
                    anchored: true,
                    network: chain.network,
                    txHash: chain.txHash,
                    blockHeight: chain.blockNumber,
                    cardanoScanUrl: chain.cardanoScanUrl,
                    confirmedAt: chain.confirmedAt,
                    simulated: chain.simulated,
                  });
                  // KS-563: chain evidence proves the hash was anchored, not
                  // that anyone certified it — claim only what was performed.
                  const chainCertId = chain.metadata?.certId || chain.metadata?.certificationId || null;
                  const chainIsCertified = Boolean(chainCertId);
                  return res.json({
                    verified: true,
                    source: chain.source === 'chain' ? 'blockchain' : 'blockchain-indexed',
                    documentId: chain.metadata?.documentId || chain.metadata?.certId,
                    title: null,
                    documentType: chain.metadata?.documentType || null,
                    status: 'anchored',
                    contentHash: chain.metadata?.contentHash || computedHash,
                    certifiedAt: chain.confirmedAt,
                    issuer: chain.metadata?.issuerName || chain.metadata?.issuerOrgId || null,
                    blockchain: honestChain,
                    ...(chainIsCertified
                      ? {
                          certification: {
                            certificationId: chainCertId,
                            certificationType: chain.metadata?.certificationType ?? null,
                            certifiedAt: chain.confirmedAt ?? null,
                            certifiedBy: chain.metadata?.issuerName ?? null,
                            certifierOrganizationId: chain.metadata?.issuerOrgId ?? null,
                          },
                        }
                      : {}),
                    onChainMetadata: chain.metadata,
                    checks: {
                      documentExists: true,
                      hashValid: true,
                      isCertified: chainIsCertified,
                      isAnchored: isAnchoredHonestly(honestChain, 'anchored'),
                      isRevoked: false,
                      integrityVerified: true,
                    },
                    verifiedAt: new Date().toISOString(),
                  });
                }
              }
            } catch (chainErr: any) {
              logger.warn('Chain-first /verify lookup failed — falling back to DB', { error: chainErr?.message });
            }
          }

          if (rows.length > 0) {
            // KS-70: best-effort lineage attachment. The strategy-1 SELECTs
            // above may not include tenant_id (cross-tenant lookups in
            // particular). Re-fetch the minimal {external_id, tenant_id,
            // parent_document_id} so the walk has the right scope.
            // KS-584 (interim): select the evidencing row; carry sibling
            // certification; confirm stale 'pending' chain state; scope
            // tenant-owned fields out of cross-tenant answers (and skip the
            // lineage walks for them — they enumerate tenant-owned chains).
            const docRow = selectVerifiableRow(rows);
            const preHeal = chainBlobOfRow(docRow);
            const healedChain = await healVerifyRow(docRow, preHeal, (req.headers.authorization as string) || '');
            const scoped = isCrossTenantResponse(req, docRow);
            // KS-1557: resolve the derived rows' evidence only when it can be used (no certified row, no carried evidence).
            const siblingCert = buildCertification(docRow) || docRow._siblingCertification
              ? undefined
              : siblingCertification(rows, docRow, await resolveTrustedCertificationEvidence(rows, { db }));
            // KS-1119: the hash flag is computed from the selected row, never assumed. Every row that reaches this line
            // was found by its hash (bare, `sha256:` or prefixed input), so it is true for those; it stops being an
            // assumption a future lookup could break without anything noticing.
            const hashMatch = typeof docRow.content_hash === 'string' && normaliseHash(docRow.content_hash) === hashNorm;
            const base = scopeTenantFields(
              buildResponse(docRow, hashMatch, { siblingCert, healedChain }),
              scoped,
            );
            if (scoped) return res.json(base);
            try {
              // KS-299: a certification can be stored as a separate documents
              // row that shares the content_hash with its source document but
              // has a NULL external_id and no parent_document_id — the
              // `certified_at DESC` resolve above picks that cert row, so the
              // ancestor walk (which keys on external_id) returns empty. Re-
              // resolve the lineage from the external_id-bearing document row
              // for this hash, preferring the resolved row itself, so verify
              // shows the document's provenance rather than an empty lineage.
              // The verify response above is unchanged — only the lineage walk
              // is re-scoped to a row that actually has a chain to follow.
              const lineageHash = (docRow.content_hash || '').replace(/^sha256:/, '');
              const tenantLookup: any[] = await db.$queryRaw`
                SELECT external_id, tenant_id FROM documents
                 WHERE external_id IS NOT NULL AND tenant_id IS NOT NULL
                   AND (id = ${docRow.id}::uuid
                        OR content_hash = ${lineageHash}
                        OR content_hash = ${'sha256:' + lineageHash})
                 ORDER BY (id = ${docRow.id}::uuid) DESC, certified_at DESC NULLS LAST, created_at DESC
                 LIMIT 1
              `;
              if (tenantLookup.length > 0) {
                const { lineage, truncated } = await walkLineageForDoc(tenantLookup[0]);
                const fwd = await walkNewerVersionsForDoc(tenantLookup[0]);
                if (lineage.length > 0 || fwd.newerVersions.length > 0) {
                  return res.json({
                    ...base,
                    ...(lineage.length > 0
                      ? { lineage, lineageTruncated: truncated, lineageDepthAtTruncation: truncated ? MAX_LINEAGE_DEPTH : undefined }
                      : {}),
                    ...(fwd.newerVersions.length > 0
                      ? { newerVersions: fwd.newerVersions, newerVersionsTruncated: fwd.truncated, hasNewerCertifiedVersion: fwd.hasNewerCertifiedVersion }
                      : {}),
                  });
                }
              }
            } catch (lineageErr: any) {
              logger.warn('KS-70 verify lineage attach failed', {
                error: lineageErr instanceof Error ? lineageErr.message : String(lineageErr),
              });
            }
            return res.json(base);
          }

          // Hash not found anywhere — this file was never certified
          return res.json({
            verified: false,
            error: 'This document hash is not registered. The file may have been modified or was never certified.',
            providedHash: computedHash,
            checks: { documentExists: false, hashValid: false, integrityVerified: false },
          });
        }

        // STRATEGY 2: Look up by document ID only (weaker — confirms existence but not integrity)
        if (documentId) {
          let rows: any[] = await db.$queryRaw`
            SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
                   d.certification_metadata, d.metadata, d.created_at, d.certified_at,
                   o.name AS organization_name
            FROM documents d
            LEFT JOIN organizations o ON d.issuer_organization_id = o.id
            WHERE d.external_id = ${documentId} LIMIT 1
          `;
          if (rows.length === 0) {
            try {
              rows = await db.$queryRaw`
                SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
                       d.certification_metadata, d.metadata, d.created_at, d.certified_at,
                       o.name AS organization_name
                FROM documents d
                LEFT JOIN organizations o ON d.issuer_organization_id = o.id
                WHERE d.id = ${documentId}::uuid LIMIT 1
              `;
            } catch { /* not UUID */ }
          }
          if (rows.length === 0) {
            const crossDoc = await crossTenantLookup(documentId);
            if (crossDoc) rows = [crossDoc];
          }

          if (rows.length > 0) {
            return respondExistenceOnly(
              rows[0],
              'Document found by ID but no hash was provided. To verify integrity, provide the document file or its SHA-256 hash.',
            );
          }

          return res.json({
            verified: false,
            documentId,
            error: 'Document not found in the registry',
            checks: { documentExists: false, hashValid: false, integrityVerified: false },
          });
        }

        // STRATEGY 3 (KS-1114): look up by TITLE — weakest, confirms existence only.
        // Kam's ruling, verbatim: "Title lookup open to anyone, one tenant". Reached only by a
        // body carrying a title and NOTHING else the strategies above read, so every body that
        // answered before answers byte-identically now.
        //
        // ⚠ AN EXISTENCE ORACLE, BY KAM'S RULING. A hash needs the bytes; a title is a guess.
        // This route is unauthenticated and public, and an anonymous caller can now learn
        // whether a document of a given title exists in the default tenant. The pen-test
        // enumeration finding's mitigation is the per-IP limit on this route
        // (api-gateway/src/index.ts, the `/api/verification/verify` limiter). Recorded here so
        // nobody has to rediscover it.
        //
        // "ONE TENANT", by construction rather than by RLS: the caller's tenant is bound in the
        // SQL, and there is NO cross-tenant fallback — crossTenantLookup is deliberately not
        // called. `documents` is FORCE RLS, so the predicate is the second line, not the only one.
        // The caller's tenant is callerTenantOf(req): an anonymous caller resolves in the default
        // tenant, and a caller's own tenant applies only when the gateway VOUCHED the request's
        // x-tenant-id (KS-1032). Compared as text so a malformed tenant value cannot throw a cast.
        //
        // THE REPLY IS EXISTENCE ONLY (KS-1114 round 2). Kam, card
        // secuura-ks1114-title-reply-leaks-details-fix-now-or-wait-1015 = a, its detail verbatim:
        // "#1555 stays held, unmerged. The J seat fixes it after the reset: an existence-only reply,
        // drafts and revoked kept out, then round 2 of its gate." His 10-13 card (b) also binds: the
        // lookup is open "even if the reply hides the details". Round 1 answered a title hit with the
        // whole by-id body (contentHash, issuer, lineage, newerVersions...), so a guessed title gave a
        // hash and the hash gave `verified:true` (gate F1). Now:
        //   * a HIT answers exactly { verified: false, checks: { documentExists: true } } and nothing
        //     else — no id, hash, issuer, status, certification or lineage. Shape ruled by Wednesday,
        //     2026-10-18T08:31:18Z: `verified` stays because VerifyResponseSchema REQUIRES it (it is the
        //     route's discriminator), `documentExists` sits at the declared `checks` path where the
        //     miss carries it, and nothing else, so a hit and a miss differ only in that bit and the
        //     miss's `error`. Because no row's identity is returned, which row matched is irrelevant:
        //     the query asks only whether one exists.
        //   * DRAFT and REVOKED documents are never matched — in the WHERE, not on the newest row
        //     afterwards, so a newer draft cannot shadow an older published document. A draft or a
        //     revoked match answers the ordinary not-found, and so does a deleted or an expired one (KS-1114
        //     follow-up: the status is lower-cased and trimmed before it is compared). Every other status can be a hit.
        //   * the GDPR erasure sentinel never matches (Wednesday, 2026-10-13T10:52:44Z). Every erased
        //     document's title holds ERASED_MARKER (the column is NOT NULL), so a naive lookup would
        //     make an erased document discoverable through the very field that was erased.
        // Absent, another tenant's, draft, revoked, deleted, expired and the sentinel all answer ONE not-found body.
        if (titleToFind && !documentId && !computedHash) {
          // The title is deliberately NOT echoed: echoing it would make the sentinel's not-found
          // differ from a missing title's by exactly that field, and Wednesday's ruling requires the
          // two bodies to be byte-identical so the answer reveals nothing about erasure.
          const titleNotFound = () => res.json({
            verified: false,
            error: 'Document not found in the registry',
            checks: { documentExists: false, hashValid: false, integrityVerified: false },
          });
          const tenantForTitle = callerTenantOf(req);
          // callerTenantOf always yields a tenant today (resolveRequestTenantId falls back to the
          // default; gate F5 measured this guard unreachable). Kept so a missing tenant answers the
          // not-found without running the query at all.
          if (!tenantForTitle || titleToFind === ERASED_MARKER) return titleNotFound();
          // documents.status is NOT NULL (migration 001), so NOT IN cannot silently drop a NULL row.
          const titleRows: any[] = await db.$queryRaw`
            SELECT 1 AS found
            FROM documents d
            WHERE d.title = ${titleToFind}
              AND d.title <> ${ERASED_MARKER}
              AND d.tenant_id::text = ${tenantForTitle}
              AND lower(btrim(d.status)) NOT IN ('draft', 'revoked', 'deleted', 'expired')
            LIMIT 1
          `;
          if (titleRows.length === 0) return titleNotFound();
          return res.json({ verified: false, checks: { documentExists: true } });
        }
      } catch (dbErr: any) {
        logger.warn('Verification lookup failed', { documentId, error: dbErr?.message });
        return res.json({ verified: false, error: 'Verification lookup failed' });
      }

      res.json({ verified: false, error: 'No verifiable input provided' });
    } catch (error) {
      logger.error('Verification error', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Verification failed' } });
    }
  }
);

/**
 * POST /api/verification/hash
 * Generate hash for document data
 */
verificationRouter.post(
  '/hash',
  [body('data').notEmpty().withMessage('Data is required')],
  async (req: Request, res: Response) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const { data } = req.body;
      const hash = generateHash(data);

      res.json({
        hash,
        algorithm: 'sha256',
        generatedAt: new Date().toISOString(),
      });
    } catch (error) {
      logger.error('Hash generation error', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Hash generation failed' } });
    }
  }
);

/**
 * GET /api/verification/status/:documentId
 * Check verification status of a document
 */
verificationRouter.get(
  '/status/:documentId',
  async (req: Request, res: Response) => {
    try {
      const { documentId } = req.params;

      res.json({
        documentId,
        status: 'unknown',
        message: 'Use POST /api/verification/verify with documentId or contentHash for full verification.',
      });
    } catch (error) {
      logger.error('Status check error', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Status check failed' } });
    }
  }
);

export default verificationRouter;
