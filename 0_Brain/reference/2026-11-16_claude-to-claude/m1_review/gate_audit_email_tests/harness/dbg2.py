import sys; sys.argv=['x','/private/tmp/claude-501/qae/corp/c1','/private/tmp/claude-501/qae/corp/c1.base.out','/private/tmp/claude-501/qae/corp/c1.head.out']
src=open('/private/tmp/claude-501/qae/h/qa_analyze.py').read().split('# ---- survivors ----')[0]
exec(src)
WS_BYTE.discard(0x0b)  # Rust is_ascii_whitespace set
from collections import Counter
c=Counter(); ex={}
for i,(raw,m,nw) in enumerate(zip(raws,meta,new)):
    if sorted(nw['em'])!=sorted(oracle(nw['clean'],xn_ci=True)) or sorted(nw['emw'])!=sorted(oracle(nw['cleanw'],xn_ci=True)):
        c['still differs with Rust ASCII-whitespace reading']+=1; ex.setdefault('x',raw[:100])
print('after removing VT from the whitespace set, code vs oracle(xn-- ci) differences:', dict(c) or 0, ex)
WS_BYTE.add(0x0b)
n=0; kinds=Counter()
for i,(raw,m,nw) in enumerate(zip(raws,meta,new)):
    a=sorted(oracle(nw['clean'],xn_ci=True)); b=sorted(oracle(nw['clean'],xn_ci=True,ws='unicode'))
    if a!=b:
        # what follows the ':'?
        t=nw['clean']; 
        for s,e in set(b)-set(a):
            bb=t.encode(); ch=bb[e+1:].decode('utf-8','ignore')[:1]; kinds[hex(ord(ch))]+=1
print('Unicode-whitespace reading masks more after ":" + :', dict(kinds))
