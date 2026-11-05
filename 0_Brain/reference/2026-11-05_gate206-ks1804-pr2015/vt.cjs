// runs vitest with cwd = argv[2] (no shell cd)
const root = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate206-ks1804-pr2015/'+process.env.GN+'/Blockchain/Dev'; const dir = process.argv[2]; process.chdir(dir);
process.argv = [process.argv[0], 'vitest', 'run', ...process.argv.slice(3)];
import(require('path').join(root, 'node_modules/vitest/vitest.mjs'));
