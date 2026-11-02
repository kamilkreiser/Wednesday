# writes head-id -> base-id map using the same alignment as corpus_cmp.py
import json,sys
sys.argv=['x']
exec(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate135-ks1725-pr1953/scripts/corpus_cmp.py').read().split("skipped=collections.Counter()")[0])
json.dump({kh:kb for kb,kh,_ in pairs},open(G+'/logs/pairmap.json','w'))
