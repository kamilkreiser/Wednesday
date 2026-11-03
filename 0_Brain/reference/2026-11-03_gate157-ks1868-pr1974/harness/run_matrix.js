'use strict';
// Runs cell.js for every (site x kind x env x version) in its own process (6 at a time); writes logs/matrix.json + .tsv.
// Then judges mechanically: every head cell must equal the base ordinaryError cell of the same site+env on
// (exit, alive, flag, initDb outcome, startupCatch, logged levels+messages, logged error TYPE).
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const H = __dirname;
const W = path.resolve(H, '..');
const KINDS = ['ordinaryError', 'plainString', 'number42', 'emailMessage', 'null', 'undefined', 'revokedProxy', 'messageGetterThrows',
  'symbolMessage', 'objToStringThrows', 'messageToStringThrows', 'bigintMessage', 'messageToJSONThrows', 'messageIsRevokedProxy', 'toJSONThrowsError'];
const SITES = ['pool', 'hookBoot', 'hookRecovery', 'hookRealBoot', 'hookRealRecovery'];
const ENVS = ['test', 'production'];
const jobs = [];
for (const site of SITES) for (const kind of KINDS) for (const env of ENVS) for (const version of ['base', 'head']) jobs.push({ site, kind, env, version });
const out = [];
function runOne(j) {
  return new Promise((resolve) => {
    const p = spawn(process.execPath, [path.join(H, 'cell.js'), j.version, j.site, j.kind, j.env], { cwd: path.join(W, 'logs/cwd') });
    let so = '', se = '';
    p.stdout.on('data', (d) => { so += d; });
    p.stderr.on('data', (d) => { se += d; });
    const t = setTimeout(() => p.kill('SIGKILL'), 20000);
    p.on('close', (status) => {
      clearTimeout(t);
      const line = so.split('\n').find((l) => l.startsWith('G157REC '));
      const rec = line ? JSON.parse(line.slice(8)) : { ...j };
      rec.status = status;
      rec.stderrFirst = se.split('\n').filter(Boolean).filter((l) => /Error|at /.test(l)).slice(0, 2).join(' | ').slice(0, 240);
      out.push(rec);
      resolve();
    });
  });
}
(async () => {
  let i = 0;
  await Promise.all(Array.from({ length: 6 }, async () => { while (i < jobs.length) await runOne(jobs[i++]); }));
  const key = (r) => `${r.site}|${r.kind}|${r.nodeEnv || r.env}|${r.version}`;
  out.sort((a, b) => key(a).localeCompare(key(b)));
  fs.writeFileSync(path.join(W, 'logs/matrix.json'), JSON.stringify(out, null, 1));
  const sig = (r) => {
    const ev = r.events || [];
    const init = ev.find((e) => e && typeof e === 'object' && ('initDbResolved' in e || 'initDb' in e));
    return JSON.stringify({
      exit: r.status, alive: !!r.alive, flag: r.flagAfter, emitReturned: ev.includes('emit returned'),
      init: init ? (init.initDbResolved ?? init.initDb) : null, startupCatch: ev.some((e) => e && e.startupCatch),
      logs: (r.logs || []).map((l) => `${l.level}:${l.message}:${l.hasErrorKey ? l.errorType : 'nokey'}`.replace(/:nokey$|:string$/, ':string-or-absent')),
    });
  };
  const rows = []; const verdict = { hold: 0, differ: [], baseDead: {}, headDead: 0 };
  for (const r of out) {
    const env = r.nodeEnv || r.env;
    const ref = out.find((x) => x.site === r.site && x.kind === 'ordinaryError' && (x.nodeEnv || x.env) === env && x.version === 'base');
    const msg = r.site === 'pool' ? 'DB pool unexpected error' : null;
    const logs = (r.logs || []).filter((l) => l.level === 'error' || l.level === 'warn').filter((l) => !/unavailable|ECONN/.test(l.message))
      .map((l) => `${l.level}:${l.message.slice(0, 28)}=${l.errorType}:${String(l.error).slice(0, 40)}`).join(' ; ');
    const same = sig(r) === sig(ref);
    if (r.version === 'head') { if (same) verdict.hold++; else verdict.differ.push(key(r)); if (r.status !== 0) verdict.headDead++; }
    else if (r.status !== 0) { const k = `${r.site}|${env}`; (verdict.baseDead[k] = verdict.baseDead[k] || []).push(r.kind); }
    const ev = r.events || [];
    const init = ev.find((e) => e && typeof e === 'object' && ('initDbResolved' in e || 'initDb' in e));
    rows.push([r.site, env, r.kind, r.version, `exit=${r.status}`, r.alive ? 'alive' : 'DEAD', `flag=${r.flagAfter}`,
      `init=${init ? (init.initDbResolved ?? init.initDb) : (ev.some((e) => e && e.startupCatch) ? 'REJECTED' : '-')}`,
      `sameAsOrdinary=${same}`, `log=${logs || '-'}`, r.alive ? '' : `stderr=${r.stderrFirst}`].join('\t'));
  }
  fs.writeFileSync(path.join(W, 'logs/matrix.tsv'), rows.join('\n') + '\n');
  fs.writeFileSync(path.join(W, 'logs/matrix_verdict.json'), JSON.stringify(verdict, null, 1));
  console.log('cells', out.length, 'head hold', verdict.hold, '/', out.length / 2, 'head dead', verdict.headDead);
  console.log('head differ from base-ordinaryError:', JSON.stringify(verdict.differ));
  console.log('base dead:', JSON.stringify(verdict.baseDead, null, 1));
})();
