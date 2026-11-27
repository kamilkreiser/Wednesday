#!/usr/bin/env python3
"""tests/f1_paced_attack.py <braindb.sh of a scratch copy> <work dir> <socket dir> <pause seconds> [rebuilds]

ROUND 5, F1. The third checker's SP4 writer (qa-checks/braindb-r4b/scripts/special_attack.py) with ONE thing
made a parameter: the pause between its transitions. SP4 pauses 3 ms, which is shorter than one read of its
300-lesson tree, so against a tool that validates its snapshot every rebuild is refused and SP4's own control
("the instrument saw both states") cannot be met. With a pause of the order of one read, some rebuilds meet a
still tree and finish, some are refused, and the question SP4 asks can be answered WITH its control:
is the OTHER text (scoped to tuesday at every instant it existed on disk) ever indexed?

States: A = (lesson text qzflipOWN, row scoped all), B = (lesson text qzflipOTHER, row scoped tuesday).
The writer goes A->B row first then text, B->A text first then row, each by atomic replace of a whole file.

BOUNDED: the writer only ever replaces two small files with fixed text; nothing grows. It runs a fixed number
of rebuilds (default 40) and stops. Never point it at a lane or a real tree: it builds its own tree in <work dir>
and addresses its own cluster there. Standard library only.
"""
import os, sys, time, threading, subprocess, random

TOOL, work, sock, pause = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
N = int(sys.argv[5]) if len(sys.argv) > 5 else 40
PGBIN = "/opt/homebrew/opt/postgresql@15/bin"
L = "0_Brain/learnings/"
root, pgd = os.path.join(work, "tree"), os.path.join(work, "pg")
FM = "---\ndate: 2027-01-01\ntype: correction\nstatus: live\ntier: W\n---\n"
P = lambda s: print(s, flush=True)


def env():
    e = dict((k, v) for k, v in os.environ.items() if not k.startswith("BRAINDB_") and k != "WED_AGENT" and not k.startswith("PG"))
    e.update(BRAINDB_ROOT=root, BRAINDB_PGDATA=pgd, BRAINDB_SOCKDIR=sock)
    return e


def tool(*args):
    r = subprocess.run(["/bin/bash", TOOL] + list(args), env=env(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
    return r.returncode, r.stdout.decode("utf-8", errors="replace")


def dump():
    r = subprocess.run([PGBIN + "/pg_dump", "--data-only", "--schema=brain", "-h", sock, "-d", "braindb"], env=env(),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return r.stdout.decode("utf-8", errors="replace") if r.returncode == 0 else ""


def put(path, text):
    tmp = os.path.join(work, "put.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, path)


def row(key, seats="all", rule="When testing: do the thing."):
    return "\t".join([key, "live", seats, "learning-loop", "drive", "-", rule])


os.makedirs(os.path.join(root, L))
rows = [row("2027-01-01_q-control.md", rule="When testing: qzcontrolrule do it.")]
put(os.path.join(root, L + "2027-01-01_q-control.md"), FM + "\n# Control\n\nThe word is qzcontrol here.\n")
for i in range(300):
    n = "2027-06-%02d_q-fill-%03d.md" % (i % 28 + 1, i)
    put(os.path.join(root, L + n), FM + "\n# Lesson\n\nThe word is qzfill%03d here.\n" % i); rows.append(row(n))
Z = "2027-01-02_q-flip.md"
zpath, ipath = os.path.join(root, L + Z), os.path.join(root, L + "_rules_index.tsv")
TXT = lambda t: FM + "\n# Flip\n\nThe word is %s here.\n" % t
IDX = lambda seats: "# header\n" + "\n".join(rows + [row(Z, seats, rule="When testing: qzfliprule%s do it." % seats)]) + "\n"
put(zpath, TXT("qzflipOWN")); put(ipath, IDX("all"))
stop = threading.Event(); flips = [0]
rnd = random.Random(5)


def writer():
    while not stop.is_set():
        put(ipath, IDX("tuesday")); put(zpath, TXT("qzflipOTHER")); time.sleep(pause * (0.5 + rnd.random()))
        put(zpath, TXT("qzflipOWN")); put(ipath, IDX("all")); time.sleep(pause * (0.5 + rnd.random()))
        flips[0] += 1


P("== F1 paced attack: %d rebuilds, the writer pauses about %.3f s between transitions; tool %s" % (N, pause, TOOL))
rc, out = tool("rebuild")            # the first rebuild creates the cluster, before the writer starts
P("   first rebuild (tree still): rc %d" % rc)
th = threading.Thread(target=writer); th.start()
own = other = neither = failed = refused = retries = 0
for i in range(N):
    rc, out = tool("rebuild")
    retries += out.count("the tree changed while it was read (try")
    if rc != 0:
        failed += 1
        refused += "REFUSED: the tree changed while it was read; nothing was changed in the index" in out
        continue
    d = dump()
    if "qzflipOTHER" in d:
        other += 1
        open(os.path.join(work, "leak-%d.rebuild.out" % i), "w").write(out)
    elif "qzflipOWN" in d:
        own += 1
    else:
        neither += 1
stop.set(); th.join()
P("  %d rebuilds while the pair flipped %d times: indexed with OWN text %d, left out %d, rebuild failed %d (of them refused "
  "'the tree changed while it was read' %d), **indexed with OTHER text %d**; 'read it again' notices %d"
  % (N, flips[0], own, neither, failed, refused, other, retries))
P("  control (the instrument saw both states and at least one finished rebuild of each): own %d > 0 and left out %d > 0: %s"
  % (own, neither, "MET" if own and neither else "NOT MET"))
rc, out = tool("stop"); P("stop rc %d: %s" % (rc, out.strip().split("\n")[-1]))
