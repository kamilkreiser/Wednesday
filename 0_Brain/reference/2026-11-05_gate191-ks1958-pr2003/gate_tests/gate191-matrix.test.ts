/**
 * Gate 191 (KS-1958, PR 2003) matrix harness. Written by the gate, not by the seat.
 * REAL: credentialRepo, revocationResolvers, the shared verifier, the credentials and presentations routers,
 * errorHandler, helmet, cors, boundedJson, rejectNulBytes, express, and a real HTTP server on 127.0.0.1:<ephemeral>.
 * REPLACED: ../db (an in-memory table whose SELECTs / UPDATEs can be made to fail) and ../utils/logger (captures warns).
 * index.ts is NOT booted (its middleware order is reproduced; jwtAuthenticate is replaced by a fake-user middleware
 * that only sets req.user when the request carries x-g191-user, so verify calls are made WITHOUT a user, as public).
 * Every cell appends one JSON line to $G191_OUT.
 */
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import fs from 'fs';
import type { AddressInfo } from 'net';

const h = vi.hoisted(() => ({
  db: new Map<string, any>(),
  available: true,
  selectFail: undefined as unknown,
  selectFailOn: false,
  updateFail: undefined as unknown,
  updateFailOn: false,
  selects: 0,
  updates: 0,
  warns: [] as Array<{ msg: string; meta: any }>,
}));

vi.mock('../db', () => ({
  isDbAvailable: () => h.available,
  initDb: async () => true,
  closeDb: async () => {},
  query: (sql: string, params: any[] = []) => {
    if (/LIMIT 0/i.test(sql)) return Promise.resolve({ rows: [] });
    if (/^\s*INSERT/i.test(sql)) { h.db.set(params[0], JSON.parse(params[1])); return Promise.resolve({ rows: [] }); }
    if (/^\s*UPDATE/i.test(sql)) {
      h.updates++;
      if (h.updateFailOn) return Promise.reject(h.updateFail);
      h.db.set(params[1], JSON.parse(params[0]));
      return Promise.resolve({ rows: [] });
    }
    if (/^\s*SELECT/i.test(sql)) {
      h.selects++;
      if (h.selectFailOn) return Promise.reject(h.selectFail);
      if (/WHERE id = \$1/.test(sql)) {
        const c = h.db.get(params[0]);
        return Promise.resolve({ rows: c ? [{ credential: c, created_by_user_id: 'g191-user', created_by_tenant_id: null }] : [] });
      }
    }
    return Promise.resolve({ rows: [] });
  },
}));
vi.mock('../utils/logger', () => {
  const l = { debug() {}, info() {}, error(msg: string, meta: any) { h.warns.push({ msg: 'ERROR ' + msg, meta }); }, warn(msg: string, meta: any) { h.warns.push({ msg, meta }); } };
  return { logger: l, createLogger: () => l };
});

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { boundedJson, rejectNulBytes } from '@secuura/shared';
import * as repo from '../repositories/credentialRepo';
import { credentialRoutes } from '../routes/credentials';
import { presentationRoutes } from '../routes/presentations';
import { errorHandler } from '../middleware/errorHandler';

const OUT = process.env.G191_OUT as string;
const SIDE = process.env.G191_SIDE as string;
const rec = (o: Record<string, unknown>) => fs.appendFileSync(OUT, JSON.stringify({ side: SIDE, ...o }) + '\n');

