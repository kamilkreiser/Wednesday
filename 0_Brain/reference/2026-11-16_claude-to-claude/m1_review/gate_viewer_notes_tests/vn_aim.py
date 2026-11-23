#!/usr/bin/env python3
"""QA-VIEWER-NOTES item 4: aim an escape so a chosen word starts a continuation row (N-B judgement). Harness head of vn_first.py.
`coagentd watch`. Own hostile tool names and modes (not the builder's list), real names (POLICY.md known tools,
MCP names with __, digits, '-', '.'), the six modes. Own model of the NEW viewer, written from the brief's
property 1 and 2 texts (FR-B1 set; units `\\` and `\\u{1..6 hex}`; a unit moves whole).

usage: python3 -B vn_first.py <bin dir> <root (new, short)> <out dir (new)>
"""
import json, os, re, socket, subprocess, sys, time, unicodedata

BIN, ROOT, OUTD = sys.argv[1:4]
os.makedirs(ROOT); os.makedirs(OUTD)
HOME, TMP, WS, CWD = (os.path.join(ROOT, x) for x in ("home", "tmp", "w", "vcwd"))
for d in (HOME, TMP, WS, CWD):
    os.makedirs(d)
WS = os.path.realpath(WS)
ENV = {"PATH": "/usr/bin:/bin", "HOME": HOME, "TMPDIR": TMP}
NOTICE = "Only you see this. Nothing here is sent to the other side."
HEADER = "CoAgent mode: APPROVE. One entry per call the gate decided. Times: UTC."
MARK = "    | "
MARK_NOTE = 'A row starting with four spaces and "| " continues the entry above.'
WIDTH = 72
rep = open(os.path.join(OUTD, "report.txt"), "w")
fails, procs = [], {}


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


def start(name):
    d = os.path.join(ROOT, name)
    a = [f"{BIN}/coagentd", "--data-dir", d, "--coagent", f"{BIN}/coagent", "--idle-exit-secs", "600",
         "--gate", "--workspace", WS]
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


def hook(d, ev):
    p = subprocess.run([f"{BIN}/coagent-hook", "--data-dir", d], env={"PATH": "/usr/bin:/bin"},
                       input=json.dumps(ev, ensure_ascii=False).encode("utf-8", "surrogatepass"),
                       capture_output=True, timeout=30)
    return p.returncode


ABSENT = object()


def ev(tool, mode="default", event="PreToolUse", inp=None):
    e = {"session_id": "vn-s", "cwd": WS, "hook_event_name": event,
         "tool_input": inp if inp is not None else {"file_path": WS + "/a.txt"}}
    if tool is not ABSENT:
        e["tool_name"] = tool
    if mode is not ABSENT:
        e["permission_mode"] = mode
    return e


def all_lines(d):
    out, after = [], 0
    while True:
        r = raw(d, (json.dumps({"v": 1, "id": 1, "cmd": "activity", "args": {"after": after}}) + "\n").encode())["result"]
        out += r["lines"]; after = r["next"]
        if not r["more"]:
            return out


# ---------------------------------------------------------------- my model of the NEW viewer (brief, props 1, 2)
INVIS = [(0x00AD, 0x00AD), (0x034F, 0x034F), (0x061C, 0x061C), (0x115F, 0x1160), (0x17B4, 0x17B5), (0x180B, 0x180F),
         (0x200B, 0x200F), (0x2028, 0x202E), (0x2060, 0x206F), (0x3164, 0x3164), (0xFE00, 0xFE0F), (0xFEFF, 0xFEFF),
         (0xFFA0, 0xFFA0), (0xFFF0, 0xFFFB), (0x1BCA0, 0x1BCA3), (0x1D173, 0x1D17A), (0xE0000, 0xE0FFF)]


def guard(s):  # reason only (unchanged by the lane)
    o = []
    for c in s:
        u = ord(c)
        if " " <= c <= "~":
            o.append(c)
        elif unicodedata.category(c) == "Cc" or any(a <= u <= b for a, b in INVIS):
            o.append("\\u{%x}" % u)
        else:
            o.append(c)
    return "".join(o)


