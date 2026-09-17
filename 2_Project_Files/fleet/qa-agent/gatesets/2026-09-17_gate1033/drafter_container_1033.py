#!/usr/bin/env python3
"""drafter_container_1033.py — #1033 in node:24-alpine (the image's base; image 50c8e8ca1d27 present locally). NOT an image build: each container
replays the originate Dockerfile's steps from copied sources (read-only /src mount; installs inside the container filesystem; census JSON and logs
to a /out mount). apk (:23 python3 make g++ openssl) is NOT replayed (install scripts are off at :30 and :79). Containers are named uniquely
(drafter1033-<tree>-<epoch>), run SEQUENTIALLY, and removed only by that exact name. jest runs --runInBand.
Per tree (base bb848b828, head 2cab54988): runner :79 `npm ci --ignore-scripts --omit=dev` census; /shared :14/:16; builder :30 full census;
:32 link; :38 `npx prisma generate`; :44 tsc; originate jest --runInBand; runner completion + an in-process traced start (busybox timeout
inside MY container) + GET /health; positive control require('mysql2') with the same hook. Plus head2: runner step only (determinism)."""
import datetime, hashlib, json, os, re, shutil, subprocess, tempfile, time
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1033'
OUT = GS + '/out'
P = json.load(open(OUT + '/drafter_paths.json')); SCR = P['SCR']
CT = tempfile.mkdtemp(prefix='container_', dir='/private/tmp/claude-501/drafter1033')
def now(): return datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z')
def load(): return '%.1f/%.1f/%.1f' % os.getloadavg()
print('drafter_container_1033 start', now(), 'load', load(), '| CT', CT, flush=True)
IMG = 'node:24-alpine'
print('image', subprocess.run(['docker', 'image', 'inspect', IMG, '--format', '{{.Id}} {{.Os}}/{{.Architecture}}'], capture_output=True, text=True).stdout.strip())
open(CT + '/census.mjs', 'w').write(r'''
import { readdirSync, readFileSync } from 'node:fs'; import { createHash } from 'node:crypto'; import path from 'node:path';
const d = process.argv[2]; const pk = {}, files = {};
function walk(dir) {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name); const rel = path.relative(d, p);
    if (rel.startsWith('node_modules/.prisma')) continue;
    if (e.isSymbolicLink()) continue;
    if (e.isDirectory()) { walk(p); continue; }
    if (!e.isFile()) continue;
    const buf = readFileSync(p); files[rel] = createHash('sha256').update(buf).digest('hex');
    if (e.name === 'package.json') {
      const par = path.basename(path.dirname(dir)), par2 = path.basename(path.dirname(path.dirname(dir)));
      if (par === 'node_modules' || (par.startsWith('@') && par2 === 'node_modules')) { try { pk[path.relative(d, dir)] = JSON.parse(buf).version; } catch { pk[path.relative(d, dir)] = '?'; } }
    }
  }
}
walk(path.join(d, 'node_modules')); process.stdout.write(JSON.stringify({ pk, files }));
''')
open(CT + '/qa_trace_hook.cjs', 'w').write(r'''
const fs = require('node:fs'); const Module = require('node:module'); const net = require('node:net');
const OUT = process.env.QA_TRACE_OUT; const seen = new Set();
function rec(kind, s) { if (!OUT || !s) return; const k = kind + ' ' + s; if (seen.has(k)) return; seen.add(k); fs.appendFileSync(OUT, k + '\n'); }
rec('I', 'pid ' + process.pid + ' argv ' + process.argv.slice(1).join(' '));
if (typeof Module.registerHooks === 'function') { Module.registerHooks({ resolve(spec, ctx, next) { const r = next(spec, ctx); rec('R', r.url); return r; } }); rec('I', 'registerHooks active'); }
const origLoad = Module._load;
Module._load = function (request, parent, isMain) { try { rec('L', Module._resolveFilename(request, parent, isMain)); } catch (e) {} return origLoad.apply(this, arguments); };
if (process.env.QA_FORCE_LOOPBACK) {
  const origListen = net.Server.prototype.listen;
  net.Server.prototype.listen = function (...args) { const cb = args.find(a => typeof a === 'function'); const srv = this;
    srv.once('listening', () => rec('P', String(srv.address().port) + ' ' + srv.address().address)); return origListen.call(this, { port: 0, host: '127.0.0.1' }, cb); };
}
''')
open(CT + '/ctr.sh', 'w').write(r'''set -u
T=$1; MODE=$2
echo "== $T $MODE start $(date) loadavg $(cat /proc/loadavg) node $(node -v) npm $(npm -v)"
mkdir -p /rt && cp /src/$T/originate/package.json /src/$T/originate/package-lock.json /rt/
cd /rt && npm ci --ignore-scripts --omit=dev --no-audit --no-fund; echo "RT_CI_RC=$?"
node /src/census.mjs /rt > /out/rt_$T.json; echo "RT_CENSUS_RC=$?"
npm ls mysql2; echo "RT_LS_RC=$?"
[ "$MODE" = rtonly ] && { echo "== $T end $(date)"; exit 0; }
cp -r /src/$T/shared /shared && cd /shared && npm ci --ignore-scripts --no-audit --no-fund > /out/shared_ci_$T.log 2>&1; echo "SHARED_CI_RC=$?"
npm run build > /out/shared_build_$T.log 2>&1; echo "SHARED_BUILD_RC=$?"
mkdir -p /app && cp /src/$T/originate/package.json /src/$T/originate/package-lock.json /app/ && cd /app && npm ci --ignore-scripts --no-audit --no-fund; echo "FULL_CI_RC=$?"
node /src/census.mjs /app > /out/full_$T.json; echo "FULL_CENSUS_RC=$?"
npm ls mysql2; echo "FULL_LS_RC=$?"
npm ls --all > /out/lsall_full_$T.txt 2>&1; echo "FULL_LSALL_RC=$? invalid=$(grep -c invalid /out/lsall_full_$T.txt) overridden=$(grep -c overridden /out/lsall_full_$T.txt)"
mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared
cp -r /src/$T/prisma ./prisma
QA_TRACE_OUT=/out/trace_ctr_prisma_generate_$T.txt NODE_OPTIONS=--require=/src/qa_trace_hook.cjs npx prisma generate; echo "PRISMA_GENERATE_RC=$?"
cp -r /src/$T/originate/. ./ && npm run build > /out/tsc_$T.log 2>&1; echo "TSC_RC=$?"
echo "jest start $(date) loadavg $(cat /proc/loadavg)"
npx jest --runInBand > /out/jest_$T.log 2>&1; echo "JEST_RC=$?"; grep -E "^(Tests|Test Suites):" /out/jest_$T.log; echo "jest end $(date) loadavg $(cat /proc/loadavg)"
cp -r /app/dist /rt/dist && cp -r /app/node_modules/.prisma /rt/node_modules/.prisma && mkdir -p /rt/node_modules/@secuura && ln -s /shared /rt/node_modules/@secuura/shared
cd /rt
( sleep 12; PORT=$(grep '^P ' /out/trace_ctr_start_$T.txt | head -1 | cut -d' ' -f2); echo "PORT=$PORT"; wget -q -S -O /dev/null "http://127.0.0.1:$PORT/health" 2>&1 | head -1; echo "HEALTH_RC=$?" ) &
QA_TRACE_OUT=/out/trace_ctr_start_$T.txt QA_FORCE_LOOPBACK=1 NODE_OPTIONS=--require=/src/qa_trace_hook.cjs NODE_ENV=development PORT=4000 \
  DATABASE_URL=postgresql://qa:qa@127.0.0.1:1/qa REDIS_URL=redis://127.0.0.1:1 ANCHORING_SERVICE_URL=http://127.0.0.1:1 AUTH_SERVICE_URL=http://127.0.0.1:1 \
  timeout -s TERM 25 node dist/index.js > /out/start_$T.log 2>&1; echo "START_RC=$? (143 = ended by my timeout TERM)"
wait
QA_TRACE_OUT=/out/trace_ctr_control_$T.txt NODE_OPTIONS=--require=/src/qa_trace_hook.cjs node -e "require('mysql2'); console.log('control mysql2', require('mysql2/package.json').version)"; echo "CONTROL_RC=$?"
echo "== $T end $(date)"
''')
for t in ('base', 'head'):
    src = SCR + '/wt_%s/Blockchain/Dev' % t
    os.makedirs(CT + '/' + t)
    shutil.copytree(src + '/services/originate', CT + '/%s/originate' % t)
    shutil.copytree(src + '/prisma', CT + '/%s/prisma' % t)
    shutil.copytree(src + '/packages/shared', CT + '/%s/shared' % t, ignore=shutil.ignore_patterns('node_modules', 'dist'))
