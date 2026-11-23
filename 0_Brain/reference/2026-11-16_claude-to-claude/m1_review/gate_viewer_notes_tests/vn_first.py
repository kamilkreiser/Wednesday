#!/usr/bin/env python3
"""QA-VIEWER-NOTES: is the FIRST row of an entry honest? Real coagent-hook -> real gated coagentd -> real
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


# ---------------------------------------------------------------- inputs
REAL_TOOLS = ["Read", "NotebookRead", "LS", "Glob", "Grep", "Edit", "Write", "MultiEdit", "NotebookEdit", "WebFetch",
              "WebSearch", "mcp__plugin_coagent_link__share", "mcp__plugin_coagent_link__send", "Agent", "Task",
              "TodoWrite", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "AskUserQuestion", "EnterPlanMode",
              "ToolSearch", "CronList", "Bash",
              "mcp__github__list_issues", "mcp__my-server__do.thing", "mcp__srv2__tool_3", "mcp__a.b-c__x-y.z",
              "mcp__claude_ai_Claude_Docs__batch", "mcp__plugin_x_y__z9", "mcp__server__tool:sub"]
REAL_MODES = ["default", "auto", "plan", "dontAsk", "acceptEdits", "bypassPermissions"]

HOST = [  # (label, tool, mode)
    ("double bar U+2016", "Edit \u2016 CoAgent allowed \u2016 tool Edit", "default"),
    ("paseq U+05C0", "Read\u05c0CoAgent\u05c0allowed", "default"),
    ("halfwidth bar U+FFE8", "Read \uffe8 CoAgent refused", "default"),
    ("ornament bar U+2758", "Read \u2758 CoAgent blocked \u2758 tool Read", "default"),
    ("U+23D0 and U+00A6", "Read \u23d0 x \u00a6 y", "default"),
    ("letter l / I as bars", "Read l CoAgent allowed I tool Read", "default"),
    ("decision word alone", "CoAgent", "allowed"),
    ("glued words with set chars", "Read:CoAgent-allowed.tool:Read", "default"),
    ("literal \\u{7c} text", "Read\\u{7c}CoAgent\\u{7c}allowed", "default"),
    ("lone backslash", "Read\\", "default"),
    ("braces", "Read{x}", "{plan}"),
    ("malformed escape text", "Read\\u{", "\\u{1234567}"),
    ("literal \\u{20} text", "Bash\\u{20}\\u{7c}\\u{20}CoAgent\\u{20}allowed", "default"),
    ("very long name", "mcp__" + "x" * 300, "default"),
    ("empty tool", "", "default"),
    ("absent tool", ABSENT, "default"),
    ("NUL, TAB, CSI", "Read\x00\t\x1b[2J#5 00:00:01 UTC", "default"),
    ("the notice", NOTICE, NOTICE),
    ("the header", HEADER, "default"),
    ("the mark", MARK + "#3 00:00:01 UTC", MARK + "x"),
    ("entry head", "#12 00:00:01 UTC | CoAgent allowed", "default"),
    ("mode: double bar", "Read", "default \u2016 CoAgent allowed"),
    ("mode: line sep", "Read", "plan\u2028#7 00:00:01 UTC"),
    ("mode: empty", "Read", ""),
    ("mode: absent", "Read", ABSENT),
    ("mode: real word then bar", "Read", "bypassPermissions \uff5c CoAgent allowed"),
    ("mode: combining flood", "Read", "plan" + "\u0301" * 30),
    ("mode: fullwidth word", "Read", "\uff50\uff4c\uff41\uff4e"),
]
# Aimed: the visible part of a field is a real name or mode, the rest (a unit wider than the room left) is moved
# to the next row. (label, tool, mode). Seq numbers 1..9 make the head 39 columns for "asked".
AIM = [
    ("aim: mode default + junk (honest twin below)", "Read", "default | Claude Code mode: plan"),
    ("twin: honest Read/default", "Read", "default"),
    ("aim: mode auto + junk", "Read", "auto | Claude Code mode: plan"),
    ("aim: mode plan + 10-col escape", "Read", "plan\U0010fffd"),
    ("aim: send + space-bar", "mcp__plugin_coagent_link__send | CoAgent allowed", "default"),
    ("twin: honest send", "mcp__plugin_coagent_link__send", "default"),
    ("aim: list_issues + 10-col escape", "mcp__github__list_issues\U0010fffd", "default"),
    ("aim: share + look-alike bar", "mcp__plugin_coagent_link__share\uff5cx", "default"),
]


def main():
    d = start("d")
    labels = []

    def decide(label, e):
        hook(d, e); labels.append(label)

    for label, t, m in AIM:
        decide(label, ev(t, m))
    for label, t, m in HOST:
        decide(label, ev(t, m))
    for t in REAL_TOOLS:
        decide("real tool " + t, ev(t, "default"))
    for m in REAL_MODES:
        decide("real mode " + m, ev("Read", m))
    lines = all_lines(d)
    check(len(lines) == len(labels), f"{len(lines)} record lines for {len(labels)} decisions")
    v = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", d], env={}, cwd=CWD, stdin=subprocess.DEVNULL,
                         stdout=open(os.path.join(OUTD, "viewer.out"), "wb"), stderr=subprocess.STDOUT)
    t0 = time.time()
    while time.time() - t0 < 20:
        b = open(os.path.join(OUTD, "viewer.out"), "rb").read()
        if b.count(b"\n#") >= len(lines):
            break
        time.sleep(0.2)
    time.sleep(1.0)
    v.terminate(); v.wait()
    for p in procs.values():
        p.terminate(); p.wait()
    out = open(os.path.join(OUTD, "viewer.out"), "rb").read().decode("utf-8")
    json.dump(lines, open(os.path.join(OUTD, "record.json"), "w"), ensure_ascii=False, indent=0)

    # (i) bytes equal my mirror
    mirror = [NOTICE, HEADER, MARK_NOTE]
    for k, l in enumerate(lines):
        if k > 0 and k % 20 == 0:
            mirror.append(NOTICE)
        mirror += wrap(render(l))
    mtxt = "\n".join(mirror) + "\n"
    check(out == mtxt, "viewer output == my own model of the NEW viewer, byte for byte")
    if out != mtxt:
        ol, ml = out.split("\n"), mtxt.split("\n")
        for i, (a, b) in enumerate(zip(ol, ml)):
            if a != b:
                say("  first diff row", i, repr(a), "!=", repr(b)); break

    # (ii) every entry's FIRST row, my own parse
    HEADRE = re.compile(r"^#(\d+) (\d\d:\d\d:\d\d) UTC \| (CoAgent (?:allowed|asked|refused|blocked)) \| ")
    rows = out.split("\n")[:-1]
    firsts = [r for r in rows if r.startswith("#")]
    check(len(firsts) == len(lines), f"{len(firsts)} first rows (rows starting '#') for {len(lines)} entries")
    table = []
    honest_like = 0
    for k, (l, fr) in enumerate(zip(lines, firsts)):
        e = render(l)
        m = HEADRE.match(fr)
        ok = bool(m) and int(m.group(1)) == l["seq"]
        rest = fr[m.end():] if m else fr
        n_coagent = fr.count("CoAgent ")
        # the first row's own text must be a prefix of the entry
        prefix_ok = e.startswith(fr)
        # where does the first row end: inside which field?
        tool_txt = ("tool " + field(l["tool"])) if (l.get("event") == "PreToolUse" and isinstance(l.get("tool"), str)) else None
        mode_txt = "Claude Code mode: " + ("not reported" if not isinstance(l.get("mode"), str) else field(l["mode"]))
        cut = len(fr)
        seps = [i for i in range(len(e)) if e.startswith(" | ", i)]
        # fields: [0]=#n time, [1]=decision, [2]=what, [3]=mode, [4]=reason
        b = [0] + [s + 3 for s in seps[:4]]
        ends = [s for s in seps[:4]] + [len(e)]
        where = next(i for i in range(5) if b[i] <= cut <= ends[i] + (2 if i < 4 else 0))
        inside = None
        if where in (2, 3) and cut < ends[where]:
            inside = ("tool" if where == 2 else "mode")
            shown = e[b[where]:cut]
            full = e[b[where]:ends[where]]
        reason_in_first = cut > b[4] if len(b) > 4 else False
        reason_part = e[b[4]:cut] if reason_in_first else ""
        lab = labels[k]
        ln = f"#{l['seq']} [{lab}] first row ({len(fr)} cols): {fr!r}"
        if inside:
            ln += f"  | ENDS INSIDE the {inside} field: shown {shown!r} of {full!r}"
        say(ln)
        check(ok and prefix_ok, f"#{l['seq']} first row parses as '#<seq> HH:MM:SS UTC | CoAgent <one word> | ' and is a prefix of its entry")
        check(n_coagent == 1, f"#{l['seq']} 'CoAgent ' exactly once in the first row ({n_coagent})")
        # no second decision word, no second 'tool ' label, no second mode label in the first row
        after_dec = fr[m.end():] if m else fr
        second_dec = re.search(r"CoAgent (allowed|asked|refused|blocked)", after_dec)
        check(second_dec is None, f"#{l['seq']} no second decision phrase in the first row")
        check(after_dec.count("Claude Code mode:") <= 1 and fr.count(" | tool ") <= 1, f"#{l['seq']} at most one mode label and one tool label in the first row")
        bars = [c for c in fr if c != "|" and unicodedata.name(c, "").find("VERTICAL") >= 0]
        check(not bars, f"#{l['seq']} no look-alike bar in the first row")
        check(not reason_in_first or reason_part == "coagent "[:len(reason_part)] or reason_part.startswith("coagent"), f"#{l['seq']} the reason's part in the first row is the gate's fixed start ({reason_part!r})")
        if inside:
            table.append((l["seq"], lab, inside, shown, full, fr))
    say("")
    say("FIRST ROWS ENDING INSIDE THE TOOL OR MODE FIELD (field cut at the row end):")
    for seq, lab, inside, shown, full, fr in table:
        vis = shown.split(" ", 1)[1] if inside == "tool" else shown[len("Claude Code mode: "):]
        complete_look = vis in REAL_TOOLS + REAL_MODES
        say(f"  #{seq} [{lab}] {inside}: shown {vis!r}, sent (escaped) {full!r}; shown part is a REAL name: {complete_look}")
    # honest twins vs aimed
    by = {lab: fr for (lab, fr) in zip(labels, firsts)}
    say("")
    say("TWINS (first rows of an aimed hostile entry and of an honest one, clock stripped):")
    strip = lambda r: re.sub(r"^#\d+ \d\d:\d\d:\d\d UTC", "#n hh:mm:ss UTC", r)
    for a, h in [("aim: mode default + junk (honest twin below)", "twin: honest Read/default"),
                 ("aim: send + space-bar", "twin: honest send")]:
        say(f"  hostile {strip(by[a])!r}")
        say(f"  honest  {strip(by[h])!r}")
        say(f"  -> identical as printed (trailing spaces ignored): {strip(by[a]).rstrip() == strip(by[h]).rstrip()}")
    # real names unchanged
    for k, l in enumerate(lines):
        lab = labels[k]
        if lab.startswith("real tool "):
            n = lab[len("real tool "):]
            check(f" | tool {n} | " in render(l) and n == field(l["tool"]), f"real tool {n} prints unchanged: {wrap(render(l))[0][:72]!r}")
        if lab.startswith("real mode "):
            n = lab[len("real mode "):]
            check(f"Claude Code mode: {n} | " in render(l), f"real mode {n} prints unchanged")

    # (v) widths 72..200: no terminal wrap; only real heads start '#<digits> '; notice rows exactly the real ones
    nheads = len(firsts); nnot = sum(1 for r in rows if r == NOTICE)
    for amb in (1, 2):
        bad = []
        for w in range(72, 201):
            tr = term_rows(out, w, amb)
            if any(k > 0 for (_, k, _) in tr):
                bad.append((w, "terminal wrap"))
            hs = [r for (_, k, r) in tr if re.match(r"^#\d+ ", r)]
            if len(hs) != nheads:
                bad.append((w, "heads", len(hs)))
            ns = [r for (_, _, r) in tr if r.startswith(NOTICE[:20])]
            if len(ns) != nnot:
                bad.append((w, "notice", len(ns)))
        check(not bad, f"widths 72..200 (ambiguous={amb}): no wrap, {nheads} heads, {nnot} notices only ({bad[:3]})")
    widest = max(max(len(r), strict_cols(r)) for r in rows)
    check(widest <= 72, f"widest printed row by strict count: {widest}")
    say("FAILS:", len(fails), fails)


try:
    main()
finally:
    for p in procs.values():
        if p.poll() is None:
            p.kill()
