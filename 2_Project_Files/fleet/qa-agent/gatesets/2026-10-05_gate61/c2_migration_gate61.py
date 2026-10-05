#!/usr/bin/env python3
"""c2_migration_gate61.py — gate61 C2 MIGRATION READ for #1383 (KS-1401): a STATIC read of 049 at the head (git objects in YOUR scratch
clone; nothing is executed, no database is touched).
  L0 LIVE-SQL GUARD (runs FIRST; every other check reads ONLY the stripped text): a tokenizer strips `--` line comments and `/* */` block
     comments (nesting honoured) while leaving single-quoted strings and $tag$ dollar-quoted bodies intact; then asserts > 20 live
     (non-blank) lines, that the stripped text still carries `DO $`, `CREATE POLICY` and `END`, and that the stripper removed > 0 comment
     lines (CONTROL: it did something). Seat F 2nd's own run hit a comment-strip that blanked its live-SQL guard: this guard exists for that.
  M1 ONE DO BLOCK      exactly one `DO $tag$ … $tag$;`, and NOTHING live outside it (no top-level ALTER / CREATE / UPDATE / BEGIN).
  M2 LOCK_TIMEOUT      set_config('lock_timeout', '<n>s|ms', true) (or SET LOCAL lock_timeout) inside the block, BEFORE the first ALTER.
  M3 NO SET NOT NULL   0 `SET NOT NULL` (Q-NOTNULL).
  M4 ABSENT RAISES     `IF NOT EXISTS (SELECT … information_schema.tables …) THEN RAISE EXCEPTION` (Q-ABSENT), and no NOTICE-and-CONTINUE.
  M5 MUST-NOT          0 of: INSERT INTO _secuura_migrations; DELETE FROM; TRUNCATE; DROP TABLE; DROP/ALTER COLUMN; CREATE/DROP/ALTER
                       FUNCTION; GRANT/REVOKE; DISABLE ROW LEVEL; NO FORCE; top-level BEGIN;/COMMIT;/ROLLBACK;; oauth_apps_auth_lookup;
                       any (CREATE|DROP|ALTER) POLICY whose name is not tenant_isolation. Each pattern's count printed.
  M6 NULL-ONLY BACKFILL every UPDATE sets ONLY tenant_id = $1 and is guarded `WHERE tenant_id IS NULL`; >= 1 UPDATE exists.
  M7 TABLES            the ONE ARRAY[...] == exactly the kit's 4 tables; every ALTER TABLE / ON target is the %I placeholder (no literal
                       table name anywhere in an ALTER / POLICY statement).
  M8 POLICY FIDELITY   the $p$…$p$ CREATE POLICY literal in 049 is BYTE-EQUAL to 039's at develop (CONTROL: 039's literal found, carries
                       platform_admin). The gate's C3 measures the deparsed qual/with_check on a real database; this is the source half.
  M9 NO OTHER MIGRATION `git diff --name-status develop head -- Blockchain/Dev/migrations/` == exactly `A 049_…`; 038a and 039 blobs ==
                       kit (038a not edited, 039 not edited).
  M10 NAME             049_*, no 'platform' (routes MAIN only), sorts after every .sql at develop, the ONLY 049_* at head.
  M11 ENABLE+FORCE     both present; DROP POLICY IF EXISTS tenant_isolation precedes CREATE POLICY tenant_isolation.
  M12 ADD COLUMN GUARD `ADD COLUMN tenant_id` only under IF NOT EXISTS (… information_schema.columns … tenant_id …).
  INFO the CREATE POLICY target is `%I` (search_path) while ALTER/DROP use `public.%I`; the backfill runs BEFORE this file's ENABLE/FORCE
       but UNDER any FORCE already on the table — a non-bypass, non-superuser migrating role sees 0 rows there (probe X7 measures it).
--selftest  the REAL 049 PASSES (T0); stripper unit arms (a `--` inside a quoted string survives; a block comment's DROP POLICY is not
            counted); planted copies each FAIL their named check.
Usage: c2_migration_gate61.py --repo <clone> [--head sha] [--sql-file f]  |  --selftest --repo <clone>     rc 0 PASS / 1 FAIL / 2 usage
Prints `CHECKED <n>`; 0 checked is a FAIL."""
import copy, hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate61 import K, git, now, Checks, opt_factory, show, has_commit, blob, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); HEAD = opt('--head', K['head']); DEV = K['develop']; MIG = K['migration']
for s in (HEAD, DEV):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)


