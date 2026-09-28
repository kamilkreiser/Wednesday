#!/usr/bin/env python3
"""pgprobe_gate40.py <scratchpad> — the drafter's REAL-POSTGRES measurement of #1338 (KS-1370) for the gate40 kit (kit.json and pins_gate40.json
beside this script; run AFTER predict_gate40.py). Shape copied from gate39's pgprobe (gate38 -> gate37 lineage: the same throwaway-cluster method),
re-cut for KS-1370. A drafter's run is a PREDICTION for the gate, never the gate's evidence.

WHY (requirement 2 of Wednesday's commission): the builder's drill ran as `postgres` (rolsuper, rolbypassrls), so it could not show whether the
SECURITY DEFINER carve-out security_find_api_key_by_hash (039, owner secuura_auth_lookup, permissive policy svc_api_keys_auth_lookup) actually returns
the row under FORCE RLS — the whole premise of half (ii). HERE every product module instance connects as `secuura_app`, created by the REAL api-gateway
provisionAppRole() (APP_DB_PASSWORD set; NOSUPERUSER NOINHERIT NOBYPASSRLS, read back from pg_roles) — the role docker-compose.yml and
deployment/azure/deploy.sh give every data service. The superuser run of the same drill is kept ONLY as the control that shows what a superuser
cannot see.

METHOD: a throwaway Homebrew PostgreSQL 18 cluster (initdb-18 -U postgres --auth=trust; trust on the LOCAL socket only, disclosed), `-c
listen_addresses=''` (NO TCP listener), `-k <a socket dir shorter than 103 bytes>` (a short `mkdtemp('/tmp/q40.')`), the data dir in the scratchpad
(<scratchpad>/g40_pg/data, the Data volume), stopped with `pg_ctl -m fast stop`, the data dir KEPT, never deleted; never the native :5432, never a
container. Every product byte is EXTRACTED from the scratch clone (g40_sp/clone.git) by `git archive` (a read verb) at base (the pinned develop ==
#1338's merge-base) and head; ARM sides are COPIES of head with ONE asserted edit each (the extract is never edited). The schema is built on each
fresh database by the REAL `runStartupMigrations()` (booted twice). Node resolves the product's dependencies through a SYMLINK FARM
(<side>/Blockchain/Dev/node_modules -> every entry of the checkout's node_modules, READ-only use) EXCEPT @secuura/shared, which is a shim whose `main`
is the SIDE's OWN packages/shared/src/index.ts (compiled on require by the checkout's tsx CJS hook) — the checkout's built shared dist is from
2026-09-11 and is NOT used.

SIDES: base (RED expected), head (GREEN expected), and four ARMS of head (each must turn one cell): armA_nosticky (design call (a): the
`if (revokedInMemory)` line removed -> A1 answers valid), armB_noevict (design call (b): the eviction removed -> D1 evicted false), armC_revive
(half (i) put back to dbSaveApiKey AND half (ii) neutralised -> R2 revives the row, the seat's W4), armD_half1only (half (ii) neutralised, half (i)
kept -> R2 answers valid but the row STAYS revoked: each half is load-bearing on its own).
CONTROLS: CT1 a wrong socket dir does not connect; CT2 `SHOW listen_addresses` == ''; CT2b `lsof -a -p <postmaster pid> -i` finds 0 inet sockets while
the same lsof on a pid that holds one (the native pg, if running) finds >0 (a control that returns the same number as its subject is not a control);
CT3 base RED / head GREEN on R2 (the drill discriminates); CT4 every arm turns ITS cell and no other design cell.
Writes pgprobe_gate40.json beside this script; prints a summary; raw per-run output under <scratchpad>/g40_pg/. Usage: pgprobe_gate40.py <scratchpad>"""
import json, os, re, subprocess, sys, tempfile, datetime, tarfile, io, shutil, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_%s.json' % K['kit']), encoding='utf-8'))
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP): print('usage: pgprobe_gate40.py <scratchpad on the Data volume>'); sys.exit(9)
CL = os.path.join(SP, 'g40_sp', 'clone.git')
W = os.path.join(SP, 'g40_pg'); os.makedirs(os.path.join(W, 'runs'), exist_ok=True)
DEVCO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev'
TSX = ['node', '--require', DEVCO + '/node_modules/tsx/dist/cjs/index.cjs']   # the tsx CJS hook, NOT the tsx CLI (its IPC pipe in a long TMPDIR fails: listen EINVAL, gate38 MEASURED)
PGB = '/opt/homebrew/bin/'
RUNNER = os.path.join(G, 'pgprobe_gate40.runner.ts'); DRILL = os.path.join(G, 'pgprobe_gate40.drill.cjs')
PORT = '55440'   # names the socket file only: listen_addresses='' opens NO TCP port
SEC = 'Blockchain/Dev/services/security/src/index.ts'
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def run(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
pr = P['prs']['1338']
SIDES = {'base': pr['merge_base'], 'head': pr['head']}
assert P['develop'] == pr['merge_base'], 'the pinned develop is not #1338\'s merge-base — re-cut the sides'
PATHS = ['Blockchain/Dev/services/security', 'Blockchain/Dev/packages/shared', 'Blockchain/Dev/migrations', 'Blockchain/Dev/docker/init', 'Blockchain/Dev/package.json',
         'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts', 'Blockchain/Dev/services/api-gateway/src/services/startupMigrationStatus.ts']
print('pgprobe_gate40 %s | #1338 base %s head %s | work %s' % (now(), SIDES['base'][:12], SIDES['head'][:12], W))
RES = {'engine': None, 'controls': {}, 'runs': {}, 'boots': {}, 'arms': {}, '_summary': {}}
# 1. extract base and head (git archive: a READ verb; tar writes only under the scratchpad)
for side, rev in SIDES.items():
    d = os.path.join(W, side)
    if not os.path.isdir(os.path.join(d, 'Blockchain/Dev/services/security')):
        a = subprocess.run(['git', '--git-dir', CL, 'archive', '--format=tar', rev] + PATHS, capture_output=True)
        if a.returncode: print('REFUSING: git archive %s rc %d %s' % (side, a.returncode, a.stderr[-300:])); sys.exit(1)
        tarfile.open(fileobj=io.BytesIO(a.stdout)).extractall(d)
    blob = run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (rev, SEC)]).stdout.strip()
    got = run(['git', 'hash-object', os.path.join(d, SEC)]).stdout.strip()
    assert blob == got, '%s: the extracted index.ts %s != the blob at %s %s' % (side, got, rev[:12], blob)
    print('  %s @ %s extracted; index.ts blob %s == the clone\'s' % (side, rev[:12], got[:12]))
