/**
 * QA Gate 189 (Wednesday), PR 2001 / KS-1256. Independent base-vs-head matrix harness.
 * Written by the gate, not copied from the seat. Drives the REAL routers over real HTTP (express on 127.0.0.1:0):
 *   create (routes/verification.ts POST /api/documents), info (services/health.ts GET /api/connector/info,
 *   with the real authenticateToken(true) and an api-key cache entry), put (routes/admin.ts PUT /api/admin/settings).
 * Doubles: Redis (up / down = in-memory fallback / throws) and Postgres (honours the three statements' semantics).
 * Output: one JSON line per cell to $G189_OUT. Same file runs at head and at base (develop readers swapped in).
 */
import { describe, it, beforeAll, afterAll, expect } from 'vitest';
import express from 'express';
import http from 'node:http';
import fs from 'node:fs';
import type { AddressInfo } from 'node:net';
import type { RequestHandler } from 'express';
import { apiKeyCache, connectorBearerCache } from '../middleware/auth';
import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';

const OUT = process.env.G189_OUT || '';
const ONLY = process.env.G189_ONLY || ''; // optional filter "redis/key/row"
const C = 'g189-conn-7';
const APIKEY = 'sk_g189_matrix_key';
const META = { connectorId: C, scopes: ['documents:write'], organizationId: 'org-g189', tenantId: 'ten-g189', rateLimit: 1e9, rateLimitWindow: 60 };
const DEFAULTS = {
  general: { platformName: 'Secuura', defaultLanguage: 'en', maintenanceMode: false },
  security: { mfaRequired: false, sessionTimeout: 3600, passwordPolicy: 'strong' },
  notifications: { emailEnabled: true, slackEnabled: false, webhookUrl: '' },
  blockchain: { network: 'preprod', confirmationBlocks: 6, autoAnchor: false },
};
const CFG: Record<string, unknown> = {
  R: { ...DEFAULTS, integrations: [{ id: C, config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }] },
  O: { ...DEFAULTS, integrations: [{ id: C, config: { name: 'open' } }] },
  S: { ...DEFAULTS },
  B: { ...DEFAULTS, integrations: [{ id: C, config: { allowedDocumentTypes: ['SSD_DOCUMENT'], workflowPolicy: 'bypass' } }] },
};
const REDIS_MODES = ['up', 'down', 'throws'] as const;
const KEYS = ['R', 'O', 'S', 'B', 'missing'] as const;
const ROWS = ['R', 'O', 'S', 'B', 'missing', 'db-down', 'read-throws', 'not-object'] as const;
const READERS = ['create-out', 'create-in', 'create-default', 'info', 'put'] as const;
const clone = (v: unknown) => (v === null || v === undefined ? null : JSON.parse(JSON.stringify(v)));

// ---- doubles ----
const rs = { mode: 'up' as string, redisVal: null as unknown, mem: null as unknown, sets: 0 };
const redisDouble = {
  isRedisAvailable: () => rs.mode !== 'down',
  getNotificationSettings: async (_k: string) => {
    if (rs.mode === 'throws') throw new Error('g189 redis read fault');
    return clone(rs.mode === 'down' ? rs.mem : rs.redisVal) as object | null;
  },
  setNotificationSettings: async (_k: string, data: object) => {
    if (rs.mode === 'throws') throw new Error('g189 redis write fault');
    rs.sets += 1;
    if (rs.mode === 'down') rs.mem = clone(data); else rs.redisVal = clone(data);
  },
};
const pg = { mode: 'ok' as string, row: null as null | { settings: unknown; origin: string }, verbs: [] as string[] };
const dbQuery = async (text: string, params: unknown[] = []) => {
  if (!/svc_gateway_settings/.test(text)) return { rows: [], rowCount: 0 };
  const verb = text.trim().split(/\s+/)[0].toUpperCase();
  pg.verbs.push(verb);
  if (verb === 'SELECT') {
    if (pg.mode === 'read-throws') throw new Error('g189 db read fault');
    if (!pg.row) return { rows: [], rowCount: 0 };
    return { rows: [{ settings: clone(pg.row.settings) }], rowCount: 1 };
  }
  if (verb === 'INSERT') { pg.row = { settings: JSON.parse(String(params[1])), origin: 'put' }; return { rows: [], rowCount: 1 }; }
  if (verb === 'UPDATE') {
    if (!pg.row || pg.row.origin !== 'seed') return { rows: [], rowCount: 0 };
    pg.row = { settings: JSON.parse(String(params[1])), origin: 'backfill' };
    return { rows: [], rowCount: 1 };
  }
  throw new Error('g189 unexpected verb ' + verb);
};
const isDbAvailable = () => pg.mode !== 'db-down';

