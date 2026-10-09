/**
 * =============================================================================
 * KS-584 P3 — authenticate() classifies JWT errors across module instances
 * =============================================================================
 * verifyRs256 delegates to @secuura/shared's jsonwebtoken; in the container
 * layout (/shared/node_modules vs /app/node_modules) that is a DIFFERENT
 * module instance than middleware/auth.ts's own import, so
 * `error instanceof jwt.JsonWebTokenError` is FALSE for the very errors the
 * branch exists to catch. Live symptom (first exposed by the v2 verify
 * mount): `Authorization: Bearer not-a-real-token` → raw 500 "jwt malformed"
 * instead of 401. The fix classifies by error NAME as well, which survives
 * crossing module instances.
 * =============================================================================
 */

process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

// Reproduce the cross-instance shape exactly: an error whose NAME says
// JsonWebTokenError but which is NOT an instance of this module tree's
// jsonwebtoken classes (plain Error with the name overwritten).
const crossInstanceJwtError = () => {
  const e = new Error('jwt malformed');
  e.name = 'JsonWebTokenError';
  return e;
};

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    isSessionActive: jest.fn().mockResolvedValue(true),
  }),
);

jest.mock('@secuura/shared/crypto/jwks', () => ({
  verifyJwtRs256: jest.fn().mockImplementation(() => { throw crossInstanceJwtError(); }),
}));

import express from 'express';
import { authenticate } from '../middleware/auth';

const app = express();
app.get('/optional', authenticate({ required: false }), (_req, res) => res.json({ ok: true }));
app.get('/required', authenticate(), (_req, res) => res.json({ ok: true }));
// A next(error) fall-through would land here as a 500.
// eslint-disable-next-line @typescript-eslint/no-unused-vars
app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
});

let baseUrl = '';
let server: ReturnType<typeof app.listen>;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => {
  server?.close();
});

describe('KS-584 P3 — cross-instance JWT error classification', () => {
  it('optional-auth route: PRESENT-but-invalid bearer → 401, not a raw 500', async () => {
    const res = await fetch(`${baseUrl}/optional`, { headers: { Authorization: 'Bearer not-a-real-token' } });
    expect(res.status).toBe(401);
    const body: any = await res.json();
    expect(body.error.code).toBe('UNAUTHORIZED');
  });

  it('optional-auth route: ABSENT bearer → anonymous pass-through', async () => {
    const res = await fetch(`${baseUrl}/optional`);
    expect(res.status).toBe(200);
  });

  it('required-auth route: the same cross-instance error is also a 401', async () => {
    const res = await fetch(`${baseUrl}/required`, { headers: { Authorization: 'Bearer not-a-real-token' } });
    expect(res.status).toBe(401);
  });
});
