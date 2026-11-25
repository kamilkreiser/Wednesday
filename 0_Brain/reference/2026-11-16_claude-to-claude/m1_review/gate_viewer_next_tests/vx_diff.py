#!/usr/bin/env python3
"""QA-VIEWER-NEXT item 5 (a), (b), (c-viewer side): the OLD (main 9145840) and NEW (head 64c74ae) real viewers
(`coagentd watch`) are each fed the SAME `activity` lines by a socket stub; their screens are compared by program.

usage: python3 -B vx_diff.py <old bin dir> <new bin dir> <root (new, short)> <out dir (new)> <corpus.json> [<corpus.json> ...]
A corpus file is a JSON list of activity lines (the daemon's answer form) or {"lines": [...], "labels": [...]}.
Per corpus it prints:
  (a) old rows 0-3 == new rows 0-3; new row 4 == the new line; new == old with exactly one row inserted after row 4;
      the new line in old 0x / in new 1x; new == the earlier check's independent model (m2) with the new row 5.
  (b) every width 72..200 (ambiguous as 1 and as 2): widest row by the viewer's count and a strict count, terminal
      wraps, forged entry heads / notice / header rows, where the new line appears.
  (c) per entry, my own reader (marks off; " >>" taken off ONLY where the row, without it, ends strictly inside a
      tool or mode field span of the entry, computed from m2's pieces): joined back == the render; every row end at a
      unit start (no escape split); every row-final " >>" outside a field is the entry's own text (CUT never printed
      outside a field); reach (entries / rows whose reason row ends " >>"); the OLD reading (every row-final " >>"
      off, last row aside) misreads exactly those entries.
Nothing is deleted; the stub sockets live under <root>.
"""
import json, os, re, socket, subprocess, sys, threading, time, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2  # the earlier check's model of render + layout (written from the rules, not from the builder's test)

OLD, NEW, ROOT, OUTD = sys.argv[1:5]
CORPORA = sys.argv[5:]
os.makedirs(ROOT)
os.makedirs(OUTD)
SCOPE = 'Only a tool or mode is cut; any other " >>" is part of the text.'
HEADS = [m2.NOTICE, m2.HEADER, m2.MARK_NOTE, m2.CUT_NOTE]
PAGE = 64


def run_viewer(bindir, lines, tag):
    d = os.path.join(ROOT, tag)
    os.makedirs(os.path.join(d, "ipc"))
    os.chmod(d, 0o700)
    os.chmod(os.path.join(d, "ipc"), 0o700)
    path = os.path.join(d, "ipc", "daemon.sock")
    ls = socket.socket(socket.AF_UNIX)
    ls.bind(path)
    ls.listen(16)
    ls.settimeout(0.2)
    stop = threading.Event()

    def serve():
        while not stop.is_set():
            try:
                c, _ = ls.accept()
            except socket.timeout:
                continue
            f = c.makefile("rb")
            try:
                req = json.loads(f.readline())
                after = int(req["args"]["after"])
            except Exception:
                c.close()
                continue
            page = lines[after:after + PAGE]
            r = {"lines": page, "next": after + len(page), "last": len(lines), "dropped": 0,
                 "more": after + len(page) < len(lines), "start": "stub-qvx"}
            try:
                c.sendall((json.dumps({"v": 1, "id": 1, "ok": True, "result": r}, ensure_ascii=False) + "\n").encode())
            except OSError:
                pass
            c.close()

    th = threading.Thread(target=serve, daemon=True)
    th.start()
    of = os.path.join(OUTD, tag + ".out")
    p = subprocess.Popen([f"{bindir}/coagentd", "watch", "--data-dir", d], env={}, stdin=subprocess.DEVNULL,
                         stdout=open(of, "wb"), stderr=subprocess.STDOUT)
    t0 = time.time()
    while time.time() - t0 < 600:
        b = open(of, "rb").read()
        if b.count(b"\n#") >= len(lines):
            break
        time.sleep(0.3)
    time.sleep(1.2)
    p.terminate()
    p.wait()
    stop.set()
    th.join()
    ls.close()
    return open(of, "rb").read().decode("utf-8")


def ea(c, amb):
    if unicodedata.combining(c):
        return 0
    w = unicodedata.east_asian_width(c)
    return 2 if w in "WF" else (amb if w == "A" else 1)


