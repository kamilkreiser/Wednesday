// tsc (plain + a scratch config that adds the tests) for both services at the CURRENT worktree product, and eslint on the changed files.
// usage: node tsc_lint.js <tag>
const { spawnSync } = require('child_process'); const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate114-ks1868-pr1932';
const D = G + '/repo/Blockchain/Dev', B = D + '/node_modules/.bin'; const tag = process.argv[2] || 'head';
const run = (cmd, args, cwd, log) => { const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', maxBuffer: 1 << 26 }); const out = (r.stdout || '') + (r.stderr || ''); fs.writeFileSync(G + '/logs/' + log, out + '\nrc=' + r.status + '\n'); const n = (out.match(/error TS\d+/g) || []).length; console.log(log, 'rc', r.status, 'TS errors', n); return out; };
for (const [svc, types] of [['anchoring', ['node', 'vitest/globals']], ['originate', ['node', 'jest']]]) {
  const A = D + '/services/' + svc;
  run(B + '/tsc', ['-p', 'tsconfig.json', '--noEmit'], A, `tsc_plain_${svc}_${tag}.log`);
  const cfg = A + '/tsconfig.g114tests.json';
  fs.writeFileSync(cfg, JSON.stringify({ extends: './tsconfig.json', compilerOptions: { noEmit: true, rootDir: './src', types }, include: ['src/**/*'], exclude: ['node_modules', 'dist', 'src/**/*.integration.test.ts'] }));
  run(B + '/tsc', ['-p', 'tsconfig.g114tests.json'], A, `tsc_tests_${svc}_${tag}.log`);
  if (tag === 'head') {
    const t = A + '/src/__tests__/' + fs.readdirSync(A + '/src/__tests__').find((f) => f.startsWith('ks1868-anch'));
    const orig = fs.readFileSync(t, 'utf8'); fs.writeFileSync(t, orig + '\nconst G114_UNUSED = 1;\n');
    run(B + '/tsc', ['-p', 'tsconfig.g114tests.json'], A, `tsc_tests_${svc}_planted.log`);
    fs.writeFileSync(t, orig); console.log('restored', svc, fs.readFileSync(t, 'utf8') === orig);
  }
  fs.renameSync(cfg, G + `/logs/_quarantine/tsconfig.g114tests.${svc}.${tag}.json`);
}
if (tag === 'head') {
  run(B + '/eslint', ['services/anchoring/src/index.ts', 'services/originate/src/routes/anchors.ts', 'services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts', 'services/originate/src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts'], D, 'eslint_pr_files.log');
  fs.writeFileSync(D + '/services/anchoring/src/zz_g114_planted.ts', 'export function f(): number { const unused = 1; debugger; return 2; }\n');
  run(B + '/eslint', ['services/anchoring/src/zz_g114_planted.ts'], D, 'eslint_planted.log');
  fs.renameSync(D + '/services/anchoring/src/zz_g114_planted.ts', G + '/logs/_quarantine/zz_g114_planted.ts');
}
