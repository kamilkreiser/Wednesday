#!/bin/bash
# regenerates the operator-14 briefs from the clone checked out at the base; usage: gen_all.sh <spec-basename>...
TIP=7152ac669d2d6af08be5b9dcd35132818377155d
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator14
export GEN_TIP=$TIP GEN_SRC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/7fe6fe98-e251-41b8-83ea-c831f0aa2549/scratchpad/op14/src GEN_OVERWRITE=1
B=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs
for s in "$@"; do
  python3 -I /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk_testonly.py $R/$s.py || exit 1
  case $s in spec1830b) n=ks_1830_p2_charclass_sweep;; spec1815b) n=ks_1815_p3_trailing_comment;; spec1816b) n=ks_1816_p1_message_less;; esac
  case $s in spec1830b) so='KS-1830 follow-up: PR 1817 merged at 7152ac66; this brief edits ONE existing test file, no product line; no open PR (20 checked) touches it';; spec1815b) so='KS-1827 follow-up: PR 1815 merged; this brief edits ONE existing test file, no product line; no open PR (20 checked) touches it';; spec1816b) so='KS-1817 follow-up: PR 1816 merged; this brief edits ONE existing test file, no product line; no open PR (20 checked) touches it';; esac
  d=$B/$n
  sed -i '' '/^Tip:/s/on 2026-10-28/on 2026-10-30/' $d/KS-*.md
  grep -q '^ctx=' $d/spark.pins || echo 'ctx=65536' >> $d/spark.pins
  grep -q '^started_ok=' $d/spark.pins || printf '# the ticket is In Progress (Linear) only because its PR is merged and a follow-up remains; the carve-out is recorded in round.json, written by Spark operator 14, Wednesday to confirm before queueing\nstarted_ok=%s\n' "$(echo "$so" | tr ' ' '_')" >> $d/spark.pins
done
