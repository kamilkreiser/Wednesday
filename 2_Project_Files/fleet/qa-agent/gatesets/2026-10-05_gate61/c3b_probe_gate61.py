#!/usr/bin/env python3
"""c3b_probe_gate61.py — gate61 C3b SECURITY PROBE for #1383 (KS-1401): the GATE's OWN cells on a throwaway PostgreSQL keg (independent of
the author's suite: its own fixture, its own roles, its own readings), plus a READ-ONLY census of every charge_events writer.
THE DRAFTER NEVER RAN `probe` (no PostgreSQL was started at drafting); `census` and `--selftest` were run.
MODES
  probe  --worktree <wt at head> --out <dir> [--pgbin <keg bin>] [--sql049 <file>] [--label head]
    Starts ONE socket-only cluster (listen_addresses='', socket dir a short mkdtemp under /tmp, data under --out; never 127.0.0.1:5432),
    builds the ks949 deployed shape from the worktree's docker/init/0[1-9]*.sql + every non-platform migration except 049 (each recorded,
    failures counted), then the kintsugi-shape fixture (charge_events RLS off / 0 policies, 8 rows: 4 A, 3 B, 1 NULL; certifications
    tenant_id + forced + 0 policies, rows A, B and ONE NULL). Roles: secuura_app (NOLOGIN, as ks949) and g61_owner (NOLOGIN NOSUPERUSER
    NOBYPASSRLS). Cells, each read BEFORE and AFTER 049 (default: the worktree's; --sql049 a tampered copy for a behavioural tamper arm):
      X0  roles: secuura_app and g61_owner rolbypassrls/rolsuper == false/false (else every red is vacuous)
      X1  cross-tenant SELECT: GUC=A counts tenant B's charge_events               before 3   after 0
      X2  no GUC (fail-closed): count charge_events                               before 8   after 0
      X3  cross-tenant INSERT under GUC=A of a tenant-B row (rolled back)          before ok  after refused (row-level security)
      X3b CONTROL same-tenant INSERT under GUC=A of a tenant-A row (rolled back)   after ok (WITH CHECK admits the right tenant)
      X4  platform_admin bypass (app.tenant_scope_bypass) counts charge_events     before 8   after 8 (the gdprService carve-out)
      X5  FORCE binds the OWNER: in a 2nd DB the four tables are owned by g61_owner and 049 is applied AS g61_owner; owner, no GUC,
          counts charge_events                                                    before 8   after 0   (FORCE is behavioural, not a flag)
      X6  own certification: GUC=A counts tenant A's certifications               before 0   after 1
      X7  NULL-tenant certification row: applied as SUPERUSER -> the default tenant (MUST); applied as the non-bypass OWNER -> MEASURED and
          printed with 049's NOTICE for certifications (the drafter PREDICTS it stays NULL while the NOTICE says "0 NULL rows": D3)
      X8  fresh shape at head: 049 on the plain ks949 shape -> the four tables rls/force true, tenant_isolation present, certifications
          carries tenant_id
      X9  nothing else touched: md5 of every public function signature+body before == after; oauth_apps_auth_lookup (qual, with_check,
          roles, cmd, permissive) before == after; policies per table after == before + (1 if it had no tenant_isolation)
      X10 policy fidelity BY TEXT: each table's tenant_isolation qual AND with_check == the users policy 039 itself created, same DB
      X11 pg_dump nonce: two RAW --schema-only dumps of one unchanged DB differ only in `\\restrict`/`\\unrestrict` lines; filtered equal
      X12 lock_timeout honoured: a 2nd session holds ACCESS SHARE on charge_events; 049 (psql -v ON_ERROR_STOP=1 -f) fails with a lock
          timeout in < 15 s, NOTHING committed (charge_events still rls false), and the clean retry after release succeeds
    Writes <out>/c3b_probe_<label>.json and stops its cluster (pg_ctl stop); it deletes nothing (data and socket dirs are left).
  judge  --json <file>   re-judge a saved probe.
  census --repo <clone> [--head sha]   READ-ONLY (git grep at the head): every charge_events line under kit writer_census_roots classified
    WRITE (INSERT/UPDATE/DELETE/TRUNCATE), DDL (CREATE/ALTER TABLE), CALLER (createChargeEvent call sites), READ, OTHER; billing_charge_events
    EXCLUDED (the must-hit CONTROL: > 0). W1 the WRITE/DDL/CALLER sets == kit writer_census_expected (a NEW or GONE site FAILS: re-read
    it). Each site printed with file:line and its context (the 3 lines above; the tenant argument of a CALLER; runWithPlatformScope within
    60 lines above a WRITE). The gate RULES, per site, whether the write runs inside a tenant / platform scope that sets the GUC — a write
    outside one is refused by 049's WITH CHECK (fail-closed) on any box whose services connect as a non-bypass role.
--selftest  the probe judge on SYNTHETIC readings (the expected shape PASSES; each flipped cell FAILS its X) and the census classifier on
            planted lines (a billing_charge_events INSERT is EXCLUDED, an UPDATE is WRITE, a new caller is NEW).
Usage: c3b_probe_gate61.py probe --worktree <wt> --out <dir> [--pgbin d] [--sql049 f] [--label l] | judge --json f | census --repo <clone>
       | --selftest [--repo <clone>]        rc 0 PASS / 1 FAIL / 2 usage. Prints `CHECKED <n>`; 0 checked is a FAIL."""
