#!/usr/bin/env python3
"""c3b_pgprobe_gate68.py — the guarded revoke UPDATE run against a REAL PostgreSQL (#1393 ROUND 2, KS-1278, gate68).

WHAT IT IS: the statement TEXT is EXTRACTED from documentRepo.ts at --head (c2's template reader, never re-typed); every `${expr}` is
bound as a PREPARE parameter of the type Prisma sends (boolean for preserveTerminal, text for every string / null), so a text that is
not a UUID reaching `::uuid` raises 22P02 exactly as it would in production. `idAsUuid` is bound as the head's own declaration says
(`isValidUuid(id) ? id : null` -> the Python mirror of :1026's regex; `= id` -> raw).
WHAT IT IS NOT: the repo's own Postgres (docker compose — forbidden by the hold "No Docker, no stack"). The server is the HOST's
homebrew PostgreSQL (K pg_probe.pg_bin, machine-local), initdb'd in the caller's scratch, listening on 127.0.0.1 ONLY, superuser
(so RLS policies from migration 011 are NOT exercised). The table is a DDL SUBSET of docker/init/01-schema.sql `documents` + migration
011's tenant_id. Using it in a gate needs Wednesday's named exception (X9, RULINGS Q3).

ARMS (each on fresh fixtures; tenant T1 = a0…01, T2 = b0…02):
  P1 UUID-addressed live owned doc            -> UPDATE 1, status 'revoked'          (gate65 N-1393-1: the round-1 key gave 0)
  P2 external_id-addressed                    -> UPDATE 1
  P3 NON-UUID external id 'doc-1278'           -> NO ERROR (no 22P02), UPDATE 1       (Wednesday's condition)
  P4 already revoked                           -> UPDATE 0, status unchanged          (the guard IN the statement)
  P5 another tenant's doc, by uuid AND by external_id, from T1 -> UPDATE 0 both, the T2 row untouched
  P6 precedence: row A.external_id == row B.id (same tenant), address that uuid -> A updated, B untouched (external_id arm first)
  P7 no such row (deleted)                     -> UPDATE 0  (the KS-1419 shape: 0 rows -> null -> 400 where 404 belongs)
  P8 CONCURRENCY, two sessions, READ COMMITTED: A = BEGIN; EXECUTE; pg_sleep(2); COMMIT, B = EXECUTE started 0.7 s later
       -> A UPDATE 1, B UPDATE 0 (B blocked on A's row lock, re-checked the guard on the committed row)
  P8c CONTROL for P8: the BRANCH BASE's unguarded statement (32e0, develop's) under the same two sessions -> A 1, B 1 (the probe CAN
       see a double write; without this the 0 of P8 is not a measurement)
  P9 INFO: the head's UNGUARDED statement (the 12 other callers), UUID-addressed -> UPDATE 0 = KS 1424's class, measured
--selftest: the real head must pass P1-P8 + P8c; PLANTED sources must FAIL: U1 (idAsUuid = id) -> P3 22P02; T1 (guard clause deleted on
            the guarded branch) -> P4 and P8; T5b (` OR TRUE` appended after the clause) -> P4 + P5; K1 (key reverted to external_id) -> P1.
Usage: c3b_pgprobe_gate68.py run|--selftest --repo <clone> --scratch <dir outside !CODING> [--head H]     rc 0 / 1 / 2 refused"""
import os, re, socket, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate68 import K, Tally, outside_forbidden, resolvable, show
from c2_product_gate68 import templates

BIN = K['pg_probe']['pg_bin']
T1, T2 = 'a0000000-0000-4000-8000-000000000001', 'b0000000-0000-4000-8000-000000000002'
UA, UB, UC = '2539dc16-c5f1-4d8c-b7e4-2d3ff3551278', '11111111-2222-4333-8444-555555555555', '99999999-8888-4777-8666-555555555555'
UUID_RX = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
DDL = """DROP TABLE IF EXISTS documents;
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  external_id VARCHAR(255) UNIQUE,
  title VARCHAR(500) NOT NULL DEFAULT 't',
  status VARCHAR(20) NOT NULL DEFAULT 'draft',
  metadata JSONB DEFAULT '{}',
  certification_metadata JSONB DEFAULT '{}',
  updated_at TIMESTAMPTZ DEFAULT now(),
  tenant_id UUID NOT NULL);
"""


