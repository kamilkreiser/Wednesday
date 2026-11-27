# starve.py — writers starved past the wait. (lock_attacks part A2 cut the wait to 0.2 s and still saw 0 refusals: each write holds
# the lock for milliseconds, so nobody starved. Here a holder is PAUSED inside the lock while N writers queue with a 1 s wait.)
import os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
KW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kwrap.py")
for n in (1, 5, 10):
    root = mk("n%d" % n, "starve"); S0, H = blk("S0"), blk("HOLDER")
    ho(root, "write", "--stdin", data=S0)
    gate = os.path.join(BASE, "starve", "n%d" % n, "gate")
    core = os.path.join(root, "2_Project_Files/wake/handover_core.py")
    ph = subprocess.Popen([sys.executable, KW, "barrier:" + gate, core, "write", "--seat", "wednesday", "--tasks-dir", T(root), "--stamp", "QA", "--cap", "10000"],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV())
    ph.stdin.write(H); ph.stdin.close()
    while not os.path.exists(gate + ".waiting"): time.sleep(0.01)
    datas = [blk("Q%d" % k) for k in range(n)]
    t0 = time.time()
    ps = [subprocess.Popen(["/bin/bash", os.path.join(root, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": "1"})) for _ in datas]
    for p, d in zip(ps, datas): p.stdin.write(d); p.stdin.close()
    res = [(p.wait(), p.stdout.read().decode(), p.stderr.read().decode(), time.time() - t0) for p in ps]
    mid_state = body(root)
    open(gate, "w").close(); rch = ph.wait()
    a = rd(ar(root)) or b""; s = body(root)
    print("holder paused inside the lock, %2d writers queue with a 1 s wait: exit codes %s; slowest refusal %.1f s; every refusal says LOCK BUSY %s and names the holder's pid %s; "
          "stdout of the refused all empty %s; state while they were refused still S0 %s; then holder rc %d, state is HOLDER %s; refused blocks on disk %d; lock gone %s"
          % (n, sorted(set(r[0] for r in res)), max(r[3] for r in res), all("LOCK BUSY" in r[2] for r in res), all(("pid %d " % ph.pid) in r[2] for r in res),
             all(r[1] == "" for r in res), mid_state == S0, rch, s == H, sum(a.count(d) + (s == d) for d in datas), not os.path.exists(lockd(root))))
# starved writers that RETRY as the message says: all must get through, none lost
root = mk("retry", "starve"); ho(root, "write", "--stdin", data=blk("S0"))
gate = os.path.join(BASE, "starve", "retry", "gate"); core = os.path.join(root, "2_Project_Files/wake/handover_core.py")
ph = subprocess.Popen([sys.executable, KW, "barrier:" + gate, core, "write", "--seat", "wednesday", "--tasks-dir", T(root), "--stamp", "QA", "--cap", "10000"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV())
ph.stdin.write(blk("HOLDER")); ph.stdin.close()
while not os.path.exists(gate + ".waiting"): time.sleep(0.01)
datas = [blk("R%d" % k) for k in range(5)]; first = []
for d in datas:
    rc, o, e = ho(root, "write", "--stdin", data=d, env={"HANDOVER_LOCK_WAIT": "0.2"}); first.append(rc)
open(gate, "w").close(); ph.wait()
second = [ho(root, "write", "--stdin", data=d, env={"HANDOVER_LOCK_WAIT": "5"})[0] for d in datas]
a = rd(ar(root)) or b""; s = body(root)
print("5 refused writers run again after the holder finished: first exit codes %s, second %s; each block on disk exactly once: %s; HOLDER on disk once: %s"
      % (first, second, all(a.count(d) + (s == d) == 1 for d in datas), a.count(blk("HOLDER")) == 1))
