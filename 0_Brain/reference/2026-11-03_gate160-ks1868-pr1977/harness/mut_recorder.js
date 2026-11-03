// G160: recorder cells for one path against build_mut; compares end state to base+ordinaryError (matrix_all.json).
const { spawnSync } = require('child_process');
const path = require('path');
const W = path.resolve(__dirname, '..');
const p = process.argv[2];
const KINDS = ['ordinaryError', 'plainString', 'number42', 'null', 'undefined', 'revokedProxy', 'messageGetterThrows',
  'symbolMessage', 'bigintMessage', 'bigintValue', 'messageToJSONThrows', 'errToJSONThrows', 'objToStringThrows',
  'messageToStringThrows', 'messageIsRevokedProxy'];
const S = ['alive', 'initOutcome', 'emitReturned', 'flagAfter', 'initResult', 'ddlAttempts', 'getSession', 'createSession',
  'passwordChange', 'passwordReset', 'denylistRevokedJ1', 'denylistFreshJ2', 'lockoutLockedVictim', 'health', 'wouldExit1'];
const sig = (x) => S.map((k) => k + '=' + (x ? x[k] : (k === 'alive' ? 'DEAD' : '-'))).join(' ');
const all = require(path.join(W, 'logs', 'matrix_all.json'));
const diffs = []; let n = 0;
for (const env of ['development', 'production']) {
  const ref = all.find((r) => r.env === env && r.path === p && r.mode === 'default' && r.version === 'base' && r.kind === 'ordinaryError');
  for (const kind of KINDS) {
    const c = spawnSync(process.execPath, [path.join(__dirname, 'cell.js'), 'mut', p, kind, 'default'],
      { cwd: path.join(W, 'logs', 'cwd'), env: { ...process.env, NODE_ENV: env, LOG_LEVEL: '', G160_BUILD: process.argv[3] }, timeout: 60000 });
    const line = String(c.stdout).split('\n').find((l) => l.startsWith('G160RESULT '));
    const x = line ? JSON.parse(line.slice(11)) : null;
    n++;
    if (sig(x) !== sig(ref.result)) diffs.push(env.slice(0, 4) + ':' + kind + (x ? '' : '(DEAD)'));
    else if (x) { // also compare log TEXT with head for the same cell (detects text-only regressions)
      const h = all.find((r) => r.env === env && r.path === p && r.mode === 'default' && r.version === 'head' && r.kind === kind);
      const pick = (L) => (L || []).filter((l) => /Redis error|Redis unavailable|DB pool|Column migration/.test(l)).map((l) => l.replace(/"timestamp":"[^"]*"/, '').replace(/^\d{4}-\d\d-\d\d \S+ /, '')).join('\n');
      if (pick(x.logs) !== pick(h.result.logs)) diffs.push(env.slice(0, 4) + ':' + kind + '(logtext)');
    }
  }
}
console.log(`cells=${n} stateOrTextDiffs=${diffs.length} ${diffs.join(',')}`);
