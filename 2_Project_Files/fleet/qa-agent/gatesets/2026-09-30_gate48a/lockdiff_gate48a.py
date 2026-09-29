#!/usr/bin/env python3
"""lockdiff_gate48a.py — the drafter's READ of #1354's lock change (a PREDICTION for LOCK-DIFF-ONE-ENTRY and JSYAML-OUT-OF-RANGE; the gate
re-derives both, and re-runs the regen itself). From the SCRATCH clone (<scratchpad>/g48a_sp/clone), `git show <tree>:systemTest/performance/package-lock.json`
at the BASE (pins develop) and at the HEAD (pins head; or --head <sha> for a control plant):
  L1 both parse; `lockfileVersion` and `name` equal; the top-level keys equal.
  L2 the `packages` map: entries base -> head, ADDED / REMOVED / MOVED (version changed) / OTHER (any entry whose non-version fields changed).
     Exactly ONE entry moves (`node_modules/js-yaml`, 5.2.3 -> 5.4.2) and nothing else changes: ADDED 0, REMOVED 0, OTHER 0.
  L3 inside the moved entry only `version`, `resolved`, `integrity` differ; every other field (funding, license, bin, dependencies, engines…) equal.
  L4 every link entry (`link: true`) and every key naming `secuura-observability` is JSON-equal base vs head, AND its raw text span is byte-equal.
  L5 the moved entry's `resolved` and `integrity` == the npm REGISTRY's own dist.tarball / dist.integrity for js-yaml@5.4.2 (a public GET of
     https://registry.npmjs.org/js-yaml/5.4.2), and the base's == the registry's for 5.2.3 (the control that the comparison can hold).
  L6 JSYAML-OUT-OF-RANGE: the vulnerable range of GHSA-r3ph-w7gj-g6xm READ FROM THE ADVISORY (GitHub advisory API, public GET), evaluated
     for the base pin (must be IN range — the control) and the head pin (must be OUT of range), with a minimal semver comparator.
  L7 the raw text diff: `git diff --numstat` == 3 3 and every changed line sits inside the js-yaml entry.
--offline (controls): skip L5/L6's network reads and say so (NOT MEASURED). --head <sha> (controls): judge that commit instead of the pinned head.
rc 0 LOCKDIFF PASS / rc 1 FAIL. Writes nothing. Usage: lockdiff_gate48a.py <scratchpad> [--head <sha>] [--offline]"""
import json, os, re, subprocess, sys, urllib.request
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate48a.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]; CL = os.path.join(SP, 'g48a_sp', 'clone'); OFF = '--offline' in A
N = K['order'][0]; BASE = P['develop']; HEAD = A[A.index('--head') + 1] if '--head' in A else P['prs'][N]['head']
LOCK = 'systemTest/performance/package-lock.json'; PKG = 'node_modules/js-yaml'; FROM, TO = '5.2.3', '5.4.2'; ADV = 'GHSA-r3ph-w7gj-g6xm'
def git(*a): return subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True, check=True).stdout
bad = []
def chk(tag, ok, msg):
    print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
    if not ok: bad.append(tag)
print('lockdiff_gate48a | %s at base %s and head %s%s' % (LOCK, BASE[:12], HEAD[:12], ' (OFFLINE: L5/L6 not measured)' if OFF else ''))
tb, th = git('show', '%s:%s' % (BASE, LOCK)), git('show', '%s:%s' % (HEAD, LOCK))
b, h = json.loads(tb), json.loads(th)
chk('L1', b.get('lockfileVersion') == h.get('lockfileVersion') and b.get('name') == h.get('name') and sorted(b) == sorted(h),
    'lockfileVersion %s -> %s | name %r -> %r | top-level keys equal: %s' % (b.get('lockfileVersion'), h.get('lockfileVersion'), b.get('name'), h.get('name'), sorted(b) == sorted(h)))
bp, hp = b['packages'], h['packages']
added = sorted(set(hp) - set(bp)); removed = sorted(set(bp) - set(hp)); both = sorted(set(bp) & set(hp))
moved = [k for k in both if bp[k].get('version') != hp[k].get('version')]
other = [k for k in both if {x: y for x, y in bp[k].items() if x not in ('version', 'resolved', 'integrity')} != {x: y for x, y in hp[k].items() if x not in ('version', 'resolved', 'integrity')}
         or (bp[k].get('version') == hp[k].get('version') and bp[k] != hp[k])]
print('    entries %d -> %d | MOVED=%d %s | ADDED=%d %s | REMOVED=%d %s | OTHER (non-version field changes)=%d %s' % (
    len(bp), len(hp), len(moved), ['%s %s -> %s' % (k, bp[k].get('version'), hp[k].get('version')) for k in moved][:6], len(added), added[:6], len(removed), removed[:6], len(other), other[:6]))
chk('L2', moved == [PKG] and not added and not removed and not other and len(bp) == len(hp),
    'exactly ONE entry moves (%s %s -> %s) and nothing else changes' % (PKG, bp.get(PKG, {}).get('version'), hp.get(PKG, {}).get('version')))
