Template for tier test_only_input. Replace Tip/File/Test file paths, the plant line/from/to (from: must equal the tip line
exactly, indentation included), the red-cell names, and write golden.diff (the cells, test files only). For a test-side plant
(a fixture/JSON the cells read) delete the `## Plant` block and add golden_red.diff instead - exactly one of the two.
Prove it with: round.sh <dir> --control   (golden in place of a model answer; no endpoint).
