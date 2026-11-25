#!/usr/bin/env python3
"""QA-DAEMON-NEXT (b): `coagentd relay-guard` through the real binary, as the daemon runs it (stdin a
pipe carrying the identity frame: 4-byte big-endian length, then the bytes; stdout and stderr pipes).
Extends the DAEMON-NOTES check's qa_guard_epipe.py to the relay-exit arm, a stand-in relay that exits
with code 3, and hostile variants (reader closed at other moments, stdout closed too, fd 2 closed,
SIGPIPE ignored / default, stdout closed before the `relay pid` line).
Usage: python3 -B qa_guard.py <bin dir> <identity blob file> <work dir> <label>
One line per case: label | case | exit status | relay gone after the guard | stderr bytes (the `<n> ms`
digits normalised) | notes. Every relay left running is SIGKILLed by this script and reported."""
import os, re, select, signal, struct, subprocess, sys, time

BIN, BLOBF, WORK, LABEL = sys.argv[1:5]
COAGENTD = os.path.join(BIN, "coagentd")
blob = open(BLOBF, "rb").read()
FRAME = struct.pack(">I", len(blob)) + blob
os.makedirs(WORK, exist_ok=True)


def state(pid):
    """'' = no such process; else ps STAT (Z = zombie)."""
    r = subprocess.run(["/bin/ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True)
    return r.stdout.strip()


def gone(pid):
    s = state(pid)
    return s == "" or s.startswith("Z")


def stand_in(tag):
    exe = os.path.join(WORK, f"{tag}.coagent")
    pidf = os.path.join(WORK, f"{tag}.pid")
    go = os.path.join(WORK, f"{tag}.go")
    for f in (pidf, go):
        if os.path.exists(f):
            os.rename(f, f + f".old{time.time_ns()}")
    with open(exe, "w") as f:
        f.write(f"#!/bin/sh\necho $$ > '{pidf}'\nexec >/dev/null 2>&1\ncat >/dev/null\n"
                f"while [ ! -e '{go}' ]; do /bin/sleep 0.05 </dev/null; done\nexit 3\n")
    os.chmod(exe, 0o700)
    return exe, pidf, go


def read_line(fobj, t=10):
    fd = fobj.fileno()
    buf = b""
    t0 = time.time()
    while not buf.endswith(b"\n") and time.time() - t0 < t:
        r, _, _ = select.select([fd], [], [], 0.2)
        if r:
            c = os.read(fd, 1)
            if not c:
                break
            buf += c
    return buf.decode(errors="replace")


def children(ppid):
    r = subprocess.run(["/usr/bin/pgrep", "-P", str(ppid)], capture_output=True, text=True)
    return [int(x) for x in r.stdout.split()]


def case(name, relay, event, err_close="after_pid_sleep", out_close=None, fd2_closed=False, sigpipe="default"):
    tag = f"{LABEL}_{name}".replace(" ", "_").replace("/", "_")
    notes = []
    if relay == "stand":
        coagent, pidf, go = stand_in(tag)
    else:
        coagent, pidf, go = os.path.join(BIN, "coagent"), None, None
    gargs = [COAGENTD, "relay-guard", "--coagent", coagent, "--listen", "127.0.0.1:0"]
    r = w = None
    if fd2_closed:
        argv = ["/bin/sh", "-c", 'exec "$0" "$@" 2>&-'] + gargs
        errarg = subprocess.DEVNULL
    else:
        r, w = os.pipe()
        argv = gargs
        errarg = w
    g = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errarg,
                         env={"PATH": "/usr/bin:/bin", "HOME": "/nonexistent-qa"}, cwd="/",
                         restore_signals=(sigpipe == "default"))
    if w is not None:
        os.close(w)
    if err_close == "before_frame" and r is not None:
        os.close(r); r = None
    if out_close == "before_pid":
        g.stdout.close()
    g.stdin.write(FRAME)
    g.stdin.flush()
    line = ""
    relay_pid = None
    if out_close != "before_pid":
        line = read_line(g.stdout)
        if line.startswith("relay-guard: relay pid "):
            relay_pid = int(line.strip().rsplit(" ", 1)[1])
    if relay_pid is None:
        # no line (stdout closed before it, or the guard ended): look for the guard's child
        t0 = time.time()
        while time.time() - t0 < 3 and relay_pid is None:
            c = children(g.pid)
            relay_pid = c[0] if c else None
            if g.poll() is not None:
                break
            time.sleep(0.05)
        notes.append(f"pid line {line!r}; relay pid from pgrep -P: {relay_pid}")
    if pidf:
        t0 = time.time()
        while time.time() - t0 < 5 and not os.path.exists(pidf):
            time.sleep(0.02)
    if out_close == "after_pid":
        g.stdout.close()
    early = b""
    if err_close == "after_pid" and r is not None:
        os.close(r); r = None
    elif err_close in ("after_pid_sleep", "never"):
        time.sleep(1.0)
        if err_close == "after_pid_sleep" and r is not None:
            os.set_blocking(r, False)
            try:
                early = os.read(r, 65536)
            except BlockingIOError:
                pass
            os.close(r); r = None
    elif err_close == "with_eof":
        time.sleep(1.0)
    guard_alive_before = g.poll() is None
    if not guard_alive_before:
        notes.append(f"guard already exited ({g.returncode}) before the event")
    t_ev = time.time()
    if event == "eoi":
        if err_close == "with_eof" and r is not None:
            os.close(r); r = None
        g.stdin.close()
    elif event == "self":
        if relay == "stand":
            open(go, "wb").close()
        elif relay_pid:
            try:
                os.kill(relay_pid, signal.SIGKILL)
            except ProcessLookupError:
                notes.append("the relay was already gone at the SIGKILL")
    elif event == "self_term":
        if relay_pid:
            try:
                os.kill(relay_pid, signal.SIGTERM)
            except ProcessLookupError:
                notes.append("the relay was already gone at the SIGTERM")
    try:
        code = g.wait(15)
    except subprocess.TimeoutExpired:
        g.kill(); g.wait()
        code = "TIMEOUT(killed)"
    dt = time.time() - t_ev
    if event != "eoi":
        try:
            g.stdin.close()
        except Exception:
            pass
    rg = None
    if relay_pid:
        t0 = time.time()
        while time.time() - t0 < 3 and not gone(relay_pid):
            time.sleep(0.02)
        rg = gone(relay_pid)
        if not rg:
            st = state(relay_pid)
            try:
                os.kill(relay_pid, signal.SIGKILL)
                notes.append(f"RELAY LEFT RUNNING (pid {relay_pid}, stat {st}); killed by this script")
            except ProcessLookupError:
                rg = f"True (stat {st!r} at 3 s, gone at the kill)"
    late = b""
    if r is not None:
        t0 = time.time()
        while time.time() - t0 < 5:
            rr, _, _ = select.select([r], [], [], 0.2)
            if rr:
                c = os.read(r, 65536)
                if not c:
                    break
                late += c
        os.close(r)
        errtxt = early + late
        errs = re.sub(rb"reaped in \d+ ms", b"reaped in <n> ms", errtxt)
        errshow = repr(errs)
    else:
        errshow = "(reader closed)" if not fd2_closed else "(fd 2 closed)"
        if early:
            notes.append(f"bytes read before the close: {early!r}")
    try:
        g.stdout.close()
    except Exception:
        pass
    print(f"{LABEL} | {name} | exit {code} | {dt:.2f}s | relay gone: {rg} | stderr {errshow}"
          + (f" | {'; '.join(notes)}" if notes else ""), flush=True)


S = [
    # the four cases, each relay
    ("real eoi reader-closed", "real", "eoi", {}),
    ("real eoi reader-kept", "real", "eoi", {"err_close": "never"}),
    ("real self(SIGKILL) reader-closed", "real", "self", {}),
    ("real self(SIGKILL) reader-kept", "real", "self", {"err_close": "never"}),
    ("real self(SIGTERM) reader-closed", "real", "self_term", {}),
    ("real self(SIGTERM) reader-kept", "real", "self_term", {"err_close": "never"}),
    ("stand eoi reader-closed", "stand", "eoi", {}),
    ("stand eoi reader-kept", "stand", "eoi", {"err_close": "never"}),
    ("stand self(3) reader-closed", "stand", "self", {}),
    ("stand self(3) reader-kept", "stand", "self", {"err_close": "never"}),
]
for rel in ("real", "stand"):
    sev = "self"
    S += [
        (f"H1 {rel} reader closed before the frame, eoi", rel, "eoi", {"err_close": "before_frame"}),
        (f"H1 {rel} reader closed before the frame, self", rel, sev, {"err_close": "before_frame"}),
        (f"H2 {rel} reader closed right after the pid line, eoi", rel, "eoi", {"err_close": "after_pid"}),
        (f"H2 {rel} reader closed right after the pid line, self", rel, sev, {"err_close": "after_pid"}),
        (f"H3 {rel} reader closed in the same instant as eoi", rel, "eoi", {"err_close": "with_eof"}),
        (f"H4 {rel} stdout+stderr readers closed after pid, eoi", rel, "eoi", {"out_close": "after_pid"}),
        (f"H4 {rel} stdout+stderr readers closed after pid, self", rel, sev, {"out_close": "after_pid"}),
        (f"H4b {rel} stdout closed after pid, stderr kept, eoi", rel, "eoi", {"out_close": "after_pid", "err_close": "never"}),
        (f"H5 {rel} fd 2 closed altogether, eoi", rel, "eoi", {"fd2_closed": True, "err_close": "never"}),
        (f"H5 {rel} fd 2 closed altogether, self", rel, sev, {"fd2_closed": True, "err_close": "never"}),
        (f"H6 {rel} SIGPIPE ignored, reader closed, eoi", rel, "eoi", {"sigpipe": "ignored"}),
        (f"H6 {rel} SIGPIPE ignored, reader closed, self", rel, sev, {"sigpipe": "ignored"}),
        (f"H6 {rel} SIGPIPE ignored, reader kept, eoi", rel, "eoi", {"sigpipe": "ignored", "err_close": "never"}),
        (f"P1 {rel} stdout closed BEFORE the pid line, stderr kept, eoi", rel, "eoi", {"out_close": "before_pid", "err_close": "never"}),
        (f"P1 {rel} stdout closed BEFORE the pid line, stderr closed, eoi", rel, "eoi", {"out_close": "before_pid"}),
    ]
only = os.environ.get("QA_ONLY")
for name, rel, ev, kw in S:
    if only and not re.search(only, name):
        continue
    case(name, rel, ev, **kw)
left = "\n".join(l for l in subprocess.run(["/usr/bin/pgrep", "-fl", WORK + "|" + BIN], capture_output=True, text=True).stdout.splitlines() if not l.startswith(str(os.getpid()) + " "))
print(f"{LABEL} | processes of this run left: {left or 'none'}")
