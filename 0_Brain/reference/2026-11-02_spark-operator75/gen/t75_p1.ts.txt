// KS-1868: the originate anchor routes read a rejection value in three catch blocks. When the value cannot be read
// (a revoked Proxy throws on property reads; an Error whose `message` getter throws, throws on `.message`) the catch
// itself used to throw before its log line. Cells: GET /api/anchors/:documentId (the lookup `getAnchorByDocumentId`
// logs a warn and RETHROWS; the route catch then logs an error and answers the constant 500) and
// `verifyAnchorsDbReady` (logs an error and throws the constant `Database is required for anchor operations`).
// An ordinary Error is the control. Harness: the ks1657 anchor-read-fault suite (same mocks; real router, real
// loopback server). The database stand-in rejects with a plain function, not jest.fn(): a spy inspects what it
// rejects with and could itself fail on a revoked Proxy before the code under test saw it. Nothing is written.
const mockState: { toThrow: unknown; warned: unknown[][]; errored: unknown[][]; writes: number } = {
  toThrow: undefined,
  warned: [],
  errored: [],
  writes: 0,
};

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: (..._args: unknown[]) => Promise.reject(mockState.toThrow),
    $executeRaw: (..._args: unknown[]) => {
      mockState.writes += 1;
      return Promise.reject(mockState.toThrow);
    },
  },
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
  logger: {
    info: () => undefined,
    debug: () => undefined,
    warn: (...args: unknown[]) => {
      mockState.warned.push(args);
    },
    error: (...args: unknown[]) => {
      mockState.errored.push(args);
    },
  },
}));

import express from 'express';
import { anchorsRouter, verifyAnchorsDbReady } from '../routes/anchors';

const app = express();
app.use('/api/anchors', express.json(), anchorsRouter);

const DOC = 'doc-ks1868-lookup-target';
const DB_READY_MESSAGE = 'Database is required for anchor operations';

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
  mockState.toThrow = undefined;
  mockState.warned.length = 0;
  mockState.errored.length = 0;
  mockState.writes = 0;
  delete process.env.SIMULATE_ANCHORING;
});

const revokedProxy = (): unknown => {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
};

const getterThrows = (): unknown =>
  Object.create(Error.prototype, {
    message: {
      get() {
        throw new Error('getter boom');
      },
    },
  });

async function getAnchor(): Promise<{ status: number; code: string | undefined }> {
  const res = await fetch(`${baseUrl}/api/anchors/${DOC}`);
  const body = (await res.json()) as { error?: { code?: string } };
  return { status: res.status, code: body.error?.code };
}

describe('KS-1868 the originate anchor catches read the rejection value safely', () => {
  it('control ks1868 C1 GET /:documentId: an ordinary Error is logged with its own message and the route answers 500', async () => {
    mockState.toThrow = new Error('Connection terminated unexpectedly');
    expect(await getAnchor()).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
    expect(mockState.warned).toEqual([['Failed to fetch anchor from DB', { documentId: DOC, error: 'Connection terminated unexpectedly' }]]);
    expect(mockState.errored).toEqual([['Failed to get anchor', { error: 'Connection terminated unexpectedly' }]]);
    expect(mockState.writes).toBe(0);
  });

  it('control ks1868 C2 verifyAnchorsDbReady: an ordinary Error is logged with its own message and the constant error is thrown', async () => {
    mockState.toThrow = new Error('db down');
    await expect(verifyAnchorsDbReady()).rejects.toThrow(DB_READY_MESSAGE);
    expect(mockState.errored).toHaveLength(1);
    expect(mockState.errored[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 GET /:documentId: a revoked Proxy rejection logs both lines with a constant reason and the route answers 500', async () => {
    mockState.toThrow = revokedProxy();
    expect(await getAnchor()).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
    expect(mockState.warned).toEqual([['Failed to fetch anchor from DB', { documentId: DOC, error: 'unreadable thrown value' }]]);
    expect(mockState.errored).toEqual([['Failed to get anchor', { error: 'unreadable thrown value' }]]);
    expect(mockState.writes).toBe(0);
  });

  it('RED ks1868 R2 GET /:documentId: an Error whose message getter throws logs both lines with a constant reason and the route answers 500', async () => {
    mockState.toThrow = getterThrows();
    expect(await getAnchor()).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
    expect(mockState.warned).toEqual([['Failed to fetch anchor from DB', { documentId: DOC, error: 'unreadable thrown value' }]]);
    expect(mockState.errored).toEqual([['Failed to get anchor', { error: 'unreadable thrown value' }]]);
    expect(mockState.writes).toBe(0);
  });

  it('RED ks1868 R3 verifyAnchorsDbReady: a revoked Proxy rejection logs a constant reason and the constant error is thrown', async () => {
    mockState.toThrow = revokedProxy();
    await expect(verifyAnchorsDbReady()).rejects.toThrow(DB_READY_MESSAGE);
    expect(mockState.errored).toHaveLength(1);
    expect(mockState.errored[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R4 verifyAnchorsDbReady: an Error whose message getter throws logs a constant reason and the constant error is thrown', async () => {
    mockState.toThrow = getterThrows();
    await expect(verifyAnchorsDbReady()).rejects.toThrow(DB_READY_MESSAGE);
    expect(mockState.errored).toHaveLength(1);
    expect(mockState.errored[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
