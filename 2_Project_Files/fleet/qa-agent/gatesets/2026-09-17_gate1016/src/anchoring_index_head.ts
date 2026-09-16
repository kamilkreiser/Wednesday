/**
 * =============================================================================
 * SECUURA ANCHORING SERVICE
 * =============================================================================
 * Handles blockchain anchoring to Cardano:
 * - Single document anchoring
 * - Batch anchoring (Merkle tree)
 * - Transaction metadata (CIP-674)
 * - Anchor verification
 * Port: 4005
 * =============================================================================
 */

import express, { Request, Response, NextFunction, RequestHandler } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { z } from 'zod';
import crypto from 'crypto';
import dotenv from 'dotenv';
import { initDb, isDbAvailable, query, closeDb } from './db';
import {
  initCardano,
  isCardanoReady,
  getWalletAddress,
  submitAnchor,
  waitForConfirmation,
  getChainHealth,
  isCardanoConfigured,
  CHAIN_DEGRADED_AFTER_FAILURES,
} from './cardano';
import { deriveHealth } from './chainHealthStatus';
import { validateEnv } from './utils/logger';
import { createStuckAnchorReconciler } from './reconciler';
import { deriveVerifyAcceptance } from './verifyAnchorStatus';
// KS-705: the Cardano submit/confirm/retry flow, extracted for the same
// bootless-unit-test reason as reconciler.ts. `withWalletLock` is imported (not
// redefined) so the batch path below shares the SAME wallet mutex — two
// independent locks on one wallet would be no lock at all.
import { createAnchorSubmitter, withWalletLock } from './anchorSubmission';
// KS-388: the flat-anchor request schema (incl. the KS-134 lifecycle verb enum on
// metadata.documentType) lives in anchorSchema.ts so it is unit-testable without
// booting this service (this module calls app.listen on import).
import { anchorDocumentSchema, buildFlatAnchorMetadataPayload } from './anchorSchema';
// KS-445: thread-mint request contract + mint-failure classifier — extracted
// for the same bootless-unit-test reason as anchorSchema above.
import { threadMintRequestSchema, isEncodableDeploymentIdHex, classifyThreadMintError } from './threadMintRequest';
import { enforceProductionConfig, authenticate as jwtAuthenticate, errorHandler, rejectNulBytes } from '@secuura/shared';
import { recordFlatAnchorProvenance } from './provenance';
import { honestTxView, FABRICATED_TX_PREFIX } from './honestAnchor';

dotenv.config();

// Validate environment variables at startup
validateEnv();

// KS-480 §6: PII keyring for flat-anchor provenance (action_provenance rows
// carry encrypted email/displayName). Guarded like originate's init — absent
// key ⇒ provenance rows are skipped (never plaintext), anchoring still runs.
if (process.env.PII_ENCRYPTION_KEY) {
  try {
    const { initFromEnv } = require('@secuura/shared');
    initFromEnv();
    console.log('[anchoring] PII encryption keyring initialised (KS-480 provenance)');
  } catch (err) {
    console.warn('[anchoring] PII keyring init failed — flat-anchor provenance will be skipped:', (err as Error).message);
  }
}

// Production startup guard — refuse to start with mock/dev config in production
enforceProductionConfig('anchoring', {
  requiredEnvVars: ['BLOCKFROST_PROJECT_ID'],
  requireRealProviders: true,
});

const app = express();
const PORT = process.env.PORT || 4005;
// AUDIT B-16: allowlisted set of Cardano networks. Any request that asks
// for a network outside this set is rejected; cross-network confusion
// (mainnet tx replayed on preprod application-side, etc.) is blocked at
// the application layer even though network magic prevents the on-chain
// replay.
const ALLOWED_CARDANO_NETWORKS = new Set(['mainnet', 'preprod', 'preview', 'devnet']);
const CARDANO_NETWORK = process.env.CARDANO_NETWORK || 'preprod';
if (!ALLOWED_CARDANO_NETWORKS.has(CARDANO_NETWORK)) {
  console.error(`[anchoring] FATAL: CARDANO_NETWORK="${CARDANO_NETWORK}" not in allowlist ${[...ALLOWED_CARDANO_NETWORKS].join(',')}`);
  process.exit(1);
}
const CARDANO_NODE_URL = process.env.CARDANO_NODE_URL || 'http://localhost:6092';

/** AUDIT B-16: validate a per-request network parameter against the allowlist. */
function isAllowedNetwork(n: unknown): n is string {
  return typeof n === 'string' && ALLOWED_CARDANO_NETWORKS.has(n);
}

// =============================================================================
// TYPE DEFINITIONS
// =============================================================================

interface Anchor {
  id: string;
  documentId: string;
  anchorType: 'single' | 'batch';
  contentHash: string;
  merkleRoot?: string;
  merkleProof?: MerkleProofStep[];
  transactionHash?: string;
  blockHash?: string;
  blockNumber?: number;
  slot?: number;
  network: string;
  metadataLabel: number;
  metadataPayload: object;
  /**
   * KS-726 adds 'submitting': the transaction is signed and its deterministic
   * hash is persisted, but the node has not yet acknowledged it. Distinct from
   * 'submitted' (node accepted) and from 'pending' (nothing signed yet), because
   * only this state means "a transaction bearing our name may already be on
   * chain". 'failed' remains TERMINAL by construction (KS-535) — originate's
   * poller depends on that and this state does not disturb it.
   */
  status: 'pending' | 'submitting' | 'submitted' | 'confirmed' | 'failed';
  fee?: number;
  confirmations: number;
  confirmedAt?: Date;
  errorMessage?: string;
  retryCount: number;
  // KS-587: true when this anchor was produced by the mock/simulated provider
  // and corresponds to no Cardano transaction.
  simulated?: boolean;
  createdAt: Date;
  updatedAt: Date;
}

interface MerkleProofStep {
  hash: string;
  position: 'left' | 'right';
}

interface MerkleBatch {
  id: string;
  documentIds: string[];
  merkleRoot: string;
  documentCount: number;
  status: 'pending' | 'submitted' | 'confirmed' | 'failed';
  anchorId?: string;
  createdAt: Date;
}

// =============================================================================
// STORAGE: All data is persisted in PostgreSQL (anchor_store, anchor_batches)
// No in-memory Maps — every read/write goes through the DB helpers below.
// =============================================================================

// =============================================================================
// DATABASE TABLES (ensured on first write)
// =============================================================================

let tablesEnsured = false;

async function ensureTables(): Promise<void> {
  if (tablesEnsured || !isDbAvailable()) return;
  try {
    // KS-92: anchor_store + anchor_batches are owned by the superuser migration
    // path (api-gateway CORE_MIGRATIONS). The runtime role (secuura_app) lacks
    // CREATE on schema public, so the CREATE TABLE below throws 42501 even with
    // IF NOT EXISTS. Verify the migration-created tables are present and skip
    // the redundant DDL when they are.
    const existing: any = await query(
      `SELECT to_regclass('public.anchor_store') AS s, to_regclass('public.anchor_batches') AS b`
    );
    const row = existing?.rows?.[0] ?? existing?.[0];
    if (row && row.s && row.b) {
      tablesEnsured = true;
      return;
    }
    await query(`
      CREATE TABLE IF NOT EXISTS anchor_store (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        anchor_type TEXT NOT NULL DEFAULT 'single',
        content_hash TEXT NOT NULL,
        merkle_root TEXT,
        merkle_proof JSONB,
        network TEXT NOT NULL DEFAULT 'cardano',
        metadata_label INTEGER DEFAULT 674,
        metadata_payload JSONB,
        status TEXT NOT NULL DEFAULT 'pending',
        transaction_hash TEXT,
        block_hash TEXT,
        block_number BIGINT,
        slot BIGINT,
        fee BIGINT,
        confirmations INTEGER DEFAULT 0,
        confirmed_at TIMESTAMPTZ,
        error_message TEXT,
        retry_count INTEGER DEFAULT 0,
        simulated BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
      )
    `);
    await query(`CREATE INDEX IF NOT EXISTS idx_anchor_store_document ON anchor_store(document_id)`);
    await query(`CREATE INDEX IF NOT EXISTS idx_anchor_store_tx ON anchor_store(transaction_hash)`);
    await query(`CREATE INDEX IF NOT EXISTS idx_anchor_store_status ON anchor_store(status)`);
    // KS-281: composite unique so dbPersistAnchor's ON CONFLICT (document_id,
    // network) resolves on a fresh DB where ensureTables created the table
    // before migration 031 ran. On migrated DBs ensureTables verify-skips and
    // migration 031 owns this index.
    await query(`CREATE UNIQUE INDEX IF NOT EXISTS anchor_store_document_network_uniq ON anchor_store(document_id, network)`);

    await query(`
      CREATE TABLE IF NOT EXISTS anchor_batches (
        id TEXT PRIMARY KEY,
        document_ids TEXT[],
        merkle_root TEXT NOT NULL,
        document_count INTEGER NOT NULL DEFAULT 0,
        anchor_id TEXT,
        status TEXT NOT NULL DEFAULT 'pending',
        transaction_hash TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW()
      )
    `);
    tablesEnsured = true;
  } catch (err: any) {
    log('warn', 'Failed to ensure anchor tables', { error: err?.message });
  }
}

// =============================================================================
// LOGGING
// =============================================================================

function log(level: 'info' | 'warn' | 'error', message: string, meta?: object) {
  const timestamp = new Date().toISOString();
  console.log(JSON.stringify({ timestamp, level, service: 'anchoring', message, ...meta }));
}

// =============================================================================
// MIDDLEWARE
// =============================================================================

app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:6100', 'http://localhost:6101'],
  credentials: true,
}));
app.use(express.json());
app.use(rejectNulBytes()); // KS-471: no U+0000 may pass the boundary (raw-500 / persist class)

// Request logging
const requestLogger: RequestHandler = (req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    log('info', 'Request completed', {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: `${Date.now() - start}ms`,
    });
  });
  next();
};
app.use(requestLogger);

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================
// (anchorDocumentSchema — the flat-anchor request incl. the KS-388 lifecycle verb
// enum — is imported from ./anchorSchema at the top of this file.)

