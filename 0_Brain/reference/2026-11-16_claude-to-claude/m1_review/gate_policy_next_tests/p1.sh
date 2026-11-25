#!/bin/bash
# QA-POLICY-NEXT item 1: head, base, zero bytes of source diff
G() { git -C /private/tmp/claude-501/qpx/clone "$@"; }
B=7fc61882b6eed3245428d0e120714bd3b06e0c18; H=7677162edf6a2fac91156da3e54309f0bfdf5fd9; M=74dc861634cb020855e7e79d79a901fde819e611
L=/private/tmp/claude-501/qpx/logs
echo "cat-file: $(G cat-file -t $H)"; G log --format='%H %P | %s' $B..$H; G merge-base --is-ancestor $B $H && echo "base is ancestor of head"
echo "merges in range: $(G rev-list --count --merges $B..$H); commits: $(G rev-list --count $B..$H)"
echo "--- R-6 (1)"
echo "base..head src/Cargo/red bytes: $(G diff $B $H -- crates/coagent-policy/src crates/coagent-policy/Cargo.toml crates/coagent-policy/red-controls.sh | wc -c)"
echo "base..74dc861 same paths: $(G diff $B $M -- crates/coagent-policy/src crates/coagent-policy/Cargo.toml crates/coagent-policy/red-controls.sh | wc -c)"
echo "control b6af26c^..b6af26c same paths: $(G diff b6af26c^ b6af26c -- crates/coagent-policy/src crates/coagent-policy/Cargo.toml crates/coagent-policy/red-controls.sh | wc -c)"
echo "b6af26c..base crate+POLICY.md: $(G diff b6af26c $B -- crates/coagent-policy docs/POLICY.md | wc -c)"
echo "--- R-6 (2)"
for p in crates/coagent-policy/src crates/coagent-policy/Cargo.toml crates/coagent-policy/red-controls.sh; do echo "$p base $(G rev-parse "$B:$p") head $(G rev-parse "$H:$p")"; done
G ls-tree -r $B -- crates/coagent-policy/src > $L/src_base.txt; G ls-tree -r $H -- crates/coagent-policy/src > $L/src_head.txt
echo "src files base $(wc -l < $L/src_base.txt) head $(wc -l < $L/src_head.txt)"
python3 -B - $L/src_base.txt $L/src_head.txt <<'PY'
import sys
def rd(p): return {l.split('\t')[1].strip(): l.split()[2] for l in open(p)}
a,b=rd(sys.argv[1]),rd(sys.argv[2])
diff=[k for k in set(a)|set(b) if a.get(k)!=b.get(k)]
print("by program: paths base",len(a),"head",len(b),"differing blob ids",len(diff))
PY
echo "control (b6af26c^ vs b6af26c src blobs differing lines): $(diff <(G ls-tree -r b6af26c^ -- crates/coagent-policy/src) <(G ls-tree -r b6af26c -- crates/coagent-policy/src) | grep -c '^[<>]')"
echo "--- numstat base..head"; G diff --numstat $B $H; G diff --shortstat $B $H
echo "--- name-only base...head"; G diff --name-only $B...$H
echo "--- fix commit"; G diff --numstat $M $H; G diff --stat $M $H | tail -1
echo "--- unsafe in added lines: $(G diff -U0 $B $H | grep '^+' | grep -c unsafe)"
echo "forbid at head lib.rs:17: $(G show "$H:crates/coagent-policy/src/lib.rs" | sed -n 17p)"
echo "red rows base $(G show "$B:crates/coagent-policy/red-controls.sh" | grep -c '"red_') head $(G show "$H:crates/coagent-policy/red-controls.sh" | grep -c '"red_')"
echo "POLICY.md lines base $(G show "$B:docs/POLICY.md" | wc -l) head $(G show "$H:docs/POLICY.md" | wc -l)"
