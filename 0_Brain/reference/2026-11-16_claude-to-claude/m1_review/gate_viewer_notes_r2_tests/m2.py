"""QA-VIEWER-NOTES-R2: my OWN model of the viewer after addendum 1, written from the addendum's rules 1-4,
the fourth header line and docs/DAEMON.md section 8 (not from the builder's test), plus a READER's checker that
judges rows only by the stated rule: "A tool or mode is whole only if " |" follows it; " >>" marks a cut."

Model rules (as I read them):
  entry = head "#<seq> HH:MM:SS UTC | <decision words> | " then the TOOL piece then " | " then the MODE piece
          then " | " + reason (guarded).
  TOOL piece: a FIELD "tool " + field(tool) for a PreToolUse with a tool string; else fixed text.
  MODE piece: always a FIELD "Claude Code mode: " + (field(mode) or "not reported").
  Fixed text: unit by unit; a unit that does not fit moves whole to a new row (MARK + text).
  A FIELD is laid out with its closing " |":
    - if field + " |" fits in the room left: placed whole, closed.
    - else, at the field's start: if it holds no "\\" and MARK + field + " |" fits on a fresh row: a plain row
      break, the field starts the next row. Also a row break if not even its first unit + CUT fits.
    - else: as many units as fit leaving room for CUT, then CUT, a new row, and the rest again.
"""
import re, unicodedata

NOTICE = "Only you see this. Nothing here is sent to the other side."
HEADER = "CoAgent mode: APPROVE. One entry per call the gate decided. Times: UTC."
MARK = "    | "
MARK_NOTE = 'A row starting with four spaces and "| " continues the entry above.'
CUT_NOTE = 'A tool or mode is whole only if " |" follows it; " >>" marks a cut.'
CUT = " >>"
WIDTH = 72
SET = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.:\\{}")
HEXD = set("0123456789abcdefABCDEF")
WORDS = {"allow": "CoAgent allowed", "ask": "CoAgent asked", "deny": "CoAgent refused", "block": "CoAgent blocked"}
INVIS = [(0x00AD, 0x00AD), (0x034F, 0x034F), (0x061C, 0x061C), (0x115F, 0x1160), (0x17B4, 0x17B5), (0x180B, 0x180F),
         (0x200B, 0x200F), (0x2028, 0x202E), (0x2060, 0x206F), (0x3164, 0x3164), (0xFE00, 0xFE0F), (0xFEFF, 0xFEFF),
         (0xFFA0, 0xFFA0), (0xFFF0, 0xFFFB), (0x1BCA0, 0x1BCA3), (0x1D173, 0x1D17A), (0xE0000, 0xE0FFF)]


def guard(s):
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


def field(s):
    return "".join(c if c in SET else "\\u{%x}" % ord(c) for c in s)


def bcols(c):  # the viewer's conservative count: printable ASCII 1, everything else 2
    return 1 if " " <= c <= "~" else 2


def ucols(u):
    return sum(bcols(c) for c in u)


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


def units(t):
    out, i = [], 0
    while i < len(t):
        n = unit(t, i)
        out.append(t[i:i + n]); i += n
    return out


