import subprocess, hashlib, sys, re
C='/private/tmp/b1818-gate/clone'
M='2a58dc5d9c62cc021b01e3fe5ebdcd09e76d7f9a'; MAIN='b4681297d974ac3d8e74a4a12baeb9ea41962c52'; OLD='851057291ffb019baee6c3c51a50d7b8833f5b3a'; BASE='308b7aa60cd8d2a8576b29e0422538cbaf140f24'
def g(*a, raw=False):
    r=subprocess.run(['git','-C',C,*a],capture_output=True)
    return r.stdout if raw else r.stdout.decode()
def ok(name,cond): print(('PASS ' if cond else 'FAIL ')+name)
par=g('rev-list','--parents','-n1',M).split()
print('parents',par[1:]); ok('parents order old,main', par[1:]==[OLD,MAIN])
new=g('rev-list',M,'^'+OLD,'^'+MAIN).split(); print('new commits',new); ok('exactly one new commit = merge', new==[M])
def lstree(c):
    d={}
    for line in g('ls-tree','-r','-z',c,raw=True).split(b'\0'):
        if not line: continue
        meta,path=line.split(b'\t',1); mode,typ,sha=meta.split()
        d[path]=(mode,typ,sha)
    return d
tm,to,tx,tb=lstree(MAIN),lstree(OLD),lstree(M),lstree(BASE)
pr=set(g('diff','--name-only','-z',BASE,OLD,raw=True).split(b'\0'))-{b''}
mn=set(g('diff','--name-only','-z',BASE,MAIN,raw=True).split(b'\0'))-{b''}
print('PR paths',len(pr),'main paths',len(mn),'common',len(pr&mn))
# overlay
ov=dict(tm)
for p in pr:
    if p in to: ov[p]=to[p]
    else: ov.pop(p,None)
# build tree hash
def treehash(entries):
    # entries: path->(mode,typ,sha)
    root={}
    for p,(mode,typ,sha) in entries.items():
        parts=p.split(b'/'); d=root
        for x in parts[:-1]: d=d.setdefault(x,{})
        d[parts[-1]]=(mode,sha)
    def h(d):
        items=[]
        for name,v in d.items():
            if isinstance(v,dict): items.append((name+b'/',b'40000',name,bytes.fromhex(h(v))))
            else: items.append((name,v[0],name,bytes.fromhex(v[1].decode())))
        items.sort(key=lambda t:t[0])
        body=b''.join(m+b' '+n+b'\0'+s for _,m,n,s in items)
        return hashlib.sha1(b'tree %d\0'%len(body)+body).hexdigest()
    return h(root)
mt=g('rev-parse',M+'^{tree}').strip()
print('own hasher main',treehash(tm)==g('rev-parse',MAIN+'^{tree}').strip(),'old',treehash(to)==g('rev-parse',OLD+'^{tree}').strip())
oh=treehash(ov); print('overlay tree',oh,'merge tree',mt,'files',len(ov)); ok('overlay == merge tree',oh==mt)
ov2=dict(ov); k=sorted(ov2)[0]; ov2[k]=(ov2[k][0],ov2[k][1],b'0'*40); ok('control: one blob swapped differs',treehash(ov2)!=mt)
d1=set(g('diff','--name-only','-z',OLD,M,raw=True).split(b'\0'))-{b''}
d2=set(g('diff','--name-only','-z',MAIN,M,raw=True).split(b'\0'))-{b''}
ok('diff old..merge == main 87 (%d)'%len(d1), d1==mn and len(mn)==87)
ok('diff main..merge == PR 57 (%d)'%len(d2), d2==pr and len(pr)==57)
ok('control: one path dropped seen', (d2-{sorted(d2)[0]})!=pr)
c_old={p:v for p,v in to.items() if p.startswith(b'content/')}; c_m={p:v for p,v in tx.items() if p.startswith(b'content/')}
ok('content/ byte-equal to old head (%d paths)'%len(c_m), c_old==c_m)
c_main={p:v for p,v in tm.items() if p.startswith(b'content/')}
print('control content main vs merge differing', sum(1 for p in set(c_main)|set(c_m) if c_main.get(p)!=c_m.get(p)))
for f in ('content/release-demo/CONTENT_HASH','content/release-draft/CONTENT_HASH'):
    print(f,'merge',g('show',M+':'+f).strip(),'main',g('show',MAIN+':'+f).strip())
ok('lock = main', tx[b'package-lock.json']==tm[b'package-lock.json']); print('lock control old!=main', to[b'package-lock.json']!=tm[b'package-lock.json'])
# modes
bad=[p for p in tx if p in ov and tx[p][0]!=ov[p][0]]; ok('modes equal overlay',not bad)
modes={}
for p,v in tx.items(): modes[v[0]]=modes.get(v[0],0)+1
print('mode census merge',modes)
# conflict markers
pat=re.compile(rb'^(<{7}|>{7})( |$)|^={7}$',re.M)
hits=[]
for p,(mode,typ,sha) in tx.items():
    if typ!=b'blob' or mode==b'120000': continue
    data=g('cat-file','blob',sha.decode(),raw=True)
    if pat.search(data): hits.append(p)
print('conflict-marker files',len(hits),[h.decode() for h in hits][:10])
planted=b'a\n<<<<<<< HEAD\nx\n=======\ny\n>>>>>>> main\n'; ok('control planted marker found',bool(pat.search(planted)))
