#!/usr/bin/env python3
"""brief_bytes.py <input.json> <sections.json> — contract clause 2 for the MULTI-FILE tiers (2026-10-07, rung 3):
"every line the brief adds is in the output BYTE-IDENTICAL", measured PER DECLARED FILE, in order.

WHY: code_patch2's A3c compares the brief's '+' lines as a stripped MULTISET over the union of sections, and A3i reads
only `## The exact change`, so a NEW test given in full under `## The test` (a ```ts block, KS-1278) was "not measured":
the 2026-10-05 KS-1278 r3 review had to byte-compare the new test's 157 lines by hand ("the checker did NOT prove the
second part"). bash_patch2 has no A3i at all. This tool is that leg, shared by both tiers.

WHAT the brief contributes, per file (read from input.ticket.description = the brief; only its `## The exact change`
and `## The test` regions, each up to the next `## ` heading, so a tamper/example fence elsewhere is never read):
  - a fenced block holding `+++ ` headers (a diff): every '+' line (not '+++') after a `+++ b/<path>` header is that
    path's, in order. '+' lines before any header are UNATTRIBUTED (counted; they make that block unmeasurable).
  - a fenced block with no `+++ ` header: the WHOLE block is the content of the file named by the closest preceding
    `File: \\`<path>\\`` / `Test file: \\`<path>\\`` line in the same region (after the previous block) — accepted only
    when that path is a declared NEW file (a new file's '+' lines ARE its content). Otherwise ignored, and said so.
What the output contributes: every '+' line (not '+++') of every section (sections.json `path` -> `file`) whose path is
that declared file, in section order — the checker's split of the model's diff.
Paths match when equal or when one ends with "/" + the other (sections may be service- or repo-relative).

Compared EXACTLY (no strip, no unescape, no trailing-comment allowance — those live in A3c; this is the byte clause).
One normalisation, applied to BOTH sides alike: inside one hunk, a '+' line byte-equal to a '-' line of that same hunk is
a no-op rewrite (the kit convention writes a blank line beside an edit point as a `-`/`+` empty pair, where `git diff`
writes one blank context line — measured on KS-1278's git-form golden, 2026-10-07), so each such '+' consumes one equal
'-' and is dropped before the compare. A real addition is never byte-equal to a line its own hunk removes.
Output: `OK <path> <n>` · `DIFF <path> ...first difference...` · `UNMEASURED <path> <why>` · `INFO ...` lines, then
`SUMMARY declared=… measured=… ok=… diff=… unmeasured=…`.
rc 0 no DIFF (unmeasured files are named, not failed) · 1 at least one DIFF · 2 usage / measure error. Read-only.
"""
import json
import re
import sys


def same(a, b):
    a = a[2:] if a.startswith(("a/", "b/")) else a
    b = b[2:] if b.startswith(("a/", "b/")) else b
    return a == b or a.endswith("/" + b) or b.endswith("/" + a)


def additions(lines):
    """[(path or None, content)] for every '+' line of a diff text, minus the same-hunk no-op rewrites (docstring)."""
    res, path, hunk_minus, hunk_plus = [], None, [], []

    def flush():
        pool = list(hunk_minus)
        for p, c in hunk_plus:
            if c in pool:
                pool.remove(c)
            else:
                res.append((p, c))
        hunk_minus.clear(); hunk_plus.clear()

    for l in lines:
        if l.startswith("+++ "):
            flush(); path = l[4:].strip(); continue
        if l.startswith("--- ") or l.startswith("@@"):
            flush(); continue
        if l.startswith("+"):
            hunk_plus.append((path, l[1:]))
        elif l.startswith("-"):
            hunk_minus.append(l[1:])
    flush()
    return res


def regions(desc):
    out = []
    for m in re.finditer(r"(?m)^##+\s*(The exact change|The test)\b[^\n]*\n", desc):
        start = m.end()
        nxt = re.search(r"(?m)^##\s", desc[start:])
        out.append((m.group(1), desc[start:start + nxt.start()] if nxt else desc[start:]))
    return out