class PG:
    def __init__(self, scratch):
        self.dir = os.path.join(scratch, 'pgprobe'); self.data = os.path.join(self.dir, 'data'); os.makedirs(self.dir, exist_ok=True)
        s = socket.socket(); s.bind(('127.0.0.1', 0)); self.port = s.getsockname()[1]; s.close()
        self.log = os.path.join(self.dir, 'server.log')

    def start(self):
        if not os.path.exists(os.path.join(self.data, 'PG_VERSION')):
            r = subprocess.run([BIN + '/initdb', '-D', self.data, '-A', 'trust', '-U', 'probe', '-E', 'UTF8', '--no-locale'], capture_output=True, text=True)
            if r.returncode: raise SystemExit('PGPROBE REFUSED: initdb rc %d %s' % (r.returncode, r.stderr[-300:]))
        o = "-c listen_addresses=127.0.0.1 -p %d -c unix_socket_directories=''" % self.port
        r = subprocess.run([BIN + '/pg_ctl', '-D', self.data, '-o', o, '-l', self.log, '-w', 'start'], capture_output=True, text=True)
        if r.returncode: raise SystemExit('PGPROBE REFUSED: pg_ctl start rc %d %s' % (r.returncode, (r.stdout + r.stderr)[-300:]))
        print('INFO server %s on 127.0.0.1:%d data %s' % (self.psql('SELECT version();').strip()[:60], self.port, self.data))

    def stop(self):
        subprocess.run([BIN + '/pg_ctl', '-D', self.data, '-m', 'fast', '-w', 'stop'], capture_output=True)

    def cmd(self):
        return [BIN + '/psql', '-X', '-h', '127.0.0.1', '-p', str(self.port), '-U', 'probe', '-d', 'postgres', '-v', 'ON_ERROR_STOP=1', '-A', '-t']

    def psql(self, sql):
        r = subprocess.run(self.cmd() + ['-c', sql], capture_output=True, text=True)
        return r.stdout + ('ERR ' + r.stderr if r.returncode else '')

    def script(self, sql):
        r = subprocess.run(self.cmd(), input=sql, capture_output=True, text=True)
        return r.returncode, r.stdout, r.stderr


def prepare(tmpl, name):
    exprs = re.findall(r'\$\{([^}]+)\}', tmpl); i = [0]
    def sub(m):
        i[0] += 1; return '$%d' % i[0]
    body = re.sub(r'\$\{([^}]+)\}', sub, tmpl)
    types = ['boolean' if e == 'preserveTerminal' else 'text' for e in exprs]
    return 'PREPARE %s(%s) AS %s;' % (name, ', '.join(types), body.strip()), exprs


def lit(v):
    if v is None: return 'NULL'
    if v is True: return 'true'
    if v is False: return 'false'
    return "'" + str(v).replace("'", "''") + "'"


def binding(src):
    if '    const idAsUuid = isValidUuid(id) ? id : null;\n' in src: return 'guarded'
    if '    const idAsUuid = id;\n' in src: return 'raw'
    return 'absent'


def execute(name, exprs, idv, tenant, mode):
    vals = {'preserveTerminal': False, 'updated.status': 'revoked', 'metadata': '{}', 'certMeta': '{}', 'id': idv, 'tenantId': tenant,
            'guardStatus': 'revoked', 'idAsUuid': (idv if UUID_RX.match(idv) else None) if mode == 'guarded' else idv}
    miss = [e for e in exprs if e not in vals]
    if miss: raise SystemExit('PGPROBE REFUSED: the statement binds unknown expression(s) %s — read it and extend the mirror' % miss)
    return 'EXECUTE %s(%s);' % (name, ', '.join(lit(vals[e]) for e in exprs))


def fixtures(rows):
    return DDL + ''.join("INSERT INTO documents (id, external_id, status, tenant_id) VALUES ('%s', %s, '%s', '%s');\n" % (i, lit(x), s, t) for i, x, s, t in rows)


def count_of(out):
    m = re.findall(r'^UPDATE (\d+)$', out, re.M)
    return int(m[-1]) if m else None


