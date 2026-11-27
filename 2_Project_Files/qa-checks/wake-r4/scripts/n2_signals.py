# n2_signals.py — a write interrupted by a CATCHABLE signal (SIGINT, SIGTERM, SIGHUP: a Ctrl-C, a tool-call timeout, a closed pane),
# a write whose owner file cannot be written, and a write whose stdout is closed. kill -9 is in n2_lock.py section K.
import os, re, signal, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_copies"))
from qlib import *
PW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pwrap.py"); TAG = str(os.getpid())
def eng(root, mode, data):
    core = os.path.join(root, "2_Project_Files/wake/handover_core.py")
    p = subprocess.Popen([sys.executable, PW, mode, core, "write", "--seat", "wednesday", "--tasks-dir", T(root), "--stamp", "QA4", "--cap", "10000"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": "5"}))
    p.stdin.write(data); p.stdin.close(); return p
print("## 1. a catchable signal while the writer is at <point> (history S0, S1; the writer carries C; then F is written, with the printed line if refused)")
for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    for pt in ("after-mkdir", "after-owner", "after-fsync2", "before-replace2", "after-replace2"):
        root = mk("%s_%s" % (sig.name, pt), "n2sig_" + TAG); S0, S1, C, F = blk("S0"), blk("S1"), blk("C"), blk("F")
        ho(root, "write", "--stdin", data=S0); ho(root, "write", "--stdin", data=S1)
        gate = os.path.join(os.path.dirname(root), "gate"); p = eng(root, "pause:%s:%s" % (pt, gate), C)
        t0 = time.time()
        while not os.path.exists(gate + ".waiting") and time.time() - t0 < 30: time.sleep(0.005)
        os.kill(p.pid, sig); rcc = p.wait(); oc = p.stdout.read().decode(); ec = p.stderr.read().decode()
        L = lockd(root); inside = sorted(re.sub(r"\.tmp\..*", ".tmp", x) for x in os.listdir(L)) if os.path.isdir(L) else "no lock dir"
        a = rd(ar(root)) or b""; s = body(root); c_on = a.count(C) + (s == C)
        t1 = time.time(); rc1, o1, e1 = ho(root, "write", "--stdin", data=F, env={"HANDOVER_LOCK_WAIT": "1"}); took = time.time() - t1
        k1 = "written" if rc1 == 0 else ("STALE LOCK" if "STALE LOCK" in e1 else ("LOCK BUSY" if "LOCK BUSY" in e1 else "other"))
        ran = "-"; rc2 = rc1
        if rc1:
            rec = [l.strip() for l in e1.split("\n") if l.strip().startswith("mv -n '")]
            if len(rec) == 1 and rec[0].count(BASE) == 2:
                ran = subprocess.run(["/bin/sh", "-c", rec[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode
                rc2 = ho(root, "write", "--stdin", data=F, env={"HANDOVER_LOCK_WAIT": "1"})[0]
        a = rd(ar(root)) or b""; s = body(root)
        print("- %-7s at %-16s writer rc %s, said written %s, traceback %s | lock left: %s; C on disk %d | next write: rc %s %s in %.1fs; line run rc %s; then rc %s | S0 %d S1 %d F %d; check rc %d"
              % (sig.name, pt, rcc, "handover: written" in oc, "YES" if "Traceback" in ec else "no", inside, c_on, rc1, k1, took, ran, rc2, a.count(S0), a.count(S1) + (s == S1), a.count(F) + (s == F), ho(root, "check")[0]))
print("## 2. the owner file cannot be written after mkdir succeeded (ENOSPC injected at the open)")
wrap = os.path.join(BASE, "n2sig_" + TAG, "failowner.py")
open(wrap, "w").write('''import builtins, errno, os, runpy, sys
sys.dont_write_bytecode = True
engine = sys.argv[1]; sys.argv = [engine] + sys.argv[2:]
r_open = builtins.open
def p_open(p, *a, **k):
    if isinstance(p, str) and p.endswith(".lock.d/owner") and a and "w" in a[0]:
        raise OSError(errno.ENOSPC, "No space left on device (injected)")
    return r_open(p, *a, **k)
builtins.open = p_open
runpy.run_path(engine, run_name="__main__")
''')
root = mk("failowner", "n2sig_" + TAG); ho(root, "write", "--stdin", data=blk("S0"))
p = subprocess.run([sys.executable, wrap, os.path.join(root, "2_Project_Files/wake/handover_core.py"), "write", "--seat", "wednesday", "--tasks-dir", T(root), "--stamp", "QA4", "--cap", "10000"], input=blk("C"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV())
L = lockd(root)
print("- writer rc %d | %s" % (p.returncode, p.stderr.decode().strip().split("\n")[-1][:200]))
print("  the lock directory THIS call made is still there: %s (holding %s); state still S0: %s" % (os.path.isdir(L), os.listdir(L) if os.path.isdir(L) else "-", body(root) == blk("S0")))
t1 = time.time(); rc1, o1, e1 = ho(root, "write", "--stdin", data=blk("F"), env={"HANDOVER_LOCK_WAIT": "1"})
print("  the next write: rc %d %s in %.1f s" % (rc1, "LOCK BUSY" if "LOCK BUSY" in e1 else ("STALE LOCK" if "STALE LOCK" in e1 else "written"), time.time() - t1))
print("## 3. stdout is closed before the writer prints 'written' (a reader that went away)")
root = mk("closedout", "n2sig_" + TAG); ho(root, "write", "--stdin", data=blk("S0"))
rd_, wr_ = os.pipe(); os.close(rd_)
p = subprocess.Popen(["/bin/bash", os.path.join(root, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], stdin=subprocess.PIPE, stdout=wr_, stderr=subprocess.PIPE, env=ENV()); os.close(wr_)
p.stdin.write(blk("C")); p.stdin.close(); rc = p.wait(); e = p.stderr.read().decode()
print("- writer rc %s; traceback %s; state is C %s; S0 in archive %d; lock left %s | %s" % (rc, "YES" if "Traceback" in e else "no", body(root) == blk("C"), (rd(ar(root)) or b"").count(blk("S0")), os.path.exists(lockd(root)), e.strip().split("\n")[-1][:120]))
