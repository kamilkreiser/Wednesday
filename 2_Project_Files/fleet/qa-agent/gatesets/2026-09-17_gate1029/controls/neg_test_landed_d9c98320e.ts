// =============================================================================
// KS-1072 — latest-anchor selector documents a confirmedAt tiebreak it does
// not implement
// =============================================================================
//
// In makeFetchDocFromAnchorStore the comment promises: "Latest = highest
// blockNumber, fall back to most-recent confirmedAt." The comparator only
// orders by blockNumber descending; two anchors with the same blockNumber are
// ordered arbitrarily. Since KS-1057 this selection decides the verdict.
//
// Driven against the real router with a stub server that plays originate AND
// anchoring over HTTP, copied from the KS-1071 file's mocking shape so both
// files cannot fail together on a shared helper.
// =============================================================================

import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import express from 'express';
import http from 'node:http';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import type { RequestHandler } from 'express';

const DOC_ID = 'doc-ks1072';
const CONTENT_HASH = 'b'.repeat(64);

let gateway: Server;
let anchorServer: Server;
let gatewayPort: number;
/** Tier-2 rows served by the stub anchor store for the current cell. */
let anchorStoreRows: Array<Record<string, unknown>> | null = null;
// KS-1072 (seat A): the READY's `tier1Absent` flag was assigned but never read (the stub originate below 404s
// every request, which is what forces tier 2), so it is removed; the originate stub is now closed in afterAll.
let originate: Server;
const jsonHead = { 'Content-Type': 'application/json' };

