#!/usr/bin/env python3
"""c1_pin_gate61.py — gate61 C1 PIN for #1383 (KS-1401), a SINGLE-PARENT head on develop. Three instruments: ONE `git ls-remote` from the
Secuura checkout (READ), the GitHub PULLS API (+ files), and git objects in YOUR scratch clone (fetch develop + refs/pull/1383/head first).
  P1 HEAD       input == refs/pull/<n>/head == refs/heads/<branch> (ls-remote) == the API head; API branch == kit branch (exact name).
  P2 API        open, not merged, base develop, API base sha == ls-remote develop; API changed_files == 4.
  P3 PARENT     EXACTLY one parent == kit develop (46c3e20cfbd2). A merge-in head is NOT this pin: judge it with c4_docs_gate61.py qm.
  P4 FILES      `git diff --numstat <develop> <head>` == EXACTLY the kit's 4 paths with the kit +/- per path, AND the API files list
                (filename, additions, deletions) == the same, both ways.
  P5 END-TREE   head tree == kit end_tree (b393b20f29b4); CONTROL: develop's tree differs.
  P6 NO-TRAILER `%(trailers)` RAW on the head == kit trailer_head_bytes_raw (1 byte: the bare newline) and stripped empty; CONTROL kit
                trailer_control_commit prints kit trailer_control_bytes_raw (55) raw bytes, > 0 stripped (the reading is not blind).
  P7 SUBJECT    the declared squash subject == the head subject byte-for-byte, <= 92 chars, '(#' 0 times.
  P8 KEYS       the head's commit MESSAGE carries exactly ONE `Refs KS-1401` line, 0 other `Refs` lines, and NO hyphenated KS key other
                than KS-1401 (KS 1376 etc. de-hyphenated) — the message is what the squash body may carry.
  P9 MODES      `git ls-tree` modes at the head == kit modes (the suite 100755, the migration and the docs 100644). core.filemode is false
                in the shared checkout, so the TREE is the only witness — a worktree's `ls -l` is not evidence.
  P10 DEVELOP   ls-remote develop == kit develop. A move FAILS here: the head no longer squashes to END_TREE; read what moved, and judge any
                later merge-in with c4_docs_gate61.py qm (Q-M M1-M7).
--selftest  gathers the REAL facts once (live, or --offline fixtures), proves they PASS (positive control T0), then drives TAMPER arms on
            copies of the facts, each of which must FAIL on its named check.
Usage: c1_pin_gate61.py --repo <your clone> [--pr 1383] [--head <40-hex>] [--offline dir] [--selftest]      rc 0 PASS / 1 FAIL / 2 usage
Prints `CHECKED <n>`; 0 checked is a FAIL."""
import copy, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate61 import K, git, now, Checks, opt_factory, has_commit, tree, GH, ls_remote, selftest_arm

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--repo' not in A:
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A); REPO = opt('--repo'); PR = opt('--pr', K['pr']); HEAD = opt('--head', K['head'])
if not re.fullmatch(r'[0-9a-f]{40}', HEAD):
    print('REFUSING: --head must be the FULL 40-hex sha, got %r' % HEAD); raise SystemExit(2)
OWN = K['pr_text']['own_key']


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
    for s in (HEAD, K['develop']):
        if not has_commit(REPO, s):
            print('REFUSING: %s is not in %s — fetch develop and refs/pull/%s/head into YOUR clone first' % (s[:12], REPO, PR)); raise SystemExit(2)
    F['parents'] = git(REPO, 'log', '-1', '--format=%P', HEAD).split()
    F['numstat'] = sorted((l.split('\t')[2], int(l.split('\t')[0]), int(l.split('\t')[1])) for l in git(REPO, 'diff', '--numstat', K['develop'], HEAD).splitlines() if l.strip())
    F['head_tree'] = tree(REPO, HEAD); F['develop_tree'] = tree(REPO, K['develop'])
    F['trailers_raw'] = {'head': git(REPO, 'log', '-1', '--format=%(trailers)', HEAD), 'control': git(REPO, 'log', '-1', '--format=%(trailers)', K['trailer_control_commit'])}
    F['subject'] = git(REPO, 'log', '-1', '--format=%s', HEAD).rstrip('\n')
    F['message'] = git(REPO, 'log', '-1', '--format=%B', HEAD)
    F['declared'] = K['squash_subject_declared']
    F['modes'] = {}
    for p_ in K['modes']:
        l = git(REPO, 'ls-tree', HEAD, '--', p_).strip()
        F['modes'][p_] = l.split()[0] if l else 'ABSENT'
    return F


