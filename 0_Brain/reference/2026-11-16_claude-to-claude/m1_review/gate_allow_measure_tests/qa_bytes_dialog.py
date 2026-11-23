#!/usr/bin/env python3
"""QA-ALLOW-MEASURE item 4: search EVERY byte the pane received (pipe-pane) for permission-dialog text, robust to the
TUI writing cursor moves instead of spaces: escape sequences removed, then all whitespace removed. Only text after the
trust dialog's last 'Yes, I trust this folder' is searched. usage: qa_bytes_dialog.py <pane.bytes>"""
import re,sys
raw=open(sys.argv[1],'rb').read().decode('utf-8','replace')
t=re.sub(r'\x1b\][^\x07\x1b]*(\x07|\x1b\\)|\x1b\[[0-9;?<>=]*[ -/]*[@-~]|\x1b[()][A-Za-z0-9]|\x1b[=>78DEHMNOc]','',raw)
t=re.sub(r'\s+','',t)
cut=t.rfind('Yes,Itrustthisfolder'); t=t[cut+len('Yes,Itrustthisfolder'):] if cut>=0 else t
for s in ['Doyouwanttocreate','Doyouwanttoproceed','Doyouwant','Esctocancel','Yes,and','No,andtell','Createfile','Bashcommand','Wrote1line','Ran1shellcommand','QA-BASH-RAN']:
    print('%-20s %d'%(s,t.count(s)))
