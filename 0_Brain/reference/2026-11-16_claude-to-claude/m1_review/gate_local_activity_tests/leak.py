#!/usr/bin/env python3
"""QA-LOCAL-ACTIVITY leak test: A (gated) joins B (ungated, hosts the relay), A decides many MARKED events of
every outcome, then fixed traffic both ways; afterwards every marker is searched as bytes everywhere the
daemons can put anything. Own markers, own events.

usage: python3 -B leak.py <bin dir> <root (new)> <out dir (new)> <mode>
mode: control       same steps and timings, no marked decisions
      decide        marked decisions
      decide-viewer marked decisions while `coagentd watch` runs
      decide-poller marked decisions while a second local client calls `activity` in a loop
Nothing is deleted; the caller moves the root aside.
"""
import json, os, re, secrets, subprocess, sys, threading, time

BIN, ROOT, OUTD, MODE = sys.argv[1:5]
DECIDE = MODE != "control"
os.makedirs(ROOT); os.makedirs(OUTD)
HOME, TMP, WS = (os.path.join(ROOT, x) for x in ("home", "tmp", "w"))
for d in (HOME, TMP, WS, os.path.join(WS, "secret"), os.path.join(WS, "src")):
    os.makedirs(d)
WS = os.path.realpath(WS)
open(os.path.join(WS, "src", "a.rs"), "w").write("fn a(){}")
A, B = os.path.join(ROOT, "a"), os.path.join(ROOT, "b")
ENV = {"PATH": "/usr/bin:/bin", "HOME": HOME, "TMPDIR": TMP}
procs, log = {}, open(os.path.join(OUTD, "steps.jsonl"), "w")
TAG = "QLAMK" + secrets.token_hex(3)
markers = []


def mk(where):
    m = f"{TAG}{len(markers):03d}{where}"
    markers.append(m)
    return m


def rec(**kw):
    log.write(json.dumps(kw, sort_keys=True) + "\n"); log.flush()


def ctl(d, cmd, args=None):
    p = subprocess.run([f"{BIN}/coagentd", "ctl", "--data-dir", d,
                        json.dumps({"v": 1, "id": 7, "cmd": cmd, "args": args or {}})], env={}, capture_output=True, timeout=60)
    try:
        return json.loads(p.stdout)
    except Exception:
        return {"raw": p.stdout.decode("utf-8", "replace")}


def start(name, d, gated):
    args = [f"{BIN}/coagentd", "--data-dir", d, "--coagent", f"{BIN}/coagent", "--idle-exit-secs", "300"]
    if gated:
        args += ["--gate", "--workspace", WS, "--exclude", "<ws>/secret/**"]
    procs[name] = subprocess.Popen(args, env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                   stderr=open(os.path.join(ROOT, f"{name}.stderr"), "ab"))
    t0 = time.time()
    while ctl(d, "status").get("ok") is not True:
        if time.time() - t0 > 15:
            raise SystemExit("not ready " + name)
        time.sleep(0.05)


def stop(name):
    p = procs.pop(name); p.terminate(); p.wait(timeout=20)


def until(what, f, t=60):
    t0 = time.time()
    while not f():
        if time.time() - t0 > t:
            raise SystemExit("timeout: " + what)
        time.sleep(0.1)


def hook(ev=None, raw=None):
    stdin = raw if raw is not None else json.dumps(ev).encode()
    p = subprocess.run([f"{BIN}/coagent-hook", "--data-dir", A], env={"PATH": "/usr/bin:/bin"}, input=stdin,
                       capture_output=True, timeout=30)
    with open(os.path.join(OUTD, "hook_outputs.txt"), "ab") as f:   # the agent's side: outside the root
        f.write(p.stdout + p.stderr + b"\n")
    try:
        j = json.loads(p.stdout); return j.get("hookSpecificOutput", {}).get("permissionDecision") or j.get("decision")
    except Exception:
        return f"exit{p.returncode}"


def pre(sess, tool, inp, mode="default"):
    e = {"session_id": sess, "transcript_path": os.path.join(WS, "t.jsonl"), "cwd": WS, "hook_event_name": "PreToolUse",
         "tool_name": tool, "tool_input": inp, "tool_use_id": "tu-x"}
    if mode is not None:
        e["permission_mode"] = mode
    return e


