import sys, os, io, zipfile, subprocess, shutil, gzip, struct, lzma
H = sys.argv[1]; OUT = sys.argv[2]
G = os.path.join(H, "build", "release_guard.py")
def folder(label, files):
    d = os.path.join(OUT, label)
    os.makedirs(d)
    for name, data in files.items():
        p = os.path.join(d, name); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(data)
    return d
def run(label, files, *extra):
    d = folder(label, files)
    r = subprocess.run([sys.executable, "-I", G, d] + list(extra), capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if not l.startswith("GUARD-WARN")]
    print("%-34s rc %d | %s" % (label, r.returncode, " ; ".join(l.replace(d, "<d>") for l in lines)))
cer = b"\x30\x82\x01\x00" + b"\x00" * 256
def zipped(members, prefix=b""):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in members.items(): z.writestr(n, data)
    return prefix + b.getvalue()
run("control-ca-name", {"ExtSDKRootCA.cer": cer})
run("ca-name-with-bang-after", {"ExtSDKRootCA!.cer": cer})
run("ca-name-bang-in-zip-member", {"a.zip": zipped({"ExtSDKRootCA!x.cer": cer})})
run("control-zip-member", {"a.zip": zipped({"ExtSDKRootCA.cer": cer})})
run("zip-with-1-byte-prefix", {"a.bin": zipped({"ExtSDKRootCA.cer": cer}, b"\n")})
run("zip-empty-eocd-start", {"a.zip": b"PK\x05\x06" + b"\x00" * 18})
run("lz4-frame", {"a.lz4": b"\x04\x22\x4d\x18" + b"\x00" * 40})
run("unix-compress-Z", {"a.Z": b"\x1f\x9d\x90" + b"\x00" * 40})
run("lzma-alone", {"a.lzma": lzma.compress(b"ExtSDKRootCA" * 10, format=lzma.FORMAT_ALONE)})
run("ar-archive", {"a.a": b"!<arch>\nExtSDKRootCA.c/0           0     0     644     260       `\n" + cer})
run("cpio-newc", {"a.cpio": b"070701" + b"0" * 104 + b"ExtSDKRootCA.cer\x00" + cer})
run("control-gzip", {"a.gz": gzip.compress(b"hello")})
run("lib-utf16be-at-eof", {"a.dat": b"\x00\x01" + "OXPd2Lib".encode("utf-16-be")})
run("lib-utf16be-mid", {"a.dat": b"\x00\x01" + "OXPd2Lib.".encode("utf-16-be")})
run("lib-utf32le", {"a.dat": b"\x00" + "OXPd2Lib".encode("utf-32-le")})
run("lib-text-no-nul", {"a.deps.json": b'{"OXPd2Lib/1.0": {}}'})
run("clean-text-starting-BZh", {"notes.txt": b"BZh is how a bzip2 file starts\n"})
run("clean-text-starting-MSCF", {"MSCF.txt": b"MSCF: a cabinet header word\n"})
run("clean-dll-with-bang-name", {"a!b.dll": b"MZ\x00\x00"})
run("release-clean-folder", {"a.txt": b"hello\n"}, "--release")