def strip_sql(src):
    """-> (stripped text with comments replaced by spaces, newlines kept; number of lines that held a comment)"""
    out = []; i = 0; n = len(src); com_lines = set(); line = 0; state = None; tag = ''; depth = 0
    while i < n:
        c = src[i]
        if c == '\n': line += 1
        if state is None:
            if src.startswith('--', i):
                state = 'line'; com_lines.add(line); out.append('  '); i += 2; continue
            if src.startswith('/*', i):
                state = 'block'; depth = 1; com_lines.add(line); out.append('  '); i += 2; continue
            if c == "'":
                state = 'str'; out.append(c); i += 1; continue
            m = re.match(r'\$[A-Za-z_0-9]*\$', src[i:])
            if m:
                state = 'dollar'; tag = m.group(0); out.append(tag); i += len(tag); continue
            out.append(c); i += 1; continue
        if state == 'line':
            if c == '\n': state = None; out.append('\n')
            else: out.append(' ')
            i += 1; continue
        if state == 'block':
            if c == '\n': com_lines.add(line + 0); out.append('\n'); i += 1; continue
            if src.startswith('/*', i): depth += 1; out.append('  '); i += 2; continue
            if src.startswith('*/', i):
                depth -= 1; out.append('  '); i += 2
                if depth == 0: state = None
                continue
            out.append(' '); i += 1; continue
        if state == 'str':
            out.append(c); i += 1
            if c == "'":
                if i < n and src[i] == "'": out.append("'"); i += 1
                else: state = None
            continue
        if state == 'dollar':
            if src.startswith(tag, i):
                out.append(tag); i += len(tag); state = None; continue
            # INSIDE a dollar-quoted body (a DO block or a $p$ literal): SQL comments there are still comments when the body is SQL
            # (a DO body is parsed again as PL/pgSQL). Strip `--` to EOL inside the body too, but not inside a nested quoted string.
            if src.startswith('--', i):
                j = src.find('\n', i); j = n if j < 0 else j
                com_lines.add(line); out.append(' ' * (j - i)); i = j; continue
            if c == "'":
                j = i + 1
                while j < n:
                    if src[j] == "'" and (j + 1 >= n or src[j + 1] != "'"): break
                    j += 2 if src[j] == "'" else 1
                seg = src[i:j + 1]; out.append(seg); line += seg.count('\n'); i = j + 1; continue
            out.append(c); i += 1; continue
    return ''.join(out), len(com_lines)


def facts(sql049, sql039, diff_ns, blobs, ls_head, ls_dev):
    return {'sql': sql049, 'sql039': sql039, 'diff': diff_ns, 'blobs': blobs, 'ls_head': ls_head, 'ls_dev': ls_dev}


def p_literal(src):
    m = re.search(r'\$p\$(.*?)\$p\$', src, re.S)
    return m.group(1) if m else None


