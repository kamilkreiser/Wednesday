import sys, urllib.request, urllib.error
sys.path.insert(0, sys.argv[1]); from ghget import tok
class NR(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k): return None
req = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/actions/jobs/%s/logs' % sys.argv[2], headers={'Authorization':'Bearer '+tok(),'Accept':'application/vnd.github+json'})
try:
    data = urllib.request.build_opener(NR).open(req, timeout=60).read()
except urllib.error.HTTPError as e:
    if e.code not in (301,302,303,307,308): raise
    data = urllib.request.urlopen(urllib.request.Request(e.headers['Location']), timeout=120).read()
open(sys.argv[3],'wb').write(data); print('bytes', len(data))
