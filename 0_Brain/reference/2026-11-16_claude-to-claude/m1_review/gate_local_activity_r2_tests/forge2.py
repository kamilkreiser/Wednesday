#!/usr/bin/env python3
"""QA-LOCAL-ACTIVITY-R2: attack the viewer's hard wrap. Real coagent-hook -> real coagentd (gated) -> real
`coagentd watch`. Every decision goes through the REAL hook binary. The viewer's bytes are then rendered as a
terminal of each width would show them (own model: East Asian width; W/F = 2 columns, ambiguous = 1 and, in a
second pass, 2; combining marks 0) and the rules of the R2 brief, section 3, are asserted by program.

usage: python3 -B forge2.py <bin dir> <root (new, short)> <out dir (new)>
"""
import json, os, re, signal, socket, subprocess, sys, time, unicodedata

BIN, ROOT, OUTD = sys.argv[1:4]
os.makedirs(ROOT); os.makedirs(OUTD)
HOME, TMP, WS, CWD = (os.path.join(ROOT, x) for x in ("home", "tmp", "w", "vcwd"))
for d in (HOME, TMP, WS, CWD, os.path.join(WS, "secret")):
    os.makedirs(d)
WS = os.path.realpath(WS)
ENV = {"PATH": "/usr/bin:/bin", "HOME": HOME, "TMPDIR": TMP}
NOTICE = "Only you see this. Nothing here is sent to the other side."
HEADER = "CoAgent mode: APPROVE. One entry per call the gate decided. Times: UTC."
MARK = "    | "
MARK_NOTE = 'A row starting with four spaces and "| " continues the entry above.'
WIDTH = 72
FIXED = ["coagentd watch: the daemon restarted; the lines before it are gone",
         "coagentd watch: the daemon stopped; nothing more will be shown",
         "coagentd watch: the daemon does not answer (5 s); nothing more will be shown",
         "coagentd watch: the daemon is not running (nothing answers on its socket)"]
DROPPED = re.compile(r"^\d+ older lines dropped$")
HEAD = re.compile(r"^#\d+ ")
rep = open(os.path.join(OUTD, "report.txt"), "w")
fails = []
procs = {}


def say(*a):
    s = " ".join(str(x) for x in a); print(s); rep.write(s + "\n"); rep.flush()


def check(c, what):
    say(("PASS " if c else "FAIL ") + what)
    if not c:
        fails.append(what)


# ---------------------------------------------------------------- daemon, hook, viewer
def raw(d, line):
    s = socket.socket(socket.AF_UNIX); s.settimeout(30); s.connect(os.path.join(d, "ipc", "daemon.sock"))
    s.sendall(line); buf = b""
    while not buf.endswith(b"\n"):
        c = s.recv(1 << 20)
        if not c:
            break
        buf += c
    s.close(); return json.loads(buf)


def start(name, d=None):
    d = d or os.path.join(ROOT, name)
    a = [f"{BIN}/coagentd", "--data-dir", d, "--coagent", f"{BIN}/coagent", "--idle-exit-secs", "600",
         "--gate", "--workspace", WS, "--exclude", "<ws>/secret/**"]
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
    """The REAL hook binary decides the event (it asks the daemon's gate). Returns (exit, decision, reason)."""
    p = subprocess.run([f"{BIN}/coagent-hook", "--data-dir", d], env={"PATH": "/usr/bin:/bin"},
                       input=json.dumps(ev, ensure_ascii=False).encode("utf-8", "surrogatepass"),
                       capture_output=True, timeout=30)
    try:
        o = json.loads(p.stdout)
    except Exception:
        return p.returncode, None, p.stdout.decode(errors="replace")
    h = o.get("hookSpecificOutput", {})
    return p.returncode, h.get("permissionDecision", o.get("decision")), h.get("permissionDecisionReason", o.get("reason"))


def ev(tool, inp, mode="default", sess="r2-s", event="PreToolUse"):
    e = {"session_id": sess, "cwd": WS, "hook_event_name": event, "tool_name": tool, "tool_input": inp}
    if mode is not None:
        e["permission_mode"] = mode
    return e


def viewer(d, name):
    out = open(os.path.join(OUTD, name + ".out"), "wb")
    p = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", d], env={}, cwd=CWD, stdin=subprocess.DEVNULL,
                         stdout=out, stderr=subprocess.STDOUT)
    return p


