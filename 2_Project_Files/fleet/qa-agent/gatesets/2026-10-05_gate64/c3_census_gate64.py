#!/usr/bin/env python3
"""c3_census_gate64.py — COUPLING census for #1389 (KS-1330). The head runner launches every suite ASYNC (stdin /dev/null, SIGINT
ignored — c3_inherit_gate64.sh measures both); develop's ran each in a foreground pipeline. So which of the tracked suites the runner
globs could notice? READ verbs only (git show / ls-tree at a rev; nothing is checked out or run).

Per suite (the runner's own glob: `<root>/*.test.sh` for each ROOT, non-recursive):
  READ-HEAD   `read` used as a COMMAND (after line start, ; & | ( ) { } ! $( , or then/do/else/while/until/if, allowing VAR=val
              prefixes) on a COMMENT-STRIPPED line (a `#` at line start or after whitespace, outside quotes, starts a comment).
              The builder's first count matched the English word "read" in comments: that is exactly what this strips.
  INPUT       each READ-HEAD is classified: `fd` (read -u N), `redirected` (`<`, `<<<`, `<<` after it on its line, or the enclosing
              while/until loop's `done <…`), `piped` (a `|` before it on its line, or the loop is piped into), else INHERITED — the only
              class whose behaviour changes when the suite's stdin becomes /dev/null.
  TRAP-INT    a `trap` command (not `trap -p` / `trap -l` / `trap - …` resets) whose line names INT or SIGINT; ALSO-TERM-EXIT: the same
              suite has a trap naming TERM / SIGTERM / EXIT.
Prints one row per suite with a hit, then:
  CENSUS <rev> suites <n> | read-head suites <a> | INHERITED-read suites <b> | trap-INT suites <c> | of those also TERM/EXIT <d>
  CONTROL the READ-HEAD detector must fire on the kit's must-hit suite (run_shell_suites.test.sh's `while IFS= read -r _root`)
--extra <rev>:<path>   also classify one suite at another rev (e.g. F 3rd's ks1401_049 suite on #1383's head; it is NOT on develop)
--selftest             planted fixture suites (in <G64_SCRATCH>/fixtures): every arm must land in its class.
Usage: c3_census_gate64.py --repo <git dir> [--rev <sha>] [--extra <rev>:<path> ...] | --selftest
rc 0 read OK and the control fired / rc 3 the must-hit control is blind / rc 1 selftest broken."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gate64 import K, git, SCRATCH

HEAD_RX = re.compile(r"(?:^|[;&|(){}!]|\$\(|\bthen\b|\bdo\b|\belse\b|\bwhile\b|\buntil\b|\bif\b)\s*"
                     r"(?:[A-Za-z_][A-Za-z0-9_]*=(?:'[^']*'|\"[^\"]*\"|\$'[^']*'|[^\s;]*)\s+)*(read)(?=\s|;|$)")
WORD = lambda w: re.compile(r'(?<![\w-])' + w + r'(?![\w-])')
DO, DONE = WORD('do'), WORD('done')


def strip_comment(line):
    q = None; out = []
    for i, ch in enumerate(line):
        if q:
            if ch == q and (q == "'" or line[i - 1] != '\\'): q = None
            out.append(ch); continue
        if ch in ('"', "'"): q = ch; out.append(ch); continue
        if ch == '#' and (i == 0 or line[i - 1] in ' \t;') and not (i > 0 and line[i - 1] == '$'): break
        out.append(ch)
    return ''.join(out)


def blank_quotes(s):
    """replace quoted text by spaces of equal length, so `|`, `<`, `do` inside strings do not count — EXCEPT a double-quoted string
    that holds a command substitution `$(`: its body is code (drafter's census_*_ex1, quarantined: `named="$(… | while IFS= read …)"`
    in doc_npm_scripts_exist.test.sh was blanked whole and its read went uncounted)"""
    return re.sub(r"'[^']*'|\"(?:\\.|[^\"\\])*\"", lambda m: m.group(0) if m.group(0).startswith('"') and '$(' in m.group(0) else ' ' * len(m.group(0)), s)


def classify(text):
    RAW = [strip_comment(l) for l in text.split('\n')]
    L = [blank_quotes(r) for r in RAW]
    reads, traps = [], {'INT': 0, 'TERMEXIT': 0}
    for i, l in enumerate(L):
        if not HEAD_RX.search(l) and HEAD_RX.search(RAW[i]):
            # a command-shaped `read` that sits inside quotes after blanking: nested quotes inside a quoted "$( … )" defeat the
            # blanker, so it is NOT classified — it is listed for the gate to READ BY HAND (never silently dropped, never counted)
            reads.append((i + 1, 'MANUAL', text.split('\n')[i].strip()[:110]))
        for m in HEAD_RX.finditer(l):
            pre, post = l[:m.start(1)], l[m.end(1):]
            loop = re.search(r'\b(while|until)\s*(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)*$', pre)
            if re.match(r'\s+(-\w+\s+)*-u\s*\S', post): cls = 'fd'
            elif '|' in pre or l.lstrip().startswith('|') or (i > 0 and L[i - 1].rstrip().endswith(('|', '| \\', '|\\'))): cls = 'piped'
            elif re.search(r'<', post.split(';')[0]) and not loop: cls = 'redirected'
            elif loop:
                depth = 0; cls = None; seen = False
                for j in range(i, min(len(L), i + 400)):
                    seg = L[j] if j > i else post
                    for tok in re.finditer(r'(?<![\w-])(do|done)(?![\w-])', seg):
                        depth += 1 if tok.group(1) == 'do' else -1
                        if tok.group(1) == 'do': seen = True
                        if seen and depth == 0:
                            tail = seg[tok.end():]
                            cls = 'redirected' if '<' in tail else ('piped' if '|' in pre else 'INHERITED')
                            break
                    if cls: break
                cls = cls or 'UNRESOLVED'
            else: cls = 'INHERITED'
            reads.append((i + 1, cls, text.split('\n')[i].strip()[:110]))
        if re.search(r'(?<![\w-])trap(?![\w-])', l) and not re.search(r'(?<![\w-])trap\s+-[pl]\b|(?<![\w-])trap\s+-\s', l):
            if re.search(r'(?<![\w-])(SIG)?INT(?![\w-])', l): traps['INT'] += 1
            if re.search(r'(?<![\w-])((SIG)?TERM|EXIT)(?![\w-])', l): traps['TERMEXIT'] += 1
    return reads, traps


def suites(repo, rev):
    out = []
    for root in K['roots']:
        for l in git(repo, 'ls-tree', '--name-only', rev, root + '/').splitlines():
            if re.fullmatch(re.escape(root) + r'/[^/]+\.test\.sh', l): out.append(l)
    return sorted(out)


def census(repo, rev, extras):
    S = suites(repo, rev); a = b = c = d = mm = 0; ctl = None
    for p in S:
        reads, traps = classify(git(repo, 'show', '%s:%s' % (rev, p)))
        man = [r for r in reads if r[1] == 'MANUAL']; reads = [r for r in reads if r[1] != 'MANUAL']
        inh = [r for r in reads if r[1] in ('INHERITED', 'UNRESOLVED')]
        mm += bool(man)
        a += bool(reads); b += bool(inh); c += bool(traps['INT']); d += bool(traps['INT'] and traps['TERMEXIT'])
        if p == K['test']: ctl = len(reads)
        if reads or traps['INT'] or man:
            print('SUITE %s | read-heads %d %s | INHERITED %d | trap INT %d, TERM/EXIT %d | MANUAL %d' % (
                os.path.basename(p), len(reads), sorted(set(r[1] for r in reads)), len(inh), traps['INT'], traps['TERMEXIT'], len(man)))
            for r in inh: print('    INHERITED :%d %s' % (r[0], r[2]))
            for r in man: print('    MANUAL (read by hand) :%d %s' % (r[0], r[2]))
    print('CENSUS %s suites %d | read-head suites %d | INHERITED-read suites %d | trap-INT suites %d | of those also TERM/EXIT %d | '
          'suites with MANUAL (quoted, unclassified) read lines %d' % (rev[:12], len(S), a, b, c, d, mm))
    for ex in extras:
        r, p = ex.split(':', 1)
        rc, _, _ = git(repo, 'cat-file', '-e', '%s:%s' % (K['develop'], p), check=False)
        reads, traps = classify(git(repo, 'show', '%s:%s' % (r, p)))
        print('EXTRA %s at %s (on develop %s: %s) | read-heads %d INHERITED %d | trap INT %d TERM/EXIT %d' % (
            os.path.basename(p), r[:12], K['develop'][:12], 'PRESENT' if rc == 0 else 'ABSENT', len(reads),
            len([x for x in reads if x[1] in ('INHERITED', 'UNRESOLVED')]), traps['INT'], traps['TERMEXIT']))
    print('CONTROL READ-HEAD detector on %s: %s read-head(s) %s' % (os.path.basename(K['test']), ctl, 'FIRES' if ctl else 'BLIND'))
    return 0 if ctl else 3


FIX = {
    'comment_only.test.sh': ('# read the config first; we never read stdin\necho "do not read me"\n', 0, 0, 0, 0),
    'bare_read.test.sh': ('#!/usr/bin/env bash\nread -r answer\necho "$answer"\n', 1, 1, 0, 0),
    'while_done_redirect.test.sh': ('while IFS= read -r l; do\n  echo "$l"\ndone < "$f"\n', 1, 0, 0, 0),
    'while_procsub.test.sh': ('while IFS= read -r v; do X+=("$v"); done < <(list)\n', 1, 0, 0, 0),
    'piped_while.test.sh': ('printf "a\\n" | while IFS= read -r l; do\n  :\ndone\n', 1, 0, 0, 0),
    'herestring.test.sh': ("IFS='|' read -r a b <<< \"$(x)\"\n", 1, 0, 0, 0),
    'read_fd.test.sh': ('read -u 3 line\n', 1, 0, 0, 0),
    'while_inherited.test.sh': ('while read -r l; do\n  echo "$l"\ndone\n', 1, 1, 0, 0),
    'trap_int_only.test.sh': ("trap 'cleanup' INT\n", 0, 0, 1, 0),
    'trap_int_term.test.sh': ("trap 'cleanup' INT TERM\n", 0, 0, 1, 1),
    'trap_reset_and_print.test.sh': ("trap - INT\ntrap -p INT\n", 0, 0, 0, 0),
    'read_in_string.test.sh': ('echo "then read x"\n', 0, 0, 0, 0),
    'piped_read_in_quoted_cmdsubst.test.sh': ('n="$(git ls-files | while IFS= read -r f; do echo "$f"; done)"\n', 1, 0, 0, 0),
    'nested_quotes_in_quoted_cmdsubst_is_MANUAL_not_counted.test.sh': ('n="$(git -C "$R" ls-files | while IFS= read -r f; do :; done)"\n', 0, 0, 0, 0),
    'bare_read_in_quoted_cmdsubst.test.sh': ('v="$(read -r y; echo "$y")"\n', 1, 1, 0, 0),
    'trap_in_message_string.test.sh': ('_skip="no handler (trap -p INT empty)"\n', 0, 0, 0, 0),
}


def selftest():
    fx = os.path.join(SCRATCH, 'fixtures', 'census'); os.makedirs(fx, exist_ok=True)
    ok = 0
    for name, (body, w_reads, w_inh, w_int, w_te) in FIX.items():
        open(os.path.join(fx, name), 'w').write(body)
        reads, traps = classify(body)
        reads = [r for r in reads if r[1] != 'MANUAL']
        inh = len([r for r in reads if r[1] in ('INHERITED', 'UNRESOLVED')])
        got = (len(reads), inh, traps['INT'], traps['TERMEXIT'] if traps['INT'] else 0)
        g = got == (w_reads, w_inh, w_int, w_te); ok += g
        print('SELFTEST %s %s: want reads/INHERITED/trapINT/alsoTE %s | got %s %s' % ('OK' if g else 'MISS', name, (w_reads, w_inh, w_int, w_te), got,
                                                                                   [r[1] for r in reads]))
    total = len(FIX) + 1
    man = [r for r in classify(FIX['nested_quotes_in_quoted_cmdsubst_is_MANUAL_not_counted.test.sh'][0])[0] if r[1] == 'MANUAL']
    g = len(man) == 1; ok += g
    print('SELFTEST %s the nested-quote read is LISTED as MANUAL (never silently dropped): got %d MANUAL line(s)' % ('OK' if g else 'MISS', len(man)))
    print('SELFTEST %s %d of %d' % ('OK' if ok == total else 'BROKEN', ok, total)); print('CHECKED %d arm(s)' % total)
    return 0 if ok == total else 1


if __name__ == '__main__':
    A = sys.argv[1:]
    if '--help' in A or '-h' in A: print(__doc__); raise SystemExit(0)
    if '--selftest' in A: raise SystemExit(selftest())
    def opt(k, d=None): return A[A.index(k) + 1] if k in A else d
    repo = opt('--repo')
    if not repo: raise SystemExit('need --repo')
    extras = [A[i + 1] for i, a in enumerate(A) if a == '--extra']
    raise SystemExit(census(repo, opt('--rev', K['head']), extras))
