#!/usr/bin/env python3
"""QA-MEASURE-2-R2 byte scan: a copy of QA-MEASURE-2's qm2_scan.py with three additions (marked R2): a class for the old
path's tail, --literals (substrings, any case: e.g. the real runs' tmux server name, given at run time), and --names now
also matched after %2F / %5C (on top of the URL-decoded form). Original docstring:
QA-MEASURE-2 own byte scan (independent of the seat's scan_bytes.py / redact.py). Prints class names, files and counts,
never a matched value. usage:
  python3 -I -B qm2_scan.py --clone <clone> --rev <sha> --base <sha> --roots <root>... [--names <word>...]
  python3 -I -B qm2_scan.py --control <file> --roots <root>... [--names <word>...]
Reads every file of spikes/U-B2-host-facts at --rev as BYTES (binaries included) plus the lines the branch ADDS to
BACKLOG.md and docs/M0-OUTCOMES.md, in five forms (raw, ANSI removed, backslashes removed, URL-decoded, control bytes
removed). Classes: account (id -un and each part >=3 of id -F), machine (hostname, scutil names), home path, email shape,
each explicit root (plain, shell-escaped, URL-encoded, slug), each --names word as a WHOLE path component (any case),
UUID, prompt_id/agent_id values not a placeholder, req_/msg_/toolu_ ids, the uid-bearing temp paths."""
import os, re, subprocess, sys, urllib.parse
sys.dont_write_bytecode = True
a = sys.argv[1:]
def opt(flag, many=False):
    if flag not in a: return [] if many else None
    i = a.index(flag) + 1; out = []
    while i < len(a) and not a[i].startswith("--"): out.append(a[i]); i += 1
    return out if many else out[0]
def sh(*c):
    try: return subprocess.run(c, capture_output=True, text=True).stdout.strip()
    except OSError: return ""
USER = sh("id", "-un"); FULL = sh("id", "-F"); HOME = os.path.expanduser("~")
HOSTS = {h for h in (sh("hostname"), sh("hostname", "-s"), sh("scutil", "--get", "ComputerName"), sh("scutil", "--get", "LocalHostName")) if h}
def pathrx(p):
    alt = {" ": r"(?:\\ | |%20|-)", "!": r"(?:\\!|!|%21|-)", "/": r"(?:/|%2F|-)"}
    return re.compile("".join(alt.get(c, re.escape(c)) for c in p), re.I)
C = {"account_name": [re.compile(r"(?<![A-Za-z])%s(?![a-z])" % re.escape(p), re.I) for p in set(re.split(r"\s+", FULL) + [USER]) if len(p) >= 3],
     "machine_name": [re.compile(re.escape(h), re.I) for h in HOSTS],
     "home_path": [pathrx(HOME)],
     "email": [re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]*[A-Za-z]{2,}")],
     "uuid": [re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)],
     "prompt_or_agent_id_value": [re.compile(r"\"(?:prompt|agent)_?[iI]d\"\s*:\s*\"(?!<)[^\"]+\"")],
     "req_msg_toolu_id": [re.compile(r"\b(?:req|msg|toolu)_[A-Za-z0-9]{8,}")],
     "tmp_uid_path": [re.compile(r"/(?:private/)?tmp/(?:tmux|claude)-\d+/")]}
for i, r in enumerate(opt("--roots", True)):
    C["root%d" % (i + 1)] = [pathrx(r.rstrip("/"))]
for i, w in enumerate(opt("--names", True)):
    C["name%d" % (i + 1)] = [re.compile(r"(?:^|[/\\\s'\"(=-])%s(?=$|[/\\\s'\")])" % re.escape(w), re.I | re.M),
                             re.compile(r"%%(?:2F|5C)%s(?=%%(?:2F|5C)|$|[\s'\")])" % re.escape(w), re.I | re.M)]   # R2
for i, w in enumerate(opt("--literals", True)):                                                        # R2
    C["literal%d" % (i + 1)] = [re.compile(re.escape(w), re.I)]
C["old_tail"] = [re.compile(r"\.claude[/\\]+plugins[/\\]+marketplaces", re.I)]                     # R2
ANSI = re.compile(rb"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b[@-_]")
CTRL = re.compile(rb"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
def scan(b):
    hits = {}
    for fb in (b, ANSI.sub(b"", b), b.replace(b"\\", b""), urllib.parse.unquote_to_bytes(b), CTRL.sub(b"", b)):
        t = fb.decode("utf-8", "replace")
        for c, rxs in C.items():
            n = sum(len(rx.findall(t)) for rx in rxs)
            if n: hits[c] = max(hits.get(c, 0), n)
    return hits
print("classes: %s" % sorted(C))
if opt("--control"):
    h = scan(open(opt("--control"), "rb").read()); print("CONTROL %s -> %s" % (os.path.basename(opt("--control")), h)); sys.exit(0)
cl, rev, base = opt("--clone"), opt("--rev"), opt("--base")
g = lambda *x: subprocess.run(["git", "-C", cl, *x], capture_output=True).stdout
names = [n for n in g("ls-tree", "-r", "--name-only", rev, "--", "spikes/U-B2-host-facts").decode().split("\n") if n]
tot = {}; nfiles = nbin = 0
for n in names:
    b = g("show", "%s:%s" % (rev, n)); nfiles += 1; nbin += b"\x00" in b
    h = scan(b)
    if h:
        print("HIT %s %s" % (n[len("spikes/U-B2-host-facts/"):], h))
        for k, v in h.items(): tot[k] = tot.get(k, 0) + v
for d in ("BACKLOG.md", "docs/M0-OUTCOMES.md"):
    diff = g("diff", base, rev, "--", d)
    added = b"\n".join(l[1:] for l in diff.split(b"\n") if l.startswith(b"+") and not l.startswith(b"+++"))
    h = scan(added); nfiles += 1
    if h:
        print("HIT added lines of %s %s" % (d, h))
        for k, v in h.items(): tot[k] = tot.get(k, 0) + v
print("scanned %d items (%d binary); totals per class: %s" % (nfiles, nbin, tot))
