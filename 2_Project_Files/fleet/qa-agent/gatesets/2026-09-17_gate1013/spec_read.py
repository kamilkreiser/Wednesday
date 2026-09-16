#!/usr/bin/env python3
"""spec_read.py — READ-ONLY: which of the calling routes are documented in docs/openapi/*.yaml at head, and do they document 503? git show by SHA only."""
import subprocess, re, datetime
R = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; H = '5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2'
print('spec_read', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
ls = subprocess.run(['git', '-C', R, 'ls-tree', '-r', '--name-only', H, 'Blockchain/Dev/docs/openapi/'], capture_output=True, text=True).stdout.split()
print('docs/openapi files', ls)
ROUTES = ['/api/users/me', '/api/auth/me', '/api/users/me/change-password', '/api/users/me/mfa/enable', '/api/users/me/verification', '/api/users/admin/{id}', '/api/auth/mfa/status', '/api/auth/mfa/setup/start', '/api/auth/mfa/backup-codes/regenerate', '/api/auth/wallet/unlink', '/api/auth/wallet/link', '/api/auth/login', '/api/auth/social/link', '/api/oauth/token', '/api/oauth/authorize', '/api/auth/register', '/api/auth/reset-password', '/api/auth/verify-email']
for f in ls:
    if not f.endswith(('.yaml', '.yml')): continue
    t = subprocess.run(['git', '-C', R, 'show', H + ':' + f], capture_output=True, text=True).stdout
    lines = t.split('\n')
    print('\n', f, 'lines', len(lines), '| control ^paths:', sum(1 for l in lines if l.startswith('paths:')), '| control /api/documents', t.count('/api/documents'), "| '503' total", t.count("'503'") + t.count('"503"') + len(re.findall(r'^\s+503:', t, re.M)))
    # split paths block into path entries (two-space indent keys)
    idx = [(i, l.strip().rstrip(':').strip("'\"")) for i, l in enumerate(lines) if re.match(r'^  /', l)]
    for r in ROUTES:
        hits = [(i, p) for i, p in idx if p == r or p.rstrip('/') == r]
        if not hits: print('   %-42s absent' % r); continue
        for i, p in hits:
            nxt = [j for j, _ in idx if j > i]; end = nxt[0] if nxt else len(lines)
            block = '\n'.join(lines[i:end])
            codes = sorted(set(re.findall(r"^\s+'?\"?(\d{3})'?\"?:", block, re.M)))
            print('   %-42s line %d statuses %s' % (r, i + 1, codes))
