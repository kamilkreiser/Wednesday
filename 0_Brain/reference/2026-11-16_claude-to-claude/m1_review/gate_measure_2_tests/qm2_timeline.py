#!/usr/bin/env python3
"""QA-MEASURE-2 own timeline reader (independent of the seat's elicit_read.py).
usage: python3 -I -B qm2_timeline.py <raw case dir>
Merges, by epoch time: mcp.log (elicitation/create out, every elicit-1 response in, its action), keys.log (every line),
cwd.inject.log, cwd.answer.log, hook.stdin.jsonl (event, tool), debug.excerpt.log lines about elicitation/ConfigChange/
settings changes (ISO time -> epoch), and every frame: whether it holds the dialog text M2CONFIRM and the dialog's
checkbox/cursor lines. Prints the merged list, then derived facts."""
import datetime, json, os, re, sys
sys.dont_write_bytecode = True
D = sys.argv[1]
ev = []
def P(p): return os.path.join(D, p)
def jl(p):
    out = []
    if os.path.exists(P(p)):
        for l in open(P(p), encoding="utf-8"):
            l = l.strip()
            if l: out.append(json.loads(l))
    return out
creates, resps = [], []
for m in jl("mcp.log"):
    msg = m.get("msg") if isinstance(m.get("msg"), dict) else {}
    if m["dir"] == "out" and msg.get("method") == "elicitation/create":
        creates.append(m["ts"]); ev.append((m["ts"], "MCP  out elicitation/create id=%s" % msg.get("id")))
    if m["dir"] == "in" and msg.get("id") == "elicit-1" and "method" not in msg:
        a = (msg.get("result") or {}).get("action"); c = (msg.get("result") or {}).get("content")
        resps.append((m["ts"], a)); ev.append((m["ts"], "MCP  in  RESPONSE action=%s content=%s" % (a, json.dumps(c))))
    if m["dir"] == "in" and msg.get("method") == "tools/call":
        ev.append((m["ts"], "MCP  in  tools/call %s" % (msg.get("params") or {}).get("name")))
keys = []
if os.path.exists(P("keys.log")):
    for l in open(P("keys.log"), encoding="utf-8"):
        t, rest = l.rstrip("\n").split(" ", 1); keys.append((float(t), rest)); ev.append((float(t), "KEYS " + rest[:110]))
for name, tag in (("cwd.inject.log", "INJ "), ("cwd.answer.log", "ANS ")):
    if os.path.exists(P(name)):
        for l in open(P(name), encoding="utf-8"):
            l = l.rstrip("\n")
            if tag == "ANS ":
                o = json.loads(l); ev.append((o["t"], "ANS  answer.py ran (stdin %d bytes)" % len(o["stdin"])))
            else:
                m = re.match(r"^(\d+\.\d+) (.*)$", l)
                if m: ev.append((float(m.group(1)), "INJ  " + m.group(2)[:120]))
                else: ev.append((None, "INJ  (no time) " + l[:160]))
for h in jl("hook.stdin.jsonl"):
    e = h["event"]; ev.append((h["t"], "HOOK %s %s %s" % (e.get("hook_event_name"), e.get("tool_name") or "", (json.dumps(e.get("tool_input"))[:90] if e.get("tool_input") else ""))))
DRX = re.compile(r"[Ee]licitation|ConfigChange|Detected change|settings\.local|Hook .*(?:blocked|returned)|with status|Watching for changes")
if os.path.exists(P("debug.excerpt.log")):
    for l in open(P("debug.excerpt.log"), encoding="utf-8"):
        m = re.match(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z (.*)$", l.rstrip("\n"))
        if m and DRX.search(m.group(2)):
            t = datetime.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=datetime.timezone.utc).timestamp()
            ev.append((t, "DBG  " + m.group(2)[:150]))
frames = []
if os.path.exists(P("frames.txt")):
    for blk in open(P("frames.txt"), encoding="utf-8", errors="replace").read().split("=== FRAME t=")[1:]:
        t, body = blk.split("\n", 1); t = float(t)
        has = "M2CONFIRM" in body
        box = [x.strip() for x in body.splitlines() if re.search(r"Switch to ALLOW|Accept\s+Decline|❯", x)]
        frames.append((t, has, box))
        ev.append((t, "FRM  dialog=%s %s" % ("YES" if has else "no ", " | ".join(box)[:150] if has else "")))
ev.sort(key=lambda x: (x[0] is None, x[0] or 0))
for t, s in ev: print("%s  %s" % ("%.3f" % t if t is not None else "   (none)    ", s))
print("\n== derived")
c0 = creates[0] if creates else None
print("elicitation/create count %d, first t=%s" % (len(creates), c0))
rk = [(t, s) for t, s in keys if s.startswith(("KEY", "SAY"))]
after = [(t, s) for t, s in rk if c0 is not None and t > c0]
print("runner keys/says in order: %s" % [(round(t, 3), s[:40]) for t, s in rk])
fk = after[0] if after else None
print("runner's first key/say AFTER create: %s" % (fk,))
for t, a in resps:
    print("response t=%.3f action=%s  +%.3f s after create ; %s runner's first key after create%s" % (
        t, a, t - c0, "BEFORE" if (fk is None or t < fk[0]) else "AFTER", (" (by %.3f s)" % (fk[0] - t)) if fk else ""))
df = [f for f in frames if f[1]]
print("frames %d ; frames with M2CONFIRM %d ; first %s ; last %s" % (len(frames), len(df), df[0][0] if df else None, df[-1][0] if df else None))
if os.path.exists(P("pane.bytes")): print("pane.bytes M2CONFIRM count %d" % open(P("pane.bytes"), "rb").read().count(b"M2CONFIRM"))
if os.path.exists(P("cwd.listing.txt")): print("cwd.listing: %s" % open(P("cwd.listing.txt")).read().split())
