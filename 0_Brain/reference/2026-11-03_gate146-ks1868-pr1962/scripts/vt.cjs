// vitest anchored: --root = the transfer service in the gate clone, config = its own, cwd = <workdir>/logs/child_cwd.
const { spawnSync } = require('child_process');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962';
const D = W + '/repo/Blockchain/Dev', T = D + '/services/transfer';
const r = spawnSync(D + '/node_modules/.bin/vitest', ['run', '--root', T, '--config', T + '/vitest.config.ts', ...process.argv.slice(2)],
  { cwd: W + '/logs/child_cwd', stdio: 'inherit', env: { ...process.env, TMPDIR: '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g146' } });
process.exit(r.status == null ? 99 : r.status);
