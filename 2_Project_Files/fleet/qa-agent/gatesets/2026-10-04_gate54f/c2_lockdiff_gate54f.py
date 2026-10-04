#!/usr/bin/env python3
"""c2_lockdiff_gate54f.py — gate54f C2: the three lockfiles, diffed ENTRY BY ENTRY and FIELD BY FIELD as parsed JSON, plus a text-level
diff, base blob vs head blob, read from SHAs with read-only git verbs (no install, no network, no working tree).

Per lock (kit.json `locks`):
  L1 entries: changed == [kit bump_key] exactly; ADDED 0; REMOVED 0; every top-level key other than `packages` equal.
  L2 fields of the one changed entry: changed fields subset of allowed_changed_fields (version/resolved/integrity); added fields subset of
     allowed_added_fields (root only: resolved/integrity, because the base root entry carries ONLY version + license); removed fields 0;
     head version == kit to_version; head resolved / integrity == kit's 4.3.0 values WHEN PRESENT (C3 recomputes them from the tarball).
  L3 collateral: flag flips (dev / optional / devOptional / peer) across EVERY entry 0; libc: count of entries carrying `libc` == base ==
     kit libc_base, and every libc array value-equal to base.
  L4 kit untouched_key (@types/http-cache-semantics): value-equal AND raw text block byte-identical.
  L5 text: every changed line lies inside the bump entry's block (base and head line ranges); printed as -n/+n.
Verdict line: `LOCKDIFF PASS|FAIL: <n> FAIL of <m> checks | base <sha12> head <sha12>` then one `CHANGED-ENTRIES <lock> <n>` line per lock.

--selftest  runs the SAME check function over in-memory plants built from the BASE blobs (no repo write):
  T0 base vs base           -> must FAIL with 0 changed entries on every lock (the "0 changed" reading)
  T1 the legitimate bump    -> must PASS (service: 3 field lines replaced; root: version replaced + resolved/integrity inserted)
  T2 T1 + a dev flip        -> must FAIL and report flips 1 (planted `"dev": true` on another entry)
  T3 T1 + a libc removal    -> must FAIL and report libc 10 -> 9 (service locks)
  T4 T1 + @types touched    -> must FAIL on L1 (changed 2) and L4
  T5 T1 + an added entry    -> must FAIL on L1 (ADDED 1)
  rc 0 only if EVERY arm returns its expected verdict AND names the expected collateral.

Usage: c2_lockdiff_gate54f.py --repo <your clone> --base <sha> --head <sha>
       c2_lockdiff_gate54f.py --repo <any clone holding the base> --selftest
rc 0 PASS / rc 1 FAIL / rc 2 usage."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate54f import K, git, commit, show, block, find_member, member_span, opcodes, now, Checks

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
REPO = opt('--repo'); BUMP = K['bump_key']; UNT = K['untouched_key']; FL = K['flag_fields']; TO = K['to_version']


def check_lock(C, path, bt, ht, quiet=False):
    """returns dict of measured facts; records checks into C"""
    cfg = K['locks'][path]; lb, lh = json.loads(bt), json.loads(ht); pb, ph = lb['packages'], lh['packages']
    add = sorted(set(ph) - set(pb)); rem = sorted(set(pb) - set(ph)); both = set(pb) & set(ph)
    chg = sorted(k for k in both if pb[k] != ph[k])
    tk = sorted(k for k in set(lb) | set(lh) if k != 'packages' and lb.get(k) != lh.get(k))
    tag = path.replace('Blockchain/Dev/', '')
    print('INFO %s entries %d -> %d | ADDED %d %s | REMOVED %d %s | CHANGED %d %s' % (tag, len(pb), len(ph), len(add), add[:3], len(rem), rem[:3], len(chg), chg[:4]))
    C.chk('L1 %s entries' % tag, chg == [BUMP] and not add and not rem and not tk,
          'changed %s (want [%s]) | added %d | removed %d | top-level keys other than packages that differ: %s' % (chg, BUMP, len(add), len(rem), tk or 'NONE'))
    fb, fh = pb.get(BUMP, {}), ph.get(BUMP, {})
    fchg = sorted(f for f in set(fb) & set(fh) if fb[f] != fh[f]); fadd = sorted(set(fh) - set(fb)); frem = sorted(set(fb) - set(fh))
    okf = (set(fchg) <= set(cfg['allowed_changed_fields']) and set(fadd) <= set(cfg['allowed_added_fields']) and not frem and fh.get('version') == TO
           and (fh.get('resolved') is None or fh.get('resolved') == K['resolved'][TO]) and (fh.get('integrity') is None or fh.get('integrity') == K['integrity'][TO]))
    C.chk('L2 %s fields' % tag, okf,
          '%s: changed fields %s | ADDED fields %s (allowed %s) | removed fields %s | version %s -> %s | resolved %s | integrity %s' % (
              BUMP, fchg, fadd, cfg['allowed_added_fields'], frem, fb.get('version'), fh.get('version'),
              'ABSENT' if fh.get('resolved') is None else ('== kit %s' % TO if fh.get('resolved') == K['resolved'][TO] else 'OTHER %s' % fh.get('resolved')),
              'ABSENT' if fh.get('integrity') is None else ('== kit %s' % TO if fh.get('integrity') == K['integrity'][TO] else 'OTHER %s' % fh.get('integrity')[:24])))
    if 'resolved' in fh and 'license' in fh:   # INFO, never a check: npm's own field order, read from the same base lock (README D1)
        maj = [list(v).index('resolved') < list(v).index('license') for k, v in pb.items() if k != BUMP and 'resolved' in v and 'license' in v]
        print('INFO L6 %s field order at head %s | resolved %s license | the base lock\'s other entries carrying both: resolved BEFORE license %d, AFTER %d%s' % (
            tag, list(fh), 'before' if list(fh).index('resolved') < list(fh).index('license') else 'AFTER', maj.count(True), maj.count(False),
            '  <- NOT the order npm writes in this lock: a hand edit? (D1, the gate rules METHOD-STATED)' if list(fh).index('resolved') > list(fh).index('license') and maj.count(True) > maj.count(False) else ''))
    flips = sorted(k for k in both if any(pb[k].get(f) != ph[k].get(f) for f in FL))
    lcb = sorted(k for k in pb if 'libc' in pb[k]); lch = sorted(k for k in ph if 'libc' in ph[k])
    lneq = sorted(k for k in set(lcb) | set(lch) if pb.get(k, {}).get('libc') != ph.get(k, {}).get('libc'))
    C.chk('L3 %s collateral' % tag, not flips and len(lcb) == len(lch) == cfg['libc_base'] and not lneq,
          'flag flips (%s) %d %s | libc entries %d -> %d (kit base %d) | libc arrays not equal to base %d %s' % (
              '/'.join(FL), len(flips), flips[:3], len(lcb), len(lch), cfg['libc_base'], len(lneq), lneq[:3]))
    ub, uh = block(bt, UNT), block(ht, UNT)
    C.chk('L4 %s %s' % (tag, UNT), pb.get(UNT) == ph.get(UNT) and ub is not None and ub == uh,
          'value-equal %s | raw block byte-identical %s (%s bytes) | version %s' % (pb.get(UNT) == ph.get(UNT), ub is not None and ub == uh, len(uh or ''), ph.get(UNT, {}).get('version')))
    bl, hl = bt.split('\n'), ht.split('\n'); ib, ih = find_member(bl, BUMP), find_member(hl, BUMP)
    sb = member_span(bl, ib) if ib is not None else None; sh = member_span(hl, ih) if ih is not None else None
    ops = opcodes(bt, ht); outside = []
    for o in ops:
        okb = sb is not None and (o[1] == o[2] or (sb[0] <= o[1] and o[2] - 1 <= sb[1]))
        okh = sh is not None and (o[3] == o[4] or (sh[0] <= o[3] and o[4] - 1 <= sh[1]))
        if not (okb and okh): outside.append(o)
    mi = sum(o[2] - o[1] for o in ops); pl = sum(o[4] - o[3] for o in ops)
    C.chk('L5 %s text' % tag, not outside and bool(ops) == bool(chg),
          '%d hunk(s), -%d/+%d line(s) | hunks outside the %s block: %d %s | base block lines %s, head block lines %s' % (
              len(ops), mi, pl, BUMP, len(outside), [o[:5] for o in outside[:2]], sb and (sb[0] + 1, sb[1] + 1), sh and (sh[0] + 1, sh[1] + 1)))
    return {'changed': len(chg), 'added': len(add), 'removed': len(rem), 'flips': len(flips), 'libc': (len(lcb), len(lch)), 'minus': mi, 'plus': pl}


def run(pairs):
    C = Checks(); facts = {}
    for path in sorted(K['locks']):
        bt, ht = pairs[path]
        if bt is None or ht is None:
            C.chk('L0 %s present' % path, False, 'blob missing at base %s / head %s' % (bt is None, ht is None)); continue
        facts[path] = check_lock(C, path, bt, ht)
    return C, facts


# ---------- plants (in memory, from the base text) ----------
def set_field(lines, i0, i1, field, value):
    for j in range(i0, i1 + 1):
        s = lines[j]
        if s.strip().startswith('"%s":' % field):
            lines[j] = s[:s.index('"%s":' % field)] + '"%s": %s%s' % (field, json.dumps(value), ',' if s.rstrip().endswith(',') else ''); return True
    return False


def plant_bump(text, path):
    ls = text.split('\n'); i = find_member(ls, BUMP); a, b = member_span(ls, i)
    set_field(ls, a, b, 'version', TO)
    if not set_field(ls, a, b, 'resolved', K['resolved'][TO]):   # the stripped root entry: insert after version, as npm writes it
        vi = [j for j in range(a, b + 1) if ls[j].strip().startswith('"version":')][0]; ind = ls[vi][:len(ls[vi]) - len(ls[vi].lstrip())]
        ls[vi + 1:vi + 1] = ['%s"resolved": %s,' % (ind, json.dumps(K['resolved'][TO])), '%s"integrity": %s,' % (ind, json.dumps(K['integrity'][TO]))]
    else:
        set_field(ls, a, b, 'integrity', K['integrity'][TO])
    return '\n'.join(ls)


def plant_devflip(text):
    ls = text.split('\n'); d = json.loads(text)['packages']
    k = next(k for k in sorted(d) if k and k not in (BUMP, UNT) and 'dev' not in d[k] and 'version' in d[k])
    i = find_member(ls, k); vi = next(j for j in range(i, i + 6) if ls[j].strip().startswith('"version":'))
    ind = ls[vi][:len(ls[vi]) - len(ls[vi].lstrip())]; ls[vi + 1:vi + 1] = ['%s"dev": true,' % ind]
    return '\n'.join(ls), k


def plant_libc_removal(text):
    ls = text.split('\n'); st = [j for j, l in enumerate(ls) if l.strip() == '"libc": [']
    if not st: return None, None
    a, b = member_span(ls, st[0])
    if not ls[b].rstrip().endswith(','): ls[a - 1] = ls[a - 1].rstrip().rstrip(',')
    owner = next(ls[j].strip().split('"')[1] for j in range(a, -1, -1) if ls[j].strip().endswith('{') and ls[j].strip().startswith('"node_modules/'))
    del ls[a:b + 1]
    return '\n'.join(ls), owner


def plant_types(text):
    ls = text.split('\n'); i = find_member(ls, UNT); a, b = member_span(ls, i); set_field(ls, a, b, 'version', '4.2.1'); return '\n'.join(ls)


def plant_added(text):
    ls = text.split('\n'); i = find_member(ls, BUMP); ind = ls[i][:len(ls[i]) - len(ls[i].lstrip())]
    ls[i:i] = ['%s"node_modules/zz-gate54f-planted": {' % ind, '%s  "version": "0.0.1"' % ind, '%s},' % ind]; return '\n'.join(ls)


if '--selftest' in A:
    B = commit(REPO, K['base'])
    print('c2_lockdiff_gate54f SELFTEST %s | repo %s | base %s (every plant built in memory from the base blobs; nothing written)' % (now(), REPO, B[:12]))
    base = {p: show(REPO, B, p) for p in K['locks']}
    T1 = {p: plant_bump(base[p], p) for p in base}
    arms = []
    def arm(name, pairs, want_pass, expect):
        print('\n=== ARM %s (expected %s) ===' % (name, 'PASS' if want_pass else 'FAIL'))
        C, f = run(pairs); got = C.nfail() == 0; ex_ok = expect(f)
        print('ARM %s: verdict %s (expected %s) | named collateral %s -> %s' % (name, 'PASS' if got else 'FAIL', 'PASS' if want_pass else 'FAIL', 'as expected' if ex_ok else 'NOT as expected', 'OK' if (got == want_pass and ex_ok) else 'MISMATCH'))
        for p in sorted(f): print('  CHANGED-ENTRIES %s %d | added %d | removed %d | flips %d | libc %d -> %d | text -%d/+%d' % (p, f[p]['changed'], f[p]['added'], f[p]['removed'], f[p]['flips'], f[p]['libc'][0], f[p]['libc'][1], f[p]['minus'], f[p]['plus']))
        arms.append(got == want_pass and ex_ok)
    arm('T0 base-vs-base', {p: (base[p], base[p]) for p in base}, False, lambda f: all(f[p]['changed'] == 0 for p in f))
    arm('T1 legitimate bump', {p: (base[p], T1[p]) for p in base}, True,
        lambda f: all(f[p]['changed'] == 1 for p in f) and f['Blockchain/Dev/package-lock.json']['plus'] == 3 and all(f[p]['minus'] == f[p]['plus'] == 3 for p in f if 'services/' in p))
    dv = {}; T2 = {}
    for p in base: T2[p], dv[p] = plant_devflip(T1[p])
    print('\n(T2 plants `"dev": true` on: %s)' % json.dumps(dv))
    arm('T2 bump + dev flip', {p: (base[p], T2[p]) for p in base}, False, lambda f: all(f[p]['flips'] == 1 for p in f))
    T3 = dict(T1); own = {}
    for p in base:
        if K['locks'][p]['libc_base']: T3[p], own[p] = plant_libc_removal(T1[p])
    print('\n(T3 removes one libc array from: %s)' % json.dumps(own))
    arm('T3 bump + libc removal', {p: (base[p], T3[p]) for p in base}, False,
        lambda f: all(f[p]['libc'] == (10, 9) for p in f if K['locks'][p]['libc_base']) and f['Blockchain/Dev/package-lock.json']['libc'] == (0, 0))
    arm('T4 bump + @types touched', {p: (base[p], plant_types(T1[p])) for p in base}, False, lambda f: all(f[p]['changed'] == 2 for p in f))
    arm('T5 bump + an added entry', {p: (base[p], plant_added(T1[p])) for p in base}, False, lambda f: all(f[p]['added'] == 1 for p in f))
    n = arms.count(False)
    print('\nSELFTEST %s: %d of %d arms returned their expected verdict and collateral' % ('OK' if n == 0 else 'MISMATCH', len(arms) - n, len(arms)))
    raise SystemExit(1 if n else 0)

B = commit(REPO, opt('--base', K['base'])); H = commit(REPO, opt('--head') or sys.exit('--head <sha> is required (or --selftest)'))
print('c2_lockdiff_gate54f %s | repo %s | base %s | head %s' % (now(), REPO, B, H))
C, f = run({p: (show(REPO, B, p), show(REPO, H, p)) for p in K['locks']})
n = C.nfail()
print('LOCKDIFF %s: %d FAIL of %d checks | base %s head %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), B[:12], H[:12]))
for p in sorted(f): print('CHANGED-ENTRIES %s %d | added %d | removed %d | flips %d | libc %d -> %d | text -%d/+%d' % (p, f[p]['changed'], f[p]['added'], f[p]['removed'], f[p]['flips'], f[p]['libc'][0], f[p]['libc'][1], f[p]['minus'], f[p]['plus']))
raise SystemExit(1 if n else 0)
