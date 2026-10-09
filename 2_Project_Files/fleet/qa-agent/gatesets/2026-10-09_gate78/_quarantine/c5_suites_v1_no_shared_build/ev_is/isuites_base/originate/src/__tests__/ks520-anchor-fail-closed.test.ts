/**
 * KS-520 — anchoring must fail CLOSED when simulation was not requested.
 *
 * Two fabrication sites are pinned here:
 *
 * 1. POST /api/documents auto-anchor `.catch`: with `SIMULATE_ANCHORING`
 *    unset and the anchoring service unreachable, the handler used to
 *    fabricate a `tx_sim_…` hash and mark the document `anchored` — an
 *    on-chain-looking proof for a transaction that does not exist. It must
 *    instead record a retryable `anchor_failed` state and never write
 *    `status: 'anchored'` or any `tx_sim_` value.
 *
 * 2. GET /api/anchors/:documentId: with no anchor on record, any
 *    non-production env used to fabricate AND persist a simulated anchor on
 *    a read. Only an explicit `SIMULATE_ANCHORING=true` may synthesize one;
 *    otherwise the route answers an honest 404.
 *
 * The anchoring service is made unreachable by pointing
 * ANCHORING_SERVICE_URL at a closed local port (no global fetch mock — the
 * test harness itself uses fetch to drive the routes).
 */

// Fail-open only ever happened when simulation was NOT requested — make sure
// no sibling test file's env leaks into this worker.
delete process.env.SIMULATE_ANCHORING;
// KS-1266: port 2, not port 1 — port 1 is on the Fetch-spec bad-port list and undici refuses
// it before any socket opens, so the header's "closed local port" was not the mechanism.
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';

// KS-596: saveDocument returns { dbId, inserted } — the create route reads dbId.
const mockSaveDocument = jest.fn(async (..._args: any[]) => ({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true }));
const mockUpdateDocument = jest.fn(async () => undefined);

jest.mock('../repositories/documentRepo', () => ({
  getDocument: jest.fn(),
  listDocuments: jest.fn(),
  saveDocument: mockSaveDocument,
  updateDocument: mockUpdateDocument,
  getSigningRequest: jest.fn(),
  saveSigningRequest: jest.fn(),
  deleteSigningRequest: jest.fn(),
  generateContentHash: jest.fn(() => 'a'.repeat(64)),
  seedDemoDocuments: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
}));

jest.mock('../repositories/shareRepo', () => ({ createShare: jest.fn() }));

jest.mock('../repositories/lifecycleEventRepo', () => ({
  createLifecycleEvent: jest.fn(),
  setLifecycleEventAnchor: jest.fn(),
  listLifecycleEvents: jest.fn(),
}));

jest.mock('../events', () => ({
  publishEvent: jest.fn(async () => undefined),
  EventTypes: {
    DOCUMENT_CREATED: 'document.created',
    DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred',
    DOCUMENT_VERSIONED: 'document.versioned',
  },
}));

jest.mock('../services/threadTokenClient', () => ({
  mintAndRegisterThreadToken: jest.fn(async () => ({})),
}));

jest.mock('../routes/verification', () => ({
  registerInPlatformRegistry: jest.fn(async () => undefined),
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: '11111111-2222-4333-8444-555555555555', role: 'ISSUER_ADMIN' };
    next();
  },
}));

jest.mock('../middleware/rbac', () => ({
  isAllowedByRoleOrScope: () => true,
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

// The anchors router reads anchor rows through prisma directly.
const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();
jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw },
  getTenantManager: jest.fn(() => null),
}));

import express from 'express';
import { documentsRouter } from '../routes/documents';
import { anchorsRouter } from '../routes/anchors';

const app = express();
app.use('/api/documents', express.json(), documentsRouter);
app.use('/api/anchors', express.json(), anchorsRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => server?.close());
beforeEach(() => {
  jest.clearAllMocks();
  delete process.env.SIMULATE_ANCHORING;
});

/** Poll until the fire-and-forget anchor `.catch` has run (bounded). */
async function waitForUpdateDocumentCall(timeoutMs = 3000): Promise<void> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (mockUpdateDocument.mock.calls.length > 0) return;
    await new Promise((r) => setTimeout(r, 25));
  }
}

describe('KS-520 auto-anchor fails closed when SIMULATE_ANCHORING is unset', () => {
  it('records anchor_failed (terminal-status-guarded) and never fabricates a tx_sim_ hash', async () => {
    const res = await fetch(`${baseUrl}/api/documents`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ title: 'ks520 fail closed', type: 'general', data: { note: 'x' } }),
    });
    expect(res.status).toBe(201);

    // The anchoring POST to the closed port rejects asynchronously.
    await waitForUpdateDocumentCall();

    expect(mockUpdateDocument).toHaveBeenCalled();
    const calls = mockUpdateDocument.mock.calls as unknown[][];
    // No call may fabricate: no anchored status, no tx_sim_ anywhere.
    expect(JSON.stringify(calls)).not.toContain('tx_sim_');
    for (const call of calls) {
      const updates = call[2] as { status?: string };
      expect(updates.status).not.toBe('anchored');
    }
    // The fail-closed state is recorded, guarded against racing revokes.
    const failCall = calls.find(
      (c) => ((c[2] as { blockchain?: { status?: string } }).blockchain?.status) === 'anchor_failed',
    );
    expect(failCall).toBeDefined();
    expect(failCall![4]).toEqual({ preserveTerminalStatuses: true });
    const blockchain = (failCall![2] as { blockchain: { txHash: string | null; error?: string } }).blockchain;
    expect(blockchain.txHash).toBeNull();
    expect(blockchain.error).toBeTruthy();
  });
});