def main():
    if len(sys.argv) != 3:
        print("usage: brief_bytes.py <input.json> <sections.json>")
        return 2
    try:
        d = json.load(open(sys.argv[1], encoding="utf-8"))
        secs = json.load(open(sys.argv[2], encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 — a measure error is reported, never guessed past
        print(f"MEASURE ERROR: {e!r}")
        return 2
    desc = (d.get("ticket") or {}).get("description") or ""
    products = list(d.get("product_files") or ([d["product_file"]] if d.get("product_file") else []))
    tests = d.get("test_files") or []
    declared = products + [t["path"] for t in tests]
    new = {t["path"] for t in tests if t.get("status") == "new"}
    if not declared:
        print("MEASURE ERROR: the input declares no files (product_files / test_files)")
        return 2

    brief = {}          # declared path -> [lines]
    notes = []
    unattributed = 0
    for name, body in regions(desc):
        last_named = None
        pos = 0
        for fm in re.finditer(r"(?ms)^```[^\n]*\n(.*?)^```[ \t]*$", body):
            between = body[pos:fm.start()]
            for nm in re.finditer(r"(?m)^(?:Test )?[Ff]ile:\s*`([^`]+)`", between):
                last_named = nm.group(1)
            pos = fm.end()
            blk = fm.group(1)
            lines = blk.split("\n")
            if lines and lines[-1] == "":
                lines = lines[:-1]
            if any(l.startswith("+++ ") for l in lines):
                for p in dict.fromkeys(l[4:].strip() for l in lines if l.startswith("+++ ")):
                    if p != "/dev/null" and not any(same(x, p) for x in declared):
                        notes.append(f"INFO the brief's diff names {p}, which is not declared (its lines are not measured here; A3 refuses an undeclared file)")
                for p, c in additions(lines):
                    if p is None:
                        unattributed += 1
                        continue
                    cur = next((x for x in declared if same(x, p)), None)
                    if cur is not None:
                        brief.setdefault(cur, []).append(c)
            else:
                tgt = next((x for x in declared if last_named and same(x, last_named)), None)
                if tgt and tgt in new:
                    if tgt in brief:
                        notes.append(f"INFO a second whole-file block for {tgt} in `## {name}` — appended")
                    brief.setdefault(tgt, []).extend(lines)
                elif last_named:
                    notes.append(f"INFO a non-diff block under `## {name}` follows `{last_named}`, which is not a declared NEW file — not read as content")
                last_named = None

    out = {}
    for s in secs:
        p = s.get("path") or ""
        tgt = next((x for x in declared if p and same(x, p)), None)
        if tgt is None:
            continue
        sec = open(s["file"], encoding="utf-8", errors="surrogateescape").read().split("\n")
        out.setdefault(tgt, []).extend(c for _, c in additions(sec))

    for n in notes:
        print(n)
    if unattributed:
        print(f"INFO {unattributed} '+' line(s) in a brief diff block before any `+++` header — not attributable to a file")
    ok = diff = unm = 0
    for p in declared:
        if p not in brief:
            print(f"UNMEASURED {p} — the brief's `## The exact change` / `## The test` carry no lines attributable to it")
            unm += 1
            continue
        b, o = brief[p], out.get(p, [])
        if b == o:
            print(f"OK {p} {len(b)} '+' line(s) byte-identical to the brief, in order")
            ok += 1
            continue
        i = next((k for k in range(min(len(b), len(o))) if b[k] != o[k]), min(len(b), len(o)))
        bi = repr(b[i][:90]) if i < len(b) else "<none>"
        oi = repr(o[i][:90]) if i < len(o) else "<none>"
        print(f"DIFF {p} brief={len(b)} output={len(o)} '+' line(s); first difference at '+' #{i + 1}: brief={bi} output={oi}")
        diff += 1
    print(f"SUMMARY declared={len(declared)} measured={ok + diff} ok={ok} diff={diff} unmeasured={unm}")
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main())
