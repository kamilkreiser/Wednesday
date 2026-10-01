#!/usr/bin/env python3
"""images_gate53.py — the drafter's prediction for requirement 6: does ANY image build copy a lock this PR changes (the workspace-root
`Blockchain/Dev/package-lock.json`)? Static, from blobs at the head (overridable). No docker, no build.
  I1 every tracked Dockerfile (`(^|/)Dockerfile[^/]*$`, counted and printed, with the count inside Blockchain/Dev beside it);
  I2 every COPY / ADD line that is not `--from=` (a stage copy reads the stage, never the build context), with each SOURCE token classified:
       ROOT-LOCK   the source names the root lock's context-relative path (`package-lock.json`, `package*.json`, `package-lock*`, `*.json`, `*`)
                   at the context ROOT, or `.` / `./` (the whole context) — its effect depends on the build CONTEXT;
       PER-DIR     a source under a directory (`services/x/package*.json`, `packages/shared/`, ...) — cannot be the root lock;
     a ROOT-LOCK source is RESOLVED against every compose `build:` that names that Dockerfile (context + dockerfile, all compose files
     parsed as YAML, compose's `!reset`/`!override` tags read as null; an unreadable compose file FAILS); it HITS when its context IS `Blockchain/Dev` (the directory holding the root lock); a ROOT-LOCK source whose
     Dockerfile no compose file builds is UNRESOLVED and FAILS (the instrument will not guess a context).
  I3 CONTROL that must hit: kit dockerfile_control (`services/originate/Dockerfile:28 COPY services/originate/package*.json ./`) is found as a
     PER-DIR manifest copy at that line; and the originate image's prisma lines are printed (COPY prisma/, npx prisma generate).
PASS = 0 HITS, 0 UNRESOLVED, the control found. Override (controls): --tree <sha>. rc 0 PASS / rc 1 FAIL. Usage: images_gate53.py <scratchpad> [--tree sha]"""
import json, os, re, subprocess, sys, posixpath, datetime
import yaml
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate53.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
def opt(n, d=None): return A[A.index(n) + 1] if n in A else d
CL = os.path.join(SP, 'g53_sp', 'clone'); N = K['order'][0]
def git(*a): return subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True).stdout
T = git('rev-parse', opt('--tree', P['pr_pins'][N]['head']) + '^{commit}').strip()
ROOTDIR = posixpath.dirname(K['root_lock'])   # Blockchain/Dev
print('images_gate53 %s | tree %s%s | root lock %s' % (datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), T[:12], ' (OVERRIDDEN)' if opt('--tree') else '', K['root_lock']))
allf = git('ls-tree', '-r', '--name-only', T).splitlines()
DF = [f for f in allf if re.search(r'(^|/)Dockerfile[^/]*$', f)]
CF = [f for f in allf if re.search(r'(^|/)(docker-)?compose[^/]*\.ya?ml$', f)]
print('I1 %d tracked Dockerfiles (%d inside %s/, %d outside: %s) | %d compose files' % (len(DF), sum(f.startswith(ROOTDIR + '/') for f in DF), ROOTDIR,
      sum(not f.startswith(ROOTDIR + '/') for f in DF), [f for f in DF if not f.startswith(ROOTDIR + '/')], len(CF)))
class Loader(yaml.SafeLoader): pass
Loader.add_multi_constructor('!', lambda ld, suffix, node: None)   # compose's own tags (`!reset`, `!override`) read as null, never a parse failure
BUILDS = {}; UNREADABLE = []   # dockerfile path -> set of context dirs (repo-relative)
for cf in CF:
    try: y = yaml.load(git('show', '%s:%s' % (T, cf)), Loader=Loader) or {}
    except Exception as e: UNREADABLE.append(cf); print('UNREADABLE compose %s: %s' % (cf, str(e)[:80])); continue
    for name, svc in ((y.get('services') or {}) if isinstance(y, dict) else {}).items():
        b = (svc or {}).get('build')
        if not b: continue
        ctx, dfn = (b, 'Dockerfile') if isinstance(b, str) else (b.get('context', '.'), b.get('dockerfile', 'Dockerfile'))
        cdir = posixpath.normpath(posixpath.join(posixpath.dirname(cf), str(ctx)))
        BUILDS.setdefault(posixpath.normpath(posixpath.join(cdir, str(dfn))), set()).add(cdir)
ROOTISH = re.compile(r'^(\./)?(package-lock\.json|package\*\.json|package-lock\*|package-lock\.json\*|\*\.json|\*|\.|)$')
hits, unres, manif, ctl_found = [], [], 0, False
dc = K['dockerfile_control']
for f in DF:
    for i, l in enumerate(git('show', '%s:%s' % (T, f)).split('\n'), 1):
        m = re.match(r'^\s*(COPY|ADD)\s+(.*)$', l, re.I)
        if not m: continue
        toks = [t for t in m.group(2).split() if not t.startswith('--')]
        if any(t.startswith('--from') for t in m.group(2).split()): continue
        if len(toks) < 2: continue
        for s in toks[:-1]:
            if ROOTISH.match(s.rstrip('/')) or s in ('.', './'):
                ctxs = BUILDS.get(posixpath.normpath(f)) or set()
                if not ctxs: unres.append('%s:%d %s' % (f, i, l.strip())); print('UNRESOLVED %s:%d `%s` — source %r reads the context root and no compose build names this Dockerfile' % (f, i, l.strip(), s)); continue
                for c in sorted(ctxs):
                    hit = c == ROOTDIR
                    print('%s %s:%d `%s` — source %r at the context root, context %s' % ('HIT ' if hit else 'ROOT-CTX-OTHER', f, i, l.strip(), s, c))
                    if hit: hits.append('%s:%d' % (f, i))
            elif re.search(r'package(-lock)?[*.]', s): manif += 1
        if f == dc['path'] and i == dc['line'] and l.strip() == dc['text']: ctl_found = True
for f in [dc['path']]:
    for i, l in enumerate(git('show', '%s:%s' % (T, f)).split('\n'), 1):
        if re.search(r'prisma', l, re.I) and re.match(r'^\s*(COPY|RUN)', l): print('INFO %s:%d %s' % (f, i, l.strip()))
print('I2 per-directory manifest COPY sources: %d | ROOT-LOCK hits (context %s): %d %s | UNRESOLVED: %d' % (manif, ROOTDIR, len(hits), hits, len(unres)))
print('I3 CONTROL %s:%d `%s` found: %s' % (dc['path'], dc['line'], dc['text'], ctl_found))
print('I1b compose files parsed %d of %d | builds resolved: %d Dockerfile path(s) | unreadable %s' % (len(CF) - len(UNREADABLE), len(CF), len(BUILDS), UNREADABLE or 'NONE'))
ok = not hits and not unres and not UNREADABLE and ctl_found and manif > 0
print('IMAGES %s: %d Dockerfiles, %d image(s) copy the root lock, %d unresolved, control %s | tree %s' % ('PASS' if ok else 'FAIL', len(DF), len(hits), len(unres), 'FIRED' if ctl_found else 'DID NOT FIRE', T[:12]))
raise SystemExit(0 if ok else 1)
