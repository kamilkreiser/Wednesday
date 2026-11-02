import json,re,sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955/logs/'
tamper=sys.argv[1] if len(sys.argv)>1 else None
def load(p): return [json.loads(l) for l in open(G+p)]
fails=[];checks=0
def ck(c,m):
    global checks; checks+=1
    if not c: fails.append(m)
A={s:load(f'probe_anch_{s}.jsonl') for s in ('base','head')}
O={(s,e):load(f'probe_orig_{s}_{e}.jsonl') for s in ('base','head') for e in ('development','production')}
if tamper=='chain_verified_unreadable_only':  # head: hostile kind verified while ordinary is not (miss cell)
    for r in A['head']:
        if r['cell']=='hash_chain_miss' and r['kind']=='msgRevokedProxy': r['res']={'status':200,'body':'{"verified":true,"source":"chain"}'}
if tamper=='db_verified':
    for r in A['head']:
        if r['cell']=='hash_nochain' and r['kind']=='msgBigInt': r['res']={'status':200,'body':'{"verified":true,"source":"db"}'}
if tamper=='orig_hang':
    for r in O[('head','production')]:
        if r['cell']=='get_lookup_throws' and r['kind']=='msgSymbol': r['res']={'status':'NO_RESPONSE'}
def body(r):
    try: return json.loads((r.get('res') or {}).get('body') or 'null')
    except Exception: return None
def sh(b):
    if isinstance(b,dict): return {k:('<H>' if k in('hash','contentHash','txHash','explorerUrl','id','confirmedAt','timestamp') else sh(v)) for k,v in b.items()}
    if isinstance(b,list): return [sh(x) for x in b]
    if isinstance(b,str): return re.sub(r'[0-9a-f]{64}','<H>',b)
    return b
def verified(b):
    if not isinstance(b,dict): return False
    if b.get('verified') is True: return True
    d=b.get('data')
    return isinstance(d,dict) and d.get('verified') is True
# anchoring
for s in ('base','head'):
    H={(r['cell'],r['kind']):r for r in A[s] if r['cell']!='network'}
    net=[r for r in A[s] if r['cell']=='network'][0]; ck(net['outbound']==[],f'anch {s} outbound')
    for (c,k),r in H.items():
        ck(len(r['writes'])==0 and r['submits']==0,f'anch {s} {c} {k} write/submit')
        if k.startswith('none'): continue
        o=H[(c,'ordinary')]
        b=body(r)
        # Q2: a verified answer from a failed lookup only where the ordinary Error gets the same, and only from the chain
        if verified(b): ck(verified(body(o)) and b.get('source')=='chain' and c=='hash_chain_hit',f'anch {s} {c} {k} verified where ordinary is not / not chain')
        if s=='head':
            ck(r['res'].get('status')==o['res'].get('status') and sh(b)==sh(body(o)),f'anch head {c} {k} response != ordinary ({r["res"].get("status")})')
            ck(r['unhandled']==0 and r['uncaught']==0,f'anch head {c} {k} unhandled')
            ck(len([l for l in r['logs'] if 'lookup' in l])==1,f'anch head {c} {k} not exactly one lookup log line')
            ck(r['providerCalls']==o['providerCalls'],f'anch head {c} {k} chain calls != ordinary')
for (c,k),r in {(r['cell'],r['kind']):r for r in A['head'] if r['cell']!='network'}.items():
    if c.startswith('anon_control'):
        ck((c.endswith('auth') and r['res']['status']==401) or (c.endswith('db_hit') and r['res']['status']==200),f'anon control {c}')
# originate
for (s,e),recs in O.items():
    H={(r['cell'],r['kind']):r for r in recs if r['cell']!='network'}
    net=[r for r in recs if r['cell']=='network'][0]; ck(net['outbound']==[],f'orig {s} {e} outbound')
    for (c,k),r in H.items():
        ck(r.get('writes',0)==0,f'orig {s} {e} {c} {k} writes')
        if c=='get_control_found': ck(r['res']['status']==200,'orig found control'); continue
        if c=='get_control_absent': ck(r['res']['status']==404,'orig absent control'); continue
        if c=='get_lookup_throws':
            ck(r['res'].get('status')!=404 and not verified(body(r)) and r['res'].get('status')!=200,f'orig {s} {e} {k} positive/absent answer to a fault')
        if s=='head' and k!='ordinary':
            o=H[(c,'ordinary')]
            if c=='get_lookup_throws': ck(r['res'].get('status')==o['res'].get('status') and body(r)==body(o),f'orig head {e} {c} {k} != ordinary')
            if c=='dbready_direct': ck(r['out']==o['out'],f'orig head {e} dbready {k} != ordinary {r["out"]}')
            if c=='dbready_boot': ck(r['out']==o['out'],f'orig head {e} boot {k} != ordinary')
            ck(r.get('unhandled',0)==0,f'orig head {e} {c} {k} unhandled')
            # every captured line carries a string error
            for L in r['logs']:
                line=L.get('line') or ''
                if 'Failed to fetch anchor' in line or 'Failed to get anchor' in line or 'database connection FAILED' in line:
                    ck(re.search(r'"error":"',line) is not None,f'orig head {e} {c} {k} line without string error: {line[:80]}')
print(f'checks {checks} fails {len(fails)}'); [print(' FAIL',f) for f in fails[:30]]
sys.exit(1 if fails else 0)
