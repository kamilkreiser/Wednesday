// G161: run the clone's vitest with cwd = services/auth (no shell cd). argv: outJson, ...vitest args
const { spawnSync } = require('child_process');
const path = require('path');
const W = path.resolve(__dirname, '..');
const A = path.join(W, 'repo/Blockchain/Dev/services/auth');
const VT = path.join(W, 'repo/Blockchain/Dev/node_modules/.bin/vitest');
const [out, ...rest] = process.argv.slice(2);
const r = spawnSync(VT, ['run', '--root', A, '--reporter=json', '--outputFile=' + out, ...rest], { cwd: A, stdio: ['ignore', 'ignore', 'ignore'] });
process.exit(r.status === null ? 99 : r.status);
