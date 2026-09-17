#!/usr/bin/env python3
"""drafter_r2.py — #1018 (KS-1050) TIER 2 ROUND 2 delta drafter runs, in the EXISTING drafter clone only (never the Secuura checkout; cwd inside the clone).
1. Trees: worktrees wt_r2head (efd677e98) and wt_r2dev (develop 19f1e5475) added IN THE CLONE; merge-tree --write-tree re-derivation of the seat's two
   merge-ins (267bd8624 x efaaa6034 = tree of 9c66589bb, predicted 0d351b735; c08cec102 x 19f1e5475 = tree of efd677e98, predicted ce49c7bfd); the round-2
   change's own files; what each merge brought; auth/shared subtrees; develop an ancestor of the head. node_modules farmed PER ENTRY, shared dist per tree.
2. Whole auth vitest (json) + project tsc at develop 19f1e5475 and head efd677e98.
3. At the head: the seat's 9 rows re-derived (T0, RP-BASE, RP-R1, TN-a, TN-b, TS, TI, G-MSG, G-NULLONLY) + the drafter's D-HELPER-MSG (a tamper INSIDE
   updateUserOrThrow's message that the ks1050 cells must see: proves the harness runs the real helper) and D-LOG-EARLY (the success log moved BEFORE the
   helper call). Each row: anchor count 1 + marker, tsc rc (VOID if != 0), WHOLE auth suite, reds per file split ASSERTION vs TIMEOUT, restore by bytes +
   sha256 + git diff --quiet. Never rm. Listener census before/after (LISTEN rows; node argv login_stub.mjs count)."""
import json, subprocess, datetime, os, hashlib, re
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018'
REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
paths = json.load(open(GS + '/out/drafter_paths.json')); W = paths['W']; C = paths['C']
S = dict(head='efd677e98c917a52f8af442c9fcfde756166070e', r2='c08cec102cac7ce6bea66d9a0b38acfcac19c6bb', m1='9c66589bb889c82b1ba3fa7d3e19e064f5deeb54',
         r1='267bd8624ce276ca62160216d042b8477bac52f1', d1='efaaa6034f036dd9538ee35b189217b1d08b90a9', dev='19f1e54750ce2b65312a687add2db4f5628edb7d',
         base='7e89318bcedbc9a35757d4298ace54a6a23020bd')
DEV = 'Blockchain/Dev'; A = DEV + '/services/auth'
USERS = A + '/src/routes/users.ts'; REPOF = A + '/src/repositories/userRepo.ts'; T = 'src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts'
def P(*a): print(' '.join(str(x) for x in a), flush=True)
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def run(c, cwd=None): p = subprocess.run(c, cwd=cwd, capture_output=True, text=True); return p.returncode, p.stdout.strip(), p.stderr.strip()
def g(*a): return run(['git', '-C', C] + list(a))
def census():
    lis = len(subprocess.run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True).stdout.splitlines()[1:])
    stubs = [l for l in subprocess.run(['ps', '-ax', '-o', 'pid=,command='], capture_output=True, text=True).stdout.splitlines() if re.match(r'\s*\d+\s+node\s.*login_stub\.mjs', l)]
    return lis, len(stubs)
