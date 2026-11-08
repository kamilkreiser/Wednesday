import json,sys
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator107/'
d={x['identifier']:x for x in json.load(open(O+'open_tickets.json'))}
for k in sys.argv[1:]:
    x=d['KS-'+k]
    print('#####',x['identifier'],x['title'],x['state']['name'],x['updatedAt'])
    print(x['description'])
    for c in sorted(x['comments']['nodes'],key=lambda c:c['createdAt'],reverse=True):
        print('--- comment',c['createdAt'],(c['user'] or {}).get('name'));print(c['body'])
