#!/usr/bin/env python3
"""overlaps_gate49a.py — the drafter's READ behind COLLISION-CENSUS's second half: "does each overlapping PR still apply after ITEM A merges?"
For every PR the census (gh_read_1.json; or --census <file>, e.g. the pre-pin gh_read_census_prepin.json) lists as touching one of the 18 locks
or carrying a census key (nothing is sequenced), in the SCRATCH clone only (<scratchpad>/g49a_sp/clone; `git fetch origin
+refs/pull/<n>/head:refs/remotes/pr/<n>`, never the checkout):
  O1 the fetched head == the head the PULLS API read, or the row says STALE READ;
  O2 TODAY: `git merge-tree --write-tree develop <head>` — clean / CONFLICT (with the conflicted paths), and how far behind develop it is;
  O3 AFTER ITEM A: the same over the simulated squash (pins squash_sim, tree END_TREE) — clean / CONFLICT and the conflicted paths;
  O4 RESIDUE: when O3 is clean, the paths the PR would still change on top of END (diff(END, merged tree)) — EMPTY means superseded;
  O5 whether the PR's own diff of any of the 18 locks touches a brace-expansion / fast-uri / ip-address entry (the entries ITEM A moves) —
     a dependabot bump that re-resolves those entries could RE-INTRODUCE a vulnerable version after ITEM A: O5 names each such PR.
A CONFLICT here is the textual fact only; whether the PR "still applies" is the gate's ruling. Controls: CT-CLEAN a plant (develop + one unrelated
path) reads clean over END; CT-CONFLICT a plant that edits the root lock's fast-uri version line reads CONFLICT over END (the instrument can print
both). rc 0 OVERLAPS READ (controls hold) / rc 1. Usage: overlaps_gate49a.py <scratchpad> [--pins <name>] [--census <file>]"""
import json, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
A = sys.argv[1:]; SP = A[0]
PF = 'pins_gate49a.SIM-%s.json' % A[A.index('--pins') + 1] if '--pins' in A else 'pins_gate49a.json'
P = json.load(open(os.path.join(G, PF), encoding='utf-8'))
CF = A[A.index('--census') + 1] if '--census' in A else os.path.join(G, 'gh_read_1.json'); GH = json.load(open(CF, encoding='utf-8'))
CL = os.path.join(SP, 'g49a_sp', 'clone'); SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
N = P['pr']; DEV = P['develop']; SQ = P['squash_sim']; END = P['end_tree']; FILES = K['prs'][N if N in K['prs'] else '<PR>']['files']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate49a sim', GIT_AUTHOR_EMAIL='sim@gate49a.invalid', GIT_COMMITTER_NAME='gate49a sim',
           GIT_COMMITTER_EMAIL='sim@gate49a.invalid', GIT_AUTHOR_DATE='2026-09-30T00:00:00Z', GIT_COMMITTER_DATE='2026-09-30T00:00:00Z')
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
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
hits = {n: r for n, r in GH['census'].items() if r['kit_paths_touched'] or r['census_keys_in_title']}
print('overlaps_gate49a %s | develop %s | #%s squash_sim %s (END_TREE %s) | pins %s | %d overlapping PR(s) from %s (read %s)' % (now(), DEV[:12], N, SQ[:12], END, PF, len(hits), os.path.basename(CF), GH['read_at']))
if hits: git('fetch', '-q', 'origin', *['+refs/pull/%s/head:refs/remotes/pr/%s' % (n, n) for n in sorted(hits, key=int)])
rows = {}
for n in sorted(hits, key=int, reverse=True):
    r = hits[n]; h = git('rev-parse', 'refs/remotes/pr/%s' % n).stdout.strip()
    mb = git('merge-base', DEV, h, ok=(0, 1)).stdout.strip(); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)).stdout) if mb else -1
    rc0, t0, c0 = mt(DEV, h); rc1, t1, c1 = mt(SQ, h)
    res = git('diff', '--name-only', END, t1).stdout.split() if rc1 == 0 else []
    own = git('diff', '--name-only', mb, h).stdout.split() if mb else []
    touch = []
    for lk in FILES:
        if lk in own:
            d = git('diff', '-U0', mb, h, '--', lk).stdout
            touch += ['%s:%s' % (lk.replace('/package-lock.json', ''), p) for p in K['packages'] if ('node_modules/%s"' % p) in d or ('/%s/-/%s-' % (p, p)) in d]
    rows[n] = dict(user=r['user'], title=r['title'], head=h, api_head=r['head'], behind=behind, today=('clean' if rc0 == 0 else 'CONFLICT'), today_conf=c0,
                   after=('clean' if rc1 == 0 else 'CONFLICT'), after_conf=c1, residue=res, pkg_touch=touch, kit_paths=r['kit_paths_touched'], keys=r['census_keys_in_title'])
    print('  #%-5s %-15s behind %-4s | today %-8s%s | after ITEM A %-8s%s | residue on END: %s | touches the moved packages: %s | %s%s' % (
        n, r['user'][:15], behind, rows[n]['today'], (' ' + str(c0)) if c0 else '', rows[n]['after'], (' ' + str(c1)) if c1 else '',
        ('%d path(s) %s' % (len(res), res[:3])) if rc1 == 0 else 'n/a (conflict)', touch or 'no', r['title'][:70], '' if h == r['head'] else ' | STALE READ: fetched %s != API %s' % (h[:12], r['head'][:12])))
