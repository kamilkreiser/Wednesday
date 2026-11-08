#!/usr/bin/env python3
"""Seat X 8th: a HARD WALL-CLOCK BOUND for one command and everything it starts (Wednesday's ADDENDUM 06:36:21Z, from W 29th's hung ssh).
usage: bound_x8.py SECS cmd [args...]        SECS = whole seconds, at least 1
The command runs in its OWN session (start_new_session), so its children (the ssh that git starts) share one process group that this helper can
signal. stdin is /dev/null; stdout and stderr are inherited, so the caller's redirections and $( ) captures apply unchanged.
exit = the command's own exit code (a death by signal N reads 128+N)
       124 = the bound fired: TERM to the group, KILL 3 s later (reaps a grandchild that ignored TERM); one line on stderr: 'x8-bound: killed <cmd> after N s'
       125 = bad usage, 127 = the command could not be started, 130 = this helper was told to stop (TERM, INT or HUP) and took the group down with it.
F16 (gate 227): a suite that setpgid'd itself leaves that group, and a group kill misses it. So the kill also walks THIS command's descendants by parent pid, read at kill time. BOUND: a descendant already re-parented to launchd before the kill is not found.
Only this helper's own child and its descendants are ever signalled; nothing is looked up by name (STANDING_LINES 2026-10-28: stop only
processes you started, by the pid you recorded)."""
import os, signal, subprocess, sys


def main():
    if len(sys.argv) < 3 or not sys.argv[1].isdigit() or int(sys.argv[1]) < 1:
        print("usage: bound_x8.py SECS cmd [args...]   (SECS a whole number, at least 1)", file=sys.stderr)
        return 125
    secs, cmd = int(sys.argv[1]), sys.argv[2:]
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, start_new_session=True)
    except OSError as e:
        print(f"x8-bound: cannot start {cmd[0]}: {e}", file=sys.stderr)
        return 127
    pgid = p.pid                      # a new session makes the child its own group leader

    def descendants():
        kids = {}
        for l in subprocess.run(["ps", "-ax", "-o", "pid=,ppid="], capture_output=True, text=True).stdout.splitlines():
            f = l.split()
            if len(f) == 2 and f[0].isdigit() and f[1].isdigit():
                kids.setdefault(int(f[1]), []).append(int(f[0]))
        seen, todo = [], [p.pid]
        while todo:
            for c in kids.get(todo.pop(), []):
                seen.append(c); todo.append(c)
        return seen

    outside = []                      # F16: descendants that left the group, read once at the first signal (a dead parent would hide them from a later read)

    def kill_group(sig):
        if not outside:
            outside.extend(descendants())
        try:
            os.killpg(pgid, sig)
        except ProcessLookupError:    # the whole group is already gone
            pass
        for c in outside:
            try:
                os.kill(c, sig)
            except (ProcessLookupError, PermissionError):
                pass

    def stop(_signum, _frame):        # the driver (or a seat) told this helper to stop: take OUR group down, then go
        kill_group(signal.SIGTERM)
        try:
            p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            pass
        kill_group(signal.SIGKILL)
        os._exit(130)

    for s in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(s, stop)
    try:
        rc = p.wait(timeout=secs)
        return rc if rc >= 0 else 128 - rc
    except subprocess.TimeoutExpired:
        kill_group(signal.SIGTERM)
        try:
            p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            pass
        kill_group(signal.SIGKILL)    # also whatever in the group ignored TERM
        p.wait()
        print(f"x8-bound: killed {os.path.basename(cmd[0])} after {secs} s", file=sys.stderr)
        return 124


if __name__ == "__main__":
    sys.exit(main())
