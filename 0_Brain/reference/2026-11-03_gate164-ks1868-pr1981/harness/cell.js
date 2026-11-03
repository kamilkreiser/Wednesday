// G164 recorder cell: one process per (version, site, kind). NODE_ENV from the parent (development|production).
// REAL base/head security service (src extracted by blob, transpiled verbatim), REAL express app driven over HTTP,
// REAL db.ts against a REAL migrated Postgres (gate164-pg, app role secuura_app, FORCE RLS), REAL @secuura/shared.
// The ONE substitution: index.js's `require('./db')` gets the real db module with `query` and `transaction` wrapped
// so that, while FAULT is armed, the retire UPDATE (retirePriorStatement: `UPDATE svc_api_keys ... RETURNING id`)
// rejects with the hostile value INSTEAD of being sent. Everything else is sent to Postgres.
// No process-level handlers: an unhandled rejection takes Node's default (exit 1).
// argv: version(base|head|<build dir>) site(route|routeUp|direct|directUp) kind
const path = require('path');
const crypto = require('crypto');
const Module = require('module');
const [, , version, site, kind] = process.argv;
const W = path.resolve(__dirname, '..');
const SEC = path.join(W, 'repo/Blockchain/Dev/services/security');
const BUILD = process.env.G164_BUILD || path.join(__dirname, 'build_' + version);
const out = { version, site, kind, env: process.env.NODE_ENV, build: path.basename(BUILD) };

// ---- values ----
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMessage = (m) => Object.create(Error.prototype, { message: { get() { return m; } } });
const KINDS = {
  ordinaryError: () => new Error('g164 boom'),
  plainString: () => 'g164 boom',
  number42: () => 42,
  null: () => null,
  undefined: () => undefined,
  revokedProxy: revoked,
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  symbolMessage: () => withMessage(Symbol('g164')),
  bigintMessage: () => withMessage(10n),
  bigintValue: () => 10n,
  messageToJSONThrows: () => withMessage({ toJSON() { throw new Error('toJSON boom'); } }),
  errToJSONThrows: () => { const e = new Error('g164 boom'); e.toJSON = () => { throw new Error('toJSON boom'); }; return e; },
  objToStringThrows: () => ({ toString() { throw new Error('toString boom'); } }),
  messageToStringThrows: () => withMessage({ toString() { throw new Error('toString boom'); } }),
  messageIsRevokedProxy: () => withMessage(revoked()),
  cyclicMessage: () => { const o = { a: 1 }; o.self = o; return withMessage(o); },
  numberMessage: () => withMessage(42),
  nullMessage: () => withMessage(null),
  nullProtoMessage: () => withMessage(Object.create(null)),
};
if (!KINDS[kind]) { console.error('unknown kind', kind); process.exit(2); }
const UP = /Up$/.test(site);
// routeLock: no injected value; a superuser holds FOR UPDATE on the prior row so the real retire UPDATE hits lock_timeout

// ---- env (no secrets of any real system; local throwaway container) ----
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
process.env.SECURITY_DISABLE_BOOT = '1';
process.env.PII_ENCRYPTION_KEY = crypto.randomBytes(32).toString('hex'); // throwaway per process: production refuses to start without one (index.ts:2193-2196)
process.env.DATABASE_URL = 'postgres://secuura_app:g164app@127.0.0.1:55164/secuura';
process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }).toString(), 'utf8').toString('base64');
delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL; delete process.env.API_KEY_ROTATION_GRACE_SECONDS;
const b64url = (b) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function token(claims) {
  const h = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const p = b64url(Buffer.from(JSON.stringify({ sub: 'g164', iat: now, exp: now + 600, ...claims })));
  return `${h}.${p}.${b64url(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), PRIVATE_PEM))}`;
}

// ---- the fault seam ----
let FAULT = false;
out.faultFired = 0;
const RETIRE = /^\s*UPDATE\s+svc_api_keys\b[\s\S]*RETURNING\s+id\s*$/i;
let realDb;
const origLoad = Module._load;
let dbWrapper;
Module._load = function (req, parent, isMain) {
  if (req === './db' && parent && parent.filename === path.join(BUILD, 'index.js')) return dbWrapper;
  if (!req.startsWith('.') && !req.startsWith('/') && !req.startsWith('node:') && !Module.isBuiltin(req))
    return origLoad.call(this, require.resolve(req, { paths: [SEC] }), parent, isMain);
  return origLoad.apply(this, arguments);
};
realDb = require(path.join(BUILD, 'db.js'));
const wrappedClient = (client) => new Proxy(client, {
  get(t, p) {
    if (p === 'query') return (text, ...rest) => {
      if (FAULT && typeof text === 'string' && RETIRE.test(text)) { out.faultFired += 1; return Promise.reject(KINDS[kind]()); }
      return t.query(text, ...rest);
    };
    const v = t[p]; return typeof v === 'function' ? v.bind(t) : v;
  },
});
dbWrapper = {
  ...realDb,
  query: (text, params) => {
    if (FAULT && typeof text === 'string' && RETIRE.test(text)) { out.faultFired += 1; return Promise.reject(KINDS[kind]()); }
    return realDb.query(text, params);
  },
  transaction: (fn) => realDb.transaction((client) => fn(wrappedClient(client))),
};

