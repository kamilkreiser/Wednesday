# Read-only: find Seat F's READY FOR GATE mail for PR 1908 in wednesday-agent@ (no send, no modify).
import json,urllib.request,sys
key=None
for l in open('/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env'):
    if l.startswith('AGENTMAIL_API_KEY='): key=l.split('=',1)[1].strip().strip('"').strip("'")
H={'Authorization':'Bearer '+key}
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908'
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=60))
hits=[]
for inbox in ['wednesday-agent@agentmail.to']:
    d=get(f'https://api.agentmail.to/v0/inboxes/{inbox}/messages?limit=100')
    for m in d.get('messages',[]):
        s=m.get('subject','')
        if '1908' in s: hits.append((inbox,m['message_id'],s,m.get('timestamp')))
for h in hits: print(h)
for inbox,mid,s,t in hits:
    if 'READY' in s.upper():
        import urllib.parse
        m=get(f'https://api.agentmail.to/v0/inboxes/{inbox}/messages/'+urllib.parse.quote(mid,safe=''))
        open(W+'/evidence/ready_mail_pr1908.txt','w').write(s+'\n'+str(t)+'\n\n'+(m.get('text') or m.get('extracted_text') or ''))
        print('saved',s); break
