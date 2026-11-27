# n1_extra.py — (a) what the REAL register holds that my surviving register mutants would alter; (b) a register rewritten IN PLACE
# by one plain write (no artificial pause) while builds run; (c) the same hostile cases for --check GREEN after build.
import hashlib, os, re, subprocess, sys, threading, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_copies"))
from qlib import *
REL = "0_Brain/tasks/EXPIRING-GRANTS.md"
BEGIN = b"<<< BEGIN 0_Brain/tasks/EXPIRING-GRANTS.md (verbatim) >>>\n"; END = b"<<< END 0_Brain/tasks/EXPIRING-GRANTS.md (verbatim) >>>\n"
real = open(os.path.join(R, REL), "rb").read(); lines = real.split(b"\n")
print("## a. the REAL register now: %d bytes, %d lines, sha256 %s" % (len(real), len(lines), hashlib.sha256(real).hexdigest()[:16]))
print("- lines ending in a space or tab: %d; CR bytes: %d; NUL bytes: %d; BOM at start: %s; ends with a newline: %s; lines over 2000 characters: %d (longest %d); lines in all: %d (a 120-line cap would drop %d)"
      % (sum(1 for l in lines if l.endswith((b" ", b"\t"))), real.count(b"\r"), real.count(b"\x00"), real.startswith(b"\xef\xbb\xbf"), real.endswith(b"\n"),
         sum(1 for l in lines if len(l.decode("utf-8")) > 2000), max(len(l.decode("utf-8")) for l in lines), len(lines), max(0, len(lines) - 120)))
print("  positive control for the counters: '|' bytes %d, non-ASCII bytes %d" % (real.count(b"|"), sum(1 for c in real if c > 127)))
print("## b. the register rewritten IN PLACE by ONE plain write() per rewrite (no pause), while 60 builds run")
r = mk_real("inplace", "n1x_%d" % os.getpid()); p = os.path.join(r, REL); base = open(p, "rb").read()
row = lambda t: b"| **WEDNESDAY: " + t + b"** | Kam | **No end stated.** | scope |\n"
vers = {}
for k in range(40): vers[hashlib.sha256(base + row(b"QA-V%03d" % k) * (1 + k % 5)).hexdigest()] = k
stop = [False]; nrw = [0]
def churn():
    k = 0
    while not stop[0]:
        v = base + row(b"QA-V%03d" % (k % 40)) * (1 + (k % 40) % 5)
        with open(p, "wb") as f: f.write(v)
        k += 1; nrw[0] += 1; time.sleep(0.002)
th = threading.Thread(target=churn); th.start()
res = {"whole version": 0, "refused rc 2": 0, "rc other": 0, "PARTIAL": 0}; why = {}
for i in range(60):
    outp = os.path.join(r, "0_Brain/wake/try_%d.md" % i)
    pr = subprocess.run([sys.executable, os.path.join(r, "2_Project_Files/wake/wake_pack.py"), "--seat", "wednesday", "--root", r, "--out", outp, "--today", "2026-11-27"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV())
    if pr.returncode == 0:
        pk = rd(outp); b = pk[pk.find(BEGIN) + len(BEGIN):pk.rfind(END)]
        if hashlib.sha256(b).hexdigest() in vers: res["whole version"] += 1
        else: res["PARTIAL"] += 1
    elif pr.returncode == 2:
        res["refused rc 2"] += 1; k = pr.stderr.decode().strip().split("\n")[-1][:90]; why[k] = why.get(k, 0) + 1
    else: res["rc other"] += 1
stop[0] = True; th.join()
print("- %d rewrites happened during the 60 builds: %s; refusal reasons: %s" % (nrw[0], res, why or "-"))
