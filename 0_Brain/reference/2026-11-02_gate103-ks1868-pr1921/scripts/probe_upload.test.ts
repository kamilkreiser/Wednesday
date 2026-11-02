// QA GATE 103 probe U (not part of the PR). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// The REAL kyc app on a REAL loopback listener, REAL db.ts (initDb/query/isDbAvailable), REAL subjectDeks over the
// REAL shared SubjectDekProvider + PII crypto, REAL JWT authenticate (RS256 token), REAL kyc winston logger, REAL
// shared errorHandler. ONLY the `pg` driver is replaced: a recording Pool over in-memory tables
// (svc_kyc_verifications, svc_kyc_images, svc_kyc_consents, pii_subject_keys). The svc_kyc_images INSERT rejects
// with the chosen value (front, back-only, or selfie).
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import http from 'http';
import type { AddressInfo } from 'net';
import { appendFileSync } from 'fs';
import Transport from 'winston-transport';
import winston from 'winston';

process.env.NODE_ENV = 'development';
process.env.KYC_PROVIDER = 'mock';
process.env.PORT = '0';
process.env.DATABASE_URL = 'postgres://gate103:stub@127.0.0.1:1/gate103';
process.env.PII_ENCRYPTION_KEY = crypto.randomBytes(32).toString('hex');
process.env.KYC_RATE_LIMIT_PER_HOUR = '100000';
delete process.env.REDIS_URL; delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;

const OUT = process.env.PROBE_OUT as string;

const h = vi.hoisted(() => ({
  failOn: 'none' as string,          // none | front | back | selfie | all
  toThrow: undefined as unknown,
  imageInsertAttempts: 0,
  verif: new Map<string, Record<string, any>>(),
  images: new Map<string, Record<string, any>>(),
  consents: 0,
  keys: new Map<string, Record<string, any>>(),
  upserts: 0,
  imgCall: 0,
}));

const COLS = ['id','user_id','requested_level','current_level','status','provider','provider_application_id','provider_check_id','documents','liveness_completed','liveness_score','checks','overall_score','risk_level','reviewed_by','review_notes','consent_given','consent_timestamp','data_retention_expiry','created_at','updated_at','completed_at','expires_at'];

vi.mock('pg', () => {
  const norm = (s: string) => String(s).replace(/\s+/g, ' ').trim();
  function exec(text: string, v: any[] = []): Promise<any> {
    const n = norm(text);
    if (/^SELECT 1 AS ok/i.test(n)) return Promise.resolve({ rows: [{ ok: 1 }], rowCount: 1 });
    if (/^SELECT COUNT\(\*\) AS cnt FROM svc_kyc_verifications/i.test(n)) return Promise.resolve({ rows: [{ cnt: h.verif.size }], rowCount: 1 });
    if (/^INSERT INTO svc_kyc_images/i.test(n)) {
      h.imageInsertAttempts += 1; h.imgCall += 1;
      const which = h.imgCall; // 1 = first image in the request, 2 = second
      const fail = h.failOn === 'all' || (h.failOn === 'front' && which === 1) || (h.failOn === 'selfie' && which === 1) || (h.failOn === 'back' && which === 2);
      if (fail) return Promise.reject(h.toThrow);
      if (!h.images.has(v[0])) h.images.set(v[0], { id: v[0], mime_type: v[1], user_id: v[2] });
      return Promise.resolve({ rows: [], rowCount: 1 });
    }
    if (/^INSERT INTO svc_kyc_verifications/i.test(n)) {
      const row: Record<string, any> = {}; COLS.forEach((c, i) => { row[c] = v[i]; });
      h.upserts += 1; h.verif.set(row.id, row);
      return Promise.resolve({ rows: [], rowCount: 1 });
    }
    if (/^SELECT \* FROM svc_kyc_verifications WHERE id = \$1/i.test(n)) { const r = h.verif.get(v[0]); return Promise.resolve({ rows: r ? [{ ...r }] : [], rowCount: r ? 1 : 0 }); }
    if (/^INSERT INTO svc_kyc_consents/i.test(n)) { h.consents += 1; return Promise.resolve({ rows: [], rowCount: 1 }); }
    if (/^SELECT wrapped_dek.*FROM pii_subject_keys/i.test(n)) { const r = h.keys.get(v[0]); return Promise.resolve({ rows: r ? [{ ...r }] : [], rowCount: r ? 1 : 0 }); }
    if (/^INSERT INTO pii_subject_keys/i.test(n)) {
      if (h.keys.has(v[0])) return Promise.resolve({ rows: [], rowCount: 0 });
      h.keys.set(v[0], { wrapped_dek: v[1], wrap_iv: v[2], wrap_auth_tag: v[3], kek_version: v[4], destroyed_at: null });
      return Promise.resolve({ rows: [{ subject_id: v[0] }], rowCount: 1 });
    }
    return Promise.resolve({ rows: [], rowCount: 0, unmodelled: n.slice(0, 60) });
  }
  class Pool { constructor(_o?: unknown) {} on() { return this; } query(t: string, v?: any[]) { return exec(t, v); }
    connect() { return Promise.resolve({ query: (t: string, v?: any[]) => exec(t, v), release() {} }); } end() { return Promise.resolve(); } }
  return { Pool, default: { Pool } };
});

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64url = (b: Buffer) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const USER = 'a1030000-0000-4000-8000-000000000103';
function token(): string {
  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const payload = b64url(Buffer.from(JSON.stringify({ sub: USER, userId: USER, role: 'user', iat: now, exp: now + 600 })));
  const sig = b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM));
  return `${header}.${payload}.${sig}`;
}

