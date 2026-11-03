#!/bin/bash
# Q3 two-commit shape check
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976/repo
g() { git -C "$R" "$@"; }
echo "== commit1 parent:"; g rev-parse bdc1d4d8^
echo "== commit2 parent:"; g rev-parse dba3a90a^
echo "== commit1 stat (base..c1)"; g diff --stat 4d1ab2cb6574 bdc1d4d8
echo "== commit2 stat (HEAD~1..HEAD)"; g diff --stat dba3a90a~1 dba3a90a
echo "== commit2 numstat"; g diff --numstat dba3a90a~1 dba3a90a
echo "== commit2 diff"; g diff dba3a90a~1 dba3a90a
echo "== squash check: tree of base+squash vs head tree"
H=$(g rev-parse 'dba3a90a^{tree}')
S=$(g commit-tree "$H" -p 4d1ab2cb6574 -m squash)
echo "head tree $H ; squash commit $S tree $(g rev-parse "$S^{tree}")"
echo "== base..head stat (squash)"; g diff --stat 4d1ab2cb6574 dba3a90a
echo "== paths c1 vs squash"; diff <(g diff --name-only 4d1ab2cb6574 bdc1d4d8) <(g diff --name-only 4d1ab2cb6574 dba3a90a) && echo SAME_PATHS
echo "== commit messages"; g log --format='--- %H%n%an <%ae>%n%B' 4d1ab2cb6574..dba3a90a
