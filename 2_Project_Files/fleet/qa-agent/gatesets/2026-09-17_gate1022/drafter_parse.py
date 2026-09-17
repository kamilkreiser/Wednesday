#!/usr/bin/env python3
"""drafter_parse.py — #1022: parse-level scope control of the 3 locks + baseline conservation, from blobs in the drafter's OWN clone.
Every zero is paired with a planted control on the same instrument."""
import json, subprocess, sys, copy
C = open('/private/tmp/claude-501/drafter1022/CLONE_PATH').read().strip() + '/repo'
HEAD = '58684e6534b4d420c9fb9ea246d3a32c70c70828'; BASE = 'f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'
DEV = '581c9db0db4201c42cbbf702f339b750989acdb1'; PR1021 = '742e1c6080f2527973268146611930e4a70edef2'
M_DEV_1022 = 'b475cfbe1c7e7864adf0eb81bdcf829dd5637e06'; M_BOTH = '1b03e6951f447a28c60bf69d2ebbed426a272697'
def show(rev, path): return subprocess.run(['git', '-C', C, 'show', rev + ':' + path], capture_output=True, text=True, check=True).stdout
D = 'Blockchain/Dev/'
LOCKS = [D + 'services/mcp-server/package-lock.json', D + 'services/originate/package-lock.json', D + 'package-lock.json']
FLAGS = ('dev', 'optional', 'devOptional', 'peer')
def diff_packages(a, b):
    pa, pb = a['packages'], b['packages']
    out = []
    for k in sorted(set(pa) | set(pb)):
        if k not in pa: out.append((k, 'ADDED', None)); continue
        if k not in pb: out.append((k, 'REMOVED', None)); continue
        if pa[k] != pb[k]:
            fields = sorted(f for f in set(pa[k]) | set(pb[k]) if pa[k].get(f) != pb[k].get(f))
            out.append((k, 'CHANGED', {f: (pa[k].get(f), pb[k].get(f)) for f in fields}))
    return out
def is_hono(k): return k.split('node_modules/')[-1] == 'hono'
RULED_LIGHTNING = None
for lock in LOCKS:
    a = json.loads(show(BASE, lock)); b = json.loads(show(HEAD, lock))
    print('LOCK', lock, '| top-level keys equal except packages:', {k: a[k] == b.get(k) for k in a if k != 'packages'}, '| entries base', len(a['packages']), 'head', len(b['packages']))
    d = diff_packages(a, b)
    for k, kind, f in d:
        tag = 'HONO' if is_hono(k) else 'OTHER'
        print('  %s %s %s %s' % (tag, kind, k, json.dumps(f, sort_keys=True)))
    hono_entries = [k for k in a['packages'] if is_hono(k)]
    for k in hono_entries:
        e = a['packages'][k]; h = b['packages'].get(k, {})
        print('  hono entry', k, 'base', e.get('version'), {x: e.get(x) for x in FLAGS if x in e}, '| head', h.get('version'), {x: h.get(x) for x in FLAGS if x in h}, '| integrity changed', e.get('integrity') != h.get('integrity'), '| resolved', h.get('resolved'))
    decl = []
    for k, v in b['packages'].items():
        for sect in ('dependencies', 'optionalDependencies', 'peerDependencies', 'devDependencies'):
            for dep, rng in (v.get(sect) or {}).items():
                if dep in ('hono', '@hono/node-server'): decl.append((k or '<root>', v.get('version'), sect, dep, rng, v.get('dev'), v.get('devOptional')))
    for x in decl: print('  declarer at head:', x)
    nonhono = [x for x in d if not is_hono(x[0])]
    if lock == D + 'package-lock.json':
        light = [x for x in nonhono if 'lightningcss-' in x[0] and x[1] == 'CHANGED' and x[2] == {'dev': (True, None)}]
        mag = [x for x in nonhono if x[0].endswith('node_modules/magicast') and x[2] == {'dev': (True, None), 'devOptional': (None, True)}]
        rest = [x for x in nonhono if x not in light and x not in mag]
        vers = [x for x in nonhono if x[2] and 'version' in x[2]]
        print('  ROOT RULED: lightningcss-<platform> dev removed only: %d | magicast dev->devOptional: %d | other non-hono changes: %d | version fields among non-hono: %d' % (len(light), len(mag), len(rest), len(vers)))
        for x in light: print('    ruled', x[0])
        # control: plant an unruled flag change and a version change; the classifier must count them as rest
        bb = copy.deepcopy(b); key = sorted(k for k in bb['packages'] if k.endswith('node_modules/semver'))[0]
        bb['packages'][key]['dev'] = not bb['packages'][key].get('dev', False)
        key2 = sorted(k for k in bb['packages'] if k.endswith('node_modules/lightningcss-darwin-arm64'))
        if key2: bb['packages'][key2[0]]['version'] = '0.0.0-planted'
        dd = [x for x in diff_packages(a, bb) if not is_hono(x[0])]
        light2 = [x for x in dd if 'lightningcss-' in x[0] and x[1] == 'CHANGED' and x[2] == {'dev': (True, None)}]
        mag2 = [x for x in dd if x[0].endswith('node_modules/magicast') and x[2] == {'dev': (True, None), 'devOptional': (None, True)}]
        rest2 = [x for x in dd if x not in light2 and x not in mag2]
        print('  CONTROL planted (%s dev flip, %s version): ruled lightningcss %d, magicast %d, other %d -> %s' % (key, key2[0] if key2 else 'none', len(light2), len(mag2), len(rest2), [r[0] for r in rest2]))
    else:
        print('  non-hono changes: %d' % len(nonhono))
    # hono control: move a non-hono version in a copy, classifier must flag it
    bb = copy.deepcopy(b); k0 = sorted(k for k in bb['packages'] if k and not is_hono(k))[0]; bb['packages'][k0]['version'] = '9.9.9-planted'
    print('  CONTROL planted version on %s -> non-hono changes %d' % (k0, len([x for x in diff_packages(a, bb) if not is_hono(x[0])])))
