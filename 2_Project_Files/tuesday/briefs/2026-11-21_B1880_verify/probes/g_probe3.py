import sys, os, io, zipfile, subprocess, tarfile
H, OUT = sys.argv[1], sys.argv[2]
def z(name, data):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as f: f.writestr(name, data)
    return b.getvalue()
cer = b"\x30\x82\x00\x04abcd"
inner = z("ExtSDKRootCA.cer", cer)
d2 = z("in.zip", inner); d3 = z("in2.zip", d2); d4 = z("in3.zip", d3)
tb = io.BytesIO()
with tarfile.open(fileobj=tb, mode="w") as t:
    ti = tarfile.TarInfo("in.zip"); ti.size = len(inner); t.addfile(ti, io.BytesIO(inner))
for label, data in (("zip-depth2", d2), ("zip-depth3", d3), ("zip-depth4", d4), ("zip-in-tar", tb.getvalue())):
    d = os.path.join(OUT, label); os.makedirs(d); open(os.path.join(d, "a.bin"), "wb").write(data)
    r = subprocess.run([sys.executable, "-I", os.path.join(H, "build/release_guard.py"), d], capture_output=True, text=True)
    print("%-12s rc %d | %s" % (label, r.returncode, " ; ".join(l for l in r.stdout.splitlines() if "WARN" not in l)))
