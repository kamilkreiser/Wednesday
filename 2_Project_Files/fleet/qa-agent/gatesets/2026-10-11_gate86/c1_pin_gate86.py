#!/usr/bin/env python3
"""c1_pin_gate86.py — C1 PIN for gate86: a TIER-2 BATCH of FOUR PRs (#1451 #1452 #1454 #1455). Read verbs only. Ported from c1_pin_gate85.py; [g86] marks this kit's changes:
  * the PRs have DIFFERENT bases (#1451 f8c86f859fe0, #1452 4a7cc1f697f8, #1454 / #1455 e27b9dceff39 = develop at the draft): `pin` and `docsbase` take --base PER PR and compare it with kit prs.<n>.base;
  * `isolation` is new: the file-ownership matrix of the four PRs (no PR touches another's files except the two docs and, for #1451 / #1452 only, the yaml), the number / key collision
    census against the landed block 57, and the cheat-sheet keys.
EVERY PIN IS A REQUIRED ARGUMENT (no default; a wrong value FAILS its check — the wrong-value arms are in --selftest):
  c1_pin_gate86.py pin       --repo R --pr N --head H --base B --develop D --end-tree T --parents-n 1 [--no-remote]
  c1_pin_gate86.py docsbase  --repo R --pr N --head H --base B --develop D
  c1_pin_gate86.py isolation --repo R --develop D --head 1451=H --head 1452=H --head 1454=H --head 1455=H
  c1_pin_gate86.py --selftest
  P1  origin refs/pull/<n>/head == refs/heads/<branch> == --head   (ls-remote; NOT RUN by name with --no-remote)
  P2  head is a commit | EXACTLY --parents-n parents | its parent == --base == the kit's base | rev-list base..head == 1
  P2b develop descends from --base; merge-base(head, develop) == --base; develop's distance from the base is printed (0 = this PR's base IS develop)
  P3  base..head paths == EXACTLY the kit's paths with the kit numstat
  P4  END_TREE == --end-tree (== the kit's)
  P5  %(trailers) CONTENT 0 bytes; CONTROL bf277eead268 prints > 0      P6  0 Co-Authored-By; CONTROL >= 1
  P7  subject == the kit's declared subject (= the PR title), <= 92, no `(#`, starts with the own key      P8  only the own key hyphenated; closing-family words counted (INFO); ONE `Refs ` line
  P9  PER-PATH modes at base and head == the kit's (100644 all; diff --summary shows only the kit's created paths)
  P10 NO-NEW-LEG: every kit tooling path (minus the PR's own) PRESENT with the SAME blob at base, head and develop
  P11 0 package.json / package-lock.json paths in base..head
  P12 base..develop intersected with the PR's paths is a subset of the known docs overlap; any CODE / yaml / tooling path FAILS
  DB1..DB3 (docsbase) docs base = merge-base(develop, head) == --base; each doc head == base + ONE exact insert before the closing tags; fragment size AND sha equal the kit's; CONTROLS: an unrelated
      older commit and the head itself read NOT an exact insert; a one-byte-flipped fragment fails the sha
  I1..I6 (isolation) live path sets per PR; every pair's overlap is within the allowed set; the landed block 57 is present exactly once and unique; 55 / 56 / 58 / 59 are absent from develop and distinct;
      the PR's own cheat heading not already on develop (control: the landed KS-1432 heading); each control (a planted extra overlap) FIRES
rc 0 all pass / 1 a FAIL / 2 refused (missing argument, unresolvable sha)."""
import hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate86 import K, PR, Tally, git, resolvable, blob, req, opt, docs_base, show, exact_tail_insert, TAIL

CLOSING = re.compile(K['closing_rx'], re.I)
FLOW, CHEAT = K['known_develop_overlap']; YAML = K['shared_yaml']
DOCS = set(K['known_develop_overlap'])


