#!/usr/bin/env python3
"""overlaps_gate48b.py — the drafter's READ behind OUT-OF-KIT-CENSUS's second half: "does each overlapping PR still apply after #1355 merges?"
For every PR gh_read_1.json lists as touching a kit path or carrying a census key (the census; nothing is sequenced), in the SCRATCH clone only
(<scratchpad>/g48b_sp/clone; `git fetch origin +refs/pull/<n>/head:refs/remotes/pr/<n>`, never the checkout):
  O1 the fetched head == the head the PULLS API read (gh_read_1.json), or the row says STALE READ;
  O2 TODAY: `git merge-tree --write-tree develop <head>` — clean / CONFLICT (with the conflicted paths), and the PR's merge-base age (behind develop);
  O3 AFTER #1355: the same over the simulated squash (pins squash_sim, tree END_TREE) — clean / CONFLICT and the conflicted paths;
  O4 RESIDUE: when O3 is clean, the paths the PR would still change on top of END (diff(END, merged tree)) — an EMPTY residue means the PR's whole
     effect is already in END (superseded); for #1354 the residue must be exactly its audit-baseline row (the js-yaml blob is #1355's);
  O5 whether the PR's own diff of the root / issuer lock touches an `undici` or `@fastify/busboy` entry (the entries #1355 moves).
A CONFLICT here is the textual fact only; whether the PR "still applies" (its bump still wanted) is the gate's ruling — the drafter rules none.
Controls: CT-CLEAN a PR-shaped plant (develop + one unrelated path) reads clean over END; CT-CONFLICT a plant that edits the root lock's undici
line reads CONFLICT over END (the instrument can print both). rc 0 OVERLAPS READ (controls hold) / rc 1. Usage: overlaps_gate48b.py <scratchpad>"""
import json, os, subprocess, sys, datetime, re
G = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
P = json.load(open(os.path.join(G, 'pins_gate48b.json'), encoding='utf-8')); GH = json.load(open(os.path.join(G, 'gh_read_1.json'), encoding='utf-8'))
SP = sys.argv[1]; CL = os.path.join(SP, 'g48b_sp', 'clone'); SSH = 'ssh -i "%s" -o IdentitiesOnly=yes' % K['deploy_key']
N = '1354 then #1355'; DEV = P['develop']; SQ = P['squash_sim']; END = P['end_tree']
ENV = dict(os.environ, GIT_AUTHOR_NAME='gate48b sim', GIT_AUTHOR_EMAIL='sim@gate48b.invalid', GIT_COMMITTER_NAME='gate48b sim',
           GIT_COMMITTER_EMAIL='sim@gate48b.invalid', GIT_AUTHOR_DATE='2026-09-30T00:00:00Z', GIT_COMMITTER_DATE='2026-09-30T00:00:00Z')
def git(*a, ok=(0,)):
    r = subprocess.run(['git', '-C', CL, '-c', 'core.sshCommand=' + SSH] + list(a), capture_output=True, text=True, env=ENV)
    if r.returncode not in ok: raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a[:4]), r.returncode, r.stderr.strip()[:300]))
    return r
def mt(base, head):
    r = git('merge-tree', '--write-tree', '--name-only', base, head, ok=(0, 1))
    ls = r.stdout.splitlines(); tree = ls[0].strip() if ls else ''
    conf = []
    if r.returncode:   # --name-only: line 1 the tree, then one conflicted path per line up to the first blank line, then the messages
        for l in ls[1:]:
            if not l.strip(): break
            conf.append(l.strip())
    return r.returncode, tree, sorted(set(conf))
