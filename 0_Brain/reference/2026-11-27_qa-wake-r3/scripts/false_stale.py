# false_stale.py — is "STALE LOCK" ever reported for a lock that was RELEASED NORMALLY?
# acquire_lock reads the owner file, and only then asks whether that pid is alive. If the holder finishes (releases, exits) between the
# two, the waiter sees "pid not running" and refuses at once with STALE LOCK and the recovery line, although nothing died and the lock
# directory is already gone (or is by then a THIRD writer's live lock).
# Part 1 (deterministic): the waiter is paused between the owner read and the liveness test (os.kill patched in a wrapper; the engine is unmodified).
# Part 2 (natural): N trials of 5 writers under CPU load, counting refusals by kind.
import os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
HERE = os.path.dirname(os.path.abspath(__file__))
KW = os.path.join(HERE, "kwrap.py")
PAUSE = os.path.join(BASE, "false_stale_pausewrap.py")
open(PAUSE, "w").write('''import os, runpy, sys, time
sys.dont_write_bytecode = True
gate, engine = sys.argv[1], sys.argv[2]; sys.argv = [engine] + sys.argv[3:]
real = os.kill; n = [0]
def kill(pid, sig):
    n[0] += 1
    if n[0] == 1:
        open(gate + ".atkill", "w").close()
        while not os.path.exists(gate): time.sleep(0.005)
    return real(pid, sig)
os.kill = kill
runpy.run_path(engine, run_name="__main__")
''')


def eng(wrapper, mode, root, data, wait="30"):
    core = os.path.join(root, "2_Project_Files/wake/handover_core.py")
    p = subprocess.Popen([sys.executable, wrapper, mode, core, "write", "--seat", "wednesday", "--tasks-dir", T(root), "--stamp", "QA", "--cap", "10000"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": wait}))
    p.stdin.write(data); p.stdin.close(); return p


def waitfor(path):
    t0 = time.time()
    while not os.path.exists(path):
        if time.time() - t0 > 20: raise SystemExit("timeout waiting for " + path)
        time.sleep(0.005)


print("## 1. deterministic: holder A finishes normally while waiter B sits between 'read the owner file' and 'is that pid alive'")
root = mk("det", "false_stale"); S0, A, B, C = blk("S0"), blk("A"), blk("B"), blk("C")
ho(root, "write", "--stdin", data=S0)
gA = os.path.join(BASE, "false_stale", "det", "gateA"); gB = os.path.join(BASE, "false_stale", "det", "gateB"); gC = os.path.join(BASE, "false_stale", "det", "gateC")
pa = eng(KW, "barrier:" + gA, root, A); waitfor(gA + ".waiting")          # A holds the lock, paused before its first rename
pb = eng(PAUSE, gB, root, B); waitfor(gB + ".atkill")                     # B has read A's owner file and is about to test A's pid
open(gA, "w").close(); rca = pa.wait(); oa = pa.stdout.read().decode()    # A finishes: both renames, releases the lock, exits 0 (reaped here)
lock_after_a = os.path.exists(lockd(root))
pc = eng(KW, "barrier:" + gC, root, C); waitfor(gC + ".waiting")          # a THIRD writer C now holds a fresh, LIVE lock
open(gB, "w").close(); t0 = time.time(); rcb = pb.wait(); eb = pb.stderr.read().decode(); took = time.time() - t0
rec = [l.strip() for l in eb.split("\n") if l.strip().startswith("mv -n '")]
print("- A: rc %d (%s); the lock directory existed after A ended: %s" % (rca, oa.strip().split("\n")[-1][:40], lock_after_a))
print("- B: rc %d after %.2f s (wait was 30 s); says STALE LOCK: %s; names A's pid as the dead holder: %s; gives the recovery line: %s"
      % (rcb, took, "STALE LOCK" in eb, ("pid %d " % pa.pid) in eb, bool(rec)))
print("- at that moment the lock at the path named by B's recovery line belongs to writer C, which is ALIVE and mid-write: owner pid %s, C's pid %d, C running %s"
      % (re.search(r"pid: (\d+)", open(os.path.join(lockd(root), "owner")).read()).group(1), pc.pid, pc.poll() is None))
print("  B's message, first 330 characters: " + eb.strip().replace("\n", " / ")[:330])
# what happens if the seat does what the message says (it is told the holder is dead)
D = blk("D")
if rec:
    assert rec[0].count(BASE) == 2
    r = subprocess.run(["/bin/sh", "-c", rec[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rcd, od, ed = ho(root, "write", "--stdin", data=D, env={"HANDOVER_LOCK_WAIT": "2"})     # the seat runs the write again, as told
    open(gC, "w").close(); rcc = pc.wait(); ec = pc.stderr.read().decode()
    a = rd(ar(root)) or b""; s = body(root)
    onD = a.count(D) + (s == D); onC = a.count(C) + (s == C); onA = a.count(A) + (s == A)
    print("- the seat runs B's recovery line (rc %d) and writes again: D rc %d; C then finishes rc %d. On disk: A %d, C %d, D %d copy(ies); state is %s"
          % (r.returncode, rcd, rcc, onA, onC, onD, "C" if s == C else ("D" if s == D else "?")))
    print("  => acknowledged block LOST: %s" % ", ".join(n for n, rc_, k in (("A", rca, onA), ("C", rcc, onC), ("D", rcd, onD)) if rc_ == 0 and k == 0) or "  => none lost")
else:
    open(gC, "w").close(); pc.wait()

print("## 2. natural: 5 writers per trial, 9 KB blocks, wait 30 s, with 8 CPU burners running beside them")
burn = [subprocess.Popen([sys.executable, "-c", "import time\nt=time.time()\nwhile time.time()-t<%d:\n    pass" % int(sys.argv[2] if len(sys.argv) > 2 else 90)]) for _ in range(8)]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 150
kinds = {}; lost = acked = 0; ex = []
t_start = time.time()
for i in range(N):
    if time.time() - t_start > int(sys.argv[2] if len(sys.argv) > 2 else 90) - 5: N = i; break
    root = mk("t%03d" % i, "false_stale_nat"); ho(root, "write", "--stdin", data=blk("BASE%d" % i, 8800))
    datas = [blk("W%d-%d" % (k, i), 8800) for k in range(5)]
    ps = [subprocess.Popen(["/bin/bash", os.path.join(root, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": "30"})) for _ in datas]
    for p, d in zip(ps, datas): p.stdin.write(d); p.stdin.close()
    t0 = time.time(); res = []
    for p in ps:
        rc = p.wait(); res.append((rc, p.stderr.read().decode(), time.time() - t0)); p.stdout.close(); p.stderr.close()
    a = rd(ar(root)) or b""; s = body(root)
    for d, (rc, se, took) in zip(datas, res):
        if rc == 0:
            acked += 1; lost += not (s == d or d in a)
        else:
            k = "STALE LOCK" if "STALE LOCK" in se else ("LOCK BUSY" if "LOCK BUSY" in se else "other")
            kinds[(rc, k)] = kinds.get((rc, k), 0) + 1
            if len(ex) < 2: ex.append("trial %d rc %d after %.2f s; lock dir present afterwards: %s; %s" % (i, rc, took, os.path.exists(lockd(root)), se.strip().replace("\n", " / ")[:300]))
for b in burn: b.kill()
print("- trials run %d: acknowledged %d, acknowledged LOST %d, refusals by (rc, kind): %s" % (N, acked, lost, dict(kinds)))
for e in ex: print("    " + e)
