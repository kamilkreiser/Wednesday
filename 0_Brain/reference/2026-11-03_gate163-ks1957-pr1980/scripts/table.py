import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980/logs/probe/'
vers=sys.argv[1:] or ['base','head']
R={v:json.load(open(W+v+'.json')) for v in vers}
for v in vers: print(v, R[v]['bootLine'], R[v].get('driverError'))
rows=R[vers[0]]['rows']
print('i  route   | '+' | '.join(f'{v}: st code aw(mr/rr/ref) writes stmts' for v in vers)+' | label')
for k,x in enumerate(rows):
    parts=[]
    for v in vers:
        y=R[v]['rows'][k]; assert y['label']==x['label']
        parts.append(f"{y['status']!s:4} {str(y.get('code','-')):12} {y['awards']}({y['milestoneAwards']}/{y['referralRewards']}/{'Q' if y['pendingReferral']!='PENDING' else '-'}) w={y['writeRows']:<2} s={y['appStatements']}")
    print(f"{x['i']:2} {x['route']:7} | "+' | '.join(parts)+f" | {x['label']}")
