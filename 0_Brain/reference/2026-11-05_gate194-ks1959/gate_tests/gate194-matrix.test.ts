/**
 * Gate 194 (KS-1959, PR 2005) matrix harness. Written by the gate (adapted from gate 191's gate191-matrix.test.ts), not by the seat.
 * REAL: credentialRepo, revocationResolvers, the shared verifier, the credentials and presentations routers,
 * errorHandler, helmet, cors, boundedJson, rejectNulBytes, express, and a real HTTP server on 127.0.0.1:<ephemeral>.
 * REPLACED: ../db (an in-memory table whose INSERT / SELECT / UPDATE can be made to throw, and whose UPDATE result's
 * rowCount can be chosen: real count, 0, null, undefined, key absent) and ../utils/logger (captures warn/error).
 * index.ts is NOT booted; jwtAuthenticate is replaced by a fake-user middleware (x-g194-user). Verify calls carry no user.
 * Every cell appends one JSON line to $G194_OUT. Cells never assert: the compare script reads the lines.
 * The RESTART cells (q5) build a SECOND app over fresh module instances (vi.resetModules) against the SAME table and
 * drive its real loadFromDb, i.e. a fresh process; they run last.
 */
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import fs from 'fs';
import type { AddressInfo } from 'net';

type Row = { credential: any; userId: string | null; tenantId: string | null };
const h = vi.hoisted(() => ({
  db: new Map<string, Row>(),
  available: true,
  insertFailOn: false,
  selectFail: undefined as unknown,
  selectFailOn: false,
  updateFail: undefined as unknown,
  updateFailOn: false,
  // how the UPDATE answers when it does not throw: 'real' = rowCount = rows matched (pg's semantics);
  // 'zero' = rowCount 0 and NO write; 'null' | 'undefined' | 'absent' = that rowCount, with ('W') or without ('N') the write
  updateMode: 'real' as string,
  updateWrites: true,
  selects: 0,
  updates: 0,
  warns: [] as Array<{ msg: string; meta: any }>,
}));

vi.mock('../db', () => ({
  isDbAvailable: () => h.available,
  initDb: async () => true,
  closeDb: async () => {},
  query: (sql: string, params: any[] = []) => {
    if (/LIMIT 0/i.test(sql)) return Promise.resolve({ rows: [], rowCount: 0 });
    if (/^\s*INSERT/i.test(sql)) {
      if (h.insertFailOn) return Promise.reject(new Error('g194 insert refused'));
      h.db.set(params[0], { credential: JSON.parse(params[1]), userId: params[2] ?? null, tenantId: params[3] ?? null });
      return Promise.resolve({ rows: [], rowCount: 1 });
    }
    if (/^\s*UPDATE/i.test(sql)) {
      h.updates++;
      if (h.updateFailOn) return Promise.reject(h.updateFail);
      const row = h.db.get(params[1]);
      if (h.updateMode === 'real') {
        if (!row) return Promise.resolve({ rows: [], rowCount: 0 });
        h.db.set(params[1], { ...row, credential: JSON.parse(params[0]) });
        return Promise.resolve({ rows: [], rowCount: 1 });
      }
      if (h.updateMode === 'zero') return Promise.resolve({ rows: [], rowCount: 0 });
      if (row && h.updateWrites) h.db.set(params[1], { ...row, credential: JSON.parse(params[0]) });
      if (h.updateMode === 'null') return Promise.resolve({ rows: [], rowCount: null });
      if (h.updateMode === 'undefined') return Promise.resolve({ rows: [], rowCount: undefined });
      return Promise.resolve({ rows: [] }); // 'absent'
    }
    if (/^\s*SELECT/i.test(sql)) {
      h.selects++;
      if (h.selectFailOn) return Promise.reject(h.selectFail);
      if (/WHERE id = \$1/.test(sql)) {
        const row = h.db.get(params[0]);
        return Promise.resolve({
          rows: row ? [{ id: params[0], credential: row.credential, created_by_user_id: row.userId, created_by_tenant_id: row.tenantId }] : [],
          rowCount: row ? 1 : 0,
        });
      }
      if (/FROM vc_credentials_store ORDER BY created_at/i.test(sql)) {
        const rows = Array.from(h.db.entries()).map(([id, r]) => ({ id, credential: r.credential, created_by_user_id: r.userId, created_by_tenant_id: r.tenantId }));
        return Promise.resolve({ rows, rowCount: rows.length });
      }
    }
    return Promise.resolve({ rows: [], rowCount: 0 });
  },
}));
vi.mock('../utils/logger', () => {
  const l = { debug() {}, info() {}, error(msg: string, meta: any) { h.warns.push({ msg: 'ERROR ' + msg, meta }); }, warn(msg: string, meta: any) { h.warns.push({ msg, meta }); } };
  return { logger: l, createLogger: () => l };
});

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { boundedJson, rejectNulBytes, ErrorResponseSchema } from '@secuura/shared';
import * as repo from '../repositories/credentialRepo';
import { credentialRoutes } from '../routes/credentials';
import { presentationRoutes } from '../routes/presentations';
import { errorHandler } from '../middleware/errorHandler';

