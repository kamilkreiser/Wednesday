#!/usr/bin/env python3
"""QA-W-DAEMON: case-insensitive scan of every ADDED line of gh/main...HEAD for personal, machine,
client names and home/volume paths. Arg: a file of lines to scan instead (positive control)."""
import re, subprocess, sys, collections
if len(sys.argv) > 1:
    lines = open(sys.argv[1], encoding='utf-8').read().splitlines()
else:
    d = subprocess.run(['git','-C','/private/tmp/claude-501/qwd/h','diff','gh/main...HEAD'],capture_output=True,text=True).stdout
    lines = [l for l in d.splitlines() if l.startswith('+') and not l.startswith('+++')]
PAT = re.compile(r'kamil|kreiser|secuura|datasec|smashhome|laptop-dev|/volumes/|/private/tmp|agentmail|@me\.com|friday-windows|c2c[\\/]|wdcc|wdc3|wdjt|/home/|\b[0-9a-f]{8}-[0-9a-f]{4}-|S-1-5-21', re.I)
USERS = re.compile(r'users[\\/]+([^\\/\s"`\')|,;]+)', re.I)
print('lines scanned:', len(lines))
hits = [l for l in lines if PAT.search(l)]
print('hits of the fixed list:', len(hits))
for l in hits[:40]: print('  HIT', l[:200])
names = collections.Counter(m.group(1).lower() for l in lines for m in USERS.finditer(l))
print('every name after a Users folder:', dict(names))
