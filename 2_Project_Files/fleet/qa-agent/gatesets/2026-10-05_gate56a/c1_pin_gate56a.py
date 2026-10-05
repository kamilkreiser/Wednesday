#!/usr/bin/env python3
"""c1_pin_gate56a.py — gate56a C1 PIN + PATH for ONE of Seat B 59th's two re-date PRs (run it once per PR: --which pr3, --which pr4).
Two instruments for the head (ls-remote + the PULLS API), the commit read from the clone with READ-ONLY git verbs.
  P1  ls-remote origin (run in --remote-repo, default the kit checkout, whose origin is git@github.com:Secuura/Distributed_Secuura.git —
      a `git clone --no-local` of the checkout has the LOCAL path as origin and reads its stale develop): refs/pull/<PR>/head == HEAD ==
      the branch ref; develop present.
  P2  PULLS API: open, not merged, base.ref develop, base.sha == origin develop, head.sha == HEAD, branch carries the PR's own key
      (kit branch_rx, lower-case ks-528 / ks-769) and NOT the sibling's; mergeable shown.
  P3  shape: HEAD has ONE parent, EXACTLY ONE commit over develop. develop == kit base (14d40d4455c7) -> parent == develop, ahead 1 / behind 0.
      SIBLING-ADVANCE (the other gate56a PR merged first): develop's ONE parent == kit base, develop's subject == the sibling's kit subject
      EXACTLY, kit base..develop changes ONLY the sibling's path -> parent == kit base, ahead 1 / behind 1, PASS with that named. Anything
      else: STALE BASE (a re-draft).
  P4  ONE PATH: API /files == clone `git diff --numstat HEAD^ HEAD` == EXACTLY [the PR's kit path]; +/- printed (pr3 want +2/-2, or +4/-4
      with the appended reason notes; pr4 the expires line plus its comment lines).
  P5  NO TRAILER: `%(trailers)` empty and 0 Co-Authored-By; CONTROL kit trailer_control_commit prints one.
  P6  SUBJECT EXACT: the commit subject == kit subject byte-for-byte (69 / 67 chars) and carries no `(#`; the PR title == the same string.
  P7  KEY SET == {own}: title, body, commit message carry the hyphenated own key and NO other hyphenated KS key (the sibling's key, KS 493,
      KS 763 ... must be de-hyphenated); branch carries only the lower-case own key; no closing keyword; `Refs <own>` on its own body line.
  P8  MODES: the path 100644 at HEAD; CONTROL kit mode_control_path 100755.
  P9  BASE BLOB: the path's blob at HEAD^ == kit base_blob (the edit starts from the drafted file).
  INFO END_TREE: HEAD^{tree} (the squash's tree while develop == HEAD^) beside develop^{tree} (the control that differs).
Base-state run (--base-state, no PR): ls-remote develop == kit base, both kit paths' blobs at develop == kit base_blob, P5/P8 controls fire;
  rc 4 "NO PR YET" (never a PASS).
Controls-only inputs: --offline-dir <d> replays the PULLS API from pr_<PR>.json + files_<PR>.json; --lsremote-file <f> replays ls-remote.
Usage: c1_pin_gate56a.py --which pr3|pr4 --repo <clone> (--pr <n> --head <40-hex> | --base-state) [--remote-repo r] [--offline-dir d] [--lsremote-file f]
rc 0 PASS / 1 FAIL / 2 usage / 3 API / 4 base state only"""
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate56a import K, git, now, Checks, GH, has_commit, count_range, blob_id, pr_cfg, opt_factory

A = sys.argv[1:]
if not A or '--help' in A or '-h' in A or '--which' not in A or '--repo' not in A or not ('--base-state' in A or ('--pr' in A and '--head' in A)):
    print(__doc__); raise SystemExit(0 if ('--help' in A or '-h' in A) else 2)
opt = opt_factory(A)
W = opt('--which'); P = pr_cfg(W); SIB = K['prs']['pr4' if W == 'pr3' else 'pr3']
REPO, PR, HEAD, OFF, LSF = opt('--repo'), opt('--pr'), opt('--head'), opt('--offline-dir'), opt('--lsremote-file')
RREPO = opt('--remote-repo', K['checkout'])   # ls-remote runs HERE: the shared checkout's origin is GitHub; a `clone --no-local` of it has the LOCAL path as origin (stale develop)
C = Checks()


def lsremote(refs):
    if LSF:
        return 0, open(LSF, encoding='utf-8').read()
    rc, out, _ = git(RREPO, 'ls-remote', 'origin', *refs, check=False)
    return rc, out


def trailers(sha):
    t = git(REPO, 'log', '-1', '--format=%(trailers)', sha).strip(); m = git(REPO, 'log', '-1', '--format=%B', sha)
    return t, len(re.findall(r'(?im)^co-authored-by:', m)), m


