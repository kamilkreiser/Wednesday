#!/usr/bin/env python3
"""special_attack2.py <work dir> <socket dir> - SP4b (the aftermath of one torn rebuild), SP6 bounded, SP8."""
import os, sys, time, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *

work, sock = sys.argv[1], sys.argv[2]
pgd = os.path.join(work, "pg")
P = lambda s: print(s, flush=True)


def les(root, name, tok):
    w(root, L + name, FM + "\n# Lesson\n\nThe word is %s here.\n" % tok)


P("== SP4b. one torn rebuild, then what search, check and doctor say (the writer is stopped in state A: own text, row all)")
root = os.path.join(work, "sp4b"); rows = base_tree(root)
Z = "2027-01-02_q-flip.md"
for i in range(300):
    n = "2027-06-%02d_q-fill-%03d.md" % (i % 28 + 1, i); les(root, n, "qzfill%03d" % i); rows.append(row(n))
zpath = os.path.join(root, L + Z); ipath = os.path.join(root, L + "_rules_index.tsv")
TXT = lambda t: FM + "\n# Flip\n\nThe word is %s here.\n" % t
IDX = lambda seats: "# header\n" + "\n".join(rows + [row(Z, seats, rule="When testing: qzfliprule%s do it." % seats)]) + "\n"


def put(path, text):
    tmp = os.path.join(work, "sp4.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, path)


put(zpath, TXT("qzflipOWN")); put(ipath, IDX("all"))
stop = threading.Event()


def writer():
    while not stop.is_set():
        put(ipath, IDX("tuesday")); put(zpath, TXT("qzflipOTHER")); time.sleep(0.003)   # A -> B: row first, then text
        put(zpath, TXT("qzflipOWN")); put(ipath, IDX("all")); time.sleep(0.003)          # B -> A: text first, then row


th = threading.Thread(target=writer); th.start()
got = None
for i in range(80):
    rc, out = tool(["rebuild"], root, pgd, sock)
    d, err = dump(sock)
    if rc == 0 and d and "qzflipOTHER" in d:
        got = i; break
stop.set(); th.join()
P("  disk now: lesson text holds %s; index row seats = %s" % ("qzflipOWN" if "qzflipOWN" in open(zpath).read() else "qzflipOTHER",
                                                                [l.split("\t")[2] for l in open(ipath).read().split("\n") if l.startswith(Z)]))
if got is None:
    P("  no torn rebuild in 80 tries (INSTRUMENT: nothing shown this run)")
else:
    P("  rebuild number %d returned rc 0 with the OTHER text indexed; its last line: %s" % (got + 1, out.strip().split("\n")[-1]))
    P("  the report names the lesson as left out: %s" % (Z in out))
    rc, so = tool(["search", "qzflipOTHER"], root, pgd, sock)
    P("  search qzflipOTHER rc %d:\n%s" % (rc, "\n".join("      " + l for l in so.strip().split("\n")[:6])))
    rc, ao = tool(["at", "drive"], root, pgd, sock)
    P("  at drive: rule line for the lesson present %d (which seats word it carries: %s)" % (ao.count("qzfliprule"), "all" if "qzfliprulall" in ao.replace("rule", "rul") else "?"))
    rc, co = tool(["check"], root, pgd, sock)
    P("  check rc %d: %s" % (rc, " / ".join(co.strip().split("\n")[:2])[:300]))
    rc, do = tool(["doctor"], root, pgd, sock)
    P("  doctor rc %d: %s" % (rc, do.strip()[:160]))
    rc, uo = tool(["up"], root, pgd, sock)
    d, err = dump(sock)
    P("  after `up` (which rebuilds because check is red): rc %d, OTHER text in the index %d, OWN text %d" % (rc, d.count("qzflipOTHER"), d.count("qzflipOWN")))

P("== SP6 (bounded). a lesson that grows by 100 MB while one rebuild reads it")
root = os.path.join(work, "sp6"); rows = base_tree(root)
G = "2027-07-02_q-grow.md"; les(root, G, "qzsp6grow")
w(root, L + "_rules_index.tsv", "# h\n" + "\n".join(rows + [row(G)]) + "\n")
stop = threading.Event()


def grower():
    n = 0
    with open(os.path.join(root, L + G), "a") as f:
        while not stop.is_set() and n < 100 * 1024 * 1024:
            s = "more words here qzsp6more\n" * 400; f.write(s); f.flush(); n += len(s); time.sleep(0.001)


th = threading.Thread(target=grower); th.start()
t0 = time.time(); rc, out = tool(["rebuild"], root, pgd, sock, timeout=900)
stop.set(); th.join()
P("  rebuild rc %d in %.1f s; traceback %s; file is now %d bytes; last line: %s" % (rc, time.time() - t0, "Traceback" in out, os.path.getsize(os.path.join(root, L + G)), out.strip().split("\n")[-1][:200]))
rc, co = tool(["check"], root, pgd, sock); P("  check rc %d: %s" % (rc, co.split("\n")[0][:200]))
os.truncate(os.path.join(root, L + G), 200)

P("== SP8. a 300 MB sparse lesson file (NUL bytes after a clean head)")
root = os.path.join(work, "sp8"); rows = base_tree(root)
H = "2027-07-03_q-huge.md"; les(root, H, "qzsp8huge")
w(root, L + "_rules_index.tsv", "# h\n" + "\n".join(rows + [row(H)]) + "\n")
with open(os.path.join(root, L + H), "r+b") as f:
    f.truncate(300 * 1024 * 1024)
t0 = time.time(); rc, out = tool(["rebuild"], root, pgd, sock, timeout=900)
P("  rebuild rc %d in %.1f s; traceback %s; named: %s; last line: %s" % (rc, time.time() - t0, "Traceback" in out, left_out_from_report(out), out.strip().split("\n")[-1][:200]))
os.truncate(os.path.join(root, L + H), 200)
rc, so = tool(["stop"], root, pgd, sock); P("stop rc %d: %s" % (rc, so.strip().split("\n")[-1]))
