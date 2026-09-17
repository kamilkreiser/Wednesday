#!/usr/bin/env python3
"""drafter_runtime_1033.py — #1033 RUNTIME REACH + LOAD TRACE + host suites. HOST npm (node 24.7 / npm 11.5, darwin — NOT node:24-alpine;
the container route is drafter_container_1033.py), OUTSIDE Blockchain/Dev (npm ci inside a member dir installs from the workspace ROOT lock),
under /private/tmp/claude-501/drafter1033/. Never cd; every subprocess has an explicit cwd in the scratch tree.
P0 anchor-assert every originate Dockerfile line this reproduces, at base bb848b828 AND head 2cab54988.
P1 builder :28/:30  `npm ci --ignore-scripts` (FULL = positive control)   and runner :64/:79 `npm ci --ignore-scripts --omit=dev` (RUNTIME),
   at base, head and head2 (determinism pair); census = every installed package.json (relpath@version) + sha256 of every non-symlink file.
   `npm ls mysql2` and `npm ls --all` rc in each tree.
P2 builder completion at base and head: /shared (:13-:16 npm ci --ignore-scripts + npm run build), :32 link, :35 prisma/, :38 `npx prisma generate`
   (TRACED: does the prisma CLI load mysql2?), :41 source, :44 `npm run build`; originate jest --runInBand in the builder tree.
P3 runner completion (:62 dist, :86 .prisma, :88/:89 /shared link) and an IN-PROCESS originate start `node dist/index.js` with a require/resolve
   hook (module.registerHooks + Module._load), every listener forced to 127.0.0.1:0, DB/Redis/upstreams pointed at closed loopback port 1,
   GET /health, then SIGTERM to the verified child pid. POSITIVE CONTROL: the same hook sees `require('mysql2')` in the same tree."""
import concurrent.futures, datetime, hashlib, json, os, re, shutil, signal, subprocess, sys, tempfile, time, urllib.request
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1033'
OUT = GS + '/out'
P = json.load(open(OUT + '/drafter_paths.json')); SCR = P['SCR']
RT = tempfile.mkdtemp(prefix='runtime_', dir='/private/tmp/claude-501/drafter1033')
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
LOG = open(OUT + '/drafter_runtime.cmdlog', 'a')
def sh(args, cwd, env=None, timeout=900, tag=''):
    t0, l0 = now(), load()
    try:
        p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=env, timeout=timeout); rc, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        rc, so, se = 'TIMEOUT', str(e.stdout), str(e.stderr)
    LOG.write('\n### %s $ %s (cwd %s) rc %s [%s load %s -> %s]\n%s\n--stderr--\n%s\n' % (tag, ' '.join(args), cwd, rc, t0, l0, now(), so[-20000:], se[-20000:])); LOG.flush()
    return rc, so, se, '[%s load %s -> %s]' % (t0, l0, now())
print('drafter_runtime_1033 start', now(), 'load', load(), '| RT', RT, '| outside Blockchain/Dev:', '/Blockchain/Dev' not in RT, flush=True)
# P0 anchors
ANCH = {13: 'COPY packages/shared/package*.json ./', 14: 'RUN npm ci --ignore-scripts', 16: 'RUN npm run build', 28: 'COPY services/originate/package*.json ./',
        30: 'RUN npm ci --ignore-scripts', 32: 'RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared', 35: 'COPY prisma/ ./prisma/',
        38: 'RUN npx prisma generate', 41: 'COPY services/originate/ ./', 44: 'RUN npm run build', 62: 'COPY --from=builder /app/dist ./dist',
        63: 'COPY --from=builder /app/node_modules ./node_modules', 64: 'COPY --from=builder /app/package.json /app/package-lock.json ./',
        79: 'RUN npm ci --ignore-scripts --omit=dev', 86: 'COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma',
        89: 'RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared', 99: 'ENV NODE_ENV=production', 108: 'CMD ["node", "dist/index.js"]'}
