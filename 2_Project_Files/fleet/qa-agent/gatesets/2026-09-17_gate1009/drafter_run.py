#!/usr/bin/env python3
"""drafter_run.py — #1009: whole api-gateway suite on base 0308b7a04 / head 6ec0cb198 / merged (head + develop 73d3fcb90); tamper rows on head
(anchor count asserted 1, markers asserted, project tsc --noEmit -p . rc per row AND the including program's error lines in the ks864 files,
WHOLE suite with the denominator asserted, numFailed + numPending read, restore by git checkout asserted sha256-identical); red-before-green
of ks864c against the pre-#1007 system-status.ts blob 5b39da2ee; env probes. Predictions are FIXED here before the run. Scratch files are moved
out by rename (never rm)."""
import sys, os, json, re, subprocess
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1009')
from drafterlib import *
GWR = 'Blockchain/Dev/services/api-gateway'
FARM = ['?? Blockchain/Dev/node_modules', '?? Blockchain/Dev/packages/shared/node_modules', '?? Blockchain/Dev/services/api-gateway/node_modules', '?? node_modules']
SS = GWR + '/src/routes/system-status.ts'; KC = GWR + '/src/__tests__/ks864c-portal-env-vars.test.ts'
os.makedirs(W + '/_quarantine', exist_ok=True)
INC = '{"extends": "./tsconfig.json", "include": ["src/**/*"], "exclude": ["node_modules", "dist"]}\n'
def tsc(tree):
    gw = T[tree] + '/' + GWR; b = T[tree] + '/Blockchain/Dev/node_modules/.bin/tsc'
    p = subprocess.run([b, '--noEmit', '-p', '.'], cwd=gw, capture_output=True, text=True)
    cfg = gw + '/tsconfig.qa-including.json'; open(cfg, 'w').write(INC)
    q = subprocess.run([b, '--noEmit', '-p', 'tsconfig.qa-including.json'], cwd=gw, capture_output=True, text=True)
    os.rename(cfg, W + '/_quarantine/tsconfig.qa-including.%s.%d.json' % (tree, len(os.listdir(W + '/_quarantine'))))
    ks = [l for l in q.stdout.splitlines() if 'error TS' in l and 'ks864' in l]
    return p.returncode, ks
def porc(tree):
    got = [l for l in porcelain(tree) if not (l.startswith('?? ') and l.rstrip('/').endswith('node_modules'))]; return got
S = {}
P('drafter_run start', ts())
for t in ('base', 'head', 'merged'):
    assert porc(t) == [], porc(t)
    S[t] = vitest('suite_' + t, t, 'gw')
DEN = (S['head']['files'], S['head']['tests']); P('denominator asserted for tamper rows:', DEN)
P('ks864 cells at head:', {k.split(' :: ')[0].split('/')[-1][:6] + ' ' + k.split(' — ')[-1][:70]: v['status'] for k, v in S['head']['cells'].items() if 'ks864' in k})
def cell(sub):
    m = [k for k in S['head']['cells'] if sub(k)]; assert len(m) == 1, (m, len(m)); return m[0]
C = {}
for portal in ('issuer', 'verifier', 'admin'):
    for env in ('staging', 'development'):
        C[portal[0] + env[0]] = cell(lambda k: 'ks864c' in k and ('%s-portal reports' % portal) in k and k.endswith('NODE_ENV=' + env))
