"""B1894 round 3: more N3-class shapes (git's quoted pattern) against git check-attr and the tree's repo_rules.py.
usage: python3 -I r8_more.py <tree> <out>"""
import sys, os, subprocess
H, OUT = sys.argv[1], sys.argv[2]
RR = os.path.join(H, "build", "repo_rules.py")
cases = {
 "indented-quoted": (".gitattributes", b'   "a.bin"filter=lfs\n'),
 "tab-led-quoted": (".gitattributes", b'\t"a.bin"filter=lfs\n'),
 "cr-led-quoted": (".gitattributes", b'\r"a.bin"filter=lfs\n'),
 "bom-led-quoted": (".gitattributes", b'\xef\xbb\xbf"a.bin"filter=lfs\n'),
 "hash-inside-quoted-pattern": (".gitattributes", b'"#a.bin"filter=lfs\n"a.bin"filter=lfs\n'),
 "escaped-quote-in-pattern": (".gitattributes", b'"a\\".bin"filter=lfs\n"a.bin"filter=lfs\n'),
 "quoted-then-tab": (".gitattributes", b'"a.bin"\tfilter=lfs\n'),
 "crlf-file-quoted": (".gitattributes", b'* -text\r\n"a.bin"filter=lfs\r\n'),
 "nested-sub-quoted": ("sub/.gitattributes", b'"a.bin"filter=lfs\n'),
 "second-line-after-plain": (".gitattributes", b'* -text\n"a.bin"filter=lfs\n'),
 "no-final-lf": (".gitattributes", b'"a.bin"filter=lfs'),
 "quiet-comment-with-quote": (".gitattributes", b'# "a.bin"filter=lfs\n  # "x"\n* -text\n'),
}
for label, (rel, data) in cases.items():
    d = os.path.join(OUT, label); os.makedirs(os.path.join(d, "sub"))
    g = lambda *a: subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True)
    g("init", "-q")
    for n in ("a.bin", "sub/a.bin"):
        open(os.path.join(d, n), "w").write("t\n")
    open(os.path.join(d, rel), "wb").write(data)
    g("add", "-A")
    ca = g("check-attr", "filter", "--", "a.bin", "sub/a.bin").stdout.strip().replace("\n", " ; ")
    r = subprocess.run([sys.executable, "-I", RR, d], capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if not l.startswith("RULES-NOTE")]
    print("%-28s git: %-50s | rc %d %s" % (label, ca, r.returncode, " ; ".join(lines)))
