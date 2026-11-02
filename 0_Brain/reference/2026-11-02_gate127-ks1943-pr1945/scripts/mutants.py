import hashlib, json, subprocess, sys, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945'
O = W + '/repo/Blockchain/Dev/services/originate/src'
DB, GD = O + '/db.ts', O + '/services/gdprService.ts'
A = O + '/__tests__/'
TESTS = [A + 'ks1943-retention-sweep-unit-all-or-nothing.test.ts', A + 'ks1943-platform-scope-transaction-helper.test.ts', A + 'ks1938-gdpr-retention-sweep-catches-unreadable-throw.test.ts']
HEAD = {DB: W + '/evidence/src/db_head.ts', GD: W + '/evidence/src/gdpr_head.ts'}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
HSHA = {k: sha(v) for k, v in HEAD.items()}
INS_OLD = "const logRows: any[] = await tx.$queryRaw`\n            INSERT INTO data_deletion_log"
STAMP_OLD = "          await tx.$executeRaw`\n          UPDATE data_retention_policies SET last_enforcement_at"
HELPER_ST = "    await tx.$executeRaw`SELECT set_config('app.tenant_scope_bypass', 'platform_admin', true)`;\n    return fn(tx as TenantTx);\n  });\n}"
M = {
 'M1 log INSERT outside the unit (prisma, not tx)': (GD, INS_OLD, INS_OLD.replace('await tx.$queryRaw', 'await prisma.$queryRaw'), ['st', 'mt']),
 'M2 stamp dropped from the unit (prisma, not tx)': (GD, STAMP_OLD, STAMP_OLD.replace('await tx.$executeRaw', 'await prisma.$executeRaw'), ['st', 'mt']),
 'M3 logs.push before commit (inside the unit)': (GD, "            row = logRows[0];\n", "            row = logRows[0];\n            if (row) logs.push(mapDeletionLogRow(row));\n", ['st']),
 'M3b logs.push before commit AND the post-commit push removed': (GD, "        if (logRow) logs.push(mapDeletionLogRow(logRow));\n", "        void logRow;\n", None),
 'M4 timeout dropped (st: Prisma timeout raised to 600000 ms)': (DB, HELPER_ST, HELPER_ST.replace('  });\n}', '  }, { timeout: 600000 });\n}'), ['to']),
 'M5a helper without a transaction (fn(prisma))': (DB, "  if (MULTI_TENANCY && tenantManager) {\n    const client = await tenantManager.getDefaultPool().connect();", "  return fn(prisma as unknown as TenantTx);\n  if (MULTI_TENANCY && tenantManager) {\n    const client = await tenantManager.getDefaultPool().connect();", ['st', 'mt']),
 'M5b sweep without the helper (inline fn(prisma))': (GD, "await withPlatformScopeTransaction(async (tx) => {", "await (async (f: any) => f(prisma))(async (tx: any) => {", ['st']),
 'M5c sweep without the helper, compiles (import kept used)': (GD, "        const logRow: any = await withPlatformScopeTransaction(async (tx) => {", "        void withPlatformScopeTransaction;\n        const logRow: any = await (async (f: any) => f(prisma))(async (tx: any) => {", ['st']),
 'M6a st: error swallowed inside the unit (commit attempted)': (DB, HELPER_ST, HELPER_ST.replace('return fn(tx as TenantTx);', 'return fn(tx as TenantTx).catch(() => undefined as any);'), ['st']),
 'M6b mt: error swallowed inside the unit (COMMIT sent)': (DB, "      const result = await fn(createPoolProxy(client) as TenantTx);\n      await client.query('COMMIT');\n      return result;\n    } catch (err) {\n      try { await client.query('ROLLBACK'); } catch { /* connection may be broken; the original", "      const result = await fn(createPoolProxy(client) as TenantTx).catch(() => undefined as any);\n      await client.query('COMMIT');\n      return result;\n    } catch (err) {\n      try { await client.query('ROLLBACK'); } catch { /* connection may be broken; the original", ['mt']),
 'M7 st: bypass set_config dropped': (DB, HELPER_ST, HELPER_ST.replace("    await tx.$executeRaw`SELECT set_config('app.tenant_scope_bypass', 'platform_admin', true)`;\n", ''), ['st']),
 'M8 mt: applyTenantGuc dropped': (DB, "      await applyTenantGuc(client);\n", "", ['mt']),
 'M5d helper without a transaction, compiles (guarded early return)': (DB, "  if (MULTI_TENANCY && tenantManager) {\n    const client = await tenantManager.getDefaultPool().connect();", "  if (true as boolean) return fn(prisma as unknown as TenantTx);\n  if (MULTI_TENANCY && tenantManager) {\n    const client = await tenantManager.getDefaultPool().connect();", None),
 'M8b mt: applyTenantGuc dropped, compiles (import kept used)': (DB, "      await applyTenantGuc(client);\n", "      void applyTenantGuc;\n", None),
 'M9 scope refusal removed': (DB, "  if (!isPlatformScope()) {\n    throw new Error('withPlatformScopeTransaction refused", "  if (false as boolean) {\n    throw new Error('withPlatformScopeTransaction refused", None),
 'M10 mt: no ROLLBACK on a throw': (DB, "      try { await client.query('ROLLBACK'); } catch { /* connection may be broken; the original error is the useful one */ }\n", "", ['mt']),
}
only = sys.argv[1:] if len(sys.argv) > 1 else None
env = dict(os.environ, TMPDIR='/tmp/g127')
rows = []
for name, (f, old, new, pg) in M.items():
    if only and not any(name.startswith(o + ' ') for o in only): continue
    src = open(HEAD[f]).read()
    n = src.count(old)
    if n != 1:
        rows.append((name, f'ANCHOR COUNT {n}', '', '', '')); print(name, 'ANCHOR', n, flush=True); continue
    open(f, 'w').write(src.replace(old, new))
    tag = name.split(' ')[0]
    out = W + f'/logs/mut_{tag}'
    rc = subprocess.run(['bash', W + '/scripts/run.sh', out, '--runTestsByPath', *TESTS], env=env).returncode
    killed = []
    try:
        j = json.load(open(out + '.json'))
        for tf in j['testResults']:
            for a in tf['assertionResults']:
                if a['status'] == 'failed':
                    msg = ' '.join(a.get('failureMessages') or [])[:400]
                    how = 'assert' if ('expect(' in msg or 'toEqual' in msg or 'toBe' in msg or 'toHaveLength' in msg or 'rejects' in msg) else 'OTHER'
                    killed.append(f"{a['title'].split(':')[0][:60]} [{how}]")
            if tf.get('status') == 'failed' and not tf['assertionResults']:
                killed.append('SUITE FAILED TO RUN: ' + tf.get('message', '')[:200])
    except Exception as e:
        killed.append(f'NO JSON {e}')
    pgres = []
    for m in (pg or []):
        if m == 'to':
            r = subprocess.run(['bash', '-c', f'set -a; . /tmp/g127/pg/env; set +a; export G127_PG_PORT=$(docker port g127-pg 5432 | sed "s/.*://"); nice -n 10 {W}/repo/Blockchain/Dev/node_modules/.bin/tsx {W}/scripts/pgtimeout_g127.mts mut{tag} st {out}_pgto.json 9000 > {out}_pgto.txt 2>&1'], env=env)
            j = json.load(open(out + '_pgto.json'))
            pgres.append(f"timeout st: remaining={j['afterState']['remaining']} log={len(j['afterState']['logRows'])} returned={j['returned']}")
        else:
            r = subprocess.run(['bash', '-c', f'set -a; . /tmp/g127/pg/env; set +a; export G127_PG_PORT=$(docker port g127-pg 5432 | sed "s/.*://"); nice -n 10 {W}/repo/Blockchain/Dev/node_modules/.bin/tsx {W}/scripts/pgproof_g127.mts mut{tag} {m} {out}_pg_{m}.json > {out}_pg_{m}.txt 2>&1'], env=env)
            j = json.load(open(f'{out}_pg_{m}.json'))
            fails = [x['name'] for x in j['results'] if not x['ks1943']]
            pgres.append(f"real-PG {m}: {len(j['results']) - len(fails)}/{len(j['results'])} pass; FAIL {fails}")
    open(f, 'w').write(src)
    ok = all(sha(p) == HSHA[p] for p in HEAD)
    verdict = 'KILLED' if killed else 'SURVIVED (unit cells)'
    rows.append((name, verdict, '; '.join(killed), ' | '.join(pgres), f'restore {ok}'))
    print(f'{name}: {verdict} jest rc={rc} :: {"; ".join(killed)} :: {" | ".join(pgres)} :: restore {ok}', flush=True)
    if not ok: print('RESTORE FAILED - STOP'); sys.exit(9)
with open(W + '/logs/mutants_table.log', 'a') as fh:
    for r in rows: fh.write(' || '.join(r) + '\n')