import glob, hashlib, json, os, re, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate61 import K, git, now, Checks, opt_factory, guard_scratch, guard_out, has_commit, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A:
    print(__doc__); raise SystemExit(0 if A else 2)
opt = opt_factory(A); PB = K['probe']; TA, TB = PB['tenant_a'], PB['tenant_b']; OWNER = PB['owner_role']; DEFAULT = K['default_tenant']
MODE = next((m for m in ('probe', 'judge', 'census') if m in A), None)
EXP = {'X1': (3, 0), 'X2': (8, 0), 'X4': (8, 8), 'X5': (8, 0), 'X6': (0, 1)}


def judge(C, R):
    r0 = R.get('X0', {})
    C.chk('X0 non-bypass roles', r0.get('secuura_app') == 'false/false' and r0.get(OWNER) == 'false/false', 'rolbypassrls/rolsuper %s' % r0)
    for x, (b, a) in EXP.items():
        v = R.get(x, {})
        C.chk('%s %s' % (x, {'X1': 'cross-tenant SELECT', 'X2': 'no-GUC fail-closed', 'X4': 'platform_admin bypass', 'X5': 'FORCE binds the owner', 'X6': 'own certification'}[x]),
              str(v.get('before')) == str(b) and str(v.get('after')) == str(a), 'before %s (want %s) | after %s (want %s)' % (v.get('before'), b, v.get('after'), a))
    x3 = R.get('X3', {}); x3b = R.get('X3b', {})
    C.chk('X3 cross-tenant INSERT', x3.get('before') == 'ok' and str(x3.get('after', '')).startswith('refused') and 'row-level security' in str(x3.get('after', '')) and x3b.get('after') == 'ok',
          'before %r (want ok) | after %r (want refused by row-level security) | CONTROL same-tenant INSERT after %r (want ok)' % (x3.get('before'), str(x3.get('after'))[:90], x3b.get('after')))
    x7 = R.get('X7', {})
    C.chk('X7 NULL row backfill (superuser apply)', x7.get('su') == DEFAULT, 'NULL-tenant certification after a superuser apply: %r (want the default tenant %s)' % (x7.get('su'), DEFAULT))
    print('INFO X7 NULL-tenant certification after an apply AS the non-bypass OWNER: %r | 049\'s certifications NOTICE: %r — the gate RULES this (README D3)' % (x7.get('owner'), x7.get('owner_notice')))
    x8 = R.get('X8', {}); bad8 = {t: v for t, v in x8.items() if not re.fullmatch(r'%s\|\d+\|true\|true\|true\|[1-9]\d*' % t, str(v))}
    C.chk('X8 fresh shape at head', len(x8) == 4 and not bad8, 'readings (table|cols|has_tenant_id|rls|force|policies) %s | not fail-closed %s' % (x8, bad8 or 'NONE'))
    x9 = R.get('X9', {})
    C.chk('X9 nothing else touched', x9.get('proc_before') and x9.get('proc_before') == x9.get('proc_after') and x9.get('lookup_before') and x9.get('lookup_before') == x9.get('lookup_after') and x9.get('policy_delta_ok') is True,
          'pg_proc md5 before %s after %s | oauth_apps_auth_lookup md5 before %s after %s | policy counts %s -> %s, delta as expected: %s' % (
              str(x9.get('proc_before'))[:12], str(x9.get('proc_after'))[:12], str(x9.get('lookup_before'))[:12], str(x9.get('lookup_after'))[:12], x9.get('policies_before'), x9.get('policies_after'), x9.get('policy_delta_ok')))
    x10 = R.get('X10', {}); u = x10.get('users')
    bad10 = {t: v for t, v in x10.items() if t != 'users' and v != u}
    C.chk('X10 policy text == 039 users', u and len(x10) == 5 and not bad10, 'users (039) qual|with_check md5 %s | differing %s' % (str(u)[:40], bad10 or 'NONE'))
    x11 = R.get('X11', {})
    C.chk('X11 dump nonce filtered', x11.get('filtered_equal') is True and x11.get('restrict_lines', 0) >= 0, 'raw dumps equal %s (a nonce makes them differ) | \\restrict lines %s | filtered equal %s' % (
        x11.get('raw_equal'), x11.get('restrict_lines'), x11.get('filtered_equal')))
    x12 = R.get('X12', {})
    C.chk('X12 lock_timeout honoured', x12.get('rc') not in (None, 0) and 'lock timeout' in str(x12.get('err', '')).lower() and (x12.get('secs') or 99) < 15 and x12.get('unchanged') is True and x12.get('retry_rc') == 0,
          'apply under a held lock rc %s in %s s, %r | charge_events unchanged %s | retry after release rc %s' % (x12.get('rc'), x12.get('secs'), str(x12.get('err'))[:80], x12.get('unchanged'), x12.get('retry_rc')))