const OUT = process.env.G194_OUT as string;
const SIDE = process.env.G194_SIDE as string;
const rec = (o: Record<string, unknown>) => fs.appendFileSync(OUT, JSON.stringify({ side: SIDE, ...o }) + '\n');

function mkApp(credR: any, presR: any, eh: any) {
  const app = express();
  app.use(helmet());
  app.use(cors({ origin: ['http://localhost:6100'], credentials: true }));
  app.use(boundedJson({ service: 'vc-issuer', limit: '10mb' }));
  app.use(express.urlencoded({ extended: true }));
  app.use(rejectNulBytes());
  app.use((req: any, _res, next) => {
    if (req.headers['x-g194-user']) req.user = { userId: 'g194-user', role: 'SYSTEM_ADMIN', organizationId: 'org-g194' };
    next();
  });
  app.use('/api/credentials', credR);
  app.use('/api/presentations', presR);
  app.use(eh);
  return app;
}
async function listen(app: any): Promise<{ server: any; url: string }> {
  let server: any;
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  return { server, url: 'http://127.0.0.1:' + (server.address() as AddressInfo).port };
}

let P1 = ''; let server1: any; let server2: any;
beforeAll(async () => {
  const { privateKey } = crypto.generateKeyPairSync('ed25519');
  process.env.VC_SIGNING_KEY = privateKey.export({ type: 'pkcs8', format: 'der' }).toString('hex');
  const s = await listen(mkApp(credentialRoutes, presentationRoutes, errorHandler));
  server1 = s.server; P1 = s.url;
});
afterAll(async () => {
  await new Promise((r) => server1.close(r));
  if (server2) await new Promise((r) => server2.close(r));
});

