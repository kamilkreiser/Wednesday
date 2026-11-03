// Gate 167 driver: boots the REAL referral service (node + tsx, real index.ts: helmet, boundedJson, rejectNulBytes,
// app.use('/api', authenticate()) from @secuura/shared, the real routes, services, error handler and logger, real `pg`)
// against a REAL PostgreSQL 15 (container g167-pg), at base (PR parent 1e6df0b6) or head (68897dda).
// Principals are REAL RS256 JWTs signed by a key whose public half is the service's JWT_PUBLIC_KEY.
// Per cell: TRUNCATE + seed, one request, then measure: status, referral rows, reward rows, code uses, fraud-log rows,
// every row write (AFTER triggers -> g167_writes, admin-owned), every statement the app role sent (log_statement=all
// for the app role, bracketed by admin markers), and the service's own log lines during the cell.
// argv: <ver base|head>  -> logs/probe/<ver>.json
const { spawn, spawnSync } = require('child_process');
const crypto = require('crypto'); const fs = require('fs'); const net = require('net');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate167-ks1572-pr1984';
const D = W + '/repo/Blockchain/Dev';
const { Client } = require(D + '/node_modules/pg');
const [ver] = process.argv.slice(2);
const T = ver === 'head' ? `${D}/services/referral` : `${W}/scratch/wt/${ver}/Blockchain/Dev/services/referral`;
const PGPORT = 55167;
const ADMIN = `postgres://postgres@127.0.0.1:${PGPORT}/g167`;
const APPURL = `postgres://g167_app@127.0.0.1:${PGPORT}/g167`;
const OUT = `${W}/logs/probe/${ver}${process.env.G167_TAG ? '_' + process.env.G167_TAG : ''}.json`;
const DDL = fs.readFileSync(W + '/scripts/referral_ddl_from_repo.sql', 'utf8');
// The repo has NO DDL for svc_referral_milestones_rewards (G153-F4); same shape gates 162/163 used.
const MRDDL = `CREATE TABLE svc_referral_milestones_rewards (id TEXT PRIMARY KEY, user_id TEXT NOT NULL, type TEXT NOT NULL,
  amount BIGINT NOT NULL DEFAULT 0, status TEXT NOT NULL DEFAULT 'PENDING', source_id TEXT NOT NULL, source_type TEXT NOT NULL DEFAULT 'REFERRAL',
  transaction_hash TEXT, metadata JSONB DEFAULT '{}', created_at TIMESTAMPTZ DEFAULT NOW(), claimed_at TIMESTAMPTZ);`;
// Minimal users table (NOT the full migration chain): the columns getLinkedWalletAddress reads, FORCE RLS on the tenant GUC
// the shared applyTenantGuc sets (app.current_tenant_id), so the app role sees a row only under its tenant.
const USERSDDL = `CREATE TABLE users (id UUID PRIMARY KEY, email TEXT, tenant_id UUID NOT NULL, wallet_address TEXT, role TEXT, status TEXT);
  ALTER TABLE users ENABLE ROW LEVEL SECURITY; ALTER TABLE users FORCE ROW LEVEL SECURITY;
  CREATE POLICY users_tenant ON users USING (tenant_id::text = current_setting('app.current_tenant_id', true));`;
const TABLES = ['svc_referral_codes', 'svc_referrals', 'svc_referral_rewards', 'svc_referral_milestones', 'svc_referral_fraud_log', 'svc_referral_milestones_rewards'];

