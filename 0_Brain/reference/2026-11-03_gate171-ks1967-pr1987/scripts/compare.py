import json, sys, collections
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate171-ks1967-pr1987'
base = json.load(open(sys.argv[1])); head = json.load(open(sys.argv[2]))
DOWN = {'null', 'throwAll', 'maxRetries', 'readsThrow', 'writesThrow'}
UP = {'connected', 'slow'}
def granted(c):
    return c['tokenPairs'] > 0 or c['codesMinted'] > 0 or (isinstance(c['result'], dict) and c['result'].get('ok') is True)
OBS = ['status', 'body', 'headers', 'thrownStatus', 'result', 'verifyCalls', 'totpCalls', 'cip8Calls', 'createSessionCalls', 'sessionsMinted', 'codesMinted', 'tokenPairs', 'challengeDeletes', 'storeOps']
assert set(base) == set(head), 'cell sets differ'
print('cells', len(head))
# Q1: more permissive (head grants where base refuses), both directions
more, less = [], []
for k in sorted(head):
    hb, bb = granted(head[k]), granted(base[k])
    if hb and not bb: more.append(k)
    if bb and not hb: less.append(k)
for mode_set, name in ((DOWN, 'DOWN'), (UP, 'UP')):
    print(f'{name}: head-more-permissive', sum(1 for k in more if k.split('|')[1] in mode_set), '| base-more-permissive (control direction)', sum(1 for k in less if k.split('|')[1] in mode_set))
print('  head-more cells:', more)
print('  base-more cells:', less)
# locked account reaching password verify / factor verify
for lab, d in (('base', base), ('head', head)):
    n = [k for k, c in d.items() if '|locked|' in k and k.split('|')[1] in DOWN and (c['verifyCalls'] or c['totpCalls'])]
    print(f'{lab}: DOWN locked cells that ran a password/TOTP verify:', len(n))
    u = [k for k, c in d.items() if k.endswith('|wrong') and k.split('|')[1] in DOWN and c['status'] in (401,) ]
    print(f'{lab}: DOWN wrong-credential cells answered a plain 401:', len(u), u[:12])
# Q2: right vs wrong differences per group
def groups(d):
    g = collections.defaultdict(dict)
    for k, c in d.items():
        door, mode, lk, cr = k.split('|'); g[(door, mode, lk)][cr] = c
    return g
for lab, d in (('base', base), ('head', head)):
    diffs = collections.defaultdict(list)
    for (door, mode, lk), rw in sorted(groups(d).items()):
        if mode not in DOWN: continue
        fs = [f for f in OBS if rw['right'][f] != rw['wrong'][f]]
        if fs: diffs[mode].append((door, lk, fs, rw['right']['status'] or rw['right']['thrownStatus'] or rw['right']['result'], rw['wrong']['status'] or rw['wrong']['thrownStatus'] or rw['wrong']['result']))
    tot = sum(len(v) for v in diffs.values())
    print(f'\n{lab}: DOWN groups where right != wrong: {tot} of {sum(1 for x in groups(d) if x[1] in DOWN)}')
    for m, v in diffs.items():
        print(f'  {m}: {len(v)}')
        for x in v: print('    ', x)
# Q3 sentinels
for lab, d in (('base', base), ('head', head)):
    print(f'\n{lab}: LOCK sentinel in logs (cells/hits):', sum(1 for c in d.values() if c['lockSentInLogs']), sum(c['lockSentInLogs'] for c in d.values()),
          '| in body/headers:', sum(c['lockSentInBody'] for c in d.values()),
          '| SESS sentinel in logs (cells):', sum(1 for c in d.values() if c['sessSentInLogs']), '| SESS in body:', sum(c['sessSentInBody'] for c in d.values()))
    lk = [l for c in d.values() for l in c['lockoutLogLines'] if 'G171LOCK' in l]
    print('   lockout-module lines carrying the LOCK sentinel:', len(lk))
# Q5 UP equality
neq = []
for k in sorted(head):
    if k.split('|')[1] not in UP: continue
    fs = [f for f in OBS if head[k][f] != base[k][f]]
    if fs: neq.append((k, fs))
print('\nUP cells', sum(1 for k in head if k.split("|")[1] in UP), 'head != base on observables:', len(neq), neq[:10])
lneq = [k for k in head if k.split('|')[1] in UP and head[k]['lockoutLogLines'] != base[k]['lockoutLogLines']]
print('UP cells whose lockout log lines differ:', len(lneq))
