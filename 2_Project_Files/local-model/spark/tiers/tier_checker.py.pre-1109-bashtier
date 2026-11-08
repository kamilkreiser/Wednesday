#!/usr/bin/env python3
"""tier_checker.py <input.json> <out.md> <clone-dir> — the checker for tiers test_only_input and doc_only (2026-10-31).

Run by spark/round.sh in place of tasks/code_patch/spark_checker.sh for these two tiers. It is a sibling of
tasks/code_patch/checker.sh, not a fork of round.sh: lint, lock, base, clone, golden compare and run-dir record are all
round.sh's; only the verdict legs differ, because checker.sh's test_only mode can only red a test under a PRODUCT tamper
and has no doc mode. It reuses checker.sh's A1 extract rules (exactly one ```diff fence, nothing outside), A2 strict
apply (then --recount --ignore-whitespace, reported apart), A2a (tasks/code_patch/a2a_anchor.py, unchanged), and the
exact-touched-set, before/after-count and sha256-restore disciplines. It edits nothing outside <clone-dir>; every
write (git apply, the plant, test runs) is inside the clone and is reverted and sha256-verified before it exits.

Output: PASS/FAIL/INFO lines, then `RESULT: PASS|FAIL (...)` and `SPARK RESULT: ...`. rc 0 only when every leg passes.

test_only_input legs
  A1 extract · A2 applies · A2a anchor · A3 touched set == the header's Test files (never the product, never the plant file)
  A3p the plant is applicable at the tip (pin: `line:` holds `from:` exactly; diff: git apply --check) — a brief defect otherwise
  A4 GREEN WITHOUT PLANT: every declared red cell exists after the patch and passes; no new red in the declared files
  A5 RED WITH PLANT: the plant applied (scratch only) -> every matched red cell FAILS BY ASSERTION (not a crash, not a load error)
  A6 whole-service suite after the patch (no plant) is no worse than at the tip: no new red, no cell lost, failed count not higher
  A7 restore: every touched/planted file back to its tip sha256, no stray file
doc_only legs
  A1 · A2 · A2a · A3 touched set == the header's File lines · A3d every path is *.md / Projects Documents/fragments/** or a
  code file whose changed lines are ALL whole-line comments (0 changed non-comment lines, computed per file, base vs patched)
  A4 RED AT BASE: each expect_absent text is present, each expect_present text absent, at the untouched tip
  A5 GREEN AFTER: the opposite, after the patch · A6 doc checks (docs-fragments.mjs check when fragments are touched and the
  script exists, plus the brief's `## Doc checks`) no worse than at the tip · A7 REVERSION: `git apply -R` of the patch
  must make the expectations FAIL again · A8 restore: sha256-verified.
"""
import difflib
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tier_brief as tb  # noqa: E402

FAILS = 0


def say(s):
    print(s, flush=True)


def passed(s):
    say("PASS " + s)


def failed(s):
    global FAILS
    FAILS += 1
    say("FAIL " + s)


def info(s):
    say("INFO " + s)


def sha(path):
    if not os.path.isfile(path):
        return None
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


