// vitest anchored: --root = the referral service in the gate clone (or argv ROOT env), config = its own, cwd = <workdir>/logs/child_cwd.
const { spawnSync } = require('child_process');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate153-ks1868-pr1969';
const D = W + '/repo/Blockchain/Dev', T = process.env.G153_ROOT || (D + '/services/referral');
const r = spawnSync(D + '/node_modules/.bin/vitest', ['run', '--root', T, '--config', T + '/vitest.config.ts', ...process.argv.slice(2)],
  { cwd: W + '/logs/child_cwd', stdio: 'inherit', env: { ...process.env, TMPDIR: '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g153' } });
process.exit(r.status == null ? 99 : r.status);
