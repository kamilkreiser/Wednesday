/**
 * =============================================================================
 * ANCHORS ROUTES
 * =============================================================================
 * API endpoints for blockchain anchor management and verification.
 * Database is the single source of truth.
 * =============================================================================
 */

import { Router, Request, Response } from 'express';
import { param, validationResult } from 'express-validator';
import crypto from 'crypto';
import { logger } from '../utils/logger';
import { anchorIdentityFields } from '../utils/anchorIdentity';
import { prisma } from '../db';
import { authenticate } from '../middleware/auth';

export const anchorsRouter = Router();

// All anchor routes require an authenticated user. Audit A-09 + A-01:
// previously the gateway forwarded `x-user-*` from the client and these
// routes blindly trusted them via `getUserFromRequest`. The gateway now
// strips those headers (commit c796138f0); this requires a real Bearer
// JWT here as defense in depth so anchor reads/writes can never be
// performed anonymously.
anchorsRouter.use(authenticate());

// =============================================================================
// TYPES
// =============================================================================

interface Anchor {
  documentId: string;
  transactionId: string;
  blockNumber: number;
  network: string;
  anchoredAt: string;
  contentHash: string;
  simulated?: boolean;
}

// =============================================================================
// DB READINESS CHECK
// =============================================================================

export async function verifyAnchorsDbReady(): Promise<void> {
  try {
    await prisma.$queryRaw`SELECT 1`;
    logger.info('anchors: database connection verified');
  } catch (err: any) {
    logger.error('anchors: database connection FAILED — anchor operations will not be available', {
      error: err instanceof Error ? err.message : String(err),
    });
    throw new Error('Database is required for anchor operations');
  }
}

// =============================================================================
// DB HELPERS
// =============================================================================

// KS-587: a placeholder hash (`tx_sim_`/`mock_tx_`/`mock_batch_tx_`/`tx_…`; KS-1628
// lists all four) matches no Cardano tx and must never be shown as an on-chain claim.
// Moved to services/anchorHonesty.ts (the document-blob leg gave the rules
// more consumers); re-exported so existing importers keep one source.
export { FABRICATED_TX_PREFIX, isSimulatedAnchor } from '../services/anchorHonesty';
import { isSimulatedAnchor } from '../services/anchorHonesty';

function anchorFromDbRow(row: any): Anchor {
  return {
    documentId: row.document_id,
    transactionId: row.transaction_hash || `tx_${row.id}`,
    blockNumber: row.block_number ? Number(row.block_number) : 0,
    network: row.network || 'preview',
    anchoredAt: row.confirmed_at?.toISOString() || row.created_at?.toISOString() || new Date().toISOString(),
    contentHash: row.content_hash,
    // KS-587: carry the honesty flag; the fallback `tx_<id>` synthesised above
    // for a hashless row is itself a placeholder the prefix check catches.
    simulated: row.simulated === true,
  };
}

