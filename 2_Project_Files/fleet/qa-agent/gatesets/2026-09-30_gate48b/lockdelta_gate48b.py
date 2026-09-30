#!/usr/bin/env python3
"""lockdelta_gate48b.py — the drafter's READ of #1355's five files (a PREDICTION for LOCK-DELTA-BOTH; the gate re-derives it AND regenerates a
pristine develop itself — the drafter ran no regen). From the SCRATCH clone (<scratchpad>/g48b_sp/clone), `git show` at the BASE (pins develop)
and the HEAD (pins head; or --head <sha> for a control plant):
  M1 each manifest (Blockchain/Dev/package.json, frontend/issuer/package.json): the ONLY difference in the parsed JSON is `overrides.undici`
     ABSENT -> "^7.29.1" (the jsdom-scoped `overrides.jsdom.undici` unchanged); `git diff --numstat` 1 0.
  D1 the ISSUER lock: lockfileVersion / name equal; entries 723 -> 721; the delta set is EXACTLY {MOVED node_modules/undici 5.29.0 -> 7.30.0,
     REMOVED node_modules/@fastify/busboy 2.1.1, REMOVED node_modules/jsdom/node_modules/undici 7.30.0} and NOTHING else.
  D2 the ROOT lock: entries 1970 -> 1968; the same three, PLUS the drift set: entries whose ONLY changed fields are `dev` / `devOptional`, every one
     named lightningcss-* or magicast, 12 in all (the seat's npm-drift attribution is by a pristine regen — the GATE's to re-derive; the drafter
     only reads that the 12 exist, are flag-only and are named as claimed). Any OTHER change is a FAIL.
  D3 inside node_modules/undici only version / resolved / integrity / engines / dependencies differ, and `dependencies` loses exactly
     @fastify/busboy; `engines.node` is printed (the builder's node is read from the issuer Dockerfile's FROM lines).
  D4 undici 7.30.0 `resolved` / `integrity` in BOTH locks == the npm registry's dist for 7.30.0 (public GET); CONTROL: 7.29.1's integrity
     compared the same way reads False.
  D5 ADVISORY RANGES READ (GitHub advisory API, public GETs): GHSA-r53p AND every undici row of audit-baseline.json at develop (the 12
     grandfathered siblings): 7.30.0 OUTSIDE each, 5.29.0 INSIDE each (the control). js-yaml GHSA-r3ph: 5.4.2 outside, 5.2.3 inside.
  D6 systemTest/performance/package-lock.json: the head blob == #1354's head blob == kit.json jsyaml_blob_1354; develop's blob differs
     (the control that makes the equality informative); js-yaml 5.2.3 -> 5.4.2 is its only moved entry.
  D7 THE RESOLVER (the seat's NOT-RUN rationale, SUITES): in each lock at base and head, node's resolution walk for `undici` from every
     `jsdom` entry and from every `@connectrpc/connect-node` entry: the version each resolves to, and the declared range of each dependant.
     The seat: jsdom -> 7.30.0 on BOTH sides; connect-node 5.29.0 -> 7.30.0 (a MAJOR against its declared ^5.28.3).
--offline (controls): skip D4/D5's network reads and say so (NOT MEASURED). --head <sha> (controls): judge that commit instead of the pinned head.
rc 0 LOCKDELTA PASS / rc 1 FAIL. Writes nothing. Usage: lockdelta_gate48b.py <scratchpad> [--head <sha>] [--offline]"""
import json, os, re, subprocess, sys, urllib.request, hashlib, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate48b.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g48b_sp', 'clone'); OFF = '--offline' in A
N = '1355'; BASE = P['develop']; HEAD = A[A.index('--head') + 1] if '--head' in A else P['prs'][N]['head']
ROOT, ISS, PERF = 'Blockchain/Dev/package-lock.json', 'Blockchain/Dev/frontend/issuer/package-lock.json', 'systemTest/performance/package-lock.json'
MANS = ['Blockchain/Dev/package.json', 'Blockchain/Dev/frontend/issuer/package.json']
U, BB, JU = 'node_modules/undici', 'node_modules/@fastify/busboy', 'node_modules/jsdom/node_modules/undici'
def git(*a, ok=(0,)):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if r.returncode not in ok: raise SystemExit('REFUSING: git %s rc %d %s' % (' '.join(a[:3]), r.returncode, r.stderr[:200]))
    return r.stdout
