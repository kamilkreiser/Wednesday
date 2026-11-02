const { spawnSync } = require('child_process');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate154-ks1868-pr1971';
const D = W + '/repo/Blockchain/Dev'; const S = D + '/services/m365-integration';
const r = spawnSync(D + '/node_modules/.bin/eslint', process.argv.slice(2), { cwd: S, encoding: 'utf8' });
console.log(r.stdout + r.stderr + 'rc=' + r.status);
