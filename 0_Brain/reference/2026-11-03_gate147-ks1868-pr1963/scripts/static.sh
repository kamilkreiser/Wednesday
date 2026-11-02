#!/bin/bash
# per service: tsc incl. tests (head; base product + new test file removed; planted); service tsc; eslint changed + base + planted. Then docs-fragments with planted defects.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate147-ks1868-pr1963
R=$W/repo; D=$R/Blockchain/Dev; B=$D/node_modules/.bin; MB=4d1ab2cb6574e2b221353ac3a1de56d515711aaf; Q=$W/logs/_quarantine/static
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
for s in kyc wallet-connector; do
  S=$D/services/$s; P=$S/src/userErasedSubscriber.ts; T=src/__tests__/ks1868-$s-user-erased-handler-failed-catch-unreadable-throw.test.ts
  HP=$(sha $P); TC=$W/scripts/tsconfig.tests.$s.json
  tl(){ nice -n 10 $B/tsc -p $TC --listFilesOnly > $W/logs/tsc_files_${s}_$1.log 2>&1; nice -n 10 $B/tsc -p $TC > $W/logs/tsc_tests_${s}_$1.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_${s}_$1.log; }
  tl head
  nice -n 10 $B/tsc -p $S/tsconfig.json --noEmit > $W/logs/tsc_service_${s}_head.log 2>&1; echo "rc=$?" >> $W/logs/tsc_service_${s}_head.log
  echo 'export const g147planted: number = "x";' > $S/src/__tests__/zz_g147_planted.test.ts
  tl planted
  mv $S/src/__tests__/zz_g147_planted.test.ts $Q/zz_g147_planted_$s.test.ts
  git -C $R show $MB:Blockchain/Dev/services/$s/src/userErasedSubscriber.ts > $P
  mv $S/$T $Q/
  tl base
  ( cd $S 2>/dev/null; true )
  node -e 'const {spawnSync}=require("child_process");const fs=require("fs");const [W,S,B,s]=process.argv.slice(1);const r=spawnSync(B+"/eslint",["src/userErasedSubscriber.ts"],{cwd:S,encoding:"utf8"});fs.writeFileSync(W+"/logs/eslint_"+s+"_base.log",(r.stdout||"")+(r.stderr||"")+"\nrc="+r.status+"\n");' $W $S $B $s
  mv $Q/$(basename $T) $S/$T
  git -C $R show pr1963:Blockchain/Dev/services/$s/src/userErasedSubscriber.ts > $P
  node -e '
const { spawnSync } = require("child_process"); const fs = require("fs");
const [W,S,B,s,T] = process.argv.slice(1);
const run = (label, args) => { const r = spawnSync(B + "/eslint", args, { cwd: S, encoding: "utf8" }); fs.writeFileSync(W + "/logs/eslint_" + s + "_" + label + ".log", (r.stdout||"") + (r.stderr||"") + "\nfiles=" + args.join(",") + "\nrc=" + r.status + "\n"); };
run("head", ["src/userErasedSubscriber.ts", T]);
const pl = S + "/src/zz_g147_planted.ts"; fs.writeFileSync(pl, "export function f(): number { const unused = 1; debugger; return 2; }\n");
run("planted", ["src/zz_g147_planted.ts"]); fs.renameSync(pl, W + "/logs/_quarantine/static/zz_g147_planted_" + s + ".ts");
' $W $S $B $s $T
  { for f in head base planted; do echo "$s tsc $f: $(grep -c 'error TS' $W/logs/tsc_tests_${s}_$f.log) errors, $(tail -1 $W/logs/tsc_tests_${s}_$f.log), files under __tests__ $(grep -c '/src/__tests__/' $W/logs/tsc_files_${s}_$f.log), PR test file listed $(grep -c 'user-erased-handler-failed' $W/logs/tsc_files_${s}_$f.log)"; grep 'error TS' $W/logs/tsc_tests_${s}_$f.log | sed 's#.*/src/#   src/#'; done
    echo "$s service tsc: $(grep -c 'error TS' $W/logs/tsc_service_${s}_head.log) $(tail -1 $W/logs/tsc_service_${s}_head.log)"
    for l in head base planted; do echo "$s eslint $l: $(grep -E '^rc=' $W/logs/eslint_${s}_$l.log) $(grep -E 'problem' $W/logs/eslint_${s}_$l.log)"; done
    [ "$(sha $P)" = "$HP" ] && echo "$s static restore OK" || echo "$s static RESTORE FAIL"; } >> $W/logs/static_summary.log
done
F="$R/Projects Documents/fragments"; N=KS-1868-user-erased-handlers.html
chk(){ nice -n 10 node $D/scripts/docs-fragments.mjs check --root $R > "$1" 2>&1; echo "rc=$?" >> "$1"; }
{
chk $W/logs/frag_check_clean.log
for k in flow cheat; do
  f="$F/$k/$N"; h=$(sha "$f"); cp "$f" $Q/frag_orig_$k.html
  printf '\n<div>planted unclosed</div><div>\n' >> "$f"
  chk $W/logs/frag_check_planted_${k}_div.log
  cp $Q/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k div restore OK" || echo "$k div RESTORE FAIL"
  if [ $k = flow ]; then sed 's/<h2><!--n-->\. /<h2>/' $Q/frag_orig_flow.html > "$f"; else sed 's#</table>#</tabl>#' $Q/frag_orig_cheat.html > "$f"; fi
  cmp -s "$f" $Q/frag_orig_$k.html && echo "$k second defect DID NOT APPLY (sed no-op)"
  chk $W/logs/frag_check_planted_${k}_2.log
  cp $Q/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k d2 restore OK" || echo "$k d2 RESTORE FAIL"
done
chk $W/logs/frag_check_after_restore.log
for l in clean planted_flow_div planted_flow_2 planted_cheat_div planted_cheat_2 after_restore; do echo "== $l"; grep -i "KS-1868-user-erased\|finding\|error" $W/logs/frag_check_$l.log | head -3; tail -2 $W/logs/frag_check_$l.log; done
} > $W/logs/frag_summary.log 2>&1
git -C $R status --short > $W/logs/static_status_after.log
echo done > $W/logs/static.done