bad = []
def chk(tag, ok, msg):
    print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
    if not ok: bad.append(tag)
print('lockdelta_gate48b %s | 5 files at base %s and head %s%s' % (datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), BASE[:12], HEAD[:12], ' (OFFLINE: D4/D5 not measured)' if OFF else ''))
def J(t, p): return json.loads(git('show', '%s:%s' % (t, p)))
for mf in MANS:
    b, h = J(BASE, mf), J(HEAD, mf)
    diffs = sorted(k for k in set(b) | set(h) if b.get(k) != h.get(k))
    ob, oh = dict(b.get('overrides') or {}), dict(h.get('overrides') or {})
    od = sorted(k for k in set(ob) | set(oh) if ob.get(k) != oh.get(k))
    ns = git('diff', '--numstat', BASE, HEAD, '--', mf).split()[:2]
    chk('M1 ' + mf.split('/')[-2], diffs == ['overrides'] and od == ['undici'] and 'undici' not in ob and oh.get('undici') == '^7.29.1' and ob.get('jsdom') == oh.get('jsdom') and ns == ['1', '0'],
        'top-level keys that differ %s | overrides keys that differ %s | undici %r -> %r | jsdom-scoped %r unchanged: %s | numstat %s' % (
            diffs, od, ob.get('undici'), oh.get('undici'), oh.get('jsdom'), ob.get('jsdom') == oh.get('jsdom'), ' '.join(ns)))
def delta(p):
    b, h = J(BASE, p), J(HEAD, p); bp, hp = b['packages'], h['packages']
    add = sorted(set(hp) - set(bp)); rem = sorted(set(bp) - set(hp)); chg = {}
    for k in sorted(set(bp) & set(hp)):
        if bp[k] != hp[k]: chg[k] = sorted(x for x in set(bp[k]) | set(hp[k]) if bp[k].get(x) != hp[k].get(x))
    return b, h, bp, hp, add, rem, chg
UFIELDS = ['dependencies', 'engines', 'integrity', 'resolved', 'version']
for tag, p, n0, n1 in (('D1', ISS, 723, 721), ('D2', ROOT, 1970, 1968)):
    b, h, bp, hp, add, rem, chg = delta(p)
    drift = sorted(k for k, f in chg.items() if k != U and set(f) <= {'dev', 'devOptional'})
    other = sorted(k for k in chg if k != U and k not in drift)
    print('    %s %s: lockfileVersion %s -> %s | entries %d -> %d | ADDED %s | REMOVED %s | CHANGED %d: undici %s, flag-only %d, other %s' % (
        tag, p, b.get('lockfileVersion'), h.get('lockfileVersion'), len(bp), len(hp), add or 'none', ['%s %s' % (k, bp[k].get('version')) for k in rem], len(chg), chg.get(U), len(drift), other or 'none'))
    core = (not add and rem == sorted([BB, JU]) and U in chg and not other and b.get('lockfileVersion') == h.get('lockfileVersion') and b.get('name') == h.get('name')
            and len(bp) == n0 and len(hp) == n1 and bp[U].get('version') == '5.29.0' and hp[U].get('version') == '7.30.0' and bp[BB].get('version') == '2.1.1' and bp[JU].get('version') == '7.30.0')
    if tag == 'D1':
        chk(tag, core and not drift, 'issuer: exactly {undici 5.29.0 -> 7.30.0, -@fastify/busboy 2.1.1, -jsdom nested undici 7.30.0}, %d -> %d, nothing else (flag-only %d)' % (len(bp), len(hp), len(drift)))
    else:
        dn = all(re.fullmatch(r'node_modules/(lightningcss-[a-z0-9-]+|magicast)', k) for k in drift)
        print('    D2 drift set (flag-only): %s' % ' '.join('%s[%s]' % (k.split('/')[-1], ','.join('%s %s->%s' % (f, bp[k].get(f), hp[k].get(f)) for f in chg[k])) for k in drift))
        chk(tag, core and len(drift) == 12 and dn and sum('lightningcss' in k for k in drift) == 11, 'root: the same 3 undici entries + exactly 12 flag-only entries (11 lightningcss-* + magicast): %d, names as claimed %s — attribution to npm is the GATE\'s pristine regen' % (len(drift), dn))
    f = chg.get(U, [])
    dep = (bp.get(U, {}).get('dependencies'), hp.get(U, {}).get('dependencies'))
    chk('D3 ' + tag, sorted(f) == UFIELDS and dep == ({'@fastify/busboy': '^2.0.0'}, None), 'fields changed inside %s: %s | dependencies %s -> %s | engines %s -> %s' % (U, f, dep[0], dep[1], bp.get(U, {}).get('engines'), hp.get(U, {}).get('engines')))
    globals()['HP_' + tag] = hp; globals()['BP_' + tag] = bp
