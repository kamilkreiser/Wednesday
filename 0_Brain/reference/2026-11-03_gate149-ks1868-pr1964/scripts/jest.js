// Runs originate's jest with cwd anchored in the gate workdir (G144-F7): any logger file lands under logs/child_cwd/logs.
const { spawnSync } = require('child_process');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964';
const D = W + '/repo/Blockchain/Dev', O = D + '/services/originate';
const r = spawnSync(D + '/node_modules/.bin/jest', ['-c', O + '/jest.config.js', '--rootDir', O, ...process.argv.slice(2)], { cwd: W + '/logs/child_cwd', stdio: 'inherit', env: { ...process.env, TMPDIR: '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/efc1d998-fa1a-49cf-954c-5ff5b12449f9/scratchpad/g149' } });
process.exit(r.status == null ? 99 : r.status);
