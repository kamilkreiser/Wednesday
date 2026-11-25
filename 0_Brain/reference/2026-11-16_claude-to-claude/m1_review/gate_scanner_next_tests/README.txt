QA-SCANNER-NEXT (independent check of scanner-next, head dd70630, base debbb44). Copies of every test and tool written by the check.
To re-run: clone the project at dd70630; run qa_tools/mkqa.sh <clone> and qa_tools/mkloose.sh <clone>; copy the earlier checks'
gate_scanner_core_tests/qa/gen.rs to <crate>/tests/qa/gen.rs and gate_scanner_core_r2_tests/qa_r2_gen.rs to <crate>/tests/;
python3 -B -I qa_tools/mkdocs.py <clone> <crate>/tests/qa_sx_data.rs <gate_scanner_notes_tests/tests/qa_n_cases.rs>;
copy t07_pure.rs at each SHA to <crate>/tests/qa_t07_{base,head}.rs with `fn hits(` -> `pub fn hits(` and the test renamed
(see the verdict, section 4); copy tests/*.rs here into <crate>/tests/; then
  cargo test --locked --release -p coagent-scanner --test qa_sx_diff -- --nocapture
  cargo test --locked -p coagent-scanner --test qa_sx_pins -- --nocapture
  cargo test --locked -p coagent-scanner --test qa_sx_t07 -- --nocapture   (t07_hostile takes ~45 s in debug: the quadratic rows)
Plants: qa_tools/plant.py on a copy of src/, then COAGENT_SCANNER_SRC_DIR=<copy> cargo test --test t07_pure (own target dir each).
rustc_ws/: the gap spellings compiled with `rustc --edition 2021 --crate-type lib --emit=metadata` (logs beside them).
The name scan's planted controls and their log are NOT copied (they hold the planted words). Every value is made up.
