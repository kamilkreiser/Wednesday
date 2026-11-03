// vitest anchored: --root = the referral service in the chosen tree (G167_ROOT, default head clone), its own config,
// cwd = <workdir>/logs/child_cwd, TMPDIR = <workdir>/tmp, HOME = <workdir>/home. Never run from the coordinator's tree.
const { spawnSync } = require('child_process');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate167-ks1572-pr1984';
const D = W + '/repo/Blockchain/Dev', T = process.env.G167_ROOT || (D + '/services/referral');
const cfg = process.env.G167_CFG || 'vitest.config.ts';
const r = spawnSync(D + '/node_modules/.bin/vitest', ['run', '--root', T, '--config', T + '/' + cfg, ...process.argv.slice(2)],
  { cwd: W + '/logs/child_cwd', stdio: 'inherit',
    env: { PATH: process.env.PATH, HOME: W + '/home', TMPDIR: W + '/tmp', NODE_ENV: 'test', ...(process.env.G167_ENV ? JSON.parse(process.env.G167_ENV) : {}) } });
process.exit(r.status == null ? 99 : r.status);
