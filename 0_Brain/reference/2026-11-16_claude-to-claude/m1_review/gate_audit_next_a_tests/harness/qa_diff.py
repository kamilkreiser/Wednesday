#!/usr/bin/env python3
"""QA-AUDIT-NEXT-A (c): the r2 check's qa_diff.py plus full status values, status.audit, and one more audit_seal after the forms.
QA-AUDIT-WIRE task 5: one scripted two-daemon session for one build; every answer recorded.
Usage: python3 -B qa_diff.py <bin dir> <work dir (new)> <out.json> [--audit-a]
(--audit-a: the convener `a` runs with --audit: the switch-ON comparison against the base.)"""
import json, os, socket, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q, keypaths

BIN, ROOT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
AUD = "--audit-a" in sys.argv
q = Q(BIN, ROOT)
rec = []  # (label, value)


def put(label, v):
    rec.append([label, v])


def ctl(who, cmd, args=None, label=None, raw_args=False):
    req = {"v": 1, "id": 7, "cmd": cmd}
    if raw_args or args is not None:
        req["args"] = args
    v = q.ctl_raw(who, req)
    put(label or f"{who} {cmd} {json.dumps(args)}", v)
    return v


def forms(who, tag):
    """audit_seal in every form of the word"""
    for nm, a, present in [("no args", None, False), ("{}", {}, True), ("null", None, True), ("an argument", {"x": 1}, True),
                           ("a wrong type (string)", "s", True), ("a wrong type (list)", [1], True), ("a wrong type (number)", 5, True)]:
        req = {"v": 1, "id": 9, "cmd": "audit_seal"}
        if present:
            req["args"] = a
        put(f"{tag}: {who} audit_seal {nm}", q.ctl_raw(who, req))


def raw_conn(who, tag):
    """two requests on ONE connection: audit_seal, then status: is the connection kept?"""
    path = os.path.join(q.dir(who), "ipc", "daemon.sock")
    s = socket.socket(socket.AF_UNIX)
    s.settimeout(10)
    s.connect(path)
    f = s.makefile("rwb")
    out = []
    for req in ({"v": 1, "id": 1, "cmd": "audit_seal"}, {"v": 1, "id": 2, "cmd": "status"}):
        f.write((json.dumps(req) + "\n").encode())
        f.flush()
        l = f.readline()
        out.append(json.loads(l)["ok"] if l else "CLOSED")
    s.close()
    put(f"{tag}: {who} one connection: audit_seal then status (ok flags)", out)


def keys(who, tag):
    st = q.status(who)
    put(f"{tag}: {who} status key paths", sorted(keypaths(st)))
    put(f"{tag}: {who} status values", st)
    if "audit" in st:
        put(f"{tag}: {who} status.audit", st["audit"])


def listing(tag):
    for who in ("a", "b"):
        out = []
        d = q.dir(who)
        for r, ds, fs in os.walk(d):
            for x in ds + fs:
                out.append(os.path.relpath(os.path.join(r, x), d))
        put(f"{tag}: {who} data folder listing", sorted(out))


def mcp(who, tag):
    p = subprocess.Popen([os.path.join(BIN, "coagent-mcp"), "--data-dir", q.dir(who)], env=q.env(),
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(os.path.join(ROOT, "mcp.stderr"), "ab"))
    lines = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "qa", "version": "0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "send", "arguments": {"kind": "chat", "text": "QAD via mcp"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "inbox_read", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "wait", "arguments": {"timeout_s": 1}}},
    ]
    out = {}
    for l in lines:
        p.stdin.write((json.dumps(l) + "\n").encode())
        p.stdin.flush()
        if "id" in l:
            while True:
                r = p.stdout.readline()
                if not r:
                    break
                v = json.loads(r)
                if v.get("id") == l["id"]:
                    out[l["method"] + ("/" + l["params"]["name"] if l["method"] == "tools/call" else "")] = v
                    break
    p.stdin.close()
    p.wait(10)
    for k, v in out.items():
        put(f"{tag}: {who} mcp {k}", v)