def judge(C, F):
    raw = F['sql']; S, ncl = strip_sql(raw); live = [l for l in S.split('\n') if l.strip()]
    must = {'DO $': 'DO $' in S, 'CREATE POLICY': 'CREATE POLICY' in S, 'END': re.search(r'\bEND\b', S) is not None}
    ok0 = len(live) > 20 and all(must.values()) and ncl > 0
    C.chk('L0 live-SQL guard', ok0, '%d live line(s) after stripping (want > 20) | still carries %s | comment line(s) stripped %d (CONTROL > 0) | raw %d lines' % (
        len(live), must, ncl, raw.count('\n') + 1))
    if not ok0:
        print('REFUSING VERDICT: the live-SQL guard failed — every M check below would read blanked text'); return
    U = S.upper()
    dos = list(re.finditer(r'\bDO\s+(\$[A-Za-z0-9_]*\$)', S))
    outside = None
    if len(dos) == 1:
        tag = dos[0].group(1); end = S.find(tag, dos[0].end())
        semi = re.match(r'\s*;', S[end + len(tag):]) if end >= 0 else None
        outside = (S[:dos[0].start()] + (S[end + len(tag) + semi.end():] if semi else 'UNTERMINATED')).strip()
    C.chk('M1 one DO block', len(dos) == 1 and outside == '', 'DO blocks %d (want 1) | live text outside the block %r' % (len(dos), (outside or '')[:120] if outside is not None else 'n/a'))
    lt = re.search(r"set_config\(\s*'lock_timeout'\s*,\s*'(\d+)\s*(ms|s)'\s*,\s*true\s*\)|SET\s+LOCAL\s+lock_timeout\s*(=|TO)\s*'?(\d+)\s*(ms|s)", S, re.I)
    fa = re.search(r'ALTER\s+TABLE', S, re.I)
    C.chk('M2 lock_timeout', lt is not None and fa is not None and lt.start() < fa.start(), 'lock_timeout %s at offset %s | first ALTER TABLE at %s | before it: %s' % (
        lt.group(0) if lt else 'ABSENT', lt.start() if lt else '-', fa.start() if fa else '-', bool(lt and fa and lt.start() < fa.start())))
    C.chk('M3 no SET NOT NULL', not re.search(r'SET\s+NOT\s+NULL', U), '`SET NOT NULL` count %d' % len(re.findall(r'SET\s+NOT\s+NULL', U)))
    ab = re.search(r'IF\s+NOT\s+EXISTS\s*\(\s*SELECT[^;]*?information_schema\.tables[^;]*?\)\s*THEN\s*RAISE\s+EXCEPTION', S, re.I | re.S)
    nc = re.search(r'information_schema\.tables[^;]*?\)\s*THEN\s*RAISE\s+NOTICE[^;]*;\s*CONTINUE', S, re.I | re.S)
    C.chk('M4 absent table RAISEs', ab is not None and nc is None, 'IF NOT EXISTS(information_schema.tables) THEN RAISE EXCEPTION: %s | NOTICE-and-CONTINUE on absence: %s' % (ab is not None, nc is not None))
    pats = {'INSERT INTO _secuura_migrations': r'INSERT\s+INTO\s+_secuura_migrations', 'DELETE FROM': r'\bDELETE\s+FROM\b', 'TRUNCATE': r'\bTRUNCATE\b',
            'DROP TABLE': r'\bDROP\s+TABLE\b', 'DROP/ALTER COLUMN': r'\b(DROP|ALTER)\s+COLUMN\b', 'CREATE/DROP/ALTER FUNCTION': r'\b(CREATE|DROP|ALTER)\s+(OR\s+REPLACE\s+)?FUNCTION\b',
            'GRANT/REVOKE': r'\b(GRANT|REVOKE)\b', 'DISABLE ROW LEVEL': r'\bDISABLE\s+ROW\s+LEVEL\b', 'NO FORCE': r'\bNO\s+FORCE\b',
            'top-level BEGIN;/COMMIT;/ROLLBACK;': r'(?m)^\s*(BEGIN|COMMIT|ROLLBACK)\s*;', 'oauth_apps_auth_lookup': r'oauth_apps_auth_lookup'}
    cnt = {k: len(re.findall(v, S, re.I)) for k, v in pats.items()}
    pol = [m.group(3) for m in re.finditer(r'\b(CREATE|DROP|ALTER)\s+POLICY\s+(IF\s+EXISTS\s+)?(\w+)', S, re.I)]
    badpol = [p for p in pol if p != 'tenant_isolation']
    C.chk('M5 must-not', not any(cnt.values()) and not badpol and pol, 'counts %s | policy names touched %s (only tenant_isolation allowed; non-empty) | foreign %s' % (
        {k: v for k, v in cnt.items()}, sorted(set(pol)), badpol or 'NONE'))
    ups = re.findall(r"\bUPDATE\b([^';]*)", S, re.I)
    good = [u for u in ups if re.fullmatch(r"\s+public\.%I\s+SET\s+tenant_id\s*=\s*\$1\s+WHERE\s+tenant_id\s+IS\s+NULL\s*", u, re.I)]
    C.chk('M6 NULL-only backfill', ups and len(good) == len(ups), '%d UPDATE statement(s), %d of them `SET tenant_id = $1 WHERE tenant_id IS NULL` exactly | %s' % (len(ups), len(good), [u.strip()[:80] for u in ups]))
    arr = re.findall(r'ARRAY\s*\[([^\]]*)\]', S, re.I); names = sorted(re.findall(r"'(\w+)'", arr[0])) if len(arr) == 1 else []
    lit = [m.group(0) for m in re.finditer(r'(ALTER\s+TABLE|POLICY\s+(IF\s+EXISTS\s+)?\w+\s+ON)\s+(?!(public\.)?%I\b)\S+', S, re.I)]
    C.chk('M7 tables', len(arr) == 1 and names == sorted(K['tables']) and not lit, 'ARRAY literals %d | tables %s (kit %s) | statements with a literal target %s' % (len(arr), names, sorted(K['tables']), lit or 'NONE'))
    a, b = p_literal(raw), p_literal(F['sql039'] or '')
    C.chk('M8 policy literal == 039', a is not None and b is not None and a == b and 'platform_admin' in (b or ''),
          '049 $p$ literal %s | 039 (develop) $p$ literal %s | byte-equal %s | CONTROL 039 literal found and carries platform_admin: %s' % (
              hashlib.sha256((a or '').encode()).hexdigest()[:16] if a else 'ABSENT', hashlib.sha256((b or '').encode()).hexdigest()[:16] if b else 'ABSENT', a == b, bool(b and 'platform_admin' in b)))
    bl = F['blobs']
    C.chk('M9 no other migration', F['diff'] == [('A', MIG)] and bl['038a'] == K['blobs']['develop']['038a'] and bl['039'] == K['blobs']['develop']['039'],
          'name-status develop..head under migrations/ %s (want [A %s]) | 038a blob %s (kit %s) | 039 blob %s (kit %s)' % (
              F['diff'], MIG.split('/')[-1], (bl['038a'] or 'ABSENT')[:12], K['blobs']['develop']['038a'][:12], (bl['039'] or 'ABSENT')[:12], K['blobs']['develop']['039'][:12]))
    base = MIG.split('/')[-1]; sq_dev = sorted(x for x in F['ls_dev'] if x.endswith('.sql')); n049 = [x for x in F['ls_head'] if x.startswith('049_')]
    C.chk('M10 name', base.startswith('049_') and 'platform' not in base.lower() and all(base > x for x in sq_dev) and n049 == [base],
          '%s | "platform" in name: %s | sorts after all %d .sql at develop (last %s): %s | 049_* at head %s' % (
              base, 'platform' in base.lower(), len(sq_dev), sq_dev[-1] if sq_dev else '-', all(base > x for x in sq_dev), n049))
    en = re.search(r'ENABLE\s+ROW\s+LEVEL\s+SECURITY', S, re.I); fo = re.search(r'\bFORCE\s+ROW\s+LEVEL\s+SECURITY', S, re.I)
    dp = re.search(r'DROP\s+POLICY\s+IF\s+EXISTS\s+tenant_isolation', S, re.I); cp = re.search(r'CREATE\s+POLICY\s+tenant_isolation', S, re.I)
    C.chk('M11 ENABLE + FORCE + replace', en and fo and dp and cp and dp.start() < cp.start(), 'ENABLE %s | FORCE %s | DROP POLICY IF EXISTS tenant_isolation %s before CREATE POLICY tenant_isolation %s: %s' % (
        bool(en), bool(fo), bool(dp), bool(cp), bool(dp and cp and dp.start() < cp.start())))
    adds = list(re.finditer(r'ADD\s+COLUMN\s+(IF\s+NOT\s+EXISTS\s+)?tenant_id', S, re.I))
    def _guarded(m):
        if m.group(1): return True
        pre = S[:m.start()]; th = [x for x in re.finditer(r'\bTHEN\b', pre, re.I)]
        if not th or ';' in pre[th[-1].end():]: return False
        ifs = [x for x in re.finditer(r'\bIF\b', pre[:th[-1].start()], re.I)]
        cond = pre[ifs[-1].start():th[-1].start()] if ifs else ''
        return re.fullmatch(r"IF\s+NOT\s+EXISTS\s*\(\s*SELECT[^;]*information_schema\.columns[^;]*'tenant_id'[^;]*\)\s*", cond, re.I | re.S) is not None
    guarded = all(_guarded(m) for m in adds)
    C.chk('M12 ADD COLUMN guarded', adds and guarded, '%d ADD COLUMN tenant_id, each under IF NOT EXISTS(information_schema.columns … tenant_id) or IF NOT EXISTS: %s' % (len(adds), bool(guarded)))
    tg = re.findall(r'CREATE\s+POLICY\s+\w+\s+ON\s+(\S+)', S, re.I); at = sorted(set(re.findall(r'(?:ALTER\s+TABLE|ON)\s+(public\.%I|%I)\b', S, re.I)))
    print('INFO CREATE POLICY targets %s vs ALTER/DROP targets %s — a mixed qualification resolves CREATE POLICY through search_path (039 uses bare %%I throughout)' % (tg, at))
    print('INFO the UPDATE runs before this file\'s ENABLE/FORCE but UNDER any FORCE already on the table (certifications, oauth_apps, svc_webhooks on kintsugi): as a non-bypass, non-superuser OWNER it sees 0 rows and the NOTICE reads "0 NULL rows" — the probe X7 measures it')


