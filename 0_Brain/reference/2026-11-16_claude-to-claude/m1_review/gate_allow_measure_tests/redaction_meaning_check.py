#!/usr/bin/env python3
"""QA-ALLOW-MEASURE item 6: compare a redacted committed file with its unredacted original for MEANING.
Every placeholder (<RUN>, <ID-n>, ...) in the redacted text is turned into a wildcard; each redacted line must then
match its original line; reports line counts, unmatched lines (by number only) and whether every marker/decision token
present in the original survives. Prints nothing of the original's content.
usage: redaction_meaning_check.py <redacted> <original>"""
import re,sys
red=open(sys.argv[1],errors='replace').read().split('\n'); org=open(sys.argv[2],errors='replace').read().split('\n')
print('lines redacted=%d original=%d'%(len(red),len(org)))
bad=[]
for i,(a,b) in enumerate(zip(red,org)):
    pat='^'+re.sub(r'<[A-Z_]+(?:-\d+)?>|-[A-Z_]+-', '.+?', re.escape(a).replace(r'\<','<').replace(r'\>','>').replace(r'\-','-'))+'$'
    try: ok=re.match(pat,b,re.S) is not None
    except re.error: ok=False
    if not ok: bad.append(i+1)
print('lines not matching their original after placeholder wildcarding:',bad[:20],'count',len(bad))
keys=['MK3','allow','deny','permission','"result"','is_error','permission_denials','PreToolUse','PostToolUse','Exit code','M7_','READ_OPEN','WRITE_OPEN','TTYLINE','session_id']
t_r='\n'.join(red); t_o='\n'.join(org)
print('token survival (original count -> redacted count):',{k:(t_o.count(k),t_r.count(k)) for k in keys if t_o.count(k)})
