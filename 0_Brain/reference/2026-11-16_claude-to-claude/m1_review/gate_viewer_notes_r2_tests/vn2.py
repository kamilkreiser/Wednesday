#!/usr/bin/env python3
"""QA-VIEWER-NOTES-R2 item 2 (the heart): is an entry's FIRST row honest under addendum 1? Real coagent-hook ->
real gated coagentd -> real `coagentd watch`. My own model (m2.py) must equal the viewer byte for byte; then a
READER (m2.reader) judges every entry's rows by the stated rule only (fourth header line). Inputs: the first check's
twins, aimed cases, hostile list and real names; the cut mark's characters inside tool, mode and command; values that
fill the room exactly, one shorter, one longer; label words; `not reported` literally; a sweep of value end columns
55..80 at sequence numbers of 2 and 3 digits (1 digit: the first entries).

usage: python3 -B vn2.py <bin dir> <root (new, short)> <out dir (new)>
"""
import json, os, re, socket, subprocess, sys, time, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2

BIN, ROOT, OUTD = sys.argv[1:4]
os.makedirs(ROOT); os.makedirs(OUTD)
HOME, TMP, WS, CWD = (os.path.join(ROOT, x) for x in ("home", "tmp", "w", "vcwd"))
for d in (HOME, TMP, WS, CWD):
    os.makedirs(d)
