import json, subprocess, sys, itertools
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ba10491f-d904-4eb7-a83b-e46c1bc8cc8e/scratchpad/raise18"
DEV = sys.argv[1]
m = json.load(open(S + "/measure_0a6177.json"))
DOCS = {"Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html",
        "Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html"}
YAML = "Blockchain/Dev/docs/openapi/secuura-api.yaml"
seats = {
    "R18": ["2026-10-07_KS-1274-trivy-bare-object", "2026-10-07_KS-1410-apigw-notifications-500",
            "2026-10-07_KS-1410-apigw-batch-audit-export-500", "2026-10-07_KS-1139-smoke-test-counters-errexit"],
    "E11": ["2026-10-05_KS-591-anchors-post-thread-mint", "2026-10-05_KS-591-billing-customers-bundle",
            "2026-10-05_KS-591-platform-tenants-create-status", "2026-10-05_KS-591-stake-complete-unstake",
            "2026-10-05_KS-591-transfer-delegation-posts", "2026-10-05_KS-1364-analytics-exports-r4",
            "2026-10-05_KS-1364-billing-credits-use-r4", "2026-10-05_KS-1364-originate-share-system-errors",
            "2026-10-05_KS-1364-teams-webhook-notify", "2026-10-06_KS-1364-apigw-batch-certify-delegate",
            "2026-10-05_KS-591-nft-mint-upload-fee", "2026-10-05_KS-1364-nft-ipfs-pin-unpin-size"],
    "G4": ["2026-10-05_KS-593-adminconfig-negative-offset-r2", "2026-10-05_KS-593-share-null-recipient-cp2",
           "2026-10-06_KS-593-signatories-non-uuid-id", "2026-10-05_KS-1171-b1-boundary-pin"],
    "F5": ["2026-10-05_KS-808-applied-counts-skips", "2026-10-06_KS-1355-stack-guard-one-line-per-project",
           "2026-10-06_KS-1328-db-retry-describe-budget"],
}
excluded = ["2026-10-05_KS-865-header-lists-checked-files-r2", "2026-10-05_KS-948-mixed-backtick-r3",
            "2026-10-06_KS-1355-dev-reload-slot-container-r2", "2026-10-07_KS-1432-apigw-ks529-guard-real-predicate",
            "2026-10-07_KS-591-platform-tenant-id-uuid"]
files = {}
for s, items in seats.items():
    fs = set()
    for it in items:
        fs |= set(m[it]["files"])
    if s == "E11":
        fs.add(YAML)
    files[s] = fs
allitems = sum(seats.values(), []) + excluded
unraised = [k for k, r in m.items() if r.get("whole_fwd") == 0 and r.get("whole_rev") != 0]
print("UNRAISED measured:", len(unraised), "| assigned:", len(sum(seats.values(), [])), "| excluded:", len(excluded),
      "| set-equal:", set(unraised) == set(allitems))
for a, b in itertools.combinations(files, 2):
    inter = files[a] & files[b]
    print(f"{a} x {b}: {len(inter)} shared payload files {sorted(inter)}")
# control: the docs pair is shared by every seat (§4) - must read non-empty
print("CONTROL docs ∩ (every seat + docs):", all(DOCS & (files[s] | DOCS) for s in files))
ctl = files["E11"] & (files["E11"] | {"x"})
print("CONTROL self-intersection non-empty:", len(ctl) > 0)
for s in files:
    for f in sorted(files[s]):
        p = subprocess.run(["git", "-C", S + "/clone", "ls-tree", DEV, "--", f], capture_output=True, text=True)
        mode = p.stdout.split()[0] if p.stdout.strip() else "NEW"
        if mode not in ("100644",):
            print(f"  mode {s}: {mode} {f}")
# excluded vs seats
for e in excluded:
    for s in files:
        inter = set(m[e]["files"]) & files[s]
        if inter:
            print(f"EXCLUDED {e} shares {sorted(inter)} with {s}")
