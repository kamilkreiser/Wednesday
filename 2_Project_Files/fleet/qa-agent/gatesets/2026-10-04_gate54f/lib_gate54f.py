#!/usr/bin/env python3
"""lib_gate54f.py — shared helpers for the gate54f check scripts. READ-ONLY git verbs only (show, ls-tree, rev-parse, cat-file, log, diff,
rev-list, merge-base, ls-remote). Nothing here writes to a repository. Imported by c1..c6; never run on its own."""
import json, os, subprocess, datetime, difflib

G = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(G, 'kit.json'), encoding='utf-8'))
READ_VERBS = {'show', 'ls-tree', 'rev-parse', 'cat-file', 'log', 'diff', 'rev-list', 'merge-base', 'ls-remote'}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def git(repo, *a, check=True):
    if a[0] not in READ_VERBS:
        raise SystemExit('REFUSING: lib_gate54f.git allows read verbs only, got %r' % a[0])
    r = subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit('REFUSING: git %s rc %d: %s' % (' '.join(a)[:120], r.returncode, r.stderr.strip()[:300]))
    return r.stdout if check else (r.returncode, r.stdout, r.stderr)


def commit(repo, rev):
    rc, out, err = git(repo, 'rev-parse', '--verify', '--quiet', rev + '^{commit}', check=False)
    if rc:
        raise SystemExit('REFUSING: %s does not resolve to a commit in %s (fetch it into YOUR clone first)' % (rev, repo))
    return out.strip()


def show(repo, sha, path):
    """the blob text at sha:path, resolved with cat-file -e first (rev-parse echoes an unresolved path)"""
    rc, _, _ = git(repo, 'cat-file', '-e', '%s:%s' % (sha, path), check=False)
    if rc:
        return None
    return git(repo, 'show', '%s:%s' % (sha, path))


def _depth(s):
    """net bracket depth of one line of pretty-printed JSON, IGNORING brackets inside strings (reason texts carry `[...]`)"""
    d = 0; ins = False; esc = False
    for ch in s:
        if ins:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': ins = False
        elif ch == '"': ins = True
        elif ch in '{[': d += 1
        elif ch in '}]': d -= 1
    return d


def member_span(lines, start):
    """index range [start, end] of a JSON member whose opening line is lines[start] (ending in `{` or `[`), by string-aware bracket depth"""
    depth = 0
    for j in range(start, len(lines)):
        depth += _depth(lines[j])
        if depth == 0:
            return start, j
    return None


def find_member(lines, key):
    want = '"%s": {' % key
    st = [i for i, l in enumerate(lines) if l.strip() == want]
    return st[0] if len(st) == 1 else None


def block(text, key):
    """raw text of member `"key": {...}` (trailing comma stripped), or None if absent / ambiguous"""
    ls = text.split('\n'); i = find_member(ls, key)
    if i is None:
        return None
    sp = member_span(ls, i)
    return '\n'.join(ls[sp[0]:sp[1] + 1]).rstrip(',') if sp else None


def opcodes(a, b):
    sm = difflib.SequenceMatcher(None, a.split('\n'), b.split('\n'), autojunk=False)
    return [op for op in sm.get_opcodes() if op[0] != 'equal']


class Checks:
    def __init__(self):
        self.res = []; self.tags = []

    def failed(self, prefix):
        return [t for t, ok in self.tags if not ok and t.startswith(prefix)]

    def chk(self, tag, ok, msg):
        self.res.append(bool(ok)); self.tags.append((tag, bool(ok))); print('%s %s: %s' % ('PASS' if ok else 'FAIL', tag, msg))
        return bool(ok)

    def nfail(self):
        return self.res.count(False)
