#!/usr/bin/env python3
"""lockcensus_gate48a.py — the drafter's READ (git plumbing only, no build, no install) behind CLAUSE2-REMEASURE and the grant's EXCEPTION: at a
NAMED tree (default the pinned END_TREE), EVERY tracked `package-lock.json` (node_modules excluded) is parsed and every entry whose key ends in
`node_modules/undici` or `node_modules/js-yaml` is listed with its version, its `dev` flag (ABSENT in a v3 lock = a PRODUCTION entry) and whether
it is inside a vulnerable range of GHSA-r53p-7pc4-xj5r (undici) / GHSA-r3ph-w7gj-g6xm (js-yaml), the ranges READ from the GitHub advisory API.
Then the lock's DIRECTORY is classed by what could ship it (a READ, not a build):
  DOCKERFILE-IN-DIR  a Dockerfile* sits in that directory;   COPIED-BY  Dockerfiles anywhere whose COPY/ADD line names that dir's package*.json
  or package-lock.json (the path as written, relative);   COMPOSE-CONTEXT  a compose `context:` value ending in that directory;
  APP  the directory is under mobile/ (a shipped app, not an image: the gate rules whether its bundle is a "shipped tree").
Controls: CT-PARSE the entries parsed across all locks (a parser that sees nothing prints 0); CT-POS a package known to sit in many locks
(`react`) is found in >= 1 lock; CT-NEG a nonsense package is found in 0. The gate re-measures ALL of this (and builds the issuer image) —
this is a PREDICTION with its instruments named, never evidence. rc 0 CENSUS DONE (controls hold) / rc 1. Writes lockcensus_gate48a.json (at END) or lockcensus_gate48a.<tree12>.json (any other tree).
Usage: lockcensus_gate48a.py <scratchpad> [--tree <sha>] [--offline]"""
import json, os, re, subprocess, sys, urllib.request, datetime
G = os.path.dirname(os.path.abspath(__file__)); P = json.load(open(os.path.join(G, 'pins_gate48a.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g48a_sp', 'clone'); T = A[A.index('--tree') + 1] if '--tree' in A else P['end_tree']
def git(*a): return subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True, check=True).stdout
ADV = {'undici': 'GHSA-r53p-7pc4-xj5r', 'js-yaml': 'GHSA-r3ph-w7gj-g6xm'}
FALLBACK = {'undici': ['< 6.28.1', '>= 7.0.0, < 7.29.1', '>= 8.0.0, < 8.10.2'], 'js-yaml': ['>= 5.0.0, <= 5.4.0']}
RNG = {}
for pk, g in ADV.items():
    if '--offline' in A: RNG[pk] = FALLBACK[pk]; continue
    a = json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/advisories/' + g, headers={'Accept': 'application/vnd.github+json'}), timeout=60))
    RNG[pk] = [v['vulnerable_version_range'] for v in a.get('vulnerabilities', []) if (v.get('package') or {}).get('name') == pk]
def V(s): return tuple(int(x) for x in re.findall(r'\d+', s)[:3])
def inr(ver, rng):
    for c in rng.split(','):
        m = re.match(r'\s*(>=|<=|>|<|=)?\s*([\d.]+)', c); op, x = m.group(1) or '=', V(m.group(2)); v = V(ver)
        if not {'>=': v >= x, '<=': v <= x, '>': v > x, '<': v < x, '=': v == x}[op]: return False
    return True
files = git('ls-tree', '-r', '--name-only', T).splitlines()
locks = sorted(f for f in files if f.endswith('package-lock.json') and '/node_modules/' not in '/' + f)
dfs = [f for f in files if re.search(r'(^|/)Dockerfile[^/]*$', f) and '/node_modules/' not in '/' + f]
comp = [f for f in files if re.search(r'(^|/)(docker-)?compose[^/]*\.ya?ml$', f)]
copies = {}
for d in dfs:
    for l in git('show', '%s:%s' % (T, d)).splitlines():
        if re.match(r'\s*(COPY|ADD)\b', l, re.I) and re.search(r'package(-lock)?[^ ]*\.json|package\*\.json', l): copies.setdefault(d, []).append(l.strip())
ctxs = []
for c in comp:
    for l in git('show', '%s:%s' % (T, c)).splitlines():
        m = re.match(r'\s*context:\s*["\']?([^"\'#\s]+)', l)
        if m: ctxs.append((c, m.group(1)))
print('lockcensus_gate48a %s | tree %s (%s) | %d tracked package-lock.json | %d Dockerfile(s), %d with a package*.json COPY | %d compose file(s), %d context(s)' % (
    datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), T, 'END_TREE' if T == P['end_tree'] else 'NOT END', len(locks), len(dfs), len(copies), len(comp), len(ctxs)))
