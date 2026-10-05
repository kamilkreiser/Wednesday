#!/usr/bin/env python3
"""c1_pin_gate59.py — gate59 C1 PIN for #1382 (KS-1005), a MERGE-IN head. Three instruments: ONE `git ls-remote` from the Secuura checkout,
the GitHub PULLS API (+ files), and git objects in YOUR scratch clone (fetch develop + refs/pull/1382/head into it first).
  P1 HEAD      input == refs/pull/<n>/head == refs/heads/<branch> (ls-remote) == the API head; the branch matches kit branch_rx.
  P2 API       open, not merged, base develop, API base sha == ls-remote develop; API changed_files == 4.
  P3 PARENTS   EXACTLY two: [kit built 4346bc7fbdf8, kit develop 46c3e20cfbd2] in that order (Q-M M2 for the folded merge-in); the built
               commit has ONE parent == kit built_parent 3ce8cd4026a6 and its tree == kit built_tree (E 1st's commit, unrewritten).
  P4 FILES     `git diff --numstat <develop> <head>` == EXACTLY the kit's 4 paths with the kit +/- per path, AND the API files list
               (filename, additions, deletions) == the same, both ways (nothing missing, nothing extra).
  P5 END-TREE  head tree == kit end_tree; CONTROL: develop's tree differs (the comparison can fail).
  P6 NO-TRAILER `%(trailers)` empty on the head AND on the built commit; CONTROL kit trailer_control_commit prints one.
  P7 SUBJECT   the declared squash subject (kit squash_subject_declared) == the built commit's subject byte-for-byte, <= 92 chars as it
               LANDS (the merger sets it; no ` (#n)` appended), contains '(#' 0 times. The merge commit's subject is reported, never landed.
  P8 DEVELOP   ls-remote develop == kit develop. A move is a FAIL here: the head no longer merges as gated; a later merge-in is judged by
               c4_docs_gate59.py qm (Q-M M1-M4), never by re-reading this pin.
--selftest  gathers the REAL facts once (live, or --offline fixtures), proves they PASS (positive control), then drives 9 TAMPER arms on
            copies of the facts, each of which must FAIL on its named check: head == develop (base-vs-base), a 5th path, a +/- drift, a
            single parent (a rebase), a trailer, a `(#1382)` subject, a 93-char subject, develop moved, the API head moved.
Usage: c1_pin_gate59.py --repo <your clone> [--pr 1382] [--head <40-hex>] [--offline dir] [--selftest]      rc 0 PASS / 1 FAIL / 2 usage"""
import copy, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate59 import K, git, now, Checks, opt_factory, has_commit, tree, GH, ls_remote, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); PR = opt('--pr', K['pr']); HEAD = opt('--head', K['head'])
if not re.fullmatch(r'[0-9a-f]{40}', HEAD):
    print('REFUSING: --head must be the FULL 40-hex sha, got %r' % HEAD); raise SystemExit(2)


def gather():
    F = {'input': HEAD}
    if opt('--offline'):
        import json
        F['ls'] = json.load(open(os.path.join(opt('--offline'), 'lsremote.json')))
    else:
        F['ls'] = ls_remote(['refs/heads/develop', 'refs/pull/%s/head' % PR, 'refs/heads/' + K['branch']])
    gh = GH(opt('--offline')); p = gh.get('pulls/' + PR); fs = gh.pages('pulls/%s/files' % PR)
    F['api'] = {'head': p['head']['sha'], 'branch': p['head']['ref'], 'state': p['state'], 'merged': p.get('merged'), 'base': p['base']['ref'],
                'base_sha': p['base']['sha'], 'changed_files': p.get('changed_files'), 'files': sorted((f['filename'], f['additions'], f['deletions']) for f in fs)}
    for s in (HEAD, K['develop'], K['built']):
        if not has_commit(REPO, s):
            print('REFUSING: %s is not in %s — fetch develop and refs/pull/%s/head into YOUR clone first' % (s[:12], REPO, PR)); raise SystemExit(2)
    F['parents'] = git(REPO, 'log', '-1', '--format=%P', HEAD).split()
    F['built_parents'] = git(REPO, 'log', '-1', '--format=%P', K['built']).split()
    F['built_tree'] = tree(REPO, K['built'])
    F['numstat'] = sorted((l.split('\t')[2], int(l.split('\t')[0]), int(l.split('\t')[1])) for l in git(REPO, 'diff', '--numstat', K['develop'], HEAD).splitlines() if l.strip())
    F['head_tree'] = tree(REPO, HEAD); F['develop_tree'] = tree(REPO, K['develop'])
    F['trailers'] = {'head': git(REPO, 'log', '-1', '--format=%(trailers)', HEAD).strip(), 'built': git(REPO, 'log', '-1', '--format=%(trailers)', K['built']).strip(),
                     'control': git(REPO, 'log', '-1', '--format=%(trailers)', K['trailer_control_commit']).strip()}
    F['built_subject'] = git(REPO, 'log', '-1', '--format=%s', K['built']).rstrip('\n')
    F['merge_subject'] = git(REPO, 'log', '-1', '--format=%s', HEAD).rstrip('\n')
    F['declared'] = K['squash_subject_declared']
    return F


