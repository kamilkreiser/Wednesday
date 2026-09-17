import json,os,urllib.request
tok=os.environ['GH_TOKEN']
def gh(p):
    r=urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura'+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}); return json.load(urllib.request.urlopen(r))
c=gh('/compare/79933c79817ce4ef013ce885b3a32ea06419924f...develop')
print('status',c['status'],'ahead',c['ahead_by'],'behind',c['behind_by'])
for k in c['commits']: print(k['sha'][:9], k['commit']['message'].split('\n')[0][:100])
x=gh('/compare/79933c79817ce4ef013ce885b3a32ea06419924f...81ee4b729e86a645fc9098aafa1aaf39035a9950'); print('control (squash vs its parent): status',x['status'])
