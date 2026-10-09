#!/usr/bin/env python3
"""c6_reach_gate78.py — RUNTIME REACH for #1435 (KS-1452), from Dockerfile READS at a sha (git show; no image built, no Docker) and an
importer census. Carried from c6_reach_gate72.py; [g78] marks this kit's changes: a node_modules STATE model per stage (an `npm ci`
REPLACES node_modules; `npm prune --omit=dev` makes it prod-only; `COPY --from` carries a stage's state), because governance / referral
prune before their runtime copy and originate's runner re-installs over a full copy. The c5 `omit` install is the runtime measurement;
this is the static read it is compared with.

  reach --repo R --rev REV [--json-out F]          (REQUIRED: --repo --rev)
    CENSUS  Dockerfiles at REV under TWO definitions, both printed: (a) basename == Dockerfile / Dockerfile.* / *.Dockerfile; (b) any
            tracked path containing "dockerfile" case-insensitively. Lock-copying Dockerfiles (a COPY source naming package*.json or
            package-lock.json; builder: 31). The literal `package-lock.json` in Dockerfile COPY sources counted (builder: 8). The literal
            `Dev/package-lock.json` counted (builder: 0).
    STAGES  every FROM starts a stage (name = AS <x> or its index; `FROM <stage>` inherits that stage's state); per stage an ordered event
            list: COPY (with --from), RUN npm ci|install (omit-dev flag), RUN npm prune (--omit=dev / --production). Build context from the
            docker-compose files at REV (context + dockerfile), else INFERRED from the COPY sources and NAMED (never silent).
    R0  every basename-Dockerfile has a context (compose or inferred); 0 unresolved
    R1  ROOT LOCK: 0 stages install from the Blockchain/Dev root package-lock.json
    R2  per changed standalone lock: the images whose FINAL stage's node_modules (at the install dir) came from that lock, and whether it
        is prod-only there (omit at install, or a later prune); the planned package ships iff the state is full, or prod-only and the
        package is NOT `dev` in that lock. Printed per image with the path of events that decided it.
    R3  POSITIVE CONTROL: services/originate ships handlebars (runner :79 `npm ci --omit=dev` from its own lock; handlebars PROD there)
    R4  NEGATIVE CONTROLS: governance and referral (prune --omit=dev before the runtime COPY) and vc-issuer (runner --omit=dev) do NOT ship
        it; a fabricated stage name matches 0 Dockerfiles
    R5  [g78] IMPORTERS: tracked source files (.js .cjs .mjs .ts .tsx .jsx, node_modules / dist excluded) that `require('handlebars')`,
        `import ... from 'handlebars'` or `import('handlebars')` at REV: 0 (builder: 0); CONTROLS on the same instrument: express > 0
        (builder 339), ts-jest named in a config / source file > 0 (builder 14) — the zero is a reading only beside them
  --selftest   synthetic Dockerfiles: root-lock COPY + npm ci FIRES R1; prune after a full ci makes dev deps not ship; a re-install over a
               full COPY replaces it; COPY --from a full-ci builder ships dev deps; the importer regex.
rc 0 / 1 / 2 refused."""
import fnmatch, json, os, posixpath, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate78 import K, Tally, git, git_bytes, req, opt, pkg_name

PLAN = K['plan']; PKG = sorted(PLAN)[0]; RB = K['reach_builder_claims']


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
    for i, l in enumerate(logical_lines(text)):
        w = l.split(); kw = w[0].upper()
        if kw == 'FROM':
            m = re.search(r'\s+AS\s+(\S+)\s*$', l, re.I)
            img = [x for x in w[1:] if not x.startswith('--')][0]
            st.append({'name': m.group(1) if m else str(len(st)), 'from': img, 'workdir': '/', 'events': []})
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
                st[-1]['events'].append({'kind': 'copy', 'from': frm, 'srcs': args[:-1], 'dst': dst, 'dst_raw': args[-1], 'line': l[:160]})
        elif kw == 'RUN' and re.search(r'\bnpm\s+(ci|install|i)\b', l):
            st[-1]['events'].append({'kind': 'install', 'dir': st[-1]['workdir'], 'line': l[:160],
                                     'omit_dev': bool(re.search(r'--omit[= ]dev|--production|--only[= ]prod', l))})
        elif kw == 'RUN' and re.search(r'\bnpm\s+prune\b', l):
            st[-1]['events'].append({'kind': 'prune', 'dir': st[-1]['workdir'], 'line': l[:160],
                                     'omit_dev': bool(re.search(r'--omit[= ]dev|--production', l))})
    return st


