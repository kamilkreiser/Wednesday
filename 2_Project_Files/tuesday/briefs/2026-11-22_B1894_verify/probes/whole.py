"""B1894 round 3: shapes appended to a tree's ci.yml, repo_rules.py of THAT tree run on a fresh git tree (export + git
init + add -A), plus Ruby Psych's reading of jobs.extra. Never prints a line of ci.yml.
usage: python3 -I whole.py <draft clone> <sha> <out folder> <shape-set: n|mine|bytes>"""
import os, subprocess, sys, io, tarfile, json
D, SHA, OUT, SET = sys.argv[1:5]
os.makedirs(OUT)
base_dir = os.path.join(OUT, "_base")
os.makedirs(base_dir)
arc = subprocess.run(["git", "-C", D, "archive", SHA], capture_output=True, check=True).stdout
tarfile.open(fileobj=io.BytesIO(arc)).extractall(base_dir)
assert not os.path.exists(os.path.join(base_dir, "1_Project_Definition"))
ci = open(os.path.join(base_dir, ".github/workflows/ci.yml"), "rb").read()
hid6 = b'      "runs-on": ubuntu-latest\n      "permissions": write-all\n      env: {A: b}\n      steps:\n        - "uses": actions/checkout@main\n        - run: echo "\\x41"\n'
hid4 = b'    "runs-on": ubuntu-latest\n    env: {A: b}\n    steps:\n      - "uses": actions/checkout@main\n      - run: echo "\\x41"\n'
S = {}
if SET == "n":
    S["N1 a-ring-in-trailing-comment"] = "  extra: # \u00c5b: |\n".encode() + hid6
    S["N1 a-ogonek-in-full-line-comment"] = "  extra:\n    # \u0105b: |\n".encode() + hid6
    S["N1 control-plain-a-in-comment"] = b"  extra: # Ab: |\n" + hid6
    S["N2 dq-continuation-less-indented"] = b'  extra:\n    name: "a\n  b: |\n    "\n' + hid4
    S["N2 sq-continuation-less-indented"] = b"  extra:\n    name: 'a\n  b: |\n    '\n" + hid4
    S["N2 dq-continuation-col0"] = b'  extra:\n    name: "a\nb: |\n    "\n' + hid4
    S["N2 control-closed-on-one-line"] = b'  extra:\n    name: "a b: |"\n' + hid4
elif SET == "mine":
    S["D32 plain-key-sq-spans-dq-opener"] = b"  extra:\n    k 'x: \"a'\n  b: |\n    \"\n" + hid4
    S["D32 plain-key-dq-spans-sq-opener"] = b"  extra:\n    k \"x: 'a\"\n  b: |\n    '\n" + hid4
    S["D32 plain-key-sq-spans-dq-col0"] = b"  extra:\n    k 'x: \"a'\nb: |\n    \"\n" + hid4
    S["D32 name-value-sq-spans-dq"] = b"  extra:\n    name: x 'y: \"a'\n  b: |\n    \"\n" + hid4
    S["D32 expression-covers-opener"] = b'  extra:\n    ${{ x: "a }}\n  b: |\n    "\n' + hid4
    S["D32 expression-then-hash"] = b'  extra:\n    k ${{ y }}#: "a\n  b: |\n    "\n' + hid4
    S["D32 control-plain-key-open"] = b'  extra:\n    k x: "a\n  b: |\n    "\n' + hid4
    S["D32 control-hidden-lines-alone"] = b"  extra:\n    name: a\n" + hid4
elif SET == "bytes":
    allowed = set(range(0x20, 0x7f)) | {0x0a}
    for b in range(256):
        if b in allowed or b == 0:
            continue
        S["byte-%02x" % b] = b"  extra: # " + bytes([b]) + b"b: |\n" + hid6
    for label, seq in (("C2 85 NEL", "\u0085"), ("E2 80 A8 LS", "\u2028"), ("E2 80 A9 PS", "\u2029"), ("EF BB BF BOM", "\ufeff"), ("C4 85", "\u0105")):
        S["utf8-" + label] = ("  extra: # " + seq + "b: |\n").encode() + hid6
    S["bom-at-file-start"] = "\ufeff".encode() + ci + b"  extra:\n    name: a\n"
    S["no-final-lf-cr-at-end"] = ci + b"  extra:\n    name: a\r"
    S["control-plain"] = b"  extra: # Ab: |\n" + hid6
for label, tail in S.items():
    d = os.path.join(OUT, label.replace(" ", "_"))
    subprocess.run(["cp", "-Rc", base_dir, d], check=True)
    wf = os.path.join(d, ".github/workflows/ci.yml")
    data = tail if label == "bom-at-file-start" else ci + tail
    if label == "no-final-lf-cr-at-end":
        data = tail
    open(wf, "wb").write(data)
    g = lambda *a: subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True)
    g("init", "-q"); g("add", "-A")
    r = subprocess.run([sys.executable, "-I", os.path.join(d, "build/repo_rules.py"), d], capture_output=True, text=True)
    find = [l[7:] for l in r.stdout.splitlines() if l.startswith("RULES: ")]
    ps = ""
    if SET != "bytes":
        p = subprocess.run(["/usr/bin/ruby", "-ryaml", "-rjson", "-e", 'begin; y = YAML.load(STDIN.read); e = y["jobs"]["extra"]; print(e.keys.inspect); rescue => x; print("INVALID " + x.class.to_s + ": " + x.message[0,90]); end'], input=data, capture_output=True)
        ps = " | Psych " + p.stdout.decode("utf-8", "replace")
    print("%-40s rc %d %s%s" % (label, r.returncode, " ; ".join(find)[:150], ps))
