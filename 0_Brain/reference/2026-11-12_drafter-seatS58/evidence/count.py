import json,collections,sys
d=json.load(open(sys.argv[1]))
c=collections.Counter(i['state']['name'] for i in d); print(len(d),dict(c))
print('started-type',sum(1 for i in d if i['state']['type']=='started'))
print('open',sum(1 for i in d if i['state']['type'] in('backlog','unstarted','started')))
b=collections.Counter(i['priority'] for i in d if i['state']['name']=='Backlog'); print('backlog prio',dict(b))
a=collections.Counter((i['assignee'] or {}).get('email','UNASSIGNED') for i in d); print(dict(a))
for who in ('stuart','peter'):
    ks=sorted((i['identifier'],i['state']['name']) for i in d if i['assignee'] and who in i['assignee']['email'].lower()); print(who,len(ks),ks)
for k in ['KS-2166','KS-2167','KS-2168','KS-1882','KS-663','KS-1535','KS-1376','KS-2064','KS-636','KS-1175','KS-579','KS-1845']:
    r=[i for i in d if i['identifier']==k]; print(k, r and (r[0]['state']['name'],r[0]['priority'],r[0]['updatedAt'],(r[0]['project'] or {}).get('name'),len(r[0]['comments']['nodes']),(r[0]['assignee'] or {}).get('email')) )
print('max key',max(int(i['identifier'][3:]) for i in d))
print('todo',sorted(i['identifier'] for i in d if i['state']['name']=='Todo'))
