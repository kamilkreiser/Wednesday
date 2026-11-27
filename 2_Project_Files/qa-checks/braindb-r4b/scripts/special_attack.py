#!/usr/bin/env python3
"""special_attack.py <work dir> <socket dir> [drive dir] - shapes that need their own tree or a moving target.
SP1 two files whose names are equal once format characters are removed; SP2/SP3 names differing only in
normalisation or case (on the scratch volume and, when <drive dir> is given, on the drive volume);
SP4 the rules index edited DURING rebuilds; SP5 a lesson renamed between listing and open; SP6 a lesson that
grows while it is read; SP8 a 300 MB sparse lesson."""
import os, sys, time, unicodedata, threading, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *

work, sock = sys.argv[1], sys.argv[2]
drive = sys.argv[3] if len(sys.argv) > 3 else None
pgd = os.path.join(work, "pg")
P = lambda s: print(s, flush=True)


def les(root, name, tok, front=FM, body=""):
    w(root, L + name, front + "\n# Lesson\n\nThe word is %s here.\n%s" % (tok, body))


def build(root, rows):
    w(root, L + "_rules_index.tsv", "# header\n" + "\n".join(rows) + "\n")


def rebuild(root, label):
    rc, out = tool(["rebuild"], root, pgd, sock)
    open(os.path.join(work, label + ".rebuild.out"), "w").write(out)
    d = None
    if rc == 0:
        d, err = dump(sock)
    return rc, out, d or ""


def last(out):
    return out.strip().split("\n")[-1][:260]


# ---------------------------------------------------------------- SP1
P("== SP1. two lesson FILES whose names are equal once format characters are removed (one row)")
root = os.path.join(work, "sp1"); rows = base_tree(root)
X = "2027-05-01_q-dup.md"; XZ = "2027-05-01_q-dup​.md"
les(root, X, "qzsp1own"); les(root, XZ, "qzsp1twin")
build(root, rows + [row(X, rule="When testing: qzsp1rule do it.")])
rc, out, d = rebuild(root, "sp1")
P("  rebuild rc %d; last line: %s" % (rc, last(out)))
P("  psql error lines: %s" % [l for l in out.split("\n") if "ERROR" in l or "duplicate" in l][:3])
P("  in the index: qzsp1own %d, qzsp1twin %d, control qzcontrol %d" % (d.count("qzsp1own"), d.count("qzsp1twin"), d.count("qzcontrol")))
rc2, cout = tool(["check"], root, pgd, sock); P("  check rc %d: %s" % (rc2, cout.split("\n")[0][:200]))
P("== SP1b. the same, but ONLY the file with the zero-width space in its NAME exists (its row's key is the plain name)")
root = os.path.join(work, "sp1b"); rows = base_tree(root)
les(root, XZ, "qzsp1btwin"); build(root, rows + [row(X, rule="When testing: qzsp1brule do it.")])
rc, out, d = rebuild(root, "sp1b")
P("  rebuild rc %d; last line: %s" % (rc, last(out)))
P("  in the index: qzsp1btwin %d, its rule line qzsp1brule %d" % (d.count("qzsp1btwin"), d.count("qzsp1brule")))
P("== SP1c. a row scoped TUESDAY for the plain name; the file on disk carries a zero-width space in its name")
root = os.path.join(work, "sp1c"); rows = base_tree(root)
les(root, XZ, "qzsp1ctwin"); build(root, rows + [row(X, "tuesday", rule="When testing: qzsp1crule do it.")])
rc, out, d = rebuild(root, "sp1c")
P("  rebuild rc %d; in the index: qzsp1ctwin %d (want 0); named: %s" % (rc, d.count("qzsp1ctwin"), left_out_from_report(out)))

# ---------------------------------------------------------------- SP2 / SP3 on each volume
def vol_test(base, label):
    P("== SP2/SP3 on %s (%s)" % (label, base))
    root = os.path.join(base, "sp23"); rows = base_tree(root)
    nfc = "2027-05-02_q-café.md"; nfd = unicodedata.normalize("NFD", nfc)
    les(root, nfc, "qzsp2nfc")
    try:
        with open(os.path.join(root, L + nfd), "x", encoding="utf-8") as f:
            f.write(FM + "\n# twin\n\nThe word is qzsp2nfd here.\n")
        both = True
    except FileExistsError:
        both = False
    names = [n for n in os.listdir(os.path.join(root, L)) if "caf" in n]
    P("  NFC and NFD names can coexist on this volume: %s (directory lists %d name(s): %s)" % (both, len(names), [n.encode("unicode_escape").decode() for n in names]))
    lo = "2027-05-03_q-case.md"; up = "2027-05-03_Q-CASE.md"
    les(root, lo, "qzsp3lower")
    try:
        with open(os.path.join(root, L + up), "x", encoding="utf-8") as f:
            f.write(FM + "\n# twin\n\nThe word is qzsp3upper here.\n")
        cboth = True
    except FileExistsError:
        cboth = False
    P("  names differing only in case can coexist on this volume: %s" % cboth)
    build(root, rows + [row(nfc, rule="When testing: qzsp2rule do it."), row(lo, rule="When testing: qzsp3rule do it.")])
    rc, out, d = rebuild(root, "sp23-" + label)
    P("  rebuild rc %d; last line: %s" % (rc, last(out)))
    P("  psql error lines: %s" % [l for l in out.split("\n") if "ERROR" in l][:2])
    P("  in the index: qzsp2nfc %d, qzsp2nfd %d, qzsp3lower %d, qzsp3upper %d (the upper-case twin has no row: want 0)" % (
        d.count("qzsp2nfc"), d.count("qzsp2nfd"), d.count("qzsp3lower"), d.count("qzsp3upper")))
    P("  named as left out: %s" % dict((k.encode("unicode_escape").decode(), v[0]) for k, v in left_out_from_report(out).items()))