def src_covers(src, lock_rel_ctx):
    """does COPY source `src` (context-relative) bring `lock_rel_ctx` (context-relative path of a package-lock.json)?"""
    s = src.rstrip('/').lstrip('./') if src not in ('.', './') else ''
    if s == '': return True                                         # COPY . <dst>
    if fnmatch.fnmatch(lock_rel_ctx, s): return True                # package*.json, services/x/package-lock.json
    return lock_rel_ctx.startswith(s + '/')                          # a directory copy


def landing_dir(ev):
    multi = len(ev['srcs']) > 1 or any('*' in x for x in ev['srcs']) or ev['srcs'][0].endswith('/') or ev['dst_raw'].endswith('/') or ev['dst_raw'] in ('.', './')
    return posixpath.normpath(ev['dst'] if multi else posixpath.dirname(ev['dst']))


def stage_state(st, idx, lock_rel_ctx, memo=None):
    """[g78] -> ({dir: state}, lock_dirs) after every event of stage idx, for node_modules installed from lock_rel_ctx.
    state = {'omit': bool, 'how': [...]}. A stage `FROM <earlier stage>` starts from that stage's end state. lock_dirs = the dirs where
    THIS lock file sits: a no-`--from` COPY of it, or a `COPY --from=<stage>` of a lock file that sat in that stage's lock_dirs.
    An `npm ci|install` in dir d REPLACES d's node_modules: from this lock if d is in lock_dirs, else from some other lock (state dropped).
    `npm prune --omit=dev` makes d prod-only. `COPY --from` of a node_modules dir (or of a dir containing one) carries the state."""
    memo = memo if memo is not None else {}
    if idx in memo: return memo[idx]
    byname = dict((x['name'], i) for i, x in enumerate(st))
    s = st[idx]
    if s['from'] in byname and byname[s['from']] < idx:
        ps, pl = stage_state(st, byname[s['from']], lock_rel_ctx, memo)
        state = dict((d, {'omit': v['omit'], 'how': list(v['how'])}) for d, v in ps.items()); lock_dirs = set(pl)
    else:
        state, lock_dirs = {}, set()
    for ev in s['events']:
        if ev['kind'] == 'copy' and ev['from'] is None:
            if any(src_covers(x, lock_rel_ctx) for x in ev['srcs']): lock_dirs.add(landing_dir(ev))
        elif ev['kind'] == 'copy' and ev['from'] in byname:
            si = byname[ev['from']]; src_st, src_locks = stage_state(st, si, lock_rel_ctx, memo); src_wd = st[si]['workdir']
            for x in ev['srcs']:
                sp = posixpath.normpath(x if x.startswith('/') else posixpath.join(src_wd, x))
                if posixpath.basename(sp) in ('package-lock.json',) and posixpath.dirname(sp) in src_locks:
                    lock_dirs.add(landing_dir(ev))
                for d, v in src_st.items():
                    nm = posixpath.join(d, 'node_modules'); carried = None
                    if sp == nm:
                        dst = ev['dst'].rstrip('/')
                        carried = posixpath.dirname(dst) if posixpath.basename(dst) == 'node_modules' else dst
                    elif sp == posixpath.normpath(d) or d.startswith(sp + '/'):
                        carried = posixpath.join(ev['dst'], posixpath.relpath(d, sp))
                    if carried is not None:
                        state[posixpath.normpath(carried)] = {'omit': v['omit'], 'how': v['how'] + ['COPY --from=%s %s' % (ev['from'], x)]}
        elif ev['kind'] == 'install':
            d = posixpath.normpath(ev['dir'])
            if d in lock_dirs:
                state[d] = {'omit': ev['omit_dev'], 'how': ['npm %s%s at %s' % ('ci', ' --omit=dev' if ev['omit_dev'] else '', d)]}
            elif d in state:
                del state[d]
        elif ev['kind'] == 'prune' and ev['omit_dev']:
            d = posixpath.normpath(ev['dir'])
            if d in state: state[d] = {'omit': True, 'how': state[d]['how'] + ['npm prune --omit=dev at %s' % d]}
    memo[idx] = (state, lock_dirs)
    return memo[idx]


