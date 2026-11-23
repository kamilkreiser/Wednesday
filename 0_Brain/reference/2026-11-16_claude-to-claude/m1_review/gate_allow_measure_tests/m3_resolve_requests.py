#!/usr/bin/env python3
"""QA-ALLOW-MEASURE: resolve every api-request 'tail' hash in a Claude Code transcript to the record it names
(hash = sha256 of the message JSON, compact, sorted keys, ensure_ascii False; recipe learned from a blob's own hash),
and say which M3 markers each referenced record holds. Prints counts and record types only, never content.
usage: python3 -I m3_resolve_requests.py <transcript.jsonl> <case-name>"""
import json,sys,hashlib
L=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]
H=lambda m: hashlib.sha256(json.dumps(m,separators=(',',':'),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
idx={}
for i,e in enumerate(L):
    if isinstance(e.get('message'),dict):
        idx.setdefault(H(e['message']),[]).append(i)
        m=e['message']; idx.setdefault(H({'role':m.get('role'),'content':m.get('content')}),[]).append(i)
b=next(e for e in L if e.get('type')=='api-request-blob'); print('recipe check (blob hash reproduces):', H(b['message'])==b['hash'])
print('==',sys.argv[2])
for i,e in enumerate(L):
    if e.get('type')=='api-request':
        res=[]
        for h in e['tail']:
            j=idx.get(h)
            if j: r=L[j[0]]; s=json.dumps(r); res.append('rec%d:%s%s'%(j[0],r['type'],''.join(' '+m for m in ('SYS','ADC','PDR','TSQ','ERR') if 'MK3'+m in s)))
            else: res.append('UNRESOLVED')
        print(' req@%d'%i, res)
