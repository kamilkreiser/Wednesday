import json,sys
def load(p): return {(r['route'],r['fault'],r['v']):r for r in map(json.loads,open(p))}
a=load(sys.argv[1]); b=load(sys.argv[2]); ok=diff=0; common=sorted(set(a)&set(b))
for k in common:
    for f in ['status','body','state','sql','anchorCalls','notifies']:
        if a[k][f]==b[k][f]: ok+=1
        else: diff+=1; print('DIFF',k,f)
print(f'common cells {len(common)}: OK {ok} DIFF {diff}')
