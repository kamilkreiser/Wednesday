#!/usr/bin/env python3
"""c6_reach_gate72.py — RUNTIME REACH for #1406 (KS-1437), from Dockerfile READS at a sha (git show; no image built, no Docker).
[g72] NEW — gate70 had no reach question. The builder MEASURED a reach table (READY :55-:64); this re-measures it with an
independent stage parser and controls, so the gate never copies the builder's numbers.

  reach --repo R --rev REV [--json-out F]          (REQUIRED: --repo --rev)
    CENSUS  Dockerfiles at REV under TWO definitions, both printed: (a) basename == Dockerfile / Dockerfile.* / *.Dockerfile;
            (b) any tracked path containing "dockerfile" case-insensitively (the builder's "38" may be (b): it counts
            scripts/check-dockerfile-non-root.sh). COPY lines naming package*.json / package.json / package-lock.json counted.
    STAGES  every FROM starts a stage (name = AS <x> or its index); per stage: WORKDIR, COPY (with --from), RUN npm ci|install (+ --omit=dev).
            Build context: from the docker-compose files at REV (build.context + dockerfile), else the Dockerfile's own dir is REPORTED
            as UNRESOLVED (never guessed silently).
    R1  ROOT LOCK: 0 images install from the Blockchain/Dev root package-lock.json (a COPY of `package*.json` / `package-lock.json`
        / `.` from the Blockchain/Dev context root into a stage that then runs npm ci)
    R2  for each changed lock: the images whose FINAL stage carries that lock's node_modules (installed in the final stage, or COPY
        --from a stage that installed it into the copied path), and whether dev deps were omitted; the planned package's dev flag in
        that lock decides whether it ships
    R3  POSITIVE CONTROLS (hand-read at draft): mcp-server ships sdk (Dockerfile :56-:57 final-stage `npm ci --omit=dev` from its own
        lock); anchoring ships pbkdf2 (:38-:39); the shared-builder /shared full `npm ci` (mcp-server :10-:13, :59)
    R4  NEGATIVE CONTROLS: a fabricated stage name matches 0 Dockerfiles; the issuer image's FINAL stage installs NOTHING (nginx serving
        dist — the bundle question is c5's, not this one's)
  --selftest   synthetic Dockerfiles: a root-lock COPY + npm ci FIRES R1; COPY --from a full-ci builder ships dev deps; --omit=dev does not.
rc 0 / 1 / 2 refused."""
import fnmatch, json, os, posixpath, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate72 import K, Tally, git, git_bytes, req, opt, pkg_name

PLAN = K['plan']; DEV = 'Blockchain/Dev'


def logical_lines(text):
    out, cur = [], ''
    for raw in text.split('\n'):
        s = raw.strip()
        if not cur and (not s or s.startswith('#')): continue
        if s.endswith('\\'): cur += s[:-1] + ' '; continue
        cur += s; out.append(cur); cur = ''
    if cur: out.append(cur)
    return out


def stages(text):
    st = []
    for l in logical_lines(text):
        w = l.split(); kw = w[0].upper()
        if kw == 'FROM':
            m = re.search(r'\s+AS\s+(\S+)\s*$', l, re.I)
            st.append({'name': m.group(1) if m else str(len(st)), 'workdir': '/', 'copies': [], 'installs': []})
        elif not st: continue
        elif kw == 'WORKDIR': st[-1]['workdir'] = posixpath.join(st[-1]['workdir'], w[1])
        elif kw in ('COPY', 'ADD'):
            frm = None; args = []
            for x in w[1:]:
                if x.startswith('--from='): frm = x.split('=', 1)[1]
                elif x.startswith('--'): continue
                else: args.append(x)
            if len(args) >= 2:
                dst = args[-1]; dst = dst if dst.startswith('/') else posixpath.join(st[-1]['workdir'], dst)
                st[-1]['copies'].append({'from': frm, 'srcs': args[:-1], 'dst': dst})
        elif kw == 'RUN' and re.search(r'\bnpm\s+(ci|install|i)\b', l):
            st[-1]['installs'].append({'omit_dev': bool(re.search(r'--omit[= ]dev|--production|--only[= ]prod', l)), 'dir': st[-1]['workdir'],
                                       'after_copies': len(st[-1]['copies']), 'line': l[:160]})
    return st


