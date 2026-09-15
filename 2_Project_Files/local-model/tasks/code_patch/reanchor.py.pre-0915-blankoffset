#!/usr/bin/env python3
"""reanchor.py <section.diff> <file-at-tip> <out.diff> — rebuild a section's hunks from their -/+ lines only.

WHY (2026-09-15, the ten-ticket test): the commonest Ornith failure is not a wrong fix but INVENTED CONTEXT — a
one-line edit emitted under neighbours that sit ten lines away (KS-844 q4), or a 7-line hunk whose context lines
drift by a word (KS-1018 q8, KS-864 q8). The `-` lines are almost always right (they are quoted in the brief). So:
for every hunk, take the `-` lines, find them as a CONTIGUOUS, UNIQUE block in the real file, and rebuild the hunk
with the file's own context (3 lines each side) — the `+` lines keep the order the model gave them relative to the
`-` block. An insert-only hunk (no `-` lines) is anchored on its nearest non-blank context line if that line is
unique in the file. Anything ambiguous is left exactly as the model wrote it, and the caller sees the note.

Exit 0 = wrote out.diff (possibly identical); the notes on stdout say per hunk: reanchored / kept / ambiguous.
This is an ACCOMMODATION the checker records loudly (A2 "REANCHORED"), never a silent repair.
"""
import os
import re
import sys


def parse(section_text):
    lines = section_text.split("\n")
    head = []
    i = 0
    while i < len(lines) and not lines[i].startswith("@@"):
        head.append(lines[i]); i += 1
    hunks = []
    cur = None
    for ln in lines[i:]:
        if ln.startswith("@@"):
            cur = {"header": ln, "body": []}
            hunks.append(cur)
        elif cur is not None:
            cur["body"].append(ln)
    for h in hunks:
        while h["body"] and h["body"][-1] == "":
            h["body"].pop()
    return head, hunks


def recount(header, body):
    """a kept hunk still gets honest counts (the model's are wrong more often than not)"""
    m = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@(.*)$", header)
    if not m:
        return header
    old = sum(1 for b in body if b.startswith((" ", "-")))
    new = sum(1 for b in body if b.startswith((" ", "+")))
    return f"@@ -{m.group(1)},{old} +{m.group(2)},{new} @@{m.group(3)}"


def find_block(file_lines, block):
    """all start indexes where block (list of stripped-right strings) occurs contiguously"""
    n = len(block)
    if n == 0:
        return []
    hits = []
    for s in range(0, len(file_lines) - n + 1):
        ok = True
        for k in range(n):
            if file_lines[s + k].rstrip() != block[k].rstrip():
                ok = False; break
        if ok:
            hits.append(s)
    return hits


def span_match(file_lines, seq):
    """unique (start,end) span where seq's NON-BLANK lines occur in order with only blank FILE lines between; None if not unique"""
    nb = [m for m in seq if m.strip()]
    if not nb:
        return None
    cands = []
    for s0 in range(len(file_lines)):
        if file_lines[s0].rstrip() != nb[0].rstrip():
            continue
        k = 0; pos = s0; gap = 0
        while pos < len(file_lines) and k < len(nb):
            if file_lines[pos].rstrip() == nb[k].rstrip():
                k += 1; pos += 1; gap = 0
            elif not file_lines[pos].strip():
                pos += 1
            elif gap < 2:
                gap += 1; pos += 1          # the model DROPPED a file line (a comment, usually) — tolerate up to 2 per gap
            else:
                break
        if k == len(nb):
            cands.append((s0, pos))
    return cands[0] if len(cands) == 1 else None


