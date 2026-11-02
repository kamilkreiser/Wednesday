// eslint with cwd = Blockchain/Dev (flat config base path), no shell cd. Planted control file moved to quarantine after.
const { spawnSync } = require('child_process'); const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952';
const D = G + '/repo/Blockchain/Dev', B = D + '/node_modules/.bin';
const run = (args, log) => { const r = spawnSync('nice', ['-n', '10', B + '/eslint', ...args], { cwd: D, encoding: 'utf8', maxBuffer: 1 << 26 }); fs.writeFileSync(G + '/logs/' + log, (r.stdout || '') + (r.stderr || '') + '\nrc=' + r.status + '\n'); console.log(log, 'rc', r.status, ((r.stdout || '').match(/✖.*problems?.*/) || ['no problems line'])[0]); };
const S = 'services/governance/src/';
const files = ['services/governanceService.ts', 'governance.openapi.ts', '__tests__/ks1950-an-admin-change-made-mid-request-is-not-reverted-by-a-stale-row-write.test.ts', '__tests__/ks1942-register-binds-the-linked-wallet-and-stake-is-admin-set.test.ts', '__tests__/ks1940-failed-participant-lookup-answers-503-and-writes-nothing.test.ts'].map((f) => S + f);
run(files, 'eslint_changed.log');
fs.writeFileSync(D + '/' + S + 'zz_gate134_planted.ts', 'export function f(): number { const unused = 1; debugger; return 2; }\n');
run([S + 'zz_gate134_planted.ts'], 'eslint_planted.log');
fs.mkdirSync(G + '/logs/_quarantine', { recursive: true });
fs.renameSync(D + '/' + S + 'zz_gate134_planted.ts', G + '/logs/_quarantine/zz_gate134_planted_eslint.ts');
