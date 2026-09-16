/**
 * =============================================================================
 * VERIFICATION ROUTES — /api/v2 (KS-584 P3: the verify-list contract)
 * =============================================================================
 * v1 verify-by-hash collapses the same-hash registration SET to one row —
 * the interim fix (KS-584, #662) made that collapse deterministic and honest,
 * but a single-row answer still cannot represent what the platform actually
 * holds: the certify flow legitimately creates multiple registrations for the
 * same bytes (original + signed_document), and templates/forms are registered
 * by many parties. v2 dissolves the selection problem instead of refining it:
 * every same-hash registration is returned as its own match, each presented
 * through the SAME honesty rules v1 applies to its selected row (KS-522
 * simulated-anchor labelling, KS-563 narrow certification claim, KS-584
 * tenant-field scoping).
 *
 * Contract (docs/design/2026-08-11_p3-verify-list-design.md):
 *   POST /api/v2/verification/verify        {hash|contentHash|documentId|documentData}
 *   POST /api/v2/verification/verify-file   raw file bytes as body
 *   → 200 { hash, count, matches: [...], verifiedAt }
 *
 * Anchor truth is CALLER-INDEPENDENT (QA finding, 2026-08-11): the anchoring
 * chain-fact read is pre-auth (leg 1), and this module never forwards the
 * caller's bearer — an anonymous caller and an authenticated one get byte-
 * identical anchor facts. Auth posture (Kam ruling: anonymous verify is a
 * supported public path): ABSENT token → anonymous 200; PRESENT-but-invalid
 * token → 401 via authenticate({required:false}) so a misconfigured client
 * learns to re-auth instead of silently degrading to anonymous.
 *
 * v1 (/api/verification/*) is UNTOUCHED — versioned coordinated cutover;
 * the cutover word is Kam's alone.
 */

import { Router, Request, Response } from 'express';
import { body, validationResult } from 'express-validator';
import crypto from 'crypto';
import { logger } from '../utils/logger';
import { prisma, getTenantManager } from '../db';
// KS-458: cross-tenant registry lookups run under the RESOLVED tenant's GUC.
import { runWithTenantId, queryWithTenantGuc } from '@secuura/shared';
import { authenticate } from '../middleware/auth';
import {
  presentBlockchainHonestly,
  isCertifiedStatus,
  isVerifiableStatus,
  isAnchoredHonestly,
  buildCertification,
  chainBlobOfRow,
  rowHasRealTx,
  rowCreatedMs,
  isCrossTenantResponse,
  scopeTenantFields,
  persistHealedAnchor,
  generateHash,
  REAL_TXHASH_RE,
  VERIFY_ROWSET_LIMIT,
  CHAIN_VERIFY_TIMEOUT_MS,
} from './verification';

export const verificationV2Router = Router();

// PRESENT-but-invalid bearer → 401; ABSENT → anonymous pass-through. The
// design-doc lean, implemented by the existing middleware's optional mode.
verificationV2Router.use(authenticate({ required: false }));

// Cross-tenant enumeration ceiling: distinct tenants consulted per hash.
// Widely-shared bytes (a statutory form) could be registered by many tenants;
// the list stays bounded and deterministic (registry order) rather than open.
const V2_CROSS_TENANT_LIMIT = 8;

// Column list for the cross-tenant pg-pool queries (the Prisma tagged
// templates below inline the same list — keep them in step).
const SELECT_COLUMNS = `
  d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
  d.certification_metadata, d.metadata, d.created_at, d.certified_at,
  d.tenant_id, o.name AS organization_name`;

// Mirrors repositories/documentRepo.ts — the KS-596 dual-identifier rule:
// external_id is the S-supplied documentUuid when registration carried one;
// otherwise the pkey UUID serves (it is already a working lookup key).
function isValidUuid(s: unknown): boolean {
  return typeof s === 'string'
    && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(s);
}

const toIso = (v: unknown): string | null => {
  if (!v) return null;
  const d = v instanceof Date ? v : new Date(String(v));
  return Number.isNaN(d.getTime()) ? null : d.toISOString();
};

/**
 * One chain-fact read per request, CALLER-INDEPENDENT: no bearer is forwarded
 * (the anchoring endpoint is pre-auth since leg 1), so the answer cannot vary
 * with who asks. Non-2xx and transport errors are logged, never swallowed
 * silently (QA finding: the v1 heal used to fail closed in silence).
 */
