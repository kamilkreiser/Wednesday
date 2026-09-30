#!/usr/bin/env python3
"""reach_gate50a.py — the drafter's READ (git plumbing only: no build, no install) behind RUNTIME-REACH and SHARED-GUARD-TESTS, at a NAMED tree
(default the pinned head):
  R1 IMAGE REACH: every Dockerfile at the tree; its COPY/ADD lines naming a package manifest or lock, resolved against the compose build context
     that uses it (compose `context:` + `dockerfile:` pairs, every compose file); which tracked lock each line copies; whether that lock is one of
     the 18; the stage that copies it and whether that stage (or a later COPY --from of its node_modules) reaches the FINAL stage, with the
     `npm ci` / `npm prune` flags (--omit=dev ⇒ PROD entries only). ROOT-LOCK: a bare `package-lock.json` / `package*.json` from a context that
     IS Blockchain/Dev copies the workspace-root lock — counted (gate49a: 0). CONTROL: the same matcher finds services/kyc's own
     `services/kyc/package-lock.json` COPY (a matcher that finds nothing proves nothing).
  R2 per image whose copied lock moved: the PROD moves and dev moves in THAT lock (from lockdelta's measurement at this tree) — which moved
     versions can be in the served image (PROD) and which only in a builder stage (dev).
  R3 SHARED-GUARD-TESTS: for each of the 4 changed paths, `git grep -l -F` of (a) the full repo path and (b) the path relative to
     Blockchain/Dev — every TEST file that names it (test / spec / __tests__ / tests/ / *.test.* / *_test.sh / *.bats); and every test file that
     names the generic `package-lock.json` (the lock-discovery / cleanroom / preflight guards that read EVERY lock). CONTROLS: the matcher finds
     `advisory-fetch-stub.mjs` in gate-exit-codes.test.mjs (fires) and a nonsense path in 0 files.
rc 0 REACH READ (controls hold) / rc 1. Writes nothing. Usage: reach_gate50a.py <scratchpad> [--tree <sha>] [--pins <name>]"""
import json, os, re, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
PF = 'pins_gate50a.SIM-%s.json' % A[A.index('--pins') + 1] if '--pins' in A else 'pins_gate50a.json'
P = json.load(open(os.path.join(G, PF), encoding='utf-8'))
CL = os.path.join(SP, 'g50a_sp', 'clone'); DEV = P['develop']; T = A[A.index('--tree') + 1] if '--tree' in A else P['pr_pins']['head']
N = P['pr']; FILES = sorted(K['prs'][N if N in K['prs'] else '<PR>']['files'])
def git(*a, ok=(0,)):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True)
    if r.returncode not in ok: raise SystemExit('REFUSING: git %s rc %d %s' % (' '.join(a[:3]), r.returncode, r.stderr[:200]))
    return r.stdout
T = git('rev-parse', T + '^{commit}').strip()
files = git('ls-tree', '-r', '--name-only', T).splitlines(); nm = lambda f: '/node_modules/' in '/' + f
dfs = sorted(f for f in files if re.search(r'(^|/)Dockerfile[^/]*$', f) and not nm(f))
comp = sorted(f for f in files if re.search(r'(^|/)(docker-)?compose[^/]*\.ya?ml$', f) and not nm(f))
locks = set(f for f in files if f.endswith('package-lock.json') and not nm(f))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print('reach_gate50a %s | tree %s (%s) | %d Dockerfile(s) | %d compose file(s) | %d tracked locks' % (now, T, 'the pinned head' if T == P['pr_pins']['head'] else ('develop' if T == DEV else 'OTHER'), len(dfs), len(comp), len(locks)))
# the moves at THIS tree vs develop (flags from the head entries)
MV = {}
for lk in FILES:
    try: b, h = json.loads(git('show', '%s:%s' % (DEV, lk)))['packages'], json.loads(git('show', '%s:%s' % (T, lk)))['packages']
    except Exception: continue
    MV[lk] = [(k, b[k].get('version'), h[k].get('version'), 'dev' if (h[k].get('dev') or h[k].get('devOptional')) else 'PROD') for k in sorted(set(b) & set(h)) if b[k] != h[k]]
# R1
ctxs = []
for c in comp:
    base = os.path.dirname(c)
    for l in git('show', '%s:%s' % (T, c)).splitlines():
        m = re.match(r'\s*context:\s*["\']?([^"\'#\s]+)', l)
        if m: ctxs.append([c, os.path.normpath(os.path.join(base, m.group(1))), None]); continue
        m = re.match(r'\s*dockerfile:\s*["\']?([^"\'#\s]+)', l)
        if m and ctxs and ctxs[-1][2] is None and ctxs[-1][0] == c: ctxs[-1][2] = os.path.normpath(os.path.join(ctxs[-1][1], m.group(1)))
for x in ctxs:
    if x[2] is None: x[2] = os.path.join(x[1], 'Dockerfile')
