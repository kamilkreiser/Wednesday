import json,sys,urllib.request
envp="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
tok=None
for line in open(envp):
    if line.startswith("GH_TOKEN="): tok=line.split("=",1)[1].strip().strip('"').strip("'")
H={"Authorization":"Bearer "+tok,"Accept":"application/vnd.github+json","User-Agent":"wed-drafter-readonly"}
B="https://api.github.com/repos/Secuura/Distributed_Secuura"
for n in sys.argv[1:]:
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(B+"/pulls/"+n,headers=H),timeout=60))
        print(n,d['state'],'merged' if d['merged'] else 'notmerged',d['head']['sha'][:12],(d.get('merge_commit_sha') or '')[:12],d.get('merged_at'),d['title'][:70])
    except Exception as e: print(n,'ERR',e)
