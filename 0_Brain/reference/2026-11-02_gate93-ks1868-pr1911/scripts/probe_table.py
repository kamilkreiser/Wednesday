import json
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911/logs/'
rows={}
for v in ['base','head']:
    for l in open(G+f'probe_reset_{v}.jsonl'):
        d=json.loads(l)
        if 'positive_control' in d: print(v,d); continue
        b=d['body'] or {}; e=b.get('error',{}) if isinstance(b,dict) else {}
        line=[x[1].get('error') for x in d['error_lines'] if x[0].startswith('Password reset: the session revocation THREW')]
        eh=[x[1].get('error') for x in d['error_lines'] if x[0]=='Error occurred']
        rows.setdefault(d['case'],{})[v]=dict(status=d['status'],code=e.get('code','ok'),msg=(e.get('message') or b.get('message') or '')[:50],
          pw=d['password_changed'],argon=d['password_is_argon2'],burned=d['token_used'],sess=' '.join(d['sessions']),unh=d['unhandled'],
          ks1692_line=line,errhandler=[str(x)[:60] for x in eh],sql=d['sql'],retry=d['retry_status'],retry_sess=' '.join(d['sessions_after_retry']),retry_burned=d['token_used_after_retry'],unknown=d['unknown_sql'])
for c,vv in rows.items():
    print('##',c)
    for v in ['base','head']:
        print(' ',v,json.dumps(vv[v]))
    same={k:vv['base'][k]==vv['head'][k] for k in vv['base']}
    print('  differs in:',[k for k,s in same.items() if not s])
# compare unreadable head rows against ordinary rows (same failAt) on state fields
F=['status','code','msg','pw','argon','burned','sess','unh','sql','retry','retry_sess','retry_burned']
for at in ['smembers','get','del']:
    o=rows[f'{at}/ordinary']['head']
    for k in ['revokedProxy','throwingGetter']:
        for v in ['base','head']:
            x=rows[f'{at}/{k}'][v]
            print(f'{at}/{k} {v} vs {at}/ordinary head: differs in',[f for f in F if x[f]!=o[f]])
