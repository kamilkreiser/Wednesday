#!/usr/bin/env python3
"""specdiff_gate52.py — the drafter's PREDICTION for requirements 4 (goldens, yaml) and 5 (the red-cell census), by reading blobs and plumbing in
the SCRATCH clone only (<scratchpad>/g52_sp/clone; temp index files under <scratchpad>/g52_sp/). Develop, heads and END_B come from pins_gate52.json.
Per PR (kit order: #1367 = A, #1368 = B):
  S1 the file set == kit.json prs.<n>.files; per-file numstat; the *.openapi.ts numstat == kit openapi_ts; the yaml numstat == kit yaml_numstat
  S2 the product hunks:
     B: every changed *.openapi.ts line is an INSERTED `required: true,` inside a `request: { body: ... }` block (no removal, no other key);
     A: exactly ONE removed line (the 200's `schema: ReferralCodeSchema` content line) and every changed line falls INSIDE the registerPath block
        whose path is the kit envelope_op spec_path, between its `200: {` and the next status key (no other operation, no other status touched)
  S3 the yaml: B: every added line == kit yaml_added_line, directly under `requestBody:`, landing on exactly kit yaml_ops, no removal;
     A: every changed line lands in kit envelope_op spec_path, method get, under responses "200"; the one removed line is the ReferralCode $ref
  S4 the Spark goldens (kit prs.<n>.goldens): sha256 prefix == kit golden_sha256_prefix; applied with `git apply --cached` onto develop under a
     TEMP index: the tree == the head on every non-yaml PR path, blob-exact (the yaml is the CONTROL that differs: the goldens carry none)
  S5 the YAML shas the seat reports: sha256 of the yaml blob at the head == kit yaml_sha256_prefix; line count and `required: true` count
  S6 the new tests: RED cells (kit red_rx) == kit red_cells; control cells (kit control_rx) == kit control_cells; each file's imports
  S7 no non-test, non-*.openapi.ts source path (the runtime-handler zero; CONTROL: the same listing on develop~2..develop~1 names #1364's 2 audit paths)
And over the pair:
  S8 the yaml at END_TREE_B: sha256 prefix == kit yaml_sha256_prefix.union, lines and `required: true` count == kit (the A+B union)
Overrides (controls): --head-<n> <sha> --end-b <tree> --goldens-dir <dir>. rc 0 PASS / rc 1 FAIL. Usage: specdiff_gate52.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
P = json.load(open(os.path.join(G, 'pins_gate52.json'), encoding='utf-8'))
CL = os.path.join(SP, 'g52_sp', 'clone'); ORDER = K['order']; NA, NB = ORDER
DEV = P['develop']; H = {n: opt('--head-' + n, P['pr_pins'][n]['head']) for n in ORDER}; ENDB = opt('--end-b', P['end_tree_b']); GD = opt('--goldens-dir', K['goldens_dir'])
Y = K['yaml']; YL = K['yaml_added_line']; EOP = K['envelope_op']
def git(*a, env=None, check=True):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True, env=env)
    if check and r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a), r.returncode, r.stderr.strip()[:300]))
    return r.stdout
def blobbytes(t, p):
    r = subprocess.run(['git', '-C', CL, 'cat-file', 'blob', '%s:%s' % (t, p)], capture_output=True)
    return r.stdout if r.returncode == 0 else None
res = []
def chk(tag, ok, msg): res.append(ok); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
def newlines_of(diff):
    out = []
    for l in diff:
        m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', l)
        if m:
            st = int(m.group(3)); cnt = int(m.group(4)) if m.group(4) is not None else 1; out += list(range(st, st + cnt))
    return out
def oldlines_of(diff):
    out = []
    for l in diff:
        m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', l)
        if m:
            st = int(m.group(1)); cnt = int(m.group(2)) if m.group(2) is not None else 1; out += list(range(st, st + cnt))
    return out
def yaml_loc(lines, i):
    """(path, method, status-or-None, under_requestBody) for 0-based line i of the yaml"""
    path = meth = status = None
    for j in range(i, -1, -1):
        if status is None and meth is None and re.match(r'^        "?(\d{3})"?:\s*$', lines[j]): status = re.match(r'^        "?(\d{3})"?:', lines[j]).group(1)
        if meth is None and re.match(r'^    (get|put|post|patch|delete):\s*$', lines[j]): meth = lines[j].strip()[:-1]
        mm = re.match(r'^  (/\S+):\s*$', lines[j])
        if mm: path = mm.group(1); break
    return path, meth, status
print('specdiff_gate52 | base %s | #%s head %s | #%s head %s | END_B %s | clone %s' % (DEV[:12], NA, H[NA][:12], NB, H[NB][:12], (ENDB or 'none')[:12], CL))
for n in ORDER:
    k = K['prs'][n]; h = H[n]; print('--- #%s (%s, %s)' % (n, k['keys'][0], k['role']))
    # S1
    names = git('diff', '--name-only', DEV, h).split(); ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in git('diff', '--numstat', DEV, h).strip().splitlines() if l}
    chk('#%s S1 file set' % n, sorted(names) == sorted(k['files']), '%d paths | extra %s | missing %s' % (len(names), sorted(set(names) - set(k['files'])), sorted(set(k['files']) - set(names))))
    for p in sorted(names): print('    numstat %s +%s/-%s' % (p, ns[p][0], ns[p][1]))
    ots = {p: '+%s/-%s' % ns[p] for p in names if p.endswith('.openapi.ts')}; yn = '+%s/-%s' % ns[Y] if Y in ns else 'ABSENT'
    chk('#%s S1 numstat' % n, ots == k['openapi_ts'] and yn == k['yaml_numstat'], 'openapi.ts %s (kit %s) | yaml %s (kit %s) | whole PR +%d/-%d (the seat claimed %s)' % (
        ots, k['openapi_ts'], yn, k['yaml_numstat'], sum(int(v[0]) for v in ns.values()), sum(int(v[1]) for v in ns.values()), k['claimed_numstat']))
    # S2
    if n == NB:
        ins = 0; bad2 = []
        for p in sorted(ots):
            d = git('diff', '-U0', DEV, h, '--', p).splitlines()
            minus = [l[1:] for l in d if l.startswith('-') and not l.startswith('---')]; plus = [l[1:] for l in d if l.startswith('+') and not l.startswith('+++')]
            other = [l for l in plus if l.strip() != 'required: true,']; ins += len(plus) - len(other)
            hb = git('show', '%s:%s' % (h, p)).splitlines(); inb = []
            for ln in newlines_of(d):
                win = '\n'.join(hb[max(0, ln - 4):ln]); inb.append(bool(re.search(r'request:\s*\{', win) and re.search(r'\bbody:\s*\{', win)))
            print('    %s: -%d +%d | inserted `required: true,` %d | other changed lines %d | each inside request.body at head: %s' % (p.split('/src/')[-1], len(minus), len(plus), len(plus) - len(other), len(minus) + len(other), inb))
            if minus or other or not all(inb): bad2.append(p)
        chk('#%s S2 only `required: true` inserted' % n, not bad2 and ins == len(ots), '%d inserted over %d files, 0 replacements | files with another change: %s' % (ins, len(ots), bad2 or 'NONE'))
    else:
        p = EOP['spec_file']; d = git('diff', '-U0', DEV, h, '--', p).splitlines(); hb = git('show', '%s:%s' % (h, p)).splitlines()
        minus = [l[1:] for l in d if l.startswith('-') and not l.startswith('---')]; plus = [l[1:] for l in d if l.startswith('+') and not l.startswith('+++')]
        st = next((i for i, l in enumerate(hb) if EOP['spec_anchor'] in l), None); en = None; s200 = s_next = None
        if st is not None:
            en = next((i for i in range(st + 1, len(hb)) if 'sharedRegistry.registerPath(' in hb[i]), len(hb))
            s200 = next((i for i in range(st, en) if re.match(r'^\s+200:\s*\{', hb[i])), None)
            if s200 is not None: s_next = next((i for i in range(s200 + 1, en) if re.match(r'^\s+\d{3}:\s', hb[i])), en)
        nl = newlines_of(d); inside = bool(nl) and s200 is not None and all(s200 + 1 <= x - 1 < s_next for x in nl)
        print('    %s: -%d +%d | the removed line(s): %s | GET block :%s-:%s, its 200 :%s-:%s | every changed line inside the 200: %s' % (
            p.split('/src/')[-1], len(minus), len(plus), [m.strip() for m in minus], (st or -1) + 1, en, (s200 or -1) + 1, s_next, inside))
        chk('#%s S2 only the GET 200 changed' % n, len(minus) == 1 and 'ReferralCodeSchema' in minus[0] and inside, 'one removed `ReferralCodeSchema` content line: %s | %d added lines all inside the 200 of %s: %s' % (
            len(minus) == 1 and 'ReferralCodeSchema' in (minus or [''])[0], len(plus), EOP['op'], inside))
    # S3
    yd = git('diff', '-U0', DEV, h, '--', Y).splitlines(); hy = git('show', '%s:%s' % (h, Y)).splitlines(); by = git('show', '%s:%s' % (DEV, Y)).splitlines()
    ya = [l[1:] for l in yd if l.startswith('+') and not l.startswith('+++')]; yr = [l[1:] for l in yd if l.startswith('-') and not l.startswith('---')]
    locs = [yaml_loc(hy, ln - 1) for ln in newlines_of(yd)]
    if n == NB:
        under = sum(1 for ln in newlines_of(yd) if hy[ln - 2].strip() == 'requestBody:'); ops = sorted((a, b) for a, b, _ in locs); want = sorted(tuple(x) for x in k['yaml_ops'])
        print('    yaml +%d/-%d | == %r: %d of %d | directly under requestBody: %d | ops %s' % (len(ya), len(yr), YL, sum(l == YL for l in ya), len(ya), under, ops))
        chk('#%s S3 yaml' % n, not yr and len(ya) == len(want) and all(l == YL for l in ya) and under == len(want) and ops == want, 'ops == kit yaml_ops %s: %s' % (want, ops == want))
    else:
        rl = [yaml_loc(by, ln - 1) for ln in oldlines_of(yd)]
        allin = all(x == (EOP['spec_path'], 'get', '200') for x in locs + rl)
        print('    yaml +%d/-%d | removed %s | every changed line (new %d, old %d) lands in (%s, get, 200): %s | distinct locations %s' % (
            len(ya), len(yr), [r.strip() for r in yr], len(locs), len(rl), EOP['spec_path'], allin, sorted(set(locs + rl), key=str)))
        chk('#%s S3 yaml' % n, len(yr) == 1 and 'ReferralCode' in yr[0] and allin, 'the one removed line is the ReferralCode $ref, all hunks in the GET 200: %s' % allin)
    # S4
    idx = os.path.join(SP, 'g52_sp', 'idx.specdiff.%s.%d' % (n, os.getpid())); env = dict(os.environ, GIT_INDEX_FILE=idx)
    git('read-tree', DEV, env=env); offs = []; shaok = []
    for g in k['goldens']:
        pf = os.path.join(GD, g, 'out.md.checker', 'patch.diff')
        if not os.path.isfile(pf): chk('#%s S4 golden %s' % (n, g), False, 'patch.diff ABSENT at %s' % pf); continue
        sh = hashlib.sha256(open(pf, 'rb').read()).hexdigest(); shaok.append(sh.startswith(k['golden_sha256_prefix'][g]))
        r = subprocess.run(['git', '-C', CL, 'apply', '--cached', '-v', pf], capture_output=True, text=True, env=env)
        offs.append((g, r.returncode, len(re.findall(r'offset', r.stderr)), sh[:12]))
        if r.returncode: print('    golden %s apply rc %d: %s' % (g, r.returncode, r.stderr.strip()[:200]))
    T = git('write-tree', env=env).strip()   # the temp index stays in the scratchpad (never deleted)
    nonyaml = [p for p in k['files'] if p != Y]
    eqs = {p: blobbytes(T, p) is not None and blobbytes(T, p) == blobbytes(h, p) for p in nonyaml}
    yeq = blobbytes(T, Y) == blobbytes(h, Y)
    print('    goldens (name, rc, offset lines, sha256): %s | golden tree %s' % (offs, T[:12]))
    for p in nonyaml: print('    golden == head %s: %s' % (p.split('/src/')[-1], eqs[p]))
    print('    CONTROL the yaml: golden tree == head: %s (the goldens carry no yaml: must be False)' % yeq)
    chk('#%s S4 goldens byte-equal' % n, all(rc == 0 for _, rc, _, _ in offs) and len(offs) == len(k['goldens']) and all(shaok) and all(eqs.values()) and not yeq,
        '%d of %d non-yaml paths blob-equal to the golden(s) applied onto develop; golden sha256 == kit: %s; yaml control differs: %s' % (sum(eqs.values()), len(nonyaml), all(shaok) and bool(shaok), not yeq))
    # S5
    yb = blobbytes(h, Y) or b''; ysh = hashlib.sha256(yb).hexdigest(); yln = yb.count(b'\n'); yrq = sum(1 for l in yb.decode('utf-8', 'replace').split('\n') if l == YL)
    chk('#%s S5 yaml sha' % n, ysh.startswith(k['yaml_sha256_prefix']) and yln == K['yaml_lines'][n] and yrq == K['yaml_required_counts'][n],
        'sha256 %s (the seat %s) | %d lines (kit %d) | %r lines %d (kit %d)' % (ysh[:16], k['yaml_sha256_prefix'], yln, K['yaml_lines'][n], YL, yrq, K['yaml_required_counts'][n]))
    # S6
    reds = []; ctl = 0
    for p in sorted(x for x in names if '/__tests__/' in x):
        t = git('show', '%s:%s' % (h, p)); r = re.findall(k['red_rx'], t); c = len(re.findall(k['control_rx'], t)); reds += r; ctl += c
        imps = re.findall(r"^import .*?from '([^']+)'|^import '([^']+)'", t, re.M)
        print('    %s: RED %s | control %d | imports %s' % (p.split('/')[-1], r, c, sorted(set(a or b for a, b in imps))))
    chk('#%s S6 red cells' % n, sorted(reds) == sorted(k['red_cells']) and ctl == k['control_cells'], 'RED %s (kit %s) | control cells %d (kit %d)' % (sorted(reds), k['red_cells'], ctl, k['control_cells']))
    # S7
    out = [p for p in names if not any(p.startswith(a) for a in K['allowed_prefixes'])]
    rt = [p for p in names if re.search(r'\.(ts|js|mjs|cjs|json|sql|sh)$', p) and '/__tests__/' not in p and not p.endswith('.openapi.ts')]
    mv = git('diff', '--name-only', DEV + '~2', DEV + '~1').split()
    mvrt = [p for p in mv if re.search(r'\.(ts|js|mjs|cjs|json|sql|sh)$', p) and '/__tests__/' not in p and not p.endswith('.openapi.ts')]
    chk('#%s S7 no runtime path' % n, not out and not rt and len(mvrt) > 0, 'outside prefixes %s | non-test non-openapi source paths %s | CONTROL the same listing on develop~2..develop~1 (#1364) reads %d path(s), %d of them non-test non-openapi source (must be > 0)' % (
        out or 'NONE', rt or 'NONE', len(mv), len([p for p in mv if re.search(r'\.(ts|js|mjs|cjs|json|sql|sh)$', p) and '/__tests__/' not in p and not p.endswith('.openapi.ts')])))
print('--- the pair')
if ENDB:
    ub = blobbytes(ENDB, Y) or b''; ush = hashlib.sha256(ub).hexdigest(); uln = ub.count(b'\n'); urq = sum(1 for l in ub.decode('utf-8', 'replace').split('\n') if l == YL)
    bb = blobbytes(DEV, Y) or b''; bsh = hashlib.sha256(bb).hexdigest()
    print('    CONTROL develop yaml sha256 %s (kit %s), %d lines, %d required' % (bsh[:16], K['yaml_sha256_prefix']['develop'], bb.count(b'\n'), sum(1 for l in bb.decode().split('\n') if l == YL)))
    chk('S8 union yaml at END_B', ush.startswith(K['yaml_sha256_prefix']['union']) and uln == K['yaml_lines']['union'] and urq == K['yaml_required_counts']['union'] and not bsh.startswith(K['yaml_sha256_prefix']['union']),
        'END_B %s yaml sha256 %s (the seat %s) | %d lines (kit %d) | %d required (kit %d) | develop differs: %s' % (
            ENDB[:12], ush[:16], K['yaml_sha256_prefix']['union'], uln, K['yaml_lines']['union'], urq, K['yaml_required_counts']['union'], not bsh.startswith(K['yaml_sha256_prefix']['union'])))
else: chk('S8 union yaml at END_B', False, 'no END_B in the pins')
nf = res.count(False)
print('SPECDIFF %s: %d FAIL of %d checks | base %s | #%s %s | #%s %s' % ('PASS' if nf == 0 else 'FAIL', nf, len(res), DEV[:12], NA, H[NA][:12], NB, H[NB][:12]))
raise SystemExit(1 if nf else 0)
