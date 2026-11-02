import json,sys
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate148-ks1868-pr1970'
for l in open(W+'/logs/probe.jsonl'):
    d=json.loads(l); c=d['cell']; k=f"{d['variant']:4} {c:16} {d['val']:13} {d.get('env','?'):10}"
    if 'harnessError' in d: print(k,'HARNESS',d); continue
    ex=f"unh={len(d['unhandled'])}{d['unhandled'][:1]} unc={d['uncaught']}"
    if c=='bf': r=f"login={d['login']['status']} {d['login']['body'][:40]}"
    elif c=='bf_arm': r=f"12fails={d['twelveFailedLogins']} bfkeys={d['bfKeysAfter']} planted={d['plantedLockout']} planted+redisErr={d['plantedLockoutRedisOrdinaryError']} planted+revoked={d['plantedLockoutRedisRevokedProxy']}"
    elif c.startswith('rl'): r="3req="+str([x['status'] for x in d['three']])+f" remaining={[x['rl'] for x in d['three']]} reached={d['handlerReached']} redisCtr={d['redisCounter']}"
    elif c=='audit': r=f"post={d['post']['status']} post2={d['post2']['status']} q={d['queryCalls']}"
    logs=[x for x in d['logs'] if 'Unhandled error' not in x or True]
    print(k,r,ex); [print('      ',x[:230]) for x in logs[:4]]
