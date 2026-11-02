import json,sys
for l in open(sys.argv[1]):
    r=json.loads(l)
    b=r['body']; bs=(b.get('error',{}).get('message') if isinstance(b,dict) and isinstance(b.get('error'),dict) else (list(b.keys())[:4] if isinstance(b,dict) else b))
    st=r['state']; docs=';'.join(f"{d['id']}:{d['status']}{'/rev' if d['revoked'] else ''}" for d in st['documents'])
    print(f"{r['route']:9} {r['fault']:34} {r['v']:4} fired={str(r['fired']):5} {str(r['status']):9} {str(bs)[:42]:42} docs={docs} ev={len(st['events'])} sh={len(st['shares'])} ch={st['charges'][1:]} err={[e.get('error') if isinstance(e,dict) else e for e in r['routeErr']]}")
