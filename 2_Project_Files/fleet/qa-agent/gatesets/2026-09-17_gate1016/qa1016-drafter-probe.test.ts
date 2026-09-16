// qa1016-drafter-probe.test.ts — #1016 (KS-1072) DRAFTER RECORDING probe (not an asserting gate file).
// The REAL createVerificationRoutes behind loopback stubs, the ks1072 harness shape (head :16-114) plus:
//   * an anchor-store HIT COUNTER (the tier witness; blockchain.source is NOT one — #1005 gate P-1005-1),
//   * a switchable tier-1 document (null -> originate 404s),
//   * an optional request contentHash.
// Each row is recorded to QA1016_OUT as JSON. The gate writes its OWN asserting cells (FAIL condition first).
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import express from 'express';
import http from 'node:http';
import fs from 'node:fs';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import type { RequestHandler } from 'express';

const DOC_ID = 'doc-qa1016';
const CH = 'b'.repeat(64);
const X = 'c'.repeat(64);
const Y = 'd'.repeat(64);
const R = (c: string) => c.repeat(64);

let gateway: Server;
let anchorServer: Server;
let originate: Server;
let gatewayPort: number;
let anchorRows: Array<Record<string, unknown>> | null = null;
let tier1Doc: Record<string, unknown> | null = null;
let hits = 0;
const jsonHead = { 'Content-Type': 'application/json' };

beforeAll(async () => {
  anchorServer = http.createServer((req, res) => {
    if (req.url === `/api/anchors/document/${DOC_ID}`) {
      hits += 1;
      if (!anchorRows || anchorRows.length === 0) { res.writeHead(404, jsonHead); res.end('{}'); return; }
      res.writeHead(200, jsonHead);
      res.end(JSON.stringify({ success: true, data: { documentId: DOC_ID, anchors: anchorRows, count: anchorRows.length } }));
      return;
    }
    res.writeHead(404, jsonHead); res.end('{}');
  });
  anchorServer.listen(0, '127.0.0.1');
  await new Promise<void>((r) => anchorServer.once('listening', () => r()));
  const anchorPort = (anchorServer.address() as AddressInfo).port;
  originate = http.createServer((req, res) => {
    if (tier1Doc && req.url === `/api/documents/${DOC_ID}`) { res.writeHead(200, jsonHead); res.end(JSON.stringify(tier1Doc)); return; }
    res.writeHead(404, jsonHead); res.end('{}');
  });
  originate.listen(0, '127.0.0.1');
  await new Promise<void>((r) => originate.once('listening', () => r()));
  const origPort = (originate.address() as AddressInfo).port;
  // the live chain scan (fetch to ANCHORING_SERVICE_URL/api/anchors/verify/:hash) must miss: point it at the anchor stub (404)
  process.env.ANCHORING_SERVICE_URL = `http://127.0.0.1:${anchorPort}`;
  const { createVerificationRoutes } = await import('../routes/verification');
  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
  const app = express();
  app.use(createVerificationRoutes({
    authenticateToken: () => (_req, _res, next) => next(),
    mockBodyParser,
    query: vi.fn(async () => ({ rows: [] })) as never,
    isDbAvailable: () => false,
    redisService: {
      getPendingDocument: vi.fn(async () => null), deletePendingDocument: vi.fn(async () => undefined),
      getAllDocumentTypes: vi.fn(async () => []), getAllWorkflowInstances: vi.fn(async () => []),
      getNotificationSettings: vi.fn(async () => ({})), getRejectedDocument: vi.fn(async () => null),
      setRejectedDocument: vi.fn(async () => undefined), getWorkflowDocumentMapping: vi.fn(async () => null),
      getWorkflowInstance: vi.fn(async () => null), setWorkflowInstance: vi.fn(async () => undefined),
    } as never,
    services: { originate: { url: `http://127.0.0.1:${origPort}` }, anchoring: { url: `http://127.0.0.1:${anchorPort}` } } as never,
    log: () => undefined,
    memWorkflowToDocumentMap: new Map(), memRejectedDocuments: new Map(),
    dbSaveRejection: vi.fn(async () => undefined), ADMIN_ROLES: ['ADMIN', 'admin'],
    enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never,
    createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never,
    meetsVerificationLevel: () => true,
  }));
  gateway = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => gateway.once('listening', () => r()));
  gatewayPort = (gateway.address() as AddressInfo).port;
});

afterAll(async () => {
  await new Promise<void>((r) => gateway.close(() => r()));
  await new Promise<void>((r) => anchorServer.close(() => r()));
  await new Promise<void>((r) => originate.close(() => r()));
});

