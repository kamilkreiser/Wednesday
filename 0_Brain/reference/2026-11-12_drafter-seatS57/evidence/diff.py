import json
a={i['identifier']:i for i in json.load(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_drafter-seatS56/evidence/board_all_1111.json'))}
b={i['identifier']:i for i in json.load(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/evidence/board_all_1112.json'))}
print(len(a),len(b))
print('gone',sorted(set(a)-set(b)),'new',sorted(set(b)-set(a)))
for k in sorted(set(a)&set(b),key=lambda x:int(x[3:])):
    x,y=a[k],b[k]
    ch=[]
    if x['state']['name']!=y['state']['name']: ch.append(f"state {x['state']['name']}->{y['state']['name']}")
    if x['priority']!=y['priority']: ch.append(f"prio {x['priority']}->{y['priority']}")
    if (x['assignee'] or {}).get('email')!=(y['assignee'] or {}).get('email'): ch.append("assignee")
    if ch: print(k,'; '.join(ch),y['updatedAt'])
