// G160: run a command with cwd set to argv[2] (no shell cd). Inherits stdio; exits with the child's code.
const { spawnSync } = require('child_process');
const [dir, cmd, ...args] = process.argv.slice(2);
const r = spawnSync(cmd, args, { cwd: dir, stdio: 'inherit' });
process.exit(r.status === null ? 99 : r.status);
