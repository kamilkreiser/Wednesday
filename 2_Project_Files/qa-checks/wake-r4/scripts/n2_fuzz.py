# n2_fuzz.py — the seat's stated limit ("the guard is as strong as rename(2)"): try to lose an acknowledged block WITHOUT a patched
# pause point. A real writer C (the unmodified engine, started through handover.sh) is frozen with SIGSTOP at a RANDOM instant while
# it holds the lock; the lock directory is moved away exactly as the recovery line does; writers D and E run to completion; C is
# resumed with SIGCONT. Mode 'nostop': the same without freezing C (the lock is moved away under a RUNNING writer, D started at once).
# argv: <mode stop|nostop> <trials>
import os, random, re, signal, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_copies"))
from qlib import *
mode, N = sys.argv[1], int(sys.argv[2]); TAG = "%s_%d" % (mode, os.getpid())
random.seed(20261127)
def up(): return subprocess.run(["uptime"], stdout=subprocess.PIPE).stdout.decode().strip().split("load averages:")[-1].strip()
stat = dict(hit=0, miss=0, acked=0, lost=0, dup_state=0); crc = {}; where = {}; examples = []
print("load at start %s" % up())
for i in range(N):
    root = mk("t%04d" % i, "n2fuzz_" + TAG); B = dict((n, blk("%s-%d" % (n, i), 8800)) for n in ("S0", "S1", "C", "D", "E"))
    rcs = {"S0": ho(root, "write", "--stdin", data=B["S0"])[0], "S1": ho(root, "write", "--stdin", data=B["S1"])[0]}
    L = lockd(root)
    pc = subprocess.Popen(["/bin/bash", os.path.join(root, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": "5"}))
    pc.stdin.write(B["C"]); pc.stdin.close()
    t0 = time.time()
    while not os.path.exists(L) and pc.poll() is None and time.time() - t0 < 20: pass          # spin until C has made its lock
    d = random.choice([0, 0, 0.0002, 0.0005, 0.001, 0.002, 0.003, 0.005]); t1 = time.time()
    while time.time() - t1 < d: pass
    if mode == "stop":
        try: os.kill(pc.pid, signal.SIGSTOP)
        except ProcessLookupError: pass
        time.sleep(0.02)
    try:
        inside = sorted(re.sub(r"\.tmp\..*", ".tmp", x) for x in os.listdir(L))
        os.rename(L, L + ".stale-fuzz"); moved = True
    except OSError:
        inside = None; moved = False
    if moved:
        stat["hit"] += 1; k = "+".join(inside) or "(empty)"; where[k] = where.get(k, 0) + 1
    else:
        stat["miss"] += 1
    rcs["D"] = ho(root, "write", "--stdin", data=B["D"], env={"HANDOVER_LOCK_WAIT": "5"})[0]
    rcs["E"] = ho(root, "write", "--stdin", data=B["E"], env={"HANDOVER_LOCK_WAIT": "5"})[0]
    if mode == "stop":
        try: os.kill(pc.pid, signal.SIGCONT)
        except ProcessLookupError: pass
    rcs["C"] = pc.wait(); ec = pc.stderr.read().decode(); oc = pc.stdout.read().decode(); pc.stdout.close(); pc.stderr.close()
    a = rd(ar(root)) or b""; s = body(root); sraw = rd(st(root)) or b""
    if moved: crc[rcs["C"]] = crc.get(rcs["C"], 0) + 1
    for n in ("S0", "S1", "C", "D", "E"):
        if rcs[n] == 0:
            stat["acked"] += 1
            if a.count(B[n]) + (s == B[n]) == 0:
                stat["lost"] += 1
                if len(examples) < 5: examples.append("trial %d: %s acknowledged (rc 0) and on disk 0 times; C rc %s; inside the lock when moved: %s; C stderr: %s" % (i, n, rcs["C"], inside, ec.strip()[:200]))
    stat["dup_state"] += sraw.count(b"## FLOOR\n") != 1
    if rcs["C"] not in (0, 4, 5, 6) and len(examples) < 5: examples.append("trial %d: C rc %s: %s" % (i, rcs["C"], ec.strip()[-300:]))
print("mode %s, trials %d: the lock was moved away under a live writer in %d (missed the window in %d); what was inside the lock at that instant: %s" % (mode, N, stat["hit"], stat["miss"], where))
print("  the displaced writer's exit codes (hits only): %s" % dict(sorted(crc.items())))
print("  acknowledged writes %d; acknowledged LOST %d; state file not ONE block %d | load at end %s" % (stat["acked"], stat["lost"], stat["dup_state"], up()))
for x in examples: print("    " + x)
