#!/usr/bin/env python3
"""Arms for spark_check.py C1 apply modes: strict / PASS-RECOUNT (per file) / FAIL, and the per-file split.

Throwaway git repo + evidence dirs in the system temp dir (never a real repo). Nothing is deleted.
Usage: python3 tests/recount_arms.py   -> one `PASS|FAIL  <arm>: ...` line per arm; exit 0 iff all PASS.
"""
import json, os, re, subprocess, sys, tempfile

SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = os.path.join(SP, "spark_check.py")
W = tempfile.mkdtemp(prefix="spark_recount_arms_")
REPO = os.path.join(W, "repo")
os.makedirs(REPO)


def sh(args, cwd=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


for name, stem in (("a.txt", "a"), ("b.txt", "b")):
    with open(os.path.join(REPO, name), "w") as f:
        f.write("".join("%s%d\n" % (stem, i) for i in range(1, 6)))
for a in (["init", "-q"], ["config", "user.email", "arms@example.invalid"], ["config", "user.name", "arms"],
          ["add", "-A"], ["commit", "-q", "-m", "fixture"]):
    rc, out = sh(["git", "-C", REPO] + a)
    assert rc == 0, out
SHA = sh(["git", "-C", REPO, "rev-parse", "HEAD"])[1].strip()

A_OK = "--- a/a.txt\n+++ b/a.txt\n@@ -2,3 +2,3 @@\n a2\n-a3\n+A3\n a4\n"
B_OK = "--- a/b.txt\n+++ b/b.txt\n@@ -2,3 +2,3 @@\n b2\n-b3\n+B3\n b4\n"
A_MISCOUNT = A_OK.replace("@@ -2,3 +2,3 @@", "@@ -2,3 +2,4 @@")  # lines right, header over-counts the new side
B_MISCOUNT = B_OK.replace("@@ -2,3 +2,3 @@", "@@ -2,3 +2,4 @@")
A_WRONG = A_OK.replace("-a3\n", "-aX\n")  # content does not match the file

EXP2 = {"commit": SHA, "files": ["a.txt", "b.txt"], "expected_added": {"a.txt": ["A3"], "b.txt": ["B3"]},
        "red_test_cmd": "grep -qx A3 a.txt && grep -qx B3 b.txt", "suite_cmd": "test -f a.txt && test -f b.txt"}
EXP1 = {"commit": SHA, "files": ["a.txt"], "expected_added": {"a.txt": ["A3"]},
        "red_test_cmd": "grep -qx A3 a.txt", "suite_cmd": "test -f a.txt"}


def check(tag, diff, exp):
    d = os.path.join(W, tag)
    os.makedirs(d)
    dp, ep = os.path.join(d, "cand.diff"), os.path.join(d, "expect.json")
    with open(dp, "w") as f:
        f.write(diff)
    with open(ep, "w") as f:
        json.dump(exp, f)
    rc, out = sh([sys.executable, CHECK, "--brief-json", ep, "--diff", dp, "--repo", REPO, "--out", os.path.join(d, "ev")])
    got = {}
    for ln in out.splitlines():
        m = re.match(r"^(C\d|VERDICT|APPLY-MODE): (.*)$", ln)
        if m:
            got[m.group(1)] = m.group(2)
    return rc, got, out


def c1(got):
    return (got.get("C1") or "").split(" ")[0]


arms = []


def arm(name, fn):
    try:
        ok, detail = fn()
    except Exception as e:  # an arm that cannot run is a FAIL, never a skip
        ok, detail = False, "error %r" % e
    arms.append(ok)
    print("%s  %s: %s" % ("PASS" if ok else "FAIL", name, detail))


def a_strict():
    rc, g, _ = check("a", A_OK + B_OK, EXP2)
    ok = rc == 0 and c1(g) == "PASS" and g.get("VERDICT") == "PASS" and "recount" not in g.get("VERDICT", "")
    return ok, "rc=%d C1=%s VERDICT=%s" % (rc, c1(g), g.get("VERDICT"))


def b_first_miscount():
    rc, g, _ = check("b", A_MISCOUNT + B_OK, EXP2)
    line = g.get("C1", "")
    # the C1 line must name a.txt as the recount file and b.txt as strict (per-file mode recorded)
    ok = (rc == 0 and c1(g) == "PASS-RECOUNT" and "--recount (hunk header miscounted) for: a.txt;" in line and "strict: b.txt" in line
          and g.get("VERDICT") == "PASS (recount: a.txt)" and all(c1({"C1": g.get(k, "")}) == "PASS" for k in ("C2", "C4", "C5")))
    return ok, "rc=%d C1=%r VERDICT=%r C4=%s" % (rc, line[:110], g.get("VERDICT"), (g.get("C4") or "")[:4])


def b2_second_miscount():
    rc, g, _ = check("b2", A_OK + B_MISCOUNT, EXP2)
    ok = rc == 0 and c1(g) == "PASS-RECOUNT" and g.get("VERDICT") == "PASS (recount: b.txt)"
    return ok, "rc=%d C1=%s VERDICT=%r" % (rc, c1(g), g.get("VERDICT"))


def c_no_apply():
    rc, g, _ = check("c", A_WRONG + B_OK, EXP2)
    ok = rc == 1 and c1(g) == "FAIL" and g.get("VERDICT") == "FAIL" and "a.txt" in g.get("C1", "")
    return ok, "rc=%d C1=%r VERDICT=%s" % (rc, g.get("C1", "")[:90], g.get("VERDICT"))


def d_single_miscount():
    rc, g, _ = check("d", A_MISCOUNT, EXP1)
    ok = rc == 0 and c1(g) == "PASS-RECOUNT" and g.get("VERDICT") == "PASS (recount: a.txt)"
    return ok, "rc=%d C1=%s VERDICT=%r" % (rc, c1(g), g.get("VERDICT"))


def e_split_identity():
    sys.dont_write_bytecode = True
    sys.path.insert(0, SP)
    import spark_check as sc
    samples = [A_OK + B_OK, A_MISCOUNT + B_OK, "diff --git a/a.txt b/a.txt\nindex 1..2 100644\n" + A_OK
               + "diff --git a/b.txt b/b.txt\n" + B_OK, A_OK, (A_OK + B_OK).rstrip("\n"), "preamble line\n" + A_OK + B_OK]
    bad = []
    for s in samples:
        parts = sc.split_per_file(s)
        if "".join(p for _, p in parts) != s:
            bad.append("concat != original")
    two = sc.split_per_file("diff --git a/a.txt b/a.txt\n" + A_OK + "diff --git a/b.txt b/b.txt\n" + B_OK)
    if [p for p, _ in two] != ["a.txt", "b.txt"] or not two[1][1].startswith("diff --git a/b.txt"):
        bad.append("paths/boundaries wrong: %r" % [(p, t[:30]) for p, t in two])
    return not bad, "%d samples byte-identical; boundaries %s" % (len(samples), bad or "ok")


arm("a strict two-file diff -> PASS", a_strict)
arm("b two-file, FIRST header miscounted -> PASS-RECOUNT naming a.txt only", b_first_miscount)
arm("b2 two-file, SECOND header miscounted -> PASS-RECOUNT naming b.txt", b2_second_miscount)
arm("c two-file, content does not match -> FAIL", c_no_apply)
arm("d single-file miscounted -> PASS-RECOUNT", d_single_miscount)
arm("e split per file: concat byte-identical", e_split_identity)
print("evidence under %s" % W)
sys.exit(0 if all(arms) else 1)
