import json,sys
for line in open(sys.argv[1]):
    r=json.loads(line)
    if r['id']=='__outbound': print('OUTBOUND',r['outbound']); continue
    st=r['st']; nz={k:v for k,v in st.items() if v and k!='events'}
    logs=[(l['lvl'],l['msg'][:38],l.get('vals',{}).get('error','-') if 'vals' in l else '-', 'THREW' if l['threw'] else '') for l in r['logs'] if l['lvl'] in('warn','error')]
    print(f"{r['id']:28} {str(r['status']):11} succ={r['success']!s:5} tok={int(r['tokenInBody'])} loc={int(r['codeInLocation'])} ck={r['cookie']:7} unh={r['unhandled']} leak={int(r['bodyLeaks'])} {nz} ev={st['events']} {logs}")