def final_ships(st, lock_rel_ctx, is_dev):
    """-> [(dir, how, omit)] by which the FINAL stage carries node_modules from lock_rel_ctx that hold the package (dev flag is_dev)."""
    fin = stage_state(st, len(st) - 1, lock_rel_ctx)[0]
    return [(d, ' -> '.join(v['how']), v['omit']) for d, v in sorted(fin.items()) if not (v['omit'] and is_dev)]


def any_install_from(st, lock_rel_ctx):
    return [s['name'] for i, s in enumerate(st) if stage_state(st, i, lock_rel_ctx)[0] and any(e['kind'] == 'install' for e in s['events'])]


def compose_contexts(repo, rev):
    ctx = {}
    for f in [l for l in git(repo, 'ls-tree', '-r', '--name-only', rev).split('\n') if re.search(r'docker-compose[^/]*\.ya?ml$', l)]:
        txt = git_bytes(repo, rev, f).decode('utf-8', 'replace'); base = posixpath.dirname(f)
        for m in re.finditer(r'context:\s*(\S+)\s*\n\s*dockerfile:\s*(\S+)', txt):
            c = posixpath.normpath(posixpath.join(base, m.group(1))); d = posixpath.normpath(posixpath.join(c, m.group(2)))
            ctx.setdefault(d, set()).add(c)
    return ctx


def infer_context(f, st, fileset, dirset):
    srcs = [s.rstrip('/') for st_ in st for e in st_['events'] if e['kind'] == 'copy' and e['from'] is None
            for s in e['srcs'] if s not in ('.', './') and not s.startswith('/')]
    d = posixpath.dirname(f)
    while True:
        ok = bool(srcs)
        for s in srcs:
            full = posixpath.join(d, s) if d else s
            ok &= any(fnmatch.fnmatch(x, full) for x in fileset) if ('*' in s or '?' in s) else (full in fileset or full in dirset)
        if ok: return d
        if not d: return None
        d = posixpath.dirname(d)


def is_dockerfile(p):
    b = posixpath.basename(p)
    return b == 'Dockerfile' or b.startswith('Dockerfile.') or b.endswith('.Dockerfile')


IMPORT_RX = r"(?:require\(\s*['\"]%s['\"]\s*\)|from\s+['\"]%s['\"]|import\(\s*['\"]%s['\"]\s*\)|import\s+['\"]%s['\"])"
SRC_EXT = ('.js', '.cjs', '.mjs', '.ts', '.tsx', '.jsx')


def importers(repo, rev, name, files):
    rx = re.compile(IMPORT_RX % ((re.escape(name),) * 4))
    out = []
    for f in files:
        if not f.endswith(SRC_EXT) or '/node_modules/' in f or '/dist/' in f: continue
        try: txt = git_bytes(repo, rev, f).decode('utf-8', 'replace')
        except SystemExit: continue
        if rx.search(txt): out.append(f)
    return out


