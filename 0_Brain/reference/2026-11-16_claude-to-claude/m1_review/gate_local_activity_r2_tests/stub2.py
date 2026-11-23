#!/usr/bin/env python3
"""QA-LOCAL-ACTIVITY-R2 item 2f: something other than the daemon answers on the socket. Cases: raw ESC, CR, LF, C1,
bidi and the notice/an entry head inside every field; an over-long answer line; a wrong sequence (backwards,
repeated, 0, huge); non-string fields; a changing start value; no start; an error code that is not a code.
usage: python3 -B stub2.py <bin dir> <root (new, short)> <out dir (new)>"""
import json, os, re, signal, socket, subprocess, sys, threading, time, unicodedata
BIN, ROOT, OUTD = sys.argv[1:4]
os.makedirs(ROOT); os.makedirs(OUTD)
NOTICE = "Only you see this. Nothing here is sent to the other side."
HEADER = "CoAgent mode: APPROVE. One entry per call the gate decided. Times: UTC."
MARK = "    | "
MARK_NOTE = 'A row starting with four spaces and "| " continues the entry above.'
rep = open(os.path.join(OUTD, "report.txt"), "w")
fails = []


def say(*a):
    s = " ".join(str(x) for x in a); print(s); rep.write(s + "\n"); rep.flush()


def check(c, what):
    say(("PASS " if c else "FAIL ") + what)
    if not c:
        fails.append(what)


def run_stub(name, answers, secs=2.0):
    """answers: function(after, n) -> bytes to send (whole answer, newline included) or None to close."""
    d = os.path.join(ROOT, name)
    os.makedirs(os.path.join(d, "ipc")); os.chmod(d, 0o700); os.chmod(os.path.join(d, "ipc"), 0o700)
    path = os.path.join(d, "ipc", "daemon.sock")
    L = socket.socket(socket.AF_UNIX); L.bind(path); L.listen(16); L.settimeout(0.2)
    stop = threading.Event(); n = [0]; afters = []

    def serve():
        while not stop.is_set():
            try:
                c, _ = L.accept()
            except socket.timeout:
                continue
            f = c.makefile("rb")
            try:
                req = json.loads(f.readline())
            except Exception:
                c.close(); continue
            after = req["args"]["after"]; afters.append(after)
            b = answers(after, n[0]); n[0] += 1
            try:
                if b is not None:
                    c.sendall(b)
            except OSError:
                pass
            c.close()
    th = threading.Thread(target=serve, daemon=True); th.start()
    of = open(os.path.join(OUTD, name + ".out"), "wb")
    p = subprocess.Popen([f"{BIN}/coagentd", "watch", "--data-dir", d], env={}, stdin=subprocess.DEVNULL, stdout=of, stderr=subprocess.STDOUT)
    try:
        rc = p.wait(timeout=secs)
    except subprocess.TimeoutExpired:
        p.terminate(); rc = p.wait()
    stop.set(); th.join(); L.close()
    b = open(os.path.join(OUTD, name + ".out"), "rb").read()
    return rc, b, afters


def ok_answer(lines, nxt, last, start="s1", more=False, dropped=0, extra=None):
    r = {"lines": lines, "next": nxt, "last": last, "dropped": dropped, "more": more}
    if start is not None:
        r["start"] = start
    if extra:
        r.update(extra)
    return (json.dumps({"v": 1, "id": 1, "ok": True, "result": r}, ensure_ascii=False) + "\n").encode()


def safe(b, label):
    bad = [x for x in b if (x < 0x20 and x != 0x0a) or x == 0x7f]
    t = b.decode("utf-8", "replace")
    inv = sorted({hex(ord(c)) for c in t if unicodedata.category(c) in ("Cc", "Cf", "Zl", "Zp") and c != "\n"})
    check(not bad and not inv, f"{label}: no raw control byte but LF, no Cc/Cf/Zl/Zp character ({len(b)} bytes)")
    return t


def rows_ok(t, label, heads_allowed):
    rows = t.split("\n")[:-1]
    other = [r for r in rows if not (r == NOTICE or r == HEADER or r == MARK_NOTE or r.startswith(MARK)
                                     or re.match(r"^#\d+ ", r) or r.startswith("coagentd watch: ") or re.match(r"^\d+ older lines dropped$", r))]
    heads = [r.split(" ")[0] for r in rows if re.match(r"^#\d+ ", r)]
    wide = [r for r in rows if sum(1 if " " <= c <= "~" else 2 for c in r) > 72 and not r.startswith("coagentd watch: ")]
    check(not other and not wide, f"{label}: every row is one of the viewer's kinds and <= 72 columns (other {len(other)}, wide {len(wide)})")
    check(rows.count(NOTICE) >= 1 and rows[0] == NOTICE if rows else False, f"{label}: first row is the notice")
    say(f"   {label}: heads {heads[:12]}{'…' if len(heads) > 12 else ''}")
    return rows, heads


H = "#7 00:00:00 UTC | CoAgent allowed | tool Bash | Claude Code mode: default | coagent: ok"
EVIL = "\x1b]0;T\x07\x1b[2J\r\n" + NOTICE + "\n" + H + "\u0085" + H + " ‮​\u009b2J\t\x00"