chk('L2v', bp.get(PKG, {}).get('version') == FROM and hp.get(PKG, {}).get('version') == TO, '%s version %s -> %s (want %s -> %s)' % (PKG, bp.get(PKG, {}).get('version'), hp.get(PKG, {}).get('version'), FROM, TO))
if PKG in bp and PKG in hp:
    dk = sorted(x for x in set(bp[PKG]) | set(hp[PKG]) if bp[PKG].get(x) != hp[PKG].get(x))
    chk('L3', dk == ['integrity', 'resolved', 'version'], 'fields that differ inside %s: %s (want exactly integrity, resolved, version)' % (PKG, dk))
links = sorted(k for k in set(bp) | set(hp) if (bp.get(k) or {}).get('link') or (hp.get(k) or {}).get('link') or 'secuura-observability' in k)
def span(txt, key):
    i = txt.find('"%s": {' % key)
    if i < 0: return None
    j = txt.find('\n        }', i); return txt[i:j + 10] if j > 0 else None
leq = all(bp.get(k) == hp.get(k) for k in links); seq = all(span(tb, k) == span(th, k) and span(tb, k) is not None for k in links)
chk('L4', bool(links) and leq and seq, '%d link / secuura-observability entr(y/ies) %s: JSON-equal %s, raw text byte-equal %s | e.g. %s' % (
    len(links), links, leq, seq, json.dumps(hp.get(links[0]) if links else None)[:160]))
if OFF: print('NOT MEASURED L5 / L6: --offline (the registry and the advisory API were not read)')
else:
    def reg(v): return json.load(urllib.request.urlopen('https://registry.npmjs.org/js-yaml/%s' % v, timeout=60))['dist']
    rt, rf = reg(TO), reg(FROM)
    chk('L5', hp[PKG].get('resolved') == rt['tarball'] and hp[PKG].get('integrity') == rt['integrity'],
        'head resolved/integrity == registry js-yaml@%s dist (%s, %s…)' % (TO, rt['tarball'], rt['integrity'][:24]))
    chk('L5c', bp[PKG].get('resolved') == rf['tarball'] and bp[PKG].get('integrity') == rf['integrity'],
        'CONTROL: base resolved/integrity == registry js-yaml@%s dist (%s…)' % (FROM, rf['integrity'][:24]))
    a = json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/advisories/' + ADV, headers={'Accept': 'application/vnd.github+json'}), timeout=60))
    rngs = [v.get('vulnerable_version_range') for v in a.get('vulnerabilities', []) if (v.get('package') or {}).get('name') == 'js-yaml']
    fp = [v.get('first_patched_version') for v in a.get('vulnerabilities', []) if (v.get('package') or {}).get('name') == 'js-yaml']
    def V(s): return tuple(int(x) for x in re.findall(r'\d+', s)[:3])
    def inr(ver, rng):
        for c in rng.split(','):
            m = re.match(r'\s*(>=|<=|>|<|=)?\s*([\d.]+)', c); op, x = m.group(1) or '=', V(m.group(2)); v = V(ver)
            if not {'>=': v >= x, '<=': v <= x, '>': v > x, '<': v < x, '=': v == x}[op]: return False
        return True
    print('    advisory %s (%s, published %s): js-yaml range(s) %s | first patched %s' % (ADV, a.get('severity'), a.get('published_at'), rngs, fp))
    chk('L6c', bool(rngs) and any(inr(FROM, r) for r in rngs), 'CONTROL: the base pin %s IS inside %s' % (FROM, rngs))
    HV = hp[PKG].get('version', '?')   # the head's RECORDED pin, never the constant it is expected to be (L2v judges that)
    chk('L6', bool(rngs) and not any(inr(HV, r) for r in rngs), 'the head pin %s is OUTSIDE every vulnerable range %s' % (HV, rngs))
ns = git('diff', '--numstat', BASE, HEAD, '--', LOCK).split()
hunk = git('diff', '-U0', BASE, HEAD, '--', LOCK)
chg = [l for l in hunk.splitlines() if l[:1] in '+-' and not l.startswith(('+++', '---'))]
want = sorted(['-"%s": "%s",' % (f, bp[PKG][f]) for f in ('version', 'resolved', 'integrity')] + ['+"%s": "%s",' % (f, hp[PKG][f]) for f in ('version', 'resolved', 'integrity')])
got = sorted(l[0] + l[1:].strip() for l in chg)
inside = got == want   # the six changed lines are exactly the js-yaml entry's version / resolved / integrity lines, old and new
chk('L7', ns[:2] == ['3', '3'] and len(chg) == 6 and inside, 'git diff --numstat %s | %d changed line(s), all version/resolved/integrity lines of the js-yaml entry: %s' % (' '.join(ns[:2]), len(chg), inside))
print('LOCKDIFF %s: %d FAIL | base %s head %s | sha256 lock base %s head %s' % ('PASS' if not bad else 'FAIL', len(bad), BASE[:12], HEAD[:12],
      __import__('hashlib').sha256(tb.encode()).hexdigest()[:16], __import__('hashlib').sha256(th.encode()).hexdigest()[:16]))
raise SystemExit(1 if bad else 0)