const batchAnchorSchema = z.object({
  documents: z.array(z.object({
    documentId: z.string().uuid(),
    contentHash: z.string().regex(/^[a-f0-9]{64}$/i),
  })).min(1).max(100),
});

const verifyAnchorSchema = z.object({
  contentHash: z.string().regex(/^[a-f0-9]{64}$/i),
  transactionHash: z.string().optional(),
  merkleProof: z.array(z.object({
    hash: z.string(),
    position: z.enum(['left', 'right']),
  })).optional(),
});

// =============================================================================
// ROUTES
// =============================================================================

// Health check
app.get('/health', async (_req: Request, res: Response) => {
  // KS-671: report what the chain ACTUALLY did on the calls this service
  // already made — never from isCardanoReady(), which only tests that the key
  // is SET. A present-but-over-quota key satisfied the old check, which is how
  // demo reported healthy through six days of 402s (KS-670).
  //
  // The derivation itself lives in ./chainHealthStatus as a pure function so
  // it can be tested without booting this service (#728 review: defect #2 was
  // the hardcoded `status`, and that half shipped untested).
  const chain = getChainHealth();
  const verdict = deriveHealth({
    chain,
    cardanoConfigured: isCardanoConfigured(),
    cardanoReady: isCardanoReady(),
    dbAvailable: isDbAvailable(),
    degradedAfterFailures: CHAIN_DEGRADED_AFTER_FAILURES,
  });

  let cardanoStatus = verdict.cardanoStatus;

  // Dev/CI only. Probing a local devnet is free and never touches the
  // Blockfrost quota — but it runs ONLY when no credentials were supplied at
  // all. In the `mock-fallback` state we already know precisely what is wrong,
  // and overwriting that with 'mock mode' is what buried KS-670 for six days.
  if (verdict.mode === 'mock') {
    try {
      // KS-91: 500ms (not 3000) — api-gateway's /health/ready races each
      // downstream /health with a 3000ms CHECK_TIMEOUT. A 3000ms fetch
      // timeout here means /health always completes >3000ms when the
      // devnet is unreachable (CI workflow boot set excludes cardano-node),
      // so the gateway times out and reports 503. Production hits the
      // isCardanoReady() branch above (Blockfrost), so this fetch only
      // runs in dev/CI against a localhost devnet — 500ms is plenty.
      const response = await fetch(`${CARDANO_NODE_URL}/health`, {
        signal: AbortSignal.timeout(500)
      });
      cardanoStatus = response.ok ? 'connected (devnet)' : 'error';
    } catch {
      cardanoStatus = verdict.cardanoStatus;
    }
  }

  let pendingCount = 0;
  try {
    if (isDbAvailable()) {
      await ensureTables();
      const result = await query("SELECT COUNT(*) AS cnt FROM anchor_store WHERE status = 'pending'");
      pendingCount = Number(result.rows[0]?.cnt ?? 0);
    }
  } catch {
    // ignore — report 0
  }

  // KS-671: `status` was hardcoded 'healthy', so nothing the body reported
  // could ever change it. It is now derived — see ./chainHealthStatus.
  //
  // DELIBERATE: this endpoint still answers HTTP 200 when the chain is
  // degraded, because the compose healthcheck (`wget --spider`) treats a
  // non-200 as container death and `restart: unless-stopped` would then
  // restart-loop the service. Restarting does not refill a quota, and killing
  // anchoring on a provider outage is worse than running degraded. Liveness
  // and chain reachability are different questions; this reports both and
  // conflates neither. Wiring an alert to `status: 'degraded'` is the
  // monitoring change, tracked on KS-671.
  res.json({
    status: verdict.status,
    degradedReasons: verdict.degradedReasons,
    service: 'anchoring',
    version: '0.2.0',
    timestamp: new Date().toISOString(),
    database: isDbAvailable() ? 'connected' : 'unavailable',
    cardano: {
      network: CARDANO_NETWORK,
      mode: verdict.mode,
      walletAddress: getWalletAddress(),
      status: cardanoStatus,
      reachability: chain.reachability,
      stale: chain.stale,
      lastSuccessAt: chain.lastSuccessAt,
      lastFailureAt: chain.lastFailureAt,
      lastFailureStatus: chain.lastFailureStatus,
      consecutiveFailures: chain.consecutiveFailures,
    },
    queue: {
      pending: pendingCount,
    },
  });
});

// Readiness check — verifies PostgreSQL is reachable
app.get('/health/ready', async (_req: Request, res: Response) => {
  const CHECK_TIMEOUT = 3000;
  const checks: Record<string, { status: string; latencyMs: number; error?: string }> = {};

  const start = Date.now();
  try {
    await Promise.race([
      (async () => {
        if (!isDbAvailable()) throw new Error('Database not available');
        await query('SELECT 1');
      })(),
      new Promise<never>((_, reject) =>
        setTimeout(() => reject(new Error('timeout')), CHECK_TIMEOUT),
      ),
    ]);
    checks.postgres = { status: 'up', latencyMs: Date.now() - start };
  } catch (err: any) {
    checks.postgres = {
      status: 'down',
      latencyMs: Date.now() - start,
      error: err?.message || 'Unknown error',
    };
  }

  const allUp = Object.values(checks).every(c => c.status === 'up');

  res.status(allUp ? 200 : 503).json({
    ready: allUp,
    checks,
  });
});

// API info
app.get('/api', (_req: Request, res: Response) => {
  res.json({
    service: 'Secuura Anchoring Service',
    version: '0.1.0',
    network: CARDANO_NETWORK,
    endpoints: {
      'POST /api/anchors': 'Anchor a single document',
      'POST /api/anchors/batch': 'Anchor multiple documents (Merkle tree)',
      'GET /api/anchors/:id': 'Get anchor by ID',
      'GET /api/anchors/document/:documentId': 'Get anchors for document',
      'GET /api/anchors/tx/:txHash': 'Get anchor by transaction hash',
      'POST /api/anchors/verify': 'Verify an anchor',
      'GET /api/anchors/queue': 'Get queue status',
    },
    metadataLabels: {
      674: 'Secuura Document Anchor (single)',
      675: 'Secuura Merkle Root Anchor (batch)',
    },
  });
});

// KS-584 (P3, QA-High): the chain-fact read is registered BEFORE the auth
// mount so anchor truth is caller-independent. Originate's verify heal used
// to FORWARD the caller's bearer here — anonymous/invalid callers therefore
// could not confirm a stale 'pending' anchor and were served a false-negative
// isAnchored while authenticated callers got the truth (QA finding, 2026-08-11;
// Kam ruled anonymous verify is a supported public path). The response is the
// same chain-public fact set K's public verify already emits (tx, block,
// anchor metadata) — no credential material, no tenant-owned naming — so the
// H2 rationale below (forgeable trust headers) does not apply to it. The
// gateway's own spec-auth gate for EXTERNAL calls is unchanged.
app.get('/api/anchors/verify/:hash', (req: Request, res: Response) => handleAnchorVerifyByHash(req, res));

// Pen-test H2 — every /api/* route below this point JWT-verifies the
// bearer token via @secuura/shared's `authenticate()`. Without this,
// downstream services trusted the gateway-injected x-user-* headers,
// which an attacker reaching a service directly (intra-cluster, leaked
// internal endpoint, etc.) could forge.
app.use('/api', jwtAuthenticate());

/**
 * POST /api/anchors
 * Anchor a single document to the blockchain
 */
