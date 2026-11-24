#!/usr/bin/env python3
"""QA-VIEWER-NOTES-R2 item 4 (the first check's vn_wrap.py with ONLY the model replaced by m2, the header block four rows,
and joins that take off the cut marks a reader sees inside a field; plus hostile tool/mode runs). Original: QA-VIEWER-NOTES item 4: the wrap and escapes. Shared harness head of vn_first.py (same model of the NEW viewer).
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


import sys as _s; _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2
guard, field, render, unit, bcols = m2.guard, m2.field, m2.render, m2.unit, m2.bcols
CUT_NOTE, CUT = m2.CUT_NOTE, m2.CUT


def rows_of(l):
    return m2.rows_of(l)


def join_reader(rs):
    """Join an entry's rows as a READER would from the rows alone: marks off; a row-final ' >>' off ONLY on a row
    that the reader saw end inside a tool or mode field (m2.reader); everything else is text."""
    probs, flds = m2.reader(rs)
    cut_rows = set()
    for want, got, close_row, rows_used, cuts in flds:
        for k in range(close_row - rows_used + 1, close_row):
            cut_rows.add(k)
    parts = []
    for k, r in enumerate(rs):
        b = r if k == 0 else r[len(MARK):]
        if k in cut_rows:
            assert b.endswith(CUT), (k, r)
            b = b[:-len(CUT)]
        parts.append(b)
    return parts, probs


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
    labels, cmds = [], []

    def bash(label, cmd):
        hook(d, ev("Bash", inp={"command": cmd})); labels.append(label); cmds.append(cmd)

    kinds = [("NEL", "\x85"), ("LRI", "\u2066"), ("NUL", "\x00"), ("BOM", "\ufeff"), ("DEL", "\x7f"),
             ("ESC", "\x1b"), ("TAG", "\U000e0041"), ("backslash", "\\")]
    for name, ch in kinds:
        for k in range(12):
            bash(f"{name} run after {k}", "echo " + "p" * k + ch * 25)
    lits = ["\\u{1b}", "\\\\u{1b}", "\\u{zz}", "\\u{}", "\\u{1234567}", "\\u1b", "{}", "\\\\\\", "\\\x1b", "\\u{1b"]
    for s in lits:
        for k in range(0, 12, 3):
            bash(f"literal {s!r} after {k}", "echo " + "q" * k + (s + "Z") * 12 + "\\")
    # aimed: a chosen word right after the mark, behind an escape run (judged as N-B)
    for k in range(10):
        bash(f"aim word after ESC run {k}", "echo " + "r" * (40 + k) + "\x1b" * 3 + "CoAgent allowed | tool Read")
    for k in range(6):
        bash(f"aim head after LRI {k}", "echo " + "s" * (30 + k) + "\u2066" + "#9 00:00:01 UTC | CoAgent refused")
    # tool and mode values with escape runs and literal backslashes straddling the row ends inside the fields
    for k in range(0, 40):
        hook(d, ev("t" * k + "\x1b" * 9 + "\\" * 5 + "x", "p" * (k % 9) + "\u2066" * 6)); labels.append(f"tool/mode escape run {k}"); cmds.append(None)
    # paths with backslashes through Read (the gate's targets text)
    for p in ["a\\u{1b}b", "a\\\\b", "c\\"]:
        hook(d, ev("Read", inp={"file_path": WS + "/" + p})); labels.append(f"Read path {p!r}"); cmds.append(None)
    lines = all_lines(d)
    check(len(lines) == len(labels), f"{len(lines)} record lines for {len(labels)} decisions")
    v = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", d], env={}, cwd=CWD, stdin=subprocess.DEVNULL,
                         stdout=open(os.path.join(OUTD, "viewer.out"), "wb"), stderr=subprocess.STDOUT)
    t0 = time.time()
    while time.time() - t0 < 30:
        b = open(os.path.join(OUTD, "viewer.out"), "rb").read()
        if b.count(b"\n#") >= len(lines):
            break
        time.sleep(0.2)
    time.sleep(1.0); v.terminate(); v.wait()
    for p in procs.values():
        p.terminate(); p.wait()
    out = open(os.path.join(OUTD, "viewer.out"), "rb").read().decode("utf-8")
    json.dump(lines, open(os.path.join(OUTD, "record.json"), "w"), ensure_ascii=False, indent=0)
    mirror, notice_before = [NOTICE, HEADER, MARK_NOTE, CUT_NOTE], []
    for k, l in enumerate(lines):
        if k > 0 and k % 20 == 0:
            mirror.append(NOTICE); notice_before.append(k + 1)
        mirror += rows_of(l)
    mtxt = "\n".join(mirror) + "\n"
    check(out == mtxt, "viewer output == my own model of the NEW viewer, byte for byte")
    rows = out.split("\n")[:-1]
    # classes
    other = [r for r in rows[4:] if not (r == NOTICE or r.startswith(MARK) or re.match(r"^#\d+ \d\d:\d\d:\d\d UTC \| CoAgent ", r))]
    check(not other, f"every row is notice/header/mark line/entry head/continuation ({other[:2]})")
    check(rows[:4] == [NOTICE, HEADER, MARK_NOTE, CUT_NOTE] and rows[4:].count(HEADER) == 0 and rows[4:].count(MARK_NOTE) == 0 and rows[4:].count(CUT_NOTE) == 0,
          "header, mark line and cut line only as rows 2, 3 and 4")
    # entries: split, join back, cuts at unit starts, widths
    ents, cur = [], None
    for r in rows[4:]:
        if r == NOTICE:
            continue
        if r.startswith("#"):
            cur = [r]; ents.append(cur)
        else:
            cur.append(r)
    check(len(ents) == len(lines), f"{len(ents)} entries")
    inside, short, joined_bad, wide, starts_like_esc = [], 0, [], [], []
    for l, rs, lab in zip(lines, ents, labels):
        e = render(l)
        parts, rprobs = join_reader(rs)
        if rprobs:
            joined_bad.append(lab + f" (reader: {rprobs})")
        if "".join(parts) != e:
            joined_bad.append(lab)
        if guard(l.get("reason", "")) not in "".join(parts):
            joined_bad.append(lab + " (reason)")
        st, i = set(), 0
        while i < len(e):
            st.add(i); i += unit(e, i)
        st.add(len(e))
        at = 0
        for p, r in zip(parts, rs):
            at += len(p)
            if at not in st:
                inside.append((lab, at, p[-8:]))
            if max(len(r), strict_cols(r)) > 72:
                wide.append(r)
            if len(r) < 72 and r is not rs[-1]:
                short += 1
        for r in rs[1:]:
            t = r[len(MARK):]
            if re.match(r"^\\u\{[0-9a-f]+\}", t) and lab.startswith("literal"):
                # a continuation row starting with what looks like a real escape: is it one, in the entry's units?
                starts_like_esc.append((lab, t[:20]))
    check(not joined_bad, f"every entry joined back by a reader (marks off, cut marks inside fields off) == its render; every reason whole ({joined_bad[:3]})")
    check(not inside, f"no row ends inside a unit (\\\\ or \\u{{..}}) ({inside[:3]})")
    check(not wide, f"no row wider than 72 by the viewer's and a strict count ({wide[:2]})")
    say(f"rows shorter than 72 that are not an entry's last row (a unit moved whole): {short}")
    say(f"continuation rows of literal-text cases starting like an escape: {len(starts_like_esc)} {starts_like_esc[:6]}")
    # aimed words after the mark
    for r in rows:
        if r.startswith(MARK + "CoAgent allowed") or r.startswith(MARK + "#9 00:00:01"):
            say("AIMED ROW (after the mark):", repr(r))
    # notice cadence
    idx = [i for i, r in enumerate(rows) if r == NOTICE][1:]
    nxt = [int(re.match(r"^#(\d+)", rows[i + 1]).group(1)) for i in idx]
    check(nxt == notice_before, f"notices before entries {nxt} (expected {notice_before})")
    # widths
    nheads = len(ents); nnot = rows.count(NOTICE)
    for amb in (1, 2):
        bad = []
        for w in range(72, 201):
            tr = term_rows(out, w, amb)
            if any(k > 0 for (_, k, _) in tr):
                bad.append((w, "wrap"))
            if len([r for (_, _, r) in tr if re.match(r"^#\d+ ", r)]) != nheads:
                bad.append((w, "heads"))
            if len([r for (_, _, r) in tr if r.startswith(NOTICE[:20])]) != nnot:
                bad.append((w, "notice"))
        check(not bad, f"widths 72..200 amb={amb}: no terminal wrap, {nheads} heads only, {nnot} notices only ({bad[:3]})")
    # the Read paths: how the gate wrote a literal backslash in the target text
    for l, lab in zip(lines, labels):
        if lab.startswith("Read path"):
            say(lab, "->", repr(l["reason"][-60:]))
    say("FAILS:", len(fails), fails)


try:
    main()
finally:
    for p in procs.values():
        if p.poll() is None:
            p.kill()
