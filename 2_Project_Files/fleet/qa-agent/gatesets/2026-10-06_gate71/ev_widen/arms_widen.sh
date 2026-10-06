#!/bin/bash
# gate71 widening arms — launcher (--check, G71_* overrides) and repin (--dry-run, G71_LSFILE stand-ins). Writes only under the kit's _scratch/arms_widen.
set -u
K=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate71; A=$K/_scratch/arms_widen; L=$K/launch_qa_secuura_gate71.sh; R=$K/repin_and_launch_gate71.sh
H4=c117c0160684d1ae72b220a8d2ccfe9aafb8eb8d; H8=9414aa54e92ca243565d0d967aad991dc4c13840; DV=b39051390ff6f252601d6f7b45f0ea6c21c31023
FAKE=1234567890abcdef1234567890abcdef12345678
RES=$A/RESULTS.txt; : > $RES
arm() { # name want cmd...
  local n="$1" w="$2"; shift 2
  "$@" > "$A/arm_$n.out" 2> "$A/arm_$n.err"; local rc=$?
  local v="FIRES"; [ "$rc" = "$w" ] || v="DID NOT FIRE AS WANTED"
  printf '%-34s want rc %-3s got rc %-3s %s | %s\n' "$n" "$w" "$rc" "$v" "$(cat "$A/arm_$n.err" "$A/arm_$n.out" | tr -d '\r' | grep -E 'REFUSING|all guards pass|DRY RUN COMPLETE|REFUSED|SELFTEST|PASS M1' | head -1 | cut -c1-170)" >> $RES
}
# ---- launcher (--check) ----
arm L01_rendered_live 0 env G71_PROMPT=$A/rendered.good G71_HEADFILE=$A/head.good $L --check
mkdir -p $A/files_bad; for f in lib_gate71.py composee5_copy.py recompose_gate71.py c1_pin_gate71.py c2_product_gate71.py c3_suites_gate71.py c4_docs_gate71.py c5_job06_gate71.py gh_gate71.py prompt_gate71.txt launch_qa_secuura_gate71.sh repin_and_launch_gate71.sh; do cp -p $K/$f $A/files_bad/$f; done
printf '# tampered\n' >> $A/files_bad/c5_job06_gate71.py
arm L02_badpin_c5 31 env G71_FILES_DIR=$A/files_bad $L --check
python3 -c 'import json,sys; k=json.load(open(sys.argv[1])); k["script_sha256"].pop("recompose_gate71.py"); json.dump(k,open(sys.argv[2],"w"))' $K/kit.json $A/kit_nopin.json
arm L03_nopin_recompose 30 env G71_KITJSON=$A/kit_nopin.json $L --check
mkdir -p $A/files_missing; for f in $(ls $A/files_bad); do [ "$f" = c5_job06_gate71.py ] || cp -p $K/$f $A/files_missing/$f; done
arm L04_missingfile_c5 30 env G71_FILES_DIR=$A/files_missing $L --check
arm L05_unrendered 8 env G71_PROMPT=$K/prompt_gate71.txt G71_HEADFILE=$A/head.good $L --check
sed 's/GO (Seat R 5th): merge 1404 on gate71/GO (Seat R 4th): merge 1404 on gate71/' $A/rendered.good > $A/rendered.goR4
arm L06_GO_names_R4th_merge 8 env G71_PROMPT=$A/rendered.goR4 G71_HEADFILE=$A/head.good $L --check
printf '\nA planted line: GO (Seat R 4th) is how the author would sign.\n' | cat $A/rendered.good - > $A/rendered.goR4bare
arm L07_GO_names_R4th_bare 8 env G71_PROMPT=$A/rendered.goR4bare G71_HEADFILE=$A/head.good $L --check
sed 's/GO (Seat R 5th): merge 1398 on gate71/GO (Seat R 3rd): merge 1398 on gate71/' $A/rendered.good > $A/rendered.goR3
arm L08_GO_names_R3rd 8 env G71_PROMPT=$A/rendered.goR3 G71_HEADFILE=$A/head.good $L --check
sed 's/GO (Seat R 5th): merge 1404 on gate71/(the 1404 GO string removed)/g' $A/rendered.good > $A/rendered.go1only
arm L09_only_one_GO 8 env G71_PROMPT=$A/rendered.go1only G71_HEADFILE=$A/head.good $L --check
grep -v '^P 1404' $A/head.good > $A/head.oneP
arm L10_headfile_one_P 7 env G71_PROMPT=$A/rendered.good G71_HEADFILE=$A/head.oneP $L --check
grep -v '^D ' $A/head.good > $A/head.noD
arm L11_headfile_no_D 7 env G71_PROMPT=$A/rendered.good G71_HEADFILE=$A/head.noD $L --check
awk -v f=$FAKE 'BEGIN{OFS="\t"} $2=="refs/pull/1404/head"{$1=f} {print}' $A/ls.good > $A/ls.moved1404
arm L12_1404_head_moved 6 env G71_PROMPT=$A/rendered.good G71_HEADFILE=$A/head.good G71_LS=$A/ls.moved1404 $L --check
awk -v f=$FAKE 'BEGIN{OFS="\t"} $2=="refs/pull/1398/head"{$1=f} {print}' $A/ls.good > $A/ls.moved1398
arm L13_1398_head_moved 6 env G71_PROMPT=$A/rendered.good G71_HEADFILE=$A/head.good G71_LS=$A/ls.moved1398 $L --check
awk -v f=$FAKE 'BEGIN{OFS="\t"} $2=="refs/heads/feature/ks-1436-tenant-isolation-stderr-own-file-ra4-6"{$1=f} {print}' $A/ls.good > $A/ls.movedbr1404
arm L14_1404_branch_moved 6 env G71_PROMPT=$A/rendered.good G71_HEADFILE=$A/head.good G71_LS=$A/ls.movedbr1404 $L --check
awk 'BEGIN{OFS="\t"} $2=="refs/heads/develop"{$1="40270d263ab00b003055563c33112d7aaf8a95fb"} {print}' $A/ls.good > $A/ls.devmoved
arm L15_develop_moved 17 env G71_PROMPT=$A/rendered.good G71_HEADFILE=$A/head.good G71_LS=$A/ls.devmoved $L --check
sed "s/$H4/$FAKE/g" $A/rendered.good > $A/rendered.fake1404; sed "s/$H4/$FAKE/g" $A/head.good > $A/head.fake1404; sed "s/$H4/$FAKE/g" $A/ls.good > $A/ls.fake1404
arm L16_absent_1404_head 19 env G71_PROMPT=$A/rendered.fake1404 G71_HEADFILE=$A/head.fake1404 G71_LS=$A/ls.fake1404 $L --check
sed "s/$DV/$FAKE/g" $A/rendered.good > $A/rendered.fakedev; sed "s/$DV/$FAKE/g" $A/head.good > $A/head.fakedev; sed "s/$DV/$FAKE/g" $A/ls.good > $A/ls.fakedev
arm L17_absent_develop 19 env G71_PROMPT=$A/rendered.fakedev G71_HEADFILE=$A/head.fakedev G71_LS=$A/ls.fakedev $L --check
python3 -c 'import sys; t=open(sys.argv[1]).read(); open(sys.argv[2],"w").write(t.replace("JOB06-CHAIN","JOB06_CHAIN"))' $A/rendered.good $A/rendered.nokw
arm L18_keyword_missing 33 env G71_PROMPT=$A/rendered.nokw G71_HEADFILE=$A/head.good $L --check
python3 -c 'import sys; t=open(sys.argv[1]).read(); open(sys.argv[2],"w").write(t.replace("ascending order is NOT asserted","ascending order is asserted"))' $A/rendered.good $A/rendered.ascend
arm L19_docs_rule_demands_ascent 33 env G71_PROMPT=$A/rendered.ascend G71_HEADFILE=$A/head.good $L --check
mkdir -p $A/movedkit; cp -p $L $A/movedkit/
arm L20_moved_kit 2 $A/movedkit/launch_qa_secuura_gate71.sh --check
arm L21_launch_non_tty 21 $L < /dev/null
# ---- repin (--dry-run --no-api, stand-ins) ----
arm R01_short_head 9 $R 1404:c117c0160684 1398:$H8 --dry-run --no-api
arm R02_missing_row 9 $R 1404:$H4 --dry-run --no-api
arm R03_noapi_real_launch 9 $R 1404:$H4 1398:$H8 --no-api
arm R04_head_not_in_READY 18 $R 1404:$FAKE 1398:$H8 --dry-run --no-api
arm R05_1404_head_moved 11 env G71_LSFILE=$A/ls.moved1404 $R 1404:$H4 1398:$H8 --dry-run --no-api
arm R06_1398_head_moved 11 env G71_LSFILE=$A/ls.moved1398 $R 1404:$H4 1398:$H8 --dry-run --no-api
awk 'BEGIN{OFS="\t"} $2=="refs/heads/develop"{$1="f556373b941823931a9858a788c478e50e822a79"} {print}' $A/ls.good > $A/ls.devanc
arm R07_dev_not_descendant 13 env G71_LSFILE=$A/ls.devanc $R 1404:$H4 1398:$H8 --dry-run --no-api
awk -v f=$(cat $A/touched06.sha) 'BEGIN{OFS="\t"} $2=="refs/heads/develop"{$1=f} {print}' $A/ls.good > $A/ls.devtouched06
arm R08_dev_touched_job06 13 env G71_LSFILE=$A/ls.devtouched06 $R 1404:$H4 1398:$H8 --dry-run --no-api
awk -v f=$(cat $A/skillother.sha) 'BEGIN{OFS="\t"} $2=="refs/heads/develop"{$1=f} {print}' $A/ls.good > $A/ls.devskill
arm R09_dev_skill_other_blob 13 env G71_LSFILE=$A/ls.devskill $R 1404:$H4 1398:$H8 --dry-run --no-api
arm R10_dev_moved_no_repin 10 env G71_LSFILE=$A/ls.devmoved $R 1404:$H4 1398:$H8 --dry-run --no-api
arm R11_dev_moved_stale_repin 10 env G71_LSFILE=$A/ls.devmoved $R 1404:$H4 1398:$H8 --dry-run --no-api --repin-develop b39051390ff6f252601d6f7b45f0ea6c21c31023
awk -v f=$FAKE 'BEGIN{OFS="\t"} $2=="refs/heads/develop"{$1=f} {print}' $A/ls.good > $A/ls.devabsent
arm R12_dev_absent 19 env G71_LSFILE=$A/ls.devabsent $R 1404:$H4 1398:$H8 --dry-run --no-api
arm R13_dev_moved_repinned 13 env G71_LSFILE=$A/ls.devmoved $R 1404:$H4 1398:$H8 --dry-run --no-api --repin-develop 40270d263ab00b003055563c33112d7aaf8a95fb
# ---- docs arms ----
arm C01_c4_rule_demands_ascent 1 env PYTHONDONTWRITEBYTECODE=1 G71_DOCS_DEMAND_ASCENDING=1 python3 $K/c4_docs_gate71.py --selftest --pr 1404 --repo $K/_scratch/clone
arm C02_1398_keeps_23_fails_UNIQUE 1 env PYTHONDONTWRITEBYTECODE=1 python3 $K/c4_docs_gate71.py predict --pr 1398 --repo $K/_scratch/clone --head $H8 --develop-after 391bdbffa023bc8782466451a40b5df571f2a899 --num-map 23:23
arm C03_1398_ruled_28_predicts 0 env PYTHONDONTWRITEBYTECODE=1 python3 $K/c4_docs_gate71.py predict --pr 1398 --repo $K/_scratch/clone --head $H8 --develop-after 391bdbffa023bc8782466451a40b5df571f2a899 --num-map 23:28
cat $RES
