#!/usr/bin/env python3
"""installprobe_gate42.py <scratchpad> — the drafter's MEASURED install probe for gate42 (#1339 KS-1378 ROUND 2 OF 2), run AFTER predict_gate42.py (it
reads the pins beside it: develop, #1339's head and kit.json's round-1 head). Re-cut from gate41's probe (which measured only the standalone nodemailer /
morgan installs and never ran tsc — the prediction that MISSED N-1339-1). Every install is a STANDALONE `npm ci --ignore-scripts --no-audit --no-fund`
of a lock read from the scratch clone (`git archive` / `git show`, never the checkout's working tree), under <scratchpad>/g42/ip/, npm cache in the
scratchpad — a CLEAN install from the committed lock, never an incremental one. Three SIDES: base (the pinned develop), r1 (the round-1
head that gate41 graded NO GO — THE PLANTED-BAD CASE, real code, not a synthetic plant) and head (the round-2 head).
PART A — THE DOCKERFILE BUILD PATH (requirement 1), a faithful host mirror of each service Dockerfile's two builder stages (gate41's report,
imagebuild_mirror2): stage shared-builder = standalone `npm ci` of packages/shared + `npm run build`; stage builder = standalone `npm ci` of the
service lock, node_modules/@secuura/shared -> that built shared, the service source, `npm run build` (tsc). For services/auth and services/originate
at base, r1 and head: rc, every `error TS` line, and (head) `tsc --listFilesOnly` naming WHICH nodemailer declarations tsc read.
PART B — nodemailer / morgan inside the base and head service installs (installprobe_gate42.cjs, gate41's probe unchanged): resolved versions and
entry paths, createTransport with the call site's SMTP option SHAPE (never connected), sendMail via streamTransport (built, not sent), morgan
'combined' on 127.0.0.1 port 0 with a CONTROL and a PLANTED quote.
PART C — THE RUNTIME-MOVED SERVICES (Wednesday's KS-1379 condition, requirement 3): services/queue (bullmq -> msgpackr 2) and services/m365-integration +
packages/shared (@azure/identity -> @azure/msal-node 6), standalone installs at base and head: EVERY installed copy of bullmq / msgpackr /
@azure/identity / @azure/msal-node / @azure/msal-common (by path), a load smoke (installprobe_rt_gate42.cjs: msgpackr pack/unpack round trip, bullmq
required, msal-node ConfidentialClientApplication constructed, @azure/identity ClientSecretCredential constructed — nothing connects), and each
workspace's OWN suite (`npx vitest run`, CI=true) run in the standalone install (m365 and queue with @secuura/shared linked as their Dockerfiles do).
CONTROLS (each must hold or the probe says CONTROLS FAIL; every one can fail and names the direction):
 CT1 every install and build step ran (rc recorded) · CT2 BASE resolves nodemailer 9.1.1 · CT3 HEAD resolves nodemailer 10.x >= 10.0.2 ·
 CT4 morgan control line logs both sides · CT5 BASE morgan logs the planted quote RAW, HEAD escapes it · CT6 call-site shapes build on both majors ·
 CT7 BASE tsc rc 0 / 0 errors for auth AND originate (the mirror builds a green tree) · CT8 R1 tsc rc != 0 with EXACTLY the TS2503 pair in email.ts per
 service (THE INSTRUMENT SEES N-1339-1 on the real round-1 code) · CT9 HEAD tsc rc 0 / 0 errors for both (the round-2 fix, measured) · CT10 the r1 and
 head service locks and packages/shared trees are byte-identical (so CT8 vs CT9 differ ONLY by the round-2 source) · CT11 queue msgpackr major 1 at
 BASE and 2 at HEAD (the instrument sees the KS-1379 move) · CT12 the @azure/identity-nested / shared msal-node major 5 at BASE and 6 at HEAD ·
 CT13 every runtime load smoke ok at both sides.
The suites in PART C are MEASURED and REPORTED, not controls (a suite red is a finding for the gate, never hidden by a control). packages/shared's
standalone lock carries NO vitest and its vitest.config.ts imports `vitest/config`: run with the same side's m365 vitest binary it does NOT START
(recorded as DID NOT START with its first Error line — never read as a red suite, never as a pass). Writes
installprobe_gate42.json beside this script; install trees stay in the scratchpad (a previous dir is MOVED aside as *.prevN, never removed).
Usage: installprobe_gate42.py <scratchpad dir under /private/tmp/claude-501/>"""
import json, os, re, subprocess, sys, datetime
GS = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(GS, 'kit.json'), encoding='utf-8'))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP) or not os.path.isdir(SP): print('usage: installprobe_gate42.py <scratchpad>'); sys.exit(9)
P = json.load(open(os.path.join(GS, 'pins_%s.json' % K['kit']), encoding='utf-8'))
if P.get('fail') != 0 or P.get('simulation') != 'none': print('REFUSING: the pins are not a passing real run'); sys.exit(1)
CL = os.path.join(SP, 'g42_sp', 'clone.git'); IP = os.path.join(SP, 'g42', 'ip'); os.makedirs(IP, exist_ok=True)
CACHE = os.path.join(SP, 'g42', 'npmcache')
n = sorted(K['prs'])[0]; SIDES = {'base': P['develop'], 'r1': K['round1_head'], 'head': P['prs'][n]['head']}
DR = 'Blockchain/Dev/'
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def sh(cmd, timeout=900, **kw):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)
    except subprocess.TimeoutExpired as e: return subprocess.CompletedProcess(cmd, 124, (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or ''), 'TIMEOUT %ds' % timeout)