try:
    h = subprocess.run([os.path.join(BIN, "coagentd"), "--help"], capture_output=True, env=q.env())
    put("--help stdout", h.stdout.decode())
    put("--help stderr", h.stderr.decode())
    put("--help rc", h.returncode)
    q.start("a", ["--audit"] if AUD else [])
    q.start("b")
    # ---- idle
    T = "idle"
    for who in ("a", "b"):
        keys(who, T)
    for c, a in [("status", None), ("send", {"kind": "chat", "text": "x"}), ("inbox_read", None), ("inbox_ack", {"upto": 0}),
                 ("wait", {"timeout_s": 1}), ("gate", {"event": {}}), ("activity", {"after": 0}), ("verify_start", None),
                 ("verify_confirm", {"words": "a b c", "matched": True}), ("end", None), ("nope", None)]:
        ctl("a", c, a, label=f"{T}: a {c}")
    forms("a", T)
    raw_conn("a", T)
    listing(T)
    # ---- invited
    T = "invited"
    inv = ctl("a", "invite", {}, label=f"{T}: a invite")
    keys("a", T)
    forms("a", T)
    # ---- paired
    T = "paired"
    ctl("b", "join", {"blob": inv["result"]["line"]}, label=f"{T}: b join")
    q.wait_connected("a", "b")
    for who in ("a", "b"):
        keys(who, T)
    ctl("a", "send", {"kind": "chat", "text": "QAD chat one"}, label=f"{T}: a send chat")
    ctl("a", "send", {"kind": "request", "text": "QAD request two"}, label=f"{T}: a send request")
    ctl("a", "send", {"kind": "nope", "text": "x"}, label=f"{T}: a send bad kind")
    ctl("a", "send", {"kind": "reply", "text": "x"}, label=f"{T}: a send reply without re")
    time.sleep(1.5)
    ib = ctl("b", "inbox_read", label=f"{T}: b inbox_read")
    rid = [m for m in ib["result"]["messages"] if m["type"] == "request.new"][0]
    rid = rid.get("request_id") or rid.get("id")
    ctl("b", "send", {"kind": "reply", "text": "QAD the reply", "re": rid}, label=f"{T}: b send reply")
    ctl("b", "inbox_ack", {"upto": ib["result"]["ack"]}, label=f"{T}: b inbox_ack")
    time.sleep(1.5)
    ctl("a", "inbox_read", label=f"{T}: a inbox_read")
    ctl("a", "wait", {"timeout_s": 1}, label=f"{T}: a wait")
    for c, a in [("gate", {"event": {}}), ("activity", {"after": 0}), ("verify_start", None), ("nope", None)]:
        ctl("a", c, a, label=f"{T}: a {c}")
    forms("a", T)
    ctl("a", "audit_seal", None, label=f"{T}: a audit_seal again (nothing new)")
    keys("a", T + " after seals")
    forms("b", T)
    raw_conn("a", T)
    mcp("a", T)
    time.sleep(1.0)
    ctl("b", "inbox_read", label=f"{T}: b inbox_read after mcp")
    for who in ("a", "b"):
        keys(who, T + " after")
        try:
            put(f"{T}: {who} outbox.json", json.load(open(os.path.join(q.dir(who), "outbox.json"))))
        except Exception as e:
            put(f"{T}: {who} outbox.json", repr(e))
    listing(T)
    # ---- a's state save failed (data folder unwritable): audit_seal in every form
    T = "save failed"
    os.chmod(q.dir("a"), 0o500)
    try:
        ctl("a", "send", {"kind": "chat", "text": "QAD while unsaved"}, label=f"{T}: a send")
        forms("a", T)
        ctl("a", "status", label=f"{T}: a status ok?")
    finally:
        os.chmod(q.dir("a"), 0o700)
    # ---- ended
    T = "ended"
    ctl("a", "end", label=f"{T}: a end")
    time.sleep(1.5)
    for who in ("a", "b"):
        keys(who, T)
    ctl("a", "send", {"kind": "chat", "text": "x"}, label=f"{T}: a send")
    forms("a", T)
    forms("b", T)
    listing(T)
    q.stop("a")
    q.stop("b")
    listing("stopped")
finally:
    put("left processes", q.cleanup())
    json.dump(rec, open(OUT, "w"), indent=0)
    print("records", len(rec), OUT)