def judge(C, F):
    ls = F['ls']; ph = ls.get('refs/pull/%s/head' % PR); bh = ls.get('refs/heads/' + K['branch']); dv = ls.get('refs/heads/develop'); a = F['api']
    C.chk('P1 head', F['input'] == ph == bh == a['head'] and a['branch'] == K['branch'] and re.match(K['branch_rx'], a['branch'] or '') is not None,
          'input %s | pull/head %s | branch %s | API %s | API branch %s (kit %s, exact name)' % (F['input'][:12], (ph or 'ABSENT')[:12], (bh or 'ABSENT')[:12], a['head'][:12], a['branch'], K['branch']))
    C.chk('P2 API', a['state'] == 'open' and a['merged'] is False and a['base'] == 'develop' and a['base_sha'] == dv and a['changed_files'] == len(K['files']),
          'state %s merged %s base %s base_sha %s (ls-remote develop %s) changed_files %s (want %d)' % (a['state'], a['merged'], a['base'], a['base_sha'][:12], (dv or 'ABSENT')[:12], a['changed_files'], len(K['files'])))
    C.chk('P3 single parent', F['parents'] == [K['develop']], 'head parents %s (want [develop %s]: a clean single-parent row)' % ([p[:12] for p in F['parents']], K['develop'][:12]))
    want = sorted((p, v[0], v[1]) for p, v in K['files'].items())
    miss = [w for w in want if w not in F['numstat']]; extra = [x for x in F['numstat'] if x not in want]
    amiss = [w for w in want if w not in a['files']]; aextra = [x for x in a['files'] if x not in want]
    C.chk('P4 files', not miss and not extra and not amiss and not aextra,
          'numstat develop..head %d path(s), API %d | missing (numstat) %s extra %s | missing (API) %s extra %s' % (len(F['numstat']), len(a['files']), miss or 'NONE', extra or 'NONE', amiss or 'NONE', aextra or 'NONE'))
    C.chk('P5 END-TREE', F['head_tree'] == K['end_tree'] and F['develop_tree'] != K['end_tree'],
          'head tree %s (kit END_TREE %s) | CONTROL develop tree %s differs: %s' % (F['head_tree'], K['end_tree'], F['develop_tree'][:12], F['develop_tree'] != K['end_tree']))
    t = F['trailers_raw']
    C.chk('P6 NO-TRAILER', len(t['head'].encode()) == K['trailer_head_bytes_raw'] and t['head'].strip() == '' and len(t['control'].encode()) == K['trailer_control_bytes_raw'] and t['control'].strip() != '',
          'head %%(trailers) raw %d byte(s) %r (want %d, stripped empty) | CONTROL %s raw %d byte(s) (want %d, non-empty stripped)' % (
              len(t['head'].encode()), t['head'][:40], K['trailer_head_bytes_raw'], K['trailer_control_commit'], len(t['control'].encode()), K['trailer_control_bytes_raw']))
    d = F['declared']
    C.chk('P7 SUBJECT', d == F['subject'] and len(d) <= K['subject_max'] and '(#' not in d,
          'declared %r (%d chars, <= %d: %s, "(#" %d) | head subject byte-equal: %s' % (d, len(d), K['subject_max'], len(d) <= K['subject_max'], d.count('(#'), d == F['subject']))
    m = F['message']; refs = re.findall(r'(?m)^Refs\b.*$', m); own = re.findall(r'(?m)^Refs %s\s*$' % OWN, m)
    keys = sorted(set(re.findall(r'\bKS-\d+\b', m)))
    C.chk('P8 KEYS', len(own) == 1 and len(refs) == 1 and keys == [OWN],
          '`Refs %s` lines %d (want 1) | all Refs lines %s | hyphenated keys in the message %s (want [%s]) | de-hyphenated %s' % (
              OWN, len(own), refs, keys, OWN, sorted(set(re.findall(r'\bKS \d+\b', m))) or 'NONE'))
    bad = {p_: (F['modes'].get(p_), w) for p_, w in K['modes'].items() if F['modes'].get(p_) != w}
    C.chk('P9 MODES', not bad, 'ls-tree modes at head %s | mismatches %s' % ({p_.split('/')[-1][:40]: v for p_, v in F['modes'].items()}, bad or 'NONE'))
    C.chk('P10 DEVELOP', dv == K['develop'], 'ls-remote develop %s | kit develop %s%s' % ((dv or 'ABSENT')[:12], K['develop'][:12],
          '' if dv == K['develop'] else ' — DEVELOP MOVED: the head no longer squashes to END_TREE; read what moved; a later merge-in is judged by c4_docs_gate61.py qm'))


