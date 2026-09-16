import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
import http from 'node:http';
import express from 'express';

const savedEnv = { ...process.env };
process.env.NODE_ENV = 'staging';
process.env.ANCHORING_SERVICE_URL = 'http://anch.example:1';
delete process.env.API_GATEWAY_URL;

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

describe('KS-864 A — dead Azure estate pointers removed from runtime source', () => {
  it('🔴 KS-864 A — api-gateway falls back to its localhost default under NODE_ENV=staging when its env var is unset', async () => {
    const services = await flatServices();
    const gw = services.find((s) => s.name === 'api-gateway')?.url;
    expect(gw).toBe('http://localhost:8080');
  });

  it('🔴 KS-864 A — no served URL names the internal dead estate', async () => {
    const services = await flatServices();
    for (const s of services) {
      expect(s.url ?? '').not.toContain('.internal.ashypond');
    }
  });

  it('KS-864 A control — an explicit env var still wins', async () => {
    const services = await flatServices();
    const anchoring = services.find((s) => s.name === 'anchoring');
    expect(anchoring?.url).toBe('http://anch.example:1');
  });
});
