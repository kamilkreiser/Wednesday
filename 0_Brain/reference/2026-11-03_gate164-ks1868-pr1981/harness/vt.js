// G164: run the clone's vitest with cwd = services/security (no shell cd). argv: outJson, ...vitest args
const { spawnSync } = require('child_process');
const path = require('path');
const W = path.resolve(__dirname, '..');
const S = path.join(W, 'repo/Blockchain/Dev/services/security');
const VT = path.join(W, 'repo/Blockchain/Dev/node_modules/.bin/vitest');
const [out, ...rest] = process.argv.slice(2);
const r = spawnSync(VT, ['run', '--root', S, '--reporter=json', '--outputFile=' + out, ...rest], { cwd: S, stdio: ['ignore', 'ignore', 'ignore'] });
process.exit(r.status === null ? 99 : r.status);
