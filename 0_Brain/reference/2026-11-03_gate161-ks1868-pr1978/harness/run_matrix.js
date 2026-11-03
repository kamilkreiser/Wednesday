// G161 matrix runner: one child process per cell (concurrency 3, host load high).
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const W = path.resolve(__dirname, '..');
const KINDS = ['ordinaryError', 'plainString', 'number42', 'null', 'undefined', 'revokedProxy', 'messageGetterThrows',
  'symbolMessage', 'bigintMessage', 'bigintValue', 'messageToJSONThrows', 'errToJSONThrows', 'objToStringThrows',
  'messageToStringThrows', 'messageIsRevokedProxy', 'cyclicMessage', 'numberMessage', 'nullMessage', 'nullProtoMessage'];
const PATHS = ['verify', 'hibp', 'acsNoSmtp', 'acsSmtpOk', 'smtp', 'oauthGetdel', 'oauthMulti', 'sweepMark', 'sweepFind7', 'sweepPubExpired', 'sweepPubSoon'];
const UPS = ['verifyUp', 'hibpUp', 'emailUp', 'oauthUp', 'oauthMultiUp', 'sweepUp'];
const tag = process.argv[2] || 'all';
const build = process.env.G161_BUILD;
const cells = [];
for (const env of ['development', 'production'])
  for (const version of (process.env.G161_VERSIONS || 'base,head').split(',')) {
    for (const p of UPS) cells.push({ version, path: p, kind: 'ordinaryError', env });
    for (const p of PATHS) for (const kind of KINDS) cells.push({ version, path: p, kind, env });
  }
const only = process.env.G161_PATHS ? process.env.G161_PATHS.split(',') : null;
const todo = only ? cells.filter((c) => only.includes(c.path)) : cells;
const results = [];
function run(c) {
  return new Promise((resolve) => {
    const ch = spawn(process.execPath, [path.join(__dirname, 'cell.js'), c.version, c.path, c.kind], {
      cwd: path.join(W, 'logs', 'cwd'), env: { ...process.env, NODE_ENV: c.env, LOG_LEVEL: '' },
    });
    let so = ''; let se = '';
    const t = setTimeout(() => ch.kill('SIGKILL'), 60000);
    ch.stdout.on('data', (d) => (so += d)); ch.stderr.on('data', (d) => (se += d));
    ch.on('close', (code, sig) => {
      clearTimeout(t);
      const line = so.split('\n').find((l) => l.startsWith('G161RESULT '));
      resolve({ ...c, exit: code, signal: sig, result: line ? JSON.parse(line.slice(11)) : null, stderrTail: se.slice(-400) });
    });
  });
}
(async () => {
  const N = 3; let i = 0;
  await Promise.all(Array.from({ length: N }, async () => { while (i < todo.length) { const c = todo[i++]; results.push(await run(c)); } }));
  fs.writeFileSync(path.join(W, 'logs', `matrix_${tag}.json`), JSON.stringify(results, null, 1));
  console.log('cells', results.length, 'noResult', results.filter((r) => !r.result).length);
})();