def rebuild_old_side(hunk, file_lines, notes, idx):
    """2026-09-15 (KS-864 q8 ×2): '-' lines in TWO runs with context between them — anchor on the whole OLD SIDE
    (context + '-'), blank-tolerant, and re-emit the hunk over the file's real span: context lines take the file's
    text, '-' lines mark the file's line, '+' lines keep the model's text and position."""
    body = [b for b in hunk["body"] if b != "\\ No newline at end of file"]
    old_side = [b[1:] for b in body if b.startswith((" ", "-"))]
    sp = span_match(file_lines, old_side)
    if sp is None:
        return None
    start, end = sp
    out = []; pos = start
    for b in body:
        if b.startswith("+"):
            out.append(b); continue
        want = b[1:]
        # consume file lines up to the one matching this body line (blank file lines in between become context)
        gap = 0
        while pos < end and file_lines[pos].rstrip() != want.rstrip():
            if not file_lines[pos].strip() or gap < 2:
                if file_lines[pos].strip(): gap += 1
                out.append(" " + file_lines[pos]); pos += 1   # a file line the model dropped becomes context
            else:
                return None
        if pos >= end:
            return None
        out.append(("-" if b.startswith("-") else " ") + file_lines[pos]); pos += 1
    while pos < end:
        out.append(" " + file_lines[pos]); pos += 1
    pre = file_lines[max(0, start - 3):start]; post = file_lines[end:end + 3]
    old_count = len(pre) + sum(1 for o in out if o.startswith((" ", "-"))) + len(post)
    new_count = len(pre) + sum(1 for o in out if o.startswith((" ", "+"))) + len(post)
    res = [f"@@ -{max(0, start - 3) + 1},{old_count} +{max(0, start - 3) + 1},{new_count} @@"]
    res += [" " + l for l in pre] + out + [" " + l for l in post]
    notes.append(f"hunk {idx}: reanchored on the whole OLD SIDE at {start + 1}-{end} (the '-' lines were not one run)")
    return res


def _join_run(file_lines, s, n):
    """the space-join of n tip lines from s: continuation lines lose their indent (a wrapped bullet), and a BLANK
    line ends a paragraph — a run may never span one (returns None so the caller stops)"""
    seg = file_lines[s:s + n]
    if len(seg) < n or any(not l.strip() for l in seg):
        return None
    return " ".join((l.rstrip() if k == 0 else l.strip()) for k, l in enumerate(seg))


def reflow(body, file_lines, notes, idx):
    """2026-09-15 21:4x (KS-1097 B r2, a doc_patch): the model RE-FLOWS a hard-wrapped markdown paragraph into ONE
    line — five tip lines joined by single spaces — and the hunk cannot apply. Gated by REANCHOR_REFLOW=1 (set by
    the doc_patch checker only). For each body line whose text is not a tip line: a '-' or ' ' line that EQUALS the
    space-join of N>=2 consecutive tip lines is split back into those N lines; a '+' line whose text STARTS with such
    a join (N>=2) is split so the first N-1 lines are the tip's and the last carries the tip line plus the remainder.
    A ' ' (context) line that starts with a join but carries EXTRA text is an edit hidden in a context line —
    refused by name, never inferred. Every split is a note the verdict carries."""
    out = []
    tip_set = {l.rstrip() for l in file_lines}
    for b in body:
        if not b or b[0] not in " -+" or b[1:].rstrip() in tip_set or b == "\\ No newline at end of file":
            out.append(b); continue
        kind, text = b[0], b[1:].rstrip()
        # 2026-09-15 21:5x (KS-1097 C r3): a '-' or context line carrying a DOUBLE marker — "--  not the reviewer" where
        # the tip line is "  not the reviewer" — the model applied the bullet rule ("-- " = marker + bullet) to a
        # continuation line. Repair only when the stripped text IS a tip line and the unstripped is not.
        if kind in " -" and text.startswith("-") and text[1:].rstrip() in tip_set:
            out.append(kind + text[1:]); notes.append(f"hunk {idx}: REFLOW — a '{kind}' line carried a double marker; one '-' stripped to match the tip line"); continue
        best = None  # (start, n, exact)
        for s0 in range(len(file_lines)):
            first = file_lines[s0].rstrip()
            if not first or not text.startswith(first):
                continue
            n = 1
            while s0 + n < len(file_lines):
                jn = _join_run(file_lines, s0, n + 1)
                if jn is None or not text.startswith(jn):
                    break
                n += 1
            if n < 2:
                continue
            j = _join_run(file_lines, s0, n)
            if text == j:
                best = (s0, n, True); break
            if best is None or n > best[1]:
                best = (s0, n, False)
        if best is None:
            out.append(b); continue
        s0, n, exact = best
        pieces = [file_lines[s0 + k].rstrip() for k in range(n)]
        if exact:
            out += [kind + pc for pc in pieces]
            notes.append(f"hunk {idx}: REFLOW — a '{kind}' line was the space-join of tip lines {s0 + 1}-{s0 + n}; split back")
        elif kind == "+":
            n, pieces, model_last = _extend_last(file_lines, s0, n, pieces, text)
            out += ["+" + pc for pc in pieces[:-1]] + ["+" + model_last]
            notes.append(f"hunk {idx}: REFLOW — a '+' line started with the space-join of tip lines {s0 + 1}-{s0 + n}; split back, the remainder kept on the last line")
        else:
            # 2026-09-15 21:5x (KS-1097 B r1-r3, three rounds of one shape): the model writes the whole paragraph as ONE
            # CONTEXT line carrying the appended tail. Inferring an edit from context is refused in general — UNLESS the
            # brief's own must_remove list (REANCHOR_MUST_REMOVE=<file of lines>, written by the doc checker) names the
            # LAST joined tip line: then the brief authorised replacing exactly that line, and the tail is the edit.
            n, pieces, model_last = _extend_last(file_lines, s0, n, pieces, text)
            last = pieces[-1]
            rem = model_last[len(last.rstrip(".;:,!?")):] if model_last.startswith(last.rstrip(".;:,!?")) else model_last
            if kind == " " and last in _must_remove() and rem.strip():
                out += [" " + pc for pc in pieces[:-1]] + ["-" + last, "+" + model_last]
                notes.append(f"hunk {idx}: REFLOW INFERRED — a context line was the space-join of tip lines {s0 + 1}-{s0 + n} plus a tail; line {s0 + n} is a brief must-remove line, so the tail is applied to it as -/+ (D7/D5 judge the result)")
            else:
                notes.append(f"hunk {idx}: REFLOW REFUSED — a '{kind}' line is the space-join of tip lines {s0 + 1}-{s0 + n} PLUS extra text: an edit hidden in a context line is not inferred")
                out.append(b)
    return out