A1 = cell(lambda k: 'ks864a' in k and 'falls back to its localhost default' in k); A2 = cell(lambda k: 'ks864a' in k and 'no served URL names' in k)
B1 = cell(lambda k: 'ks864b' in k and 'issuer portal falls back' in k); B2 = cell(lambda k: 'ks864b' in k and 'no portal URL names' in k)
ISS = "    url: process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80',\n"
PL = "  // KS-864: the Azure staging estate is decommissioned — URLs come from the env var above or the localhost default.\n"
RESET = "      vi.resetModules();\n"
SETIMP_OLD = "      for (const p of PORTALS) process.env[p.envVar] = p.value;\n      const router = (await import('../routes/system-status')).default;\n"
SETIMP_NEW = "      const router = (await import('../routes/system-status')).default;\n      for (const p of PORTALS) process.env[p.envVar] = p.value;\n"
RESTORE = "      for (const k of Object.keys(process.env)) if (!(k in savedEnv)) delete process.env[k];\n      Object.assign(process.env, savedEnv);\n"
PROBE = "describeUnder('development');\n\ndescribe('qa1009 env probe', () => {\n  it('qa1009 probe — NODE_ENV and the three portal vars are restored after both blocks', () => {\n    expect([process.env.NODE_ENV, process.env.ISSUER_PORTAL_URL, process.env.VERIFIER_PORTAL_URL, process.env.ADMIN_PORTAL_URL]).toEqual([savedEnv.NODE_ENV, savedEnv.ISSUER_PORTAL_URL, savedEnv.VERIFIER_PORTAL_URL, savedEnv.ADMIN_PORTAL_URL]);\n  });\n});\n"
PROBE_CELL = '__tests__/ks864c-portal-env-vars.test.ts :: qa1009 env probe qa1009 probe — NODE_ENV and the three portal vars are restored after both blocks'
def tern(env, var, default):
    return "    url: process.env.NODE_ENV === '%s' ? '%s' : (process.env.%s || '%s'),\n" % (env, default, var, default)
# (label, [(file, old, new, markers)], predicted red set, extra tests added)
ROWS = [
 ('G2_issuer', [(SS, ISS, "    url: 'http://issuer-frontend:80',\n", [('ISSUER_PORTAL_URL', 0)])], {C['is'], C['id']}, 0),
 ('G2_verifier', [(SS, "    url: process.env.VERIFIER_PORTAL_URL || 'http://verifier-frontend:80',\n", "    url: 'http://verifier-frontend:80',\n", [('VERIFIER_PORTAL_URL', 0)])], {C['vs'], C['vd']}, 0),
 ('G2_admin', [(SS, "    url: process.env.ADMIN_PORTAL_URL || 'http://admin-frontend:80',\n", "    url: 'http://admin-frontend:80',\n", [('ADMIN_PORTAL_URL', 0)])], {C['as'], C['ad']}, 0),
 ('SA_1007seat_helper_staging_branch_restored', [(SS, PL, "  if (process.env.NODE_ENV === 'staging' && _azureServiceName) {\n    return `https://${_azureServiceName}.internal.ashypond-b460d1a1.westeurope.azurecontainerapps.io`;\n  }\n", [('.internal.ashypond-b460d1a1', 1)])], {A1, A2}, 0),
 ('SB_1007seat_issuer_staging_ternary_restored', [(SS, ISS, "    url: process.env.NODE_ENV === 'staging'\n      ? 'https://secuura-staging-issuer.ashypond-b460d1a1.westeurope.azurecontainerapps.io'\n      : (process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80'),\n", [('secuura-staging-issuer', 1)])], {B1, B2, C['is']}, 0),
 ('Q_devonly_issuer_ignores_var_under_development', [(SS, ISS, tern('development', 'ISSUER_PORTAL_URL', 'http://issuer-frontend:80'), [("=== 'development'", 1)])], {C['id']}, 0),
 ('Q_setup_resetModules_removed_PLUS_devonly', [(SS, ISS, tern('development', 'ISSUER_PORTAL_URL', 'http://issuer-frontend:80'), [("=== 'development'", 1)]), (KC, RESET, '', [('vi.resetModules();', 0)])], set(), 0),
 ('Q_setup_resetModules_removed_alone', [(KC, RESET, '', [('vi.resetModules();', 0)])], set(), 0),
 ('Q_setup_env_set_after_import', [(KC, SETIMP_OLD, SETIMP_NEW, [('default;\n      for (const p', 1)])], set(C.values()), 0),
 ('Q_residual_prodonly_issuer_ignores_var_under_production', [(SS, ISS, tern('production', 'ISSUER_PORTAL_URL', 'http://issuer-frontend:80'), [("=== 'production'", 1)])], set(), 0),
 ('Q_residual_issuer_or_to_nullish', [(SS, ISS, "    url: process.env.ISSUER_PORTAL_URL ?? 'http://issuer-frontend:80',\n", [('ISSUER_PORTAL_URL ??', 1)])], set(), 0),
 ('Q_envprobe_restore_intact', [(KC, "describeUnder('development');\n", PROBE, [('qa1009 env probe', 1)])], set(), 1),
 ('Q_envprobe_restore_removed_CONTROL', [(KC, "describeUnder('development');\n", PROBE, [('qa1009 env probe', 1)]), (KC, RESTORE, '', [('Object.assign(process.env, savedEnv)', 0)])], {PROBE_CELL}, 1),
]
pristine = {f: sha(T['head'] + '/' + f) for f in (SS, KC)}; P('pristine sha', {f.split('/')[-1]: v[:12] for f, v in pristine.items()})
rc0, ks0 = tsc('head'); P('head untampered: tsc -p . rc', rc0, '| including-program error lines in ks864 files', len(ks0), ks0[:3])
summary = []
ONLY = [x for x in os.environ.get('QA_ONLY', '').split(',') if x]
for label, edits, predicted, added in ROWS:
    if ONLY and label not in ONLY: continue
    P('== ROW', label, ts(), '| PREDICTED reds %d:' % len(predicted), sorted(x.split(' :: ')[0].split('/')[-1][:6] + ' ' + x.split(' — ')[-1][:60] for x in predicted))
    assert porc('head') == [], porc('head')
    try:
        for f, old, new, markers in edits: edit(T['head'] + '/' + f, old, new, markers)
    except AssertionError as e:
        P('   ROW ABORTED (anchor):', e); [restore('head', f, pristine[f]) for f in {e_[0] for e_ in edits} if sha(T['head'] + '/' + f) != pristine[f]]; summary.append((label, 'ABORTED', str(e))); continue
    trc, ks = tsc('head')
    r = vitest('t_' + label, 'head', 'gw')
    reds = set(k for k, v in r['cells'].items() if v['status'] != 'passed') if r else {'NO JSON'}
    den = (r['files'], r['tests']) if r else None
    kinds = sorted({v['msg'].split('\n')[0][:50] for k, v in r['cells'].items() if v['status'] != 'passed'}) if r else []
    ok = den == (DEN[0], DEN[1] + added)
    P('   tsc -p . rc', trc, '| including ks864 error lines', len(ks), [l.split(': error ')[1][:60] for l in ks][:4])
    P('   denominator', den, 'asserted', ok, '| failed', r['failed'], 'pending', r['pending'], '| reds', len(reds), '| MATCHES PREDICTION', reds == predicted, '| kinds', kinds)
    for f in sorted({e_[0] for e_ in edits}): restore('head', f, pristine[f])
    summary.append(dict(row=label, tsc_rc=trc, incl_ks864_errs=len(ks), den=den, den_ok=ok, failed=r['failed'], pending=r['pending'], reds=sorted(reds), predicted=sorted(predicted), match=reds == predicted))
