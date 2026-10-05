#!/usr/bin/env python3
"""c2_lockdiff_gate58.py — gate58 C2: the SIX lockfiles, base blob vs head blob, read from SHAs with read-only git verbs (no install, no
network, no working tree), diffed SEMANTICALLY (parsed JSON, entry by entry, field by field) AND by LINE (the raw text). B 56th's lesson:
a semantic differ and a line differ answer different questions (a `libc` array moved to the end of its entry is value-equal and
line-different), so BOTH run and both must pass.

Per lock (kit.json `locks`; 23 ruled entries in all: root 5, admin 3, outlook-addin 4, verifier 3, governance 4, referral 4):
  L1 entries: the CHANGED set == exactly the lock's kit expected_changes keys; ADDED 0; REMOVED 0; entry count equal; every top-level key
     other than `packages` equal (lockfileVersion, name, requires, ...).
  L2 fields of each ruled entry: version base == kit from AND head == kit to; changed fields subset of allowed (version / resolved /
     integrity / dependencies — dependencies only on browserslist); ADDED fields only resolved + integrity and only in the ROOT lock (its
     base entries are stripped); REMOVED fields 0; head resolved AND integrity PRESENT and == the kit's registry values for the new version
     (C3 recomputes those from the tarball); browserslist's head dependencies map == 4.28.7's declared map exactly (kit).
  L3 collateral across EVERY entry: flag flips (dev / optional / devOptional / peer) 0; libc / os / cpu: the number of entries carrying
     each == base == kit, and every such array value-equal to base.
  L4 KEY ORDER of each ruled entry at head == its base order, with resolved + integrity inserted IMMEDIATELY after `version` where they
     were added (npm's own order; Q-ROOT). INFO: lock-wide, how many entries carry both and how many of those use that order (base, head).
  L5 dependency maps ALPHABETICAL in every ruled entry at head (npm writes them sorted); INFO: lock-wide count of non-alphabetical maps at
     base (the control that npm's own entries are sorted).
  L6 LINE: every changed line (difflib opcodes, base text vs head text) lies inside a ruled entry's block, base AND head line ranges;
     -n/+n printed per lock. A hunk outside the ruled blocks is collateral even when the parsed values are equal.
  L7 RESOLVABILITY (an `npm ls` stand-in, no install): every entry's dependencies / peerDependencies / optionalDependencies on a kit
     dep_family package resolve node-style (nested node_modules, then up) to a version that satisfies the declared range; unsatisfied
     at head 0 (base count printed: the instrument reads the same predicate at both sides). A range this reader cannot parse is UNPARSED,
     never satisfied.
  L8 RECONSTRUCTION (strict): the kit's OWN surgical edit of the BASE text (kit values only, never the head) == the head text, byte for
     byte. Independent of the builder's tooling; a mismatch prints the first differing line.
Verdict line: `LOCKDIFF PASS|FAIL: <n> FAIL of <m> checks | base <sha12> head <sha12>` then one `CHANGED-ENTRIES <lock> <n>` line per lock.

--selftest runs the SAME check function over in-memory plants built from the BASE blobs (nothing written):
  T0 base vs base                         -> FAIL, 0 changed entries on every lock
  T1 the legitimate bump (reconstruction) -> PASS on every check
  T2 T1 + a dev flip                       -> FAIL L3, flips 1 per lock
  T3 T1 + one libc array removed (referral)-> FAIL L3, libc 10 -> 9
  T4 T1 + one libc array MOVED to its entry's end (value-equal) -> semantic L1-L3 PASS, L6 LINE FAIL (the B 56th catch)
  T5 T1 + an extra entry changed (update-browserslist-db) -> FAIL L1
  T6 T1 + an added entry                   -> FAIL L1, added 1
  T7 T1 with the root's resolved+integrity AFTER `license` (the #1373 shape) -> FAIL L4 on the root lock only
  T8 T1 + browserslist's dependencies map un-sorted (same values) -> FAIL L5 (L2 value-equal)
  T9 browserslist ONLY (no data packages)  -> FAIL L1 and L7 (governance: 3 unsatisfied — the P10 `npm ls` control, re-derived)
  T10 T1 + one os array element changed   -> FAIL L3
  T11 T1 + caniuse-lite carrying the OLD version's integrity -> FAIL L2
  rc 0 only if EVERY arm returns its expected verdict AND names the expected check.

Usage: c2_lockdiff_gate58.py --repo <your clone> --base <sha> --head <sha>
       c2_lockdiff_gate58.py --repo <any clone holding the base> --selftest
rc 0 PASS / rc 1 FAIL / rc 2 usage."""
import json, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate58 import K, commit, show, find_member, member_span, opcodes, now, Checks, satisfies, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
REPO = opt('--repo'); FL = K['flag_fields']; AR = K['arch_fields']; PK = K['packages']; BLD = K['browserslist_427_dependencies']; FAM = set(K['dep_family'])
ROOT = 'Blockchain/Dev/package-lock.json'
name_of = lambda key: key.rsplit('node_modules/', 1)[-1]


