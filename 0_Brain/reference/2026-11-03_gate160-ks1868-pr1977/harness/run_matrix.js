// G160 matrix runner: one child process per cell; records exit code, the G160RESULT line, stderr tail.
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const W = path.resolve(__dirname, '..');
const KINDS = ['ordinaryError', 'plainString', 'number42', 'null', 'undefined', 'revokedProxy', 'messageGetterThrows',
  'symbolMessage', 'bigintMessage', 'bigintValue', 'messageToJSONThrows', 'errToJSONThrows', 'objToStringThrows',
  'messageToStringThrows', 'messageIsRevokedProxy'];
const only = process.argv[2]; // optional filter "path"
const cells = [];
for (const env of ['development', 'production'])
  for (const version of ['base', 'head']) {
    cells.push({ version, path: 'up', kind: 'ordinaryError', mode: 'default', env });
    for (const p of ['listener', 'connect', 'pool', 'migrate'])
      for (const kind of KINDS) {
        cells.push({ version, path: p, kind, mode: 'default', env });
        if (p === 'listener') cells.push({ version, path: p, kind, mode: 'survive', env });
      }
  }
const todo = only ? cells.filter((c) => c.path === only) : cells;
const results = [];
function run(c) {
  return new Promise((resolve) => {
    const ch = spawn(process.execPath, [path.join(__dirname, 'cell.js'), c.version, c.path, c.kind, c.mode], {
      cwd: path.join(W, 'logs', 'cwd'), env: { ...process.env, NODE_ENV: c.env, LOG_LEVEL: '' },
    });
    let so = ''; let se = '';
    const t = setTimeout(() => ch.kill('SIGKILL'), 60000);
    ch.stdout.on('data', (d) => (so += d)); ch.stderr.on('data', (d) => (se += d));
    ch.on('close', (code, sig) => {
      clearTimeout(t);
      const line = so.split('\n').find((l) => l.startsWith('G160RESULT '));
      const r = line ? JSON.parse(line.slice(11)) : {};
      resolve({ ...c, exit: code, signal: sig, result: line ? r : null, stderrTail: se.slice(-600), stdoutTail: line ? '' : so.slice(-600) });
    });
  });
}
(async () => {
  fs.mkdirSync(path.join(W, 'logs', 'cwd'), { recursive: true });
  const N = 6; let i = 0;
  await Promise.all(Array.from({ length: N }, async () => { while (i < todo.length) { const c = todo[i++]; results.push(await run(c)); } }));
  results.sort((a, b) => JSON.stringify([a.env, a.path, a.mode, a.kind, a.version]).localeCompare(JSON.stringify([b.env, b.path, b.mode, b.kind, b.version])));
  const tag = only || 'all';
  fs.writeFileSync(path.join(W, 'logs', `matrix_${tag}.json`), JSON.stringify(results, null, 1));
  const cols = ['initOutcome', 'emitReturned', 'flagAfter', 'initResult', 'ddlAttempts', 'getSession', 'createSession', 'passwordChange', 'passwordReset', 'denylistRevokedJ1', 'denylistFreshJ2', 'lockoutLockedVictim', 'health', 'startCatchThrew'];
  const lines = ['env\tpath\tmode\tkind\tversion\texit\talive\t' + cols.join('\t') + '\tuncaught\tlastLog'];
  for (const r of results) {
    const x = r.result || {};
    const last = (x.logs || []).filter((l) => /Redis error|Redis unavailable|DB pool|Column migration|Failed to start/.test(l)).slice(-1)[0] || '';
    lines.push([r.env, r.path, r.mode, r.kind, r.version, r.exit, x.alive ? 'alive' : (r.result ? 'exited' : 'DEAD'),
      ...cols.map((k) => (x[k] === undefined ? '-' : String(x[k]))), (x.uncaught || []).join('|') || '-', last.slice(0, 160)].join('\t'));
  }
  fs.writeFileSync(path.join(W, 'logs', `matrix_${tag}.tsv`), lines.join('\n') + '\n');
  console.log('cells', results.length);
})();