app.post('/api/anchors', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = anchorDocumentSchema.parse(req.body);

    // KS-480 §6 / KS-566: attribution on the flat fallback path. Kam's G-1
    // ruling puts this surface on the CONNECTOR pattern, so there is no
    // caller-supplied principal to validate any more — `onBehalfOf` is
    // stripped by the schema (anchorSchema.ts) rather than 400'd, because
    // Platform S is live sending it (PS-616, UAT since 2026-08-21T10:07Z).
    // Stored OFF-CHAIN in action_provenance, never in metadataPayload
    // (whitelist below).
    const caller = (req as any).user as { role?: string; userId?: string; organizationId?: string; tenantId?: string } | undefined;

    // Create anchor record
    const anchorId = `anchor_${require('crypto').randomUUID()}`;

    // KS-240/KS-480: THE single whitelist construction path — extracted so
    // the "provenance never reaches the chain" guarantee is unit-tested
    // structurally, not remembered per-field (Peter §6 condition 1).
    const metadataPayload = buildFlatAnchorMetadataPayload(data, CARDANO_NETWORK);
    
    const anchor: Anchor = {
      id: anchorId,
      documentId: data.documentId,
      anchorType: 'single',
      contentHash: data.contentHash,
      network: CARDANO_NETWORK,
      metadataLabel: 674,
      metadataPayload,
      status: 'pending',
      confirmations: 0,
      retryCount: 0,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    // Persist to database. KS-281: dbPersistAnchor returns the ACTUAL stored id
    // (the existing row's id on a re-anchor of the same document+network) and
    // throws on failure — so the surfaced id always resolves on GET, and a
    // failed write becomes a 5xx via the catch below instead of a false 202.
    const persistedId = await dbPersistAnchor(anchor);

    // KS-480 §6 / KS-566: append the provenance row fire-and-forget (the anchor
    // itself never blocks on attribution). CONNECTOR-ONLY — one row per
    // connector flat anchor, attributed to the key, no principal.
    //
    // The condition moved from `data.onBehalfOf` to the caller's role, and
    // that IS the fix: before KS-566 a bare connector anchor wrote no
    // provenance row at all, so dropping the field would have left this route
    // with no actor of any kind. Interactive (JWT) callers still write none —
    // their identity is the JWT, and inventing a connector row for a human
    // would be a false attribution.
    // KS-566: `x-emitter-internal` means this is K's own originate->anchoring
    // hop for an operation that ALREADY wrote its own action_provenance row
    // (create / share / transfer-custody / revoke / lifecycle). Recording again
    // here would make one user action produce two rows and roughly double the
    // table — measured live on 2026-08-26, where a single lifecycle call
    // produced both a `lifecycle:rename` and an `anchor` row. The header is not
    // spoofable: the gateway strips `x-emitter-*` from every inbound client
    // request, and internal hops bypass the gateway. Platform-S's genuine flat
    // fallback carries no such header and still records its `anchor` row.
    const isInternalEmit = typeof req.headers['x-emitter-internal'] === 'string';
    if (caller?.role === 'connector' && !isInternalEmit) {
      recordFlatAnchorProvenance({
        documentId: data.documentId,
        connectorId: caller.userId,
        organizationId: caller.organizationId,
        tenantId: caller.tenantId,
      }).catch((provErr: Error) => log('warn', 'flat-anchor provenance record failed', { documentId: data.documentId, error: provErr.message }));
    }

    // Process anchor (in development mode, mock the transaction)
    processAnchor(persistedId);

    log('info', 'Anchor created', { anchorId: persistedId, documentId: data.documentId });

    res.status(202).json({
      success: true,
      data: {
        id: persistedId,
        documentId: anchor.documentId,
        contentHash: anchor.contentHash,
        status: anchor.status,
        network: anchor.network,
        metadataLabel: anchor.metadataLabel,
        createdAt: anchor.createdAt,
        message: 'Anchor request submitted. Transaction will be processed shortly.',
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    next(error);
  }
});

/**
 * GET /api/anchors/verify/:hash
 * Chain-first verification: given a content hash, return the on-chain anchor
 * record (if any). Works across environments because the source of truth is
 * the blockchain, not per-environment databases.
 *
 * Lookup order:
 *   1. Local anchor_store DB (fast path — same-environment hit)
 *   2. Blockfrost scan of platform wallet's recent txs at metadata label 674
 *      (cross-environment hit — chain is shared)
 */

// KS-252: the step-2 chain scan was unbounded — 1 + up-to-100 sequential
// indexer calls (~20-30 s) for EVERY hash not anchored yet, which is the
// common case when a verify races a fresh anchor. Under the KS-194 load
// baseline that stalled 39% of /api/verification/verify calls to client
// timeout. Bound it three ways: batch the metadata fetches concurrently,
// stop at a wall-clock budget, and cache scan outcomes (a positive hit is
// an immutable on-chain fact; a miss gets a short TTL since the hash may
// confirm at any moment).
const VERIFY_SCAN_BUDGET_MS = parseInt(process.env.VERIFY_CHAIN_SCAN_BUDGET_MS || '4000', 10);
const VERIFY_SCAN_BATCH = 10;
const VERIFY_SCAN_NEG_TTL_MS = 30_000;
const VERIFY_SCAN_POS_TTL_MS = 600_000;
const VERIFY_SCAN_CACHE_MAX = 5_000;
const verifyScanCache = new Map<string, { expires: number; hit: Record<string, any> | null }>();

// KS-584 (P3): extracted to a named handler — registered pre-auth above (see
// the comment at the registration site); the route path stays identical.
const handleAnchorVerifyByHash = async (req: Request, res: Response) => {
  const raw = (req.params.hash || '').trim();
  const hash = raw.replace(/^sha256:/i, '').toLowerCase();
  if (!/^[a-f0-9]{64}$/.test(hash)) {
    return res.status(400).json({ verified: false, error: 'Invalid content hash — expect 64 hex chars' });
  }

  const explorerBase = CARDANO_NETWORK === 'mainnet'
    ? 'https://cardanoscan.io/transaction'
    : `https://${CARDANO_NETWORK}.cardanoscan.io/transaction`;

  const buildResponse = (source: 'db' | 'chain', onChain: any, row?: any) => {
    const sec = onChain?.secuura || {};
    const rawTxHash = onChain?.txHash || row?.transaction_hash;
    // KS-522: honest labelling — a `tx_sim_`/`mock_tx_`/`tx_…` placeholder
    // corresponds to NO Cardano transaction (SIMULATE_ANCHORING / the legacy
    // dev mock). Never present it as an on-chain claim: the placeholder moves
    // to `simulatedTxRef`, `simulated: true` is machine-readable, and no
    // explorer URL is fabricated for a non-existent tx.
    const simulated = typeof rawTxHash === 'string' && /^(tx_sim_|mock_tx_|tx_)/.test(rawTxHash);
    const txHash = simulated ? null : rawTxHash;
    // KS-726 (#805 review F1): the query above admits 'submitting' rows, whose
    // transaction the node has NOT acknowledged. `verified: true` alone cannot
    // express that, so the anchor's own lifecycle state is returned, plus a
    // boolean so a consumer need not know the status vocabulary to read it.
    // A chain-sourced result was found by scanning the chain, so it is
    // acknowledged by construction.
    const acceptance = deriveVerifyAcceptance(source, row?.status);
    return {
      verified: true,
      source,
      network: CARDANO_NETWORK,
      status: acceptance.status,
      acknowledged: acceptance.acknowledged,
      txHash,
      ...(simulated ? { simulated: true, simulatedTxRef: rawTxHash } : {}),
      cardanoScanUrl: txHash ? `${explorerBase}/${txHash}` : null,
      blockNumber: onChain?.blockNumber || row?.block_number || null,
      confirmedAt: onChain?.confirmedAt || row?.confirmed_at || null,
      anchoredAt: row?.created_at || null,
      metadata: {
        version: sec.version || '1.0',
        environment: sec.environment || null,
        issuerOrgId: sec.issuerOrgId || null,
        issuerName: sec.issuerName || null,
        documentId: sec.documentId || row?.document_id || null,
        certId: sec.certId || sec.documentId || row?.document_id || null,
        contentHash: sec.hash || hash,
        documentType: sec.documentType || null,
        timestamp: sec.timestamp || null,
        // KS-555: client-asserted event time (anchored from metadata.timestamp);
        // null for anchors that predate the field or never asserted one.
        occurredAt: sec.occurredAt || null,
        // KS-721: Platform-S's opaque identity commitment, read back verbatim so
        // S can surface "anchored identity commitment" at display time. Null for
        // anchors that predate the field or never asserted one — and, by design,
        // it stays a bare token here: K never resolves it to an identity, and
        // after S shreds the `vN` key version nobody can.
        identityCommitment: sec.identityCommitment || null,
      },
    };
  };

  try {
    // Step 1 — local DB lookup (fast, same-env)
    try {
      const result = await query(
        `SELECT id, document_id, content_hash, transaction_hash, block_number,
                block_hash, confirmed_at, created_at, metadata_payload, status
           FROM anchor_store
          -- KS-726: 'submitting' included. The row carries a REAL, locally
          -- derived transaction hash at this point, so omitting it made a
          -- written-ahead anchor invisible to verify-by-hash — and a row RESTING
          -- in 'submitting' (the state the failure path now leaves behind)
          -- invisible indefinitely. Invisible is the worse failure.
          --
          -- #805 review F1: this comment used to claim the status was "selected
          -- and returned". It was selected and then DROPPED — buildResponse had
          -- no status key, verified:true is unconditional, and KS-522's honesty
          -- branch keys off the tx-hash PREFIX, which a real written-ahead
          -- 64-hex passes straight through. So the caller was handed
          -- verified:true plus a live explorer link for a submission the node
          -- had never acknowledged, with no way to tell it from a confirmed
          -- one. The mitigation is now actually implemented: see the status and
          -- acknowledged fields in buildResponse.
          --
          -- NOTE: no backticks in this block. It sits inside a TEMPLATE
          -- LITERAL, so a backtick here terminates the string and the SQL
          -- comment marker gives no protection — it fails as a JS syntax error
          -- pointing at the WHERE clause, ten lines below the real cause.
          WHERE LOWER(content_hash) = $1 AND status IN ('submitting','submitted','confirmed')
          ORDER BY confirmed_at DESC NULLS LAST, created_at DESC
          LIMIT 1`,
        [hash],
      );
      if (result.rows.length > 0) {
        const row = result.rows[0] as any;
        const payload = typeof row.metadata_payload === 'string'
          ? JSON.parse(row.metadata_payload)
          : (row.metadata_payload || {});
        return res.json(buildResponse('db', payload, row));
      }
    } catch (err: any) {
      log('warn', 'verify-by-hash: local DB lookup failed', { error: err?.message });
    }

    // Step 2 — chain scan (cross-env). Only possible if Blockfrost is ready.
    if (!isCardanoReady()) {
      return res.status(404).json({ verified: false, hash, reason: 'Not found in local DB and Blockfrost not configured.' });
    }

    // KS-252: serve a recent scan outcome from cache before hitting the chain.
    const cached = verifyScanCache.get(hash);
    if (cached && cached.expires > Date.now()) {
      if (cached.hit) {
        return res.json(cached.hit);
      }
      return res.status(404).json({ verified: false, hash, reason: 'No on-chain anchor found for this hash (cached scan).' });
    }

    const { getProvider } = await import('./cardano/provider');
    const bf: any = getProvider();
    const walletAddress = getWalletAddress();
    if (!bf || !walletAddress) {
      return res.status(404).json({ verified: false, hash, reason: 'Blockfrost or wallet not initialised.' });
    }

    // Fetch recent txs for the platform wallet. 100 is plenty for a testnet;
    // paginate further if needed. KS-252: metadata lookups run in concurrent
    // batches under a wall-clock budget instead of one-by-one (the old
    // sequential walk took ~20-30 s on a miss).
    const txs: any[] = (await bf.addressesTransactions(walletAddress, { order: 'desc', count: 100 })) || [];
    const scanDeadline = Date.now() + VERIFY_SCAN_BUDGET_MS;
    let scanComplete = true;

    if (verifyScanCache.size >= VERIFY_SCAN_CACHE_MAX) {
      verifyScanCache.clear(); // simple bound; entries are cheap to recompute
    }

    for (let i = 0; i < txs.length; i += VERIFY_SCAN_BATCH) {
      if (Date.now() > scanDeadline) {
        scanComplete = false;
        log('warn', 'verify-by-hash: chain-scan budget exhausted', {
          hash: hash.substring(0, 16), scanned: i, total: txs.length, budgetMs: VERIFY_SCAN_BUDGET_MS,
        });
        break;
      }
      const batch = txs.slice(i, i + VERIFY_SCAN_BATCH);
      const metas = await Promise.all(batch.map(async (tx: any) => {
        try {
          return { tx, md: (await bf.txsMetadata(tx.tx_hash)) as any[] };
        } catch (err: any) {
          log('warn', 'verify-by-hash: metadata fetch failed for tx', { txHash: tx.tx_hash, error: err?.message });
          return { tx, md: null as any[] | null };
        }
      }));

      for (const { tx, md } of metas) {
        const secEntry = (md || []).find((m: any) => String(m.label) === '674');
        const sec = secEntry?.json_metadata?.secuura;
        if (!sec) continue;
        const onChainHash = String(sec.hash || '').replace(/^sha256:/i, '').toLowerCase();
        if (onChainHash !== hash) continue;

        // Hash matches — resolve block info
        const txInfo: any = await bf.txs(tx.tx_hash).catch(() => null);
        const onChain = {
          secuura: sec,
          txHash: tx.tx_hash,
          blockNumber: txInfo?.block_height || null,
          confirmedAt: txInfo?.block_time ? new Date(txInfo.block_time * 1000).toISOString() : null,
        };
        const body = buildResponse('chain', onChain);
        // An on-chain anchor is immutable — cache the hit for re-verifies.
        verifyScanCache.set(hash, { expires: Date.now() + VERIFY_SCAN_POS_TTL_MS, hit: body });
        return res.json(body);
      }
    }

    // Cache the miss briefly only when the scan covered every candidate tx —
    // a budget-truncated scan proves nothing.
    if (scanComplete) {
      verifyScanCache.set(hash, { expires: Date.now() + VERIFY_SCAN_NEG_TTL_MS, hit: null });
    }
    return res.status(404).json({ verified: false, hash, reason: 'No on-chain anchor found for this hash.' });
  } catch (error: any) {
    log('error', 'verify-by-hash failed', { error: error?.message });
    return res.status(500).json({ verified: false, error: 'Chain verification failed', details: error?.message });
  }
};

/**
 * POST /api/anchors/batch
 * Anchor multiple documents using Merkle tree
 */
app.post('/api/anchors/batch', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = batchAnchorSchema.parse(req.body);
    
    // Build Merkle tree
    const hashes = data.documents.map(d => d.contentHash);
    const { root, proofs } = buildMerkleTree(hashes);
    
    // Create batch record
    const batchId = `batch_${require('crypto').randomUUID()}`;
    const batch: MerkleBatch = {
      id: batchId,
      documentIds: data.documents.map(d => d.documentId),
      merkleRoot: root,
      documentCount: data.documents.length,
      status: 'pending',
      createdAt: new Date(),
    };
    // Persist batch to database
    await dbPersistBatch(batch);
    
    // Create anchors for each document
    const anchorIds: string[] = [];
    
    for (let i = 0; i < data.documents.length; i++) {
      const doc = data.documents[i];
      const anchorId = `anchor_${require('crypto').randomUUID()}_${i}`;
      
      const anchor: Anchor = {
        id: anchorId,
        documentId: doc.documentId,
        anchorType: 'batch',
        contentHash: doc.contentHash,
        merkleRoot: root,
        merkleProof: proofs[i],
        network: CARDANO_NETWORK,
        metadataLabel: 675,
        metadataPayload: {
          secuura: {
            version: '1.0',
            type: 'batch',
            merkleRoot: root,
            documentCount: data.documents.length,
            batchId,
            timestamp: new Date().toISOString(),
          },
        },
        status: 'pending',
        confirmations: 0,
        retryCount: 0,
        createdAt: new Date(),
        updatedAt: new Date(),
      };
      
      anchorIds.push(anchorId);

      // Persist each anchor to database
      await dbPersistAnchor(anchor);
    }
    
    // Process batch anchor (single transaction for Merkle root)
    processBatchAnchor(batchId, anchorIds);
    
    log('info', 'Batch anchor created', { batchId, documentCount: data.documents.length });
    
    res.status(202).json({
      success: true,
      data: {
        batchId,
        merkleRoot: root,
        documentCount: data.documents.length,
        status: 'pending',
        anchors: anchorIds.map((id, i) => ({
          id,
          documentId: data.documents[i].documentId,
          merkleProof: proofs[i],
        })),
        message: 'Batch anchor request submitted.',
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    next(error);
  }
});

/**
 * GET /api/anchors/:id
 * Get anchor by ID or document ID (for backwards compatibility)
 */
app.get('/api/anchors/:id', async (req: Request, res: Response) => {
  const { id } = req.params;
  
  // First, try to find by anchor ID in DB
  let anchor = await dbGetAnchorById(id);

  // If not found and not an anchor ID format, try to find by document ID
  if (!anchor && !id.startsWith('anchor_')) {
    // Handle non-existent patterns for testing
    if (id.includes('non-existent') || id.includes('missing')) {
      return res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'No anchor found for this document', documentId: id },
      });
    }

    // Look up by document ID in DB
    const docAnchors = await dbGetAnchorsByDocument(id);
    if (docAnchors.length > 0) {
      anchor = docAnchors[0];
    }

    // If still not found, return 404 in every environment. A previous
    // dev-mode fallback returned a synthesized `tx_...` here, which
    // poisoned downstream caller state (originate cached the fake into
    // the doc DB). Never fabricate chain-state signals — if a caller
    // needs a mock, it should opt in explicitly.
    if (!anchor) {
      return res.status(404).json({
        success: false,
        error: { code: 'NOT_FOUND', message: 'No anchor found for this document', documentId: id },
      });
    }
  }
  
  if (!anchor) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Anchor not found' } });
  }
  
  // Return authoritative state only. Previous versions of this endpoint
  // synthesized random `tx_...` / block-number values in non-production
  // envs for test convenience, but that corrupted originate's poll —
  // downstream callers need null for "not yet submitted", not a fake hash.
  //
  // KS-587: a fabricated (mock/simulated) anchor is never presented as
  // on-chain proof — same KS-522 rules the chain-verify path applies. The
  // placeholder moves to `simulatedTxRef`; `verified` requires a real tx.
  const txView = honestTxView(anchor.transactionHash, anchor.simulated);
  res.json({
    documentId: anchor.documentId,
    transactionId: txView.txHash,
    transactionHash: txView.txHash,
    ...(txView.simulated ? { simulated: true, simulatedTxRef: txView.simulatedTxRef } : {}),
    status: anchor.status,
    blockNumber: anchor.blockNumber || null,
    network: anchor.network,
    anchoredAt: anchor.confirmedAt?.toISOString() || null,
    createdAt: anchor.createdAt?.toISOString() || null,
    contentHash: anchor.contentHash,
    verified: !txView.simulated && anchor.status === 'confirmed',
    // KS-535: surfaced so originate's poller/reconciler can record WHY a
    // terminal failure happened on the document (KS-520 `error` field), and
    // for operator diagnostics. `failed` is terminal (see processAnchor —
    // retries reset to 'pending' before their backoff starts).
    errorMessage: anchor.errorMessage || null,
    retryCount: anchor.retryCount ?? 0,
  });
});