print('    ranges READ %s: undici %s | js-yaml %s' % ('(OFFLINE fallback, not read)' if '--offline' in A else 'from the advisory API', RNG['undici'], RNG['js-yaml']))
rows = []; nent = 0; react = 0; nons = 0
for lk in locks:
    try: d = json.loads(git('show', '%s:%s' % (T, lk)))
    except Exception as e: print('    UNPARSED %s: %s' % (lk, e)); continue
    pk = d.get('packages') or {}; nent += len(pk)
    react += any(k.endswith('node_modules/react') for k in pk); nons += any(k.endswith('node_modules/zz-gate48a-no-such-pkg') for k in pk)
    dr = os.path.dirname(lk) or '.'
    for k, v in pk.items():
        for name in ADV:
            if k.endswith('node_modules/' + name):
                ver = v.get('version', '?'); vul = any(inr(ver, r) for r in RNG[name])
                rel = dr[len('Blockchain/Dev/'):] if dr.startswith('Blockchain/Dev/') else dr   # Dockerfiles COPY relative to their context
                cp = sorted(x for x, ls in copies.items() if any(re.search(r'(^|[\s./])' + re.escape(rel) + r'/package', l) for l in ls))
                cls = []
                if any(os.path.dirname(x) == dr for x in dfs): cls.append('DOCKERFILE-IN-DIR')
                if cp: cls.append('COPIED-BY ' + ','.join(cp[:3]))
                if any(c[1].rstrip('/').endswith(dr.split('/')[-1]) and (dr.split('/')[-1] not in ('.', 'Dev')) for c in ctxs): cls.append('COMPOSE-CONTEXT')
                if dr.startswith('mobile/') or '/mobile/' in dr: cls.append('APP (mobile: the gate rules whether its bundle is a shipped tree)')
                rows.append(dict(lock=lk, key=k, pkg=name, version=ver, dev=v.get('dev', False), vulnerable=vul, classes=cls))
for r in rows:
    print('    %-3s %-8s %-8s dev=%-5s %-55s %s | %s' % ('VUL' if r['vulnerable'] else 'ok', r['pkg'], r['version'], r['dev'], r['lock'], r['key'][:60], ' ; '.join(r['classes']) or 'no image / app class found'))
vul = [r for r in rows if r['vulnerable']]
print('    VULNERABLE entries: %d in %d lock(s): %s' % (len(vul), len(set(r['lock'] for r in vul)), sorted(set('%s %s %s%s' % (r['lock'], r['pkg'], r['version'], ' (dev)' if r['dev'] else ' (PRODUCTION entry)') for r in vul))))
print('    VULNERABLE in a lock whose dir has an image / app class (the EXCEPTION question, as a READ): %s' % (sorted(set('%s %s %s [%s]' % (r['lock'], r['pkg'], r['version'], '; '.join(r['classes'])) for r in vul if r['classes'])) or 'NONE'))
print('    Dockerfiles copying a package manifest: %d | lines naming the WORKSPACE-ROOT lock (Blockchain/Dev/package-lock.json as a bare `package-lock.json` from a context of Blockchain/Dev): READ ONLY — the gate measures' % len(copies))
for x, ls in sorted(copies.items())[:60]: print('      %s: %s' % (x, ' || '.join(ls)[:220]))
ok = nent > 0 and react >= 1 and nons == 0
print('CT-PARSE %d entries across %d lock(s) | CT-POS react found in %d lock(s) | CT-NEG a nonsense package in %d lock(s) -> %s' % (nent, len(locks), react, nons, 'OK' if ok else 'FAIL'))
json.dump(dict(tree=T, locks=locks, rows=rows, ranges=RNG, copies=copies, contexts=ctxs), open(os.path.join(G, 'lockcensus_gate48a.json' if T == P['end_tree'] else 'lockcensus_gate48a.%s.json' % T[:12]), 'w'), indent=1)
print('CENSUS %s: %d lock(s), %d undici/js-yaml entr(y/ies), %d vulnerable' % ('DONE' if ok else 'FAILED', len(locks), len(rows), len(vul)))
raise SystemExit(0 if ok else 1)