const TEN = 'a0000000-0000-4000-8000-000000001672';
const A = 'a1672aaa-1672-4672-8672-00000000000a';   // referrer, owns code G167AAAA, linked wallet addr_A
const X = 'b1672bbb-1672-4672-8672-00000000000b';   // ordinary caller, linked wallet addr_X
const V = 'e1672eee-1672-4672-8672-00000000000e';   // victim who never signs in
const Y = 'f1672fff-1672-4672-8672-00000000000f';   // caller whose LINKED wallet is the referrer's wallet addr_A
const N = 'c1672ccc-1672-4672-8672-00000000000c';   // caller with NO linked wallet

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const b64u = (b) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const OMIT = Symbol('omit');
function jwt(claims) {
  const h = b64u(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' }))); const now = Math.floor(Date.now() / 1000);
  const p = b64u(Buffer.from(JSON.stringify({ verificationLevel: 'BASIC', iat: now, exp: now + 600, ...claims })));
  return `Bearer ${h}.${p}.${b64u(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), privateKey))}`;
}
function who(userId, { role = 'USER', email = 'g167-token@example.test', tenantId = TEN } = {}) {
  const c = { role, tenantId }; if (email !== OMIT) c.email = email;
  if (userId !== OMIT) { c.userId = userId; c.sub = typeof userId === 'string' ? userId : String(userId); }
  return jwt(c);
}
const freePort = () => new Promise((r) => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => r(p)); }); });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const strip = (s) => s.replace(/\x1b\[[0-9;]*m/g, '');

let admin;
const adm = (sql, params) => admin.query(sql, params);
async function resetSchema() {
  await adm(`DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'g167_app') THEN CREATE ROLE g167_app LOGIN; END IF; END $$`);
  await adm(`ALTER ROLE g167_app SET log_statement = 'all'`);
  await adm(`ALTER SYSTEM SET log_line_prefix = '%m [%p] %u '`); await adm(`SELECT pg_reload_conf()`);
  await adm(`SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'g167_app'`);
  await adm(`DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public; GRANT USAGE ON SCHEMA public TO g167_app;`);
  await adm(DDL); await adm(MRDDL); await adm(USERSDDL);
  await adm(`CREATE TABLE g167_writes (id BIGSERIAL PRIMARY KEY, tbl TEXT, op TEXT, who TEXT, at TIMESTAMPTZ DEFAULT clock_timestamp())`);
  await adm(`CREATE FUNCTION g167_log() RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER AS $$
    BEGIN INSERT INTO g167_writes (tbl, op, who) VALUES (TG_TABLE_NAME, TG_OP, session_user); RETURN NULL; END $$`);
  for (const t of [...TABLES, 'users']) await adm(`CREATE TRIGGER g167_w AFTER INSERT OR UPDATE OR DELETE ON ${t} FOR EACH ROW EXECUTE FUNCTION g167_log()`);
  await adm(`GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO g167_app; REVOKE ALL ON g167_writes FROM g167_app;`);
}
async function seed({ usersReadable = true } = {}) {
  await adm(`TRUNCATE ${TABLES.join(', ')}, users`);
  await adm(`INSERT INTO svc_referral_codes (id, code, owner_id, owner_wallet_address) VALUES ('code-A', 'G167AAAA', $1, 'addr_A')`, [A]);
  const u = (id, w) => adm(`INSERT INTO users (id, email, tenant_id, wallet_address, role, status) VALUES ($1, $2, $3, $4, 'user', 'active')`, [id, `u-${id.slice(0, 4)}@example.test`, TEN, w]);
  await u(A, 'addr_A'); await u(X, 'addr_X'); await u(V, 'addr_V'); await u(Y, 'addr_A'); await u(N, null);
  if (usersReadable) await adm(`GRANT SELECT ON users TO g167_app`); else await adm(`REVOKE SELECT ON users FROM g167_app`);
  await adm(`TRUNCATE g167_writes`);
}
async function measure() {
  const rows = async (sql) => (await adm(sql)).rows;
  const ref = await rows(`SELECT referred_user_id AS u, status, referred_wallet_address AS w, fraud_check_passed AS ok, fraud_flags::text AS flags FROM svc_referrals ORDER BY created_at`);
  const rew = await rows(`SELECT user_id AS u, type, amount::text AS amount, status FROM svc_referral_rewards ORDER BY created_at`);
  const code = (await rows(`SELECT current_uses FROM svc_referral_codes WHERE id = 'code-A'`))[0];
  const fl = await rows(`SELECT ip_address AS ip, device_fingerprint AS dev, referrer_id AS referrer, flag_type AS flag FROM svc_referral_fraud_log`);
  const w = (await rows(`SELECT tbl, op, count(*)::int AS n FROM g167_writes GROUP BY 1,2 ORDER BY 1,2`)).map((r) => `${r.tbl}:${r.op}:${r.n}`);
  const nm = (x) => x === A ? 'A' : x === X ? 'X' : x === V ? 'V' : x === Y ? 'Y' : x === N ? 'N' : x === X.toUpperCase() ? 'X_UPPER' : x;
  return { referrals: ref.map((r) => ({ ...r, u: nm(r.u) })), rewards: rew.map((r) => ({ ...r, u: nm(r.u) })), codeUses: code && code.current_uses,
    fraudLog: fl.map((r) => ({ ...r, referrer: nm(r.referrer) })), writes: w, writeRows: w.reduce((s, x) => s + Number(x.split(':')[2]), 0) };
}
async function boot(dbUrl) {
  const port = await freePort();
  const env = { PATH: process.env.PATH, HOME: W + '/home', TMPDIR: W + '/tmp', PORT: String(port), DATABASE_URL: dbUrl,
    JWT_PUBLIC_KEY: Buffer.from(publicKey.export({ type: 'spki', format: 'pem' })).toString('base64') };
  const child = spawn(process.execPath, ['--import', 'file://' + D + '/node_modules/tsx/dist/loader.mjs', T + '/src/index.ts'],
    { cwd: W + '/logs/child_cwd', env, stdio: ['ignore', 'pipe', 'pipe'] });
  const p = { port, child, out: '', exited: null };
  child.stdout.on('data', (d) => { p.out += strip(String(d)); }); child.stderr.on('data', (d) => { p.out += strip(String(d)); });
  child.on('exit', (code, sig) => { p.exited = { code, sig }; });
  const t0 = Date.now();
  while (!(/Database initialization/.test(p.out) && /Referral Service running/.test(p.out)) && p.exited === null && Date.now() - t0 < 90000) await sleep(100);
  await sleep(300);
  return p;
}
async function post(p, path, { auth, body, xff }) {
  try {
    const h = { 'Content-Type': 'application/json' }; if (auth !== undefined) h.Authorization = auth; if (xff) h['X-Forwarded-For'] = xff;
    const r = await fetch(`http://127.0.0.1:${p.port}${path}`, { method: 'POST', headers: h, body: JSON.stringify(body), signal: AbortSignal.timeout(20000) });
    let b = await r.text(); try { b = JSON.parse(b); } catch {}
    return { status: r.status, code: b && b.error && b.error.code, msg: b && b.error && String(b.error.message).slice(0, 80), bonus: b && b.data && b.data.signupBonus };
  } catch (e) { return { status: 'ERR ' + String(e && e.message).slice(0, 80) }; }
}
const body = (userId, extra = {}) => ({ code: 'G167AAAA', userId, walletAddress: 'addr_from_body', ipAddress: '203.0.113.7', deviceId: 'dev-from-body', email: 'body@example.test', ...extra });
const AP = '/api/referrals/apply';
// [label, path, request, seedOpts]
function cells() {
  return [
    ['Q1 USER X, body userId = victim V', AP, { auth: who(X), body: body(V) }],
    ['Q1 no Authorization header, body userId = V', AP, { body: body(V) }],
    ['Q1 token with NO userId claim (sub = X), body userId = X', AP, { auth: who(OMIT), body: body(X) }],
    ['Q1 token userId "" , body userId = V', AP, { auth: who(''), body: body(V) }],
    ['Q1 token userId numeric 1672, body userId = V', AP, { auth: who(1672), body: body(V) }],
    ['Q1 token userId [X] (array), body userId = X', AP, { auth: who([X]), body: body(X) }],
    ['Q1 SYSTEM_ADMIN X naming V', AP, { auth: who(X, { role: 'SYSTEM_ADMIN' }), body: body(V) }],
    ['Q1 SUPER_ADMIN X naming V', AP, { auth: who(X, { role: 'SUPER_ADMIN' }), body: body(V) }],
    ['Q1 body userId = X upper-cased', AP, { auth: who(X), body: body(X.toUpperCase()) }],
    ['Q1 token userId = X upper-cased, body userId = X', AP, { auth: who(X.toUpperCase()), body: body(X) }],
    ['Q1 body userId = " " + X (space-padded)', AP, { auth: who(X), body: body(' ' + X) }],
    ['Q1 body userId = X + " " (space-padded)', AP, { auth: who(X), body: body(X + ' ') }],
    ['Q1 bad body (no code) + body userId = V', AP, { auth: who(X), body: { userId: V } }],
    ['Q1 path /API/Referrals/Apply (case) naming V', '/API/Referrals/Apply', { auth: who(X), body: body(V) }],
    ['Q1 path trailing slash naming V', AP + '/', { auth: who(X), body: body(V) }],
    ['Q1 forged x-user-id header = V on X token, body V', AP, { auth: who(X), body: body(V) }],
    ['Q1 X token, tenant claim missing, body V', AP, { auth: jwt({ userId: X, sub: X, role: 'USER' }), body: body(V) }],
    ['Q4 OWN id X (control, 201)', AP, { auth: who(X), body: body(X) }],
    ['Q4 OWN id X, body with NO wallet/ip/device/email', AP, { auth: who(X), body: { code: 'G167AAAA', userId: X } }],
    ['Q4 OWN id X, body walletAddress = referrer wallet addr_A', AP, { auth: who(X), body: body(X, { walletAddress: 'addr_A' }) }],
    ['Q4 OWN id Y (LINKED wallet = referrer wallet addr_A), body omits wallet', AP, { auth: who(Y), body: { code: 'G167AAAA', userId: Y } }],
    ['Q4 OWN id N (no linked wallet)', AP, { auth: who(N), body: body(N) }],
    ['Q4 OWN id X, token email disposable (mailinator)', AP, { auth: who(X, { email: 'x@mailinator.com' }), body: body(X) }],
    ['Q4 OWN id X, body email disposable, token email normal', AP, { auth: who(X), body: body(X, { email: 'x@mailinator.com' }) }],
    ['Q4 OWN id X, token without tenantId', AP, { auth: jwt({ userId: X, sub: X, role: 'USER', email: 'g167-token@example.test' }), body: body(X) }],
    ['Q1 OWN id X, users table UNREADABLE (wallet read fails)', AP, { auth: who(X), body: body(X) }, { usersReadable: false }],
    ['Q1 OWN id A (self-referral, own code)', AP, { auth: who(A), body: body(A) }],
  ];
}
function pgLog() { const r = spawnSync('docker', ['logs', 'g167-pg'], { encoding: 'utf8', maxBuffer: 1 << 28 }); return (r.stdout || '') + (r.stderr || ''); }

(async () => {
  admin = new Client({ connectionString: ADMIN }); await admin.connect();
  await adm(`SET log_statement = 'all'`);
  const res = { ver, tree: T, at: new Date().toISOString(), rows: [] };
  let p;
  try {
    await resetSchema();
    await seed();
    p = await boot(APPURL);
    res.bootLine = (p.out.match(/Database initialization[^\n]*/) || [''])[0].slice(0, 160);
    res.exitedAtBoot = p.exited;
    const list = cells();
    for (let i = 0; i < list.length; i++) {
      const [label, path, req, so] = list[i];
      if (label.startsWith('Q1 forged')) req.headersExtra = true;
      await seed(so);
      const mark = `G167MARK-${ver}-${i}`;
      await adm(`SELECT $1::text AS m`, [mark + '-start']);
      const outStart = p.out.length;
      let r;
      if (req.headersExtra) {
        r = await (async () => { const h = { 'Content-Type': 'application/json', Authorization: req.auth, 'x-user-id': V, 'x-user-role': 'SYSTEM_ADMIN' };
          const rr = await fetch(`http://127.0.0.1:${p.port}${path}`, { method: 'POST', headers: h, body: JSON.stringify(req.body) });
          let b = await rr.text(); try { b = JSON.parse(b); } catch {} return { status: rr.status, code: b && b.error && b.error.code, bonus: b && b.data && b.data.signupBonus }; })();
      } else r = await post(p, path, req);
      await sleep(250);
      await adm(`SELECT $1::text AS m`, [mark + '-end']);
      const m = await measure();
      const svcLog = p.out.slice(outStart).split('\n').filter((l) => /error|warn|Referral applied|Reward created|Fraud check completed|INTERNAL/i.test(l)).map((l) => l.slice(0, 220));
      res.rows.push({ i, label, status: r.status, code: r.code, msg: r.msg, bonus: r.bonus, ...m, svcLog });
    }
    await sleep(800);
    const log = pgLog().split('\n');
    for (const row of res.rows) {
      const s = log.findIndex((l) => l.includes(`G167MARK-${ver}-${row.i}-start`)); const e = log.findIndex((l) => l.includes(`G167MARK-${ver}-${row.i}-end`));
      const seg = s >= 0 && e > s ? log.slice(s + 1, e) : null;
      row.appStatements = seg ? seg.filter((l) => / g167_app /.test(l) && /statement:|execute /.test(l)).length : 'MARKERS-NOT-FOUND';
    }
  } catch (e) { res.driverError = String(e && e.stack || e); }
  if (p) { res.pid = p.child.pid; p.child.kill('SIGTERM'); await sleep(600); if (p.exited === null) p.child.kill('SIGKILL'); await sleep(200); res.exitedAtEnd = p.exited; }
  await admin.end();
  fs.writeFileSync(OUT, JSON.stringify(res, null, 1));
  console.log(JSON.stringify({ ver, rows: res.rows.length, err: res.driverError && res.driverError.slice(0, 300) }));
  process.exit(0);
})();
