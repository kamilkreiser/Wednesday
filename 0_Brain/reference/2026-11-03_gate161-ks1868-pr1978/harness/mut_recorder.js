// G161: recorder cells for given paths against a mutated build; compares state AND site-log text with head unmutated.
const { spawnSync } = require('child_process');
const path = require('path');
const W = path.resolve(__dirname, '..');
const [paths, build] = process.argv.slice(2);
const KINDS = ['ordinaryError', 'plainString', 'number42', 'null', 'undefined', 'revokedProxy', 'messageGetterThrows',
  'symbolMessage', 'bigintMessage', 'bigintValue', 'messageToJSONThrows', 'errToJSONThrows', 'objToStringThrows',
  'messageToStringThrows', 'messageIsRevokedProxy', 'cyclicMessage', 'numberMessage', 'nullMessage', 'nullProtoMessage'];
const all = require(path.join(W, 'logs', 'matrix_all.json'));
const st = (x) => x ? JSON.stringify({ a: !!x.alive, d: !!x.died, o: x.outcome, c: x.calls, s: x.stateStillStored, r: x.replay }) : 'NORESULT';
const txt = (x) => ((x && x.logs) || []).filter((l) => /failed|threw|Failed to send|Send threw/i.test(l)).map((l) => l.replace(/"timestamp":"[^"]*"/, '').replace(/^\d{4}-\d\d-\d\d \S+ /, '')).join('\n');
const diffs = []; let n = 0;
for (const p of paths.split(',')) for (const env of ['development', 'production']) for (const kind of KINDS) {
  const c = spawnSync(process.execPath, [path.join(__dirname, 'cell.js'), 'mut', p, kind], { cwd: path.join(W, 'logs', 'cwd'), env: { ...process.env, NODE_ENV: env, LOG_LEVEL: '', G161_BUILD: build }, timeout: 60000 });
  const line = String(c.stdout).split('\n').find((l) => l.startsWith('G161RESULT '));
  const x = line ? JSON.parse(line.slice(11)) : null; n++;
  const h = all.find((r) => r.env === env && r.path === p && r.version === 'head' && r.kind === kind).result;
  if (st(x) !== st(h)) diffs.push(p + ':' + env.slice(0, 4) + ':' + kind + ':STATE');
  else if (txt(x) !== txt(h)) diffs.push(p + ':' + env.slice(0, 4) + ':' + kind + ':text');
}
const nState = diffs.filter((d) => d.endsWith('STATE')).length;
console.log(JSON.stringify({ cells: n, stateDiffs: nState, textDiffs: diffs.length - nState, sample: diffs.slice(0, 8) }));