let base = '';
let server: any;
beforeAll(async () => {
  const { privateKey } = crypto.generateKeyPairSync('ed25519');
  process.env.VC_SIGNING_KEY = privateKey.export({ type: 'pkcs8', format: 'der' }).toString('hex');
  const app = express();
  app.use(helmet());
  app.use(cors({ origin: ['http://localhost:6100'], credentials: true }));
  app.use(boundedJson({ service: 'vc-issuer', limit: '10mb' }));
  app.use(express.urlencoded({ extended: true }));
  app.use(rejectNulBytes());
  app.use((req: any, _res, next) => {
    if (req.headers['x-g191-user']) req.user = { userId: 'g191-user', role: 'SYSTEM_ADMIN', organizationId: 'org-g191' };
    next();
  });
  app.use('/api/credentials', credentialRoutes);
  app.use('/api/presentations', presentationRoutes);
  app.use(errorHandler);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(async () => { await new Promise((r) => server.close(r)); });

async function http(method: string, path: string, body?: unknown, user = false) {
  const t0 = performance.now();
  const r = await fetch(base + path, {
    method,
    headers: { 'content-type': 'application/json', ...(user ? { 'x-g191-user': '1' } : {}) },
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
async function issue(tag: string) {
  seq++;
  const r = await http('POST', '/api/credentials', {
    documentId: `doc-g191-${tag}-${seq}`, documentHash: `hash-g191-${tag}-${seq}`,
    documentType: 'PropertyDeed', documentTitle: 'g191 ' + tag,
  }, true);
  if (r.status !== 201 && r.status !== 200) throw new Error('issue failed ' + r.status + ' ' + r.text.slice(0, 300));
  return r.json?.credential ?? r.json?.data?.credential ?? r.json;
}

async function verify(route: string, doc: any) {
  const s0 = h.selects;
  if (route === 'credentials') {
    const r = await http('POST', '/api/credentials/verify', { credential: doc });
    return { ...r, selects: h.selects - s0, verified: r.json?.verified, errors: (r.json?.result?.errors ?? []) as string[] };
  }
  const r = await http('POST', '/api/presentations/verify', {
    presentation: {
      '@context': ['https://www.w3.org/2018/credentials/v1'], type: ['VerifiablePresentation'],
      id: 'urn:uuid:g191-presentation', holder: 'did:secuura:g191-holder', verifiableCredential: [doc],
    },
  });
  const first = r.json?.credentialResults?.[0];
  return { ...r, selects: h.selects - s0, verified: first?.verified, errors: (first?.errors ?? []) as string[] };
}

const TOKEN = 'PLANTED-G191';
class PgLikeError extends Error {
  code = '57P01'; detail = TOKEN + '-DETAIL'; hint = TOKEN + '-HINT'; where = TOKEN + '-WHERE'; severity = 'FATAL';
  constructor() { super(TOKEN + '-MSG terminating connection: relation "vc_credentials_store" host db-int-g191.internal'); this.name = 'error'; }
}
const revokedProxy = () => { const rp = Proxy.revocable({}, {}); rp.revoke(); return rp.proxy; };
const getterThrows = () => Object.create(Error.prototype, {
  message: { get() { throw new Error(TOKEN + '-GETTER'); } },
  stack: { value: 'Error: ' + TOKEN + '-STACK\n    at g191 (/srv/vc-issuer/dist/db.js:1:1)' },
});
const SHAPES: Array<[string, () => unknown]> = [['ordinary', () => new PgLikeError()], ['proxy', revokedProxy], ['getter', getterThrows]];
const LEAK = /PLANTED-G191|vc_credentials_store|db-int-g191|57P01|\.ts:\d+|\.js:\d+|node_modules|    at /;

function revokeElsewhere(id: string) {
  const row = h.db.get(id);
  h.db.set(id, { ...row, credentialStatus: { ...row.credentialStatus, revoked: true, revokedAt: '2026-11-05T00:00:00.000Z', revocationReason: 'g191 other replica' } });
}
function reset() { h.available = true; h.selectFailOn = false; h.updateFailOn = false; h.selectFail = undefined; h.updateFail = undefined; h.warns.length = 0; }
function out(cell: string, route: string, shape: string, v: any, extra: Record<string, unknown> = {}) {
  const warnText = JSON.stringify(h.warns, (_k, val) => (typeof val === 'string' ? val : val));
  rec({
    cell, route, shape, status: v.status, verified: v.verified, errors: v.errors, ms: Math.round(v.ms), selects: v.selects,
    bodyLeak: LEAK.test(v.text) ? (v.text.match(LEAK) || [])[0] : null, headerLeak: LEAK.test(v.headers) ? (v.headers.match(LEAK) || [])[0] : null,
    warnHasToken: warnText.includes(TOKEN), warnMsgs: h.warns.map((w) => w.msg), ...extra,
  });
}

describe('gate191 matrix', () => {
  for (const route of ['credentials', 'presentations']) {
    for (const [shape, mk] of SHAPES) {
      it(`A ${route} ${shape}`, async () => {
        reset(); const c = await issue('A');
        const rv = await http('POST', `/api/credentials/${encodeURIComponent(c.id)}/revoke`, { reason: 'g191 A' }, true);
        h.warns.length = 0; h.selectFailOn = true; h.selectFail = mk();
        out('A', route, shape, await verify(route, c), { revokeStatus: rv.status }); reset();
      });
      it(`B ${route} ${shape}`, async () => {
        reset(); const c = await issue('B'); revokeElsewhere(c.id);
        h.warns.length = 0; h.selectFailOn = true; h.selectFail = mk();
        out('B', route, shape, await verify(route, c)); reset();
      });
      it(`Bctrl ${route} ${shape}`, async () => {
        reset(); const c = await issue('Bc'); revokeElsewhere(c.id);
        h.warns.length = 0;
        out('Bctrl', route, shape, await verify(route, c)); reset();
      });
      it(`C ${route} ${shape}`, async () => {
        reset(); h.updateFailOn = true; h.updateFail = mk();
        const c = await issue('C');
        const rv = await http('POST', `/api/credentials/${encodeURIComponent(c.id)}/revoke`, { reason: 'g191 C' }, true);
        h.updateFailOn = false; h.warns.length = 0;
        out('C', route, shape, await verify(route, c), { revokeStatus: rv.status, revokeLeak: LEAK.test(rv.text) ? (rv.text.match(LEAK) || [])[0] : null, dbRowRevoked: h.db.get(c.id)?.credentialStatus?.revoked === true }); reset();
      });
      it(`D ${route} ${shape}`, async () => {
        reset(); const c = await issue('D');
        h.warns.length = 0; h.selectFailOn = true; h.selectFail = mk();
        out('D', route, shape, await verify(route, { ...c, id: c.id + '-unknown' })); reset();
      });
      it(`U ${route} ${shape}`, async () => {
        reset(); const c = await issue('U');
        h.warns.length = 0; h.selectFailOn = true; h.selectFail = mk();
        out('U', route, shape, await verify(route, c)); reset();
      });
      it(`Uhealthy ${route} ${shape}`, async () => {
        reset(); const c = await issue('Uh');
        h.warns.length = 0;
        out('Uhealthy', route, shape, await verify(route, c)); reset();
      });
    }
  }

  // Q4: revoke() and the three siblings with every SELECT failing
  for (const [shape, mk] of SHAPES) {
    it(`Q4 revoke ${shape}`, async () => {
      reset(); const c = await issue('q4r');
      h.selectFailOn = true; h.selectFail = mk(); const u0 = h.updates;
      const rv = await http('POST', `/api/credentials/${encodeURIComponent(c.id)}/revoke`, { reason: 'g191 q4' }, true);
      h.selectFailOn = false;
      rec({ cell: 'Q4revoke', shape, status: rv.status, bodyRevoked: rv.json?.credential?.credentialStatus?.revoked ?? rv.json?.data?.credentialStatus?.revoked ?? null,
        bodyKeys: Object.keys(rv.json ?? {}), updateIssued: h.updates - u0, dbRowRevoked: h.db.get(c.id)?.credentialStatus?.revoked === true,
        memRevoked: (await repo.getById(c.id))?.credentialStatus?.revoked === true, warnMsgs: h.warns.map((w) => w.msg) });
      reset();
    });
    it(`Q4 getRecordById route ${shape}`, async () => {
      reset(); const c = await issue('q4g'); h.warns.length = 0;
      h.selectFailOn = true; h.selectFail = mk();
      const r = await http('GET', `/api/credentials/${encodeURIComponent(c.id)}`, undefined, true);
      rec({ cell: 'Q4getRecordById', shape, status: r.status, idEcho: (r.json?.credential?.id ?? r.json?.data?.id ?? r.json?.id) === c.id, warnMsgs: h.warns.map((w) => w.msg) });
      reset();
    });
    it(`Q4 getByHash ${shape}`, async () => {
      reset(); const c = await issue('q4h'); h.warns.length = 0;
      h.selectFailOn = true; h.selectFail = mk();
      let res: string; try { res = (await repo.getByHash(c.credentialSubject.documentHash))?.id === c.id ? 'memory hit' : 'miss'; } catch (e: any) { res = 'threw ' + String(e?.name); }
      rec({ cell: 'Q4getByHash', shape, res, warnMsgs: h.warns.map((w) => w.msg) });
      reset();
    });
    it(`Q4 getReadableByHash route ${shape}`, async () => {
      reset(); const c = await issue('q4rh'); h.warns.length = 0;
      h.selectFailOn = true; h.selectFail = mk();
      const r = await http('GET', `/api/credentials/by-hash/${encodeURIComponent(c.credentialSubject.documentHash)}`, undefined, true);
      rec({ cell: 'Q4getReadableByHash', shape, status: r.status, leak: LEAK.test(r.text) ? (r.text.match(LEAK) || [])[0] : null, warnMsgs: h.warns.map((w) => w.msg) });
      reset();
    });
  }
});
