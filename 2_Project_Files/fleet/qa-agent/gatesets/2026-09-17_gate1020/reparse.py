#!/usr/bin/env python3
"""reparse.py — re-reads drafter_run.py's saved out/*.out (node 24 --test prints the SPEC reporter when stdout is not a TTY, so the TAP
parse in drafter_run.py read '?'). Counts come from the 'ℹ tests|pass|fail N' summary lines; failing case names from the '✖' lines above
'✖ failing tests:'. Positive control: every *_lockdiscovery / *_contract file must carry a 'tests' summary line, else it is reported NO-SUMMARY."""
import glob, os, re
O = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1020/out'
for f in sorted(glob.glob(O + '/*.out')):
    s = open(f, encoding='utf-8').read(); name = os.path.basename(f)[:-4]
    rc = re.search(r'^# cwd .* fake (\S+) rc (-?\d+)', s, re.M)
    fake, rc = (rc.group(1), rc.group(2)) if rc else ('?', '?')
    if name.endswith('_lockdiscovery') or name.endswith('_contract'):
        g = lambda k: (re.findall(r'^ℹ %s (\d+)' % k, s, re.M) or ['NO-SUMMARY'])[-1]
        head = s.split('✖ failing tests:')[0]
        fails = [re.sub(r' \([\d.]+ms\)$', '', l[2:]) for l in head.splitlines() if l.startswith('✖ ')]
        print('%-52s fake %-24s rc %s tests %s pass %s fail %s skipped %s' % (name, fake, rc, g('tests'), g('pass'), g('fail'), g('skipped')))
        for x in fails: print('      fail:', x[:130])
    elif name.startswith('npmci'):
        continue
    else:
        body = s.split('--- stdout', 1)[-1]
        key = [l.strip() for l in body.splitlines() if re.search(r'LAPSED|not an ISO|^OK|standalone lockfiles|FAIL', l)]
        print('%-52s fake %-24s rc %s | %s' % (name, fake, rc, ' || '.join(k[:110] for k in key[:3])))
