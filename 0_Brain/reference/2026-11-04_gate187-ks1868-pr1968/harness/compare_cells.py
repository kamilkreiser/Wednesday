import json,sys
W=sys.argv[1]
def key(r): return (r['site'],r['value'])
out=[]
for kind in ('repo','db'):
    b={key(r):r for r in json.load(open(f'{W}/runs/cells_{kind}_base.json'))}
    h={key(r):r for r in json.load(open(f'{W}/runs/cells_{kind}_head.json'))}
    assert set(b)==set(h)
    def state(r):  # control-relevant state, excluding the logged reason text
        return {k:r.get(k) for k in ('threw','value_out','initDb','lines')}
    sites=sorted({k[0] for k in b})
    for s in sites:
        ordb=state(b[(s,'ordinaryError')])
        for k in sorted(x for x in b if x[0]==s):
            rb,rh=b[k],h[k]
            print(f"{s:14} {k[1]:28} BASE {json.dumps(state(rb)):60} reason={rb.get('reasonType')}:{rb.get('reason')!s:28} tok={rb['tokenInLogs']!s:5} | HEAD {json.dumps(state(rh)):60} reason={rh.get('reasonType')}:{rh.get('reason')!s:26} tok={rh['tokenInLogs']!s:5} head==base-ord:{state(rh)==ordb if k[1]!='rowWithToken' else 'n/a'}")
