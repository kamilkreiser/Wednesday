# wrap_replace.py — test wrapper: runs the UNMODIFIED handover engine with os.replace / os.fsync instrumented.
# Lifted from the checker's scripts/wrap.py (0_Brain/reference/2026-11-27_qa-wake/), which found Blocker B1.
# argv: <mode> <engine path> [engine args...]
#   barrier:<gate>            pause at the FIRST os.replace (after every check, lock held) until the file <gate> exists;
#                             <gate>.waiting is created when the pause begins
#   crash-before-2nd          os._exit(137) at the SECOND os.replace: the process dies between the archive rename
#                             and the state rename
#   edit-state-at-fsync2:<p>  at the second os.fsync (the state temp file), append bytes to the state file <p>:
#                             a hand edit landing while the write is being prepared
#   truncate-tmp-at-fsync1    after the first os.fsync (the archive temp file), cut one byte off that temp file:
#                             a temp file that does not read back as written
# Round 4 (the second checker's N2; pause-at-kill is lifted from its scripts/false_stale.py):
#   pause-at-kill:<gate>      pause at the FIRST os.kill (the liveness test of the pid just read from the owner
#                             file) until <gate> exists; <gate>.atkill is created when the pause begins
#   steal-lock-at:<n>:<lock>  inside the n-th os.replace, BEFORE the real rename (so after every check the
#                             engine makes in Python), move the lock directory away, as the recovery line does
#   steal-lock-after:<n>:<lock>   after the n-th os.replace has returned, move the lock directory away
#   swap-lock-after:<n>:<lock>    the same, then put ANOTHER owner's lock at the path (owner pid = our parent)
#   foreign-owner-at-fsync2:<lock>  at the second os.fsync, overwrite the lock's owner file with another owner's
import os
import runpy
import sys
import time

sys.dont_write_bytecode = True
mode = sys.argv[1]
engine = sys.argv[2]
sys.argv = [engine] + sys.argv[3:]
real_replace, real_fsync, real_kill = os.replace, os.fsync, os.kill
n_replace, n_fsync, n_kill = [0], [0], [0]
FOREIGN = "pid: %d\nhost: %s\nstarted: a foreign writer\nepoch: 1\ntoken: FOREIGN-TOKEN\n"


def nth(prefix):
    """'<prefix>:<n>:<path>' -> (n, path) when the mode is that one, else (None, None)."""
    if not mode.startswith(prefix + ":"):
        return None, None
    _, n, path = mode.split(":", 2)
    return int(n), path


def foreign_owner(lock):
    import socket
    with open(os.path.join(lock, "owner"), "w") as f:
        f.write(FOREIGN % (os.getppid(), socket.gethostname()))


def patched_kill(pid, sig):
    n_kill[0] += 1
    if mode.startswith("pause-at-kill:") and n_kill[0] == 1:
        gate = mode.split(":", 1)[1]
        open(gate + ".atkill", "w").close()
        while not os.path.exists(gate):
            time.sleep(0.005)
    return real_kill(pid, sig)


def patched_replace(a, b):
    n_replace[0] += 1
    if mode == "crash-before-2nd" and n_replace[0] == 2:
        os._exit(137)
    if mode.startswith("barrier:") and n_replace[0] == 1:
        gate = mode.split(":", 1)[1]
        open(gate + ".waiting", "w").close()
        while not os.path.exists(gate):
            time.sleep(0.01)
    n, lock = nth("steal-lock-at")
    if n == n_replace[0]:
        os.rename(lock, lock + ".stale-test")
    r = real_replace(a, b)
    for prefix in ("steal-lock-after", "swap-lock-after"):
        n, lock = nth(prefix)
        if n == n_replace[0]:
            os.rename(lock, lock + ".stale-test")
            if prefix == "swap-lock-after":
                os.mkdir(lock)
                foreign_owner(lock)
    return r


def patched_fsync(fd):
    n_fsync[0] += 1
    r = real_fsync(fd)
    if mode == "truncate-tmp-at-fsync1" and n_fsync[0] == 1:
        os.ftruncate(fd, os.fstat(fd).st_size - 1)
    if mode.startswith("edit-state-at-fsync2:") and n_fsync[0] == 2:
        with open(mode.split(":", 1)[1], "ab") as f:
            f.write(b"\nHAND-EDIT-DURING-THE-WRITE\n")
    if mode.startswith("foreign-owner-at-fsync2:") and n_fsync[0] == 2:
        foreign_owner(mode.split(":", 1)[1])
    return r


os.replace = patched_replace
os.fsync = patched_fsync
os.kill = patched_kill
runpy.run_path(engine, run_name="__main__")
