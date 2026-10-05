#!/usr/bin/env python3
"""c4b_predict_gate57.py — gate57 C4b: RE-DERIVE #1381's PREDICTED merge-in tree T2 INDEPENDENTLY, and (later) judge a real merge-in head
against Wednesday's ruling Q-M. Writes ONLY in YOUR scratch clone (commit-tree / merge-tree / hash-object / a temp index file under --out;
never a ref, never the shared store: lib wgit refuses any repo under /Volumes/DevMASTER).
  X1 SQUASH: a synthetic squash of #1380 on develop (`--develop`, default kit cut_base): its tree == #1380's head tree when develop ==
     cut_base, else `merge-tree --write-tree develop #1380` must merge CLEAN (rc 0) and that tree is used.
  X2 CONFLICT: `merge-tree --write-tree --name-only <squash> <#1381 head>` -> rc 1, the conflicted paths == EXACTLY the two Projects
     Documents files (printed verbatim); every other path auto-merged.
  X3 RESOLUTION (independent of the seat's): each doc = the squash side's text with #1381's OWN tail block (its insert hunk vs cut_base)
     inserted immediately before `  </body>`; the conflicted tree with those two blobs replaced -> write-tree -> T2.
  X4 T2 == the READY's END_TREE (kit prs.pr2.ready_end_tree) when develop == cut_base (else printed as the NEW prediction); the resolved
     tree differs from the conflicted tree in EXACTLY the two docs; from #1381's head tree in EXACTLY the two docs + #1380's own non-doc
     file(s) (+ any path the develop advance moved).
  X4c CONTROL: the same resolution with the blocks in the WRONG order (13 before 12) gives a DIFFERENT tree (the comparison can fail).
  X5 READ-BACK from T2: flow <h2> numbers == [1..13]; the cheat sheet's KS-1404, KS-1333, KS-1345 sections in that order; PR 1's ruled
     edits survive ('# 36 cells' 1, '# 27 cells' 0 in the cheat; 'other 27 KS-1015' 0 and '26 remain unowned' 1 per doc); each PR's block
     is BYTE-IDENTICAL to the block in its own head (the resolution invents nothing).
  Q-M  --merge-in-head <sha>: Wednesday's ruling — "a merge-in head whose tree == T2 and whose diff from its gated head is ONLY the two docs
     is covered by gate57". Judged as: M1 tree == T2; M2 TWO parents [gated #1381 head, develop-with-#1380]; M3 the TWO-DOT diff gated..merge-in
     == the two docs + exactly the paths develop brought in since cut_base, each of those at develop's blob (README section 2, doubt QM:
     read literally, a two-dot diff can NEVER be "only the two docs" — it always carries #1380's test file); M4 0 trailers.
--selftest: X1-X5 on the real heads, then Q-M against SIM merge-in commits made with commit-tree in your clone (never a ref): the
resolved one PASSES; one with an extra edit to webhooks.ts, one resolved 13-before-12, and one with a single parent FAIL their named checks.
Usage: c4b_predict_gate57.py --repo <your clone> --out <scratch dir> [--develop sha] [--merge-in-head sha [--develop-after sha]] [--selftest]
rc 0 PASS / 1 FAIL / 2 usage"""
import os, re, sys, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate57 import K, git, wgit, now, Checks, opt_factory, show, has_commit, opcodes, guard_scratch, guard_out

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A or '--out' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = guard_scratch(opt('--repo'), 'clone'); OUT = guard_out(opt('--out'))
CUT = K['cut_base']; DEV = opt('--develop', CUT); H1 = K['prs']['pr1']['ready_head']; H2 = K['prs']['pr2']['ready_head']
for s in (CUT, DEV, H1, H2):
    if not has_commit(REPO, s): print('REFUSING: %s not in %s' % (s[:12], REPO)); raise SystemExit(2)
DOCS = K['docs']; FLOW, CHEAT = DOCS; ANCH = K['doc_close_anchor']
ENV = {'GIT_AUTHOR_NAME': 'g57', 'GIT_AUTHOR_EMAIL': 'g57@sim', 'GIT_COMMITTER_NAME': 'g57', 'GIT_COMMITTER_EMAIL': 'g57@sim',
       'GIT_AUTHOR_DATE': '2026-10-05T00:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-05T00:00:00Z'}
IDX = os.path.join(OUT, 'c4b.index')


def tree(rev): return git(REPO, 'rev-parse', rev + '^{tree}').strip()
def ctree(*a): return wgit(REPO, 'commit-tree', *a, env=ENV).strip()
def blobtext(t, p): return show(REPO, t, p)
def tdiff(a, b): return sorted(set(git(REPO, 'diff', '--name-only', a, b).splitlines()))


def own_block(head, d):
    b = show(REPO, CUT, d).split('\n'); h = show(REPO, head, d).split('\n')
    ins = [o for o in opcodes(b, h) if o[0] == 'insert' and b[o[1]] == ANCH]
    return h[ins[0][3]:ins[0][4]] if len(ins) == 1 else None