for t in ('base', 'head'):
    lines = open(SCR + '/wt_%s/Blockchain/Dev/services/originate/Dockerfile' % t).read().split('\n')
    bad = [n for n, s in ANCH.items() if lines[n - 1].strip() != s]
    npmci = [i + 1 for i, l in enumerate(lines) if re.search(r'\bnpm (ci|install|prune)\b', l)]
    print('P0 %s Dockerfile anchors %d/%d exact %s | every npm ci/install/prune line: %s' % (t, len(ANCH) - len(bad), len(ANCH), bad, npmci))
    if bad: print('P0 ANCHOR MISMATCH — refusing'); sys.exit(1)
def census(d):
    pk, files = {}, {}
    nm = d + '/node_modules'
    for root, dirs, fs in os.walk(nm):
        if os.path.relpath(root, d).split(os.sep)[:2] == ['node_modules', '.prisma']: continue
        for f in fs:
            p = os.path.join(root, f); rel = os.path.relpath(p, d)
            if os.path.islink(p): continue
            files[rel] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            if f == 'package.json':
                par = os.path.basename(os.path.dirname(root)); par2 = os.path.basename(os.path.dirname(os.path.dirname(root)))
                if par == 'node_modules' or (par.startswith('@') and par2 == 'node_modules'):
                    try: pk[os.path.relpath(root, d)] = json.load(open(p)).get('version')
                    except Exception: pk[os.path.relpath(root, d)] = '?'
    return pk, files
def prep(d, tree):
    os.makedirs(d)
    src = SCR + '/wt_%s/Blockchain/Dev/services/originate' % tree
    for f in ('package.json', 'package-lock.json'): shutil.copyfile(src + '/' + f, d + '/' + f)
    return sha(d + '/package-lock.json')
def p1(label, tree):
    o = {}
    full, rt = RT + '/%s/builder' % label, RT + '/%s/runner' % label
    s0 = prep(full, tree); prep(rt, tree)
    o['full_rc'], _, e1, o['full_t'] = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], full, tag=label + ' builder:30')
    o['full'] = census(full)
    o['rt_rc'], _, e2, o['rt_t'] = sh(['npm', 'ci', '--ignore-scripts', '--omit=dev', '--no-audit', '--no-fund'], rt, tag=label + ' runner:79')
    o['rt'] = census(rt)
    o['lock'] = '%s->%s,%s' % (s0, sha(full + '/package-lock.json'), sha(rt + '/package-lock.json'))
    for k, d in (('full', full), ('rt', rt)):
        rc, so, se, _ = sh(['npm', 'ls', 'mysql2'], d, tag=label + ' ls ' + k); o['ls_' + k] = (rc, ' '.join(so.split())[-300:], ' '.join(se.split())[-200:])
        rc, so, se, _ = sh(['npm', 'ls', '--all'], d, tag=label + ' lsall ' + k)
        o['lsall_' + k] = (rc, len(re.findall(r'\binvalid\b', so)), len(re.findall(r'\boverridden\b', so)), [l.strip()[:120] for l in so.splitlines() if re.search(r'invalid|UNMET|extraneous', l)][:6], ' '.join(se.split())[-300:])
    o['err'] = (e1[-300:], e2[-300:])
    return label, tree, o
R = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    for fut in concurrent.futures.as_completed([ex.submit(p1, l, t) for l, t in (('base', 'base'), ('head', 'head'), ('head2', 'head'))]):
        l, t, o = fut.result(); R[l] = o
        pick = lambda c: sorted('%s@%s' % (k, v) for k, v in c[0].items() if re.search(r'node_modules/(mysql2|sql-escaper|seq-queue|sqlstring|prisma|@prisma/client|@prisma/adapter-pg|@prisma/dev|express|jest|typescript)$', k))
        print('P1 %-5s (%s) FULL rc %s %s pkgs %d files %d | RUNTIME rc %s %s pkgs %d files %d | lock %s' % (l, t, o['full_rc'], o['full_t'], len(o['full'][0]), len(o['full'][1]), o['rt_rc'], o['rt_t'], len(o['rt'][0]), len(o['rt'][1]), o['lock']), flush=True)
        print('P1 %-5s FULL picks %s' % (l, pick(o['full'])))
        print('P1 %-5s RUNTIME picks %s' % (l, pick(o['rt'])))
        print('P1 %-5s npm ls mysql2 full %s | runtime %s' % (l, o['ls_full'], o['ls_rt']))
        print('P1 %-5s npm ls --all full rc/invalid/overridden/lines %s | runtime %s' % (l, o['lsall_full'], o['lsall_rt']))
        if o['full_rc'] or o['rt_rc']: print('P1 %-5s stderr tails %s' % (l, o['err']))
