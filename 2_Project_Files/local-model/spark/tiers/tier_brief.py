#!/usr/bin/env python3
"""tier_brief.py — brief parsing shared by brief_lint.py, build_tier_input.py and tier_checker.py for the two tiers
added 2026-10-31 (test_only_input, doc_only). Pure functions, stdlib only, no I/O beyond reading a brief file.

Brief blocks (all values are inside backticks so indentation and spaces survive; a value is everything between the
FIRST and the LAST backtick of its line):

  ## Plant            (test_only_input; or a `golden_red.diff` file in the brief dir — exactly one of the two)
  file: `<repo path>`        a group starts at each `file:` line
  line: <N>                  1-based line at the tip
  from: `<the exact line at the tip>`
  to:   `<the mutated line>`

  ## Red cells        (test_only_input) one bullet per cell:   - `<substring of the cell's full name>`

  ## Expect           (doc_only)  expect_absent: `<text>` [in `<repo path>`]   (>= 1 required)
                                  expect_present: `<text>` [in `<repo path>`]
  ## Expect           (test_only_bash, the no-plant shape) the same lines, graded against the declared bash suite's OUTPUT
  ## Doc checks       (doc_only, optional)  one bullet per extra command:   - `node path/to/check.mjs`
"""
import re

COMMENT_C = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}
COMMENT_HASH = {".sh", ".bash", ".py", ".yml", ".yaml"}


