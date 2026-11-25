#!/usr/bin/env python3
"""QA-MEASURE-2-R2 task 1: search the searched words (given on the command line, never stored here) in git objects.
usage: python3 -I -B qm2r_namesearch.py <repo> <mode> <rev-or-range-or-file> <word>...
  mode tree   : every blob of `git ls-tree -r <rev>` read as bytes
  mode objs   : every blob object reachable in <range> but not from its base (git rev-list --objects <range>)
  mode logp   : every line of `git log -p --binary <range>`
  mode file   : a file, /dev/stdin or /dev/fd/N (planted control, built in memory, never written to disk)
Each blob is searched in five forms: as is; URL-decoded (repeatedly); backslashes removed; shell-escape removed (\\x -> x);
lower-cased. A hit is counted when a word occurs ANYWHERE (substring, any case) - wider than a path component on purpose -
and it is then classified: component (after / \\ ~ or a token start, before / \\ or a token end), slug (-word-), other.
The tail `.claude/plugins/marketplaces` is searched too. Prints counts and file names only, never the words or the lines."""
import re, subprocess, sys, urllib.parse
sys.dont_write_bytecode = True
repo, mode, target, words = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
TAIL = b".claude/plugins/marketplaces"
def git(*a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, check=True).stdout
def forms(b):
    out = [b]
    u = b
    for _ in range(3):
        u2 = urllib.parse.unquote_to_bytes(u)
        if u2 == u: break
        u = u2
    out.append(u)
    out.append(b.replace(b"\\", b""))
    out.append(re.sub(rb"\\(.)", rb"\1", b))
    return out
def classify(b, w):
    wl = w.lower().encode(); bl = b.lower(); res = {"component": 0, "slug": 0, "other": 0}
    for m in re.finditer(re.escape(wl), bl):
        s, e = m.start(), m.end()
        pre = bl[s - 1:s] if s else b""; post = bl[e:e + 1]
        if (pre in (b"/", b"\\", b"~", b"") or pre.isspace() or pre in b"\"'`(<[=:,;") and (post in (b"/", b"\\", b"") or post.isspace() or post in b"\"'`)>],;:."):
            res["component"] += 1
        elif pre == b"-" and post == b"-": res["slug"] += 1
        else: res["other"] += 1
    return res
def scan(name, b):
    hits = {}
    for i, w in enumerate(words):
        c = {"component": 0, "slug": 0, "other": 0}
        for f in forms(b):
            r = classify(f, w)
            for k in c: c[k] = max(c[k], r[k])
        if any(c.values()): hits["word%d" % (i + 1)] = c
    t = max(f.lower().count(TAIL) for f in forms(b))
    if t: hits["tail"] = t
    return hits
results = []
if mode == "tree":
    for line in git("ls-tree", "-r", target).decode().splitlines():
        meta, path = line.split("\t", 1); sha = meta.split()[2]
        h = scan(path, git("cat-file", "blob", sha)); results.append((path, h))
elif mode == "objs":
    base = target.split("..")[0]
    for line in git("rev-list", "--objects", target, "^" + base).decode().splitlines():
        parts = line.split(" ", 1); sha = parts[0]
        if git("cat-file", "-t", sha).strip() != b"blob": continue
        h = scan(parts[1] if len(parts) > 1 else sha, git("cat-file", "blob", sha)); results.append((parts[1] if len(parts) > 1 else sha, h))
elif mode == "logp":
    out = git("log", "-p", "--binary", "--format=COMMIT %H", target)
    n = 0; cur = None; per = {}
    for ln in out.split(b"\n"):
        if ln.startswith(b"+++ b/") or ln.startswith(b"--- a/"): cur = ln[6:].decode("utf-8", "replace")
        h = scan(cur, ln)
        if h: n += 1; per[cur] = per.get(cur, 0) + 1
    print("log -p lines scanned: %d ; lines with a hit: %d ; per file: %s" % (out.count(b"\n"), n, per)); sys.exit(0)
elif mode == "file":   # a path, or /dev/stdin or /dev/fd/N (the planted control is never written to disk)
    results.append((target, scan(target, open(target, "rb").read())))
hit = [(p, h) for p, h in results if h]
print("items scanned: %d ; items with a hit: %d" % (len(results), len(hit)))
for p, h in hit: print("  HIT %s %s" % (p, h))
