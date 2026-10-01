#!/usr/bin/env python3
"""specdiff_gate51a.py — the drafter's PREDICTION for requirement 1 (and the red-cell census of requirement 4), by reading blobs and plumbing in the
SCRATCH clone only (<scratchpad>/g51a_sp/clone; temp index files under <scratchpad>/g51a_sp/). Develop and head come from pins_gate51a.json.
  S1 the file set == kit.json prs.<n>.files (11), each path under kit.json allowed_prefixes; per-file numstat; the 4 *.openapi.ts == kit openapi_ts
  S2 every changed *.openapi.ts line ONLY adds `required: true` to a request body: drop each added line that is exactly `required: true,` and strip
     `, required: true` from the others; the result must equal the removed lines, IN ORDER, per file; and every `required: true` sits inside a
     `request: { body: ... }` block. Counts replacements vs insertions (the PR body claims 5 / 6)
  S3 the yaml: numstat +11/-0, every added line == kit yaml_added_line, each directly under `requestBody:`, and the (path, method) each one lands
     in == the 11 kit operations' spec_path, all `post`
  S4 the Spark goldens (kit goldens, in order) applied with `git apply --cached` onto develop under a TEMP index: the tree == the head on every
     non-yaml path, blob-exact (the yaml is the CONTROL that differs: the goldens carry no yaml)
  S5 the new tests: the `RED KS-1364 <id>` cells across the 6 files == kit red_cells (11), the control cells counted, and each file's imports
S6 no path outside the allowed prefixes, and no non-test, non-*.openapi.ts source path in the diff (the runtime-handler zero; control: the same
     filter applied to develop..develop^ moves reads the files #1364 touched)
Overrides (controls): --head <sha> --goldens-dir <dir>. rc 0 PASS / rc 1 FAIL. Usage: specdiff_gate51a.py <scratchpad> [overrides]"""
import json, os, re, subprocess, sys
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
P = json.load(open(os.path.join(G, 'pins_gate51a.json'), encoding='utf-8'))
CL = os.path.join(SP, 'g51a_sp', 'clone'); N = K['order'][0]; k = K['prs'][N]
DEV = P['develop']; H = opt('--head', P['pr_pins']['head']); GD = opt('--goldens-dir', K['goldens_dir'])
def git(*a, env=None, check=True):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True, env=env)
    if check and r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a), r.returncode, r.stderr.strip()[:300]))
    return r.stdout
res = []
def chk(tag, ok, msg): res.append(ok); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
print('specdiff_gate51a | base %s | head %s | clone %s' % (DEV[:12], H[:12], CL))
# S1
names = git('diff', '--name-only', DEV, H).split(); ns = {l.split('\t')[2]: (l.split('\t')[0], l.split('\t')[1]) for l in git('diff', '--numstat', DEV, H).strip().splitlines()}
chk('S1 file set', sorted(names) == sorted(k['files']), '%d paths | extra %s | missing %s' % (len(names), sorted(set(names) - set(k['files'])), sorted(set(k['files']) - set(names))))
for p in sorted(names): print('    numstat %s +%s/-%s' % (p, ns[p][0], ns[p][1]))
ots = {p: '+%s/-%s' % ns[p] for p in names if p.endswith('.openapi.ts')}
chk('S1 openapi.ts numstat', ots == K['openapi_ts'], '%s (kit %s) | summed +%d/-%d' % (ots, K['openapi_ts'], sum(int(ns[p][0]) for p in ots), sum(int(ns[p][1]) for p in ots)))
tot = (sum(int(v[0]) for v in ns.values()), sum(int(v[1]) for v in ns.values()))
print('    whole PR +%d/-%d (the seat claimed %s)' % (tot[0], tot[1], k['claimed_numstat']))
# S2
rep = ins = req = 0; bad2 = []
for p in sorted(ots):
    d = git('diff', '-U0', DEV, H, '--', p).splitlines()
    minus = [l[1:] for l in d if l.startswith('-') and not l.startswith('---')]; plus = [l[1:] for l in d if l.startswith('+') and not l.startswith('+++')]
    stripped = []
    for l in plus:
        if l.strip() == 'required: true,': ins += 1; req += 1; continue
        if ', required: true }' in l: rep += 1; req += 1; stripped.append(l.replace(', required: true }', ' }', 1)); continue
        stripped.append(l)
    if stripped != minus: bad2.append(p)
    hb = git('show', '%s:%s' % (H, p)).splitlines(); ctx = []
    for i, l in enumerate(hb):
        if 'required: true' in l and ('body' in l or l.strip() == 'required: true,'):
            win = '\n'.join(hb[max(0, i - 12):i + 1])
            ctx.append(bool(re.search(r'request:\s*\{', win) and re.search(r'\bbody\b', win)))
    print('    %s: -%d +%d | after stripping `required: true` the + side == the - side: %s | `required: true` in a request.body block at head: %d of %d' % (p, len(minus), len(plus), stripped == minus, sum(ctx), len(ctx)))