async function fetchChainFact(hashNorm: string): Promise<Record<string, any> | null> {
  try {
    const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
    const resp = await fetch(`${anchoringBase}/api/anchors/verify/${encodeURIComponent(hashNorm)}`, {
      signal: AbortSignal.timeout(CHAIN_VERIFY_TIMEOUT_MS), // KS-252 ceiling
    });
    if (!resp.ok) {
      logger.warn('v2 verify: chain-fact read returned non-2xx; matches present stored state', { status: resp.status });
      return null;
    }
    const chain: any = await resp.json();
    return chain?.verified === true ? chain : null;
  } catch (err: any) {
    logger.warn('v2 verify: chain-fact read failed; matches present stored state', { error: err?.message });
    return null;
  }
}

/**
 * Row-level stale-anchor heal against the shared chain fact — the interim's
 * attribution rules (same tx, or the chain index attributes its confirmed
 * anchor to this very registration), applied per row instead of to one
 * selected row. Fail closed: no chain fact / no attribution → stored state.
 */
function healBlobWithChainFact(
  blob: Record<string, unknown> | null,
  row: any,
  chain: Record<string, any> | null,
): Record<string, unknown> | null {
  if (!blob || blob.simulated === true || !chain) return blob;
  const tx = typeof blob.txHash === 'string' ? blob.txHash : null;
  if (!tx || !REAL_TXHASH_RE.test(tx)) return blob;
  const settled = blob.anchored === true || blob.status === 'confirmed';
  const failed = blob.status === 'failed' || blob.status === 'anchor_failed';
  if (settled || failed) return blob;
  const chainTx = typeof chain.txHash === 'string' ? chain.txHash : null;
  if (!chainTx || !REAL_TXHASH_RE.test(chainTx)) return blob;
  const rowId = row?.external_id || row?.id;
  const sameTx = chainTx.toLowerCase() === tx.toLowerCase();
  const sameDoc = Boolean(rowId)
    && (chain.metadata?.documentId === rowId || chain.metadata?.certId === rowId);
  if (!sameTx && !sameDoc) return blob;
  return {
    ...blob,
    txHash: chainTx,
    status: 'confirmed',
    blockHeight: chain.blockNumber ?? blob.blockHeight ?? 0,
    ...(chain.network ? { network: chain.network } : {}),
    ...(chain.confirmedAt ? { confirmedAt: chain.confirmedAt } : {}),
    ...(chain.cardanoScanUrl ? { cardanoScanUrl: chain.cardanoScanUrl } : {}),
  };
}

/**
 * The certification act recorded ON THIS ROW by the lineage certify path —
 * a 'signed' derived row carrying certificationId in its metadata blob
 * (written only by POST /api/certifications/issue; the sign-cert version path
 * writes none). In the list contract each registration testifies for itself,
 * so there is no sibling smear: the consumer sees the certification-act row
 * as its own match.
 */
function ownRowCertification(row: any): Record<string, unknown> | undefined {
  const fromStatus = buildCertification(row);
  if (fromStatus) return fromStatus;
  const meta = (row?.metadata || {}) as Record<string, any>;
  if (row?.status !== 'signed' || !meta.certificationId) return undefined;
  const certifiedAt = meta.certifiedAt || row?.certified_at || row?.created_at || undefined;
  return {
    certificationId: meta.certificationId,
    certificationType: meta.certificationType ?? row?.document_type ?? null,
    certifiedAt: certifiedAt ? new Date(certifiedAt).toISOString() : null,
    certifiedBy: meta.issuerName ?? meta.issuedBy ?? row?.organization_name ?? null,
    certifierOrganizationId: meta.issuerId ?? null,
  };
}

/**
 * One registration → one match, through the same honesty rules as v1's
 * selected row: KS-522 simulated labelling, KS-563 narrow certification,
 * KS-584 tenant-field scoping (with an explicit `fieldsWithheld` marker so a
 * consumer can tell "withheld" from "absent").
 */