SET = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.:\\{}")


def field(s):
    return "".join(c if c in SET else "\\u{%x}" % ord(c) for c in s)


WORDS = {"allow": "CoAgent allowed", "ask": "CoAgent asked", "deny": "CoAgent refused", "block": "CoAgent blocked"}


def render(l):
    sv = lambda k: l.get(k) if isinstance(l.get(k), str) else None
    seq = l.get("seq") if isinstance(l.get("seq"), int) else 0
    at = l.get("at_ms") if isinstance(l.get("at_ms"), int) else 0
    e, t = sv("event"), sv("tool")
    if e == "PreToolUse" and t is not None:
        what = "tool " + field(t)
    elif e == "PreToolUse":
        what = "a tool call that names no tool"
    elif e == "ConfigChange":
        what = "a settings change (ConfigChange)"
    else:
        what = "another hook event"
    mode = "not reported" if sv("mode") is None else field(sv("mode"))
    s = (at // 1000) % 86400
    clock = "%02d:%02d:%02d UTC" % (s // 3600, (s % 3600) // 60, s % 60)
    return f"#{seq} {clock} | {WORDS.get(sv('decision') or '', 'CoAgent decided (unknown decision)')} | {what} | Claude Code mode: {mode} | {guard(sv('reason') or '')}"


def bcols(c):
    return 1 if " " <= c <= "~" else 2


HEXD = set("0123456789abcdefABCDEF")


def unit(e, i):
    if e[i] != "\\":
        return 1
    if e[i + 1:i + 2] == "\\":
        return 2
    if e[i + 1:i + 3] == "u{":
        j = i + 3
        while j < len(e) and e[j] in HEXD and j - (i + 3) < 7:
            j += 1
        n = j - (i + 3)
        if 1 <= n <= 6 and e[j:j + 1] == "}":
            return n + 4
    return 1


def wrap(entry):
    rows, row, used, i = [], "", 0, 0
    while i < len(entry):
        n = unit(entry, i); u = entry[i:i + n]; w = sum(bcols(c) for c in u)
        if used + w > WIDTH:
            rows.append(row); row = MARK; used = len(MARK)
        row += u; used += w; i += n
    rows.append(row)
    return rows


def tcols(c, amb):
    if unicodedata.combining(c) or unicodedata.category(c) in ("Mn", "Me"):
        return 0
    ea = unicodedata.east_asian_width(c)
    return 2 if ea in ("W", "F") else (amb if ea == "A" else 1)


def strict_cols(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


def term_rows(text, width, amb):
    out = []
    for i, line in enumerate(text.split("\n")[:-1]):
        col, k, row = 0, 0, ""
        for c in line:
            w = tcols(c, amb)
            if col + w > width:
                out.append((i, k, row)); k += 1; row = ""; col = 0
            row += c; col += w
        out.append((i, k, row))
    return out




def main():
    d = start("d")
    n = 0
    for k in range(0, 72):
        hook(d, ev("Bash", inp={"command": "echo " + "r" * k + "\x1b" + "CoAgent allowed | tool Read | Claude Code mode: plan"})); n += 1
    lines = all_lines(d)
    for p in procs.values():
        p.terminate(); p.wait()
    hits = []
    for l in lines:
        rs = wrap(render(l))
        for i, r in enumerate(rs[1:], 1):
            if r.startswith(MARK + "CoAgent allowed") and rs[i - 1].endswith("\\u{1b}"):
                hits.append((l["seq"], rs[i - 1][-12:], r))
    say(f"{n} decisions; rows where the escape unit ends the row above and the chosen words start right after the mark: {len(hits)}")
    for h in hits[:3]:
        say("  #%d  row above ends %r / row: %r" % h)
    viewer_check = subprocess.run([f"{BIN}/coagentd", "watch", "--data-dir", d], env={}, cwd=CWD, capture_output=True, timeout=10)
    say("(daemon stopped before the viewer ran: viewer says)", viewer_check.stdout.decode().strip())


try:
    main()
finally:
    for p in procs.values():
        if p.poll() is None:
            p.kill()