class Clone:
    def __init__(self, path, tip, rep):
        self.p, self.tip, self.rep = path, tip, rep
        self.quar = os.path.join(rep, "quarantine")
        self.snap = {}

    def git(self, *a, inp=None):
        return subprocess.run(["git", "-C", self.p, *a], capture_output=True, text=True, input=inp)

    def show(self, rel):
        r = self.git("show", f"{self.tip}:{rel}")
        return r.stdout if r.returncode == 0 else None

    def path(self, rel):
        return os.path.join(self.p, rel)

    def read(self, rel):
        f = self.path(rel)
        return open(f, encoding="utf-8", errors="replace").read() if os.path.isfile(f) else None

    def watch(self, rels):
        for r in rels:
            if r not in self.snap:
                self.snap[r] = sha(self.path(r))

    def restore(self):
        """Put every watched file back to its tip state. A tracked file is checked out from the tip; a file the tip does
        not have is MOVED to quarantine (nothing is deleted)."""
        for rel, h in self.snap.items():
            f = self.path(rel)
            if h is not None:
                if sha(f) != h:
                    self.git("checkout", self.tip, "--", rel)
            elif os.path.exists(f):
                dst = os.path.join(self.quar, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(f, dst)

    def verify(self):
        bad = [r for r, h in self.snap.items() if sha(self.path(r)) != h]
        st = self.git("status", "--porcelain", "--untracked-files=no").stdout.strip()
        return bad, st


def extract(out_md, diff_path):
    text = open(out_md, encoding="utf-8").read()
    blocks = re.findall(r"```diff[^\n]*\n(.*?)```", text, flags=re.DOTALL)
    allblocks = re.findall(r"```[^\n]*\n.*?```", text, flags=re.DOTALL)
    outside = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.DOTALL).strip()
    tail = [l for l in text.split("\n") if l.strip()][-41:]
    if len(tail) >= 12:
        for k in range(1, 7):
            cyc = tail[-k:]
            n = min(len(tail), 8 * k)
            if all(tail[-(i + 1)] == cyc[-(i % k + 1)] for i in range(n)):
                return None, f"REPETITION LOOP: the last {n} non-blank lines repeat a {k}-line cycle", 4
    if not blocks:
        return None, "no ```diff block — prose instead of a diff; nothing to apply", 2
    body = blocks[0] if blocks[0].endswith("\n") else blocks[0] + "\n"
    open(diff_path, "w", encoding="utf-8").write(body)
    ok = len(blocks) == 1 and len(allblocks) == 1 and not outside
    return body, ("" if ok else f"diff_blocks={len(blocks)} all_blocks={len(allblocks)} prose_outside_chars={len(outside)}"), (0 if ok else 3)


def split_sections(body, rep):
    """Sections per file header (`--- X` directly followed by `+++ Y`) -> sections.json for a2a_anchor.py."""
    lines = body.split("\n")
    starts = [i for i in range(len(lines) - 1) if lines[i].startswith("--- ") and lines[i + 1].startswith("+++ ")]
    secs = []
    for k, i in enumerate(starts):
        j = starts[k + 1] if k + 1 < len(starts) else len(lines)
        # drop a `diff --git` / `index` preamble line that belongs to the NEXT section
        while j > i + 2 and re.match(r"^(diff --git |index |new file mode|deleted file mode|similarity |rename )", lines[j - 1]):
            j -= 1
        minus, plus = lines[i][4:].split("\t")[0].strip(), lines[i + 1][4:].split("\t")[0].strip()
        pth = re.sub(r"^[ab]/", "", plus if plus != "/dev/null" else minus)
        if plus == "/dev/null":
            pth = re.sub(r"^[ab]/", "", minus)
        f = os.path.join(rep, f"section_{k + 1}.diff")
        open(f, "w", encoding="utf-8").write("\n".join(lines[i:j]).rstrip("\n") + "\n")
        secs.append({"n": k + 1, "path": pth, "file": f, "new": minus == "/dev/null", "delete": plus == "/dev/null"})
    json.dump(secs, open(os.path.join(rep, "sections.json"), "w"), indent=1)
    return secs


def apply_check(cl, diff, reverse=False):
    """-> opts used (list) or None. Strict first; then the ONE accommodation (reported apart)."""
    for opts in ([], ["--recount", "--ignore-whitespace"]):
        args = ["apply", "--check", "-p1"] + (["-R"] if reverse else []) + opts + [diff]
        r = cl.git(*args)
        if r.returncode == 0:
            return opts
    return None


def apply_real(cl, diff, opts, reverse=False):
    r = cl.git("apply", "-p1", *(["-R"] if reverse else []), *opts, diff)
    return r.returncode == 0, (r.stderr or r.stdout).strip()


# ------------------------------------------------------------------ test runners (vitest | jest | node-tap)
ASSERT_RX = re.compile(r"AssertionError|ERR_ASSERTION|expect\(|toBe|toEqual|toThrow|Expected|expected .* to ")


