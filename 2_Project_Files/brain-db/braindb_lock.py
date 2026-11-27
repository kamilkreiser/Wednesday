#!/usr/bin/env python3
"""braindb_lock.py <lock file> <wait seconds> <command...> - run one command while holding an exclusive lock.

braindb.sh wraps init, start and stop in this, so two commands that both find the server down cannot
both run initdb or pg_ctl on the same data directory (the second waits, then finds it running).

The lock is flock() on a file that is never deleted. The kernel releases it when this process ends,
however it ends, so there is no stale lock to clean up. The descriptor is not inheritable, so the
Postgres server started under the lock does not keep it. Standard library only.
"""
import sys, os, time, fcntl, subprocess

if len(sys.argv) < 4:
    print("usage: braindb_lock.py <lock file> <wait seconds> <command...>", file=sys.stderr)
    sys.exit(2)
path, wait_s, cmd = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
try:
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
except OSError as e:
    print("braindb: cannot open the lock file %s: %s" % (path, e), file=sys.stderr)
    sys.exit(2)
deadline = time.time() + wait_s
while True:
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        break
    except OSError:
        if time.time() > deadline:
            print("braindb: another braindb command has held %s for more than %.0f s; nothing was done" % (path, wait_s),
                  file=sys.stderr)
            sys.exit(75)
        time.sleep(0.1)
sys.exit(subprocess.call(cmd))
