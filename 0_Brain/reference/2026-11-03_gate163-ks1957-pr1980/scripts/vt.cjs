// vitest anchored: --root = the referral service in the gate clone (or G163_ROOT), its own config, cwd = <workdir>/logs/child_cwd,
// TMPDIR in the session scratchpad. Never run from the coordinator's tree.
const { spawnSync } = require('child_process');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980';
const D = W + '/repo/Blockchain/Dev', T = process.env.G163_ROOT || (D + '/services/referral');
const SC = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6b87194c-7310-4eff-9191-a63be490f43e/scratchpad/g163';
require('fs').mkdirSync(SC, { recursive: true });
const r = spawnSync(D + '/node_modules/.bin/vitest', ['run', '--root', T, '--config', T + '/vitest.config.ts', ...process.argv.slice(2)],
  { cwd: W + '/logs/child_cwd', stdio: 'inherit', env: { ...process.env, TMPDIR: SC } });
process.exit(r.status == null ? 99 : r.status);
