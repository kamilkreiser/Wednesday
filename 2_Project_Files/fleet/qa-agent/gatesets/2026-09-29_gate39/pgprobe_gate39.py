#!/usr/bin/env python3
"""pgprobe_gate39.py <scratchpad> — the drafter's REAL-POSTGRES measurement for #1332 ROUND 2 (KS-1054), the gate39 kit (kit.json and pins_gate39.json
beside this script; run AFTER predict_gate39.py). Shape copied from gate38's pgprobe (gate37's gate method), extended to the THREE fresh-database paths
Wednesday's commission names — the paths the seat did NOT drive ("⚠ The gateway runner was not driven"; "Two of the three sides you named were NOT
driven"). A drafter's run is a PREDICTION for the gate, never the gate's evidence.

METHOD: a throwaway Homebrew PostgreSQL 18 cluster, `-c listen_addresses=''` (NO TCP listener) and `-k <a socket dir shorter than 103 bytes>`, stopped
with `pg_ctl -m fast stop`, the data dir KEPT, never deleted; never the native :5432, never a container. The data dir lives in the scratchpad
(<scratchpad>/g39_pg/data_*, the Data volume — /Volumes/DevMASTER is full); ONLY the socket dir is a short `mkdtemp('/tmp/q39.')`. Every product byte is
EXTRACTED from the scratch clone (g39_sp/clone.git) by `git archive` (a read verb) at: base (#1332's merge-base 0d156d12cc0f), r1 (round 1's head
f5381338 — round 1's defect, the control that the drill discriminates), head (#1332's round-2 head), dev (the pinned develop — its docker/init seeded path
is the fourth side of the schema equality) and END (END_TREE, when its migrations / init / runner files differ from head's; asserted otherwise). The REAL
`runStartupMigrations()` runs by node with the checkout's tsx CJS hook (`pg` from the checkout's node_modules via NODE_PATH — READ-only use); the REAL,
UNMODIFIED `scripts/run-migrations.sh` runs under `sh` with LC_ALL=C (the migrations image is node:24-alpine: musl collates by bytes) and ONE disclosed
shim: `pg_isready` on PATH probes the real socket (the script TCP-probes a host it seds out of DATABASE_URL, which a unix-socket URL cannot express —
the seat's drill used the same shim); `psql` on PATH is psql-18. The script writes its own `/tmp/migrate-err.log` (its code, not the drafter's).

PATHS, each on a FRESH database:
  (i)   BARE -> the GATEWAY runner, boot 1 and boot 2                     [head; r1 and base as the two-sided control; head-minus-038a as a GATE arm]
  (ii)  BARE -> scripts/run-migrations.sh (pass 1) -> the GATEWAY runner, boot 1 and boot 2   [head; base for the pre-existing failures]
  (iii) docker/init-seeded -> the GATEWAY runner, boot 1 and boot 2       [head]
  (dev) docker/init-seeded -> the GATEWAY runner, boot 1 and boot 2 at the pinned DEVELOP (no 038a): the equality's fourth side
  (rm)  BARE -> scripts/run-migrations.sh pass 1 and pass 2 alone          [head: the seat's own container path, re-measured]
  (ct)  BARE -> gateway boot 1, then boot 2 with a CORE-stage THROW        [head vs r1: N-1332-2 / N-1332-3 two-sided]
After each boot: `_secuura_migrations` (039, 006, 008, 047, the whole list), to_regprocedure('auth_find_oauth_app_by_client_id(text)') and its owner, the
oauth_apps_auth_lookup policy, tenant_isolation (count, and per table of the four: RLS, FORCE, the policy and its qual), a call of the function, the
run's return value and the recorded summary (`failed`, `error`). After the LAST boot of (i), (ii), (iii), (dev): `pg_dump --schema-only -t <table>` of each
of the four tables, filtered of pg_dump 18's per-dump `\\restrict` / `\\unrestrict` nonce lines — compared byte-for-byte across the four; and a WHOLE
`pg_dump --schema-only` before and after each second boot (a second boot must change nothing).
CONTROLS: CT1 a wrong socket dir does not connect; CT2 `SHOW listen_addresses` == '' and CT2b lsof finds 0 inet sockets on the postmaster; CT3 the
drill DISCRIMINATES — r1's bare database records 039 with the function ABSENT (round 1's defect reproduced) and base's fails 039 at boot 1; CT4 the
dump comparator: a one-character mutation of a dump DIFFERS, and two different tables' dumps differ; CT5 the nonce filter removed exactly the
`\\restrict` lines (a dump that carried none would make the filter vacuous).
Writes pgprobe_gate39.json beside this script; prints a summary; raw per-boot output and every dump go to <scratchpad>/g39_pg/. Usage: pgprobe_gate39.py <scratchpad>"""
import json, os, re, subprocess, sys, tempfile, datetime, glob, tarfile, io, shutil, hashlib
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_%s.json' % K['kit']), encoding='utf-8'))
SP = sys.argv[1]
if not re.match(r'^/private/tmp/claude-501/.*/scratchpad', SP): print('usage: pgprobe_gate39.py <scratchpad on the Data volume>'); sys.exit(9)
CL = os.path.join(SP, 'g39_sp', 'clone.git')
W = os.path.join(SP, 'g39_pg'); os.makedirs(os.path.join(W, 'boots'), exist_ok=True); os.makedirs(os.path.join(W, 'dumps'), exist_ok=True)
DEVCO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev'
TSX = ['node', '--require', DEVCO + '/node_modules/tsx/dist/cjs/index.cjs']   # the tsx CJS hook, NOT the tsx CLI (its IPC pipe in a long TMPDIR fails: listen EINVAL, gate38 MEASURED)
PGB = '/opt/homebrew/bin/'
RUNNER = os.path.join(G, 'pgprobe_gate39.runner.ts')
PORT = '55439'   # names the socket file only: listen_addresses='' opens NO TCP port
FOUR = ('oauth_apps', 'svc_webhooks', 'certifications', 'charge_events')
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def run(cmd, **kw): return subprocess.run(cmd, capture_output=True, text=True, **kw)
pr = P['prs']['1332']
SIDES = {'base': pr['merge_base'], 'r1': pr['commits'][0], 'head': pr['head'], 'dev': P['develop'], 'END': P['end_tree']}
PATHS = ['Blockchain/Dev/migrations', 'Blockchain/Dev/docker/init', 'Blockchain/Dev/scripts/run-migrations.sh', 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts']
print('pgprobe_gate39 %s | #1332 base %s r1 %s head %s | develop %s | END %s | work %s' % (now(), SIDES['base'][:12], SIDES['r1'][:12], SIDES['head'][:12], SIDES['dev'][:12], SIDES['END'][:12], W))
# 0. is END's product for these paths the head's? (then END's runs ARE the head's; asserted, never assumed)
def lstree(rev, p):
    r_ = run(['git', '--git-dir', CL, 'rev-parse', '--verify', '-q', '%s:%s' % (rev, p)]); return r_.stdout.strip() if r_.returncode == 0 else ''
same_end = {p: lstree(SIDES['END'], p) == lstree(SIDES['head'], p) for p in PATHS + ['Blockchain/Dev/services/api-gateway/src/services/startupMigrationStatus.ts']}
print('  END_TREE == head for every drilled path: %s %s' % (all(same_end.values()), same_end if not all(same_end.values()) else ''))
if all(same_end.values()): del SIDES['END']
# 1. extract each side (git archive: a READ verb on the scratch clone; tar writes only under the scratchpad)
for side, rev in SIDES.items():
    d = os.path.join(W, side)
    if os.path.isdir(d): print('  %s already extracted at %s (a re-run reuses it: the rev is pinned)' % (side, d)); continue
    paths = list(PATHS)
    if lstree(rev, 'Blockchain/Dev/services/api-gateway/src/services/startupMigrationStatus.ts'): paths.append('Blockchain/Dev/services/api-gateway/src/services/startupMigrationStatus.ts')
    a = subprocess.run(['git', '--git-dir', CL, 'archive', '--format=tar', rev] + paths, capture_output=True)
    if a.returncode: print('REFUSING: git archive %s rc %d %s' % (side, a.returncode, a.stderr[-300:])); sys.exit(1)
    tarfile.open(fileobj=io.BytesIO(a.stdout)).extractall(d)
    print('  extracted %s @ %s -> %s (%d bytes of tar)' % (side, rev[:12], d, len(a.stdout)))
# the GATE arm on a real database: head's migrations WITHOUT 038a (a COPY; the extract is never edited)
arm = os.path.join(W, 'head_no038a')
if not os.path.isdir(arm):
    shutil.copytree(os.path.join(W, 'head'), arm)
    os.rename(os.path.join(arm, 'Blockchain/Dev/migrations/038a_ks1054_core_tables_before_039.sql'), os.path.join(W, 'head_no038a.QUARANTINED-038a.sql'))
# the glob order run-migrations.sh sees, under two locales on THIS host (the image is musl/alpine: byte order)
glob_order = {}
for loc in ('C', 'en_US.UTF-8'):
    r = run(['/bin/sh', '-c', 'for f in migrations/*.sql; do echo "$f"; done'], cwd=os.path.join(W, 'head', 'Blockchain/Dev'), env=dict(os.environ, LC_ALL=loc))
    L = [os.path.basename(x) for x in r.stdout.split()]
    i = L.index('038a_ks1054_core_tables_before_039.sql'); glob_order[loc] = L[i - 1:i + 2]
print('  /bin/sh glob order around 038a on this host: %s' % glob_order)
# 2. the throwaway cluster: data in the scratchpad, the socket in a SHORT /tmp dir, NO TCP listener
data = os.path.join(W, 'data_' + datetime.datetime.now().strftime('%H%M%S'))
sock = tempfile.mkdtemp(prefix='q39.', dir='/tmp')
assert len(sock + '/.s.PGSQL.' + PORT) < 103, 'socket path too long'
shim = os.path.join(W, 'shim'); os.makedirs(shim, exist_ok=True)
open(os.path.join(shim, 'pg_isready'), 'w').write('#!/bin/sh\n# gate39 DRILL SHIM, disclosed: run-migrations.sh TCP-probes a host it seds out of DATABASE_URL; this probes the real unix socket instead.\n'
                                                  '# It replaces ONLY the readiness probe; every migration is applied by the REAL, UNMODIFIED script through the REAL psql-18.\n'
                                                  'exec %spg_isready-18 -h %s -p %s -U q39 -q\n' % (PGB, sock, PORT))
os.chmod(os.path.join(shim, 'pg_isready'), 0o755)
for b in ('psql', 'pg_dump'):
    if not os.path.lexists(os.path.join(shim, b)): os.symlink(PGB + b + '-18', os.path.join(shim, b))
r = run([PGB + 'initdb-18', '-D', data, '-U', 'q39', '-A', 'trust', '--no-locale', '-E', 'UTF8'])
print('  initdb-18 rc %d -> %s' % (r.returncode, data))
if r.returncode: print(r.stderr[-500:]); sys.exit(1)
r = run([PGB + 'pg_ctl-18', '-D', data, '-l', data + '.log', '-w', '-o', "-c listen_addresses='' -k %s -p %s" % (sock, PORT), 'start'])
print('  pg_ctl-18 start rc %d (socket dir %s, %d bytes incl. the socket file)' % (r.returncode, sock, len(sock + '/.s.PGSQL.' + PORT)))
if r.returncode: print(r.stdout[-500:], r.stderr[-500:]); sys.exit(1)
res = {'engine': None, 'socket_dir': sock, 'data_dir': data, 'port_name_only': PORT, 'sides': {k: v for k, v in SIDES.items()}, 'end_equals_head': same_end,
       'glob_order_this_host': glob_order, 'runs': {}, 'dumps': {}, 'controls': {}}
def psql(db, sql, stop=True):
    return run([PGB + 'psql-18', '-h', sock, '-p', PORT, '-U', 'q39', '-d', db, '-v', 'ON_ERROR_STOP=%d' % (1 if stop else 0), '-tAc', sql])
def url(db): return 'postgresql://q39@localhost:%s/%s?host=%s' % (PORT, db, sock)
def boot(db, side, tag, core_throw=False):
    smp = os.path.join(W, side, 'Blockchain/Dev/services/api-gateway/src/startup-migrations.ts')
    mig = os.path.join(W, side, 'Blockchain/Dev/migrations')
    env = dict(os.environ, NODE_PATH=DEVCO + '/node_modules', TMPDIR=os.path.join(W, 'tmp'))
    if core_throw: env['QA_CORE_THROW'] = '1'
    os.makedirs(env['TMPDIR'], exist_ok=True)
    r = run(TSX + [RUNNER, smp, mig, url(db)], env=env, timeout=600)
    open(os.path.join(W, 'boots', '%s.stdout' % tag), 'w').write(r.stdout); open(os.path.join(W, 'boots', '%s.stderr' % tag), 'w').write(r.stderr)
    js = [l for l in r.stdout.splitlines() if l.startswith('{')]
    out = json.loads(js[-1]) if js else {'fatal': 'no JSON line (rc %d) %s' % (r.returncode, r.stderr[-300:])}
    out['rc'] = r.returncode; d = out.get('db', {})
    tr = d.get('tracked') if isinstance(d.get('tracked'), list) else []
    out['tracked_of_interest'] = {f: f in tr for f in ('006_f18_webhook_secret_encryption.sql', '008_drop_webhook_secret_legacy.sql', '038_rls_consolidate_policy.sql', '038a_ks1054_core_tables_before_039.sql', '039_rls_fail_closed.sql', '047_oauth_app_type_vocabulary.sql')}
    print('  %-26s rc %s | 039 %s | fn %s | policy %s | tenant_isolation %s | four %s | tracked %s | failed files %s | ret %s%s' % (
        tag, r.returncode, d.get('tracked_039'), d.get('fn_auth_find_oauth_app_by_client_id'), d.get('oauth_apps_auth_lookup_policy'), d.get('tenant_isolation_policies'),
        [(x['t'], x['rls'], x['force'], x['ti']) for x in d.get('four_tables', [])] if isinstance(d.get('four_tables'), list) else d.get('four_tables'), d.get('tracked_total'),
        out.get('failed_files'), json.dumps(out.get('ret'))[:160], (' | planted CORE throws %s' % out.get('planted')) if core_throw else ''))
    return out
def runmig(db, side, tag):
    env = dict(os.environ, PATH=shim + ':' + os.environ['PATH'], DATABASE_URL=url(db), LC_ALL='C')
    env.pop('PLATFORM_DATABASE_URL', None)
    r = run(['/bin/sh', 'scripts/run-migrations.sh'], cwd=os.path.join(W, side, 'Blockchain/Dev'), env=env, timeout=600)
    open(os.path.join(W, 'boots', '%s.runmig.out' % tag), 'w').write(r.stdout + '\n--- stderr\n' + r.stderr)
    summ = [l for l in r.stdout.splitlines() if l.startswith('Summary:')]
    fails = re.findall(r'^\[main\] FAILED (\S+):', r.stdout, re.M)
    t = psql(db, "SELECT count(*) FROM _secuura_migrations WHERE filename = '039_rls_fail_closed.sql'").stdout.strip()
    fn = psql(db, "SELECT coalesce(to_regprocedure('auth_find_oauth_app_by_client_id(text)')::text, 'ABSENT')").stdout.strip()
    ti = psql(db, "SELECT count(*) FROM pg_policies WHERE policyname = 'tenant_isolation'").stdout.strip()
    tabs = psql(db, "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('oauth_apps','svc_webhooks','certifications','charge_events')").stdout.strip()
    out = {'rc': r.returncode, 'summary': summ[-1] if summ else None, 'failed_files': fails, 'tracked_039': t, 'fn': fn, 'tenant_isolation': ti, 'four_tables': tabs}
    print('  %-26s run-migrations.sh rc %s | %s | FAILED %s | 039 %s | fn %s | tenant_isolation %s | four %s' % (tag, r.returncode, out['summary'], fails, t, fn, ti, tabs))
    return out
def init_seed(db, side, tag):
    ie = []
    for f in sorted(glob.glob(os.path.join(W, side, 'Blockchain/Dev/docker/init/*.sql'))):
        rr = run([PGB + 'psql-18', '-h', sock, '-p', PORT, '-U', 'q39', '-d', db, '-v', 'ON_ERROR_STOP=0', '-q', '-f', f])
        errs = [l for l in rr.stderr.splitlines() if 'ERROR' in l]
        if errs: ie.append((os.path.basename(f), len(errs), errs[0][:140]))
    print('  %-26s docker/init seeded; files with ERROR lines: %s' % (tag, [(a, b) for a, b, c in ie]))
    return ie
RESTRICT = re.compile(r'^\\(un)?restrict ')
def dump(db, tag, table=None):
    cmd = [PGB + 'pg_dump-18', '-h', sock, '-p', PORT, '-U', 'q39', '--schema-only', '-d', db] + (['-t', table] if table else [])
    r = run(cmd)
    raw = r.stdout; kept = '\n'.join(l for l in raw.split('\n') if not RESTRICT.match(l))
    nres = sum(1 for l in raw.split('\n') if RESTRICT.match(l))
    open(os.path.join(W, 'dumps', '%s%s.raw.sql' % (tag, ('.' + table) if table else '')), 'w').write(raw)
    open(os.path.join(W, 'dumps', '%s%s.clean.sql' % (tag, ('.' + table) if table else '')), 'w').write(kept)
    return {'rc': r.returncode, 'sha256': hashlib.sha256(kept.encode()).hexdigest(), 'bytes': len(kept), 'restrict_lines_removed': nres, 'text': kept}
def schema_delta(a, b):
    import difflib
    ch = [l for l in difflib.unified_diff(a['text'].split('\n'), b['text'].split('\n'), n=0, lineterm='') if l[:1] in '+-' and not l.startswith(('+++', '---'))]
    return [sorted(set(re.findall(r'public\.(\w+)', '\n'.join(ch)))), len(ch)]
def newdb(name):
    psql('postgres', 'CREATE DATABASE %s' % name); return name
try:
    res['engine'] = psql('postgres', 'SELECT version()').stdout.strip()
    res['controls']['CT1 a wrong socket dir does not connect'] = run([PGB + 'psql-18', '-h', sock + '/nope', '-p', PORT, '-U', 'q39', '-d', 'postgres', '-tAc', 'SELECT 1']).returncode != 0
    res['controls']['CT2 no TCP listener (listen_addresses is empty)'] = psql('postgres', 'SHOW listen_addresses').stdout.strip() == ''
    lo = run(['/usr/sbin/lsof', '-a', '-p', open(os.path.join(data, 'postmaster.pid')).read().split()[0], '-i'])
    res['controls']['CT2b lsof: the postmaster holds 0 inet sockets'] = lo.stdout.strip() == ''
    print('  engine %s' % res['engine'])
    R = res['runs']
    # (ct-control) base and r1: the drill must tell the sides apart
    db = newdb('bare_base'); R['i base boot 1'] = boot(db, 'base', 'i_base_boot1'); R['i base boot 2'] = boot(db, 'base', 'i_base_boot2')
    BASE_I = {t: dump(db, 'p1_base', t) for t in FOUR}   # the merge-base's bare end state (CORE-created tables): the PRE-EXISTING reference for (i)
    db = newdb('bare_r1'); R['i r1 boot 1'] = boot(db, 'r1', 'i_r1_boot1'); R['i r1 boot 2 CORE-THROW'] = boot(db, 'r1', 'i_r1_boot2_corethrow', core_throw=True)
    # (i) BARE -> gateway x2 (head)
    db = newdb('p1_head'); R['i head boot 1'] = boot(db, 'head', 'i_head_boot1')
    d1 = dump(db, 'p1_head_after_boot1'); R['i head boot 2'] = boot(db, 'head', 'i_head_boot2'); d2 = dump(db, 'p1_head_after_boot2')
    R['i head second boot changes nothing (whole pg_dump --schema-only)'] = d1['sha256'] == d2['sha256']
    R['i head second boot: tables whose schema changed, and +/- line count'] = schema_delta(d1, d2)
    for t in FOUR: res['dumps'].setdefault(t, {})['i'] = dump(db, 'p1_head', t)
    # (ct) head: boot 1 normal on a fresh bare DB, boot 2 with the CORE throw planted
    db = newdb('ct_head'); R['ct head boot 1'] = boot(db, 'head', 'ct_head_boot1'); R['ct head boot 2 CORE-THROW'] = boot(db, 'head', 'ct_head_boot2_corethrow', core_throw=True)
    # (arm) head WITHOUT 038a on a bare DB: round 1's permanent skip must come back (the GATE arm on a real database)
    db = newdb('arm_no038a'); R['arm head-minus-038a boot 1'] = boot(db, 'head_no038a', 'arm_no038a_boot1'); R['arm head-minus-038a boot 2'] = boot(db, 'head_no038a', 'arm_no038a_boot2')
    # (ii) BARE -> run-migrations.sh -> gateway x2 (head), and base's run-migrations for the pre-existing failures
    db = newdb('p2_head'); R['ii head run-migrations pass 1'] = runmig(db, 'head', 'ii_head_rm1')
    R['ii head boot 1'] = boot(db, 'head', 'ii_head_boot1'); d1 = dump(db, 'p2_head_after_boot1')
    R['ii head boot 2'] = boot(db, 'head', 'ii_head_boot2'); d2 = dump(db, 'p2_head_after_boot2')
    R['ii head second boot changes nothing (whole pg_dump --schema-only)'] = d1['sha256'] == d2['sha256']
    R['ii head second boot: tables whose schema changed, and +/- line count'] = schema_delta(d1, d2)
    for t in FOUR: res['dumps'][t]['ii'] = dump(db, 'p2_head', t)
    db = newdb('rm_base'); R['rm base pass 1'] = runmig(db, 'base', 'rm_base_1'); R['rm base pass 2'] = runmig(db, 'base', 'rm_base_2')
    db = newdb('rm_head'); R['rm head pass 1'] = runmig(db, 'head', 'rm_head_1'); R['rm head pass 2'] = runmig(db, 'head', 'rm_head_2')
    R['rm head pass 3'] = runmig(db, 'head', 'rm_head_3')
    # (iii) docker/init -> gateway x2 (head)
    db = newdb('p3_head'); R['iii head docker/init errors'] = init_seed(db, 'head', 'iii_head_init')
    R['iii head boot 1'] = boot(db, 'head', 'iii_head_boot1'); d1 = dump(db, 'p3_head_after_boot1')
    R['iii head boot 2'] = boot(db, 'head', 'iii_head_boot2'); d2 = dump(db, 'p3_head_after_boot2')
    R['iii head second boot changes nothing (whole pg_dump --schema-only)'] = d1['sha256'] == d2['sha256']
    R['iii head second boot: tables whose schema changed, and +/- line count'] = schema_delta(d1, d2)
    for t in FOUR: res['dumps'][t]['iii'] = dump(db, 'p3_head', t)
    # (dev) develop's seeded path: docker/init -> develop's gateway x2
    db = newdb('pd_dev'); R['dev docker/init errors'] = init_seed(db, 'dev', 'dev_init')
    R['dev boot 1'] = boot(db, 'dev', 'dev_boot1'); R['dev boot 2'] = boot(db, 'dev', 'dev_boot2')
    for t in FOUR: res['dumps'][t]['dev'] = dump(db, 'pd_dev', t)
    # (app) the four tables AS AN APP ROLE (NOSUPERUSER, NOBYPASSRLS — the superuser q39 bypasses RLS, so every read above is blind to it): in ONE
    # transaction, ROLLED BACK, with the tenant GUC set, INSERT one row and count it back; run AFTER every dump (the GRANTs change the database)
    psql('postgres', "DO $$ BEGIN CREATE ROLE q39app NOSUPERUSER NOBYPASSRLS NOLOGIN; EXCEPTION WHEN duplicate_object THEN NULL; END $$", stop=False)
    TEN = 'a0000000-0000-4000-8000-000000000001'
    INS = {'certifications': "INSERT INTO certifications (certification_type, tenant_id) VALUES ('qa-g39', '%s')" % TEN,
           'oauth_apps': "INSERT INTO oauth_apps (name, client_id, tenant_id) VALUES ('qa-g39', 'qa-g39-client', '%s')" % TEN,
           'charge_events': "INSERT INTO charge_events (id, event_type, tenant_id) VALUES ('qa-g39', 'qa', '%s')" % TEN,
           'svc_webhooks': "INSERT INTO svc_webhooks (url, secret_v2, tenant_id) VALUES ('https://qa.invalid', 'x', '%s')" % TEN}
    APP = {}
    for dbn in ('bare_base', 'p1_head', 'p2_head', 'p3_head', 'pd_dev'):
        psql(dbn, 'GRANT USAGE ON SCHEMA public TO q39app; GRANT SELECT, INSERT ON certifications, oauth_apps, charge_events, svc_webhooks TO q39app', stop=False)
        APP[dbn] = {}
        for t, ins in INS.items():
            sql = "BEGIN; SET LOCAL ROLE q39app; SET LOCAL app.current_tenant_id = '%s'; %s; SELECT 'ROWS=' || count(*) FROM %s; ROLLBACK;" % (TEN, ins, t)
            rr = run([PGB + 'psql-18', '-h', sock, '-p', PORT, '-U', 'q39', '-d', dbn, '-v', 'ON_ERROR_STOP=0', '-tA', '-c', sql])
            m = re.search(r'ROWS=(\d+)', rr.stdout); er = [l for l in rr.stderr.splitlines() if 'ERROR' in l]
            APP[dbn][t] = ('rows %s' % m.group(1)) if m else ('ERROR ' + (er[0][:120] if er else rr.stderr[-120:]))
        print('  %-26s AS q39app (tenant GUC set, rolled back): %s' % ('app_' + dbn, APP[dbn]))
    R['app role insert+count per table'] = APP
    # a CONTROL for the app-role probe: the same insert WITHOUT the tenant GUC must be refused where a fail-closed policy exists
    rr = run([PGB + 'psql-18', '-h', sock, '-p', PORT, '-U', 'q39', '-d', 'p1_head', '-v', 'ON_ERROR_STOP=0', '-tA', '-c', "BEGIN; SET LOCAL ROLE q39app; %s; ROLLBACK;" % INS['oauth_apps']])
    res['controls']['CT6 app-role probe: oauth_apps INSERT WITHOUT the tenant GUC is refused by RLS at head'] = 'row-level security' in rr.stderr
    if 'END' in SIDES:
        db = newdb('p1_end'); R['i END boot 1'] = boot(db, 'END', 'i_end_boot1'); R['i END boot 2'] = boot(db, 'END', 'i_end_boot2')
finally:
    r = run([PGB + 'pg_ctl-18', '-D', data, '-m', 'fast', 'stop'])
    print('  pg_ctl-18 -m fast stop rc %d (the data dir is KEPT at %s; the socket dir %s is left empty, never deleted)' % (r.returncode, data, sock))
    res['stopped_rc'] = r.returncode
R = res['runs']
def dbv(k, f): return R[k].get('db', {}).get(f) if isinstance(R.get(k), dict) else None
def fnok(k): v = str(dbv(k, 'fn_auth_find_oauth_app_by_client_id')); return v not in ('None', '') and not v.startswith('ERROR')
def four_closed(k):
    """oauth_apps, svc_webhooks, charge_events each RLS + FORCE + ONE tenant_isolation policy; certifications as develop's seeded path leaves it
    (RLS + FORCE, NO tenant_isolation: 039 skips it because 038a / CORE create it WITHOUT tenant_id, which a later CORE ALTER adds — PRE-EXISTING,
    gate38 N-DEV-1; its state is compared with develop's, never assumed)"""
    ft = dbv(k, 'four_tables'); fdev = dbv('dev boot 2', 'four_tables')
    if not (isinstance(ft, list) and len(ft) == 4 and isinstance(fdev, list)): return False
    c = {x['t']: x for x in ft}; cdev = {x['t']: x for x in fdev}
    return all(c[t]['rls'] and c[t]['force'] and c[t]['ti'] == 1 for t in ('oauth_apps', 'svc_webhooks', 'charge_events')) and (c['certifications']['rls'], c['certifications']['force'], c['certifications']['ti']) == (cdev['certifications']['rls'], cdev['certifications']['force'], cdev['certifications']['ti'])
# the dump equality across (i), (ii), (iii), (dev) — per table
eq = {}
for t in FOUR:
    ds = res['dumps'].get(t, {})
    eq[t] = {'sides': sorted(ds), 'sha256': {s: v['sha256'][:16] for s, v in ds.items()}, 'identical': len({v['sha256'] for v in ds.values()}) == 1 and len(ds) == 4,
             'restrict_removed': {s: v['restrict_lines_removed'] for s, v in ds.items()}}
    if not eq[t]['identical'] and len(ds) >= 2:
        base_s = 'i'; diffs = {}
        for s, v in ds.items():
            if v['sha256'] != ds[base_s]['sha256']:
                import difflib
                diffs[s] = [l for l in difflib.unified_diff(ds[base_s]['text'].split('\n'), v['text'].split('\n'), 'i', s, n=0, lineterm='') if l[:1] in '+-' and not l.startswith(('+++', '---'))][:12]
        eq[t]['diff_vs_i'] = diffs
res['dump_equality'] = eq
res['dump_base_bare'] = {t: {k: v for k, v in BASE_I[t].items() if k != 'text'} for t in FOUR}
_d = res['dumps'].get('oauth_apps', {}).get('i', {}).get('text', '')
res['controls']['CT4 dump comparator: a one-character mutation DIFFERS, two tables DIFFER'] = bool(_d) and hashlib.sha256(_d.replace('character varying(64)', 'character varying(63)', 1).encode()).hexdigest() != hashlib.sha256(_d.encode()).hexdigest() and res['dumps']['oauth_apps']['i']['sha256'] != res['dumps']['svc_webhooks']['i']['sha256']
res['controls']['CT5 the nonce filter removed restrict lines from every table dump'] = all(v['restrict_lines_removed'] >= 1 for t in FOUR for v in res['dumps'].get(t, {}).values())
res['controls']['CT3a base bare boot 1 FAILS 039 (the ticket\'s defect)'] = dbv('i base boot 1', 'tracked_039') == 0
res['controls']['CT3b r1 bare boot 1 RECORDS 039 with the function ABSENT (round 1\'s defect, gate38 N-1332-1)'] = dbv('i r1 boot 1', 'tracked_039') == 1 and not fnok('i r1 boot 1')
for t in FOUR:
    for s in res['dumps'].get(t, {}): res['dumps'][t][s].pop('text', None)
summ = {
 '(i) head bare -> gateway boot 1: 039 recorded, function present, policy present, the four tables RLS+FORCE+tenant_isolation': dbv('i head boot 1', 'tracked_039') == 1 and fnok('i head boot 1') and dbv('i head boot 1', 'oauth_apps_auth_lookup_policy') == 1 and four_closed('i head boot 1'),
 '(i) head: a second boot changes nothing (whole schema) — else [the tables it changes, +/- lines]': R.get('i head second boot changes nothing (whole pg_dump --schema-only)') or R.get('i head second boot: tables whose schema changed, and +/- line count'),
 '(ii) head bare -> run-migrations.sh -> gateway boot 1: 039 recorded, function, policy, four closed': dbv('ii head boot 1', 'tracked_039') == 1 and fnok('ii head boot 1') and dbv('ii head boot 1', 'oauth_apps_auth_lookup_policy') == 1 and four_closed('ii head boot 1'),
 '(ii) head: a second boot changes nothing (whole schema) — else [the tables it changes, +/- lines]': R.get('ii head second boot changes nothing (whole pg_dump --schema-only)') or R.get('ii head second boot: tables whose schema changed, and +/- line count'),
 '(iii) head docker/init -> gateway boot 1: 039 recorded, function, policy, four closed': dbv('iii head boot 1', 'tracked_039') == 1 and fnok('iii head boot 1') and dbv('iii head boot 1', 'oauth_apps_auth_lookup_policy') == 1 and four_closed('iii head boot 1'),
 '(iii) head: a second boot changes nothing (whole schema) — else [the tables it changes, +/- lines]': R.get('iii head second boot changes nothing (whole pg_dump --schema-only)') or R.get('iii head second boot: tables whose schema changed, and +/- line count'),
 'pg_dump -t of the four tables byte-identical across (i), (ii), (iii) and develop\'s seeded path — per table': {t: v['identical'] for t, v in eq.items()},
 'pg_dump -t: the MERGE-BASE\'s bare end state (boot 2, CORE-created tables) == head (i) per table — so a bare-vs-seeded difference is PRE-EXISTING where True': {t: BASE_I[t]['sha256'] == res['dumps'][t]['i']['sha256'] for t in FOUR},
 'pg_dump -t: the two BARE paths (i) == (ii) per table': {t: len({eq[t]['sha256'].get('i'), eq[t]['sha256'].get('ii')}) == 1 for t in FOUR},
 'pg_dump -t: the two SEEDED paths (iii) == (dev) per table': {t: len({eq[t]['sha256'].get('iii'), eq[t]['sha256'].get('dev')}) == 1 for t in FOUR},
 'the four tables at (dev) boot 2 (RLS, FORCE, tenant_isolation) — develop\'s seeded path': [(x['t'], x['rls'], x['force'], x['ti']) for x in (dbv('dev boot 2', 'four_tables') or [])],
 'arm head-minus-038a: round 1\'s permanent skip returns (039 recorded, function ABSENT after boot 2)': dbv('arm head-minus-038a boot 2', 'tracked_039') == 1 and not fnok('arm head-minus-038a boot 2'),
 'N-1332-2 two-sided: a CORE throw on boot 2 reads failed > 0 at head, failed == 0 at round 1': isinstance(R.get('ct head boot 2 CORE-THROW', {}).get('recorded'), dict) and R['ct head boot 2 CORE-THROW']['recorded'].get('failed', 0) > 0 and isinstance(R.get('i r1 boot 2 CORE-THROW', {}).get('recorded'), dict) and R['i r1 boot 2 CORE-THROW']['recorded'].get('failed') == 0,
 'N-1332-3: the CORE-throw boot records `error` naming the throw': 'QA-PLANT' in str((R.get('ct head boot 2 CORE-THROW', {}).get('recorded') or {}).get('error', '')),
 'run-migrations.sh head pass 1: 039 recorded with the function present (the container path)': R.get('rm head pass 1', {}).get('tracked_039') == '1' and R.get('rm head pass 1', {}).get('fn', 'ABSENT') != 'ABSENT',
 'run-migrations.sh head still exits non-zero (pre-existing failures)': R.get('rm head pass 1', {}).get('rc') not in (0, None),
 'AS AN APP ROLE (tenant GUC set): certifications INSERT+count per database — base bare boot 2 vs head (i) (ii) (iii) vs develop seeded': {k: v.get('certifications') for k, v in (R.get('app role insert+count per table') or {}).items()},
 'AS AN APP ROLE: the other three tables at head (i)': (R.get('app role insert+count per table') or {}).get('p1_head'),
 'controls all behaved': all(res['controls'].values()),
}
res['_summary'] = summ
res['measured_at'] = now()
json.dump(res, open(os.path.join(G, 'pgprobe_gate39.json'), 'w'), indent=1)
print('  controls: %s' % res['controls'])
for t, v in eq.items(): print('  DUMP %-15s identical %s %s%s' % (t, v['identical'], v['sha256'], (' diff vs (i): %s' % v.get('diff_vs_i')) if not v['identical'] else ''))
for k, v in summ.items(): print('  SUMMARY %-130s %s' % (k, v))
print('  recorded (head, i): boot1 %s | boot2 %s || ct boot2 %s || r1 ct boot2 %s' % (json.dumps(R['i head boot 1'].get('recorded')), json.dumps(R['i head boot 2'].get('recorded')), json.dumps(R['ct head boot 2 CORE-THROW'].get('recorded')), json.dumps(R['i r1 boot 2 CORE-THROW'].get('recorded'))))
sys.exit(0 if res['controls'] and all(res['controls'].values()) else 1)
