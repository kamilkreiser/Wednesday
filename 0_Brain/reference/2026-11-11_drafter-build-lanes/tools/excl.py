import json, sys, re
D = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_drafter-build-lanes/evidence/"
prs = json.load(open(D + "open_prs.json"))
ready = json.load(open(D + "ready_paths.json"))
o139 = ["issuerCert.ts", "services/tokenisation/src/index.ts", "nft.routes.ts", "services/tenant-provisioning/src/index.ts"]
def check(p):
    r = []
    for x in prs:
        if p in x["files"]: r.append("PR%d" % x["number"])
    for k, v in ready.items():
        if k == p: r.append("READY:" + v[0][:40])
    for t in o139:
        if p.endswith(t): r.append("o139")
    return r
if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(p, "->", check(p) or "free")