os.makedirs(CT + '/out')
ctr_out = CT + '/out'
for t, mode in (('head', 'full'), ('base', 'full'), ('head', 'rtonly')):
    name = 'drafter1033-%s-%s-%d' % (t, mode, int(time.time()))
    lbl = t if mode == 'full' else 'head2'
    o = ctr_out if mode == 'full' else CT + '/out_head2'
    os.makedirs(o, exist_ok=True)
    t0, l0 = now(), load()
    p = subprocess.run(['docker', 'run', '--name', name, '-v', CT + ':/src:ro', '-v', o + ':/out', IMG, 'sh', '/src/ctr.sh', t, mode], capture_output=True, text=True, timeout=3000)
    open(OUT + '/container_%s.log' % lbl, 'w').write(p.stdout + '\n--stderr--\n' + p.stderr)
    rm = subprocess.run(['docker', 'rm', name], capture_output=True, text=True)
    print('CTR %s (%s) container %s rc %d [%s load %s -> %s] | docker rm by exact name rc %d %s' % (lbl, mode, name, p.returncode, t0, l0, now(), rm.returncode, rm.stdout.strip()), flush=True)
    for l in (p.stdout + p.stderr).splitlines():
        if re.search(r'_RC=|^Tests:|^Test Suites:|PORT=|HTTP/|mysql2@|control mysql2|^== |jest (start|end)|invalid|overridden', l): print('CTR %s   %s' % (lbl, l.strip()[:200]))
