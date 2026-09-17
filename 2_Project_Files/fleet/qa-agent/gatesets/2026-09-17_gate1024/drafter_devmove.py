#!/usr/bin/env python3
"""drafter_devmove.py — develop moved during drafting (581c9db0d -> 81ee4b729, #1021). Fetch the new develop by SHA INTO THE DRAFTER CLONE ONLY over https with
GH_TOKEN by NAME handed to git through a GIT_ASKPASS helper reading an env var (never on a command line, never printed); then merge-tree --write-tree head x new develop
IN THE CLONE, name the merged-tree OID, and diff it against the head tree (expected: exactly #1021's 3 files)."""
import json, os, subprocess, tempfile, datetime, stat
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1024'
paths = json.load(open(GS + '/out/drafter_paths.json')); C = paths['C']
NEW = '81ee4b729e86a645fc9098aafa1aaf39035a9950'; HEAD = paths['sha']['head']
tok = ''
for line in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if line.startswith('GH_TOKEN='): tok = line.split('=', 1)[1].strip().strip('"').strip("'")
assert tok; print('GH_TOKEN: set |', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
d = tempfile.mkdtemp(prefix='askpass_', dir=paths['W']); ap = d + '/askpass.sh'
open(ap, 'w').write('#!/bin/sh\ncase "$1" in Username*) echo x-access-token ;; *) printf "%s" "$QA_GH_TOKEN" ;; esac\n'); os.chmod(ap, stat.S_IRWXU)
env = dict(os.environ, GIT_ASKPASS=ap, QA_GH_TOKEN=tok, GIT_TERMINAL_PROMPT='0')
def run(c, e=None): p = subprocess.run(c, capture_output=True, text=True, env=e); return p.returncode, p.stdout.strip(), p.stderr.strip().replace(tok, '<redacted>')
print('fetch', run(['git', '-C', C, 'fetch', '--quiet', '--no-tags', 'https://github.com/Secuura/Distributed_Secuura.git', NEW], env)[::2])
print('new develop parents', run(['git', '-C', C, 'rev-list', '--parents', '-n', '1', NEW]))
rc, mt, e = run(['git', '-C', C, 'merge-tree', '--write-tree', HEAD, NEW]); mt = mt.split('\n')[0]; print('merge-tree --write-tree head x 81ee4b729 (IN THE CLONE) rc', rc, 'tree', mt, e[:200])
rc, ht, e = run(['git', '-C', C, 'rev-parse', HEAD + '^{tree}']); print('head tree', ht)
print('head tree -> merged tree files:', run(['git', '-C', C, 'diff-tree', '-r', '--name-status', ht, mt])[1].replace('\n', ' | '))
print('581c9db0d -> 81ee4b729 files:', run(['git', '-C', C, 'diff', '--name-status', paths['sha']['dev'], NEW])[1].replace('\n', ' | '))
print('originate + api-gateway trees equal head vs merged:', run(['git', '-C', C, 'rev-parse', HEAD + ':Blockchain/Dev/services/originate', mt + ':Blockchain/Dev/services/originate', HEAD + ':Blockchain/Dev/services/api-gateway', mt + ':Blockchain/Dev/services/api-gateway'])[1].split())
