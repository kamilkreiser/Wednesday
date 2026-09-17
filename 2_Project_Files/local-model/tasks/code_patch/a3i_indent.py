#!/usr/bin/env python3
"""a3i_indent.py <input.json> <clone> <section.diff> <target repo path> [git apply opts ...]

A3i INDENT-EXACT (2026-09-17, KS-623 r1, IMPROVEMENTS row 2026-09-17 13:10): the model shifted EVERY line of its
product hunk right by 2 spaces; strict and lenient apply refused it, FUZZY (-C1, which carries --ignore-whitespace)
applied it, and the brief's `+` line landed at 4-space indent inside a 2-space block. A3c compares whitespace-STRIPPED
text, so it passed, and so did the suite and tsc. For TS that is lint; for Python/YAML/Makefile it changes meaning.

Rule: every brief `+` line must be in the APPLIED target file byte-exact INCLUDING its leading whitespace.

Where the exact lines come from: the builder stores `defect_line.expected_plus` STRIPPED (build_input.sh:
`expected_plus.append(ln[1:].strip())`), so the indent is not in that list. The brief text itself IS in the input:
build_input.sh puts the whole brief in `ticket.description` when night/briefs/<ticket>.md exists. This helper
re-parses that text with the builder's own `## The exact change` regexes and keeps `ln[1:]` UNSTRIPPED. It uses the
result only when its stripped form equals `expected_plus` exactly, in order; otherwise it cannot know which lines the
builder meant, and it SKIPS (rc 5, one INFO line). An input with no expected_plus also skips: legacy behaviour kept.

How "applied" is measured (the a3b_line.py pattern): the tip's target file is written into a fresh temp dir OUTSIDE
any git repository, and the section is applied there with the SAME opts the checker recorded (strict / --recount
--ignore-whitespace / -C1 / the reanchored file). `git diff --no-index -U0` then names the lines the apply ADDED. The
clone is only READ (`git show <tip>:<target>`). For a `--- /dev/null` section every line counts as added.

Content equivalence is A3c's (a3c_plus.py) and nothing looser: the stripped text is equal, or equal once the applied
line's trailing ` // …` comment is removed, with `\\uXXXX` escapes decoded. A3i adds ONE dimension, leading
whitespace. It never passes content that A3c refuses and never fails content that A3c accepts. It is not a prefix
match: `  if (x) { y(); }` does not satisfy a brief `  if (x) {`.

Matching per brief line, in brief order, consuming lines so duplicates are counted (KS-1186 has four identical ones):
  1. an unconsumed ADDED line with equal content AND the same leading whitespace (byte-exact) → ok
  2. else an unconsumed ADDED line with equal content but different leading whitespace → SHIFT (that line)
  3. else no added line carries it (the tip already has that exact line, so the diff did not add it): an exact line
     anywhere in the applied file → ok; otherwise NOTADDED (INFO only: that is A3c's territory, and A3c passed)
Trailing whitespace is not gated (A3c strips it; git would show it as a change anyway).

Prints:
  SHIFT :<n> observed=<w> expected=<v> delta=<+/-d> `<text>`   (n = the line number in the APPLIED file)
  NOTADDED `<text>`
  OK <k> line(s) byte-exact incl. leading whitespace
  INFO <why skipped>
rc 0 all exact · 1 at least one SHIFT · 5 skipped (no recoverable exact lines) · 2 measure error.
Arms: local-model/tests/a3i_indent_arms.sh.
"""
import json, os, re, subprocess, sys, tempfile

_TRAIL = re.compile(r"\s+//[^\n]*$")
_UESC = re.compile(r"\\u([0-9a-fA-F]{4})")


def _unescape(line):
    return _UESC.sub(lambda m: chr(int(m.group(1), 16)), line)


def _norm(line):
    return _unescape(line).strip()


def _nocomment(line):
    return _TRAIL.sub("", _unescape(line)).strip()


def _same_content(applied, brief_stripped):
    # A3c's relation, applied-line side only (the expectation is never rewritten)
    return _norm(applied) == brief_stripped or _nocomment(applied) == brief_stripped


def _lead(s):
    return s[: len(s) - len(s.lstrip(" \t"))]


def _width(ws):
    return f"{len(ws)}" + (" (tab)" if "\t" in ws else "")


