#!/bin/bash
# QA-POLICY-AT: the by-hand plants, one after the other; each own tree under qpa/pl/, own EMPTY target, own test tmp.
W=/private/tmp/claude-501/qpa; . $W/h/envx.sh
run() { n=$1; shift
  export CARGO_TARGET_DIR=$W/tt_pl/$n/target COAGENT_TEST_TMP=$W/tt_pl/$n/testtmp; mkdir -p $COAGENT_TEST_TMP
  s=$(date +%s); python3 -B $W/h/inroot.py $W/pl/$n cargo test -p coagent-policy --locked --offline "$@" > $W/dout/plant_$n.log 2>&1; rc=$?
  echo "== $n ($*): rc $rc $(( $(date +%s)-s ))s heavy-at-end $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh) compiled $(grep -c Compiling $W/dout/plant_$n.log) crate $(grep -c 'Compiling coagent-policy' $W/dout/plant_$n.log)"
  grep -E 'test result' $W/dout/plant_$n.log | tail -1
  grep -A3 'panicked at' $W/dout/plant_$n.log | grep -v '^--$' | grep -v 'panicked at' | grep -v RUST_BACKTRACE | head -3 | cut -c1-420
}
run h1_docs --test t25_owner_allow docs_name_the_owner_origin
run h2_guard --test t25_owner_allow fixture_facts_residuals_are_known
run h6_t27base --test t27_owner_dark
run h7_quote --test t28_at_names at_spellings_property
run h8_words --test t28_at_names at_non_file_shapes_property
run p4s_base --test t26_owner_property
run p4s_head --test t26_owner_property
run p4c_head --test t26_owner_property
run pT26a --test t26_owner_property
run pT26b --test t26_owner_property
