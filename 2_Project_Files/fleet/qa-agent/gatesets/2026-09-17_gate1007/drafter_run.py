#!/usr/bin/env python3
"""drafter_run.py — #1007: whole api-gateway suite at base / head / merged, then tamper rows on head (anchor count asserted = 1, markers,
WHOLE suite with the denominator asserted 44/388, restore by git checkout asserted sha256-identical), T0-after. Predictions are FIXED here,
before the run, and compared after. For row G2 (portal env var ignored) the parity probe is also run under the tamper and compared with
the untampered head probe. Probe files are moved out by rename (never rm)."""
import sys, os, json, shutil
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007')
from drafterlib import *
SS=GWR+'/src/routes/system-status.ts'
A='__tests__/ks864a-dead-estate-helper.test.ts :: KS-864 A — dead Azure estate pointers removed from runtime source '
B='__tests__/ks864b-dead-estate-portals.test.ts :: KS-864 — dead-estate portal URLs removed from runtime source '
A1=A+'🔴 KS-864 A — api-gateway falls back to its localhost default under NODE_ENV=staging when its env var is unset'
A2=A+'🔴 KS-864 A — no served URL names the internal dead estate'
AC=A+'KS-864 A control — an explicit env var still wins'
B1=B+'🔴 KS-864 B — the issuer portal falls back to its compose default under NODE_ENV=staging when its env var is unset'
B2=B+'🔴 KS-864 B — no portal URL names the dead estate'
BC=B+'KS-864 B control — an explicit env var still wins for a helper-built service'
P('drafter_run start', ts())
S={}
for t in ('base','head','merged'):
    assert porcelain(t)==FARM, porcelain(t)
    S[t]=vitest('suite_'+t, t)
P('   ks864 cells at head:', {k.split(' :: ')[1][:60]:v['status'] for k,v in S['head']['cells'].items() if 'ks864' in k})
DEN=(S['head']['files'], S['head']['tests']); P('denominator asserted for tamper rows:', DEN)
PL="  // KS-864: the Azure staging estate is decommissioned — URLs come from the env var above or the localhost default.\n"
ROWS=[
 ('SA_partA_staging_branch_restored', PL, "  if (process.env.NODE_ENV === 'staging' && _azureServiceName) {\n    return `https://${_azureServiceName}.internal.ashypond-b460d1a1.westeurope.azurecontainerapps.io`;\n  }\n", [('.internal.ashypond-b460d1a1',1)], {A1,A2}),
 ('SB_issuer_staging_ternary_restored', "    url: process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80',\n", "    url: process.env.NODE_ENV === 'staging'\n      ? 'https://secuura-staging-issuer.ashypond-b460d1a1.westeurope.azurecontainerapps.io'\n      : (process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80'),\n", [('secuura-staging-issuer',1)], {B1,B2}),
 ('SC_helper_ignores_env_var', "  if (envUrl) return envUrl;\n", "  if (envUrl && false) return envUrl;\n", [('envUrl && false',1)], {AC,BC}),
 ('G1_aimed_at_B_control_gateway_reads_wrong_var', "getServiceUrl('API_GATEWAY_URL', 8080, 'secuura-staging-api')", "getServiceUrl('API_GATEWAY_URL_QA', 8080, 'secuura-staging-api')", [('API_GATEWAY_URL_QA',1)], {BC}),
 ('G2_portal_ignores_its_env_var', "    url: process.env.ISSUER_PORTAL_URL || 'http://issuer-frontend:80',\n", "    url: 'http://issuer-frontend:80',\n", [('ISSUER_PORTAL_URL',0)], set()),
 ('G3_verifier_staging_ternary_restored', "    url: process.env.VERIFIER_PORTAL_URL || 'http://verifier-frontend:80',\n", "    url: process.env.NODE_ENV === 'staging'\n      ? 'https://secuura-staging-verifier.ashypond-b460d1a1.westeurope.azurecontainerapps.io'\n      : (process.env.VERIFIER_PORTAL_URL || 'http://verifier-frontend:80'),\n", [('secuura-staging-verifier',1)], {B2}),
 ('G4_hint_removed_from_response', "          `az containerapp revision restart --name secuura-staging-${service.name} --resource-group secuura-staging-rg`,\n", "", [('az containerapp',0)], set()),
 ('T6_inert_comment', "// Helper to determine environment-appropriate URL\n", "// Helper to determine environment-appropriate URL\n// qa inert comment\n", [('qa inert comment',1)], set()),
]
pristine=sha(T['head']+'/'+SS); P('system-status.ts pristine sha', pristine[:16])
summary=[]
PROBE_SRC=GS+'/qa1007-drafter-parity.test.ts'; PROBE_REL=GWR+'/src/__tests__/qa1007-drafter-parity.test.ts'
for label, old, new, markers, predicted in ROWS:
    P('== ROW', label, ts(), '| PREDICTED reds:', sorted(x.split(' :: ')[0].split('/')[-1][:6]+' '+x.split(' — ')[-1][:50] for x in predicted) or '0')
    assert porcelain('head')==FARM, porcelain('head')
    try: edit(T['head']+'/'+SS, old, new, markers)
    except AssertionError as e: P('   ROW ABORTED (anchor):', e); summary.append((label,'ABORTED',str(e))); continue
    r=vitest('t_'+label,'head')
    reds=set(k for k,v in r['cells'].items() if v['status']!='passed') if r else {'NO JSON'}
    den=(r['files'], r['tests']) if r else None
    msgs=sorted({v['msg'].split('\n')[0][:60] for k,v in r['cells'].items() if v['status']!='passed'}) if r else []
    P('   denominator', den, 'asserted', den==DEN, '| reds', len(reds), '| matches prediction', reds==predicted, '| failure kinds', msgs)
    if label.startswith('G2'):
        dst=T['head']+'/'+PROBE_REL; shutil.copyfile(PROBE_SRC, dst); out=W+'/parity_t_G2.jsonl'; open(out,'w').close()
        vitest('parity_t_G2','head',files=['src/__tests__/qa1007-drafter-parity.test.ts'],env_extra={'QA_OUT':out},save=False)
        os.rename(dst, W+'/_quarantine/qa1007-drafter-parity.t_G2.test.ts')
        g2={json.loads(l)['id']:json.loads(l) for l in open(out)}; h0={json.loads(l)['id']:json.loads(l) for l in open(W+'/parity_head.jsonl')}
        diff=sorted(i for i in g2 if g2[i]['statusHash']!=h0[i]['statusHash'])
        P('   G2 probe: cells whose /system/status differs from untampered head: %d of %d -> %s'%(len(diff), len(g2), diff))
    restore('head', SS, pristine)
    summary.append((label, den, sorted(reds), reds==predicted))
r=vitest('t_T0_after','head'); summary.append(('T0_after', (r['files'], r['tests']), r['failed']))
P('porcelain head', porcelain('head'))
json.dump(summary, open(GS+'/drafter_run_summary.json','w'), indent=1, ensure_ascii=False)
P('drafter_run end', ts())
