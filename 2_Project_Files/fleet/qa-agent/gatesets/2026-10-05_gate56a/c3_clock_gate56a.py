#!/usr/bin/env python3
"""c3_clock_gate56a.py — gate56a C3 FROZEN-CLOCK PROOF for ONE of Seat B 59th's two re-date PRs. THE POINT OF THE GATE.
It runs the repo's OWN date-reading code, at base and at head, with the clock PINNED, and asks whether the fuse has lapsed.
METHOD (faketime-free): the five files the gates need (kit audit_files_for_c3) are extracted with `git show` (READ ONLY) per side into
<OUT>/<side>/Blockchain/Dev/scripts/audit/; `node --import c3_freeze_clock_gate56a.mjs` replaces Date's ZERO-ARG constructor / Date.now()
with FROZEN_NOW_ISO, so utcToday() (baseline-contract.mjs:92-94) returns the pinned UTC day and everything else is the real Date.
  S0 SEMANTICS (read from each side's extracted files, printed with file:line): isLapsed's `return expires <= today;`; utcToday's
     `new Date().toISOString().slice(0, 10)`; pr3 audit-gate.mjs `const today = utcToday();` + `isLapsed(entry, today)`; pr4
     lock-discovery.mjs `isLapsed(entry)` inside validateOutOfScope. FAILS if any side's comparison is not `<=` (the valid-through table
     below assumes it).
  K0 CLOCK SELF-TEST: pinned run prints the pinned day; CONTROL: the same probe with FROZEN_NOW_ISO unset prints the REAL UTC day, which
     differs (the pin is what moves it); a malformed FROZEN_NOW_ISO refuses (exit 97).
  The clock TABLE (instants chosen at the day edges: 23:59:59.999Z = last instant of a valid day; 00:00:00.000Z = first instant of the
  dead day), for the PR's target(s) (pr3: the two react-router rows; pr4: the KS-769 mobile-tree exclusion):
     A1 before_old @23:59:59.999Z   base NOT lapsed, head NOT lapsed      (CONTROL: the instrument can say "alive")
     A2 at_old     @00:00:00.000Z   base LAPSED,     head NOT lapsed      (the `<=` boundary: dead ON the written day)
     A3 between    @12:00:00.000Z   base LAPSED,     head NOT lapsed      (i) after the old expiry, before the new
     A4 last_valid @23:59:59.999Z   head NOT lapsed                       the new value is valid THROUGH this UTC day
     A5 at_new     @00:00:00.000Z   head LAPSED                           (ii) the fuse still exists at head
     A6 at every instant, the set of OTHER lapsed rows / problems is equal base vs head (no other fuse moved)
  pr3 also runs the REAL leg-6 gate end-to-end: audit-gate.mjs with a FAKE `npm` first on PATH (OUT/fakebin/npm prints a canned
     `npm audit --json` naming the two advisories; nothing reaches the registry):
     G1 base @between: rc 1, both ids under `LAPSED`.   G2 head @between: rc 0, `OK`.   G3 head @at_new: rc 1, both ids `LAPSED`.
     G4 CONTROL head @between with the canned report + one UNKNOWN advisory: rc 1 `NEW` (the gate fires on a fresh id; judged on NEW only).
     G5 CONTROL base @before_old: rc 0.
  pr4 also runs D1 DISCRIMINATION CONTROL: validateOutOfScope([]) at head @before_old (entry alive on both sides) throws `matches NO tracked` and the probe does NOT
     count it as lapsed (a throw is not automatically a lapse).
  (iii) the controls that fire: K0, A1/G5 (alive arms), G4, D1, and A5 (the head arm that DOES lapse).
Base-state run (no --head, no --head-file): S0, K0 and the BASE column only; exits 4 "NO PR YET — base state" (never a PASS).
--head-file <f>: a SYNTHETIC head for this PR's one path (drafter/tester exercise; the verdict line says SYNTHETIC).
OUT must be OUTSIDE /Volumes/DevMASTER/!CODING/ unless under the QA reports root (lib guard_out: lexical + realpath BEFORE any mkdir).
Usage: c3_clock_gate56a.py --which pr3|pr4 --repo <clone> --out <dir> [--base sha] [--head sha | --head-file f]
rc 0 PASS / 1 FAIL / 2 usage / 4 base state only"""
import json, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate56a import K, G, git, now, Checks, has_commit, pr_cfg, side_text, guard_out, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or not all(x in A for x in ('--which', '--repo', '--out')):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
W = opt('--which'); P = pr_cfg(W); REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head'); HF = opt('--head-file')
for s in [BASE] + ([HEAD] if HEAD else []):
    if not re.fullmatch(r'[0-9a-f]{40}', s or '') or not has_commit(REPO, s):
        print('REFUSING: %r is not a full sha of a commit in %s' % (s, REPO)); raise SystemExit(2)