def resolve(pk, frm, dep):
    """node-style resolution of `dep` required by entry key `frm`: <frm>/node_modules/<dep>, then each ancestor, then the top"""
    base = frm
    while True:
        cand = (base + '/node_modules/' + dep) if base else ('node_modules/' + dep)
        if cand in pk: return cand
        if not base: return None
        i = base.rfind('/node_modules/')
        base = base[:i] if i >= 0 else ''


def unsatisfied(pk):
    bad = []; unp = []
    for k, v in pk.items():
        for fld in ('dependencies', 'peerDependencies', 'optionalDependencies'):
            for d, rng in (v.get(fld) or {}).items():
                if d not in FAM: continue
                r = resolve(pk, k, d)
                if r is None:
                    if fld == 'dependencies': bad.append((k or '(root)', d, rng, 'MISSING'))
                    continue
                s = satisfies(pk[r].get('version', ''), rng)
                if s is None: unp.append((k or '(root)', d, rng, pk[r].get('version')))
                elif not s: bad.append((k or '(root)', d, rng, pk[r].get('version')))
    return bad, unp


def check_lock(C, path, bt, ht):
    cfg = K['locks'][path]; EXP = cfg['expected_changes']; lb, lh = json.loads(bt), json.loads(ht); pb, ph = lb['packages'], lh['packages']
    add = sorted(set(ph) - set(pb)); rem = sorted(set(pb) - set(ph)); both = set(pb) & set(ph)
    chg = sorted(k for k in both if pb[k] != ph[k]); want = sorted(EXP)
    tk = sorted(k for k in set(lb) | set(lh) if k != 'packages' and lb.get(k) != lh.get(k))
    tag = path.replace('Blockchain/Dev/', '')
    C.chk('L1 %s entries' % tag, chg == want and not add and not rem and not tk and len(pb) == len(ph),
          'entries %d -> %d | changed %d %s | want %d | UNRULED changed %s | ruled but UNCHANGED %s | added %d %s | removed %d %s | other top-level keys differing %s' % (
              len(pb), len(ph), len(chg), [name_of(k) for k in chg], len(want), sorted(set(chg) - set(want)) or 'NONE', sorted(set(want) - set(chg)) or 'NONE',
              len(add), add[:3], len(rem), rem[:3], tk or 'NONE'))
    # L2
    l2 = []
    for k in want:
        n = name_of(k); fb, fh = pb.get(k, {}), ph.get(k, {}); P = PK[n]; to = P['to']
        fchg = sorted(f for f in set(fb) & set(fh) if fb[f] != fh[f]); fadd = sorted(set(fh) - set(fb)); frem = sorted(set(fb) - set(fh))
        allow_c = set(cfg['allowed_changed_fields']) - ({'dependencies'} if n != 'browserslist' else set())
        bad = []
        if fb.get('version') != EXP[k]['from']: bad.append('base version %s != kit from %s' % (fb.get('version'), EXP[k]['from']))
        if fh.get('version') != to: bad.append('head version %s != %s' % (fh.get('version'), to))
        if not set(fchg) <= allow_c: bad.append('changed fields %s outside %s' % (sorted(set(fchg) - allow_c), sorted(allow_c)))
        if not set(fadd) <= set(cfg['allowed_added_fields']): bad.append('ADDED fields %s (allowed %s)' % (fadd, cfg['allowed_added_fields']))
        if frem: bad.append('REMOVED fields %s' % frem)
        if fh.get('resolved') != P['resolved'][to]: bad.append('resolved %s' % ('ABSENT' if 'resolved' not in fh else 'OTHER ' + str(fh.get('resolved'))))
        if fh.get('integrity') != P['integrity'][to]: bad.append('integrity %s' % ('ABSENT' if 'integrity' not in fh else ('the OLD %s value' % P['neg_control'] if fh.get('integrity') == P['integrity'][P['neg_control']] else 'OTHER ' + str(fh.get('integrity'))[:24])))
        if n == 'browserslist' and fh.get('dependencies') != BLD: bad.append('dependencies %s != 4.28.7 declared %s' % (fh.get('dependencies'), BLD))
        l2.append((k, bad, fchg, fadd))
    C.chk('L2 %s fields' % tag, all(not b for _, b, _, _ in l2),
          '; '.join('%s %s->%s changed %s added %s%s' % (name_of(k), EXP[k]['from'], PK[name_of(k)]['to'], fc, fa, (' BAD: ' + ' / '.join(b)) if b else ' ok') for k, b, fc, fa in l2))
    # L3
    flips = sorted(k for k in both if any(pb[k].get(f) != ph[k].get(f) for f in FL))
    arch = {}
    for f in AR:
        cb = sorted(k for k in pb if f in pb[k]); chh = sorted(k for k in ph if f in ph[k])
        neq = sorted(k for k in set(cb) | set(chh) if pb.get(k, {}).get(f) != ph.get(k, {}).get(f))
        arch[f] = (len(cb), len(chh), cfg['%s_base' % f], neq)
    C.chk('L3 %s collateral' % tag, not flips and all(a == b == c and not d for a, b, c, d in arch.values()),
          'flag flips (%s) %d %s | %s' % ('/'.join(FL), len(flips), flips[:3], ' | '.join('%s entries %d -> %d (kit %d), arrays not equal to base %d %s' % (f, a, b, c, len(d), d[:2]) for f, (a, b, c, d) in arch.items())))
    # L4
    l4 = []
    for k in want:
        ob = list(pb.get(k, {})); oh = list(ph.get(k, {})); exp = list(ob)
        for f in ('integrity', 'resolved'):
            if f in oh and f not in exp: exp.insert(exp.index('version') + 1, f)
        if exp != oh: l4.append((name_of(k), oh, exp))
    for n, s in (('base', pb), ('head', ph)):
        bo = [k for k, v in s.items() if 'resolved' in v and 'integrity' in v]
        npm = [k for k in bo if list(s[k]).index('resolved') == list(s[k]).index('version') + 1 == list(s[k]).index('integrity') - 1] if bo else []
        print('INFO L4 %s %s: %d entr(ies) carry resolved+integrity; %d of them put both immediately after version (npm order); %d carry neither' % (
            tag, n, len(bo), len(npm), sum(1 for v in s.values() if 'resolved' not in v and 'integrity' not in v)))
    C.chk('L4 %s key order' % tag, not l4, 'ruled entries whose head key order != base order with resolved+integrity right after version: %d %s' % (len(l4), [(n, oh) for n, oh, _ in l4][:2]))
    # L5
    l5 = [name_of(k) for k in want for f in ('dependencies', 'peerDependencies', 'optionalDependencies') if isinstance(ph.get(k, {}).get(f), dict) and list(ph[k][f]) != sorted(ph[k][f])]
    nb = sum(1 for v in pb.values() for f in ('dependencies',) if isinstance(v.get(f), dict) and list(v[f]) != sorted(v[f]))
    nmaps = sum(1 for v in pb.values() if isinstance(v.get('dependencies'), dict))
    C.chk('L5 %s alphabetical maps' % tag, not l5, 'ruled entries with an un-sorted dependency map at head %d %s | INFO base lock: %d of %d dependencies maps NOT alphabetical' % (len(l5), l5, nb, nmaps))
    # L6
    bl, hl = bt.split('\n'), ht.split('\n'); spans_b = []; spans_h = []
    for k in want:
        ib, ih = find_member(bl, k), find_member(hl, k)
        if ib is not None: spans_b.append(member_span(bl, ib))
        if ih is not None: spans_h.append(member_span(hl, ih))
    inside = lambda spans, a, b: a == b or any(s and s[0] <= a and b - 1 <= s[1] for s in spans)
    ops = opcodes(bt, ht); outside = [o for o in ops if not (inside(spans_b, o[1], o[2]) and inside(spans_h, o[3], o[4]))]
    mi = sum(o[2] - o[1] for o in ops); pl = sum(o[4] - o[3] for o in ops)
    C.chk('L6 %s LINE' % tag, not outside and bool(ops) == bool(chg),
          '%d hunk(s), -%d/+%d line(s) | hunks OUTSIDE the %d ruled entry blocks: %d %s' % (len(ops), mi, pl, len(want), len(outside),
              ['%s base %d-%d head %d-%d' % (o[0], o[1] + 1, o[2], o[3] + 1, o[4]) for o in outside[:3]]))
    # L7
    ub, _ = unsatisfied(pb); uh, unp = unsatisfied(ph)
    C.chk('L7 %s resolvability' % tag, not uh and not unp, 'dep_family edges unsatisfied at head %d %s | UNPARSED ranges %d %s | INFO base %d unsatisfied %s' % (
        len(uh), uh[:3], len(unp), unp[:2], len(ub), ub[:2]))
    # L8
    rec = reconstruct(bt, path)
    if rec == ht:
        C.chk('L8 %s reconstruction' % tag, True, 'the kit\'s own surgical edit of the base text == head, byte for byte (%d bytes)' % len(ht))
    else:
        rl, hl2 = rec.split('\n'), ht.split('\n'); i = next((j for j in range(min(len(rl), len(hl2))) if rl[j] != hl2[j]), min(len(rl), len(hl2)))
        C.chk('L8 %s reconstruction' % tag, False, 'differs from the kit reconstruction at line %d: kit %r | head %r (lines %d vs %d)' % (
            i + 1, (rl[i] if i < len(rl) else '<EOF>')[:120], (hl2[i] if i < len(hl2) else '<EOF>')[:120], len(rl), len(hl2)))
    return {'changed': len(chg), 'added': len(add), 'removed': len(rem), 'flips': len(flips), 'libc': arch['libc'][:2], 'minus': mi, 'plus': pl,
            'unsat': len(uh), 'outside': len(outside)}


