#!/bin/bash
# usage: list_tests.sh <tree> <target dir> <out>   (test names per binary, `cargo test -- --list`)
W=/private/tmp/claude-501/qpb; . $W/h/envx.sh; export CARGO_TARGET_DIR=$2 COAGENT_TEST_TMP=$W/tt_list/testtmp
python3 -B $W/h/inroot.py $W/$1 cargo test -p coagent-policy --locked --offline -- --list 2>&1 | awk '/Running/ {split($2,a,"/"); b=a[length(a)]; sub(/-[0-9a-f]+$/,"",b); if ($0 ~ /unittests/) b="lib"} /: test$/ {print b"::"$1}' | sed 's/:$//' | sort > $3
wc -l < $3
