#!/usr/bin/env python3
"""QA-DAEMON-NOTES item 4(d): the tool server, head against the base build, on the SAME head daemon.
Usage: python3 -B qa_mcp.py <head bin dir> <base bin dir> <work dir (new)>
Every well-formed call is sent to the head coagent-mcp and to the base coagent-mcp in turn and the two
answers compared (32-hex ids normalised); every wrong type is sent to the head (and, where the base would
not block, to the base) and the head's answer checked against the fixed text."""
import json, os, queue, re, subprocess, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q

HEAD, BASE = sys.argv[1], sys.argv[2]
q = Q(HEAD, sys.argv[3])
WAIT_T = "coagent: timeout_s must be a whole number from 1 to 300."
SEND_T = "coagent: re and audience must be strings when given."
ARGS_T = "coagent: the tool arguments must be a JSON object."
fail = []
n_same = 0


class Mcp:
    def __init__(self, bindir, data, tag):
        self.p = subprocess.Popen([os.path.join(bindir, "coagent-mcp"), "--data-dir", data], env=q.env(),
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=open(os.path.join(q.root, f"mcp-{tag}.stderr"), "wb"))
        self.q = queue.Queue()
        threading.Thread(target=self._read, daemon=True).start()
        self.id = 0
        r = self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "qa", "version": "0"}})
        assert "result" in r, r
        self.raw(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}))

    def _read(self):
        for l in self.p.stdout:
            self.q.put(l.decode())

    def raw(self, line):
        self.p.stdin.write(line.encode() + b"\n")
        self.p.stdin.flush()

    def lines(self, t):
        out = []
        t0 = time.time()
        while time.time() - t0 < t:
            try:
                out.append(self.q.get(timeout=0.1))
            except queue.Empty:
                pass
        return out

    def rpc(self, method, params, t=30):
        self.id += 1
        self.raw(json.dumps({"jsonrpc": "2.0", "id": self.id, "method": method, "params": params}))
        t0 = time.time()
        while time.time() - t0 < t:
            try:
                v = json.loads(self.q.get(timeout=0.2))
            except queue.Empty:
                continue
            if v.get("id") == self.id:
                return v
        return {"NO ANSWER within": t}

    def call(self, args_present, args, name):
        p = {"name": name}
        if args_present:
            p["arguments"] = args
        return self.rpc("tools/call", p)

    def close(self):
        self.p.stdin.close()
        self.p.wait(10)


def norm(v):
    s = json.dumps(v, sort_keys=True)
    s = re.sub(r"[0-9a-f]{32}", "<ID>", s)
    return re.sub(r'"id": \d+', '"id": <N>', s)


def preload(text):
    r = q.ctl("b", "send", {"kind": "chat", "text": text})
    assert r["ok"] is True, r
    q.until("delivered to a", 30, lambda: _peek_unread() > 0)


def _peek_unread():
    r = q.ctl("a", "inbox_read", {})
    try:
        return len(r["result"].get("messages", []))
    except Exception:
        return 0


def same(label, name, args, present=True, needs_msg=False):
    global n_same
    if needs_msg:
        preload(f"QA-MCP {label}")
    rh = h.call(present, args, name)
    if needs_msg:
        preload(f"QA-MCP {label}")
    rb = b.call(present, args, name)
    ok = norm(rh) == norm(rb)
    n_same += ok
    print(("SAME " if ok else "DIFF ") + f"{label} | head={json.dumps(rh.get('result', rh))[:230]}" + ("" if ok else f" | base={json.dumps(rb.get('result', rb))[:230]}"), flush=True)
    if not ok:
        fail.append("well-formed differs: " + label)


def refused(label, name, args, want, present=True):
    r = h.call(present, args, name)
    res = r.get("result", {})
    txt = (res.get("content") or [{}])[0].get("text")
    ok = res.get("isError") is True and txt == want and "error" not in r
    print(("OK   " if ok else "BAD  ") + f"{label} | head={json.dumps(r.get('result', r))[:200]}", flush=True)
    if not ok:
        fail.append("wrong type: " + label)


