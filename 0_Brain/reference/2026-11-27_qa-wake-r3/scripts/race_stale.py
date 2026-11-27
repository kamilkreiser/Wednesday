# race_stale.py — follow-up to lock_attacks part A: one writer of 150 was refused rc 5 although the wait was 30 s and no lock was stale.
# This run keeps the stderr of every refused writer and the time it took, to see WHICH refusal it was.
# argv: <writers> <trials> [pad]
import os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
W, N = int(sys.argv[1]), int(sys.argv[2]); PAD = int(sys.argv[3]) if len(sys.argv) > 3 else 8800
kinds = {}; lost = 0; acked = 0; examples = []
for i in range(N):
    root = mk("t%03d" % i, "race_stale_%d_%d" % (W, PAD))
    ho(root, "write", "--stdin", data=blk("BASE%d" % i, PAD))
    datas = [blk("W%d-%d" % (k, i), PAD) for k in range(W)]
    t0 = time.time()
    ps = [subprocess.Popen(["/bin/bash", os.path.join(root, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": "30"})) for _ in datas]
    for p, d in zip(ps, datas):
        p.stdin.write(d); p.stdin.close()
    res = []
    for p in ps:
        rc = p.wait(); took = time.time() - t0; so = p.stdout.read().decode(); se = p.stderr.read().decode(); p.stdout.close(); p.stderr.close()
        res.append((rc, so, se, took))
    a = rd(ar(root)) or b""; s = body(root)
    for d, (rc, so, se, took) in zip(datas, res):
        if rc == 0:
            acked += 1
            if not (s == d or d in a): lost += 1
        else:
            kind = "STALE LOCK" if "STALE LOCK" in se else ("LOCK BUSY" if "LOCK BUSY" in se else "other")
            kinds[(rc, kind)] = kinds.get((rc, kind), 0) + 1
            lock_now = os.path.exists(lockd(root))
            if len(examples) < 3:
                examples.append("trial %d: rc %d after %.2f s; the lock directory exists after all writers ended: %s; stderr:\n%s"
                                % (i, rc, took, lock_now, "\n".join("      " + l[:260] for l in se.strip().split("\n")[:4])))
print("writers %d, trials %d, block pad %d, HANDOVER_LOCK_WAIT 30: acknowledged %d, acknowledged LOST %d, refusals by kind %s"
      % (W, N, PAD, acked, lost, dict(kinds)))
for e in examples: print("  " + e)