function buildMatch(
  req: Request,
  row: any,
  hashValid: boolean,
  chain: Record<string, any> | null,
): Record<string, unknown> {
  const isRevoked = row.status === 'revoked';
  const isVerifiable = isVerifiableStatus(row.status);
  const certMeta = (row.certification_metadata || {}) as Record<string, any>;
  const meta = (row.metadata || {}) as Record<string, any>;
  const preHeal = chainBlobOfRow(row);
  const healed = healBlobWithChainFact(preHeal, row, chain);
  persistHealedAnchor(row, preHeal, healed);
  const honest = presentBlockchainHonestly(healed ?? certMeta.blockchain) as Record<string, unknown> | null;
  const certification = ownRowCertification(row);
  const isCertified = isCertifiedStatus(row.status) || Boolean(certification);
  const issuerName = certMeta.issuerName || certMeta.certificationData?.issuedBy
    || meta.issuedBy || meta.certifiedBy || meta.issuerName || row.organization_name || null;
  const match: Record<string, unknown> = {
    documentId: row.external_id || row.id,
    documentUuid: isValidUuid(row.external_id) ? row.external_id : row.id,
    title: row.title ?? null,
    documentType: row.document_type ?? null,
    status: row.status,
    contentHash: row.content_hash,
    createdAt: toIso(row.created_at),
    certifiedAt: (certification?.certifiedAt as string | undefined) ?? toIso(row.certified_at),
    issuer: issuerName,
    blockchain: honest ?? null,
    ...(honest && honest.simulated === true ? { simulated: true } : {}),
    ...(certification ? { certification } : {}),
    checks: {
      documentExists: true,
      hashValid,
      isCertified,
      isAnchored: isAnchoredHonestly(honest, row.status),
      isRevoked,
      integrityVerified: hashValid && isVerifiable && !isRevoked,
    },
  };
  if (isCrossTenantResponse(req, row)) {
    return { ...scopeTenantFields(match, true), fieldsWithheld: true };
  }
  return match;
}

/**
 * A hash known ONLY to the chain index (cross-env cert, no registry row in
 * any reachable tenant) still gets an honest match — the v1 chain-first
 * fallback, in list shape. Claims only what the chain evidences (KS-563).
 */