def run(pairs, quiet=False):
    C = Checks(quiet=quiet); facts = {}
    for path in sorted(K['locks']):
        bt, ht = pairs[path]
        if bt is None or ht is None:
            C.chk('L0 %s present' % path, False, 'blob missing at base %s / head %s' % (bt is None, ht is None)); continue
        facts[path] = check_lock(C, path, bt, ht)
    return C, facts


# ---------- the reconstruction and the plants (in memory, from the base text) ----------
def _ind(s): return s[:len(s) - len(s.lstrip())]


def set_field(ls, a, b, field, value):
    for j in range(a, b + 1):
        s = ls[j]
        if s.strip().startswith('"%s":' % field) and _ind(s) == _ind(ls[a]) + '  ':
            ls[j] = '%s"%s": %s%s' % (_ind(s), field, json.dumps(value), ',' if s.rstrip().endswith(',') else ''); return True
    return False


def reconstruct(text, path, only=None, after_license=False, unsorted_deps=False, wrong_int=None):
    ls = text.split('\n')
    for key in sorted(K['locks'][path]['expected_changes']):
        n = name_of(key)
        if only and n not in only: continue
        P = PK[n]; to = P['to']; i = find_member(ls, key); a, b = member_span(ls, i); ind = _ind(ls[a]) + '  '
        integ = P['integrity'][P['neg_control']] if wrong_int == n else P['integrity'][to]
        set_field(ls, a, b, 'version', to)
        if not set_field(ls, a, b, 'resolved', P['resolved'][to]):
            new = ['%s"resolved": %s,' % (ind, json.dumps(P['resolved'][to])), '%s"integrity": %s,' % (ind, json.dumps(integ))]
            anchor = 'license' if after_license else 'version'
            vi = next(j for j in range(a, b + 1) if ls[j].startswith(ind + '"%s":' % anchor))
            if after_license and not ls[vi].rstrip().endswith(','):
                ls[vi] += ','; new[-1] = new[-1].rstrip(',')
            ls[vi + 1:vi + 1] = new; a, b = member_span(ls, i)
        else:
            set_field(ls, a, b, 'integrity', integ)
        if n == 'browserslist':
            di = next(j for j in range(a, b + 1) if ls[j] == ind + '"dependencies": {')
            da, db = member_span(ls, di)
            ks = sorted(BLD) if not unsorted_deps else sorted(BLD, reverse=True)
            ls[da + 1:db] = ['%s  "%s": %s%s' % (ind, d, json.dumps(BLD[d]), ',' if q < len(ks) - 1 else '') for q, d in enumerate(ks)]
    return '\n'.join(ls)


