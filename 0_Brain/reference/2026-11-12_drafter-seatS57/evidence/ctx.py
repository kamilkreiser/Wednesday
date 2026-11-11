import json,sys
d={i['identifier']:i for i in json.load(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/evidence/board_text_1112.json'))}
k=sys.argv[1]; t=sys.argv[2].lower(); w=int(sys.argv[3]) if len(sys.argv)>3 else 300
i=d[k]; print('==',k,i['state']['name'],i['title'][:150])
def show(label,s):
    sl=(s or '').lower(); p=0
    while True:
        j=sl.find(t,p)
        if j<0: break
        print(f'  [{label}] ...',(s[max(0,j-w):j+w]).replace('\n',' '),'...'); p=j+w
show('desc',i['description'])
for c in i['comments']['nodes']: show('c '+c['id'][:8],c['body'])