P('drafter_r2', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| LISTEN rows / node login_stub.mjs BEFORE', census())
P('source checkout BEFORE | worktrees', len(os.listdir(REPO + '/.git/worktrees')), '| porcelain', len(run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])[1].splitlines()))
for k in S: P('object', k, S[k][:9], g('cat-file', '-t', S[k])[1])
tree = lambda x: g('rev-parse', x + '^{tree}')[1]
P('parents', {k: g('rev-list', '--parents', '-n', '1', S[k])[1].split()[1:] for k in ('head', 'r2', 'm1')})
rc, o, e = g('merge-tree', '--write-tree', S['r1'], S['d1']); mt1 = o.split('\n')[0]
P('merge-in 1: merge-tree 267bd8624 x efaaa6034 rc', rc, 'tree', mt1, '| tree(9c66589bb)', tree(S['m1']), 'EQUAL' if mt1 == tree(S['m1']) else 'DIFFER', '| seat prediction 0d351b735 match', mt1.startswith('0d351b735'))
rc, o, e = g('merge-tree', '--write-tree', S['r2'], S['dev']); mt2 = o.split('\n')[0]
P('merge-in 2: merge-tree c08cec102 x 19f1e5475 rc', rc, 'tree', mt2, '| tree(efd677e98)', tree(S['head']), 'EQUAL' if mt2 == tree(S['head']) else 'DIFFER', '| seat prediction ce49c7bfd match', mt2.startswith('ce49c7bfd'))
P('round-2 change c08cec102^..c08cec102 files:', g('diff', '--numstat', S['m1'], S['r2'])[1].replace('\n', ' | '))
P('merge-in 1 brought (267bd8624 -> 9c66589bb):', g('diff', '--name-only', S['r1'], S['m1'])[1].replace('\n', ' | '))
P('  = develop delta 7e89318bc -> efaaa6034:', g('diff', '--name-only', S['base'], S['d1'])[1].replace('\n', ' | '))
P('  check: 267bd8624 -> 9c66589bb minus develop delta empty:', sorted(set(g('diff', '--name-only', S['r1'], S['m1'])[1].split()) - set(g('diff', '--name-only', S['base'], S['d1'])[1].split())))
P('merge-in 2 brought (c08cec102 -> efd677e98):', g('diff', '--name-only', S['r2'], S['head'])[1].replace('\n', ' | '), '| develop delta efaaa6034 -> 19f1e5475:', g('diff', '--name-only', S['d1'], S['dev'])[1].replace('\n', ' | '))
P('develop 19f1e5475 -> head files (the PR delta):', g('diff', '--name-status', S['dev'], S['head'])[1].replace('\n', ' | '))
P('blobs at head: users.ts', g('rev-parse', S['head'] + ':' + USERS)[1][:9], 'test', g('rev-parse', S['head'] + ':' + A + '/' + T)[1][:9], '| same at c08cec102:', g('rev-parse', S['r2'] + ':' + USERS)[1] == g('rev-parse', S['head'] + ':' + USERS)[1], g('rev-parse', S['r2'] + ':' + A + '/' + T)[1] == g('rev-parse', S['head'] + ':' + A + '/' + T)[1])
for sub in (A, DEV + '/packages/shared'):
    P('subtree', sub.split('/')[-1], {k: g('rev-parse', S[k] + ':' + sub)[1][:9] for k in ('base', 'dev', 'r2', 'head')})
P('develop 19f1e5475 ancestor of head: rc', g('merge-base', '--is-ancestor', S['dev'], S['head'])[0], '(0 = yes)')
P('develop auth unchanged since the PR parent 7e89318bc:', g('diff', '--name-only', S['base'], S['dev'], '--', A)[1] or 'NONE')
def farm_dir(src, dst, rewrite):
    os.mkdir(dst); n = 0
    for ent in sorted(os.listdir(src)):
        if ent in ('.vite', '.vitest', '.cache'): continue
        s = os.path.join(src, ent)
        if rewrite and ent == '@secuura':
            os.mkdir(os.path.join(dst, ent))
            for sub in sorted(os.listdir(s)): os.symlink(os.path.normpath(os.path.join(dst, ent, os.readlink(os.path.join(s, sub)))), os.path.join(dst, ent, sub))
        else: os.symlink(s, os.path.join(dst, ent))
        n += 1
    return n
