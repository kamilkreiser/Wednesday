import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
import http from 'node:http';
import express from 'express';

const savedEnv = { ...process.env };
process.env.NODE_ENV = 'staging';
process.env.API_GATEWAY_URL = 'http://gw.example:1';
delete process.env.ISSUER_PORTAL_URL; delete process.env.VERIFIER_PORTAL_URL; delete process.env.ADMIN_PORTAL_URL;

vi.mock('../services/redis', () => ({ getRedisHealth: vi.fn(async () => ({ status: 'healthy' })) }));
vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('offline in test'); }));

let server: ReturnType<ReturnType<typeof express>['listen']>; let port = 0;
beforeAll(async () => {
  const router = (await import('../routes/system-status')).default;
  const app = express(); app.use('/api/system', router);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { port = (server.address() as any).port; r(); }); });
}, 10_000);
afterAll(async () => {
  await new Promise<void>((r) => server.close(() => r()));
  for (const k of Object.keys(process.env)) if (!(k in savedEnv)) delete process.env[k];
  Object.assign(process.env, savedEnv);
  vi.unstubAllGlobals();
});
function getJson(path: string): Promise<any> {
  return new Promise((resolve, reject) => {
    http.get({ hostname: '127.0.0.1', port, path }, (res) => {
      let data = ''; res.on('data', (c) => (data += c));
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
    }).on('error', reject);
  });
}
async function flatServices(): Promise<Array<{ name?: string; url?: string }>> {
  const body = await getJson('/api/system/status');
  return Object.values(body.services).flat() as any;
}

describe('KS-864 — dead-estate portal URLs removed from runtime source', () => {
  it('🔴 KS-864 B — the issuer portal falls back to its compose default under NODE_ENV=staging when its env var is unset', async () => {
    expect((await flatServices()).find((s) => s.name === 'issuer-portal')?.url).toBe('http://issuer-frontend:80');
  });

  it('🔴 KS-864 B — no portal URL names the dead estate', async () => {
    const portals = (await flatServices()).filter(s => ['issuer-portal', 'verifier-portal', 'admin-portal'].includes(s.name ?? ''));
    for (const s of portals) {
      expect(s.url ?? '').not.toContain('secuura-staging-');
    }
  });

  it('KS-864 B control — an explicit env var still wins for a helper-built service', async () => {
    const entry = (await flatServices()).find((s) => s.name === 'api-gateway');
    expect(entry?.url).toBe('http://gw.example:1');
  });
});