def arms(pg, gsrc, gtmpl, base_tmpl, ung_tmpl, t):
    mode = binding(gsrc)
    prep, ex = prepare(gtmpl, 'g')
    def one(rows, idv, tenant, tail=''):
        sql = fixtures(rows) + prep + '\n' + execute('g', ex, idv, tenant, mode) + '\n' + tail
        rc, o, e = pg.script(sql)
        return rc, o, e
    def status_of(o): return dict(re.findall(r'^([0-9a-f-]{36})\|(\w+)$', o, re.M))
    sel = "\\pset tuples_only on\nSELECT id || '|' || status FROM documents ORDER BY id;\n"
    rc, o, e = one([(UA, 'doc-1278', 'draft', T1)], UA, T1, sel)
    t.check('P1', rc == 0 and count_of(o) == 1 and status_of(o).get(UA) == 'revoked', 'UUID-addressed: rc %d UPDATE %s status %s %s' % (rc, count_of(o), status_of(o).get(UA), e.strip()[:120]))
    rc, o, e = one([(UA, 'doc-1278', 'draft', T1)], 'doc-1278', T1, sel)
    t.check('P2', rc == 0 and count_of(o) == 1, 'external_id-addressed: rc %d UPDATE %s %s' % (rc, count_of(o), e.strip()[:120]))
    rc, o, e = one([(UA, 'doc-1278', 'draft', T1)], 'doc-1278', T1, sel)
    t.check('P3', rc == 0 and '22P02' not in e and 'invalid input syntax for type uuid' not in e and count_of(o) == 1,
            "NON-UUID 'doc-1278' (idAsUuid bound %s): rc %d UPDATE %s | 22P02 %s %s" % (mode, rc, count_of(o), 'invalid input syntax for type uuid' in e, e.strip()[:140]))
    rc, o, e = one([(UA, 'doc-1278', 'revoked', T1)], UA, T1, sel)
    t.check('P4', rc == 0 and count_of(o) == 0 and status_of(o).get(UA) == 'revoked', 'already revoked: rc %d UPDATE %s (want 0)' % (rc, count_of(o)))
    rc, o, e = one([(UB, 'doc-t2', 'draft', T2)], UB, T1, sel); a = count_of(o); s1 = status_of(o).get(UB)
    rc2, o2, e2 = one([(UB, 'doc-t2', 'draft', T2)], 'doc-t2', T1, sel); b = count_of(o2); s2 = status_of(o2).get(UB)
    t.check('P5', rc == 0 and rc2 == 0 and a == 0 and b == 0 and s1 == 'draft' and s2 == 'draft', 'cross-tenant from T1: by uuid UPDATE %s, by external_id UPDATE %s, T2 row %s/%s' % (a, b, s1, s2))
    rc, o, e = one([(UA, UB, 'draft', T1), (UB, 'doc-b', 'draft', T1)], UB, T1, sel); st = status_of(o)
    t.check('P6', rc == 0 and count_of(o) == 1 and st.get(UA) == 'revoked' and st.get(UB) == 'draft', 'precedence (A.external_id == B.id): UPDATE %s, A %s, B %s (external_id arm first: A revoked, B untouched)' % (count_of(o), st.get(UA), st.get(UB)))
    rc, o, e = one([(UA, 'doc-1278', 'draft', T1)], UC, T1, sel)
    t.check('P7', rc == 0 and count_of(o) == 0, 'no such row (deleted): UPDATE %s (want 0 -> null -> 400 where 404 belongs: KS 1419 shape)' % count_of(o))
    a, b = concurrent(pg, gtmpl, mode, UA, 'g')
    t.check('P8', a == 1 and b == 0, 'CONCURRENCY guarded: session A UPDATE %s, session B UPDATE %s (want 1 / 0)' % (a, b))
    a, b = concurrent(pg, base_tmpl, 'absent', 'doc-1278', 'b0')
    t.check('P8c', a == 1 and b == 1, 'CONTROL develop\'s unguarded statement under the same two sessions: A %s, B %s (want 1 / 1: the probe sees a double write)' % (a, b))
    if ung_tmpl:
        pu, eu = prepare(ung_tmpl, 'u')
        rc, o, e = pg.script(fixtures([(UA, 'doc-1278', 'draft', T1)]) + pu + '\n' + execute('u', eu, UA, T1, 'absent') + '\n')
        t.info('P9', "head's UNGUARDED statement (12 other callers) UUID-addressed: rc %d UPDATE %s — the KS 1424 class (0 rows, caller reports success)" % (rc, count_of(o)))


