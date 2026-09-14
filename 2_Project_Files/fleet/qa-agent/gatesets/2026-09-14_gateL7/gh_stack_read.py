#!/usr/bin/env python3
"""The compare-API readings the launcher's stack guards assert (exit 10). Token by NAME, never printed."""
import json, urllib.request, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; tok=''
for line in open(ENV,encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok=line.strip().split('=',1)[1].strip().strip('"').strip("'")
assert tok
API='https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p): return json.load(urllib.request.urlopen(urllib.request.Request(API+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}),timeout=60))
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for a,b,l in [('8861e62161466c40f08d2b10a30edeb203123993','b54487216ebb49f1de7ed9349f089d92a3e5bfc1','M18...918'),
              ('8861e62161466c40f08d2b10a30edeb203123993','5341b1daed8afe4254e05ef66ef4350fd8220d4f','M18...925'),
              ('d4cf7e3cf73e91422a229b7d0767cf6c3a04fe57','b85f1db24596a5e0ce98fe2b1343d9f515a1a995','d4cf7e3cf...924'),
              ('b54487216ebb49f1de7ed9349f089d92a3e5bfc1','5341b1daed8afe4254e05ef66ef4350fd8220d4f','918...925'),
              ('a4f71cde660c1442d98317e26d93845340b20098','5341b1daed8afe4254e05ef66ef4350fd8220d4f','903...925'),
              ('b85f1db24596a5e0ce98fe2b1343d9f515a1a995','5341b1daed8afe4254e05ef66ef4350fd8220d4f','924...925 (NOT contained)'),
              ('21368d250d0b2c9a3f0f2cb1a3a4b9c6d2e8f7a1','b54487216ebb49f1de7ed9349f089d92a3e5bfc1','918merge...918 (placeholder sha, expect 404)')]:
    try:
        c=get('/compare/%s...%s'%(a,b))
        print('%-32s status %-9s ahead %3d behind %3d merge_base %s files %d' % (l, c['status'], c['ahead_by'], c['behind_by'], c['merge_base_commit']['sha'][:9], len(c.get('files') or [])), sorted(f['filename'].split('/')[-1] for f in (c.get('files') or [])))
        json.dump(c, open('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL7/gh/compare_stack_%s.json'%l.split(' ')[0].replace('...','_'),'w'), indent=1)
    except Exception as e: print(l, 'ERR', type(e).__name__, str(e)[:60])
# the contents API blobs at develop for the seven judged files (what the launcher reads)
for f in ['Blockchain/Dev/scripts/preflight/preflight.sh','Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh','Blockchain/Dev/scripts/run-code-guards.sh','Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh','Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh','.githooks/pre-push','Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh']:
    try: print('develop contents', f.split('/')[-1], get('/contents/'+f+'?ref=a5334350221c819f54d4a20a3308daeb9ca09617')['sha'][:9])
    except Exception as e: print('develop contents', f.split('/')[-1], 'ABSENT' if '404' in str(e) else type(e).__name__)