beforeAll(async () => {
  // Stub anchor store: serves `data.data.anchors` under test control.
  anchorServer = http.createServer((req, res) => {
    if (req.url === `/api/anchors/document/${DOC_ID}`) {
      if (!anchorStoreRows || anchorStoreRows.length === 0) {
        res.writeHead(404, jsonHead);
        res.end('{}');
        return;
      }
      res.writeHead(200, jsonHead);
      res.end(JSON.stringify({ data: { anchors: anchorStoreRows } }));
      return;
    }
    res.writeHead(404, jsonHead);
    res.end('{}');
  });
  anchorServer.listen(0, '127.0.0.1');
  await new Promise<void>((r) => anchorServer.once('listening', () => r()));
  const anchorPort = (anchorServer.address() as AddressInfo).port;

  // Stub originate: always 404s to force the tier-2 path through anchoring.
  originate = http.createServer((_req, res) => {
    res.writeHead(404, jsonHead);
    res.end('{}');
  });
  originate.listen(0, '127.0.0.1');
  await new Promise<void>((r) => originate.once('listening', () => r()));
  const origPort = (originate.address() as AddressInfo).port;

  const { createVerificationRoutes } = await import('../routes/verification');
  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });

  const app = express();
  app.use(
    createVerificationRoutes({
      authenticateToken: () => (_req, _res, next) => next(),
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
      services: {
        originate: { url: `http://127.0.0.1:${origPort}` },
        anchoring: { url: `http://127.0.0.1:${anchorPort}` },
      } as never,
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
  await new Promise<void>((r) => gateway.close(() => r()));
  await new Promise<void>((r) => anchorServer.close(() => r()));
  await new Promise<void>((r) => originate.close(() => r()));
});

async function postTier2(rows: Array<Record<string, unknown>>): Promise<any> {
  anchorStoreRows = rows.map((r) => ({ contentHash: CONTENT_HASH, ...r }));
  const anchorStoreUrls: string[] = []; // KS-1180 (P-1016-1): the requests the stub anchor store receives during this verify
  const onAnchorStoreRequest = (req: { url?: string }): void => { anchorStoreUrls.push(String(req.url)); };
  anchorServer.on('request', onAnchorStoreRequest);
  const res = await fetch(`http://127.0.0.1:${gatewayPort}/api/documents/${DOC_ID}/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ purpose: 'test' }),
  });
  expect(res.status).toBe(200);
  const body = await res.json();
  anchorServer.off('request', onAnchorStoreRequest);
  // KS-1180 (P-1016-1): the tier witness. blockchain.source reads 'persisted' on BOTH tiers, so it cannot say which tier
  // answered. Tier 2 answered only if the stub anchor store served this document exactly once.
  expect(anchorStoreUrls, 'KS-1180: tier 2 answered, one anchor-store read of this document').toEqual(['/api/anchors/document/' + DOC_ID]);
  return body;
}

describe('KS-1072 — latest-anchor selector confirmedAt tiebreak', () => {
  it('KS-1180 control - a document the anchor store does not have: 404, and the stub anchor store was asked once', async () => {
    const missUrls: string[] = [];
    const onMiss = (req: { url?: string }): void => { missUrls.push(String(req.url)); };
    anchorServer.on('request', onMiss);
    const res = await fetch('http://127.0.0.1:' + String(gatewayPort) + '/api/documents/doc-ks1180-absent/verify', { method: 'POST', headers: jsonHead, body: JSON.stringify({ purpose: 'test' }) });
    anchorServer.off('request', onMiss);
    expect([res.status, missUrls], 'KS-1180 control: a tier-2 miss is asked once and answers 404').toEqual([404, ['/api/anchors/document/doc-ks1180-absent']]);
  }); // KS-1180 control

  it('\u{1F534} KS-1072 \u2014 equal blockNumber: the most recent confirmedAt wins', async () => {
    // Base: stable sort keeps first-in-array when byBlock === 0 → old anchor selected.
    const body = await postTier2([
      { blockNumber: 100, confirmedAt: '2026-01-01T00:00:00Z', transaction_hash: 'a'.repeat(64), status: 'confirmed' },
      { blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transaction_hash: 'b'.repeat(64), status: 'confirmed' },
    ]);
    expect(body.blockchain.txHash).toBe('b'.repeat(64));
  });

  it('\u{1F534} KS-1072 \u2014 a missing confirmedAt loses the tiebreak', async () => {
    // A dated anchor beats an undated one on equal blockNumber: Date.parse(undefined) || 0 is 0. At base the
    // comparator returned 0 for the pair, so the stable sort kept the undated anchor listed first.
    // (KS-1072, seat A: replaces the READY's working-out comment; the cell is unchanged.)
    const body = await postTier2([
      { blockNumber: 100, transaction_hash: 'c'.repeat(64), status: 'confirmed' },
      { blockNumber: 100, confirmedAt: '2026-06-01T00:00:00Z', transaction_hash: 'd'.repeat(64), status: 'confirmed' },
    ]);
    expect(body.blockchain.txHash).toBe('d'.repeat(64));
  });

  // KS-1072 (seat A): the ticket names the common 0/null blockNumber case, which `|| 0` collapses to a tie.
  it('\u{1F534} KS-1072 \u2014 a null and a 0 blockNumber tie, and the most recent confirmedAt wins', async () => {
    const body = await postTier2([
      { blockNumber: null, confirmedAt: '2026-02-01T00:00:00Z', transaction_hash: '1'.repeat(64), status: 'confirmed' },
      { blockNumber: 0, confirmedAt: '2026-07-01T00:00:00Z', transaction_hash: '2'.repeat(64), status: 'confirmed' },
    ]);
    expect(body.blockchain.txHash).toBe('2'.repeat(64));
  });

  // KS-1072 (seat A): every tie above lists the OLDER anchor first, so a comparator that picked the oldest would
  // red them exactly as a missing tiebreak does. Listing the newer anchor first separates the two: this cell is
  // green at base (the stable sort keeps the first row) and reds only if recency is ordered the wrong way.
  it('KS-1072 control \u2014 equal blockNumber with the newer anchor listed first: the newer still wins', async () => {
    const body = await postTier2([
      { blockNumber: 100, confirmedAt: '2026-08-01T00:00:00Z', transaction_hash: '3'.repeat(64), status: 'confirmed' },
      { blockNumber: 100, confirmedAt: '2026-03-01T00:00:00Z', transaction_hash: '4'.repeat(64), status: 'confirmed' },
    ]);
    expect(body.blockchain.txHash).toBe('3'.repeat(64));
  });

  it('KS-1072 control \u2014 a higher blockNumber still wins regardless of confirmedAt', async () => {
    // Green at base and after — blockNumber ordering is unchanged.
    const body = await postTier2([
      { blockNumber: 101, confirmedAt: '2026-01-01T00:00:00Z', transaction_hash: 'e'.repeat(64), status: 'confirmed' },
      { blockNumber: 100, confirmedAt: '2026-12-01T00:00:00Z', transaction_hash: 'f'.repeat(64), status: 'confirmed' },
    ]);
    expect(body.blockchain.txHash).toBe('e'.repeat(64));
  });
});
