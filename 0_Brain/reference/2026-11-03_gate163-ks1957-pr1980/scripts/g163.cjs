// Gate 163 driver: boots the REAL referral service (node + tsx, real index.ts with the real @secuura/shared authenticate()
// mounted on /api, real routes, real services, real `pg`) against a REAL PostgreSQL 15 (container g163-pg), base or head.
// Every principal is a REAL RS256 JWT signed by a key whose public half is the service's JWT_PUBLIC_KEY, so the claim set
// (userId, role) reaches the route exactly as the verifier decodes it. Nothing in the service is stubbed.
// Per cell: TRUNCATE + seed, one request, then measure: HTTP status, award rows (milestone rewards + referral rewards),
// referral status, every row write (AFTER triggers on every table -> g163_writes, admin-owned), and every SQL statement
// the app role sent (postgres log_statement=all for the app role, bracketed by admin markers).
// argv: <ver base|head>  -> logs/probe/<ver>.json
const { spawn, execFileSync } = require('child_process');
const crypto = require('crypto'); const fs = require('fs'); const net = require('net');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980';
const D = W + '/repo/Blockchain/Dev';
const { Client } = require(D + '/node_modules/pg');
const [ver] = process.argv.slice(2);
const T = ver === 'head' ? `${W}/repo/Blockchain/Dev/services/referral` : `${W}/wt/${ver}/Blockchain/Dev/services/referral`;
const PGPORT = process.env.G163_PGPORT;
const ADMIN = `postgres://postgres@127.0.0.1:${PGPORT}/g163`;
const APPURL = `postgres://g163_app@127.0.0.1:${PGPORT}/g163`;
const OUT = `${W}/logs/probe/${ver}${process.env.G163_EXTRA ? '_' + process.env.G163_EXTRA : ''}.json`;
const DDL = fs.readFileSync(W + '/scripts/referral_ddl_from_repo.sql', 'utf8');
// The repo has NO DDL for svc_referral_milestones_rewards (G153-F4); same shape gate 162 used ('pk').
const MRDDL = `CREATE TABLE svc_referral_milestones_rewards (id TEXT PRIMARY KEY, user_id TEXT NOT NULL, type TEXT NOT NULL,
  amount BIGINT NOT NULL DEFAULT 0, status TEXT NOT NULL DEFAULT 'PENDING', source_id TEXT NOT NULL, source_type TEXT NOT NULL DEFAULT 'REFERRAL',
  transaction_hash TEXT, metadata JSONB DEFAULT '{}', created_at TIMESTAMPTZ DEFAULT NOW(), claimed_at TIMESTAMPTZ);`;
const TABLES = ['svc_referral_codes', 'svc_referrals', 'svc_referral_rewards', 'svc_referral_milestones', 'svc_referral_fraud_log', 'svc_referral_milestones_rewards'];