def census_classify(lines):
    """lines: [(path, lineno, text)] -> {class: [(path:line, text)]}"""
    out = {'WRITE': [], 'DDL': [], 'CALLER': [], 'READ': [], 'OTHER': [], 'EXCLUDED': []}
    for p, n, t in lines:
        loc = '%s:%s' % (p, n)
        if 'billing_charge_events' in t and 'charge_events' not in t.replace('billing_charge_events', ''):
            out['EXCLUDED'].append((loc, t)); continue
        if re.search(r'\b(INSERT\s+INTO|UPDATE|DELETE\s+FROM|TRUNCATE(\s+TABLE)?)\s+charge_events\b', t, re.I): out['WRITE'].append((loc, t))
        elif re.search(r'\b(CREATE\s+TABLE(\s+IF\s+NOT\s+EXISTS)?|ALTER\s+TABLE(\s+IF\s+EXISTS)?)\s+(public\.)?charge_events\b', t, re.I): out['DDL'].append((loc, t))
        elif re.search(r'\bcreateChargeEvent\s*\(', t) and not re.search(r'function\s+createChargeEvent|import|typeof\s+createChargeEvent', t): out['CALLER'].append((loc, t))
        elif re.search(r'\bFROM\s+charge_events\b', t, re.I): out['READ'].append((loc, t))
        else: out['OTHER'].append((loc, t))
    return out


def judge_census(C, cl):
    exp = K['writer_census_expected']; probs = {}
    for k in ('WRITE', 'DDL', 'CALLER'):
        got = sorted(l for l, _ in cl[k]); want = sorted(exp[k])
        probs[k] = {'NEW': [g for g in got if g not in want], 'GONE': [w for w in want if w not in got]}
    ok = all(not v['NEW'] and not v['GONE'] for v in probs.values()) and len(cl['EXCLUDED']) > 0 and len(cl['WRITE']) > 0
    C.chk('W1 writer census == kit', ok, 'WRITE %d DDL %d CALLER %d READ %d OTHER %d | CONTROL billing_charge_events EXCLUDED %d (> 0) | NEW/GONE %s' % (
        len(cl['WRITE']), len(cl['DDL']), len(cl['CALLER']), len(cl['READ']), len(cl['OTHER']), len(cl['EXCLUDED']), {k: v for k, v in probs.items() if v['NEW'] or v['GONE']} or 'NONE'))


