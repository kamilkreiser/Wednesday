"""B1891 round 2: archive or compressed formats WITH magic bytes that the README's G3 list does not name.
usage: python3 -I g3_more.py <head clone> <out folder>"""
import sys, os, subprocess, zlib
H, OUT = sys.argv[1], sys.argv[2]
G = os.path.join(H, "build", "release_guard.py")
cases = {
 "lzip": b"LZIP\x01" + b"\x00" * 40,
 "zlib-stream": zlib.compress(b"ExtSDKRootCA.cer " * 20),
 "ole-cfb-msi": b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 40,
 "xar": b"xar!\x00\x1c" + b"\x00" * 40,
 "squashfs": b"hsqs" + b"\x00" * 40,
 "wim": b"MSWIM\x00\x00\x00" + b"\x00" * 40,
 "control-xz": b"\xfd7zXZ\x00" + b"\x00" * 40,
}
for label, data in cases.items():
    d = os.path.join(OUT, label); os.makedirs(d); open(os.path.join(d, "a.bin"), "wb").write(data)
    r = subprocess.run([sys.executable, "-I", G, d], capture_output=True, text=True)
    print("%-14s rc %d | %s" % (label, r.returncode, " ; ".join(l for l in r.stdout.splitlines() if "WARN" not in l)))
