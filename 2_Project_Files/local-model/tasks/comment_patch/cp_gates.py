#!/usr/bin/env python3
"""cp_gates.py — the comment_patch tier's shared measure (2026-09-17, HARNESS_WIDEN_PROPOSAL_2026-09-17b §3).

Used by BOTH night/build_comment_input.sh (brief parse + the R8 golden self-check) and tasks/comment_patch/checker.sh
(C4, C4b, C5, C6, C7), so the builder refuses exactly what the checker would fail. Nothing in doc_patch/ or code_patch/
imports it or is imported by it.

CLI:
  cp_gates.py check <input.json> <before file> <after file> <typescript dir>   → PASS/FAIL lines, rc = number failed
  cp_gates.py lines <typescript dir> <file> <name>                             → the token_equiv `lines` JSON

Gates (on BEFORE = the tip file, AFTER = the file with the diff applied):
  C4  token equivalence: every syntax leaf (kind, text) identical, in order — tasks/comment_patch/token_equiv.cjs under the
      given typescript package; an AFTER parse error the BEFORE did not have is a FAIL; an instrument error FAILS (closed)
  C4b directives: the multiset of directive comment lines (@ts-…, eslint…, /// <reference, istanbul/c8 ignore,
      *-environment, prettier-ignore, @jsx…) identical
  C5  region: every changed line (difflib on the tip's positions) lies inside a named range; an insert lands after a range line
  C6  must-remove: every brief '-' line is the tip's line AT its number before, and absent after
  C7  exact adds: every brief '+' line is in AFTER byte-exact (leading whitespace included)
"""
import difflib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_EQUIV = os.path.join(HERE, "token_equiv.cjs")
NODE = os.environ.get("CP_NODE") or next((p for p in ("/opt/homebrew/bin/node", "/usr/local/bin/node") if os.path.exists(p)), "node")


def node_json(args):
    r = subprocess.run([NODE, TOKEN_EQUIV] + args, capture_output=True, text=True)
    try:
        j = json.loads(r.stdout.strip().split("\n")[-1]) if r.stdout.strip() else {}
    except Exception:
        j = {}
    if r.returncode != 0 or "error" in j or not j:
        return None, f"rc={r.returncode} {(j.get('error') if j else '') or r.stderr.strip()[:300] or r.stdout.strip()[:300]}"
    return j, None


def split_lines(text):
    """Lines of a file; a trailing newline does not make an extra line."""
    ls = text.split("\n")
    if ls and ls[-1] == "":
        ls = ls[:-1]
    return ls