let resetBackfill: () => void = () => undefined;
let wfCalls = 0;
const realFetch = globalThis.fetch;
let gw: http.Server; let gwPort = 0;
let orig: http.Server; let origPort = 0; let origHits = 0;

async function call(method: string, path: string, headers: Record<string, string>, body?: unknown) {
  try {
    const r = await realFetch(`http://127.0.0.1:${gwPort}${path}`, {
      method, headers: { 'Content-Type': 'application/json', ...headers },
      body: body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(1500),
    });
    const txt = await r.text();
    let j: any = null; try { j = JSON.parse(txt); } catch { j = txt; }
    return { status: r.status, body: j };
  } catch (e) {
    return { status: -1, body: { hang: (e as Error).name } };
  }
}
async function create(docType: string | undefined) {
  wfCalls = 0; origHits = 0;
  const body: Record<string, unknown> = { title: 'G189', contentHash: 'a'.repeat(64) };
  if (docType !== undefined) body.documentType = docType;
  const r = await call('POST', '/api/documents', { Authorization: 'Bearer g189' }, body);
  const path = r.status >= 200 && r.status < 300 ? (origHits ? 'orig' : wfCalls ? 'wf' : 'pass?') : null;
  return { status: r.status, code: r.body?.error?.code ?? null, path };
}
async function info() {
  const r = await call('GET', '/api/connector/info', { 'x-api-key': APIKEY });
  return { status: r.status, code: r.body?.error?.code ?? null, types: r.status === 200 ? r.body.allowedDocumentTypes : null, policy: r.status === 200 ? r.body.workflowPolicy : null };
}
async function put() {
  const r = await call('PUT', '/api/admin/settings', { Authorization: 'Bearer g189-admin' }, { general: { platformName: 'G189-put' } });
  return { status: r.status, code: r.body?.error?.code ?? null };
}

function setState(redis: string, key: string, row: string) {
  resetBackfill();
  const kv = key === 'missing' ? null : clone(CFG[key]);
  rs.mode = redis; rs.redisVal = kv; rs.mem = redis === 'down' ? kv : null; rs.sets = 0;
  pg.verbs = [];
  pg.mode = row === 'db-down' ? 'db-down' : row === 'read-throws' ? 'read-throws' : 'ok';
  if (['R', 'O', 'B'].includes(row)) pg.row = { settings: clone(CFG[row]), origin: 'put' };
  else if (row === 'S') pg.row = { settings: clone(CFG.S), origin: 'seed' };
  else if (row === 'not-object') pg.row = { settings: ['not', 'an', 'object'], origin: 'put' };
  else if (row === 'db-down' || row === 'read-throws') pg.row = { settings: clone(CFG.R), origin: 'put' };
  else pg.row = null;
}

