#!/usr/bin/env python3
"""QA-LOCAL-ACTIVITY item 4: the `activity` IPC command, own requests.
usage: python3 -B ipc_probe.py <bin dir> <root (new)> <out.txt>
Raw socket client (one request per connection, as the daemon's clients do), so oversized answers are measured,
not refused by a client. Nothing is deleted.
"""
import json, os, socket, subprocess, sys, threading, time

BIN, ROOT, OUT = sys.argv[1:4]
os.makedirs(ROOT)
HOME, TMP, WS = (os.path.join(ROOT, x) for x in ("home", "tmp", "w"))
for d in (HOME, TMP, WS, os.path.join(WS, "secret")):
    os.makedirs(d)
WS = os.path.realpath(WS)
ENV = {"PATH": "/usr/bin:/bin", "HOME": HOME, "TMPDIR": TMP}
o = open(OUT, "w")
fails = []
MAX_RESPONSE_LINE = 256 * 1024 * 7 + ((16 * 1024 + 2 * 64 + 32 + 8 * 1024) * 7 + 1024) + 64 * 1024  # limits.rs:75


def say(*a):
    s = " ".join(str(x) for x in a); print(s); o.write(s + "\n"); o.flush()


def check(cond, what):
    say(("PASS " if cond else "FAIL ") + what)
    if not cond:
        fails.append(what)


def raw(d, line, timeout=30):
    s = socket.socket(socket.AF_UNIX); s.settimeout(timeout)
    s.connect(os.path.join(d, "ipc", "daemon.sock"))
    s.sendall(line if isinstance(line, bytes) else line.encode()); buf = b""
    try:
        while not buf.endswith(b"\n"):
            c = s.recv(1 << 20)
            if not c:
                break
            buf += c
    finally:
        s.close()
    return buf


def req(d, cmd, args=None, id_=5, extra=None):
    r = {"v": 1, "id": id_, "cmd": cmd}
    if args is not None:
        r["args"] = args
    if extra:
        r.update(extra)
    b = raw(d, json.dumps(r) + "\n")
    return json.loads(b) if b else None, len(b)


procs = {}


def start(name, gated, idle=300, extra=()):
    d = os.path.join(ROOT, name)
    args = [f"{BIN}/coagentd", "--data-dir", d, "--coagent", f"{BIN}/coagent", "--idle-exit-secs", str(idle), *extra]
    if gated:
        args += ["--gate", "--workspace", WS, "--exclude", "<ws>/secret/**"]
    procs[name] = subprocess.Popen(args, env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                   stderr=open(os.path.join(ROOT, name + ".stderr"), "ab"))
    t0 = time.time()
    while True:
        try:
            if req(d, "status")[0]["ok"]:
                return d
        except Exception:
            pass
        if time.time() - t0 > 15:
            raise SystemExit("not ready")
        time.sleep(0.05)


def stop(name):
    p = procs.pop(name); p.terminate(); p.wait(timeout=20)


def gate(d, ev):
    return req(d, "gate", {"event": ev})[0]


def bash(cmd, sess="qa-s"):
    return {"session_id": sess, "cwd": WS, "hook_event_name": "PreToolUse", "permission_mode": "default",
            "tool_name": "Bash", "tool_input": {"command": cmd}}


def walk(d, after=0):
    """Page like a viewer; return (seqs, pages, first page)."""
    seqs, pages, first, mx = [], 0, None, 0
    while True:
        r, n = req(d, "activity", {"after": after})
        mx = max(mx, n)
        res = r["result"]; pages += 1
        first = first or res
        seqs += [l["seq"] for l in res["lines"]]
        after = res["next"]
        if not res["more"]:
            return seqs, pages, first, mx