if '--selftest' in A:
    st = {'ok': 0, 'n': 0}
    GOOD = {'X0': {'secuura_app': 'false/false', OWNER: 'false/false'}, 'X1': {'before': 3, 'after': 0}, 'X2': {'before': 8, 'after': 0},
            'X3': {'before': 'ok', 'after': 'refused: ERROR:  new row violates row-level security policy for table "charge_events"'}, 'X3b': {'after': 'ok'},
            'X4': {'before': 8, 'after': 8}, 'X5': {'before': 8, 'after': 0}, 'X6': {'before': 0, 'after': 1},
            'X7': {'su': DEFAULT, 'owner': None, 'owner_notice': 'KS-1401: certifications.tenant_id had 0 NULL rows; no data was written'},
            'X8': {'charge_events': 'charge_events|12|true|true|true|1', 'certifications': 'certifications|17|true|true|true|1', 'oauth_apps': 'oauth_apps|17|true|true|true|2', 'svc_webhooks': 'svc_webhooks|11|true|true|true|1'},
            'X9': {'proc_before': 'a' * 32, 'proc_after': 'a' * 32, 'lookup_before': 'b' * 32, 'lookup_after': 'b' * 32, 'policies_before': {}, 'policies_after': {}, 'policy_delta_ok': True},
            'X10': {'users': 'q|w', 'charge_events': 'q|w', 'certifications': 'q|w', 'oauth_apps': 'q|w', 'svc_webhooks': 'q|w'},
            'X11': {'raw_equal': False, 'restrict_lines': 2, 'filtered_equal': True},
            'X12': {'rc': 3, 'secs': 5.2, 'err': 'ERROR:  canceling statement due to lock timeout', 'unchanged': True, 'retry_rc': 0}}

    def flip(path, val):
        R = json.loads(json.dumps(GOOD)); d = R
        for p in path[:-1]: d = d[p]
        d[path[-1]] = val; return lambda C: judge(C, R)
    selftest_arm(st, 'P-0 the expected readings (positive control)', lambda C: judge(C, GOOD), None)
    for name, path, val, want in [('P-1 secuura_app bypasses RLS', ('X0', 'secuura_app'), 'true/false', 'X0'), ('P-2 B rows still visible to A', ('X1', 'after'), 3, 'X1'),
                                  ('P-3 no-GUC still 8 (fail-open)', ('X2', 'after'), 8, 'X2'), ('P-4 cross-tenant INSERT accepted', ('X3', 'after'), 'ok', 'X3'),
                                  ('P-5 WITH CHECK refuses the RIGHT tenant too', ('X3b', 'after'), 'refused: row-level security', 'X3'),
                                  ('P-6 the platform_admin carve-out broken', ('X4', 'after'), 0, 'X4'), ('P-7 FORCE dropped: owner still sees 8', ('X5', 'after'), 8, 'X5'),
                                  ('P-8 certifications still default-deny', ('X6', 'after'), 0, 'X6'), ('P-9 superuser backfill missed the NULL row', ('X7', 'su'), None, 'X7'),
                                  ('P-10 fresh shape: certifications no policy', ('X8', 'certifications'), 'certifications|17|true|true|true|0', 'X8'),
                                  ('P-11 a function body changed', ('X9', 'proc_after'), 'c' * 32, 'X9'), ('P-12 oauth_apps_auth_lookup changed', ('X9', 'lookup_after'), 'd' * 32, 'X9'),
                                  ('P-13 a weakened qual on charge_events', ('X10', 'charge_events'), 'true|w', 'X10'), ('P-14 the filtered dump unstable', ('X11', 'filtered_equal'), False, 'X11'),
                                  ('P-15 lock_timeout NOT honoured (applied under the lock)', ('X12', 'rc'), 0, 'X12'), ('P-16 a partial commit under the lock', ('X12', 'unchanged'), False, 'X12')]:
        selftest_arm(st, name, flip(path, val), want)
    PL = [('Blockchain/Dev/services/originate/src/services/chargeEvents.ts', 180, '      INSERT INTO charge_events (id, event_type'),
          ('Blockchain/Dev/services/originate/src/services/gdprService.ts', 561, '      DELETE FROM charge_events WHERE initiated_by = ${userId}'),
          ('Blockchain/Dev/services/api-gateway/src/startup-migrations.ts', 332, '  `CREATE TABLE IF NOT EXISTS charge_events ('),
          ('Blockchain/Dev/services/originate/src/index.ts', 458, '        CREATE TABLE IF NOT EXISTS charge_events (')] + \
         [('Blockchain/Dev/services/originate/src/routes/certifications.ts', n, '      x = await createChargeEvent(...)') for n in (593, 596, 966, 1071, 1219, 1357)] + \
         [('Blockchain/Dev/services/billing/src/chargeable-events.ts', 169, '        `INSERT INTO billing_charge_events')]
    selftest_arm(st, 'W-0 the drafter\'s census shape (positive control)', lambda C: judge_census(C, census_classify(PL)), None)
    selftest_arm(st, 'W-1 a NEW writer (UPDATE charge_events in metering.ts)', lambda C: judge_census(C, census_classify(PL + [('Blockchain/Dev/services/originate/src/routes/metering.ts', 99, 'UPDATE charge_events SET status = 1')])), 'W1')
    selftest_arm(st, 'W-2 a writer GONE (the INSERT moved)', lambda C: judge_census(C, census_classify(PL[1:])), 'W1')
    selftest_arm(st, 'W-3 a NEW caller of createChargeEvent', lambda C: judge_census(C, census_classify(PL + [('Blockchain/Dev/packages/shared/src/jobs/x.ts', 7, 'await createChargeEvent(a, b, c, d)')])), 'W1')
    selftest_arm(st, 'W-4 a blind control (no billing_charge_events line)', lambda C: judge_census(C, census_classify(PL[:-1])), 'W1')
    st['n'] += 1; cl = census_classify([('x', 1, 'INSERT INTO billing_charge_events (a)')]); ok = len(cl['EXCLUDED']) == 1 and not cl['WRITE']; st['ok'] += ok
    print('SELFTEST %s W-5 a billing_charge_events INSERT is EXCLUDED, never a WRITE: %s' % ('OK' if ok else 'MISS', {k: len(v) for k, v in cl.items()}))
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n']))
    print('CHECKED %d arm(s)' % st['n']); raise SystemExit(0 if st['ok'] == st['n'] and st['n'] > 0 else 1)

