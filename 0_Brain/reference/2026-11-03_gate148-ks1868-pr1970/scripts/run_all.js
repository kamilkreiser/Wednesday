// Runs suites, static, mutants with cwd anchored in the gate workdir (G144-F7: production-mode cells write logs/*.log relative to cwd).
const { spawnSync } = require('child_process');
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970';
const cwd = W + '/logs/run_cwd';
for (const [cmd, args] of [['bash', [W + '/scripts/suites.sh']], ['bash', [W + '/scripts/static.sh']], ['python3', ['-I', W + '/scripts/mutants.py']]]) {
  const r = spawnSync(cmd, args, { cwd, stdio: ['ignore', 'pipe', 'pipe'], encoding: 'utf8', maxBuffer: 1 << 28 });
  require('fs').appendFileSync(W + '/logs/run_all.log', args.join(' ') + ' rc=' + r.status + '\n' + (r.stdout || '').slice(-4000) + (r.stderr || '').slice(-2000) + '\n');
}
require('fs').writeFileSync(W + '/logs/run_all.done', new Date().toISOString() + '\n');