fr = [l.strip() for l in git('show', '%s:Blockchain/Dev/frontend/issuer/Dockerfile' % HEAD).splitlines() if re.match(r'\s*FROM\b', l, re.I)]
print('INFO issuer Dockerfile FROM lines at head: %s (undici 7.30.0 engines %s)' % (fr, HP_D1.get(U, {}).get('engines')))
def _tok():   # the Secuura GH_TOKEN, read by NAME and never printed: an authenticated GET of the PUBLIC advisory API (5000/h, not 60/h per IP)
    try:
        for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
            if l.startswith('GH_TOKEN='): return l.split('=', 1)[1].strip().strip('"').strip("'")
    except OSError: pass
    return ''
_T = _tok()
def ADVGET(g): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/advisories/' + g, headers=dict({'Accept': 'application/vnd.github+json'}, **({'Authorization': 'Bearer ' + _T} if _T else {}))), timeout=60))
def V(s): return tuple(int(x) for x in re.findall(r'\d+', s)[:3])
def inr(ver, rng):
    for c in rng.split(','):
        m = re.match(r'\s*(>=|<=|>|<|=)?\s*([\d.]+)', c); op, x = m.group(1) or '=', V(m.group(2)); v = V(ver)
        if not {'>=': v >= x, '<=': v <= x, '>': v > x, '<': v < x, '=': v == x}[op]: return False
    return True
