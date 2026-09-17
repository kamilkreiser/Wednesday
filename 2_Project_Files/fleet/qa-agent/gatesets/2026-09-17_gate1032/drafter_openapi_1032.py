#!/usr/bin/env python3
"""drafter_openapi_1032.py — in the drafter clone head worktree (cwd inside the clone): `npm run generate-openapi -- --check` (rc + tail); the YAML's
/api/users/* verification paths counted case-insensitively with a positive control (/api/users/me:); auth.openapi.ts registrations for verification."""
import json, subprocess, datetime, re
GS = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1032'
paths = json.load(open(GS + '/out/drafter_paths.json')); HT = paths['trees']['head']; D = HT + '/Blockchain/Dev'
print('drafter_openapi_1032', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
p = subprocess.run(['npm', 'run', 'generate-openapi', '--', '--check'], cwd=D, capture_output=True, text=True)
print('generate-openapi --check rc', p.returncode, '| tail:', (p.stdout + p.stderr).strip()[-600:])
y = open(D + '/docs/openapi/secuura-api.yaml').read().splitlines()
paths_ = [l for l in y if re.match(r'^  /api/', l)]
print('YAML paths', len(paths_), '| /api/users/* paths', sum(bool(re.match(r'^  /api/users', l, re.I)) for l in paths_), '| containing "verification" under /api/users', [l.strip() for l in paths_ if re.match(r'^  /api/users', l, re.I) and 'verification' in l.lower()], '| control /api/users/me: present', any(l.strip().lower() == '/api/users/me:' for l in paths_))
a = open(D + '/services/auth/src/auth.openapi.ts').read()
print('auth.openapi.ts: path strings containing verification', sorted(set(m for m in re.findall(r"path:\s*'([^']+)'", a) if 'verification' in m.lower())), '| control path count', len(re.findall(r"path:\s*'", a)))
print('git diff --quiet after (tracked files unchanged by the generator):', subprocess.run(['git', '-C', HT, 'diff', '--quiet', 'HEAD'], capture_output=True).returncode, '| porcelain', subprocess.run(['git', '-C', HT, 'status', '--porcelain'], capture_output=True, text=True).stdout.strip().replace('\n', ' | '))
