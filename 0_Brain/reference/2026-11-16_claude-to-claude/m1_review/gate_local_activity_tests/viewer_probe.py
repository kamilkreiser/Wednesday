#!/usr/bin/env python3
"""QA-LOCAL-ACTIVITY item 5: `coagentd watch` against the real daemon, own hostile inputs.
usage: python3 -B viewer_probe.py <bin dir> <root (new)> <out dir (new)>
"""
import json, os, signal, socket, subprocess, sys, time, unicodedata

BIN, ROOT, OUTD = sys.argv[1:4]
os.makedirs(ROOT); os.makedirs(OUTD)
HOME, TMP, WS, CWD = (os.path.join(ROOT, x) for x in ("home", "tmp", "w", "vcwd"))
for d in (HOME, TMP, WS, CWD, os.path.join(WS, "secret")):
    os.makedirs(d)
WS = os.path.realpath(WS)
ENV = {"PATH": "/usr/bin:/bin", "HOME": HOME, "TMPDIR": TMP}
NOTICE = "Only you see this. Nothing here is sent to the other side."
rep = open(os.path.join(OUTD, "report.txt"), "w")
fails = []
procs = {}


def say(*a):
    s = " ".join(str(x) for x in a); print(s); rep.write(s + "\n"); rep.flush()


def check(c, what):
    say(("PASS " if c else "FAIL ") + what)
    if not c:
        fails.append(what)


def raw(d, line):
    s = socket.socket(socket.AF_UNIX); s.settimeout(30); s.connect(os.path.join(d, "ipc", "daemon.sock"))
    s.sendall(line); buf = b""
    while not buf.endswith(b"\n"):
        c = s.recv(1 << 20)
        if not c:
            break
        buf += c
    s.close(); return json.loads(buf)


def gate(d, ev):
    # raw UTF-8 on the wire, as the hook sends it (serde), not \u escapes
    return raw(d, (json.dumps({"v": 1, "id": 3, "cmd": "gate", "args": {"event": ev}}, ensure_ascii=False) + "\n").encode("utf-8", "surrogatepass"))


def start(name, gated=True):
    d = os.path.join(ROOT, name)
    a = [f"{BIN}/coagentd", "--data-dir", d, "--coagent", f"{BIN}/coagent", "--idle-exit-secs", "300"]
    if gated:
        a += ["--gate", "--workspace", WS, "--exclude", "<ws>/secret/**"]
    procs[name] = subprocess.Popen(a, env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                   stderr=open(os.path.join(ROOT, name + ".stderr"), "ab"))
    t0 = time.time()
    while True:
        try:
            if raw(d, b'{"v":1,"id":1,"cmd":"status"}\n')["ok"]:
                return d
        except Exception:
            pass
        if time.time() - t0 > 15:
            raise SystemExit("not ready")
        time.sleep(0.02)


def viewer(d, name):
    out = open(os.path.join(OUTD, name + ".out"), "wb")
    # stdin is a pipe we fill: the viewer must not read it (checked: it stays unread)
    p = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", d], env={}, cwd=CWD, stdin=subprocess.PIPE,
                         stdout=out, stderr=subprocess.STDOUT)
    p.stdin.write(b"y\n" * 1000); p.stdin.flush()
    return p


def ev(tool, inp, mode="default", sess="v-s"):
    e = {"session_id": sess, "cwd": WS, "hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": inp}
    if mode is not None:
        e["permission_mode"] = mode
    return e


FAKE = "#7 05:00:00 UTC | CoAgent refused | tool Bash | Claude Code mode: default | coagent: a target is on the owner's exclusion list"
HOSTILE = ["\x1b]0;PWNED-TITLE\x07", "\x1b]2;T\x1b\\", "\x1b[2J\x1b[H", "\x1bc", "\x9b2J", "\r" + NOTICE, "\n" + FAKE, "\n" + NOTICE,
           "‮evil‬", "⁦x⁩", "a​b‌c‍d﻿e", " " + FAKE, " x", "\u0085" + FAKE,
           "\x00nul", "\x7fdel", "؜ alm", "᠎ mvs", "\U000e0041tag", "￹anchor"]