def all_lines(d):
    out, after = [], 0
    while True:
        r = raw(d, (json.dumps({"v": 1, "id": 1, "cmd": "activity", "args": {"after": after}}) + "\n").encode())["result"]
        out += r["lines"]; after = r["next"]
        if not r["more"]:
            return out, r


# ---------------------------------------------------------------- mirror of watch.rs render + wrap
INVIS = [(0x00AD, 0x00AD), (0x034F, 0x034F), (0x061C, 0x061C), (0x115F, 0x1160), (0x17B4, 0x17B5), (0x180B, 0x180F),
         (0x200B, 0x200F), (0x2028, 0x202E), (0x2060, 0x206F), (0x3164, 0x3164), (0xFE00, 0xFE0F), (0xFEFF, 0xFEFF),
         (0xFFA0, 0xFFA0), (0xFFF0, 0xFFFB), (0x1BCA0, 0x1BCA3), (0x1D173, 0x1D17A), (0xE0000, 0xE0FFF)]


def invisible(c):
    u = ord(c); return any(a <= u <= b for a, b in INVIS)


def guard(s):
    o = []
    for c in s:
        if " " <= c <= "~":
            o.append(c)
        elif c == "\\":
            o.append("\\\\")
        elif unicodedata.category(c) == "Cc" or invisible(c):
            o.append("\\u{%x}" % ord(c))
        else:
            o.append(c)
    return "".join(o)


def field(s):
    return guard(s).replace("|", "\\u{7c}")


WORDS = {"allow": "CoAgent allowed", "ask": "CoAgent asked", "deny": "CoAgent refused", "block": "CoAgent blocked"}


def render(l):
    sv = lambda k: l.get(k) if isinstance(l.get(k), str) else None
    seq = l.get("seq") if isinstance(l.get("seq"), int) and l.get("seq") >= 0 else 0
    at = l.get("at_ms") if isinstance(l.get("at_ms"), int) and l.get("at_ms") >= 0 else 0
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


def wrap(entry):
    rows, row, used = [], "", 0
    for c in entry:
        w = bcols(c)
        if used + w > WIDTH:
            rows.append(row); row = MARK; used = len(MARK)
        row += c; used += w
    rows.append(row)
    return rows


# ---------------------------------------------------------------- terminal model
def tcols(c, amb):
    if unicodedata.combining(c) or unicodedata.category(c) in ("Mn", "Me"):
        return 0
    ea = unicodedata.east_asian_width(c)
    if ea in ("W", "F"):
        return 2
    if ea == "A":
        return amb
    return 1


def strict_cols(s):
    """A count stricter than a terminal's: W, F and A count 2; a combining mark counts 1 (a terminal that does not
    combine it); everything else 1."""
    n = 0
    for c in s:
        ea = unicodedata.east_asian_width(c)
        n += 2 if ea in ("W", "F", "A") else 1
    return n


def term_rows(text, width, amb):
    """(printed line index, wrap index, row text) as a terminal of `width` columns shows `text` (autowrap on: a
    character that does not fit starts the next row; a wide one at the last column moves whole)."""
    out = []
    for i, line in enumerate(text.split("\n")[:-1] if text.endswith("\n") else text.split("\n")):
        col, k, row = 0, 0, ""
        for c in line:
            w = tcols(c, amb)
            if col + w > width:
                out.append((i, k, row)); k += 1; row = ""; col = 0
            row += c; col += w
        out.append((i, k, row))
    return out


# ---------------------------------------------------------------- forges
def bash_prefix(d):
    """The entry text before a Bash command, learned from one harmless call (as the agent can compute it)."""
    code, dec, reason = hook(d, ev("Bash", {"command": "echo PROBE"}))
    lines, _ = all_lines(d)
    e = render(lines[-1])
    return e[: e.index("echo PROBE")], e[e.index("echo PROBE") + len("echo PROBE"):]


def place(prefix_len_cols, head, fill, target_row, target_col, seqdigits_delta=0):
    """Number of fill characters so that the text after `head`+fill starts at printed row `target_row` (0-based,
    >=1 for continuation rows), printed column `target_col`. Works in the viewer's own (builder's) columns."""
    for k in range(0, 4000):
        e = "x" * prefix_len_cols + head + fill * k + "~"
        rows = wrap(e)
        for r_i, r in enumerate(rows):
            if "~" in r:
                if r_i >= target_row and sum(bcols(c) for c in r[: r.index("~")]) == target_col:
                    return k
                break
    raise SystemExit(f"cannot place at row {target_row} col {target_col}")


