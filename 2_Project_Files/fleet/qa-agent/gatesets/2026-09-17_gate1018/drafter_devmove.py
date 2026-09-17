#!/usr/bin/env python3
"""drafter_devmove.py — develop moved 81ee4b729 -> ee40d3099 (#1024 + #1022) during the guard controls. If the object is missing from the shared clone,
fetch it by SHA INTO THE DRAFTER CLONE ONLY over https (GH_TOKEN by NAME through a GIT_ASKPASS helper reading an env var; never on a command line, never
printed); then merge-tree --write-tree head x ee40d3099 IN THE CLONE: rc, tree OID, develop -> merged files, auth subtree equality."""
import json, os, subprocess, tempfile, datetime, stat
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1018'
paths = json.load(open(GS + '/out/drafter_paths.json')); C = paths['C']; HEAD = paths['sha']['head']
NEW = 'ee40d3099599fa2db23a37049da8e00ac953eacd'
def run(c, e=None): p = subprocess.run(c, capture_output=True, text=True, env=e); return p.returncode, p.stdout.strip(), p.stderr.strip()
print('drafter_devmove', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
rc, o, e = run(['git', '-C', C, 'cat-file', '-t', NEW]); print('object in clone before:', rc, o, e[:120])
if rc != 0:
    tok = ''
    for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
        if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
    assert tok; print('GH_TOKEN: set')
    d = tempfile.mkdtemp(prefix='askpass_', dir=paths['W']); ap = d + '/askpass.sh'
    open(ap, 'w').write('#!/bin/sh\ncase "$1" in Username*) echo x-access-token ;; *) printf "%s" "$QA_GH_TOKEN" ;; esac\n'); os.chmod(ap, stat.S_IRWXU)
    env = dict(os.environ, GIT_ASKPASS=ap, QA_GH_TOKEN=tok, GIT_TERMINAL_PROMPT='0')
    rc, o, e = run(['git', '-C', C, 'fetch', '--quiet', '--no-tags', 'https://github.com/Secuura/Distributed_Secuura.git', NEW], env); print('fetch rc', rc, e.replace(tok, '<redacted>')[:200])
print('new develop parents', run(['git', '-C', C, 'rev-list', '--parents', '-n', '3', NEW])[1].replace('\n', ' | '))
rc, mt, e = run(['git', '-C', C, 'merge-tree', '--write-tree', '--name-only', '--messages', HEAD, NEW]); print('merge-tree --write-tree head x ee40d3099 (IN THE CLONE) rc', rc, '| out', mt.replace('\n', ' | ')[:600], e[:200])
mt = mt.split('\n')[0]
print('develop -> merged files:', run(['git', '-C', C, 'diff', '--name-status', NEW, mt])[1].replace('\n', ' | '))
print('81ee4b729 -> ee40d3099 files:', run(['git', '-C', C, 'diff', '--name-status', paths['sha']['dev'], NEW])[1].replace('\n', ' | '))
for sub in ('Blockchain/Dev/services/auth', 'Blockchain/Dev/packages/shared'):
    a = run(['git', '-C', C, 'rev-parse', HEAD + ':' + sub])[1]; b = run(['git', '-C', C, 'rev-parse', mt + ':' + sub])[1]; print('subtree', sub, a[:9], b[:9], 'EQUAL' if a == b else 'DIFFER')
print('auth-relevant blobs at ee40d3099 vs 81ee4b729:', run(['git', '-C', C, 'diff', '--name-only', paths['sha']['dev'], NEW, '--', 'Blockchain/Dev/services/auth', 'Blockchain/Dev/packages/shared', 'Blockchain/Dev/eslint.config.mjs', 'Blockchain/Dev/docs/openapi'])[1] or 'NONE')