def judge(C, F):
    ls = F['ls']; ph = ls.get('refs/pull/%s/head' % PR); bh = ls.get('refs/heads/' + K['branch']); dv = ls.get('refs/heads/develop'); a = F['api']
    C.chk('P1 head', F['input'] == ph == bh == a['head'] and re.match(K['branch_rx'], a['branch'] or '') is not None and a['branch'] == K['branch'],
          'input %s | pull/head %s | branch %s | API %s | API branch %s (rx %s)' % (F['input'][:12], (ph or 'ABSENT')[:12], (bh or 'ABSENT')[:12], a['head'][:12], a['branch'], K['branch_rx']))
    C.chk('P2 API', a['state'] == 'open' and a['merged'] is False and a['base'] == 'develop' and a['base_sha'] == dv and a['changed_files'] == len(K['files']),
          'state %s merged %s base %s base_sha %s (ls-remote develop %s) changed_files %s (want %d)' % (a['state'], a['merged'], a['base'], a['base_sha'][:12], (dv or 'ABSENT')[:12], a['changed_files'], len(K['files'])))
    C.chk('P3 parents', F['parents'] == [K['built'], K['develop']] and F['built_parents'] == [K['built_parent']] and F['built_tree'] == K['built_tree'],
          'head parents %s (want [built %s, develop %s]) | built parents %s (want [%s]) | built tree %s (want %s)' % (
              [p[:12] for p in F['parents']], K['built'][:12], K['develop'][:12], [p[:12] for p in F['built_parents']], K['built_parent'][:12], F['built_tree'][:12], K['built_tree'][:12]))
    want = sorted((p, v[0], v[1]) for p, v in K['files'].items())
    miss = [w for w in want if w not in F['numstat']]; extra = [x for x in F['numstat'] if x not in want]
    amiss = [w for w in want if w not in a['files']]; aextra = [x for x in a['files'] if x not in want]
    C.chk('P4 files', not miss and not extra and not amiss and not aextra,
          'numstat develop..head %d path(s), API %d | missing (numstat) %s extra %s | missing (API) %s extra %s' % (len(F['numstat']), len(a['files']), miss or 'NONE', extra or 'NONE', amiss or 'NONE', aextra or 'NONE'))
    C.chk('P5 END-TREE', F['head_tree'] == K['end_tree'] and F['develop_tree'] != K['end_tree'],
          'head tree %s (kit END_TREE %s) | CONTROL develop tree %s differs: %s' % (F['head_tree'], K['end_tree'], F['develop_tree'][:12], F['develop_tree'] != K['end_tree']))
    t = F['trailers']
    C.chk('P6 NO-TRAILER', t['head'] == '' and t['built'] == '' and t['control'] != '',
          'trailers head %r built %r | CONTROL %s prints %d byte(s) (must be > 0)' % (t['head'], t['built'], K['trailer_control_commit'], len(t['control'])))
    d = F['declared']
    C.chk('P7 SUBJECT', d == F['built_subject'] and len(d) <= K['subject_max'] and '(#' not in d,
          'declared %r (%d chars, lands as declared, <= %d: %s, "(#" %d) | built subject byte-equal: %s | merge subject %r (%d chars, reported only)' % (
              d, len(d), K['subject_max'], len(d) <= K['subject_max'], d.count('(#'), d == F['built_subject'], F['merge_subject'], len(F['merge_subject'])))
    C.chk('P8 DEVELOP', dv == K['develop'], 'ls-remote develop %s | kit develop %s%s' % ((dv or 'ABSENT')[:12], K['develop'][:12],
          '' if dv == K['develop'] else ' — DEVELOP MOVED: the head no longer merges as gated; read what moved, and judge any later merge-in with c4_docs_gate59.py qm'))


print('c1_pin_gate59 %s | clone %s | PR #%s | head %s | kit develop %s%s' % (now(), REPO, PR, HEAD[:12], K['develop'][:12], ' | OFFLINE (SIM, never evidence)' if opt('--offline') else ''))
F = gather()
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}

    def tam(fn):
        G2 = copy.deepcopy(F); fn(G2); return lambda C: judge(C, G2)
    p0 = list(K['files'])[0]
    selftest_arm(st, 'T0 the REAL facts (positive control)', lambda C: judge(C, F), None)
    selftest_arm(st, 'T1 base-vs-base (head == develop)', tam(lambda G2: G2.update(parents=['fe6daca343c143c32b1eb76d681668b4edbe4074'], numstat=[], head_tree=G2['develop_tree'])), 'P3')
    selftest_arm(st, 'T2 a 5th path in the diff', tam(lambda G2: G2['numstat'].append(('Blockchain/Dev/services/auth/src/repositories/userRepo.ts', 1, 1))), 'P4')
    selftest_arm(st, 'T3 a +/- drift on one path', tam(lambda G2: G2.update(numstat=[(p, a + 1 if p == p0 else a, d) for p, a, d in G2['numstat']])), 'P4')
    selftest_arm(st, 'T4 a single-parent rewrite (a rebase)', tam(lambda G2: G2.update(parents=[K['develop']])), 'P3')
    selftest_arm(st, 'T5 a trailer on the head', tam(lambda G2: G2['trailers'].update(head='Co-Authored-By: Sim <s@x>')), 'P6')
    selftest_arm(st, 'T6 a (#1382) subject', tam(lambda G2: G2.update(declared=G2['declared'] + ' (#1382)')), 'P7')
    selftest_arm(st, 'T7 a 93-char subject', tam(lambda G2: G2.update(declared='K' * 93, built_subject='K' * 93)), 'P7')
    selftest_arm(st, 'T8 develop moved', tam(lambda G2: G2['ls'].update({'refs/heads/develop': 'f' * 40})), 'P8')
    selftest_arm(st, 'T9 the API head moved (a push meanwhile)', tam(lambda G2: G2['api'].update(head='e' * 40)), 'P1')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n'])); raise SystemExit(0 if st['ok'] == st['n'] else 1)
C = Checks(); judge(C, F); n = C.nfail()
print('C1 PIN %s: %d FAIL of %d checks | #%s head %s | END_TREE %s' % ('PASS' if n == 0 else 'FAIL', n, len(C.res), PR, HEAD[:12], F['head_tree'][:12]))
raise SystemExit(1 if n else 0)