def aim(decide_fn, d, build, fill, target_row, target_col, label, tries=6):
    """Decide build(k) for growing k until the forged text (marked by build's returned needle) starts at a printed
    row >= target_row, printed column target_col (builder columns), measured on the REAL record line."""
    k = 0
    for t in range(tries):
        cmd, needle = build(k)
        decide_fn(label + (f" (try {t+1})" if t else ""), ev("Bash", {"command": cmd}), cmd)
        lines, _ = all_lines(d)
        rows = wrap(render(lines[-1]))
        for r_i, r in enumerate(rows):
            if needle in r and r_i >= target_row:
                col = sum(bcols(c) for c in r[: r.index(needle)])
                if col == target_col:
                    return True
                break
        # where does the needle start in the whole entry, in builder columns, and where should it be?
        e = render(lines[-1]); pos_ch = e.index(needle)
        # step one fill char at a time towards the target, using the mirror offline
        for k2 in range(k, k + 400):
            cmd2, nd2 = build(k2)
            e2 = e.replace(cmd if cmd in e else "\0", cmd2) if cmd in e else None
            if e2 is None:
                break
            ok = False
            for r_i, r in enumerate(wrap(e2)):
                if nd2 in r:
                    if r_i >= target_row and sum(bcols(c) for c in r[: r.index(nd2)]) == target_col:
                        ok = True
                    break
            if ok:
                k = k2; break
        else:
            k += 1
    return False