def run_tests(inp, cl, label, files=None):
    """-> {'cells': {fullName: (status, msg)}, 'load_errors': [..], 'rc': int, 'total': n, 'failed': n}"""
    repo = inp["repo"]
    kind = repo["test_runner"].split(" ")[0]
    svc = os.path.join(cl.p, inp["repo_subdir"], inp["service_dir"])
    rel = [os.path.relpath(cl.path(f), svc) for f in (files or [])]
    jf = os.path.join(cl.rep, f"{label}.json")
    outf = os.path.join(cl.rep, f"{label}.out")
    if kind == "vitest":
        cmd = ["npx", "vitest", "run", *rel, "--reporter=json", f"--outputFile={jf}"]
    elif kind == "jest":
        cmd = ["npx", "jest", *rel, "--json", f"--outputFile={jf}"]
    elif kind == "node-tap":   # harness-only runner (the arms' fixture repo); real services are vitest or jest
        cmd = ["node", "--test", "--test-reporter=tap", *rel]
    else:
        return {"cells": {}, "load_errors": [f"unknown runner {kind}"], "rc": 99, "total": 0, "failed": 0}
    r = subprocess.run(cmd, cwd=svc, capture_output=True, text=True)
    open(outf, "w").write((r.stdout or "") + "\n--- stderr ---\n" + (r.stderr or ""))
    cells, lerr = {}, []
    if kind == "node-tap":
        cells, lerr = parse_tap(r.stdout)
    elif os.path.isfile(jf):
        cells, lerr = parse_json_report(jf)
    else:
        lerr.append("no json report written")
    return {"cells": cells, "load_errors": lerr, "rc": r.returncode, "total": len(cells),
            "failed": sum(1 for s, _ in cells.values() if s == "failed")}


def parse_json_report(path):
    j = json.load(open(path))
    cells, lerr = {}, []
    for tr in j.get("testResults", []):
        ars = tr.get("assertionResults", [])
        for a in ars:
            n = a.get("fullName") or a.get("title")
            st = {"passed": "passed", "failed": "failed"}.get(a.get("status"), "skipped")
            cells[n] = (st, "\n".join(a.get("failureMessages") or []))
        if tr.get("status") == "failed" and not ars:
            lerr.append(os.path.basename(tr.get("name", "?")) + ": " + (tr.get("message") or "")[:200].replace("\n", " "))
    return cells, lerr


def parse_tap(text):
    cells, lerr = {}, []
    path, child_seen, last = {}, {}, None
    for ln in (text or "").split("\n"):
        m = re.match(r"^( *)# Subtest: (.*)$", ln)
        if m:
            d = len(m.group(1)) // 4
            path[d] = m.group(2)
            for k in [k for k in path if k > d]:
                del path[k]
            last = None
            continue
        m = re.match(r"^( *)(not )?ok \d+ - (.*?)(?: # .*)?$", ln)
        if m:
            d = len(m.group(1)) // 4
            name = m.group(3)
            parent = child_seen.get(d, False)
            child_seen[d] = False
            if d > 0:
                child_seen[d - 1] = True
            full = " ".join([path[k] for k in sorted(path) if k < d] + [name])
            last = None
            if parent:
                continue
            st = "failed" if m.group(2) else "passed"
            if st == "failed" and d == 0 and re.search(r"\.(c|m)?js$", name) and "/" in name:
                lerr.append(os.path.basename(name) + ": did not load")
                continue
            cells[full] = [st, ""]
            last = full
            continue
        if last is not None:
            cells[last][1] += ln + "\n"
    return {k: (v[0], v[1]) for k, v in cells.items()}, lerr


def by_assertion(msg):
    return bool(ASSERT_RX.search(msg or ""))


def a2a(inp_path, cl, rep):
    here = os.path.dirname(HERE)
    a2a_py = os.path.join(os.path.dirname(here), "tasks", "code_patch", "a2a_anchor.py")
    r = subprocess.run(["python3", a2a_py, inp_path, cl.p, os.path.join(rep, "sections.json")], capture_output=True, text=True)
    open(os.path.join(rep, "a2a_anchor.out"), "w").write(r.stdout + r.stderr)
    summ = next((l for l in r.stdout.split("\n") if l.startswith("SUMMARY")), "")
    if r.returncode == 0:
        passed(f"A2a ANCHOR: every hunk's old side sits at its header's start line at the tip ({summ})")
    elif r.returncode == 1:
        failed("A2a ANCHOR: a hunk's header does NOT name the line its old side sits at: "
               + " ".join(l for l in r.stdout.split("\n") if l.startswith("BAD"))[:400] + f" ({summ})")
    elif r.returncode == 5:
        info("A2a skipped — nothing to check")
    else:
        failed(f"A2a ANCHOR MEASURE ERROR rc={r.returncode}: {(r.stdout + r.stderr)[:200]}")