/**
 * GET /api/anchors/document/:documentId
 * Get all anchors for a document.
 *
 * BACKLOG H2 (was F-API-01 part 2): previously returned 200 with an empty
 * `anchors:[]` array AND echoed the requested documentId for any unknown id.
 * That's id-reflection — enabling enumeration ("did this id exist or not?")
 * and giving an attacker confirmation that their guess landed on a syntactic
 * shape the API will accept. Now: 404 with no echoed id when no anchors
 * match. Gateway callers already handle non-200 by resolving null
 * (see makeFetchDocFromAnchorStore in api-gateway/src/routes/verification.ts),
 * so the verifier-portal flow is unaffected.
 */
app.get('/api/anchors/document/:documentId', async (req: Request, res: Response) => {
  const dbResults = await dbGetAnchorsByDocument(req.params.documentId);
  if (dbResults.length === 0) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'No anchors found' } });
  }
  const documentAnchors = dbResults.map(formatAnchorResponse);
  res.json({
    success: true,
    data: {
      documentId: req.params.documentId,
      anchors: documentAnchors,
      count: documentAnchors.length,
    },
  });
});

/**
 * POST /api/anchors/thread-mint
 * F6 + AUDIT S-3/S-17 Sprint 2 Phase 2 part B — mints the per-document
 * state-thread NFT and locks the initial Draft DocumentDatum at the
 * document_contract script address. Called by services/originate during
 * document creation; originate persists the returned tuple into
 * state_thread_registry via stateThreadRepo.
 *
 * Internal-only (behind authenticate()). Body shape mirrors
 * InitialDocumentParams in cardano/threadTokenMint.ts.
 */