same = {p: run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (SIDES['base'], p)]).stdout == run(['git', '--git-dir', CL, 'rev-parse', '%s:%s' % (SIDES['head'], p)]).stdout for p in PATHS[1:]}
print('  base == head for every path but services/security (the schema, shared and the gateway runner are the same bytes): %s' % all(same.values()))
RES['base_eq_head_outside_security'] = same
# 2. the ARM copies of head: ONE asserted edit each (count == 1 before, 0 after)
ARMS = {
 'armA_nosticky': [('      if (revokedInMemory) apiKey.isActive = false;\n', '')],
 'armB_noevict': [('      if (storedResult.rows.length === 0) {\n        memApiKeys.delete(apiKey.id);\n', '      if (storedResult.rows.length === 0) {\n')],
 'armC_revive': [('  await dbRecordApiKeyUsage(apiKey);\n', '  await dbSaveApiKey(apiKey);\n'), ('  if (apiKey && isDbAvailable()) {\n', '  if (false && apiKey && isDbAvailable()) {\n')],
 'armD_half1only': [('  if (apiKey && isDbAvailable()) {\n', '  if (false && apiKey && isDbAvailable()) {\n')],
}
for arm, edits in ARMS.items():
    d = os.path.join(W, arm)
    if os.path.isdir(d): shutil.move(d, os.path.join(W, '_quarantine_2026-09-29', arm + '.' + datetime.datetime.now().strftime('%H%M%S')))
    shutil.copytree(os.path.join(W, 'head'), d, symlinks=True, ignore=shutil.ignore_patterns('node_modules'))
    f = os.path.join(d, SEC); t = open(f, encoding='utf-8').read()
    for old, new in edits:
        assert t.count(old) == 1, '%s: anchor count %d for %r' % (arm, t.count(old), old[:60])
        t = t.replace(old, new); assert t.count(old) == 0 or new.count(old) == t.count(old)
    open(f, 'w', encoding='utf-8').write(t)
    RES['arms'][arm] = {'edits': [(o.strip()[:80], n.strip()[:80]) for o, n in edits], 'sha256': hashlib.sha256(t.encode()).hexdigest()[:16]}
    print('  %s: %d asserted edit(s) on a COPY of head' % (arm, len(edits)))