def finish(code_msg):
    ok = FAILS == 0
    say(f"RESULT: {'PASS' if ok else 'FAIL'} ({code_msg})")
    say(f"SPARK RESULT: {'PASS' if ok else 'FAIL'} (tier checker: {FAILS} failed leg(s))")
    sys.exit(0 if ok else 1)


def common_front(inp, inp_path, out_md, cl, declared, label):
    """A1, A2, A2a, A3 (touched == declared). -> (diff_path, opts, secs) or exits."""
    rep = cl.rep
    diff = os.path.join(rep, "patch.diff")
    body, note, rc = extract(out_md, diff)
    if rc in (2, 4):
        failed(f"A1 {note}")
        finish("stopped at A1")
    if rc == 3:
        failed(f"A1 output is not exactly one fenced diff block with nothing outside it ({note}) — continuing with the first block")
    else:
        passed("A1 output is exactly one fenced ```diff block, nothing outside it")
    secs = split_sections(body, rep)
    if not secs:
        failed("A1 the diff block has no `--- a/<path>` / `+++ b/<path>` file header")
        finish("stopped at A1")
    opts = apply_check(cl, diff)
    if opts is None:
        r = cl.git("apply", "--check", "-p1", "--recount", "--ignore-whitespace", diff)
        failed(f"A2 the diff does not apply at the tip {cl.tip[:12]}: {(r.stderr or r.stdout).strip()[:300]}")
        finish("stopped at A2")
    passed("A2 the diff applies at the tip" + (" (strict)" if not opts else " ONLY with --recount --ignore-whitespace (the one accommodation)"))
    a2a(inp_path, cl, rep)
    touched = [s["path"] for s in secs]
    dup = sorted({t for t in touched if touched.count(t) > 1})
    if dup:
        failed(f"A3 the diff names the same file in more than one section: {dup}")
    if sorted(set(touched)) == sorted(set(declared)) and not dup:
        passed(f"A3 touched set == the brief's declared set ({', '.join(sorted(set(touched)))})")
    else:
        extra = sorted(set(touched) - set(declared))
        missing = sorted(set(declared) - set(touched))
        failed(f"A3 touched set != the declared set: extra {extra or 'none'}, missing {missing or 'none'} (declared {sorted(declared)})")
        finish("stopped at A3 — nothing was applied")
    return diff, opts, secs


# ------------------------------------------------------------------ test_only_input
def apply_plant(inp, cl):
    """Apply the brief's plant in the clone (scratch). -> (files touched, error|None)"""
    groups, pdiff = inp.get("plant") or [], inp.get("plant_diff")
    if pdiff:
        f = os.path.join(cl.rep, "golden_red.diff")
        open(f, "w", encoding="utf-8").write(pdiff if pdiff.endswith("\n") else pdiff + "\n")
        opts = apply_check(cl, f)
        if opts is None:
            return [], "golden_red.diff does not apply"
        cl.watch(plant_diff_paths(pdiff))
        ok, err = apply_real(cl, f, opts)
        return plant_diff_paths(pdiff), (None if ok else err)
    touched = []
    for g in groups:
        cl.watch([g["file"]])
        txt = cl.read(g["file"])
        if txt is None:
            return touched, f"plant file {g['file']} missing"
        ls = txt.split("\n")
        n = g["line"]
        if not (1 <= n <= len(ls)) or ls[n - 1].rstrip("\r") != g["from"]:
            return touched, f"plant: line {n} of {g['file']} is {ls[n - 1] if 1 <= n <= len(ls) else '<outside the file>'!r}, not the brief's `from:` {g['from']!r}"
        ls[n - 1] = g["to"]
        open(cl.path(g["file"]), "w", encoding="utf-8").write("\n".join(ls))
        touched.append(g["file"])
    return touched, None


