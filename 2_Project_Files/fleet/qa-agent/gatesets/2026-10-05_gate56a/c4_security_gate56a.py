#!/usr/bin/env python3
"""c4_security_gate56a.py — gate56a C4 SECURITY: the re-dated suppressions are ACCEPTED RISK EXTENDED, not fixed, and not WIDENED.
READ ONLY on git objects (+ an optional unauthenticated GET of the public GitHub advisory DB); prints only.
  --which pr3 (KS-528, audit-baseline.json):
    S1 NO ROW ADDED OR REMOVED: `accepted` key set and count base == head (kit 25).
    S2 THE TWO ROWS ARE THE SAME ACCEPTANCE: package / ticket / decidedAt / scope byte-equal base == head; only `expires` (and an appended
       reason note) moved. A changed package or ticket is a DIFFERENT suppression wearing the old row's id.
    S3 STILL THE INSTALLED EXPOSURE (no silent widening, no silent fix): every tracked package-lock.json at the head (lock blobs equal base ==
       head) is read for kit lock_packages (react-router, react-router-dom); each advisory's `vulnerabilities[]` names npm `react-router` (==
       the row's package) and every installed react-router version lies INSIDE its vulnerable_version_range — so the row still describes a
       real, unfixed exposure (an installed version >= first_patched would make the row STALE: a cleanup, not a re-date).
       CONTROL: the same range test says OUTSIDE for first_patched (7.18.0) and for 5.3.4.
    Advisory source: --advisory-dir <d> (files <GHSA>.json, e.g. the drafter's captures advisory_<GHSA>.json in this kit) or, by default, a
       live unauthenticated GET https://api.github.com/advisories/<GHSA> (no token; the tester's X6-class read).
  --which pr4 (KS-769, lock-discovery.mjs):
    S1 NO EXCLUSION ADDED OR REMOVED: the OUT_OF_SCOPE_LOCKS key set base == head == [kit entry_dir].
    S2 SAME EXCLUSION: the entry's `reason` text and `ticket` byte-equal base == head (the 'dormant' reason is unchanged, per the card).
    S3 THE TREE IS THE SAME TREE: kit mobile_lock blob base == head == kit mobile_lock_blob_base (2f5f8c1f4edf) — the exclusion is extended
       over the SAME dependency set it was ruled on; the "81 advisories (2 critical, 45 high)" figure is the CODE'S claim, NOT re-measured here.
       CONTROL: the same blob comparison against the base's root lock (Blockchain/Dev/package-lock.json) differs.
Base-state run (no --head, no --head-file): prints the base facts; rc 4 (never a PASS).
Usage: c4_security_gate56a.py --which pr3|pr4 --repo <clone> [--base sha] [--head sha | --head-file f] [--advisory-dir d]
rc 0 PASS / 1 FAIL / 2 usage / 3 advisory read failed / 4 base state only"""
import json, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate56a import K, git, now, Checks, has_commit, pr_cfg, side_text, blob_id, show, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--which' not in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
W = opt('--which'); P = pr_cfg(W); REPO = opt('--repo'); BASE = opt('--base', K['base']); HEAD = opt('--head'); HF = opt('--head-file'); ADV = opt('--advisory-dir')
for s in [BASE] + ([HEAD] if HEAD else []):
    if not re.fullmatch(r'[0-9a-f]{40}', s or '') or not has_commit(REPO, s):
        print('REFUSING: %r is not a full sha of a commit in %s' % (s, REPO)); raise SystemExit(2)
if HEAD and HF:
    print('REFUSING: --head and --head-file are exclusive'); raise SystemExit(2)
HSHA = HEAD or BASE    # for --head-file, every OTHER path is the base's (the synthetic changes only the PR's one path)
BT = side_text(REPO, BASE, P['path']); HT = side_text(REPO, HSHA, P['path'], HF) if (HEAD or HF) else None
print('c4_security_gate56a %s | %s %s | base %s | head %s' % (now(), W, P['ticket'], BASE[:12], ('SYNTHETIC FILE %s' % HF) if HF else (HEAD or 'NONE (base state)')))


def vt(v):
    m = re.match(r'^(\d+)\.(\d+)\.(\d+)', v or '')
    return tuple(int(x) for x in m.groups()) if m else None


def in_range(ver, rng):
    """GitHub vulnerable_version_range: comma-joined clauses like '>= 6.0.0, < 7.18.0' (all must hold)"""
    v = vt(ver)
    if v is None:
        return None
    for cl in [c.strip() for c in rng.split(',') if c.strip()]:
        m = re.match(r'^(>=|<=|>|<|=)\s*(\S+)$', cl)
        if not m or vt(m.group(2)) is None:
            return None
        op, b = m.group(1), vt(m.group(2))
        if not {'>=': v >= b, '<=': v <= b, '>': v > b, '<': v < b, '=': v == b}[op]:
            return False
    return True


