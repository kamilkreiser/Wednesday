// tsc (plain + tests + leg 16) and eslint, run with cwd inside the clone via spawnSync (no shell cd).
const { spawnSync } = require('child_process'); const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate94-ks1868-pr1912';
const D = G + '/repo/Blockchain/Dev', A = D + '/services/security', B = D + '/node_modules/.bin';
const run = (cmd, args, cwd, log, input) => { const r = spawnSync(cmd, args, { cwd, input, encoding: 'utf8', maxBuffer: 1 << 26 }); fs.writeFileSync(G + '/logs/' + log, (r.stdout || '') + (r.stderr || '') + '\nrc=' + r.status + '\n'); console.log(log, 'rc', r.status); };
run(B + '/tsc', ['-p', 'tsconfig.json', '--noEmit'], A, 'tsc_plain_head.log');
run(B + '/tsc', ['-p', 'tsconfig.test.json'], A, 'tsc_tests_head.log');
run('node', ['scripts/typecheck-tests/check.cjs', 'services/security'], D, 'leg16_security.log');
const news = ['ks1868-security-key-register-save-catch-unreadable-throw.test.ts', 'ks1868-security-key-revoke-save-catch-unreadable-throw.test.ts', 'ks1868-security-admin-scopes-put-catch-unreadable-throw.test.ts'].map((f) => 'src/__tests__/' + f);
run(B + '/eslint', ['src/index.ts', ...news], A, 'eslint_pr_files.log');
// base index.ts through stdin with the same filename, so the same config applies
run(B + '/eslint', ['--stdin', '--stdin-filename', 'src/index.ts'], A, 'eslint_base_index.log', fs.readFileSync(G + '/logs/base_index.ts', 'utf8'));
// the minimal follow-up (declare without the useless initialiser) checked the same way
const head = fs.readFileSync(G + '/logs/head_index.ts', 'utf8');
const fixed = head.replace('    let isZod = false;\n    let infra = false;\n    try {\n      isZod = error instanceof z.ZodError;', '    let isZod: boolean;\n    let infra: boolean;\n    try {\n      isZod = error instanceof z.ZodError;');
console.log('fix applied', fixed !== head);
run(B + '/eslint', ['--stdin', '--stdin-filename', 'src/index.ts'], A, 'eslint_fixed_index.log', fixed);
fs.mkdirSync(G + '/logs/_quarantine', { recursive: true });
fs.writeFileSync(A + '/src/zz_gate94_planted.ts', 'export function f(): number { const unused = 1; debugger; return 2; }\n');
run(B + '/eslint', ['src/zz_gate94_planted.ts'], A, 'eslint_planted.log');
fs.renameSync(A + '/src/zz_gate94_planted.ts', G + '/logs/_quarantine/zz_gate94_planted.ts');
const t = A + '/' + news[0]; const orig = fs.readFileSync(t, 'utf8');
fs.writeFileSync(t, orig + '\nconst GATE94_UNUSED = 1;\n');
run(B + '/tsc', ['-p', 'tsconfig.test.json'], A, 'tsc_tests_planted.log');
fs.writeFileSync(t, orig); console.log('restored test file', fs.readFileSync(t, 'utf8') === orig);
// tsc on the fixed variant: write it, check, restore by sha
const M = A + '/src/index.ts'; fs.writeFileSync(M, fixed);
run(B + '/tsc', ['-p', 'tsconfig.json', '--noEmit'], A, 'tsc_fixed_variant.log');
fs.writeFileSync(M, head); console.log('index restored', fs.readFileSync(M, 'utf8') === head);
