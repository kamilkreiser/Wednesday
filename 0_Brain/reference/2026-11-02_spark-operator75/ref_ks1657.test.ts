/**
 * KS-1657 — GET /api/anchors/:documentId must not answer 404 when its database
 * read FAILS.
 *
 * What was open. `getAnchorByDocumentId` caught every error and returned null,
 * and the route reads null as "no anchor on record" — a 404 with
 * `anchored: false`. So a broken lookup (connection lost, pool starved, a
 * statement error) and a genuine absence were one answer. A caller that was told
 * "this document has no anchor" could believe it and act on it, when the truth
 * was "the platform could not look".
 *
 * The ruling (Kam, 2026-10-28 07:13 AEDT, "a — Fix it"). A fault answers 500 (the
 * route's own catch), a genuine absence keeps its 404. The fault now propagates
 * out of the lookup instead of being flattened into null; the warn log stays.
 *
 * WHY 500 AND NOT 503. auth classifies infrastructure faults with
 * `isInfrastructureDbError` (services/auth/src/repositories/dbErrors.ts), but it
 * reads `pg` error codes and `pg` pool messages; originate reads through Prisma,
 * whose errors carry other codes and other text. originate has no classifier of
 * its own, so a 503 here would mean writing and proving a new one for a single
 * route. The route's existing catch already answers a constant 500, which is
 * inside the ruling.
 *
 * WHAT DISCRIMINATES. Measured at develop 8894c7486f82 before the fix: A1, A2,
 * A3, A4 and B3 are red (A1/A3 answer 404 where 500 is wanted, A2 finds
 * `anchored: false` in the body, A4 fails on the route-catch log, B3 reads
 * [404, 404]); A5, B1 and B2 are green. A5 is the no-write property, kept so the
 * fix cannot trade one dishonest answer for a write. B1/B2 are the controls that
 * catch the fix going too far: a real absence must still be a 404 with the same
 * body, and a real anchor must still read back. B3 puts both answers on the SAME
 * id in one run, which is the property the ticket is about: two different
 * situations, two different answers.
 */

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();
jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw },
  getTenantManager: jest.fn(() => null),
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: '11111111-2222-4333-8444-555555555555', role: 'ISSUER_ADMIN' };
    next();
  },
}));

jest.mock('../middleware/rbac', () => ({ isAllowedByRoleOrScope: () => true }));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import { anchorsRouter } from '../routes/anchors';
import { logger } from '../utils/logger';

const app = express();
app.use('/api/anchors', express.json(), anchorsRouter);

const DOC = 'doc-ks1657-lookup-target';
const REAL_TX = 'e'.repeat(64);

type ErrorBody = { success?: boolean; error?: { code?: string; message?: string; anchored?: boolean; documentId?: string } };

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

/** A database fault as the `pg`/Prisma layer raises it: an Error, not a row set. */
const DB_FAULT = new Error('Connection terminated unexpectedly');

const anchorRow = () => [
  {
    document_id: DOC,
    transaction_hash: REAL_TX,
    block_number: 42,
    network: 'preview',
    created_at: new Date('2026-01-01T00:00:00Z'),
    content_hash: `sha256:${'c'.repeat(64)}`,
    simulated: false,
  },
];

describe('KS-1657 A — a failed read is not an absence', () => {
  it('A1 the lookup rejects with an Error: the route answers 500, not 404', async () => {
    mockQueryRaw.mockRejectedValue(DB_FAULT);

    const res = await fetch(`${baseUrl}/api/anchors/${DOC}`);

    // Before the fix this was 404 NOT_FOUND with `anchored: false`.
    expect(res.status).toBe(500);
    const body = (await res.json()) as ErrorBody;
    expect(body.error?.code).toBe('INTERNAL_ERROR');
  });

  it('A2 the 500 body never claims the document has no anchor', async () => {
    mockQueryRaw.mockRejectedValue(DB_FAULT);

    const res = await fetch(`${baseUrl}/api/anchors/${DOC}`);
    const body = (await res.json()) as ErrorBody;

    // `anchored: false` is the platform saying "I looked and there is none".
    // After a failed look it must not be said, in either spelling.
    expect(body.error?.anchored).toBeUndefined();
    expect(JSON.stringify(body)).not.toContain('NOT_FOUND');
    // And the fault text itself is not relayed to the caller.
    expect(JSON.stringify(body)).not.toContain('Connection terminated');
  });

  it('A3 a non-Error rejection (a bare string) is a 500 too', async () => {
    mockQueryRaw.mockRejectedValue('pool exhausted');

    const res = await fetch(`${baseUrl}/api/anchors/${DOC}`);
    expect(res.status).toBe(500);
  });

  it('A4 the fault is still logged, with the document id and the message', async () => {
    mockQueryRaw.mockRejectedValue(DB_FAULT);

    await fetch(`${baseUrl}/api/anchors/${DOC}`);

    expect(logger.warn).toHaveBeenCalledWith('Failed to fetch anchor from DB', {
      documentId: DOC,
      error: 'Connection terminated unexpectedly',
    });
    // The route's own catch logs the 500 it sends.
    expect(logger.error).toHaveBeenCalledWith('Failed to get anchor', expect.anything());
  });

  it('A5 a failed read writes nothing', async () => {
    mockQueryRaw.mockRejectedValue(DB_FAULT);

    await fetch(`${baseUrl}/api/anchors/${DOC}`);

    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });
});

describe('KS-1657 B — what must NOT change', () => {
  it('B1 CONTROL: a genuine absence (zero rows) is still the same 404 body', async () => {
    mockQueryRaw.mockResolvedValue([]);

    const res = await fetch(`${baseUrl}/api/anchors/${DOC}`);

    expect(res.status).toBe(404);
    const body = (await res.json()) as ErrorBody;
    expect(body).toEqual({
      success: false,
      error: { code: 'NOT_FOUND', message: 'No anchor found for this document', documentId: DOC, anchored: false },
    });
    // The fault path's warn log must not fire for a plain absence.
    expect(logger.warn).not.toHaveBeenCalled();
  });

  it('B2 CONTROL: an anchor that exists still reads back', async () => {
    mockQueryRaw.mockResolvedValue(anchorRow());

    const res = await fetch(`${baseUrl}/api/anchors/${DOC}`);

    expect(res.status).toBe(200);
    const body = (await res.json()) as { transactionId?: string | null; verified?: boolean };
    expect([body.transactionId, body.verified]).toEqual([REAL_TX, true]);
  });

  it('B3 the SAME id answers 500 for a fault and 404 for an absence, in one run', async () => {
    mockQueryRaw.mockRejectedValueOnce(DB_FAULT).mockResolvedValueOnce([]);

    const failed = await fetch(`${baseUrl}/api/anchors/${DOC}`);
    const absent = await fetch(`${baseUrl}/api/anchors/${DOC}`);

    expect([failed.status, absent.status]).toEqual([500, 404]);
  });
});
