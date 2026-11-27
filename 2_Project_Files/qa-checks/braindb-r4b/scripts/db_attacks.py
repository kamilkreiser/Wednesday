#!/usr/bin/env python3
"""db_attacks.py <work dir> <socket dir> - the right database inside the same session, and the server life cycle.
Every server here has its data directory under <work dir>. After each block: a process listing that selects by
EXECUTABLE (postgres) and reads -D, with a positive control."""
import os, sys, time, subprocess, hashlib, re, signal, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *

work, sock = sys.argv[1], sys.argv[2]
P = lambda s: print(s, flush=True)
c1, c2, c3 = work + "/c1", work + "/c2", work + "/c3"
t1, t2 = work + "/t1", work + "/t2"
PY = sys.executable


def mini(root, tok, n=0):
    rows = base_tree(root)
    w(root, L + "2027-01-03_q-own.md", FM + "\n# Own\n\nThe word is %s here.\n" % tok)
    rows.append(row("2027-01-03_q-own.md", rule="When testing: %srule do it." % tok))
    for i in range(n):
        w(root, "0_Brain/skills/bulk-%03d.md" % i, "# bulk %d\n\n" % i + "".join("## part %d\n\n%s\n\n" % (k, ("lorem ipsum dolor sit amet word%d k%d " % (i, k)) * 80) for k in range(300)))
    w(root, L + "_rules_index.tsv", "# h\n" + "\n".join(rows) + "\n")


def procs(under=None):
    """[(pid, -D value)] for every process whose executable is postgres AND whose command line carries -D (the postmasters)"""
    snap = subprocess.run(["ps", "-axww", "-o", "pid=,comm="], stdout=subprocess.PIPE).stdout.decode()
    out = []
    for line in snap.strip().split("\n"):
        pid, comm = line.strip().split(None, 1)
        if comm.rsplit("/", 1)[-1] != "postgres":
            continue
        cmd = subprocess.run(["ps", "-ww", "-p", pid, "-o", "command="], stdout=subprocess.PIPE).stdout.decode().strip()
        m = re.search(r" -D (\S+)", cmd)
        if m and (under is None or m.group(1).startswith(under)):
            out.append((pid, m.group(1)))
    return out


def proc_line(label):
    mine = procs(work)
    P("  [procs after %s] postgres postmasters with -D under my work dir: %d %s ; all postmasters on this Mac: %d" % (
        label, len(mine), [d[len(work):] for _, d in mine], len(procs())))


def count(sockdir, pat, port="5432"):
    rc, out, err = psql(sockdir, "select count(*) from brain.chunks where body like '%%%s%%'" % pat, port=port)
    return out if rc == 0 else "ERR(%s)" % err[:80]


def holder(lock, release):
    p = subprocess.Popen([PY, "-c", "import fcntl,os,sys,time\nfd=os.open(sys.argv[1],os.O_RDWR|os.O_CREAT,0o600); fcntl.flock(fd,fcntl.LOCK_EX); open(sys.argv[2]+'.held','w').close()\nt=time.time()\nwhile not os.path.exists(sys.argv[2]) and time.time()-t<120: time.sleep(0.1)", lock, release])
    while not os.path.exists(release + ".held"):
        time.sleep(0.05)
    return p


def bg(args, root, pgd, extra=None, outname="bg.out"):
    e = dict(BRAINDB_ROOT=root, BRAINDB_PGDATA=pgd, BRAINDB_SOCKDIR=sock); e.update(extra or {})
    f = open(os.path.join(work, outname), "w")
    return subprocess.Popen(["/bin/bash", TOOL] + args, env=clean_env(e), stdout=f, stderr=subprocess.STDOUT, start_new_session=True), f