def pdiff(x, y): return sorted('%s %s->%s' % (k, x.get(k), y.get(k)) for k in set(x) | set(y) if x.get(k) != y.get(k))
def fdiff(x, y): return sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
SUBTREE = re.compile(r'^node_modules/(mysql2|sql-escaper|seq-queue|sqlstring)(/|$)')
for kind in ('full', 'rt'):
    b, h, h2 = R['base'][kind], R['head'][kind], R['head2'][kind]
    pm, fm = pdiff(b[0], h[0]), fdiff(b[1], h[1])
    outside = [f for f in fm if not SUBTREE.search(f)]
    print('CENSUS %-4s base->head package moves %d %s | differing files %d (inside mysql2/sql-escaper/seq-queue/sqlstring %d; OUTSIDE %d %s)' % (kind, len(pm), pm, len(fm), len(fm) - len(outside), len(outside), outside[:8]))
    print('CENSUS %-4s DETERMINISM head vs head2: package moves %d, differing files %d %s' % (kind, len(pdiff(h[0], h2[0])), len(fdiff(h[1], h2[1])), fdiff(h[1], h2[1])[:6]))
b, h = R['base']['rt'], R['head']['rt']
print('CENSUS runtime NEGATIVE CONTROLS absent (jest, typescript, ts-jest, eslint) base/head:', [(n, 'node_modules/' + n in b[0], 'node_modules/' + n in h[0]) for n in ('jest', 'typescript', 'ts-jest', 'eslint')])
print('CENSUS runtime PRESENCE controls (express, @prisma/client, prisma, mysql2) base/head:', [(n, b[0].get('node_modules/' + n), h[0].get('node_modules/' + n)) for n in ('express', '@prisma/client', 'prisma', 'mysql2', '@prisma/dev')])
json.dump({k: {'full_pk': v['full'][0], 'rt_pk': v['rt'][0]} for k, v in R.items()}, open(OUT + '/drafter_runtime_census_pk.json', 'w'), indent=0)
# P2 / P3 hook
HOOK = RT + '/qa_trace_hook.cjs'
open(HOOK, 'w').write(r'''
const fs = require('node:fs'); const Module = require('node:module'); const net = require('node:net');
const OUT = process.env.QA_TRACE_OUT; const seen = new Set();
function rec(kind, s) { if (!OUT || !s) return; const k = kind + ' ' + s; if (seen.has(k)) return; seen.add(k); fs.appendFileSync(OUT, k + '\n'); }
rec('I', 'pid ' + process.pid + ' argv ' + process.argv.slice(1).join(' '));
if (typeof Module.registerHooks === 'function') {
  Module.registerHooks({ resolve(spec, ctx, next) { const r = next(spec, ctx); rec('R', r.url); return r; } });
  rec('I', 'registerHooks active');
}
const origLoad = Module._load;
Module._load = function (request, parent, isMain) { try { rec('L', Module._resolveFilename(request, parent, isMain)); } catch (e) {} return origLoad.apply(this, arguments); };
if (process.env.QA_FORCE_LOOPBACK) {
  const origListen = net.Server.prototype.listen;
  net.Server.prototype.listen = function (...args) {
    const cb = args.find(a => typeof a === 'function'); const srv = this;
    srv.once('listening', () => rec('P', String(srv.address().port) + ' ' + srv.address().address));
    return origListen.call(this, { port: 0, host: '127.0.0.1' }, cb);
  };
}
''')
shared_tree = {t: subprocess.run(['git', '-C', P['C'], 'rev-parse', P[t.upper()] + ':Blockchain/Dev/packages/shared'], capture_output=True, text=True).stdout.strip() for t in ('base', 'head')}
print('P2 packages/shared tree base %s head %s equal %s' % (shared_tree['base'][:9], shared_tree['head'][:9], shared_tree['base'] == shared_tree['head']))
SH = RT + '/shared'
shutil.copytree(SCR + '/wt_head/Blockchain/Dev/packages/shared', SH)
print('P2 /shared npm ci', sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], SH, tag='shared ci')[::3], '| build', sh(['npm', 'run', 'build'], SH, tag='shared build')[::3], flush=True)
def summ(txt):
    return [l.strip() for l in txt.splitlines() if re.match(r'\s*(Tests|Test Suites):', l)]
