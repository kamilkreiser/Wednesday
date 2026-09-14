#!/usr/bin/env python3
"""gh_read_close.py — restart-drafter's close-time re-check: live GitHub compare API for develop...HEAD(912) and
develop...HEAD(937), plus branches/develop, run at completion time to confirm the merge-base pin and characterise
any further develop move past the dead drafter's M19 read. Token sourced by NAME (GH_TOKEN) from the Secuura .env
in-process; never printed. Read-only (GET only)."""
import json, sys, os, urllib.request, urllib.error, datetime
ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
HEAD='609c44c55323b5c90320847b6837ca37f6586705'
HEAD937='6fd3a8bec4e4cc858d38925e00703a37ffcf1b30'
M18='8861e62161466c40f08d2b10a30edeb203123993'
tok=''
for line in open(ENV, encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok=line.split('=',1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN not found by name'
base='https://api.github.com/repos/Secuura/Distributed_Secuura'
def get(p):
    r=urllib.request.urlopen(urllib.request.Request(base+p,headers={'Authorization':'Bearer '+tok,'Accept':'application/vnd.github+json'}), timeout=60)
    return json.load(r)
print('read at', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
bd=get('/branches/develop'); DEV=bd['commit']['sha']
print('branches/develop now:', DEV, bd['commit']['commit']['author']['date'], repr(bd['commit']['commit']['message'].splitlines()[0][:140]))
cm=get(f'/compare/develop...{HEAD}'); print(f"compare develop...912head: status={cm['status']} merge_base={cm['merge_base_commit']['sha']} ahead={cm['ahead_by']} behind={cm['behind_by']} files={len(cm['files'])}")
cm2=get(f'/compare/develop...{HEAD937}'); print(f"compare develop...937head: status={cm2['status']} merge_base={cm2['merge_base_commit']['sha']} ahead={cm2['ahead_by']} behind={cm2['behind_by']} files={len(cm2['files'])}")
cmm=get(f'/compare/{M18}...{DEV}'); print(f"compare M18...develop-now: status={cmm['status']} ahead={cmm['ahead_by']} behind={cmm['behind_by']} files={len(cmm['files'])}")
for f in cmm['files']: print(f"  M18->now file {f['status']:9} {f['filename']}")
print('merge_base == M18?', cm['merge_base_commit']['sha']==M18, cm2['merge_base_commit']['sha']==M18)
print('done at', datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
