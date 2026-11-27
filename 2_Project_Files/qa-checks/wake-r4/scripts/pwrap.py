# pwrap.py — round-4 checker's wrapper: runs the UNMODIFIED handover engine and, at ONE named point of a write,
# pauses it (until a gate file exists), kills it (SIGKILL on its own pid), or plants a foreign file in the lock directory.
# argv: <mode> <engine> [engine args...]
#   pause:<point>:<gate>     <gate>.waiting is created when the pause begins
#   kill:<point>
#   plant:<point>:<name>     create an empty file <lock dir>/<name> at the point, then go on
# points: after-mkdir | after-owner | after-fsync1 | after-fsync2 | before-replace1 | after-replace1 |
#         before-replace2 | after-replace2 | after-remove-owner | before-kill
# before-replaceN is INSIDE the engine's os.replace call, before the real rename: after every check the engine makes in Python.
import builtins, os, runpy, signal, sys, time
sys.dont_write_bytecode = True
mode, engine = sys.argv[1], sys.argv[2]
sys.argv = [engine] + sys.argv[3:]
kind, point, arg = (mode.split(":", 2) + [""])[:3]
r_mkdir, r_fsync, r_replace, r_remove, r_open, r_kill = os.mkdir, os.fsync, os.replace, os.remove, builtins.open, os.kill
n = {"fsync": 0, "replace": 0, "kill": 0}
lockdir = [None]
done = [False]


def at(p):
    if p != point or done[0]:
        return
    done[0] = True
    if kind == "kill":
        r_kill(os.getpid(), signal.SIGKILL); time.sleep(5)
    elif kind == "pause":
        r_open(arg + ".waiting", "w").close()
        while not os.path.exists(arg):
            time.sleep(0.005)
    elif kind == "plant":
        r_open(os.path.join(lockdir[0], arg), "w").close()


def p_mkdir(p, *a, **k):
    r = r_mkdir(p, *a, **k)
    if str(p).endswith(".lock.d"):
        lockdir[0] = p
        at("after-mkdir")
    return r


class _F:
    def __init__(self, f): self.f = f
    def __enter__(self): self.f.__enter__(); return self.f
    def __exit__(self, *a):
        r = self.f.__exit__(*a)
        at("after-owner")
        return r


def p_open(p, *a, **k):
    f = r_open(p, *a, **k)
    if isinstance(p, str) and p.endswith(".lock.d/owner") and a and "w" in a[0]:
        return _F(f)
    return f


def p_fsync(fd):
    n["fsync"] += 1
    r = r_fsync(fd)
    at("after-fsync%d" % n["fsync"])
    return r


def p_replace(a, b):
    n["replace"] += 1
    at("before-replace%d" % n["replace"])
    r = r_replace(a, b)
    at("after-replace%d" % n["replace"])
    return r


def p_remove(p, *a, **k):
    r = r_remove(p, *a, **k)
    if str(p).endswith(".lock.d/owner"):
        at("after-remove-owner")
    return r


def p_kill(pid, sig):
    n["kill"] += 1
    at("before-kill")
    return r_kill(pid, sig)


os.mkdir, os.fsync, os.replace, os.remove, builtins.open, os.kill = p_mkdir, p_fsync, p_replace, p_remove, p_open, p_kill
runpy.run_path(engine, run_name="__main__")
