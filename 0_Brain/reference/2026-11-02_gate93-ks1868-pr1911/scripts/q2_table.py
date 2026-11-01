import json,re
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911/logs/'
for p in ['q2_register','q2_login']:
    R={v:{json.loads(l)['case']:json.loads(l) for l in open(G+f'{p}_{v}.jsonl')} for v in ['base','head']}
    for k in R['base']:
        b,h=R['base'][k],R['head'][k]
        norm=lambda s: re.sub(r'"(createdAt|updatedAt|id|expiresAt|sessionId)":"[^"]*"','"\\1":"<x>"',s)
        print(p,k,'status',b['status'],h['status'],'| body equal',norm(b['body'])==norm(h['body']),'| set-cookie equal',b['setCookie']==h['setCookie'],'| unhandled',b['unhandled'],h['unhandled'],'| lines',b['lines'],h['lines'],'| body[:90]',h['body'][:90])
