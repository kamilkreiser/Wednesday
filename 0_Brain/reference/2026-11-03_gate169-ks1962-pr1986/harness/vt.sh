#!/bin/bash
# usage: vt.sh <base|head> <outname> [vitest args...]  -- runs the real vitest anchored at the worktree's anchoring dir
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate169-ks1962-pr1986
T=$1; O=$2; shift 2
A=$W/scratch/$T/Blockchain/Dev/services/anchoring
V="$A/../../node_modules/vitest/vitest.mjs"
mkdir -p $W/runs
env -i PATH="$(dirname "$(command -v node)"):/usr/bin:/bin" HOME=$W/home TMPDIR=$W/tmp ${EXTRA_ENV:-} \
  node "$V" run --root "$A" --reporter=json --outputFile="$W/runs/$O.json" "$@" >"$W/runs/$O.stdout" 2>"$W/runs/$O.stderr"
rc=$?
node -e '
const r=require(process.argv[1]);let p=0,f=0,o=[];
for(const t of r.testResults)for(const a of t.assertionResults){if(a.status==="passed")p++;else{f++;o.push("  FAIL "+t.name.split("/__tests__/")[1]+" | "+a.title.slice(0,90)+" | "+(a.failureMessages[0]||"").split("\n")[0].slice(0,140))}}
console.log("rc='$rc' files "+r.testResults.length+" passed "+p+"/"+(p+f)+" failed "+f);o.forEach(x=>console.log(x))' "$W/runs/$O.json" | tee "$W/runs/$O.sum"
