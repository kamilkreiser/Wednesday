#!/usr/bin/env python3
"""spark_check.py - assert the six checker clauses (spark-kit 05 "What a checker must assert").

Usage:
  spark_check.py --brief-json <expect.json> --diff <file.diff> --repo <git working copy> --out <evidence dir>

expect.json:
  commit            sha the diff must apply to
  files             EXACT list of repo-relative paths the diff may touch
  expected_added    {path: [exact added line, ...]}  (in order, no leading '+')
  red_test_cmd      shell cmd (repo root) that PASSES with the diff, FAILS reverted; null -> C4 NOT-RUN
  suite_cmd         shell cmd for the wider suite, run at base and after; null -> C5 NOT-RUN
  suite_count_regex optional python regex with named groups `passed` (and optionally `failed`)

Output: one line per clause `Cn: PASS|FAIL|NOT-RUN — detail`, then `VERDICT: PASS|FAIL|INCOMPLETE`.
Exit: 0 PASS, 1 FAIL, 2 INCOMPLETE (a NOT-RUN clause, none failed), 3 setup error.

The source working copy is never modified: work happens in a fresh clone in the system temp dir (path in 00_clone_location.txt).
Nothing is deleted. Python 3 stdlib only.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

CMD_TIMEOUT = 600


class Evidence(object):
    def __init__(self, out_dir):
        self.out_dir = out_dir
        self.n = 0
        self.expected = []  # every file we promised to write

    def run(self, label, cmd, cwd, shell=False):
        """Run a command, save cmd/rc/stdout/stderr to a numbered file, return (rc, stdout, stderr)."""
        self.n += 1
        name = "%02d_%s.txt" % (self.n, re.sub(r"[^A-Za-z0-9_.-]+", "_", label))
        path = os.path.join(self.out_dir, name)
        self.expected.append(path)
        t0 = time.time()
        timed_out = False
        try:
            # PYTHONDONTWRITEBYTECODE: a same-size edit applied within the same second as a
            # previous run would otherwise be masked by a stale __pycache__ .pyc (seen in self-test).
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            p = subprocess.run(cmd, cwd=cwd, shell=shell, capture_output=True, timeout=CMD_TIMEOUT, env=env)
            rc, so, se = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            timed_out = True
            rc = 124
            so = e.stdout or b""
            se = (e.stderr or b"") + ("\n[spark_check] TIMEOUT after %ds\n" % CMD_TIMEOUT).encode()
        dt = time.time() - t0
        shown = cmd if isinstance(cmd, str) else " ".join(_q(c) for c in cmd)
        with open(path, "wb") as f:
            f.write(("# label: %s\n# cwd: %s\n# cmd: %s\n# rc: %d%s\n# seconds: %.2f\n"
                     % (label, cwd, shown, rc, " (TIMEOUT)" if timed_out else "", dt)).encode())
            f.write(b"# ---- stdout ----\n")
            f.write(so)
            f.write(b"\n# ---- stderr ----\n")
            f.write(se)
            f.write(b"\n")
        return rc, so.decode("utf-8", "replace"), se.decode("utf-8", "replace"), name


def _q(s):
    return s if re.match(r"^[A-Za-z0-9_./:=@+-]+$", s) else "'" + s.replace("'", "'\\''") + "'"


# ---------------------------------------------------------------- diff parsing
def _strip_path(p):
    p = p.split("\t", 1)[0].strip()
    if p.startswith('"') and p.endswith('"'):
        p = p[1:-1]
    if p == "/dev/null":
        return None
    if p.startswith("a/") or p.startswith("b/"):
        p = p[2:]
    return p


def parse_diff(text):
    """Return (touched_set, added: {path: [lines]}, removed: {path: n}, problems: [str]).

    A file header is a `--- ` line IMMEDIATELY followed by a `+++ ` line; everything else inside a
    file section is content, so an added line that itself starts with '++' is still counted.
    Hunk header counts are deliberately NOT trusted here (C1 judges them)."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    touched = set()
    added = {}
    removed = {}
    problems = []
    cur = None
    in_hunk = False
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("--- ") and i + 1 < len(lines) and lines[i + 1].startswith("+++ "):
            old = _strip_path(ln[4:])
            new = _strip_path(lines[i + 1][4:])
            for p in (old, new):
                if p is not None:
                    touched.add(p)
            if old is not None and new is not None and old != new:
                problems.append("header renames %r -> %r" % (old, new))
            cur = new if new is not None else old
            added.setdefault(cur, [])
            removed.setdefault(cur, 0)
            in_hunk = False
            i += 2
            continue
        if ln.startswith("diff --git ") or ln.startswith("index ") or ln.startswith("new file mode") \
                or ln.startswith("deleted file mode") or ln.startswith("similarity index") \
                or ln.startswith("rename from ") or ln.startswith("rename to "):
            if ln.startswith("rename ") or ln.startswith("new file mode") or ln.startswith("deleted file mode"):
                problems.append("git extended header: %r" % ln)
            in_hunk = False
            i += 1
            continue
        if ln.startswith("@@"):
            in_hunk = True
            i += 1
            continue
        if in_hunk and cur is not None and ln.startswith("+"):
            added[cur].append(ln[1:])
        elif in_hunk and cur is not None and ln.startswith("-"):
            removed[cur] += 1
        i += 1
    return touched, added, removed, problems


