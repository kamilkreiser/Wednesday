#!/usr/bin/env python3
"""overlaps_gate49b.py — the drafter's READ behind COLLISION-CENSUS's second half: "does each overlapping PR still apply after this batch merges,
and would it UNDO #1358?" For every PR the census (gh_read_1.json) lists as touching a kit path or carrying a census key (nothing is sequenced),
in the SCRATCH clone only (<scratchpad>/g49b_sp/clone; `git fetch origin +refs/pull/<n>/head:refs/remotes/pr/<n>`, never the checkout):
  O1 the fetched head == the head the PULLS API read, or the row says STALE READ;
  O2 TODAY: `git merge-tree --write-tree develop <head>` — clean / CONFLICT (with the conflicted paths), and how far behind develop it is;
  O3 AFTER THE BATCH: the same over the simulated END chain tip (pins squash_sim, tree END_TREE) — clean / CONFLICT and the conflicted paths;
  O4 RESIDUE: when O3 is clean, the paths the PR would still change on top of END (diff(END, merged tree)) — EMPTY means superseded;
  O5 whether the PR's own diff of a kit lock touches an @types/express-serve-static-core or @types/pg entry (the entries #1358 moves);
  O6 RE-DISAGREE (the #1358 post-merge audit rows, from gh_read_1.json audit_census): when O3 is clean, the lock-agreement read (every tracked lock vs packages/shared, top-level) on the MERGED tree: a PR that
     would leave >= 1 lock disagreeing after the batch (END reads 0) is named — it would re-open KS-1380 if merged after #1358.
A CONFLICT is the textual fact only; whether the PR "still applies" is the gate's ruling. Controls: CT-CLEAN a plant (develop + one unrelated path)
reads clean over END; CT-CONFLICT a plant that edits deploy.sh's rc-1 message line (a #1359 path) reads CONFLICT over END; CT-AGREE a plant that moves
one service lock's @types/pg back to 8.20.0 reads 1 disagreeing lock on the merged tree (O6 can fire). rc 0 OVERLAPS READ (controls hold) / rc 1.
Usage: overlaps_gate49b.py <scratchpad> [--pins <name>]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
PF = 'pins_gate49b.SIM-%s.json' % A[A.index('--pins') + 1] if '--pins' in A else 'pins_gate49b.json'
P = json.load(open(os.path.join(G, PF), encoding='utf-8')); GH = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))
CL = os.path.join(SP, 'g49b_sp', 'clone'); SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
DEV = P['develop']; SQ = P['squash_sim']; END = P['end_tree']; FILES = sorted(P['union']); PKGS = K['types_packages']; SHL = K['shared_lock']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate49b sim', GIT_AUTHOR_EMAIL='sim@gate49b.invalid', GIT_COMMITTER_NAME='gate49b sim',
           GIT_COMMITTER_EMAIL='sim@gate49b.invalid', GIT_AUTHOR_DATE='2026-09-30T00:00:00Z', GIT_COMMITTER_DATE='2026-09-30T00:00:00Z')
def git(*a, ok=(0,)):
    r = subprocess.run(['git', '-C', CL, '-c', 'core.sshCommand=' + SSH] + list(a), capture_output=True, text=True, env=ENV)
    if r.returncode not in ok: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a[:4]), r.returncode, r.stderr.strip()[:300]))
    return r
def mt(base, head):
    r = git('merge-tree', '--write-tree', '--name-only', base, head, ok=(0, 1))
    ls = r.stdout.splitlines(); tree = ls[0].strip() if ls else ''; conf = []
    if r.returncode:
        for l in ls[1:]:
            if not l.strip(): break
            conf.append(l.strip())
    return r.returncode, tree, sorted(set(conf))
def disagree(tree):
    ref = {pk: (json.loads(git('show', '%s:%s' % (tree, SHL)).stdout)['packages'].get('node_modules/' + pk) or {}).get('version') for pk in PKGS}
    locks = [l for l in git('ls-tree', '-r', '--name-only', tree, '--', 'Blockchain/Dev').stdout.splitlines() if l.endswith('/package-lock.json') and l != SHL]
    bad = []
    for l in locks:
        try: pk = json.loads(git('show', '%s:%s' % (tree, l)).stdout)['packages']
        except Exception: continue
        for x in PKGS:
            v = (pk.get('node_modules/' + x) or {}).get('version')
            if v is not None and v != ref[x]: bad.append('%s %s %s!=%s' % (l.replace('Blockchain/Dev/', ''), x, v, ref[x]))
    return bad
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
hits = {n: r for n, r in GH['census'].items() if r['kit_paths_touched'] or r['census_keys_in_title']}
hits.update({n: dict(r, audit=True) for n, r in (GH.get('audit_census') or {}).items() if n not in hits})   # the #1358 post-merge audit census (reported only)
print('overlaps_gate49b %s | develop %s | squash_sim %s (END_TREE %s) | pins %s | %d overlapping PR(s) from gh_read_1.json (read %s) | END disagreeing locks: %d' % (
    now(), DEV[:12], SQ[:12], END, PF, len(hits), GH['read_at'], len(disagree(END))))
if hits: git('fetch', '-q', 'origin', *['+refs/pull/%s/head:refs/remotes/pr/%s' % (n, n) for n in sorted(hits, key=int)])
rows = {}
for n in sorted(hits, key=int, reverse=True):
    r = hits[n]; h = git('rev-parse', 'refs/remotes/pr/%s' % n).stdout.strip()
    mb = git('merge-base', DEV, h, ok=(0, 1)).stdout.strip(); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)).stdout) if mb else -1
    rc0, t0, c0 = mt(DEV, h); rc1, t1, c1 = mt(SQ, h)
    res = git('diff', '--name-only', END, t1).stdout.split() if rc1 == 0 else []
    own = git('diff', '--name-only', mb, h).stdout.split() if mb else []
    touch = []
    for lk in own:
        if lk.endswith('package-lock.json'):
            d = git('diff', '-U0', mb, h, '--', lk).stdout
            touch += ['%s:%s' % (lk.replace('Blockchain/Dev/', '').replace('/package-lock.json', '') or 'root', p) for p in PKGS if ('node_modules/%s"' % p) in d or ('/%s/-/' % p.split('/')[-1]) in d and p.split('/')[0] in d]
    dis = disagree(t1) if rc1 == 0 else None
    rows[n] = dict(audit=bool(r.get('audit')), user=r['user'], title=r['title'], head=h, api_head=r['head'], behind=behind, today=('clean' if rc0 == 0 else 'CONFLICT'), today_conf=c0,
                   after=('clean' if rc1 == 0 else 'CONFLICT'), after_conf=c1, residue=res, types_touch=sorted(set(touch)), disagree_after=dis, kit_paths=r['kit_paths_touched'], keys=r['census_keys_in_title'])
    print('  %s' % ('AUDIT-ROW ' if r.get('audit') else 'KIT-ROW '), end='')
    print('#%-5s %-15s behind %-4s | today %-8s%s | after the batch %-8s%s | residue on END: %s | touches @types esc/pg: %s | disagreeing locks if merged after: %s | %s%s' % (
        n, r['user'][:15], behind, rows[n]['today'], (' ' + str(c0)) if c0 else '', rows[n]['after'], (' ' + str(c1)) if c1 else '',
        ('%d path(s)' % len(res)) if rc1 == 0 else 'n/a (conflict)', rows[n]['types_touch'] or 'no', ('%d %s' % (len(dis), dis[:3])) if dis is not None else 'n/a (conflict)',
        r['title'][:60], '' if h == r['head'] else ' | STALE READ: fetched %s != API %s' % (h[:12], r['head'][:12])))
W = os.path.join(SP, 'g49b_sp', 'overlaps_ctl_' + datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')); os.makedirs(W, exist_ok=True)
def plant(par, path, fn):
    blob = git('show', '%s:%s' % (par, path)).stdout; nb = fn(blob); fp = os.path.join(W, 'blob'); open(fp, 'w').write(nb)
    oid = git('hash-object', '-w', fp).stdout.strip(); idx = os.path.join(W, 'idx.%d' % len(os.listdir(W))); e = dict(ENV, GIT_INDEX_FILE=idx)
    for c in (['read-tree', par], ['update-index', '--cacheinfo', '100644,%s,%s' % (oid, path)]): subprocess.run(['git', '-C', CL] + c, env=e, check=True, capture_output=True)
    t = subprocess.run(['git', '-C', CL, 'write-tree'], env=e, check=True, capture_output=True, text=True).stdout.strip()
    return git('commit-tree', t, '-p', par, '-m', 'gate49b overlaps control plant').stdout.strip()
pc = plant(DEV, 'Blockchain/Dev/BACKLOG.md', lambda s: s + '\n<!-- gate49b overlaps control: unrelated -->\n')
def pgline(s):
    a = '"node_modules/@types/pg": {\n      "version": "8.20.0"'; assert a in s, '@types/pg 8.20.0 anchor absent in the root lock at develop'
    return s.replace(a, '"node_modules/@types/pg": {\n      "version": "8.22.0"', 1)
def dline(s):
    a = 'startup migrations FAILED — see above'; assert a in s, 'deploy.sh message anchor absent at develop'
    return s.replace(a, 'startup migrations FAILED (control) — see above', 1)
pk = plant(DEV, 'Blockchain/Dev/deployment/azure/deploy.sh', dline)
def back(s):
    a = '"node_modules/@types/pg": {\n      "version": "8.23.1"'; assert a in s, '@types/pg 8.23.1 anchor absent in the kyc lock at END'
    return s.replace(a, '"node_modules/@types/pg": {\n      "version": "8.20.0"', 1)
pa = plant(SQ, 'Blockchain/Dev/services/kyc/package-lock.json', back)
a, _, _ = mt(SQ, pc); b, _, cb = mt(SQ, pk); dz = disagree(git('rev-parse', pa + '^{tree}').stdout.strip())
ok = a == 0 and b == 1 and len(dz) == 1
print('CT-CLEAN an unrelated plant over the batch: %s | CT-CONFLICT a deploy.sh message-line plant (a #1359 path): %s %s | CT-AGREE kyc @types/pg back to 8.20.0 on END: %d disagreeing %s -> %s' % (
    'clean' if a == 0 else 'CONFLICT', 'clean' if b == 0 else 'CONFLICT', cb, len(dz), dz, 'OK' if ok else 'FAIL'))
json.dump(dict(read_at=now(), develop=DEV, squash_sim=SQ, pins=PF, rows=rows), open(os.environ.get('G49B_OVJSON') or os.path.join(G, 'overlaps_gate49b.json'), 'w'), indent=1)
nc = sum(1 for x in rows.values() if x['after'] == 'CONFLICT'); nt = sum(1 for x in rows.values() if x['today'] == 'CONFLICT')
nd = sum(1 for x in rows.values() if x['disagree_after'])
print('OVERLAPS %s: %d PR(s) (%d on the kit paths, %d on the #1358 audit locks) | conflict today %d | conflict after the batch %d | empty residue (superseded) %d | touching @types esc/pg %d | would re-open a lock disagreement %d' % (
    'READ' if ok else 'FAILED', len(rows), sum(1 for x in rows.values() if not x['audit']), sum(1 for x in rows.values() if x['audit']), nt, nc, sum(1 for x in rows.values() if x['after'] == 'clean' and not x['residue']), sum(1 for x in rows.values() if x['types_touch']), nd))
raise SystemExit(0 if ok else 1)
