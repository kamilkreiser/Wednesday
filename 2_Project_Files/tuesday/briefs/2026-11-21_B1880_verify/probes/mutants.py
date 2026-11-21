import sys, os, re, subprocess
W = sys.argv[1]
M = [
 ("b-r6-dash-quoted-key", "build/repo_rules.py", r'''R6_QUOTED_KEY = re.compile(r"""^\s*(?:-\s+)*(["'])''', r'''R6_QUOTED_KEY = re.compile(r"""^\s*(["'])'''),
 ("b-r6-flow-only-after-colon", "build/repo_rules.py", '"{" in bare)', '": {" in bare)'),
 ("b-r6-dash-block-start-unseen", "build/repo_rules.py", r'R6_BLOCK_START = re.compile(r"(?:^\s*|:\s+|^\s*-\s+)[|>]', r'R6_BLOCK_START = re.compile(r"(?:^\s*|:\s+)[|>]'),
 ("b-r6-bash-env-case-sensitive", "build/repo_rules.py", "if R6_SHELL_FILE in line.lower():", 'if "BASH_ENV" in line:'),
 ("b-r7-git-binary-heuristic-8000", "build/repo_rules.py", 'if b"\\0" in data and name', 'if b"\\0" in data[:8000] and name'),
 ("b-r8-space-split-only", "build/repo_rules.py", "for word in line.split()[1:]", 'for word in line.split(" ")[1:]'),
 ("b-r8-tracked-root-file-only", "build/repo_rules.py", "if lower_base == R8_FILE_NAME and", "if lower_name == R8_FILE_NAME and"),
 ("b-sq-control-rc-ignored", "build/squash_scan.py", "control_ok = rc == 1 and found >= 2", "control_ok = found >= 2"),
 ("b-sq-message-copies-unchecked", "build/squash_scan.py", "message_ok = rc == 0 and found == 0 and stored >= 1 and written == 2 * stored", "message_ok = rc == 0 and found == 0"),
 ("b-sq-scratch-inside-checkout-allowed", "build/squash_scan.py", "        if os.path.realpath(scratch).startswith(os.path.realpath(ROOT) + os.sep):\n", "        if False:\n"),
 ("b-sq-halves-any-indent", "build/squash_scan.py", 'raise CutError("a planted half is found twice")', 'pass'),
 ("b-g-name-case-sensitive", "build/release_guard.py", '.rsplit("/", 1)[-1].lower()', '.rsplit("/", 1)[-1]'),
 ("b-g-jceks-name-unseen", "build/release_guard.py", '".jks", ".jceks", ".keystore"', '".jks", ".keystore"'),
 ("b-g-cab-unseen", "build/release_guard.py", ',\n                  b"MSCF")', ')'),
 ("b-g-utf16-pem-text-only", "build/release_guard.py", "        if binary:\n            for encoding", "        if False:\n            for encoding"),
 ("b-ci-tree-length-check-dropped", ".github/workflows/ci.yml", '                  else if (kind[id] == "tree" && (size[id] > 0) != (first[id] > 55)) wrong++\n', ''),
]
def run_suite():
    r = subprocess.run([sys.executable, "-I", "-m", "unittest", "discover", "-s", os.path.join(W, "build/tests")], capture_output=True, text=True)
    out = r.stdout + r.stderr
    fails = sorted(set(re.sub(r" \(.*", "", l) for l in out.splitlines() if l.startswith("FAIL:")))
    errs = [l for l in out.splitlines() if l.startswith("ERROR:")]
    return r.returncode, fails, errs, [l for l in out.splitlines() if l.startswith("Ran ")]
for label, rel, old, new in M:
    p = os.path.join(W, rel)
    orig = open(p, encoding="utf-8", newline="").read()
    n = orig.count(old)
    if n != 1:
        print("%-38s NOT APPLIED (count %d)" % (label, n)); continue
    open(p, "w", encoding="utf-8", newline="").write(orig.replace(old, new))
    try:
        rc, fails, errs, ran = run_suite()
    finally:
        open(p, "w", encoding="utf-8", newline="").write(orig)
    st = subprocess.run(["git", "-C", W, "status", "--porcelain"], capture_output=True, text=True).stdout
    verdict = "KILLED" if (rc != 0 and fails and not errs) else ("ERROR-ONLY" if errs and not fails else ("SURVIVED" if rc == 0 else "KILLED+ERR"))
    print("%-38s %-9s rc %d FAIL %d ERROR %d %s | undone porcelain=%r | %s" % (label, verdict, rc, len(fails), len(errs), ran, st.strip(), "; ".join(f[6:] for f in fails)[:300]))
rc, fails, errs, ran = run_suite()
print("AFTER ALL: rc %d %s FAIL %d ERROR %d" % (rc, ran, len(fails), len(errs)))
