import json,collections,sys
d=json.load(open(sys.argv[1]))
c=collections.Counter(i['state']['name'] for i in d); print(len(d),dict(c))
print('started-type',sum(1 for i in d if i['state']['type']=='started'))
print('open',sum(1 for i in d if i['state']['type'] in('backlog','unstarted','started')))
print('types',dict(collections.Counter(i['state']['type'] for i in d)))
b=collections.Counter(i['priority'] for i in d if i['state']['name']=='Backlog'); print('backlog prio',dict(b))
a=collections.Counter((i['assignee'] or {}).get('email','UNASSIGNED') for i in d); print(dict(a))
for who in ('stuart','peter'):
    ks=sorted((i['identifier'],i['state']['name']) for i in d if i['assignee'] and who in i['assignee']['email'].lower())
    print(who,len(ks),ks)
for k in ['KS-1845','KS-1509','KS-2164','KS-2055','KS-1176','KS-663','KS-1175','KS-491','KS-135','KS-2015','KS-1954','KS-1927','KS-1928','KS-2163','KS-2158','KS-2156','KS-2149','KS-2085']:
    r=[i for i in d if i['identifier']==k]; print(k, r and (r[0]['state']['name'],r[0]['priority'],r[0]['updatedAt']) )
mx=max(int(i['identifier'][3:]) for i in d); print('max key',mx)
t=sorted(i['identifier'] for i in d if i['state']['name']=='Todo'); print('todo',len(t),t)
