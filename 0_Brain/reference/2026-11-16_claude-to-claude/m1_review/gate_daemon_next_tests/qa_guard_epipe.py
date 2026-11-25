#!/usr/bin/env python3
"""QA-DAEMON-NOTES: the relay guard's new stderr lines when nobody reads its stderr any more (the
daemon crashed: the guard's stderr is a pipe to the daemon). Runs `coagentd relay-guard` directly, as
the daemon does: stdin a pipe carrying the identity frame (4-byte big-endian length + blob), stderr a
pipe. Then the stderr pipe's read end is closed (the daemon gone) and stdin closed (end of input).
Reports the guard's exit status and whether the relay it started is gone.
Usage: python3 -B qa_guard_epipe.py <bin dir> <identity blob file> [--keep-reader]"""
import os, signal, struct, subprocess, sys, time

bindir, blobf = sys.argv[1], sys.argv[2]
keep_reader = "--keep-reader" in sys.argv
blob = open(blobf, "rb").read()
r, w = os.pipe()
g = subprocess.Popen([os.path.join(bindir, "coagentd"), "relay-guard", "--coagent", os.path.join(bindir, "coagent"),
                      "--listen", "127.0.0.1:0"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=w,
                     env={"PATH": "/usr/bin:/bin", "HOME": "/nonexistent-qa"}, cwd="/")
os.close(w)
g.stdin.write(struct.pack(">I", len(blob)) + blob)
g.stdin.flush()
line = g.stdout.readline().decode().strip()
relay_pid = int(line.rsplit(" ", 1)[1]) if line.startswith("relay-guard: relay pid") else None
time.sleep(1.0)
early = b""
os.set_blocking(r, False)
try:
    early = os.read(r, 65536)
except BlockingIOError:
    pass
if not keep_reader:
    os.close(r)          # the daemon (the stderr reader) is gone
g.stdin.close()          # end of input: the guard stops the relay
code = g.wait(15)
late = b""
if keep_reader:
    os.set_blocking(r, True)
    late = os.read(r, 65536)
    os.close(r)


def alive(p):
    try:
        os.kill(p, 0)
        return True
    except ProcessLookupError:
        return False


print(f"guard said: {line!r}; relay alive after the guard exited: {alive(relay_pid) if relay_pid else 'n/a'}")
print(f"guard exit status: {code} (negative = killed by that signal)")
print(f"stderr before: {early.decode(errors='replace').strip()!r}")
if keep_reader:
    print(f"stderr after end of input: {late.decode(errors='replace').strip()!r}")
if relay_pid and alive(relay_pid):
    os.kill(relay_pid, signal.SIGKILL)
    print("relay killed by this script")