const A = 'a1957aaa-1957-4957-8957-00000000000a';   // /check target: 1 QUALIFIED referral -> FIRST milestone if the check runs
const X = 'b1957bbb-1957-4957-8957-00000000000b';   // another ordinary user
const B = 'c1957ccc-1957-4957-8957-00000000000c';   // /qualify referrer (0 qualified)
const Q = 'd1957ddd-1957-4957-8957-00000000000d';   // /qualify referee: PENDING referral from B
const NUM = '1957';                                 // a referrer whose id is the path string '1957' (1 QUALIFIED)

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const other = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 }).privateKey;
const b64u = (b) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const OMIT = Symbol('omit');
function jwtWith(claims, { key = privateKey, alg = 'RS256' } = {}) {
  const h = b64u(Buffer.from(JSON.stringify({ alg, typ: 'JWT' }))); const now = Math.floor(Date.now() / 1000);
  const p = b64u(Buffer.from(JSON.stringify({ email: 'g163@example.test', verificationLevel: 'BASIC', iat: now, exp: now + 600, ...claims })));
  let sig = '';
  if (alg === 'RS256') sig = b64u(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), key));
  if (alg === 'HS256') sig = b64u(crypto.createHmac('sha256', publicKey.export({ type: 'spki', format: 'pem' })).update(`${h}.${p}`).digest());
  return `${h}.${p}.${sig}`;
}
function principal(userId, role) {
  const c = {}; if (userId !== OMIT) { c.userId = userId; c.sub = typeof userId === 'string' ? userId : String(userId); }
  if (role !== OMIT) c.role = role; return c;
}
const freePort = () => new Promise((r) => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => r(p)); }); });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const strip = (s) => s.replace(/\x1b\[[0-9;]*m/g, '');

let admin;
const adm = (sql, params) => admin.query(sql, params);
async function resetSchema() {
  await adm(`DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'g163_app') THEN CREATE ROLE g163_app LOGIN; END IF; END $$`);
  await adm(`ALTER ROLE g163_app SET log_statement = 'all'`);
  await adm(`SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'g163_app'`);
  await adm(`DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public; GRANT USAGE ON SCHEMA public TO g163_app;`);
  await adm(DDL); await adm(MRDDL);
  await adm(`CREATE TABLE g163_writes (id BIGSERIAL PRIMARY KEY, tbl TEXT, op TEXT, who TEXT, at TIMESTAMPTZ DEFAULT clock_timestamp())`);
  await adm(`CREATE FUNCTION g163_log() RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER AS $$
    BEGIN INSERT INTO g163_writes (tbl, op, who) VALUES (TG_TABLE_NAME, TG_OP, session_user); RETURN NULL; END $$`);
  for (const t of TABLES) await adm(`CREATE TRIGGER g163_w AFTER INSERT OR UPDATE OR DELETE ON ${t} FOR EACH ROW EXECUTE FUNCTION g163_log()`);
  for (const t of TABLES) await adm(`CREATE TRIGGER g163_wt AFTER TRUNCATE ON ${t} FOR EACH STATEMENT EXECUTE FUNCTION g163_log()`);
  await adm(`GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO g163_app; REVOKE ALL ON g163_writes FROM g163_app;`);
}
async function seed() {
  await adm(`TRUNCATE ${TABLES.join(', ')}`);
  const code = async (owner, c) => adm(`INSERT INTO svc_referral_codes (id, code, owner_id) VALUES ($1, $2, $3)`, ['code-' + owner, c, owner]);
  await code(A, 'G163AAAA'); await code(B, 'G163BBBB'); await code(NUM, 'G1631957');
  const ins = (id, codeOwner, referrer, referred, status, q) => adm(`INSERT INTO svc_referrals (id, referral_code_id, referrer_id, referred_user_id, status,
    referrer_reward, referred_reward, fraud_check_passed, qualified_at) VALUES ($1, $2, $3, $4, $5, 50000000, 25000000, true, ${q ? 'NOW()' : 'NULL'})`,
    [id, 'code-' + codeOwner, referrer, referred, status]);
  await ins('ref-a-1', A, A, 'u-a-1', 'QUALIFIED', true);
  await ins('ref-n-1', NUM, NUM, 'u-n-1', 'QUALIFIED', true);
  await ins('pend-q', B, B, Q, 'PENDING', false);
  await adm(`TRUNCATE g163_writes`);
}
async function measure() {
  const one = async (sql) => (await adm(sql)).rows[0];
  const mr = await one(`SELECT count(*)::int AS n, COALESCE(sum(amount),0)::text AS sum, string_agg(user_id || ':' || source_id, ',' ORDER BY user_id, source_id) AS who FROM svc_referral_milestones_rewards`);
  const rr = await one(`SELECT count(*)::int AS n, COALESCE(sum(amount),0)::text AS sum, string_agg(user_id || ':' || type, ',' ORDER BY user_id, type) AS who FROM svc_referral_rewards`);
  const pend = await one(`SELECT status FROM svc_referrals WHERE id = 'pend-q'`);
  const prog = await one(`SELECT count(*)::int AS n FROM svc_referral_milestones`);
  const w = (await adm(`SELECT tbl, op, count(*)::int AS n FROM g163_writes GROUP BY 1,2 ORDER BY 1,2`)).rows.map((r) => `${r.tbl}:${r.op}:${r.n}`);
  return { milestoneAwards: mr.n, milestoneSum: mr.sum, milestoneWho: mr.who, referralRewards: rr.n, referralRewardSum: rr.sum, referralRewardWho: rr.who,
    pendingReferral: pend && pend.status, progressRows: prog.n, writes: w, writeRows: w.reduce((s, x) => s + Number(x.split(':')[2]), 0),
    awards: mr.n + rr.n + (pend && pend.status !== 'PENDING' ? 1 : 0) };
}

async function boot(dbUrl) {
  const port = await freePort();
  const env = { PATH: process.env.PATH, HOME: process.env.HOME, TMPDIR: process.env.TMPDIR, PORT: String(port), DATABASE_URL: dbUrl,
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
async function http(p, path, { auth, body, headers = {} }) {
  try {
    const h = { 'Content-Type': 'application/json', ...headers }; if (auth !== undefined) h.Authorization = auth;
    const r = await fetch(`http://127.0.0.1:${p.port}${path}`, { method: 'POST', headers: h, body: JSON.stringify(body === undefined ? {} : body), signal: AbortSignal.timeout(20000) });
    let b = await r.text(); try { b = JSON.parse(b); } catch {}
    return { status: r.status, code: b && b.error && b.error.code, data: b && b.data ? Object.keys(b.data).join('|') : undefined };
  } catch (e) { return { status: 'ERR ' + String(e && e.message).slice(0, 80) }; }
}
const bearer = (claims, o) => 'Bearer ' + jwtWith(claims, o);

// [id, route, label, request-builder]. route: check -> POST /api/milestones/check/<path>; qualify -> POST /api/referrals/qualify {userId: Q}
const roleCells = [
  ['USER-other', X, 'USER'], ['ORG_ADMIN', X, 'ORG_ADMIN'], ['ADMIN', X, 'ADMIN'], ['ISSUER_ADMIN', X, 'ISSUER_ADMIN'], ['ISSUER_APPROVER', X, 'ISSUER_APPROVER'],
  ['OWNER-role', X, 'OWNER'], ['VERIFIER', X, 'VERIFIER'], ['connector', 'connector:api-key', 'connector'], ['admin-lower(auth-platform)', X, 'admin'],
  ['platform_admin(tokenisation-list)', X, 'platform_admin'],
  ['SYSTEM_ADMIN', X, 'SYSTEM_ADMIN'], ['SUPER_ADMIN', X, 'SUPER_ADMIN'], ['super_admin', X, 'super_admin'], ['system_admin', X, 'system_admin'], ['Super_Admin', X, 'Super_Admin'],
  ['array[SUPER_ADMIN]', X, ['SUPER_ADMIN']], ['array[SYSTEM_ADMIN]', X, ['SYSTEM_ADMIN']], ['dotless-i SUPER_ADMıN', X, 'SUPER_ADMıN'], ['long-s ſUPER_ADMIN', X, 'ſUPER_ADMIN'],
  ['dotless-i SYSTEM_ADMıN', X, 'SYSTEM_ADMıN'], ['lead-space " SUPER_ADMIN"', X, ' SUPER_ADMIN'], ['trail-space "SUPER_ADMIN "', X, 'SUPER_ADMIN '],
  ['trail-newline', X, 'SUPER_ADMIN\n'], ['NUL-suffix', X, 'SUPER_ADMIN\u0000'], ['fullwidth Ｓ', X, 'ＳUPER_ADMIN'], ['zero-width-joiner', X, 'SUPER_‍ADMIN'],
  ['object role', X, { toString: 'SUPER_ADMIN' }], ['null role', X, null], ['missing role', X, OMIT], ['number role', X, 1],
];
function cells() {
  const out = [];
  if (process.env.G163_EXTRA === 'apply') {
    // Pre-existing (not this PR): POST /api/referrals/apply takes userId from the BODY. A USER X attaches victim V to A's code.
    const V = 'e1957eee-1957-4957-8957-00000000000e';
    out.push(['apply', 'USER X applies A\'s code FOR victim V (body userId=V)', '/api/referrals/apply', { auth: bearer(principal(X, 'USER')), body: { code: 'G163AAAA', userId: V, ipAddress: '203.0.113.7', deviceId: 'dev-g163-1' } }]);
    out.push(['apply', 'USER X applies A\'s code for itself (control)', '/api/referrals/apply', { auth: bearer(principal(X, 'USER')), body: { code: 'G163AAAA', userId: X, ipAddress: '203.0.113.8', deviceId: 'dev-g163-2' } }]);
    return out;
  }
  for (const route of ['check', 'qualify']) {
    const path = route === 'check' ? `/api/milestones/check/${A}` : '/api/referrals/qualify';
    const body = route === 'qualify' ? { userId: Q } : undefined;
    out.push([route, 'no Authorization', path, { body }]);
    out.push([route, 'Bearer garbage', path, { auth: 'Bearer abc.def.ghi', body }]);
    out.push([route, 'SUPER_ADMIN signed by a foreign key', path, { auth: bearer(principal(X, 'SUPER_ADMIN'), { key: other }), body }]);
    out.push([route, 'SUPER_ADMIN HS256 keyed by the public PEM', path, { auth: bearer(principal(X, 'SUPER_ADMIN'), { alg: 'HS256' }), body }]);
    out.push([route, 'SUPER_ADMIN alg none', path, { auth: bearer(principal(X, 'SUPER_ADMIN'), { alg: 'none' }), body }]);
    for (const [label, uid, role] of roleCells) out.push([route, label, path, { auth: bearer(principal(uid, role)), body }]);
    out.push([route, 'forged x-user-* / x-gateway headers on a USER-other token', path, { auth: bearer(principal(X, 'USER')), body,
      headers: { 'x-user-id': route === 'check' ? A : Q, 'x-user-role': 'SYSTEM_ADMIN', 'x-gateway-vouch': 'forged', 'x-tenant-id': 't', 'x-forwarded-user': A } }]);
  }
  // /check owner classes
  out.push(['check', 'OWNER: USER, userId === path (control)', `/api/milestones/check/${A}`, { auth: bearer(principal(A, 'USER')) }]);
  out.push(['check', 'OWNER: ORG_ADMIN self', `/api/milestones/check/${A}`, { auth: bearer(principal(A, 'ORG_ADMIN')) }]);
  out.push(['check', 'OWNER via trailing slash path', `/api/milestones/check/${A}/`, { auth: bearer(principal(A, 'USER')) }]);
  out.push(['check', 'owner-id UPPERCASED in token', `/api/milestones/check/${A}`, { auth: bearer(principal(A.toUpperCase(), 'USER')) }]);
  out.push(['check', 'owner-id with trailing space in token', `/api/milestones/check/${A}`, { auth: bearer(principal(A + ' ', 'USER')) }]);
  out.push(['check', 'other user, path %-encoded target', `/api/milestones/check/${encodeURIComponent(A).replace(/a/g, '%61')}`, { auth: bearer(principal(X, 'USER')) }]);
  out.push(['check', 'token has sub=A but NO userId claim', `/api/milestones/check/${A}`, { auth: bearer({ sub: A, role: 'USER' }) }]);
  out.push(['check', 'token userId [A] (array)', `/api/milestones/check/${A}`, { auth: bearer(principal([A], 'USER')) }]);
  out.push(['check', 'NUMERIC userId 1957 vs path "1957"', `/api/milestones/check/${NUM}`, { auth: bearer(principal(1957, 'USER')) }]);
  out.push(['check', 'STRING userId "1957" vs path "1957" (owner control)', `/api/milestones/check/${NUM}`, { auth: bearer(principal('1957', 'USER')) }]);
  out.push(['check', 'empty userId "" vs path A', `/api/milestones/check/${A}`, { auth: bearer(principal('', 'USER')) }]);
  out.push(['check', 'empty userId "" vs EMPTY path /check/', `/api/milestones/check/`, { auth: bearer(principal('', 'USER')) }]);
  out.push(['check', 'missing userId (no claim) role USER', `/api/milestones/check/${A}`, { auth: bearer(principal(OMIT, 'USER')) }]);
  out.push(['check', 'SUPER_ADMIN, numeric path target 1957', `/api/milestones/check/${NUM}`, { auth: bearer(principal(X, 'SUPER_ADMIN')) }]);
  // /qualify extra classes
  out.push(['qualify', 'the referee themselves (USER, userId=Q)', '/api/referrals/qualify', { auth: bearer(principal(Q, 'USER')), body: { userId: Q } }]);
  out.push(['qualify', 'the referrer themselves (USER, userId=B)', '/api/referrals/qualify', { auth: bearer(principal(B, 'USER')), body: { userId: Q } }]);
  out.push(['qualify', 'referee, bad body {}', '/api/referrals/qualify', { auth: bearer(principal(Q, 'USER')), body: {} }]);
  out.push(['qualify', 'SYSTEM_ADMIN, bad body {} (KS-444 400)', '/api/referrals/qualify', { auth: bearer(principal(X, 'SYSTEM_ADMIN')), body: {} }]);
  out.push(['qualify', 'SYSTEM_ADMIN, userId as number', '/api/referrals/qualify', { auth: bearer(principal(X, 'SYSTEM_ADMIN')), body: { userId: 1957 } }]);
  out.push(['qualify', 'no principal, bad body {}', '/api/referrals/qualify', { body: {} }]);
  return out;
}

function pgLog() { return execFileSync('docker', ['logs', 'g163-pg'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 }) + ''; }
function pgLogBoth() {
  const r = require('child_process').spawnSync('docker', ['logs', 'g163-pg'], { encoding: 'utf8', maxBuffer: 1 << 28 });
  return (r.stdout || '') + (r.stderr || '');
}

(async () => {
  admin = new Client({ connectionString: ADMIN }); await admin.connect();
  await adm(`SET log_statement = 'all'`);
  const res = { ver, tree: T, at: new Date().toISOString(), rows: [] };
  let p;
  try {
    await resetSchema();
    p = await boot(APPURL);
    res.bootLine = (p.out.match(/Database initialization[^\n]*/) || [''])[0].slice(0, 160);
    res.exitedAtBoot = p.exited;
    const list = cells();
    for (let i = 0; i < list.length; i++) {
      const [route, label, path, req] = list[i];
      await seed();
      const mark = `G163MARK-${ver}-${i}`;
      await adm(`SELECT $1::text AS m`, [mark + '-start']);
      const r = await http(p, path, req);
      await sleep(250);
      await adm(`SELECT $1::text AS m`, [mark + '-end']);
      const m = await measure();
      res.rows.push({ i, route, label, path: path.replace(A, 'A').replace(Q, 'Q'), status: r.status, code: r.code, data: r.data, ...m });
    }
    await sleep(800);
    const log = pgLogBoth().split('\n');
    for (const row of res.rows) {
      const s = log.findIndex((l) => l.includes(`G163MARK-${ver}-${row.i}-start`)); const e = log.findIndex((l) => l.includes(`G163MARK-${ver}-${row.i}-end`));
      const seg = s >= 0 && e > s ? log.slice(s + 1, e) : null;
      row.appStatements = seg ? seg.filter((l) => / g163_app /.test(l) && /statement:|execute /.test(l)).length : 'MARKERS-NOT-FOUND';
    }
  } catch (e) { res.driverError = String(e && e.stack || e); }
  if (p) { p.child.kill('SIGTERM'); await sleep(600); if (p.exited === null) p.child.kill('SIGKILL'); }
  await admin.end();
  fs.writeFileSync(OUT, JSON.stringify(res, null, 1));
  console.log(JSON.stringify({ ver, rows: res.rows.length, err: res.driverError && res.driverError.slice(0, 300) }));
  process.exit(0);
})();