def main():
    d = start("h")
    p = viewer(d, "hostile")
    time.sleep(0.8)
    n = 0
    for h in HOSTILE:
        gate(d, ev("T" + h, {"x": 1})); n += 1                           # tool name
        gate(d, ev("Bash", {"command": "ls"}, mode="m" + h)); n += 1       # mode
        gate(d, ev("Bash", {"command": "echo " + h})); n += 1             # reason (command text)
    # whitespace forging under terminal soft wrap (the agent controls the command text)
    pad = " " * 200
    gate(d, ev("Bash", {"command": "echo hi" + pad + FAKE + pad})); n += 1
    gate(d, ev("Bash", {"command": "echo hi" + pad + NOTICE + pad})); n += 1
    # a large reason: many path words of zero-width characters (each shown as 8 bytes)
    words = " ".join("/tmp/" + "​" * 990 for _ in range(40))
    r = gate(d, ev("Bash", {"command": "ls " + words})); n += 1
    say("  large reason event:", r["result"]["decision"], "reason bytes", len(r["result"]["reason"].encode()))
    for i in range(45):
        gate(d, ev("Read", {"file_path": f"{WS}/f{i}"})); n += 1
    time.sleep(1.5)
    leftover = p.stdin  # still open and full
    p.terminate(); p.wait()
    b = open(os.path.join(OUTD, "hostile.out"), "rb").read()
    lines = b.split(b"\n")[:-1]
    bad = [c for c in b if (c < 0x20 and c != 0x0a) or c == 0x7f]
    check(not bad, f"no raw control byte but LF in {len(b)} bytes of viewer output")
    t = b.decode("utf-8")
    inv = sorted({hex(ord(c)) for c in t if unicodedata.category(c) in ("Cf", "Cc", "Zl", "Zp", "Co", "Cs") and c != "\n"})
    check(not inv, f"no format/control/separator character (Cf, Cc, Zl, Zp) in the output: {inv}")
    check(lines[0].decode() == NOTICE, "line 1 is exactly the notice")
    check(lines[1].decode().startswith("CoAgent mode: APPROVE."), "line 2 is the header")
    entries = [i for i, l in enumerate(lines) if l.startswith(b"#")]
    notices = [i for i, l in enumerate(lines) if l == NOTICE.encode()]
    check(len(entries) == n, f"one printed line per decision ({len(entries)} of {n})")
    starts_ok = all(l.startswith(b"#") or l == NOTICE.encode() or i == 1 for i, l in enumerate(lines))
    check(starts_ok, "every line is the notice, the header, or starts with '#<seq>'")
    # notice before entry 21, 41, 61, ...
    exp = [entries[k] - 1 for k in range(20, len(entries), 20)]
    check(notices == [0] + exp, f"notice at line 1 and before every 20 more entries: {notices[:6]}…")
    check(all(lines[i + 1].startswith(b"#") for i in notices[1:]), "each repeated notice is followed by an entry")
    # a NOTICE look-alike can only appear inside an entry line, never at a line start
    fake_starts = [i for i, l in enumerate(lines) if (l.startswith(NOTICE.encode()) and l != NOTICE.encode())]
    check(not fake_starts, "no line starts with the notice text unless it IS the notice")
    seqs = [int(l.split(b" ")[0][1:]) for l in lines if l.startswith(b"#")]
    check(seqs == list(range(1, n + 1)), "printed seq numbers 1..n in order")
    longest = max(len(l) for l in lines)
    say(f"  longest printed line {longest} bytes")
    open(os.path.join(OUTD, "hostile_sample.txt"), "w").write("\n".join(l.decode()[:400] for l in lines[:12]))
    # soft wrap simulation: where does the forged text land at common widths?
    for l in lines:
        s = l.decode()
        if "echo hi" in s and (FAKE in s or NOTICE in s):
            for w in (80, 100, 120, 160, 200):
                rows = [s[i:i + w] for i in range(0, len(s), w)]
                hit = [r for r in rows if r.lstrip(" ").startswith(("#7 05:00:00", NOTICE))]
                if hit:
                    say(f"  soft wrap at {w} columns: a row reads {hit[0].strip()[:90]!r}")
    # files: the viewer's cwd and HOME/TMP stay empty
    check(os.listdir(CWD) == [] and os.listdir(HOME) == [] and os.listdir(TMP) == [], "viewer cwd, HOME, TMPDIR empty")
    # gate off
    d2 = start("off", gated=False)
    q = subprocess.run([f"{BIN}/coagentd", "watch", "--data-dir", d2], env={}, capture_output=True, timeout=20)
    say("  gate off:", q.returncode, q.stdout.decode().strip())
    check(q.returncode == 3 and q.stdout.decode().count("\n") == 1, "gate off: one line, exit 3")
    procs.pop("off").terminate()
    # daemon absent
    t0 = time.time()
    q = subprocess.run([f"{BIN}/coagentd", "watch", "--data-dir", os.path.join(ROOT, "nobody")], env={}, capture_output=True, timeout=20)
    say(f"  no daemon: exit {q.returncode} after {time.time()-t0:.2f}s: {q.stdout.decode().strip()!r} stderr {q.stderr.decode().strip()!r}")
    check(q.returncode == 1 and "not running" in q.stdout.decode(), "no daemon: says so, exit 1")
    # SIGSTOP'd daemon (socket accepts, never answers): bound
    d3 = start("hung")
    pv = viewer(d3, "hung"); time.sleep(1.0)
    os.kill(procs["hung"].pid, signal.SIGSTOP)
    t0 = time.time()
    try:
        pv.wait(timeout=15); el = time.time() - t0
    except subprocess.TimeoutExpired:
        el = None; pv.kill()
    os.kill(procs["hung"].pid, signal.SIGCONT)
    say(f"  daemon stopped with SIGSTOP: viewer exited after {el}, exit {pv.returncode}: {open(os.path.join(OUTD,'hung.out')).read().splitlines()[-1]!r}")
    check(el is not None and el <= 6.5, "a hung daemon is said within GONE_BOUND (6.5 s)")
    procs.pop("hung").terminate()
    # killed while it runs
    pk = viewer(d, "killed"); time.sleep(1.0)
    t0 = time.time(); procs.pop("h").kill()
    pk.wait(timeout=15)
    say(f"  daemon SIGKILLed: viewer exit {pk.returncode} after {time.time()-t0:.2f}s, last line {open(os.path.join(OUTD,'killed.out')).read().splitlines()[-1]!r}")
    check(pk.returncode == 1, "killed daemon: viewer exits 1")
    # restart under the viewer, fast, with MORE decisions than the viewer had seen
    d = start("r")
    for i in range(3):
        gate(d, ev("Read", {"file_path": f"{WS}/old{i}"}))
    pr = viewer(d, "restart"); time.sleep(1.2)              # viewer has seen seq 1..3 (after = 3)
    procs.pop("r").kill()
    d = start("r")                                          # same data dir, new process
    for i in range(6):
        gate(d, ev("Read", {"file_path": f"{WS}/new{i}"}))   # new seq 1..6, before the viewer's next poll
    time.sleep(1.5)
    pr.terminate(); pr.wait()
    out = open(os.path.join(OUTD, "restart.out")).read()
    say("  restart under the viewer, output:\n    " + "\n    ".join(l[:110] for l in out.splitlines()))
    shown_new = [l for l in out.splitlines() if "/new" in l]
    said = "restarted" in out or "stopped" in out
    say(f"  new-daemon lines shown {len(shown_new)} of 6; restart or stop said: {said}")
    procs.pop("r").terminate()
    say(f"FAILS: {len(fails)} {fails}")


try:
    main()
finally:
    for n, p in list(procs.items()):
        try:
            os.kill(p.pid, signal.SIGCONT)
        except Exception:
            pass
        p.kill(); p.wait()
