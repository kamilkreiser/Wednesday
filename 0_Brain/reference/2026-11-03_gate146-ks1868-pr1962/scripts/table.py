import json, glob, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962'
def inst(s):
    if not s: return 'n/a'
    return ' '.join(f"{i['id']}:{i['status'][:4]}{'/esc' if i['escalated_at'] else ''}" for i in s['instances'])
def short(lines):
    out = []
    for l in lines:
        if 'boot work failed' in l: out.append('HOOK-FAILED:' + l.split('"error":')[-1][:60])
        elif 'approvalWorkflowService' in l or 'delegationService' in l: out.append(l.replace('[approvalWorkflowService] ', 'AWS ')[:90])
        elif 'TypeError' in l or 'Unhandled' in l or 'unhandled' in l: out.append(l[:90])
    return ' | '.join(out[:4])
rows = []
for f in sorted(glob.glob(W + '/logs/probe/*.result.json')):
    r = json.load(open(f)); tag = r['tag']
    if tag.startswith('head__boot_probe__none') and False: pass
    ver, scen, kind = tag.split('__')
    if scen.startswith('boot'):
        rows.append(f"{ver:8} {scen:13} {kind:15} boot={r['bootDone']} conn={r['connected']} delegProbe={r['delegationProbeRan']} upserts={r['wfUpsertAttempts']} served={len(r['workflowsServed']) if isinstance(r['workflowsServed'], list) else r['workflowsServed']} health={r['health'].get('status')} exit={r['finalExit']} :: {short(r['lines'])}")
    else:
        p1 = r.get('post1', {}); p2 = r.get('post2', {})
        fmt = lambda p: (str(p.get('status')) + ' ' + (json.dumps(p['body']['data'] if isinstance(p.get('body'), dict) and 'data' in p['body'] else p.get('body'))[:60] if 'status' in p else p.get('error', 'not sent')))
        rows.append(f"{ver:8} {scen:13} {kind:15} POST1={fmt(p1)} exitAfterPOST1={r.get('exitedAfterPost1')} health1={r.get('healthAfterPost1', {}).get('status', r.get('healthAfterPost1', {}).get('error'))} after1=[{inst(r.get('storeAfterPost1'))}] POST2={fmt(p2) if p2 else 'not sent'} after2=[{inst(r.get('storeAfterPost2'))}] :: {short(r['lines'])}")
open(W + '/logs/probe_table.log', 'w').write('\n'.join(rows) + '\n'); print('\n'.join(rows))