if MODE == 'census':
    REPO = opt('--repo'); HEAD = opt('--head', K['head'])
    if not REPO or not has_commit(REPO, HEAD): print('REFUSING: --repo <clone> with %s' % HEAD[:12]); raise SystemExit(2)
    rc, o, e = git(REPO, 'grep', '-n', '-I', '-i', '-E', 'charge_events|createChargeEvent', HEAD, '--', *K['writer_census_roots'], check=False)
    lines = []
    for l in o.splitlines():
        m = re.match(r'^[0-9a-f]{40}:([^:]+):(\d+):(.*)$', l)
        if m and '__tests__' not in m.group(1) and '.test.' not in m.group(1): lines.append((m.group(1), int(m.group(2)), m.group(3)))
    cl = census_classify(lines)
    # the must-hit CONTROL runs through the SAME classifier on a root where billing_charge_events lives (services/billing): every one of
    # those lines must land in EXCLUDED and none in WRITE — else the classifier cannot tell the two tables apart and its zero is blind
    rcc, oc, _ = git(REPO, 'grep', '-n', '-I', '-E', 'billing_charge_events', HEAD, '--', 'Blockchain/Dev/services/billing/src', check=False)
    ctl = census_classify([(m.group(1), int(m.group(2)), m.group(3)) for m in (re.match(r'^[0-9a-f]{40}:([^:]+):(\d+):(.*)$', l) for l in oc.splitlines()) if m])
    cl['EXCLUDED'] += ctl['EXCLUDED']
    print('c3b census %s | head %s | git grep rc %d | %d line(s) under %s (tests excluded) | CONTROL services/billing: %d billing_charge_events line(s) -> EXCLUDED %d, WRITE %d' % (
        now(), HEAD[:12], rc, len(lines), K['writer_census_roots'], len(oc.splitlines()), len(ctl['EXCLUDED']), len(ctl['WRITE'])))
    if ctl['WRITE']: cl['WRITE'] += ctl['WRITE']
    cache = {}
    def ctx(p, n, back=3):
        if p not in cache: cache[p] = git(REPO, 'show', '%s:%s' % (HEAD, p)).split('\n')
        return cache[p][max(0, n - 1 - back):n - 1]
    for k in ('WRITE', 'DDL', 'CALLER', 'READ'):
        for loc, t in cl[k]:
            p, n = loc.rsplit(':', 1); n = int(n); extra = ''
            if k == 'WRITE':
                above = ctx(p, n, 60); extra = ' | runWithPlatformScope within 60 lines above: %s | prisma.$executeRaw (GUC proxy) within 5 above: %s' % (
                    any('runWithPlatformScope' in x for x in above), any('$executeRaw' in x or '$queryRaw' in x for x in above[-5:]))
            if k == 'CALLER':
                m = re.search(r'createChargeEvent\(([^)]*)', t); args = [a.strip() for a in (m.group(1).split(',') if m else [])]
                extra = ' | tenant argument (4th): %r' % (args[3] if len(args) > 3 else 'NOT ON THIS LINE')
            print('%-6s %s | %s%s' % (k, loc, ' '.join(t.split())[:110], extra))
    print('EXCLUDED (control) %d billing_charge_events line(s); OTHER (comments / types / imports) %d' % (len(cl['EXCLUDED']), len(cl['OTHER'])))
    C = Checks(); judge_census(C, cl)
elif MODE == 'judge':
    R = json.load(open(opt('--json'))); C = Checks(); judge(C, R)