def mentions(repo, rev, needle, files):
    """files (source or config, json / js / ts) whose text names `needle` as a token — the ts-jest control."""
    rx = re.compile(r'(?<![\w@/-])%s(?![\w-])' % re.escape(needle)); out = []
    for f in files:
        if '/node_modules/' in f or f.endswith('package-lock.json') or not f.endswith(SRC_EXT + ('.json',)): continue
        try: txt = git_bytes(repo, rev, f).decode('utf-8', 'replace')
        except SystemExit: continue
        if rx.search(txt): out.append(f)
    return out


def cmd_reach(repo, rev, json_out):
    t = Tally(); files = [l for l in git(repo, 'ls-tree', '-r', '--name-only', rev).split('\n') if l]
    dfa = [f for f in files if is_dockerfile(f)]; dfb = [f for f in files if 'dockerfile' in f.lower()]
    ctx = compose_contexts(repo, rev)
    texts = dict((f, git_bytes(repo, rev, f).decode('utf-8', 'replace')) for f in dfa)
    lockcopy = [f for f in dfa if any(re.search(r'package(\*|-lock)\.json', x) for s in stages(texts[f]) for e in s['events'] if e['kind'] == 'copy' for x in e['srcs'])]
    lit = sum(1 for f in dfa for s in stages(texts[f]) for e in s['events'] if e['kind'] == 'copy' for x in e['srcs'] if 'package-lock.json' in x)
    devlit = sum(texts[f].count('Dev/package-lock.json') for f in dfa)
    print('CENSUS at %s: Dockerfiles (a) basename %d | (b) any path containing "dockerfile" %d (extra in (b): %s) | compose (context, dockerfile) pairs %d' % (
        rev[:12], len(dfa), len(dfb), sorted(set(dfb) - set(dfa)), len(ctx)))
    print('CENSUS lock-copying Dockerfiles (a COPY source naming package*.json or package-lock.json): %d (builder %s) | COPY sources naming the literal package-lock.json: %d (builder 8) | the literal Dev/package-lock.json in any Dockerfile: %d (builder 0)' % (
        len(lockcopy), RB['lock_copying_dockerfiles'], lit, devlit))
    changed = sorted(l for l in K['pr']['numstat'] if l != K['root_lock'])
    lock_dev = {}
    for l in changed:
        pk = json.loads(git_bytes(repo, rev, l))['packages']; e = pk.get('node_modules/%s' % PKG)
        lock_dev[l] = None if e is None else bool(e.get('dev') or e.get('devOptional'))
    print('FLAGS %s in each changed standalone lock at %s: %s' % (PKG, rev[:12], dict((l.split('/')[-2], 'ABSENT' if v is None else ('dev' if v else 'PROD')) for l, v in lock_dev.items())))
    fileset = set(files); dirset = set(posixpath.dirname(x) for x in files)
    while True:
        more = set(posixpath.dirname(d) for d in dirset) - dirset
        if not more: break
        dirset |= more
    rows = []; unresolved = []; inferred = []; root_hits = []; ships = {}
    for f in sorted(dfa):
        st = stages(texts[f]); cs = ctx.get(f)
        if not cs:
            c = infer_context(f, st, fileset, dirset)
            if c is None:
                if not any(e['kind'] in ('copy', 'install') for x in st for e in x['events']): inferred.append('%s -> NO COPY / NO npm (cannot carry a lock)' % f); continue
                unresolved.append(f); continue
            inferred.append('%s -> %s' % (f, c or '<repo root>')); cs = {c}
        for c in sorted(cs):
            if not st: continue
            rl = K['root_lock']
            if rl.startswith(c + '/') or c == '':
                hits = any_install_from(st, rl[len(c) + 1:] if c else rl)
                if hits: root_hits.append('%s stages %s' % (f, hits))
            for l in changed:
                if not (l.startswith(c + '/') or c == ''): continue
                lr = l[len(c) + 1:] if c else l
                if lock_dev[l] is None: continue
                for d, how, om in final_ships(st, lr, lock_dev[l]):
                    ships.setdefault(f, []).append((l, d, how, om)); rows.append((f, l, d, how, om))
                fin = stage_state(st, len(st) - 1, lr)[0]
                for d, v in fin.items():
                    if v['omit'] and lock_dev[l]: print('NOT SHIPPED %s <- %s at %s: prod-only (%s) and %s is dev there' % (f, l, d, ' -> '.join(v['how']), PKG))
    for r in rows: print('SHIPS %s <- %s at %s via %s (prod-only %s)' % r)
    t.check('R0', not unresolved, 'build context for every basename-Dockerfile: from compose %d | INFERRED %d %s | unresolved %d %s' % (
        len(dfa) - len(inferred) - len(unresolved), len(inferred), inferred[:4], len(unresolved), unresolved[:6]))
    t.check('R1', not root_hits, 'ROOT LOCK: stages installing from %s: %d %s' % (K['root_lock'], len(root_hits), root_hits[:3]))
    svc = lambda f: f.replace('Blockchain/Dev/', '').replace('/Dockerfile', '')
    shipping = sorted(svc(f) for f in ships)
    t.info('R2', 'images whose final stage carries %s from a changed standalone lock: %s (builder: %s)' % (PKG, shipping, RB['images_shipping']))
    t.check('R3', 'services/originate' in shipping, 'POSITIVE CONTROL: services/originate ships %s: %s' % (PKG, 'services/originate' in shipping))
    fab = sum(1 for f in dfa if any(s['name'] == 'gate78-fabricated-stage' for s in stages(texts[f])))
    neg = [x for x in RB['not_shipping'] if x in shipping]
    t.check('R4', fab == 0 and not neg and shipping == sorted(RB['images_shipping']), 'NEGATIVE CONTROLS: fabricated stage matches %d Dockerfiles | of %s, shipping anyway: %s | the shipping set == builder %s' % (
        fab, RB['not_shipping'], neg or 'none', shipping == sorted(RB['images_shipping'])))
    imp = importers(repo, rev, PKG, files); ex = importers(repo, rev, 'express', files); tj = mentions(repo, rev, 'ts-jest', files)
    print('IMPORTERS %s %d %s | CONTROL express importers %d (builder %d) | CONTROL files naming ts-jest %d (builder %d)' % (
        PKG, len(imp), imp[:5], len(ex), RB['importer_controls']['express'], len(tj), RB['importer_controls']['ts-jest']))
    t.check('R5', not imp and len(ex) > 0 and len(tj) > 0, 'IMPORTERS of %s: %d (want 0) beside controls express %d and ts-jest %d (want > 0 each)' % (PKG, len(imp), len(ex), len(tj)))
    if json_out:
        json.dump({'rev': rev, 'dockerfiles_a': len(dfa), 'dockerfiles_b': len(dfb), 'lock_copying': len(lockcopy), 'lockfile_literal': lit, 'dev_lock_literal': devlit,
                   'ships': shipping, 'root_hits': root_hits, 'importers': imp, 'express': len(ex), 'ts_jest': len(tj)}, open(json_out, 'w'), indent=1)
    return t.end()


