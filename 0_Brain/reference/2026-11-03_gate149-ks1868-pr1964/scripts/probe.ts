// QA gate 149 probe. usage: tsx probe.ts <base|head|merged> <development|production> <out.jsonl>
// REAL: routes/documents.ts (base or head copy), repositories/documentRepo.ts + lifecycleEventRepo.ts (their own catches),
// the in-memory signing-request map, express 4, express-validator, verifyMessageSignature (a real CIP-8 signature), the
// winston logger utils/logger.ts in the requested NODE_ENV, index.ts's process handlers (copied verbatim, exit recorded
// instead of performed). REPLACED: ../db (the Prisma client -> an in-memory documents/lifecycle model that can reject
// before or after applying a write), ../middleware/auth (a fixed authenticated user), ../events publishEvent (recorder),
// the auth-service /api/issuer-certs/sign hop (a local HTTP stand-in). Optional L2 injection wraps repo functions.
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964';
const [variant, env, outFile] = process.argv.slice(2);
const fs = require('fs');
const path = require('path');
const http = require('http');
const crypto = require('crypto');
const cwd = `${W}/logs/child_cwd/${variant}_${env}`;
fs.mkdirSync(cwd, { recursive: true });
process.chdir(cwd); // production logger writes logs/*.log relative to cwd
process.env.NODE_ENV = env;
process.env.DATABASE_URL = 'postgresql://g149:g149@127.0.0.1:1/g149';
delete process.env.REDIS_URL;
const SRC = W + '/repo/Blockchain/Dev/services/originate/src/';
const Module = require('module');
const G: any = globalThis;

// ---- log capture (Console transport writes to process.stdout) ----
const lines: string[] = [];
const realOut = process.stdout.write.bind(process.stdout);
(process.stdout as any).write = (c: any) => { lines.push(String(c)); return true; };
const realErr = process.stderr.write.bind(process.stderr);
(process.stderr as any).write = (c: any) => { lines.push('STDERR:' + String(c)); return true; };
setTimeout(() => { realErr('WATCHDOG\n' + lines.slice(-30).join('') + '\n'); process.exit(3); }, 600000).unref();

// ---- index.ts:79-92 process handlers, verbatim except trackError -> recorder and exit -> recorded ----
G.__unhandled = 0; G.__uncaught = 0; G.__wouldExit = 0;
let logger: any;
process.on('unhandledRejection', (reason: unknown) => {
  G.__unhandled += 1;
  const message = reason instanceof Error ? reason.message : String(reason);
  const stack = reason instanceof Error ? reason.stack : undefined;
  logger.error('Unhandled promise rejection', { message, stack });
});
process.on('uncaughtException', (err: Error) => {
  G.__uncaught += 1;
  try { logger.error('Uncaught exception — exiting for a clean restart', { message: err.message, stack: err.stack }); } catch { /* recorded */ }
  G.__wouldExit += 1; // index.ts: setTimeout(() => process.exit(1), 100)
});