def modes(sha, f):
    o = git(REPO, 'ls-tree', sha, '--', f).strip()
    return o.split()[0] if o else 'ABSENT'


ct, cn, _ = trailers(K['trailer_control_commit'])
if '--base-state' in A:
    rc, ls = lsremote(['refs/heads/develop'])
    dev = next((l.split('\t')[0] for l in ls.splitlines() if l.endswith('\trefs/heads/develop')), None)
    print('c1_pin_gate56a %s | %s BASE STATE | repo %s | ls-remote in %s | origin develop %s%s' % (now(), W, REPO, RREPO, dev, ' | LS-REMOTE REPLAY' if LSF else ''))
    C.chk('B1 develop == kit base', rc == 0 and dev == K['base'], 'ls-remote rc %d develop %s | kit base %s' % (rc, dev, K['base']))
    probe = dev if dev and has_commit(REPO, dev) else K['base_standin']
    for w, q in K['prs'].items():
        b = blob_id(REPO, probe, q['path'])
        C.chk('B2 %s base blob' % w, b == q['base_blob'], '%s at %s: %s (kit %s)%s' % (q['path'], probe[:12], b[:12], q['base_blob'][:12], '' if probe == dev else '  [read at the tree-identical stand-in %s]' % probe[:12]))
    C.chk('B3 controls fire', cn >= 1 and modes(probe, K['mode_control_path']) == '100755', 'trailer control %s prints %d Co-Authored-By | mode control %s %s' % (
        K['trailer_control_commit'][:12], cn, K['mode_control_path'], modes(probe, K['mode_control_path'])))
    n = C.nfail(); print('C1 %s NO PR YET — base state: %d FAIL of %d (rc %d; never a PASS)' % (W, n, len(C.res), 4 if n == 0 else 1)); raise SystemExit(4 if n == 0 else 1)

if not re.fullmatch(r'\d+', PR or '') or not re.fullmatch(r'[0-9a-f]{40}', HEAD or ''):
    print('REFUSING: --pr must be digits and --head 40 lowercase hex (a verdict is valid only at a FULL sha)'); raise SystemExit(2)
gh = GH(OFF)
p = gh.get('pulls/' + PR); tries = 1
while not OFF and p.get('mergeable') is None and tries < 3:
    time.sleep(10); p = gh.get('pulls/' + PR); tries += 1
fl = gh.pages('pulls/%s/files' % PR)
print('c1_pin_gate56a %s | %s %s | repo %s | PR #%s | HEAD %s%s%s' % (now(), W, P['ticket'], REPO, PR, HEAD, ' | OFFLINE %s' % OFF if OFF else '', ' | LS-REMOTE REPLAY %s' % LSF if LSF else ''))
br = p['head']['ref']
rc, ls = lsremote(['refs/heads/develop', 'refs/pull/%s/head' % PR, 'refs/heads/' + br])
R = {l.split('\t')[1]: l.split('\t')[0] for l in ls.splitlines() if '\t' in l}
dev = R.get('refs/heads/develop'); ph = R.get('refs/pull/%s/head' % PR); bh = R.get('refs/heads/' + br)
C.chk('P1 ls-remote', rc == 0 and ph == HEAD and bh == HEAD and dev is not None,
      'rc %d | refs/pull/%s/head %s | refs/heads/%s %s | develop %s | HEAD %s (WHOLE-FIELD equality)' % (rc, PR, ph or 'ABSENT', br, bh or 'ABSENT', dev, HEAD))
bok = re.search(P['branch_rx'], br) is not None and re.search(SIB['branch_rx'], br) is None
C.chk('P2 pulls API', p['state'] == 'open' and not p.get('merged') and p['base']['ref'] == 'develop' and p['base']['sha'] == dev and p['head']['sha'] == HEAD and bok,
      'state %s | merged %s | base %s @ %s (== origin develop: %s) | head.sha %s | branch %s carries %s and not %s: %s | mergeable %s (%d read(s)) / %s' % (
          p['state'], p.get('merged'), p['base']['ref'], str(p['base']['sha'])[:12], p['base']['sha'] == dev, p['head']['sha'], br, P['branch_rx'], SIB['branch_rx'], bok,
          p.get('mergeable'), tries, p.get('mergeable_state')))
hc = has_commit(REPO, HEAD); dc = has_commit(REPO, dev or '0' * 40)
numstat = []; msg = ''
if not (hc and dc):
    C.chk('P3 shape', False, 'HEAD present in the clone %s | develop %s present %s — fetch refs/pull/%s/head and develop into YOUR clone first' % (hc, dev, dc, PR))