async function http(base: string, method: string, path: string, body?: unknown, user = false) {
  const t0 = performance.now();
  const r = await fetch(base + path, {
    method,
    headers: { 'content-type': 'application/json', ...(user ? { 'x-g194-user': '1' } : {}) },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await r.text();
  const ms = performance.now() - t0;
  const headers: string[] = [];
  r.headers.forEach((v, k) => headers.push(k + ': ' + v));
  let json: any; try { json = JSON.parse(text); } catch { json = undefined; }
  return { status: r.status, text, json, headers: headers.join('\n'), ms };
}

let seq = 0;
async function issue(tag: string, base = P1) {
  seq++;
  const r = await http(base, 'POST', '/api/credentials', {
    documentId: `doc-g194-${tag}-${seq}`, documentHash: `hash-g194-${tag}-${seq}`,
    documentType: 'PropertyDeed', documentTitle: 'g194 ' + tag,
  }, true);
  if (r.status !== 201 && r.status !== 200) throw new Error('issue failed ' + r.status + ' ' + r.text.slice(0, 300));
  return r.json?.credential ?? r.json?.data?.credential ?? r.json;
}

async function verify(base: string, route: string, doc: any) {
  const s0 = h.selects;
  if (route === 'credentials') {
    const r = await http(base, 'POST', '/api/credentials/verify', { credential: doc });
    return { ...r, selects: h.selects - s0, verified: r.json?.verified, errors: (r.json?.result?.errors ?? []) as string[] };
  }
  const r = await http(base, 'POST', '/api/presentations/verify', {
    presentation: {
      '@context': ['https://www.w3.org/2018/credentials/v1'], type: ['VerifiablePresentation'],
      id: 'urn:uuid:g194-presentation', holder: 'did:secuura:g194-holder', verifiableCredential: [doc],
    },
  });
  const first = r.json?.credentialResults?.[0];
  return { ...r, selects: h.selects - s0, verified: first?.verified, errors: (first?.errors ?? []) as string[] };
}

const TOKEN = 'PLANTED-G194';
class PgLikeError extends Error {
  code = '57P01'; detail = TOKEN + '-DETAIL'; hint = TOKEN + '-HINT'; where = TOKEN + '-WHERE'; severity = 'FATAL';
  constructor() {
    super(TOKEN + '-MSG terminating connection: relation "vc_credentials_store" host db-int-g194.internal');
    this.name = 'error';
    this.stack = 'error: ' + TOKEN + '-STACK\n    at g194 (/srv/vc-issuer/node_modules/pg/lib/client.js:526:17)';
  }
}
const revokedProxy = () => { const rp = Proxy.revocable({}, {}); rp.revoke(); return rp.proxy; };
const getterThrows = () => Object.create(Error.prototype, {
  message: { get() { throw new Error(TOKEN + '-GETTER'); } },
  stack: { value: 'Error: ' + TOKEN + '-STACK\n    at g194 (/srv/vc-issuer/dist/db.js:1:1)' },
});
const SHAPES: Array<[string, () => unknown]> = [['ordinary', () => new PgLikeError()], ['proxy', revokedProxy], ['getter', getterThrows]];
const LEAK = /PLANTED-G194|vc_credentials_store|db-int-g194|57P01|\.ts:\d+|\.js:\d+|node_modules|    at /;
const leak = (s: string) => (LEAK.test(s) ? (s.match(LEAK) || [])[0] : null);
const FIXED_503 = 'The revocation could not be saved. Retry the revoke.';

function reset() {
  h.available = true; h.insertFailOn = false; h.selectFailOn = false; h.updateFailOn = false;
  h.selectFail = undefined; h.updateFail = undefined; h.updateMode = 'real'; h.updateWrites = true; h.warns.length = 0;
}
async function memRevoked(r: any, id: string) {
  const a = h.available; h.available = false;
  try { const c = await r.getById(id); return c ? c.credentialStatus?.revoked === true : 'absent'; } finally { h.available = a; }
}
const dbRevoked = (id: string) => { const row = h.db.get(id); return row ? row.credential?.credentialStatus?.revoked === true : 'no row'; };
function revokeFacts(rv: any) {
  let schema503: string | null = null;
  if (rv.status === 503) { const p = ErrorResponseSchema.safeParse(rv.json); schema503 = p.success ? 'ErrorResponse ok' : 'ErrorResponse FAIL'; }
  return {
    revokeStatus: rv.status, revokeMsg: rv.json?.message ?? rv.json?.error?.message ?? null, revokeCode: rv.json?.error?.code ?? null,
    revokeBodyKeys: Object.keys(rv.json ?? {}), revokeMs: Math.round(rv.ms), revokeBodyLeak: leak(rv.text), revokeHeaderLeak: leak(rv.headers),
    revokeFixed503: rv.status === 503 ? rv.json?.error?.message === FIXED_503 : null, schema503,
    revokeText: rv.status >= 300 ? rv.text.slice(0, 400) : null,
    revokeHeaders: rv.headers.split('\n').map((l: string) => l.split(':')[0]).filter((k: string) => k.startsWith('x-g194')),
  };
}
function out(cell: string, route: string, shape: string, v: any, extra: Record<string, unknown> = {}) {
  const warnText = JSON.stringify(h.warns);
  rec({
    cell, route, shape, status: v.status, verified: v.verified, errors: v.errors, ms: Math.round(v.ms), selects: v.selects,
    bodyLeak: leak(v.text), headerLeak: leak(v.headers),
    warnHasToken: warnText.includes(TOKEN), warnMsgs: h.warns.map((w) => w.msg), ...extra,
  });
}

async function revokeCell(cell: string, route: string, shape: string, setup: () => void, opts: { insertFail?: boolean; noDb?: boolean } = {}) {
  reset();
  if (opts.noDb) h.available = false;
  if (opts.insertFail) h.insertFailOn = true;
  const c = await issue(cell);
  h.insertFailOn = false;
  setup();
  const u0 = h.updates;
  const rv = await http(P1, 'POST', `/api/credentials/${encodeURIComponent(c.id)}/revoke`, { reason: 'g194 ' + cell }, true);
  const updates = h.updates - u0;
  const warnAtRevoke = JSON.stringify(h.warns);
  // the DB is healthy again for the verify (as gate 191 C)
  const keepNoDb = h.available === false; reset(); if (keepNoDb) h.available = false;
  const facts = { ...revokeFacts(rv), updates, dbRowRevoked: dbRevoked(c.id), memRevoked: await memRevoked(repo, c.id), warnAtRevokeHasToken: warnAtRevoke.includes(TOKEN), warnAtRevokeMsgs: JSON.parse(warnAtRevoke).map((w: any) => w.msg) };
  h.warns.length = 0;
  out(cell, route, shape, await verify(P1, route, c), facts);
  reset();
  return c;
}

describe('gate194 matrix', () => {
  for (const route of ['credentials', 'presentations']) {
    for (const [shape, mk] of SHAPES) {
      it(`C ${route} ${shape}`, async () => { await revokeCell('C', route, shape, () => { h.updateFailOn = true; h.updateFail = mk(); }); });
      it(`S ${route} ${shape}`, async () => { await revokeCell('S', route, shape, () => { h.selectFailOn = true; h.selectFail = mk(); }); });
    }
    it(`Z0 ${route}`, async () => { await revokeCell('Z0', route, '-', () => { h.updateMode = 'zero'; }); });
    it(`Zreal ${route}`, async () => { await revokeCell('Zreal', route, '-', () => {}, { insertFail: true }); });
    for (const mode of ['null', 'undefined', 'absent']) {
      it(`N-${mode}-W ${route}`, async () => { await revokeCell('N-' + mode + '-W', route, '-', () => { h.updateMode = mode; h.updateWrites = true; }); });
      it(`N-${mode}-N ${route}`, async () => { await revokeCell('N-' + mode + '-N', route, '-', () => { h.updateMode = mode; h.updateWrites = false; }); });
    }
    it(`H ${route}`, async () => { await revokeCell('H', route, '-', () => {}); });
    it(`M ${route}`, async () => { await revokeCell('M', route, '-', () => {}, { noDb: true }); });
    it(`AR ${route}`, async () => {
      reset(); const c = await issue('AR');
      const first = await http(P1, 'POST', `/api/credentials/${encodeURIComponent(c.id)}/revoke`, { reason: 'g194 AR1' }, true);
      const u0 = h.updates;
      const rv = await http(P1, 'POST', `/api/credentials/${encodeURIComponent(c.id)}/revoke`, { reason: 'g194 AR2' }, true);
      const facts = { ...revokeFacts(rv), firstStatus: first.status, updates: h.updates - u0, dbRowRevoked: dbRevoked(c.id), memRevoked: await memRevoked(repo, c.id) };
      h.warns.length = 0;
      out('AR', route, '-', await verify(P1, route, c), facts); reset();
    });
  }
  // unknown id (no verify read)
  it('UNK', async () => {
    reset(); const u0 = h.updates;
    const rv = await http(P1, 'POST', `/api/credentials/${encodeURIComponent('urn:uuid:g194-unknown')}/revoke`, { reason: 'g194' }, true);
    rec({ cell: 'UNK', route: '-', shape: '-', ...revokeFacts(rv), updates: h.updates - u0, revokeText: rv.text.slice(0, 200) });
  });
  // latency band: 30 healthy revokes (UPDATE count each)
  it('LAT', async () => {
    reset(); const ms: number[] = []; const ups: number[] = []; const sel: number[] = []; const st: number[] = [];
    for (let i = 0; i < 30; i++) {
      const c = await issue('lat');
      const u0 = h.updates; const s0 = h.selects;
      const rv = await http(P1, 'POST', `/api/credentials/${encodeURIComponent(c.id)}/revoke`, { reason: 'g194 lat' }, true);
      ms.push(rv.ms); ups.push(h.updates - u0); sel.push(h.selects - s0); st.push(rv.status);
    }
    ms.sort((a, b) => a - b);
    rec({ cell: 'LAT', route: '-', shape: '-', n: 30, statuses: Array.from(new Set(st)), updatesPerRevoke: Array.from(new Set(ups)), selectsPerRevoke: Array.from(new Set(sel)),
      p50: +ms[15].toFixed(2), p90: +ms[27].toFixed(2), min: +ms[0].toFixed(2), max: +ms[29].toFixed(2) });
  });
});

// Q5: the restart case, a second app over FRESH module instances against the same table (runs last).
describe('gate194 restart', () => {
  it('RESTART', async () => {
    reset();
    // cells in process 1 first
    const cA = await issue('RSa');             // C ordinary -> then fresh process, no retry
    const cB = await issue('RSb');             // C ordinary -> retry healthy -> fresh process
    h.insertFailOn = true; const cZ = await issue('RSz'); h.insertFailOn = false; // memory-only (INSERT failed), DB healthy
    const rvs: Record<string, any> = {};
    h.updateFailOn = true; h.updateFail = new PgLikeError();
    rvs.A = await http(P1, 'POST', `/api/credentials/${encodeURIComponent(cA.id)}/revoke`, { reason: 'g194 RSa' }, true);
    rvs.B1 = await http(P1, 'POST', `/api/credentials/${encodeURIComponent(cB.id)}/revoke`, { reason: 'g194 RSb' }, true);
    h.updateFailOn = false;
    const p1AfterA = { cred: await verify(P1, 'credentials', cA), pres: await verify(P1, 'presentations', cA) };
    rvs.B2 = await http(P1, 'POST', `/api/credentials/${encodeURIComponent(cB.id)}/revoke`, { reason: 'g194 RSb retry' }, true);
    rvs.Z1 = await http(P1, 'POST', `/api/credentials/${encodeURIComponent(cZ.id)}/revoke`, { reason: 'g194 RSz' }, true);
    rvs.Z2 = await http(P1, 'POST', `/api/credentials/${encodeURIComponent(cZ.id)}/revoke`, { reason: 'g194 RSz retry' }, true);
    const p1 = async (c: any) => ({ cred: (await verify(P1, 'credentials', c)), pres: (await verify(P1, 'presentations', c)) });
    const P1B = await p1(cB); const P1Z = await p1(cZ);
    // process 2: fresh modules, real loadFromDb against the same table
    vi.resetModules();
    const repo2 = await import('../repositories/credentialRepo');
    const { credentialRoutes: cr2 } = await import('../routes/credentials');
    const { presentationRoutes: pr2 } = await import('../routes/presentations');
    const { errorHandler: eh2 } = await import('../middleware/errorHandler');
    const fresh = repo2 !== (repo as any);
    const memBeforeLoad = await memRevoked(repo2, cA.id);
    await repo2.loadFromDb();
    const s = await listen(mkApp(cr2, pr2, eh2)); server2 = s.server; const P2 = s.url;
    const p2 = async (c: any) => ({ cred: (await verify(P2, 'credentials', c)), pres: (await verify(P2, 'presentations', c)) });
    const P2A = await p2(cA); const P2B = await p2(cB); const P2Z = await p2(cZ);
    const v = (x: any) => ({ status: x.status, verified: x.verified, errors: x.errors });
    const pv = (o: any) => ({ cred: v(o.cred), pres: v(o.pres) });
    rec({ cell: 'RESTART', route: '-', shape: 'ordinary', freshModuleInstance: fresh, p2MemBeforeLoad_A: memBeforeLoad,
      A: { revoke: rvs.A.status, revokeMsg: rvs.A.json?.error?.message ?? rvs.A.json?.message, dbRow: dbRevoked(cA.id), p1Mem: await memRevoked(repo, cA.id), p2Mem: await memRevoked(repo2, cA.id), p1Verify: pv(p1AfterA), p2Verify: pv(P2A) },
      B: { revoke1: rvs.B1.status, retry: rvs.B2.status, dbRow: dbRevoked(cB.id), p1Mem: await memRevoked(repo, cB.id), p2Mem: await memRevoked(repo2, cB.id), p1Verify: pv(P1B), p2Verify: pv(P2B) },
      Z: { revoke1: rvs.Z1.status, retry: rvs.Z2.status, dbRow: dbRevoked(cZ.id), p1Mem: await memRevoked(repo, cZ.id), p2Mem: await memRevoked(repo2, cZ.id), p1Verify: pv(P1Z), p2Verify: pv(P2Z) },
    });
  });
});
