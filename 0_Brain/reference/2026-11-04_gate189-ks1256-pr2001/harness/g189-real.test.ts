/**
 * QA Gate 189: real Redis (container g189-redis, 127.0.0.1:56389, allkeys-lru) + real Postgres 15 (gate's own cluster,
 * 127.0.0.1:56390, db from $G189_DB, migration 057 applied as the app role's default privileges allow).
 * The REAL gateway modules: services/redis (ioredis), db (pg pool via queryWithTenantGuc), and the three routers wired
 * as index.ts wires them (health with its DEFAULT settingsDb). Only auth (pass-through), document-type enforcement
 * and the workflow gate are stand-ins, as in the matrix. One JSON line per step to $G189_OUT.
 * $G189_SIDE = head | base (base = develop's three readers swapped in; it never touches the table).
 */
import { describe, it, beforeAll, afterAll, expect } from 'vitest';
import express from 'express';
import http from 'node:http';
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import type { AddressInfo } from 'node:net';
import type { RequestHandler } from 'express';
import pg from 'pg';
import * as redisService from '../services/redis';
import { initDb, query, isDbAvailable, closeDb } from '../db';
import { apiKeyCache, connectorBearerCache } from '../middleware/auth';
import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
import { logger } from '../utils/logger';

const OUT = process.env.G189_OUT!;
const SIDE = process.env.G189_SIDE || 'head';
const DBNAME = process.env.G189_DB || 'g189';
const C = 'g189-conn-real';
const APIKEY = 'sk_g189_real_key';
const MARK = 'G189MARK';
const META = { connectorId: C, scopes: ['documents:write'], organizationId: 'org-g189', tenantId: 'ten-g189', rateLimit: 1e9, rateLimitWindow: 60 };
const RKEY = 'secuura:gateway:notif:platform-settings';
const RESTRICTED = { integrations: [{ id: C, name: `${MARK}_NAME`, config: { allowedDocumentTypes: ['SSD_DOCUMENT', `${MARK}_TYPE`] } }] };
const OPEN = { integrations: [{ id: C, name: `${MARK}_OPEN`, config: {} }] };
const lines: string[] = [];
const rec = (step: string, o: Record<string, unknown>) => { lines.push(JSON.stringify({ side: SIDE, step, ...o })); };

const dk = (...a: string[]) => execFileSync('docker', ['exec', 'g189-redis', 'redis-cli', ...a], { encoding: 'utf8' }).trim();
let su: pg.Client;
const realFetch = globalThis.fetch;
let gw: http.Server; let gwPort = 0; let orig: http.Server; let origPort = 0; let origHits = 0; let wfCalls = 0;

