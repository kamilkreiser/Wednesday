#!/usr/bin/env python3
"""QA-ALLOW-MEASURE item 4: analyse one run of qa_repro.sh. usage: qa_repro_analyse.py <run dir>"""
import re,sys,json
d=sys.argv[1]
DRE=re.compile(r'Do you want to|Yes, and|No, and tell|Allow once|Esc to cancel|❯ 1\. Yes|Do you want to proceed|Do you want to create')
fr=re.split(r'^=== FRAME ',open(d+'/frames.txt').read(),flags=re.M)[1:]
ts=[float(re.match(r't=([\d.]+)',f).group(1)) for f in fr]
keys=[l.split(' ',2) for l in open(d+'/keys.log').read().splitlines()]
says=[float(k[0]) for k in keys if k[1]=='SAY']
trust_t=[float(k[0]) for k in keys if k[1]=='KEY' and 'Enter' in k[2]]
after=[f for f,t in zip(fr,ts) if t>=says[0]]
gaps=[b-a for a,b in zip(ts,ts[1:]) if a>=says[0]-1]
print('frames total',len(fr),'frames after first prompt',len(after),'dialog-frames after first prompt',sum(1 for f in after if DRE.search(f)))
print('frame gap after first prompt: min %.2f s, median %.2f s (frames only when screen changed; poll 0.1 s)'%(min(gaps),sorted(gaps)[len(gaps)//2]))
print('keys:',[ (k[1],k[2][:30]) for k in keys])
raw=open(d+'/pane.bytes','rb').read().decode('utf-8','replace')
noansi=re.sub(r'\x1b\][^\x07\x1b]*(\x07|\x1b\\)|\x1b\[[0-9;?<>=]*[ -/]*[@-~]|\x1b[()][A-Za-z0-9]|\x1b[=>78DEHMNOc]','',raw)
# the trust dialog also says "Esc to cancel": count dialog strings only AFTER the trust dialog's last text
cut=noansi.rfind('Yes, I trust this folder'); tail=noansi[cut:] if cut>=0 else noansi
for s in ['Do you want to create','Do you want to proceed','Esc to cancel','Yes, and','❯ 1. Yes','No, and tell']:
    print('pane.bytes after trust dialog, ANSI removed: %-22s %d'%(s,tail.count(s)))
print('pane.bytes size',len(raw))
dl=open(d+'/debug.log').read()
for pat in ['Hook approved tool use for (\\w+), bypassing permission prompt','permissionDecisionMs=\\d+','executePermissionRequestHooks called for tool: \\w+','(\\w+) tool permission denied','dispatching to firstParty model=[\\w.-]+','Registered \\d+ hooks from \\d+ plugins']:
    print('debug:',pat.split(' ')[0][:30],'->',re.findall(pat,dl)[:6] if '(' in pat else re.findall(pat,dl)[:6])
try:
    for l in open(d+'/hook/stdin.jsonl'):
        l=l.strip()
        if l: e=json.loads(l); print('hook stdin:',e['hook_event_name'],e.get('tool_name'),'permission_mode=',e.get('permission_mode'))
except FileNotFoundError: print('hook stdin: none (no hook)')
print('footer:',[l.strip() for l in open(d+'/startup-footer.txt') if l.strip()][-1:])