def selftest():
    res = []
    def rep(c, m): res.append(bool(c)); print('%s %s' % ('PASS' if c else 'FAIL', m))
    gov = ('FROM node AS builder\nWORKDIR /app\nCOPY services/g/package*.json ./\nRUN npm ci --ignore-scripts\nRUN npm run build\nRUN npm prune --omit=dev\n'
           'FROM node\nWORKDIR /app\nCOPY --from=builder /app/node_modules ./node_modules\n')
    rep(final_ships(stages(gov), 'services/g/package-lock.json', True) == [], 'governance shape: prune --omit=dev before the runtime COPY: a DEV package does NOT ship')
    rep(len(final_ships(stages(gov), 'services/g/package-lock.json', False)) == 1, 'governance shape: a PROD package DOES ship (the prune keeps it)')
    nop = gov.replace('RUN npm prune --omit=dev\n', '')
    rep(len(final_ships(stages(nop), 'services/g/package-lock.json', True)) == 1, 'PLANTED prune removed: the DEV package now SHIPS (the parser sees the prune, not the name)')
    org = ('FROM node AS builder\nWORKDIR /app\nCOPY services/o/package*.json ./\nRUN npm ci --ignore-scripts\n'
           'FROM node AS runner\nWORKDIR /app\nCOPY --from=builder /app/node_modules ./node_modules\nCOPY --from=builder /app/package.json /app/package-lock.json ./\nRUN npm ci --ignore-scripts --omit=dev\n')
    f = final_ships(stages(org), 'services/o/package-lock.json', False)
    rep(len(f) == 1 and f[0][2] is True, 'originate shape: a runner re-install --omit=dev REPLACES the full copy; a PROD package ships prod-only: %s' % f)
    rep(final_ships(stages(org), 'services/o/package-lock.json', True) == [], 'originate shape: a DEV package does NOT ship after the --omit=dev re-install')
    vci = ('FROM node AS builder\nWORKDIR /app\nCOPY services/v/package*.json ./\nRUN npm ci\nFROM node AS runner\nWORKDIR /app\n'
           'COPY services/v/package*.json ./\nRUN npm ci --ignore-scripts --omit=dev\nCOPY --from=builder /app/dist ./dist\n')
    rep(final_ships(stages(vci), 'services/v/package-lock.json', True) == [], 'vc-issuer shape: runner --omit=dev from its own lock, only dist copied: a DEV package does NOT ship')
    full = 'FROM node AS b\nWORKDIR /shared\nCOPY packages/shared/package*.json ./\nRUN npm ci --ignore-scripts\nFROM node\nWORKDIR /app\nCOPY --from=b /shared /shared\n'
    rep(len(final_ships(stages(full), 'packages/shared/package-lock.json', True)) == 1, 'COPY --from a FULL-ci builder ships its node_modules WITH dev deps')
    root = 'FROM node\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci\n'
    rep(any_install_from(stages(root), 'package-lock.json'), 'PLANTED root `COPY package*.json` + npm ci FIRES R1')
    rep(not any_install_from(stages(gov), 'package-lock.json'), 'a service-dir COPY does not read as the root lock')
    dot = 'FROM node\nWORKDIR /app\nCOPY . .\nRUN npm ci\n'
    rep(any_install_from(stages(dot), 'package-lock.json'), 'PLANTED `COPY . .` + npm ci FIRES R1 (a whole-context copy carries the root lock)')
    inh = 'FROM node AS base\nWORKDIR /app\nCOPY services/g/package*.json ./\nRUN npm ci\nFROM base AS runner\n'
    rep(len(final_ships(stages(inh), 'services/g/package-lock.json', True)) == 1, '`FROM <stage>` inherits that stage\'s node_modules')
    rep(len(logical_lines('RUN a \\\n  b\n# c\nRUN d')) == 2, 'continuation lines join; comments drop')
    oth = ('FROM node AS builder\nWORKDIR /app\nCOPY services/o/package*.json ./\nRUN npm ci\n'
           'FROM node\nWORKDIR /app\nCOPY --from=builder /app/node_modules ./node_modules\nCOPY other/package*.json ./\nRUN npm ci --omit=dev\n')
    rep(final_ships(stages(oth), 'services/o/package-lock.json', False) == [], 'a final re-install from a DIFFERENT lock REPLACES the copied node_modules: nothing from ours ships')
    rx = re.compile(IMPORT_RX % ((re.escape('handlebars'),) * 4))
    rep(all(rx.search(x) for x in ("const h = require('handlebars')", 'import Handlebars from "handlebars"', "await import('handlebars')", "import 'handlebars'")),
        'importer regex: require / import-from / dynamic import / side-effect import all match')
    rep(not any(rx.search(x) for x in ("require('handlebars-helpers')", "// handlebars is unused", "from 'express-handlebars'")),
        'importer regex: handlebars-helpers, a comment and express-handlebars do NOT match')
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
