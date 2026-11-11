import re,json,os,sys
D='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57'
t=open(D+'/brief_S57_body.md').read()
# keys named in the brief, excluding the PROVENANCE section itself
body=t.split('\nPROVENANCE:')[0]
keys=sorted(set(int(k) for k in re.findall(r'KS-(\d+)',body)))
# also bare-number lists like "KS-1090, 1000, 1497" and "KS-61, 101, 135"
extra=set()
for m in re.finditer(r'KS-\d+(?:, (?:KS-)?\d+)+',body):
    for n in re.findall(r'(?:KS-)?(\d+)',m.group(0)): extra.add(int(n))
for m in re.finditer(r'\((?:KS-)\d+(?:, \d+)+',body):
    pass
print(len(keys),'explicit keys;',len(extra-set(keys)),'bare-number extras:',sorted(extra-set(keys)))
json.dump({'keys':keys,'extra':sorted(extra-set(keys))},open(D+'/evidence/keys.json','w'))
cen={i['identifier']:i for i in json.load(open(D+'/evidence/board_all_1112.json'))}
miss=[k for k in keys+sorted(extra-set(keys)) if f'KS-{k}' not in cen]
print('not in census:',miss)