def marked_events():
    E = []
    for i in range(3):
        s = "s-" + mk("session")
        E += [pre(s, "Bash", {"command": f"echo {mk('cmd')} && cat {WS}/{mk('cmdpath')}", "description": mk("desc")}, mode="auto"),
              pre(s, "Write", {"file_path": f"{WS}/{mk('writepath')}.txt", "content": mk("content")}),
              pre(s, "Read", {"file_path": f"{WS}/secret/{mk('excluded')}"}),
              pre(s, "Edit", {"file_path": f"{WS}/src/a.rs", "old_string": mk("old"), "new_string": mk("new")}),
              pre(s, "WebFetch", {"url": f"https://{mk('host').lower()}.example/{mk('url')}", "prompt": mk("prompt")}),
              pre(s, mk("tool"), {"x": mk("unknowninput")}),
              pre(s, "Bash", {"command": "ls"}, mode=mk("mode")),
              pre(s, "Bash", {"command": f"cat {WS}/secret/{mk('denycmd')}"}),
              pre(s, "mcp__plugin_coagent_link__send", {"kind": "chat", "text": mk("sendtext")}),
              {"session_id": s, "hook_event_name": "ConfigChange", "source": "project_settings", "file_path": f"{WS}/{mk('cfgpath')}"},
              {"session_id": s, "hook_event_name": "Stop", "x": mk("stopfield")},
              {"session_id": s, "hook_event_name": "PreToolUse", "tool_name": mk("unreadable")},
              ]
    return E


bg_stop = threading.Event()


def viewer():
    with open(os.path.join(OUTD, "viewer.out"), "wb") as o:
        p = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", A], env={}, stdin=subprocess.DEVNULL, stdout=o,
                             stderr=subprocess.STDOUT)
        bg_stop.wait(); p.terminate(); p.wait()


def poller():
    n, after = 0, 0
    with open(os.path.join(OUTD, "poller.out"), "w") as o:
        while not bg_stop.is_set():
            r = ctl(A, "activity", {"after": after})
            o.write(json.dumps(r) + "\n"); n += 1
            after = r.get("result", {}).get("next", after)
    rec(step="poller requests", n=n)