elif MODE == 'probe':
    WT = guard_scratch(opt('--worktree') or '', 'worktree'); OUT = guard_out(opt('--out') or ''); LABEL = opt('--label', 'head')
    PGBIN = opt('--pgbin') or next((c for c in ('/opt/homebrew/opt/postgresql@15/bin', '/usr/local/opt/postgresql@15/bin') if os.path.isfile(os.path.join(c, 'initdb'))), None)
    if not PGBIN: print('REFUSING: no PostgreSQL 15 keg (pass --pgbin; never $PATH) — a missing probe is NOT a pass'); raise SystemExit(2)
    DEVD = os.path.join(WT, K['install_dir']); F049 = opt('--sql049') or os.path.join(WT, K['migration'])
    if not os.path.isfile(F049): print('REFUSING: 049 not at %s' % F049); raise SystemExit(2)
    DATA = os.path.join(OUT, 'pg_%s_%s' % (LABEL, now().replace(':', ''))); SOCK = tempfile.mkdtemp(prefix='g61s.', dir='/tmp')
    LOG = open(os.path.join(OUT, 'c3b_probe_%s.log' % LABEL), 'w')
    def sh(cmd, **kw):
        r = subprocess.run(cmd, capture_output=True, text=True, **kw); LOG.write('$ %s\nrc %d\n%s%s\n' % (' '.join(cmd)[:300], r.returncode, r.stdout[-2000:], r.stderr[-2000:])); return r
    def psql(db, sql=None, f=None, pre=None, tA=True):
        cmd = [os.path.join(PGBIN, 'psql'), '-X', '-h', SOCK, '-U', 'postgres', '-d', db, '-v', 'ON_ERROR_STOP=1'] + (['-tA'] if tA else ['-q'])
        if pre: cmd += ['-c', pre]
        cmd += (['-f', f] if f else ['-c', sql]); return sh(cmd)
    def val(db, sql, pre=None):
        r = psql(db, sql, pre=pre); ls = [x for x in r.stdout.strip().split('\n') if x.strip()]; return ls[-1] if ls and r.returncode == 0 else 'ERR:%s' % r.stderr.strip()[:120]
    print('c3b probe %s | keg %s | %s | data %s | socket %s | 049 %s (sha256 %s)' % (now(), PGBIN, sh([os.path.join(PGBIN, 'postgres'), '--version']).stdout.strip(), DATA, SOCK, F049,
          hashlib.sha256(open(F049, 'rb').read()).hexdigest()[:16]))
    r = sh([os.path.join(PGBIN, 'initdb'), '-D', DATA, '-U', 'postgres', '--auth=trust', '-E', 'UTF8'])
    if r.returncode: print('REFUSING: initdb rc %d' % r.returncode); raise SystemExit(2)
    r = sh([os.path.join(PGBIN, 'pg_ctl'), '-D', DATA, '-l', os.path.join(DATA, 'pg.log'), '-o', "-c listen_addresses='' -c unix_socket_directories=%s -c fsync=off" % SOCK, '-w', 'start'])
    if r.returncode: print('REFUSING: pg_ctl start rc %d' % r.returncode); raise SystemExit(2)
    R = {}
    READ = ("SELECT c.relname||'|'||(SELECT count(*) FROM information_schema.columns k WHERE k.table_name=c.relname AND k.table_schema='public')||'|'||"
            "EXISTS(SELECT 1 FROM information_schema.columns k WHERE k.table_name=c.relname AND k.table_schema='public' AND k.column_name='tenant_id')||'|'||"
            "c.relrowsecurity||'|'||c.relforcerowsecurity||'|'||(SELECT count(*) FROM pg_policies p WHERE p.tablename=c.relname AND p.schemaname='public') "
            "FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relname='%s'")
    try:
        def build(db):
            psql('postgres', 'CREATE DATABASE %s' % db)
            psql(db, "DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='secuura_app') THEN CREATE ROLE secuura_app NOLOGIN; END IF; "
                     "IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='%s') THEN CREATE ROLE %s NOLOGIN NOSUPERUSER NOBYPASSRLS; END IF; END $$;" % (OWNER, OWNER))
            psql(db, 'CREATE TABLE IF NOT EXISTS _secuura_migrations (filename TEXT PRIMARY KEY, applied_at TIMESTAMPTZ DEFAULT NOW())')
            fails = []
            for f in sorted(glob.glob(os.path.join(DEVD, 'docker/init/0[1-9]*.sql'))):
                if psql(db, f=f).returncode: fails.append(os.path.basename(f))
            for f in sorted(glob.glob(os.path.join(DEVD, 'migrations/*.sql'))):
                b = os.path.basename(f)
                if 'latform' in b or b.startswith('049_'): continue
                if psql(db, f=f).returncode: fails.append(b)
                else: psql(db, "INSERT INTO _secuura_migrations (filename) VALUES ('%s') ON CONFLICT DO NOTHING" % b)
            print('INFO shape %s built: %d failed file(s) %s' % (db, len(fails), fails)); return fails
        def kfix(db):
            psql(db, "ALTER TABLE public.certifications ADD COLUMN IF NOT EXISTS tenant_id UUID; ALTER TABLE public.certifications ENABLE ROW LEVEL SECURITY; "
                     "ALTER TABLE public.certifications FORCE ROW LEVEL SECURITY; DROP POLICY IF EXISTS tenant_isolation ON public.charge_events; "
                     "ALTER TABLE public.charge_events NO FORCE ROW LEVEL SECURITY; ALTER TABLE public.charge_events DISABLE ROW LEVEL SECURITY; "
                     "GRANT SELECT,INSERT,UPDATE,DELETE ON public.charge_events, public.certifications TO secuura_app")
            psql(db, "INSERT INTO public.charge_events (id, event_type, tenant_id, amount) SELECT 'g61-'||g, 'g61.event', CASE WHEN g<=4 THEN '%s'::uuid WHEN g<=7 THEN '%s'::uuid ELSE NULL END, 1 FROM generate_series(1,8) g" % (TA, TB))
            psql(db, "INSERT INTO public.certifications (id, certification_type, tenant_id) VALUES ('11111111-1111-4111-8111-111111111111','g61','%s'),('22222222-2222-4222-8222-222222222222','g61','%s'),('33333333-3333-4333-8333-333333333333','g61',NULL)" % (TA, TB))
        APP = 'SET ROLE secuura_app'
        def cells(db, phase):
            R.setdefault('X1', {})[phase] = val(db, "SELECT count(*) FROM charge_events WHERE tenant_id='%s'" % TB, pre="%s; SELECT set_config('app.current_tenant_id','%s',false)" % (APP, TA))
            R.setdefault('X2', {})[phase] = val(db, 'SELECT count(*) FROM charge_events', pre=APP)
            r3 = psql(db, "BEGIN; SET LOCAL ROLE secuura_app; SELECT set_config('app.current_tenant_id','%s',true); INSERT INTO charge_events (id,event_type,tenant_id,amount) VALUES ('g61-x','x','%s',1); ROLLBACK;" % (TA, TB))
            R.setdefault('X3', {})[phase] = 'ok' if r3.returncode == 0 else 'refused: ' + r3.stderr.strip()[:160]
            r3b = psql(db, "BEGIN; SET LOCAL ROLE secuura_app; SELECT set_config('app.current_tenant_id','%s',true); INSERT INTO charge_events (id,event_type,tenant_id,amount) VALUES ('g61-y','y','%s',1); ROLLBACK;" % (TA, TA))
            R.setdefault('X3b', {})[phase] = 'ok' if r3b.returncode == 0 else 'refused: ' + r3b.stderr.strip()[:160]
            R.setdefault('X4', {})[phase] = val(db, 'SELECT count(*) FROM charge_events', pre="%s; SELECT set_config('app.tenant_scope_bypass','platform_admin',false)" % APP)
            R.setdefault('X6', {})[phase] = val(db, "SELECT count(*) FROM certifications WHERE tenant_id='%s'" % TA, pre="%s; SELECT set_config('app.current_tenant_id','%s',false)" % (APP, TA))
        PROC = "SELECT md5(string_agg(p.oid::regprocedure::text||':'||md5(coalesce(p.prosrc,'')), '|' ORDER BY p.oid::regprocedure::text)) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public'"
        LOOK = "SELECT md5(coalesce(qual,'')||'#'||coalesce(with_check,'')||'#'||roles::text||'#'||cmd||'#'||permissive) FROM pg_policies WHERE schemaname='public' AND tablename='oauth_apps' AND policyname='oauth_apps_auth_lookup'"
        PCNT = "SELECT string_agg(tablename||'='||n||':'||ti, ',' ORDER BY tablename) FROM (SELECT tablename, count(*) n, bool_or(policyname='tenant_isolation') ti FROM pg_policies WHERE schemaname='public' AND tablename IN ('charge_events','certifications','oauth_apps','svc_webhooks') GROUP BY tablename) s"
        R['build_failures'] = {'k_su': build('k_su')}; kfix('k_su')
        R['X0'] = {r_: val('k_su', "SELECT rolbypassrls::text||'/'||rolsuper::text FROM pg_roles WHERE rolname='%s'" % r_) for r_ in ('secuura_app', OWNER)}
        cells('k_su', 'before')
        pb, lb, cb = val('k_su', PROC), val('k_su', LOOK), val('k_su', PCNT)
        ra = psql('k_su', f=F049); R['apply_su'] = {'rc': ra.returncode, 'notices': [l for l in ra.stderr.split('\n') if 'NOTICE' in l]}
        cells('k_su', 'after')
        pa, la, ca = val('k_su', PROC), val('k_su', LOOK), val('k_su', PCNT)
        def pc(s): return {x.split('=')[0]: (int(x.split('=')[1].split(':')[0]), x.split(':')[1] == 'true') for x in (s or '').split(',') if '=' in x}
        b_, a_ = pc(cb), pc(ca)
        R['X9'] = {'proc_before': pb, 'proc_after': pa, 'lookup_before': lb, 'lookup_after': la, 'policies_before': cb, 'policies_after': ca,
                   'policy_delta_ok': all(a_.get(t, (0, False))[0] == b_.get(t, (0, False))[0] + (0 if b_.get(t, (0, False))[1] else 1) and a_.get(t, (0, False))[1] for t in K['tables'])}
        R['X7'] = {'su': val('k_su', "SELECT coalesce(tenant_id::text,'NULL') FROM certifications WHERE id='33333333-3333-4333-8333-333333333333'")}
        if R['X7']['su'] == 'NULL': R['X7']['su'] = None
        QW = "SELECT md5(coalesce(qual,''))||'|'||md5(coalesce(with_check,'')) FROM pg_policies WHERE schemaname='public' AND tablename='%s' AND policyname='tenant_isolation'"
        R['X10'] = {t: val('k_su', QW % t) for t in ['users'] + K['tables']}
        def dump(db):
            return subprocess.run([os.path.join(PGBIN, 'pg_dump'), '-h', SOCK, '-U', 'postgres', '-d', db, '--schema-only'] + sum([['-t', 'public.' + t] for t in K['tables']], []), capture_output=True, text=True).stdout
        d1, d2 = dump('k_su'), dump('k_su'); flt = lambda d: '\n'.join(l for l in d.split('\n') if not re.match(r'^\\(un)?restrict ', l))
        R['X11'] = {'raw_equal': d1 == d2, 'restrict_lines': len(re.findall(r'(?m)^\\(un)?restrict ', d1)), 'filtered_equal': flt(d1) == flt(d2) and len(flt(d1)) > 100}
        # X5 / X7-owner: a second DB whose four tables are owned by the non-bypass owner, 049 applied AS that owner
        R['build_failures']['k_own'] = build('k_own'); kfix('k_own')
        psql('k_own', '; '.join('ALTER TABLE public.%s OWNER TO %s' % (t, OWNER) for t in K['tables']))
        R['X5'] = {'before': val('k_own', 'SELECT count(*) FROM charge_events', pre='SET ROLE %s' % OWNER)}
        ro = psql('k_own', f=F049, pre='SET ROLE %s' % OWNER); R['apply_owner'] = {'rc': ro.returncode, 'err': ro.stderr.strip()[-300:]}
        R['X5']['after'] = val('k_own', 'SELECT count(*) FROM charge_events', pre='SET ROLE %s' % OWNER)
        v = val('k_own', "SELECT coalesce(tenant_id::text,'NULL') FROM certifications WHERE id='33333333-3333-4333-8333-333333333333'")
        R['X7']['owner'] = None if v == 'NULL' else v
        R['X7']['owner_notice'] = next((l.strip() for l in ro.stderr.split('\n') if 'certifications.tenant_id' in l), None)
        # X8 fresh shape
        R['build_failures']['fresh'] = build('fresh'); rf = psql('fresh', f=F049)
        R['X8'] = {t: val('fresh', READ % t) for t in K['tables']}; R['X8_apply_rc'] = rf.returncode
        # X12 lock_timeout
        R['build_failures']['k_lock'] = build('k_lock'); kfix('k_lock')
        holder = subprocess.Popen([os.path.join(PGBIN, 'psql'), '-X', '-h', SOCK, '-U', 'postgres', '-d', 'k_lock', '-c',
                                   'BEGIN; LOCK TABLE public.charge_events IN ACCESS SHARE MODE; SELECT pg_sleep(25); COMMIT;'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            if val('k_lock', "SELECT count(*) FROM pg_locks l JOIN pg_class c ON c.oid=l.relation WHERE c.relname='charge_events' AND l.mode='AccessShareLock' AND l.granted AND l.pid<>pg_backend_pid()") not in ('0', '') : break
            time.sleep(0.2)
        before = val('k_lock', READ % 'charge_events'); t0 = time.time(); rl = psql('k_lock', f=F049); secs = round(time.time() - t0, 1)
        after = val('k_lock', READ % 'charge_events'); holder.wait(timeout=60); rr = psql('k_lock', f=F049)
        R['X12'] = {'rc': rl.returncode, 'secs': secs, 'err': rl.stderr.strip()[-200:], 'unchanged': before == after, 'before': before, 'after': after, 'retry_rc': rr.returncode}
    finally:
        sh([os.path.join(PGBIN, 'pg_ctl'), '-D', DATA, '-m', 'fast', 'stop']); LOG.close()
    jp = os.path.join(OUT, 'c3b_probe_%s.json' % LABEL); json.dump(R, open(jp, 'w'), indent=1, default=str)
    for k_, v_ in R.items(): print('CELL %s %s' % (k_, json.dumps(v_, default=str)[:300]))
    print('INFO readings saved %s; cluster stopped; data %s and socket %s LEFT in place (never deleted)' % (jp, DATA, SOCK))
    C = Checks(); judge(C, R)
else:
    print(__doc__); raise SystemExit(2)
n = C.nfail()
print('CHECKED %d check(s)' % len(C.res))
print('C3B %s %s: %d FAIL of %d checks' % (MODE.upper(), 'PASS' if n == 0 and C.res else 'FAIL', n, len(C.res)))
raise SystemExit(1 if n or not C.res else 0)
