const { spawnSync } = require('child_process'); const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate118-ks1868-pr1936';
const D = G + '/repo/Blockchain/Dev', B = D + '/node_modules/.bin', A = D + '/services/originate'; const tag = process.argv[2] || 'head';
fs.mkdirSync(G + '/logs/_quarantine', { recursive: true });
const run = (cmd, args, cwd, log) => { const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', maxBuffer: 1 << 26 }); const out = (r.stdout || '') + (r.stderr || ''); fs.writeFileSync(G + '/logs/' + log, out + '\nrc=' + r.status + '\n'); const n = (out.match(/error TS\d+/g) || []).length; console.log(log, 'rc', r.status, 'TS errors', n); return out; };
run(B + '/tsc', ['-p', 'tsconfig.json', '--noEmit'], A, `tsc_plain_${tag}.log`);
const cfg = A + '/tsconfig.g118tests.json';
fs.writeFileSync(cfg, JSON.stringify({ extends: './tsconfig.json', compilerOptions: { noEmit: true, rootDir: './src', types: ['node', 'jest'] }, include: ['src/**/*'], exclude: ['node_modules', 'dist', 'src/**/*.integration.test.ts'] }));
const files = run(B + '/tsc', ['-p', 'tsconfig.g118tests.json', '--listFilesOnly'], A, `tsc_files_${tag}.log`);
console.log('originate src files', files.split('\n').filter((l) => l.includes('/services/originate/src/')).length);
run(B + '/tsc', ['-p', 'tsconfig.g118tests.json'], A, `tsc_tests_${tag}.log`);
const T = A + '/src/__tests__/ks1868-signatories-nominate-catch-o77p2-unreadable-throw.test.ts';
const T2 = 'services/originate/src/__tests__/ks1868-third-party-verifiers-register-approve-catches-o77p3-unreadable-throw.test.ts';
if (tag === 'head') {
  const orig = fs.readFileSync(T, 'utf8'); fs.writeFileSync(T, orig + '\nconst G118_UNUSED: number = "x";\n');
  run(B + '/tsc', ['-p', 'tsconfig.g118tests.json'], A, `tsc_tests_planted.log`);
  fs.writeFileSync(T, orig); console.log('restored', fs.readFileSync(T, 'utf8') === orig);
  run(B + '/eslint', ['services/originate/src/routes/signatories.ts', 'services/originate/src/routes/thirdPartyVerifiers.ts', 'services/originate/src/__tests__/ks1868-signatories-nominate-catch-o77p2-unreadable-throw.test.ts', T2], D, 'eslint_pr_files.log');
  fs.writeFileSync(A + '/src/zz_g118_planted.ts', 'export function f(): number { const unused = 1; debugger; return 2; }\n');
  run(B + '/eslint', ['services/originate/src/zz_g118_planted.ts'], D, 'eslint_planted.log');
  fs.renameSync(A + '/src/zz_g118_planted.ts', G + '/logs/_quarantine/zz_g118_planted.ts');
}
fs.renameSync(cfg, G + `/logs/_quarantine/tsconfig.g118tests.${tag}.json`);
