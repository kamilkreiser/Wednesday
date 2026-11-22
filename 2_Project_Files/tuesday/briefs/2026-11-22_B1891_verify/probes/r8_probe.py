"""B1891 round 2: R8 against `git check-attr filter` for shapes the kit's r8_vs_git.py did not list.
usage: python3 -I r8_probe.py <head clone> <out folder>. One tiny git repository per shape (a.bin, x, x y tracked)."""
import sys, os, subprocess
H, OUT = sys.argv[1], sys.argv[2]
RR = os.path.join(H, "build", "repo_rules.py")
cases = {
 "control-space": b"* filter=lfs\n",
 "control-lone-cr-r1-F3": b"* -text\rfilter=lfs\n",
 "quoted-pattern-no-blank-after": b'"a.bin"filter=lfs\n',
 "quoted-pattern-star-no-blank": b'"*"filter=lfs\n',
 "quoted-pattern-with-space-no-blank": b'"x y"filter=lfs\n',
 "macro-defined-then-used": b"[attr]keep filter=lfs\n* keep\n",
 "macro-use-only-control": b"* binary\n",
}
for label, data in cases.items():
    d = os.path.join(OUT, label); os.makedirs(d)
    g = lambda *a: subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True)
    g("init", "-q")
    for n in ("a.bin", "x", "x y"):
        open(os.path.join(d, n), "w").write("t\n")
    open(os.path.join(d, ".gitattributes"), "wb").write(data)
    g("add", "-A")
    ca = g("check-attr", "filter", "--", "a.bin", "x y").stdout.strip().replace("\n", " ; ")
    r = subprocess.run([sys.executable, "-I", RR, d], capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if not l.startswith("RULES-NOTE")]
    print("%-36s git: %-48s | R8 rc %d %s" % (label, ca, r.returncode, " ; ".join(lines)))