async function call(method: string, path: string, headers: Record<string, string>, body?: unknown) {
  try {
    const r = await realFetch(`http://127.0.0.1:${gwPort}${path}`, { method, headers: { 'Content-Type': 'application/json', ...headers }, body: body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(8000) });
    const t = await r.text(); let j: any; try { j = JSON.parse(t); } catch { j = t; }
    return { status: r.status, body: j, raw: t };
  } catch (e) { return { status: -1, body: { hang: (e as Error).name }, raw: '' }; }
}
async function create(docType?: string) {
  wfCalls = 0; origHits = 0;
  const b: Record<string, unknown> = { title: 'G189 real', contentHash: 'b'.repeat(64) };
  if (docType) b.documentType = docType;
  const r = await call('POST', '/api/documents', { Authorization: 'Bearer g189' }, b);
  return { status: r.status, code: r.body?.error?.code ?? null, path: r.status === 201 ? (origHits ? 'orig' : wfCalls ? 'wf' : '?') : null, raw: r.raw };
}
async function info() { const r = await call('GET', '/api/connector/info', { 'x-api-key': APIKEY }); return { status: r.status, code: r.body?.error?.code ?? null, types: r.body?.allowedDocumentTypes ?? null, raw: r.raw }; }
async function put(body: unknown) { const r = await call('PUT', '/api/admin/settings', { Authorization: 'Bearer g189-admin' }, body); return { status: r.status, code: r.body?.error?.code ?? null, message: r.body?.error?.message ?? null, raw: r.raw }; }
async function getAdmin() { const r = await call('GET', '/api/admin/settings', { Authorization: 'Bearer g189-admin' }); return { status: r.status, hasIntegrations: !!r.body?.settings?.integrations, raw: r.raw }; }
async function row() { try { const r = await su.query('SELECT origin, settings FROM svc_gateway_settings'); return r.rows[0] ? { origin: r.rows[0].origin, restricted: JSON.stringify(r.rows[0].settings).includes('SSD_DOCUMENT'), keys: Object.keys(r.rows[0].settings).sort().join(',') } : null; } catch (e) { return { err: (e as Error).message.slice(0, 80) }; } }
function rkey() { const v = dk('GET', RKEY); return v === '' ? null : { restricted: v.includes('SSD_DOCUMENT'), open: v.includes(`${MARK}_OPEN`), len: v.length }; }
const strip = (o: any) => { const { raw, ...rest } = o; return rest; };
const allRaw: string[] = [];
const keep = (...os: any[]) => { for (const o of os) if (o?.raw) allRaw.push(o.raw); };
const waitFor = async (f: () => boolean, ms: number) => { const t = Date.now(); while (!f() && Date.now() - t < ms) await new Promise((r) => setTimeout(r, 100)); return f(); };

beforeAll(async () => {
  su = new pg.Client({ host: '127.0.0.1', port: 56390, user: 'g189su', database: DBNAME });
  await su.connect();
  dk('FLUSHALL');
  await redisService.initRedis();
  await initDb();
  rec('boot', { redisAvailable: redisService.isRedisAvailable(), dbAvailable: isDbAvailable() });
  apiKeyCache.set(APIKEY, { result: META as never, expiresAt: Date.now() + 3_600_000 });
  connectorBearerCache.set(APIKEY, { token: 'g189.connector.jwt', expiresAt: Date.now() + 3_600_000 });
  globalThis.fetch = (async () => ({ ok: false, status: 404, json: async () => ({}), text: async () => '' })) as never;
  orig = http.createServer((q, s) => { origHits += 1; q.resume(); q.on('end', () => { s.writeHead(201, { 'Content-Type': 'application/json' }); s.end('{"success":true}'); }); });
  await new Promise<void>((r) => orig.listen(0, '127.0.0.1', () => r()));
  origPort = (orig.address() as AddressInfo).port;
  const { createHealthRoutes } = await import('../services/health');
  const { createVerificationRoutes } = await import('../routes/verification');
  const pass: RequestHandler = (_q, _s, n) => n();
  const app = express();
  app.use(createHealthRoutes({}, redisService as never)); // as index.ts:855 wires it (default settingsDb)
  app.use(createAdminRoutes({ authenticateToken: () => pass, parseTestToken: () => ({ userId: 'g189-admin', email: 'g189@test.invalid', role: 'SYSTEM_ADMIN', verificationLevel: 'BASIC' }), query: query as never, isDbAvailable, redisService: redisService as never, services: {}, log: (l: string, m: string, meta?: object) => (logger as any)[l](m, meta) } as unknown as AdminRouteDeps));
  app.use(createVerificationRoutes({
    authenticateToken: () => (req, _res, next) => { (req as any).user = { userId: `connector:${C}`, email: 'c@test.invalid', role: 'connector', organizationId: 'org-g189', verificationLevel: 'api_key', authMethod: 'api_key', connectorId: C, rateLimit: 1e9, rateLimitWindow: 60, scopes: ['documents:write'], tenantId: 'ten-g189' }; (req as any).connectorMeta = { ...META }; next(); },
    mockBodyParser: express.json({ limit: '1mb' }), query: query as never, isDbAvailable, redisService: redisService as never,
    services: { originate: { url: `http://127.0.0.1:${origPort}` }, anchoring: { url: 'http://127.0.0.1:1' } } as never,
    log: (l: string, m: string, meta?: object) => (logger as any)[l](m, meta), memWorkflowToDocumentMap: new Map(), memRejectedDocuments: new Map(), dbSaveRejection: async () => undefined,
    ADMIN_ROLES: ['ADMIN', 'admin'],
    enforceDocumentTypeRules: (async () => ({ ok: true, docType: {} })) as never,
    createWorkflowInstanceIfRequired: (async () => { wfCalls += 1; return { gated: true, response: { success: true } }; }) as never,
  } as never));
  gw = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => gw.once('listening', () => r()));
  gwPort = (gw.address() as AddressInfo).port;
});

