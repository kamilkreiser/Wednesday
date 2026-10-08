import json, sys, urllib.request
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
def tok():
    for l in open(ENV, encoding='utf-8'):
        if l.startswith('GH_TOKEN='): return l.split('=',1)[1].strip().strip('"').strip("'")
    raise SystemExit('GH_TOKEN absent by name')
def get(p):
    r = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/'+p, headers={'Authorization':'Bearer '+tok(),'Accept':'application/vnd.github+json'})
    return json.load(urllib.request.urlopen(r, timeout=60))
if __name__ == '__main__':
    out = get(sys.argv[1]); json.dump(out, open(sys.argv[2],'w'), indent=1); print('ok', sys.argv[1], type(out).__name__, len(out))
