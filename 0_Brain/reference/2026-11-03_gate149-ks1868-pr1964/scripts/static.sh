#!/bin/bash
# tsc incl. tests (head, base products + no new tests, planted); service tsc; eslint changed + planted; docs-fragments with planted defects.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964
R=$W/repo; D=$R/Blockchain/Dev; O=$D/services/originate; B=$D/node_modules/.bin; REL=Blockchain/Dev/services/originate
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
P1=src/routes/documents.ts; H1=$(sha $O/$P1)
T1=src/__tests__/ks1868-documents-lookup-routes-message-coercion-unreadable-throw.test.ts; T2=src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts
TC=$W/scripts/tsconfig.tests.json
tl(){ nice -n 10 $B/tsc -p $TC --listFilesOnly > $W/logs/tsc_files_$1.log 2>&1; nice -n 10 $B/tsc -p $TC > $W/logs/tsc_tests_$1.log 2>&1; echo "rc=$?" >> $W/logs/tsc_tests_$1.log; }
tl head
nice -n 10 $B/tsc -p $O/tsconfig.json --noEmit > $W/logs/tsc_service_head.log 2>&1; echo "rc=$?" >> $W/logs/tsc_service_head.log
echo 'export const g149planted: number = "x";' > $O/src/__tests__/zz_g149_planted.test.ts
tl planted
mv $O/src/__tests__/zz_g149_planted.test.ts $W/logs/_quarantine/zz_g149_planted.test.ts
git -C $R show 4d1ab2cb6574:$REL/$P1 > $O/$P1
mv $O/$T1 $W/logs/_quarantine/t1.ts; mv $O/$T2 $W/logs/_quarantine/t2.ts
tl base
mv $W/logs/_quarantine/t1.ts $O/$T1; mv $W/logs/_quarantine/t2.ts $O/$T2
git -C $R show pr1964:$REL/$P1 > $O/$P1
{ for f in head base planted; do echo "$f: $(grep -c 'error TS' $W/logs/tsc_tests_$f.log) errors, $(tail -1 $W/logs/tsc_tests_$f.log), files $(grep -c '/src/' $W/logs/tsc_files_$f.log) (under __tests__ $(grep -c '/src/__tests__/' $W/logs/tsc_files_$f.log)), PR test files listed $(grep -c 'ks1868-documents-lookup\|ks1868-documents-signing' $W/logs/tsc_files_$f.log)"; done
  echo "planted errors: $(grep 'error TS' $W/logs/tsc_tests_planted.log | sed 's#.*/src/#src/#' )"
  echo "service tsc: $(grep -c 'error TS' $W/logs/tsc_service_head.log) $(tail -1 $W/logs/tsc_service_head.log)"; } > $W/logs/tsc_summary.log
# eslint (cwd = originate, its own flat config)
node -e '
const { spawnSync, execFileSync } = require("child_process"); const fs = require("fs");
const [W,O,B,R] = process.argv.slice(1);
const run = (label, args) => { const r = spawnSync(B + "/eslint", args, { cwd: O, encoding: "utf8" }); fs.writeFileSync(W + "/logs/eslint_" + label + ".log", (r.stdout||"") + (r.stderr||"") + "\nfiles=" + args.join(",") + "\nrc=" + r.status + "\n"); console.log(label, "rc", r.status, ((r.stdout||"").match(/\d+ problems?.*$/m) || ["0 problems"])[0]); };
run("head", ["src/routes/documents.ts","src/__tests__/ks1868-documents-lookup-routes-message-coercion-unreadable-throw.test.ts","src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts"]);
const pl = O + "/src/zz_g149_planted.ts"; fs.writeFileSync(pl, "export function f(): number { const unused = 1; debugger; return 2; }\n");
run("planted", ["src/zz_g149_planted.ts"]); fs.renameSync(pl, W + "/logs/_quarantine/zz_g149_planted.ts");
' $W $O $B $R > $W/logs/eslint_summary.log 2>&1
# eslint at base product files
git -C $R show 4d1ab2cb6574:$REL/$P1 > $O/$P1
node -e 'const {spawnSync}=require("child_process");const fs=require("fs");const [W,O,B]=process.argv.slice(1);const r=spawnSync(B+"/eslint",["src/routes/documents.ts"],{cwd:O,encoding:"utf8"});fs.writeFileSync(W+"/logs/eslint_base.log",(r.stdout||"")+(r.stderr||"")+"\nrc="+r.status+"\n");console.log("base rc",r.status);' $W $O $B >> $W/logs/eslint_summary.log 2>&1
git -C $R show pr1964:$REL/$P1 > $O/$P1
{ [ "$(sha $O/$P1)" = "$H1" ] && echo "static restore OK" || echo "static RESTORE FAIL"; git -C $R status --short; } > $W/logs/static_restore.log
# fragments
F="$R/Projects Documents/fragments"; N=KS-1868-documents-routes.html
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
for l in clean planted_flow_div planted_flow_2 planted_cheat_div planted_cheat_2 after_restore; do echo "== $l"; tail -3 $W/logs/frag_check_$l.log; done
} > $W/logs/frag_summary.log 2>&1
git -C $R status --short > $W/logs/static_status_after.log
echo done > $W/logs/static.done
