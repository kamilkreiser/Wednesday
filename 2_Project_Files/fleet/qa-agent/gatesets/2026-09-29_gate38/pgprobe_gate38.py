#!/usr/bin/env python3
"""pgprobe_gate38.py <scratchpad> — the drafter's REAL-POSTGRES measurement for #1332 (KS-1054), the gate38 kit (kit.json and pins_gate38.json beside
this script; run AFTER predict_gate38.py). The seat NEVER executed 039 ("No Postgres here ... does not prove the guarded SQL parses in PostgreSQL"); this
is the two-sided FRESH-DATABASE drill, done by the drafter as a PREDICTION for the gate (the gate re-measures; a drafter's run is not the gate's evidence).

METHOD (gate37's gate method, its report's THE ROTATION TABLE: a throwaway Homebrew PostgreSQL 18 cluster, `-c listen_addresses=''` — NO TCP listener —
and `-k <a socket dir shorter than 103 bytes>`, stopped with `pg_ctl -m fast stop`, the data dir kept, never deleted; never the native :5432, never a
container). The data dir lives in the scratchpad (<scratchpad>/g38_pg/data); ONLY the socket dir is a short `mkdtemp('/tmp/q38.')` (the scratchpad path
is too long for a unix socket — gate37's drafter measured that limit). Every product byte is EXTRACTED from the scratch clone (g38_sp/clone.git) by
`git archive` (a read verb) at #1332's merge-base and at its head: Blockchain/Dev/migrations/ and api-gateway src/startup-migrations.ts (+ the head's
src/services/startupMigrationStatus.ts). The REAL `runStartupMigrations()` is then run — by node with the checkout's tsx CJS hook (`--require tsx/dist/cjs/index.cjs`), `pg` resolved from the checkout's
node_modules via NODE_PATH (READ-only use; nothing is written into the checkout) — against:
  BARE-<side>:  a fresh database with NOTHING in it (a database the gateway meets without docker/init), booted TWICE;
  INIT-<side>:  a fresh database seeded with the tree's own docker/init/*.sql first (the docker-compose first start), booted ONCE — the guard's inert path.
After each boot the runner reads: to_regprocedure('auth_find_oauth_app_by_client_id(text)'), the oauth_apps_auth_lookup policy, oauth_apps itself, the
_secuura_migrations row for 039, a call of the function, the run's return value and (head) the recorded summary that /health and /health/ready serve.
CONTROLS: CT1 a wrong socket dir does not connect (the socket check can fail); CT2 the postmaster holds no TCP listener (`SHOW listen_addresses` == '');
CT3 BARE-base boot 1 FAILS 039 (the defect the PR exists for is reproduced — otherwise the drill cannot tell base from head).
Writes pgprobe_gate38.json beside this script; prints a summary; the raw per-boot JSON lines go to <scratchpad>/g38_pg/boots/. Usage: pgprobe_gate38.py <scratchpad>"""
import json, os, re, subprocess, sys, tempfile, datetime, glob, tarfile, io
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_%s.json' % K['kit']), encoding='utf-8'))
SP = sys.argv[1]
CL = os.path.join(SP, 'g38_sp', 'clone.git')
W = os.path.join(SP, 'g38_pg'); os.makedirs(os.path.join(W, 'boots'), exist_ok=True)
DEV = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev'
TSX = ['node', '--require', DEV + '/node_modules/tsx/dist/cjs/index.cjs']   # the tsx CJS hook, NOT the tsx CLI: the CLI opens an IPC pipe in TMPDIR and a scratchpad TMPDIR is too long for a unix socket (MEASURED: listen EINVAL)
PGB = '/opt/homebrew/bin/'
RUNNER = os.path.join(G, 'pgprobe_gate38.runner.ts')
PORT = '55438'   # names the socket file only: listen_addresses='' opens NO TCP port
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def run(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
pr = P['prs']['1332']; SIDES = {'base': pr['merge_base'], 'head': pr['head']}
print('pgprobe_gate38 %s | #1332 merge-base %s head %s | work %s' % (now(), SIDES['base'][:12], SIDES['head'][:12], W))
# 1. extract each side (git archive: a READ verb on the scratch clone; tar writes only under the scratchpad)
for side, rev in SIDES.items():
    d = os.path.join(W, side)
    if os.path.isdir(d): print('  %s already extracted at %s (a re-run reuses it: the rev is pinned)' % (side, d)); continue
    paths = ['Blockchain/Dev/migrations', 'Blockchain/Dev/docker/init', 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts']
    if side == 'head': paths.append('Blockchain/Dev/services/api-gateway/src/services/startupMigrationStatus.ts')
    a = subprocess.run(['git', '--git-dir', CL, 'archive', '--format=tar', rev] + paths, capture_output=True)
    if a.returncode: print('REFUSING: git archive %s rc %d %s' % (side, a.returncode, a.stderr[-300:])); sys.exit(1)
    tarfile.open(fileobj=io.BytesIO(a.stdout)).extractall(d)
    print('  extracted %s @ %s -> %s (%d bytes of tar)' % (side, rev[:12], d, len(a.stdout)))
# 2. the throwaway cluster: data in the scratchpad, the socket in a SHORT /tmp dir, NO TCP listener
data = os.path.join(W, 'data_' + datetime.datetime.now().strftime('%H%M%S'))
sock = tempfile.mkdtemp(prefix='q38.', dir='/tmp')
assert len(sock + '/.s.PGSQL.' + PORT) < 103, 'socket path too long'
r = run([PGB + 'initdb-18', '-D', data, '-U', 'q38', '-A', 'trust', '--no-locale', '-E', 'UTF8'])
print('  initdb-18 rc %d -> %s' % (r.returncode, data))
if r.returncode: print(r.stderr[-500:]); sys.exit(1)
r = run([PGB + 'pg_ctl-18', '-D', data, '-l', os.path.join(W, os.path.basename(data) + '.log'), '-w', '-o', "-c listen_addresses='' -k %s -p %s" % (sock, PORT), 'start'])
print('  pg_ctl-18 start rc %d (socket dir %s, %d bytes incl. the socket file)' % (r.returncode, sock, len(sock + '/.s.PGSQL.' + PORT)))
if r.returncode: print(r.stdout[-500:], r.stderr[-500:]); sys.exit(1)
res = {'engine': None, 'socket_dir': sock, 'data_dir': data, 'port_name_only': PORT, 'runs': {}, 'controls': {}}
def psql(db, sql, stop=True):
    return run([PGB + 'psql-18', '-h', sock, '-p', PORT, '-U', 'q38', '-d', db, '-v', 'ON_ERROR_STOP=%d' % (1 if stop else 0), '-tAc', sql])
try:
    res['engine'] = psql('postgres', 'SELECT version()').stdout.strip()
    res['controls']['CT1 a wrong socket dir does not connect'] = run([PGB + 'psql-18', '-h', sock + '/nope', '-p', PORT, '-U', 'q38', '-d', 'postgres', '-tAc', 'SELECT 1']).returncode != 0
    res['controls']['CT2 no TCP listener (listen_addresses is empty)'] = psql('postgres', 'SHOW listen_addresses').stdout.strip() == ''
    lo = run(['/usr/sbin/lsof', '-a', '-p', open(os.path.join(data, 'postmaster.pid')).read().split()[0], '-i'])
    res['controls']['CT2b lsof: the postmaster holds 0 inet sockets'] = lo.stdout.strip() == ''
    print('  engine %s' % res['engine'])
    def boot(db, side, tag):
        smp = os.path.join(W, side, 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts')
        mig = os.path.join(W, side, 'Blockchain/Dev/migrations')
        url = 'postgresql://q38@localhost:%s/%s?host=%s' % (PORT, db, sock)
        env = dict(os.environ, NODE_PATH=DEV + '/node_modules', TMPDIR=os.path.join(W, 'tmp'))
        os.makedirs(env['TMPDIR'], exist_ok=True)
        r = run(TSX + [RUNNER, smp, mig, url], env=env, timeout=600)
        open(os.path.join(W, 'boots', '%s.stdout' % tag), 'w').write(r.stdout); open(os.path.join(W, 'boots', '%s.stderr' % tag), 'w').write(r.stderr)
        js = [l for l in r.stdout.splitlines() if l.startswith('{')]
        out = json.loads(js[-1]) if js else {'fatal': 'no JSON line (rc %d) %s' % (r.returncode, r.stderr[-300:])}
        out['rc'] = r.returncode
        f039 = [w for w in out.get('warn', []) if '039' in w]
        print('  %-16s rc %s | 039 tracked %s | fn %s | policy %s | oauth_apps %s | lookup %s | ret %s | warn %d (039: %s)' % (tag, r.returncode, out.get('db', {}).get('tracked_039'), out.get('db', {}).get('fn_auth_find_oauth_app_by_client_id'),
              out.get('db', {}).get('oauth_apps_auth_lookup_policy'), out.get('db', {}).get('oauth_apps'), str(out.get('db', {}).get('lookup_call'))[:60], json.dumps(out.get('ret'))[:120], len(out.get('warn', [])), [x[:110] for x in f039]))
        return out
    for side in ('base', 'head'):
        db = 'bare_' + side
        psql('postgres', 'CREATE DATABASE %s' % db)
        res['runs']['BARE-%s boot 1' % side] = boot(db, side, 'bare_%s_boot1' % side)
        res['runs']['BARE-%s boot 2' % side] = boot(db, side, 'bare_%s_boot2' % side)
        db2 = 'init_' + side
        psql('postgres', 'CREATE DATABASE %s' % db2)
        inits = sorted(glob.glob(os.path.join(W, side, 'Blockchain/Dev/docker/init/*.sql')))
        ie = []
        for f in inits:
            rr = run([PGB + 'psql-18', '-h', sock, '-p', PORT, '-U', 'q38', '-d', db2, '-v', 'ON_ERROR_STOP=0', '-q', '-f', f])
            errs = [l for l in rr.stderr.splitlines() if 'ERROR' in l]
            if errs: ie.append((os.path.basename(f), len(errs), errs[0][:140]))
        res['runs']['INIT-%s docker/init errors' % side] = ie
        print('  INIT-%s: %d docker/init files applied; files with ERROR lines: %s' % (side, len(inits), [(a, b) for a, b, c in ie]))
        res['runs']['INIT-%s boot 1' % side] = boot(db2, side, 'init_%s_boot1' % side)
finally:
    r = run([PGB + 'pg_ctl-18', '-D', data, '-m', 'fast', 'stop'])
    print('  pg_ctl-18 -m fast stop rc %d (the data dir is KEPT at %s; the socket dir %s is left empty, never deleted)' % (r.returncode, data, sock))
    res['stopped_rc'] = r.returncode
R = res['runs']
def fnok(x): return str(x.get('db', {}).get('fn_auth_find_oauth_app_by_client_id')) not in ('None', '') and not str(x.get('db', {}).get('fn_auth_find_oauth_app_by_client_id')).startswith('ERROR')
res['controls']['CT3 BARE-base boot 1 FAILS 039 (the defect reproduced)'] = R['BARE-base boot 1'].get('db', {}).get('tracked_039') == 0 and any('039' in w for w in R['BARE-base boot 1'].get('warn', []))
summ = {
 'base: bare DB boot 1 fails 039 (not tracked), boot 2 applies it (tracked, function present)': res['controls']['CT3 BARE-base boot 1 FAILS 039 (the defect reproduced)'] and R['BARE-base boot 2'].get('db', {}).get('tracked_039') == 1 and fnok(R['BARE-base boot 2']),
 'head: bare DB boot 1 records 039 (tracked) with the function ABSENT': R['BARE-head boot 1'].get('db', {}).get('tracked_039') == 1 and not fnok(R['BARE-head boot 1']),
 'head: bare DB boot 2 STILL has no auth_find_oauth_app_by_client_id (039 never re-runs)': R['BARE-head boot 2'].get('db', {}).get('tracked_039') == 1 and not fnok(R['BARE-head boot 2']),
 'head: bare DB boot 2 has no oauth_apps_auth_lookup policy': R['BARE-head boot 2'].get('db', {}).get('oauth_apps_auth_lookup_policy') == 0,
 'base: bare DB boot 2 HAS the oauth_apps_auth_lookup policy': R['BARE-base boot 2'].get('db', {}).get('oauth_apps_auth_lookup_policy') == 1,
 'docker-init DB: 039 tracked and the function present at base AND head after ONE boot (the guard inert)': all(R['INIT-%s boot 1' % s].get('db', {}).get('tracked_039') == 1 and fnok(R['INIT-%s boot 1' % s]) for s in ('base', 'head')),
 'head: the recorded summary after bare boot 1 reads ran:true and failed == the run\'s own count': isinstance(R['BARE-head boot 1'].get('recorded'), dict) and R['BARE-head boot 1']['recorded'].get('ran') is True and R['BARE-head boot 1'].get('ret') == R['BARE-head boot 1'].get('recorded'),
 'controls all behaved': all(res['controls'].values()),
}
res['_summary'] = summ
res['_extracted_from'] = SIDES
res['measured_at'] = now()
json.dump(res, open(os.path.join(G, 'pgprobe_gate38.json'), 'w'), indent=1)
print('  controls: %s' % res['controls'])
for k, v in summ.items(): print('  SUMMARY %-110s %s' % (k, v))
print('  recorded summaries (head): boot1 %s | boot2 %s | init %s' % (json.dumps(R['BARE-head boot 1'].get('recorded')), json.dumps(R['BARE-head boot 2'].get('recorded')), json.dumps(R['INIT-head boot 1'].get('recorded'))))
print('  base return values: boot1 %s | boot2 %s' % (json.dumps(R['BARE-base boot 1'].get('ret')), json.dumps(R['BARE-base boot 2'].get('ret'))))
sys.exit(0 if res['controls'] and all(res['controls'].values()) else 1)
