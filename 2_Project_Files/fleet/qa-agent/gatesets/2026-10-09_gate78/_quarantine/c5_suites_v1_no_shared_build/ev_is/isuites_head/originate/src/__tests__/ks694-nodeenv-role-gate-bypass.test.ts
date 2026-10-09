/**
 * KS-694 — role gates that vanish whenever NODE_ENV !== 'production'.
 *
 * Four routes shipped their admin role check inside a spread that contributes
 * an EMPTY ARRAY off production:
 *
 *   router.get(path, ...(isDev ? [] : [requireRole('SYSTEM_ADMIN','ORG_ADMIN')]), handler)
 *
 * `isDev` is `process.env.NODE_ENV !== 'production'`, and **nothing we deploy
 * sets 'production'**: docker-compose (which the demo VM runs verbatim) sets
 * `development`, the Azure bicep sets `staging`, and `docker exec
 * secuura-originate printenv NODE_ENV` on the live demo VM returns
 * `development`. So the gate was absent everywhere it has ever run.
 *
 * Reproduced against the live local stack before the fix — an ISSUER_ADMIN
 * token returned 200 with another subject's deletion log (userId, dsrId,
 * performedBy) and the platform error log (userId, ipAddress, stack traces).
 * A comparable role-gated route (POST /api/gdpr/retention/enforce) correctly
 * returned 403 for the same token, so `requireRole` demonstrably works and
 * these were a real gap rather than an over-privileged token.
 *
 * These tests run with NODE_ENV='test' — i.e. isDev true — so on the unfixed
 * code every 403 expectation below FAILS with a 200. That is deliberate: the
 * suite must be red before the fix to be worth anything after it.
 *
 * ---------------------------------------------------------------------------
 * HOW TO RUN IT (from Blockchain/Dev/services/originate)
 * ---------------------------------------------------------------------------
 *
 *   npx jest src/__tests__/ks694-nodeenv-role-gate-bypass.test.ts   # this file
 *   npm test                                                       # whole originate suite
 *
 * 33 cases across all four routes: ISSUER_ADMIN / OWNER / VERIFIER / role-less
 * -> 403, unauthenticated -> 401, and SYSTEM_ADMIN / ORG_ADMIN / SUPER_ADMIN
 * -> 200 as the positive control that the fix does not lock out the admins who
 * actually need these routes.
 *
 * The red->green transition it was written to prove (measured 2026-08-27, PR
 * #747 — re-measure, do not quote these forward):
 *
 *   old `...(isDev ? [] : [...])` shape, same harness   18 failed / 15 passed
 *   with the unconditional gates                        33 passed / 33
 *
 * To reproduce the red half, restore the spread on one route and re-run this
 * file — a control that does not fire is not a control.
 *
 * The full originate suite carries pre-existing failures that are NOT this
 * change: see BACKLOG.md ("originate unit suite — pre-existing failures").
 * Confirm any red you see is on that list by stashing your branch and
 * re-running the same file on the clean tree before treating it as yours.
 */

jest.mock('../services/gdprService', () => ({
  getPendingDSRs: jest.fn(async () => []),
  getDeletionLog: jest.fn(async () => []),
}));

jest.mock('../services/errorTrackingService', () => ({
  getRecentErrors: jest.fn(async () => ({ errors: [], total: 0 })),
  getErrorStats: jest.fn(async () => ({ total: 0, bySeverity: {}, byService: {} })),
}));

jest.mock('../db', () => ({
  prisma: { $queryRaw: jest.fn(), $executeRaw: jest.fn(), $executeRawUnsafe: jest.fn() },
}));

// Mutable per-test caller — the mock factory reads it on every request.
let testUser: Record<string, unknown> | null = null;

jest.mock('../middleware/auth', () => {
  const actual = jest.requireActual('../middleware/auth');
  return {
    ...actual,
    authenticate: () => (req: any, res: any, next: () => void) => {
      if (!testUser) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      }
      // Mirror the real setUser(): the module stashes the payload under BOTH
      // `_secuuraUser` (what requireRole reads) and `user` (what handlers read).
      req._secuuraUser = testUser;
      req.user = testUser;
      next();
    },
  };
});

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import express from 'express';
import { gdprRouter } from '../routes/gdpr';
import { systemErrorsRouter } from '../routes/systemErrors';

const app = express();
app.use('/api/gdpr', express.json(), gdprRouter);
app.use('/api/system-errors', express.json(), systemErrorsRouter);

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
  testUser = null;
});

const BASE = { userId: '11111111-2222-4333-8444-555555555555', email: 'caller@example.com' };

/** Every route that carried the vanishing gate. */
const GATED_ROUTES = [
  '/api/gdpr/dsr/pending',
  '/api/gdpr/deletion-log',
  '/api/system-errors',
  '/api/system-errors/stats',
] as const;

function get(path: string): Promise<Response> {
  return fetch(`${baseUrl}${path}`);
}

interface Envelope {
  success?: boolean;
  error?: { code?: string; message?: string };
}

describe('KS-694 — the admin gate must not depend on NODE_ENV', () => {
  it('sanity: this suite runs with NODE_ENV !== production, the condition under test', () => {
    expect(process.env.NODE_ENV).not.toBe('production');
  });

  describe.each(GATED_ROUTES)('%s', (path) => {
    it('403s an ISSUER_ADMIN — a real role, but not an admin of this data', async () => {
      testUser = { ...BASE, role: 'ISSUER_ADMIN' };
      const res = await get(path);
      expect(res.status).toBe(403);
      const body = (await res.json()) as Envelope;
      expect(body.error?.code).toBe('FORBIDDEN');
    });

    it.each(['OWNER', 'VERIFIER'])('403s a %s', async (role) => {
      testUser = { ...BASE, role };
      expect((await get(path)).status).toBe(403);
    });

    it('403s a role-less authenticated caller', async () => {
      testUser = { ...BASE };
      expect((await get(path)).status).toBe(403);
    });

    it('401s an unauthenticated caller', async () => {
      testUser = null;
      expect((await get(path)).status).toBe(401);
    });

    // Positive control: the fix must not lock out the admins who need these.
    it.each(['SYSTEM_ADMIN', 'ORG_ADMIN'])('still admits %s (200)', async (role) => {
      testUser = { ...BASE, role };
      expect((await get(path)).status).toBe(200);
    });

    it('admits SUPER_ADMIN via the alias normalisation requireRole applies', async () => {
      testUser = { ...BASE, role: 'SUPER_ADMIN' };
      expect((await get(path)).status).toBe(200);
    });
  });
});
