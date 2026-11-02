// eslint with cwd = Blockchain/Dev (flat config base path), no shell cd. Planted control file moved to quarantine after.
const { spawnSync } = require('child_process'); const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947';
const D = G + '/repo/Blockchain/Dev', B = D + '/node_modules/.bin';
const run = (args, log) => { const r = spawnSync('nice', ['-n', '10', B + '/eslint', ...args], { cwd: D, encoding: 'utf8', maxBuffer: 1 << 26 }); fs.writeFileSync(G + '/logs/' + log, (r.stdout || '') + (r.stderr || '') + '\nrc=' + r.status + '\n'); console.log(log, 'rc', r.status, ((r.stdout || '').match(/✖.*problems?.*/) || ['no problems line'])[0]); };
const S = 'services/governance/src/';
const files = ['db.ts', 'routes/governance.ts', 'services/governanceService.ts', '__tests__/ks1942-register-binds-the-linked-wallet-and-stake-is-admin-set.test.ts', '__tests__/ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts', '__tests__/governance.test.ts'].map((f) => S + f);
run(files, 'eslint_changed.log');
fs.writeFileSync(D + '/' + S + 'zz_gate129_planted.ts', 'export function f(): number { const unused = 1; debugger; return 2; }\n');
run([S + 'zz_gate129_planted.ts'], 'eslint_planted.log');
fs.mkdirSync(G + '/logs/_quarantine', { recursive: true });
fs.renameSync(D + '/' + S + 'zz_gate129_planted.ts', G + '/logs/_quarantine/zz_gate129_planted_eslint.ts');