if OFF: print('NOT MEASURED D4 / D5: --offline (the registry and the advisory API were not read)')
else:
    def reg(pk, v): return json.load(urllib.request.urlopen('https://registry.npmjs.org/%s/%s' % (pk, v), timeout=60))['dist']
    r730, r7291 = reg('undici', '7.30.0'), reg('undici', '7.29.1')
    for tag, hp in (('issuer', HP_D1), ('root', HP_D2)):
        e = hp.get(U, {})
        chk('D4 ' + tag, e.get('resolved') == r730['tarball'] and e.get('integrity') == r730['integrity'], '%s lock undici resolved/integrity == registry undici@7.30.0 dist (%s, %s…)' % (tag, r730['tarball'], r730['integrity'][:22]))
        chk('D4c ' + tag, e.get('integrity') != r7291['integrity'], 'CONTROL: the same comparison against undici@7.29.1\'s integrity (%s…) reads %s' % (r7291['integrity'][:22], e.get('integrity') == r7291['integrity']))
    bl = J(BASE, 'Blockchain/Dev/scripts/audit/audit-baseline.json')['accepted']
    ids = ['GHSA-r53p-7pc4-xj5r'] + sorted(k for k, v in bl.items() if v.get('package') == 'undici')
    out_all = True; ctl_all = True
    for g in ids:
        a = ADVGET(g)
        rng = [v.get('vulnerable_version_range') for v in a.get('vulnerabilities', []) if (v.get('package') or {}).get('name') == 'undici']
        o = bool(rng) and not any(inr('7.30.0', r) for r in rng); c = any(inr('5.29.0', r) for r in rng); out_all &= o; ctl_all &= c
        row = bl.get(g) or {}
        print('    %s %-8s %s | row %s %s expires %s | undici ranges %s | 7.30.0 outside: %s | 5.29.0 inside (control): %s' % (g, a.get('severity'), 'NEW (not in the baseline)' if not row else 'baseline', row.get('ticket', '-'), '', row.get('expires', '(none)'), rng, o, c))
    chk('D5', out_all and ctl_all, '7.30.0 OUTSIDE all %d undici advisory ranges read (r53p + %d baseline rows); 5.29.0 INSIDE each (control)' % (len(ids), len(ids) - 1))
    a = ADVGET('GHSA-r3ph-w7gj-g6xm')
    rj = [v.get('vulnerable_version_range') for v in a.get('vulnerabilities', []) if (v.get('package') or {}).get('name') == 'js-yaml']
    chk('D5j', bool(rj) and not any(inr('5.4.2', r) for r in rj) and any(inr('5.2.3', r) for r in rj), 'GHSA-r3ph js-yaml %s: 5.4.2 outside, 5.2.3 inside (control)' % rj)
hb, bb, rb = git('rev-parse', '%s:%s' % (HEAD, PERF)).strip(), git('rev-parse', '%s:%s' % (BASE, PERF)).strip(), git('rev-parse', 'refs/remotes/pr/1354:%s' % PERF, ok=(0, 128)).strip()
pb, ph = J(BASE, PERF)['packages'], J(HEAD, PERF)['packages']
mv = sorted(k for k in set(pb) | set(ph) if pb.get(k) != ph.get(k))
chk('D6', hb == K['jsyaml_blob_1354'] == rb and bb != hb and mv == ['node_modules/js-yaml'] and ph['node_modules/js-yaml']['version'] == '5.4.2',
    'performance lock blob head %s == #1354 head %s == kit %s: %s | develop %s differs (control): %s | entries changed %s (%s -> %s)' % (
        hb[:12], rb[:12], K['jsyaml_blob_1354'][:12], hb == rb == K['jsyaml_blob_1354'], bb[:12], bb != hb, mv, pb['node_modules/js-yaml']['version'], ph['node_modules/js-yaml']['version']))
def resolve(pk, frm, name):
    parts = frm.split('node_modules/')
    for i in range(len(parts), 0, -1):
        cand = 'node_modules/'.join(parts[:i]).rstrip('/')
        key = (cand + '/node_modules/' + name) if cand else 'node_modules/' + name
        if key in pk and not pk[key].get('link'): return key, pk[key].get('version')
    return None, None
print('D7 THE RESOLVER — undici as node would resolve it from each dependant (key -> resolved entry version)')
for tag, lk in (('issuer', ISS), ('root', ROOT)):
    for side, t in (('develop', BASE), ('head', HEAD)):
        pk = J(t, lk)['packages']
        for dep in ('jsdom', '@connectrpc/connect-node'):
            srcs = sorted(k for k in pk if k.endswith('node_modules/' + dep))
            rs = ['%s(declares %s) -> %s' % (s, (pk[s].get('dependencies') or {}).get('undici'), '%s %s' % resolve(pk, s, 'undici')) for s in srcs]
            print('    %-6s %-7s %-26s %d entr(y/ies): %s' % (tag, side, dep, len(srcs), ' ; '.join(rs)))
print('LOCKDELTA %s: %d FAIL | base %s head %s | root %s -> %s | issuer %s -> %s' % ('PASS' if not bad else 'FAIL', len(bad), BASE[:12], HEAD[:12], len(BP_D2), len(HP_D2), len(BP_D1), len(HP_D1)))
raise SystemExit(1 if bad else 0)
