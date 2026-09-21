#!/usr/bin/env python3
"""dev_move_reads_gate15.py — READ-ONLY GitHub GETs on the develop move 581ed7fa1 -> <current origin develop> (the head is NOT in the local
object store; a fetch is a write — read via the API): the compare (commits, files, +/-), PR #1138 (the suspected squash), and the intersection
of the moved files with this round's 11 paths + the paths the gate reads (hook, preflight.sh, run-shell-suites.sh, the four lanes' package.json /
lock / vitest / jest / tsconfig, jwt.ts, provenance.ts, proxy.ts). GH_TOKEN by NAME; never printed. stdout only."""
import json, os, subprocess, sys, urllib.request, urllib.error
print('date', subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip())
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok
REPO = 'https://api.github.com/repos/Secuura/Distributed_Secuura/'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
OLD = '581ed7fa124b85c7c2da89ac05d52f99c2502911'
cur = subprocess.run(['git', '-C', '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files', 'ls-remote', 'origin', 'refs/heads/develop'], capture_output=True, text=True).stdout.split()[0]
print('origin develop now', cur, '| pinned-at-raise', OLD, '| moved', cur != OLD)
D = 'Blockchain/Dev/'
MINE = {D + 'docs/DEV-PROCESS.md', D + 'CONTRIBUTING.md', D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md', 'CLAUDE.md', D + 'deployment/DEPLOYMENT-ARCHITECTURE.md',
        D + 'packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts', D + 'packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts',
        D + 'services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts', D + 'services/originate/src/__tests__/ks597-issuer-org-bind.test.ts',
        D + 'services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts', D + 'services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts'}
READS = {'.githooks/pre-push', D + 'scripts/preflight/preflight.sh', D + 'scripts/run-shell-suites.sh', D + 'services/auth/src/services/jwt.ts', D + 'services/originate/src/services/provenance.ts', D + 'services/api-gateway/src/routes/proxy.ts',
         D + 'package.json', D + 'package-lock.json', D + 'eslint.config.mjs'}
for lane in ('packages/shared', 'services/originate', 'services/vc-issuer', 'services/api-gateway'):
    for f in ('package.json', 'package-lock.json', 'tsconfig.json', 'vitest.config.ts', 'jest.config.js', 'jest.config.ts', 'jest.config.cjs'): READS.add(D + lane + '/' + f)
if cur != OLD:
    c = get(REPO + 'compare/' + OLD + '...' + cur)
    files = c.get('files') or []
    print('compare %s...%s: status %s ahead %d behind %d commits %d files %d' % (OLD[:9], cur[:9], c.get('status'), c['ahead_by'], c['behind_by'], len(c.get('commits') or []), len(files)))
    for cm in c.get('commits') or []: print('  commit %s %s | %s' % (cm['sha'][:9], (cm['commit'].get('committer') or {}).get('date'), cm['commit']['message'].splitlines()[0][:120]))
    for f in files: print('  %-8s +%-4d -%-4d %s' % (f['status'], f['additions'], f['deletions'], f['filename']))
    paths = {f['filename'] for f in files}
    print('∩ this round 11 paths:', sorted(paths & MINE) or 'NONE', '| ∩ the paths the gate reads / runs:', sorted(paths & READS) or 'NONE')
    lanes_hit = sorted({p.split('/')[2] + '/' + p.split('/')[3] for p in paths if p.startswith(D + 'services/') or p.startswith(D + 'packages/')} - set())
    print('lanes touched by the move (services/<x> or packages/<x>):', lanes_hit or 'NONE', '| any of shared / originate / vc-issuer / api-gateway:', sorted(x for x in lanes_hit if x.split('/')[1] in ('shared', 'originate', 'vc-issuer', 'api-gateway')) or 'NONE')
for n in (1138,):
    try:
        p = get(REPO + 'pulls/%d' % n); print('PR #%d: state %s merged %s merged_at %s merge_commit %s title %r head %s branch %s base %s' % (n, p['state'], p.get('merged'), p.get('merged_at'), (p.get('merge_commit_sha') or '')[:9], (p.get('title') or '')[:100], p['head']['sha'][:9], p['head']['ref'][:80], p['base']['ref']))
        fl = get(REPO + 'pulls/%d/files?per_page=100' % n); print('  files', [(f['filename'], f['additions'], f['deletions']) for f in fl])
    except urllib.error.HTTPError as e: print('PR #%d HTTP %s' % (n, e.code))
# every one of the 11 target blobs at the CURRENT develop (contents API sha == git blob sha)
print('--- the 11 target blobs at the current develop (contents API)')
want = {D + 'docs/DEV-PROCESS.md': 'c9cd41d588a2', D + 'CONTRIBUTING.md': '953067eb7aa7', D + 'deployment/KINTSUGI-DEV-SERVER-PLAN.md': 'bbd5bbf78778', 'CLAUDE.md': 'dd782eab7435', D + 'deployment/DEPLOYMENT-ARCHITECTURE.md': 'daabe1087bb9',
        D + 'packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts': '7f0ac617f675', D + 'packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts': 'ab8e46d795d2',
        D + 'services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts': 'eb7782db8816', D + 'services/originate/src/__tests__/ks597-issuer-org-bind.test.ts': '9bb899a10677',
        D + 'services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts': 'eb0e5305c815', D + 'services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts': '548e1ec1217e'}
ok = 0
for p, b in want.items():
    s = get(REPO + 'contents/' + p + '?ref=' + cur)['sha']; ok += s.startswith(b); print('  %-100s %s == %s %s' % (p, s[:12], b, s.startswith(b)))
print('identical at the current develop:', ok, 'of 11')
