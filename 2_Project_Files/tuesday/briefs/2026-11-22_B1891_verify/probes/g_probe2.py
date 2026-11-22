import sys, os, subprocess, hashlib, base64, shutil
B = sys.argv[1]; OUT = sys.argv[2]
cert = b"\x30\x82\x01\x00" + bytes(range(256))
fp = hashlib.sha256(cert).hexdigest()
open(os.path.join(B, "denylist", "dev_ca_sha256.txt"), "w").write(fp + "\n")
def b64lines(data): 
    s = base64.b64encode(data).decode(); return "\n".join(s[i:i+64] for i in range(0, len(s), 64))
p7 = b"\x30\x82\x01\x10" + b"\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x07\x02" + b"\xa0\x82\x01\x04" + cert
cases = {
 "control-der-cert.cer": cert,
 "control-pem-cert.pem": ("-----BEGIN CERTIFICATE-----\n%s\n-----END CERTIFICATE-----\n" % b64lines(cert)).encode(),
 "p7b-der.p7b": p7,
 "p7b-pem.p7b": ("-----BEGIN PKCS7-----\n%s\n-----END PKCS7-----\n" % b64lines(p7)).encode(),
 "x5c-in-json.json": ('{"x5c": ["%s"]}' % base64.b64encode(cert).decode()).encode(),
 "pem-crlf-lowercase-end.pem": ("-----BEGIN CERTIFICATE-----\r\n%s\r\n-----END CERTIFICATE-----\r\n" % b64lines(cert).replace("\n", "\r\n")).encode(),
 "pem-utf16le-no-bom-no-nul?.pem": ("-----BEGIN CERTIFICATE-----\n%s\n-----END CERTIFICATE-----\n" % b64lines(cert)).encode("utf-16-le"),
}
for name, data in cases.items():
    d = os.path.join(OUT, name.split(".")[0]); os.makedirs(d)
    open(os.path.join(d, name), "wb").write(data)
    for mode in ([], ["--release"]):
        r = subprocess.run([sys.executable, "-I", os.path.join(B, "release_guard.py"), d] + mode, capture_output=True, text=True)
        print("%-32s %-9s rc %d | %s" % (name, "release" if mode else "default", r.returncode, " ; ".join(r.stdout.splitlines())))