def src_covers(src, lock_rel_ctx):
    """does COPY source `src` (context-relative) bring `lock_rel_ctx` (context-relative path of a package-lock.json)?"""
    s = src.rstrip('/').lstrip('./') if src not in ('.', './') else ''
    d = posixpath.dirname(lock_rel_ctx)
    if s == '': return True                                         # COPY . <dst>
    if fnmatch.fnmatch(lock_rel_ctx, s): return True                # package*.json, services/x/package-lock.json
    return lock_rel_ctx.startswith(s + '/')                          # a directory copy


def stage_installs_lock(stage, lock_rel_ctx):
    """the install records of `stage` whose lock came from `lock_rel_ctx` (a COPY before the install, landing in the install dir)."""
    hits = []
    for ins in stage['installs']:
        for c in stage['copies'][:ins['after_copies']]:
            if c['from'] is None and any(src_covers(s, lock_rel_ctx) for s in c['srcs']):
                dst = c['dst'].rstrip('/') or '/'
                landing = dst if c['dst'].endswith('/') or len(c['srcs']) > 1 or '*' in ''.join(c['srcs']) or c['srcs'][0].endswith('/') else posixpath.dirname(dst)
                if posixpath.normpath(landing) == posixpath.normpath(ins['dir']): hits.append(ins)
    return hits


def final_ships(st, lock_rel_ctx):
    """-> list of (how, omit_dev) by which the FINAL stage carries node_modules installed from lock_rel_ctx."""
    fin = st[-1]; out = [('final-stage npm ci', i['omit_dev']) for i in stage_installs_lock(fin, lock_rel_ctx)]
    byname = dict((s['name'], s) for s in st)
    for c in fin['copies']:
        if c['from'] in byname:
            src_st = byname[c['from']]
            for ins in stage_installs_lock(src_st, lock_rel_ctx):
                for s in c['srcs']:
                    sp = posixpath.normpath(s if s.startswith('/') else posixpath.join(src_st['workdir'], s))
                    nm = posixpath.join(ins['dir'], 'node_modules')
                    if nm == sp or nm.startswith(sp + '/') or sp == posixpath.normpath(ins['dir']):
                        out.append(('COPY --from=%s %s' % (c['from'], s), ins['omit_dev']))
    return out


def compose_contexts(repo, rev):
    ctx = {}
    for f in [l for l in git(repo, 'ls-tree', '-r', '--name-only', rev).split('\n') if re.search(r'docker-compose[^/]*\.ya?ml$', l)]:
        txt = git_bytes(repo, rev, f).decode('utf-8', 'replace'); base = posixpath.dirname(f)
        for m in re.finditer(r'context:\s*(\S+)\s*\n\s*dockerfile:\s*(\S+)', txt):
            c = posixpath.normpath(posixpath.join(base, m.group(1))); d = posixpath.normpath(posixpath.join(c, m.group(2)))
            ctx.setdefault(d, set()).add(c)
    return ctx


def infer_context(f, st, fileset, dirset):
    """[g72] no compose entry: the DEEPEST ancestor of the Dockerfile's dir under which EVERY relative COPY source (no --from, not `.`)
    exists as a tracked file or directory. None if no ancestor fits. Reported as INFERRED, never silently."""
    srcs = [s.rstrip('/') for st_ in st for c in st_['copies'] if c['from'] is None for s in c['srcs'] if s not in ('.', './') and not s.startswith('/')]
    d = posixpath.dirname(f)
    while True:
        ok = bool(srcs)
        for s in srcs:
            full = posixpath.join(d, s) if d else s
            if '*' in s or '?' in s:
                ok &= any(fnmatch.fnmatch(x, full) for x in fileset)
            else:
                ok &= full in fileset or full in dirset
        if ok: return d
        if not d: return None
        d = posixpath.dirname(d)