# 3. the node_modules symlink farm per side (READ-only use of the checkout's installed packages) + the @secuura/shared shim -> the side's own source
def farm(side):
    dev = os.path.join(W, side, 'Blockchain/Dev'); nm = os.path.join(dev, 'node_modules')
    if os.path.isdir(nm) and not os.path.islink(nm):
        shutil.move(nm, os.path.join(W, '_quarantine_2026-09-29', side + '.node_modules.' + datetime.datetime.now().strftime('%H%M%S')))
    os.makedirs(os.path.join(nm, '@secuura', 'shared'))
    for e in os.listdir(os.path.join(DEVCO, 'node_modules')):
        if e in ('@secuura', '.bin', '.package-lock.json'): continue
        os.symlink(os.path.join(DEVCO, 'node_modules', e), os.path.join(nm, e))
    for e in os.listdir(os.path.join(DEVCO, 'node_modules', '@secuura')):
        if e != 'shared': os.symlink(os.path.join(DEVCO, 'node_modules', '@secuura', e), os.path.join(nm, '@secuura', e))
    json.dump({'name': '@secuura/shared', 'version': '0.0.0-gate40-shim', 'main': os.path.join(dev, 'packages/shared/src/index.ts')}, open(os.path.join(nm, '@secuura', 'shared', 'package.json'), 'w'))
    snm = os.path.join(dev, 'services/security/node_modules')
    if not os.path.exists(snm): os.symlink(os.path.join(DEVCO, 'services/security/node_modules'), snm)
    return dev
os.makedirs(os.path.join(W, '_quarantine_2026-09-29'), exist_ok=True)
DEVS = {s: farm(s) for s in list(SIDES) + list(ARMS)}
# 4. the cluster
DATA = os.path.join(W, 'data')
if os.path.isdir(DATA): shutil.move(DATA, os.path.join(W, '_quarantine_2026-09-29', 'data.' + datetime.datetime.now().strftime('%H%M%S')))
r = run([PGB + 'initdb-18', '-U', 'postgres', '--auth=trust', '-D', DATA]); assert r.returncode == 0, r.stderr[-400:]
SOCK = tempfile.mkdtemp(prefix='q40.', dir='/tmp'); assert len(SOCK + '/.s.PGSQL.' + PORT) < 103
r = run([PGB + 'pg_ctl-18', '-D', DATA, '-l', os.path.join(W, 'pg.log'), '-w', '-o', "-c listen_addresses='' -k %s -p %s" % (SOCK, PORT), 'start']); assert r.returncode == 0, r.stdout[-400:] + r.stderr[-400:]
PSQL = lambda db, sql, u='postgres': run([PGB + 'psql-18', '-h', SOCK, '-p', PORT, '-U', u, '-d', db, '-tAc', sql])
RES['engine'] = PSQL('postgres', 'SELECT version()').stdout.strip()
pid = open(os.path.join(DATA, 'postmaster.pid')).readline().strip()
ct1 = run([PGB + 'psql-18', '-h', '/tmp/no-such-q40', '-p', PORT, '-U', 'postgres', '-d', 'postgres', '-tAc', 'SELECT 1'])
lsof_me = run(['lsof', '-a', '-p', pid, '-i']).stdout.strip().splitlines()
nat = run(['pgrep', '-x', 'postgres']).stdout.split(); nat = [x for x in nat if x != pid]
lsof_ctl = []
for x in nat:
    lsof_ctl = run(['lsof', '-a', '-p', x, '-i']).stdout.strip().splitlines()
    if lsof_ctl: break
RES['controls'] = {'CT1 wrong socket dir does not connect': ct1.returncode != 0, "CT2 SHOW listen_addresses == ''": PSQL('postgres', 'SHOW listen_addresses').stdout.strip() == '',
                   'CT2b lsof -a -p <my postmaster> -i: 0 inet lines': len(lsof_me) == 0,
                   'CT2b control: the same lsof on another postgres pid that holds a socket finds > 0 (or no such pid running)': (len(lsof_ctl) > 0) if nat else 'no other postgres running'}
print('  engine %s | socket %s | postmaster pid %s | controls %s' % (RES['engine'][:60], SOCK, pid, RES['controls']))
def boot(side, db):
    dev = DEVS[side]
    url = 'postgresql://postgres@localhost/%s?host=%s&port=%s' % (db, SOCK, PORT)
    out = []
    for b in (1, 2):
        r_ = run(TSX + [RUNNER, os.path.join(dev, 'services/api-gateway/src/startup-migrations.ts'), os.path.join(dev, 'migrations'), url], env=dict(os.environ, NODE_PATH=os.path.join(dev, 'node_modules')), cwd=dev)
        open(os.path.join(W, 'runs', '%s.boot%d.out' % (db, b)), 'w').write(r_.stdout + '\n--- stderr\n' + r_.stderr)
        last = (r_.stdout.strip().splitlines() or ['{}'])[-1]
        try: j = json.loads(last)
        except Exception: j = {'unparsed': last[:300], 'stderr': r_.stderr[-400:]}
        out.append(j)
    return out
