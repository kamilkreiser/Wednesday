#!/usr/bin/env python3
"""merged_read.py — IN THE DRAFTER CLONE ONLY: merge-base and merge-tree --write-tree of head x the landed develop fa887f382 (object reachable through the
--shared alternates), compared with the drafter's merged14 worktree tree. No write verb in the checkout."""
import json, subprocess, datetime
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1017'
PA = json.load(open(G + '/drafter_paths.json')); C = PA['C']; H = PA['sha']['head']; DEV = 'fa887f382b212b8da4a0a4a556bacb05ea34daaa'
def run(c): p = subprocess.run(c, capture_output=True, text=True); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('merged_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('cat-file develop in clone', run(['git', '-C', C, 'cat-file', '-t', DEV]))
print('develop tree', run(['git', '-C', C, 'rev-parse', DEV + '^{tree}']))
print('merge-base head develop', run(['git', '-C', C, 'merge-base', H, DEV]))
rc, o, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', H, DEV]); print('merge-tree --write-tree head x develop (IN THE CLONE) rc', rc, 'tree', o.split('\n')[0], 'conflict lines', len(o.split('\n')) - 1, e[:200])
print('merged14 worktree HEAD^{tree}', run(['git', '-C', PA['trees']['merged14'], 'rev-parse', 'HEAD^{tree}']))
for f in ('services/api-gateway/src/routes/verification.ts', 'services/api-gateway/src/services/enforcement.ts', 'services/api-gateway/src/middleware/auth.ts', 'services/api-gateway/src/middleware/rateLimitEnforce.ts', 'services/api-gateway/src/index.ts', 'packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts'):
    print('  merged blob', f.split('/')[-1], run(['git', '-C', PA['trees']['merged14'], 'rev-parse', 'HEAD:Blockchain/Dev/' + f])[1][:9])