def resolve(squash_tree_rev, conflicted_tree, order=('pr1', 'pr2')):
    e = {'GIT_INDEX_FILE': IDX}
    wgit(REPO, 'read-tree', conflicted_tree, env=e)
    for d in DOCS:
        side = show(REPO, squash_tree_rev, d).split('\n'); blk2 = own_block(H2, d)
        at = [i for i, l in enumerate(side) if l == ANCH]
        if len(at) != 1 or blk2 is None: raise SystemExit('REFUSING: cannot locate %r or #1381 block in %s' % (ANCH, d))
        if order == ('pr1', 'pr2'):
            txt = side[:at[0]] + blk2 + side[at[0]:]
        else:   # CONTROL: #1381's block BEFORE #1380's
            blk1 = own_block(H1, d); s0 = '\n'.join(side); j = s0.index('\n'.join(blk1))
            pre = s0[:j].split('\n')[:-1]; txt = pre + blk2 + s0[j:].split('\n')
        sha = wgit(REPO, 'hash-object', '-w', '--stdin', inp='\n'.join(txt)).strip()
        wgit(REPO, 'update-index', '--cacheinfo', '100644,%s,%s' % (sha, d), env=e)
    return wgit(REPO, 'write-tree', env=e).strip()


def predict(C, dev, real_squash=None):
    if real_squash:
        st = tree(real_squash); how = 'the REAL develop with #1380 landed (--develop-after)'
    elif dev == CUT:
        st = tree(H1); how = '#1380 head tree (develop == cut_base)'
    else:
        rc, o, e = wgit(REPO, 'merge-tree', '--write-tree', dev, H1, check=False)
        st = o.split('\n')[0].strip() if rc == 0 else None; how = 'merge-tree develop #1380 rc %d' % rc
    sq = real_squash or (ctree(st, '-p', dev, '-m', 'SIM squash #1380 (gate57 c4b)') if st else None)
    C.chk('X1 squash', sq is not None, 'synthetic squash %s on develop %s | tree %s (%s)' % ((sq or 'NONE')[:12], dev[:12], st, how))
    if not sq: return None
    rc, o, e = wgit(REPO, 'merge-tree', '--write-tree', '--name-only', sq, H2, check=False)
    lines = o.split('\n'); ct = lines[0].strip(); conf = sorted(set(l for l in lines[1:] if l and not l.startswith(('Auto-merging', 'CONFLICT')) and l in set(git(REPO, 'ls-tree', '-r', '--name-only', ct).splitlines())))
    msgs = [l for l in lines if l.startswith('CONFLICT')]
    C.chk('X2 conflict exactly the two docs', rc == 1 and conf == sorted(DOCS) and len(msgs) == 2, 'merge-tree rc %d | conflicted paths %s | verbatim: %s' % (rc, conf, msgs))
    t2 = resolve(sq, ct)
    rt = tdiff(ct, t2); r2 = tdiff(tree(H2), t2); want2 = sorted(set(DOCS) | (set(tdiff(CUT, dev)) | set(tdiff(CUT, H1))) - set(DOCS))
    claim = K['prs']['pr2']['ready_end_tree']
    C.chk('X4 T2', (t2 == claim if dev == CUT else True) and rt == sorted(DOCS) and r2 == want2,
          'T2 %s | READY claims %s: %s | resolved vs conflicted tree differ in %s (want the two docs) | T2 vs #1381 head tree differ in %s (want %s)' % (
              t2, claim, t2 == claim if dev == CUT else 'n/a (develop advanced: a NEW prediction)', rt, r2, want2))
    tw = resolve(sq, ct, order=('pr2', 'pr1'))
    C.chk('X4c wrong-order control', tw != t2, 'blocks 13-before-12 -> tree %s, differs from T2: %s' % (tw[:12], tw != t2))
    fl, ch = blobtext(t2, FLOW), blobtext(t2, CHEAT)
    nums = [int(m) for m in re.findall(r'(?m)^\s*<h2>(\d+)\.', fl)]
    pos = [ch.find(s) for s in ('&mdash; KS-1404</h2>', '&mdash; KS-1333</h2>', '&mdash; KS-1345</h2>')]
    cnt = {'# 36 cells (cheat)': ch.count('# 36 cells'), '# 27 cells (cheat)': ch.count('# 27 cells'),
           'other 27 KS-1015 (flow, cheat)': (len(re.findall('other 27 KS-1015', fl, re.I)), len(re.findall('other 27 KS-1015', ch, re.I))),
           '26 remain unowned (flow, cheat)': (fl.count('26 remain unowned'), ch.count('26 remain unowned'))}
    same = all('\n'.join(own_block(h, d)) in blobtext(t2, d) for h in (H1, H2) for d in DOCS)
    C.chk('X5 read-back', nums == list(range(1, 14)) and -1 not in pos and pos == sorted(pos) and cnt == {'# 36 cells (cheat)': 1, '# 27 cells (cheat)': 0, 'other 27 KS-1015 (flow, cheat)': (0, 0), '26 remain unowned (flow, cheat)': (1, 1)} and same,
          'flow <h2> numbers %s | cheat KS-1404 / KS-1333 / KS-1345 at %s (in order: %s) | %s | both PRs\' blocks byte-identical inside T2: %s' % (nums, pos, pos == sorted(pos) and -1 not in pos, cnt, same))
    return t2, sq


