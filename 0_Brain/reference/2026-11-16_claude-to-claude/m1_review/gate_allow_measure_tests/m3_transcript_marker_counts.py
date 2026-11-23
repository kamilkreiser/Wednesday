#!/usr/bin/env python3
"""QA-ALLOW-MEASURE: count each M3 marker per transcript record type. usage: <transcript.jsonl> <suffix> <case>"""
import json,sys
t,sfx,c=sys.argv[1:4]; cnt={}
for l in open(t):
    try: e=json.loads(l)
    except ValueError: continue
    ty=e.get('type')
    if ty=='attachment': ty='attachment:'+str((e.get('attachment') or {}).get('type'))
    for m in ('PDR','SYS','TSQ','ERR','ADC'):
        if 'MK3'+m+sfx in l: cnt.setdefault(m,{}); cnt[m][ty]=cnt[m].get(ty,0)+1
print(c, {m:cnt.get(m,{}) for m in ('PDR','SYS','TSQ','ERR','ADC')})
