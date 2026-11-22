"""B1891 round 2: my five round-1 mutants whose old text moved, re-made on the fixed lines (r-*), and new mutants of
the fixed code (n-*). Each applied once to <worktree>, the suite run, the file written back, porcelain printed.
usage: python3 -I mutants2.py <worktree at the head>"""
import sys, os, re, subprocess
W = sys.argv[1]
RR, RG, SQ = "build/repo_rules.py", "build/release_guard.py", "build/squash_scan.py"
M = [
 ("r-b-r6-flow-only-after-colon", RR, 'or "\\\\" in line or "{" in bare', 'or "\\\\" in line or ": {" in bare'),
 ("r-b-r6-bash-env-case-sensitive", RR, "if any(word in line.lower() for word in R6_SHELL_WORDS):", "if any(word.upper() in line for word in R6_SHELL_WORDS):"),
 ("r-b-r8-space-split-only", RR, 'R8_SEPARATOR = re.compile(r"[ \\t\\r]+")', 'R8_SEPARATOR = re.compile(r" +")'),
 ("r-b-r8-tracked-root-file-only", RR, "        if lower_base == R8_FILE_NAME:\n", "        if lower_name == R8_FILE_NAME:\n"),
 ("r-b-g-cab-unseen", RG, 'b"MSCF\\x00\\x00\\x00\\x00", ', ''),
 ("n-yaml-hash-anywhere", RR, 'elif character == "#" and (at == 0 or line[at - 1] in " \\t"):', 'elif character == "#":'),
 ("n-yaml-quote-anywhere", RR, "starts_token = at == 0 or line[at - 1] in R6_TOKEN_START", "starts_token = True"),
 ("n-yaml-sq-doubled-quote-dropped", RR, "if quote == \"'\" and line[at + 1:at + 2] == \"'\":", "if False:"),
 ("n-yaml-comment-kept", RR, "            break\n        else:\n            out.append(character)", "            out.append(character)\n        else:\n            out.append(character)"),
 ("n-r6-bracket-on-bare", RR, 'or "[" in structure)', 'or "[" in bare)'),
 ("n-r6-bracket-dropped", RR, '\n                or "[" in structure)', ')'),
 ("n-r6-bash-func-dropped", RR, 'R6_SHELL_WORDS = ("bash_env", "bash_func_")', 'R6_SHELL_WORDS = ("bash_env",)'),
 ("n-r8-comment-any-word", RR, 'if words[0].startswith("#"):', 'if any(w.startswith("#") for w in words):'),
 ("n-r8-cr-still-splits-lines", RR, 'enumerate(data.decode("latin-1").split("\\n"), 1)', 'enumerate(data.decode("latin-1").splitlines(), 1)'),
 ("n-g2-base-only", RG, "if CA_NAME in path.lower():", "if CA_NAME in base:"),
 ("n-g3-prefixed-zip-dropped", RG, "or (data[:4] != ZIP_MAGIC and zipfile.is_zipfile(io.BytesIO(data))))", "or False)"),
 ("n-g3-bzip2-any-BZh", RG, 'BZIP2_HEAD = re.compile(rb"BZh[1-9](?:\\x31\\x41\\x59\\x26\\x53\\x59|\\x17\\x72\\x45\\x38\\x50\\x90)")', 'BZIP2_HEAD = re.compile(rb"BZh")'),
 ("n-g3-cpio-binary-one-order", RG, ', b"\\xc7\\x71", b"\\x71\\xc7")', ', b"\\xc7\\x71")'),
 ("n-sq-nul-check-dropped", SQ, 'if "\\0" in subject or "\\0" in body:', 'if False:'),
 ("n-sq-nul-body-only", SQ, 'if "\\0" in subject or "\\0" in body:', 'if "\\0" in body:'),
 ("n-sq-failed-step-not-caught", SQ, "except (subprocess.CalledProcessError, OSError, UnicodeError) as error:", "except ZeroDivisionError as error:"),
]
def run_suite():
    r = subprocess.run([sys.executable, "-I", "-B", "-m", "unittest", "discover", "-s", os.path.join(W, "build/tests")], capture_output=True, text=True)
    out = r.stdout + r.stderr
    fails = sorted(set(re.sub(r" \(.*", "", l) for l in out.splitlines() if l.startswith("FAIL:")))
    errs = [l for l in out.splitlines() if l.startswith("ERROR:")]
    return r.returncode, fails, errs, [l for l in out.splitlines() if l.startswith("Ran ")]
for label, rel, old, new in M:
    p = os.path.join(W, rel)
    orig = open(p, encoding="utf-8", newline="").read()
    n = orig.count(old)
    if n != 1:
        print("%-36s NOT APPLIED (count %d)" % (label, n)); continue
    open(p, "w", encoding="utf-8", newline="").write(orig.replace(old, new))
    try:
        rc, fails, errs, ran = run_suite()
    finally:
        open(p, "w", encoding="utf-8", newline="").write(orig)
    st = subprocess.run(["git", "-C", W, "status", "--porcelain"], capture_output=True, text=True).stdout
    verdict = "KILLED" if (rc != 0 and fails and not errs) else ("ERROR-ONLY" if errs and not fails else ("SURVIVED" if rc == 0 else "KILLED+ERR"))
    print("%-36s %-9s rc %d FAIL %d ERROR %d %s | porcelain=%r | %s" % (label, verdict, rc, len(fails), len(errs), ran, st.strip(), "; ".join(f[6:] for f in fails)[:200]))
rc, fails, errs, ran = run_suite()
print("AFTER ALL: rc %d %s FAIL %d ERROR %d" % (rc, ran, len(fails), len(errs)))