trees = {}
for name, sha in (('r2head', S['head']), ('r2dev', S['dev'])):
    wt = W + '/wt_' + name; rc, o, e = g('worktree', 'add', '--detach', '--quiet', wt, sha); assert rc == 0, e; trees[name] = wt
    n = [farm_dir(os.path.join(REPO, DEV, r, 'node_modules'), os.path.join(wt, DEV, r, 'node_modules'), r == '') for r in ('', 'packages/shared', 'services/auth')]
    b = subprocess.run([wt + '/' + DEV + '/node_modules/.bin/tsc', '-p', '.'], cwd=wt + '/' + DEV + '/packages/shared', capture_output=True, text=True).returncode
    r = subprocess.run(['node', '-e', "const r=require('fs').realpathSync(require.resolve('@secuura/shared'));console.log(r.startsWith(process.argv[1]) ? 'IN TREE' : 'OUTSIDE TREE')", wt], cwd=wt + '/' + A + '/src', capture_output=True, text=True).stdout.strip()
    P('tree', name, sha[:9], '| farm per entry', n, '| shared dist rc', b, '| @secuura/shared from auth', r)
def suite(tree, tag):
    out = GS + '/out_r2/suite_%s.json' % tag
    p = subprocess.run([tree + '/' + DEV + '/node_modules/.bin/vitest', 'run', '--reporter=json', '--outputFile=' + out], cwd=tree + '/' + A, capture_output=True, text=True, env=dict(os.environ, CI='1'))
    j = json.load(open(out)); reds = {}
    for s in j['testResults']:
        f = [a for a in s['assertionResults'] if a['status'] == 'failed']
        if f or s['status'] != 'passed':
            kinds = ['TIMEOUT' if 'STACK_TRACE_ERROR' in (a.get('failureMessages') or [''])[0] or 'timed out' in (a.get('failureMessages') or [''])[0] else 'ASSERT' for a in f]
            reds[s['name'].split('/src/')[-1]] = dict(n=len(f), kinds=kinds, cells=[a['title'][:48] + ' :: ' + re.sub(r'\s+', ' ', (a.get('failureMessages') or [''])[0])[:110] for a in f][:4], msg=(s.get('message') or '')[:160])
    return dict(files=len(j['testResults']), tests=j['numTotalTests'], failed=j['numFailedTests'], pending=j['numPendingTests']), reds