describe('KS-520 GET /api/anchors/:documentId read-fallback', () => {
  it('404s when no anchor exists and simulation was not requested', async () => {
    mockQueryRaw.mockResolvedValue([]); // no anchor row
    const res = await fetch(`${baseUrl}/api/anchors/doc-ks520`);
    expect(res.status).toBe(404);
    // Nothing may be fabricated or persisted on the read path.
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it('still synthesizes a clearly-simulated anchor under explicit SIMULATE_ANCHORING=true', async () => {
    process.env.SIMULATE_ANCHORING = 'true';
    mockQueryRaw.mockResolvedValue([]); // no anchor row
    mockExecuteRaw.mockResolvedValue(undefined);
    const res = await fetch(`${baseUrl}/api/anchors/doc-ks520`);
    expect(res.status).toBe(200);
    const body = (await res.json()) as {
      transactionId?: string | null;
      simulated?: boolean;
      simulatedTxRef?: string;
      verified?: boolean;
    };
    // KS-587 tightened the honest shape: the placeholder moves to
    // simulatedTxRef, transactionId is null, and no verification is claimed
    // (previously this test accepted the tx_sim_ placeholder AS the
    // transactionId, which is exactly what let fabricated hashes read as
    // on-chain proof downstream).
    expect(body.transactionId).toBeNull();
    expect(body.simulated).toBe(true);
    expect(body.simulatedTxRef).toMatch(/^tx_sim_/);
    expect(body.verified).toBe(false);
  });
});

// KS-1124 O1: the thread-token mint callback at document create wrote the create-time local (which has
// no blockchain key) plus the token, and updateDocument replaces the blockchain column wholesale. So an
// anchor accept persisted FIRST lost its txHash, status and anchorId. The callback now merges into the
// blob as persisted at write time. Same harness as above: documentRepo and the thread-token client are
// this file's own mocks, reached through jest.requireMock.
const KS1124_TX = 'a'.repeat(64);
const KS1124_MINTED = { policyId: 'policy-ks1124', scriptAddress: 'addr_test1ks1124', mintTxHash: 'b'.repeat(64), network: 'preprod' };
const ks1124GetDocument = (jest.requireMock('../repositories/documentRepo') as { getDocument: jest.Mock }).getDocument;
const ks1124Mint = (jest.requireMock('../services/threadTokenClient') as { mintAndRegisterThreadToken: jest.Mock }).mintAndRegisterThreadToken;

/** Create a document, then wait (bounded) for the fire-and-forget thread-token write and return its blob. */
async function ks1124ThreadTokenWrite(): Promise<Record<string, any> | undefined> {
  const res = await fetch(baseUrl + '/api/documents', {
    method: 'POST',
    headers: { 'content-type': 'application/json', authorization: 'Bearer t' },
    body: JSON.stringify({ title: 'ks1124 thread token', type: 'general', data: { note: 'x' } }),
  });
  expect(res.status).toBe(201);
  const deadline = Date.now() + 3000;
  while (Date.now() < deadline) {
    const hit = (mockUpdateDocument.mock.calls as unknown[][]).find(
      (c) => (c[2] as { blockchain?: { threadToken?: { mintTxHash?: string } } }).blockchain?.threadToken?.mintTxHash === KS1124_MINTED.mintTxHash,
    );
    if (hit) return (hit[2] as { blockchain: Record<string, any> }).blockchain;
    await new Promise((r) => setTimeout(r, 25));
  }
  return undefined;
}

describe('KS-1124 O1: the thread-token cache write merges into the persisted blob', () => {
  beforeEach(() => {
    process.env.STATE_THREAD_NFT_ENABLED = 'true';
    ks1124Mint.mockResolvedValue(KS1124_MINTED);
  });
  afterEach(() => {
    delete process.env.STATE_THREAD_NFT_ENABLED;
  });

  it('RED KS-1124 M1: an anchor accept already persisted keeps its txHash, status and anchorId', async () => {
    ks1124GetDocument.mockResolvedValue({
      id: 'doc-ks1124',
      blockchain: { txHash: KS1124_TX, status: 'submitted', anchorId: 'anchor-ks1124', network: 'preprod' },
    });
    const blob = await ks1124ThreadTokenWrite();
    expect(blob).toBeDefined();
    expect({ txHash: blob?.txHash, status: blob?.status, anchorId: blob?.anchorId })
      .toEqual({ txHash: KS1124_TX, status: 'submitted', anchorId: 'anchor-ks1124' });
  });

  it('control KS-1124 C1: the write carries the minted thread token, field for field', async () => {
    ks1124GetDocument.mockResolvedValue({ id: 'doc-ks1124', blockchain: { txHash: KS1124_TX, status: 'submitted' } });
    const blob = await ks1124ThreadTokenWrite();
    expect(ks1124Mint).toHaveBeenCalledTimes(1);
    expect(blob?.threadToken).toEqual(KS1124_MINTED);
  });

  it('control KS-1124 C2: with no persisted row the write carries the thread token and invents no anchor field', async () => {
    ks1124GetDocument.mockResolvedValue(null);
    const blob = await ks1124ThreadTokenWrite();
    expect(Object.keys(blob ?? {})).toEqual(['threadToken']);
  });
});