if HEAD and HF:
    print('REFUSING: --head and --head-file are exclusive'); raise SystemExit(2)
OUT = guard_out(opt('--out'))     # refuses (rc 2) BEFORE creating anything under !CODING/ outside the reports root
FREEZE = os.path.join(G, 'c3_freeze_clock_gate56a.mjs'); PROBE = os.path.join(G, 'c3_probe_gate56a.mjs')
NODE = 'node'
SIDES = ['base'] + (['head'] if (HEAD or HF) else [])
print('c3_clock_gate56a %s | %s %s %s | base %s | head %s | OUT %s | node %s' % (now(), W, P['ticket'], P['path'], BASE[:12],
      ('SYNTHETIC FILE %s' % HF) if HF else (HEAD or 'NONE (base state)'), OUT, subprocess.run([NODE, '--version'], capture_output=True, text=True).stdout.strip()))


def extract(side):
    sha = BASE if side == 'base' else (HEAD or BASE)
    d = os.path.join(OUT, side)
    for f in K['audit_files_for_c3']:
        t = side_text(REPO, sha, f, HF if (side == 'head' and HF and f == P['path']) else None)
        p = os.path.join(d, f); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(t)
    locks = sorted(l for l in git(REPO, 'ls-tree', '-r', '--name-only', sha).splitlines() if l.endswith('package-lock.json'))
    json.dump(locks, open(os.path.join(d, 'locks.json'), 'w'))
    return os.path.join(d, K['audit_dir']), os.path.join(d, 'locks.json'), sha


def node(args, iso, extra_env=None, cwd=None):
    env = {k: v for k, v in os.environ.items() if k != 'FROZEN_NOW_ISO'}
    if iso is not None:
        env['FROZEN_NOW_ISO'] = iso
    env.update(extra_env or {})
    r = subprocess.run([NODE, '--import', 'file://' + FREEZE] + args, capture_output=True, text=True, env=env, cwd=cwd, timeout=120)
    return r.returncode, r.stdout, r.stderr


def probe(side_dir, locks, iso):
    rc, o, e = node([PROBE, 'baseline' if W == 'pr3' else 'lockdisc', side_dir] + ([] if W == 'pr3' else [locks]), iso)
    if rc != 0 or not o.strip():
        print('PROBE ERROR rc %d stderr %s' % (rc, e.strip()[:400])); return None
    return json.loads(o.strip().splitlines()[-1])


def target_lapsed(r):
    if r is None:
        return None
    if W == 'pr3':
        n = sum(1 for x in P['rows'] if x in r['lapsed'])
        return True if n == len(P['rows']) else False if n == 0 else None   # None: only ONE of the two rows lapsed — never a pass
    return bool(r['lapsed'])


def others(r):
    if r is None:
        return None
    if W == 'pr3':
        return sorted(x for x in r['lapsed'] if x not in P['rows'])
    m = r.get('message', '')
    return sorted(l.strip() for l in m.split('\n') if l.strip().startswith('- ') and P['entry_dir'] not in l)


C = Checks()
SD = {s: extract(s) for s in SIDES}

