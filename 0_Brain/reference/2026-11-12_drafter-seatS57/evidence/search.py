import json,sys,re
d=json.load(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/evidence/board_text_1112.json'))
for t in sys.argv[1:]:
    tl=t.lower(); hits=[]
    for i in d:
        where=[]
        if tl in (i['title'] or '').lower(): where.append('title')
        if tl in (i['description'] or '').lower(): where.append('desc')
        n=sum(1 for c in i['comments']['nodes'] if tl in (c['body'] or '').lower())
        if n: where.append(f'comments x{n}')
        if where: hits.append(f"{i['identifier']}[{i['state']['name']}]({','.join(where)})")
    print(f"{t!r}: {len(hits)} hits: {' '.join(hits[:25])}")