def term_cols(r, amb):
    return sum(ea(c, amb) for c in r)


def strict(r):
    # a strict count: every character outside printable ASCII 2 columns (never fewer than any terminal gives it)
    return sum(1 if " " <= c <= "~" else 2 for c in r)


def spans(l):
    out, at = [], 0
    for kind, t in m2.pieces(l):
        n = len(t)
        if kind == "F":
            out.append((at, at + n))
        at += n
    return out


def unit_starts(e):
    s, i = set(), 0
    while i < len(e):
        s.add(i)
        i += m2.unit(e, i)
    s.add(len(e))
    return s


def read_entry(l, rows):
    """My reader. Returns (joined, problems, reason_rows_ending_cut, field_cuts)."""
    e = m2.render(l)
    sp = spans(l)
    starts = unit_starts(e)
    probs, rr, fc = [], 0, 0
    at, out = 0, []
    for k, r in enumerate(rows):
        if k > 0:
            if not r.startswith(m2.MARK):
                probs.append(f"row {k} without the mark")
                return "".join(out), probs, rr, fc
            body = r[len(m2.MARK):]
        else:
            body = r
        last = k + 1 == len(rows)
        if not last and body.endswith(m2.CUT):
            o = at + len(body) - len(m2.CUT)
            if any(a < o < b for a, b in sp):
                body = body[:-len(m2.CUT)]
                fc += 1
            else:
                # outside every field: it must be the entry's own text there
                if e[at:at + len(body)] != body or not e[:at + len(body)].endswith(m2.CUT):
                    probs.append(f"row {k}: ' >>' outside a field that is not the entry's text")
                if any(a < at + len(body) <= b for a, b in sp):
                    probs.append(f"row {k}: ' >>' ends at a field end")
                rr += 1
        if e[at:at + len(body)] != body:
            probs.append(f"row {k}: body differs from the render at {at}")
        at += len(body)
        if at not in starts:
            probs.append(f"row {k}: ends inside a unit (escape split) at {at}")
        out.append(body)
    j = "".join(out)
    if j != e:
        probs.append("joined back != render")
    return j, probs, rr, fc


def old_join(rows):
    out = []
    for k, r in enumerate(rows):
        b = r if k == 0 else r[len(m2.MARK):]
        if k + 1 < len(rows) and b.endswith(m2.CUT):
            b = b[:-len(m2.CUT)]
        out.append(b)
    return "".join(out)


def groups_of(rows, skip):
    gs, cur, kinds = [], None, []
    for i, r in enumerate(rows):
        if i < skip:
            continue
        if r == m2.NOTICE:
            kinds.append((i, "notice"))
            cur = None
            continue
        if re.match(r"^#\d+ ", r):
            cur = [r]
            gs.append(cur)
            kinds.append((i, "head"))
        else:
            if cur is None:
                kinds.append((i, "orphan"))
                continue
            cur.append(r)
            kinds.append((i, "cont"))
    return gs, kinds