# ---------------------------------------------------------------- brief parsing
def section(text, heading_re):
    m = re.search(r"^##+\s*" + heading_re + r"[^\n]*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def parse_diff_sections(diff_text):
    """[{minus_path, plus_path, hunks:[{old_start, old_len, new_start, new_len, body:[lines]}]}]"""
    secs = []
    cur = None
    hunk = None
    for ln in diff_text.split("\n"):
        if ln.startswith("--- "):
            cur = {"minus_path": re.sub(r"^--- (a/)?", "", ln).strip(), "plus_path": None, "hunks": []}
            secs.append(cur); hunk = None
            continue
        if ln.startswith("+++ ") and cur is not None and cur["plus_path"] is None:
            cur["plus_path"] = re.sub(r"^\+\+\+ (b/)?", "", ln).strip()
            continue
        m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", ln)
        if m and cur is not None:
            hunk = {"old_start": int(m.group(1)), "old_len": int(m.group(2) or 1), "new_start": int(m.group(3)),
                    "new_len": int(m.group(4) or 1), "body": []}
            cur["hunks"].append(hunk)
            continue
        if hunk is not None and ln[:1] in (" ", "-", "+"):
            hunk["body"].append(ln)
    return secs


def strict_apply(tip_lines, hunks):
    """Apply hunks by their declared old_start, every context/'-' line byte-exact. Returns (after_lines, minus, plus, err).
    minus = [{line, text, hunk}], plus = [{text, hunk, after_line}]."""
    out = []
    pos = 0  # 0-based index into tip_lines already copied
    minus, plus = [], []
    for hi, h in enumerate(hunks, 1):
        old = [l for l in h["body"] if l[:1] in (" ", "-")]
        new = [l for l in h["body"] if l[:1] in (" ", "+")]
        if (len(old), len(new)) != (h["old_len"], h["new_len"]):
            return None, None, None, f"hunk {hi}: header declares old={h['old_len']} new={h['new_len']} but the body has old={len(old)} new={len(new)}"
        start = h["old_start"] - 1 if h["old_len"] > 0 else h["old_start"]  # a zero-length old side inserts AFTER old_start
        if start < pos:
            return None, None, None, f"hunk {hi}: overlaps the previous hunk"
        out.extend(tip_lines[pos:start]); pos = start
        for l in h["body"]:
            if l[:1] in (" ", "-"):
                n = pos + 1
                if pos >= len(tip_lines) or tip_lines[pos] != l[1:]:
                    got = tip_lines[pos] if pos < len(tip_lines) else "<past EOF>"
                    return None, None, None, f"hunk {hi}: the {'context' if l[0] == ' ' else chr(39) + '-' + chr(39)} line {l[1:][:70]!r} is not the tip's line {n} ({got[:70]!r})"
                if l[0] == "-":
                    minus.append({"line": n, "text": l[1:], "hunk": hi})
                else:
                    out.append(tip_lines[pos])
                pos += 1
            else:
                out.append(l[1:]); plus.append({"text": l[1:], "hunk": hi, "after_line": len(out)})
    out.extend(tip_lines[pos:])
    return out, minus, plus, None


# ---------------------------------------------------------------- gates
def gate_c4(before_path, after_path, ts_dir, name):
    j, err = node_json(["compare", ts_dir, before_path, after_path, name])
    if j is None:
        return [("FAIL", "C4", f"token equivalence INSTRUMENT ERROR — the TypeScript measure could not account for the file(s): {err} (fail closed; the harness, not the model)")], None
    res = []
    new_errs = [e for e in j["parse_errors_after"] if e.split(": ", 1)[-1] not in {x.split(": ", 1)[-1] for x in j["parse_errors_before"]}]
    if new_errs:
        res.append(("FAIL", "C4", f"CODE CHANGED — the file no longer parses as it did: {new_errs[:2]}"))
    elif not j["equal"]:
        fd = j["first_diff"]
        b, a = fd.get("before"), fd.get("after")
        res.append(("FAIL", "C4", "CODE CHANGED — the code-token stream differs at token %d: before %s, after %s (tokens %d → %d)" % (
            fd["index"], f"{b['kind']} {b['text']!r} at tip :{b['line']}" if b else "<end>", f"{a['kind']} {a['text']!r} at after :{a['line']}" if a else "<end>",
            j["n_before"], j["n_after"])))
    else:
        res.append(("PASS", "C4", f"token equivalence: {j['n_before']} code tokens (kind + text, literals included) identical before and after (typescript {j['ts_version']} parser leaves; gaps proven trivia-only)"))
    if j["directives_equal"]:
        res.append(("PASS", "C4b", f"directive comments unchanged ({len(j['directives_before'])} before, {len(j['directives_after'])} after)"))
    else:
        bt = sorted(d["text"] for d in j["directives_before"]); at = sorted(d["text"] for d in j["directives_after"])
        gone = [t for t in bt if bt.count(t) > at.count(t)]; new = [t for t in at if at.count(t) > bt.count(t)]
        res.append(("FAIL", "C4b", f"DIRECTIVE CHANGED — removed/altered: {sorted(set(gone))[:3]}; added/altered: {sorted(set(new))[:3]} (a lint/type directive is behaviour, not prose)"))
    return res, j


def gate_c5(before, after, ranges):
    bad = []
    sm = difflib.SequenceMatcher(None, before, after, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag in ("replace", "delete"):
            outside = [n for n in range(i1 + 1, i2 + 1) if not any(a <= n <= b for a, b in ranges)]
            if outside:
                bad.append(f"{tag} tip :{i1 + 1}-{i2} (outside: {outside[:4]})")
        else:  # insert after tip line i1
            if not any(a <= i1 <= b for a, b in ranges):
                bad.append(f"insert after tip :{i1} ({after[j1][:50]!r})")
    rs = ", ".join(f":{a}-{b}" for a, b in ranges)
    if bad:
        return [("FAIL", "C5", f"CHANGE OUTSIDE THE NAMED LINES ({rs}): {bad[:3]}")]
    return [("PASS", "C5", f"every changed line lies inside the named lines ({rs})")]


def gate_c6(before, after, must_remove):
    if not must_remove:
        return [("INFO", "C6", "no brief '-' lines (an insert-only brief)")]
    ctrl = [m for m in must_remove if not (0 < m["line"] <= len(before) and before[m["line"] - 1] == m["text"])]
    if ctrl:
        return [("FAIL", "C6", f"control: {len(ctrl)} brief '-' line(s) are not the tip's line at their number (the input is wrong): {[(m['line'], m['text'][:50]) for m in ctrl[:2]]}")]
    still = [m for m in must_remove if m["text"] in after]
    if still:
        return [("FAIL", "C6", f"OLD LINE KEPT — {len(still)} of {len(must_remove)} brief '-' line(s) still present after: {[(m['line'], m['text'][:60]) for m in still[:3]]}")]
    return [("PASS", "C6", f"every brief '-' line ({len(must_remove)}) is the tip's line at its number and absent after")]


def gate_c7(after, expected_plus):
    if not expected_plus:
        return [("INFO", "C7", "no brief '+' lines")]
    miss = [p for p in expected_plus if p not in after]
    if miss:
        return [("FAIL", "C7", f"ADDITION ALTERED — {len(miss)} of {len(expected_plus)} brief '+' line(s) not in the file after, byte-exact: {[m[:70] for m in miss[:3]]}")]
    return [("PASS", "C7", f"every brief '+' line ({len(expected_plus)}) is in the file after, byte-exact")]


def run_gates(before_path, after_path, ts_dir, name, ranges, must_remove, expected_plus):
    before = split_lines(open(before_path, encoding="utf-8").read())
    after = split_lines(open(after_path, encoding="utf-8").read())
    res, _ = gate_c4(before_path, after_path, ts_dir, name)
    res += gate_c5(before, after, ranges)
    res += gate_c6(before, after, must_remove)
    res += gate_c7(after, expected_plus)
    return res


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "check" and len(sys.argv) == 6:
        inp = json.load(open(sys.argv[2], encoding="utf-8"))
        c = inp["comment"]
        res = run_gates(sys.argv[3], sys.argv[4], sys.argv[5], os.path.basename(inp["product_file"]),
                        [tuple(r) for r in c["ranges"]], c["must_remove"], c["expected_plus"])
        nf = 0
        for st, g, msg in res:
            print(f"{st} {g} {msg}")
            nf += st == "FAIL"
        sys.exit(min(nf, 50))
    if len(sys.argv) >= 2 and sys.argv[1] == "lines" and len(sys.argv) == 5:
        j, err = node_json(["lines", sys.argv[2], sys.argv[3], sys.argv[4]])
        if j is None:
            print(json.dumps({"error": err})); sys.exit(3)
        print(json.dumps(j)); sys.exit(0)
    sys.stderr.write(__doc__); sys.exit(2)


if __name__ == "__main__":
    main()