def _extend_last(file_lines, s0, n, pieces, text):
    """the model drops a line's trailing punctuation before its tail ("…author*." → "…author* — superseded"): if the
    remainder starts with the NEXT tip line minus trailing punctuation, that line is part of the run and the model's
    version of it (core + tail) is the last '+' line. Returns (n, pieces, model_last)."""
    rem = text[len(_join_run(file_lines, s0, n)):]
    nxt_i = s0 + n
    if nxt_i < len(file_lines):
        nxt = file_lines[nxt_i].rstrip(); core = nxt.rstrip(".;:,!?")
        if core and rem.lstrip().startswith(core):
            pieces = pieces + [nxt]
            return n + 1, pieces, core + rem.lstrip()[len(core):]
    return n, pieces, pieces[-1] + rem


_MR = None
def _must_remove():
    global _MR
    if _MR is None:
        pth = os.environ.get("REANCHOR_MUST_REMOVE", "")
        try:
            _MR = {l.rstrip("\n") for l in open(pth, encoding="utf-8")} if pth else set()
        except OSError:
            _MR = set()
    return _MR


def rebuild(hunk, file_lines, notes, idx):
    body = [b for b in hunk["body"] if b != "\\ No newline at end of file"]
    if os.environ.get("REANCHOR_REFLOW") == "1":
        body = reflow(body, file_lines, notes, idx)
    if any(b.startswith("++++ b/") or b.startswith("+--- ") for b in body):
        notes.append(f"hunk {idx}: a file HEADER sits inside the hunk as a '+' line — refused, kept as written (the splitter should have caught it)")
        return None
    minus = [b[1:] for b in body if b.startswith("-")]
    plus = [b[1:] for b in body if b.startswith("+")]
    ctx = [b[1:] for b in body if b.startswith(" ")]
    if minus:
        hits = find_block(file_lines, minus)
        blank_span = None
        if len(hits) == 0:
            # 2026-09-15 (KS-864 q8 ×2): the model DROPS blank lines from a '-' block (the four staging lines
            # follow the signature line with the file's empty line 45 omitted). Match the NON-BLANK '-' lines
            # in order, allowing only blank FILE lines between them; the real span (blanks included) becomes
            # the '-' block, so the rebuilt hunk removes exactly what the file holds there.
            nb = [m for m in minus if m.strip()]
            if nb:
                cands = []
                for s0 in range(len(file_lines)):
                    if file_lines[s0].rstrip() != nb[0].rstrip():
                        continue
                    k = 0; pos = s0
                    while pos < len(file_lines) and k < len(nb):
                        if file_lines[pos].rstrip() == nb[k].rstrip():
                            k += 1; pos += 1
                        elif not file_lines[pos].strip():
                            pos += 1
                        else:
                            break
                    if k == len(nb):
                        cands.append((s0, pos))
                if len(cands) == 1:
                    blank_span = cands[0]
                    hits = [blank_span[0]]
                    notes.append(f"hunk {idx}: '-' block matched with the model's dropped blank line(s) restored from the file (span {blank_span[0]+1}-{blank_span[1]})")
        if len(hits) == 0:
            alt = rebuild_old_side(hunk, file_lines, notes, idx)
            if alt is not None:
                return alt
            notes.append(f"hunk {idx}: ambiguous — the {len(minus)} '-' line(s) occur 0x in the file; kept as written")
            return None
        if len(hits) > 1:
            m = re.match(r"@@ -(\d+)", hunk["header"])
            declared = int(m.group(1)) if m else 0
            hits.sort(key=lambda h: abs(h - (declared - 1)))
            if len(hits) > 1 and abs(hits[0] - (declared - 1)) > 40:
                notes.append(f"hunk {idx}: ambiguous — the '-' block occurs {len(hits)}x and none within 40 lines of the declared start {declared}; kept as written")
                return None
            notes.append(f"hunk {idx}: '-' block occurs {len(hits)}x — took the one nearest the declared start {declared}")
        start = hits[0]
        # where do the '+' lines sit relative to the '-' block? keep the model's ordering of -/+ within the body
        mid = [b for b in body if b.startswith("-") or b.startswith("+")]
        end = start + len(minus)
        if blank_span is not None:
            end = blank_span[1]
            minus = file_lines[start:end]
            plus_only = [b for b in body if b.startswith("+")]
            mid = ["-" + l for l in minus] + plus_only
    else:
        # insert-only: anchor on the first non-blank context line BEFORE the '+' block, else AFTER it
        before, after = [], []
        seen_plus = False
        for b in body:
            if b.startswith("+"):
                seen_plus = True
            elif b.startswith(" "):
                (after if seen_plus else before).append(b[1:])
        anchor = None
        for cand in reversed(before):
            if cand.strip():
                # 2026-09-15 22:0x (KS-976 B r1): an insert anchored right after a line that OPENS a block comment
                # (`/**`, `/*`) lands inside the comment — the helper was commented out and tsc could not find it.
                if cand.strip() in ("/**", "/*") or cand.strip().endswith(("/**", "/*")):
                    notes.append(f"hunk {idx}: insert-only — refused to anchor after a block-comment opener ({cand.strip()!r}); trying the line before it")
                    continue
                hits = find_block(file_lines, [cand])
                if len(hits) == 1:
                    anchor = ("before", hits[0]); break
        if anchor is None:
            for cand in after:
                if cand.strip():
                    hits = find_block(file_lines, [cand])
                    if len(hits) == 1:
                        anchor = ("after", hits[0]); break
        if anchor is None:
            notes.append(f"hunk {idx}: ambiguous — insert-only and no unique context line; kept as written")
            return None
        if anchor[0] == "before":
            start = end = anchor[1] + 1
        else:
            start = end = anchor[1]
        # 2026-09-15 22:0x (KS-976 B r1): an insert placed just below a block-comment opener (`/**`, `/*`) — the
        # "after" branch anchored on ` * POST …` — lands INSIDE the comment; move it above the opener.
        moved = 0
        while start > 0 and (file_lines[start - 1].strip() in ("/**", "/*") or file_lines[start - 1].strip().endswith(("/**", "/*"))):
            start -= 1; end = start; moved += 1
        if moved:
            notes.append(f"hunk {idx}: insert-only — moved above a block-comment opener ({moved} line(s)) so the insert is not commented out")
        mid = ["+" + p for p in plus]
    pre = file_lines[max(0, start - 3):start]
    post = file_lines[end:end + 3]
    old_count = len(pre) + len(minus) + len(post)
    new_count = len(pre) + len(plus) + len(post)
    out = [f"@@ -{max(0, start - 3) + 1},{old_count} +{max(0, start - 3) + 1},{new_count} @@"]
    out += [" " + l for l in pre]
    out += mid
    out += [" " + l for l in post]
    notes.append(f"hunk {idx}: reanchored at {start + 1} ({len(minus)} '-' / {len(plus)} '+' lines; model header {hunk['header'].split('@@')[1].strip()})")
    return out