afterAll(async () => {
  globalThis.fetch = realFetch;
  await new Promise<void>((r) => gw.close(() => r()));
  await new Promise<void>((r) => orig.close(() => r()));
  try { await redisService.getRedisClient()?.quit(); } catch { /* down */ }
  try { redisService.getRedisClient()?.disconnect(); } catch { /* */ }
  await closeDb();
  await su.end();
});

describe('G189 real stack', () => {
  it('runs the sequence', async () => {
    // 1. FIRST BOOT: fresh DB (057 applied, seed row), empty Redis.
    let a = await create('diploma'), b = await create('SSD_DOCUMENT'), c = await create(), i = await info(), g = await getAdmin();
    keep(a, b, c, i, g);
    rec('1 first-boot', { createOut: strip(a), createIn: strip(b), createDefault: strip(c), info: strip(i), adminGet: strip(g), redisAfter: rkey(), row: await row() });

    // 2. PUT a restricted config (marker inside).
    let p = await put(RESTRICTED); keep(p);
    rec('2 put restricted', { put: strip(p), redis: rkey(), row: await row() });

    // 3. key present.
    a = await create('diploma'); b = await create('SSD_DOCUMENT'); i = await info(); keep(a, b, i);
    rec('3 key present', { createOut: strip(a), createIn: strip(b), info: strip(i) });

    // 4. key DELETED with Redis up (eviction stand-in).
    dk('DEL', RKEY);
    a = await create('diploma'); const redisAfterOut = rkey(); dk('DEL', RKEY);
    b = await create('SSD_DOCUMENT'); dk('DEL', RKEY); i = await info(); keep(a, b, i);
    rec('4 key deleted, row present', { createOut: strip(a), redisAfterCreateOut: redisAfterOut, createIn: strip(b), info: strip(i), redisAfterInfo: rkey() });

    // 5. REAL allkeys-lru eviction.
    if (!rkey()) await create('SSD_DOCUMENT');
    dk('CONFIG', 'SET', 'maxmemory', '3mb');
    let n = 0; const filler = 'x'.repeat(20000);
    while (dk('EXISTS', RKEY) === '1' && n < 2000) { dk('SET', `g189:fill:${n}`, filler); n += 1; }
    const evicted = dk('EXISTS', RKEY) === '0';
    const ev = dk('INFO', 'stats').split('\n').find((l) => l.startsWith('evicted_keys')) || '';
    a = await create('diploma'); keep(a);
    const afterEvict = rkey();
    rec('5 real eviction', { fillerKeys: n, keyEvicted: evicted, stat: ev.trim(), createOut: strip(a), redisAfter: afterEvict });
    dk('CONFIG', 'SET', 'maxmemory', '256mb');
    for (const k of dk('KEYS', 'g189:fill:*').split('\n').filter(Boolean)) dk('DEL', k);

    // 6. key missing AND row missing.
    const saved = (await su.query('SELECT settings, origin FROM svc_gateway_settings')).rows[0];
    await su.query('DELETE FROM svc_gateway_settings'); dk('DEL', RKEY);
    a = await create('diploma'); b = await create('SSD_DOCUMENT'); i = await info(); p = await put({ general: { platformName: 'x' } }); keep(a, b, i, p);
    rec('6 key + row missing', { createOut: strip(a), createIn: strip(b), info: strip(i), put: strip(p), redis: rkey(), row: await row() });
    await su.query("INSERT INTO svc_gateway_settings (key, settings, origin) VALUES ('platform-settings', $1::jsonb, $2)", [JSON.stringify(saved.settings), saved.origin]);
    // 6b. key missing, row present but SELECT denied to the app role (a real failed read).
    await su.query('REVOKE SELECT ON svc_gateway_settings FROM g189app'); dk('DEL', RKEY);
    a = await create('diploma'); i = await info(); keep(a, i);
    rec('6b key missing, row unreadable (SELECT revoked)', { createOut: strip(a), info: strip(i) });
    await su.query('GRANT SELECT ON svc_gateway_settings TO g189app');
    p = await put(RESTRICTED); keep(p);
    rec('6c restore', { put: strip(p), redis: rkey(), row: await row() });

    // 7. PUT: DB write fails (INSERT/UPDATE revoked) -> response, Redis untouched?
    const before7 = dk('GET', RKEY);
    await su.query('REVOKE INSERT, UPDATE ON svc_gateway_settings FROM g189app');
    p = await put(OPEN); keep(p);
    const after7 = dk('GET', RKEY);
    rec('7 put, DB write fails', { put: strip(p), redisUnchanged: before7 === after7, redis: rkey(), row: await row() });
    await su.query('GRANT INSERT, UPDATE ON svc_gateway_settings TO g189app');

    // 8. PUT: DB write ok, Redis write fails (noeviction + maxmemory 1 -> OOM on SET; GET still works).
    dk('CONFIG', 'SET', 'maxmemory-policy', 'noeviction'); dk('CONFIG', 'SET', 'maxmemory', '1');
    p = await put(OPEN); keep(p);
    const r8 = rkey(); const row8 = await row();
    a = await create('diploma'); keep(a);
    dk('CONFIG', 'SET', 'maxmemory', '256mb'); dk('CONFIG', 'SET', 'maxmemory-policy', 'allkeys-lru');
    rec('8 put, Redis write fails after DB', { put: strip(p), redis: r8, row: row8, createOutWhileStale: strip(a) });
    dk('DEL', RKEY); const a8 = await create('diploma'); keep(a8);
    rec('8b stale cache then eviction', { createOut: strip(a8), redis: rkey() });
    p = await put(RESTRICTED); keep(p); rec('8c restore', { put: strip(p), redis: rkey(), row: await row() });

    // 9. malformed bytes in Redis (marker inside) -> each reader; then leak scan covers the logs.
    dk('SET', RKEY, `${MARK}_BYTES{not json`);
    a = await create('diploma'); i = await info(); p = await put({ general: { platformName: 'y' } }); keep(a, i, p);
    rec('9 malformed bytes', { createOut: strip(a), info: strip(i), put: strip(p) });
    dk('DEL', RKEY); p = await put(RESTRICTED); keep(p);

    // 10. Redis DOWN (container stopped): readers, and a PUT during the outage.
    logger.warn('g189 positive control', { v: `${MARK}_CTRL` });
    execFileSync('docker', ['stop', '-t', '1', 'g189-redis']);
    const down = await waitFor(() => !redisService.isRedisAvailable(), 15000);
    a = await create('diploma'); b = await create('SSD_DOCUMENT'); i = await info(); p = await put(OPEN); keep(a, b, i, p);
    rec('10 redis down', { observedDown: down, createOut: strip(a), createIn: strip(b), info: strip(i), putDuringOutage: strip(p), row: await row() });

    fs.writeFileSync(OUT, lines.join('\n') + '\n');
    fs.writeFileSync(OUT + '.bodies.txt', allRaw.join('\n') + '\n');
    expect(lines.length).toBeGreaterThan(5);
  }, 240_000);
});