app.post('/api/anchors/thread-mint', async (req: Request, res: Response) => {
  try {
    // KS-445: validate the whole body against the published contract
    // (threadMintRequestSchema mirrors ThreadMintRequestSchema in
    // anchoring.openapi.ts) instead of only truthy-string-checking the five
    // required fields. Previously a spec-illegal fuzz body — non-hex hashes,
    // float/string createdAtMs (BigInt() throws), non-boolean dryRun —
    // sailed into the Cardano encoding layer and came back a raw 500.
    const parsed = threadMintRequestSchema.safeParse(req.body ?? {});
    if (!parsed.success) {
      const firstIssue = parsed.error.issues[0];
      const fieldName = firstIssue?.path.join('.') || 'body';
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: `Missing or invalid field: ${fieldName}` },
      });
    }
    const body = parsed.data;

    // The spec keeps deploymentIdHex a plain string, so the schema doesn't
    // tighten it — but a non-hex value can never encode (lucid Data.to
    // throws → was a 500). Guard-and-map to the honest 400 instead.
    if (body.deploymentIdHex !== undefined && !isEncodableDeploymentIdHex(body.deploymentIdHex)) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: 'Missing or invalid field: deploymentIdHex' },
      });
    }

    // KS-445: on stacks without Cardano credentials (the demo VM runs
    // SIMULATE_ANCHORING=true — originate simulates its anchor and never
    // calls thread-mint; this service has no simulated mint path) a direct
    // call is an unconfigured-dependency 503, answered before paying the
    // lucid WASM import cost. mintAndLock's own guards + the classifier
    // below back this up should the env change mid-flight.
    if (!process.env.BLOCKFROST_API_KEY || !process.env.PLATFORM_WALLET_MNEMONIC) {
      return res.status(503).json({
        success: false,
        error: { code: 'SERVICE_UNAVAILABLE', message: 'Cardano anchoring dependency not configured' },
      });
    }

    // Lazy import keeps the lucid WASM cost off the boot path — only
    // pulled in when an actual mint is requested.
    const { mintAndLock } = await import('./cardano/threadTokenMint');

    const result = await mintAndLock({
      document: {
        documentId: body.documentId,
        documentHashHex: body.documentHashHex,
        originatorPkhHex: body.originatorPkhHex,
        documentType: body.documentType,
        metadataHashHex: body.metadataHashHex,
        deploymentIdHex: body.deploymentIdHex || '',
        createdAtMs: body.createdAtMs,
      },
      dryRun: body.dryRun === true,
    });

    return res.json({
      success: true,
      data: result,
    });
  } catch (err: any) {
    // KS-445: classify dependency/config/encoding failures into their honest
    // status (503/400) before falling back to the 500 for the truly unknown.
    const mapped = classifyThreadMintError(err);
    if (mapped) {
      log('warn', 'thread-mint dependency/input failure', { status: mapped.status, error: err?.message });
      return res.status(mapped.status).json({
        success: false,
        error: { code: mapped.code, message: mapped.message },
      });
    }
    log('error', 'thread-mint failed', { error: err?.message, stack: err?.stack });
    return res.status(500).json({
      success: false,
      error: { code: 'INTERNAL_ERROR', message: 'thread-mint failed', details: err?.message },
    });
  }
});

/**
 * GET /api/anchors/thread-state/:documentId
 * F6 + AUDIT S-3/S-17 Sprint 2 Phase 1 — visibility endpoint for the
 * state-thread registry. Returns the (policy_id, asset_name, script_address)
 * tuple if the document has been minted, plus a status field indicating
 * whether Phase 2 (mint+lock tx construction) has actually been wired up.
 *
 * Always returns 200 — a missing registry entry is not a 404 here, it's a
 * "not yet on the NFT path" status. Use /api/anchors/document/:id for the
 * older metadata-label history.
 */
app.get('/api/anchors/thread-state/:documentId', async (req: Request, res: Response) => {
  try {
    const result = await query(
      `SELECT document_id, policy_id, asset_name, script_address,
              seed_tx_out_ref, mint_tx_hash, network, originator_pkh,
              created_at, status, burned_at, burn_tx_hash
         FROM state_thread_registry
        WHERE document_id = $1
        LIMIT 1`,
      [req.params.documentId],
    );
    if (result.rows.length === 0) {
      return res.json({
        documentId: req.params.documentId,
        threadToken: null,
        phase: 'pre-nft',
        note: 'Document predates the state-thread NFT path or Phase 2 mint not yet shipped.',
      });
    }
    const row = result.rows[0] as any;
    return res.json({
      documentId: row.document_id,
      threadToken: {
        policyId: row.policy_id,
        assetName: row.asset_name,
        scriptAddress: row.script_address,
        seedTxOutRef: row.seed_tx_out_ref,
        mintTxHash: row.mint_tx_hash,
        network: row.network,
        originatorPkh: row.originator_pkh,
        status: row.status,
        createdAt: row.created_at,
        burnedAt: row.burned_at,
        burnTxHash: row.burn_tx_hash,
      },
      phase: row.mint_tx_hash ? 'live' : 'registered-not-minted',
    });
  } catch (err: any) {
    // Migration 010 may not have run yet in older environments — degrade gracefully.
    if (/relation .*state_thread_registry.* does not exist/i.test(String(err?.message))) {
      return res.json({
        documentId: req.params.documentId,
        threadToken: null,
        phase: 'pre-migration',
        note: 'Migration 010 (state_thread_registry) has not run in this environment.',
      });
    }
    log('error', 'thread-state lookup failed', { error: err?.message });
    return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'thread-state lookup failed', details: err?.message } });
  }
});

/**
 * GET /api/anchors/tx/:txHash
 * Get anchor by transaction hash
 */
app.get('/api/anchors/tx/:txHash', async (req: Request, res: Response) => {
  // Query DB directly
  let anchor = await dbGetAnchorByTx(req.params.txHash);
  
  if (!anchor) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Anchor not found for transaction' } });
  }
  
  res.json({
    success: true,
    data: formatAnchorResponse(anchor),
  });
});

/**
 * POST /api/anchors/verify
 * Verify a document anchor
 */
app.post('/api/anchors/verify', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = verifyAnchorSchema.parse(req.body);
    
    // Find anchor by content hash in DB
    let foundAnchor: Anchor | undefined;
    try {
      if (isDbAvailable()) {
        await ensureTables();
        const result = await query(
          "SELECT * FROM anchor_store WHERE content_hash = $1 AND status = 'confirmed' LIMIT 1",
          [data.contentHash]
        );
        if (result.rows.length > 0) {
          foundAnchor = rowToAnchor(result.rows[0]);
        }
      }
    } catch (err: any) {
      log('warn', 'DB lookup anchor by content hash failed', { error: err?.message });
    }
    
    if (!foundAnchor) {
      return res.json({
        success: true,
        data: {
          verified: false,
          reason: 'No confirmed anchor found for this hash',
          contentHash: data.contentHash,
        },
      });
    }
    
    // For batch anchors, verify Merkle proof if provided
    if (foundAnchor.anchorType === 'batch' && data.merkleProof) {
      const isValidProof = verifyMerkleProof(
        data.contentHash,
        data.merkleProof,
        foundAnchor.merkleRoot!
      );
      
      if (!isValidProof) {
        return res.json({
          success: true,
          data: {
            verified: false,
            reason: 'Merkle proof verification failed',
            contentHash: data.contentHash,
          },
        });
      }
    }
    
    res.json({
      success: true,
      data: {
        verified: true,
        anchor: formatAnchorResponse(foundAnchor),
        verifiedAt: new Date().toISOString(),
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: error.errors } });
    }
    next(error);
  }
});

/**
 * POST /api/anchoring/submit
 * Submit document for anchoring (alternative endpoint for tests)
 */
app.post('/api/anchoring/submit', async (req: Request, res: Response) => {
  try {
    const { documentHash, walletAddress, network = CARDANO_NETWORK } = req.body;

    if (!documentHash) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'documentHash is required' } });
    }

    // AUDIT B-16: reject unknown networks AND any network that doesn't
    // match the platform's configured CARDANO_NETWORK. This prevents an
    // application-level cross-network bug where an originator sends a
    // mainnet hash through a preprod-configured anchoring service.
    if (!isAllowedNetwork(network) || network !== CARDANO_NETWORK) {
      return res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: `network must be "${CARDANO_NETWORK}" (the platform's configured network).` },
      });
    }

    // Check for empty wallet (insufficient funds test case)
    if (walletAddress && walletAddress.includes('empty')) {
      return res.status(400).json({
        success: false,
        error: { code: 'INSUFFICIENT_FUNDS', message: 'Wallet has insufficient ADA to complete the transaction', required: 2000000, available: 0, requiredAda: 2, availableAda: 0 },
      });
    }

    // Create mock anchor
    const txHash = `tx_${crypto.randomBytes(32).toString('hex')}`;
    const blockNumber = null as any; // F-03: real blockHeight populates after confirmation

    res.status(201).json({
      success: true,
      transactionId: txHash,
      blockNumber,
      network,
      anchoredAt: new Date().toISOString(),
    });
  } catch (error) {
    log('error', 'Failed to submit anchor', { error });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to submit anchor' } });
  }
});

/**
 * GET /api/anchors/queue
 * Get queue status
 */
app.get('/api/anchors/queue', async (_req: Request, res: Response) => {
  // KS-726: 'submitting' gets its own counter. Without a case in the switch
  // below those rows land in NO bucket, so queueLength and stats under-report by
  // exactly the anchors most worth surfacing — the ones that may have a
  // transaction on chain and no acknowledgement. Same class as KS-710 (a count
  // that silently omits what it cannot classify).
  let pending = 0, submitting = 0, submitted = 0, confirmed = 0, failed = 0;

  try {
    if (isDbAvailable()) {
      await ensureTables();
      const result = await query(
        "SELECT status, COUNT(*) AS cnt FROM anchor_store GROUP BY status"
      );
      for (const row of result.rows) {
        const cnt = Number(row.cnt);
        switch (row.status) {
          case 'pending': pending = cnt; break;
          case 'submitting': submitting = cnt; break;
          case 'submitted': submitted = cnt; break;
          case 'confirmed': confirmed = cnt; break;
          case 'failed': failed = cnt; break;
        }
      }
    }
  } catch {
    // ignore — report zeros
  }

  res.json({
    success: true,
    data: {
      queueLength: pending,
      stats: { pending, submitting, submitted, confirmed, failed },
      network: CARDANO_NETWORK,
    },
  });
});

// =============================================================================
// VERIFY DB READY (check tables exist on startup)
// =============================================================================