beforeAll(async () => {
  try {
    const p = '../services/settingsStore';
    const store = (await import(/* @vite-ignore */ p)) as { resetSettingsBackfillState?: () => void };
    if (store.resetSettingsBackfillState) resetBackfill = store.resetSettingsBackfillState;
  } catch { /* base: no settings store */ }
  apiKeyCache.set(APIKEY, { result: META as never, expiresAt: Date.now() + 3_600_000 });
  connectorBearerCache.set(APIKEY, { token: 'g189.connector.jwt', expiresAt: Date.now() + 3_600_000 });
  globalThis.fetch = (async () => ({ ok: false, status: 404, json: async () => ({}), text: async () => '' })) as never;

  orig = http.createServer((req, res) => { origHits += 1; req.resume(); req.on('end', () => { res.writeHead(201, { 'Content-Type': 'application/json' }); res.end(JSON.stringify({ success: true, data: { g189: 'orig' } })); }); });
  await new Promise<void>((r) => orig.listen(0, '127.0.0.1', () => r()));
  origPort = (orig.address() as AddressInfo).port;

  const settingsDb = { query: dbQuery as never, isDbAvailable };
  const { createHealthRoutes } = await import('../services/health');
  const { createVerificationRoutes } = await import('../routes/verification');
  const pass: RequestHandler = (_q, _s, n) => n();
  const app = express();
  app.use((createHealthRoutes as unknown as (...a: unknown[]) => express.Router)({}, { ...redisDouble, getRedisClient: () => null }, settingsDb));
  app.use(createAdminRoutes({
    authenticateToken: () => pass,
    parseTestToken: () => ({ userId: 'g189-admin', email: 'g189@test.invalid', role: 'SYSTEM_ADMIN', verificationLevel: 'BASIC' }),
    query: dbQuery, isDbAvailable, redisService: redisDouble, services: {}, log: () => undefined,
  } as unknown as AdminRouteDeps));
  app.use(createVerificationRoutes({
    authenticateToken: () => (req, _res, next) => {
      (req as any).user = { userId: `connector:${C}`, email: 'c@test.invalid', role: 'connector', organizationId: 'org-g189', verificationLevel: 'api_key', authMethod: 'api_key', connectorId: C, rateLimit: 1e9, rateLimitWindow: 60, scopes: ['documents:write'], tenantId: 'ten-g189' };
      (req as any).connectorMeta = { ...META };
      next();
    },
    mockBodyParser: express.json({ limit: '1mb' }),
    query: dbQuery as never, isDbAvailable,
    redisService: {
      ...redisDouble,
      getPendingDocument: async () => null, deletePendingDocument: async () => undefined,
      getAllDocumentTypes: async () => [], getAllWorkflowInstances: async () => [],
      getRejectedDocument: async () => null, setRejectedDocument: async () => undefined,
      getWorkflowDocumentMapping: async () => null, getWorkflowInstance: async () => null, setWorkflowInstance: async () => undefined,
    } as never,
    services: { originate: { url: `http://127.0.0.1:${origPort}` }, anchoring: { url: 'http://127.0.0.1:1' } } as never,
    log: () => undefined, memWorkflowToDocumentMap: new Map(), memRejectedDocuments: new Map(), dbSaveRejection: async () => undefined,
    ADMIN_ROLES: ['ADMIN', 'admin'],
    enforceDocumentTypeRules: (async () => ({ ok: true, docType: {} })) as never,
    createWorkflowInstanceIfRequired: (async () => { wfCalls += 1; return { gated: true, response: { success: true, data: { g189: 'wf' } } }; }) as never,
  } as never));
  gw = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => gw.once('listening', () => r()));
  gwPort = (gw.address() as AddressInfo).port;
});

afterAll(async () => {
  globalThis.fetch = realFetch;
  await new Promise<void>((r) => gw.close(() => r()));
  await new Promise<void>((r) => orig.close(() => r()));
});

describe('G189 matrix', () => {
  it('runs every cell and writes one line per cell', async () => {
    const lines: string[] = [];
    for (const redis of REDIS_MODES) for (const key of KEYS) for (const row of ROWS) {
      if (ONLY && ONLY !== `${redis}/${key}/${row}`) continue;
      for (const reader of READERS) {
        setState(redis, key, row);
        let out: Record<string, unknown>;
        if (reader === 'create-out') out = await create('diploma');
        else if (reader === 'create-in') out = await create('SSD_DOCUMENT');
        else if (reader === 'create-default') out = await create(undefined);
        else if (reader === 'info') out = await info();
        else {
          const p = await put();
          const redisAfter = clone(redis === 'down' ? rs.mem : rs.redisVal);
          const rowAfter = pg.row ? { origin: pg.row.origin } : null;
          const sets = rs.sets;
          // follow-up: Redis back UP (its own store untouched), same DB; what does a restricted create see now?
          rs.mode = 'up';
          const f = await create('diploma');
          out = { ...p, sets, rowOriginAfter: rowAfter?.origin ?? null, redisAfterHasIntegrations: !!(redisAfter as any)?.integrations, follow: f };
        }
        lines.push(JSON.stringify({ reader, redis, key, row, ...out, dbVerbs: pg.verbs.join(',') }));
      }
    }
    if (OUT) fs.writeFileSync(OUT, lines.join('\n') + '\n');
    expect(lines.length).toBeGreaterThan(0);
  }, 300_000);
});