try:
    q.start("a")
    q.start("b")
    q.pair("a", "b")
    h = Mcp(HEAD, q.dir("a"), "head")
    b = Mcp(BASE, q.dir("a"), "base")
    th, tb = h.rpc("tools/list", {}), b.rpc("tools/list", {})
    print(("SAME " if norm(th) == norm(tb) else "DIFF ") + "tools/list")
    if norm(th) != norm(tb):
        fail.append("tools/list")
    # --- well-formed calls ---
    same("send chat", "send", {"kind": "chat", "text": "qa1"})
    same("send request", "send", {"kind": "request", "text": "qa2"})
    same("send reply with re", "send", {"kind": "reply", "text": "qa3", "re": "0123456789abcdef0123456789abcdef"})
    for au in ("people", "agent", "both"):
        same(f"send audience {au}", "send", {"kind": "chat", "text": "qa4", "audience": au})
    same("send re null audience null", "send", {"kind": "chat", "text": "qa5", "re": None, "audience": None})
    same("send audience not in enum (string)", "send", {"kind": "chat", "text": "qa6", "audience": "everyone"})
    same("send re empty string", "send", {"kind": "chat", "text": "qa7", "re": ""})
    same("send extra field", "send", {"kind": "chat", "text": "qa8", "x": 1})
    same("send kind bogus", "send", {"kind": "bogus", "text": "qa9"})
    same("send missing kind", "send", {"text": "qa10"})
    same("send missing text", "send", {"kind": "chat"})
    same("send kind number", "send", {"kind": 5, "text": "x"})
    same("send text number", "send", {"kind": "chat", "text": 5})
    same("send missing kind AND re number (required first)", "send", {"text": "x", "re": 5})
    same("send arguments absent", "send", None, present=False)
    same("send arguments null", "send", None)
    same("inbox_read {}", "inbox_read", {})
    same("inbox_read extra field", "inbox_read", {"x": 1})
    same("inbox_read arguments absent", "inbox_read", None, present=False)
    same("inbox_read arguments null", "inbox_read", None)
    same("wait 1 (nothing arrives)", "wait", {"timeout_s": 1})
    same("wait 0 (clamped to 1)", "wait", {"timeout_s": 0})
    same("wait 1 extra field", "wait", {"timeout_s": 1, "x": "y"})
    same("wait null timeout + message (default 110)", "wait", {"timeout_s": None}, needs_msg=True)
    same("wait absent timeout + message", "wait", {}, needs_msg=True)
    same("wait arguments absent + message", "wait", None, present=False, needs_msg=True)
    same("wait 300 + message", "wait", {"timeout_s": 300}, needs_msg=True)
    same("wait 301 + message (clamped)", "wait", {"timeout_s": 301}, needs_msg=True)
    same("wait u64 max + message (clamped)", "wait", {"timeout_s": 18446744073709551615}, needs_msg=True)
    same("unknown tool", "nosuch", {})
    same("unknown tool, non-object args", "nosuch", "x")
    same("empty tool name", "", {})
    # --- wrong types (head) ---
    for bad in ["x", "30", 2.5, 30.0, -1, True, [1], {}, 1e3, -0.0, 18446744073709551616]:
        refused(f"wait timeout_s {json.dumps(bad)}", "wait", {"timeout_s": bad}, WAIT_T)
    for k in ("re", "audience"):
        for bad in [5, [], {"a": 1}, False]:
            refused(f"send {k} {json.dumps(bad)}", "send", {"kind": "chat", "text": "t", k: bad}, SEND_T)
    for bad in ["x", [1], 5, True, []]:
        for name in ("send", "inbox_read", "wait"):
            refused(f"{name} arguments {json.dumps(bad)}", name, bad, ARGS_T)
    # --- the base's answer to two wrong types (the old silent default), with a message preloaded ---
    preload("QA-MCP base-x")
    rb = b.call(True, {"timeout_s": "x"}, "wait")
    print(f"BASE wait 'x' (message preloaded): isError={rb['result'].get('isError')} text starts {json.dumps(rb['result']['content'][0]['text'][:60])}")
    rb = b.call(True, {"kind": "chat", "text": "t", "re": 5}, "send")
    print(f"BASE send re 5: {json.dumps(rb['result'])[:160]}")
    # --- a batch: unanswered by both ---
    batch = json.dumps([{"jsonrpc": "2.0", "id": 900, "method": "ping"}, {"jsonrpc": "2.0", "id": 901, "method": "tools/list"}])
    h.raw(batch); b.raw(batch)
    lh, lb = h.lines(2.0), b.lines(2.0)
    ok = lh == [] and lb == []
    print(("SAME " if ok else "DIFF ") + f"batch: head lines {lh}, base lines {lb}")
    if not ok:
        fail.append("batch")
    # both still answer after the batch
    same("ping-like inbox_read after batch", "inbox_read", {})
    h.close(); b.close()
finally:
    left = q.cleanup()
    print(f"processes left and killed by cleanup: {left}")
print(f"well-formed identical: {n_same}")
print("ALL OK" if not fail else "FAILURES: " + "; ".join(fail))