def ld(p): return json.load(open(p))
def pdiff(x, y): return sorted('%s %s->%s' % (k, x.get(k), y.get(k)) for k in set(x) | set(y) if x.get(k) != y.get(k))
def fdiff(x, y): return sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
SUB = re.compile(r'^node_modules/(mysql2|sql-escaper|seq-queue|sqlstring)(/|$)')
try:
    for kind in ('rt', 'full'):
        b, h = ld(ctr_out + '/%s_base.json' % kind), ld(ctr_out + '/%s_head.json' % kind)
        fm = fdiff(b['files'], h['files']); outside = [f for f in fm if not SUB.search(f)]
        print('CTR CENSUS %-4s base->head pkgs %d/%d package moves %s | differing files %d, OUTSIDE the mysql2 subtree %d %s' % (kind, len(b['pk']), len(h['pk']), pdiff(b['pk'], h['pk']), len(fm), len(outside), outside[:6]))
    h, h2 = ld(ctr_out + '/rt_head.json'), ld(CT + '/out_head2/rt_head.json')
    print('CTR CENSUS rt DETERMINISM head vs head2: package moves %d, differing files %d %s' % (len(pdiff(h['pk'], h2['pk'])), len(fdiff(h['files'], h2['files'])), fdiff(h['files'], h2['files'])[:5]))
    b = ld(ctr_out + '/rt_base.json')
    print('CTR runtime presence (express, @prisma/client, prisma, mysql2, sql-escaper, sqlstring, jest, typescript) base/head:', [(n, b['pk'].get('node_modules/' + n), h['pk'].get('node_modules/' + n)) for n in ('express', '@prisma/client', 'prisma', 'mysql2', 'sql-escaper', 'sqlstring', 'jest', 'typescript')])
    # host vs container runtime package sets (platform drift, informational)
    hp = json.load(open(OUT + '/drafter_runtime_census_pk.json')) if os.path.exists(OUT + '/drafter_runtime_census_pk.json') else None
    if hp: print('CTR vs HOST runtime package-set (head): only-host %s | only-container %s' % (sorted(set(hp['head']['rt_pk']) - set(h['pk']))[:10], sorted(set(h['pk']) - set(hp['head']['rt_pk']))[:10]))
except Exception as e:
    print('CTR CENSUS unreadable', type(e).__name__, e)
for t in ('base', 'head'):
    for tr in ('start', 'prisma_generate', 'control'):
        f = ctr_out + '/trace_ctr_%s_%s.txt' % (tr, t)
        if not os.path.exists(f): print('CTR TRACE %s %s missing' % (tr, t)); continue
        paths = [l.split(' ', 1)[1] for l in open(f).read().splitlines() if l[:2] in ('R ', 'L ')]
        c = lambda n: len({p for p in paths if re.search(r'node_modules/%s/' % re.escape(n), p)})
        print('CTR TRACE %-15s %s lines %d | mysql2 %d sql-escaper %d sqlstring %d prisma-CLI %d @prisma/dev %d || controls @prisma/client %d @prisma/adapter-pg %d pg %d express %d' % (
            tr, t, len(paths), c('mysql2'), c('sql-escaper'), c('sqlstring'), c('prisma'), c('@prisma/dev'), c('@prisma/client'), c('@prisma/adapter-pg'), c('pg'), c('express')))
for f in ('jest_head.log', 'jest_base.log', 'start_head.log'):
    if os.path.exists(ctr_out + '/' + f): shutil.copyfile(ctr_out + '/' + f, OUT + '/ctr_' + f)
print('containers of mine remaining:', subprocess.run(['docker', 'ps', '-a', '--filter', 'name=drafter1033-', '--format', '{{.Names}}'], capture_output=True, text=True).stdout.split())
print('done', now(), 'load', load())
