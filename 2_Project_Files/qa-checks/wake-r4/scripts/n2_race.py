# n2_race.py — round 4: N simultaneous handover.sh writers, 9 KB blocks. A block is ACKNOWLEDGED when its writer exited 0.
# argv: [control]   'control' runs ONLY the negative control (a COPY of the engine whose lock path differs per process: no mutual exclusion).
import os, re, shutil, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_copies"))
import qlib
from qlib import *
TAG = str(os.getpid())
HEADS = [b"## FLOOR\n", b"## FIRST WORK\n", b"## OWED\n", b"## OPEN CARDS\n", b"## GRANTS IN PLAY\n"]


def up():
    return subprocess.run(["uptime"], stdout=subprocess.PIPE).stdout.decode().strip().split("load averages:")[-1].strip()


def race(nw, trials, wait, tag, tools=LANE):
    tot = dict(acked=0, refused=0, lost=0, dup=0, ghost=0, lockleft=0, tmpleft=0, entries_bad=0, stack=0, slowest=0.0)
    kinds = {}; ex = []
    for i in range(trials):
        root = mk("t%03d" % i, "n2race_%s_%s" % (tag, TAG), tools_from=tools)
        base = blk("BASE%d" % i, 8800)
        rc, o, e = ho(root, "write", "--stdin", data=base); assert rc == 0, e
        datas = [blk("W%d-%d" % (k, i), 8800) for k in range(nw)]
        t0 = time.time()
        ps = [subprocess.Popen(["/bin/bash", os.path.join(root, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": wait})) for _ in datas]
        for p, d in zip(ps, datas):
            p.stdin.write(d); p.stdin.close()
        res = []
        for p in ps:
            rc = p.wait(); took = time.time() - t0; so = p.stdout.read().decode(); se = p.stderr.read().decode(); p.stdout.close(); p.stderr.close()
            res.append((rc, so, se)); tot["slowest"] = max(tot["slowest"], took)
        a = rd(ar(root)) or b""; s = body(root); sraw = rd(st(root)) or b""
        acked = 0
        for d, (rc, so, se) in zip(datas, res):
            held = (s == d) + a.count(d)
            if rc == 0:
                acked += 1; tot["acked"] += 1
                tot["lost"] += held == 0; tot["dup"] += held > 1
            else:
                tot["refused"] += 1; tot["ghost"] += held > 0
                k = (rc, "STALE LOCK" if "STALE LOCK" in se else ("LOCK BUSY" if "LOCK BUSY" in se else ("LOCK LOST" if "LOCK LOST" in se else "other")))
                kinds[k] = kinds.get(k, 0) + 1
                if len(ex) < 2: ex.append("trial %d rc %d: %s" % (i, rc, se.strip().replace("\n", " / ")[:260]))
        tot["dup"] += a.count(base) != 1
        tot["entries_bad"] += len(re.findall(rb"^# ARCHIVED ", a, re.M)) != acked
        tot["stack"] += not all(sraw.count(h) == 1 for h in HEADS)
        tot["lockleft"] += any("lock.d" in f for f in os.listdir(T(root)))
        tot["tmpleft"] += any(".tmp." in f for f in os.listdir(T(root)))
    print("RACE %-10s writers %2d, trials %3d, wait %s s: acknowledged %d, refused %d %s; acknowledged LOST %d; a block more than once %d; refused-but-on-disk %d; "
          "archive entry count wrong %d; state file not ONE block %d; lock dir (or set-aside) left %d; temp files left %d; slowest writer %.1f s | load %s"
          % (tag, nw, trials, wait, tot["acked"], tot["refused"], dict(kinds) or "", tot["lost"], tot["dup"], tot["ghost"], tot["entries_bad"], tot["stack"],
             tot["lockleft"], tot["tmpleft"], tot["slowest"], up()))
    for x in ex: print("    " + x)
    return tot


if sys.argv[1:] == ["control"]:
    nolock = os.path.join(BASE, "n2race_nolock_tools_" + TAG); os.makedirs(nolock)
    for f in ("handover.sh", "handover_core.py", "wake_pack.py", "wake_census.sh"):
        shutil.copy(os.path.join(LANE, f), os.path.join(nolock, f))
    src = open(os.path.join(nolock, "handover_core.py"), encoding="utf-8").read()
    needle = '    return os.path.join(tasks_dir, "STATE-%s.lock.d" % seat)'
    assert src.count(needle) == 1
    open(os.path.join(nolock, "handover_core.py"), "w", encoding="utf-8").write(src.replace(needle, '    return os.path.join(tasks_dir, "STATE-%s.lock.d.%d" % (seat, os.getpid()))'))
    print("## NEGATIVE CONTROL: the same harness, a COPY of the engine with a per-process lock path (no mutual exclusion). It must SEE a loss or a refusal.")
    t = race(3, 60, "30", "NOLOCK", tools=nolock)
    print("control verdict: the harness %s (lost %d, entry count wrong %d, refused %d)" % ("SEES the missing lock" if t["lost"] or t["entries_bad"] or t["refused"] else "DOES NOT SEE IT (instrument blind!)", t["lost"], t["entries_bad"], t["refused"]))
else:
    print("## 3, 5, 10 and 20 simultaneous handover.sh writers")
    tt = [race(3, 60, "60", "w3"), race(5, 40, "60", "w5"), race(10, 20, "120", "w10"), race(20, 12, "180", "w20")]
    print("TOTAL acknowledged %d, refused %d, acknowledged LOST %d, duplicated %d" % (sum(t["acked"] for t in tt), sum(t["refused"] for t in tt), sum(t["lost"] for t in tt), sum(t["dup"] for t in tt)))