# S0 semantics, with file:line, per side
for s in SIDES:
    ad = SD[s][0]
    bc = open(os.path.join(ad, 'baseline-contract.mjs'), encoding='utf-8').read().split('\n')
    cmp_ = [(i + 1, l.strip()) for i, l in enumerate(bc) if re.search(r'return expires\s*(<=|<|>=|>)\s*today', l)]
    ut = [(i + 1, l.strip()) for i, l in enumerate(bc) if 'new Date().toISOString().slice(0, 10)' in l]
    if W == 'pr3':
        rd = open(os.path.join(ad, 'audit-gate.mjs'), encoding='utf-8').read().split('\n')
        callers = [(i + 1, l.strip()) for i, l in enumerate(rd) if re.search(r'const today = utcToday\(\)|isLapsed\(entry, today\)', l)]
        cname = 'audit-gate.mjs'
    else:
        rd = open(os.path.join(ad, 'lock-discovery.mjs'), encoding='utf-8').read().split('\n')
        callers = [(i + 1, l.strip()) for i, l in enumerate(rd) if re.search(r'isLapsed\(entry\)|^export function validateOutOfScope|validateOutOfScope\(locks\)', l)]
        cname = 'lock-discovery.mjs'
    ok = len(cmp_) == 1 and '<=' in cmp_[0][1] and len(ut) == 1 and len(callers) >= 2
    C.chk('S0 semantics %s' % s, ok, 'baseline-contract.mjs:%s %r | utcToday baseline-contract.mjs:%s | %s %s' % (
        cmp_[0][0] if cmp_ else '?', cmp_[0][1] if cmp_ else 'NOT FOUND', ut[0][0] if ut else '?', cname, ['%d %s' % c for c in callers]))
print('INFO S0 MEANING: `expires <= today` -> a written day D is DEAD from D 00:00:00Z, valid THROUGH D-1 (UTC). Old %s valid through %s; new %s valid through %s (UTC; AEDT = UTC+11 from 2026-10-04, so the head value dies at %s 11:00 AEDT).' % (
    P['old'], (datetime.date.fromisoformat(P['old']) - datetime.timedelta(days=1)).isoformat(), P['new'], P['valid_through_new'], P['new']))

# K0 clock self-test
rc1, o1, e1 = node([PROBE, 'clock'], P['clock']['between'] + 'T12:00:00.000Z')
rc2, o2, e2 = node([PROBE, 'clock'], None)
rc3, o3, e3 = node([PROBE, 'clock'], 'not-a-date')
real = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
t1 = json.loads(o1)['today'] if rc1 == 0 else None; t2 = json.loads(o2)['today'] if rc2 == 0 else None
C.chk('K0 clock self-test', t1 == P['clock']['between'] and t2 == real and t2 != t1 and rc3 == 97,
      'pinned %s -> today %s | CONTROL unpinned -> %s (real UTC %s) | malformed pin rc %d (want 97) | stderr %r' % (P['clock']['between'], t1, t2, real, rc3, e1.strip()[:80]))

ck = P['clock']
TABLE = [('A1 before_old', ck['before_old'] + 'T23:59:59.999Z', False, False),
         ('A2 at_old', ck['at_old'] + 'T00:00:00.000Z', True, False),
         ('A3 between', ck['between'] + 'T12:00:00.000Z', True, False),
         ('A4 last_valid_new', ck['last_valid_new'] + 'T23:59:59.999Z', True, False),
         ('A5 at_new', ck['at_new'] + 'T00:00:00.000Z', True, True)]
oth = []
for tag, iso, want_b, want_h in TABLE:
    rb = probe(SD['base'][0], SD['base'][1], iso); lb = target_lapsed(rb)
    if 'head' in SD:
        rh = probe(SD['head'][0], SD['head'][1], iso); lh = target_lapsed(rh)
        ok = lb is want_b and lh is want_h
        C.chk(tag, ok, '@%s: base today %s lapsed %s (want %s) | head today %s lapsed %s (want %s)' % (iso, rb and rb['today'], lb, want_b, rh and rh['today'], lh, want_h))
        oth.append((tag, others(rb), others(rh)))
        if W == 'pr4' and rh:
            print('INFO %s head entries %s | message %r' % (tag, rh['entries'], rh['message'][:160]))
    else:
        C.chk(tag + ' (base only)', lb is want_b, '@%s: base today %s lapsed %s (want %s) | base expires %s' % (
            iso, rb and rb['today'], lb, want_b, (rb or {}).get('entries') if W == 'pr4' else {k: (rb or {}).get('expires', {}).get(k) for k in P['rows']}))
if 'head' in SD:
    C.chk('A6 no other fuse moved', all(b == h for _, b, h in oth), '; '.join('%s other-lapsed base %s head %s' % (t, b, h) for t, b, h in oth))