def main():
    d = start("h", True)
    # 1. Argument shapes.
    for label, args, extra in [("after absent (args {})", {}, None), ("args absent", None, None), ("args null", None, {"args": None}),
                               ("after 0", {"after": 0}, None), ("after huge u64", {"after": 18446744073709551615}, None),
                               ("after > u64", {"after": 18446744073709551616}, None), ("after 1e30", {"after": 1e30}, None),
                               ("after -1", {"after": -1}, None), ("after string", {"after": "5"}, None), ("after float 1.5", {"after": 1.5}, None),
                               ("after 1.0", {"after": 1.0}, None), ("after null", {"after": None}, None), ("after bool", {"after": True}, None),
                               ("extra field", {"after": 0, "x": 1}, None), ("args array", [0], None), ("args string", "0", None)]:
        r = raw(d, json.dumps({"v": 1, "id": 5, "cmd": "activity", **({"args": args} if args is not None else {}), **(extra or {})}) + "\n")
        say(f"  {label}: {r.decode().strip()[:160]}")
    r, _ = req(d, "activity", {"after": 18446744073709551615})
    check(r["ok"] and r["result"]["lines"] == [] and r["result"]["last"] == 0 and r["result"]["dropped"] == 0, "after=u64::MAX on an empty record: ok, no lines, dropped 0")
    check(req(d, "status")[0]["ok"], "daemon alive after the argument shapes")
    # 2. Decisions, then paging invariants (count bound).
    big = " ".join(f"/tmp/w{i:02d}" + "q" * 1790 for i in range(34))  # ~61 KiB of path words, the gate asks
    v = gate(d, bash("ls " + big))
    say("  large event decision:", v["result"]["decision"], "reason bytes", len(v["result"]["reason"]))
    for i in range(1100):
        gate(d, bash(f"echo n{i}"))
    seqs, pages, first, mx = walk(d)
    check(seqs == list(range(seqs[0], seqs[0] + len(seqs))), f"walk from 0: contiguous ({len(seqs)} lines in {pages} pages)")
    check(len(seqs) == 1000 and seqs[-1] == 1101 and first["dropped"] == 101, f"1101 decided -> 1000 kept, first seq {seqs[0]}, dropped {first['dropped']}")
    check(mx < MAX_RESPONSE_LINE, f"largest answer {mx} < MAX_RESPONSE_LINE {MAX_RESPONSE_LINE}")
    r, _ = req(d, "activity", {"after": 1050})
    check([l["seq"] for l in r["result"]["lines"]] == list(range(1051, 1102)) and r["result"]["dropped"] == 0, "after=1050: 1051..1101, dropped 0")
    r, _ = req(d, "activity", {"after": 1101})
    check(r["result"]["lines"] == [] and r["result"]["next"] == 1101 and not r["result"]["more"], "after=last: empty, next=last, more false")
    r, _ = req(d, "activity", {"after": 5000})
    check(r["result"]["lines"] == [] and r["result"]["last"] == 1101, "after>last: empty, last told")
    # 3. Byte bound: many large reasons.
    for i in range(120):
        gate(d, bash(f"ls n{i} " + big))
    seqs, pages, first, mx = walk(d)
    check(seqs == list(range(seqs[0], seqs[0] + len(seqs))) and seqs[-1] == 1221, f"after 120 large: contiguous, {len(seqs)} kept, first {seqs[0]}, {pages} pages")
    check(first["dropped"] == seqs[0] - 1, f"dropped {first['dropped']} = first kept - 1")
    check(mx < MAX_RESPONSE_LINE, f"largest answer {mx} bytes < {MAX_RESPONSE_LINE}")
    # 4. Burst: 50 threads x 20 activity requests while 200 gate decisions run.
    errs, sizes = [], []

    def burst():
        for _ in range(20):
            try:
                r, n = req(d, "activity", {"after": 0}); sizes.append(n)
                if not r["ok"]:
                    errs.append(r)
            except Exception as e:
                errs.append(repr(e))
    ths = [threading.Thread(target=burst) for _ in range(50)]
    t0 = time.time()
    [t.start() for t in ths]
    gate_res = [gate(d, bash(f"echo burst{i}"))["result"]["decision"] for i in range(200)]
    [t.join() for t in ths]
    say(f"  burst: 1000 activity requests + 200 gate decisions in {time.time()-t0:.1f}s; errors {len(errs)}; max answer {max(sizes)}")
    check(not errs and set(gate_res) == {"ask"}, "burst: no error, every concurrent gate decision answered ask")
    seqs, _, _, _ = walk(d)
    check(seqs[-1] == 1421 and seqs == list(range(seqs[0], 1422)), "after the burst: last 1421, contiguous")
    # 5. Over-long request line and a request split weirdly.
    try:
        b = raw(d, b'{"v":1,"id":5,"cmd":"activity","args":{"after":' + b"0" * 200_000 + b"}}\n")
        say("  200 KB activity request:", b[:160])
    except Exception as e:
        say("  200 KB activity request: connection", repr(e))
    check(req(d, "status")[0]["ok"], "daemon alive after the long request")
    # 6. Read-only: status before/after many activity calls.
    s0 = req(d, "status")[0]["result"]
    for _ in range(50):
        req(d, "activity", {"after": 0})
    s1 = req(d, "status")[0]["result"]
    check(s0 == s1, "status identical before/after 50 activity calls")
    files0 = sorted((f, os.path.getmtime(os.path.join(dp, f))) for dp, _, fs in os.walk(d) for f in fs)
    for _ in range(20):
        req(d, "activity", {"after": 0})
    files1 = sorted((f, os.path.getmtime(os.path.join(dp, f))) for dp, _, fs in os.walk(d) for f in fs)
    check(files0 == files1, f"no file in the data dir created or modified by 20 activity calls ({len(files0)} files)")
    # 7. Restart: the record is empty; a reader ahead sees last < after.
    stop("h"); d = start("h", True)
    r, _ = req(d, "activity", {"after": 1421})
    check(r["result"]["lines"] == [] and r["result"]["last"] == 0, "after a restart: empty record, last 0 < the reader's after")
    stop("h")
    # 8. Gate off.
    d2 = start("off", False)
    r, _ = req(d2, "activity", {"after": 0})
    check(not r["ok"] and r["error"]["code"] == "gate_off", f"no --gate: {json.dumps(r)}")
    stop("off")
    # 9. Idle: a daemon polled only by `activity` exits at its idle limit; one polled by `status` does not.
    for cmd, expect_exit in (("activity", True), ("status", False)):
        d3 = start("idle_" + cmd, True, idle=3)
        t0 = time.time(); exited = None
        while time.time() - t0 < 12:
            if procs["idle_" + cmd].poll() is not None:
                exited = time.time() - t0; break
            try:
                req(d3, cmd, {"after": 0} if cmd == "activity" else None)
            except Exception:
                pass
            time.sleep(0.2)
        say(f"  idle 3 s, polled by {cmd} every 0.2 s: exited after {exited}")
        check((exited is not None) == expect_exit, f"idle with {cmd} polling: {'exits' if expect_exit else 'stays alive'}")
        if procs["idle_" + cmd].poll() is None:
            stop("idle_" + cmd)
        else:
            procs.pop("idle_" + cmd)
    say(f"FAILS: {len(fails)} {fails}")


try:
    main()
finally:
    for n in list(procs):
        try:
            stop(n)
        except Exception:
            procs[n].kill()
