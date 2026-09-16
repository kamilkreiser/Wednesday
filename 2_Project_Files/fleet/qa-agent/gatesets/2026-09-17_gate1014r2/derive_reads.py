#!/usr/bin/env python3
"""derive_reads.py — derive gh_read.py / linear_read.py for the #1014 ROUND 2 set from the round-1 set's scripts by ASSERTED substitutions (each anchor count asserted)."""
import sys
R1 = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014/'
R2 = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2/'
def derive(name, subs):
    s = open(R1 + name).read()
    for old, new, want in subs:
        n = s.count(old)
        if n != want: print('ANCHOR COUNT', name, repr(old[:60]), n, '!=', want); sys.exit(1)
        s = s.replace(old, new)
    open(R2 + name, 'w').write(s); print('derived', name, len(subs), 'substitutions')
derive('gh_read.py', [
  ("G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014'", "G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2'", 1),
  ("H = '616c766a57a51238450c99bbf1d59bb109e3841c'", "H = '9ba0caf78b8ddb737541df38303b776c982521d2'", 1),
  ("for ref in (dev, H):", "for ref in (dev, H, 'a226d94fe8c6fbfecb81de415feb645302cdd166'):", 1),
  ("print('  blob %-72s develop %s head %s' % (f, row[dev[:9]], row[H[:9]]))", "print('  blob %-72s develop %s head %s pr1016 %s' % (f, row[dev[:9]], row[H[:9]], row['a226d94fe']))", 1),
  ("'services/api-gateway/src/services/enforcement.ts', ", "'services/api-gateway/src/services/enforcement.ts', 'services/originate/src/routes/documents.ts', ", 1),
])
derive('linear_read.py', [
  ('for the #1014 set (KS-1176, KS-1190, KS-1187)', 'for the #1014 ROUND 2 set (KS-1176, KS-1187, KS-1190, KS-1195..KS-1198)', 1),
  ("'https://github.com/Secuura/Distributed_Secuura/pull/1011']", "'https://github.com/Secuura/Distributed_Secuura/pull/1011', 'https://github.com/Secuura/Distributed_Secuura/pull/1015', 'https://github.com/Secuura/Distributed_Secuura/pull/1016']", 1),
])