# manifests
out = subprocess.run(['git', '-C', C, 'diff', '--name-only', BASE, HEAD], capture_output=True, text=True, check=True).stdout.split()
print('MANIFESTS changed:', [f for f in out if f.endswith('package.json')], '| control: package.json files in the tree at head:',
      len([l for l in subprocess.run(['git', '-C', C, 'ls-tree', '-r', '--name-only', HEAD], capture_output=True, text=True).stdout.split() if l.endswith('/package.json')]))
# baseline conservation
BL = D + 'scripts/audit/audit-baseline.json'
def rows(rev):
    j = json.loads(show(rev, BL))
    assert isinstance(j, dict) and isinstance(j.get('accepted'), dict), 'baseline shape unknown'
    return j, 'accepted', [dict(v, _id=k) for k, v in j['accepted'].items()]
def key(r): return r['_id']
for label, rev in (('base', BASE), ('head', HEAD), ('develop', DEV), ('#1021', PR1021), ('merged dev+#1022', M_DEV_1022), ('merged dev+#1021+#1022', M_BOTH)):
    j, k, r = rows(rev)
    print('BASELINE', label, 'rows', len(r), '| key field', k, '| top-level keys', list(j) if isinstance(j, dict) else 'list')
jb, kf, rb = rows(BASE); jh, _, rh = rows(HEAD)
kb = {key(x): x for x in rb}; kh = {key(x): x for x in rh}
removed = sorted(set(kb) - set(kh)); added = sorted(set(kh) - set(kb)); altered = sorted(x for x in set(kb) & set(kh) if kb[x] != kh[x])
print('CONSERVATION base->head: removed', removed, '| added', added, '| altered', altered, '| other top-level keys equal', {k: jb[k] == jh[k] for k in jb if k != kf} if isinstance(jb, dict) else '')
for x in removed: print('  removed row', json.dumps({kk: vv for kk, vv in kb[x].items() if kk != 'reason'}), '| reason chars', len(kb[x].get('reason', '')))
ctrl = copy.deepcopy(rh); first = 'expires' if 'expires' in ctrl[0] else 'reason'; ctrl[0][first] = str(ctrl[0].get(first)) + 'x'
kc = {key(x): x for x in ctrl}
print('CONTROL altered-row planted on head row 0 field', first, '-> altered', len([x for x in set(kb) & set(kc) if kb[x] != kc[x]]))
jm, _, rm_ = rows(M_BOTH); _, _, r21 = rows(PR1021)
print('MERGED both: rows', len(rm_), '= base 38 - 3 (hono) - 1 (colord):', len(rm_) == len(rb) - 3 - 1, '| removed vs base', sorted(set(kb) - {key(x) for x in rm_}))
print('bytes merged-both baseline valid JSON: yes (parsed above)')
