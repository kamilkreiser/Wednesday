#!/usr/bin/env python3
# Re-run the unit-survivor mutants that change SQL or recorded state against the REAL-PG legacy cell (wt/mut -> repo/), sha-restored.
import hashlib, subprocess, json, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979'
P = W + '/repo/Blockchain/Dev/services/referral/src/services/milestoneService.ts'
orig = open(P).read(); osha = hashlib.sha256(orig.encode()).hexdigest()
port = subprocess.run(['docker', 'port', 'g162-pg', '5432'], capture_output=True, text=True).stdout.strip().split(':')[-1]
M = [('M0 none (clone = head)', None, None),
 ('M11 awarded read CLAIMABLE only', "WHERE user_id = $1 AND source_type = $2\n", "WHERE user_id = $1 AND source_type = $2 AND status = 'CLAIMABLE'\n"),
 ('M13 total not incremented for stored rows', "        progress.currentTier = milestone.tier;\n        progress.totalMilestoneRewards += milestone.rewardAmount;\n        continue;", "        progress.currentTier = milestone.tier;\n        continue;"),
 ('M12 achievedAt now', "          achievedAt: firstAwardedAt,", "          achievedAt: new Date(),")]
out = []
for name, a, b in M:
    if a: assert orig.count(a) == 1; open(P, 'w').write(orig.replace(a, b))
    subprocess.run(['node', W + '/scripts/g162.cjs', 'mut', 'legacy', 'pk'], env={**os.environ, 'G162_PGPORT': port}, capture_output=True)
    d = json.load(open(W + '/logs/probe/mut__legacy__mr-pk.json'))
    out.append(f"{name} | c1={d['c1'].get('new')} c2={d['c2'].get('new')} counts={d['counts']} progress={d['progress']}")
    os.replace(W + '/logs/probe/mut__legacy__mr-pk.json', W + f"/logs/probe_mut/{name.split()[0]}__legacy.json") if os.path.isdir(W + '/logs/probe_mut') else None
    open(P, 'w').write(orig)
    assert hashlib.sha256(open(P).read().encode()).hexdigest() == osha
open(W + '/logs/mutants_realpg.log', 'w').write('\n'.join(out) + '\nrestore sha256 equal: True\n')
print('\n'.join(out))
