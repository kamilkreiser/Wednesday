# kwrap.py — my own wrapper: runs the UNMODIFIED engine and SIGKILLs it (kill -9 on its own pid) at one chosen step,
# or pauses it at the first rename. argv: <mode> <engine> [engine args...]
#   kill:mkdir        right after the lock directory is made, before the owner file is written
#   kill:owner        right after the owner file is written and closed (lock fully taken, nothing read yet)
#   kill:fsync1       after the first temp file is fsynced (archive temp when there is one)
#   kill:fsync2       after the second temp file is fsynced
#   kill:pre-rename1  just before the first os.replace
#   kill:mid          between the two renames (after the first os.replace returned)
#   kill:post-rename2 after the last os.replace, before the lock is released and before 'written' is printed
#   kill:unlock-mid   after the owner file is removed, before rmdir
#   barrier:<gate>    pause before the first os.replace until <gate> exists (<gate>.waiting marks the pause)
import os, runpy, signal, sys, time, builtins
sys.dont_write_bytecode = True
mode, engine = sys.argv[1], sys.argv[2]
sys.argv = [engine] + sys.argv[3:]
N_REN = int(os.environ.get("KW_RENAMES", "2"))   # how many os.replace calls this write makes (1 when there is no archive)


def die():
    os.kill(os.getpid(), signal.SIGKILL)
    time.sleep(5)


r_mkdir, r_fsync, r_replace, r_remove, r_open = os.mkdir, os.fsync, os.replace, os.remove, builtins.open
n = {"fsync": 0, "replace": 0}


def p_mkdir(p, *a, **k):
    r = r_mkdir(p, *a, **k)
    if mode == "kill:mkdir" and p.endswith(".lock.d"):
        die()
    return r


class _F:
    def __init__(self, f): self.f = f
    def __enter__(self): self.f.__enter__(); return self.f
    def __exit__(self, *a):
        r = self.f.__exit__(*a)
        die()
        return r


def p_open(p, *a, **k):
    f = r_open(p, *a, **k)
    if mode == "kill:owner" and isinstance(p, str) and p.endswith(".lock.d/owner") and a and "w" in a[0]:
        return _F(f)
    return f


def p_fsync(fd):
    n["fsync"] += 1
    r = r_fsync(fd)
    if mode == "kill:fsync%d" % n["fsync"]:
        die()
    return r


def p_replace(a, b):
    n["replace"] += 1
    if n["replace"] == 1:
        if mode == "kill:pre-rename1":
            die()
        if mode.startswith("barrier:"):
            gate = mode.split(":", 1)[1]
            r_open(gate + ".waiting", "w").close()
            while not os.path.exists(gate):
                time.sleep(0.01)
    r = r_replace(a, b)
    if mode == "kill:mid" and n["replace"] == 1 and N_REN == 2:
        die()
    if mode == "kill:post-rename2" and n["replace"] == N_REN:
        die()
    return r


def p_remove(p, *a, **k):
    r = r_remove(p, *a, **k)
    if mode == "kill:unlock-mid" and p.endswith(".lock.d/owner"):
        die()
    return r


os.mkdir, os.fsync, os.replace, os.remove, builtins.open = p_mkdir, p_fsync, p_replace, p_remove, p_open
runpy.run_path(engine, run_name="__main__")