def judge_mergein(C, M, t2, gated, dev_after):
    mt = tree(M); par = git(REPO, 'log', '-1', '--format=%P', M).split()
    C.chk('M1 tree == T2', mt == t2, 'merge-in head %s tree %s | T2 %s' % (M[:12], mt, t2))
    C.chk('M2 two parents', len(par) == 2 and par[0] == gated and par[1] == dev_after, 'parents %s (want [gated %s, develop-with-#1380 %s])' % ([p[:12] for p in par], gated[:12], dev_after[:12]))
    d = tdiff(gated, M); brought = set(tdiff(CUT, dev_after)); extra = [p for p in d if p not in DOCS and p not in brought]
    blobs_ok = all(git(REPO, 'ls-tree', M, '--', p).split()[2:3] == git(REPO, 'ls-tree', dev_after, '--', p).split()[2:3] for p in d if p not in DOCS)
    C.chk('M3 Q-M diff', set(DOCS) <= set(d) and not extra and blobs_ok, 'two-dot gated..merge-in %s | outside the two docs and not brought by develop: %s | every non-doc path at develop\'s blob: %s' % (d, extra or 'NONE', blobs_ok))
    t = git(REPO, 'log', '-1', '--format=%(trailers)', M).strip()
    C.chk('M4 no trailer', t == '', 'trailers %r' % t)


print('c4b_predict_gate57 %s | clone %s | develop %s | #1380 %s | #1381 %s' % (now(), REPO, DEV[:12], H1[:12], H2[:12]))
if '--selftest' in A:
    C = Checks(); r = predict(C, CUT); n = C.nfail()
    print('SELFTEST part 1 (the real prediction): %d FAIL of %d' % (n, len(C.res)))
    if not r: raise SystemExit(1)
    t2, sq = r; ok = 0; arms = []
    good = ctree(t2, '-p', H2, '-p', sq, '-m', "SIM merge develop into #1381")
    hw = git(REPO, 'ls-tree', t2, '--', K['ks1345']['product']).split()[2]
    e = {'GIT_INDEX_FILE': IDX}; wgit(REPO, 'read-tree', t2, env=e)
    bad_src = show(REPO, t2, K['ks1345']['product']) + '\n// sim extra edit\n'
    wgit(REPO, 'update-index', '--cacheinfo', '100644,%s,%s' % (wgit(REPO, 'hash-object', '-w', '--stdin', inp=bad_src).strip(), K['ks1345']['product']), env=e)
    bad_tree = wgit(REPO, 'write-tree', env=e).strip()
    arms = [('Q0 the resolved merge-in', good, None),
            ('Q1 an extra edit to webhooks.ts', ctree(bad_tree, '-p', H2, '-p', sq, '-m', 'SIM bad'), 'M'),
            ('Q2 resolved 13-before-12', ctree(resolve(sq, wgit(REPO, 'merge-tree', '--write-tree', sq, H2, check=False)[1].split('\n')[0].strip(), order=('pr2', 'pr1')), '-p', H2, '-p', sq, '-m', 'SIM order'), 'M1'),
            ('Q3 a single-parent rewrite (a rebase)', ctree(t2, '-p', sq, '-m', 'SIM rebase'), 'M2'),
            ('Q4 a trailer on the merge-in', ctree(t2, '-p', H2, '-p', sq, '-m', 'SIM merge\n\nCo-Authored-By: Sim <s@x>'), 'M4')]
    for name, M, want in arms:
        buf = io.StringIO(); Cq = Checks()
        with contextlib.redirect_stdout(buf): judge_mergein(Cq, M, t2, H2, sq)
        f = Cq.failed(); g = (not f) if want is None else any(x.startswith(want) for x in f); ok += g
        print('SELFTEST %s %s: want %s | failed %s' % ('OK' if g else 'MISS', name, 'PASS' if want is None else 'FAIL on ' + want, f or 'NONE'))
        if not g: print(buf.getvalue())
    print('SELFTEST %s: prediction %d FAIL of %d | Q-M arms %d of %d' % ('OK' if n == 0 and ok == len(arms) else 'BROKEN', n, len(C.res), ok, len(arms)))
    raise SystemExit(0 if n == 0 and ok == len(arms) else 1)
DA = opt('--develop-after')
if opt('--merge-in-head') and not (has_commit(REPO, opt('--merge-in-head')) and DA and has_commit(REPO, DA)):
    print('REFUSING: --merge-in-head needs --develop-after (develop WITH #1380 landed), both commits in the clone'); raise SystemExit(2)
C = Checks(); r = predict(C, DEV, real_squash=DA)
if opt('--merge-in-head') and r:
    judge_mergein(C, opt('--merge-in-head'), r[0], H2, DA)
n = C.nfail()
print('C4b PREDICT %s: %d FAIL of %d checks | T2 %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), r[0] if r else 'NONE'))
raise SystemExit(1 if n else 0)