def pieces(l):
    """[(kind, text)] kind 'T' fixed text, 'F' a field (label + value). The closing ' |' of a field is the start
    of the next 'T' piece."""
    sv = lambda k: l.get(k) if isinstance(l.get(k), str) else None
    seq = l.get("seq") if isinstance(l.get("seq"), int) else 0
    at = l.get("at_ms") if isinstance(l.get("at_ms"), int) else 0
    s = (at // 1000) % 86400
    clock = "%02d:%02d:%02d UTC" % (s // 3600, (s % 3600) // 60, s % 60)
    dec = WORDS.get(sv("decision") or "", "CoAgent decided (unknown decision)")
    out = []
    head = f"#{seq} {clock} | {dec} | "
    e, t = sv("event"), sv("tool")
    if e == "PreToolUse" and t is not None:
        out += [("T", head), ("F", "tool " + field(t))]
        nxt = " | "
    else:
        what = ("a tool call that names no tool" if e == "PreToolUse" else
                "a settings change (ConfigChange)" if e == "ConfigChange" else "another hook event")
        nxt = head + what + " | "
    m = sv("mode")
    out += [("T", nxt), ("F", "Claude Code mode: " + ("not reported" if m is None else field(m)))]
    out.append(("T", " | " + guard(sv("reason") or "")))
    return out


def render(l):
    return "".join(t for _, t in pieces(l))


def layout(ps):
    rows, row, used = [], "", 0

    def brk():
        nonlocal row, used
        rows.append(row); row = MARK; used = len(MARK)

    after_field = False
    for kind, t in ps:
        if kind == "T":
            if after_field:
                assert t.startswith(" |"); t = t[2:]
            after_field = False
            for u in units(t):
                w = ucols(u)
                if used + w > WIDTH:
                    brk()
                row += u; used += w
            continue
        after_field = True
        us = units(t)
        first = True
        while True:
            rest = sum(ucols(u) for u in us)
            if used + rest + 2 <= WIDTH:
                row += "".join(us) + " |"; used += rest + 2
                break
            if first and (("\\" not in t and len(MARK) + rest + 2 <= WIDTH) or used + ucols(us[0]) + len(CUT) > WIDTH):
                brk(); first = False
                continue
            first = False
            k = 0
            while k < len(us) and used + ucols(us[k]) + len(CUT) <= WIDTH:
                row += us[k]; used += ucols(us[k]); k += 1
            us = us[k:]
            row += CUT
            brk()
    rows.append(row)
    return rows


def rows_of(l):
    return layout(pieces(l))


def screen(lines):
    out = [NOTICE, HEADER, MARK_NOTE, CUT_NOTE]
    for k, l in enumerate(lines):
        if k > 0 and k % 20 == 0:
            out.append(NOTICE)
        out += rows_of(l)
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------------------------------------ the reader
HEADRE = re.compile(r"^#(\d+) (\d\d:\d\d:\d\d) UTC \| (CoAgent (?:allowed|asked|refused|blocked|decided \(unknown decision\))) \| ")
FIXED_WHAT = ["a tool call that names no tool", "a settings change (ConfigChange)", "another hook event"]


def read_value(s, i):
    """A reader scanning a field value from s[i]: set characters and whole units; returns end index."""
    while i < len(s):
        c = s[i]
        if c == "\\":
            n = unit(s, i); i += n; continue
        if c in SET:
            i += 1; continue
        break
    return i


def reader(rows):
    """Judge ONE entry's rows by the stated rule only, as a careful reader would. Returns (verdicts, fields) where
    fields = [(label, value_as_reader_reconstructs_it, closed_on_row, rows_used, cut_count)] and verdicts is a list of
    problems (empty = honest). The reader: strips MARK from continuation rows; a field starts with its label; inside
    a field a row may end only with CUT (then the field goes on after the next MARK) or the field closes with ' |'.
    A field value never holds a space or '>' raw, so ' >>' at a row end inside a field is a cut, and a value that
    reaches a row end without ' |' and without ' >>' is an ERROR of the viewer (the MJ-1 kind)."""
    probs, fields = [], []
    bodies = [rows[0]] + [r[len(MARK):] if r.startswith(MARK) else None for r in rows[1:]]
    if any(b is None for b in bodies):
        probs.append("a continuation row without the mark"); return probs, fields
    m = HEADRE.match(bodies[0])
    if not m:
        probs.append("first row does not parse"); return probs, fields
    r, i = 0, m.end()

    def at_end():
        return i >= len(bodies[r])

    def next_row(why):
        nonlocal r, i
        if r + 1 >= len(bodies):
            probs.append("entry ends " + why); return False
        r += 1; i = 0
        return True

    # tool piece
    for want in ("tool", "mode"):
        # a field (or the fixed 'what') may start on the next row when the row ended at ' | '
        while at_end():
            if not next_row("before the " + want):
                return probs, fields
        b = bodies[r]
        if want == "tool" and any(b.startswith(w, i) for w in FIXED_WHAT):
            w = next(w for w in FIXED_WHAT if b.startswith(w, i))
            i += len(w)
            if b[i:i + 3] != " | " and not (b[i:] == " |" or b[i:] == " | "):
                probs.append(f"fixed text '{w}' not followed by ' | '")
            i += 3
            continue
        label = "tool " if want == "tool" else "Claude Code mode: "
        # where the field starts: its row, its column, and the columns used on the row before (if it starts a row)
        start_r, start_col = r, (0 if r == 0 else len(MARK)) + ucols(bodies[r][:i])
        prev_used = ucols(rows[r - 1]) if (r > 0 and i == 0) else None
        # the label itself may be cut
        got, rows_used, cuts = "", 1, 0
        lab_left = label
        while lab_left:
            b = bodies[r]
            tail0 = b[i:]
            label_cut = tail0.endswith(CUT) and len(tail0) - len(CUT) < len(lab_left) and lab_left.startswith(tail0[:-len(CUT)])
            if b.startswith(lab_left, i) and not label_cut:
                i += len(lab_left); lab_left = ""; break
            # label cut: the rest of this row must be a prefix of lab_left followed by CUT
            tail = b[i:]
            if tail == CUT:
                probs.append(f"row {r}: a cut mark with nothing of the {want} field before it")
            if tail.endswith(CUT) and lab_left.startswith(tail[:-len(CUT)]) and len(tail) > len(CUT) - 1:
                lab_left = lab_left[len(tail) - len(CUT):]; cuts += 1
                if not next_row("inside a label"):
                    return probs, fields
                rows_used += 1; continue
            probs.append(f"row {r}: expected the {want} label at {b[i:i+20]!r}")
            return probs, fields
        # the value ("not reported" is the viewer's own words, laid out as the mode field)
        lit = "not reported" if want == "mode" else None
        while lit is not None:
            b = bodies[r]; tail = b[i:]
            if tail.startswith(lit + " |"):
                got += lit; i += len(lit); lit = None; break
            if tail.endswith(CUT) and lit.startswith(tail[:-len(CUT)]) and len(tail) > len(CUT):
                got += tail[:-len(CUT)]; lit = lit[len(tail) - len(CUT):]; cuts += 1
                if not next_row("inside 'not reported'"):
                    return probs, fields
                rows_used += 1; continue
            # not the viewer's words: what was read so far ("not", set characters) is an ordinary value
            lit = None
        while True:
            b = bodies[r]
            j = read_value(b, i)
            got += b[i:j]; i = j
            if b.startswith(" |", i):
                i += 2
                fields.append((want, got, r, rows_used, cuts))
                fw = ucols(label + got)
                if cuts and start_col + fw + 2 <= WIDTH:
                    probs.append(f"the {want} field {got!r} is CUT although it and its ' |' fit on row {start_r}")
                if prev_used is not None and prev_used + fw + 2 <= WIDTH:
                    probs.append(f"the {want} field {got!r} MOVED to row {start_r} although it fit on the row before")
                break
            if b[i:] == CUT:
                cuts += 1
                if not next_row("inside a value"):
                    return probs, fields
                rows_used += 1
                continue
            if i >= len(b):
                probs.append(f"row {r} ENDS INSIDE the {want} value {got!r} with neither ' |' nor the cut mark (MJ-1)")
                return probs, fields
            probs.append(f"row {r}: unexpected {b[i:i+12]!r} after the {want} value {got!r}")
            return probs, fields
        # the separator space after ' |'
        if want == "tool":
            if i < len(bodies[r]):
                if bodies[r][i] != " ":
                    probs.append("no space after the tool field's ' |'")
                i += 1
            else:
                # the space moved to the next row
                if not next_row("after the tool field"):
                    return probs, fields
                if bodies[r].startswith(" "):
                    i = 1
    # the reason: rest
    return probs, fields