def is_dockerfile(p):
    b = posixpath.basename(p)
    return b == 'Dockerfile' or b.startswith('Dockerfile.') or b.endswith('.Dockerfile')


def cmd_reach(repo, rev, json_out):
    t = Tally(); files = [l for l in git(repo, 'ls-tree', '-r', '--name-only', rev).split('\n') if l]
    dfa = [f for f in files if is_dockerfile(f)]; dfb = [f for f in files if 'dockerfile' in f.lower()]
    ctx = compose_contexts(repo, rev)
    print('CENSUS at %s: Dockerfiles (a) basename %d | (b) any path containing "dockerfile" %d, extra in (b): %s | compose (context, dockerfile) pairs %d' % (
        rev[:12], len(dfa), len(dfb), sorted(set(dfb) - set(dfa)), len(ctx)))
    changed = sorted(K['pr']['numstat'])
    lock_dev = {}
    for l in changed:
        pk = json.loads(git_bytes(repo, rev, l))['packages']
        for k, e in pk.items():
            if pkg_name(k) in PLAN and k.count('node_modules/') == 1: lock_dev[(l, pkg_name(k))] = bool(e.get('dev') or e.get('devOptional'))
    rows = []; pkg_copy_lines = 0; unresolved = []; inferred = []; root_hits = []; per_pkg = dict((n, set()) for n in PLAN)
    fileset = set(files); dirset = set(posixpath.dirname(x) for x in files)
    while True:
        more = set(posixpath.dirname(d) for d in dirset) - dirset
        if not more: break
        dirset |= more
    for f in sorted(dfa):
        text = git_bytes(repo, rev, f).decode('utf-8', 'replace'); st = stages(text)
        pkg_copy_lines += sum(1 for s in st for c in s['copies'] if any(re.search(r'package(\*|-lock)?\.json', x) for x in c['srcs']))
        cs = ctx.get(f)
        if not cs:
            c = infer_context(f, st, fileset, dirset)
            if c is None:
                if not any(x['copies'] or x['installs'] for x in st): inferred.append('%s -> NO COPY / NO npm (cannot carry a lock)' % f); continue
                unresolved.append(f); continue
            inferred.append('%s -> %s' % (f, c or '<repo root>')); cs = {c}
        for c in sorted(cs):
            if not st: continue
            for l in changed + [K['root_lock']]:
                if not l.startswith(c + '/') and c != '': continue
                lr = l[len(c) + 1:] if c else l
                ships = final_ships(st, lr)
                anyinst = [s['name'] for s in st if stage_installs_lock(s, lr)]
                if l == K['root_lock'] and anyinst: root_hits.append('%s stages %s' % (f, anyinst))
                for how, omit in ships:
                    for (ll, n), isdev in lock_dev.items():
                        if ll == l and not (omit and isdev):
                            per_pkg[n].add(f); rows.append((f, l, n, how, omit))
    for r in rows: print('SHIPS %s <- %s %s via %s (omit-dev %s)' % r)
    print('COPY lines naming package*.json / package.json / package-lock.json: %d (builder: %s)' % (pkg_copy_lines, K['reach_builder_claims']['package_copy_lines']))
    t.check('R0', not unresolved, 'build context for every basename-Dockerfile: from compose %d | INFERRED from its COPY sources %d %s | unresolved %d %s' % (
        len(dfa) - len(inferred) - len(unresolved), len(inferred), inferred, len(unresolved), unresolved[:6]))
    t.check('R1', not root_hits, 'ROOT LOCK: stages installing from %s: %d %s' % (K['root_lock'], len(root_hits), root_hits[:3]))
    t.info('R2', 'images shipping each package: %s' % dict((n, len(v)) for n, v in per_pkg.items()))
    for n, v in per_pkg.items(): print('  %s -> %d: %s' % (n, len(v), [x.replace('Blockchain/Dev/', '').replace('/Dockerfile', '') for x in sorted(v)]))
    mcp = 'Blockchain/Dev/services/mcp-server/Dockerfile'; anc = 'Blockchain/Dev/services/anchoring/Dockerfile'
    t.check('R3', mcp in per_pkg['@modelcontextprotocol/sdk'] and anc in per_pkg['pbkdf2'] and mcp in per_pkg['pbkdf2'],
            'POSITIVE CONTROLS: mcp-server ships sdk %s | anchoring ships pbkdf2 %s | mcp-server ships pbkdf2 via shared-builder /shared %s' % (
                mcp in per_pkg['@modelcontextprotocol/sdk'], anc in per_pkg['pbkdf2'], mcp in per_pkg['pbkdf2']))
    fab = sum(1 for f in dfa if any(s['name'] == 'gate72-fabricated-stage' for s in stages(git_bytes(repo, rev, f).decode('utf-8', 'replace'))))
    iss = stages(git_bytes(repo, rev, 'Blockchain/Dev/frontend/issuer/Dockerfile').decode())
    t.check('R4', fab == 0 and not iss[-1]['installs'], 'NEGATIVE CONTROLS: fabricated stage name matches %d Dockerfiles | issuer FINAL stage installs %d (nginx serving dist)' % (fab, len(iss[-1]['installs'])))
    if json_out:
        json.dump({'rev': rev, 'dockerfiles_a': len(dfa), 'dockerfiles_b': len(dfb), 'package_copy_lines': pkg_copy_lines,
                   'ships': dict((n, sorted(v)) for n, v in per_pkg.items()), 'root_hits': root_hits}, open(json_out, 'w'), indent=1)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    full = 'FROM node AS b\nWORKDIR /shared\nCOPY packages/shared/package*.json ./\nRUN npm ci --ignore-scripts\nFROM node\nWORKDIR /app\nCOPY --from=b /shared /shared\n'
    rep(final_ships(stages(full), 'packages/shared/package-lock.json') == [('COPY --from=b /shared', False)], 'COPY --from a FULL-ci builder ships its node_modules WITH dev deps')
    omit = 'FROM node\nWORKDIR /app\nCOPY services/x/package.json services/x/package-lock.json ./\nRUN npm ci --omit=dev\n'
    rep(final_ships(stages(omit), 'services/x/package-lock.json') == [('final-stage npm ci', True)], 'final-stage `npm ci --omit=dev` ships prod deps only')
    root = 'FROM node\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci\n'
    rep(stage_installs_lock(stages(root)[-1], 'package-lock.json'), 'PLANTED root `COPY package*.json` + npm ci FIRES R1')
    rep(not stage_installs_lock(stages(omit)[-1], 'package-lock.json'), 'a service-dir COPY does not read as the root lock')
    dot = 'FROM node\nWORKDIR /app\nCOPY . .\nRUN npm ci\n'
    rep(stage_installs_lock(stages(dot)[-1], 'package-lock.json'), 'PLANTED `COPY . .` + npm ci FIRES R1 (a whole-context copy carries the root lock)')
    nginx = 'FROM node AS builder\nWORKDIR /app\nCOPY frontend/i/package*.json ./\nRUN npm ci\nFROM nginx\nCOPY --from=builder /app/dist/ /usr/share/nginx/html/\n'
    rep(final_ships(stages(nginx), 'frontend/i/package-lock.json') == [], 'a dist-only COPY --from does NOT ship node_modules')
    rep(len(logical_lines('RUN a \\\n  b\n# c\nRUN d')) == 2, 'continuation lines join; comments drop')
    print('SELFTEST %d/%d' % (sum(res), len(res))); return 0 if all(res) else 1


def main():
    A = sys.argv[1:]
    if '--selftest' in A: return selftest()
    if not A or A[0] != 'reach': print(__doc__); return 2
    try:
        return cmd_reach(req(A, '--repo'), req(A, '--rev', True), opt(A, '--json-out'))
    except SystemExit as e:
        print(e); return 2


if __name__ == '__main__':
    sys.exit(main())
