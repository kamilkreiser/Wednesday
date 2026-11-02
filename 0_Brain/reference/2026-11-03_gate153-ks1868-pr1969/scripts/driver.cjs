// Gate 153 driver: boots the REAL referral service (node + tsx loader, real index.ts/db.ts/services, real winston logger)
// with only 'pg' replaced (scripts/pgstub.cjs), cwd anchored at <workdir>/logs/child_cwd. One process per cell.
// argv: <label> <treeDir> <scenario> <kind> [mr]
const { spawn } = require('child_process');
const crypto = require('crypto'); const fs = require('fs'); const net = require('net');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate153-ks1868-pr1969';
const [label, tree, scen, kind, mrArg] = process.argv.slice(2); const mr = mrArg || 'present';
const D = W + '/repo/Blockchain/Dev', T = tree + '/Blockchain/Dev/services/referral';
const OUTDIR = W + '/logs/probe'; fs.mkdirSync(OUTDIR, { recursive: true });
const tag = `${label}__${scen}__${kind}__mr-${mr}`; const OUT = `${OUTDIR}/${tag}.events.jsonl`;
for (const f of [OUT, OUT + '.snap.json']) { try { fs.unlinkSync(f); } catch {} }
const REF = '11111111-1111-4111-8111-111111111111', BAD = '22222222-2222-4222-8222-222222222222', NEWU = '33333333-3333-4333-8333-333333333333';
const REF2 = '44444444-4444-4444-8444-444444444444', GEN = '55555555-5555-4555-8555-555555555555';
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const b64u = (b) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function token(userId) {
  const h = b64u(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' }))); const now = Math.floor(Date.now() / 1000);
  const p = b64u(Buffer.from(JSON.stringify({ sub: userId, userId, role: 'USER', iat: now, exp: now + 300 })));
  return `${h}.${p}.${b64u(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), privateKey))}`;
}
const freePort = () => new Promise((r) => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => r(p)); }); });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const strip = (s) => s.replace(/\x1b\[[0-9;]*m/g, '');
(async () => {
  const port = await freePort();
  const env = { PATH: process.env.PATH, HOME: process.env.HOME, TMPDIR: process.env.TMPDIR, PORT: String(port),
    DATABASE_URL: 'postgres://g153:stub@127.0.0.1:1/g153', JWT_PUBLIC_KEY: Buffer.from(publicKey.export({ type: 'spki', format: 'pem' })).toString('base64'),
    G153_OUT: OUT, G153_SCEN: scen, G153_KIND: kind, G153_MR: mr };
  const child = spawn(process.execPath, ['--require', W + '/scripts/pgstub.cjs', '--import', 'file://' + D + '/node_modules/tsx/dist/loader.mjs', T + '/src/index.ts'],
    { cwd: W + '/logs/child_cwd', env, stdio: ['ignore', 'pipe', 'pipe'] });
  let stdout = '', stderr = ''; let exited = null;
  child.stdout.on('data', (d) => { stdout += strip(String(d)); }); child.stderr.on('data', (d) => { stderr += strip(String(d)); });
  child.on('exit', (code, sig) => { exited = { code, sig }; });
  const res = { tag, scen, kind, mr };
  const t0 = Date.now();
  while (!/Database initialization/.test(stdout) && exited === null && Date.now() - t0 < 40000) await sleep(100);
  while (!/Referral Service running/.test(stdout) && exited === null && Date.now() - t0 < 40000) await sleep(100);
  await sleep(200);
  res.bootDone = /Database initialization/.test(stdout); res.exitedAtBoot = exited;
  const base = `http://127.0.0.1:${port}`;
  async function call(method, path, user, body) {
    try {
      const r = await fetch(base + path, { method, signal: AbortSignal.timeout(8000), headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token(user)}` }, body: body ? JSON.stringify(body) : undefined });
      let b = await r.text(); try { b = JSON.parse(b); } catch {}
      return { status: r.status, body: b };
    } catch (e) { return { error: String(e && e.name) + ': ' + String(e && e.message).slice(0, 80) }; }
  }
  const snapNow = () => { try { return JSON.parse(fs.readFileSync(OUT + '.snap.json', 'utf8')); } catch { return null; } };
  res.health = (await call('GET', '/health', NEWU)).status;
  res.storeAfterBoot = snapNow();
  const short = (r) => r && r.body && r.body.data ? { status: r.status, ...(r.body.data.newMilestones ? { newMilestones: r.body.data.newMilestones.map((m) => m.tier || m.id) } : {}), ...(r.body.data.totalReward ? { totalReward: r.body.data.totalReward } : {}) } : r;
  if (scen.startsWith('boot_') || scen === 'apply') {
    const a = await call('POST', '/api/referrals/apply', NEWU, { code: 'GATE1530', userId: BAD, ipAddress: '10.9.9.9', deviceId: 'dev-x' });
    res.apply = a.body && a.body.data ? { status: a.status, refStatus: a.body.data.status, fraudCheckPassed: a.body.data.fraudCheckPassed, signupBonus: a.body.data.signupBonus } : a;
    await sleep(150); res.storeAfterApply = snapNow();
  }
  if (scen.startsWith('award')) {
    const who = scen === 'award_fresh' ? REF2 : REF;
    const c1 = await call('POST', `/api/milestones/check/${who}`, who); res.check1 = c1.body && c1.body.data ? { status: c1.status, newMilestones: (c1.body.data.newMilestones || []).map((m) => m.tier), raw: Object.keys(c1.body.data) } : c1;
    await sleep(150); res.storeAfterCheck1 = snapNow();
    const c2 = await call('POST', `/api/milestones/check/${who}`, who); res.check2 = c2.body && c2.body.data ? { status: c2.status, newMilestones: (c2.body.data.newMilestones || []).map((m) => m.tier) } : c2;
    await sleep(150); res.storeAfterCheck2 = snapNow();
    const rw = await call('GET', `/api/rewards/user/${who}`, who); res.rewardsView = rw.body && rw.body.data ? rw.body.data.summary : rw;
    if (scen === 'award_read' || scen === 'award_read_wfail') {
      // a second user (not REF) triggers REF's check: is the route owner-bound?
      const c3 = await call('POST', `/api/milestones/check/${REF}`, NEWU); res.checkByOtherUser = c3.body && c3.body.data ? { status: c3.status, newMilestones: (c3.body.data.newMilestones || []).map((m) => m.tier) } : c3;
    }
  }
  if (scen.startsWith('gen_')) {
    const g1 = await call('POST', '/api/referrals/generate', GEN, {}); res.gen = { status: g1.status, ok: g1.body && g1.body.success, err: g1.body && g1.body.error && g1.body.error.message };
    const g2 = await call('POST', '/api/referrals/generate', GEN, { customCode: process.env.G153_CUSTOM || 'GATEXYZ1' }); res.genCustom = { status: g2.status, ok: g2.body && g2.body.success, err: g2.body && g2.body.error && g2.body.error.message };
    await sleep(150); res.storeAfterGen = { codesByGEN: snapNow().codesByGEN };
  }
  if (scen === 'rewards_read') { const rw = await call('GET', `/api/rewards/user/${REF}`, REF); res.rewardsView = rw.body && rw.body.data ? rw.body.data.summary : rw; }
  res.healthEnd = (await call('GET', '/health', NEWU)).status; res.exitedBeforeKill = exited;
  let evs = []; try { evs = fs.readFileSync(OUT, 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l)); } catch {}
  res.bootSql = evs.filter((e) => e.sql).slice(0, 6).map((e) => e.sql.slice(0, 50));
  res.fraudLoadRan = evs.some((e) => e.sql && e.sql.startsWith('SELECT ip_address'));
  res.injected = evs.filter((e) => e.injected).length;
  res.unmodelled = [...new Set(evs.filter((e) => e.unmodelled).map((e) => e.unmodelled))];
  res.lines = (stdout + '\n' + stderr).split('\n').filter((l) => /failed|Failed|Loaded fraud|verified|Milestone achieved|unreadable|Unhandled|TypeError|revoked|getter boom|db down|plain boom|boot work|does not exist|serialize/.test(l)).map((l) => l.replace(/^\S+ \S+ /, '').slice(0, 230));
  res.milestoneAchievedLines = (stdout.match(/Milestone achieved/g) || []).length;
  if (exited === null) child.kill('SIGTERM');
  const t1 = Date.now(); while (exited === null && Date.now() - t1 < 5000) await sleep(50);
  if (exited === null) child.kill('SIGKILL');
  res.finalExit = exited;
  fs.writeFileSync(`${OUTDIR}/${tag}.result.json`, JSON.stringify(res, null, 1));
  fs.writeFileSync(`${OUTDIR}/${tag}.stdout.log`, stdout); fs.writeFileSync(`${OUTDIR}/${tag}.stderr.log`, stderr);
  console.log(JSON.stringify(res).slice(0, 3000));
})();