W = os.path.join(SP, 'g49a_sp', 'overlaps_ctl_' + datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')); os.makedirs(W, exist_ok=True)
def plant(par, path, fn):
    blob = git('show', '%s:%s' % (par, path)).stdout; nb = fn(blob); fp = os.path.join(W, 'blob'); open(fp, 'w').write(nb)
    oid = git('hash-object', '-w', fp).stdout.strip(); idx = os.path.join(W, 'idx.%d' % len(os.listdir(W))); e = dict(ENV, GIT_INDEX_FILE=idx)
    for c in (['read-tree', par], ['update-index', '--cacheinfo', '100644,%s,%s' % (oid, path)]): subprocess.run(['git', '-C', CL] + c, env=e, check=True, capture_output=True)
    t = subprocess.run(['git', '-C', CL, 'write-tree'], env=e, check=True, capture_output=True, text=True).stdout.strip()
    return git('commit-tree', t, '-p', par, '-m', 'gate49a overlaps control plant').stdout.strip()
pc = plant(DEV, 'Blockchain/Dev/BACKLOG.md', lambda s: s + '\n<!-- gate49a overlaps control: unrelated -->\n')
def fu(s):
    a = '"node_modules/fast-uri": {\n      "version": "3.1.7"'; assert a in s, 'fast-uri 3.1.7 anchor absent at develop'
    return s.replace(a, '"node_modules/fast-uri": {\n      "version": "3.1.9"', 1)
pk = plant(DEV, 'Blockchain/Dev/package-lock.json', fu)
a, _, _ = mt(SQ, pc); b, _, cb = mt(SQ, pk); ok = a == 0 and b == 1
print('CT-CLEAN an unrelated plant over the squash: %s | CT-CONFLICT a root-lock fast-uri-line plant over the squash: %s %s -> %s' % ('clean' if a == 0 else 'CONFLICT', 'clean' if b == 0 else 'CONFLICT', cb, 'OK' if ok else 'FAIL'))
json.dump(dict(read_at=now(), develop=DEV, squash_sim=SQ, pins=PF, census=os.path.basename(CF), rows=rows), open(os.environ.get('G49A_OVJSON') or os.path.join(G, 'overlaps_gate49a.json'), 'w'), indent=1)
nc = sum(1 for x in rows.values() if x['after'] == 'CONFLICT'); nt = sum(1 for x in rows.values() if x['today'] == 'CONFLICT')
print('OVERLAPS %s: %d PR(s) | conflict today %d | conflict after ITEM A %d | empty residue (superseded) %d | touching the moved packages %d' % (
    'READ' if ok else 'FAILED', len(rows), nt, nc, sum(1 for x in rows.values() if x['after'] == 'clean' and not x['residue']), sum(1 for x in rows.values() if x['pkg_touch'])))
raise SystemExit(0 if ok else 1)