def plant_diff_paths(pdiff):
    out = []
    lines = pdiff.split("\n")
    for i in range(len(lines) - 1):
        if lines[i].startswith("--- ") and lines[i + 1].startswith("+++ "):
            p = lines[i + 1][4:].split("\t")[0].strip()
            p = lines[i][4:].split("\t")[0].strip() if p == "/dev/null" else p
            out.append(re.sub(r"^[ab]/", "", p))
    return out


def plant_paths(inp):
    if inp.get("plant_diff"):
        return plant_diff_paths(inp["plant_diff"])
    return [g["file"] for g in inp.get("plant") or []]


def tier_test_only_input(inp, inp_path, out_md, cl):
    tests = inp["test_files"]
    ppaths = plant_paths(inp)
    cl.watch(tests + ppaths)
    say(f"mode: test_only_input (declared tests {tests}; plant on {ppaths}; red cells {inp['red_cells']})")
    overlap = sorted(set(ppaths) & set(tests))
    if overlap:
        failed(f"A3p the plant touches a declared test file {overlap} — the plant must not overlap the model's files")
        finish("stopped at A3p (brief defect)")
    diff, opts, secs = common_front(inp, inp_path, out_md, cl, tests, "test_only_input")
    # A3p: the plant is applicable at the untouched tip (checked before anything is applied)
    groups, pdiff = inp.get("plant") or [], inp.get("plant_diff")
    perr = None
    if pdiff:
        pf = os.path.join(cl.rep, "golden_red.diff")
        open(pf, "w", encoding="utf-8").write(pdiff if pdiff.endswith("\n") else pdiff + "\n")
        if apply_check(cl, pf) is None:
            perr = "golden_red.diff does not `git apply --check` at the tip"
    else:
        for g in groups:
            ls = (cl.show(g["file"]) or "").split("\n")
            n = g["line"]
            if not (1 <= n <= len(ls)) or ls[n - 1].rstrip("\r") != g["from"]:
                perr = f"line {n} of {g['file']} is {ls[n - 1] if 1 <= n <= len(ls) else '<outside>'!r}, not the brief's `from:` {g['from']!r}"
    if perr:
        failed(f"A3p the plant is not applicable at the tip: {perr} (a BRIEF defect, not a model one)")
        finish("stopped at A3p")
    passed(f"A3p the plant applies at the tip ({'golden_red.diff' if pdiff else str(len(groups)) + ' pinned line(s)'})")
    # baseline (untouched tip)
    existing = [t for t in tests if cl.show(t) is not None]
    base_decl = run_tests(inp, cl, "baseline_declared", existing) if existing else {"cells": {}, "load_errors": [], "rc": 0, "total": 0, "failed": 0}
    base_suite = run_tests(inp, cl, "baseline_suite")
    info(f"baseline at the tip: declared files {base_decl['total']} cells, {base_decl['failed']} red; whole suite {base_suite['total']} cells, "
         f"{base_suite['failed']} red, {len(base_suite['load_errors'])} load error(s)")
    ok, err = apply_real(cl, diff, opts)
    if not ok:
        failed(f"A2 the real apply failed after --check passed: {err[:300]}")
        return
    try:
        # A4 green without plant
        gr = run_tests(inp, cl, "green_after", tests)
        bad = []
        for s in inp["red_cells"]:
            m = [n for n in gr["cells"] if s in n]
            if not m:
                bad.append(f"no cell contains {s!r}")
            for n in m:
                if gr["cells"][n][0] != "passed":
                    bad.append(f"{n!r} is {gr['cells'][n][0]} without the plant")
        new_red = sorted(n for n, (st, _) in gr["cells"].items() if st == "failed" and base_decl["cells"].get(n, ("",))[0] != "failed")
        if gr["load_errors"]:
            bad.append(f"load error: {gr['load_errors'][:2]}")
        if new_red:
            bad.append(f"new red cell(s) in the declared files without the plant: {new_red[:3]}")
        if bad:
            failed("A4 GREEN WITHOUT PLANT: " + "; ".join(bad)[:500])
        else:
            matched = sorted({n for s in inp["red_cells"] for n in gr["cells"] if s in n})
            passed(f"A4 GREEN WITHOUT PLANT: {len(matched)} red cell(s) exist and pass on the unmodified product; "
                   f"declared files {gr['total']} cells, {gr['failed']} red")
            pre = [n for n in matched if n in base_decl["cells"]]
            if pre:
                info(f"red cell(s) already present at the tip (changed in place, or the gap is already pinned): {pre[:3]}")
        # A6 whole suite no worse
        af = run_tests(inp, cl, "after_suite")
        lost = sorted(set(base_suite["cells"]) - set(af["cells"]))
        newr = sorted(n for n, (st, _) in af["cells"].items() if st == "failed" and base_suite["cells"].get(n, ("",))[0] != "failed")
        worse = []
        if lost:
            worse.append(f"cell(s) LOST vs the tip: {lost[:3]}")
        if newr:
            worse.append(f"new red: {newr[:3]}")
        if af["failed"] > base_suite["failed"]:
            worse.append(f"failed {base_suite['failed']} -> {af['failed']}")
        if len(af["load_errors"]) > len(base_suite["load_errors"]):
            worse.append(f"load errors {len(base_suite['load_errors'])} -> {len(af['load_errors'])}")
        if worse:
            failed("A6 WHOLE SUITE: worse after the patch — " + "; ".join(worse))
        else:
            passed(f"A6 WHOLE SUITE no worse: cells {base_suite['total']} -> {af['total']}, red {base_suite['failed']} -> {af['failed']}")
        # A5 red with plant (scratch only)
        touched, perr = apply_plant(inp, cl)
        if perr:
            failed(f"A5 the plant could not be applied after the patch: {perr}")
        else:
            rr = run_tests(inp, cl, "red_with_plant", tests)
            bad, kinds = [], []
            if rr["load_errors"]:
                bad.append(f"the plant broke the LOAD of {rr['load_errors'][:2]} (a load error is not red)")
            for s in inp["red_cells"]:
                for n in [n for n in rr["cells"] if s in n]:
                    st, msg = rr["cells"][n]
                    if st == "passed":
                        bad.append(f"{n!r} stays GREEN with the plant applied (a check that cannot fail)")
                    elif st == "failed" and not by_assertion(msg):
                        bad.append(f"{n!r} went red by a crash, not an assertion")
                    elif st == "failed":
                        kinds.append(n)
            if bad:
                failed("A5 RED WITH PLANT: " + "; ".join(bad)[:600])
            else:
                passed(f"A5 RED WITH PLANT: {len(kinds)} red cell(s) fail by assertion under the plant ({', '.join(touched)}), pass without it")
            other = sorted(n for n, (st, _) in rr["cells"].items() if st == "failed" and n not in kinds)
            if other:
                info(f"other cell(s) in the declared files also red under the plant: {other[:3]}")
    finally:
        cl.restore()
        bad, st = cl.verify()
        if bad or st:
            failed(f"A7 RESTORE: not back to the tip — sha256 mismatch {bad[:3]} status {st[:120]!r}")
        else:
            passed(f"A7 RESTORE: {len(cl.snap)} watched file(s) back at their tip sha256; tracked tree clean")


