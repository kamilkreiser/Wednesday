# n2_volume.py — the lock ON THE DevMASTER VOLUME ITSELF (both earlier checks ran on the internal disk only). The trees live inside
# the checker's own folder (vol_tree/), each a folder named WEDNESDAY holding COPIES of the tools; no test seam is used (none is
# honoured outside a temp path), so the stamp is the real clock. The real 0_Brain/tasks is never a target: handover.sh derives
# its tree from its own location (shown by --where in raw/).
import os, re, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_copies"))
import qlib
from qlib import *
qlib.BASE = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/qa-checks/wake-r4/vol_tree/run_%d" % os.getpid()
BASE = qlib.BASE
PW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pwrap.py")
def up(): return subprocess.run(["uptime"], stdout=subprocess.PIPE).stdout.decode().strip().split("load averages:")[-1].strip()
print("volume: %s" % subprocess.run(["df", "-h", "/Volumes/DevMASTER"], stdout=subprocess.PIPE).stdout.decode().strip().split("\n")[-1])
print("mount:  %s" % [l for l in subprocess.run(["mount"], stdout=subprocess.PIPE).stdout.decode().split("\n") if "DevMASTER" in l])
tot = dict(acked=0, refused=0, lost=0, dup=0, left=0, entries_bad=0); kinds = {}; slow = 0.0
for nw, trials in ((3, 30), (5, 30), (10, 12), (20, 6)):
    a0 = tot["acked"]
    for i in range(trials):
        root = mk("w%d_t%03d" % (nw, i))
        base = blk("BASE%d" % i, 8800); rc, o, e = ho(root, "write", "--stdin", data=base); assert rc == 0, e
        datas = [blk("W%d-%d" % (k, i), 8800) for k in range(nw)]
        t0 = time.time()
        ps = [subprocess.Popen(["/bin/bash", os.path.join(root, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": "120"})) for _ in datas]
        for p, d in zip(ps, datas): p.stdin.write(d); p.stdin.close()
        res = []
        for p in ps:
            rc = p.wait(); slow = max(slow, time.time() - t0); se = p.stderr.read().decode(); p.stdout.close(); p.stderr.close(); res.append((rc, se))
        a = rd(ar(root)) or b""; s = body(root); acked = 0
        for d, (rc, se) in zip(datas, res):
            held = (s == d) + a.count(d)
            if rc == 0: acked += 1; tot["acked"] += 1; tot["lost"] += held == 0; tot["dup"] += held > 1
            else:
                tot["refused"] += 1; k = (rc, "STALE LOCK" if "STALE LOCK" in se else ("LOCK BUSY" if "LOCK BUSY" in se else se.strip()[:80])); kinds[k] = kinds.get(k, 0) + 1
        tot["entries_bad"] += len(re.findall(rb"^# ARCHIVED ", a, re.M)) != acked
        tot["left"] += sorted(os.listdir(T(root))) != ["STATE-wednesday-archive.md", "STATE-wednesday.md"]
    print("on DevMASTER: writers %2d, trials %2d: acknowledged %d (running total %d); slowest writer so far %.1f s | load %s" % (nw, trials, tot["acked"] - a0, tot["acked"], slow, up()))
print("TOTAL on the DevMASTER volume: acknowledged %d, refused %d %s, acknowledged LOST %d, more than once %d, archive entry count wrong %d, trees whose tasks dir holds anything but the two STATE files %d"
      % (tot["acked"], tot["refused"], dict(kinds) or "", tot["lost"], tot["dup"], tot["entries_bad"], tot["left"]))
def eng(root, mode, data):
    core = os.path.join(root, "2_Project_Files/wake/handover_core.py")
    p = subprocess.Popen([sys.executable, PW, mode, core, "write", "--seat", "wednesday", "--tasks-dir", T(root), "--stamp", "QA4-VOL", "--cap", "10000"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": "5"}))
    p.stdin.write(data); p.stdin.close(); return p
for pt in ("after-fsync2", "before-replace2", "after-replace2"):
    root = mk("kill_" + pt); S0, S1, C, F = blk("S0"), blk("S1"), blk("C"), blk("F")
    ho(root, "write", "--stdin", data=S0); ho(root, "write", "--stdin", data=S1)
    p = eng(root, "kill:" + pt, C); rck = p.wait()
    rc1, o1, e1 = ho(root, "write", "--stdin", data=F, env={"HANDOVER_LOCK_WAIT": "1"})
    rec = [l.strip() for l in e1.split("\n") if l.strip().startswith("mv -n '")]
    assert len(rec) == 1 and rec[0].count(BASE) == 2, rec
    rr = subprocess.run(["/bin/sh", "-c", rec[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode
    rc2, o2, e2 = ho(root, "write", "--stdin", data=F); a = rd(ar(root)) or b""; s = body(root)
    print("on DevMASTER: kill -9 at %-16s engine rc %s; next write rc %s %s; line run rc %s; then rc %s; copies S0 %d S1 %d C %d F %d; check rc %d"
          % (pt, rck, rc1, "STALE LOCK" if "STALE LOCK" in e1 else "LOCK BUSY", rr, rc2, a.count(S0), a.count(S1) + (s == S1), a.count(C) + (s == C), a.count(F) + (s == F), ho(root, "check")[0]))
root = mk("displace"); S0, S1, C, D, E = blk("S0"), blk("S1"), blk("C"), blk("D"), blk("E")
ho(root, "write", "--stdin", data=S0); ho(root, "write", "--stdin", data=S1)
gate = os.path.join(BASE, "displace", "gate"); p = eng(root, "pause:before-replace1:" + gate, C)
while not os.path.exists(gate + ".waiting"): time.sleep(0.01)
rcw, ow, ew = ho(root, "write", "--stdin", data=blk("W"), env={"HANDOVER_LOCK_WAIT": "1"})
rec = [l.strip() for l in ew.split("\n") if l.strip().startswith("mv -n '")]; assert len(rec) == 1 and rec[0].count(BASE) == 2
rr = subprocess.run(["/bin/sh", "-c", rec[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode
rcd = ho(root, "write", "--stdin", data=D)[0]; rce = ho(root, "write", "--stdin", data=E)[0]
open(gate, "w").close(); rcc = p.wait(); ec = p.stderr.read().decode(); a = rd(ar(root)) or b""; s = body(root)
print("on DevMASTER: recovery line run while C is alive (paused inside its first rename): line rc %s; D rc %s, E rc %s; C rc %s %s; copies S0 %d S1 %d C %d D %d E %d"
      % (rr, rcd, rce, rcc, "LOCK LOST" if "LOCK LOST" in ec else ec.strip()[:60], a.count(S0), a.count(S1), a.count(C) + (s == C), a.count(D), a.count(E) + (s == E)))
odd = [os.path.join(dp, f) for dp, ds, fs in os.walk(BASE) for f in fs + ds if f.startswith("._") or f == ".DS_Store"]
print("AppleDouble ('._*') or .DS_Store entries anywhere in the volume trees: %d" % len(odd))
