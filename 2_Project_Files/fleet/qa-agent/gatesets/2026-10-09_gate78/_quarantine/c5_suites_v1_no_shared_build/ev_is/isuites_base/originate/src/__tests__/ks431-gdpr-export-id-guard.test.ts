/**
 * KS-431 — GET /api/gdpr/export/:userId/download userId guard.
 *
 * The handler passed :userId straight to gdpr.exportUserData → a DB query. A malformed
 * value (the sweep sent non-UTF-8 bytes) made Postgres throw (22P02 / 22021), which fell
 * through to a raw 500. The handler now rejects a non-UUID userId up front → 404.
 */

const mockExportUserData = jest.fn();

jest.mock('../services/gdprService', () => ({
  exportUserData: mockExportUserData,
}));

jest.mock('../middleware/auth', () => ({
  // Auth/authz are not under test — pass everything through.
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireSelfOrRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  hasAnyRole: () => true,
}));

import express from 'express';
import { gdprRouter } from '../routes/gdpr';

const app = express();
app.use('/api/gdpr', express.json(), gdprRouter);

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
beforeEach(() => jest.clearAllMocks());

describe('KS-431 GET /api/gdpr/export/:userId/download', () => {
  it('404s on a malformed (non-UUID) userId without touching the DB — no raw 500', async () => {
    // The exact non-UTF-8 byte sequence the sweep used.
    const res = await fetch(`${baseUrl}/api/gdpr/export/%23%F2%B5%92%9B/download`);
    expect(res.status).toBe(404);
    expect(mockExportUserData).not.toHaveBeenCalled();
  });

  it('reaches the service for a well-formed UUID userId', async () => {
    mockExportUserData.mockResolvedValueOnce({ user: {}, documents: [] });
    const res = await fetch(`${baseUrl}/api/gdpr/export/11111111-2222-4333-8444-555555555555/download`);
    expect(res.status).toBe(200);
    expect(mockExportUserData).toHaveBeenCalledWith('11111111-2222-4333-8444-555555555555');
  });
});
