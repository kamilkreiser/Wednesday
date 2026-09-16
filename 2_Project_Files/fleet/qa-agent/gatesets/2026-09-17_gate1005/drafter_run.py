#!/usr/bin/env python3
"""drafter_run.py — #1005: the recording probe at head and base, then tamper rows on head (whole suite, porcelain-asserted, then the
probe SOLO under the same tamper). Anchors counted by str.count; restore by git checkout asserted by sha256. Predictions are fixed HERE,
before the run, and compared after. Probe files are moved OUT of the tree by rename (never rm)."""
import sys, os, json, shutil
sys.path.insert(0,'/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1005')
from drafterlib import *
V=GWR+'/src/routes/verification.ts'
PROBE_SRC=GS+'/qa1005-drafter-probe.test.ts'; PROBE_REL=GWR+'/src/__tests__/qa1005-drafter-probe.test.ts'
Q=W+'/_quarantine'; os.makedirs(Q, exist_ok=True)
def probe(label, tree):
    dst=T[tree]+'/'+PROBE_REL; shutil.copyfile(PROBE_SRC, dst); out=W+'/probe_%s.jsonl'%label
    open(out,'w').close()
    r=vitest('probe_'+label, tree, files=['src/__tests__/qa1005-drafter-probe.test.ts'], env_extra={'QA_OUT':out}, save=False)
    os.rename(dst, Q+'/qa1005-drafter-probe.%s.test.ts'%label)
    rows={}
    for l in open(out):
        d=json.loads(l); rows[d['id']]=d
    json.dump({'run':{k:r[k] for k in ('files','tests','passed','failed')} if r else None,'rows':rows}, open(GS+'/probe_%s_rows.json'%label,'w'), indent=1)
    return rows
def fmt(rows): return {k:(v['confidence'], v['anchorStoreHits'], v['source']) for k,v in rows.items()}
P('drafter_run start', ts())
base_rows=probe('base','base'); head_rows=probe('head','head')
P('== PROBE head vs base (confidence, anchorStoreHits, source)')
for k in head_rows:
    b=base_rows.get(k,{}); h=head_rows[k]
    P('  %-4s tier %d | base %-15s hits %s | head %-15s hits %s source %-9s | %s'%(k,h['tier'],b.get('confidence'),b.get('anchorStoreHits'),h['confidence'],h['anchorStoreHits'],h['source'],'CHANGED' if b.get('confidence')!=h['confidence'] else 'same'))
pv=sha(T['head']+'/'+V); P('verification.ts pristine sha', pv[:16])
PL="      (persistedStatus === 'confirmed' || (persistedStatus == null && (doc as any)._source !== 'anchor_store')), // KS-1073: carve-out tier-1 only; anchor-store rows are never statusless\n"
ROWS=[
 ('S1_fix_reverted', PL, "      (persistedStatus === 'confirmed' || persistedStatus == null),\n", [("_source !== 'anchor_store')),",0)],
  'ks1073 🔴x2 only', {'A1':'on-chain','A4':'on-chain','A10':'on-chain'}),
 ('S2_carveout_deleted', PL, "      (persistedStatus === 'confirmed'),\n", [("persistedStatus == null && (doc as any)._source",0)],
  'ks1073 control + ks1057 REGRESSION', {'B1':'off-chain-only','B2':'off-chain-only','B8':'off-chain-only','B9':'off-chain-only','B10':'off-chain-only'}),
 ('GA_predicate_inverted', "(doc as any)._source !== 'anchor_store'", "(doc as any)._source === 'anchor_store'", [("(doc as any)._source === 'anchor_store'",1)],
  'ks1073 🔴x2 + ks1073 control + ks1057 REGRESSION (+ any other tier-1 statusless on-chain control)', {'A1':'on-chain','B1':'off-chain-only','B6':'on-chain'}),
 ('GL_predicate_loosened_truthy', "(doc as any)._source !== 'anchor_store'", "!(doc as any)._source", [("!(doc as any)._source",1)],
  '0 reds (equivalent for every shape the suite drives)', {'B8':'off-chain-only','B11':'off-chain-only'}),
 ('GB_tier1_mistagged', "resolve(data && data.id ? data : null);", "resolve(data && data.id ? { ...data, _source: 'anchor_store' } : null);", [("_source: 'anchor_store' } : null",1)],
  'every tier-1 statusless on-chain cell: ks1073 control + ks1057 REGRESSION at least', {'B1':'off-chain-only','B2':'off-chain-only','B5':'on-chain'}),
 ('GM_marker_deleted', "                _source: 'anchor_store',  // marker for downstream telemetry\n", "", [("marker for downstream telemetry",0)],
  'ks1073 🔴x2 only', {'A1':'on-chain','A4':'on-chain','A10':'on-chain'}),
 ('GC_aimed_at_control_tier2_confirmed_excluded', "(persistedStatus === 'confirmed' ||", "((persistedStatus === 'confirmed' && (doc as any)._source !== 'anchor_store') ||", [("((persistedStatus === 'confirmed' && (doc",1)],
  'ks1073 control + every tier-2 confirmed on-chain cell (ks1057/ks1070/ks1071/ks1130 twins)', {'A6':'off-chain-only','B5':'on-chain'}),
 ('T6_inert_comment', "    const persistedAnchored = Boolean(\n", "    // qa inert comment\n    const persistedAnchored = Boolean(\n", [("// qa inert comment",1)],
  '0 reds', {}),
]
summary=[]
for label, old, new, markers, pred_suite, pred_probe in ROWS:
    P('== ROW', label, ts(), '| PREDICTED suite:', pred_suite, '| PREDICTED probe:', pred_probe)
    assert porcelain('head')==['?? Blockchain/Dev/packages/shared/node_modules', '?? Blockchain/Dev/services/api-gateway/node_modules', '?? node_modules'], porcelain('head')
    try:
        edit(T['head']+'/'+V, old, new, markers)
    except AssertionError as e:
        P('   ROW ABORTED (anchor):', e); summary.append((label,'ABORTED',str(e))); continue
    r=vitest('t_'+label,'head')
    reds=sorted(k for k,v in r['cells'].items() if v['status']!='passed') if r else ['NO JSON']
    rows=probe('t_'+label,'head')
    flips={k:(head_rows[k]['confidence'],rows[k]['confidence']) for k in rows if rows[k]['confidence']!=head_rows[k]['confidence']}
    miss={k:(want,rows.get(k,{}).get('confidence')) for k,want in pred_probe.items() if rows.get(k,{}).get('confidence')!=want}
    P('   suite reds', len(reds), 'denominator', r and (r['files'], r['tests']))
    P('   probe flips vs head T0', flips, '| probe prediction misses', miss)
    restore('head', V, pv)
    summary.append((label, len(reds), reds, flips, miss))
r=vitest('t_T0_after','head'); summary.append(('T0_after', r['failed']))
json.dump(summary, open(GS+'/drafter_run_summary.json','w'), indent=1, ensure_ascii=False)
P('drafter_run end', ts())
