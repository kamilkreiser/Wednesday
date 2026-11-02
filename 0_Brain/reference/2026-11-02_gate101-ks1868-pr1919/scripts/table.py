import json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate101-ks1868-pr1919/logs/'
def load(f): return [json.loads(l) for l in open(W+f)]
out=[]
for v in ('base','head'):
    out.append('## '+v)
    for r in load(f'probe_{v}.jsonl'):
        lg=[ (l[0],l[1],l[2:]) for l in r['logs']]
        if r['probe']=='A': out.append(f"A {r['route']} {r['kind']}: status={r['status']} body={r['body'][:60]} rows={r['rows']} unhandled={r.get('unhandled')} logs={lg}")
        else: out.append(f"C {r['route']} {r['kind']}: status={r['status']} secretInLog={r['secretInLog']} unhandled={r['unhandled']} logs={lg}")
    for r in load(f'probe2_{v}.jsonl'):
        if r['probe']=='B': out.append(f"B {r['kind']}: out={r['out']} sent={r['sent']} warnHasRecipient={r['warnHasRecipient']} warnHasTitle={r['warnHasTitle']} allHasTitle={r['allHasTitle']} allHasRecipient={r['allHasRecipient']} logs={r['logs']}")
        else: out.append(f"D {r['repo']} {r['kind']}: ctor={r['thrownCtor']} isError={r['thrownIsError']} indexMsg={r['indexCatchMessage']} logs={r['logs']}")
open(W+'probe_table.log','w').write('\n'.join(out)+'\n')
