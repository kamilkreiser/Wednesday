#!/usr/bin/env python3
"""overlap_probe_gate47.py — the drafter's measurement of the OUT-OF-KIT open PR the launch action's census refuses on (rc 15): #1351 (KS-1386,
opened 2026-09-29T14:37:24Z by PeterObeden, 2 commits, based on 8c810023f9c9). In the SCRATCH clone only (<scratchpad>/g47_sp/clone; its
refs/remotes/pr/1351 fetched there by `git fetch origin +refs/pull/1351/head:…` — never the checkout): `git merge-tree --write-tree` of #1351
alone over develop, of #1351 against each kit head, and of #1351 over the kit's simulated END (the two squashes, commit-tree on a scratch
commit — the same plumbing pin_gate47.py uses); which kit paths and which CITED LINES (the drafted KS-1374 text's and the PR bodies' line
references) #1351 changes. Writes nothing but its stdout. Usage: overlap_probe_gate47.py <scratchpad> [<pr>=1351]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate47.json'), encoding='utf-8'))
SP = sys.argv[1]; N = sys.argv[2] if len(sys.argv) > 2 else '1351'; CL = os.path.join(SP, 'g47_sp', 'clone')
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate47 sim', GIT_AUTHOR_EMAIL='sim@gate47.invalid', GIT_COMMITTER_NAME='gate47 sim', GIT_COMMITTER_EMAIL='sim@gate47.invalid',
           GIT_AUTHOR_DATE='2026-09-30T00:00:00Z', GIT_COMMITTER_DATE='2026-09-30T00:00:00Z')
def git(*a, check=True):
    r = subprocess.run(['git', '-C', CL] + list(a), capture_output=True, text=True, env=ENV)
    if check and r.returncode: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a), r.returncode, r.stderr.strip()[:300]))
    return r.stdout.strip()
def mt(a, b):
    r = subprocess.run(['git', '-C', CL, 'merge-tree', '--write-tree', '--name-only', a, b], capture_output=True, text=True, env=ENV)
    lines = r.stdout.split('\n'); return r.returncode, lines[0].strip(), [l for l in lines[1:] if l.strip()][:12]
DEV = P['develop']; H = git('rev-parse', 'refs/remotes/pr/%s' % N); MB = git('merge-base', DEV, H)
print('overlap_probe_gate47 %s | #%s head %s | merge-base %s | behind develop %s | ahead %s | %s path(s) changed' % (
    datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), N, H, MB[:12], git('rev-list', '--count', '%s..%s' % (H, DEV)),
    git('rev-list', '--count', '%s..%s' % (MB, H)), len(git('diff', '--name-only', MB, H).splitlines())))
names = set(git('diff', '--name-only', MB, H).splitlines())
for n in K['order']:
    hit = sorted(names & set(K['prs'][n]['files']))
    print('  kit #%s paths changed by #%s: %s' % (n, N, hit or 'NONE'))
rc, t, c = mt(DEV, H); print('  #%s ALONE over develop %s: merge-tree rc %d %s' % (N, DEV[:12], rc, ('tree ' + t) if rc == 0 else ('CONFLICT ' + ' | '.join(c))))
for n in K['order']:
    rc, t, c = mt(P['prs'][n]['head'], H); print('  #%s x kit #%s head: merge-tree rc %d %s' % (N, n, rc, 'clean' if rc == 0 else ('CONFLICT ' + ' | '.join(c))))
chain = P.get('chain') or []
tip = chain[-1]['squash_sim'] if chain else None
if tip and git('rev-parse', '--verify', '-q', tip + '^{commit}', check=False):
    rc, t, c = mt(tip, H); print('  #%s over the kit END (simulated squash %s, tree %s): merge-tree rc %d %s' % (N, tip[:12], P['end_tree'][:12], rc, ('tree ' + t) if rc == 0 else ('CONFLICT ' + ' | '.join(c))))
else: print('  the kit END squash commit is not in this clone — re-run pin_gate47.py first')
for f in ['systemTest/akto/src/setup/aktoRateLimit.ts', 'systemTest/akto/src/config/index.ts', 'systemTest/akto/src/scan/scanOptions.ts', 'systemTest/akto/.env.example',
          'systemTest/akto/docs/configuration.md', 'systemTest/slot-target.sh', 'systemTest/akto/src/setup/secuuraAuth.ts',
          'systemTest/akto/tests/unit/setup/ks1374-platform-limit-from-env.test.ts', 'systemTest/akto/tests/unit/setup/aktoRateLimit.test.ts']:
    ch = f in names; ns = git('diff', '--numstat', MB, H, '--', f) if ch else ''
    print('  %-72s changed by #%s: %s' % (f, N, ('YES +%s/-%s' % tuple(ns.split('\t')[:2])) if ch else 'no'))
def find(t, f, s):
    return [('%d' % (i + 1)) for i, l in enumerate(git('show', '%s:%s' % (t, f)).splitlines()) if s in l]
for lab, f, s in [('isLocalScanTarget raw line', 'systemTest/akto/src/setup/aktoRateLimit.ts', 'const raw = env('),
                  ('scanOptions precedence', 'systemTest/akto/src/scan/scanOptions.ts', 'config.overrideAppUrl || config.secuuraUrl'),
                  ('config overrideAppUrl', 'systemTest/akto/src/config/index.ts', "overrideAppUrl: env('OVERRIDE_APP_URL')"),
                  ('.env.example OVERRIDE_APP_URL=', 'systemTest/akto/.env.example', 'OVERRIDE_APP_URL='),
                  ('configuration.md "when testing against a different environment"', 'systemTest/akto/docs/configuration.md', 'when testing against a different environment')]:
    print('  %-66s #1349 head :%s | #%s head :%s' % (lab, ','.join(find(P['prs']['1349']['head'], f, s)) or 'ABSENT', N, ','.join(find(H, f, s)) or 'ABSENT'))
print('PROBE DONE: #%s touches %d kit path(s)' % (N, len(names & set(p for n in K['order'] for p in K['prs'][n]['files']))))
