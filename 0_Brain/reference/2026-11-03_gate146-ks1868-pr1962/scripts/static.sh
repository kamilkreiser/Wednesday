#!/bin/bash
# tsc incl. tests (head, base product without the new test, planted); service tsc; eslint changed + base + planted; docs-fragments + planted defects.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate146-ks1868-pr1962
R=$W/repo; D=$R/Blockchain/Dev; T=$D/services/transfer; B=$D/node_modules/.bin; REL=Blockchain/Dev/services/transfer
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
P=src/services/approvalWorkflowService.ts; TN=src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts; H=$(sha $T/$P)
TC=$W/scripts/tsconfig.tests.json
tl(){ nice -n 10 $B/tsc -p $TC --listFilesOnly > $W/logs/tsc_files_$1.log 2>&1; nice -n 10 $B/tsc -p $TC > $W/logs/tsc_tests_$1.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_$1.log; }
tl head
nice -n 10 $B/tsc -p $T/tsconfig.json --noEmit > $W/logs/tsc_service_head.log 2>&1; echo "rc=$?" >> $W/logs/tsc_service_head.log
echo 'export const g146planted: number = "x";' > $T/src/__tests__/zz_g146_planted.test.ts
tl planted
mv $T/src/__tests__/zz_g146_planted.test.ts $W/logs/_quarantine/zz_g146_planted.test.ts
git -C $R show cc33e702:$REL/$P > $T/$P; mv $T/$TN $W/logs/_quarantine/new.test.ts
tl base
mv $W/logs/_quarantine/new.test.ts $T/$TN
node -e 'const {spawnSync}=require("child_process");const fs=require("fs");const [W,D,B]=process.argv.slice(1);const r=spawnSync(B+"/eslint",["services/transfer/src/services/approvalWorkflowService.ts"],{cwd:D,encoding:"utf8"});fs.writeFileSync(W+"/logs/eslint_base.log",(r.stdout||"")+(r.stderr||"")+"\nrc="+r.status+"\n");' $W $D $B
git -C $R show pr1962:$REL/$P > $T/$P
{ for f in head base planted; do echo "$f: $(grep -c 'error TS' $W/logs/tsc_tests_$f.log) errors, $(tail -1 $W/logs/tsc_tests_$f.log), files under transfer/src $(grep -c 'transfer/src/' $W/logs/tsc_files_$f.log) (under __tests__ $(grep -c 'transfer/src/__tests__/' $W/logs/tsc_files_$f.log)), PR test file listed $(grep -c 'ks1868-approval-workflow' $W/logs/tsc_files_$f.log)"; done
  echo "planted errors: $(grep 'error TS' $W/logs/tsc_tests_planted.log | sed 's#.*/src/#src/#')"
  echo "service tsc: $(grep -c 'error TS' $W/logs/tsc_service_head.log) $(tail -1 $W/logs/tsc_service_head.log)"; } > $W/logs/tsc_summary.log
node -e '
const { spawnSync } = require("child_process"); const fs = require("fs");
const [W,D,B] = process.argv.slice(1);
const run = (label, args) => { const r = spawnSync(B + "/eslint", args, { cwd: D, encoding: "utf8" }); fs.writeFileSync(W + "/logs/eslint_" + label + ".log", (r.stdout||"") + (r.stderr||"") + "\nfiles=" + args.join(",") + "\nrc=" + r.status + "\n"); console.log(label, "rc", r.status, ((r.stdout||"").match(/\d+ problems?.*$/m) || ["0 problems"])[0]); };
run("head", ["services/transfer/src/services/approvalWorkflowService.ts","services/transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts"]);
const pl = D + "/services/transfer/src/zz_g146_planted.ts"; fs.writeFileSync(pl, "export function f(): number { const unused = 1; debugger; return 2; }\n");
run("planted", ["services/transfer/src/zz_g146_planted.ts"]); fs.renameSync(pl, W + "/logs/_quarantine/zz_g146_planted.ts");
' $W $D $B > $W/logs/eslint_summary.log 2>&1
echo "base rc: $(tail -1 $W/logs/eslint_base.log)" >> $W/logs/eslint_summary.log
{ [ "$(sha $T/$P)" = "$H" ] && echo "static restore OK" || echo "static RESTORE FAIL"; git -C $R status --short; } > $W/logs/static_restore.log
F="$R/Projects Documents/fragments"; N=KS-1868-transfer-approval-workflow.html
chk(){ nice -n 10 node $D/scripts/docs-fragments.mjs check --root $R > "$1" 2>&1; echo "rc=$?" >> "$1"; }
{
chk $W/logs/frag_check_clean.log
for k in flow cheat; do
  f="$F/$k/$N"; h=$(sha "$f"); cp "$f" $W/logs/_quarantine/frag_orig_$k.html
  printf '\n<div>planted unclosed</div><div>\n' >> "$f"
  chk $W/logs/frag_check_planted_${k}_div.log
  cp $W/logs/_quarantine/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k div restore OK" || echo "$k div RESTORE FAIL"
  if [ $k = flow ]; then sed 's/<h2><!--n-->\. /<h2>/' $W/logs/_quarantine/frag_orig_flow.html > "$f"; else sed 's#</table>#</tabl>#' $W/logs/_quarantine/frag_orig_cheat.html > "$f"; fi
  cmp -s "$f" $W/logs/_quarantine/frag_orig_$k.html && echo "$k second defect DID NOT APPLY (sed no-op)"
  chk $W/logs/frag_check_planted_${k}_2.log
  cp $W/logs/_quarantine/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k d2 restore OK" || echo "$k d2 RESTORE FAIL"
done
chk $W/logs/frag_check_after_restore.log
for l in clean planted_flow_div planted_flow_2 planted_cheat_div planted_cheat_2 after_restore; do echo "== $l"; tail -3 $W/logs/frag_check_$l.log; grep -c "$N" $W/logs/frag_check_$l.log; done
} > $W/logs/frag_summary.log 2>&1
git -C $R status --short > $W/logs/static_status_after.log
echo done > $W/logs/static.done
