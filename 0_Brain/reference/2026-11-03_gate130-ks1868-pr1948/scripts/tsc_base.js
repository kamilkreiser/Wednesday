// tsc with tests + leg 16 at BASE product (both files swapped, restored by sha) for the baseline count
const { spawnSync } = require('child_process'); const fs = require('fs'); const crypto = require('crypto');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate130-ks1868-pr1948';
const D = G + '/repo/Blockchain/Dev', A = D + '/services/security', B = D + '/node_modules/.bin';
const sha = (p) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const run = (cmd, args, cwd, log) => { const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', maxBuffer: 1 << 26 }); fs.writeFileSync(G + '/logs/' + log, (r.stdout || '') + (r.stderr || '') + '\nrc=' + r.status + '\n'); console.log(log, 'rc', r.status); };
const h1 = sha(A + '/src/index.ts'), h2 = sha(A + '/src/db.ts');
fs.copyFileSync(G + '/logs/base_index.ts', A + '/src/index.ts'); fs.copyFileSync(G + '/logs/base_db.ts', A + '/src/db.ts');
run(B + '/tsc', ['-p', 'tsconfig.test.json'], A, 'tsc_tests_base.log');
run('node', ['scripts/typecheck-tests/check.cjs', 'services/security'], D, 'leg16_security_base.log');
fs.copyFileSync(G + '/logs/head_index.ts', A + '/src/index.ts'); fs.copyFileSync(G + '/logs/head_db.ts', A + '/src/db.ts');
console.log('restore', sha(A + '/src/index.ts') === h1 && sha(A + '/src/db.ts') === h2 ? 'RESTORE_OK' : 'RESTORE_FAIL');