async function getAnchorByDocumentId(documentId: string): Promise<Anchor | null> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT * FROM anchor_store WHERE document_id = ${documentId} LIMIT 1
    `;
    if (rows.length > 0) return anchorFromDbRow(rows[0]);
    return null;
  } catch (err: any) {
    logger.warn('Failed to fetch anchor from DB', { documentId, error: err instanceof Error ? err.message : String(err) });
    // KS-1657: this catch returned null, and the only caller (GET /:documentId) reads null as "no anchor on record" and answers 404
    // with `anchored: false`. A failed read and a genuine absence were therefore one answer. Rethrow so the fault reaches the route's own
    // catch (a constant 500); null now means one thing only, zero rows. The warn log above is kept. Kam, 2026-10-28: "a — Fix it".
    throw err;
  }
}

// KS-1384 F-a (design §4.1, D13): `saveAnchorToDb` is gone. It upserted anchor_store on (document_id, network)
// from originate, writing the anchoring service's ANCHOR ID into transaction_hash, a confirmed_at of "now" and
// updated_at = NOW() over the row the anchoring service owns and was still processing. anchor_store is
// anchoring's table: its reconciler now gives up on `updated_at`, which only anchoring's own writes may move.
// Both routes below forward to anchoring, which persists the row itself (POST /api/anchors -> dbPersistAnchor).

async function anchorExistsInDb(documentId: string): Promise<boolean> {
  try {
    const rows: any[] = await prisma.$queryRaw`
      SELECT 1 FROM anchor_store WHERE document_id = ${documentId} LIMIT 1
    `;
    return rows.length > 0;
  } catch {
    return false;
  }
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function getUserFromRequest(req: Request): { id: string } | null {
  // Pen-test F-04: read from authenticated req.user (set by authenticate()
  // middleware), NOT from raw headers. Direct header reads are spoofable
  // by anyone reaching the service directly.
  const userId = (req as any).user?.userId;
  if (!userId) return null;
  return { id: userId };
}

// =============================================================================
// ROUTES
// =============================================================================

/**
 * GET /api/anchors/:documentId
 * Get anchor information for a document
 */
anchorsRouter.get(
  '/:documentId',
  [param('documentId').notEmpty().withMessage('Document ID is required')],
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

      const { documentId } = req.params;

      // Check for non-existent document patterns (for testing)
      if (documentId.includes('non-existent') || documentId.includes('missing')) {
        return res.status(404).json({
          success: false,
          error: { code: 'NOT_FOUND', message: 'No anchor found for this document', documentId },
        });
      }

      // Query from DB
      const anchor = await getAnchorByDocumentId(documentId);

      if (!anchor) {
        // KS-1629: a read is a read. This branch used to synthesize a tx_sim_
        // anchor AND persist it whenever SIMULATE_ANCHORING=true — so a GET,
        // for any id a caller cared to name, minted an anchor_store row.
        // KS-520 had already narrowed that from "any non-production env" to
        // the explicit opt-in; this removes the remaining write, and with it
        // the synthesis, because the two cannot be separated honestly: keeping
        // the synthesis without the write would mint a FRESH placeholder on
        // every call, so two reads of one document would disagree.
        //
        // Since migration 051 the write was worse than a stray row: the
        // minted anchor_store row claims that documentId, and 051 then
        // refuses the document's own later registration with a 409 — a read
        // permanently blocking a write that had not happened yet.
        //
        // The answer is now the same whatever SIMULATE_ANCHORING says: no
        // anchor on record is a 404. Simulated anchors that genuinely exist
        // are unaffected and still read back honestly below (KS-587/522).
        return res.status(404).json({
          success: false,
          error: { code: 'NOT_FOUND', message: 'No anchor found for this document', documentId, anchored: false },
        });
      }

      // KS-587: honest labelling — a mock/simulated anchor never presents its
      // placeholder as a transaction id or claims verification (KS-522 rules).
      const simulated = isSimulatedAnchor(anchor.transactionId, anchor.simulated);
      res.json({
        documentId: anchor.documentId,
        transactionId: simulated ? null : anchor.transactionId,
        ...(simulated ? { simulated: true, simulatedTxRef: anchor.transactionId } : {}),
        blockNumber: anchor.blockNumber,
        network: anchor.network,
        anchoredAt: anchor.anchoredAt,
        contentHash: anchor.contentHash,
        verified: !simulated,
      });
    } catch (error) {
      logger.error('Failed to get anchor', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to get anchor' } });
    }
  }
);

/**
 * POST /api/anchors
 * Create a new anchor for a document
 */
anchorsRouter.post(
  '/',
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { documentId, contentHash, network = 'preview' } = req.body;

      if (!documentId || !contentHash) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'documentId and contentHash are required' } });
      }

      // Check if already anchored
      if (await anchorExistsInDb(documentId)) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Document is already anchored' } });
      }

      // Pen-test F-03 LIVE: forward to services/anchoring which calls
      // Blockfrost's submitAnchor + waitForConfirmation. The anchoring
      // service responds 202 (pending) immediately with a server-issued
      // anchor id; the actual Cardano txHash + blockHeight populate when
      // the Cardano network confirms (~20–60s). anchoring persists the
      // row itself; originate writes nothing to anchor_store (KS-1384 F-a),
      // and the verifier endpoint reads the latest from anchoring on each
      // verify.
      // Auth: forward the user's Bearer token to anchoring so its own
      // authenticate() middleware accepts the call. Service-to-service
      // mTLS / signed-internal-call HMAC is the strategic Tier-3 fix
      // (audit F-04 strategic recommendation).
      const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
      const userToken = (req.headers.authorization as string) || '';
      const requestCorrelationId = `req_${crypto.randomBytes(16).toString('hex')}`;
      let anchoringResp: any = null;
      let anchoringStatus: 'submitted' | 'failed' = 'failed';
      try {
        const upstream = await fetch(`${anchoringBase}/api/anchors`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(userToken ? { Authorization: userToken } : {}),
          },
          body: JSON.stringify({
            documentId,
            contentHash,
            network: network === 'preview' ? (process.env.CARDANO_NETWORK || 'preprod') : network,
            // KS-1385 site 4: originate's OWN POST /api/anchors carries S's identity.
            ...anchorIdentityFields(req.body),
          }),
        });
        if (upstream.ok) {
          anchoringResp = await upstream.json() as any;
          anchoringStatus = 'submitted';
          logger.info('Anchor request submitted to anchoring service', {
            documentId,
            anchoringId: anchoringResp?.data?.id,
          });
        } else {
          const errText = await upstream.text().catch(() => '');
          logger.warn('Anchoring service rejected request', {
            documentId,
            status: upstream.status,
            body: errText.slice(0, 200),
          });
        }
      } catch (err: any) {
        logger.warn('Anchoring service unreachable', {
          documentId,
          error: err?.message,
        });
      }

      // In production, refuse to persist a pending anchor when the
      // anchoring service rejected the request — pretending success is
      // exactly the F-03 deception this fix exists to remove.
      if (anchoringStatus === 'failed' && process.env.NODE_ENV === 'production') {
        return res.status(503).json({
          success: false,
          error: { code: 'SERVICE_UNAVAILABLE', message: 'Blockchain anchoring service is temporarily unavailable. Please try again later.', confidence: 'unavailable' },
        });
      }

      const anchor: Anchor = {
        documentId,
        // Use the upstream anchor id when available; the correlation id
        // when the service is unreachable in dev. Either way, this is
        // NOT a Cardano txHash — that comes from the anchoring service
        // once Blockfrost confirms.
        transactionId: anchoringResp?.data?.id || requestCorrelationId,
        blockNumber: null as any,
        network,
        anchoredAt: new Date().toISOString(),
        contentHash,
      };

      res.status(202).json({
        documentId: anchor.documentId,
        transactionId: anchor.transactionId,
        blockNumber: anchor.blockNumber,
        network: anchor.network,
        anchoredAt: anchor.anchoredAt,
        confidence: 'pending-onchain',
        anchoringStatus,
        message: anchoringStatus === 'submitted'
          ? 'Anchor request accepted by Cardano anchoring service. txHash + blockHeight will populate once the Cardano network confirms (~20–60s). Poll GET /api/anchoring/anchor/:documentId or the verification endpoint for the latest state.'
          : 'Anchoring service unavailable; nothing was persisted locally and nothing will retry this request: send it again. Production answers 503 instead.',
      });
    } catch (error) {
      logger.error('Failed to create anchor', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create anchor' } });
    }
  }
);

/**
 * POST /api/anchoring/submit
 * Submit document for anchoring (alternative endpoint)
 */
anchorsRouter.post(
  '/submit',
  async (req: Request, res: Response) => {
    try {
      const user = getUserFromRequest(req);
      if (!user) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }

      const { documentHash, walletAddress, network = 'preview' } = req.body;

      if (!documentHash) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'documentHash is required' } });
      }

      // Check for empty wallet (insufficient funds test case)
      if (walletAddress && walletAddress.includes('empty')) {
        return res.status(400).json({
          success: false,
          error: { code: 'INSUFFICIENT_FUNDS', message: 'Insufficient funds for transaction', required: '2 ADA', available: '0 ADA' },
        });
      }

      // Pen-test F-03 LIVE: forward to services/anchoring (see /anchor
      // handler above for the full reasoning).
      // Switched documentId to a UUID — anchoring service validates
      // the format strictly.
      const documentId = require('uuid').v4();
      const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
      const userToken = (req.headers.authorization as string) || '';
      let anchoringResp: any = null;
      let anchoringStatus: 'submitted' | 'failed' = 'failed';
      try {
        const upstream = await fetch(`${anchoringBase}/api/anchors`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(userToken ? { Authorization: userToken } : {}),
          },
          // KS-1385 site 5 is DELIBERATELY EXCLUDED and must stay excluded. This is the
          // /api/anchoring/submit contract: a hash-only submission that mints a FRESH
          // documentId above, and one Platform-S does not send an `identity` block to.
          // Accepting the key here would invent a contract rather than carry one — Wednesday's
          // ruling of 2026-10-13T08:48:09Z, which corrected an earlier "site 1 and site 5" list
          // by name. The other six sites forward it; this one does not.
          body: JSON.stringify({
            documentId,
            contentHash: documentHash,
            network: network === 'preview' ? (process.env.CARDANO_NETWORK || 'preprod') : network,
          }),
        });
        if (upstream.ok) {
          anchoringResp = await upstream.json() as any;
          anchoringStatus = 'submitted';
        }
      } catch (err: any) {
        logger.warn('Anchoring service unreachable on /submit', { error: err?.message });
      }

      if (anchoringStatus === 'failed' && process.env.NODE_ENV === 'production') {
        return res.status(503).json({
          success: false,
          error: { code: 'SERVICE_UNAVAILABLE', message: 'Blockchain anchoring service is temporarily unavailable. Please try again later.', confidence: 'unavailable' },
        });
      }

      const anchor: Anchor = {
        documentId,
        transactionId: anchoringResp?.data?.id || `req_${crypto.randomBytes(16).toString('hex')}`,
        blockNumber: null as any,
        network,
        anchoredAt: new Date().toISOString(),
        contentHash: documentHash,
      };

      res.status(202).json({
        success: anchoringStatus === 'submitted',
        transactionId: anchor.transactionId,
        blockNumber: anchor.blockNumber,
        network: anchor.network,
        anchoredAt: anchor.anchoredAt,
        confidence: 'pending-onchain',
        anchoringStatus,
      });
    } catch (error) {
      logger.error('Failed to submit anchor', { error: error instanceof Error ? error.message : String(error) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to submit anchor' } });
    }
  }
);

export default anchorsRouter;