// ---- the DB model ----
G.__store = new Map<string, any>();
G.__lc = [] as any[];
G.__fault = null as null | { at: string; when: 'pre' | 'post'; v: () => unknown };
G.__sql = [] as string[];
const take = (at: string, when: string) => {
  const f = G.__fault;
  if (f && f.at === at && f.when === when) { G.__fault = null; return { hit: true, v: f.v() }; }
  return { hit: false, v: undefined };
};
function sqlOf(strings: TemplateStringsArray) { return strings.join('?').replace(/\s+/g, ' ').trim(); }
function prevText(strings: TemplateStringsArray, i: number) { return strings[i].replace(/\s+/g, ' ').trimEnd(); }
async function queryRaw(strings: TemplateStringsArray, ...values: any[]) {
  const s = sqlOf(strings); G.__sql.push(s.slice(0, 60));
  if (/^SELECT \* FROM documents WHERE external_id/.test(s)) {
    const p = take('select_doc', 'pre'); if (p.hit) throw p.v;
    const r = G.__store.get(values[0]); return r ? [JSON.parse(JSON.stringify(r))].map(revive) : [];
  }
  if (/^SELECT \* FROM documents WHERE id =/.test(s)) return [];
  if (/FROM documents d LEFT JOIN documents p/.test(s)) {
    const p = take('walk', 'pre'); if (p.hit) throw p.v;
    const r = G.__store.get(values[1]); if (!r) return [];
    return [{ id: r.id, external_id: r.external_id, content_hash: r.content_hash, document_type: r.document_type, status: r.status, created_at: new Date(r.created_at), parent_external_id: r.parent_external_id || null }];
  }
  if (/FROM document_lifecycle_events e JOIN documents d/.test(s)) {
    const p = take('select_lc', 'pre'); if (p.hit) throw p.v;
    return G.__lc.filter((e: any) => e.doc === values[0]).map((e: any) => ({ ...e.row }));
  }
  return [];
}
function revive(r: any) { r.created_at = new Date(r.created_at); r.updated_at = new Date(r.updated_at); return r; }
async function executeRaw(strings: TemplateStringsArray, ...values: any[]) {
  const s = sqlOf(strings); G.__sql.push(s.slice(0, 60));
  if (/^UPDATE documents SET/.test(s)) {
    const p = take('update', 'pre'); if (p.hit) throw p.v;
    let id: string | undefined, status: any, meta: any, cert: any;
    for (let i = 0; i < values.length; i++) {
      const t = prevText(strings, i);
      if (t.endsWith('external_id =') && id === undefined) id = values[i];
      if (t.endsWith('ELSE') && status === undefined && typeof values[i] === 'string') status = values[i];
      if (t.endsWith('certification_metadata =')) cert = values[i]; else if (t.endsWith('metadata =')) meta = values[i];
    }
    const r = id && G.__store.get(id); if (!r) return 0;
    r.status = status ?? r.status; r.metadata = { ...JSON.parse(meta), ...(r.metadata.blockchain ? { blockchain: r.metadata.blockchain } : {}) };
    r.certification_metadata = JSON.parse(cert); r.updated_at = new Date().toISOString();
    const q = take('update', 'post'); if (q.hit) throw q.v; // the row is written, then the client sees a rejection
    return 1;
  }
  if (/^INSERT INTO documents/.test(s)) {
    const p = take('insert', 'pre'); if (p.hit) throw p.v;
    const v = values;
    const row = { id: v[0], external_id: v[1], tenant_id: v[2], title: v[3], description: v[4], document_type: v[5], content_hash: v[6], status: v[7], owner_user_id: v[8], metadata: JSON.parse(v[11]), certification_metadata: JSON.parse(v[12]), parent_external_id: v[13], created_at: new Date().toISOString(), updated_at: new Date().toISOString() };
    if (!G.__store.has(row.external_id)) G.__store.set(row.external_id, row);
    const q = take('insert', 'post'); if (q.hit) throw q.v;
    return 1;
  }
  return 0;
}
const model = { $queryRaw: queryRaw, $executeRaw: executeRaw, $queryRawUnsafe: async () => [], $executeRawUnsafe: async () => 0, $disconnect: async () => undefined };
const dbStub = { prisma: model, getTenantManager: () => null, getRequestPrisma: () => model, refreshTenantConfigs: async () => undefined, withTenant: async (_t: unknown, fn: any) => fn(model), withPlatformScopeTransaction: async (fn: any) => fn(model), initDb: async () => undefined, disconnectDb: async () => undefined };

