#!/usr/bin/env python3
"""registry_gate53.py — the drafter's prediction for requirement 4 (the override's VALUE) and the hoisted copy's provenance. Registry READS only
(`npm view`, no install, no write). Checks:
  R1 a 2.x major of kit override_child is PUBLISHED (so a bare `>=1.19.15` would resolve the semver-major move KS-530 exists to do properly).
  R2 what each range resolves to TODAY: `^1.19.15` -> its max satisfying (== kit registry expect_caret_max, a 1.x) and `>=1.19.15` -> a 2.x.
  R3 the head lock's hoisted copy: `integrity` == the registry's dist.integrity for kit hoisted_version, AND `resolved` == its dist.tarball;
     CONTROL in the same run: the registry's integrity for the pruned version (kit nested_version_base) must DIFFER from the lock's.
  R4 the hoisted version satisfies the override value (semver ^ by npm's own `npm view <pkg>@<range>` set, not by reasoning).
Overrides (controls): --integrity <s> (stands in for the head lock's hoisted integrity), --range-caret <r> (stands in for the override value).
rc 0 PASS / rc 1 FAIL. Usage: registry_gate53.py <scratchpad> [--integrity S] [--range-caret R]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate53.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
CL = os.path.join(SP, 'g53_sp', 'clone'); N = K['order'][0]; PK = K['override_child']; H = P['pr_pins'][N]['head']
def view(*a):
    r = subprocess.run(['npm', 'view', *a, '--json'], capture_output=True, text=True)
    if r.returncode: raise SystemExit('REFUSING: npm view %s rc %d: %s' % (' '.join(a), r.returncode, r.stderr.strip()[:200]))
    return json.loads(r.stdout)
def maxv(spec):
    v = view(spec, 'version'); v = v if isinstance(v, list) else [v]
    return sorted(v, key=lambda s: [int(x) for x in s.split('-')[0].split('.')])[-1], len(v)
print('registry_gate53 %s | npm %s | package %s | head %s' % (datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
      subprocess.run(['npm', '-v'], capture_output=True, text=True).stdout.strip(), PK, H[:12]))
res = []
def chk(tag, ok, msg): res.append(ok); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
vs = view(PK, 'versions'); tags = view(PK, 'dist-tags')
maj2 = [v for v in vs if v.startswith('2.') and '-' not in v]
chk('R1 2.x published', bool(maj2) == K['registry']['expect_major2_published'], '%d versions | stable 2.x: %d (%s .. %s) | dist-tags %s' % (len(vs), len(maj2), maj2[:1], maj2[-1:], json.dumps(tags)))
rng = opt('--range-caret', K['override_value']); cm, cn = maxv('%s@%s' % (PK, rng)); gm, gn = maxv('%s@>=%s' % (PK, K['override_value'].lstrip('^~')))
chk('R2 ranges', cm == K['registry']['expect_caret_max'] and cm.startswith('1.') and gm.startswith('2.'),
    '`%s` -> max %s over %d version(s) (want %s, a 1.x) | `>=%s` -> max %s over %d version(s) (a 2.x: the bug a bare >= would be)' % (
        rng, cm, cn, K['registry']['expect_caret_max'], K['override_value'].lstrip('^~'), gm, gn))
lock = json.loads(subprocess.run(['git', '-C', CL, 'show', '%s:%s' % (H, K['root_lock'])], capture_output=True, text=True).stdout)
hv = lock['packages'][K['hoisted_key']]; li = opt('--integrity', hv.get('integrity'))
d17 = view('%s@%s' % (PK, K['hoisted_version']), 'dist'); d11 = view('%s@%s' % (PK, K['nested_version_base']), 'dist')
chk('R3 provenance', li == d17.get('integrity') and hv.get('resolved') == d17.get('tarball') and d11.get('integrity') != li,
    'lock %s %s integrity == registry dist.integrity: %s | resolved == dist.tarball: %s (%s) | CONTROL the registry integrity of %s differs from the lock\'s: %s' % (
        K['hoisted_key'], hv.get('version'), li == d17.get('integrity'), hv.get('resolved') == d17.get('tarball'), hv.get('resolved'), K['nested_version_base'], d11.get('integrity') != li))
sat = view('%s@%s' % (PK, rng), 'version'); sat = sat if isinstance(sat, list) else [sat]
chk('R4 satisfies', hv.get('version') in sat and K['nested_version_base'] not in sat,
    'hoisted %s is in the set `%s` admits: %s | the pruned %s is NOT: %s | the set: %s' % (hv.get('version'), rng, hv.get('version') in sat, K['nested_version_base'], K['nested_version_base'] not in sat, sat))
nf = res.count(False)
print('REGISTRY %s: %d FAIL of %d checks' % ('PASS' if nf == 0 else 'FAIL', nf, len(res)))
raise SystemExit(1 if nf else 0)
