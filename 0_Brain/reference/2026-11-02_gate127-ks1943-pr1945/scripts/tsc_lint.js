const { spawnSync } = require('child_process'); const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945';
const D = G + '/repo/Blockchain/Dev', B = D + '/node_modules/.bin', A = D + '/services/originate'; const tag = process.argv[2] || 'head';
fs.mkdirSync(G + '/logs/_quarantine', { recursive: true });
const run = (cmd, args, cwd, log) => { const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', maxBuffer: 1 << 26, env: { ...process.env, TMPDIR: '/tmp/g127' } }); const out = (r.stdout || '') + (r.stderr || ''); fs.writeFileSync(G + '/logs/' + log, out + '\nrc=' + r.status + '\n'); const n = (out.match(/error TS\d+/g) || []).length; console.log(log, 'rc', r.status, 'TS errors', n, 'lines', out.split('\n').length); return out; };
run(B + '/tsc', ['-p', 'tsconfig.json', '--noEmit'], A, `tsc_plain_${tag}.log`);
const cfg = A + '/tsconfig.g127tests.json';
fs.writeFileSync(cfg, JSON.stringify({ extends: './tsconfig.json', compilerOptions: { noEmit: true, rootDir: './src', types: ['node', 'jest'] }, include: ['src/**/*'], exclude: ['node_modules', 'dist', 'src/**/*.integration.test.ts'] }));
const files = run(B + '/tsc', ['-p', 'tsconfig.g127tests.json', '--listFilesOnly'], A, `tsc_files_${tag}.log`);
console.log('originate src files in program:', files.split('\n').filter((l) => l.includes('/services/originate/src/')).length);
run(B + '/tsc', ['-p', 'tsconfig.g127tests.json'], A, `tsc_tests_${tag}.log`);
const T = A + '/src/__tests__/ks1943-retention-sweep-unit-all-or-nothing.test.ts';
if (tag === 'head') {
  const orig = fs.readFileSync(T, 'utf8'); fs.writeFileSync(T, orig + '\nconst G127_UNUSED: number = "x";\n');
  run(B + '/tsc', ['-p', 'tsconfig.g127tests.json'], A, `tsc_tests_planted.log`);
  fs.writeFileSync(T, orig); console.log('restored', fs.readFileSync(T, 'utf8') === orig);
  const changed = ['services/originate/src/db.ts', 'services/originate/src/services/gdprService.ts', 'services/originate/src/__tests__/ks1943-retention-sweep-unit-all-or-nothing.test.ts', 'services/originate/src/__tests__/ks1943-platform-scope-transaction-helper.test.ts', 'services/originate/src/__tests__/ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts'];
  run(B + '/eslint', changed, D, 'eslint_pr_files.log');
  fs.writeFileSync(A + '/src/zz_g127_planted.ts', 'export function f(): number { const unused = 1; debugger; return 2; }\n');
  run(B + '/eslint', ['services/originate/src/zz_g127_planted.ts'], D, 'eslint_planted.log');
  fs.renameSync(A + '/src/zz_g127_planted.ts', G + '/logs/_quarantine/zz_g127_planted.ts');
}
fs.renameSync(cfg, G + `/logs/_quarantine/tsconfig.g127tests.${tag}.json`);
