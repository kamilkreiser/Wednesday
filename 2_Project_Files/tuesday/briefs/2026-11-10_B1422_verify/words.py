import subprocess,sys,re,difflib
g=sys.argv[1]
def show(r): return subprocess.check_output(['git','-C',g,'show',f'refs/gate/{r}:DEPLOY.md']).decode()
a,b=show('main'),show('head')
al,bl=a.split('\n'),b.split('\n')
print('lines',len(al),len(bl))
ch=[(i,x,y) for i,(x,y) in enumerate(zip(al,bl)) if x!=y]
print('same line count',len(al)==len(bl),'changed lines',[(i+1) for i,_,_ in ch])
for i,x,y in ch:
    xw,yw=x.split(),y.split()
    # added words: multiset difference
    from collections import Counter
    added=Counter(yw)-Counter(xw); removed=Counter(xw)-Counter(yw)
    print('added',dict(added),'removed',dict(removed))
    # subsequence check
    it=iter(xw); print('head words subsequence of main words:',all(w in it for w in yw))
# whole-paragraph context: added words vs sentence in paragraph (lines 262-263 sentence)
# control: planted added word
x=al[262]; y=bl[262]+' now'
from collections import Counter
print('control added:',dict(Counter(y.split())-Counter(x.split())))
# pin paragraph byte equal lines 248-255 and 218-255
print('218-255 equal',al[217:255]==bl[217:255],'248-254',al[247:254]==bl[247:254],'255',al[254]==bl[254])
al2=list(al); al2[250]+='x'; print('control 248-254 differs when planted:',al2[247:254]!=bl[247:254])
# everything else equal
print('all other lines equal',all(x==y for i,(x,y) in enumerate(zip(al,bl)) if i!=262))
