import sys, os, re, subprocess, tempfile
H = sys.argv[1]
wf = open(os.path.join(H, ".github/workflows/ci.yml"), encoding="utf-8").read()
halves = dict(re.findall(r"^ {10}(head|tail)='([^']+)'$", wf, re.M))
pv = halves["head"] + halves["tail"]
pv_b = pv.encode()
def run(label, subject, body):
    with tempfile.TemporaryDirectory(dir="/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/724d1912-1eaf-4390-bead-8e0f615c00cd/scratchpad/b1891/sqtmp") as t:
        s = os.path.join(t, "s"); b = os.path.join(t, "b")
        open(s, "wb").write(subject); open(b, "wb").write(body)
        r = subprocess.run([sys.executable, "-I", os.path.join(H, "build/squash_scan.py"), s, b, "--scanner", "/opt/homebrew/bin/gitleaks"], capture_output=True)
        out = (r.stdout + r.stderr).decode("utf-8", "replace")
        assert pv not in out and halves["tail"] not in out, "PLANTED VALUE PRINTED"
        lines = out.strip().splitlines()
        print("%-30s rc %d | %s" % (label, r.returncode, lines[-1][:110] if lines else ""))
os.makedirs("/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/724d1912-1eaf-4390-bead-8e0f615c00cd/scratchpad/b1891/sqtmp", exist_ok=True)
run("clean", b"Add a thing (#99)", b"Body line.\n\nCo-Authored-By: X <noreply@example.invalid>\n")
run("planted-in-subject", b"Add " + pv_b + b" (#99)", b"Body.\n")
run("planted-in-body", b"Add a thing", b"Body\nvalue = \"" + pv_b + b"\"\n")
run("planted-body-crlf", b"Add a thing", b"Body\r\nvalue = \"" + pv_b + b"\"\r\n")
run("planted-split-by-lone-cr", b"Add a thing", b"Body\nvalue = \"" + pv_b[:2] + b"\r" + pv_b[2:] + b"\"\n")
run("planted-after-hash-line", b"Add a thing", b"# note\nvalue = \"" + pv_b + b"\"\n")
run("non-utf8-body", b"Add a thing", b"Body \xff\xfe\n")
run("nul-in-body", b"Add a thing", b"Body \x00 x\n")
run("subject-trailing-cr", b"Add a thing\r", b"Body\n")
run("empty-body", b"Add a thing", b"")
run("subject-two-lines", b"Add\nthing", b"Body\n")