def parse_numstat(text):
    out = {}
    for l in text.strip('\n').split('\n'):
        if l: a, d, p = l.split('\t'); out[p] = [int(a), int(d)]
    return out


def sh16(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()[:16]


def allowed_pair(a, b):
    """[g86] the paths two PRs of this batch may BOTH touch: the two docs always; the yaml only for the #1451 / #1452 pair."""
    ok = set(DOCS)
    if {a, b} == {'1451', '1452'}: ok.add(YAML)
    return ok


def pair_findings(sets):
    """sets: {pr: set(paths)} -> {pair: (overlap, disallowed)}"""
    out = {}
    prs = sorted(sets)
    for i, a in enumerate(prs):
        for b in prs[i + 1:]:
            ov = sets[a] & sets[b]; out['%s&%s' % (a, b)] = (sorted(ov), sorted(ov - allowed_pair(a, b)))
    return out


def p11_hits(paths): return [p for p in paths if p.endswith(('package.json', 'package-lock.json'))]


def p12_bad(adv, own, tooling):
    """[g86] base..develop paths that overlap THIS PR's paths outside the known docs, plus any tooling path develop moved."""
    ov = sorted(set(adv) & set(own))
    return [p for p in ov if p not in DOCS] + [p for p in adv if any(p == x or p.startswith(x) for x in tooling)]


def p10_moved(readings):
    return ['%s %s' % (p, [x[-12:] if x else 'ABSENT' for x in r]) for p, r in readings.items() if not (r[0] and len(set(r)) == 1)]


def ls_remote(repo, refs):
    e = dict(os.environ); e.pop('GIT_SSH_COMMAND', None)
    ssh = git(repo, 'config', '--get', 'core.sshCommand').strip()
    p = subprocess.run(['git', '-C', repo, '-c', 'core.sshCommand=' + ssh, 'ls-remote', K['github_url']] + refs, capture_output=True, env=e, timeout=120)
    return p.returncode, {l.split('\t')[1]: l.split('\t')[0] for l in p.stdout.decode().split('\n') if '\t' in l}, p.stderr.decode()


def pin(A):
    n = req(A, '--pr'); P = PR(n); head = req(A, '--head', True); base = req(A, '--base', True); dev = req(A, '--develop', True); et = req(A, '--end-tree', True); pn = req(A, '--parents-n'); repo = req(A, '--repo')
    t = Tally()
    for lab, s in (('head', head), ('base', base), ('develop', dev)):
        if not resolvable(repo, s): raise SystemExit('REFUSED: %s %s is not in %s (fetch it BY SHA into YOUR clone)' % (lab, s, repo))
    print('C1 PIN #%s %s | head %s base %s develop %s end-tree %s | kit head %s base %s' % (n, P['ticket'], head[:12], base[:12], dev[:12], et[:12], P['head_expected'][:12], P['base'][:12]))
    t.check('P0', head == P['head_expected'] and base == P['base'] and et == P['end_tree'] and pn == P['parent_count'], 'the arguments equal the kit pins (head, base, end-tree, parents-n): a wrong value would FAIL here')
    if '--no-remote' in A:
        t.info('P1', 'NOT RUN by name (--no-remote): origin pull/head and branch are NOT read here')
    else:
        rc, refs, err = ls_remote(repo, ['refs/pull/%s/head' % n, 'refs/heads/%s' % P['branch'], 'refs/heads/develop'])
        t.check('P1', rc == 0 and refs.get('refs/pull/%s/head' % n) == head and refs.get('refs/heads/%s' % P['branch']) == head, 'ls-remote rc %d: pull/%s/head %s branch %s want %s' % (rc, n, (refs.get('refs/pull/%s/head' % n) or 'NONE')[:12], (refs.get('refs/heads/%s' % P['branch']) or 'NONE')[:12], head[:12]))
        t.info('P1b', 'origin develop now %s (the argument: %s)' % ((refs.get('refs/heads/develop') or 'NONE')[:12], dev[:12]))
    par = git(repo, 'log', '-1', '--format=%P', head).split()
    t.check('P2', git(repo, 'cat-file', '-t', head).strip() == 'commit' and len(par) == int(pn) and par == [base] and base == P['parent'] and git(repo, 'rev-list', '--count', '%s..%s' % (base, head)).strip() == str(P['commits_n']),
            'commit with %d parent(s) %s == the base %s; base..head = %s commit(s)' % (len(par), [x[:12] for x in par], base[:12], git(repo, 'rev-list', '--count', '%s..%s' % (base, head)).strip()))
    mb = git(repo, 'merge-base', head, dev).strip(); dist = git(repo, 'rev-list', '--count', '%s..%s' % (base, dev)).strip()
    t.check('P2b', git(repo, 'merge-base', '--is-ancestor', base, dev, check=False)[0] == 0 and mb == base, 'develop descends from the base and merge-base(head, develop) = %s == the base; develop is %s commit(s) past the base' % (mb[:12], dist))
    ns = parse_numstat(git(repo, 'diff', '--numstat', base, head)); want = {p: [v['add'], v['del']] for p, v in P['paths'].items()}
    bad = [p for p in set(ns) | set(want) if ns.get(p) != want.get(p)]
    t.check('P3', not bad, '%d paths, +%d/-%d; numstat equals the kit for every path%s' % (len(ns), sum(v[0] for v in ns.values()), sum(v[1] for v in ns.values()), (' MISMATCH: %s' % bad[:4]) if bad else ''))
    t.check('P4', git(repo, 'log', '-1', '--format=%T', head).strip() == et, 'END_TREE %s == --end-tree' % et[:12])
    msg = git(repo, 'log', '-1', '--format=%B', head); tr = git(repo, 'log', '-1', '--format=%(trailers)', head).strip(); ctl = git(repo, 'log', '-1', '--format=%(trailers)', K['trailer_control']).strip() if resolvable(repo, K['trailer_control']) else None
    t.check('P5', len(tr) == 0 and (ctl is None or len(ctl) > 0), 'trailers: %d bytes (CONTROL %s prints %s bytes)' % (len(tr), K['trailer_control'], 'n/a (not in this store)' if ctl is None else len(ctl)))
    cc = len(re.findall(r'(?im)^co-authored-by:', msg)); cctl = len(re.findall(r'(?im)^co-authored-by:', git(repo, 'log', '-1', '--format=%B', K['trailer_control']))) if resolvable(repo, K['trailer_control']) else None
    t.check('P6', cc == 0 and (cctl is None or cctl >= 1), '%d Co-Authored-By (CONTROL %s: %s)' % (cc, K['trailer_control'], cctl))
    subj = git(repo, 'log', '-1', '--format=%s', head).strip()
    t.check('P7', subj == P['subject'] and len(subj) <= 92 and '(#' not in subj and subj.startswith(P['ticket'] + ':'), 'subject "%s" (%d chars) == the kit pin, <= 92, no (#, starts with %s:' % (subj, len(subj), P['ticket']))
    keys = sorted(set(re.findall(r'\bKS-\d+\b', msg))); closing = CLOSING.findall(msg); refs = len(re.findall(r'(?m)^Refs ', msg))
    t.check('P8', keys == [P['ticket']] and refs == 1, 'hyphenated keys in the message %s (want only %s); `Refs ` lines %d (want 1)' % (keys, P['ticket'], refs))
    t.info('P8b', 'closing-family hits in the message: %d' % len(closing))
    rows = {}
    for r in git(repo, 'diff', '--raw', '--no-abbrev', base, head).strip().split('\n'):
        if r: a, p = r.split('\t'); f = a.split(); rows[p] = (f[0].lstrip(':'), f[1], f[2], f[3], f[4])
    bm = [p for p, v in rows.items() if (v[0], v[1], v[4]) != (P['paths'][p]['mode_base'], P['paths'][p]['mode_head'], P['paths'][p]['status']) or v[3] != P['paths'][p]['head_blob'] or v[2] != P['paths'][p]['base_blob']] if set(rows) == set(P['paths']) else ['PATHSET']
    t.check('P9', not bm and all(v[1] == '100644' for v in rows.values()), 'modes / status / blob ids per path == the kit for all %d paths (head modes all 100644: %s)%s' % (len(rows), all(v[1] == '100644' for v in rows.values()), (' MISMATCH %s' % bm[:3]) if bm else ''))
    own = set(P['paths']); read = {}
    for p in K['tooling_paths_unchanged']:
        if p in own: continue
        read[p] = [blob(repo, x, p) for x in (base, head, dev)]
    moved = p10_moved(read)
    t.check('P10', not moved, 'NO-NEW-LEG: %d tooling paths identical at base / head / develop%s' % (len(read), (' MOVED: %s' % moved[:4]) if moved else ''))
    t.check('P10-CONTROL', p10_moved({'x': ['a' * 40, 'a' * 40, 'b' * 40]}) != [] and p10_moved({'x': ['', '', '']}) != [] and p10_moved({'x': ['a' * 40] * 3}) == [], 'CONTROL: a path whose develop blob differs reads MOVED, an ABSENT path reads MOVED, an identical path reads clean (the zero above can fail)')
    t.check('P11', not p11_hits(ns), 'no package.json / package-lock.json path in base..head')
    t.check('P11-CONTROL', p11_hits(list(ns) + ['Blockchain/Dev/package.json']) == ['Blockchain/Dev/package.json'], 'CONTROL: the same filter returns a planted package.json path')
    adv = [l for l in git(repo, 'diff', '--name-only', base, dev).split('\n') if l]; ov = sorted(set(adv) & own)
    bad = p12_bad(adv, own, K['tooling_paths_unchanged'])
    t.check('P12', not bad, 'base..develop touches %d path(s), %d of them this PR\'s: %s; outside the known docs overlap: %s' % (len(adv), len(ov), [x.split('/')[-1][:34] for x in ov], bad[:4] or 'none'))
    code1 = sorted(p for p in own if p not in DOCS)[0]
    t.check('P12-CONTROL', p12_bad([code1], own, K['tooling_paths_unchanged']) == [code1] and p12_bad([K['tooling_paths_unchanged'][0]], own, K['tooling_paths_unchanged']) != [] and p12_bad(sorted(DOCS), own, K['tooling_paths_unchanged']) == [], 'CONTROL: a planted develop change to this PR\'s code path, and to a tooling path, read as outside the overlap; the two docs alone read clean')
    return t.end()


def docsbase(A):
    n = req(A, '--pr'); P = PR(n); head = req(A, '--head', True); base = req(A, '--base', True); dev = req(A, '--develop', True); repo = req(A, '--repo'); t = Tally()
    mb, info = docs_base(repo, dev, head, base)
    t.check('DB1', mb == base == P['base'], 'docs parent = merge-base(develop %s, head %s) = %s == --base == the kit base; head^ = %s (merge_base_is_head_parent: %s)' % (dev[:12], head[:12], mb[:12], info['head_parent'][:12], info['merge_base_is_head_parent']))
    older = K['trailer_control']
    for d in (FLOW, CHEAT):
        b, h = show(repo, mb, d), show(repo, head, d); ok, frag, why = exact_tail_insert(b, h); want = P['fragments'][d]
        t.check('DB2', ok and len(frag.encode()) == want['fragment_bytes'] and sh16(frag) == want['fragment_sha256_16'], '%s: head = base + ONE exact insert before the closing tags (%s); fragment %d B sha256/16 %s (kit %d B %s)' % (d.split('/')[-1][:40], why, len(frag.encode()), sh16(frag), want['fragment_bytes'], want['fragment_sha256_16']))
        if d == FLOW:
            hs = re.findall(r'<h2>(\d+)\. ', frag); t.check('DB2b', hs == [str(P['flow_block'])], 'flow headings in the fragment %s == [%d]' % (hs, P['flow_block']))
        else:
            hs = re.findall(r'<h2>([^<]*)</h2>', frag); t.check('DB2c', len(hs) == 1 and P['cheat_key'] in hs[0], 'cheat headings in the fragment: %d, naming %s: %s' % (len(hs), P['cheat_key'], P['cheat_key'] in ''.join(hs)))
        if resolvable(repo, older):
            okc, _, whyc = exact_tail_insert(show(repo, older, d), h)
            t.check('DB3-CONTROL-OLDER', not okc, 'CONTROL: extraction against the unrelated older commit %s is NOT an exact insert (%s)' % (older, whyc[:70]))
        okh, _, whyh = exact_tail_insert(h, h)
        t.check('DB3-CONTROL-SELF', not okh, 'CONTROL: the head as its own base is NOT an exact insert (%s)' % whyh[:60])
        flipped = frag[:100] + ('Y' if frag[100] != 'Y' else 'Z') + frag[101:]
        t.check('DB3-CONTROL-FLIP', len(flipped.encode()) == len(frag.encode()) and sh16(flipped) != want['fragment_sha256_16'], 'CONTROL: a one-byte-flipped fragment keeps its size and fails the sha')
    return t.end()


def isolation(A):
    repo = req(A, '--repo'); dev = req(A, '--develop', True); heads = dict(a.split('=') for i, a in enumerate(A) if i and A[i - 1] == '--head'); t = Tally()
    if sorted(heads) != sorted(K['prs']): raise SystemExit('REFUSED: --head must be given for exactly %s' % sorted(K['prs']))
    for n, h in heads.items():
        if not resolvable(repo, h): raise SystemExit('REFUSED: %s is not in %s' % (h, repo))
        t.check('I0-%s' % n, h == PR(n)['head_expected'], '#%s --head %s == the kit head' % (n, h[:12]))
    sets = {}
    for n, h in heads.items():
        b = git(repo, 'merge-base', dev, h).strip(); sets[n] = set(l for l in git(repo, 'diff', '--name-only', b, h).split('\n') if l)
        t.check('I1-%s' % n, sets[n] == set(PR(n)['paths']), '#%s live path set (%d) == the kit path set (%d)' % (n, len(sets[n]), len(PR(n)['paths'])))
    pf = pair_findings(sets)
    for pair, (ov, bad) in pf.items(): t.check('I2-%s' % pair, not bad and len(ov) >= 2, 'pair %s overlap %d path(s) %s; outside the allowed set: %s' % (pair, len(ov), [x.split('/')[-1][:26] for x in ov], bad or 'none'))
    plant = {k: set(v) for k, v in sets.items()}; plant['1454'].add('Blockchain/Dev/scripts/stack_env.sh'); plant['1455'].add('Blockchain/Dev/scripts/stack_env.sh')
    t.check('I2-CONTROL', pair_findings(plant)['1454&1455'][1] == ['Blockchain/Dev/scripts/stack_env.sh'], 'CONTROL: a planted shared code path between #1454 and #1455 is reported as DISALLOWED (the zero above can fail)')
    plant2 = {k: set(v) for k, v in sets.items()}; plant2['1454'].add(YAML)
    t.check('I2-CONTROL2', pair_findings(plant2)['1451&1454'][1] == [YAML], 'CONTROL: the yaml is allowed ONLY for the #1451 / #1452 pair (planted on #1454: DISALLOWED)')
    yaml_owners = sorted(n for n in sets if YAML in sets[n]); t.check('I3', yaml_owners == ['1451', '1452'], 'the regenerated yaml is touched by exactly %s' % yaml_owners)
    fl = show(repo, dev, FLOW); ch = show(repo, dev, CHEAT); nums = re.findall(r'<h2>(\d+)\. ', fl)
    t.check('I4', nums.count('57') == 1 and len(nums) == len(set(nums)), 'develop %s: flow heading numbers %d, all distinct: %s; block 57 present x%d (KS-1432, the earlier-landed block); document-order tail %s' % (dev[:12], len(nums), len(nums) == len(set(nums)), nums.count('57'), nums[-8:]))
    t.check('I4-CONTROL', nums.count('52') == 1 and nums.count('99') == 0, 'CONTROL: an existing number (52) reads 1 and an impossible one (99) reads 0 with the same regex')
    batch = {n: PR(n)['flow_block'] for n in sets}
    t.check('I5', sorted(batch.values()) == [55, 56, 58, 59] and not [v for v in batch.values() if str(v) in nums], 'the batch numbers %s are distinct and ABSENT from develop (taken: %s); next free by max+1 = %d' % (batch, [v for v in batch.values() if str(v) in nums] or 'none', max(int(x) for x in nums) + 1))
    heads_dev = re.findall(r'<h2>([^<]*)</h2>', ch)
    for n in sets:
        P = PR(n); k = P['cheat_key']; c0 = len([x for x in heads_dev if k in x]); mine = P['fragments'][CHEAT]['cheat_heading']
        dup = [x for x in heads_dev if x.strip() == mine.strip()]
        t.check('I6-%s' % n, not dup, 'cheat sheet on develop already carries %d <h2> naming %s (earlier pieces of the same ticket: INFO, not a defect); the PR\'s own heading is NOT already on develop: duplicates %d' % (c0, k, len(dup)))
    t.check('I6-CONTROL', len([x for x in heads_dev if 'KS-1432' in x]) == 1 and len([x for x in heads_dev if x.strip() == [y for y in heads_dev if 'KS-1432' in y][0].strip()]) == 1,
            'CONTROL: the landed KS-1432 cheat section reads 1 and the duplicate test reports it as a duplicate when asked about itself')
    return t.end()


def selftest():
    t = Tally()
    ok = pair_findings({'1451': {FLOW, YAML, 'x'}, '1452': {FLOW, YAML, 'x'}})['1451&1452']
    t.check('S1', ok[1] == ['x'] and set(ok[0]) == {FLOW, YAML, 'x'}, 'pair_findings flags a shared code path and tolerates docs + yaml for 1451&1452: %s' % (ok,))
    t.check('S2', pair_findings({'1454': {YAML}, '1455': {YAML}})['1454&1455'][1] == [YAML], 'the yaml is DISALLOWED for any other pair')
    t.check('S3', parse_numstat('1\t2\ta\n3\t4\tb c\n') == {'a': [1, 2], 'b c': [3, 4]}, 'parse_numstat handles a path with a space')
    b = 'x\n' + TAIL; h = 'x\nNEW\n' + TAIL
    t.check('S4', exact_tail_insert(b, h)[0] and not exact_tail_insert(b, b)[0] and not exact_tail_insert(b, 'y\nNEW\n' + TAIL)[0], 'exact_tail_insert: pure insert true; identical false; changed prefix false')
    t.check('S5', allowed_pair('1451', '1452') == DOCS | {YAML} and allowed_pair('1454', '1455') == DOCS, 'allowed_pair')
    t.check('S6', sh16('a') != sh16('b') and len(sh16('a')) == 16, 'sh16')
    t.check('S7', p11_hits(['a/package.json', 'b.ts']) == ['a/package.json'] and p12_bad(['x.ts'], ['x.ts'], []) == ['x.ts'] and p12_bad([sorted(DOCS)[0]], [sorted(DOCS)[0]], []) == [] and p10_moved({'x': ['a' * 40] * 3}) == [], 'p11 / p12 / p10 helper arms')
    return t.end()


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--selftest' in A: sys.exit(selftest())
    if not A or A[0] not in ('pin', 'docsbase', 'isolation'): print(__doc__); sys.exit(2)
    sys.exit({'pin': pin, 'docsbase': docsbase, 'isolation': isolation}[A[0]](A[1:]))