def exact_plus_lines(d):
    """The brief's '+' lines with their leading whitespace, or (None, why)."""
    exp = (d.get("defect_line") or {}).get("expected_plus") or []
    if not exp:
        return None, "the input carries no expected '+' lines (a legacy or brief-less input)"
    desc = (d.get("ticket") or {}).get("description") or ""
    # the builder's own regexes (night/build_input.sh, expected_plus block)
    mx = re.search(r"^##+\s*The exact change\b.*?$(.*?)(?=^##+\s|\Z)", desc, re.M | re.S)
    if not mx:
        return None, "the input's ticket.description has no `## The exact change` section, so the brief's indentation cannot be recovered"
    raw = []
    for blk in re.findall(r"^```[^\n]*\n(.*?)^```", mx.group(1), re.M | re.S):
        for ln in blk.split("\n"):
            if ln.startswith("+") and not ln.startswith("+++") and ln[1:].strip():
                raw.append(ln[1:].rstrip("\r"))
    if [r.strip() for r in raw] != [e for e in exp]:
        return None, (f"the '+' lines re-parsed from ticket.description ({len(raw)}) are not the input's expected_plus "
                      f"({len(exp)}) — the description is not the brief the input was built from")
    return raw, ""


def main():
    if len(sys.argv) < 5:
        print(__doc__.split("\n")[0]); return 2
    inp, clone, section, target = sys.argv[1:5]
    opts = [w for o in sys.argv[5:] for w in o.split()]  # one string or many: the recorded opts line, word-split
    d = json.load(open(inp, encoding="utf-8"))
    raw, why = exact_plus_lines(d)
    if raw is None:
        print("INFO " + why); return 5
    if not section or not os.path.isfile(section) or os.path.getsize(section) == 0:
        print(f"MEASURE ERROR: no section file for {target} ({section!r})"); return 2
    sec_text = open(section, encoding="utf-8", errors="replace").read()
    new_file = sec_text.startswith("--- /dev/null") or "\n--- /dev/null" in sec_text.split("@@", 1)[0]
    tip_bytes = b""
    if not new_file:
        r = subprocess.run(["git", "-C", clone, "show", f"{d['tip']}:{target}"], capture_output=True)
        if r.returncode != 0:
            print(f"MEASURE ERROR: git show {d['tip'][:9]}:{target} rc={r.returncode}: {r.stderr.decode(errors='replace')[:200]}"); return 2
        tip_bytes = r.stdout
    tmp = tempfile.mkdtemp(prefix="a3i_indent.")
    # quarantine, never delete: the temp dir holds only a tip copy + the patched copy; the OS temp reaper takes it
    dst = os.path.join(tmp, "tree", target)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not new_file:
        open(dst, "wb").write(tip_bytes)
    tipcopy = os.path.join(tmp, "tip_copy")
    open(tipcopy, "wb").write(tip_bytes)
    env = dict(os.environ, GIT_CEILING_DIRECTORIES=tmp)
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(k, None)
    a = subprocess.run(["git", "apply", "-p1", *opts, os.path.abspath(section)], cwd=os.path.join(tmp, "tree"),
                       capture_output=True, env=env)
    if a.returncode != 0:
        print(f"MEASURE ERROR: the section did not apply to a copy of the tip (opts {opts}): {a.stderr.decode(errors='replace')[:300]}"); return 2
    if not os.path.isfile(dst):
        print(f"MEASURE ERROR: the apply did not produce {target} in the temp tree (a path/--directory mismatch?)"); return 2
    applied = open(dst, "rb").read().decode("utf-8", errors="replace").split("\n")
    added = set()
    if new_file:
        added = set(range(1, len(applied) + 1))
    else:
        g = subprocess.run(["git", "diff", "--no-index", "--no-color", "-U0", tipcopy, dst], capture_output=True, env=env, cwd=tmp)
        if g.returncode not in (0, 1):
            print(f"MEASURE ERROR: git diff --no-index rc={g.returncode}: {g.stderr.decode(errors='replace')[:200]}"); return 2
        for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", g.stdout.decode("utf-8", errors="replace"), re.M):
            start = int(m.group(1)); cnt = int(m.group(2)) if m.group(2) is not None else 1
            added.update(range(start, start + cnt))
    used = set(); shifts = []; notadded = []; ok = 0
    for e in raw:
        es = e.strip(); ew = _lead(e)
        cands = [n for n in sorted(added) if n not in used and 1 <= n <= len(applied) and _same_content(applied[n - 1], es)]
        exact = [n for n in cands if _lead(applied[n - 1]) == ew]
        if exact:
            used.add(exact[0]); ok += 1; continue
        if cands:
            n = cands[0]; used.add(n); ow = _lead(applied[n - 1])
            shifts.append(f"SHIFT :{n} observed={_width(ow)} expected={_width(ew)} delta={len(ow) - len(ew):+d} `{es[:90]}`")
            continue
        if any(_lead(l) == ew and _same_content(l, es) for l in applied):
            ok += 1; continue
        notadded.append(f"NOTADDED `{es[:90]}`")
    for s in shifts + notadded:
        print(s)
    print(f"OK {ok} line(s) byte-exact incl. leading whitespace (of {len(raw)}; {len(added)} line(s) added by the apply)")
    return 1 if shifts else 0


if __name__ == "__main__":
    sys.exit(main())
