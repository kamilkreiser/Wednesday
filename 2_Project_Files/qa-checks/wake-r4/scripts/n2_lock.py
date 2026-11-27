# n2_lock.py — round 4 check, N2: the lock. Scratch trees only. A block is ACKNOWLEDGED when its writer exited 0.
# Every acknowledged block must be the state block or in the archive; the state file must hold ONE block.
# argv: section letters (default: all)   D displaced-writer matrix   T three-actor   K kill -9 + leftovers   S lock shapes
#                                         X rc 6 cases                 O owner-less real wait (slow, ~75 s)
import os, re, signal, socket, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_copies"))
from qlib import *
HERE = os.path.dirname(os.path.abspath(__file__))
PW = os.path.join(HERE, "pwrap.py")
PARTS = sys.argv[1:] or list("DTKSXO")
TAG = str(os.getpid())   # a fresh scratch sub-tree per run (run 2 of section S reused run 1's trees: instrument error)
POINTS = ["after-mkdir", "after-owner", "after-fsync1", "after-fsync2", "before-replace1", "after-replace1", "before-replace2", "after-replace2", "after-remove-owner"]
HEADS = [b"## FLOOR\n", b"## FIRST WORK\n", b"## OWED\n", b"## OPEN CARDS\n", b"## GRANTS IN PLAY\n"]


def now():
    return subprocess.run(["date", "+%H:%M:%S"], stdout=subprocess.PIPE).stdout.decode().strip()


def up():
    return subprocess.run(["uptime"], stdout=subprocess.PIPE).stdout.decode().strip().split("load averages:")[-1].strip()


def eng(root, mode, data, wait="5"):
    core = os.path.join(root, "2_Project_Files/wake/handover_core.py")
    p = subprocess.Popen([sys.executable, PW, mode, core, "write", "--seat", "wednesday", "--tasks-dir", T(root), "--stamp", "QA4", "--cap", "10000"],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV({"HANDOVER_LOCK_WAIT": wait}))
    p.stdin.write(data); p.stdin.close()
    return p


def waitfor(path, secs=40):
    t0 = time.time()
    while not os.path.exists(path):
        if time.time() - t0 > secs: return False
        time.sleep(0.005)
    return True


def fin(p, secs=60):
    try:
        rc = p.wait(timeout=secs)
    except subprocess.TimeoutExpired:
        p.kill(); p.wait(); return "HUNG", "", ""
    return rc, p.stdout.read().decode("utf-8", "replace"), p.stderr.read().decode("utf-8", "replace")


def kind_of(e):
    for k in ("STALE LOCK", "LOCK BUSY", "LOCK LOST", "NOT ACKNOWLEDGED", "I/O fault", "cannot take the write lock"):
        if k in e: return k
    return "-"


def rec_line(e, root):
    rec = [l.strip() for l in e.split("\n") if l.strip().startswith("mv -n '")]
    if len(rec) != 1 or rec[0].count(BASE) != 2:
        return None
    return rec[0]