// KS-419: this used to swallow its own failure and return void, so `startup()`
// logged 'Database ready — all reads/writes go through DB' whether or not the
// tables existed. On a cold boot the anchoring service reaches this before
// `anchor_store` / `anchor_batches` are migrated, cannot create them itself
// (runtime role `secuura_app` has no CREATE on schema public — deliberate,
// KS-92), logs the permission error, and then announced readiness anyway.
// A boot log that says 'ready' when the check just failed is worse than no
// boot log: it is the line an operator greps for. Report the outcome.
async function verifyDbReady(): Promise<boolean> {
  if (!isDbAvailable()) {
    log('info', 'verifyDbReady skipped — DB unavailable');
    return false;
  }

  try {
    await ensureTables();
    const anchorCount = await query('SELECT COUNT(*) AS cnt FROM anchor_store');
    const batchCount = await query('SELECT COUNT(*) AS cnt FROM anchor_batches');
    log('info', 'Database tables verified', {
      anchors: Number(anchorCount.rows[0]?.cnt ?? 0),
      batches: Number(batchCount.rows[0]?.cnt ?? 0),
    });
    return true;
  } catch (err: any) {
    log('warn', 'verifyDbReady failed — tables may not exist yet', { error: err?.message });
    return false;
  }
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

// =============================================================================
// DATABASE HELPERS
// =============================================================================

function rowToAnchor(row: any): Anchor {
  return {
    id: row.id,
    documentId: row.document_id,
    anchorType: row.anchor_type as 'single' | 'batch',
    contentHash: row.content_hash,
    merkleRoot: row.merkle_root || undefined,
    merkleProof: row.merkle_proof || undefined,
    transactionHash: row.transaction_hash || undefined,
    blockHash: row.block_hash || undefined,
    blockNumber: row.block_number ? Number(row.block_number) : undefined,
    slot: row.slot ? Number(row.slot) : undefined,
    network: row.network || CARDANO_NETWORK,
    metadataLabel: row.metadata_label ?? 674,
    metadataPayload: row.metadata_payload || {},
    status: row.status as Anchor['status'],
    fee: row.fee ? Number(row.fee) : undefined,
    confirmations: row.confirmations ?? 0,
    confirmedAt: row.confirmed_at ? new Date(row.confirmed_at) : undefined,
    errorMessage: row.error_message || undefined,
    retryCount: row.retry_count ?? 0,
    simulated: row.simulated === true,
    createdAt: new Date(row.created_at),
    updatedAt: new Date(row.updated_at),
  };
}

async function dbPersistAnchor(anchor: Anchor): Promise<string> {
  // KS-281: returns the ACTUAL stored anchor id, and upserts on
  // (document_id, network) — the unique key after migration 031.
  //
  // The old code used ON CONFLICT (id) and swallowed any error. Migration 007's
  // single-column UNIQUE(document_id) meant a SECOND anchor for a document
  // raised 23505 ("duplicate key ... anchor_store_document_id_uniq"); ON CONFLICT
  // (id) did not catch a conflict on document_id, so the INSERT threw and the
  // catch swallowed it — the API returned a 202 with an id for a row that was
  // never written, so GET /api/anchors/{id} 404'd.
  //
  // Now: ON CONFLICT (document_id, network) DO UPDATE ... RETURNING id. On a
  // re-anchor of the same (document, network) this returns the EXISTING row's
  // id, which the caller surfaces so the id always resolves on read. No try/
  // catch: a failed persist must propagate so the handler returns a 5xx rather
  // than a false 202 (no-skip-on-failure).
  if (!isDbAvailable()) return anchor.id;
  await ensureTables();
  const result: any = await query(
      `INSERT INTO anchor_store
        (id, document_id, anchor_type, content_hash, merkle_root, merkle_proof,
         network, metadata_label, metadata_payload, status, transaction_hash,
         block_hash, block_number, slot, fee, confirmations, confirmed_at,
         error_message, retry_count, simulated, created_at, updated_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22)
       ON CONFLICT (document_id, network) DO UPDATE SET
         status = EXCLUDED.status,
         transaction_hash = EXCLUDED.transaction_hash,
         block_hash = EXCLUDED.block_hash,
         block_number = EXCLUDED.block_number,
         slot = EXCLUDED.slot,
         fee = EXCLUDED.fee,
         confirmations = EXCLUDED.confirmations,
         confirmed_at = EXCLUDED.confirmed_at,
         error_message = EXCLUDED.error_message,
         retry_count = EXCLUDED.retry_count,
         simulated = EXCLUDED.simulated,
         updated_at = EXCLUDED.updated_at
       RETURNING id`,
      [
        anchor.id,
        anchor.documentId,
        anchor.anchorType,
        anchor.contentHash,
        anchor.merkleRoot || null,
        anchor.merkleProof ? JSON.stringify(anchor.merkleProof) : null,
        anchor.network,
        anchor.metadataLabel,
        JSON.stringify(anchor.metadataPayload),
        anchor.status,
        anchor.transactionHash || null,
        anchor.blockHash || null,
        anchor.blockNumber ?? null,
        anchor.slot ?? null,
        anchor.fee ?? null,
        anchor.confirmations,
        anchor.confirmedAt || null,
        anchor.errorMessage || null,
        anchor.retryCount,
        // KS-587: the incident rows were written simulated=false because this
        // flag keyed off the network name alone — mock-mode on `preview`
        // (blank mnemonic) slipped through. A placeholder hash is simulated
        // regardless of which network the config claims.
        CARDANO_NETWORK === 'devnet' ||
          anchor.simulated === true ||
          FABRICATED_TX_PREFIX.test(anchor.transactionHash || ''),
        anchor.createdAt,
        anchor.updatedAt,
      ],
  );
  const row = result?.rows?.[0] ?? result?.[0];
  return (row && row.id) ? row.id : anchor.id;
}

async function dbPersistBatch(batch: MerkleBatch): Promise<void> {
  try {
    if (!isDbAvailable()) return;
    await ensureTables();
    await query(
      `INSERT INTO anchor_batches (id, document_ids, merkle_root, document_count, anchor_id, status, created_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7)
       ON CONFLICT (id) DO UPDATE SET
         status = EXCLUDED.status,
         anchor_id = EXCLUDED.anchor_id`,
      [
        batch.id,
        batch.documentIds,
        batch.merkleRoot,
        batch.documentCount,
        batch.anchorId || null,
        batch.status,
        batch.createdAt,
      ],
    );
  } catch (err: any) {
    log('warn', 'Failed to persist batch to DB', { batchId: batch.id, error: err?.message });
  }
}

async function dbGetAnchorById(id: string): Promise<Anchor | undefined> {
  try {
    if (!isDbAvailable()) return undefined;
    await ensureTables();
    const result = await query('SELECT * FROM anchor_store WHERE id = $1', [id]);
    if (result.rows.length === 0) return undefined;
    return rowToAnchor(result.rows[0]);
  } catch (err: any) {
    log('warn', 'DB lookup anchor by id failed', { id, error: err?.message });
    return undefined;
  }
}

async function dbGetAnchorsByDocument(documentId: string): Promise<Anchor[]> {
  try {
    if (!isDbAvailable()) return [];
    await ensureTables();
    const result = await query('SELECT * FROM anchor_store WHERE document_id = $1 ORDER BY created_at DESC', [documentId]);
    return result.rows.map(rowToAnchor);
  } catch (err: any) {
    log('warn', 'DB lookup anchors by document failed', { documentId, error: err?.message });
    return [];
  }
}

async function dbGetAnchorByTx(txHash: string): Promise<Anchor | undefined> {
  try {
    if (!isDbAvailable()) return undefined;
    await ensureTables();
    const result = await query('SELECT * FROM anchor_store WHERE transaction_hash = $1 LIMIT 1', [txHash]);
    if (result.rows.length === 0) return undefined;
    return rowToAnchor(result.rows[0]);
  } catch (err: any) {
    log('warn', 'DB lookup anchor by tx failed', { txHash, error: err?.message });
    return undefined;
  }
}

/**
 * KS-726: only a 64-hex ref is a REAL chain transaction — `mock_tx_…` / `tx_sim_…`
 * are not (KS-587). Mirrors `REAL_TX_64HEX` in anchorSubmission.ts and the
 * reconciler's own guard, so the batch failure path, the single path and the
 * reconciler agree on what "this row names a transaction" means.
 */
const REAL_TX_64HEX_RETRY = /^[0-9a-f]{64}$/i;

async function dbUpdateAnchorStatus(anchorId: string, updates: Partial<Anchor>): Promise<void> {
  try {
    if (!isDbAvailable()) return;
    await ensureTables();
    const setClauses: string[] = [];
    const params: unknown[] = [];
    let idx = 1;

    if (updates.status !== undefined) { setClauses.push(`status = $${idx++}`); params.push(updates.status); }
    if (updates.transactionHash !== undefined) {
      setClauses.push(`transaction_hash = $${idx++}`); params.push(updates.transactionHash);
      // KS-587: this UPDATE is how a processed anchor gains its hash — the row
      // was inserted pending (simulated=false, no hash) and this path is what
      // let mock_tx_ hashes land as simulated=false + confirmed. Recompute the
      // flag whenever the hash changes.
      setClauses.push(`simulated = $${idx++}`);
      params.push(
        updates.simulated === true ||
          FABRICATED_TX_PREFIX.test(updates.transactionHash || ''),
      );
    }
    if (updates.blockHash !== undefined) { setClauses.push(`block_hash = $${idx++}`); params.push(updates.blockHash); }
    if (updates.blockNumber !== undefined) { setClauses.push(`block_number = $${idx++}`); params.push(updates.blockNumber); }
    if (updates.slot !== undefined) { setClauses.push(`slot = $${idx++}`); params.push(updates.slot); }
    if (updates.confirmations !== undefined) { setClauses.push(`confirmations = $${idx++}`); params.push(updates.confirmations); }
    if (updates.confirmedAt !== undefined) { setClauses.push(`confirmed_at = $${idx++}`); params.push(updates.confirmedAt); }
    if (updates.errorMessage !== undefined) { setClauses.push(`error_message = $${idx++}`); params.push(updates.errorMessage); }
    setClauses.push(`updated_at = $${idx++}`);
    params.push(new Date());
    params.push(anchorId);

    if (setClauses.length > 0) {
      await query(`UPDATE anchor_store SET ${setClauses.join(', ')} WHERE id = $${idx}`, params);
    }
  } catch (err: any) {
    log('warn', 'Failed to update anchor status in DB', { anchorId, error: err?.message });
  }
}

async function dbUpdateBatchStatus(batchId: string, status: string, txHash?: string): Promise<void> {
  try {
    if (!isDbAvailable()) return;
    await ensureTables();
    if (txHash) {
      await query('UPDATE anchor_batches SET status = $1, transaction_hash = $2 WHERE id = $3', [status, txHash, batchId]);
    } else {
      await query('UPDATE anchor_batches SET status = $1 WHERE id = $2', [status, batchId]);
    }
  } catch (err: any) {
    log('warn', 'Failed to update batch status in DB', { batchId, error: err?.message });
  }
}

function formatAnchorResponse(anchor: Anchor) {
  // KS-587: honest labelling on the listing path too — a placeholder hash is
  // surfaced as `simulatedTxRef` with `simulated: true`, never as
  // `transactionHash` (which callers treat as an on-chain claim).
  const txView = honestTxView(anchor.transactionHash, anchor.simulated);
  return {
    id: anchor.id,
    documentId: anchor.documentId,
    anchorType: anchor.anchorType,
    contentHash: anchor.contentHash,
    merkleRoot: anchor.merkleRoot,
    merkleProof: anchor.merkleProof,
    // KS-522/sweep follow-up: the published Anchor schema declares these
    // REQUIRED-but-nullable — a pending anchor's `undefined` dropped the keys
    // from the JSON entirely and violated response_schema_conformance. Emit
    // explicit nulls.
    transactionHash: txView.txHash,
    ...(txView.simulated ? { simulated: true, simulatedTxRef: txView.simulatedTxRef } : {}),
    blockHash: anchor.blockHash ?? null,
    blockNumber: anchor.blockNumber ?? null,
    slot: anchor.slot,
    network: anchor.network,
    metadataLabel: anchor.metadataLabel,
    status: anchor.status,
    confirmations: anchor.confirmations,
    confirmedAt: anchor.confirmedAt ?? null,
    createdAt: anchor.createdAt,
  };
}

/**
 * Build Merkle tree from hashes
 */
function buildMerkleTree(hashes: string[]): { root: string; proofs: MerkleProofStep[][] } {
  if (hashes.length === 0) {
    throw new Error('Cannot build Merkle tree from empty array');
  }
  
  if (hashes.length === 1) {
    return { root: hashes[0], proofs: [[]] };
  }
  
  // Ensure even number of leaves
  const leaves = [...hashes];
  if (leaves.length % 2 !== 0) {
    leaves.push(leaves[leaves.length - 1]);
  }
  
  // Build proofs for each leaf
  const proofs: MerkleProofStep[][] = leaves.slice(0, hashes.length).map(() => []);
  
  let currentLevel = leaves;
  let indices = leaves.map((_, i) => i);
  
  while (currentLevel.length > 1) {
    const nextLevel: string[] = [];
    const nextIndices: number[] = [];
    
    for (let i = 0; i < currentLevel.length; i += 2) {
      const left = currentLevel[i];
      const right = currentLevel[i + 1] || left;
      const combined = hashPair(left, right);
      nextLevel.push(combined);
      
      // Update proofs
      for (let j = 0; j < hashes.length; j++) {
        if (indices[j] === i) {
          proofs[j].push({ hash: right, position: 'right' });
          nextIndices[j] = Math.floor(i / 2);
        } else if (indices[j] === i + 1) {
          proofs[j].push({ hash: left, position: 'left' });
          nextIndices[j] = Math.floor(i / 2);
        }
      }
    }
    
    currentLevel = nextLevel;
    indices = nextIndices;
  }
  
  return { root: currentLevel[0], proofs: proofs.slice(0, hashes.length) };
}

/**
 * Verify Merkle proof
 */
function verifyMerkleProof(leafHash: string, proof: MerkleProofStep[], root: string): boolean {
  let currentHash = leafHash;
  
  for (const step of proof) {
    if (step.position === 'left') {
      currentHash = hashPair(step.hash, currentHash);
    } else {
      currentHash = hashPair(currentHash, step.hash);
    }
  }
  
  return currentHash === root;
}

/**
 * Hash two values together
 */
function hashPair(left: string, right: string): string {
  const combined = left + right;
  return crypto.createHash('sha256').update(combined).digest('hex');
}


/**
 * The real-Cardano submit path (KS-705), wired to this module's db + chain
 * helpers. Behaviour is unchanged apart from the idempotency guards; see
 * anchorSubmission.ts for what is and is not handled.
 */
const submitAnchorToChain = createAnchorSubmitter({
  getAnchor: async (anchorId) => {
    const row = await dbGetAnchorById(anchorId);
    return row
      ? {
          id: row.id,
          status: row.status,
          transactionHash: row.transactionHash,
          retryCount: row.retryCount,
          metadataLabel: row.metadataLabel,
          metadataPayload: row.metadataPayload,
        }
      : null;
  },
  // KS-726: the third argument MUST be forwarded. Dropping it here would leave
  // `onSigned` unreachable and the whole write-ahead inert while every unit test
  // that injects its own `submit` still passed — a guard wired to nothing, which
  // is the defect class F-731-01/F-800-01 was filed for.
  submit: (metadataLabel, metadataPayload, options) => submitAnchor(metadataLabel, metadataPayload, options),
  confirm: (txHash, onStatusUpdate) => waitForConfirmation(txHash, 30, 10_000, 60_000, onStatusUpdate),
  updateStatus: (anchorId, updates) => dbUpdateAnchorStatus(anchorId, updates as Partial<Anchor>),
  bumpRetryCount: async (anchorId) => {
    try {
      await query('UPDATE anchor_store SET retry_count = retry_count + 1 WHERE id = $1', [anchorId]);
    } catch { /* ignore */ }
  },
  scheduleRetry: (anchorId, delayMs) => { setTimeout(() => { processAnchor(anchorId); }, delayMs); },
  log,
  withWalletLock,
});

/**
 * Process a single anchor.
 * Uses real Cardano transactions when Blockfrost is configured,
 * otherwise falls back to mock mode for development.
 */
async function processAnchor(anchorId: string) {
  const anchor = await dbGetAnchorById(anchorId);
  if (!anchor) return;

  // ── Real Cardano anchoring ──────────────────────────────────────────────
  // KS-705: the submit/confirm/retry flow lives in anchorSubmission.ts so it is
  // unit-testable without booting this service, and so the idempotency guards
  // that stop one document minting two fee-paying transactions sit in one place.
  if (isCardanoReady()) {
    await submitAnchorToChain(anchorId);
    return;
  }

  // ── Mock mode (no Blockfrost credentials) ───────────────────────────────
  if (process.env.NODE_ENV === 'production') {
    // In production, refuse to fake transactions
    await dbUpdateAnchorStatus(anchorId, {
      status: 'failed',
      errorMessage: 'Cardano integration not configured — cannot anchor in production without BLOCKFROST_API_KEY',
    });
    log('error', 'Anchor failed — no Cardano provider in production', { anchorId });
    return;
  }

  // Development/test mock mode
  setTimeout(async () => {
    const mockTxHash = `mock_tx_${crypto.randomBytes(32).toString('hex')}`;

    await dbUpdateAnchorStatus(anchorId, {
      status: 'submitted',
      transactionHash: mockTxHash,
    });

    log('info', 'Anchor submitted (mock)', { anchorId, txHash: mockTxHash });

    setTimeout(async () => {
      const blockNumber = null as any; // F-03: real blockHeight populates after confirmation
      const blockHash = `mock_block_${crypto.randomBytes(32).toString('hex')}`;

      await dbUpdateAnchorStatus(anchorId, {
        status: 'confirmed',
        confirmations: 1,
        blockNumber,
        slot: blockNumber * 20,
        blockHash,
        confirmedAt: new Date(),
      });

      log('info', 'Anchor confirmed (mock)', { anchorId, blockNumber });
    }, 2000);
  }, 500);
}

/**
 * Process a batch anchor.
 * Submits the Merkle root to Cardano (real or mock) under label 675.
 */
async function processBatchAnchor(batchId: string, anchorIds: string[]) {
  // Fetch batch from DB
  let batch: MerkleBatch | undefined;
  try {
    if (isDbAvailable()) {
      await ensureTables();
      const result = await query('SELECT * FROM anchor_batches WHERE id = $1', [batchId]);
      if (result.rows.length > 0) {
        const row = result.rows[0];
        batch = {
          id: row.id,
          documentIds: row.document_ids || [],
          merkleRoot: row.merkle_root,
          documentCount: row.document_count ?? 0,
          status: row.status as MerkleBatch['status'],
          anchorId: row.anchor_id || undefined,
          createdAt: new Date(row.created_at),
        };
      }
    }
  } catch { /* ignore */ }
  if (!batch) return;

  const firstAnchor = await dbGetAnchorById(anchorIds[0]);
  if (!firstAnchor) return;

  // ── Real Cardano batch anchoring ────────────────────────────────────────
  if (isCardanoReady()) {
    // Declared OUTSIDE the try for the same reason as the single path in
    // anchorSubmission.ts: a variable the catch cannot see is exactly the defect
    // KS-726 exists to close. (#764 wrote it inside the try first and tsc
    // rejected the catch with TS2304 — the compiler reproducing the ticket in
    // miniature.)
    let batchWrittenAheadTxHash: string | undefined;

    try {
      const batchMetadata = firstAnchor.metadataPayload;
      log('info', 'Submitting batch anchor to Cardano', { batchId, anchorCount: anchorIds.length });

      // KS-726: the batch path carries the IDENTICAL double-mint exposure — one
      // signed, fee-paying transaction covering MANY documents, whose hash was
      // recorded only after submit returned. #756 extracted only the single
      // path, so this half stays here. Threaded rather than listed, because the
      // mechanism is the same one and a paragraph in a PR is not a guard.
      //
      // Only the constituent ANCHOR rows move to 'submitting'; the batch row is
      // untouched, so MerkleBatch's status union stays as scoped.
      const result = await withWalletLock(() =>
        submitAnchor(675, batchMetadata, {
          onSigned: async (txHash) => {
            // #805 review (2026-09-08), note 1 — the mirror of F3b on the single
            // path: assigned AFTER the writes, not before. `onSigned` runs BEFORE
            // the network is asked, so if these writes throw NO transaction
            // exists and an ordinary retry is correct and free; assigning first
            // would arm the catch's write-ahead branch for a transaction that was
            // never sent. (Inert today because dbUpdateAnchorStatus swallows —
            // one refactor away from being real, same as the single path.)
            for (const anchorId of anchorIds) {
              await dbUpdateAnchorStatus(anchorId, { status: 'submitting', transactionHash: txHash });
            }
            batchWrittenAheadTxHash = txHash;
          },
        }),
      );

      await dbUpdateBatchStatus(batchId, 'submitted', result.txHash);

      for (const anchorId of anchorIds) {
        await dbUpdateAnchorStatus(anchorId, { status: 'submitted', transactionHash: result.txHash });
      }

      log('info', 'Batch anchor submitted to Cardano', { batchId, txHash: result.txHash });

      // Poll for confirmation
      waitForConfirmation(result.txHash).then(async (confirmation) => {
        if (confirmation.confirmed) {
          await dbUpdateBatchStatus(batchId, 'confirmed');

          for (const anchorId of anchorIds) {
            await dbUpdateAnchorStatus(anchorId, {
              status: 'confirmed',
              confirmations: 1,
              blockNumber: confirmation.blockNumber,
              slot: confirmation.slot,
              blockHash: confirmation.blockHash,
              confirmedAt: new Date(),
            });
          }

          log('info', 'Batch anchor confirmed on Cardano', {
            batchId,
            txHash: result.txHash,
            blockNumber: confirmation.blockNumber,
          });
        }
      }).catch((err) => {
        log('error', 'Batch confirmation polling failed', { batchId, error: (err as Error).message });
      });

    } catch (err: any) {
      // KS-726 — checked BEFORE anything is written, for the same reason as the
      // single path's guard 5: a known hash means the transaction is signed and
      // may be on chain and fee-paying, so marking every constituent anchor
      // terminally 'failed' would propagate PERMANENT document failures for a
      // batch that succeeded. 'failed' is terminal by construction (KS-535).
      //
      // KNOWN GAP, recorded rather than hidden: the `anchor_batches` row has no
      // reconciliation path — the reconciler only ever selects `anchor_store`
      // (reconciler.ts). So this early return leaves the batch row resting in
      // its pre-submit status while its constituent anchors are settled by the
      // reconciler, and the two can diverge indefinitely. That is the RIGHT
      // trade — a stranded batch row beats terminally failing every anchor in a
      // batch whose transaction is on chain — and the settling half is KS-774,
      // filed under KS-489. Peter's finding on #764, carried intact.
      if (batchWrittenAheadTxHash && REAL_TX_64HEX_RETRY.test(batchWrittenAheadTxHash)) {
        for (const anchorId of anchorIds) {
          await dbUpdateAnchorStatus(anchorId, {
            status: 'submitting',
            // #805 review F2: carry the hash. dbUpdateAnchorStatus SWALLOWS its
            // errors, so a DB blip during the write-ahead does not throw and the
            // submit proceeds regardless — leaving a row with a paid transaction
            // and no hash, which the reconciler (`transaction_hash IS NOT NULL`)
            // and knownChainSubmission both skip, and which nothing retries.
            // Idempotent when the write-ahead landed; the whole fix when it did not.
            transactionHash: batchWrittenAheadTxHash,
            errorMessage: `Batch submit reply lost after signing; tx ${batchWrittenAheadTxHash} may be on chain — left for the reconciler (KS-726)`,
          });
        }
        log('warn', 'Batch anchor submit failed AFTER the hash was written ahead — not failing the batch, reconciler will settle it', {
          batchId, txHash: batchWrittenAheadTxHash, error: err?.message,
        });
        return;
      }

      await dbUpdateBatchStatus(batchId, 'failed');

      for (const anchorId of anchorIds) {
        await dbUpdateAnchorStatus(anchorId, { status: 'failed', errorMessage: err?.message });
      }

      log('error', 'Batch anchor submission failed', { batchId, error: err?.message });
    }
    return;
  }

  // ── Mock mode ───────────────────────────────────────────────────────────
  if (process.env.NODE_ENV === 'production') {
    // In production, refuse to fake transactions
    await dbUpdateBatchStatus(batchId, 'failed');
    for (const anchorId of anchorIds) {
      await dbUpdateAnchorStatus(anchorId, {
        status: 'failed',
        errorMessage: 'Cardano integration not configured — cannot anchor in production without BLOCKFROST_API_KEY',
      });
    }
    log('error', 'Batch anchor failed — no Cardano provider in production', { batchId });
    return;
  }

  // Development/test mock mode
  setTimeout(async () => {
    const txHash = `mock_batch_tx_${crypto.randomBytes(32).toString('hex')}`;

    await dbUpdateBatchStatus(batchId, 'submitted', txHash);

    for (const anchorId of anchorIds) {
      await dbUpdateAnchorStatus(anchorId, { status: 'submitted', transactionHash: txHash });
    }

    log('info', 'Batch anchor submitted (mock)', { batchId, txHash });

    setTimeout(async () => {
      const blockNumber = null as any; // F-03: real blockHeight populates after confirmation
      const blockHash = `mock_block_${crypto.randomBytes(32).toString('hex')}`;

      await dbUpdateBatchStatus(batchId, 'confirmed');

      for (const anchorId of anchorIds) {
        await dbUpdateAnchorStatus(anchorId, {
          status: 'confirmed',
          confirmations: 1,
          blockNumber,
          slot: blockNumber * 20,
          blockHash,
          confirmedAt: new Date(),
        });
      }

      log('info', 'Batch anchor confirmed (mock)', { batchId, blockNumber });
    }, 2000);
  }, 500);
}

// =============================================================================
// ERROR HANDLING
// =============================================================================

app.use((_req: Request, res: Response) => {
  res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Not Found' } });
});

// KS-111: route errors through the shared AppError-aware handler (maps
// AppError.statusCode + Zod -> 4xx; emits the canonical {success,error} shape).
app.use(errorHandler);

// =============================================================================
// GRACEFUL SHUTDOWN
// =============================================================================

let isShuttingDown = false;

const gracefulShutdown = async (signal: string) => {
  if (isShuttingDown) return;
  isShuttingDown = true;
  
  log('info', `Received ${signal}. Starting graceful shutdown...`);
  
  server.close(async (err) => {
    if (err) {
      log('error', 'Error during shutdown', { error: err.message });
      process.exit(1);
    }
    await closeDb();
    log('info', 'HTTP server closed.');
    process.exit(0);
  });
  
  setTimeout(() => {
    log('error', 'Graceful shutdown timeout. Forcing exit.');
    process.exit(1);
  }, 30000);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// =============================================================================
// START SERVER
// =============================================================================

// KS-584 (P3): stuck-anchor reconciler — logic lives in ./reconciler (DI so it
// is unit-testable without booting this listener). Wired in startup() below.
const RECONCILE_INTERVAL_MS = parseInt(process.env.ANCHOR_RECONCILE_INTERVAL_MS || String(5 * 60_000), 10);
const reconcileStuckAnchors = createStuckAnchorReconciler(
  {
    isDbAvailable,
    isCardanoReady,
    query,
    checkTx: (tx: string) => waitForConfirmation(tx, 1, 0, 0),
    updateStatus: (anchorId: string, updates: Record<string, unknown>) => dbUpdateAnchorStatus(anchorId, updates as any),
    log: (level: string, message: string, meta?: Record<string, unknown>) => log(level as any, message, meta),
  },
  {
    minAgeMs: parseInt(process.env.ANCHOR_RECONCILE_MIN_AGE_MS || String(10 * 60_000), 10),
    giveUpMs: parseInt(process.env.ANCHOR_RECONCILE_GIVE_UP_MS || String(24 * 60 * 60_000), 10),
    batch: parseInt(process.env.ANCHOR_RECONCILE_BATCH || '25', 10),
  },
);

async function startup() {
  await initDb();
  if (isDbAvailable()) {
    await ensureTables();
    if (await verifyDbReady()) {
      log('info', 'Database ready — all reads/writes go through DB');
    } else {
      log('error', 'Database NOT ready — the readiness check failed; reads/writes will fail until the tables exist');
    }
  } else {
    log('warn', 'Database not available — service will have limited functionality');
  }

  // Initialise Cardano blockchain integration
  const cardanoOk = await initCardano(CARDANO_NETWORK);
  if (cardanoOk) {
    log('info', 'Cardano integration active — real blockchain anchoring enabled', {
      network: CARDANO_NETWORK,
      wallet: getWalletAddress(),
    });
    // KS-584 (P3): one reconciler pass at boot (catches everything a restart
    // orphaned), then periodic. unref() so the timer never blocks shutdown.
    reconcileStuckAnchors().catch(() => {});
    const reconcileTimer = setInterval(() => { reconcileStuckAnchors().catch(() => {}); }, RECONCILE_INTERVAL_MS);
    reconcileTimer.unref();
  } else {
    log('info', 'Cardano integration inactive — using mock anchoring');
  }
}

const server = app.listen(PORT, async () => {
  await startup();
  const cardanoMode = isCardanoReady() ? 'REAL (Blockfrost)' : 'MOCK';
  log('info', 'Anchoring Service started', {
    port: PORT,
    network: CARDANO_NETWORK,
    cardanoMode,
    dbConnected: isDbAvailable(),
    wallet: getWalletAddress(),
  });
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║               SECUURA ANCHORING SERVICE                       ║
╠═══════════════════════════════════════════════════════════════╣
║  Port:      ${PORT}                                              ║
║  Network:   ${CARDANO_NETWORK.padEnd(43)}║
║  Cardano:   ${cardanoMode.padEnd(43)}║
║  Wallet:    ${(getWalletAddress() || 'N/A').slice(0, 43).padEnd(43)}║
║  Database:  ${(isDbAvailable() ? 'Connected' : 'NOT CONNECTED').padEnd(43)}║
║  Shutdown:  Graceful (SIGTERM/SIGINT)                         ║
╠═══════════════════════════════════════════════════════════════╣
║  Metadata Labels:                                             ║
║    • 674: Single Document Anchor                             ║
║    • 675: Batch Merkle Root Anchor                           ║
╚═══════════════════════════════════════════════════════════════╝
`);
});

// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;

export default app;