npmv, nodev = sh(['npm', '--version']).stdout.strip(), sh(['node', '--version']).stdout.strip()
print('installprobe_gate42 %s | npm %s node %s | base %s r1 %s head %s | installs under %s' % (now(), npmv, nodev, SIDES['base'][:12], SIDES['r1'][:12], SIDES['head'][:12], IP))
res = {'measured_at': now(), 'npm': npmv, 'node': nodev, 'sides': SIDES, 'runs': {}, 'tsc': {}, 'runtime': {}, 'suites': {}}
def fresh(d):
    if os.path.exists(d):   # never rm: a previous dir is moved aside, and a fresh dir is built
        k = 1
        while os.path.exists('%s.prev%d' % (d, k)): k += 1
        os.rename(d, '%s.prev%d' % (d, k))
    os.makedirs(d)
def extract(c, sub, d):
    """the tree at <c>:Blockchain/Dev/<sub> into <d> (git archive from the scratch clone), without node_modules / dist"""
    a = subprocess.run(['git', '--git-dir', CL, 'archive', '--format=tar', c, DR + sub], capture_output=True)
    assert a.returncode == 0, a.stderr[-300:]
    t = subprocess.run(['tar', '-x', '-C', d, '--strip-components=%d' % len((DR + sub).strip('/').split('/'))], input=a.stdout, capture_output=True)
    assert t.returncode == 0, t.stderr[-300:]