C = Checks()
if W == 'pr3':
    ba = json.loads(BT)['accepted']
    if HT is None:
        print('BASE STATE %s: accepted %d | rows %s' % (BASE[:12], len(ba), {k: {f: ba[k].get(f) for f in ('package', 'ticket', 'decidedAt', 'expires')} for k in P['rows']}))
    else:
        ha = json.loads(HT)['accepted']
        C.chk('S1 no row added/removed', set(ba) == set(ha) and len(ha) == P['accepted_count'], 'base %d head %d (kit %d) | added %s | removed %s' % (
            len(ba), len(ha), P['accepted_count'], sorted(set(ha) - set(ba)) or 'NONE', sorted(set(ba) - set(ha)) or 'NONE'))
        same = {k: all((ba.get(k) or {}).get(f) == (ha.get(k) or {}).get(f) for f in ('package', 'ticket', 'decidedAt', 'scope')) for k in P['rows']}
        C.chk('S2 same acceptance', all(same.values()), 'package/ticket/decidedAt/scope equal per row: %s | head %s' % (same, {k: ((ha.get(k) or {}).get('package'), (ha.get(k) or {}).get('ticket')) for k in P['rows']}))
    locks = sorted(l for l in git(REPO, 'ls-tree', '-r', '--name-only', HSHA).splitlines() if l.endswith('package-lock.json'))
    lock_eq = all(blob_id(REPO, BASE, l) == blob_id(REPO, HSHA, l) for l in locks)
    inst = []
    for l in locks:
        d = json.loads(show(REPO, HSHA, l) or '{}')
        for k, v in (d.get('packages') or {}).items():
            for pk in P['lock_packages']:
                if k == 'node_modules/' + pk or k.endswith('/node_modules/' + pk):
                    inst.append((l, k, pk, v.get('version')))
    rr = [x for x in inst if x[2] == P['advisory_package']]
    advs = {}
    for g in P['rows']:
        try:
            if ADV:
                advs[g] = json.load(open(os.path.join(ADV, g + '.json'), encoding='utf-8'))
            else:
                advs[g] = json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/advisories/' + g, headers={'Accept': 'application/vnd.github+json'}), timeout=60))
        except Exception as e:
            print('ADVISORY READ FAILED %s: %s' % (g, e)); raise SystemExit(3)
    rows3 = []; ok3 = bool(rr) and lock_eq
    for g, a in advs.items():
        vs = [v for v in a.get('vulnerabilities', []) if (v.get('package') or {}).get('ecosystem') == 'npm' and (v.get('package') or {}).get('name') == P['advisory_package']]
        if not vs:
            ok3 = False; rows3.append('%s names no npm %s' % (g, P['advisory_package'])); continue
        for v in vs:
            r = v['vulnerable_version_range']; fp = (v.get('first_patched_version') or {}) if isinstance(v.get('first_patched_version'), dict) else {'identifier': v.get('first_patched_version')}
            ins = {x[3]: in_range(x[3], r) for x in rr}
            ok3 = ok3 and all(ins.values())
            ctl_fp = in_range(fp.get('identifier') or '', r); ctl_old = in_range('5.3.4', r)
            ok3 = ok3 and ctl_fp is False and ctl_old is False
            rows3.append('%s %s range %r first_patched %s | installed %s inside: %s | CONTROLS first_patched inside %s (want False), 5.3.4 inside %s (want False)' % (
                g, a.get('severity'), r, fp.get('identifier'), sorted(set(ins)), ins, ctl_fp, ctl_old))
    C.chk('S3 still the installed exposure', ok3, '%d tracked locks at %s, blob-equal base == head %s | %s installs: %s | %s' % (
        len(locks), HSHA[:12], lock_eq, P['advisory_package'], sorted(set((x[0].replace('Blockchain/Dev/', ''), x[3]) for x in rr)), ' || '.join(rows3)))
    print('INFO S3 %s installs (same advisory family, not a row of this PR): %s' % ('react-router-dom', sorted(set((x[0].replace('Blockchain/Dev/', ''), x[3]) for x in inst if x[2] != P['advisory_package']))))
else:
    def keys(t):
        m = re.search(r'export const OUT_OF_SCOPE_LOCKS = new Map\(\[(.*?)\n\]\);', t, re.S)
        return re.findall(r"^\s{4}'([^']+)',\s*$", m.group(1), re.M) if m else None
    def entry(t):
        m = re.search(r"\n(\s+reason:\n.*?)\n\s+ticket: '([^']+)',", t, re.S)
        return (m.group(1), m.group(2)) if m else (None, None)
    kb = keys(BT); rb, tb = entry(BT)
    if HT is None:
        print('BASE STATE %s: OUT_OF_SCOPE_LOCKS keys %s | ticket %s | reason %d chars | mobile lock blob %s' % (BASE[:12], kb, tb, len(rb or ''), blob_id(REPO, BASE, P['mobile_lock'])[:12]))
    else:
        kh = keys(HT); rh, th = entry(HT)
        C.chk('S1 no exclusion added/removed', kb == kh == [P['entry_dir']], 'keys base %s head %s (want [%s])' % (kb, kh, P['entry_dir']))
        C.chk('S2 same exclusion', rb is not None and rb == rh and tb == th == P['ticket'], 'reason byte-equal %s (%d chars) | ticket base %s head %s' % (rb == rh, len(rb or ''), tb, th))
        mb, mh = blob_id(REPO, BASE, P['mobile_lock']), blob_id(REPO, HSHA, P['mobile_lock']); ctl = blob_id(REPO, BASE, 'Blockchain/Dev/package-lock.json')
        C.chk('S3 same tree', mb == mh == P['mobile_lock_blob_base'] and ctl != mb, '%s base %s head %s kit %s | CONTROL root lock %s differs %s | the "81 advisories (2 critical, 45 high)" figure is the code comment\'s, NOT re-measured' % (
            P['mobile_lock'], mb[:12], mh[:12], P['mobile_lock_blob_base'][:12], ctl[:12], ctl != mb))
if HT is None:
    print('C4 %s NO PR YET — base state only (rc 4; never a PASS)%s' % (W, ' | S3 still measured at base: %s' % ('PASS' if not C.failed() else 'FAIL') if W == 'pr3' else ''))
    raise SystemExit(4 if not C.failed() else 1)
n = C.nfail(); print('C4 %s %s: %d FAIL of %d%s' % (W, 'PASS' if n == 0 else 'FAIL', n, len(C.res), ' | SYNTHETIC head (never evidence of the PR)' if HF else ''))
raise SystemExit(1 if n else 0)
