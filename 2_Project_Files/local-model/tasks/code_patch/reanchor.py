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


def rebuild(hunk, file_lines, notes, idx):
    body = [b for b in hunk["body"] if b != "\\ No newline at end of file"]
    if any(b.startswith("++++ b/") or b.startswith("+--- ") for b in body):
        notes.append(f"hunk {idx}: a file HEADER sits inside the hunk as a '+' line — refused, kept as written (the splitter should have caught it)")
        return None
    minus = [b[1:] for b in body if b.startswith("-")]
    plus = [b[1:] for b in body if b.startswith("+")]
    ctx = [b[1:] for b in body if b.startswith(" ")]
    if minus:
        hits = find_block(file_lines, minus)
        if len(hits) == 0:
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
    open(sys.argv[3], "w", encoding="utf-8").write("\n".join(out).rstrip("\n") + "\n")
    for n in notes:
        print(n)
    print(f"reanchored {changed}/{len(hunks)} hunk(s)")
    sys.exit(0)


if __name__ == "__main__":
    main()
