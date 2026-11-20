import sys,re,collections
E='/Volumes/Datasec_DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-11-20_B1803_evidence/runs'
DUR=re.compile(r'\x1b\[\d+m \d+\x1b\[\d+mms\x1b\[\d+m\x1b\[\d+m$')
ANSI=re.compile(r'\x1b\[[0-9;]*m')
def names(d):
    c=collections.Counter(); marks=collections.Counter()
    for f in ('vitest_renderers.log','vitest_workspace.log'):
        for l in open(f'{E}/{d}/{f}',encoding='utf-8'):
            l=l.rstrip('\n'); s=ANSI.sub('',DUR.sub('',l)).strip()
            if s[:1] in '✓×↓' and ' > ' in s:
                marks[s[0]]+=1; c[s[1:].strip()]+=1
    return c,marks
a,ma=names('chain_main'); b,mb=names('chain_merged')
print('main',sum(a.values()),dict(ma),'merged',sum(b.values()),dict(mb))
lost=a-b; added=b-a
print('lost',sum(lost.values())); [print('  L',k) for k in lost]
print('added',sum(added.values()))
byfile=collections.Counter(k.split(' > ')[0].split()[-1] for k in added.elements())
for k,v in byfile.most_common(): print('  A',v,k)
dup=[k for k,v in b.items() if v>1]; print('duplicate titles at merged',len(dup))
ctl=b.copy(); k=next(iter(a)); ctl[k]-=1; print('control lost when one main name dropped from merged:',sum((a-ctl).values()))
