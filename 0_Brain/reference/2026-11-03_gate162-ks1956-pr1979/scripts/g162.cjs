// Gate 162 driver: boots the REAL referral service (node + tsx, real index.ts / db.ts / services / logger / shared
// authenticate(), real `pg`) against a REAL PostgreSQL 15 (container g162-pg). Faults are injected NATIVELY in the database
// (REVOKE, triggers that RAISE, NOLOGIN + terminate, LOCK TABLE) by an admin connection; nothing in the service is stubbed.
// argv: <ver base|head> <cell> <mr pk|nouniq|absent>   -> logs/probe/<ver>__<cell>__mr-<mr>.json
const { spawn } = require('child_process');
const crypto = require('crypto'); const fs = require('fs'); const net = require('net');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979';
const D = W + '/repo/Blockchain/Dev';
const { Client } = require(D + '/node_modules/pg');
const [ver, cell, mr] = process.argv.slice(2);
const T = `${W}/wt/${ver}/Blockchain/Dev/services/referral`;
const PGPORT = process.env.G162_PGPORT;
const ADMIN = `postgres://postgres@127.0.0.1:${PGPORT}/g162`;
const APPURL = `postgres://g162_app@127.0.0.1:${PGPORT}/g162`;
const OUT = `${W}/logs/probe/${ver}__${cell}__mr-${mr}.json`;
const DDL = fs.readFileSync(W + '/scripts/referral_ddl_from_repo.sql', 'utf8');
const MRCOLS = `user_id TEXT NOT NULL, type TEXT NOT NULL, amount BIGINT NOT NULL DEFAULT 0, status TEXT NOT NULL DEFAULT 'PENDING',
  source_id TEXT NOT NULL, source_type TEXT NOT NULL DEFAULT 'REFERRAL', transaction_hash TEXT, metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(), claimed_at TIMESTAMPTZ`;
// The repo has NO DDL for svc_referral_milestones_rewards (G153-F4). 'pk' mirrors svc_referral_rewards (id TEXT PRIMARY KEY);
// 'nouniq' is the same table with no unique index on id; 'absent' is the schema the repo DDL builds.
const MRDDL = { pk: `CREATE TABLE svc_referral_milestones_rewards (id TEXT PRIMARY KEY, ${MRCOLS});`,
  nouniq: `CREATE TABLE svc_referral_milestones_rewards (id TEXT, ${MRCOLS});`, absent: '' }[mr];