const PNG_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('db down'),
  pgLike: () => Object.assign(new Error('relation "svc_kyc_images" does not exist'), { code: '42P01', severity: 'ERROR' }),
  string: () => 'db down (string)',
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  throwingGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
};

let server: http.Server; let base: string;
const SAVED = process.listeners('unhandledRejection');
let unhandled = 0; const onUnhandled = () => { unhandled += 1; };
const lines: string[] = [];
class Cap extends Transport { log(info: any, cb: () => void) { const { level, message, ...rest } = info; const meta: Record<string, unknown> = {}; for (const k of Object.keys(rest)) if (k !== 'timestamp') meta[k] = k === 'stack' ? String(rest[k]).split('\n')[0] : rest[k]; lines.push(JSON.stringify({ src: 'winston', level: String(level).replace(/\u001b\[[0-9;]*m/g, ''), message, meta })); cb(); } }

beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  // Every winston Console transport (the kyc logger AND the shared errorHandler's logger) is observed at the
  // transport, so no logger instance is replaced and none can be missed.
  const cap = new Cap();
  const C: any = (winston as any).transports.Console.prototype;
  const origLog = C.log;
  C.log = function (info: any, cb: () => void) { cap.log(info, () => undefined); return origLog.call(this, info, cb); };
  const shl: any = { logger: { add: true } };
  const sh: any = shl;
  const app: any = (await import('../index')).default;
  server = http.createServer(app);
  await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  await new Promise((r) => setTimeout(r, 300)); // boot probe settles
  const db = await import('../db');
  appendFileSync(OUT, JSON.stringify({ positive_control: { isDbAvailable: db.isDbAvailable(), sharedLoggerCaptured: !!sh.logger?.add, sharedErrorsLoggerCaptured: !!shl.logger?.add } }) + '\n');
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
}, 120_000);
afterAll(async () => {
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED) process.on('unhandledRejection', l as any);
  (server as any).closeAllConnections?.();
  await new Promise<void>((r) => server.close(() => r()));
});

async function call(path: string, body: unknown) {
  try {
    const res = await fetch(base + path, { method: 'POST', signal: AbortSignal.timeout(4000),
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token()}` }, body: JSON.stringify(body) });
    const t = await res.text(); let b: any; try { b = JSON.parse(t); } catch { b = t.slice(0, 200); }
    return { status: res.status, body: b };
  } catch (e) { return { status: 'UNANSWERED(' + (e as Error).name + ')', body: null }; }
}

async function cell(route: string, failOn: string, kind: string | null) {
  h.verif.clear(); h.images.clear(); h.keys.clear(); h.consents = 0; h.upserts = 0; h.imageInsertAttempts = 0; h.imgCall = 0;
  h.failOn = 'none'; h.toThrow = undefined;
  const init = await call('/api/kyc/initiate', { userId: USER, requestedLevel: 'HIGH', consentGiven: true });
  const id = init.body?.data?.verificationId;
  const upsertsAfterInit = h.upserts; const keysAfterInit = h.keys.size;
  h.failOn = failOn; h.toThrow = kind ? KINDS[kind]() : undefined; h.imgCall = 0; h.imageInsertAttempts = 0;
  unhandled = 0; lines.length = 0;
  const spies = (['log', 'error', 'warn', 'info'] as const).map((m) => vi.spyOn(console, m).mockImplementation((...a: unknown[]) => { lines.push(JSON.stringify({ src: 'console.' + m, text: a.map((x) => typeof x === 'string' ? x : (() => { try { return JSON.stringify(x); } catch { return '[unserialisable]'; } })()).join(' ') })); }));
  const res = route === 'selfie'
    ? await call(`/api/kyc/${id}/selfie`, { verificationId: id, selfieImage: PNG_B64 })
    : await call(`/api/kyc/${id}/document`, { verificationId: id, documentType: 'passport', country: 'GB', frontImage: PNG_B64, ...(route === 'frontBack' ? { backImage: PNG_B64 } : {}) });
  await new Promise((r) => setTimeout(r, 80));
  spies.forEach((s) => s.mockRestore());
  const row = h.verif.get(id);
  const rec = {
    cell: `${route}/${failOn}/${kind ?? 'none'}`, init: init.status,
    status: res.status, body: res.body,
    imageInsertAttempts: h.imageInsertAttempts, imageRowsPersisted: h.images.size,
    upsertsAfterInitiate: h.upserts - upsertsAfterInit,
    rowStatus: row?.status, rowDocumentsCipherPresent: row?.documents != null, livenessCompleted: row?.liveness_completed, livenessScore: row?.liveness_score ?? null,
    checks: JSON.parse(row?.checks ?? '[]').map((c: any) => `${c.type}:${c.status}`),
    subjectKeysMinted: h.keys.size - keysAfterInit,
    logLines: lines.filter((s) => !/Request completed/.test(s)),
    unhandled,
  };
  appendFileSync(OUT, JSON.stringify(rec) + '\n');
}

describe('gate 103 probe U: upload routes through the real app with only pg replaced', () => {
  for (const route of ['front', 'frontBack', 'selfie']) {
    const failOn = route === 'front' ? 'front' : route === 'frontBack' ? 'back' : 'selfie';
    it(`${route} control (no failure)`, async () => { await cell(route, 'none', null); });
    for (const k of Object.keys(KINDS)) it(`${route} ${failOn} INSERT rejects: ${k}`, async () => { await cell(route, failOn, k); });
  }
});
