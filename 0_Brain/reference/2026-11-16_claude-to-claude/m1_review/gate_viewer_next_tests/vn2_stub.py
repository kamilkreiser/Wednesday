#!/usr/bin/env python3
"""QA-VIEWER-NOTES-R2 item 2: the REAL viewer fed by a socket stub (the daemon's activity answer), so that every
decision word and sequence numbers of 1 to 6 digits can be combined with tool and mode values that end at every
column 55..80 (honest, hostile with an escape, hostile with ' | ...'), plus values exactly the room, one shorter, one
longer. Viewer bytes == my model (m2); every entry judged by the reader (m2.reader).
usage: python3 -B vn2_stub.py <bin dir> <root (new, short)> <out dir (new)>"""
import json, os, re, socket, subprocess, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import m2
BIN, ROOT, OUTD = sys.argv[1:4]; os.makedirs(ROOT); os.makedirs(OUTD)
DEC = {"allow": 15, "ask": 13, "deny": 15, "block": 15, "x": len("CoAgent decided (unknown decision)")}
lines, labels = [], []
def add(lab, seq, dec, tool, mode, reason="coagent asks: x (Other, T3); why: a tool the gate has not been taught"):
    lines.append({"seq": seq, "at_ms": 45_296_000, "event": "PreToolUse", "tool": tool, "mode": mode, "decision": dec, "reason": reason}); labels.append(lab)
for dg in range(1, 7):
    seq = int("123456"[:dg])
    for dec, dw in DEC.items():
        head = 1 + dg + 1 + 12 + 3 + dw + 3          # "#<seq> HH:MM:SS UTC | <dec> | "
        for c in range(55, 81):
            L = c - head - 5                          # "tool " + value ends at column c
            if L >= 1:
                base = ("mcp__" + "t" * 80)[:L] if L > 5 else "T" * L
                for kind, suf in (("honest", ""), ("hostile-esc", "\U0010fffd"), ("hostile-bar", " | CoAgent allowed"), ("hostile-cut", " >> x")):
                    add(f"d{dg} {dec} tool {kind} end {c}", seq, dec, base + suf, "default")
            for mode, kind, vis in (("default", "honest", 7), ("default | Claude Code mode: plan", "hostile-bar", 7),
                                    ("plan\U0010fffd", "hostile-esc", 4), ("plan", "honest", 4), ("bypassPermissions", "honest", 17)):
                k = c - head - 5 - 3 - 18 - vis       # tool "T"*k then " | Claude Code mode: " + mode
                if k >= 1:
                    add(f"d{dg} {dec} mode {kind} {mode[:9]!r} end {c}", seq, dec, "T" * k, mode)
        room = 72 - head - 5 - 2                      # a tool value exactly the room on row 1
        for L, tag in ((room, "exact"), (room - 1, "one shorter"), (room + 1, "one longer")):
            add(f"d{dg} {dec} tool {tag} ({L}) honest", seq, dec, ("mcp__" + "t" * 80)[:L], "default")
            add(f"d{dg} {dec} tool {tag} ({L}) hostile", seq, dec, ("mcp__" + "t" * 80)[:L] + "\U0010fffd", "default")
        add(f"d{dg} {dec} twin hostile", seq, dec, "Read", "default | Claude Code mode: plan")
        add(f"d{dg} {dec} twin honest", seq, dec, "Read", "default")
        add(f"d{dg} {dec} absent mode", seq, dec, "Read", None)
        add(f"d{dg} {dec} mode 'not reported' sent", seq, dec, "Read", "not reported")
# the viewer needs increasing sequence numbers within one answer? it prints what it is given; give each its own seq order
for i, l in enumerate(lines):
    l["_order"] = i
d = os.path.join(ROOT, "s"); os.makedirs(os.path.join(d, "ipc")); os.chmod(d, 0o700); os.chmod(os.path.join(d, "ipc"), 0o700)
path = os.path.join(d, "ipc", "daemon.sock")
Lsock = socket.socket(socket.AF_UNIX); Lsock.bind(path); Lsock.listen(16); Lsock.settimeout(0.2)
stop = threading.Event()
send = [{k: v for k, v in l.items() if k != "_order" and not (k == "mode" and v is None)} for l in lines]
PAGE = 200
def serve():
    while not stop.is_set():
        try: c, _ = Lsock.accept()
        except socket.timeout: continue
        f = c.makefile("rb")
        try: req = json.loads(f.readline())
        except Exception: c.close(); continue
        after = req["args"]["after"]           # we use 'after' as an index into our list
        page = send[after:after + PAGE]
        r = {"lines": page, "next": after + len(page), "last": len(send), "dropped": 0, "more": after + len(page) < len(send), "start": "stub"}
        try: c.sendall((json.dumps({"v": 1, "id": 1, "ok": True, "result": r}, ensure_ascii=False) + "\n").encode())
        except OSError: pass
        c.close()
th = threading.Thread(target=serve, daemon=True); th.start()
of = os.path.join(OUTD, "viewer.out")
p = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", d], env={}, stdin=subprocess.DEVNULL, stdout=open(of, "wb"), stderr=subprocess.STDOUT)
t0 = time.time()
while time.time() - t0 < 60:
    if open(of, "rb").read().count(b"\n#") >= len(send): break
    time.sleep(0.3)
time.sleep(1.0); p.terminate(); p.wait(); stop.set(); th.join(); Lsock.close()
out = open(of, "rb").read().decode()
model = m2.screen(send)
print("entries:", len(send), "| viewer == my model byte for byte:", out == model)
if out != model:
    for i, (a, b) in enumerate(zip(out.split("\n"), model.split("\n"))):
        if a != b: print("first diff row", i, repr(a), repr(b)); break
groups, cur = [], None
for r in out.split("\n")[:-1][4:]:
    if r == m2.NOTICE: continue
    if re.match(r"^#\d+ ", r): cur = [r]; groups.append(cur)
    else: cur.append(r)
bad = 0; ends = {}; cutfits = 0
for lab, l, g in zip(labels, send, groups):
    probs, flds = m2.reader(g)
    want = {"tool": m2.field(l["tool"]), "mode": "not reported" if "mode" not in l else m2.field(l["mode"])}
    got = {f[0]: f[1] for f in flds}
    for k, v in want.items():
        if got.get(k) != v: probs.append(f"{k} read {got.get(k)!r} != sent {v!r}")
    fr = g[0]
    if len(re.findall(r"CoAgent (?:allowed|asked|refused|blocked|decided)", fr)) != 1: probs.append("decision phrases != 1")
    e = "CUT" if fr.endswith(" >>") else "' | '" if fr.endswith(" | ") else "' |'" if fr.endswith(" |") else "reason"
    ends[e] = ends.get(e, 0) + 1
    if probs:
        bad += 1
        if bad <= 10: print(f"READER PROBLEM [{lab}] {probs}\n   " + "\n   ".join(g))
    if lab.endswith("twin hostile") or lab.endswith("twin honest") or "exact" in lab or "one longer" in lab or "one shorter" in lab:
        if lab.startswith(("d1 ask", "d2 ask", "d6 ask", "d6 x")): print(f"  [{lab}] {fr!r}")
print("first-row endings:", ends)
print(f"reader problems: {bad} of {len(groups)}; widest row: {max(m2.ucols(r) for r in out.split(chr(10))[:-1])}")