# ------------------------------------------------------------------ doc_only
def expectations(inp, cl, state_read):
    """-> list of (item, ok, detail). state_read(rel) -> text or None."""
    res = []
    docs = inp["doc_files"]
    for it in inp["expect"]:
        scope = [it["path"]] if it["path"] else docs
        if it["path"] and it["path"] not in docs:
            res.append((it, False, f"`in` path {it['path']} is not a declared File"))
            continue
        hit = [p for p in scope if it["text"] in (state_read(p) or "")]
        if it["kind"] == "absent":
            res.append((it, not hit, f"present in {hit}" if hit else "absent"))
        else:
            res.append((it, bool(hit), "present" if hit else "absent everywhere in scope"))
    return res


def run_doc_checks(inp, cl, paths):
    cmds = []
    sub = inp.get("tool_subdir") or ""
    script = os.path.join(sub, "scripts", "docs-fragments.mjs")
    if any("Projects Documents/fragments/" in p for p in paths):
        if os.path.isfile(cl.path(script)):
            cmds.append(["node", script, "check"])
        else:
            info(f"fragments touched but {script} is not in the repo — fragment check not run")
    for c in inp.get("doc_checks") or []:
        argv = shlex.split(c)
        if not argv or argv[0] not in ("node", "bash", "sh", "python3", "npx"):
            cmds.append(["__refused__", c])
        else:
            cmds.append(argv)
    out = []
    cwd = cl.path(inp.get("doc_check_cwd") or "")
    for argv in cmds:
        if argv[0] == "__refused__":
            out.append((argv[1], 99, "command is not node/bash/sh/python3/npx"))
            continue
        r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
        out.append((" ".join(argv), r.returncode, (r.stdout + r.stderr)))
    return out