def traced(label):
    f = RT + '/trace_%s.txt' % label
    return f, dict(os.environ, QA_TRACE_OUT=f, NODE_OPTIONS='--require=' + HOOK)
def trace_read(f):
    lines = open(f).read().splitlines() if os.path.exists(f) else []
    paths = [l.split(' ', 1)[1] for l in lines if l[:2] in ('R ', 'L ')]
    def hits(n): return sorted({re.sub(r'^file://', '', p) for p in paths if re.search(r'node_modules/%s/' % re.escape(n), p)})
    return lines, hits
def p2(label, tree):
    b = RT + '/%s/builder' % label
    os.makedirs(b + '/node_modules/@secuura', exist_ok=True); os.symlink(SH, b + '/node_modules/@secuura/shared')
    shutil.copytree(SCR + '/wt_%s/Blockchain/Dev/prisma' % tree, b + '/prisma')
    f, env = traced('prisma_generate_' + label)
    rc, so, se, t = sh(['npx', 'prisma', 'generate'], b, env=env, tag=label + ' prisma generate')
    lines, hits = trace_read(f)
    out = ['P2 %s prisma generate rc %s %s | %s | trace lines %d | mysql2 files loaded %d %s | sql-escaper %d | prisma CLI files %d (control)' % (
        label, rc, t, [l for l in (so + se).splitlines() if 'Generated' in l or 'rror' in l][:3], len(lines), len(hits('mysql2')), hits('mysql2')[:3], len(hits('sql-escaper')), len(hits('prisma')))]
    src = SCR + '/wt_%s/Blockchain/Dev/services/originate' % tree
    shutil.copytree(src, b, dirs_exist_ok=True)
    rc, so, se, t = sh(['npm', 'run', 'build'], b, tag=label + ' tsc build'); out.append('P2 %s npm run build rc %s %s dist/index.js %s' % (label, rc, t, os.path.exists(b + '/dist/index.js')))
    rc, so, se, t = sh(['npx', 'jest', '--runInBand'], b, timeout=1500, tag=label + ' jest'); out.append('P2 %s originate jest --runInBand rc %s %s %s' % (label, rc, t, summ(so + se)))
    return label, out
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
    for fut in concurrent.futures.as_completed([ex.submit(p2, l, t) for l, t in (('base', 'base'), ('head', 'head'))]):
        l, out = fut.result(); print('\n'.join(out), flush=True)
# P3 runner + in-process start
def lsof_listen(pid):
    p = subprocess.run(['lsof', '-nP', '-a', '-p', str(pid), '-iTCP', '-sTCP:LISTEN'], capture_output=True, text=True); return [l for l in p.stdout.splitlines()[1:]]