def real_facts(sha):
    s = show(REPO, sha, MIG); s39 = show(REPO, DEV, K['migration_039'])
    if s is None: print('REFUSING: %s absent at %s' % (MIG, sha[:12])); raise SystemExit(2)
    ns = [tuple(l.split('\t')[:2]) for l in git(REPO, 'diff', '--name-status', DEV, sha, '--', K['migrations_dir']).splitlines() if l.strip()]
    bl = {'038a': blob(REPO, sha, K['migration_038a']), '039': blob(REPO, sha, K['migration_039'])}
    lsh = [l.split('\t')[1].split('/')[-1] for l in git(REPO, 'ls-tree', sha, K['migrations_dir']).splitlines()]
    lsd = [l.split('\t')[1].split('/')[-1] for l in git(REPO, 'ls-tree', DEV, K['migrations_dir']).splitlines()]
    return facts(s, s39, ns, bl, lsh, lsd)


print('c2_migration_gate61 %s | clone %s | head %s | develop %s%s' % (now(), REPO, HEAD[:12], DEV[:12], ' | SQL FILE %s' % opt('--sql-file') if opt('--sql-file') else ''))
F = real_facts(HEAD)
if opt('--sql-file'):
    F['sql'] = open(opt('--sql-file'), encoding='utf-8').read()