if W == 'pr3':
    fb = os.path.join(OUT, 'fakebin'); os.makedirs(fb, exist_ok=True)
    def canned(extra):
        via = [{'url': 'https://github.com/advisories/%s' % g, 'name': 'react-router', 'severity': 'moderate', 'title': 'canned by c3_clock_gate56a'} for g in P['rows']]
        if extra:
            via.append({'url': 'https://github.com/advisories/GHSA-0000-0000-0000', 'name': 'not-a-real-package', 'severity': 'high', 'title': 'canned UNKNOWN control'})
        return json.dumps({'auditReportVersion': 2, 'vulnerabilities': {'react-router': {'name': 'react-router', 'severity': 'moderate', 'via': via}}})
    for name, extra in (('canned_two.json', False), ('canned_plus_unknown.json', True)):
        open(os.path.join(fb, name), 'w').write(canned(extra))
    def gate(side, iso, fixture):
        npm = os.path.join(fb, 'npm')
        open(npm, 'w').write('#!/bin/sh\n# FAKE npm for c3_clock_gate56a: prints a canned `npm audit --json`, never reaches a registry\ncat "%s"\nexit 1\n' % os.path.join(fb, fixture))
        os.chmod(npm, 0o755)
        dev = os.path.join(OUT, side, 'Blockchain', 'Dev')
        rc, o, e = node([os.path.join(SD[side][0], 'audit-gate.mjs')], iso, {'PATH': fb + ':' + os.environ.get('PATH', '')}, cwd=dev)
        lap = [x for x in P['rows'] if re.search(r'-\s+%s\b' % re.escape(x), e.split('LAPSED')[1] if 'LAPSED' in e else '')]
        return rc, o, e, lap
    GT = [('G5 CONTROL base alive', 'base', ck['before_old'] + 'T23:59:59.999Z', 'canned_two.json', 0, [])]
    GT.insert(0, ('G1 base between', 'base', ck['between'] + 'T12:00:00.000Z', 'canned_two.json', 1, P['rows']))
    if 'head' in SD:
        GT += [('G2 head between', 'head', ck['between'] + 'T12:00:00.000Z', 'canned_two.json', 0, []),
               ('G3 head at_new', 'head', ck['at_new'] + 'T00:00:00.000Z', 'canned_two.json', 1, P['rows']),
               ('G4 CONTROL head + unknown', 'head', ck['between'] + 'T12:00:00.000Z', 'canned_plus_unknown.json', 1, None)]
    for tag, side, iso, fx, want_rc, want_lap in GT:
        rc, o, e, lap = gate(side, iso, fx)
        extra_ok = ('NEW advisor' in e and 'GHSA-0000-0000-0000' in e) if 'unknown' in tag else True
        okl = want_lap is None or (sorted(lap) == sorted(want_lap))   # G4 judges only the NEW arm
        okk = ('OK — no advisories outside' in o) if want_rc == 0 else True
        C.chk(tag, rc == want_rc and okl and extra_ok and okk, 'audit-gate.mjs (%s) @%s fixture %s: rc %d (want %d) | LAPSED ids %s (want %s) | stdout %r | stderr %r' % (
            side, iso, fx, rc, want_rc, lap, want_lap, o.strip().split('\n')[-1][:90], ' / '.join(l.strip() for l in e.strip().split('\n') if l.strip())[:260]))
else:
    if 'head' in SD:
        emp = os.path.join(OUT, 'empty_locks.json'); json.dump([], open(emp, 'w'))
        r = probe(SD['head'][0], emp, ck['before_old'] + 'T23:59:59.999Z')   # an instant at which BOTH sides' entry is alive
        C.chk('D1 discrimination control', r is not None and r['threw'] and 'matches NO tracked' in r['message'] and not r['lapsed'],
              'validateOutOfScope([]) at head @before_old: threw %s | lapsed-classified %s (want False) | %r' % (r and r['threw'], r and r['lapsed'], (r or {}).get('message', '')[:120]))

n = C.nfail()
if 'head' not in SD:
    print('C3 %s NO PR YET — base state only: %d FAIL of %d base-side arms (rc 4; never a PASS)' % (W, n, len(C.res))); raise SystemExit(4 if n == 0 else 1)
print('C3 %s %s: %d FAIL of %d | the old value %s lapses at base, the new %s keeps the fuse alive through %s and lapses at %s 00:00Z%s' % (
    W, 'PASS' if n == 0 else 'FAIL', n, len(C.res), P['old'], P['new'], P['valid_through_new'], P['new'], ' | SYNTHETIC head (never evidence of the PR)' if HF else ''))
raise SystemExit(1 if n else 0)