def pgctl(*a):
    r = subprocess.run([PGBIN + "/pg_ctl"] + list(a), env=clean_env(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return r.returncode, r.stdout.decode()[-300:]


P("uptime: " + subprocess.run(["uptime"], stdout=subprocess.PIPE).stdout.decode().strip())
mini(t1, "zonetok"); mini(t2, "ztwotok")
rc, o = tool(["rebuild"], t2, c2, sock); P("setup: c2 built from t2 rc %d" % rc)
proc_line("building c2 (POSITIVE CONTROL: expect 1, /c2)")
rc, o = tool(["stop"], t2, c2, sock); P("setup: c2 stopped rc %d" % rc)
rc, o = tool(["rebuild"], t1, c1, sock); P("setup: c1 built from t1 rc %d (c1 now answers on the shared socket directory)" % rc)

P("== DB1. the second checker's F2c: the server is swapped while a rebuild addressed to c1 waits for c1's lock")
h = holder(c1 + ".lock", work + "/h1.release")
p, f = bg(["rebuild"], t1, c1, outname="db1.out"); time.sleep(2.5)
P("  the rebuild is waiting: %s" % (p.poll() is None))
P("  pg_ctl stop c1: rc %d" % pgctl("-D", c1, "-m", "fast", "-w", "stop")[0])
rc, o = tool(["start"], t2, c2, sock); P("  c2 started on the same socket directory: rc %d" % rc)
open(work + "/h1.release", "w").close(); h.wait(); rc = p.wait(); f.close(); o = open(work + "/db1.out").read()
P("  rebuild addressed to c1: rc %d (want 4); says: %s" % (rc, [l for l in o.split("\n") if "REFUSED" in l][:1]))
P("  'rebuild: done' printed: %s ; c2 holds ztwotok %s (want >0) and zonetok %s (want 0)" % ("rebuild: done" in o, count(sock, "ztwotok"), count(sock, "zonetok")))

P("== DB2. the narrow form: swapped after every separate session, before the load session (BRAINDB_TEST_HOLD)")
rc, o = tool(["stop"], t2, c2, sock); rc, o = tool(["start"], t1, c1, sock)
p, f = bg(["rebuild"], t1, c1, extra=dict(BRAINDB_TEST_HOLD=work + "/hold2"), outname="db2.out")
t0 = time.time()
while not os.path.exists(work + "/hold2.waiting") and time.time() - t0 < 60:
    time.sleep(0.05)
P("  the rebuild reached the hold point: %s" % os.path.exists(work + "/hold2.waiting"))
pgctl("-D", c1, "-m", "fast", "-w", "stop"); rc, o = tool(["start"], t2, c2, sock)
open(work + "/hold2", "w").close(); rc = p.wait(); f.close(); o = open(work + "/db2.out").read()
P("  rebuild addressed to c1: rc %d (want 4); 'rebuild: done' printed: %s ; c2 holds ztwotok %s and zonetok %s (want 0)" % (rc, "rebuild: done" in o, count(sock, "ztwotok"), count(sock, "zonetok")))

P("== DB3. reads addressed to c1 while c2 answers (self-start off)")
for c in (["check"], ["search", "ztwotok"], ["at", "drive"], ["status"], ["doctor"]):
    rc, o = tool(c, t1, c1, sock, extra=dict(BRAINDB_NO_AUTOSTART="1"))
    P("  %-16s rc %d ; printed GREEN %s, the other tree's token %s, a rule list %s ; first line: %s" % (" ".join(c), rc, "GREEN" in o, "ztwotok" in o.replace('"ztwotok"', ""), "Rules for" in o, o.strip().split("\n")[0][:110]))
rc, o = tool(["search", "ztwotok"], t1, c1, sock)
P("  search with self-start ON (c1 is down, c2 holds the socket): rc %d ; token printed %s ; last line: %s" % (rc, "q-own.md" in o, o.strip().split("\n")[-1][:160]))
proc_line("DB3")
rc, o = tool(["stop"], t1, c1, sock); P("  (stop c1 if that started it: rc %d %s)" % (rc, o.strip().split("\n")[-1][:80]))

P("== DB3b. a cluster with NO braindb database answers; a rebuild addressed to c1 must not CREATE one there")
rc, o = tool(["stop"], t2, c2, sock)
rc, o = tool(["init"], t1, c3, sock); rc2, o2 = tool(["start"], t1, c3, sock); P("  c3 created and started (no index database): rc %d %d" % (rc, rc2))
rc, o = tool(["rebuild"], t1, c1, sock, extra=dict(BRAINDB_NO_AUTOSTART="1"))
r2 = psql(sock, "select count(*) from pg_database where datname = 'braindb'", db="postgres")
P("  rebuild addressed to c1 (self-start off): rc %d (want 4) ; databases named braindb in c3 now: %s (want 0)" % (rc, r2[1]))
rc, o = tool(["rebuild"], t1, c1, sock)
r2 = psql(sock, "select count(*) from pg_database where datname = 'braindb'", db="postgres")
P("  the same with self-start ON: rc %d ; braindb in c3: %s (want 0) ; last line: %s" % (rc, r2[1], o.strip().split("\n")[-1][:200]))
rc, o = tool(["stop"], t1, c3, sock); P("  c3 stopped rc %d" % rc)
proc_line("DB3b")
rc, o = tool(["stop"], t1, c1, sock)

P("== DB4. the data directory is replaced by a SYMLINK to another cluster between sessions")
os.rename(c1, c1 + ".real"); os.symlink(c2, c1)
rc, o = tool(["search", "ztwotok"], t1, c1, sock)
P("  search addressed to the path c1 (tree t1), which is now a link to c2: rc %d ; returned the OTHER tree's lesson: %s" % (rc, "q-own.md" in o))
rc, o = tool(["check"], t1, c1, sock); P("  check: rc %d ; %s" % (rc, " / ".join(o.strip().split("\n")[:2])[:220]))
rc, o = tool(["status"], t1, c1, sock); P("  status: rc %d ; data directory line: %s" % (rc, [l for l in o.split("\n") if l.startswith("data directory")]))
proc_line("DB4 (the server runs with -D c2: the link's target)")
rc, o = tool(["stop"], t1, c1, sock); P("  stop through the link: rc %d %s" % (rc, o.strip().split("\n")[-1][-60:]))
os.unlink(c1); os.rename(c1 + ".real", c1)

P("== DB5. another SEAT's tool addressed to this seat's cluster (BRAINDB_PGDATA): does search or at notice the index is not its own?")
sim = work + "/sim/TUESDAY/2_Project_Files"
os.makedirs(sim + "/fleet/cockpit"); os.makedirs(sim + "/tools")
lane = os.path.dirname(TOOL); pf = os.path.dirname(lane)
shutil.copytree(lane, sim + "/brain-db", ignore=shutil.ignore_patterns("evidence", "__pycache__"))
shutil.copy(pf + "/fleet/cockpit/seat_resolve.sh", sim + "/fleet/cockpit/"); shutil.copy(pf + "/tools/seat_note.sh", sim + "/tools/")
shutil.copy(sim + "/brain-db/proposed/scope/tuesday.scope", sim + "/brain-db/scope/tuesday.scope")
TT = sim + "/brain-db/braindb.sh"
w(t1, L + "_ledger_laptop_datasec.md", "# L\n"); os.makedirs(t1 + "/0_Brain/daily_tuesday", exist_ok=True)
rc, o = tool(["search", "zonetok"], t1, c1, sock, toolpath=TT)
P("  TUESDAY tool, search zonetok in the index the WEDNESDAY tool built: rc %d ; result printed: %s ; seat line check: %s" % (rc, "q-own.md" in o, [l for l in o.split("\n") if "seat" in l.lower()][:1]))
rc, o = tool(["search", "qzledger"], t1, c1, sock, toolpath=TT)
P("  TUESDAY tool, search qzledger (a row of the Wednesday seat's LEDGER in that index): rc %d ; ledger row printed: %s" % (rc, "_ledger.md" in o))
rc, o = tool(["at", "drive"], t1, c1, sock, toolpath=TT); P("  TUESDAY tool, at drive: rc %d ; %s" % (rc, o.strip().split("\n")[0][:120]))
rc, o = tool(["check"], t1, c1, sock, toolpath=TT); P("  TUESDAY tool, check: rc %d ; %s" % (rc, o.strip().split("\n")[0][:260]))
rc, o = tool(["stop"], t1, c1, sock, toolpath=TT); P("  stop rc %d" % rc)
proc_line("DB5")

P("== DB6. a server started BY HAND")
so = "-c listen_addresses='' -c unix_socket_directories='%s' -c unix_socket_permissions=0700 -c port=5432" % sock
rc, o = pgctl("-D", c1, "-l", work + "/hand.log", "-w", "-o", so, "start"); P("  (a) by hand with the SAME spelling of -D: pg_ctl rc %d" % rc)
for c in (["status"], ["check"], ["stop"]):
    rc, o = tool(c, t1, c1, sock, extra=dict(BRAINDB_NO_AUTOSTART="1")); P("      %-7s rc %d ; %s" % (c[0], rc, [l for l in o.strip().split("\n") if l.startswith(("server:", "check:", "stop:", "braindb:"))][:1]))
proc_line("DB6a (the tool's stop took the hand-started server: want 0)")
os.symlink(c1, work + "/c1link")
rc, o = pgctl("-D", work + "/c1link", "-l", work + "/hand.log", "-w", "-o", so, "start"); P("  (b) by hand THROUGH A SYMLINK spelling of -D: pg_ctl rc %d" % rc)
proc_line("DB6b start (POSITIVE CONTROL: expect 1, /c1link)")
for c in (["status"], ["check"], ["search", "zonetok"], ["start"], ["stop"]):
    rc, o = tool(c, t1, c1, sock, extra=dict(BRAINDB_NO_AUTOSTART="1") if c[0] in ("check",) else None)
    P("      %-7s rc %d ; %s" % (c[0], rc, " | ".join(l[:230] for l in o.strip().split("\n") if l.startswith(("server:", "check:", "stop:", "braindb:", "start:")))[:520]))
proc_line("DB6b after the tool's stop (the tool said what it said above; is the server still up?)")
rc, o = pgctl("-D", work + "/c1link", "-m", "fast", "-w", "stop"); P("  my own pg_ctl stop through the same spelling: rc %d" % rc)
proc_line("DB6b after my stop (want 0)")

P("== DB7. the lock wait has a limit")
h = holder(c1 + ".lock", work + "/h7.release")
for c in (["rebuild"], ["start"], ["stop"], ["search", "zonetok"]):
    t0 = time.time(); rc, o = tool(c, t1, c1, sock, extra=dict(BRAINDB_LOCK_WAIT="3"))
    P("  %-8s behind a holder, limit 3 s: rc %d after %.1f s ; %s" % (c[0], rc, time.time() - t0, o.strip().split("\n")[-1][-120:]))
open(work + "/h7.release", "w").close(); h.wait()
proc_line("DB7")

P("== DB8. kill -9 of the tool in the middle of a rebuild; then what check says and what the index holds")
big = work + "/tbig"; mini(big, "zbigtok", n=120)
rc, o = tool(["rebuild"], big, c1, sock); P("  baseline rebuild of a 120-file, ~110 MB tree: rc %d ; %s" % (rc, [l.strip() for l in o.split("\n") if "time:" in l]))


def state():
    d, err = dump(sock)
    if d is None:
        return "DUMP-ERR " + err[:80], 0, 0
    keep = "\n".join(l for l in d.split("\n") if "built_at" not in l and not re.match(r"^.(un)?restrict ", l))
    return hashlib.sha256(keep.encode()).hexdigest()[:16], d.count("zkilltok"), len(d)


h0 = state(); P("  baseline index: hash %s, zkilltok %d, dump bytes %d" % h0)
res = []
for i, delay in enumerate((0.3, 0.8, 1.5, 2.5, 3.5, 4.5, 6.0, 8.0)):
    w(big, "0_Brain/skills/kill.md", "# kill\n\nzkilltok round %d\n" % i)
    p, f = bg(["rebuild"], big, c1, outname="db8-%d.out" % i)
    time.sleep(delay)
    alive = p.poll() is None
    if alive:
        os.killpg(p.pid, signal.SIGKILL)
    p.wait(); f.close(); time.sleep(1.5)
    left = subprocess.run(["pgrep", "-f", "psql .*-h %s " % sock], stdout=subprocess.PIPE).stdout.decode().split()
    st = state()
    rc, co = tool(["check"], big, c1, sock, extra=dict(BRAINDB_NO_AUTOSTART="1"))
    line = co.strip().split("\n")[0][:90]
    res.append((delay, alive, st, rc, line, left))
    P("  kill -9 after %.1f s (still running: %s): index hash %s, kill.md rows of THIS round in the index: %s ; psql left: %s ; check rc %d: %s" % (
        delay, alive, st[0], psql(sock, "select count(*) from brain.chunks where body like '%%zkilltok round %d%%'" % i)[1], left, rc, line))
P("  (read: a round is consistent when EITHER its kill.md row is absent and check is RED naming the change, OR the row is present and check is GREEN)")
rc, o = tool(["rebuild"], big, c1, sock); rc2, co = tool(["check"], big, c1, sock); P("  a normal rebuild afterwards: rc %d ; check rc %d %s" % (rc, rc2, co.split("\n")[0][:60]))
proc_line("DB8")

P("== DB9. two rebuilds at once, three trials; DB10. rebuilds while searches run")
for t in range(3):
    a, fa = bg(["rebuild"], big, c1, outname="db9a.out"); b, fb = bg(["rebuild"], big, c1, outname="db9b.out")
    ra, rb = a.wait(), b.wait(); fa.close(); fb.close()
    rc, co = tool(["check"], big, c1, sock)
    P("  trial %d: rc %d and %d ; check rc %d %s" % (t + 1, ra, rb, rc, co.split("\n")[0][:50]))
stopf = work + "/db10.stop"
loop = subprocess.Popen(["/bin/bash", "-c", 'while [ ! -e "$0" ]; do /bin/bash "$1" rebuild > /dev/null 2>&1; done' , stopf, TOOL],
                        env=clean_env(dict(BRAINDB_ROOT=big, BRAINDB_PGDATA=c1, BRAINDB_SOCKDIR=sock)))
okc = bad = 0; bads = []
for i in range(25):
    rc, o = tool(["search", "zbigtok"], big, c1, sock)
    if rc == 0 and "q-own.md" in o:
        okc += 1
    else:
        bad += 1; bads.append((rc, o.strip().split("\n")[-1][:140]))
open(stopf, "w").close(); loop.wait()
P("  25 searches while rebuilds ran back to back: %d answered with the lesson, %d did not %s" % (okc, bad, bads[:3]))

P("== DB11. stop, and what the tool reports against what runs")
proc_line("before stop (POSITIVE CONTROL: expect 1, /c1)")
rc, o = tool(["stop"], big, c1, sock); P("  stop rc %d: %s" % (rc, o.strip().split("\n")[-1][-70:]))
rc, o = tool(["status"], big, c1, sock); P("  status rc %d: %s" % (rc, [l for l in o.split("\n") if l.startswith("server:")]))
proc_line("stop (want 0)")
P("  postmaster.pid files left under my work dir: %s" % [r for r, d, fs in os.walk(work) if "postmaster.pid" in fs and "/base" not in r])

P("== DB12. init, start, status and stop given a scope file that EXISTS but is refused")
badscope = work + "/bad.scope"
open(badscope, "w").write(open(lane + "/scope/wednesday.scope").read().replace("seat wednesday", "seat tuesday"))
for c in (["status"], ["doctor"], ["check"], ["init"], ["start"], ["stop"]):
    rc, o = tool(c, t1, work + "/c12", sock, scope=badscope)
    P("  %-7s rc %d ; cluster directory exists: %s ; lock file exists: %s ; %s" % (c[0], rc, os.path.exists(work + "/c12"), os.path.exists(work + "/c12.lock"), o.strip().split("\n")[-1][:110]))
proc_line("DB12 (want 0)")
P("uptime: " + subprocess.run(["uptime"], stdout=subprocess.PIPE).stdout.decode().strip())