def run_rec(line):
    return subprocess.run(["/bin/sh", "-c", line], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode


def account(root, named, rcs):
    """named: [(name, block)], rcs: {name: rc}. -> text + (lost, dup) lists"""
    a = rd(ar(root)) or b""; s = body(root)
    copies = dict((n, a.count(b) + (s == b)) for n, b in named)
    lost = [n for n, b in named if rcs.get(n) == 0 and copies[n] == 0]
    dup = [n for n, b in named if copies[n] > 1]
    ghost = [n for n, b in named if rcs.get(n) not in (0, None) and copies[n] > 0]
    sraw = rd(st(root)) or b""
    one = all(sraw.count(h) == 1 for h in HEADS)
    state_is = [n for n, b in named if s == b]
    rc_chk, o_chk, _ = ho(root, "check")
    t = T(root)
    left_lock = os.path.lexists(lockd(root))
    inside = sorted(os.listdir(lockd(root))) if os.path.isdir(lockd(root)) else None
    stale = sorted(f for f in os.listdir(t) if ".lock.d.stale" in f)
    tmps = sorted(f for f in os.listdir(t) if ".md.tmp." in f)
    n_arch = len(re.findall(rb"^# ARCHIVED ", a, re.M))
    txt = ("copies %s | state is %s, ONE block %s, check rc %d | archive entries %d | lock dir left %s%s | set-aside dirs %d | temp files beside the state file %d"
           % (" ".join("%s:%d" % (n, copies[n]) for n, _ in named), state_is or "?", one, rc_chk, n_arch, left_lock,
              (" holding %s" % [re.sub(r"\.tmp\..*", ".tmp.*", x) for x in inside]) if inside is not None else "", len(stale), len(tmps)))
    return txt, lost, dup, ghost


TOTAL = {"cases": 0, "acked": 0, "lost": 0}


def tally(rcs, lost):
    TOTAL["cases"] += 1; TOTAL["acked"] += sum(1 for v in rcs.values() if v == 0); TOTAL["lost"] += len(lost)


if "D" in PARTS:
    print("## D. the PRINTED recovery line run while a writer is ALIVE, the writer paused at every point of its write (load %s)" % up())
    print("   history: S0, S1 acknowledged. C is paused at <point>. A waiter W (1 s) is refused; the line W's refusal prints is run as printed;")
    print("   D and E then write; C is released; if C exits non-zero a caller that reads non-zero as 'not written' writes C's block AGAIN (C2); F writes last.")
    for arch in (True, False):
        for pt in POINTS:
            if not arch and pt in ("after-replace2", "before-replace2", "after-fsync2"): continue     # a first write makes one rename
            root = mk("%s_%s" % (pt, "arch" if arch else "first"), "n2_displace_" + TAG)
            B = dict((n, blk(n)) for n in ("S0", "S1", "C", "W", "D", "E", "F"))
            rcs = {}
            if arch:
                rcs["S0"] = ho(root, "write", "--stdin", data=B["S0"])[0]; rcs["S1"] = ho(root, "write", "--stdin", data=B["S1"])[0]
            gate = os.path.join(BASE, "n2_displace_" + TAG, "%s_%s" % (pt, "arch" if arch else "first"), "gate")
            pc = eng(root, "pause:%s:%s" % (pt, gate), B["C"], wait="5")
            if not waitfor(gate + ".waiting"):
                print("- %-20s %-5s INSTRUMENT: C never reached the pause point; skipped" % (pt, "arch" if arch else "first")); pc.kill(); continue
            rcw, ow, ew = ho(root, "write", "--stdin", data=B["W"], env={"HANDOVER_LOCK_WAIT": "1"}); rcs["W"] = rcw
            line = rec_line(ew, root); ran = run_rec(line) if line else None
            rcs["D"], od, ed = ho(root, "write", "--stdin", data=B["D"], env={"HANDOVER_LOCK_WAIT": "3"})
            rcs["E"], oe, ee = ho(root, "write", "--stdin", data=B["E"], env={"HANDOVER_LOCK_WAIT": "3"})
            open(gate, "w").close()
            rcc, oc, ec = fin(pc); rcs["C"] = rcc
            said = "handover: written" in oc
            c2 = "-"
            named = [(n, B[n]) for n in (("S0", "S1") if arch else ()) + ("C", "W", "D", "E", "F")]
            mid_txt, mid_lost, _, _ = account(root, named, rcs)
            if rcc != 0:
                rc2, o2, e2 = ho(root, "write", "--stdin", data=B["C"], env={"HANDOVER_LOCK_WAIT": "1"})
                c2 = "rc %s %s" % (rc2, kind_of(e2))
                if rc2 == 0: rcs["C"] = 0
                elif kind_of(e2) in ("STALE LOCK", "LOCK BUSY"):
                    l2 = rec_line(e2, root)
                    c2 += "; its line run rc %s" % (run_rec(l2) if l2 else None)
                    rc3, o3, e3 = ho(root, "write", "--stdin", data=B["C"], env={"HANDOVER_LOCK_WAIT": "1"}); c2 += "; again rc %s" % rc3
                    if rc3 == 0: rcs["C"] = 0
            rcs["F"], of_, ef = ho(root, "write", "--stdin", data=B["F"], env={"HANDOVER_LOCK_WAIT": "1"})
            txt, lost, dup, ghost = account(root, named, rcs)
            tally(rcs, lost + mid_lost)
            print("- %-20s %-5s W rc %s %s, line run rc %s | D rc %s%s, E rc %s%s | C rc %s %s, said written %s | C again: %s | F rc %s %s\n      before C2: lost %s\n      end: %s\n      => acknowledged LOST %s; more than one copy %s"
                  % (pt, "arch" if arch else "first", rcw, kind_of(ew), ran, rcs["D"], (" " + kind_of(ed)) if rcs["D"] else "", rcs["E"], (" " + kind_of(ee)) if rcs["E"] else "",
                     rcc, kind_of(ec), said, c2, rcs["F"], kind_of(ef) if rcs["F"] else "", mid_lost or "none", txt, (lost + mid_lost) or "NONE", dup or "none"))
    print("D total: cases %d, acknowledged writes %d, acknowledged LOST %d" % (TOTAL["cases"], TOTAL["acked"], TOTAL["lost"]))

if "T" in PARTS:
    print("## T. three actors: C is paused and DISPLACED (lock moved away as the recovery line does); D then takes a NEW lock and is itself paused; C is released first, then D (load %s)" % up())
    t_tot = {"cases": 0, "acked": 0, "lost": 0}
    for cpt in ("after-mkdir", "after-owner", "after-fsync1", "after-fsync2", "before-replace1", "before-replace2"):
        for dpt in ("after-owner", "after-fsync1", "before-replace1", "before-replace2", "after-replace2", "after-remove-owner"):
            name = "%s__%s" % (cpt, dpt); root = mk(name, "n2_three_" + TAG)
            B = dict((n, blk(n)) for n in ("S0", "S1", "C", "D", "F", "G"))
            rcs = {"S0": ho(root, "write", "--stdin", data=B["S0"])[0], "S1": ho(root, "write", "--stdin", data=B["S1"])[0]}
            gc = os.path.join(BASE, "n2_three_" + TAG, name, "gateC"); gd = os.path.join(BASE, "n2_three_" + TAG, name, "gateD")
            pc = eng(root, "pause:%s:%s" % (cpt, gc), B["C"], wait="5")
            if not waitfor(gc + ".waiting"): print("- %s INSTRUMENT: C not paused" % name); pc.kill(); continue
            os.rename(lockd(root), lockd(root) + ".stale-qa-1")
            pd = eng(root, "pause:%s:%s" % (dpt, gd), B["D"], wait="5")
            if not waitfor(gd + ".waiting"): print("- %s INSTRUMENT: D not paused" % name); pd.kill(); open(gc, "w").close(); pc.wait(); continue
            open(gc, "w").close(); rcc, oc, ec = fin(pc); rcs["C"] = rcc
            open(gd, "w").close(); rcd, od, ed = fin(pd); rcs["D"] = rcd
            rcf, of_, ef = ho(root, "write", "--stdin", data=B["F"], env={"HANDOVER_LOCK_WAIT": "1"}); rcs["F"] = rcf
            named = [(n, B[n]) for n in ("S0", "S1", "C", "D", "F", "G")]
            txt1, lost1, _, _ = account(root, named, rcs)
            g = "-"
            if rcf != 0:
                l = rec_line(ef, root); rr = run_rec(l) if l else None
                rcs["G"], og, eg = ho(root, "write", "--stdin", data=B["G"], env={"HANDOVER_LOCK_WAIT": "1"}); g = "line rc %s, G rc %s %s" % (rr, rcs["G"], kind_of(eg) if rcs["G"] else "")
            txt, lost, dup, ghost = account(root, named, rcs)
            t_tot["cases"] += 1; t_tot["acked"] += sum(1 for v in rcs.values() if v == 0); t_tot["lost"] += len(set(lost + lost1))
            print("- C@%-15s D@%-18s C rc %s %-16s D rc %s %-16s F rc %s %-10s %s | %s => LOST %s; dup %s"
                  % (cpt, dpt, rcc, kind_of(ec), rcd, kind_of(ed), rcf, kind_of(ef) if rcf else "", g, txt, sorted(set(lost + lost1)) or "NONE", dup or "none"))
    print("T total: cases %d, acknowledged writes %d, acknowledged LOST %d" % (t_tot["cases"], t_tot["acked"], t_tot["lost"]))
    print("## T2. two displaced writers in a row, the SAME recovery line used twice (same .stale-<stamp> name)")
    root = mk("two", "n2_two_" + TAG); B = dict((n, blk(n)) for n in ("S0", "S1", "C1", "C2", "D", "E"))
    rcs = {"S0": ho(root, "write", "--stdin", data=B["S0"])[0], "S1": ho(root, "write", "--stdin", data=B["S1"])[0]}
    g1 = os.path.join(BASE, "n2_two_" + TAG, "two", "g1"); g2 = os.path.join(BASE, "n2_two_" + TAG, "two", "g2")
    p1 = eng(root, "pause:before-replace1:" + g1, B["C1"]); waitfor(g1 + ".waiting")
    rcw, ow, ew = ho(root, "write", "--stdin", data=blk("W"), env={"HANDOVER_LOCK_WAIT": "1"}); line = rec_line(ew, root)
    r1 = run_rec(line)
    p2 = eng(root, "pause:after-fsync1:" + g2, B["C2"]); waitfor(g2 + ".waiting")
    r2 = run_rec(line)      # the very same printed line, a second time
    where = sorted(f for f in os.listdir(T(root)) if "lock.d" in f)
    rcs["D"] = ho(root, "write", "--stdin", data=B["D"], env={"HANDOVER_LOCK_WAIT": "2"})[0]
    open(g1, "w").close(); open(g2, "w").close()
    rcs["C1"], o1, e1 = fin(p1); rcs["C2"], o2, e2 = fin(p2)
    rcs["E"], oe, ee = ho(root, "write", "--stdin", data=B["E"], env={"HANDOVER_LOCK_WAIT": "2"})
    txt, lost, dup, ghost = account(root, [(n, B[n]) for n in ("S0", "S1", "C1", "C2", "D", "E")], rcs)
    print("- line run twice: rc %s then rc %s; lock entries after the second run: %s\n  C1 rc %s %s; C2 rc %s %s; D rc %s; E rc %s %s | %s => LOST %s"
          % (r1, r2, where, rcs["C1"], kind_of(e1), rcs["C2"], kind_of(e2), rcs["D"], rcs["E"], kind_of(ee) if rcs["E"] else "", txt, lost or "NONE"))

if "K" in PARTS:
    print("## K. kill -9 at every point; what is left; what `check`, the next writer and the printed line do with it (load %s)" % up())
    for pt in POINTS:
        root = mk(pt, "n2_kill_" + TAG); B = dict((n, blk(n)) for n in ("S0", "S1", "C", "F"))
        rcs = {"S0": ho(root, "write", "--stdin", data=B["S0"])[0], "S1": ho(root, "write", "--stdin", data=B["S1"])[0]}
        pc = eng(root, "kill:" + pt, B["C"]); rcc, oc, ec = fin(pc); rcs["C"] = None if rcc != 0 else 0
        inside = sorted(re.sub(r"\.tmp\..*", ".tmp.*", x) for x in os.listdir(lockd(root))) if os.path.isdir(lockd(root)) else "no lock dir"
        tmps = [f for f in os.listdir(T(root)) if ".md.tmp." in f]
        rck, ok_, _ = ho(root, "check")
        t0 = time.time(); rc1, o1, e1 = ho(root, "write", "--stdin", data=B["F"], env={"HANDOVER_LOCK_WAIT": "1"}); took = time.time() - t0
        k1 = kind_of(e1) if rc1 else "written"
        ran = "-"
        if rc1 != 0:
            l = rec_line(e1, root); ran = run_rec(l) if l else None
            rc2, o2, e2 = ho(root, "write", "--stdin", data=B["F"], env={"HANDOVER_LOCK_WAIT": "1"})
        else:
            rc2 = rc1
        rcs["F"] = rc2
        txt, lost, dup, ghost = account(root, [(n, B[n]) for n in ("S0", "S1", "C", "F")], rcs)
        set_aside = [sorted(re.sub(r"\.tmp\..*", ".tmp.*", x) for x in os.listdir(os.path.join(T(root), d))) for d in os.listdir(T(root)) if ".lock.d.stale" in d]
        print("- kill at %-19s engine rc %s, said written %s | left in the lock dir: %s; temp files beside the state file %d; check rc %d | next write rc %s %s in %.1fs; its line run rc %s; then rc %s\n      end: %s; the set-aside dir holds %s => LOST %s"
              % (pt, rcc, "handover: written" in oc, inside, len(tmps), rck, rc1, k1, took, ran, rc2, txt, set_aside, lost or "NONE"))

if "S" in PARTS:
    print("## S. the lock path is not a plain fresh directory (HANDOVER_LOCK_WAIT 1)")
    dead = subprocess.Popen([sys.executable, "-c", "pass"]); dead.wait(); host = socket.gethostname()
    old = time.time() - 300

    def shape(label, make):
        root = mk(re.sub(r"\W+", "_", label)[:40], "n2_shape_" + TAG); ho(root, "write", "--stdin", data=blk("S0")); L = lockd(root)
        make(root, L)
        def snap():   # (instrument fix: run 1 crashed here on a mode-000 lock dir, and read 'state still S0' AFTER the retry)
            try: inside = sorted(os.listdir(L)) if os.path.isdir(L) else None
            except OSError as ex: inside = "unlistable: %s" % ex.strerror
            return (os.path.islink(L), os.path.isdir(L), inside)
        before = snap()
        t0 = time.time(); rc, o, e = ho(root, "write", "--stdin", data=blk("A"), env={"HANDOVER_LOCK_WAIT": "1"}); took = time.time() - t0
        after = snap(); still = body(root) == blk("S0")
        l = rec_line(e, root); ran = run_rec(l) if l else None
        rc2, o2, e2 = ho(root, "write", "--stdin", data=blk("A"), env={"HANDOVER_LOCK_WAIT": "1"})
        print("- %-66s rc %s %-10s %.1fs; traceback %s; left exactly as it was %s; state still S0 %s | its line run rc %s; write again rc %s%s"
              % (label, rc, kind_of(e), took, "YES" if "Traceback" in e else "no", before == after, still if rc else "(written)", ran, rc2, "" if rc2 == 0 else " " + kind_of(e2)))

    shape("a regular FILE, fresh", lambda r, L: open(L, "w").write("x"))
    shape("a regular FILE, 5 minutes old", lambda r, L: (open(L, "w").write("x"), os.utime(L, (old, old))))
    shape("a dangling symlink (lstat mtime is the link's: fresh)", lambda r, L: os.symlink(os.path.join(r, "nowhere"), L))
    def linkdir(r, L, owner):
        d = os.path.join(r, "elsewhere_lock"); os.mkdir(d)
        if owner is not None: open(os.path.join(d, "owner"), "w").write(owner)
        os.symlink(d, L)
    shape("a symlink to a directory whose owner file names a DEAD pid here", lambda r, L: linkdir(r, L, "pid: %d\nhost: %s\nstarted: x\ntoken: t\n" % (dead.pid, host)))
    shape("a symlink to a directory whose owner names a LIVE unrelated pid", lambda r, L: linkdir(r, L, "pid: %d\nhost: %s\nstarted: x\ntoken: t\n" % (os.getpid(), host)))
    shape("a symlink to an EMPTY directory (fresh)", lambda r, L: linkdir(r, L, None))
    shape("a directory, owner names a LIVE unrelated pid (pid reuse)", lambda r, L: (os.mkdir(L), open(os.path.join(L, "owner"), "w").write("pid: %d\nhost: %s\nstarted: long ago\nepoch: 1\ntoken: old\n" % (os.getpid(), host))))
    shape("a directory, owner names pid 1 on this host", lambda r, L: (os.mkdir(L), open(os.path.join(L, "owner"), "w").write("pid: 1\nhost: %s\n" % host)))
    shape("a directory, owner: a dead pid on ANOTHER host, 5 minutes old", lambda r, L: (os.mkdir(L), open(os.path.join(L, "owner"), "w").write("pid: %d\nhost: other-mac\n" % dead.pid), os.utime(L, (old, old))))
    shape("a directory, owner: dead pid, host line MISSING", lambda r, L: (os.mkdir(L), open(os.path.join(L, "owner"), "w").write("pid: %d\n" % dead.pid)))
    shape("a directory, owner file is a DIRECTORY, 5 minutes old", lambda r, L: (os.mkdir(L), os.mkdir(os.path.join(L, "owner")), os.utime(L, (old, old))))
    shape("a directory, no owner, holding a stray temp file, 5 minutes old", lambda r, L: (os.mkdir(L), open(os.path.join(L, "state.tmp.999-abc"), "w").write("x"), os.utime(L, (old, old))))
    shape("a directory, owner pid NEGATIVE (-1)", lambda r, L: (os.mkdir(L), open(os.path.join(L, "owner"), "w").write("pid: -1\nhost: %s\n" % host)))
    shape("a directory, owner pid with a + sign / spaces / unicode digits", lambda r, L: (os.mkdir(L), open(os.path.join(L, "owner"), "w", encoding="utf-8").write("pid: +١٢ 3\nhost: %s\n" % host)))
    shape("a directory, a 2 MB owner file of garbage", lambda r, L: (os.mkdir(L), open(os.path.join(L, "owner"), "wb").write(os.urandom(2000000))))
    shape("a directory, owner is a dead pid here but the dir is mode 000", lambda r, L: (os.mkdir(L), open(os.path.join(L, "owner"), "w").write("pid: %d\nhost: %s\n" % (dead.pid, host)), os.chmod(L, 0)))
    for d, _, _ in os.walk(os.path.join(BASE, "n2_shape_" + TAG)):
        if d.endswith(".lock.d") or ".lock.d.stale" in os.path.basename(d):
            try: os.chmod(d, 0o755)
            except OSError: pass

if "X" in PARTS:
    print("## X. rc 6: what is on disk, and what a caller that writes again gets")
    def x(label, mode_of, after=None):
        root = mk(re.sub(r"\W+", "_", label)[:40], "n2_rc6_" + TAG); B = dict((n, blk(n)) for n in ("S0", "S1", "C", "F"))
        rcs = {"S0": ho(root, "write", "--stdin", data=B["S0"])[0], "S1": ho(root, "write", "--stdin", data=B["S1"])[0]}
        gate = os.path.join(os.path.dirname(root), "gate")
        pc = eng(root, mode_of(gate), B["C"])
        if after: after(root, gate)
        rcc, oc, ec = fin(pc); rcs["C"] = rcc
        txt0, lost0, _, _ = account(root, [(n, B[n]) for n in ("S0", "S1", "C", "F")], rcs)
        t0 = time.time(); rc2, o2, e2 = ho(root, "write", "--stdin", data=B["C"], env={"HANDOVER_LOCK_WAIT": "1"}); took = time.time() - t0
        again = "rc %s %s in %.1fs" % (rc2, kind_of(e2) if rc2 else "written", took)
        if rc2 == 0: rcs["C"] = 0
        txt, lost, dup, ghost = account(root, [(n, B[n]) for n in ("S0", "S1", "C", "F")], rcs)
        print("- %-62s C rc %s %s; stdout %r\n      right after: %s\n      the caller writes C again: %s\n      then: %s => LOST %s; dup %s" % (label, rcc, kind_of(ec), oc.strip()[:30], txt0, again, txt, (lost0 + lost) or "NONE", dup or "none"))
        return root

    def mv_after(root, gate):
        waitfor(gate + ".waiting"); os.rename(lockd(root), lockd(root) + ".stale-qa"); open(gate, "w").close()
    x("the lock moved away after the 2nd rename (recovery line run then)", lambda g: "pause:after-replace2:" + g, mv_after)
    x("a foreign FILE appears in the lock dir before the 2nd rename (.DS_Store)", lambda g: "plant:before-replace2:.DS_Store")
    x("a foreign FILE appears in the lock dir after the owner is written", lambda g: "plant:after-owner:._owner")
    def mv_at_unlock(root, gate):
        waitfor(gate + ".waiting"); os.rename(lockd(root), lockd(root) + ".stale-qa"); open(gate, "w").close()
    x("the lock moved away between 'owner removed' and rmdir", lambda g: "pause:after-remove-owner:" + g, mv_at_unlock)
    def chmod_at(root, gate):
        waitfor(gate + ".waiting"); os.chmod(T(root), 0o555); open(gate, "w").close(); time.sleep(1.5); os.chmod(T(root), 0o755)
    x("the tasks directory becomes read-only after the 2nd rename (rmdir fails)", lambda g: "pause:after-replace2:" + g, chmod_at)
    print("   ordinary use: 60 plain writes one after another, exit codes seen (rc 6 must not appear without interference):")
    root = mk("plain", "n2_rc6_" + TAG); seen = {}
    for i in range(60):
        rc, o, e = ho(root, "write", "--stdin", data=blk("P%d" % i)); seen[rc] = seen.get(rc, 0) + 1
    print("   %s; lock dir left %s; files in tasks: %s" % (seen, os.path.exists(lockd(root)), sorted(os.listdir(T(root)))))

if "O" in PARTS:
    print("## O. the owner-less rule with a REAL wait (no aged mtime). load before: %s; %s" % (up(), now()))
    root = mk("real_wait", "n2_ownerless_" + TAG); ho(root, "write", "--stdin", data=blk("S0"))
    pc = eng(root, "kill:after-mkdir", blk("C")); rcc, oc, ec = fin(pc)
    made = os.stat(lockd(root)).st_mtime
    print("- a writer was killed -9 between mkdir and the owner file: engine rc %s; lock dir holds %s" % (rcc, os.listdir(lockd(root))))
    t0 = time.time(); rc, o, e = ho(root, "write", "--stdin", data=blk("A"), env={"HANDOVER_LOCK_WAIT": "5"})
    print("- at +%.0f s (wait 5): rc %s %s after %.1f s" % (t0 - made, rc, kind_of(e), time.time() - t0))
    t0 = time.time(); rc, o, e = ho(root, "write", "--stdin", data=blk("A"), env={"HANDOVER_LOCK_WAIT": "120"}); took = time.time() - t0
    print("- then ONE writer with a 120 s wait, started at +%.0f s: rc %s %s after %.1f s, i.e. when the lock was %.0f s old; says 'no usable owner file' %s"
          % (t0 - made, rc, kind_of(e), took, time.time() - made, "no usable owner file" in e))
    l = rec_line(e, root); ran = run_rec(l) if l else None
    rc2, o2, e2 = ho(root, "write", "--stdin", data=blk("A"))
    print("- its line run rc %s; write again rc %s; state is A %s; S0 in archive %d. load after: %s; %s" % (ran, rc2, body(root) == blk("A"), (rd(ar(root)) or b"").count(blk("S0")), up(), now()))
