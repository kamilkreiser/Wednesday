import json,sys
t={x['identifier']:x for x in json.load(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_spark-operator101/tickets.json'))}
for k in sys.argv[1:]:
    x=t['KS-'+k]; print('#####',x['identifier'],x['title']); print(x['description'])