type Row = { id: string; note: string; rows: Array<Record<string, unknown>>; reqHash?: string; t1?: Record<string, unknown> };
const c = (o: Record<string, unknown>) => ({ contentHash: CH, status: 'confirmed', ...o });
const ROWS: Row[] = [
  { id: 'S01', note: 'eq block 100, OLDER listed first, both confirmed', rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S02', note: 'eq block 100, NEWER listed first (control)', rows: [c({ blockNumber: 100, confirmedAt: '2026-08-01T00:00:00Z', transactionHash: R('e') }), c({ blockNumber: 100, confirmedAt: '2026-03-01T00:00:00Z', transactionHash: R('a') })] },
  { id: 'S03', note: 'eq block: older CONFIRMED first, newer FAILED second', rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e'), status: 'failed' })] },
  { id: 'S04', note: 'eq block: older FAILED first, newer CONFIRMED second', rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a'), status: 'failed' }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S05', note: 'eq block: older CONFIRMED first, newer SUBMITTED second', rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e'), status: 'submitted' })] },
  { id: 'S06', note: 'eq block: UNDATED confirmed first, DATED failed second', rows: [c({ blockNumber: 100, confirmedAt: null, transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e'), status: 'failed' })] },
  { id: 'S07', note: 'eq block: UNDATED submitted first (anchoring created_at DESC shape), DATED confirmed second', rows: [c({ blockNumber: 100, confirmedAt: null, transactionHash: R('a'), status: 'submitted' }), c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S08', note: 'eq block: older contentHash X first, newer Y second; request X', reqHash: X, rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a'), contentHash: X }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e'), contentHash: Y })] },
  { id: 'S09', note: 'eq block: older contentHash Y first, newer X second; request X', reqHash: X, rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a'), contentHash: Y }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e'), contentHash: X })] },
  { id: 'S10', note: 'eq block: older REAL tx first, newer tx_sim_ second', rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: 'tx_sim_' + 'e'.repeat(57) })] },
  { id: 'S11', note: 'eq block: older tx_sim_ first, newer REAL second', rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: 'tx_sim_' + 'a'.repeat(57) }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S12', note: 'eq block: older confirmed first, newer simulated:true second', rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e'), simulated: true })] },
  { id: 'S13', note: 'null vs 0 blockNumber, both confirmed, older first', rows: [c({ blockNumber: null, confirmedAt: '2026-02-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 0, confirmedAt: '2026-07-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S14', note: "string '100' vs number 100, older first", rows: [c({ blockNumber: '100', confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S15', note: "non-numeric 'abc' vs 100 (NaN comparator), older first", rows: [c({ blockNumber: 'abc', confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S16', note: 'tie on BOTH block and confirmedAt', rows: [c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S17', note: 'epoch-0 date first vs missing second', rows: [c({ blockNumber: 100, confirmedAt: '1970-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, transactionHash: R('e') })] },
  { id: 'S18', note: 'pre-1970 date first vs missing second', rows: [c({ blockNumber: 100, confirmedAt: '1969-12-31T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, transactionHash: R('e') })] },
  { id: 'S19', note: "invalid date string first vs dated second", rows: [c({ blockNumber: 100, confirmedAt: 'not-a-date', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S20', note: 'numeric epoch-ms confirmedAt (newer) first vs ISO older second', rows: [c({ blockNumber: 100, confirmedAt: 1780000000000, transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S21', note: "legacy non-ISO 'June 1, 2026' first vs ISO Jan second", rows: [c({ blockNumber: 100, confirmedAt: 'June 1, 2026', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S22', note: "offset-LESS '2026-06-01T05:00:00' (local time) first vs '2026-06-01T00:00:00Z' second — TZ-dependent", rows: [c({ blockNumber: 100, confirmedAt: '2026-06-01T05:00:00', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S23', note: 'snake_case block_number/confirmed_at, eq block, older first', rows: [c({ block_number: 100, confirmed_at: '2026-01-01T00:00:00Z', transaction_hash: R('a') }), c({ block_number: 100, confirmed_at: '2026-06-01T00:00:00Z', transaction_hash: R('e') })] },
  { id: 'S24', note: 'snake_case, HIGHER block listed second', rows: [c({ block_number: 100, confirmed_at: '2026-06-01T00:00:00Z', transaction_hash: R('a') }), c({ block_number: 101, confirmed_at: '2026-01-01T00:00:00Z', transaction_hash: R('e') })] },
  { id: 'S25', note: 'three rows: 101 Jan first, 100 Dec, 100 Jun', rows: [c({ blockNumber: 101, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-12-01T00:00:00Z', transactionHash: R('e') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('f') })] },
  { id: 'S26', note: 'single row control', rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') })] },
  { id: 'S27', note: "offset ISO '2026-06-01T10:00:00+10:00' (=00:00Z) first vs '2026-06-01T00:30:00Z' second", rows: [c({ blockNumber: 100, confirmedAt: '2026-06-01T10:00:00+10:00', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:30:00Z', transactionHash: R('e') })] },
  { id: 'S28', note: 'higher block listed second, older date (block beats date)', rows: [c({ blockNumber: 100, confirmedAt: '2026-12-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 101, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('e') })] },
  { id: 'S29', note: 'eq block: older confirmed hash X first, newer FAILED second; request X', reqHash: X, rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a'), contentHash: X }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e'), status: 'failed', contentHash: X })] },
  { id: 'T01', note: 'TIER 1 answers (confirmed blob) while tier-2 rows would tie: hits must be 0', t1: { id: DOC_ID, contentHash: CH, blockchain: { txHash: R('9'), blockHeight: 7, status: 'confirmed' } }, rows: [c({ blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transactionHash: R('a') }), c({ blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transactionHash: R('e') })] },
];

describe('qa1016 drafter probe (recording)', () => {
  it('records every row', async () => {
    const out: Array<Record<string, unknown>> = [];
    for (const row of ROWS) {
      anchorRows = row.rows; tier1Doc = row.t1 || null; const before = hits;
      const res = await fetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(row.reqHash ? { purpose: 'qa', contentHash: row.reqHash } : { purpose: 'qa' }),
      });
      const b = (await res.json()) as any;
      out.push({ id: row.id, note: row.note, http: res.status, hits: hits - before, verified: b.verified, confidence: b.verificationConfidence,
        txHash: typeof b.blockchain?.txHash === 'string' ? b.blockchain.txHash.slice(0, 8) : b.blockchain?.txHash, blockHeight: b.blockchain?.blockHeight,
        hashValid: b.checks?.hashValid, source: b.blockchain?.source });
    }
    fs.writeFileSync(process.env.QA1016_OUT as string, JSON.stringify({ tz: process.env.TZ || '(unset)', rows: out }, null, 1));
    expect(out.length).toBe(ROWS.length);
  });
});