for label in ('head', 'base'):
    r, b = RT + '/%s/runner' % label, RT + '/%s/builder' % label
    shutil.copytree(b + '/dist', r + '/dist'); shutil.copytree(b + '/node_modules/.prisma', r + '/node_modules/.prisma')
    os.makedirs(r + '/node_modules/@secuura', exist_ok=True); os.symlink(SH, r + '/node_modules/@secuura/shared')
    f, env = traced('start_' + label)
    env.update(QA_FORCE_LOOPBACK='1', NODE_ENV='development', PORT='4000', DATABASE_URL='postgresql://qa:qa@127.0.0.1:1/qa', REDIS_URL='redis://127.0.0.1:1',
               ANCHORING_SERVICE_URL='http://127.0.0.1:1', AUTH_SERVICE_URL='http://127.0.0.1:1', MULTI_TENANCY_ENABLED='false')
    env.pop('PII_ENCRYPTION_KEY', None)
    so_f, se_f = open(RT + '/start_%s.stdout' % label, 'w'), open(RT + '/start_%s.stderr' % label, 'w')
    t0, l0 = now(), load()
    proc = subprocess.Popen(['node', 'dist/index.js'], cwd=r, env=env, stdout=so_f, stderr=se_f)
    port, health = None, None
    for _ in range(60):
        time.sleep(0.5)
        if os.path.exists(f):
            m = [l for l in open(f).read().splitlines() if l.startswith('P ')]
            if m: port = m[0].split()[1]; break
        if proc.poll() is not None: break
    if port:
        try: health = urllib.request.urlopen('http://127.0.0.1:%s/health' % port, timeout=10).status
        except Exception as e: health = type(e).__name__ + ' ' + str(getattr(e, 'code', ''))
    time.sleep(12)
    alive = proc.poll() is None
    argv = subprocess.run(['ps', '-p', str(proc.pid), '-o', 'command='], capture_output=True, text=True).stdout.strip()
    listens = lsof_listen(proc.pid) if alive else []
    if alive and proc.pid > 1 and 'dist/index.js' in argv:
        os.kill(proc.pid, signal.SIGTERM)
        try: proc.wait(timeout=15)
        except subprocess.TimeoutExpired: os.kill(proc.pid, signal.SIGKILL); proc.wait(timeout=10)
    so_f.close(); se_f.close()
    after = subprocess.run(['ps', '-p', str(proc.pid), '-o', 'pid='], capture_output=True, text=True).stdout.strip()
    lines, hits = trace_read(f)
    loaded_db = sorted({l for l in open(RT + '/start_%s.stdout' % label).read().splitlines() + open(RT + '/start_%s.stderr' % label).read().splitlines() if re.search(r'Database initialization failed|ECONNREFUSED|Prisma|Running', l)})[:6]
    print('P3 %s in-process start %s load %s -> %s | pid %d argv %r alive-at-12s %s | port %s health %s | LISTEN rows %s | ended: exit %s, ps after %r' % (
        label, t0, l0, now(), proc.pid, argv[:60], alive, port, health, [x.split()[-2] for x in listens], proc.returncode, after))
    print('P3 %s trace lines %d | LOADED mysql2 files %d %s | sql-escaper %d | seq-queue %d | sqlstring %d | prisma CLI %d | @prisma/dev %d || CONTROLS loaded: @prisma/client %d, @prisma/adapter-pg %d, pg %d, express %d, ioredis %d' % (
        label, len(lines), len(hits('mysql2')), hits('mysql2')[:3], len(hits('sql-escaper')), len(hits('seq-queue')), len(hits('sqlstring')), len(hits('prisma')), len(hits('@prisma/dev')),
        len(hits('@prisma/client')), len(hits('@prisma/adapter-pg')), len(hits('pg')), len(hits('express')), len(hits('ioredis'))))
    print('P3 %s service log evidence of the DB path exercised: %s' % (label, [x[:160] for x in loaded_db]))
    if label == 'head':
        fc, envc = traced('control_require_mysql2')
        rc, so, se, t = sh(['node', '-e', "const m=require('mysql2'); console.log('mysql2', require('mysql2/package.json').version, typeof m.createConnection)"], r, env=envc, tag='control require mysql2')
        lc, hc = trace_read(fc)
        print('P3 POSITIVE CONTROL same hook, same runner tree: require(mysql2) rc %s %s | stdout %r | mysql2 files seen %d | sql-escaper files %d' % (rc, t, so.strip(), len(hc('mysql2')), len(hc('sql-escaper'))))
        shutil.copyfile(f, OUT + '/trace_start_head.txt'); shutil.copyfile(fc, OUT + '/trace_control_require_mysql2.txt')
print('done', now(), 'load', load())