now = lambda: datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
hits = {n: r for n, r in GH['census'].items() if r['kit_paths_touched'] or r['census_keys_in_title']}
print('overlaps_gate48b %s | develop %s | #%s squash_sim %s (END_TREE %s) | %d overlapping PR(s) from gh_read_1.json (read %s)' % (now(), DEV[:12], N, SQ[:12], END, len(hits), GH['read_at']))
git('fetch', '-q', 'origin', *['+refs/pull/%s/head:refs/remotes/pr/%s' % (n, n) for n in sorted(hits, key=int)])
LOCKS = ('Blockchain/Dev/package-lock.json', 'Blockchain/Dev/frontend/issuer/package-lock.json')
rows = {}
for n in sorted(hits, key=int, reverse=True):
    r = hits[n]; h = git('rev-parse', 'refs/remotes/pr/%s' % n).stdout.strip()
    mb = git('merge-base', DEV, h, ok=(0, 1)).stdout.strip(); behind = int(git('rev-list', '--count', '%s..%s' % (mb, DEV)).stdout) if mb else -1
    rc0, t0, c0 = mt(DEV, h); rc1, t1, c1 = mt(SQ, h)
    res = git('diff', '--name-only', END, t1).stdout.split() if rc1 == 0 else []
    own = git('diff', '--name-only', mb, h).stdout.split() if mb else []
    touch = []
    for lk in LOCKS:
        if lk in own:
            d = git('diff', '-U0', mb, h, '--', lk).stdout
            touch += ['%s:%s' % (lk.split('/')[-2] if lk.count('/') > 2 else 'root', k) for k in ('node_modules/undici"', 'node_modules/@fastify/busboy"', 'jsdom/node_modules/undici"') if k in d]
    rows[n] = dict(user=r['user'], title=r['title'], head=h, api_head=r['head'], behind=behind, today=('clean' if rc0 == 0 else 'CONFLICT'), today_conf=c0,
                   after=('clean' if rc1 == 0 else 'CONFLICT'), after_conf=c1, residue=res, undici_touch=touch, kit_paths=r['kit_paths_touched'], keys=r['census_keys_in_title'])
    print('  #%-5s %-15s behind %-4s | today %-8s%s | after #%s %-8s%s | residue on END: %s | touches undici/busboy: %s | %s%s' % (
        n, r['user'][:15], behind, rows[n]['today'], (' ' + str(c0)) if c0 else '', N, rows[n]['after'], (' ' + str(c1)) if c1 else '',
        ('%d path(s) %s' % (len(res), res[:4])) if rc1 == 0 else 'n/a (conflict)', touch or 'no', r['title'][:70], '' if h == r['head'] else ' | STALE READ: fetched %s != API %s' % (h[:12], r['head'][:12])))
# controls: plants in the scratch clone only (plumbing, temp index)
W = os.path.join(SP, 'g48b_sp', 'overlaps_ctl_' + datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')); os.makedirs(W, exist_ok=True)
def plant(par, path, fn):
    blob = git('show', '%s:%s' % (par, path)).stdout; nb = fn(blob); fp = os.path.join(W, 'blob'); open(fp, 'w').write(nb)
    oid = git('hash-object', '-w', fp).stdout.strip(); idx = os.path.join(W, 'idx.%d' % len(os.listdir(W)))
    e = dict(ENV, GIT_INDEX_FILE=idx)
    for c in (['read-tree', par], ['update-index', '--cacheinfo', '100644,%s,%s' % (oid, path)]): subprocess.run(['git', '-C', CL] + c, env=e, check=True, capture_output=True)
    t = subprocess.run(['git', '-C', CL, 'write-tree'], env=e, check=True, capture_output=True, text=True).stdout.strip()
    return git('commit-tree', t, '-p', par, '-m', 'gate48b overlaps control plant').stdout.strip()
pc = plant(DEV, 'Blockchain/Dev/BACKLOG.md', lambda s: s + '\n<!-- gate48b overlaps control: unrelated -->\n')
pk = plant(DEV, 'Blockchain/Dev/package-lock.json', lambda s: s.replace('"node_modules/undici": {\n      "version": "5.29.0"', '"node_modules/undici": {\n      "version": "5.29.1"', 1))
a, _, _ = mt(SQ, pc); b, _, cb = mt(SQ, pk)
ok = a == 0 and b == 1
print('CT-CLEAN an unrelated plant over #%s squash: %s | CT-CONFLICT a root-lock undici-line plant over #%s squash: %s %s -> %s' % (N, 'clean' if a == 0 else 'CONFLICT', N, 'clean' if b == 0 else 'CONFLICT', cb, 'OK' if ok else 'FAIL'))
json.dump(dict(read_at=now(), develop=DEV, squash_sim=SQ, rows=rows), open(os.environ.get('G48B_OVJSON') or os.path.join(G, 'overlaps_gate48b.json'), 'w'), indent=1)   # G48B_OVJSON: controls write elsewhere
nc = sum(1 for x in rows.values() if x['after'] == 'CONFLICT'); nt = sum(1 for x in rows.values() if x['today'] == 'CONFLICT')
print('OVERLAPS %s: %d PR(s) | conflict today %d | conflict after #%s %d | empty residue (superseded) %d | touching undici/busboy %d' % (
    'READ' if ok else 'FAILED', len(rows), nt, N, nc, sum(1 for x in rows.values() if x['after'] == 'clean' and not x['residue']), sum(1 for x in rows.values() if x['undici_touch'])))
raise SystemExit(0 if ok else 1)
