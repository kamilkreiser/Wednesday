// usage: node run.mjs <cwd> <cmd> [args...]; runs a command with a working directory, without a shell cd. Exits with its rc.
import { spawnSync } from 'node:child_process';
const [cwd, cmd, ...args] = process.argv.slice(2);
const r = spawnSync(cmd, args, { cwd, stdio: 'inherit' });
process.exit(r.status ?? 1);
