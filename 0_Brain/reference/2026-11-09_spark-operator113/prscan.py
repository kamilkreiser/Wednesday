import json,subprocess,os,sys
env=dict(os.environ)
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    if l.startswith('GH_TOKEN='): env['GH_TOKEN']=l.strip().split('=',1)[1].strip('"\'')
env['GH_CONFIG_DIR']='/private/tmp/spark_work_o113/ghcfg'
def gh(*a): return subprocess.run(['gh','api',*a],capture_output=True,text=True,env=env)
R='Secuura/Distributed_Secuura'
prs=json.loads(gh('--paginate','--slurp',f'repos/{R}/pulls?state=open&per_page=100').stdout)
prs=[p for pg in prs for p in pg]
out={}
for p in prs:
    n=p['number']
    fs=json.loads(gh('--paginate','--slurp',f'repos/{R}/pulls/{n}/files?per_page=100').stdout)
    out[n]={'title':p['title'],'base':p['base']['ref'],'files':[f['filename'] for pg in fs for f in pg]}
json.dump(out,open(sys.argv[1],'w'),indent=1)
print(len(out),'PRs',sum(len(v['files']) for v in out.values()),'files')
