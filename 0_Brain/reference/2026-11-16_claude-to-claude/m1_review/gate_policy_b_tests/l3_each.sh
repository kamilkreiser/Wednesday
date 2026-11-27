#!/bin/bash
# QA-POLICY-B item 7: mutant L3/M11 (MAX_FREE_WORK = u64::MAX): each t29 test alone, 600 s timeout each.
W=/private/tmp/claude-501/qpb; . $W/h/envx.sh
export CARGO_TARGET_DIR=$W/tt_pl_L3/debug COAGENT_TEST_TMP=$W/tt_pl_L3/testtmp RED_CONTROLS_LOG=$W/tt_pl_L3/red-normal.log
for t in whole_visible_part_is_checked free_text_window_property scan_b_never_drops_a_word web_fetch_prompt_is_checked json_escaped_names_are_checked scan_b_cost_is_bounded ordinary_text_is_admitted_checked_and_fast a_million_words_answer_as_their_window; do
  s=$(date +%s); out=$(timeout 600 python3 -B $W/h/inroot.py $W/pl_L3 cargo test -p coagent-policy --locked --offline --test t29_free_text -- --exact $t 2>&1); rc=$?
  echo "== $t rc $rc $(( $(date +%s) - s ))s $(echo "$out" | grep -E '^test result' | head -1)"; echo "$out" | grep -A1 "panicked at" | head -2 | cut -c1-260
done
python3 -B $W/h/inroot.py $W/pl_L3 cargo test -p coagent-policy --locked --offline --test t29_free_text -- --list 2>/dev/null | grep ": test"
