// QA drafter probe for #1005 — harness = the seat file lines 16-126 verbatim + hit counter + tier1DocExtra (asserted edits)
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import express from 'express';
import http from 'node:http';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import type { RequestHandler } from 'express';

const REAL_TX = 'a'.repeat(64);
const DOC_ID = 'doc-ks1073';
const CONTENT_HASH = 'b'.repeat(64);

let gateway: Server;
let originate: Server;
let gatewayPort: number;
const realFetch = globalThis.fetch;

/** The blockchain blob the stub originate serves for the current cell. */
let currentBlob: Record<string, unknown> | undefined;
/** The anchoring chain-scan reply for the current cell. `null` = no live hit. */
let liveAnchorReply: Record<string, unknown> | null = null;
/** Tier-2 rows served by the stub anchor store. `null` = tier 2 has nothing. */
let anchorStoreRows: Array<Record<string, unknown>> | null = null;
/** When true the stub originate 404s, so the lookup falls through to tier 2. */
let tier1Absent = false;
/** QA: anchor-store hit counter (the tier witness I-1 asked for) and extra doc-level keys for the tier-1 document. */
let anchorHits = 0;
let tier1DocExtra: Record<string, unknown> = {};
const jsonHead = { 'Content-Type': 'application/json' };

beforeAll(async () => {
  // Stub originate: the first lookup tier. Serves the document whose blockchain
  // blob each cell sets.
  originate = http.createServer((req, res) => {
    if (req.url === `/api/anchors/document/${DOC_ID}`) {
      anchorHits++;
      if (!anchorStoreRows) { res.writeHead(404, jsonHead); res.end('{}'); return; }
      res.writeHead(200, jsonHead);
      res.end(JSON.stringify({ data: { anchors: anchorStoreRows } }));
      return;
    }
    if (req.url === `/api/documents/${DOC_ID}`) {
      if (tier1Absent) { res.writeHead(404, jsonHead); res.end('{}'); return; }
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        id: DOC_ID,
        status: 'anchored',
        contentHash: CONTENT_HASH,
        owner: { id: 'org-1' },
        ...(currentBlob ? { blockchain: currentBlob } : {}),
        ...tier1DocExtra,
      }));
      return;
    }
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end('{}');
  });
  originate.listen(0, '127.0.0.1');
  await new Promise<void>((r) => originate.once('listening', () => r()));
  const originatePort = (originate.address() as AddressInfo).port;

  globalThis.fetch = (async () => (
    liveAnchorReply
      ? { ok: true, status: 200, json: async () => liveAnchorReply, text: async () => '' }
      : { ok: false, status: 404, json: async () => ({}), text: async () => '' }
  )) as never;

  const { createVerificationRoutes } = await import('../routes/verification');
  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });

  const app = express();
  app.use(
    createVerificationRoutes({
      authenticateToken: () => (req, _res, next) => {
        (req as { user?: unknown }).user = {
          userId: 'u1', email: 'u@secuura.local', role: 'ADMIN',
          organizationId: 'org-1', tenantId: 't1', verificationLevel: 'FULL',
        };
        next();
      },
      mockBodyParser,
      query: vi.fn(async () => ({ rows: [] })) as never,
      isDbAvailable: () => false,
      redisService: {
        getPendingDocument: vi.fn(async () => null),
        deletePendingDocument: vi.fn(async () => undefined),
        getAllDocumentTypes: vi.fn(async () => []),
        getAllWorkflowInstances: vi.fn(async () => []),
        getNotificationSettings: vi.fn(async () => ({})),
        getRejectedDocument: vi.fn(async () => null),
        setRejectedDocument: vi.fn(async () => undefined),
        getWorkflowDocumentMapping: vi.fn(async () => null),
        getWorkflowInstance: vi.fn(async () => null),
        setWorkflowInstance: vi.fn(async () => undefined),
      } as never,
      services: { originate: { url: `http://127.0.0.1:${originatePort}` }, anchoring: { url: `http://127.0.0.1:${originatePort}` } } as never,
      log: () => undefined,
      memWorkflowToDocumentMap: new Map(),
      memRejectedDocuments: new Map(),
      dbSaveRejection: vi.fn(async () => undefined),
      ADMIN_ROLES: ['ADMIN', 'admin'],
      enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never,
      createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never,
      meetsVerificationLevel: () => true,
    }),
  );

  gateway = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => gateway.once('listening', () => r()));
  gatewayPort = (gateway.address() as AddressInfo).port;
});

afterAll(async () => {
  globalThis.fetch = realFetch;
  await new Promise<void>((r) => gateway.close(() => r()));
  await new Promise<void>((r) => originate.close(() => r()));
});