print('INFO 049 at %s: %d bytes, sha256 %s' % (HEAD[:12], len(F['sql'].encode()), hashlib.sha256(F['sql'].encode()).hexdigest()))
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}; R = F['sql']

    def pl(old, new, cnt=1):
        assert R.count(old) >= 1, 'plant anchor absent: %r' % old[:60]
        if cnt == 1: assert R.count(old) == 1, 'plant anchor not unique (%d): %r' % (R.count(old), old[:60])
        return R.replace(old, new, cnt)

    def arm(sql=None, **upd):
        G2 = copy.deepcopy(F)
        if sql is not None: G2['sql'] = sql
        G2.update(upd); return lambda C: judge(C, G2)

    def unit(name, src, want_in, want_out):
        S, _ = strip_sql(src); ok = all(w in S for w in want_in) and not any(w in S for w in want_out)
        st['n'] += 1; st['ok'] += ok
        print('SELFTEST %s %s: stripped %r' % ('OK' if ok else 'MISS', name, ' '.join(S.split())[:120]))
    unit('U1 a `--` inside a quoted string survives the stripper', "SELECT 'a -- b'; -- gone\nSELECT 1;", ["'a -- b'", 'SELECT 1'], ['gone'])
    unit('U2 a /* */ comment (nested) is removed, live SQL after it kept', "/* DROP POLICY x /* inner */ still */ CREATE POLICY y;", ['CREATE POLICY y'], ['DROP POLICY', 'still'])
    unit('U3 a `--` inside a DO body is a comment, its quoted string is not', "DO $q$ BEGIN RAISE NOTICE 'x -- y'; -- DROP TABLE z\nEND $q$;", ["'x -- y'", 'END'], ['DROP TABLE'])
    selftest_arm(st, 'T0 the REAL 049 (positive control)', arm(), None)
    selftest_arm(st, 'T1 everything commented out (a blanked live-SQL guard)', arm('\n'.join('-- ' + l for l in R.split('\n'))), 'L0')
    selftest_arm(st, 'T2 lock_timeout removed', arm(pl("  PERFORM set_config('lock_timeout', '5s', true);\n", '')), 'M2')
    selftest_arm(st, 'T3 SET NOT NULL added', arm(pl("    GET DIAGNOSTICS filled = ROW_COUNT;\n", "    GET DIAGNOSTICS filled = ROW_COUNT;\n    EXECUTE format('ALTER TABLE public.%I ALTER COLUMN tenant_id SET NOT NULL', t);\n")), 'M3')
    selftest_arm(st, 'T4 absent table NOTICE-and-CONTINUE (039\'s old behaviour)', arm(re.sub(r"RAISE EXCEPTION\n\s+'KS-1401: table public\.% is absent[^;]*;", "RAISE NOTICE 'absent %', t;\n      CONTINUE;", R)), 'M4')
    selftest_arm(st, 'T5 a self-insert into _secuura_migrations after the block', arm(R.replace('$ks1401$;\n', "$ks1401$;\nINSERT INTO _secuura_migrations (filename) VALUES ('049_ks1401_tenant_isolation_after_039.sql');\n", 1)), 'M1')
    selftest_arm(st, 'T5b the same self-insert INSIDE the block', arm(pl('  END LOOP;\n', "  END LOOP;\n  INSERT INTO _secuura_migrations (filename) VALUES ('049');\n")), 'M5')
    selftest_arm(st, 'T6 a DELETE inside the block', arm(pl('  END LOOP;\n', "  END LOOP;\n  DELETE FROM charge_events WHERE tenant_id IS NULL;\n")), 'M5')
    selftest_arm(st, 'T7 a DROP FUNCTION inside the block', arm(pl('  END LOOP;\n', "  END LOOP;\n  DROP FUNCTION IF EXISTS auth_find_oauth_app_by_client_id(text);\n")), 'M5')
    selftest_arm(st, 'T8 oauth_apps_auth_lookup dropped', arm(pl('  END LOOP;\n', "  END LOOP;\n  DROP POLICY IF EXISTS oauth_apps_auth_lookup ON public.oauth_apps;\n")), 'M5')
    selftest_arm(st, 'T9 the NULL-only guard removed', arm(pl("'UPDATE public.%I SET tenant_id = $1 WHERE tenant_id IS NULL'", "'UPDATE public.%I SET tenant_id = $1'")), 'M6')
    selftest_arm(st, 'T10 a top-level ALTER outside the DO block', arm(R + "\nALTER TABLE public.charge_events FORCE ROW LEVEL SECURITY;\n"), 'M1')
    selftest_arm(st, 'T11 a second DO block', arm(R + "\nDO $x$ BEGIN PERFORM 1; END $x$;\n"), 'M1')
    selftest_arm(st, 'T12 a 5th table in the array', arm(pl("'charge_events', 'certifications', 'oauth_apps', 'svc_webhooks'", "'charge_events', 'certifications', 'oauth_apps', 'svc_webhooks', 'users'")), 'M7')
    selftest_arm(st, 'T13 one byte of the policy literal changed', arm(pl("OR current_setting('app.tenant_scope_bypass', true) = 'platform_admin'\n        )\n        WITH CHECK", "OR current_setting('app.tenant_scope_bypass', true) = 'platform_adm1n'\n        )\n        WITH CHECK")), 'M8')
    selftest_arm(st, 'T14 038a edited in the same PR', arm(diff=F['diff'] + [('M', K['migration_038a'])], blobs=dict(F['blobs'], **{'038a': '0' * 40})), 'M9')
    selftest_arm(st, 'T15 a second 049_ file at head', arm(ls_head=F['ls_head'] + ['049_other.sql']), 'M10')
    selftest_arm(st, 'T16 FORCE removed', arm(pl("    EXECUTE format('ALTER TABLE public.%I FORCE ROW LEVEL SECURITY', t);\n", '')), 'M11')
    selftest_arm(st, 'T17 ADD COLUMN unguarded', arm(re.sub(r"IF NOT EXISTS \(SELECT 1 FROM information_schema\.columns\s+WHERE[^)]*\) THEN\n(\s+EXECUTE format\('ALTER TABLE public\.%I ADD COLUMN tenant_id UUID', t\);)", r"IF true THEN\n\1", R)), 'M12')
    selftest_arm(st, 'T18 a literal table name in an ALTER', arm(pl('  END LOOP;\n', "  END LOOP;\n  ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;\n")), 'M7')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n']))
    print('CHECKED %d arm(s)' % st['n']); raise SystemExit(0 if st['ok'] == st['n'] and st['n'] > 0 else 1)
C = Checks(); judge(C, F); n = C.nfail()
print('CHECKED %d check(s)' % len(C.res))
print('C2 MIGRATION %s: %d FAIL of %d checks | 049 at %s' % ('PASS' if n == 0 and len(C.res) > 1 else 'FAIL', n, len(C.res), HEAD[:12]))
raise SystemExit(1 if n or len(C.res) <= 1 else 0)