def tier_doc_only(inp, inp_path, out_md, cl):
    docs = inp["doc_files"]
    cl.watch(docs)
    say(f"mode: doc_only (declared files {docs}; {len(inp['expect'])} expectation(s))")
    # path classes are decidable from the diff alone, before anything is applied
    diff, opts, secs = common_front(inp, inp_path, out_md, cl, docs, "doc_only")
    kinds = {}
    for p in docs:
        if tb.is_doc_path(p):
            kinds[p] = "doc"
        elif tb.comment_kind(p):
            kinds[p] = "comment-only code"
        else:
            kinds[p] = None
    badp = [p for p, k in kinds.items() if k is None]
    if badp:
        failed(f"A3d path(s) {badp} are neither *.md / Projects Documents/fragments/** nor a code file type whose comments can be verified")
        finish("stopped at A3d — nothing applied")
    # A4 red at base (the untouched tip)
    base = expectations(inp, cl, lambda p: cl.read(p) or "")
    cannot = [(it, d) for it, ok, d in base if ok]
    if cannot:
        failed("A4 RED AT BASE: the expectation(s) already hold at the tip, so they cannot fail — " +
               "; ".join(f"{it['kind']} {it['text']!r}: {d}" for it, d in cannot[:3]) + " (a BRIEF defect)")
    else:
        passed(f"A4 RED AT BASE: all {len(base)} expectation(s) fail at the untouched tip (the defect is there to be removed)")
    base_checks = run_doc_checks(inp, cl, docs)
    ok, err = apply_real(cl, diff, opts)
    if not ok:
        failed(f"A2 the real apply failed after --check passed: {err[:300]}")
        return
    try:
        # A3d comment-only verification
        tot_c, bad_lines = 0, []
        for p in docs:
            if kinds[p] != "comment-only code":
                continue
            a, b = (cl.show(p) or ""), (cl.read(p) or "")
            kd = tb.comment_kind(p)
            la, lb = tb.comment_lines(a, kd), tb.comment_lines(b, kd)
            al, bl = a.split("\n"), b.split("\n")
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, al, bl, autojunk=False).get_opcodes():
                if tag == "equal":
                    continue
                for i in range(i1, i2):
                    if la[i]:
                        tot_c += 1
                    else:
                        bad_lines.append(f"{p}:{i + 1}(-) {al[i].strip()[:60]!r}")
                for j in range(j1, j2):
                    if lb[j]:
                        tot_c += 1
                    else:
                        bad_lines.append(f"{p}:{j + 1}(+) {bl[j].strip()[:60]!r}")
        ncode = sum(1 for k in kinds.values() if k == "comment-only code")
        if bad_lines:
            failed(f"A3d DOC-ONLY: {len(bad_lines)} changed NON-comment line(s) in code file(s): " + "; ".join(bad_lines[:4]))
        else:
            passed(f"A3d DOC-ONLY: 0 changed non-comment lines ({tot_c} comment line(s) changed in {ncode} code file(s); "
                   f"{sum(1 for k in kinds.values() if k == 'doc')} doc file(s) are *.md / fragments)")
        # A5 green after
        post = expectations(inp, cl, lambda p: cl.read(p) or "")
        notok = [(it, d) for it, ok, d in post if not ok]
        if notok:
            failed("A5 GREEN AFTER: " + "; ".join(f"{it['kind']} {it['text']!r}: {d}" for it, d in notok[:3]))
        else:
            passed(f"A5 GREEN AFTER: all {len(post)} expectation(s) hold after the patch")
        # A6 doc checks
        after_checks = run_doc_checks(inp, cl, docs)
        if not after_checks:
            info("A6 no doc check ran (no fragments touched / none declared in `## Doc checks`)")
        for (cmd, rc, o), (cmd0, rc0, o0) in zip(after_checks, base_checks):
            if rc == 0:
                passed(f"A6 DOC CHECK `{cmd}` rc 0 after the patch (rc {rc0} at the tip)")
            elif rc0 != 0 and set(o.split("\n")) <= set(o0.split("\n")):
                passed(f"A6 DOC CHECK `{cmd}` rc {rc} but no worse than the tip (rc {rc0}, no new output line)")
            else:
                failed(f"A6 DOC CHECK `{cmd}` rc {rc} after the patch (rc {rc0} at the tip): {o.strip()[-240:]}")
        # A7 planted reversion re-fails the expectations
        ropts = apply_check(cl, diff, reverse=True)
        if ropts is None:
            failed("A7 REVERSION: the patch cannot be reverse-applied to plant the reversion")
        else:
            ok, err = apply_real(cl, diff, ropts, reverse=True)
            rev = expectations(inp, cl, lambda p: cl.read(p) or "")
            still = [(it, d) for it, okk, d in rev if okk]
            refail = [(it, d) for it, okk, d in rev if not okk]
            if ok and refail and not still:
                passed(f"A7 REVERSION: with the patch reverse-applied, {len(refail)}/{len(rev)} expectation(s) fail again (the check discriminates)")
            elif ok and refail:
                failed(f"A7 REVERSION: {len(still)} expectation(s) still hold with the patch reversed: {[it['text'] for it, _ in still][:2]} (cannot fail)")
            else:
                failed(f"A7 REVERSION: no expectation failed after the reversion ({err[:100]}) — the check cannot fail")
    finally:
        cl.restore()
        bad, st = cl.verify()
        if bad or st:
            failed(f"A8 RESTORE: not back to the tip — sha256 mismatch {bad[:3]} status {st[:120]!r}")
        else:
            passed(f"A8 RESTORE: {len(cl.snap)} watched file(s) back at their tip sha256; tracked tree clean")