def section(text, name):
    """Body of the first `## <name>` heading (case-insensitive, a following word boundary), up to the next `## `."""
    m = re.search(r"^##+\s*" + name + r"\b[^\n]*\n(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else None


def tick(s):
    """The text between the first and last backtick of s, or None."""
    a, b = s.find("`"), s.rfind("`")
    return s[a + 1:b] if a != -1 and b > a else None


def parse_plant(text):
    """-> (groups, errors). groups = [{file,line,from,to}]; None body -> ([], [])."""
    body = section(text, "Plant")
    if body is None:
        return [], []
    groups, errs, cur = [], [], None
    for raw in body.split("\n"):
        m = re.match(r"^\s*(file|line|from|to)\s*:\s*(.*)$", raw, re.I)
        if not m:
            continue
        k, v = m.group(1).lower(), m.group(2)
        if k == "file":
            cur = {"file": tick(v)}
            groups.append(cur)
            if cur["file"] is None:
                errs.append("`file:` needs the path in backticks")
            continue
        if cur is None:
            errs.append(f"`{k}:` before any `file:` line")
            continue
        if k == "line":
            mm = re.match(r"^\s*(\d+)\s*$", v)
            cur["line"] = int(mm.group(1)) if mm else None
            if not mm:
                errs.append("`line:` must be a bare integer")
        else:
            t = tick(v)
            if t is None:
                errs.append(f"`{k}:` needs its text in backticks")
            cur[k] = t
    for i, g in enumerate(groups, 1):
        for k in ("file", "line", "from", "to"):
            if g.get(k) in (None, "") and not (k == "to" and g.get(k) == ""):
                errs.append(f"plant group {i} lacks `{k}:`")
        if g.get("from") is not None and g.get("from") == g.get("to"):
            errs.append(f"plant group {i}: `to:` equals `from:` — a plant that changes nothing")
    if body is not None and not groups:
        errs.append("`## Plant` has no `file:` group")
    return groups, errs


def parse_red_cells(text):
    body = section(text, "Red cells")
    if body is None:
        return None
    cells = []
    for raw in body.split("\n"):
        m = re.match(r"^\s*[-*]\s*(.*)$", raw)
        if m:
            t = tick(m.group(1))
            if t:
                cells.append(t)
    return cells


def parse_expect(text):
    """-> (items, errors) ; item = {kind: present|absent, text, path|None}; body None -> (None, [])."""
    body = section(text, "Expect")
    if body is None:
        return None, []
    items, errs = [], []
    for raw in body.split("\n"):
        m = re.match(r"^\s*(?:[-*]\s*)?(expect_present|expect_absent)\s*:\s*(.*)$", raw, re.I)
        if not m:
            continue
        kind = m.group(1).lower().split("_")[1]
        rest = m.group(2)
        mi = re.match(r"^(.*`)\s+in\s+`([^`]+)`\s*$", rest)
        path = None
        if mi:
            rest, path = mi.group(1), mi.group(2)
        t = tick(rest)
        if not t:
            errs.append(f"expect_{kind}: needs its text in backticks")
            continue
        items.append({"kind": kind, "text": t, "path": path})
    return items, errs


def parse_doc_checks(text):
    body = section(text, "Doc checks")
    out = []
    for raw in (body or "").split("\n"):
        m = re.match(r"^\s*[-*]\s*(.*)$", raw)
        if m:
            t = tick(m.group(1))
            if t:
                out.append(t)
    return out


def header_files(text):
    """(products, tests) from the lines before the first `## `."""
    header = re.split(r"(?m)^##\s", text, maxsplit=1)[0]
    return (re.findall(r"(?m)^File:\s*`([^`]+)`", header),
            re.findall(r"(?im)^Test[^:\n`]*:\s*`([^`]+)`", header))


def is_bash_suite_path(p):
    """test_only_bash (2026-11-09): a declared test must be a bash suite — `*.test.sh`, or a `.sh`/`.bash` under a `__tests__` dir."""
    return p.endswith(".test.sh") or ("/__tests__/" in p and p.endswith((".sh", ".bash")))


def is_doc_path(p):
    return p.lower().endswith(".md") or "Projects Documents/fragments/" in p


def comment_kind(p):
    """'c' | 'hash' | None for a code path whose comment-only edits doc_only can verify."""
    ext = "." + p.rsplit(".", 1)[-1].lower() if "." in p.rsplit("/", 1)[-1] else ""
    return "c" if ext in COMMENT_C else ("hash" if ext in COMMENT_HASH else None)


def comment_lines(src, kind):
    """-> [bool per line]: True when the line is NOTHING but comment (a whole-line comment, or a line wholly inside a
    block comment). Blank lines outside a block comment are False (a blank line is not a comment line). kind 'hash':
    a line whose first non-blank char is `#` (a shebang `#!` is NOT a comment line). kind 'c': a small state machine
    over '...' "..." `...` strings, // and /* */ comments. Regex literals are not modelled (documented limit): a `'`
    or backtick inside one can desync the string state; a desync can only mislabel lines AFTER it in that file, and
    the checker compares the labels of the base and patched file, so a one-sided desync shows as a refusal."""
    lines = src.split("\n")
    if kind == "hash":
        return [bool(re.match(r"^\s*#(?!!)", l)) for l in lines]
    res = []
    in_block = False
    in_tpl = False
    for l in lines:
        i, n = 0, len(l)
        had_code = False
        had_comment = in_block
        in_str = None
        while i < n:
            c = l[i]
            if in_block:
                j = l.find("*/", i)
                if j == -1:
                    i = n
                else:
                    in_block = False
                    i = j + 2
                continue
            if in_tpl:
                had_code = True
                if c == "\\":
                    i += 2
                    continue
                if c == "`":
                    in_tpl = False
                i += 1
                continue
            if in_str:
                had_code = True
                if c == "\\":
                    i += 2
                    continue
                if c == in_str:
                    in_str = None
                i += 1
                continue
            if c.isspace():
                i += 1
                continue
            if l.startswith("//", i):
                had_comment = True
                i = n
                continue
            if l.startswith("/*", i):
                had_comment = True
                in_block = True
                i += 2
                continue
            if c in ("'", '"'):
                in_str = c
            elif c == "`":
                in_tpl = True
            had_code = True
            i += 1
        res.append(had_comment and not had_code)
    return res


# ---------------------------------------------------------------- 2026-11-11 DECLARED-RENAME allowance (commission 2026-11-11_harness-declared-rename)
#   ## Renames     (any tier whose A6 compares cells; OPT-IN — a brief without the block is graded exactly as before)
#   - `<old cell full name>` -> `<new cell full name>`     one exact pair per bullet, one-to-one, no wildcard
# A cell's full name is what the checker's report prints for it: vitest/jest fullName; bash `<suite basename> :: <label>`.
def parse_renames(text):
    """-> (pairs|None, errors). None = no `## Renames` block (the default; nothing changes). Pairs are [old, new] lists."""
    body = section(text, "Renames")
    if body is None:
        return None, []
    pairs, errs, olds, news = [], [], set(), set()
    for raw in body.split("\n"):
        m = re.match(r"^\s*[-*]\s*(.*)$", raw)
        if not m:
            continue
        mm = re.match(r"^`(.+?)`\s*(?:->|→)\s*`(.+)`\s*$", m.group(1).strip())
        if not mm:
            errs.append(f"RENAMES: bullet {m.group(1).strip()[:80]!r} is not exactly - `old cell full name` -> `new cell full name`")
            continue
        old, new = mm.group(1), mm.group(2)
        if any(w in x for x in (old, new) for w in ("*", "…", "...")):
            errs.append(f"RENAMES: {old[:50]!r} -> {new[:50]!r} contains a wildcard (`*`, `...`); a declaration names exact cells")
            continue
        if old == new:
            errs.append(f"RENAMES: {old[:60]!r} -> itself is not a rename")
            continue
        if old in olds or new in news or old in news or new in olds:
            errs.append(f"RENAMES: {old[:50]!r} -> {new[:50]!r} is not one-to-one (a name appears in two pairs)")
            continue
        olds.add(old)
        news.add(new)
        pairs.append([old, new])
    if not pairs and not errs:
        errs.append("RENAMES: the `## Renames` block has no `- `old` -> `new`` bullet (delete the heading if nothing is renamed)")
    return pairs, errs


def check_renames(renames, base_status, after_status):
    """Grade declared pairs against the measured cells. base_status/after_status: {full name: 'passed'|'failed'|...}.
    -> (valid_pairs, error strings). A pair is valid only when the old cell WAS in the baseline and is GONE after, and the
    new cell was NOT in the baseline and is PRESENT and PASSING after. Anything else is an error (FAIL)."""
    valid, errs = [], []
    for old, new in renames or []:
        bad = []
        if old not in base_status:
            bad.append("old cell was never in the baseline (a declaration cannot launder a typo)")
        elif old in after_status:
            bad.append("old cell is still present after the patch (not a rename)")
        if new in base_status:
            bad.append("new cell already existed in the baseline (not a rename)")
        if new not in after_status:
            bad.append("new cell is absent after the patch")
        elif after_status[new] != "passed":
            bad.append(f"new cell is {after_status[new]}, it must pass")
        if bad:
            errs.append(f"declared rename {old[:70]!r} -> {new[:70]!r}: " + "; ".join(bad))
        else:
            valid.append([old, new])
    return valid, errs