// ---- QA DRAFTER PROBE (#1005, never committed): RECORDS each shape; asserts only HTTP 200 and the tier witness ----
import { appendFileSync } from 'node:fs';
const OUT = process.env.QA_OUT as string;
async function drive(id: string, tier: 1 | 2, shape: Record<string, unknown>, opts: { extra?: Record<string, unknown>; live?: Record<string, unknown> | null } = {}) {
  const before = anchorHits;
  if (tier === 1) { currentBlob = shape; tier1Absent = false; anchorStoreRows = null; }
  else { currentBlob = undefined; tier1Absent = true; anchorStoreRows = [{ contentHash: CONTENT_HASH, ...shape }]; }
  tier1DocExtra = opts.extra || {};
  liveAnchorReply = opts.live || null;
  const r = await realFetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
    method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' }, body: JSON.stringify({ purpose: 'test' }),
  });
  const b: any = await r.json();
  const hits = anchorHits - before;
  tier1DocExtra = {}; liveAnchorReply = null;
  appendFileSync(OUT, JSON.stringify({ id, tier, http: r.status, anchorStoreHits: hits, verified: b.verified, confidence: b.verificationConfidence, anchored: b.blockchain?.anchored, source: b.blockchain?.source }) + '\n');
  expect(r.status).toBe(200);
  expect(hits).toBe(tier === 2 ? 1 : 0);   // the tier witness: tier 2 hits the anchor store exactly once; tier 1 never does (negative control)
}
const REAL = 'a'.repeat(64);
describe('QA drafter probe #1005 — legitimate shapes x tier, recorded', () => {
  it('A1 T2 no status, REAL, 4242', () => drive('A1', 2, { transactionHash: REAL, blockNumber: 4242 }));
  it('A2 T2 no status, hash null, height null (the KS-1123 F1 shape)', () => drive('A2', 2, { transactionHash: null, blockNumber: null }));
  it('A3 T2 no status, tx_sim_ hash, 4242', () => drive('A3', 2, { transactionHash: 'tx_sim_' + 'c'.repeat(40), blockNumber: 4242 }));
  it('A4 T2 status null explicit, REAL, 4242', () => drive('A4', 2, { transactionHash: REAL, blockNumber: 4242, status: null }));
  it('A5 T2 no status, REAL, 4242, simulated true', () => drive('A5', 2, { transactionHash: REAL, blockNumber: 4242, simulated: true }));
  it('A6 T2 confirmed, REAL, 4242', () => drive('A6', 2, { transactionHash: REAL, blockNumber: 4242, status: 'confirmed' }));
  it('A7 T2 submitted, REAL, 4242', () => drive('A7', 2, { transactionHash: REAL, blockNumber: 4242, status: 'submitted' }));
  it('A8 T2 pending, hash null, height null', () => drive('A8', 2, { transactionHash: null, blockNumber: null, status: 'pending' }));
  it('A9 T2 failed, REAL, 4242', () => drive('A9', 2, { transactionHash: REAL, blockNumber: 4242, status: 'failed' }));
  it('A10 T2 no status, REAL, snake_case keys', () => drive('A10', 2, { transaction_hash: REAL, block_number: 4242 }));
  it('A11 T2 no status, REAL, blockNumber 0', () => drive('A11', 2, { transactionHash: REAL, blockNumber: 0 }));
  it('A12 T2 no status, REAL, 4242, LIVE chain hit', () => drive('A12', 2, { transactionHash: REAL, blockNumber: 4242 }, { live: { verified: true, txHash: REAL, blockNumber: 4242, confirmedAt: '2026-09-16T00:00:00Z' } }));
  it('B1 T1 legacy statusless {txHash, blockHeight, anchoredAt}', () => drive('B1', 1, { txHash: REAL, blockHeight: 4242, anchoredAt: '2026-01-01T00:00:00Z' }));
  it('B2 T1 status null explicit, REAL', () => drive('B2', 1, { txHash: REAL, blockHeight: 4242, status: null }));
  it('B3 T1 statusless, REAL, simulated true', () => drive('B3', 1, { txHash: REAL, blockHeight: 4242, simulated: true }));
  it('B4 T1 statusless, tx_sim_', () => drive('B4', 1, { txHash: 'tx_sim_' + 'c'.repeat(40), blockHeight: 4242 }));
  it('B5 T1 confirmed, REAL', () => drive('B5', 1, { txHash: REAL, blockHeight: 4242, status: 'confirmed' }));
  it('B6 T1 statusless REAL + DOC-LEVEL _source anchor_store (the seat flag)', () => drive('B6', 1, { txHash: REAL, blockHeight: 4242 }, { extra: { _source: 'anchor_store' } }));
  it('B7 T1 confirmed REAL + DOC-LEVEL _source anchor_store', () => drive('B7', 1, { txHash: REAL, blockHeight: 4242, status: 'confirmed' }, { extra: { _source: 'anchor_store' } }));
  it('B8 T1 statusless REAL + DOC-LEVEL _source originate', () => drive('B8', 1, { txHash: REAL, blockHeight: 4242 }, { extra: { _source: 'originate' } }));
  it('B9 T1 statusless REAL + blockchain._source anchor_store (nested)', () => drive('B9', 1, { txHash: REAL, blockHeight: 4242, _source: 'anchor_store' }));
  it('B10 T1 statusless REAL + data._source anchor_store (user data, nested)', () => drive('B10', 1, { txHash: REAL, blockHeight: 4242 }, { extra: { data: { _source: 'anchor_store' } } }));
  it('B11 T1 statusless REAL + DOC-LEVEL _source ANCHOR_STORE (case)', () => drive('B11', 1, { txHash: REAL, blockHeight: 4242 }, { extra: { _source: 'ANCHOR_STORE' } }));
  it('B12 T1 statusless REAL + DOC-LEVEL _lookupSource anchor_store (handler overwrites it)', () => drive('B12', 1, { txHash: REAL, blockHeight: 4242 }, { extra: { _lookupSource: 'anchor_store' } }));
});