// ---- capture stdout/stderr (the service's log() is console.log JSON lines) ----
const logLines = [];
const origOut = process.stdout.write.bind(process.stdout);
process.stdout.write = (c) => { logLines.push(String(c)); return true; };
process.stderr.write = (c) => { logLines.push(String(c)); return true; };
let emitted = false;
function emitResult() {
  if (emitted) return; emitted = true;
  const all = logLines.join('').split('\n').filter(Boolean);
  out.failLines = all.filter((l) => l.includes('KS-577: revoke-on-rotate FAILED')).map((l) => { try { const j = JSON.parse(l); return { error: j.error === undefined ? '<omitted>' : j.error }; } catch { return { raw: l.slice(0, 200) }; } });
  out.mintRefusedLines = all.filter((l) => l.includes('KS-888: API key mint refused')).length;
  out.otherErrors = all.filter((l) => /"level":"error"|error:/i.test(l) && !l.includes('KS-577') && !l.includes('KS-888')).map((l) => l.slice(0, 200));
  origOut('G164RESULT ' + JSON.stringify(out) + '\n');
}
process.on('exit', (code) => { out.exitCode = code; if (!out.done) out.died = true; emitResult(); });

async function main() {
  const { Pool } = require(require.resolve('pg', { paths: [SEC] }));
  const superPool = new Pool({ connectionString: 'postgres://secuura:g164super@127.0.0.1:55164/secuura', max: 2 });
  if (site === 'routeLock') await superPool.query("ALTER ROLE secuura_app SET lock_timeout = '500ms'"); // a REAL pg failure of the retire alone: 55P03
  if (!(await realDb.initDb()) || !realDb.isDbAvailable()) throw new Error('initDb did not connect');
  const idx = require(path.join(BUILD, 'index.js'));
  const app = idx.default;
  const server = await new Promise((r) => { const s = app.listen(0, '127.0.0.1', () => r(s)); });
  const base = `http://127.0.0.1:${server.address().port}`;
  const TENANT = 'a0000000-0000-4000-8000-000000000164';
  const ORG = 'abcdef00-0164-4164-8164-000000000164';
  const connector = `g164:${version}:${site}:${kind}:${crypto.randomUUID()}`;
  out.connector = connector;
  const mint = async (rotate, name) => {
    const res = await fetch(`${base}/api/keys`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token({ role: 'super_admin' })}` },
      body: JSON.stringify({ name, scopes: ['documents:read'], tenantId: TENANT, organizationId: ORG, connectorId: connector, rotate }) });
    const t = await res.text(); let d = {}; try { d = JSON.parse(t).data || {}; } catch { /* non-JSON */ }
    return { status: res.status, id: d.id ?? null, key: d.key ?? null, hasPKR: 'priorKeysRevoked' in d, priorKeysRevoked: d.priorKeysRevoked };
  };
  const validate = async (key) => {
    const res = await fetch(`${base}/api/keys/validate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key }) });
    const b = await res.json().catch(() => ({}));
    return { status: res.status, valid: b?.data?.valid ?? null };
  };
  const rows = async () => (await superPool.query('SELECT id, is_active FROM svc_api_keys WHERE connector_id = $1', [connector])).rows;

  const seed = await mint(false, 'g164 seed');
  out.seedStatus = seed.status;
  out.priorValidBefore = (await validate(seed.key)).valid; // control: the prior works before the rotate

  if (site === 'route' || site === 'routeUp' || site === 'routeLock') {
    FAULT = !UP && site !== 'routeLock';
    let locker = null;
    if (site === 'routeLock') { locker = await superPool.connect(); await locker.query('BEGIN'); await locker.query('SELECT id FROM svc_api_keys WHERE id = $1 FOR UPDATE', [seed.id]); }
    const r = await mint(true, 'g164 rotate');
    if (locker) { await locker.query('ROLLBACK'); locker.release(); await superPool.query('ALTER ROLE secuura_app RESET lock_timeout'); }
    FAULT = false;
    out.rotateStatus = r.status; out.newKeyIssued = !!r.key; out.hasPKR = r.hasPKR; out.priorKeysRevoked = r.priorKeysRevoked;
    out.newKeyValid = r.key ? (await validate(r.key)).valid : 'no key issued';
    const rs = await rows();
    out.newRowActive = r.id ? (rs.find((x) => x.id === r.id)?.is_active ?? 'no row') : 'no id';
    out.rowsTotal = rs.length;
  } else {
    FAULT = !UP;
    const keep = `key_g164_keep_${crypto.randomUUID()}`;
    out.directOutcome = await idx.revokePriorConnectorKeys(connector, TENANT, keep).then((v) => 'resolved:' + JSON.stringify(v), () => 'REJECTED');
    FAULT = false;
    out.priorInMemoryActive = idx.memApiKeys.get(seed.id)?.isActive ?? 'absent';
  }
  out.priorValidAfterInProcess = (await validate(seed.key)).valid;
  const rs = await rows();
  out.priorRowActive = rs.find((x) => x.id === seed.id)?.is_active ?? 'no row';
  out.activeRows = rs.filter((x) => x.is_active).length;
  server.close();
  await superPool.end();
  await realDb.closeDb();
  out.done = true;
}
main().then(() => { emitResult(); setTimeout(() => process.exit(0), 50); }, (e) => { out.mainError = String(e && e.message).slice(0, 200); emitResult(); setTimeout(() => process.exit(3), 50); });