const U = { A: 'a1111111-1111-4111-8111-111111111111', B: 'b2222222-2222-4222-8222-222222222222', C: 'c3333333-3333-4333-8333-333333333333',
  Q1: 'd4444444-4444-4444-8444-444444444444', Q2: 'e5555555-5555-4555-8555-555555555555', Q3: 'f6666666-6666-4666-8666-666666666666' };
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const b64u = (b) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function token(userId) {
  const h = b64u(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' }))); const now = Math.floor(Date.now() / 1000);
  const p = b64u(Buffer.from(JSON.stringify({ sub: userId, userId, role: 'USER', iat: now, exp: now + 600 })));
  return `${h}.${p}.${b64u(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), privateKey))}`;
}
const freePort = () => new Promise((r) => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => r(p)); }); });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const strip = (s) => s.replace(/\x1b\[[0-9;]*m/g, '');

let admin;
async function adm(sql, params) { return admin.query(sql, params); }
async function resetSchema() {
  await adm(`SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'g162_app'`);
  await adm(`DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public; GRANT USAGE ON SCHEMA public TO g162_app;`);
  await adm(`ALTER ROLE g162_app LOGIN`);
  await adm(DDL);
  if (MRDDL) await adm(MRDDL);
  await adm(`CREATE TABLE g162_ctl (k TEXT PRIMARY KEY)`);
  await adm(`CREATE FUNCTION g162_fail() RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER AS $$
    BEGIN IF EXISTS (SELECT 1 FROM g162_ctl WHERE k = TG_ARGV[0]) THEN RAISE EXCEPTION 'g162 injected % failure', TG_ARGV[0]; END IF;
    RETURN NEW; END $$`);
  await adm(`CREATE TRIGGER g162_progress_save BEFORE INSERT OR UPDATE ON svc_referral_milestones FOR EACH ROW EXECUTE FUNCTION g162_fail('progressSave')`);
  if (MRDDL) await adm(`CREATE TRIGGER g162_reward_save BEFORE INSERT ON svc_referral_milestones_rewards FOR EACH ROW EXECUTE FUNCTION g162_fail('rewardSave')`);
  await adm(`GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO g162_app; REVOKE ALL ON g162_ctl FROM g162_app;`);
}
const fault = { on: (k) => adm(`INSERT INTO g162_ctl VALUES ($1) ON CONFLICT DO NOTHING`, [k]), off: (k) => adm(`DELETE FROM g162_ctl WHERE k = $1`, [k]) };
async function seedReferrals(referrer, nQualified, pendingFor = []) {
  const codeId = 'code-' + referrer.slice(0, 8);
  await adm(`INSERT INTO svc_referral_codes (id, code, owner_id) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING`, [codeId, ('G' + referrer.slice(0, 7)).toUpperCase(), referrer]);
  if (nQualified > 0) await adm(`INSERT INTO svc_referrals (id, referral_code_id, referrer_id, referred_user_id, status, referrer_reward, referred_reward, fraud_check_passed, qualified_at)
    SELECT 'ref-' || $1 || '-' || g, $2, $1, 'u-' || $1 || '-' || g, 'QUALIFIED', 50000000, 25000000, true, NOW() FROM generate_series(1, $3) g`, [referrer, codeId, nQualified]);
  for (const q of pendingFor) await adm(`INSERT INTO svc_referrals (id, referral_code_id, referrer_id, referred_user_id, status, referrer_reward, referred_reward, fraud_check_passed)
    VALUES ($1, $2, $3, $4, 'PENDING', 50000000, 25000000, true)`, ['pend-' + q, codeId, referrer, q]);
}
async function legacyReward(user, sourceId, status, amount) {
  await adm(`INSERT INTO svc_referral_milestones_rewards (id, user_id, type, amount, status, source_id, source_type, created_at, metadata)
    VALUES ($1, $2, 'MILESTONE_REWARD', $3, $4, $5, 'MILESTONE', '2026-10-01T00:00:00Z', '{}')`, [crypto.randomUUID(), user, amount, status, sourceId]);
}
async function snap() {
  const s = {};
  if (MRDDL) s.mr = (await adm(`SELECT user_id, source_id, status, amount::text, count(*) OVER (PARTITION BY user_id, source_id) AS n, id FROM svc_referral_milestones_rewards ORDER BY user_id, created_at, source_id`)).rows
    .map((r) => `${r.user_id.slice(0, 2)}:${r.source_id}:${r.status}:${r.amount}:n${r.n}:${r.id.slice(0, 8)}`);
  s.progress = (await adm(`SELECT user_id, current_tier, total_rewards_earned::text AS tot, milestones_completed FROM svc_referral_milestones ORDER BY user_id`)).rows
    .map((r) => `${r.user_id.slice(0, 2)}:${r.current_tier}:${r.tot}:[${(r.milestones_completed || []).map((m) => m.milestoneId + '/' + m.rewardAmount).join(',')}]`);
  s.rewards = (await adm(`SELECT user_id, type, amount::text, source_id, metadata FROM svc_referral_rewards ORDER BY created_at`)).rows
    .map((r) => `${r.user_id.slice(0, 2)}:${r.type}:${r.amount}:${JSON.stringify(r.metadata)}`);
  s.referralStatus = (await adm(`SELECT referred_user_id, status FROM svc_referrals WHERE id LIKE 'pend-%' ORDER BY id`)).rows.map((r) => `${r.referred_user_id.slice(0, 2)}:${r.status}`);
  return s;
}
async function awardCounts() {
  if (!MRDDL) return { rows: 0, maxPerUserMilestone: 0, sum: '0' };
  const r = (await adm(`SELECT count(*)::int AS rows, COALESCE(max(n),0)::int AS max, COALESCE(sum(amount),0)::text AS sum FROM
    (SELECT user_id, source_id, amount, count(*) OVER (PARTITION BY user_id, source_id) AS n FROM svc_referral_milestones_rewards) x`)).rows[0];
  return { rows: r.rows, maxPerUserMilestone: r.max, sum: r.sum };
}

async function boot(dbUrl, name) {
  const port = await freePort();
  const env = { PATH: process.env.PATH, HOME: process.env.HOME, TMPDIR: process.env.TMPDIR, PORT: String(port), DATABASE_URL: dbUrl,
    JWT_PUBLIC_KEY: Buffer.from(publicKey.export({ type: 'spki', format: 'pem' })).toString('base64') };
  const child = spawn(process.execPath, ['--import', 'file://' + D + '/node_modules/tsx/dist/loader.mjs', T + '/src/index.ts'],
    { cwd: W + '/logs/child_cwd', env, stdio: ['ignore', 'pipe', 'pipe'] });
  const p = { name, port, child, out: '', exited: null };
  child.stdout.on('data', (d) => { p.out += strip(String(d)); }); child.stderr.on('data', (d) => { p.out += strip(String(d)); });
  child.on('exit', (code, sig) => { p.exited = { code, sig }; });
  const t0 = Date.now();
  while (!(/Database initialization/.test(p.out) && /Referral Service running/.test(p.out)) && p.exited === null && Date.now() - t0 < 60000) await sleep(100);
  await sleep(200);
  p.dbAvailableAtBoot = (p.out.match(/Database initialization[^\n]*/) || [''])[0].slice(0, 160);
  return p;
}
async function call(p, method, path, user, body) {
  try {
    const r = await fetch(`http://127.0.0.1:${p.port}${path}`, { method, signal: AbortSignal.timeout(20000),
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token(user)}` }, body: body ? JSON.stringify(body) : undefined });
    let b = await r.text(); try { b = JSON.parse(b); } catch {}
    return { status: r.status, body: b };
  } catch (e) { return { error: String(e && e.name) + ': ' + String(e && e.message).slice(0, 80) }; }
}
const chk = async (p, user) => { const r = await call(p, 'POST', `/api/milestones/check/${user}`, user);
  return r.body && r.body.data ? { status: r.status, new: (r.body.data.newMilestones || []).map((m) => m.tier), msg: r.body.data.message } : r; };
const qualify = async (p, user) => { const r = await call(p, 'POST', '/api/referrals/qualify', user, { userId: user });
  return r.body && r.body.data ? { status: r.status, qualified: r.body.data.qualified } : r; };
const progress = async (p, user) => { const r = await call(p, 'GET', `/api/milestones/user/${user}`, user);
  return r.body && r.body.data ? { status: r.status, tier: r.body.data.currentTier, total: r.body.data.totalMilestoneRewards, achieved: r.body.data.achieved.map((a) => `${a.tier}:${a.reward}`), next: r.body.data.progressToNext.nextMilestone && r.body.data.progressToNext.nextMilestone.tier, ambassadorBonus: r.body.data.ambassadorBonus } : r; };
const rewardsGet = async (p, user) => { const r = await call(p, 'GET', `/api/rewards/user/${user}`, user);
  return r.body && r.body.data ? { status: r.status, keys: Object.keys(r.body.data), summary: r.body.data.summary || r.body.data.totals || null, pendingN: (r.body.data.pending || []).length } : r; };
const stats = async (p, user) => { const r = await call(p, 'GET', `/api/referrals/user/${user}`, user);
  return r.body && r.body.data ? { status: r.status, tier: r.body.data.milestoneProgress && r.body.data.milestoneProgress.currentTier, achievedN: r.body.data.milestoneProgress && (r.body.data.milestoneProgress.milestonesAchieved || []).length, pendingN: (r.body.data.pendingRewards || []).length } : r; };

async function waitBlocked(n, re, ms = 15000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    const r = await adm(`SELECT count(*)::int AS n FROM pg_stat_activity WHERE usename = 'g162_app' AND wait_event_type = 'Lock' AND query ~ $1`, [re]);
    if (r.rows[0].n >= n) return r.rows[0].n;
    await sleep(50);
  }
  return (await adm(`SELECT count(*)::int AS n FROM pg_stat_activity WHERE usename = 'g162_app' AND wait_event_type = 'Lock' AND query ~ $1`, [re])).rows[0].n;
}

const CELLS = {
  // C0/R3: healthy DB, fresh user with 1 qualified referral, three consecutive checks.
  async consecutive(res, p) { await seedReferrals(U.A, 1); res.c1 = await chk(p, U.A); res.c2 = await chk(p, U.A); res.c3 = await chk(p, U.A); res.progress = await progress(p, U.A); },
  // R4: two CONCURRENT checks, forced to race: an admin txn holds EXCLUSIVE on the rewards table (SELECTs pass, INSERTs wait),
  // both checks read "nothing awarded" and block on the INSERT; then the lock is released. two processes = two pools.
  async concurrent2proc(res, p, p2) { await seedReferrals(U.A, 1); await raced(res, [() => chk(p, U.A), () => chk(p2, U.A)]); res.progress = await progress(p, U.A); res.c3 = await chk(p, U.A); },
  async concurrent1proc(res, p) { await seedReferrals(U.A, 1); await raced(res, [() => chk(p, U.A), () => chk(p, U.A)]); res.c3 = await chk(p, U.A); },
  // R4 natural: 20 users, two processes, both checks fired at once, no lock.
  async concurrentNatural(res, p, p2) {
    const users = Array.from({ length: 20 }, (_, i) => crypto.randomUUID());
    for (const u of users) await seedReferrals(u, 5);
    const out = await Promise.all(users.flatMap((u) => [chk(p, u), chk(p2, u)]));
    res.answeredNew = out.reduce((s, r) => s + ((r.new || []).length), 0); res.statuses = [...new Set(out.map((r) => r.status))];
  },
  // R5: rows stored before the fix under OLD random ids (FIRST CLAIMED, BRONZE CLAIMABLE), no progress row (F1), 5 referrals.
  async legacy(res, p) { await seedReferrals(U.A, 5); await legacyReward(U.A, 'milestone-first', 'CLAIMED', '100000000'); await legacyReward(U.A, 'milestone-bronze', 'CLAIMABLE', '500000000');
    res.c1 = await chk(p, U.A); res.c2 = await chk(p, U.A); res.progress = await progress(p, U.A); },
  // R6: progress read fails (REVOKE SELECT on svc_referral_milestones) for a user already awarded FIRST (+CLAIMED row) with 5 referrals.
  async progressReadFails(res, p) { await seedReferrals(U.A, 5); await legacyReward(U.A, 'milestone-first', 'CLAIMED', '100000000');
    await adm(`REVOKE SELECT ON svc_referral_milestones FROM g162_app`);
    res.c1 = await chk(p, U.A); res.c2 = await chk(p, U.A); res.progressGET = await progress(p, U.A); res.statsGET = await stats(p, U.A); res.rewardsGET = await rewardsGet(p, U.A); },
  // R7: the any-status awarded read fails (REVOKE SELECT on the rewards table; INSERT still granted), fresh user 1 referral.
  async awardedReadFails(res, p) { await seedReferrals(U.A, 1); await adm(`REVOKE SELECT ON svc_referral_milestones_rewards FROM g162_app`);
    res.c1 = await chk(p, U.A); res.c2 = await chk(p, U.A); },
  // R8: the database refuses connections mid-life (NOLOGIN + terminate): reads fail at the socket, isDbAvailable() stays true.
  async connectionsRefused(res, p) { await seedReferrals(U.A, 1); res.c1 = await chk(p, U.A);
    await adm(`ALTER ROLE g162_app NOLOGIN`); await adm(`SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'g162_app'`); await sleep(300);
    res.c2 = await chk(p, U.A); res.c3 = await chk(p, U.A); res.snapDown = await snap();
    await adm(`ALTER ROLE g162_app LOGIN`); await sleep(300); res.c4 = await chk(p, U.A); },
  // R9: a read failing BETWEEN checks: check1 healthy (FIRST at 1 referral) -> 4 more referrals -> read fails -> restore -> check3.
  async readFailsBetween(res, p) { await seedReferrals(U.A, 1); res.c1 = await chk(p, U.A);
    await adm(`INSERT INTO svc_referrals (id, referral_code_id, referrer_id, referred_user_id, status, referrer_reward, referred_reward, fraud_check_passed)
      SELECT 'more-' || g, 'code-' || left($1, 8), $1, 'more-u-' || g, 'QUALIFIED', 50000000, 25000000, true FROM generate_series(1, 4) g`, [U.A]);
    await adm(`REVOKE SELECT ON svc_referral_milestones FROM g162_app`); res.c2 = await chk(p, U.A);
    await adm(`GRANT SELECT ON svc_referral_milestones TO g162_app`); res.c3 = await chk(p, U.A); res.c4 = await chk(p, U.A); },
  // R10: the progress save fails (trigger RAISE) AFTER the reward row is written; then healthy checks.
  async progressSaveFails(res, p) { await seedReferrals(U.A, 1); await fault.on('progressSave'); res.c1 = await chk(p, U.A); res.c2 = await chk(p, U.A);
    res.snapMid = await snap(); await fault.off('progressSave'); res.c3 = await chk(p, U.A); res.c4 = await chk(p, U.A); },
  // R11: the reward save fails (trigger RAISE), then healthy checks.
  async rewardSaveFails(res, p) { await seedReferrals(U.A, 1); await fault.on('rewardSave'); res.c1 = await chk(p, U.A); res.snapMid = await snap();
    await fault.off('rewardSave'); res.c2 = await chk(p, U.A); res.c3 = await chk(p, U.A); },
  // /qualify: healthy then with the progress read failing; referrer A has 0 qualified + 3 pending referrals.
  async qualifyPath(res, p) { await seedReferrals(U.A, 0, [U.Q1, U.Q2, U.Q3]);
    res.q1 = await qualify(p, U.Q1); res.snap1 = await snap();
    await adm(`REVOKE SELECT ON svc_referral_milestones FROM g162_app`); res.q2 = await qualify(p, U.Q2); res.snap2 = await snap();
    await adm(`GRANT SELECT ON svc_referral_milestones TO g162_app`); res.q3 = await qualify(p, U.Q3); },
  // Money: AMBASSADOR. 1000 qualified + 1 pending. check, then qualify the pending one: what does the REFERRER_REWARD pay?
  async ambassador(res, p) { await seedReferrals(U.A, 1000, [U.Q1]); res.c1 = await chk(p, U.A); res.progress = await progress(p, U.A);
    res.q1 = await qualify(p, U.Q1); res.c2 = await chk(p, U.A); },
  // Fresh healthy award of all 5 below AMBASSADOR (999 referrals): amounts per milestone.
  async amounts(res, p) { await seedReferrals(U.A, 999); res.c1 = await chk(p, U.A); res.c2 = await chk(p, U.A); },
};
async function raced(res, fns) {
  const lk = new Client({ connectionString: ADMIN }); await lk.connect();
  await lk.query('BEGIN'); await lk.query('LOCK TABLE svc_referral_milestones_rewards IN EXCLUSIVE MODE');
  const pr = Promise.all(fns.map((f) => f()));
  res.blockedOnInsert = await waitBlocked(fns.length, 'INSERT INTO svc_referral_milestones_rewards');
  await lk.query('COMMIT'); await lk.end();
  res.raced = await pr;
}

(async () => {
  admin = new Client({ connectionString: ADMIN }); await admin.connect();
  const res = { ver, cell, mr, tree: T, at: new Date().toISOString() };
  const procs = [];
  try {
    await resetSchema();
    procs.push(await boot(APPURL, 'p1'));
    if (/2proc|Natural/.test(cell)) procs.push(await boot(APPURL, 'p2'));
    res.boot = procs.map((x) => x.dbAvailableAtBoot);
    await CELLS[cell](res, ...procs);
    res.final = await snap(); res.counts = await awardCounts();
    res.logLines = procs.map((x) => x.out.split('\n').filter((l) => /Milestone|milestone|reward|BigInt|progress/i.test(l)).map((l) => l.slice(0, 220)).slice(0, 40));
  } catch (e) { res.driverError = String(e && e.stack || e); }
  for (const x of procs) { x.child.kill('SIGTERM'); }
  await sleep(500);
  for (const x of procs) { if (x.exited === null) x.child.kill('SIGKILL'); }
  await admin.end();
  fs.writeFileSync(OUT, JSON.stringify(res, null, 1));
  console.log(JSON.stringify({ ver, cell, mr, counts: res.counts, err: res.driverError && res.driverError.slice(0, 200) }));
  process.exit(0);
})();
