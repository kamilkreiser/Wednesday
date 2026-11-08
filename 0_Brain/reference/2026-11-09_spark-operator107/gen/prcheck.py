import json,sys
d=json.load(open(sys.argv[1]))
keys=['services/originate/src/routes/documents.ts','trustHeaders','AGENT-DOCUMENT-OPERATION-RULES','sdk/javascript','transferAccess.ts','ks2081-transfer','ks1448-notification','ks1536-inline-role','anchoring/src/__tests__','services/transfer/','api-gateway/src/__tests__/ks1448']
print(len(d),'PRs',sum(len(v['files']) for v in d.values()),'files')
ctl=[(n,f) for n,v in d.items() for f in v['files'] if 'services/originate' in f]
print('CONTROL services/originate entries (positive control; must be >0):',len(ctl))
for k in keys: print('HITS',k,[(n,f.split('/')[-1]) for n,v in d.items() for f in v['files'] if k in f])
