// gate 79 probe (NOT part of the PR): what the catch sends when a throw happens AFTER res.setHeader('Set-Cookie').
// authResult.user carries a BigInt so res.json's JSON.stringify throws inside the try.
import { describe, it, expect, vi } from 'vitest';
vi.mock('../utils/logger', () => ({ logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }, createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }) }));
vi.mock('../services/authClient', () => ({
  authenticatePersona: async () => ({ success: true, accessToken: 'AT', user: { n: BigInt(1) }, setCookieHeader: 'refresh_token=RT_SECRET; HttpOnly' }),
}));
import express from 'express';
import { personaRouter } from '../routes/persona';
describe('gate79 probe', () => {
  it('reports status, Set-Cookie and body of the catch answer', async () => {
    const app = express(); app.use(express.json()); app.use('/demo-api', personaRouter);
    const srv = app.listen(0); const port = (srv.address() as any).port;
    const r = await fetch(`http://127.0.0.1:${port}/demo-api/persona/switch`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ persona: 'alice' }) });
    console.log('PROBE status', r.status, 'set-cookie', JSON.stringify(r.headers.get('set-cookie')), 'body', await r.text());
    srv.close();
    expect(r.status).toBe(500);
  });
});
