// tsc (plain + tests via tsconfig.test.json + the repo's own leg-16 checker) and eslint, cwd = the right dirs without a shell cd
const { spawnSync } = require('child_process'); const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908';
const D = G + '/repo/Blockchain/Dev', A = D + '/services/security', B = D + '/node_modules/.bin';
const run = (cmd, args, cwd, log) => { const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', maxBuffer: 1 << 26 }); fs.writeFileSync(G + '/logs/' + log, (r.stdout || '') + (r.stderr || '') + '\nrc=' + r.status + '\n'); console.log(log, 'rc', r.status); };
run(B + '/tsc', ['-p', 'tsconfig.json', '--noEmit'], A, 'tsc_plain_head.log');
run(B + '/tsc', ['-p', 'tsconfig.test.json'], A, 'tsc_tests_head.log');
run('node', ['scripts/typecheck-tests/check.cjs', 'services/security'], D, 'leg16_security.log');
const news = fs.readdirSync(A + '/src/__tests__').filter((f) => f.startsWith('ks1868-security-')).map((f) => 'src/__tests__/' + f);
run(B + '/eslint', ['src/index.ts', ...news], A, 'eslint_pr_files.log');
fs.writeFileSync(A + '/src/zz_gate90_planted.ts', 'export function f(): number { const unused = 1; debugger; return 2; }\n');
run(B + '/eslint', ['src/zz_gate90_planted.ts'], A, 'eslint_planted.log');
fs.renameSync(A + '/src/zz_gate90_planted.ts', G + '/logs/_quarantine/zz_gate90_planted.ts');
// planted unused local in a NEW test file for tsc tests positive control
const t = A + '/src/__tests__/' + news[0].split('/').pop(); const orig = fs.readFileSync(t, 'utf8');
fs.writeFileSync(t, orig + '\nconst GATE90_UNUSED = 1;\n');
run(B + '/tsc', ['-p', 'tsconfig.test.json'], A, 'tsc_tests_planted.log');
fs.writeFileSync(t, orig); console.log('restored test file', fs.readFileSync(t, 'utf8') === orig);