// ---- L2 repo-boundary injection ----
G.__repoFault = null as null | { fn: string; when: 'pre' | 'post'; v: () => unknown };
function wrapRepo(real: any, names: string[]) {
  return new Proxy(real, { get(t, p: string) {
    const orig = t[p];
    if (!names.includes(p) || typeof orig !== 'function') return orig;
    return async (...a: any[]) => {
      const f = G.__repoFault;
      if (f && f.fn === p && f.when === 'pre') { G.__repoFault = null; throw f.v(); }
      const out = await orig(...a);
      const g = G.__repoFault;
      if (g && g.fn === p && g.when === 'post') { G.__repoFault = null; throw g.v(); }
      return out;
    };
  } });
}
G.__events = [] as any[];
const ROUTE_FILE = (variant === 'base' || variant === 'devnow') ? SRC + 'routes/documents.gate_base.ts' : SRC + 'routes/documents.ts';
const origLoad = Module._load;
Module._load = function (req: string, parent: any, ...rest: unknown[]) {
  const pf = parent && parent.filename ? String(parent.filename) : '';
  if (pf.startsWith(SRC) && (req === '../db' || req === './db')) return dbStub;
  if (pf.startsWith(SRC) && req === '../middleware/auth') {
    const real = origLoad.call(this, req, parent, ...rest);
    return { ...real, authenticate: () => (q: any, _r: unknown, next: () => void) => { const u = { userId: '11111111-2222-4333-8444-555555555555', email: 'g149@example.invalid', role: 'ISSUER_ADMIN', verificationLevel: 'basic', scopes: ['documents:write'] }; q.user = u; q._secuuraUser = u; next(); } };
  }
  if (pf === ROUTE_FILE && req === '../events') {
    const real = origLoad.call(this, req, parent, ...rest);
    return { ...real, publishEvent: async (type: string, payload: any) => { G.__events.push({ type, newId: payload?.newId }); } };
  }
  if (pf === ROUTE_FILE && req === '../repositories/documentRepo') return wrapRepo(origLoad.call(this, req, parent, ...rest), ['getDocument', 'updateDocument', 'saveDocument']);
  if (pf === ROUTE_FILE && req === '../repositories/lifecycleEventRepo') return wrapRepo(origLoad.call(this, req, parent, ...rest), ['listLifecycleEvents']);
  return origLoad.call(this, req, parent, ...rest);
};

// ---- hostile and ordinary values ----
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMsg = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const VALUES: Record<string, () => unknown> = {
  ordinary: () => new Error('Connection terminated unexpectedly'),
  plainString: () => 'plain boom',
  revokedProxy: revoked,
  getterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  getterThrowsRevoked: () => Object.create(Error.prototype, { message: { get() { throw revoked(); } } }),
  msgBigInt: () => withMsg(10n),
  msgNullProto: () => withMsg(Object.create(null)),
  msgSymbol: () => withMsg(Symbol('g149')),
};

// ---- a real CIP-8 wallet signature (shared wallet-signature.test.ts recipe) ----
const cborReal = require(W + '/repo/Blockchain/Dev/node_modules/cbor');
// HOST SHIM (Node 26.8.1 only): cbor@9.0.2's encode truncates arrays/maps to their header byte on this host (measured), so the
// REAL verifyMessageSignature (which re-encodes the Sig_structure with cbor.encode) refuses every signature here. Replace encode
// with a minimal correct encoder; decode stays real.
const cbor = require(W + '/scripts/cborlite.js');
cborReal.encode = cbor.encode;
function walletSig(message: string) {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  const ph = cbor.encode(new Map([[1, -8]]));
  const payload = Buffer.from(message, 'utf8');
  const sig = crypto.sign(null, cbor.encode(['Signature1', ph, Buffer.alloc(0), payload]), privateKey);
  const spki = publicKey.export({ format: 'der', type: 'spki' }); const pub = Buffer.from(spki.subarray(spki.length - 32));
  return { signature: cbor.encode([ph, new Map(), payload, sig]).toString('hex'), key: cbor.encode(new Map<number, unknown>([[1, 1], [3, -8], [-1, 6], [-2, pub]])).toString('hex') };
}

const DOC = 'doc-g149-target';
const HASH = 'a'.repeat(64);
function seed() {
  G.__store.clear(); G.__lc.length = 0; G.__events.length = 0; G.__fault = null; G.__repoFault = null;
  const now = new Date().toISOString();
  G.__store.set(DOC, { id: '22222222-3333-4444-8555-666666666666', external_id: DOC, tenant_id: 'a0000000-0000-4000-8000-000000000001', title: 'G149 target', description: null, document_type: 'contract', content_hash: HASH, status: 'draft', owner_user_id: '11111111-2222-4333-8444-555555555555', metadata: { sigJson: { version: 1, signature: 'g149sig' } }, certification_metadata: { signatures: [] }, parent_external_id: null, created_at: now, updated_at: now });
  G.__lc.push({ doc: DOC, row: { id: 'e1', tenant_id: 'a0000000-0000-4000-8000-000000000001', action: 'shared', payload: { note: 'x' }, actor_user_id: null, anchor_id: null, created_at: new Date(now) } });
}
function state() {
  const d = G.__store.get(DOC);
  const children = [...G.__store.values()].filter((r: any) => r.parent_external_id === DOC).length;
  return { status: d?.status, signatures: (d?.certification_metadata?.signatures || []).length, derived: children, events: G.__events.length };
}