else:
    parents = git(REPO, 'log', '-1', '--format=%P', HEAD).split(); ahead = count_range(REPO, dev, HEAD); behind = count_range(REPO, HEAD, dev)
    if dev == K['base']:
        ok = parents == [dev] and ahead == 1 and behind == 0; how = 'develop == kit base'
    else:
        dpar = git(REPO, 'log', '-1', '--format=%P', dev).split(); dsub = git(REPO, 'log', '-1', '--format=%s', dev).strip()
        dnames = [l for l in git(REPO, 'diff', '--name-only', K['base'], dev).splitlines() if l] if has_commit(REPO, K['base']) else []
        sib = dpar == [K['base']] and dsub == SIB['subject'] and dnames == [SIB['path']]
        ok = sib and parents == [K['base']] and ahead == 1 and behind == 1
        how = 'SIBLING-ADVANCE %s (develop parent %s == kit base, subject == %s subject %s, kit base..develop paths %s)' % (sib, [x[:12] for x in dpar], SIB['label'], dsub == SIB['subject'], dnames) if sib else 'STALE BASE: develop %s is neither kit base nor kit base + the sibling squash — a re-draft' % dev[:12]
    C.chk('P3 shape', ok, 'parents %s | ahead %d | behind %d | %s' % ([x[:12] for x in parents], ahead, behind, how))
    numstat = [l.split('\t') for l in git(REPO, 'diff', '--numstat', HEAD + '^', HEAD).splitlines() if l]
    tree = git(REPO, 'rev-parse', HEAD + '^{tree}').strip()
    print('INFO END_TREE: HEAD^{tree} %s (the squash lands on this tree while develop == HEAD^) | develop^{tree} %s (the control that differs)' % (tree, git(REPO, 'rev-parse', dev + '^{tree}').strip()))
api = sorted((f['filename'], f['additions'], f['deletions']) for f in fl); loc = sorted((x[2], int(x[0]), int(x[1])) for x in numstat if x[0].isdigit())
C.chk('P4 one path', [x[0] for x in api] == [P['path']] and api == loc, 'API %s | clone HEAD^..HEAD numstat %s | want exactly [%s]' % (
    ['%s +%d/-%d' % x for x in api], ['%s +%d/-%d' % x for x in loc], P['path']))
if hc:
    ht, hn, msg = trailers(HEAD)
    C.chk('P5 no trailer', ht == '' and hn == 0 and cn >= 1, 'HEAD trailers %r (%d Co-Authored-By) | CONTROL %s prints %d' % (ht, hn, K['trailer_control_commit'][:12], cn))
    subj = msg.split('\n', 1)[0]
    C.chk('P6 subject exact', subj == P['subject'] and '(#' not in subj and (p.get('title') or '') == P['subject'],
          'commit subject %r (%d chars) == kit %r (%d): %s | no `(#`: %s | PR title == kit subject: %s (%r)' % (
              subj, len(subj), P['subject'], len(P['subject']), subj == P['subject'], '(#' not in subj, (p.get('title') or '') == P['subject'], p.get('title')))
else:
    C.chk('P5 no trailer', False, 'HEAD not in the clone'); C.chk('P6 subject exact', False, 'HEAD not in the clone')
body = p.get('body') or ''; own = P['ticket']
for s, t in (('title', p.get('title') or ''), ('body', body), ('commit', msg), ('branch', br)):
    ks = sorted(set(re.findall(r'\bKS-\d+\b', t))); cl = re.findall(r'(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[:\s]+(KS-\d+|#\d+)', t)
    want_ok = (ks == [own]) if s != 'branch' else (ks == [] and re.search(P['branch_rx'], t) is not None)
    C.chk('P7 keys %s' % s, want_ok and not cl, 'hyphenated keys %s (want exactly [%s]%s) | closing keyword %s' % (ks, own, '; branch: lower-case only' if s == 'branch' else '', cl or 'NONE'))
rl = re.search(r'(?m)^Refs %s\s*$' % own, body) is not None
C.chk('P7 Refs line', rl, '`Refs %s` on its own line in the PR body: %s | INFO de-hyphenated keys in the body: %s' % (own, rl, sorted(set(re.findall(r'\bKS \d+\b', body)))))
if hc:
    m = modes(HEAD, P['path']); cm = modes(HEAD, K['mode_control_path'])
    C.chk('P8 modes', m == '100644' and cm == '100755', '%s %s (want 100644) | CONTROL %s %s (want 100755)' % (P['path'], m, K['mode_control_path'], cm))
    pb = blob_id(REPO, HEAD + '^', P['path'])
    C.chk('P9 base blob', pb == P['base_blob'], '%s at HEAD^ %s == kit base_blob %s' % (P['path'], pb[:12], P['base_blob'][:12]))
n = C.nfail()
print('PIN %s %s: %d FAIL of %d checks | PR #%s | HEAD %s | develop %s' % (W, 'PASS' if n == 0 else 'FAIL', n, len(C.res), PR, HEAD[:12], (dev or '?')[:12]))
raise SystemExit(1 if n else 0)
