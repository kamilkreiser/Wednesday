// vitest anchored: --root <service dir>, cwd = <workdir>/logs/child_cwd (any relative logs/ lands there), TMPDIR in scratchpad.
const { spawnSync } = require('child_process');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate147-ks1868-pr1963';
const D = W + '/repo/Blockchain/Dev';
const svc = process.argv[2];
const r = spawnSync(D + '/node_modules/.bin/vitest', ['run', '--root', D + '/services/' + svc, ...process.argv.slice(3)], { cwd: W + '/logs/child_cwd', stdio: 'inherit', env: { ...process.env, TMPDIR: '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g147' } });
process.exit(r.status == null ? 99 : r.status);