def plant_devflip(text, path):
    ls = text.split('\n'); d = json.loads(text)['packages']
    k = next(k for k in sorted(d) if k and k not in K['locks'][path]['expected_changes'] and 'dev' not in d[k] and 'version' in d[k])
    i = find_member(ls, k); vi = next(j for j in range(i, i + 6) if ls[j].strip().startswith('"version":'))
    ls[vi + 1:vi + 1] = ['%s"dev": true,' % _ind(ls[vi])]
    return '\n'.join(ls), k


def plant_arch(text, field, mode):
    """mode 'remove': delete the first `field` array; 'move': move it to the END of its entry (value-equal); 'alter': change its element"""
    ls = text.split('\n'); st = [j for j, l in enumerate(ls) if l.strip() == '"%s": [' % field]
    if not st: return None, None
    a, b = member_span(ls, st[0])
    own_i = next(j for j in range(a, -1, -1) if ls[j].strip().endswith('{') and ls[j].strip().startswith('"node_modules/'))
    owner = ls[own_i].strip().split('"')[1]
    if mode == 'alter':   # every arch array in these locks has ONE element (measured): change its value, keep the line shape
        s = ls[a + 1]; q = s.index('"'); ls[a + 1] = s[:q] + '"gate58-planted"' + (',' if s.rstrip().endswith(',') else '')
        return '\n'.join(ls), owner
    arr = ls[a:b + 1]; last = ls[b].rstrip().endswith(',')
    del ls[a:b + 1]
    if not last: ls[a - 1] = ls[a - 1].rstrip().rstrip(',')
    if mode == 'remove': return '\n'.join(ls), owner
    _, ob = member_span(ls, own_i)
    ls[ob - 1] = ls[ob - 1] + ','; arr[-1] = arr[-1].rstrip().rstrip(',')
    ls[ob:ob] = arr
    return '\n'.join(ls), owner


