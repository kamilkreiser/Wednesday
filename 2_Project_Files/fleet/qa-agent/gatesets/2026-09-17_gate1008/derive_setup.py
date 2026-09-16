#!/usr/bin/env python3
"""derive_setup.py — writes drafter_setup.py for #1008 from the sibling set's drafter_setup.py by asserted replacements (no writes outside the gate set)."""
import sys, re
s = open(sys.argv[1]).read()
reps = [
 ('"""drafter_setup.py — #1006 drafter substrate.', '"""drafter_setup.py — #1008 (KS-1087) drafter substrate.', 1),
 ('(base = develop 40fe4db69 / head 86fe59e6b). NO merged worktree: develop is an ANCESTOR of the head (merge-base = develop,\nbehind 0), so the merged tree IS the head tree — asserted here by merge-base, not assumed.',
  '(base = develop 93629700c / head dd7086d5a). NO merged worktree: develop is an ANCESTOR of the head (merge-base = develop,\nbehind 0), so the merged tree IS the head tree — asserted here by merge-base, not assumed.', 1),
 ('the two packages vitest runs in — packages/shared and\nservices/demo-service — are farmed per entry too', 'the packages vitest may run in — packages/shared and\nservices/api-gateway — are farmed per entry too', 1),
 ("GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1006'", "GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008'", 1),
 ("SHA = dict(base='40fe4db6963cd11dba06bd46e0b00af39e68ef3a', head='86fe59e6bf07108142fb3dbd06bef8747d2a4687', prev='e28c91f9b990273ea34036cb88ad6abf0f39e73b')",
  "SHA = dict(base='93629700c3d219c1d8ca61d69150bb9b623fc1be', head='dd7086d5aa574285beffc515f9371a438621f25d')", 1),
 ("PER_ENTRY = {'packages/shared', 'services/demo-service'}", "PER_ENTRY = {'packages/shared', 'services/api-gateway'}", 1),
 ("tempfile.mkdtemp(prefix='gate1006_draft_', dir=SCR)", "tempfile.mkdtemp(prefix='gate1008_draft_', dir=SCR)", 1),
 ("'HEAD:' + DEV + '/packages/shared', 'HEAD:' + DEV + '/services/demo-service']); P('   shared/demo-service tree hashes'", "'HEAD:' + DEV + '/packages/shared', 'HEAD:' + DEV + '/services/api-gateway']); P('   shared/api-gateway tree hashes'", 1),
 ("cwd=wt + '/' + DEV + '/services/demo-service/src')", "cwd=wt + '/' + DEV + '/services/api-gateway/src')", 1),
 ("P('  resolve from', name, 'demo-service/src:'", "P('  resolve from', name, 'api-gateway/src:'", 1),
]
for a, b, n in reps:
    c = s.count(a); assert c == n, (a[:70], c)
    s = s.replace(a, b)
left = [s[m.start()-40:m.start()+20] for m in re.finditer(r'1006|demo-service|40fe4db|86fe59e|e28c91f', s)]
assert not left, ('residual', left)
open(sys.argv[2], 'w').write(s); print('drafter_setup.py written, replacements', len(reps))