for name in ('r2dev', 'r2head'):
    t0 = now(); d, reds = suite(trees[name], name)
    tsc = subprocess.run([trees[name] + '/' + DEV + '/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=trees[name] + '/' + A, capture_output=True, text=True).returncode
    P('SUITE', name, t0, '->', now(), d, '| tsc rc', tsc, '| non-passing', reds)
HT = trees['r2head']; FU = HT + '/' + USERS; FR = HT + '/' + REPOF
ORIG = {FU: open(FU, 'rb').read(), FR: open(FR, 'rb').read()}; SHA0 = {k: hashlib.sha256(v).hexdigest() for k, v in ORIG.items()}
CALL = "    const updated = await userRepo.updateUserOrThrow(user.id, updates, 'Profile update');\n"
LOGL = "    logger.info('User profile updated', { userId: user.id });\n"
NULLB = "  if (!updated) {\n    logger.error('User update could not be confirmed — refusing to report success', {\n"
THROW = "    throw new ServiceUnavailableError(\n      `${operation} could not be confirmed. Please retry — if you already succeeded, you may not need to.`,\n    );\n"
MSG = "Profile update could not be confirmed. Please retry — if you already succeeded, you may not need to."
def blob(sha, path): return subprocess.run(['git', '-C', C, 'show', sha + ':' + path], capture_output=True).stdout
ROWS = [
  ('T0', None),
  ('RP-BASE', ('swap', FU, blob(S['base'], USERS))),
  ('RP-R1', ('swap', FU, blob(S['r1'], USERS))),
  ('TN-a', ('edit', FR, NULLB, "  if (!updated) {\n    if (Date.now() > 0) return updated as unknown as User; // QA-TAMPER TN-a\n    logger.error('User update could not be confirmed — refusing to report success', {\n")),
  ('TN-b', ('edit', FU, CALL, "    const updated = await userRepo.updateUser(user.id, updates); // QA-TAMPER TN-b\n")),
  ('TS', ('edit', FR, THROW, "    throw Object.assign(new ServiceUnavailableError(\n      `${operation} could not be confirmed. Please retry — if you already succeeded, you may not need to.`,\n    ), { statusCode: 200 }); // QA-TAMPER TS\n")),
  ('TI', ('edit', FU, CALL, "    const updated = await userRepo.updateUserOrThrow(user.id, updates, 'Profile update'); // QA-TAMPER TI inert\n")),
  ('G-MSG', ('edit', FU, CALL, "    const updated = await userRepo.updateUserOrThrow(user.id, updates, 'Profile change'); // QA-TAMPER G-MSG\n")),
  ('G-NULLONLY', ('edit', FU, CALL, "    const updated = await userRepo.updateUser(user.id, updates); // QA-TAMPER G-NULLONLY\n    if (updated === null) throw new ServiceUnavailableError('" + MSG + "');\n")),
  ('D-HELPER-MSG', ('edit', FR, THROW, "    throw new ServiceUnavailableError( // QA-TAMPER D-HELPER-MSG\n      `${operation} could not be confirmed and was not applied. Please retry — if you already succeeded, you may not need to.`,\n    );\n")),
  ('D-LOG-EARLY', ('edit', FU, CALL + LOGL, LOGL.rstrip('\n') + " // QA-TAMPER D-LOG-EARLY\n" + CALL)),
]
rows = {}
for tag, form in ROWS:
    t0 = now(); note = 'no edit'
    if form and form[0] == 'swap':
        open(form[1], 'wb').write(form[2]); note = 'users.ts blob swap ' + hashlib.sha1(b'blob %d\0' % len(form[2]) + form[2]).hexdigest()[:9]
    elif form:
        _, f, old, new = form; s = ORIG[f].decode(); c = s.count(old); assert c == 1, (tag, 'anchor', c)
        s = s.replace(old, new); assert s.count('QA-TAMPER') == 1, tag; open(f, 'w').write(s); note = 'anchor 1 in ' + f.split('/')[-1]
    tsc = subprocess.run([HT + '/' + DEV + '/node_modules/.bin/tsc', '--noEmit', '-p', '.'], cwd=HT + '/' + A, capture_output=True, text=True)
    d, reds = suite(HT, 'tamper_' + tag)
    for f, b in ORIG.items(): open(f, 'wb').write(b)
    ok = all(hashlib.sha256(open(f, 'rb').read()).hexdigest() == SHA0[f] for f in ORIG); dq = subprocess.run(['git', '-C', HT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode
    k = reds.get('__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts', {})
    other = {f: (v['n'], v['kinds'].count('TIMEOUT')) for f, v in reds.items() if 'ks1050' not in f}
    rows[tag] = dict(note=note, tsc=tsc.returncode, suite=d, ks1050=k, other=other, restored=ok, diff_quiet=dq)
    P('ROW', tag, t0, '->', now(), '|', note, '| tsc rc', tsc.returncode, (tsc.stdout + tsc.stderr).strip()[:160], '|', d, '| ks1050 reds', k.get('n', 0), k.get('kinds'), k.get('cells'), '| other (n, timeouts)', other, '| restored', ok, 'diff --quiet', dq)
json.dump(rows, open(GS + '/out_r2/tamper_rows.json', 'w'), indent=1, ensure_ascii=False)
P('source checkout AFTER | worktrees', len(os.listdir(REPO + '/.git/worktrees')), '| porcelain', len(run(['git', '-C', REPO, '--no-optional-locks', 'status', '--porcelain'])[1].splitlines()))
P('drafter_r2 end', now(), '| LISTEN rows / node login_stub.mjs AFTER', census())