def plant_extra(text):
    ls = text.split('\n'); i = find_member(ls, 'node_modules/update-browserslist-db'); a, b = member_span(ls, i)
    set_field(ls, a, b, 'version', '1.2.4'); return '\n'.join(ls)


def plant_added(text):
    ls = text.split('\n'); i = find_member(ls, 'node_modules/browserslist'); ind = _ind(ls[i])
    ls[i:i] = ['%s"node_modules/zz-gate58-planted": {' % ind, '%s  "version": "0.0.1"' % ind, '%s},' % ind]; return '\n'.join(ls)


if '--selftest' in A:
    B = commit(REPO, K['base'])
    print('c2_lockdiff_gate58 SELFTEST %s | repo %s | base %s (every plant built in memory from the base blobs; nothing written)' % (now(), REPO, B[:12]))
    base = {p: show(REPO, B, p) for p in K['locks']}
    T1 = {p: reconstruct(base[p], p) for p in base}
    arms = []

    def arm(name, pairs, want_pass, expect):
        print('\n=== ARM %s (expected %s) ===' % (name, 'PASS' if want_pass else 'FAIL'))
        C, f = run(pairs); got = C.nfail() == 0; ex_ok = expect(C, f)
        print('ARM %s: verdict %s (expected %s) | failed checks %s | named as expected %s -> %s' % (name, 'PASS' if got else 'FAIL', 'PASS' if want_pass else 'FAIL',
              C.failed() or 'NONE', ex_ok, 'OK' if (got == want_pass and ex_ok) else 'MISMATCH'))
        for p in sorted(f): print('  CHANGED-ENTRIES %s %d | added %d | flips %d | libc %d -> %d | text -%d/+%d outside %d | unsat %d' % (
            p.replace('Blockchain/Dev/', ''), f[p]['changed'], f[p]['added'], f[p]['flips'], f[p]['libc'][0], f[p]['libc'][1], f[p]['minus'], f[p]['plus'], f[p]['outside'], f[p]['unsat']))
        arms.append(got == want_pass and ex_ok)
    only = lambda C, pre: set(t.split(' ')[0] for t in C.failed()) == set(pre)
    REF = 'Blockchain/Dev/services/referral/package-lock.json'; GOV = 'Blockchain/Dev/services/governance/package-lock.json'
    arm('T0 base-vs-base', {p: (base[p], base[p]) for p in base}, False, lambda C, f: all(f[p]['changed'] == 0 for p in f) and len(C.failed('L1')) == 6)
    arm('T1 legitimate bump (kit reconstruction)', {p: (base[p], T1[p]) for p in base}, True, lambda C, f: sum(f[p]['changed'] for p in f) == 23)
    T2 = {}; dv = {}
    for p in base: T2[p], dv[p] = plant_devflip(T1[p], p)
    print('\n(T2 plants `"dev": true` on: %s)' % json.dumps({k.replace('Blockchain/Dev/', ''): v for k, v in dv.items()}))
    arm('T2 T1 + dev flip', {p: (base[p], T2[p]) for p in base}, False, lambda C, f: all(f[p]['flips'] == 1 for p in f) and set(t.split(' ')[0] for t in C.failed()) >= {'L1', 'L3'})
    T3 = dict(T1); T3[REF], o3 = plant_arch(T1[REF], 'libc', 'remove'); print('\n(T3 removes the libc array of %s in referral)' % o3)
    arm('T3 T1 + libc removal', {p: (base[p], T3[p]) for p in base}, False, lambda C, f: f[REF]['libc'] == (10, 9) and 'L3 services/referral/package-lock.json collateral' in C.failed())
    T4 = dict(T1); T4[REF], o4 = plant_arch(T1[REF], 'libc', 'move'); print('\n(T4 MOVES the libc array of %s to its entry\'s end; values equal: %s)' % (o4, json.loads(T4[REF])['packages'] == json.loads(T1[REF])['packages']))
    arm('T4 T1 + libc moved (value-equal)', {p: (base[p], T4[p]) for p in base}, False,
        lambda C, f: 'L6 services/referral/package-lock.json LINE' in C.failed() and not C.failed('L1') and not C.failed('L2') and not C.failed('L3'))
    arm('T5 T1 + update-browserslist-db touched', {p: (base[p], plant_extra(T1[p])) for p in base}, False, lambda C, f: len(C.failed('L1')) == 6)
    arm('T6 T1 + an added entry', {p: (base[p], plant_added(T1[p])) for p in base}, False, lambda C, f: all(f[p]['added'] == 1 for p in f))
    T7 = dict(T1); T7[ROOT] = reconstruct(base[ROOT], ROOT, after_license=True)
    arm('T7 root resolved+integrity AFTER license', {p: (base[p], T7[p]) for p in base}, False,
        lambda C, f: 'L4 package-lock.json key order' in C.failed() and not [t for t in C.failed() if not t.startswith(('L4 package-lock.json', 'L6 package-lock.json', 'L8 package-lock.json'))])
    T8 = {p: reconstruct(base[p], p, unsorted_deps=True) for p in base}
    arm('T8 browserslist deps map un-sorted', {p: (base[p], T8[p]) for p in base}, False, lambda C, f: len(C.failed('L5')) == 6 and not C.failed('L2'))
    T9 = {p: reconstruct(base[p], p, only={'browserslist'}) for p in base}
    arm('T9 browserslist ONLY (no data packages)', {p: (base[p], T9[p]) for p in base}, False, lambda C, f: f[GOV]['unsat'] == 3 and 'L7 services/governance/package-lock.json resolvability' in C.failed() and len(C.failed('L1')) == 6)
    T10 = dict(T1); T10[REF], o10 = plant_arch(T1[REF], 'os', 'alter'); print('\n(T10 changes the os array element of %s in referral)' % o10)
    arm('T10 T1 + os array element changed', {p: (base[p], T10[p]) for p in base}, False, lambda C, f: 'L3 services/referral/package-lock.json collateral' in C.failed())
    T11 = {p: reconstruct(base[p], p, wrong_int='caniuse-lite') for p in base}
    arm('T11 caniuse-lite with the OLD integrity', {p: (base[p], T11[p]) for p in base}, False, lambda C, f: len(C.failed('L2')) == 6)
    n = arms.count(False)
    print('\nSELFTEST %s: %d of %d arms returned their expected verdict and named check' % ('OK' if n == 0 else 'MISMATCH', len(arms) - n, len(arms)))
    raise SystemExit(1 if n else 0)

B = commit(REPO, opt('--base', K['base'])); H = commit(REPO, opt('--head') or sys.exit('--head <sha> is required (or --selftest)'))
print('c2_lockdiff_gate58 %s | repo %s | base %s | head %s' % (now(), REPO, B, H))
C, f = run({p: (show(REPO, B, p), show(REPO, H, p)) for p in K['locks']})
n = C.nfail()
print('LOCKDIFF %s: %d FAIL of %d checks | base %s head %s | ruled entries changed %d of 23' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), B[:12], H[:12], sum(x['changed'] for x in f.values())))
for p in sorted(f): print('CHANGED-ENTRIES %s %d | added %d | removed %d | flips %d | libc %d -> %d | text -%d/+%d | unsatisfied %d' % (
    p, f[p]['changed'], f[p]['added'], f[p]['removed'], f[p]['flips'], f[p]['libc'][0], f[p]['libc'][1], f[p]['minus'], f[p]['plus'], f[p]['unsat']))
raise SystemExit(1 if n else 0)