async function main() {
  const authSrv = http.createServer((req: any, res: any) => {
    let b = ''; req.on('data', (c: any) => (b += c)); req.on('end', () => {
      res.setHeader('content-type', 'application/json');
      res.end(JSON.stringify({ success: true, signature: 'c2ln', signatureAlgorithm: 'ECDSA-SHA256', signedContentHash: HASH, signedAt: new Date().toISOString(), cert: { id: 'cert-g149', fingerprintSha256: 'f'.repeat(64), subject: 'CN=g149', issuer: 'CN=g149', certPem: '-----BEGIN CERTIFICATE-----\\nZzE0OQ==\\n-----END CERTIFICATE-----', validFrom: '2026-01-01', validUntil: '2027-01-01', trustLevel: 'self' } }));
    });
  });
  await new Promise<void>((r) => authSrv.listen(0, '127.0.0.1', () => r()));
  process.env.AUTH_SERVICE_URL = `http://127.0.0.1:${authSrv.address().port}`;
  logger = require(SRC + 'utils/logger').logger;
  const express = Module.createRequire(SRC + 'index.ts')('express');
  const { documentsRouter, publicDocumentsRouter } = require(ROUTE_FILE.replace(/\.ts$/, ''));
  const app = express();
  app.use('/api/documents', express.json(), publicDocumentsRouter);
  app.use('/api/documents', express.json(), documentsRouter);
  const server = app.listen(0, '127.0.0.1');
  await new Promise((r) => server.once('listening', r));
  const base = `http://127.0.0.1:${server.address().port}`;
  await new Promise((r) => setTimeout(r, 300)); // let seedDemoDocuments settle
  const repo = require(SRC + 'repositories/documentRepo');

  async function call(method: string, p: string, body?: unknown) {
    try {
      const res = await fetch(base + p, { method, headers: { 'content-type': 'application/json' }, body: body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(1500) });
      const txt = await res.text(); let j: any = null; try { j = JSON.parse(txt); } catch { /* */ }
      return { status: res.status, code: j?.error?.code ?? (j?.signed ? 'signed' : j?.document ? 'created' : j?.hash ? 'hash' : j?.count !== undefined ? 'events' : j?.version ? 'sigjson' : null) };
    } catch (e: any) { return { status: null, code: 'NO_ANSWER_1500ms' }; }
  }
  const sw = walletSig(HASH);
  const ROUTES: Record<string, { m: string; p: string; body: () => any; catchMsg: string; nonce?: boolean }> = {
    signRequest: { m: 'POST', p: `/api/documents/${DOC}/sign/request`, body: () => ({ walletAddress: 'addr_test1g149' }), catchMsg: 'Failed to create signing request' },
    sign: { m: 'POST', p: `/api/documents/${DOC}/sign`, body: () => ({ signature: 'mock_signature_g149', nonce: G.__nonce, walletAddress: 'addr_test1g149' }), catchMsg: 'Failed to sign document', nonce: true },
    lifecycle: { m: 'GET', p: `/api/documents/${DOC}/lifecycle-events`, body: () => undefined, catchMsg: 'Failed to list lifecycle events' },
    signCert: { m: 'POST', p: `/api/documents/${DOC}/sign-cert`, body: () => ({}), catchMsg: 'Failed to sign document via issuer cert' },
    signWallet: { m: 'POST', p: `/api/documents/${DOC}/sign-wallet`, body: () => ({ walletAddress: 'addr_test1g149', signature: sw.signature, key: sw.key }), catchMsg: 'Failed to sign document via wallet' },
    sigJson: { m: 'GET', p: `/api/documents/${DOC}/sig-json`, body: () => undefined, catchMsg: 'Failed to get sig-json' },
  };
  // injection: [route, layer, point, when]
  const INJ: [string, string, string, 'pre' | 'post'][] = [
    ['signRequest', 'L1', 'select_doc', 'pre'], ['signRequest', 'L2', 'getDocument', 'pre'],
    ['sign', 'L1', 'select_doc', 'pre'], ['sign', 'L2', 'getDocument', 'pre'], ['sign', 'L1', 'update', 'post'], ['sign', 'L2', 'updateDocument', 'post'],
    ['lifecycle', 'L1', 'select_lc', 'pre'], ['lifecycle', 'L2', 'listLifecycleEvents', 'pre'],
    ['signCert', 'L1', 'select_doc', 'pre'], ['signCert', 'L1', 'walk', 'pre'], ['signCert', 'L1', 'insert', 'post'], ['signCert', 'L2', 'saveDocument', 'post'],
    ['signWallet', 'L1', 'select_doc', 'pre'], ['signWallet', 'L1', 'walk', 'pre'], ['signWallet', 'L1', 'insert', 'post'], ['signWallet', 'L2', 'saveDocument', 'post'],
    ['sigJson', 'L1', 'select_doc', 'pre'], ['sigJson', 'L2', 'getDocument', 'pre'],
  ];
  const out: string[] = [];
  const cases = ['none', ...Object.keys(VALUES)];
  for (const [rk, layer, point, when] of INJ) for (const vk of cases) {
    if (vk === 'none' && !(layer === 'L1' && (point === 'select_doc' || point === 'select_lc'))) continue;
    seed();
    const r = ROUTES[rk];
    G.__nonce = 'g149-' + crypto.randomBytes(6).toString('hex');
    if (r.nonce) repo.saveSigningRequest(G.__nonce, { documentId: DOC, walletAddress: 'addr_test1g149', hash: HASH, nonce: G.__nonce, expiresAt: new Date(Date.now() + 300000).toISOString() });
    if (vk !== 'none') { if (layer === 'L1') G.__fault = { at: point, when, v: VALUES[vk] }; else G.__repoFault = { fn: point, when, v: VALUES[vk] }; }
    const u0 = G.__unhandled, x0 = G.__uncaught, l0 = lines.length;
    const first = await call(r.m, r.p, r.body());
    await new Promise((res) => setTimeout(res, 120));
    const cellLines = lines.slice(l0).join('');
    const after1 = state();
    const faultConsumed = G.__fault === null && G.__repoFault === null;
    G.__fault = null; G.__repoFault = null;
    const nonceLeft = r.nonce ? !!repo.getSigningRequest(G.__nonce) : null;
    let retry: any = null, after2: any = null;
    if (when === 'post' && vk !== 'none') { const l1 = lines.length; retry = await call(r.m, r.p, r.body()); await new Promise((res) => setTimeout(res, 50)); after2 = state(); }
    const routeLine = cellLines.split('\n').filter((l) => l.includes(r.catchMsg)).map((l) => l.replace(/\x1b\[[0-9;]*m/g, '').replace(/^\S+ \S+ /, '').slice(0, 260));
    const otherErr = cellLines.split('\n').filter((l) => /error|warn/i.test(l) && !l.includes(r.catchMsg) && l.trim()).map((l) => l.replace(/\x1b\[[0-9;]*m/g, '').replace(/^\S+ \S+ /, '').slice(0, 200));
    out.push(JSON.stringify({ variant, env, route: rk, layer, point, when, value: vk, faultConsumed, first, unhandled: G.__unhandled - u0, uncaught: G.__uncaught - x0, wouldExit: G.__wouldExit, after1, nonceLeft, retry, after2, routeLine, otherLog: otherErr.slice(0, 4) }));
  }
  fs.writeFileSync(outFile, out.join('\n') + '\n');
  server.close(); authSrv.close();
  // production file transports: list what landed
  const ld = path.join(cwd, 'logs');
  if (fs.existsSync(ld)) for (const f of fs.readdirSync(ld)) fs.appendFileSync(outFile.replace(/\.jsonl$/, '.files.log'), `${ld}/${f} ${fs.statSync(path.join(ld, f)).size}\n`);
  realOut(`done ${variant} ${env} cells=${out.length} unhandledTotal=${G.__unhandled} uncaughtTotal=${G.__uncaught}\n`);
  setTimeout(() => process.exit(0), 300);
}
main().catch((e) => { realErr('PROBE FAIL ' + (e && e.stack) + '\n' + lines.slice(-20).join('') + '\n'); process.exit(2); });
