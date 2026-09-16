import json
G='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1016'
L=lambda n: {r['id']: r for r in json.load(open(G+'/probe_rows_%s.json'%n))['rows']}
b,h,hs,bs=L('base_UTC'),L('head_UTC'),L('head_Australia-Sydney'),L('base_Australia-Sydney')
k=lambda r:(r['http'],r['hits'],r['verified'],r['confidence'],r['txHash'],r['blockHeight'],r['hashValid'],r['source'])
print('%-4s | %-58s | %-52s | %-52s | %s' % ('id','base UTC (http hits verified confidence tx height hashValid source)','head UTC','flip?','TZ: head Sydney / base Sydney'))
for i in b:
    fl = 'FLIP' if k(b[i])!=k(h[i]) else ''
    vf = ' VERDICT' if (b[i]['verified'],b[i]['confidence'])!=(h[i]['verified'],h[i]['confidence']) else ''
    tz = '' if (k(hs[i])==k(h[i]) and k(bs[i])==k(b[i])) else 'TZ-DEP head-syd %s base-syd %s' % (k(hs[i])[4], k(bs[i])[4])
    print('%-4s | %s | %s | %s%s | %s  -- %s' % (i, k(b[i]), k(h[i]), fl, vf, tz, b[i]['note']))
