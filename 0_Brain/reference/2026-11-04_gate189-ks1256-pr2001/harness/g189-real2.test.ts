/**
 * QA Gate 189: the deploy step 3 discriminator ("a configured env should read `backfill`, a fresh one `seed`"),
 * on real Redis (g189-redis) + real Postgres (gate cluster), real modules, GET /api/connector/info as index.ts wires it.
 */
import { it, beforeAll, afterAll, expect } from 'vitest';
import express from 'express';
import http from 'node:http';
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import type { AddressInfo } from 'node:net';
import pg from 'pg';
import * as redisService from '../services/redis';
import { initDb, closeDb } from '../db';
import { apiKeyCache, connectorBearerCache } from '../middleware/auth';

const OUT = process.env.G189_OUT!;
const DBNAME = process.env.G189_DB!;
const C = 'g189-conn-real2'; const APIKEY = 'sk_g189_real2';
const META = { connectorId: C, scopes: ['documents:write'], organizationId: 'o', tenantId: 't', rateLimit: 1e9, rateLimitWindow: 60 };
const RKEY = 'secuura:gateway:notif:platform-settings';
const dk = (...a: string[]) => execFileSync('docker', ['exec', 'g189-redis', 'redis-cli', ...a], { encoding: 'utf8' }).trim();
let su: pg.Client; let gw: http.Server; let port = 0; const realFetch = globalThis.fetch;
const out: string[] = [];
const origin = async () => (await su.query('SELECT origin, settings::text AS s FROM svc_gateway_settings')).rows.map((r) => ({ origin: r.origin, restricted: r.s.includes('SSD_DOCUMENT') }))[0];
const info = async () => { const r = await realFetch(`http://127.0.0.1:${port}/api/connector/info`, { headers: { 'x-api-key': APIKEY } }); const j: any = await r.json(); return `${r.status} ${JSON.stringify(j.allowedDocumentTypes ?? j.error?.code)}`; };
async function reseed() {
  await su.query('DELETE FROM svc_gateway_settings');
  const sql = fs.readFileSync(process.env.G189_MIG!, 'utf8');
  await su.query(sql);
}
beforeAll(async () => {
  su = new pg.Client({ host: '127.0.0.1', port: 56390, user: 'g189su', database: DBNAME }); await su.connect();
  dk('FLUSHALL'); await redisService.initRedis(); await initDb();
  apiKeyCache.set(APIKEY, { result: META as never, expiresAt: Date.now() + 3_600_000 });
  connectorBearerCache.set(APIKEY, { token: 'x', expiresAt: Date.now() + 3_600_000 });
  globalThis.fetch = (async () => ({ ok: false, status: 404, json: async () => ({}), text: async () => '' })) as never;
  const { createHealthRoutes } = await import('../services/health');
  const app = express(); app.use(createHealthRoutes({}, redisService as never));
  gw = app.listen(0, '127.0.0.1'); await new Promise<void>((r) => gw.once('listening', () => r()));
  port = (gw.address() as AddressInfo).port;
});
afterAll(async () => {
  globalThis.fetch = realFetch; await new Promise<void>((r) => gw.close(() => r()));
  await redisService.getRedisClient()?.quit(); await closeDb(); await su.end();
});
it('step-3 discriminator', async () => {
  const resetBackfill = (await import('../services/settingsStore')).resetSettingsBackfillState;
  const scen = async (name: string, redisValue: string | null) => {
    await reseed(); dk('FLUSHALL'); resetBackfill();
    if (redisValue) dk('SET', RKEY, redisValue);
    const r1 = await info(); const o1 = await origin();
    const r2 = await info(); const o2 = await origin();
    out.push(JSON.stringify({ scenario: name, afterFirstGet: { answer: r1, row: o1 }, afterSecondGet: { answer: r2, row: o2 } }));
  };
  await scen('fresh env (no key, seed row)', null);
  await scen('configured env, key present at deploy', JSON.stringify({ integrations: [{ id: C, config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }] }));
  await scen('configured env, key ALREADY evicted at deploy', null);
  fs.writeFileSync(OUT, out.join('\n') + '\n');
  expect(out.length).toBe(3);
}, 60_000);