print('c1_pin_gate61 %s | clone %s | PR #%s | head %s | kit develop %s%s' % (now(), REPO, PR, HEAD[:12], K['develop'][:12], ' | OFFLINE (SIM, never evidence)' if opt('--offline') else ''))
F = gather()
if '--selftest' in A:
    st = {'ok': 0, 'n': 0}

    def tam(fn):
        G2 = copy.deepcopy(F); fn(G2); return lambda C: judge(C, G2)
    p0 = list(K['files'])[0]
    selftest_arm(st, 'T0 the REAL facts (positive control)', lambda C: judge(C, F), None)
    selftest_arm(st, 'T1 base-vs-base (head == develop)', tam(lambda G2: G2.update(parents=['fe6daca343c143c32b1eb76d681668b4edbe4074'], numstat=[], head_tree=G2['develop_tree'])), 'P3')
    selftest_arm(st, 'T2 a 5th path (039 edited)', tam(lambda G2: G2['numstat'].append((K['migration_039'], 1, 1))), 'P4')
    selftest_arm(st, 'T3 a +/- drift on one path', tam(lambda G2: G2.update(numstat=[(p, a + 1 if p == p0 else a, d) for p, a, d in G2['numstat']])), 'P4')
    selftest_arm(st, 'T4 a merge-in (two parents)', tam(lambda G2: G2.update(parents=['7b356195a5e41d530c11f8e9286a6284be55b7c2', K['develop']])), 'P3')
    selftest_arm(st, 'T5 a trailer on the head', tam(lambda G2: G2['trailers_raw'].update(head='Co-Authored-By: Sim <s@x>\n')), 'P6')
    selftest_arm(st, 'T6 a blind trailer control (0 bytes)', tam(lambda G2: G2['trailers_raw'].update(control='')), 'P6')
    selftest_arm(st, 'T7 a (#1383) subject', tam(lambda G2: G2.update(declared=G2['declared'] + ' (#1383)')), 'P7')
    selftest_arm(st, 'T8 a 93-char subject', tam(lambda G2: G2.update(declared='K' * 93, subject='K' * 93)), 'P7')
    selftest_arm(st, 'T9 a second Refs line (Refs KS-1376)', tam(lambda G2: G2.update(message=G2['message'] + '\nRefs KS-1376\n')), 'P8')
    selftest_arm(st, 'T10 KS 1376 hyphenated in the message', tam(lambda G2: G2.update(message=G2['message'].replace('KS 1376', 'KS-1376', 1))), 'P8')
    selftest_arm(st, 'T11 the suite lost its exec bit (100644)', tam(lambda G2: G2['modes'].update({K['test']: '100644'})), 'P9')
    selftest_arm(st, 'T12 develop moved', tam(lambda G2: G2['ls'].update({'refs/heads/develop': 'f' * 40})), 'P10')
    selftest_arm(st, 'T13 the API head moved (a push meanwhile)', tam(lambda G2: G2['api'].update(head='e' * 40)), 'P1')
    selftest_arm(st, 'T14 a foreign -f2- branch name', tam(lambda G2: G2['api'].update(branch='feature/ks-1118-something-r15-f2-1')), 'P1')
    print('SELFTEST %s %d of %d' % ('OK' if st['ok'] == st['n'] else 'BROKEN', st['ok'], st['n']))
    print('CHECKED %d arm(s)' % st['n']); raise SystemExit(0 if st['ok'] == st['n'] and st['n'] > 0 else 1)
C = Checks(); judge(C, F); n = C.nfail()
print('CHECKED %d check(s)' % len(C.res))
print('C1 PIN %s: %d FAIL of %d checks | #%s head %s | END_TREE %s' % ('PASS' if n == 0 and C.res else 'FAIL', n, len(C.res), PR, HEAD[:12], F['head_tree'][:12]))
raise SystemExit(1 if n or not C.res else 0)
