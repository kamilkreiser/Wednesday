/**
 * =============================================================================
 * KS-1133 - v2 reads hash FIRST in the alias chain (the ruled split)
 * =============================================================================
 */

process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();
const mockAuthenticateCalls: unknown[] = [];

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw },
  getTenantManager: () => null,
}));

jest.mock('../middleware/auth', () => ({
  authenticate: (opts?: unknown) => {
    mockAuthenticateCalls.push(opts);
    return (_req: unknown, _res: unknown, next: () => void) => next();
  },
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
    queryWithTenantGuc: jest.fn(),
  }),
);

jest.mock('../repositories/documentRepo', () => ({
  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
  updateDocument: jest.fn().mockResolvedValue(undefined),
  MAX_LINEAGE_DEPTH: 10,
}));

import express from 'express';
import { verificationV2Router } from '../routes/verificationV2';

const HASH = 'f'.repeat(64);
const OTHER = 'e'.repeat(64);

const app = express();
app.use(express.json());
app.use('/api/v2/verification', verificationV2Router);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;
const realFetch = global.fetch;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => {
  server?.close();
  global.fetch = realFetch;
});

async function verifyV2(body: Record<string, unknown>, headers: Record<string, string> = {}): Promise<{ status: number; body: any }> {
  const res = await realFetch(`${baseUrl}/api/v2/verification/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...headers },
    body: JSON.stringify(body),
  });
  return { status: res.status, body: await res.json() };
}

beforeEach(() => {
  jest.clearAllMocks();
  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
});

describe('KS-1133 - v2 reads hash FIRST in the alias chain (the ruled split)', () => {
  it('RED KS-1133 v2 {contentHash:A, hash:B} - the lookup sees B (hash is read first)', async () => {
    mockQueryRaw.mockResolvedValue([]);
    const { status, body } = await verifyV2({ contentHash: HASH, hash: OTHER });
    expect(status).toBe(200);
    expect(body.hash).toBe(`sha256:${OTHER}`);
  });

  it('RED KS-1133 v2 {providedHash:A, documentHash:A, hash:B} - hash still wins over every alias', async () => {
    mockQueryRaw.mockResolvedValue([]);
    const { status, body } = await verifyV2({ providedHash: HASH, documentHash: HASH, hash: OTHER });
    expect(status).toBe(200);
    expect(body.hash).toBe(`sha256:${OTHER}`);
  });

  it('KS-1133 control - {contentHash:A} alone is looked up as A on both chains', async () => {
    mockQueryRaw.mockResolvedValue([]);
    const { status, body } = await verifyV2({ contentHash: HASH });
    expect(status).toBe(200);
    expect(body.hash).toBe(`sha256:${HASH}`);
  });

  it('KS-1133 control - {hash:B} alone is looked up as B on both chains', async () => {
    mockQueryRaw.mockResolvedValue([]);
    const { status, body } = await verifyV2({ hash: OTHER });
    expect(status).toBe(200);
    expect(body.hash).toBe(`sha256:${OTHER}`);
  });
});
