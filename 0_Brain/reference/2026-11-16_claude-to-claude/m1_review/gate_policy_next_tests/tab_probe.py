# QA-POLICY-NEXT: compact the probe output: one line per row, the 5 states as columns of none/StillAsk/Allowed codes.
import sys,re,collections
def code(s):
    s=s.strip()
    m=re.match(r'(ASK|ALLOW|DENY) ?(.*?) (=d|≠d)$',s.replace('(=decide:true)','=d').replace('(=decide:false)','≠d'))
    if not m: return '?'+s
    k,rest,eq=m.groups()
    if k=='ASK': c='ask'+rest.replace('T','')
    elif k=='ALLOW': c='OWNER' if 'OwnerChoseAllow' in rest else 'allow:'+rest[:20]
    else:
        r=re.search(r'RefusedInAllow \{ reason: "([^"]*)"',rest)
        if r: c='REF('+r.group(1)[:38]+')'
        elif rest.startswith('HardDeny'): c='HARDDENY'
        else: c='deny:'+rest.split()[0]
    return c
rows=collections.OrderedDict()
for l in open(sys.argv[1]):
    m=re.match(r'ROW \| (\S+) \| (\S+) \| (.*?) \| (cwd=.*?) \| (\S+) \| none=(.*?) \| StillAsk=(.*?) \| Allowed=(.*?) \| FULL',l)
    key=' | '.join(m.group(1,2,3,4)); st=m.group(5)
    none,sa,al=m.group(6),m.group(7),m.group(8)
    rows.setdefault(key,[]).append((st,code(none),code(sa),code(al)))
for k,v in rows.items():
    print(k.replace('cwd=<root>/ws','ws'))
    for st,a,b,c in v: print('    %-24s none=%s  StillAsk=%s  Allowed=%s'%(st,a,b,c))