def main():
    summary = []
    for ci, cf in enumerate(CORPORA):
        data = json.load(open(cf))
        lines = data["lines"] if isinstance(data, dict) else data
        name = os.path.basename(cf).rsplit(".", 1)[0]
        print(f"== corpus {name}: {len(lines)} lines")
        old = run_viewer(OLD, lines, f"o{ci}")
        new = run_viewer(NEW, lines, f"n{ci}")
        O, N = old.split("\n"), new.split("\n")
        assert O[-1] == "" and N[-1] == ""
        O, N = O[:-1], N[:-1]
        print(f"   rows: old {len(O)}, new {len(N)}")
        a1 = O[:4] == N[:4] == HEADS
        a2 = len(N) > 4 and N[4] == SCOPE
        a3 = N[:4] + N[5:] == O
        cnt_old, cnt_new = O.count(SCOPE), N.count(SCOPE)
        model = m2.screen(lines).split("\n")[:-1]
        model5 = model[:4] + [SCOPE] + model[4:]
        a4 = N == model5
        print(f"   (a) old rows 0-3 == new rows 0-3 == the four fixed rows: {a1}")
        print(f"   (a) new row 4 (index) is the new line: {a2}; in old {cnt_old}x, in new {cnt_new}x")
        print(f"   (a) new == old with exactly one row inserted after row 4: {a3}")
        diff_after = sum(1 for x, y in zip(O[4:], N[5:]) if x != y) + abs(len(O[4:]) - len(N[5:]))
        print(f"   (a) rows after the header differing: {diff_after}")
        print(f"   (a) new == the independent model (m2, with the new row 5): {a4}")
        if not a4:
            for i, (x, y) in enumerate(zip(N, model5)):
                if x != y:
                    print("      first model diff row", i, repr(x), repr(y))
                    break
        # (b) widths
        wv = max(strict(r) for r in N)
        wv2 = max(m2.ucols(r) for r in N)
        groups, kinds = groups_of(N, 5)
        heads_real = [g[0] for g in groups]
        n_entries = len(lines)
        notice_idx = [i for i, k in kinds if k == "notice"]
        want_notices = [k for k in range(1, n_entries) if k % 20 == 0]
        bad_w = []
        head_set = {i for i, k in kinds if k == "head"}
        notice_set = set(notice_idx)
        fixed_bad = 0
        for i, r in enumerate(N):
            if re.match(r"^#\d+ ", r) and i not in head_set:
                fixed_bad += 1
            if r in (m2.HEADER, m2.MARK_NOTE, m2.CUT_NOTE, SCOPE) and i not in (1, 2, 3, 4):
                fixed_bad += 1
            if r == m2.NOTICE and i != 0 and i not in notice_set:
                fixed_bad += 1
        scope_at = [i for i, r in enumerate(N) if r == SCOPE]
        import bisect
        for amb in (1, 2):
            cs = sorted(term_cols(r, amb) for r in N)
            for w in range(72, 201):
                wraps = len(cs) - bisect.bisect_right(cs, w)
                if wraps or fixed_bad or scope_at != [4]:
                    bad_w.append((w, amb, wraps, fixed_bad, scope_at[:3]))
        print(f"   (b) rows starting like an entry head that are not one, header/notice rows out of place: {fixed_bad}; new line at rows {scope_at[:5]}")
        orphans = sum(1 for _, k in kinds if k == "orphan")
        print(f"   (b) widest row: viewer count {wv2}, strict count {wv}; widths 72-200 x ambiguous 1/2 with a wrap, a forged"
              f" head/notice/header row or the new line elsewhere than row 5: {len(bad_w)} {bad_w[:3]}")
        print(f"   (b) entry heads {len(heads_real)} == lines {n_entries}: {len(heads_real) == n_entries}; orphan rows {orphans};"
              f" notices before entries {len(notice_idx)} == {len(want_notices)}")
        # (c) per entry
        reach_e = reach_r = probs_n = fieldcuts = oldmis = oldmis_wrong = 0
        shown = 0
        for l, g in zip(lines, groups):
            j, probs, rr, fc = read_entry(l, g)
            fieldcuts += fc
            if rr:
                reach_e += 1
                reach_r += rr
            if probs:
                probs_n += 1
                if probs_n <= 5:
                    print("      PROBLEM", probs, "\n        " + "\n        ".join(g))
            mis = old_join(g) != m2.render(l)
            if mis:
                oldmis += 1
            if mis != bool(rr):
                oldmis_wrong += 1
            if rr and shown < 2 and name.startswith("own"):
                shown += 1
                print("      example (reason row ends ' >>'):\n        " + "\n        ".join(g))
        print(f"   (c) my reader: entries with a problem {probs_n} of {len(groups)}; field cuts {fieldcuts};"
              f" REACH: entries with a reason row ending ' >>' {reach_e}, such rows {reach_r}")
        print(f"   (c) old reading (every row-final ' >>' off) misreads {oldmis} entries; misread != reached: {oldmis_wrong}")
        ok = a1 and a2 and a3 and a4 and cnt_old == 0 and cnt_new == 1 and diff_after == 0 and not bad_w and \
            len(heads_real) == n_entries and orphans == 0 and probs_n == 0 and oldmis_wrong == 0 and wv <= 72 and wv2 <= 72
        summary.append((name, len(lines), len(O), len(N), reach_e, reach_r, ok))
    print("== SUMMARY (corpus, lines, old rows, new rows, reach entries, reach rows, all checks pass)")
    for s in summary:
        print("  ", s)
    sys.exit(0 if all(s[-1] for s in summary) else 1)


main()