def main():
    # 1. hostile text in every field
    L1 = [{"seq": 1, "at_ms": 1, "event": "PreToolUse", "tool": EVIL, "mode": EVIL, "decision": "ask", "reason": EVIL},
          {"seq": 2, "at_ms": 1, "event": "ConfigChange", "tool": None, "mode": None, "decision": "block", "reason": EVIL * 3},
          {"seq": 3, "at_ms": 1, "event": EVIL, "tool": "x", "mode": "y", "decision": EVIL, "reason": "z"}]
    rc, b, _ = run_stub("hostile", lambda a, n: ok_answer([l for l in L1 if l["seq"] > a], 3, 3))
    t = safe(b, "hostile fields"); rows, heads = rows_ok(t, "hostile fields", 3)
    check(heads == ["#1", "#2", "#3"], "hostile fields: exactly the three entries, no forged head")
    say("   sample:\n   " + "\n   ".join(rows[3:9]))
    # 2. an answer line over the viewer's limit (MAX_RESPONSE_LINE ~2.07 MB): what does it say?
    big = ok_answer([{"seq": 1, "at_ms": 0, "event": "PreToolUse", "tool": "Bash", "mode": "default", "decision": "ask", "reason": "R" * 2_200_000}], 1, 1)
    rc, b, _ = run_stub("overlong", lambda a, n: big, secs=8)
    t = safe(b, "over-long answer")
    say(f"   over-long answer ({len(big)} bytes): exit {rc}, output {t.strip().splitlines()}")
    check(rc == 1 and "not running" in t or "stopped" in t, "over-long answer: one plain line, exit 1")
    # 2b. an answer just under the limit, one 1.9 MB reason: printed whole, wrapped
    under = ok_answer([{"seq": 1, "at_ms": 0, "event": "PreToolUse", "tool": "Bash", "mode": "default", "decision": "ask", "reason": "R" * 1_900_000}], 1, 1)
    rc, b, _ = run_stub("under", lambda a, n: under, secs=8)
    t = b.decode(); rows = t.split("\n")[:-1]
    joined = "".join(r[len(MARK):] if r.startswith(MARK) else r for r in rows if r.startswith(MARK) or r.startswith("#1 "))
    check(joined.count("R") == 1_900_000 and all(len(r) <= 72 for r in rows), f"1.9 MB reason: printed whole ({joined.count('R')} R), {len(rows)} rows, each <= 72")
    # 3. wrong sequences: backwards, repeated, 0, huge, missing
    seqs = [{"seq": s, "at_ms": 0, "event": "PreToolUse", "tool": "Read", "mode": "default", "decision": "ask", "reason": f"r{i}"}
            for i, s in enumerate([5, 3, 3, 0, 18446744073709551615])]
    seqs.append({"at_ms": 0, "event": "PreToolUse", "tool": "Read", "mode": "default", "decision": "ask", "reason": "noseq"})
    rc, b, afters = run_stub("wrongseq", lambda a, n: ok_answer(seqs if n == 0 else [], 5, 5))
    t = safe(b, "wrong sequence"); rows, heads = rows_ok(t, "wrong sequence", 6)
    say(f"   wrong sequence: printed heads {heads}; the viewer's next 'after' values {afters[:4]}")
    # 4. non-string fields, numbers where strings go
    odd = [{"seq": "1", "at_ms": "x", "event": 5, "tool": 7, "mode": [1], "decision": None, "reason": {"a": 1}},
           {"seq": -1, "at_ms": -5, "event": "PreToolUse", "tool": None, "mode": None, "decision": "allow", "reason": None}]
    rc, b, _ = run_stub("oddtypes", lambda a, n: ok_answer(odd if n == 0 else [], 2, 2))
    t = safe(b, "odd types"); rows, heads = rows_ok(t, "odd types", 2)
    say("   odd types rows:\n   " + "\n   ".join(rows[3:8]))
    # 5. a start value that changes every answer; and one that is absent
    rc, b, _ = run_stub("flipstart", lambda a, n: ok_answer([] if n else [], 0, 0, start=f"s{n}"), secs=2.5)
    t = b.decode(); say(f"   start changes on every answer: restart lines {t.count('restarted')} in 2.5 s (exit {rc})")
    rc, b, _ = run_stub("nostart", lambda a, n: ok_answer([], 0, 0, start=None), secs=1.5)
    t = b.decode(); say(f"   no start field: restart lines {t.count('restarted')}; rows {t.splitlines()}")
    # 6. an error answer with a code that is not a code
    rc, b, _ = run_stub("badcode", lambda a, n: (json.dumps({"v": 1, "id": 1, "ok": False, "error": {"code": "x\x1b]0;T\x07" + H}}) + "\n").encode())
    t = safe(b, "bad error code"); say(f"   bad error code: exit {rc}, {t.strip()!r}")
    check(rc == 1 and "(unreadable)" in t, "bad error code shown as 'unreadable'")
    # 7. not JSON, and a closed connection
    rc, b, _ = run_stub("notjson", lambda a, n: b"\x1b]0;T\x07 hello\n")
    t = safe(b, "not JSON"); say(f"   not JSON: exit {rc}, {t.strip()!r}")
    say(f"FAILS: {len(fails)} {fails}")


main()