r = vitest('t_T0_after', 'head', 'gw'); summary.append(dict(row='T0_after', den=(r['files'], r['tests']), failed=r['failed'], pending=r['pending']))
P('== RED-BEFORE-GREEN: ks864c alone on head with system-status.ts = the pre-#1007 blob 5b39da2ee (93629700c); PREDICTED 3 staging reds, 3 development green')
blob = subprocess.run(['git', '-C', T['head'], 'show', '5b39da2eeeea2473f607775cad62028ec1d3557c'], capture_output=True).stdout
assert len(blob) > 1000; open(T['head'] + '/' + SS, 'wb').write(blob); P('   landed pre-#1007 blob, sha', sha(T['head'] + '/' + SS)[:12])
r = vitest('rbg_ks864c_on_pre1007', 'head', 'gw', files=['src/__tests__/ks864c-portal-env-vars.test.ts'])
P('   reds', sorted(k.split(' — ')[-1] for k, v in r['cells'].items() if v['status'] != 'passed'))
restore('head', SS, pristine[SS])
summary.append(dict(row='RBG_ks864c_pre1007', den=(r['files'], r['tests']), failed=r['failed'], pending=r['pending'], reds=sorted(k for k, v in r['cells'].items() if v['status'] != 'passed')))
P('porcelain head (farm lines excluded)', porc('head'))
json.dump(summary, open(GS + ('/drafter_run_summary.only.json' if ONLY else '/drafter_run_summary.json'), 'w'), indent=1, ensure_ascii=False)
P('drafter_run end', ts())
