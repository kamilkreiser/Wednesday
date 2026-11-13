#!/bin/bash
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; W=$F/s78_work2
node -v; npm -v
test ! -e $W/after || { echo after exists; exit 2; }
cp -R $W/merged $W/after
R=$W/after/Blockchain/Dev
# who requires hono in the two locks
python3 -I - <<PY
import json
for p in ["$W/merged/Blockchain/Dev/package-lock.json","$W/merged/Blockchain/Dev/services/mcp-server/package-lock.json"]:
    lk=json.load(open(p))
    print(p.split("merged/")[1])
    for k,v in lk["packages"].items():
        for sec in ("dependencies","peerDependencies","optionalDependencies","devDependencies"):
            if "hono" in (v.get(sec) or {}): print("  ",k or "<root>",sec,"hono",v[sec]["hono"])
    print("   hono entry:", {a:b for a,b in lk["packages"]["node_modules/hono"].items() if a in ("version","peer","dev","engines","resolved")})
    print("   node-server entry peerDeps/peerMeta:", lk["packages"]["node_modules/@hono/node-server"].get("peerDependencies"))
PY
npm view hono@4.13.18 version engines dist-tags --json > $F/s78_npmview_hono.out 2>&1; echo npmview rc=$?; cat $F/s78_npmview_hono.out
echo "== root update"
npm --prefix $R update hono --package-lock-only --ignore-scripts > $F/s78_update_root.out 2>&1; echo rc=$?; cat $F/s78_update_root.out
echo "== isolated mcp"
mkdir -p $W/mcpiso; cp $W/merged/Blockchain/Dev/services/mcp-server/package.json $W/merged/Blockchain/Dev/services/mcp-server/package-lock.json $W/mcpiso/
npm --prefix $W/mcpiso update hono --package-lock-only --ignore-scripts > $F/s78_update_mcp.out 2>&1; echo rc=$?; cat $F/s78_update_mcp.out
git diff --no-index --numstat $W/merged/Blockchain/Dev/package-lock.json $R/package-lock.json
git diff --no-index --numstat $W/merged/Blockchain/Dev/services/mcp-server/package-lock.json $W/mcpiso/package-lock.json
git diff --no-index -U0 $W/merged/Blockchain/Dev/package-lock.json $R/package-lock.json > $F/s78_diff_root.out
git diff --no-index -U0 $W/merged/Blockchain/Dev/services/mcp-server/package-lock.json $W/mcpiso/package-lock.json > $F/s78_diff_mcp.out
grep '^[+-]' $F/s78_diff_root.out; echo ----; grep '^[+-]' $F/s78_diff_mcp.out