print('R1 IMAGE REACH: %d compose build context(s); every Dockerfile COPY/ADD naming a manifest or lock, the lock it copies, and whether it moved' % len(ctxs))
ROOT = 'Blockchain/Dev'; rootc = []; ctl = False; rows = []; ncopy = 0
for d in dfs:
    uses = sorted(set(x[1] for x in ctxs if x[2] == d)); stage = None; stages = []; ci = []
    for l in git('show', '%s:%s' % (T, d)).splitlines():
        m = re.match(r'\s*FROM\s+\S+(?:\s+AS\s+(\S+))?', l, re.I)
        if m: stage = m.group(1) or '(final/unnamed #%d)' % (len(stages) + 1); stages.append(stage); continue
        if re.search(r'\bnpm\s+(ci|install|prune)\b', l): ci.append('%s: %s' % (stage, l.strip()[:90]))
        if not re.match(r'\s*(COPY|ADD)\b', l, re.I) or re.search(r'--from=', l) or not re.search(r'package(-lock)?\.json|package\*\.json', l): continue
        ncopy += 1; toks = [t for t in l.split()[1:] if not t.startswith('--')]; srcs = toks[:-1]; got = []
        for ctx in (uses or [None]):
            for s in srcs:
                if 'lock' not in s and '*' not in s: continue
                cand = os.path.normpath(os.path.join(ctx, s.replace('package*.json', 'package-lock.json'))) if ctx else None
                if cand in locks: got.append(cand)
        bare = [s for s in srcs if re.fullmatch(r'(\./)?(package-lock\.json|package\*\.json)', s)]
        isroot = bool(bare) and ROOT in uses
        if isroot: rootc.append((d, l.strip()))
        if d == 'Blockchain/Dev/services/kyc/Dockerfile' and 'Blockchain/Dev/services/kyc/package-lock.json' in got: ctl = True
        moved = [g for g in got if g in FILES and MV.get(g)]   # a lock that MOVED at this tree (vs develop), not merely one of the 18
        rows.append(dict(dockerfile=d, stage=stage, line=l.strip(), ctx=uses, locks=got, moved=moved, root=isroot))
        if moved or isroot or not uses: print('    %-5s %-58s stage %-16s ctx %-16s %s -> %s' % ('ROOT' if isroot else ('MOVED' if moved else '?'), d[:58], str(stage)[:16], ','.join(uses) or '(none)', l.strip()[:80], got or '(unresolved: no compose context)'))
    if any(r['dockerfile'] == d and r['moved'] for r in rows):
        print('          stages %s | npm lines: %s' % (stages, ' ; '.join(ci)))
img = sorted(set(r['dockerfile'] for r in rows if r['moved']))
print('R1 %d Dockerfile(s) copy a MOVED lock: %s' % (len(img), img))
print('R1 ROOT-LOCK copies (a bare lock / package*.json from a context that IS %s): %d %s | Dockerfiles with a manifest COPY and NO compose context (the gate resolves): %s' % (
    ROOT, len(rootc), rootc or '', sorted(set(r['dockerfile'] for r in rows if not r['ctx'])) or 'none'))
print('R1 CONTROL: the matcher finds services/kyc/Dockerfile\'s own `services/kyc/package-lock.json` COPY: %s | %d manifest/lock COPY line(s) read' % (ctl, ncopy))
# R2
print('R2 the moves inside each copied lock (PROD may reach the served image; dev only a builder stage)')
for d in img:
    for lk in sorted(set(g for r in rows if r['dockerfile'] == d for g in r['moved'])):
        pr = [m for m in MV.get(lk, []) if m[3] == 'PROD']; dv = [m for m in MV.get(lk, []) if m[3] != 'PROD']
        print('    %-58s %-52s PROD %s | dev %s' % (d[:58], lk, ['%s %s->%s' % (m[0].rsplit('node_modules/', 1)[-1], m[1], m[2]) for m in pr] or 'none', ['%s %s->%s' % (m[0].rsplit('node_modules/', 1)[-1], m[1], m[2]) for m in dv] or 'none'))
# R3
TST = re.compile(r'(^|/)(tests?|__tests__|spec)/|\.(test|spec)\.[cm]?[jt]sx?$|_test\.sh$|\.bats$|(^|/)test_[^/]*\.(sh|py)$')
def gg(s):
    r = subprocess.run(['git', '-C', CL, 'grep', '-l', '-F', s, T], capture_output=True, text=True)
    return sorted(set(x.split(':', 1)[1] for x in r.stdout.splitlines() if ':' in x))
print('R3 SHARED-GUARD-TESTS at %s: test files naming each changed path (full path, or relative to Blockchain/Dev)' % T[:12])
allt = set()
for p in FILES:
    rel = p[len('Blockchain/Dev/'):] if p.startswith('Blockchain/Dev/') else None
    hits = sorted(set(gg(p) + (gg(rel) if rel else [])))
    th = [h for h in hits if TST.search(h)]; allt |= set(th)
    print('    %-52s %d file(s) name it, %d test(s): %s' % (p, len(hits), len(th), th or '-'))
gen = [h for h in gg('package-lock.json') if TST.search(h)]
print('R3 test files naming the GENERIC `package-lock.json` (guards over every lock): %d: %s' % (len(gen), gen))
c1 = 'Blockchain/Dev/scripts/audit/gate-exit-codes.test.mjs' in gg('advisory-fetch-stub.mjs'); c0 = gg('zz-gate50a-no-such-path/package-lock.json')
print('R3 CONTROLS: `advisory-fetch-stub.mjs` found in gate-exit-codes.test.mjs: %s | a nonsense path found in %d file(s)' % (c1, len(c0)))
ok = ctl and c1 and not c0
print('REACH %s: tree %s | %d image Dockerfile(s) copy a moved lock | root-lock copies %d | %d test file(s) name a changed path, %d name the generic lock | controls %s' % (
    'READ' if ok else 'FAILED', T[:12], len(img), len(rootc), len(allt), len(gen), 'hold' if ok else 'FAILED'))
raise SystemExit(0 if ok else 1)
