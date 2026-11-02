import { describe, it, beforeAll, vi } from 'vitest';
import crypto from 'crypto';

const h = vi.hoisted(() => ({
  db: new Map<string, any>(),
  selectFail: undefined as unknown,
  selectFailOn: false,
  updateFail: undefined as unknown,
  updateFailOn: false,
}));
vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: (sql: string, params: any[] = []) => {
    if (/LIMIT 0/i.test(sql)) return Promise.resolve({ rows: [] });
    if (/^\s*INSERT/i.test(sql)) { h.db.set(params[0], JSON.parse(params[1])); return Promise.resolve({ rows: [] }); }
    if (/^\s*UPDATE/i.test(sql)) { if (h.updateFailOn) return Promise.reject(h.updateFail); h.db.set(params[1], JSON.parse(params[0])); return Promise.resolve({ rows: [] }); }
    if (/^\s*SELECT credential/i.test(sql) && /WHERE id = \$1/.test(sql)) {
      if (h.selectFailOn) return Promise.reject(h.selectFail);
      const c = h.db.get(params[0]);
      return Promise.resolve({ rows: c ? [{ credential: c, created_by_user_id: 'u', created_by_tenant_id: null }] : [] });
    }
    return Promise.resolve({ rows: [] });
  },
}));
vi.mock('../utils/logger', () => ({ logger: { debug() {}, info() {}, warn() {}, error() {} } }));

import { credentialRoutes } from '../routes/credentials';
import { errorHandler } from '../middleware/errorHandler';

type Reply = { status: number; body: any };
function dispatch(router: unknown, method: string, url: string, body?: unknown): Promise<Reply> {
  return new Promise((resolve, reject) => {
    const req: any = { method, url, baseUrl: '', originalUrl: url, headers: {}, body, params: {}, query: {},
      user: { userId: 'u', role: 'SYSTEM_ADMIN', organizationId: 'org-test' } };
    const res: any = { statusCode: 200, status(c: number) { this.statusCode = c; return this; }, json(p: unknown) { resolve({ status: this.statusCode, body: p }); return this; } };
    const next = (err?: unknown) => { if (err) errorHandler(err as Error, req, res, () => {}); else reject(new Error('nomatch')); };
    (router as any)(req, res, next);
  });
}
beforeAll(() => {
  const { privateKey } = crypto.generateKeyPairSync('ed25519');
  process.env.VC_SIGNING_KEY = privateKey.export({ type: 'pkcs8', format: 'der' }).toString('hex');
});
const cred = (m: string, u: string, b?: unknown) => dispatch(credentialRoutes, m, u, b);
let n = 0;
async function issue(tag: string) {
  n++;
  const r = await cred('POST', '/', { documentId: 'doc-' + tag + n, documentHash: 'hash-' + tag + n, documentType: 'PropertyDeed', documentTitle: 'g152 ' + tag });
  return r.body?.credential ?? r.body?.data?.credential ?? r.body;
}
async function verify(doc: unknown) {
  const r = await cred('POST', '/verify', { credential: doc });
  return { verified: r.body?.verified, errors: (r.body?.result?.errors ?? []) as string[] };
}
const revokedProxy = () => { const rp = Proxy.revocable({}, {}); rp.revoke(); return rp.proxy; };
const getterThrows = () => Object.create(Error.prototype, { message: { get() { throw new Error('g'); } } });
const VALUES: [string, () => unknown][] = [['ordinary Error', () => new Error('db down')], ['revoked Proxy', revokedProxy], ['getter throws', getterThrows]];
const rec = (s: string) => console.log('Q2 ' + s);

describe('gate152 Q2', () => {
  for (const [name, mk] of VALUES) {
    it('A revoke ok in memory+DB then DB read fails: ' + name, async () => {
      h.selectFailOn = false; h.updateFailOn = false;
      const c = await issue('A');
      const pre = await verify(c);
      const rv = await cred('POST', '/' + encodeURIComponent(c.id) + '/revoke', { reason: 'test' });
      h.selectFailOn = true; h.selectFail = mk();
      const post = await verify(c);
      rec(`A ${name}: preRevokeVerified=${pre.verified} revokeStatus=${rv.status} verifiedAfterRevokeWithDbReadFailing=${post.verified} errors=${JSON.stringify(post.errors)}`);
      h.selectFailOn = false;
    });
    it('B stale memory, DB row revoked elsewhere, DB read fails: ' + name, async () => {
      h.selectFailOn = false; h.updateFailOn = false;
      const c = await issue('B');
      const healthy = await verify(c);
      const row = h.db.get(c.id);
      h.db.set(c.id, { ...row, credentialStatus: { ...row.credentialStatus, revoked: true, revokedAt: 'x', revocationReason: 'other replica' } });
      const healthyAfter = await verify(c);
      h.selectFailOn = true; h.selectFail = mk();
      const failing = await verify(c);
      rec(`B ${name}: beforeExternalRevoke=${healthy.verified}; afterExternalRevoke DBhealthy=${healthyAfter.verified}; afterExternalRevoke DBREADFAILING=${failing.verified} errors=${JSON.stringify(failing.errors)}`);
      h.selectFailOn = false;
    });
    it('D unknown id, DB read fails: ' + name, async () => {
      h.selectFailOn = false;
      const c = await issue('D');
      const other = { ...c, id: c.id + '-other' };
      h.selectFailOn = true; h.selectFail = mk();
      const r = await verify(other);
      rec(`D ${name}: unknown id, DB read failing verified=${r.verified} errors=${JSON.stringify(r.errors)}`);
      h.selectFailOn = false;
    });
    it('C revoke DB write fails: ' + name, async () => {
      h.selectFailOn = false; h.updateFailOn = true; h.updateFail = mk();
      const c = await issue('C');
      let rv: any; try { rv = await cred('POST', '/' + encodeURIComponent(c.id) + '/revoke', { reason: 'r' }); } catch { rv = { status: 'threw' }; }
      h.updateFailOn = false;
      const v = await verify(c);
      rec(`C ${name}: revoke status=${rv.status} dbRowRevoked=${h.db.get(c.id)?.credentialStatus?.revoked === true} verifyInProcessAfter=${v.verified}`);
    });
  }
});
