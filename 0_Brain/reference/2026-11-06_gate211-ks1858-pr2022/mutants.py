import hashlib,json,subprocess,sys,os
G=sys.argv[1]; A=f"{G}/repo/Blockchain/Dev/services/auth"; V=f"{G}/repo/Blockchain/Dev/node_modules/vitest/vitest.mjs"; E=f"{G}/evidence"
S=f"{A}/src/providers/social"
T={'google':'ks1858-google','facebook':'ks1858-facebook','linkedin':'ks1858-linkedin','microsoft-personal':'ks1858-microsoft-personal','github':'ks1792-github'}
tf=lambda a:f"src/__tests__/{T[a]}-refuses-a-token-answer-without-an-access-token.test.ts"
W=['RED KS-1858 W1','RED KS-1858 W2']
# (id, adapter, old, new, predicted-red cell prefixes)
M=[
 ('S1_github_Ma','github',"tokenBody.access_token.trim() === ''","tokenBody.access_token === ''",W),
 ('S2_facebook_Ma','facebook',"tokenBody.access_token.trim() === ''","tokenBody.access_token === ''",W),
 ('S3_linkedin_Mb','linkedin'," || tokenBody.access_token.trim() === ''","",W+['RED KS-1858 R3']),
 ('S4_github_Mb','github'," || tokenBody.access_token.trim() === ''","",W+['RED KS-1792']),
 ('O1_google_send_trimmed','google',"Bearer ${tokens.access_token}","Bearer ${tokens.access_token.trim()}",[]),
 ('O2_facebook_send_trimmed','facebook',"const access_token = tokenBody.access_token;","const access_token = tokenBody.access_token.trim();",[]),
 ('O3_linkedin_send_trimmed','linkedin',"const access_token = tokenBody.access_token;","const access_token = tokenBody.access_token.trim();",[]),
 ('O4_microsoft_send_trimmed','microsoft-personal',"const access_token = tokenBody.access_token;","const access_token = tokenBody.access_token.trim();",[]),
 ('O5_github_send_trimmed','github',"const access_token = tokenBody.access_token;","const access_token = tokenBody.access_token.trim();",[]),
 ('O6_google_typeof_dropped','google',"typeof tokens.access_token !== 'string' || tokens.access_token.trim() === ''","(tokens.access_token as string).trim() === ''",['RED KS-1858 R1','RED KS-1858 R2']),
 ('O7_github_null_compare','github',"tokenBody.access_token.trim() === ''","tokenBody.access_token.trim() == null",W+['RED KS-1792']),
 ('O8_github_error_branch_dropped','github'," || tokenBody.error !== undefined","",['RED KS-1792']),
]
json.dump([{'id':m[0],'predicted_red':m[4]} for m in M],open(f"{E}/q4_predictions.json",'w'),indent=1)
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
out=[]
for mid,a,old,new,pred in M:
    p=f"{S}/{a}.ts"; before=sha(p); src=open(p).read()
    assert src.count(old)>=1,(mid,'anchor')
    mut=src.replace(old,new,1); assert mut!=src
    open(p,'w').write(mut)
    try:
        assert new in open(p).read() or new=='' ,'landed'
        assert sha(p)!=before
        tsc=None
        js=f"{E}/q4_{mid}.json"
        r=subprocess.run(['node',V,'run','--root',A,'--cache=false','--reporter=json',f'--outputFile={js}',tf(a)],capture_output=True,text=True,cwd=G)
        d=json.load(open(js)); red=[t['title'] for f in d['testResults'] for t in f['assertionResults'] if t['status']!='passed']
        msg=[(t['failureMessages'] or [''])[0].split('\n')[0][:110] for f in d['testResults'] for t in f['assertionResults'] if t['status']!='passed']
        row={'id':mid,'adapter':a,'rc':r.returncode,'total':d['numTotalTests'],'red':[x[:60] for x in red],'msg':msg[:2]}
        if mid in('O1_google_send_trimmed','O2_facebook_send_trimmed','O6_google_typeof_dropped','S4_github_Mb','O7_github_null_compare','O8_github_error_branch_dropped'):
            t=subprocess.run(['node',f"{G}/repo/Blockchain/Dev/node_modules/typescript/bin/tsc",'--noEmit','-p',A],capture_output=True,text=True,cwd=G)
            row['tsc_errors']=t.stdout.count('error TS'); row['tsc_head']=t.stdout[:200]
        out.append(row); print(json.dumps(row)[:520],flush=True)
    finally:
        open(p,'w').write(src)
    assert sha(p)==before,'restore'
json.dump(out,open(f"{E}/q4_results.json",'w'),indent=1)
print('restored by sha256: all')
