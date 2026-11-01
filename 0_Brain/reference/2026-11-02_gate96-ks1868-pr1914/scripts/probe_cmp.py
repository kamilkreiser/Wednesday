import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate96-ks1868-pr1914/logs/'
b=json.load(open(W+'probe_base.json')); h=json.load(open(W+'probe_head.json'))
print('cells',len(b),len(h))
same=0; diffs=[]
for k in b:
    if json.dumps(b[k],sort_keys=True)==json.dumps(h[k],sort_keys=True): same+=1
    else: diffs.append(k)
print('byte-identical cells',same,'differing',len(diffs))
# class summary
unread=('revokedProxy','getterThrowsError','nullProtoObject')
print('ZOD-MSG-THROWS', {k:(b[k]['status'],h[k]['status']) for k in b if 'zodErrorMessageGetterThrows' in k})
bad=[k for k in diffs if k.split('/')[1] not in unread]
print('differing cells that are NOT unreadable values:',bad)
for k in diffs[:100]:
    print(k,'| base:',b[k]['status'],b[k]['unhandled'],[l[1] for l in b[k]['logs']],'| head:',h[k]['status'],h[k]['text'][:90],[l[1] for l in h[k]['logs']],h[k]['unhandled'])
# ordinary cell sample
for k in ['overview/realSchemaZodError','overview/ordinaryError','activity/realSchemaZodError','post_reports/realSchemaZodError','realtime/ordinaryError','overview/zodErrorFromService']:
    print(k,h[k]['status'],h[k]['text'][:260],h[k]['logs'])
# unreadable head cells all constant 500?
const={}
for k in h:
    if k.split('/')[1] in unread:
        const.setdefault((h[k]['status'],h[k]['logs'][0][1]['error'] if h[k]['logs'] else None,h[k]['unhandled']),[]).append(k)
for c,v in const.items(): print('head unreadable ->',c,len(v))
cb={}
for k in b:
    if k.split('/')[1] in unread: cb.setdefault((b[k]['status'],len(b[k]['logs']),b[k]['unhandled']),[]).append(k)
for c,v in cb.items(): print('base unreadable ->',c,len(v))
