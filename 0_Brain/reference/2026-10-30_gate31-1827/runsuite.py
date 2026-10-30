#!/usr/bin/env python3
"""Gate 31: whole api-gateway suite in one tree. Waits until the 1-min load is < 8, then runs vitest (json) with
cwd = services/api-gateway. usage: runsuite.py <tree-root> <label>"""
import json, os, subprocess, sys, time

root, label = sys.argv[1], sys.argv[2]
GW = f"{root}/Blockchain/Dev/services/api-gateway"
OUT = os.path.dirname(os.path.abspath(__file__)) + f"/suite_{label}.json"
waited = 0
while os.getloadavg()[0] >= 8:
    time.sleep(15); waited += 15
load = os.getloadavg()[0]
t0 = time.time()
r = subprocess.run([f"{GW}/../../node_modules/.bin/vitest", "run", "--maxWorkers=3", "--reporter=json", f"--outputFile={OUT}"],
                   cwd=GW, capture_output=True, text=True)
d = json.load(open(OUT))
reds = [f["name"].split("/")[-1] + " :: " + a["title"][:80] for f in d["testResults"] for a in f["assertionResults"] if a["status"] == "failed"]
ffail = [f["name"].split("/")[-1] + " :: " + (f.get("message") or "")[:200] for f in d["testResults"] if f["status"] == "failed"]
print(f"{label}: files {len(d['testResults'])} (failed files {d['numFailedTestSuites']}) | tests {d['numPassedTests']} pass / "
      f"{d['numFailedTests']} fail / {d['numPendingTests']} skipped / {d['numTotalTests']} total | rc={r.returncode} | "
      f"{time.time()-t0:.0f}s | start load {load:.1f} after waiting {waited}s")
for x in reds: print("  RED", x)
for x in ffail: print("  FILE", x)
