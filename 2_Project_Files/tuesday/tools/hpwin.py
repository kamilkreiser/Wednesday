"""B250: B222 ADDENDUM-1's instrument. Every 60-character window of the HP-AUTHORED lines of the 2026-10-16 mail (Kam's own lines excluded)
is searched for in each given file (whitespace runs collapsed on both sides). Prints hits per file; never prints the mail text.
Usage: hpwin.py [--control] <file>...   (--control plants one window into a temp copy of the first file and must find it)"""
import re, sys, tempfile, os
# Default moved 2026-10-21 (s135): the mail now lives under 4_Credentials (gitignored), not tuesday/inbound/.
SRC = os.environ.get("HPWIN_SRC", "/Volumes/Laptop-DEV/TUESDAY/4_Credentials/inbound_with_secrets/2026-10-16_kam-fw-terry-hp-answers.txt")
HP = eval(os.environ.get("HPWIN_RANGES", "[(20, 75), (93, 127), (168, 501)]"))          # Terry 16 Oct; Terry 9 Oct; Terry 3 Oct, Pete, Steve (Kam's: 1-16, 76-92, 128-167)
L = open(SRC, encoding="utf-8").read().split("\n")
norm = lambda t: re.sub(r"\s+", " ", t)
hp = norm(" ".join(L[i - 1] for a, b in HP for i in range(a, min(b, len(L)) + 1)))
W = 60
wins = {hp[i:i + W] for i in range(0, len(hp) - W + 1)}
wins = {w for w in wins if len(w.strip()) == W and not re.fullmatch(r"[\W\d_ ]+", w)}
args = sys.argv[1:]; control = args and args[0] == "--control"
files = args[1:] if control else args
if control:
    w = sorted(wins)[len(wins) // 2]
    tf = tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8"); tf.write(open(files[0], encoding="utf-8").read() + "\n" + w + "\n"); tf.close()
    files = [tf.name] + files[1:]
tot = 0
for f in files:
    t = norm(open(f, encoding="utf-8", errors="replace").read())
    n = sum(1 for i in range(0, max(0, len(t) - W + 1)) if t[i:i + W] in wins)
    tot += n; print(f"{n:6d} window hits  {f if not (control and f == files[0]) else '(control copy of ' + args[1] + ')'}")
if control: os.unlink(files[0])
print("total", tot, "| windows", len(wins))
