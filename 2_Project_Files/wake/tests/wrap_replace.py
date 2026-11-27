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
import os
import runpy
import sys
import time

sys.dont_write_bytecode = True
mode = sys.argv[1]
engine = sys.argv[2]
sys.argv = [engine] + sys.argv[3:]
real_replace, real_fsync = os.replace, os.fsync
n_replace, n_fsync = [0], [0]


def patched_replace(a, b):
    n_replace[0] += 1
    if mode == "crash-before-2nd" and n_replace[0] == 2:
        os._exit(137)
    if mode.startswith("barrier:") and n_replace[0] == 1:
        gate = mode.split(":", 1)[1]
        open(gate + ".waiting", "w").close()
        while not os.path.exists(gate):
            time.sleep(0.01)
    return real_replace(a, b)


def patched_fsync(fd):
    n_fsync[0] += 1
    r = real_fsync(fd)
    if mode == "truncate-tmp-at-fsync1" and n_fsync[0] == 1:
        os.ftruncate(fd, os.fstat(fd).st_size - 1)
    if mode.startswith("edit-state-at-fsync2:") and n_fsync[0] == 2:
        with open(mode.split(":", 1)[1], "ab") as f:
            f.write(b"\nHAND-EDIT-DURING-THE-WRITE\n")
    return r


os.replace = patched_replace
os.fsync = patched_fsync
runpy.run_path(engine, run_name="__main__")
