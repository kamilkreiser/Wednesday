#!/usr/bin/env python3
"""ci_logs_read.py — READ-ONLY: the job logs of `PR Security Gates (KS-168)` (step 11) and `Security Scanning` (step 7) at the
#918 and #925 heads, saved under gh/, with the lines the brief quotes grepped (token by NAME, never printed)."""
import json, sys, os, urllib.request, re, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'; G=sys.argv[1]
tok=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok=line.split('=',1)[1].strip().strip('"').strip("'")
assert tok
base='https://api.github.com/repos/Secuura/Distributed_Secuura'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None
def get(p, raw=False):
    req=urllib.request.Request(base+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'})
    if not raw:
        return json.load(urllib.request.urlopen(req, timeout=120))
    # the logs endpoint 302s to blob storage; the redirect must NOT carry the bearer (401 otherwise)
    try:
        r=urllib.request.build_opener(NoRedirect).open(req, timeout=120); loc=None; body=r.read()
    except urllib.error.HTTPError as e:
        if e.code in (301,302,303,307): loc=e.headers['Location']; body=None
        else: raise
    if loc: body=urllib.request.urlopen(urllib.request.Request(loc), timeout=120).read()
    return body.decode('utf-8','replace')
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
for n, runs in [(918, {'gates': 34785776637, 'scan': 34785776582}), (925, {'gates': 34787428639, 'scan': 34787428627})]:
    for tag, rid in runs.items():
        jobs=get(f'/actions/runs/{rid}/jobs?per_page=50')['jobs']
        for j in jobs:
            if j['conclusion']!='failure': continue
            log=get(f"/actions/jobs/{j['id']}/logs", raw=True)
            log=re.sub(r'^\S+Z ', '', log, flags=re.M)  # strip timestamps
            p=f"{G}/gh/ci_{n}_{tag}_job{j['id']}.log"; open(p,'w',encoding='utf-8').write(log)
            lines=log.split('\n')
            print(f"\n#{n} run {rid} job {j['id']} {j['name']!r} -> {p.split('/')[-1]} ({len(lines)} lines)")
            for i,l in enumerate(lines,1):
                if re.search(r'run_code_guards\.test\.sh —|preflight_deps: \d+ passed|pre_push_hook_base|=== .*run_code_guards|=== .*preflight_deps|shell suites: \d+ passed|^FAILED: |packages/shared is not built|manifest_readers_agree.*passed|\d+ passed, \d+ failed \(of|HIGH\+CRITICAL vulnerability|Process completed with exit code|bash --version|GNU bash', l):
                    print(f"  :{i} {l.strip()[:150]}")
print('done', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