WS = os.path.realpath(WS)
ENV = {"PATH": "/usr/bin:/bin", "HOME": HOME, "TMPDIR": TMP}
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
    a = [f"{BIN}/coagentd", "--data-dir", d, "--coagent", f"{BIN}/coagent", "--idle-exit-secs", "900",
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


REAL_TOOLS = ["Read", "NotebookRead", "LS", "Glob", "Grep", "Edit", "Write", "MultiEdit", "NotebookEdit", "WebFetch",
              "WebSearch", "mcp__plugin_coagent_link__share", "mcp__plugin_coagent_link__send", "Agent", "Task",
              "TodoWrite", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "AskUserQuestion", "EnterPlanMode",
              "ToolSearch", "CronList", "Bash",
              "mcp__github__list_issues", "mcp__my-server__do.thing", "mcp__srv2__tool_3", "mcp__a.b-c__x-y.z",
              "mcp__claude_ai_Claude_Docs__batch", "mcp__plugin_x_y__z9", "mcp__server__tool:sub"]
REAL_MODES = ["default", "auto", "plan", "dontAsk", "acceptEdits", "bypassPermissions"]
TWIN_H, TWIN_O = "default | Claude Code mode: plan", "default"

# (label, tool, mode, event, input)
FIRST = [  # seq 1..9: one digit
    ("twin hostile #1", "Read", TWIN_H),
    ("twin honest #2", "Read", TWIN_O),
    ("aim: mode auto + junk", "Read", "auto | Claude Code mode: plan"),
    ("aim: mode plan + U+10FFFD", "Read", "plan\U0010fffd"),
    ("aim: send + ' | CoAgent allowed'", "mcp__plugin_coagent_link__send | CoAgent allowed", "default"),
    ("twin honest send", "mcp__plugin_coagent_link__send", "default"),
    ("aim: list_issues + U+10FFFD", "mcp__github__list_issues\U0010fffd", "default"),
    ("aim: share + U+FF5C x", "mcp__plugin_coagent_link__share｜x", "default"),
    ("tool LS, mode default (fits on row 1)", "LS", "default"),
]
NOTICE, HEADER, MARK = m2.NOTICE, m2.HEADER, m2.MARK
HOST = [
    ("aim: mode plan + U+2028 + head", "Read", "plan #7 00:00:01 UTC"),
    ("aim: mode plan + 30 combining", "Read", "plan" + "́" * 30),
    ("double bar U+2016", "Edit ‖ CoAgent allowed ‖ tool Edit", "default"),
    ("paseq U+05C0", "Read׀CoAgent׀allowed", "default"),
    ("ornament bar U+2758", "Read ❘ CoAgent blocked ❘ tool Read", "default"),
    ("letter l / I as bars", "Read l CoAgent allowed I tool Read", "default"),
    ("decision word alone", "CoAgent", "allowed"),
    ("glued words with set chars", "Read:CoAgent-allowed.tool:Read", "default"),
    ("literal \\u{7c} text", "Read\\u{7c}CoAgent\\u{7c}allowed", "default"),
    ("lone backslash", "Read\\", "default"),
    ("braces", "Read{x}", "{plan}"),
    ("malformed escape text", "Read\\u{", "\\u{1234567}"),
    ("very long name (300)", "mcp__" + "x" * 295, "default"),
    ("very long name, long mode", "mcp__" + "x" * 295, "mcp__" + "y" * 120),
    ("empty tool", "", "default"),
    ("absent tool", ABSENT, "default"),
    ("empty tool, empty mode", "", ""),
    ("absent tool, absent mode", ABSENT, ABSENT),
    ("NUL, TAB, CSI", "Read\x00\t\x1b[2J#5 00:00:01 UTC", "default"),
    ("the notice", NOTICE, NOTICE),
    ("the header", HEADER, "default"),
    ("the mark", MARK + "#3 00:00:01 UTC", MARK + "x"),
    ("the cut line", m2.CUT_NOTE, m2.CUT_NOTE),
    ("mode: empty", "Read", ""),
    ("mode: absent", "Read", ABSENT),
    ("mode literally 'not reported'", "Read", "not reported"),
    ("mode literally 'not' (fits as 'not |')", "Read", "not"),
    ("mode: real word then bar", "Read", "bypassPermissions ｜ CoAgent allowed"),
    ("mode: fullwidth word", "Read", "ｐｌａｎ"),
    # the cut mark's own characters
    ("tool 'Read >> x', mode 'default >>'", "Read >> x", "default >>"),
    ("tool 'Read >>'", "Read >>", "default"),
    ("tool '>>'", ">>", ">>"),
    ("tool 'Read |', mode 'plan |'", "Read |", "plan |"),
    ("tool 'Read>>' (no space)", "Read>>", "plan>>"),
    ("mode 'defau >>' (looks like a cut)", "Read", "defau >>"),
    ("mode 'defau' + CUT + 'lt'", "Read", "defau >>lt"),
    # label words
    ("tool literally 'tool'", "tool", "default"),
    ("tool 'Claude Code mode: plan'", "Claude Code mode: plan", "default"),
    ("tool 'Claude'", "Claude", "default"),
    ("mode 'Claude Code mode: plan'", "Read", "Claude Code mode: plan"),
    ("mode 'tool Read'", "Read", "tool Read"),
    # other events (the fixed 'what' text) with hostile modes
    ("ConfigChange, mode default+junk", "Read", TWIN_H, "ConfigChange"),
    ("unknown event, empty mode", "Read", "", "UserPromptSubmit"),
]
# the room on row 1 for a tool value at 1 digit with "asked": 72 - 38 - 1 - 2 = 31
for L, tag in ((31, "exactly the room"), (30, "one shorter"), (32, "one longer")):
    HOST.append((f"tool {tag} ({L}) honest", "mcp__" + "t" * (L - 5), "default"))
    HOST.append((f"tool {tag} ({L}) hostile +U+10FFFD", "mcp__" + "t" * (L - 5) + "\U0010fffd", "default"))
# a mode value with tool 'Read': room = 72 - 63 - d - 2  (6 at 1 digit, 5 at 2)
for L in (4, 5, 6, 7, 8):
    HOST.append((f"mode of {L} honest", "Read", "m" * L))
    HOST.append((f"mode of {L} hostile +' | x'", "Read", "m" * L + " | x"))
# commands that put ' >>' / ' |' at a reason row's end (Bash; padding steps the token across the row end)
CMDS = []
for pad in range(0, 70):
    CMDS.append((f"bash: ' >>' at a row end, pad {pad}", "echo " + "a" * pad + " >> /tmp/qvn2-f; cat /etc/hosts | tail -1"))
for pad in range(0, 70):
    CMDS.append((f"bash: 'tool Read |' in a command, pad {pad}", "echo " + "b" * pad + " tool Read | Claude Code mode: default >> x"))
# the raw tool name in the reason, aimed so that a continuation row starts like the honest mode row
AIMR = []
for pad in range(0, 70):
    AIMR.append((f"reason forge of the mode row, pad {pad}", "x" * (pad + 1) + " | Claude Code mode: plan | coagent asks: Read", "default"))


def main():
    d = start("d")
    labels, want = [], []

    def decide(label, tool, mode, event="PreToolUse", inp=None):
        hook(d, ev(tool, mode, event, inp)); labels.append(label)

    for x in FIRST:
        decide(*x)
    for x in HOST:
        decide(*x)
    for t in REAL_TOOLS:
        decide("real tool " + t, t, "default")
    for m in REAL_MODES:
        decide("real mode " + m, "Read", m)
    for lab, cmd in CMDS:
        decide(lab, "Bash", "default", "PreToolUse", {"command": cmd})
    for x in AIMR:
        decide(*x)
    # the twins again at two digits
    decide("twin hostile (2 digits)", "Read", TWIN_H)
    decide("twin honest (2 digits)", "Read", TWIN_O)
    # the sweep: value end columns 55..80 at 2 then 3 digits. head = 33 + d ("asked"); "tool " 5
    def sweep(dg):
        for c in range(55, 81):
            n = len(labels) + 1
            dd = len(str(n))
            # honest tool, hostile tool (esc), hostile tool (bar): tool value ends at column c
            L = c - (33 + dd + 5)
            if L >= 1:
                decide(f"sweep d{dd} tool honest end {c}", ("mcp__" + "t" * 60)[:L] if L > 5 else "T" * L, "plan")
                dd = len(str(len(labels) + 1)); L = c - (33 + dd + 5)
                decide(f"sweep d{dd} tool hostile-esc end {c}", (("mcp__" + "t" * 60)[:L] if L > 5 else "T" * L) + "\U0010fffd", "plan")
                dd = len(str(len(labels) + 1)); L = c - (33 + dd + 5)
                decide(f"sweep d{dd} tool hostile-bar end {c}", (("mcp__" + "t" * 60)[:L] if L > 5 else "T" * L) + " | CoAgent allowed", "plan")
            # modes: end col = 59 + d + k + len(mode); tool "T"*k
            for mode, tag, vis in (("default", "honest", 7), (TWIN_H, "hostile-bar", 7), ("plan\U0010fffd", "hostile-esc", 4),
                                   ("plan", "honest", 4)):
                dd = len(str(len(labels) + 1))
                k = c - (59 + dd + vis)
                if k >= 1:
                    decide(f"sweep d{dd} mode {tag} {mode[:7]!r} end {c}", "T" * k, mode)
    sweep(2)
    while len(labels) < 99:
        decide("pad", "Read", "default")
    sweep(3)
    decide("twin hostile (3 digits)", "Read", TWIN_H)
    decide("twin honest (3 digits)", "Read", TWIN_O)

    lines = all_lines(d)
    check(len(lines) == len(labels), f"{len(lines)} record lines for {len(labels)} decisions")
    check([l["seq"] for l in lines] == list(range(1, len(lines) + 1)), "seq = 1..n in order")
    v = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", d], env={}, cwd=CWD, stdin=subprocess.DEVNULL,
                         stdout=open(os.path.join(OUTD, "viewer.out"), "wb"), stderr=subprocess.STDOUT)
    t0 = time.time()
    while time.time() - t0 < 30:
        b = open(os.path.join(OUTD, "viewer.out"), "rb").read()
        if b.count(b"\n#") >= len(lines):
            break
        time.sleep(0.2)
    time.sleep(1.0)
    v.terminate(); v.wait()
    for p in procs.values():
        p.terminate(); p.wait()
    out = open(os.path.join(OUTD, "viewer.out"), "rb").read().decode("utf-8")
    json.dump({"labels": labels, "lines": lines}, open(os.path.join(OUTD, "record.json"), "w"), ensure_ascii=False, indent=0)

    mtxt = m2.screen(lines)
    check(out == mtxt, "viewer output == my own model (m2) byte for byte")
    if out != mtxt:
        for i, (a, b) in enumerate(zip(out.split("\n"), mtxt.split("\n"))):
            if a != b:
                say("  first diff row", i, repr(a), "!=", repr(b)); break
    rows = out.split("\n")[:-1]
    check(rows[:4] == [m2.NOTICE, m2.HEADER, m2.MARK_NOTE, m2.CUT_NOTE], "rows 1-4 are the notice, header, mark line, cut line")
    # group entries
    groups, cur = [], None
    for r in rows[4:]:
        if r == m2.NOTICE:
            continue
        if re.match(r"^#\d+ ", r):
            cur = [r]; groups.append(cur)
        else:
            check(r.startswith(m2.MARK), f"a row of known kind: {r[:30]!r}") if not r.startswith(m2.MARK) else None
            cur.append(r)
    check(len(groups) == len(lines), f"{len(groups)} entries printed")
    # the reader
    nprob = 0
    table = []
    global FL
    FL = {}
    honest_mode_row2 = honest_total = 0
    for k, (l, g) in enumerate(zip(lines, groups)):
        probs, flds = m2.reader(g)
        lab = labels[k]
        joined = "".join([g[0]] + [r[len(m2.MARK):] for r in g[1:]])
        # the reader's own join: marks off, cut marks off ONLY where the reader saw them inside a field
        if probs:
            nprob += 1
            say(f"READER PROBLEM #{l['seq']} [{lab}]: {probs}\n   " + "\n   ".join(g))
        # what the reader reconstructs must be what was sent (narrowed)
        if l.get("event") == "PreToolUse" and isinstance(l.get("tool"), str):
            tf = [f for f in flds if f[0] == "tool"]
            if not tf or tf[0][1] != m2.field(l["tool"]):
                probs.append("tool value as read != sent"); nprob += 1
        mf = [f for f in flds if f[0] == "mode"]
        want_mode = "not reported" if not isinstance(l.get("mode"), str) else m2.field(l["mode"])
        if not mf or mf[0][1] != want_mode:
            probs.append(f"mode value as read {mf[0][1] if mf else None!r} != sent {want_mode!r}"); nprob += 1
        # first row: decision phrases, ending
        fr = g[0]
        dp = len(re.findall(r"CoAgent (?:allowed|asked|refused|blocked)", fr))
        if dp != 1:
            probs.append(f"{dp} decision phrases in the first row")
        ending = ("CUT" if fr.endswith(m2.CUT) else "' | ' (next field on row 2)" if fr.endswith(" | ") else
                  "' |'" if fr.endswith(" |") else "reason" if " | coag" in fr or fr.endswith(" | c") else "other: " + fr[-12:])
        # the reason's part on the first row (after the mode field's closing)
        mclose = None
        if mf and mf[0][2] == 0:
            pos = fr.find("Claude Code mode: ")
            mclose = fr.find(" |", pos + 18 + len(mf[0][1]) - 1)
        reason_on_first = fr[mclose + 3:] if (mclose is not None and mclose >= 0 and len(fr) > mclose + 3) else ""
        if reason_on_first and not "coagent ".startswith(reason_on_first[:8]) and not reason_on_first.startswith("coagent"):
            probs.append(f"reason text on the first row: {reason_on_first!r}")
        if reason_on_first.endswith(" >>") or reason_on_first.endswith(" |"):
            probs.append("the reason puts ' >>' or ' |' at a first row's end")
        if lab.startswith("real ") or lab.startswith("pad") or "honest" in lab:
            if isinstance(l.get("mode"), str) and l["mode"] in REAL_MODES + ["m" * i for i in range(4, 9)]:
                honest_total += 1
                if mf and mf[0][2] > 0:
                    honest_mode_row2 += 1
        table.append((l["seq"], lab, fr, ending, probs))
        FL[k] = flds
        if probs:
            fails.append(f"#{l['seq']} {probs}")
    check(nprob == 0, f"the READER finds no dishonest row in {len(groups)} entries ({nprob} problems)")
    say("")
    say("FIRST ROWS (seq, label, ending, first row):")
    for seq, lab, fr, ending, probs in table:
        say(f"  #{seq} [{lab}] ends {ending}: {fr!r}" + (f"  PROBLEMS {probs}" if probs else ""))
    say("")
    say(f"honest entries with a real/plain mode: {honest_total}; mode field on row 2 or later: {honest_mode_row2}")
    # real names unchanged
    for k, l in enumerate(lines):
        lab = labels[k]
        if lab.startswith("real tool "):
            n = lab[len("real tool "):]
            tf = [f for f in FL[k] if f[0] == "tool"]
            check(bool(tf) and tf[0][1] == n and tf[0][4] == 0 and any(f"tool {n} |" in r for r in groups[k]),
                  f"real tool {n} prints unchanged, whole with ' |' on one row, no cut mark")
        if lab.startswith("real mode "):
            n = lab[len("real mode "):]
            check(any(f"Claude Code mode: {n} |" in r for r in groups[k]), f"real mode {n} prints unchanged, whole with ' |' on one row")
    # widths 72..200
    nheads = len(groups); nnot = sum(1 for r in rows if r == m2.NOTICE)
    for amb in (1, 2):
        bad = []
        for w in range(72, 201):
            tr = term_rows(out, w, amb)
            if any(k > 0 for (_, k, _) in tr):
                bad.append((w, "terminal wrap"))
            hs = [r for (_, k, r) in tr if re.match(r"^#\d+ ", r)]
            if len(hs) != nheads:
                bad.append((w, "heads", len(hs)))
            ns = [r for (_, _, r) in tr if r.startswith(m2.NOTICE[:20])]
            if len(ns) != nnot:
                bad.append((w, "notice", len(ns)))
            cn = [i for (i, _, r) in tr if r == m2.CUT_NOTE or r.startswith("A tool or mode is whole")]
            if cn != [3]:
                bad.append((w, "cut line", cn))
        check(not bad, f"widths 72..200 (ambiguous={amb}): no wrap, {nheads} heads, {nnot} notices, cut line only row 4 ({bad[:3]})")
    widest = max(max(m2.ucols(r), strict_cols(r)) for r in rows)
    check(widest <= 72, f"widest printed row (viewer count and strict count): {widest}")
    say("FAILS:", len(fails), fails[:40])


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


try:
    main()
finally:
    for p in procs.values():
        if p.poll() is None:
            p.kill()