def with_git_headers(text):
    """Insert a `diff --git a/P b/P` separator before every `--- `/`+++ ` file-header pair.

    Used ONLY for the --recount attempt: git's --recount scans hunk bodies until a line that is not
    ' ', '+', '-' or '\\', so in a multi-file diff WITHOUT `diff --git` lines it swallows the next
    `--- a/...` header as a removal and reports 'patch does not apply' (found in self-test). The
    content is unchanged; the normalised copy is kept as evidence."""
    lines = text.split("\n")
    out = []
    for i, ln in enumerate(lines):
        if (ln.startswith("--- ") and i + 1 < len(lines) and lines[i + 1].startswith("+++ ")
                and not (out and out[-1].startswith("index ")) and not (out and out[-1].startswith("diff --git "))):
            old = _strip_path(ln[4:])
            new = _strip_path(lines[i + 1][4:])
            p_old = old if old is not None else new
            p_new = new if new is not None else old
            out.append("diff --git a/%s b/%s" % (p_old, p_new))
        out.append(ln)
    return "\n".join(out)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brief-json", required=True)
    ap.add_argument("--diff", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    def die(msg):
        print("SETUP ERROR: %s" % msg)
        return 3

    for p, what in ((a.brief_json, "expect.json"), (a.diff, "diff")):
        if not os.path.isfile(p):
            return die("%s not found: %r" % (what, p))
    if not os.path.isdir(a.repo):
        return die("repo not found: %r" % a.repo)
    try:
        with open(a.brief_json, "r", encoding="utf-8") as f:
            exp = json.load(f)
    except Exception as e:
        return die("cannot read expect.json: %r" % e)
    for k in ("commit", "files", "expected_added"):
        if k not in exp:
            return die("expect.json missing required field %r" % k)
    for k in ("red_test_cmd", "suite_cmd"):
        if k not in exp:
            return die("expect.json missing field %r (use null to mean NOT-RUN explicitly)" % k)
    if not isinstance(exp["files"], list) or not isinstance(exp["expected_added"], dict):
        return die("`files` must be a list and `expected_added` an object")
    count_re = None
    if exp.get("suite_count_regex"):
        try:
            count_re = re.compile(exp["suite_count_regex"], re.M)
        except re.error as e:
            return die("bad suite_count_regex: %s" % e)
        if "passed" not in count_re.groupindex:
            return die("suite_count_regex must have a named group `passed`")

    out_dir = os.path.abspath(a.out)
    # The throwaway clone lives in the SYSTEM TEMP dir, never in the evidence dir: the evidence dir sits in a synced
    # tree, and one full clone per check reached 2.3 GB in six checks (Friday, 2026-09-23). Its path is recorded.
    import tempfile
    wc = os.path.join(tempfile.mkdtemp(prefix="spark_wc_"), "wc")
    if os.path.exists(wc):
        return die("%r already exists - use a fresh evidence dir (nothing is ever deleted)" % wc)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "00_clone_location.txt"), "w") as _f: _f.write(wc + "\n")
    ev = Evidence(out_dir)

    # keep the exact inputs next to the evidence
    diff_copy = os.path.join(out_dir, "input.diff")
    shutil.copyfile(a.diff, diff_copy)
    shutil.copyfile(a.brief_json, os.path.join(out_dir, "input_expect.json"))
    ev.expected += [diff_copy, os.path.join(out_dir, "input_expect.json")]
    with open(diff_copy, "rb") as f:
        diff_text = f.read().decode("utf-8", "surrogateescape")

    res = {}  # clause -> (status, detail)

    # ---- throwaway clone at the known commit --------------------------------
    rc, _, se, _ = ev.run("clone", ["git", "clone", "--quiet", "--no-hardlinks",
                                    os.path.abspath(a.repo), wc], cwd=out_dir)
    if rc != 0:
        return die("git clone failed: %s" % se.strip())
    rc, _, se, _ = ev.run("checkout_commit", ["git", "-C", wc, "checkout", "-q", exp["commit"]], cwd=out_dir)
    if rc != 0:
        return die("cannot check out commit %s in clone: %s" % (exp["commit"], se.strip()))
    rc, so, se, _ = ev.run("rev_parse_head", ["git", "-C", wc, "rev-parse", "HEAD"], cwd=out_dir)
    head = so.strip().lower()
    if rc != 0 or not head.startswith(str(exp["commit"]).lower()):
        return die("clone HEAD %r != expected commit %r" % (head, exp["commit"]))

    # ---- C1 apply ------------------------------------------------------------
    rc_s, _, se_s, f_s = ev.run("C1_apply_check_strict", ["git", "apply", "--check", "-v", diff_copy], cwd=wc)
    mode = None
    recount_copy = os.path.join(out_dir, "input.recount.diff")  # diff --git separators added, content identical
    if rc_s == 0:
        mode = "strict"
        res["C1"] = ("PASS", "applies STRICT at %s (evidence %s)" % (head[:12], f_s))
        # ANCHOR CHECK (Friday, 2026-09-23 smoke break 2): git apply relocates a hunk by searching for its context,
        # so a header naming a line that does not exist ('@@ -902,3' on a 17-line file) still applied 'strict'.
        # Clause 1 means the diff applies AT THE STATED LINES: every hunk's old side (context + '-') must sit at
        # exactly the header's start line in the file at the pinned commit.
        anchor_lines, anchor_bad = [], []
        cur_path = None
        dl = diff_text.split("\n")
        i = 0
        while i < len(dl):
            l = dl[i]
            if l.startswith("--- "):
                src = l[4:].split("\t")[0].strip()
                cur_path = None if src == "/dev/null" else _strip_path(src)
            m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@", l)
            if m and cur_path:
                start = int(m.group(1)); old_side = []
                j = i + 1
                while j < len(dl) and not dl[j].startswith("@@") and not dl[j].startswith("--- "):
                    if dl[j].startswith(" ") or dl[j].startswith("-"): old_side.append(dl[j][1:])
                    elif dl[j] == "": pass
                    j += 1
                rc_f, so_f, _, _ = ev.run("C1_anchor_show_%d" % start, ["git", "show", "%s:%s" % (head, cur_path)], cwd=wc)
                flines = so_f.split("\n")
                at = flines[start - 1:start - 1 + len(old_side)] if start >= 1 else []
                if at == old_side:
                    anchor_lines.append("OK   %s hunk @-%d: old side (%d lines) is at line %d" % (cur_path, start, len(old_side), start))
                else:
                    found = next((k + 1 for k in range(len(flines)) if flines[k:k + len(old_side)] == old_side), None)
                    anchor_bad.append("%s hunk @-%d: old side NOT at line %d (file has %d lines); %s"
                                      % (cur_path, start, start, len(flines) - (1 if flines and flines[-1] == "" else 0),
                                         ("content actually at line %d - git applied it by context search" % found) if found else "content not found anywhere"))
                    anchor_lines.append("BAD  " + anchor_bad[-1])
                i = j; continue
            i += 1
        anchor_file = os.path.join(out_dir, "C1_anchor_check.txt")
        with open(anchor_file, "w") as f: f.write("\n".join(anchor_lines) + "\n")
        ev.expected.append(anchor_file)
        if anchor_bad:
            res["C1"] = ("FAIL", "applies only by git's context search, NOT at the stated lines: %s (evidence %s)"
                         % (anchor_bad[0], anchor_file))
            mode = "strict-offset"
    else:
        with open(recount_copy, "w", encoding="utf-8", errors="surrogateescape") as f:
            f.write(with_git_headers(diff_text))
        ev.expected.append(recount_copy)
        rc_r, _, se_r, f_r = ev.run("C1_apply_check_recount",
                                    ["git", "apply", "--check", "-v", "--recount", recount_copy], cwd=wc)
        if rc_r == 0:
            mode = "recount-only"
            res["C1"] = ("FAIL", "applies ONLY with --recount (hunk header miscounted) (evidence %s, %s)"
                         % (f_s, f_r))
        else:
            mode = "none"
            first_err = (se_r.strip() or se_s.strip()).splitlines()
            res["C1"] = ("FAIL", "does NOT apply at %s, strict or --recount: %s (evidence %s, %s)"
                         % (head[:12], first_err[-1] if first_err else "?", f_s, f_r))
    apply_flags = ["--recount"] if mode == "recount-only" else []
    patch_file = recount_copy if mode == "recount-only" else diff_copy

    # ---- C2 / C3 on the diff text (no apply needed) --------------------------
    touched, added, removed, problems = parse_diff(diff_text)
    want = set(exp["files"])
    if touched == want and not problems:
        res["C3"] = ("PASS", "touched set == %s" % sorted(want))
    else:
        bits = []
        if touched - want:
            bits.append("UNNAMED files touched: %s" % sorted(touched - want))
        if want - touched:
            bits.append("named files NOT touched: %s" % sorted(want - touched))
        if problems:
            bits.append("; ".join(problems))
        res["C3"] = ("FAIL", "; ".join(bits))

    exp_added = exp["expected_added"]
    c2_fail = None
    for path in sorted(set(exp_added) | set(p for p, v in added.items() if v)):
        got = added.get(path, [])
        wnt = exp_added.get(path, [])
        if path not in exp_added:
            c2_fail = "%s: %d added line(s) not in expected_added; first: %r" % (path, len(got), got[0])
            break
        for idx in range(max(len(got), len(wnt))):
            g = got[idx] if idx < len(got) else None
            w = wnt[idx] if idx < len(wnt) else None
            if g != w:
                c2_fail = ("%s: added line #%d differs: expected %s, diff has %s"
                           % (path, idx + 1, repr(w) if w is not None else "<nothing>",
                              repr(g) if g is not None else "<nothing>"))
                break
        if c2_fail:
            break
    n_added = sum(len(v) for v in added.values())
    res["C2"] = ("FAIL", c2_fail) if c2_fail else ("PASS", "%d added line(s) byte-identical to expected_added" % n_added)

    # ---- C5 part 1: suite at base (before applying) ------------------------
    suite_cmd = exp.get("suite_cmd")
    red_cmd = exp.get("red_test_cmd")
    base = None
    if suite_cmd and mode != "none":
        base = ev.run("C5_suite_before", suite_cmd, cwd=wc, shell=True)

    # ---- apply for real ------------------------------------------------------
    applied = False
    if mode != "none":
        rc, _, se, f_ap = ev.run("apply_%s" % mode.replace("-", "_"),
                                 ["git", "apply"] + apply_flags + [patch_file], cwd=wc)
        applied = rc == 0
        if not applied:
            res["C1"] = ("FAIL", "apply --check passed (%s) but the real apply failed: %s (%s)"
                         % (mode, se.strip(), f_ap))
        else:
            # Fidelity: git ends a hunk when the header's counts are used up and IGNORES the lines
            # after it, so an under-counted header can apply 'strict' while silently dropping '+'
            # lines (found in self-test). Compare what git actually changed with the diff text.
            text_paths = sorted(touched)
            new_paths = [p for p in text_paths if os.path.exists(os.path.join(wc, p))]
            if new_paths:  # intent-to-add so a file the diff CREATES shows in numstat (throwaway clone only)
                ev.run("C1_intent_to_add", ["git", "add", "-N", "--"] + new_paths, cwd=wc)
            rc_n, so_n, _, f_n = ev.run("C1_applied_numstat",
                                        ["git", "diff", "--numstat", "--no-renames", "--no-ext-diff", "--"]
                                        + text_paths, cwd=wc)
            got_ns = {}
            for ln in so_n.splitlines():
                parts = ln.split("\t")
                if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
                    got_ns[parts[2]] = (int(parts[0]), int(parts[1]))
            text_ns = dict((p, (len(added.get(p, [])), removed.get(p, 0))) for p in set(added) | set(removed)
                           if len(added.get(p, [])) or removed.get(p, 0))
            if rc_n != 0 or got_ns != text_ns:
                res["C1"] = ("FAIL", "git applied (%s) something DIFFERENT from the diff text - hunk header "
                                     "count truncates/extends a hunk: applied +/- %s vs text +/- %s (%s)"
                             % (mode, sorted(got_ns.items()), sorted(text_ns.items()), f_n))
            elif mode == "strict":
                res["C1"] = ("PASS", res["C1"][1] + "; applied +/- counts match the diff text (%s)" % f_n)

    # ---- C4 red-first ------------------------------------------------------
    if mode == "none" or not applied:
        res["C4"] = ("NOT-RUN", "diff does not apply")
    elif not red_cmd:
        res["C4"] = ("NOT-RUN", "red_test_cmd is null - red-first NOT proven (a green result without it is worthless)")
    else:
        how = "applied %s" % mode
        r1, _, _, f1 = ev.run("C4_red_with_diff", red_cmd, cwd=wc, shell=True)
        rr, _, se_rv, f_rv = ev.run("C4_revert", ["git", "apply", "-R"] + apply_flags + [patch_file], cwd=wc)
        r2, f2 = None, None
        r3, f3 = None, None
        if rr == 0:
            r2, _, _, f2 = ev.run("C4_red_reverted", red_cmd, cwd=wc, shell=True)
            ra, _, se_ra, f_ra = ev.run("C4_reapply", ["git", "apply"] + apply_flags + [patch_file], cwd=wc)
            if ra == 0:
                r3, _, _, f3 = ev.run("C4_red_reapplied", red_cmd, cwd=wc, shell=True)
            else:
                applied = False
        if rr != 0:
            res["C4"] = ("FAIL", "could not revert the diff (git apply -R rc=%d) (%s)" % (rr, f_rv))
            applied = True  # still applied
        elif r3 is None:
            res["C4"] = ("FAIL", "could not re-apply after revert (%s)" % f_ra)
        elif r1 == 0 and r2 != 0 and r3 == 0:
            res["C4"] = ("PASS", "%s: with=rc0 (%s), reverted=rc%d RED (%s), re-applied=rc0 (%s)"
                         % (how, f1, r2, f2, f3))
        else:
            why = []
            if r1 != 0:
                why.append("red test FAILS with the diff (rc=%d)" % r1)
            if r2 == 0:
                why.append("red test PASSES WITHOUT the diff - it does not catch the change")
            if r3 != 0:
                why.append("red test fails after re-apply (rc=%d)" % r3)
            res["C4"] = ("FAIL", "%s: %s (%s, %s, %s)" % (how, "; ".join(why), f1, f2, f3))

    # ---- C5 part 2: suite after --------------------------------------------
    if not suite_cmd:
        res["C5"] = ("NOT-RUN", "suite_cmd is null")
    elif mode == "none" or not applied:
        res["C5"] = ("NOT-RUN", "diff does not apply (or could not be re-applied)")
    else:
        after = ev.run("C5_suite_after", suite_cmd, cwd=wc, shell=True)
        b_rc, b_out, b_err, b_f = base
        a_rc, a_out, a_err, a_f = after

        def counts(o, e):
            if not count_re:
                return None, None
            ms = list(count_re.finditer(o + "\n" + e))
            if not ms:
                return None, None
            m = ms[-1]
            p = int(m.group("passed")) if m.group("passed") is not None else None
            fl = None
            if "failed" in count_re.groupindex:
                fl = int(m.group("failed")) if m.group("failed") is not None else 0
            return p, fl

        bp, bf = counts(b_out, b_err)
        apc, af = counts(a_out, a_err)
        detail = "before rc=%d passed=%s failed=%s (%s); after rc=%d passed=%s failed=%s (%s)" % (
            b_rc, bp, bf, b_f, a_rc, apc, af, a_f)
        ok = True
        why = []
        if b_rc == 0 and a_rc != 0:
            ok = False
            why.append("suite went from green to rc=%d" % a_rc)
        if count_re:
            if bp is None or apc is None:
                ok = False
                why.append("suite_count_regex did not match before/after output")
            else:
                if apc < bp:
                    ok = False
                    why.append("passed dropped %d -> %d" % (bp, apc))
                if bf is not None and af is not None and af > bf:
                    ok = False
                    why.append("failed rose %d -> %d" % (bf, af))
        res["C5"] = ("PASS" if ok else "FAIL", ("; ".join(why) + " — " if why else "") + detail)

    # ---- C6 evidence kept ----------------------------------------------------
    missing = [os.path.basename(p) for p in ev.expected
               if not (os.path.isfile(p) and os.path.getsize(p) > 0)]
    if missing:
        res["C6"] = ("FAIL", "missing/empty evidence: %s" % missing)
    else:
        res["C6"] = ("PASS", "%d evidence file(s) present and non-empty in %s" % (len(ev.expected), out_dir))

    statuses = [res["C%d" % i][0] for i in range(1, 7)]
    if "FAIL" in statuses:
        verdict = "FAIL"
    elif all(s == "PASS" for s in statuses):
        verdict = "PASS"
    else:
        verdict = "INCOMPLETE"

    lines = ["C%d: %s — %s" % (i, res["C%d" % i][0], res["C%d" % i][1]) for i in range(1, 7)]
    lines.append("APPLY-MODE: %s" % mode)
    lines.append("VERDICT: %s" % verdict)
    text = "\n".join(lines) + "\n"
    vt = os.path.join(out_dir, "verdict.txt")
    vj = os.path.join(out_dir, "verdict.json")
    with open(vt, "w", encoding="utf-8") as f:
        f.write(text)
    with open(vj, "w", encoding="utf-8") as f:
        json.dump({"verdict": verdict, "apply_mode": mode, "commit": head,
                   "clauses": {k: {"status": v[0], "detail": v[1]} for k, v in sorted(res.items())},
                   "evidence_files": [os.path.basename(p) for p in ev.expected],
                   "checked_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, f, indent=2, ensure_ascii=False)
    sys.stdout.write(text)
    for p in (vt, vj):
        if not (os.path.isfile(p) and os.path.getsize(p) > 0):
            print("C6 POST-CHECK FAIL: %s missing or empty - VERDICT forced to FAIL" % p)
            return 1
    return {"PASS": 0, "FAIL": 1, "INCOMPLETE": 2}[verdict]


if __name__ == "__main__":
    sys.exit(main())