def drill(side, db, role):
    dev = DEVS[side]
    env = dict(os.environ, NODE_PATH=os.path.join(dev, 'node_modules'), DEV=dev, SOCK=SOCK, DB=db, ROLE=role, SUPER='postgres', SIDE=side,
               SECURITY_DISABLE_BOOT='1', NODE_ENV='test', PGPORT=PORT)
    r_ = run(TSX + [DRILL], env=env, cwd=dev, timeout=600)
    open(os.path.join(W, 'runs', '%s.%s.drill.out' % (side, role)), 'w').write(r_.stdout + '\n--- stderr\n' + r_.stderr)
    last = (r_.stdout.strip().splitlines() or ['{}'])[-1]
    try: return json.loads(last)
    except Exception: return {'unparsed': last[:300], 'rc': r_.returncode, 'stderr': r_.stderr[-600:]}
try:
    for side in list(SIDES) + list(ARMS):
        db = 'g40_' + side.lower()
        PSQL('postgres', 'CREATE DATABASE %s' % db)
        RES['boots'][side] = boot(side, db)
        b2 = RES['boots'][side][-1]
        print('  %s: boot 2 -> %s' % (side, json.dumps({k: b2.get(k) for k in ('db', 'failed_files', 'threw')})[:400]))
        roles = ['secuura_app', 'postgres'] if side in SIDES else ['secuura_app']
        for role in roles:
            RES['runs']['%s as %s' % (side, role)] = d_ = drill(side, db, role)
            print('  %s as %s: %s' % (side, role, 'FATAL ' + d_['fatal'][:300] if 'fatal' in d_ else ('UNPARSED ' + json.dumps(d_)[:500] if 'unparsed' in d_ else '%d scenario rows' % len(d_.get('scen', {})))))
finally:
    r = run([PGB + 'pg_ctl-18', '-D', DATA, '-m', 'fast', 'stop']); print('  cluster stopped rc %d (data dir kept at %s)' % (r.returncode, DATA))
def sc(key, name):
    return (RES['runs'].get(key, {}).get('scen') or {}).get(name)
def find(key, prefix):
    s = RES['runs'].get(key, {}).get('scen') or {}
    for k, v in s.items():
        if k.startswith(prefix): return v
    return None
SUM = {}
for side in list(SIDES) + list(ARMS):
    k = '%s as secuura_app' % side
    R2 = find(k, 'R2'); A1 = find(k, 'A1'); D1 = find(k, 'D1'); F1 = find(k, 'F1'); U1 = find(k, 'U1'); M1 = find(k, 'M1')
    SUM[side] = {
        'R2 stale instance after the stored revoke: answer / row after': [R2['answer'].get('valid'), R2['answer'].get('reason'), R2['row_after']] if isinstance(R2, dict) else R2,
        'A1 cached-revoked stored-active: answer / store': [A1['answer'].get('valid'), A1['answer'].get('reason'), A1['row']] if isinstance(A1, dict) else A1,
        'D1 vanished: answer / evicted / row re-created?': [D1['answer'].get('valid'), D1['answer'].get('reason'), D1['evicted'], D1['row_after']] if isinstance(D1, dict) else D1,
        'F1 stored read fails (EXECUTE revoked): status / message': [F1['answer'].get('status'), F1['answer'].get('message') or F1['answer'].get('valid')] if isinstance(F1, dict) else F1,
        'U1 usage write fails: status / valid / error lines / key lines / hash lines': [U1['answer'].get('status'), U1['answer'].get('valid'), U1['error_lines'], U1['lines_with_key'], U1['lines_with_hash']] if isinstance(U1, dict) else U1,
        'M1 memory-only: avail / active / revoked': [M1['avail'], [M1['active'].get('status'), M1['active'].get('valid')], [M1['revoked'].get('status'), M1['revoked'].get('valid'), M1['revoked'].get('reason')]] if isinstance(M1, dict) else M1,
    }
SUM['premise as secuura_app (head)'] = {k[:60]: v for k, v in (RES['runs'].get('head as secuura_app', {}).get('scen') or {}).items() if k.startswith('P ')}
SUM['premise as postgres (head)'] = {k[:60]: v for k, v in (RES['runs'].get('head as postgres', {}).get('scen') or {}).items() if k.startswith('P direct') or k.startswith('P CONTROL direct')}
SUM['R2 as postgres (the builder\'s drill), base / head'] = [find('base as postgres', 'R2'), find('head as postgres', 'R2')]
RES['_summary'] = SUM
json.dump(RES, open(os.path.join(G, 'pgprobe_gate40.json'), 'w'), indent=1, default=str)
print(json.dumps(SUM, indent=1, default=str))
print('wrote %s' % os.path.join(G, 'pgprobe_gate40.json'))
