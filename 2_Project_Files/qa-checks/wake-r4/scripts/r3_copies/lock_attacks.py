# lock_attacks.py — round 3's write lock under attack. Scratch trees only. Exit codes are the acknowledgement:
# a block is ACKNOWLEDGED when its writer exited 0. Every acknowledged block must be the state block or sit in the archive
# exactly once; a block whose writer exited non-zero must be in NEITHER (it was refused), and its stdout must not say 'written'.
import os, re, signal, socket, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
HERE = os.path.dirname(os.path.abspath(__file__))
KW = os.path.join(HERE, "kwrap.py")
PARTS = [a for a in sys.argv[1:]] or ["A", "B", "C", "D", "E", "F"]


def spawn(root, data, wait="30"):
    p = subprocess.Popen(["/bin/bash", os.path.join(root, "2_Project_Files/wake/handover.sh"), "write", "--stdin"], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": wait}))
    return p


def eng(root, mode, data, wait="5", extra=None):
    core = os.path.join(root, "2_Project_Files/wake/handover_core.py")
    e = {"HANDOVER_LOCK_WAIT": wait}
    e.update(extra or {})
    p = subprocess.Popen([sys.executable, KW, mode, core, "write", "--seat", "wednesday", "--tasks-dir", T(root), "--stamp", "QA-" + mode, "--cap", "10000"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV(e))
    p.stdin.write(data); p.stdin.close()
    return p


def n_entries(a):
    return len(re.findall(rb"^# ARCHIVED ", a or b"", re.M))


def race(n_writers, trials, wait, tag):
    tot = dict(acked=0, refused=0, lost=0, dup=0, ghost=0, lockleft=0, tmpleft=0, entries_bad=0, said_written_but_rc=0)
    rcs_seen = {}
    for i in range(trials):
        root = mk("t%03d" % i, "race_%s" % tag)
        base = blk("BASE%d" % i, 8800)
        rc, o, e = ho(root, "write", "--stdin", data=base)
        assert rc == 0, e
        datas = [blk("W%d-%d" % (k, i), 8800) for k in range(n_writers)]
        ps = [spawn(root, d, wait) for d in datas]
        for p, d in zip(ps, datas):
            p.stdin.write(d); p.stdin.close()
        res = []
        for p in ps:
            rc = p.wait(); so = p.stdout.read().decode(); se = p.stderr.read().decode(); p.stdout.close(); p.stderr.close()
            res.append((rc, so, se))
        a = rd(ar(root)) or b""; s = body(root)
        acked = [d for d, r in zip(datas, res) if r[0] == 0]
        for d, (rc, so, se) in zip(datas, res):
            rcs_seen[rc] = rcs_seen.get(rc, 0) + 1
            held = (s == d) + a.count(d)
            if rc == 0:
                tot["acked"] += 1
                if held == 0: tot["lost"] += 1
                if held > 1: tot["dup"] += 1
            else:
                tot["refused"] += 1
                if held: tot["ghost"] += 1
                if "handover: written" in so: tot["said_written_but_rc"] += 1
        if a.count(base) != 1: tot["dup"] += 1
        if n_entries(a) != len(acked): tot["entries_bad"] += 1      # base + (acked - 1) superseded acked blocks
        if os.path.exists(lockd(root)): tot["lockleft"] += 1
        if [f for f in os.listdir(T(root)) if ".tmp." in f]: tot["tmpleft"] += 1
    print("RACE %-12s writers %2d, trials %3d, wait %s s: acknowledged %d, refused %d (exit codes seen %s); acknowledged LOST %d; any block more than once %d; "
          "refused-but-present %d; refused yet stdout said written %d; archive entry count wrong %d; lock left behind %d; temp files left %d"
          % (tag, n_writers, trials, wait, tot["acked"], tot["refused"], dict(sorted(rcs_seen.items())), tot["lost"], tot["dup"], tot["ghost"],
             tot["said_written_but_rc"], tot["entries_bad"], tot["lockleft"], tot["tmpleft"]))
    return tot


if "A" in PARTS:
    print("## A. 2, 3, 5 and 10 simultaneous handover.sh writers (9 KB blocks), generous wait")
    race(2, 60, "30", "w2")
    race(3, 40, "30", "w3")
    race(5, 30, "30", "w5")
    race(10, 20, "60", "w10")
    print("## A2. the same with the wait cut to the floor (0.2 s): starved writers must be REFUSED rc 5, never written, never lost when acknowledged")
    race(5, 30, "0.2", "w5starve")
    race(10, 20, "0.2", "w10starve")

if "B" in PARTS:
    print("## B. NEGATIVE CONTROL: the same harness against a copy of the engine with the lock removed must SEE losses")
    import shutil
    nolock = os.path.join(BASE, "nolock_tools"); os.makedirs(nolock, exist_ok=True)
    for f in ("handover.sh", "handover_core.py", "wake_pack.py", "wake_census.sh"):
        shutil.copy(os.path.join(LANE, f), os.path.join(nolock, f))
    src = open(os.path.join(nolock, "handover_core.py"), encoding="utf-8").read()
    needle = "    deadline = time.monotonic() + lock_wait()\n"
    assert src.count(needle) == 1
    open(os.path.join(nolock, "handover_core.py"), "w", encoding="utf-8").write(src.replace(needle, "    return\n" + needle))
    _mk = mk
    def mk(name, sub="", folder="WEDNESDAY", tools_from=nolock):   # noqa: F811
        return _mk(name, sub, folder, tools_from)
    t = race(3, 40, "30", "NOLOCKw3")
    print("   control verdict: the harness %s a lost acknowledged block when the lock is off" % ("SEES" if t["lost"] or t["entries_bad"] else "DOES NOT SEE (instrument blind!)"))
    mk = _mk

if "C" in PARTS:
    print("## C. a lock this process did not take: owner file missing / empty / garbage / unrelated live pid / other host / odd shapes")
    dead = subprocess.Popen([sys.executable, "-c", "pass"]); dead.wait()
    host = socket.gethostname()
    cases = [
        ("no owner file", None),
        ("empty owner file", ""),
        ("garbage owner file", "\x00\xff not a lock \x01\n"),
        ("pid is not a number", "pid: abc\nhost: %s\n" % host),
        ("pid 0", "pid: 0\nhost: %s\n" % host),
        ("pid 1 (launchd: alive, not ours)", "pid: 1\nhost: %s\n" % host),
        ("a LIVE UNRELATED pid on this host (pid reuse: this harness's own pid)", "pid: %d\nhost: %s\nstarted: long ago\nepoch: 1\n" % (os.getpid(), host)),
        ("a dead pid on this host (control: STALE at once)", "pid: %d\nhost: %s\nstarted: x\nepoch: 1\n" % (dead.pid, host)),
        ("a dead pid, ANOTHER host", "pid: %d\nhost: some-other-mac\nstarted: x\nepoch: 1\n" % dead.pid),
        ("a dead pid, host line missing", "pid: %d\n" % dead.pid),
        ("an absurdly large pid", "pid: 99999999999999999999999\nhost: %s\n" % host),
        ("pid just past the C int range", "pid: 4294967296\nhost: %s\n" % host),
        ("owner file is a DIRECTORY", "DIR"),
        ("owner file unreadable (mode 000)", "CHMOD"),
        ("the lock path is a regular FILE, not a directory", "FILE"),
        ("the lock path is a dangling symlink", "DANGLING"),
    ]
    for label, owner in cases:
        root = mk("c%02d" % cases.index((label, owner)), "lockowner")
        ho(root, "write", "--stdin", data=blk("S0"))
        L = lockd(root)
        if owner == "FILE":
            open(L, "w").write("x")
        elif owner == "DANGLING":
            os.symlink(os.path.join(root, "nowhere"), L)
        else:
            os.mkdir(L)
            if owner == "DIR":
                os.mkdir(os.path.join(L, "owner"))
            elif owner == "CHMOD":
                open(os.path.join(L, "owner"), "w").write("pid: %d\nhost: %s\n" % (dead.pid, host)); os.chmod(os.path.join(L, "owner"), 0)
            elif owner is not None:
                open(os.path.join(L, "owner"), "wb").write(owner.encode("latin-1"))
        before = sorted(os.listdir(L)) if os.path.isdir(L) else "not-a-dir"
        t0 = time.time(); rc, o, e = ho(root, "write", "--stdin", data=blk("A"), env={"HANDOVER_LOCK_WAIT": "1"}); took = time.time() - t0
        still = os.path.lexists(L) and (sorted(os.listdir(L)) if os.path.isdir(L) else "not-a-dir") == before
        kind = "STALE" if "STALE LOCK" in e else ("BUSY" if "LOCK BUSY" in e else "OTHER")
        print("- %-70s rc %d in %.1fs; %s; traceback %s; recovery line given %s; lock left exactly as it was %s; state still S0 %s; A anywhere %s%s"
              % (label, rc, took, kind, "YES" if "Traceback" in e else "no", "mv -n '" in e, still, body(root) == blk("S0"),
                 (body(root) == blk("A")) or blk("A") in (rd(ar(root)) or b""), "" if kind != "OTHER" else " | stderr tail: " + e.strip().split("\n")[-1][:160]))
        if owner == "CHMOD":
            os.chmod(os.path.join(L, "owner"), 0o644)
    print("## C2. HANDOVER_LOCK_WAIT values (a held lock with no owner; how long before the refusal)")
    for val in ("0", "-5", "abc", "nan", "0.2"):
        root = mk("w_" + val.replace("-", "m").replace(".", "_"), "lockwait"); ho(root, "write", "--stdin", data=blk("S0")); os.mkdir(lockd(root))
        t0 = time.time(); rc, o, e = ho(root, "write", "--stdin", data=blk("A"), env={"HANDOVER_LOCK_WAIT": val}); took = time.time() - t0
        print("- HANDOVER_LOCK_WAIT=%-4s rc %d after %.1f s (%s)" % (val, rc, took, "LOCK BUSY" if "LOCK BUSY" in e else e.strip()[:80]))
    print("## C3. other verbs while the lock is held: dry write, show, check, seed --run")
    root = mk("verbs", "lockverbs"); ho(root, "write", "--stdin", data=blk("S0")); os.mkdir(lockd(root))
    for args, data in ((("write", "--stdin", "--dry"), blk("A")), (("show",), b""), (("check",), b""), (("--where",), b"")):
        rc, o, e = ho(root, *args, data=data, env={"HANDOVER_LOCK_WAIT": "1"})
        print("- %-22s rc %d | %s" % (" ".join(args), rc, (o.strip().split("\n")[-1] if o.strip() else e.strip().split("\n")[-1])[:150]))
    root2 = mk("seedlock", "lockverbs"); open(os.path.join(T(root2), "NEXT-PICKUP.md"), "w").write("# p\n\n## newest\n- **FLOOR:** a\n"); os.mkdir(lockd(root2))
    rc, o, e = ho(root2, "seed", "--from-legacy", "--run", env={"HANDOVER_LOCK_WAIT": "1"})
    print("- seed --from-legacy --run under a held lock: rc %d; state written %s | %s" % (rc, os.path.exists(st(root2)), e.strip().split("\n")[0][:120]))

if "D" in PARTS:
    print("## D. kill -9 (SIGKILL on the engine's own pid) at every step of a write, then the DOCUMENTED recovery line, then a normal write")
    print("   history before the kill: S0 written, S1 written (both acknowledged). The killed writer carries S2. After recovery S3 is written.")
    for mode in ("kill:mkdir", "kill:owner", "kill:fsync1", "kill:fsync2", "kill:pre-rename1", "kill:mid", "kill:post-rename2", "kill:unlock-mid"):
        root = mk(mode.replace(":", "_"), "kill9")
        S0, S1, S2, S3 = blk("S0"), blk("S1"), blk("S2"), blk("S3")
        ho(root, "write", "--stdin", data=S0); ho(root, "write", "--stdin", data=S1)
        p = eng(root, mode, S2); rck = p.wait(); so = p.stdout.read().decode(); se = p.stderr.read().decode()
        a = rd(ar(root)) or b""; s = body(root)
        state_after = "S1" if s == S1 else ("S2" if s == S2 else "OTHER")
        lost_now = [n for n, b in (("S0", S0), ("S1", S1)) if not (s == b or b in a)]
        acked_s2 = "handover: written" in so
        tmps = [f for f in os.listdir(T(root)) if ".tmp." in f]
        rc_chk, o_chk, _ = ho(root, "check")
        t0 = time.time(); rc1, o1, e1 = ho(root, "write", "--stdin", data=S3, env={"HANDOVER_LOCK_WAIT": "1"}); took = time.time() - t0
        kind = "STALE" if "STALE LOCK" in e1 else ("BUSY" if "LOCK BUSY" in e1 else ("none: rc %d" % rc1))
        rec = [l.strip() for l in e1.split("\n") if l.strip().startswith("mv -n '")]
        ran = "-"
        if rc1 == 5 and rec:
            assert BASE in rec[0] and rec[0].count(BASE) == 2, rec[0]       # the recovery line names scratch paths only
            r = subprocess.run(["/bin/sh", "-c", rec[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ran = "rc %d" % r.returncode
            rc2, o2, e2 = ho(root, "write", "--stdin", data=S3, env={"HANDOVER_LOCK_WAIT": "1"})
        else:
            rc2, o2, e2 = rc1, o1, e1
        a2 = rd(ar(root)) or b""; s2 = body(root)
        counts = dict((n, a2.count(b) + (s2 == b)) for n, b in (("S0", S0), ("S1", S1), ("S2", S2), ("S3", S3)))
        rc_chk2, _, _ = ho(root, "check")
        print("- %-18s engine rc %d (acknowledged S2: %s); right after: state %s, S0/S1 lost %s, check rc %d, temp files %d | next write rc %d (%s, %.1fs); "
              "recovery line run %s | then write rc %d; state is S3 %s; copies on disk S0 %d, S1 %d, S2 %d, S3 %d; check rc %d; lock dir now %s"
              % (mode, rck, acked_s2, state_after, lost_now or "none", rc_chk, len(tmps), rc1, kind, took, ran, rc2, s2 == S3,
                 counts["S0"], counts["S1"], counts["S2"], counts["S3"], rc_chk2, "present" if os.path.exists(lockd(root)) else "gone"))

if "E" in PARTS:
    print("## E. does the tool ever remove a lock it did not take, or write unlocked?")
    # E1: the recovery line is run by a person WHILE the writer is alive (operator error), a second writer then takes a new lock
    root = mk("e1", "lockmisuse"); S0, A, B = blk("S0"), blk("A"), blk("B")
    ho(root, "write", "--stdin", data=S0)
    gate = os.path.join(BASE, "lockmisuse", "e1", "gate")
    pb = eng(root, "barrier:" + gate, B, wait="5")
    while not os.path.exists(gate + ".waiting"): time.sleep(0.01)
    os.rename(lockd(root), lockd(root) + ".stale-operator")            # what the recovery line does
    rca, oa, ea = ho(root, "write", "--stdin", data=A, env={"HANDOVER_LOCK_WAIT": "2"})
    open(gate, "w").close(); rcb = pb.wait(); eb = pb.stderr.read().decode(); ob = pb.stdout.read().decode()
    a = rd(ar(root)) or b""; s = body(root)
    print("- E1 recovery line run while writer B is ALIVE and paused, then writer A: A rc %d, B rc %d; state is %s; A on disk %d time(s); B on disk %d; "
          "B's release said: %s" % (rca, rcb, "A" if s == A else ("B" if s == B else "?"), a.count(A) + (s == A), a.count(B) + (s == B),
                                    (eb.strip().split("\n")[-1][:170] if eb.strip() else "(nothing)")))
    print("     => an acknowledged block is %s in this operator-error case" % ("LOST" if (rca == 0 and a.count(A) + (s == A) == 0) or (rcb == 0 and a.count(B) + (s == B) == 0) else "conserved"))
    # E2: B's lock is moved away and a THIRD process's lock stands when B releases: B must leave it alone
    root = mk("e2", "lockmisuse"); ho(root, "write", "--stdin", data=S0)
    gate = os.path.join(BASE, "lockmisuse", "e2", "gate")
    pb = eng(root, "barrier:" + gate, B, wait="5")
    while not os.path.exists(gate + ".waiting"): time.sleep(0.01)
    os.rename(lockd(root), lockd(root) + ".stale-operator")
    os.mkdir(lockd(root)); open(os.path.join(lockd(root), "owner"), "w").write("pid: %d\nhost: %s\nstarted: x\nepoch: 1\n" % (os.getpid(), socket.gethostname()))
    open(gate, "w").close(); rcb = pb.wait(); eb = pb.stderr.read().decode()
    print("- E2 B releases while ANOTHER owner's lock stands at the path: B rc %d; the foreign lock is still there %s with its owner file %s; B said: %s"
          % (rcb, os.path.isdir(lockd(root)), os.path.exists(os.path.join(lockd(root), "owner")), eb.strip().split("\n")[-1][:150]))
    # E3: the lock directory vanishes during the write (nobody replaces it)
    root = mk("e3", "lockmisuse"); ho(root, "write", "--stdin", data=S0)
    gate = os.path.join(BASE, "lockmisuse", "e3", "gate")
    pb = eng(root, "barrier:" + gate, B, wait="5")
    while not os.path.exists(gate + ".waiting"): time.sleep(0.01)
    os.rename(lockd(root), lockd(root) + ".stale-operator")
    open(gate, "w").close(); rcb = pb.wait(); eb = pb.stderr.read().decode()
    print("- E3 the lock vanishes mid-write: B rc %d; state is B %s; stderr: %s" % (rcb, body(root) == B, (eb.strip().split("\n")[-1][:150] if eb.strip() else "(nothing)")))
    # E4: the owner file cannot be written after mkdir (tasks dir fine, lock dir made read-only by a racing chmod is not reproducible; use a full-path trick: none) -> static reading only
    # E5: static: every call path into write_locked
    src = open(os.path.join(LANE, "handover_core.py"), encoding="utf-8").read()
    calls = [m.start() for m in re.finditer(r"write_locked\(", src)]
    print("- E5 static: write_locked( occurs %d times in the engine (1 definition + calls); os.replace occurs %d times; os.rmdir %d; os.remove %d; shutil/rmtree/unlink %d"
          % (len(calls), src.count("os.replace("), src.count("os.rmdir("), src.count("os.remove("), len(re.findall(r"shutil|rmtree|unlink", src))))

if "F" in PARTS:
    print("## F. what a rotation script sees when the write is refused")
    root = mk("f1", "lockrc"); ho(root, "write", "--stdin", data=blk("S0")); os.mkdir(lockd(root))
    sh = os.path.join(root, "2_Project_Files/wake/handover.sh")
    blockf = os.path.join(BASE, "lockrc", "block.txt"); open(blockf, "wb").write(blk("ROT"))
    for label, cmd in (("plain call, stdin from a file", "/bin/bash '%s' write --stdin < '%s'; echo \"rc=$?\"" % (sh, blockf)),
                       ("cat | handover.sh (rc of the last command)", "cat '%s' | /bin/bash '%s' write --stdin; echo \"rc=$?\"" % (blockf, sh)),
                       ("handover.sh ... | tee log (NO pipefail: rc is tee's)", "/bin/bash '%s' write --stdin < '%s' 2>&1 | tee /dev/null >/dev/null; echo \"rc=$?\"" % (sh, blockf)),
                       ("handover.sh && echo WROTE || echo FAILED", "/bin/bash '%s' write --stdin < '%s' >/dev/null 2>&1 && echo WROTE || echo FAILED" % (sh, blockf))):
        r = subprocess.run(["/bin/bash", "-c", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": "1"}))
        so = r.stdout.decode(); se = r.stderr.decode()
        print("- %-55s stdout last line: %-10s | 'written' on stdout: %s | stderr first line: %s" % (label, so.strip().split("\n")[-1], "handover: written" in so, se.strip().split("\n")[0][:110]))
    rc, o, e = ho(root, "write", "--stdin", data=blk("ROT"), env={"HANDOVER_LOCK_WAIT": "1"})
    print("- the refusal text, whole (stdout %d bytes, stderr below):\n%s" % (len(o), "\n".join("    " + l for l in e.rstrip().split("\n"))))