def main():
    if len(sys.argv) != 4:
        print("usage: tier_checker.py <input.json> <out.md> <clone-dir>", file=sys.stderr)
        return 1
    inp_path, out_md, clone = sys.argv[1:4]
    if not (os.path.isfile(inp_path) and os.path.isfile(out_md) and os.path.isdir(os.path.join(clone, ".git"))):
        print("tier_checker: bad arguments (input/out/clone)", file=sys.stderr)
        return 1
    inp = json.load(open(inp_path, encoding="utf-8"))
    rep = out_md + ".checker"
    os.makedirs(rep, exist_ok=True)
    cl = Clone(clone, inp["tip"], rep)
    head = cl.git("rev-parse", "HEAD").stdout.strip()
    if head != inp["tip"]:
        print(f"tier_checker: clone HEAD {head} != pinned tip {inp['tip']}", file=sys.stderr)
        return 1
    dirty = cl.git("status", "--porcelain", "--untracked-files=no").stdout.strip()
    if dirty:
        print(f"tier_checker: clone has tracked modifications before the run — refusing:\n{dirty[:300]}", file=sys.stderr)
        return 1
    t = inp.get("tier")
    if t == "test_only_input":
        tier_test_only_input(inp, inp_path, out_md, cl)
    elif t == "doc_only":
        tier_doc_only(inp, inp_path, out_md, cl)
    else:
        print(f"tier_checker: unknown tier {t!r}", file=sys.stderr)
        return 1
    finish(f"tier {t}")


if __name__ == "__main__":
    main()