vol_test(work, "scratch-volume")
if drive:
    vol_test(drive, "drive-volume")

# ---------------------------------------------------------------- SP4
P("== SP4. the rules index edited DURING rebuilds")
P("   states: A = (lesson text qzflipOWN, row scoped all), B = (lesson text qzflipOTHER, row scoped tuesday).")
P("   the writer goes A->B row first then text, B->A text first then row: at EVERY instant on disk, text OTHER implies row tuesday.")
root = os.path.join(work, "sp4"); rows = base_tree(root)
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
stop = threading.Event(); flips = [0]


def writer():
    while not stop.is_set():
        put(ipath, IDX("tuesday")); put(zpath, TXT("qzflipOTHER")); time.sleep(0.003)
        put(zpath, TXT("qzflipOWN")); put(ipath, IDX("all")); time.sleep(0.003)
        flips[0] += 1


th = threading.Thread(target=writer); th.start()
own = other = neither = fail = torn_rule = 0
N4 = 40
for i in range(N4):
    rc, out, d = rebuild(root, "sp4")
    if rc != 0:
        fail += 1; continue
    o, x = d.count("qzflipOWN"), d.count("qzflipOTHER")
    if x:
        other += 1
        open(os.path.join(work, "sp4.leak-%d.rebuild.out" % i), "w").write(out)
    elif o:
        own += 1
    else:
        neither += 1
    if "qzfliprule" in d and not o and not x:
        torn_rule += 1
stop.set(); th.join()
P("  %d rebuilds while the pair flipped %d times: indexed with OWN text %d, left out %d, rebuild failed %d, **indexed with OTHER text %d**" % (N4, flips[0], own, neither, fail, other))
P("  (control: the instrument saw both states: own %d > 0 and left out %d > 0)" % (own, neither))

# ---------------------------------------------------------------- SP5
P("== SP5. a lesson renamed between listing and open")
root = os.path.join(work, "sp5"); rows = base_tree(root)
for i in range(200):
    n = "2027-06-%02d_q-fill-%03d.md" % (i % 28 + 1, i); les(root, n, "qzfill%03d" % i); rows.append(row(n))
A_, B_ = "2027-07-01_q-ren-a.md", "2027-07-01_q-ren-b.md"
les(root, A_, "qzsp5ren"); build(root, rows + [row(A_), row(B_)])
pa, pb = os.path.join(root, L + A_), os.path.join(root, L + B_)
stop = threading.Event(); flips = [0]


def renamer():
    while not stop.is_set():
        try:
            os.rename(pa, pb); os.rename(pb, pa); flips[0] += 1
        except OSError:
            pass


th = threading.Thread(target=renamer); th.start()
res = {"in": 0, "named-unreadable": 0, "absent-not-named": 0, "failed": 0, "traceback": 0, "done-with-faults": 0}
for i in range(30):
    rc, out, d = rebuild(root, "sp5")
    if "Traceback" in out:
        res["traceback"] += 1
    if rc != 0:
        res["failed"] += 1; continue
    if "DONE WITH FAULTS" in out:
        res["done-with-faults"] += 1
    if "qzsp5ren" in d:
        res["in"] += 1
    elif "FileNotFoundError" in out:
        res["named-unreadable"] += 1
    else:
        res["absent-not-named"] += 1
        open(os.path.join(work, "sp5.absent-%d.rebuild.out" % i), "w").write(out)
stop.set(); th.join()
P("  30 rebuilds while the file was renamed back and forth %d times: %s" % (flips[0], res))

# ---------------------------------------------------------------- SP6
P("== SP6. a lesson that grows while rebuilds read it")
root = os.path.join(work, "sp6"); rows = base_tree(root)
G = "2027-07-02_q-grow.md"; les(root, G, "qzsp6grow"); build(root, rows + [row(G)])
stop = threading.Event()


def grower():
    with open(os.path.join(root, L + G), "a") as f:
        while not stop.is_set():
            f.write("more words here qzsp6more\n" * 2000); f.flush()


th = threading.Thread(target=grower); th.start()
rcs = []
for i in range(6):
    t0 = time.time(); rc, out, d = rebuild(root, "sp6"); rcs.append((rc, round(time.time() - t0, 1), "Traceback" in out, last(out)[:60]))
stop.set(); th.join()
P("  6 rebuilds while the file grew to %d bytes: %s" % (os.path.getsize(os.path.join(root, L + G)), rcs))
rc2, cout = tool(["check"], root, pgd, sock); P("  check afterwards rc %d: %s" % (rc2, cout.split("\n")[0][:160]))

# ---------------------------------------------------------------- SP8
P("== SP8. a 300 MB sparse lesson file (all NUL bytes after a clean head)")
root = os.path.join(work, "sp8"); rows = base_tree(root)
H = "2027-07-03_q-huge.md"; les(root, H, "qzsp8huge"); build(root, rows + [row(H)])
with open(os.path.join(root, L + H), "r+b") as f:
    f.truncate(300 * 1024 * 1024)
t0 = time.time(); rc, out, d = rebuild(root, "sp8")
P("  rebuild rc %d in %.1f s; traceback %s; named: %s; last line: %s" % (rc, time.time() - t0, "Traceback" in out, left_out_from_report(out), last(out)))
rcs, so = tool(["stop"], root, pgd, sock); P("stop rc %d: %s" % (rcs, so.strip().split("\n")[-1]))
