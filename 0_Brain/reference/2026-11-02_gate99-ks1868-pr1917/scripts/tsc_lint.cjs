const { spawnSync } = require('child_process'); const fs = require('fs'); const crypto = require('crypto');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917';
const D = W + '/repo/Blockchain/Dev', A = D + '/services/tenant-provisioning', B = D + '/node_modules/.bin', T = A + '/src/__tests__';
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const run = (cmd, args, cwd, log) => { const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', maxBuffer: 1 << 26 }); fs.writeFileSync(W + '/logs/' + log, (r.stdout || '') + (r.stderr || '') + '\nrc=' + r.status + '\n'); console.log(log, 'rc', r.status); };
const news = fs.readdirSync(T).filter((f) => f.startsWith('ks1868-tenant-provisioning-'));
// head
run(B + '/tsc', ['-p', 'tsconfig.json', '--noEmit'], A, 'tsc_plain_head.log');
run('node', ['scripts/typecheck-tests/check.cjs', 'services/tenant-provisioning'], D, 'leg16_head.log');
run(B + '/eslint', ['src/index.ts', ...news.map((f) => 'src/__tests__/' + f)], A, 'eslint_pr_files_head.log');
fs.writeFileSync(A + '/src/zz_gate99_planted.ts', 'export function f(): number { const unused = 1; debugger; return 2; }\n');
run(B + '/eslint', ['src/zz_gate99_planted.ts'], A, 'eslint_planted.log');
fs.renameSync(A + '/src/zz_gate99_planted.ts', W + '/logs/_quarantine/zz_gate99_planted.ts');
const t = T + '/' + news[0]; const orig = fs.readFileSync(t, 'utf8');
fs.writeFileSync(t, orig + '\nconst GATE99_BAD: number = "x";\n');
run('node', ['scripts/typecheck-tests/check.cjs', 'services/tenant-provisioning'], D, 'leg16_planted.log');
fs.writeFileSync(t, orig); console.log('restored test', fs.readFileSync(t, 'utf8') === orig);
// base: product swapped, new tests moved out
fs.copyFileSync(W + '/logs/base_index.ts', A + '/src/index.ts');
for (const f of news) fs.renameSync(T + '/' + f, W + '/logs/_stash_' + f);
run(B + '/tsc', ['-p', 'tsconfig.json', '--noEmit'], A, 'tsc_plain_base.log');
run('node', ['scripts/typecheck-tests/check.cjs', 'services/tenant-provisioning'], D, 'leg16_base.log');
run(B + '/eslint', ['src/index.ts'], A, 'eslint_index_base.log');
for (const f of news) fs.renameSync(W + '/logs/_stash_' + f, T + '/' + f);
fs.copyFileSync(W + '/logs/head_index.ts', A + '/src/index.ts');
console.log('product restored', sha(A + '/src/index.ts') === sha(W + '/logs/head_index.ts'));