chk('S2 only `required: true` added', not bad2 and req == 11, '%d `required: true` added (%d replacements, %d insertions; the PR body claims 5 replacements / 6 insertions) | files where another key moved: %s' % (req, rep, ins, bad2 or 'NONE'))
# S3
Y = K['yaml']; yd = git('diff', '-U0', DEV, H, '--', Y).splitlines()
ya = [l[1:] for l in yd if l.startswith('+') and not l.startswith('+++')]; yr = [l for l in yd if l.startswith('-') and not l.startswith('---')]
hy = git('show', '%s:%s' % (H, Y)).splitlines(); ops = []; under = 0
newlines = []
for l in yd:
    m = re.match(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', l)
    if m:
        st = int(m.group(1)); cnt = int(m.group(2)) if m.group(2) is not None else 1; newlines += list(range(st, st + cnt))
for ln in newlines:
    i = ln - 1
    if hy[i - 1].strip() == 'requestBody:': under += 1
    path = meth = None
    for j in range(i, -1, -1):
        if meth is None and re.match(r'^    (get|put|post|patch|delete):\s*$', hy[j]): meth = hy[j].strip()[:-1]
        mm = re.match(r'^  (/\S+):\s*$', hy[j])
        if mm: path = mm.group(1); break
    ops.append((path, meth))
want = sorted((o['spec_path'], 'post') for o in K['operations'])
print('    yaml +%d/-%d | added lines == %r: %d of %d | directly under `requestBody:`: %d | ops: %s' % (len(ya), len(yr), K['yaml_added_line'], sum(l == K['yaml_added_line'] for l in ya), len(ya), under, sorted(ops)))
dc = sum(1 for l in git('show', '%s:%s' % (DEV, Y)).splitlines() if l == K['yaml_added_line']); hc = sum(1 for l in hy if l == K['yaml_added_line'])
print('    yaml lines == %r: develop %d, head %d (delta %d)' % (K['yaml_added_line'], dc, hc, hc - dc))
chk('S3 yaml', len(ya) == 11 and not yr and all(l == K['yaml_added_line'] for l in ya) and under == 11 and sorted(ops) == want,
    '+%d/-%d, %d under requestBody, ops == the 11 kit operations: %s (missing %s, extra %s)' % (len(ya), len(yr), under, sorted(ops) == want, sorted(set(want) - set(ops)), sorted(set(ops) - set(want))))
# S4
idx = os.path.join(SP, 'g51a_sp', 'idx.specdiff.%d' % os.getpid()); env = dict(os.environ, GIT_INDEX_FILE=idx)
git('read-tree', DEV, env=env); offs = []
for g in K['goldens']:
    pf = os.path.join(GD, g, 'out.md.checker', 'patch.diff')
    if not os.path.isfile(pf): chk('S4 golden %s' % g, False, 'patch.diff ABSENT at %s' % pf); continue
    r = subprocess.run(['git', '-C', CL, 'apply', '--cached', '-v', pf], capture_output=True, text=True, env=env)
    offs.append((g, r.returncode, len(re.findall(r'offset', r.stderr))))
    if r.returncode: chk('S4 golden %s applies' % g, False, r.stderr.strip()[:200])
T = git('write-tree', env=env).strip()   # the temp index stays in the scratchpad (never deleted)
nonyaml = [p for p in k['files'] if p != Y]
eqs = {p: (git('rev-parse', '%s:%s' % (T, p), check=False).strip() == git('rev-parse', '%s:%s' % (H, p), check=False).strip()) for p in nonyaml}
yeq = git('rev-parse', '%s:%s' % (T, Y)).strip() == git('rev-parse', '%s:%s' % (H, Y)).strip()
print('    goldens applied in order (name, rc, offset lines): %s | golden tree %s' % ([(g.split('KS-1364-')[1], rc, o) for g, rc, o in offs], T[:12]))
for p in nonyaml: print('    golden == head %s: %s' % (p.split('/src/')[-1], eqs[p]))
print('    CONTROL the yaml: golden tree == head: %s (the goldens carry no yaml: must be False)' % yeq)
chk('S4 goldens byte-equal', all(rc == 0 for _, rc, _ in offs) and len(offs) == len(K['goldens']) and all(eqs.values()) and not yeq,
    '%d of %d non-yaml paths blob-equal to the six goldens applied in order; yaml control differs: %s' % (sum(eqs.values()), len(nonyaml), not yeq))
# S5
reds = []; ctl = 0
for p in sorted(x for x in names if '/__tests__/' in x):
    t = git('show', '%s:%s' % (H, p)); r = re.findall(r"it\('RED KS-1364 ([A-Z]{2}\d)", t); c = len(re.findall(r"it\('control KS-1364", t)); reds += r; ctl += c
    imps = re.findall(r"^import .*?from '([^']+)'|^import '([^']+)'", t, re.M)
    print('    %s: RED %s | control %d | imports %s' % (p.split('/')[-1], r, c, sorted(set(a or b for a, b in imps))))
chk('S5 red cells', sorted(reds) == sorted(K['red_cells']), '%d RED cells %s == kit red_cells: %s | %d control cells' % (len(reds), sorted(reds), sorted(reds) == sorted(K['red_cells']), ctl))
# S6
out = [p for p in names if not any(p.startswith(a) for a in K['allowed_prefixes'])]
rt = [p for p in names if p.endswith('.ts') and '/__tests__/' not in p and not p.endswith('.openapi.ts')]
mv = [p for p in git('diff', '--name-only', DEV + '^', DEV).split()]
chk('S6 no runtime path', not out and not rt, 'paths outside the allowed prefixes %s | non-test non-openapi source paths %s | CONTROL the same listing on develop^..develop (#1364) reads %d path(s): %s' % (out or 'NONE', rt or 'NONE', len(mv), mv))
nf = res.count(False)
print('SPECDIFF %s: %d FAIL of %d checks | base %s | head %s' % ('PASS' if nf == 0 else 'FAIL', nf, len(res), DEV[:12], H[:12]))
raise SystemExit(1 if nf else 0)
