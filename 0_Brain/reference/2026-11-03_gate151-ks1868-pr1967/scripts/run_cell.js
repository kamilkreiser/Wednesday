const { spawnSync } = require('child_process');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate151-ks1868-pr1967';
const D = W + '/repo/Blockchain/Dev';
const [which, kind, n, mode] = process.argv.slice(2);
const r = spawnSync(D + '/node_modules/.bin/tsx', ['-r', W + '/scripts/stub_ioredis.js', W + '/scripts/probe_child.ts', which, kind, n, mode],
  { cwd: W + '/logs/cwd', env: { ...process.env, NODE_ENV: 'production', NODE_PATH: D + '/node_modules:' + D + '/services/demo-service/node_modules' }, encoding: 'utf8', timeout: 60000 });
const line = (r.stderr.split('\n').find((l) => l.startsWith('RESULT ')) || 'RESULT {"error":"no result"}').slice(7);
const warns = (r.stdout.match(/Redis unavailable/g) || []).length;
const errs = (r.stdout.match(/Failed to toggle presenter mode/g) || []).length;
const obj = JSON.parse(line); obj.rc = r.status; obj.warnLines = warns; obj.errLines = errs;
obj.errField = (r.stdout.match(/"error":"[^"]*"/g) || []).filter((x, i, a) => a.indexOf(x) === i);
if (obj.error) obj.stderrTail = r.stderr.slice(-400);
console.log(JSON.stringify(obj));
