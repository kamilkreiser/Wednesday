# property (i): C-17 ruling vs lane brief section 9, and lane sentences naming the owner
import re, sys
cl = open(sys.argv[1], encoding='utf-8').read().split('\n'); br = open(sys.argv[2], encoding='utf-8').read().split('\n')
c = cl[167]; b = br[165]
cq = re.search(r'> (Decision .*)$', c).group(1); bq = re.search(r'verbatim: "(Decision [^"]*)"', b).group(1)
print('C-17 line 168:', repr(cq)); print('brief line 166:', repr(bq))
print('equal:', cq == bq, 'chars', len(cq), len(bq), 'utf8 bytes', len(cq.encode()), len(bq.encode()))
print('C-17 context line:', [l for l in cl[160:166] if l.startswith('Context')][0][:140])
for path in sys.argv[3:]:
    for i, l in enumerate(open(path, encoding='utf-8').read().split('\n'), 1):
        if 'owner' in l.lower(): print(f'{path.split("/")[-1]}:{i}: {l[:220]}')
