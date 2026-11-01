// run eslint with cwd = services/kyc (how `npm run lint` in a workspace resolves the flat config) without a shell cd
const { spawnSync } = require('child_process');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900';
const D = G + '/repo/Blockchain/Dev', A = D + '/services/kyc';
const fs = require('fs');
const news = fs.readdirSync(A + '/src/__tests__').filter((f) => f.startsWith('ks1868-kyc-')).map((f) => 'src/__tests__/' + f);
const run = (args, log) => { const r = spawnSync(D + '/node_modules/.bin/eslint', args, { cwd: A, encoding: 'utf8' }); fs.writeFileSync(G + '/logs/' + log, (r.stdout || '') + (r.stderr || '') + '\nrc=' + r.status + '\n'); console.log(log, 'rc', r.status); };
run(['src/index.ts', ...news], 'eslint_pr_files.log');
run(['src'], 'eslint_kyc_src.log');
