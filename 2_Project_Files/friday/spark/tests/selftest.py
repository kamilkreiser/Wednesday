#!/usr/bin/env python3
"""Self-test for spark_run.py / spark_check.py on a synthetic fixture. Never calls the endpoint."""
import json
import os
import re
import subprocess
import sys
import time

ST = os.path.dirname(os.path.abspath(__file__))
SPARK = os.path.dirname(ST)  # self-locating: tests/ sits inside the spark folder
RUN = os.path.join(SPARK, "spark_run.py")
CHECK = os.path.join(SPARK, "spark_check.py")
STAMP = time.strftime("%Y%m%d-%H%M%S")
import tempfile
W = os.path.join(tempfile.mkdtemp(prefix="spark_selftest_"), "run_" + STAMP)  # never beside the tracked tests (a fixture repo got committed once)
REPO = os.path.join(W, "fixture repo")  # space in path on purpose
os.makedirs(REPO)


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def sh(args, cwd=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


# ---------------- fixture ----------------
w(os.path.join(REPO, "calc.py"), '"""Tiny calculator fixture."""\n\n\ndef add(a, b):\n    return a + b\n\n\ndef mul(a, b):\n    return a + b\n')
w(os.path.join(REPO, "test_calc.py"), 'import unittest\n\nimport calc\n\n\nclass TestCalc(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(calc.add(2, 3), 5)\n\n\nif __name__ == "__main__":\n    unittest.main()\n')
w(os.path.join(REPO, "README.md"), "# fixture\n\nNothing here.\n")
for a in (["init", "-q"], ["config", "user.email", "selftest@example.invalid"], ["config", "user.name", "selftest"],
          ["add", "-A"], ["commit", "-q", "-m", "fixture"]):
    rc, out = sh(["git", "-C", REPO] + a)
    assert rc == 0, out
SHA = sh(["git", "-C", REPO, "rev-parse", "HEAD"])[1].strip()

CALC_HUNK = """--- a/calc.py
+++ b/calc.py
@@ -7,3 +7,3 @@
<SP>
 def mul(a, b):
-    return a + b
+    return a * b
"""
TEST_HUNK = """--- a/test_calc.py
+++ b/test_calc.py
@@ -8,3 +8,6 @@
         self.assertEqual(calc.add(2, 3), 5)
+
+    def test_mul(self):
+        self.assertEqual(calc.mul(3, 4), 12)
<SP>
<SP>
"""
README_HUNK = """--- a/README.md
+++ b/README.md
@@ -1,3 +1,4 @@
 # fixture
<SP>
 Nothing here.
+Touched by an unnamed-file diff.
"""
# blank context lines must be a single space; written as a placeholder so no editor strips them
CALC_HUNK, TEST_HUNK, README_HUNK = [h.replace("<SP>", " ") for h in (CALC_HUNK, TEST_HUNK, README_HUNK)]
GOOD = CALC_HUNK + TEST_HUNK
MISCOUNT = GOOD.replace("@@ -7,3 +7,3 @@", "@@ -7,3 +7,4 @@")  # over-count: strict refuses, --recount rescues
UNDERCOUNT = GOOD.replace("@@ -7,3 +7,3 @@", "@@ -7,3 +7,2 @@")  # under-count: strict 'applies' but drops the + line
NOAPPLY = GOOD.replace("@@ -7,3 +7,3 @@", "@@ -70,3 +70,3 @@").replace(" def mul(a, b):", " def div(a, b):")
UNNAMED = GOOD + README_HUNK

EXP = {
    "commit": SHA,
    "files": ["calc.py", "test_calc.py"],
    "expected_added": {"calc.py": ["    return a * b"],
                       "test_calc.py": ["", "    def test_mul(self):", "        self.assertEqual(calc.mul(3, 4), 12)"]},
    "red_test_cmd": "python3 -c 'import calc; assert calc.mul(3, 4) == 12, calc.mul(3, 4)'",
    "suite_cmd": "python3 -m unittest -v",
    "suite_count_regex": r"^Ran (?P<passed>\d+) tests?",
}


def variant(**kw):
    e = json.loads(json.dumps(EXP))
    e.update(kw)
    return e


EXP_C2 = variant(expected_added={"calc.py": ["    return a * b "], "test_calc.py": EXP["expected_added"]["test_calc.py"]})
EXP_C3 = variant(expected_added=dict(EXP["expected_added"], **{"README.md": ["Touched by an unnamed-file diff."]}))
EXP_C4 = variant(red_test_cmd="python3 -c 'import calc; assert calc.add(2, 3) == 5'")
EXP_NULLRED = variant(red_test_cmd=None)

cases = [
    ("a correct diff", GOOD, EXP, {"VERDICT": "PASS", "C1": "PASS", "APPLY-MODE": "strict"}),
    # kit clause 1: a recount-only apply is acceptable IF recorded and never called clean (changed 2026-09-26)
    ("b miscounted hunk header", MISCOUNT, EXP, {"VERDICT": "PASS", "C1": "PASS-RECOUNT", "APPLY-MODE": "recount",
                                                 "_C1_has": "VERDICT: PASS (recount: calc.py)"}),
    ("b2 under-counted header (extra)", UNDERCOUNT, EXP, {"VERDICT": "FAIL", "C1": "FAIL", "APPLY-MODE": "strict",
                                                         "_C1_has": "something DIFFERENT from the diff text"}),
    ("c expected_added off by 1 char", GOOD, EXP_C2, {"VERDICT": "FAIL", "C2": "FAIL", "C1": "PASS", "C3": "PASS"}),
    ("d touches unnamed README.md", UNNAMED, EXP_C3, {"VERDICT": "FAIL", "C3": "FAIL", "C1": "PASS", "C2": "PASS"}),
    ("e red test passes w/o change", GOOD, EXP_C4, {"VERDICT": "FAIL", "C4": "FAIL", "C1": "PASS"}),
    ("f non-existent line range", NOAPPLY, EXP, {"VERDICT": "FAIL", "C1": "FAIL", "APPLY-MODE": "none",
                                                 "C4": "NOT-RUN", "C5": "NOT-RUN"}),
    ("g red_test_cmd null (extra)", GOOD, EXP_NULLRED, {"VERDICT": "INCOMPLETE", "C4": "NOT-RUN", "C1": "PASS"}),
]

rows = []
all_ok = True
for i, (name, diff, exp, want) in enumerate(cases):
    cdir = os.path.join(W, "case_%s" % name.split()[0])
    os.makedirs(cdir)
    dp = os.path.join(cdir, "cand.diff")
    ep = os.path.join(cdir, "expect.json")
    w(dp, diff)
    w(ep, json.dumps(exp, indent=2))
    rc, out = sh([sys.executable, CHECK, "--brief-json", ep, "--diff", dp, "--repo", REPO,
                  "--out", os.path.join(cdir, "evidence")])
    w(os.path.join(cdir, "check_stdout.txt"), out)
    got = {}
    for ln in out.splitlines():
        m = re.match(r"^(C\d|VERDICT|APPLY-MODE): (\S+)", ln)
        if m:
            got[m.group(1)] = m.group(2)
    ok = all(got.get(k) == v for k, v in want.items() if not k.startswith("_"))
    if "_C1_has" in want:
        ok = ok and want["_C1_has"] in out
    exp_rc = {"PASS": 0, "FAIL": 1, "INCOMPLETE": 2}[want["VERDICT"]]
    ok = ok and rc == exp_rc
    all_ok &= ok
    rows.append((name, ", ".join("%s=%s" % (k, v) for k, v in want.items() if not k.startswith("_")),
                 "rc=%d %s" % (rc, " ".join("%s=%s" % (k, got.get(k)) for k in
                                            ["C1", "C2", "C3", "C4", "C5", "C6", "APPLY-MODE", "VERDICT"])),
                 "OK" if ok else "MISMATCH"))
    print("---- case %s (rc=%d) ----\n%s" % (name, rc, out))

# source working copy must be untouched
rc, st = sh(["git", "-C", REPO, "status", "--porcelain"])
clean = rc == 0 and st.strip() == ""
all_ok &= clean
rows.append(("source repo untouched after all checks", "clean", "clean" if clean else st.strip(), "OK" if clean else "MISMATCH"))

# ---------------- spark_run ----------------
BRIEF = """# FIX-1 mul-multiplies — make calc.mul multiply instead of add

File: `calc.py`
Tip: `%s`
Runner: `python3 -m unittest`

## The exact change

Edit 1 — line 9, replacement.

```
-    return a + b
+    return a * b
```

## The test

File: `test_calc.py`

## Output

Exactly ONE fenced diff block, nothing outside it.
""" % SHA[:12]
bp = os.path.join(W, "brief.md")
w(bp, BRIEF)
rdir = os.path.join(W, "run_dry")
rc, out = sh([sys.executable, RUN, "--brief", bp, "--repo", REPO, "--out", rdir, "--dry-run"])
print("---- spark_run dry-run (rc=%d) ----\n%s" % (rc, out))
ok = rc == 0
detail = "rc=%d" % rc
try:
    req = json.load(open(os.path.join(rdir, "request.json")))
    um = req["messages"][1]["content"]
    checks = {
        "thinking false": req["chat_template_kwargs"] == {"thinking": False},
        "temperature 0": req["temperature"] == 0,
        "system=01 contract": req["messages"][0]["role"] == "system" and "Your task contract" in req["messages"][0]["content"],
        "brief included": "FIX-1 mul-multiplies" in um,
        "calc.py header": "=== FILE: calc.py — 9 lines" in um,
        "test_calc.py header": "=== FILE: test_calc.py — 12 lines" in um,
        "numbered line 0009": "0009|     return a + b" in um,
        "no response.json": not os.path.exists(os.path.join(rdir, "response.json")),
    }
    ok = ok and all(checks.values())
    detail += " " + ", ".join("%s=%s" % (k, v) for k, v in checks.items())
except Exception as e:
    ok = False
    detail += " error %r" % e
all_ok &= ok
rows.append(("run --dry-run builds request.json", "rc=0, thinking false, numbered lines, 2 files", detail, "OK" if ok else "MISMATCH"))


def refusal(name, brief_text, expect_substr, brief_path=None):
    global all_ok
    p = brief_path or os.path.join(W, "brief_%s.md" % name)
    if brief_text is not None:
        w(p, brief_text)
    d = os.path.join(W, "run_" + name)
    rc, out = sh([sys.executable, RUN, "--brief", p, "--repo", REPO, "--out", d, "--dry-run"])
    print("---- spark_run refusal %s (rc=%d) ----\n%s" % (name, rc, out))
    ok = rc == 2 and expect_substr in out and not os.path.exists(os.path.join(d, "request.json"))
    all_ok &= ok
    rows.append(("run refusal: " + name, "rc=2, '%s', no request.json" % expect_substr,
                 "rc=%d %s" % (rc, "msg found" if expect_substr in out else "msg MISSING"), "OK" if ok else "MISMATCH"))


refusal("tip-mismatch", BRIEF.replace(SHA[:12], "deadbeefdead"), "is NOT at brief Tip")
refusal("no-tip", re.sub(r"(?m)^Tip:.*\n", "", BRIEF), "no `Tip:` line")
refusal("missing-brief", None, "a brief-less run is a refusal", brief_path=os.path.join(W, "nope.md"))
refusal("file-not-at-tip", BRIEF.replace("File: `calc.py`", "File: `calc2.py`"), "does not exist at tip")

# extraction logic, exercised offline via import
# ---------------- spark_run against a LOCAL FAKE endpoint (never the real one) ----------------
import http.server  # noqa: E402
import threading  # noqa: E402

FAKE = {"content": "", "finish": "stop"}


class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(n))
        FAKE["last_req"] = body
        out = json.dumps({"choices": [{"message": {"role": "assistant", "content": FAKE["content"]},
                                        "finish_reason": FAKE["finish"]}],
                          "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


srv = http.server.HTTPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
FAKE_URL = "http://127.0.0.1:%d/v1" % srv.server_address[1]
fake_cases = [
    ("one diff block", "```diff\n" + GOOD + "```\n", "stop", 0, "wrote"),
    ("STOP refusal", "STOP: the file does not match the brief at line 9.", "stop", 3, "MODEL REFUSED (STOP)"),
    ("finish=length", "```diff\n--- a/calc.py\n", "length", 4, "finish_reason=length"),
    ("empty content", "", "stop", 4, "empty content"),
    ("two diff blocks", "```diff\n" + CALC_HUNK + "```\n\n```diff\n" + TEST_HUNK + "```\n", "stop", 3,
     "NOT EXACTLY ONE FENCED DIFF BLOCK"),
    ("prose + diff (warn)", "Here you go:\n```diff\n" + GOOD + "```\n", "stop", 0, "OUTSIDE the diff block"),
]
for name, content, finish, want_rc, want_msg in fake_cases:
    FAKE["content"], FAKE["finish"] = content, finish
    d = os.path.join(W, "fake_" + name.split()[0] + "_" + name.split()[-1].strip("()"))
    rc, out = sh([sys.executable, RUN, "--brief", bp, "--repo", REPO, "--out", d, "--base-url", FAKE_URL])
    print("---- spark_run fake endpoint: %s (rc=%d) ----\n%s" % (name, rc, out))
    has_diff = os.path.exists(os.path.join(d, "answer.diff"))
    ok = rc == want_rc and want_msg in out and has_diff == (want_rc == 0) \
        and FAKE["last_req"]["chat_template_kwargs"] == {"thinking": False}
    if ok and want_rc == 0:
        ok = open(os.path.join(d, "answer.diff")).read() == GOOD
    all_ok &= ok
    rows.append(("run vs fake endpoint: " + name, "rc=%d, '%s', answer.diff %s" % (want_rc, want_msg, "yes" if want_rc == 0 else "no"),
                 "rc=%d answer.diff=%s" % (rc, "yes" if has_diff else "no"), "OK" if ok else "MISMATCH"))
srv.shutdown()

# end to end: the fake model's answer.diff through the checker
d = os.path.join(W, "fake_one_block")
rc, out = sh([sys.executable, CHECK, "--brief-json", os.path.join(W, "case_a", "expect.json"),
              "--diff", os.path.join(d, "answer.diff"), "--repo", REPO, "--out", os.path.join(d, "evidence")])
ok = rc == 0 and "VERDICT: PASS" in out
all_ok &= ok
rows.append(("e2e: fake answer.diff -> spark_check", "VERDICT PASS", "rc=%d %s" % (rc, out.strip().splitlines()[-1]), "OK" if ok else "MISMATCH"))

sys.dont_write_bytecode = True
sys.path.insert(0, SPARK)
import spark_run as sr  # noqa: E402
one = "```diff\n" + GOOD + "```\n"
two = one + "\n```diff\n" + CALC_HUNK + "```\n"
ex = {
    "one diff block -> 1": len([b for b in sr.extract_fenced_blocks(one) if sr.looks_like_diff(b[0], b[1])]) == 1,
    "two diff blocks -> 2": len(sr.extract_fenced_blocks(two)) == 2,
    "empty-string + line kept": sr.extract_fenced_blocks(one)[0][1].split("\n").count("+") == 1,
}
ok = all(ex.values())
all_ok &= ok
rows.append(("run fence extraction (offline)", "1 / 2 blocks", str(ex), "OK" if ok else "MISMATCH"))

print("\n==== SELF-TEST TABLE (%s) ====" % W)
for r in rows:
    print(" | ".join(r))
print("ALL OK" if all_ok else "SOME MISMATCH")
sys.exit(0 if all_ok else 1)