function chainOnlyMatch(chain: Record<string, any>, contentHash: string): Record<string, unknown> {
  const honest = presentBlockchainHonestly({
    anchored: true,
    network: chain.network,
    txHash: chain.txHash,
    blockHeight: chain.blockNumber,
    cardanoScanUrl: chain.cardanoScanUrl,
    confirmedAt: chain.confirmedAt,
  }) as Record<string, unknown>;
  const certId = chain.metadata?.certId || chain.metadata?.certificationId || null;
  const docId = chain.metadata?.documentId || certId || null;
  return {
    documentId: docId,
    documentUuid: isValidUuid(docId) ? docId : null,
    source: chain.source === 'chain' ? 'blockchain' : 'blockchain-indexed',
    title: null,
    documentType: chain.metadata?.documentType || null,
    status: 'anchored',
    contentHash,
    createdAt: null,
    certifiedAt: chain.confirmedAt ?? null,
    issuer: chain.metadata?.issuerName || chain.metadata?.issuerOrgId || null,
    blockchain: honest,
    ...(honest && honest.simulated === true ? { simulated: true } : {}),
    ...(certId
      ? {
          certification: {
            certificationId: certId,
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
      isCertified: Boolean(certId),
      isAnchored: isAnchoredHonestly(honest, 'anchored'),
      isRevoked: false,
      integrityVerified: true,
    },
  };
}

/** Presentation order: certified (most recent act first) → real confirmed tx
 *  → real in-flight tx → the rest oldest-first. Deterministic, and mirrors the
 *  v1 interim's selection precedence so v2's matches[0] is v1's answer for
 *  every same-hash group (asserted by the parity sweep). */
function matchRank(row: any): number {
  if (isCertifiedStatus(row?.status)) return 0;
  if (rowHasRealTx(row)) return chainBlobOfRow(row)?.status === 'confirmed' ? 1 : 2;
  return 3;
}

// Millisecond-precise read of certified_at. Prisma hands back a Date, and
// Date.parse(String(date)) silently TRUNCATES to whole seconds (the default
// Date stringification carries no ms) — near-simultaneous certifications then
// tie and the wrong tiebreak wins. Caught live by the parity sweep on a
// 576-row group whose certified_at values differ by single milliseconds.
const rowCertifiedMs = (row: any): number => {
  const v = row?.certified_at;
  if (!v) return 0;
  const t = v instanceof Date ? v.getTime() : Date.parse(String(v));
  return Number.isFinite(t) ? t : 0;
};

function sortRowsForPresentation(rows: any[]): any[] {
  return [...rows].sort((a, b) => {
    const ra = matchRank(a);
    const rb = matchRank(b);
    if (ra !== rb) return ra - rb;
    if (ra === 0) {
      // Most recent certification first (v1's certified_at DESC pre-sort).
      const diff = rowCertifiedMs(b) - rowCertifiedMs(a);
      if (diff !== 0) return diff;
    }
    return rowCreatedMs(a) - rowCreatedMs(b);
  });
}

/** Same-hash rows from the caller's tenant DB (bounded). */
async function localRowsByHash(db: any, computedHash: string, hashNorm: string): Promise<any[]> {
  return await db.$queryRaw`
    SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
           d.certification_metadata, d.metadata, d.created_at, d.certified_at,
           d.tenant_id, o.name AS organization_name
    FROM documents d
    LEFT JOIN organizations o ON d.issuer_organization_id = o.id
    WHERE d.content_hash = ${computedHash}
       OR d.content_hash = ${hashNorm}
       OR d.content_hash = ${'sha256:' + hashNorm}
    ORDER BY d.certified_at DESC NULLS LAST
    LIMIT ${VERIFY_ROWSET_LIMIT}
  `;
}

/**
 * Same-hash rows from every OTHER tenant the platform registry knows about
 * (bounded). v1's crossTenantLookup stops at the FIRST registry row — one
 * tenant answers for everyone; here each registered tenant contributes its
 * rowset. Single-tenant deployments (demo, local) have no tenant manager and
 * skip this entirely.
 */
async function crossTenantRowsByHash(computedHash: string, hashNorm: string): Promise<any[]> {
  const mgr = getTenantManager();
  if (!mgr) return [];
  const out: any[] = [];
  try {
    const platformPool = mgr.getPlatformPool();
    const reg = await platformPool.query(
      `SELECT DISTINCT tenant_id, tenant_slug FROM platform_document_registry
       WHERE content_hash = $1 OR content_hash = $2 OR content_hash = $3
       ORDER BY tenant_id
       LIMIT ${V2_CROSS_TENANT_LIMIT}`,
      [computedHash, hashNorm, `sha256:${hashNorm}`],
    );
    for (const r of reg.rows) {
      try {
        const pool = mgr.getPool(r.tenant_id);
        const docRows = await runWithTenantId(r.tenant_id, () => queryWithTenantGuc(
          pool,
          `SELECT ${SELECT_COLUMNS}
           FROM documents d
           LEFT JOIN organizations o ON d.issuer_organization_id = o.id
           WHERE d.content_hash = $1 OR d.content_hash = $2 OR d.content_hash = $3
           ORDER BY d.certified_at DESC NULLS LAST
           LIMIT ${VERIFY_ROWSET_LIMIT}`,
          [computedHash, hashNorm, `sha256:${hashNorm}`],
        ));
        out.push(...docRows.rows.map((row: any) => ({ ...row, _tenantId: r.tenant_id, _tenantSlug: r.tenant_slug })));
      } catch (err: any) {
        logger.warn('v2 verify: cross-tenant rowset fetch failed', { tenant: r.tenant_slug, error: err?.message });
      }
    }
  } catch (err: any) {
    logger.warn('v2 verify: platform-registry enumeration failed', { error: err?.message });
  }
  return out;
}

/** Core: resolve a hash to its full match list. */
async function matchesForHash(req: Request, computedHash: string): Promise<{ hash: string; matches: Record<string, unknown>[] }> {
  const hashNorm = computedHash.replace(/^sha256:/, '');
  const canonicalHash = `sha256:${hashNorm}`;
  const db = (req as any).db || prisma;

  const local = await localRowsByHash(db, computedHash, hashNorm);
  const cross = await crossTenantRowsByHash(computedHash, hashNorm);
  // Dedupe on pkey — the registry enumeration can include the caller's own
  // tenant, whose rows the local query already returned (unscoped wins).
  const seen = new Set(local.map((r: any) => String(r.id)));
  const rows = [...local, ...cross.filter((r: any) => !seen.has(String(r.id)))];

  // Chain economy matches v1 (KS-252): the chain-fact read runs only when the
  // registry misses entirely (chain-first fallback) or a row needs a
  // stale-pending heal — never on every verify.
  let chain: Record<string, any> | null = null;
  const needsHeal = rows.some((r: any) => {
    const b = chainBlobOfRow(r);
    if (!b || b.simulated === true) return false;
    const tx = typeof b.txHash === 'string' ? b.txHash : null;
    if (!tx || !REAL_TXHASH_RE.test(tx)) return false;
    const settled = b.anchored === true || b.status === 'confirmed';
    const failed = b.status === 'failed' || b.status === 'anchor_failed';
    return !settled && !failed;
  });
  if (rows.length === 0 || needsHeal) {
    chain = await fetchChainFact(hashNorm);
  }

  if (rows.length === 0) {
    return { hash: canonicalHash, matches: chain ? [chainOnlyMatch(chain, canonicalHash)] : [] };
  }
  return {
    hash: canonicalHash,
    matches: sortRowsForPresentation(rows).map((row) => buildMatch(req, row, true, chain)),
  };
}

// =============================================================================
// ROUTES
// =============================================================================

/**
 * POST /api/v2/verification/verify
 * The list contract: every registration of the supplied bytes, each match
 * standing on its own evidence. 200 always carries {hash, count, matches} —
 * count 0 is the honest "never registered" answer.
 */
verificationV2Router.post(
  '/verify',
  [
    body('documentId').optional().isString(),
    body('hash').optional().isString(),
    body('contentHash').optional().isString(),
    body('providedHash').optional().isString(),
    body('documentHash').optional().isString(),
    body('documentData').optional().isObject(),
  ],
  async (req: Request, res: Response) => {
    try {
      const validationErrors = validationResult(req);
      if (!validationErrors.isEmpty()) {
        return res.status(400).json({
          success: false,
          error: {
            code: 'BAD_REQUEST',
            message: 'documentId, hash, contentHash, providedHash and documentHash must be strings; documentData must be an object.',
          },
        });
      }

      const { documentId, hash, providedHash, contentHash, documentHash, documentData } = req.body || {};
      const hashToVerify = hash || providedHash || contentHash || documentHash;
      if (!documentId && !hashToVerify && !documentData) {
        return res.status(400).json({
          success: false,
          error: { code: 'BAD_REQUEST', message: 'Provide a content hash (or documentData to hash), or a documentId.' },
        });
      }

      // Hash strategy (strongest — proves integrity) wins when present.
      let computedHash: string | undefined = hashToVerify;
      if (!computedHash && documentData) computedHash = generateHash(documentData);

      if (computedHash) {
        const { hash: canonicalHash, matches } = await matchesForHash(req, computedHash);
        return res.json({ hash: canonicalHash, count: matches.length, matches, verifiedAt: new Date().toISOString() });
      }

      // documentId-only strategy: exact registration lookup (KS-596 dual
      // identifiers: external_id first, then pkey UUID). hashValid=false —
      // existence, not integrity.
      const db = (req as any).db || prisma;
      let rows: any[] = await db.$queryRaw`
        SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
               d.certification_metadata, d.metadata, d.created_at, d.certified_at,
               d.tenant_id, o.name AS organization_name
        FROM documents d
        LEFT JOIN organizations o ON d.issuer_organization_id = o.id
        WHERE d.external_id = ${documentId} LIMIT 1
      `;
      if (rows.length === 0 && isValidUuid(documentId)) {
        try {
          rows = await db.$queryRaw`
            SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
                   d.certification_metadata, d.metadata, d.created_at, d.certified_at,
                   d.tenant_id, o.name AS organization_name
            FROM documents d
            LEFT JOIN organizations o ON d.issuer_organization_id = o.id
            WHERE d.id = ${documentId}::uuid LIMIT 1
          `;
        } catch { /* not resolvable as pkey */ }
      }
      const matches = rows.map((row) => buildMatch(req, row, false, null));
      return res.json({ hash: null, count: matches.length, matches, verifiedAt: new Date().toISOString() });
    } catch (error) {
      logger.error('v2 verification error', { error: error instanceof Error ? error.message : String(error) });
      return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Verification failed' } });
    }
  },
);

/**
 * POST /api/v2/verification/verify-file
 * Raw file bytes as the request body; the server computes the hash, so a
 * client cannot lie about it. Same list contract as /verify.
 */
verificationV2Router.post('/verify-file', async (req: Request, res: Response) => {
  try {
    const chunks: Buffer[] = [];
    await new Promise<void>((resolve, reject) => {
      req.on('data', (chunk: Buffer) => chunks.push(chunk));
      req.on('end', resolve);
      req.on('error', reject);
    });
    const fileBuffer = Buffer.concat(chunks);
    if (fileBuffer.length === 0) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'No file content received. Upload the document file as the request body.' },
      });
    }
    const fileHash = `sha256:${crypto.createHash('sha256').update(fileBuffer).digest('hex')}`;
    const { hash: canonicalHash, matches } = await matchesForHash(req, fileHash);
    return res.json({
      hash: canonicalHash,
      fileSize: fileBuffer.length,
      count: matches.length,
      matches,
      verifiedAt: new Date().toISOString(),
    });
  } catch (error) {
    logger.error('v2 file verification error', { error: error instanceof Error ? error.message : String(error) });
    return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'File verification failed' } });
  }
});

export default verificationV2Router;