def npm_ci(d, tag):
    t0 = now(); r = sh(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund', '--cache', CACHE], cwd=d)
    open(d + '.ci.out', 'w').write(r.stdout); open(d + '.ci.err', 'w').write(r.stderr)
    tail = [l for l in r.stdout.splitlines() if l.strip()][-1:]
    print('  %s: npm ci rc %d %s' % (tag, r.returncode, tail)); return {'rc': r.returncode, 'start': t0, 'end': now(), 'tail': tail}
def link_shared(d, shared_dir):
    os.makedirs(os.path.join(d, 'node_modules', '@secuura'), exist_ok=True)
    ln = os.path.join(d, 'node_modules', '@secuura', 'shared')
    if os.path.lexists(ln): os.rename(ln, ln + '.pre-link')   # a workspace symlink npm may have written: moved, never removed
    os.symlink(shared_dir, ln)
def blobs(c, sub):
    return sorted(subprocess.run(['git', '--git-dir', CL, 'ls-tree', '-r', c, DR + sub], capture_output=True, text=True).stdout.split('\n'))

# ---------------- PART A: the Dockerfile build path, base / r1 / head ----------------
print('--- PART A: the Dockerfile build path (shared-builder + builder stages mirrored on the host), sides base / r1 / head')
same_r1_head = {s: blobs(SIDES['r1'], s) == blobs(SIDES['head'], s) for s in ('packages/shared',)}
for svc in ('auth', 'originate'):
    same_r1_head['services/%s/package-lock.json' % svc] = blobs(SIDES['r1'], 'services/%s/package-lock.json' % svc) == blobs(SIDES['head'], 'services/%s/package-lock.json' % svc)
    same_r1_head['services/%s/package.json' % svc] = blobs(SIDES['r1'], 'services/%s/package.json' % svc) == blobs(SIDES['head'], 'services/%s/package.json' % svc)
res['r1_head_identical'] = same_r1_head
print('  r1 vs head byte-identical (ls-tree blob ids): %s' % same_r1_head)
SHARED = {}
for side in ('base', 'r1', 'head'):
    c = SIDES[side]
    sd = os.path.join(IP, 'build', '%s-shared' % side); fresh(sd)
    extract(c, 'packages/shared', sd)
    ci = npm_ci(sd, '%s shared' % side)
    b = sh(['npm', 'run', 'build'], cwd=sd); open(sd + '.build.out', 'w').write(b.stdout + b.stderr)
    SHARED[side] = sd
    res['tsc']['%s_shared' % side] = {'ci': ci, 'build_rc': b.returncode, 'errors': [l for l in (b.stdout + b.stderr).splitlines() if 'error TS' in l][:10]}
    print('  %s shared: npm run build rc %d' % (side, b.returncode))
    for svc in ('auth', 'originate'):
        d = os.path.join(IP, 'build', '%s-%s' % (side, svc)); fresh(d)
        extract(c, 'services/%s' % svc, d)
        ci = npm_ci(d, '%s %s' % (side, svc))
        link_shared(d, sd)
        b = sh(['npm', 'run', 'build'], cwd=d); out = b.stdout + b.stderr; open(d + '.build.out', 'w').write(out)
        errs = [l.strip() for l in out.splitlines() if 'error TS' in l]
        tscv = sh(['npx', 'tsc', '-v'], cwd=d).stdout.strip()
        row = {'ci': ci, 'build_rc': b.returncode, 'tsc': tscv, 'n_errors': len(errs), 'errors': errs[:12],
               'nodemailer': json.load(open(os.path.join(d, 'node_modules', 'nodemailer', 'package.json'))).get('version') if os.path.exists(os.path.join(d, 'node_modules', 'nodemailer', 'package.json')) else None}
        if side in ('r1', 'head'):
            lf = sh(['npx', '--no-install', 'tsc', '-p', '.', '--noEmit', '--listFilesOnly'], cwd=d)
            nf = sorted({re.sub(r'^.*?/node_modules/', 'node_modules/', l) for l in lf.stdout.splitlines() if '/nodemailer/' in l})
            row['listFilesOnly_nodemailer'] = {'bundled_dist_cjs': len([x for x in nf if x.startswith('node_modules/nodemailer/dist/cjs/')]), 'at_types': len([x for x in nf if x.startswith('node_modules/@types/nodemailer/')]),
                                               'entry_bundled_d_ts_read': 'node_modules/nodemailer/dist/cjs/nodemailer.d.ts' in nf, 'other': [x for x in nf if not x.startswith(('node_modules/nodemailer/dist/cjs/', 'node_modules/@types/nodemailer/'))][:6]}
        res['tsc']['%s_%s' % (side, svc)] = row
        print('  %s %s: nodemailer %s | npm run build (%s) rc %d | %d error TS line(s) %s' % (side, svc, row['nodemailer'], tscv, b.returncode, len(errs), errs[:4]))
        if side in ('r1', 'head'): print('    tsc --listFilesOnly, nodemailer declaration files read: %s' % row['listFilesOnly_nodemailer'])

# ---------------- PART B: nodemailer / morgan in the base and head service installs ----------------
print('--- PART B: nodemailer / morgan inside the base and head standalone service installs (installprobe_gate42.cjs)')
for side in ('base', 'head'):
    for svc in ('auth', 'originate'):
        d = os.path.join(IP, 'build', '%s-%s' % (side, svc)); key = '%s_%s' % (side, svc)
        q = sh(['node', os.path.join(GS, 'installprobe_gate42.cjs'), d])
        try: pr = json.loads(q.stdout.strip().splitlines()[-1])
        except Exception: pr = {'probe_error': (q.stdout + q.stderr)[-400:]}
        res['runs'][key] = {'npm_ci_rc': res['tsc'][key]['ci']['rc'], 'probe_rc': q.returncode, 'probe': pr}
        print('  %s: probe rc %d | %s' % (key, q.returncode, json.dumps({k: v for k, v in pr.items() if k != 'morgan_combined'})[:500]))
        if pr.get('morgan_combined'): print('    morgan combined lines: %s' % pr['morgan_combined']['lines'])

# ---------------- PART C: the runtime-moved services (KS-1379's condition) ----------------
print('--- PART C: the runtime-moved services, standalone installs at base and head: queue (bullmq -> msgpackr), m365-integration + packages/shared (@azure/identity -> msal-node)')
PK = ('bullmq', 'msgpackr', '@azure/identity', '@azure/msal-node', '@azure/msal-common')
def copies(d):
    """every installed copy of the PK packages, by path, walking ONLY the node_modules structure (package dirs and their nested node_modules;
    a symlink — the @secuura/shared link — is not followed)"""
    out = []
    def nm_dir(nmd):
        if not os.path.isdir(nmd): return
        for e in sorted(os.listdir(nmd)):
            if e.startswith('.'): continue
            p = os.path.join(nmd, e)
            if e.startswith('@') and os.path.isdir(p) and not os.path.islink(p):
                for e2 in sorted(os.listdir(p)): pkg(os.path.join(p, e2), e + '/' + e2)
            else: pkg(p, e)
    def pkg(p, name):
        if os.path.islink(p) or not os.path.isdir(p): return
        if name in PK and os.path.exists(os.path.join(p, 'package.json')):
            try: out.append((os.path.relpath(p, d), json.load(open(os.path.join(p, 'package.json'))).get('version')))
            except Exception: pass
        nm_dir(os.path.join(p, 'node_modules'))
    nm_dir(os.path.join(d, 'node_modules'))
    return sorted(out)
def suite(d, tag, fallback_vitest=None):
    """the workspace's own vitest suite in its STANDALONE install. The vitest binary is the install's own node_modules/.bin/vitest; a lock that carries
    NO vitest (packages/shared's standalone lock: vitest lives only in the ROOT lock) uses the named FALLBACK binary (the same side's m365-integration
    standalone install) and SAYS SO — never an `npx` download (a registry vitest crashed on a missing rolldown binding at drafting, measured)"""
    t0 = now(); load = sh(['uptime']).stdout.strip().split('load average')[-1]
    own = os.path.join(d, 'node_modules', '.bin', 'vitest'); vb = own if os.path.exists(own) else fallback_vitest
    if not vb or not os.path.exists(vb):
        print('  %s suite: NO vitest binary (own %s, fallback %s) — NOT RUN' % (tag, os.path.exists(own), fallback_vitest)); return {'rc': None, 'summary': [], 'vitest': None, 'start': t0, 'end': now(), 'load': load.strip(': ')}
    r = sh([vb, 'run'], cwd=d, timeout=900, env=dict(os.environ, CI='true', NO_COLOR='1'))
    out = r.stdout + r.stderr; open(d + '.suite.out', 'w').write(out)
    s = [l.strip() for l in out.splitlines() if re.match(r'^\s*(Test Files|Tests)\s', l)]
    vver = sh([vb, '--version'], cwd=d).stdout.strip()
    se = [l.strip() for l in out.splitlines() if l.strip().startswith('Error:')][:1] if not s else []   # a suite that never STARTED is not a red suite: its first Error line is recorded
    print('  %s suite: rc %d | %s | vitest %s (%s) | load%s' % (tag, r.returncode, s, vver, 'OWN install' if vb == own else 'FALLBACK ' + vb, load))
    if se: print('    %s: the suite did NOT START (no Test Files line): %s' % (tag, se[0][:200]))
    return {'rc': r.returncode, 'summary': s or (['DID NOT START: ' + se[0][:160]] if se else []), 'vitest': vver, 'vitest_bin': 'own' if vb == own else vb, 'start': t0, 'end': now(), 'load': load.strip(': ')}
for side in ('base', 'head'):
    c = SIDES[side]
    # packages/shared: its own standalone install IS the PART A shared-builder dir (source + standalone node_modules)
    sd = SHARED[side]
    res['runtime']['%s_shared' % side] = {'copies': copies(sd)}
    for svc in ('queue', 'm365-integration'):
        d = os.path.join(IP, 'rt', '%s-%s' % (side, svc)); fresh(d)
        extract(c, 'services/%s' % svc, d)
        if svc == 'queue':   # the queue Dockerfile deletes the @secuura/shared dependency line before its `npm ci` (READ, services/queue/Dockerfile)
            pj = os.path.join(d, 'package.json'); t = open(pj).read(); t2 = '\n'.join(l for l in t.split('\n') if '"@secuura/shared":' not in l)
            if t2 != t: open(pj, 'w').write(t2)
        ci = npm_ci(d, '%s %s' % (side, svc)); link_shared(d, sd)
        res['runtime']['%s_%s' % (side, svc)] = {'ci': ci, 'copies': copies(d)}
    for key in ('%s_shared' % side, '%s_queue' % side, '%s_m365-integration' % side):
        d = SHARED[side] if key.endswith('_shared') else os.path.join(IP, 'rt', key.replace('_', '-', 1))
        q = sh(['node', os.path.join(GS, 'installprobe_rt_gate42.cjs'), d])
        try: sm = json.loads(q.stdout.strip().splitlines()[-1])
        except Exception: sm = {'probe_error': (q.stdout + q.stderr)[-400:]}
        res['runtime'][key]['smoke_rc'] = q.returncode; res['runtime'][key]['smoke'] = sm
        print('  %s copies %s' % (key, res['runtime'][key]['copies']))
        print('  %s load smoke rc %d %s' % (key, q.returncode, json.dumps(sm)[:400]))
        res['suites'][key] = suite(d, key, fallback_vitest=os.path.join(IP, 'rt', '%s-m365-integration' % side, 'node_modules', '.bin', 'vitest'))

def vt(v): return tuple(int(x) for x in re.findall(r'\d+', v or '0')[:3]) or (0,)
R = res['runs']; T = res['tsc']; RT = res['runtime']
def g(k, *p):
    x = R.get(k, {}).get('probe')
    for q in p: x = (x or {}).get(q) if isinstance(x, dict) or x is None else None
    return x
def cv(key, suffix): return [v for p_, v in RT[key]['copies'] if p_.endswith('node_modules/' + suffix)]
def nested_msal(key): return [v for p_, v in RT[key]['copies'] if p_.endswith('@azure/msal-node') and ('@azure/identity/node_modules' in p_ or key.endswith('_shared'))]
TS2503 = lambda errs: len(errs) == 2 and all('src/services/email.ts' in e and 'TS2503' in e and "namespace 'nodemailer'" in e for e in errs)
CT = {
 'CT1 every install and build step ran (npm ci rc 0 everywhere, shared builds rc 0, probes rc 0)': all(v['ci']['rc'] == 0 for k, v in T.items()) and all(T['%s_shared' % s]['build_rc'] == 0 for s in SIDES) and all(v['npm_ci_rc'] == 0 and v['probe_rc'] == 0 for v in R.values()) and all(RT[k].get('ci', {'rc': 0})['rc'] == 0 for k in RT),
 'CT2 BASE resolves nodemailer 9.1.1 (the instrument sees the OLD major)': all(g('base_%s' % s, 'nodemailer', 'version') == '9.1.1' for s in ('auth', 'originate')),
 'CT3 HEAD resolves nodemailer 10.x >= 10.0.2 (the bump is what RUNS in a clean install)': all(vt(g('head_%s' % s, 'nodemailer', 'version')) >= (10, 0, 2) and vt(g('head_%s' % s, 'nodemailer', 'version'))[0] == 10 for s in ('auth', 'originate')),
 'CT4 morgan combined: the control line logs on both sides': bool(g('base_auth', 'morgan_combined', 'control_logs')) and bool(g('head_auth', 'morgan_combined', 'control_logs')),
 'CT5 BASE morgan logs the planted quote RAW, HEAD escapes it': g('base_auth', 'morgan_combined', 'planted_raw_present') is True and g('base_auth', 'morgan_combined', 'planted_quote_escaped') is False and g('head_auth', 'morgan_combined', 'planted_quote_escaped') is True,
 'CT6 the call-site shapes build on BOTH majors (createTransport SMTP shape + sendMail via streamTransport)': all(g(k, 'sendMail', 'ok') is True and g(k, 'smtp_transport', 'name') == 'SMTP' for k in R),
 'CT7 BASE `npm run build` rc 0 with 0 error TS lines for auth AND originate (the mirror builds a green tree)': all(T['base_%s' % s]['build_rc'] == 0 and T['base_%s' % s]['n_errors'] == 0 for s in ('auth', 'originate')),
 'CT8 R1 (the round-1 head gate41 graded NO GO) `npm run build` rc != 0 with EXACTLY the TS2503 pair in src/services/email.ts per service (the instrument SEES N-1339-1)': all(T['r1_%s' % s]['build_rc'] != 0 and TS2503(T['r1_%s' % s]['errors']) for s in ('auth', 'originate')),
 'CT9 HEAD `npm run build` rc 0 with 0 error TS lines for auth AND originate (the round-2 fix, on nodemailer 10)': all(T['head_%s' % s]['build_rc'] == 0 and T['head_%s' % s]['n_errors'] == 0 and vt(T['head_%s' % s]['nodemailer'])[0] == 10 for s in ('auth', 'originate')),
 'CT10 r1 and head: packages/shared tree and both service manifests + locks byte-identical (CT8 vs CT9 differ ONLY by the round-2 source)': all(res['r1_head_identical'].values()),
 'CT11 queue msgpackr major 1 at BASE and 2 at HEAD (the instrument sees the KS-1379 move)': [vt(v)[0] for v in cv('base_queue', 'msgpackr')] == [1] and [vt(v)[0] for v in cv('head_queue', 'msgpackr')] == [2],
 'CT12 the @azure/identity-nested (m365) and the shared msal-node: major 5 at BASE and 6 at HEAD': all([vt(v)[0] for v in nested_msal('%s_%s' % (sd_, w))] == [m] for sd_, m in (('base', 5), ('head', 6)) for w in ('m365-integration', 'shared')),
 'CT13 every runtime load smoke ok at both sides': all(RT[k].get('smoke', {}).get('ok') is True for k in RT),
}
res['controls'] = CT
res['_summary'] = {
 'tsc': {k: {'build_rc': v['build_rc'], 'n_errors': v.get('n_errors'), 'nodemailer': v.get('nodemailer')} for k, v in sorted(T.items()) if not k.endswith('_shared')},
 'nodemailer_probe': {k: {'nodemailer': g(k, 'nodemailer', 'version'), 'entry': g(k, 'nodemailer', 'resolved'), 'morgan': g(k, 'morgan', 'version'), '@types/nodemailer': g(k, 'types_nodemailer'),
                          'sendMail_ok': g(k, 'sendMail', 'ok'), 'morgan_planted_quote_escaped': g(k, 'morgan_combined', 'planted_quote_escaped')} for k in sorted(R)},
 'runtime_copies': {k: v['copies'] for k, v in sorted(RT.items())},
 'standalone_suites': {k: {'rc': v['rc'], 'summary': v['summary']} for k, v in sorted(res['suites'].items())},
 'tsc_reads': {k: T[k].get('listFilesOnly_nodemailer') for k in ('r1_auth', 'r1_originate', 'head_auth', 'head_originate')}}
json.dump(res, open(os.path.join(GS, 'installprobe_gate42.json'), 'w'), indent=1)
for k, v in CT.items(): print('  %s %s' % ('PASS' if v else 'FAIL', k))
print('SUMMARY %s' % json.dumps(res['_summary']))
print('installprobe_gate42: CONTROLS %s -> installprobe_gate42.json' % ('ALL PASS' if all(CT.values()) else 'FAIL'))
sys.exit(0 if all(CT.values()) else 1)