def main():
    d = start("h")
    vw = viewer(d, "forge")
    time.sleep(0.8)
    expect = []   # (label, kind, payload) per decision, in order
    pre, post = bash_prefix(d); expect.append(("probe", "cmd", "echo PROBE"))
    say(f"entry text before a Bash command: {len(pre)} characters (seq 1)")

    def decide(label, e, payload=None):
        code, dec, reason = hook(d, e)
        expect.append((label, dec, payload))
        return code, dec, reason

    def fake_head(n):
        return f"#{n} 00:00:01 UTC | CoAgent refused | tool Bash | Claude Code mode: default | coagent: a target is on the owner's exclusion list"

    # 1. the r1 forge, aligned for the old unwrapped line at 80..200 columns
    for w in (80, 100, 120, 160, 200):
        n = len(expect) + 1
        pl = len(pre) + (len(str(n)) - 1)
        head = "echo build ok"; k = (w - (pl + len(head)) % w) % w
        fk = fake_head(n + 1)[:w].ljust(w, "."); nt = NOTICE.ljust(w, ".")
        cmd = head + "." * k + fk + nt + "x"
        decide(f"r1 forge, unwrapped grid {w}", ev("Bash", {"command": cmd}), cmd)
    # 2. aligned to the viewer's OWN grid: forged text starting right after MARK on continuation rows
    aims = []
    for fill, what in (("." , "dots"), (" ", "spaces"), ("é", "two-byte filler"), ("漢", "CJK filler"), ("─", "ambiguous-width filler")):
        def build(k, fill=fill):
            n = len(expect) + 2
            body = fake_head(n)[:WIDTH - len(MARK)]
            nt = NOTICE.ljust(WIDTH - len(MARK), ".")
            return "echo ok" + fill * k + body + nt + MARK + fake_head(n + 1)[:WIDTH - 2 * len(MARK)] + "x", body
        aims.append((what, aim(decide, d, build, fill, 2, len(MARK), f"own grid, {what}: entry head, notice, mark+head right after the mark")))
    # 3. placed at the column where a NARROWER terminal would start a new row
    for tw in (36, 40, 48, 56, 60, 64, 68, 70, 71):
        def build(k):
            n = len(expect) + 2
            fk = fake_head(n)
            return "echo narrow" + "." * k + fk + "x", fk[:12]
        aims.append((f"narrow {tw}", aim(decide, d, build, ".", 2, tw, f"aimed at a {tw}-column terminal")))
    say("aims hit:", aims)
    # 4. width-count attacks: wide, ambiguous, combining, emoji, escapes split at a wrap point, tabs
    tricky = {
        "CJK run": "echo " + "漢字かなカナ한국" * 30,
        "fullwidth ASCII look-alike of an entry head": "echo " + "．" * 20 + "＃３　００：００：０１　ＵＴＣ　｜　ＣｏＡｇｅｎｔ　ｒｅｆｕｓｅｄ",
        "emoji (W) and emoji with VS16 and ZWJ": "echo " + "😀" * 40 + "❤\ufe0f" * 20 + "👩\u200d💻" * 10,
        "regional indicators": "echo " + "🇦🇺" * 40,
        "ambiguous width (box drawing, Greek, ±)": "echo " + "─│┼±αβ§" * 30,
        "combining flood (Zalgo)": "echo e" + "\u0301\u0302\u0303\u0304\u0308" * 40 + "x" * 100,
        "ideographic space U+3000 and braille blank U+2800": "echo " + "\u3000" * 40 + "\u2800" * 40 + NOTICE,
        "escapes straddling wrap points (U+202E, ESC, NUL, DEL, tab)": "echo " + "\u202e\x1b\x00\x7f\t" * 60,
        "long run of one escape (ESC x 900)": "echo " + "\x1b" * 900,
        "backslash text that looks like an escape": "echo " + "\\u{1b}\\u{a}#9 00:00:01 UTC | CoAgent allowed" * 5,
        "CR/LF + forged head": "echo a\r\n" + fake_head(77) + "\n" + NOTICE,
        "U+2028/U+0085 + forged head": "echo a\u2028" + fake_head(78) + "\u0085" + NOTICE,
        "Hangul fillers U+115F U+3164 (escaped)": "echo " + "\u115f\u3164\uffa0" * 20,
        "mark look-alike in text": "echo " + ("    | " * 30) + NOTICE,
    }
    for label, cmd in tricky.items():
        decide("count: " + label, ev("Bash", {"command": cmd}), cmd)
    # 5. paths, URL, tool name, mode (other fields that reach a reason or the head)
    pk = fake_head(90)
    decide("path: Write file_path holding a forged head", ev("Write", {"file_path": f"{WS}/{'.' * 40}{pk}{NOTICE}.txt", "content": "x"}))
    decide("path: Read with CJK and emoji", ev("Read", {"file_path": f"{WS}/漢字/😀/{'ä' * 60}/{pk}"}))
    decide("URL: WebFetch with a forged head and notice", ev("WebFetch", {"url": f"https://example.invalid/{'a' * 50}/{pk}/{NOTICE}", "prompt": NOTICE}))
    decide("Edit old/new strings", ev("Edit", {"file_path": f"{WS}/e.txt", "old_string": pk, "new_string": NOTICE}))
    heads = []
    for tool in ["Bash | CoAgent allowed | tool Read", "Read ｜ CoAgent allowed ｜ tool Read", "Read │ Claude Code mode: plan",
                 "Read ∣ #9 00:00:01 UTC ∣ CoAgent allowed", "Read ǀ CoAgent allowed", "mcp__x__y" + "ｙ" * 40,
                 "T" * 200, NOTICE, "#9 00:00:01 UTC | CoAgent allowed", MARK + "x", "\\u{7c} CoAgent allowed"]:
        decide("tool name: " + tool[:40], ev(tool, {"a": 1})); heads.append(len(expect))
    for mode in ["default ｜ CoAgent allowed", "plan │ #9 00:00:01 UTC │ CoAgent allowed", "auto | CoAgent allowed",
                 "", "x" * 120, "漢" * 40]:
        decide("mode: " + mode[:40], ev("Read", {"file_path": f"{WS}/m.txt"}, mode=mode)); heads.append(len(expect))
    decide("mode absent", ev("Read", {"file_path": f"{WS}/m2.txt"}, mode=None)); heads.append(len(expect))
    decide("mode a number", dict(ev("Read", {"file_path": f"{WS}/m3.txt"}), permission_mode=7)); heads.append(len(expect))
    decide("ConfigChange with a forged path", {"session_id": "r2-s", "cwd": WS, "hook_event_name": "ConfigChange",
                                               "source": "project_settings", "file_path": f"{WS}/{pk}"}); heads.append(len(expect))
    decide("another event (Stop) with fields", {"session_id": "r2-s", "cwd": WS, "hook_event_name": "Stop", "tool_name": pk}); heads.append(len(expect))
    # 6. a big reason (~60 KB of command) between notices, then 25 small ones (notice cadence)
    big = "echo " + ("." * 70 + NOTICE) * 450
    decide("big command (~57 KB)", ev("Bash", {"command": big}), big)
    for i in range(25):
        decide(f"small read {i}", ev("Read", {"file_path": f"{WS}/s{i}"}))
    time.sleep(2.0)
    vw.terminate(); vw.wait()
    lines, last = all_lines(d)
    b = open(os.path.join(OUTD, "forge.out"), "rb").read()
    text = b.decode("utf-8")
    n = len(lines)
    say(f"decisions through the real hook: {len(expect)}; record lines: {n}; viewer output {len(b)} bytes, {text.count(chr(10))} printed rows")
    check(n == len(expect), "every decision is one record line")
    # ---- the viewer prints exactly the mirror of the daemon's answer (so the mirror can be trusted below)
    want = NOTICE + "\n" + HEADER + "\n" + MARK_NOTE + "\n"
    for i, l in enumerate(lines):
        if i > 0 and i % 20 == 0:
            want += NOTICE + "\n"
        want += "\n".join(wrap(render(l))) + "\n"
    check(text == want, "viewer output == own mirror of render+wrap over the daemon's raw answer (byte for byte)")
    if text != want:
        a, z = text.splitlines(), want.splitlines()
        for j, (x, y) in enumerate(zip(a, z)):
            if x != y:
                say(f"  first difference at row {j}: got {x!r} want {y!r}"); break
    # ---- nothing dropped at a wrap point: each entry joined back == the whole entry; reason == the hook's
    printed = text.split("\n")[:-1]
    entries, kinds = [], []
    for r in printed:
        if HEAD.match(r):
            entries.append(r); kinds.append("head")
        elif r.startswith(MARK):
            entries[-1] += r[len(MARK):]; kinds.append("mark")
        elif r == NOTICE:
            kinds.append("notice")
        elif r in (HEADER, MARK_NOTE) or r in FIXED or DROPPED.match(r):
            kinds.append("fixed")
        else:
            kinds.append("OTHER")
    check(kinds.count("OTHER") == 0, f"every printed row is notice/header/mark note/entry head/continuation/fixed line ({kinds.count('OTHER')} other)")
    check(len(entries) == n and all(entries[i] == render(lines[i]) for i in range(n)),
          f"{len(entries)} entries joined back, each equal to the whole entry (reason whole, in order)")
    for i, (label, dec, payload) in enumerate(expect):
        if payload is not None and lines[i]["tool"] == "Bash":
            vis_cmd = "".join("\\\\" if c == "\\" else ("\\u{%x}" % ord(c) if (unicodedata.category(c) == "Cc" or invisible(c)) else c) for c in payload)
            if vis_cmd not in entries[i]:
                fails.append(f"command not shown whole: {label}"); say(f"FAIL command not whole in entry {i+1}: {label}")
    say("PASS (checked) every proposed Bash command appears whole, escaped, inside its own entry" if not any("not shown whole" in f for f in fails) else "")
    # ---- width per printed row
    worst_b = max(sum(bcols(c) for c in r) for r in printed)
    worst_s = max(strict_cols(r) for r in printed)
    worst_t2 = max(sum(tcols(c, 2) for c in r) for r in printed)
    check(worst_b <= WIDTH and worst_s <= WIDTH and worst_t2 <= WIDTH,
          f"widest printed row: builder count {worst_b}, strict count (W/F/A=2, marks=1) {worst_s}, terminal (amb=2) {worst_t2}; all <= {WIDTH}")
    over = [c for r in printed for c in r if not (" " <= c <= "~") and strict_cols(c) > bcols(c)]
    check(not over, "no character counted wider by the strict count than by the builder's")
    # ---- terminal rows at every width 72..200, ambiguous as 1 and as 2
    head_rows = [i for i, k in enumerate(kinds) if k == "head"]
    notice_rows = [i for i, k in enumerate(kinds) if k == "notice"]
    bad_w = []
    for amb in (1, 2):
        for w in range(72, 201):
            rows = term_rows(text, w, amb)
            soft = [x for x in rows if x[1] > 0]
            heads = [i for i, k, r in rows if HEAD.match(r)]
            nots = [i for i, k, r in rows if r.startswith(NOTICE) or r.lstrip().startswith(NOTICE)]
            hdr = [i for i, k, r in rows if r.startswith(HEADER) or r.startswith(MARK_NOTE)]
            ok = (not soft and heads == head_rows and nots == notice_rows and hdr == [1, 2]
                  and all(r == NOTICE or r == HEADER or r == MARK_NOTE or r.startswith(MARK) or (k == 0 and kinds[i] in ("head", "fixed"))
                          for i, k, r in rows))
            if not ok:
                bad_w.append((amb, w, len(soft), soft[:2]))
    check(not bad_w, f"at every width 72..200 (ambiguous 1 and 2): no terminal wrap; the only rows starting '#<n> ' are the {len(head_rows)} real entry heads; the notice rows are exactly the {len(notice_rows)} real ones; header and mark note only at rows 2-3" + (f" BAD: {bad_w[:4]}" if bad_w else ""))
    # ---- first rows: one decision word, one mode, one #seq
    dw = re.compile(r"CoAgent (allowed|asked|refused|blocked|ran|decided)")
    looks = "｜│┃∣ǀ⏐❘￨׀।|"
    firsts = [printed[i] for i in head_rows]
    multi = [(j + 1, f) for j, f in enumerate(firsts) if len(dw.findall(f)) != 1 or f.count("Claude Code mode:") > 1 or len(re.findall(r"#\d+ ", f)) != 1]
    say(f"first rows with more than one decision word / mode label / '#<n> ' (by text): {len(multi)}")
    for j, f in multi:
        say(f"   entry #{j}: {f}")
    lk = [(j + 1, f) for j, f in enumerate(firsts) if any(c in f for c in looks[:-1])]
    say(f"first rows holding a look-alike of '|' (U+FF5C, U+2502, U+2503, U+2223, U+01C0, U+23D0, U+2758, U+FFE8, U+05C0, U+0964): {len(lk)}")
    for j, f in lk:
        say(f"   entry #{j}: {f}")
    # ---- what each forge looks like (first rows of each entry with the label)
    say("\n== the owner's screen, per forge (printed rows) ==")
    pos = 0
    for i, l in enumerate(lines):
        rows = wrap(render(l))
        label = expect[i][0]
        if label.startswith("small read") and label != "small read 0":
            continue
        say(f"-- entry {i+1}: {label}  ({len(rows)} rows)")
        for r in rows[:6]:
            say("   |" + r)
        if len(rows) > 6:
            say(f"   ... {len(rows) - 6} more continuation rows")
    # ---- notice cadence with the big entry
    big_i = [i for i, x in enumerate(expect) if x[0].startswith("big command")][0]
    say(f"\nbig entry #{big_i+1}: {len(wrap(render(lines[big_i])))} rows; notices printed before entries: "
        f"{[sum(1 for k in kinds[:r] if k == 'head') for r in notice_rows]}")
    check([sum(1 for k in kinds[:r] if k == 'head') for r in notice_rows] == [0] + list(range(20, n, 20)),
          "notice first and before entries 21, 41, ... whatever the entries' length")
    gaps = [notice_rows[j + 1] - notice_rows[j] for j in range(len(notice_rows) - 1)]
    say(f"rows between consecutive notices: {gaps}")
    # ---- below 72 columns
    say("\n== narrower terminals (the stated limit) ==")
    for w in list(range(30, 72)):
        rows = term_rows(text, w, 1)
        fake_e = [(i, k, r) for i, k, r in rows if k > 0 and re.match(r"#\d+ \d\d:\d\d:\d\d UTC \| CoAgent", r)]
        fake_h = [(i, k, r) for i, k, r in rows if k > 0 and re.match(r"#\d+ ", r)]
        fake_n = [(i, k, r) for i, k, r in rows if k > 0 and r.startswith(NOTICE[:20])]
        unmarked = [(i, k, r) for i, k, r in rows if k > 0]
        if w in (30, 40, 50, 56, 60, 64, 70, 71) or fake_e:
            say(f"  {w} cols: {len(unmarked)} unmarked wrap rows; rows reading as an entry head '#<n> HH:MM:SS UTC | CoAgent': {len(fake_e)};"
                f" starting '#<n> ': {len(fake_h)}; starting with the notice's first 20 chars: {len(fake_n)}"
                + (f"; e.g. {fake_e[0][2]!r}" if fake_e else (f"; e.g. {fake_h[0][2]!r}" if fake_h else "")))
    procs.pop("h").terminate()
    say(f"\nFAILS: {len(fails)} {fails}")
    json.dump({"lines": lines, "expect": expect}, open(os.path.join(OUTD, "record.json"), "w"), ensure_ascii=False)


try:
    main()
finally:
    for nm, p in list(procs.items()):
        try:
            os.kill(p.pid, signal.SIGCONT)
        except Exception:
            pass
        p.kill(); p.wait()