def main():
    start("b", B, False); start("a", A, True)
    inv = ctl(B, "invite")
    rec(step="join", ok=ctl(A, "join", {"blob": inv["result"]["line"]}).get("ok"))
    until("connected", lambda: all(ctl(d, "status").get("result", {}).get("session", {}).get("connected") for d in (A, B)))
    time.sleep(1)
    sa0, sb0 = ctl(A, "status")["result"]["session"], ctl(B, "status")["result"]["session"]
    th = None
    if MODE == "decide-viewer":
        th = threading.Thread(target=viewer); th.start()
    if MODE == "decide-poller":
        th = threading.Thread(target=poller); th.start()
    t0 = time.time()
    counts = {}
    if DECIDE:
        for e in marked_events():
            d = hook(e); counts[d] = counts.get(d, 0) + 1
        for raw in (b"{" + mk("rawjson").encode(), b'{"hook_event_name":"PreToolUse","tool_name":"' + mk("raw2").encode() + b'\xff"}'):
            d = hook(raw=raw); counts[d] = counts.get(d, 0) + 1
    rec(step="decisions while paired", counts=counts, secs=round(time.time() - t0, 2))
    time.sleep(max(0, 12 - (time.time() - t0)))   # the phase lasts 12 s in every mode
    sa1, sb1 = ctl(A, "status")["result"]["session"], ctl(B, "status")["result"]["session"]
    keys = ("outbox", "send_next", "recv_upto", "unread", "unread_bytes", "unknown_frames", "stale_frames", "reconnects",
            "gaps", "refused", "relay_refused", "lost_outbound", "lost_inbound")
    rec(step="counters before/after decisions", A0={k: sa0.get(k) for k in keys}, A1={k: sa1.get(k) for k in keys},
        B0={k: sb0.get(k) for k in keys}, B1={k: sb1.get(k) for k in keys})
    # Fixed traffic, the same in every mode.
    rec(step="A send", ok=ctl(A, "send", {"kind": "chat", "text": "qa fixed text A to B"}).get("ok"))
    rec(step="B send", ok=ctl(B, "send", {"kind": "request", "text": "qa fixed text B to A"}).get("ok"))
    until("B has 1", lambda: ctl(B, "status")["result"]["session"]["unread"] == 1)
    until("A has 1", lambda: ctl(A, "status")["result"]["session"]["unread"] == 1)
    r = ctl(B, "inbox_read"); open(os.path.join(OUTD, "b_inbox.json"), "w").write(json.dumps(r))
    ctl(B, "inbox_ack", {"upto": r["result"]["ack"]})
    st = "s-taint-fixed"
    rec(step="taint witness", d=hook(pre(st, "mcp__plugin_coagent_link__inbox_read", {})))
    r = ctl(A, "inbox_read"); rec(step="A inbox_read", ok=r.get("ok"))
    ctl(A, "inbox_ack", {"upto": r["result"]["ack"]})
    time.sleep(2)
    for d, n in ((A, "a"), (B, "b")):
        open(os.path.join(OUTD, f"{n}_status_paired.json"), "w").write(json.dumps(ctl(d, "status")))
    rec(step="A end", ok=ctl(A, "end").get("ok"))
    time.sleep(2)
    if DECIDE:   # after the link closed: the allows (tainted session, T0) and more, for disk and log
        c2 = {}
        for e in [pre(st, "Grep", {"pattern": mk("allowgrep"), "path": f"{WS}/src"}),
                  pre(st, "Glob", {"pattern": mk("allowglob"), "path": f"{WS}/src"}),
                  pre(st, "Read", {"file_path": f"{WS}/src/a.rs", "offset": 1}, mode=mk("allowmode")),
                  pre(st, "Bash", {"command": "echo " + mk("closedcmd")})]:
            d = hook(e); c2[d] = c2.get(d, 0) + 1
        rec(step="decisions after the link closed", counts=c2)
    time.sleep(1)
    act = ctl(A, "activity", {"after": 0})
    rec(step="activity lines kept", n=len(act.get("result", {}).get("lines", [])), last=act.get("result", {}).get("last"))
    # MCP server of A: every listing it offers.
    reqs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "qa", "version": "0"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "resources/list"},
            {"jsonrpc": "2.0", "id": 4, "method": "prompts/list"},
            {"jsonrpc": "2.0", "id": 5, "method": "resources/templates/list"}]
    p = subprocess.run([f"{BIN}/coagent-mcp", "--data-dir", A], env={"PATH": "/usr/bin:/bin"}, capture_output=True, timeout=30,
                       input=("\n".join(json.dumps(x) for x in reqs) + "\n").encode())
    open(os.path.join(OUTD, "mcp.out"), "wb").write(p.stdout + b"\n--stderr--\n" + p.stderr)
    bg_stop.set()
    if th:
        th.join()
    stop("a"); time.sleep(2)
    open(os.path.join(OUTD, "b_status_end.json"), "w").write(json.dumps(ctl(B, "status")))
    stop("b")


try:
    main()
finally:
    bg_stop.set()
    for n in list(procs):
        try:
            stop(n)
        except Exception:
            procs[n].kill()
    json.dump(markers, open(os.path.join(OUTD, "markers.json"), "w"))
    # The search: every file under the root (both data dirs, both stderr files, HOME, TMPDIR, the workspace) and the
    # peer-side outputs, as bytes. The agent-side and owner-side outputs are listed separately (they SHOULD hold markers).
    own = {"hook_outputs.txt", "viewer.out", "poller.out", "markers.json", "steps.jsonl", "search.txt"}
    hits, nfiles = [], 0
    targets = [os.path.join(dp, f) for dp, _, fs in os.walk(ROOT) for f in fs]
    targets += [os.path.join(OUTD, f) for f in os.listdir(OUTD) if f not in own]
    pat = re.compile(re.escape(TAG).encode(), re.I)
    for t in targets:
        if os.path.islink(t) or not os.path.isfile(t):
            continue
        nfiles += 1
        b = open(t, "rb").read()
        for m in pat.finditer(b):
            hits.append(f"{t}: {b[max(0, m.start()-40):m.end()+20]!r}")
    own_hits = {f: open(os.path.join(OUTD, f), "rb").read().count(TAG.encode()) for f in own if os.path.exists(os.path.join(OUTD, f))}
    with open(os.path.join(OUTD, "search.txt"), "w") as o:
        o.write(f"mode={MODE} tag={TAG} markers={len(markers)} files searched={nfiles} hits={len(hits)}\n")
        o.write("\n".join(hits) + "\n")
        o.write(f"owner/agent side outputs (expected to hold markers): {own_hits}\n")
        o.write("files searched:\n" + "\n".join(t for t in targets) + "\n")
    print(open(os.path.join(OUTD, "search.txt")).read().split("files searched:")[0])
