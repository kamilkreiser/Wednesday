import sys,re
blocks=re.split(r'^### ',open(sys.argv[1]).read(),flags=re.M)[1:]
for b in blocks:
    l=b.splitlines(); h=l[0]
    ok = any(x.startswith('C=') and x.endswith('/tools/cargo') for x in l) and any(x.startswith('cargo 1.') for x in l)
    print(('OK   ' if ok else 'FAIL ')+h)
