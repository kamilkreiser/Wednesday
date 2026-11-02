// Gate 146 driver: boots the REAL transfer service (node + tsx loader, real index.ts/db.ts/approvalWorkflowService)
// with only 'pg' replaced (scripts/pgstub.cjs), cwd anchored at <workdir>/logs/child_cwd. One process per cell.
// argv: <label> <scenario> <kind> [failAt]
const { spawn } = require('child_process');
const crypto = require('crypto'); const fs = require('fs'); const net = require('net');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962';
const D = W + '/repo/Blockchain/Dev', T = D + '/services/transfer';
const [label, scen, kind, failAt] = process.argv.slice(2);
const OUTDIR = W + '/logs/probe'; fs.mkdirSync(OUTDIR, { recursive: true });
const tag = `${label}__${scen}__${kind}`; const OUT = `${OUTDIR}/${tag}.events.jsonl`;
for (const f of [OUT, OUT + '.snap.json']) { try { fs.unlinkSync(f); } catch {} }
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const b64u = (b) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function token(role) {
  const h = b64u(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' }))); const now = Math.floor(Date.now() / 1000);
  const p = b64u(Buffer.from(JSON.stringify({ sub: 'g146', userId: 'g146-admin', role, iat: now, exp: now + 300 })));
  return `${h}.${p}.${b64u(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), privateKey))}`;
}
const freePort = () => new Promise((r) => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => r(p)); }); });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const port = await freePort();
  const env = { PATH: process.env.PATH, HOME: process.env.HOME, TMPDIR: process.env.TMPDIR, PORT: String(port),
    DATABASE_URL: 'postgres://g146:stub@127.0.0.1:1/g146', JWT_PUBLIC_KEY: Buffer.from(publicKey.export({ type: 'spki', format: 'pem' })).toString('base64'),
    G146_OUT: OUT, G146_SCEN: scen, G146_KIND: kind, G146_FAILAT: failAt || '3' };
  const child = spawn(process.execPath, ['--require', W + '/scripts/pgstub.cjs', '--import', 'file://' + D + '/node_modules/tsx/dist/loader.mjs', T + '/src/index.ts'],
    { cwd: W + '/logs/child_cwd', env, stdio: ['ignore', 'pipe', 'pipe'] });
  let stdout = '', stderr = ''; let exited = null;
  child.stdout.on('data', (d) => { stdout += d; }); child.stderr.on('data', (d) => { stderr += d; });
  child.on('exit', (code, sig) => { exited = { code, sig }; });
  const res = { tag, scen, kind };
  const t0 = Date.now();
  while (!/"message":"Database init"/.test(stdout) && exited === null && Date.now() - t0 < 30000) await sleep(100);
  await sleep(300);
  res.bootDone = /"message":"Database init"/.test(stdout); res.exitedAtBoot = exited;
  const m = stdout.match(/"message":"Database init","connected":(\w+)/); res.connected = m ? m[1] : null;
  const base = `http://127.0.0.1:${port}`;
  async function call(method, path) {
    try {
      const r = await fetch(base + path, { method, signal: AbortSignal.timeout(4000), headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token('SUPER_ADMIN')}` } });
      let body = await r.text(); try { body = JSON.parse(body); } catch {}
      return { status: r.status, body };
    } catch (e) { return { error: String(e && e.name) + ': ' + String(e && e.message).slice(0, 80) }; }
  }
  const snapNow = () => { try { return JSON.parse(fs.readFileSync(OUT + '.snap.json', 'utf8')); } catch { return null; } };
  res.health = await call('GET', '/health');
  const wl = await call('GET', '/api/workflows');
  res.workflowsServed = wl.body && wl.body.data ? (wl.body.data.workflows || wl.body.data).map?.((w) => w.id) : wl;
  res.storeAfterBoot = snapNow();
  if (scen.startsWith('sweep')) {
    res.post1 = await call('POST', '/api/workflows/escalate'); await sleep(500);
    res.exitedAfterPost1 = exited; res.storeAfterPost1 = snapNow();
    res.healthAfterPost1 = await call('GET', '/health');
    if (exited === null) { res.post2 = await call('POST', '/api/workflows/escalate'); await sleep(300); res.storeAfterPost2 = snapNow(); }
  }
  fs.writeFileSync(`${OUTDIR}/${tag}.stdout.log`, stdout); fs.writeFileSync(`${OUTDIR}/${tag}.stderr.log`, stderr);
  let evs = []; try { evs = fs.readFileSync(OUT, 'utf8').trim().split('\n').filter(Boolean).map((l) => JSON.parse(l)); } catch {}
  res.bootSql = evs.filter((e) => e.sql && e.sweepNo === 0).map((e) => e.sql.slice(0, 45));
  res.delegationProbeRan = evs.some((e) => e.sql && e.sql.startsWith('SELECT 1 FROM svc_transfer_delegations'));
  res.wfUpsertAttempts = evs.filter((e) => e.sql && e.sql.startsWith('INSERT INTO svc_approval_workflows')).length;
  res.lines = (stdout + '\n' + stderr).split('\n').filter((l) => /approvalWorkflowService|delegationService|boot work failed|Unhandled|unhandled|TypeError|Error:|revoked/.test(l)).map((l) => l.slice(0, 220)).slice(0, 12);
  if (exited === null) child.kill('SIGTERM');
  const t1 = Date.now(); while (exited === null && Date.now() - t1 < 5000) await sleep(50);
  if (exited === null) child.kill('SIGKILL');
  res.finalExit = exited;
  fs.writeFileSync(`${OUTDIR}/${tag}.result.json`, JSON.stringify(res, null, 1));
  fs.writeFileSync(`${OUTDIR}/${tag}.stdout.log`, stdout); fs.writeFileSync(`${OUTDIR}/${tag}.stderr.log`, stderr);
  console.log(JSON.stringify(res));
})();
