#!/usr/bin/env python3
"""QA gate driver for `coagent relay --identity-file / --identity-stdin` (M1 RELAY-IDENTITY).

Every relay listens on 127.0.0.1 with an ephemeral port (or a port this script itself just took
from the OS on 127.0.0.1). Every file it makes lives under the scratch root given on the command
line. Prints one line per probe; the caller saves the output.

usage: probe.py <scratch-root> <head-binary> <main-binary> <pin-client-binary> [section ...]
"""
import base64, hashlib, os, pty, random, select, signal, socket, stat, struct, subprocess, sys, time

ROOT, HEAD, MAIN, CLIENT = sys.argv[1:5]
SECTIONS = set(sys.argv[5:]) or {"default", "usage", "file", "modes", "acl", "kill", "blob", "stdin", "pin", "scan"}
HDR = b"coagent-relay-identity v1\n"
ALL_OUTPUT = []   # (label, text) for the key scan
KEYS = []         # every key seen in a blob this run
results = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    results.append(s)


_n = [0]


def fresh_dir(tag, mode=0o700):
    _n[0] += 1
    d = os.path.join(ROOT, "p", f"{os.getpid()}-{_n[0]:04d}-{tag}")
    os.makedirs(d)
    os.chmod(d, mode)
    return d


def env_for(base):
    """cwd, TMPDIR and HOME all inside the scratch root, empty."""
    cwd = os.path.join(base, "cwd"); tmp = os.path.join(base, "tmp"); home = os.path.join(base, "home")
    for d in (cwd, tmp, home):
        os.makedirs(d, exist_ok=True); os.chmod(d, 0o700)
    env = {"PATH": "/usr/bin:/bin", "TMPDIR": tmp + "/", "HOME": home, "LANG": "C"}
    return cwd, env


def listing(d):
    out = []
    for dp, dn, fn in os.walk(d):
        for x in dn + fn:
            out.append(os.path.relpath(os.path.join(dp, x), d))
    return sorted(out)


def split_blob(b):
    h = len(HDR)
    cl = struct.unpack(">I", b[h:h + 4])[0]
    cert = b[h + 4:h + 4 + cl]
    k0 = h + 4 + cl
    kl = struct.unpack(">I", b[k0:k0 + 4])[0]
    return cert, b[k0 + 4:k0 + 4 + kl]


def join_blob(cert, key):
    return HDR + struct.pack(">I", len(cert)) + cert + struct.pack(">I", len(key)) + key


def note_key_from_file(p):
    try:
        with open(p, "rb") as f:
            b = f.read()
        if b.startswith(HDR):
            KEYS.append(split_blob(b)[1])
    except Exception:
        pass


def run(binary, args, base=None, stdin=None, stdin_bytes=None, timeout=15, keep_open=False,
        umask=None, label="", lsof=False, hold=0.0):
    """Start the binary; if it prints the stop hint, optionally lsof it, then SIGINT it.
    Returns dict(rc, out, err, started, elapsed, lsof)."""
    if base is None:
        base = fresh_dir("run")
    cwd, env = env_for(base) if not isinstance(base, tuple) else base
    pre = None
    if umask is not None:
        def pre():
            os.umask(umask)
    stdin_arg = subprocess.DEVNULL if stdin is None and stdin_bytes is None else (subprocess.PIPE if stdin_bytes is not None else stdin)
    t0 = time.monotonic()
    p = subprocess.Popen([binary] + args, cwd=cwd, env=env, stdin=stdin_arg, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, preexec_fn=pre)
    if stdin_bytes is not None:
        try:
            p.stdin.write(stdin_bytes)
            p.stdin.flush()
            if not keep_open:
                p.stdin.close()
        except BrokenPipeError:
            pass
    out = b""; err = b""; started = False; lsof_txt = ""
    fds = {p.stdout.fileno(): "o", p.stderr.fileno(): "e"}
    deadline = t0 + timeout
    while fds and time.monotonic() < deadline:
        r, _, _ = select.select(list(fds), [], [], 0.05)
        for fd in r:
            chunk = os.read(fd, 65536)
            if not chunk:
                del fds[fd]; continue
            if fds[fd] == "o":
                out += chunk
            else:
                err += chunk
        if not started and b"Press Ctrl-C" in out:
            started = True
            if hold:
                time.sleep(hold)
            if lsof:
                lsof_txt = subprocess.run(["/usr/sbin/lsof", "-n", "-P", "-p", str(p.pid)], capture_output=True, text=True).stdout
            if not keep_open:
                p.send_signal(signal.SIGINT)
        if p.poll() is not None and not fds:
            break
    if p.poll() is None:
        p.send_signal(signal.SIGINT)
        try:
            p.wait(5)
        except subprocess.TimeoutExpired:
            p.kill(); p.wait()
    # drain
    for fd, k in list(fds.items()):
        try:
            while True:
                c = os.read(fd, 65536)
                if not c:
                    break
                if k == "o":
                    out += c
                else:
                    err += c
        except OSError:
            pass
    if stdin_bytes is not None and keep_open:
        try:
            p.stdin.close()
        except Exception:
            pass
    el = time.monotonic() - t0
    o = out.decode(errors="replace"); e = err.decode(errors="replace")
    ALL_OUTPUT.append((label or " ".join(args), o + "\n" + e))
    return {"rc": p.returncode, "out": o, "err": e, "started": started, "elapsed": el, "lsof": lsof_txt,
            "listened": ("url: " in o) or ("relay listening" in e)}


def fp_of(out):
    for l in out.splitlines():
        if l.startswith("fingerprint: "):
            return l.split()[1]
    return None


def url_of(out):
    for l in out.splitlines():
        if l.startswith("url: "):
            return l.split()[1]
    return None


def prefixes(out):
    ps = []
    for l in out.splitlines():
        if l.startswith(" ") or not l.strip():
            continue
        ps.append(l.split(":")[0] if ":" in l[:30] else l[:20])
    return ps


def fstate(p):
    st = os.lstat(p)
    with open(p, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    return (h, oct(st.st_mode), st.st_mtime_ns, st.st_ino, st.st_uid, st.st_nlink)


def short(r):
    msg = [l for l in r["err"].splitlines() if l.startswith("coagent relay:")]
    return f"rc={r['rc']} listened={r['listened']} t={r['elapsed']:.2f}s msg={msg[:1]}"


def file_id_line(r):
    return [l for l in r["out"].splitlines() if l.startswith("identity:")]


def make_identity(d, name="relay.identity"):
    """Use the head binary itself to create a valid identity file at d/name; return (path, fp)."""
    p = os.path.join(d, name)
    r = run(HEAD, ["--listen", "127.0.0.1:0", "relay", "--identity-file", p][2:] if False else ["relay", "--identity-file", p], label="make")
    assert r["started"], r
    note_key_from_file(p)
    return p, fp_of(r["out"])