def _deoverlap(lines, notes):
    """2026-09-15 21:5x (KS-1097 C r3): two rebuilt hunks four lines apart share context; `git apply` refuses
    overlapping hunks AND asymmetric context (3 leading / 0 trailing), so trimming cannot fix it — overlapping
    hunks are MERGED into one by old-file line number. Context lines are the file's own text in both, so the
    union is exact; '+' lines keep their place after the old line they followed. Later hunks' '+' starts are
    recomputed from the net delta of the hunks before them."""
    head, hunks, cur = [], [], None
    for ln in lines:
        if ln.startswith("@@"):
            cur = [ln]; hunks.append(cur)
        elif cur is None:
            head.append(ln)
        else:
            cur.append(ln)
    def parse_h(h):
        m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$", h[0])
        s0 = int(m.group(1)); rows = []; num = s0 - 1
        for b in h[1:]:
            if b.startswith("+"):
                rows.append((num, "+", b))          # attached after old line `num`
            else:
                num += 1; rows.append((num, b[0], b))
        return s0, num, rows, m.group(5)
    merged = []
    for h in hunks:
        s0, e0, rows, tail = parse_h(h)
        if merged and merged[-1][1] >= s0:
            ps, pe, prow, ptail = merged[-1]
            byline = {}; plus = {}
            for num, k, b in prow + rows:
                if k == "+":
                    plus.setdefault(num, []).append(b)
                else:
                    if k == "-" or num not in byline:
                        byline[num] = (k, b)
            rows2 = []
            for num in range(min(ps, s0), max(pe, e0) + 1):
                if num in byline:
                    rows2.append((num, byline[num][0], byline[num][1]))
                for b in plus.get(num, []):
                    rows2.append((num, "+", b))
            for b in plus.get(min(ps, s0) - 1, []):
                rows2.insert(0, (min(ps, s0) - 1, "+", b))
            merged[-1] = (min(ps, s0), max(pe, e0), rows2, ptail)
            notes.append(f"hunks merged: {ps}-{pe} and {s0}-{e0} overlapped (one hunk now)")
        else:
            merged.append((s0, e0, rows, tail))
    out = list(head); delta = 0
    for s0, e0, rows, tail in merged:
        body = [b for _, _, b in rows]
        on = sum(1 for _, k, _ in rows if k != "+"); nn = sum(1 for _, k, _ in rows if k != "-")
        out.append(f"@@ -{s0},{on} +{s0 + delta},{nn} @@{tail}"); out += body; delta += nn - on
    return out


def main():
    if len(sys.argv) != 4:
        print(__doc__); sys.exit(2)
    sec = open(sys.argv[1], encoding="utf-8").read()
    file_lines = open(sys.argv[2], encoding="utf-8").read().split("\n")
    head, hunks = parse(sec)
    notes = []
    out = list(head)
    changed = 0
    for i, h in enumerate(hunks, 1):
        rb = rebuild(h, file_lines, notes, i)
        if rb is None:
            out.append(recount(h["header"], h["body"])); out += h["body"]
        else:
            out += rb; changed += 1
    out = _deoverlap(out, notes)
    open(sys.argv[3], "w", encoding="utf-8").write("\n".join(out).rstrip("\n") + "\n")
    for n in notes:
        print(n)
    print(f"reanchored {changed}/{len(hunks)} hunk(s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