def concurrent(pg, tmpl, mode, idv, name):
    prep, ex = prepare(tmpl, name)
    rc, o, e = pg.script(fixtures([(UA, 'doc-1278', 'draft', T1)]))
    run1 = prep + '\nBEGIN;\n' + execute(name, ex, idv, T1, mode) + '\nSELECT pg_sleep(2);\nCOMMIT;\n'
    run2 = prep + '\n' + execute(name, ex, idv, T1, mode) + '\n'
    pa = subprocess.Popen(pg.cmd(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pa.stdin.write(run1); pa.stdin.close()
    time.sleep(0.7)
    pb = subprocess.Popen(pg.cmd(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ob, eb = pb.communicate(run2, timeout=30); oa = pa.stdout.read(); pa.wait(timeout=30)
    return count_of(oa), count_of(ob)


def main():
    A = sys.argv[1:]
    def opt(k, d=None): return A[A.index(k) + 1] if k in A and A.index(k) + 1 < len(A) else d
    if not A or A[0] not in ('run', '--selftest'): print(__doc__); return 2
    repo, scratch = opt('--repo'), opt('--scratch')
    head = opt('--head', os.environ.get('G68_HEAD', K['head_expected']))
    if not (repo and scratch) or not outside_forbidden(scratch): print('PGPROBE REFUSED: --repo and a --scratch OUTSIDE %s are required' % K['forbidden_root']); return 2
    if not os.path.exists(BIN + '/postgres'): print('PGPROBE REFUSED: no PostgreSQL at %s (machine-local; NOT RUN)' % BIN); return 2
    for nm, s in (('head', head), ('branch base', K['branch_base'])):
        if not resolvable(repo, s): print('PGPROBE REFUSED: %s unresolvable: %s' % (nm, s)); return 2
    src = show(repo, head, K['repo_file']); ung, gua = templates(src)
    base_tmpl, _ = templates(show(repo, K['branch_base'], K['repo_file']))
    if gua is None: print('PGPROBE REFUSED: no guarded template at %s' % head[:12]); return 2
    pg = PG(scratch); pg.start()
    try:
        print('PGPROBE head %s | idAsUuid binding mode %s | guarded statement %d bindings' % (head[:12], binding(src), len(re.findall(r'\$\{', gua))))
        if A[0] == 'run':
            t = Tally(); arms(pg, src, gua, base_tmpl, ung, t); return t.end()
        res = []
        import io, contextlib
        def q(s, g):
            t = Tally(); b = io.StringIO()
            with contextlib.redirect_stdout(b): arms(pg, s, g, base_tmpl, None, t)
            return t, b.getvalue()
        t, o = q(src, gua); res.append(not t.fails and t.n == 9); print('%s POSITIVE the real head passes P1-P8 + P8c (%d checked, fails %s)' % ('PASS' if res[-1] else 'FAIL', t.n, t.fails))
        s = src.replace('    const idAsUuid = isValidUuid(id) ? id : null;\n', '    const idAsUuid = id;\n')
        t, o = q(s, gua); line = [l for l in o.split('\n') if l.startswith('FAIL P3')]
        res.append('P3' in t.fails and line and 'True' in line[0]); print('%s PLANTED U1 (idAsUuid = id): P3 FAILS with 22P02 | %s' % ('PASS' if res[-1] else 'FAIL', (line or [''])[0][:160]))
        g = gua.replace('        AND (${guardStatus}::text IS NULL OR status IS DISTINCT FROM ${guardStatus}::text)\n', '')
        t, o = q(src, g); res.append({'P4', 'P8'} <= set(t.fails)); print('%s PLANTED T1 (guard clause deleted): P4 + P8 FAIL | fails %s' % ('PASS' if res[-1] else 'FAIL', t.fails))
        g5 = gua.replace('AND (${guardStatus}::text IS NULL OR status IS DISTINCT FROM ${guardStatus}::text)', 'AND (${guardStatus}::text IS NULL OR status IS DISTINCT FROM ${guardStatus}::text) OR TRUE')
        t, o = q(src, g5); res.append(g5 != gua and {'P4', 'P5'} <= set(t.fails)); print('%s PLANTED T5b (` OR TRUE` appended after the guard: exact clause text survives): P4 + P5 FAIL (every row, every tenant) | fails %s' % ('PASS' if res[-1] else 'FAIL', t.fails))
        k1 = re.sub(r'      WHERE id = COALESCE\(.*?\n            \)\n', '      WHERE external_id = ${id}\n', gua, flags=re.S)
        t, o = q(src, k1); res.append(k1 != gua and 'P1' in t.fails); print('%s PLANTED K1 (key reverted to external_id): P1 FAILS | fails %s' % ('PASS' if res[-1] else 'FAIL', t.fails))
        print('SELFTEST %d/%d' % (sum(map(bool, res)), len(res))); return 0 if all(res) else 1
    finally:
        pg.stop(); print('INFO server stopped (data dir kept in scratch, never deleted): %s' % pg.data)


if __name__ == '__main__':
    sys.exit(main())
