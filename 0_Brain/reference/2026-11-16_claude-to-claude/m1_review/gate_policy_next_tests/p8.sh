#!/bin/bash
# QA-POLICY-NEXT items 1 and 8: scope, protected files, dark, cargo tree (git read verbs in my clone; cargo tree offline)
G() { git -C /private/tmp/claude-501/qpx/clone "$@"; }
W=/private/tmp/claude-501/qpx
B=7fc61882b6eed3245428d0e120714bd3b06e0c18; H=7677162edf6a2fac91156da3e54309f0bfdf5fd9
OWN=(BACKLOG.md docs/M0-OUTCOMES.md docs/POLICY.md crates/coagent-policy/tests/owner_common/mod.rs crates/coagent-policy/tests/t25_owner_allow.rs crates/coagent-policy/tests/t26_owner_property.rs crates/coagent-policy/tests/t27_owner_dark.rs)
EX=(); for p in "${OWN[@]}"; do EX+=(":!$p"); done
echo "every path but the 7 owned, bytes: $(G diff $B $H -- . "${EX[@]}" | wc -c)"
EX2=(); for p in "${OWN[@]:1}"; do EX2+=(":!$p"); done
echo "control (BACKLOG.md let back in): $(G diff $B $H -- . "${EX2[@]}" | wc -c)"
for p in Cargo.lock Cargo.toml rust-toolchain.toml .gitattributes scripts preview spikes crates/coagent-daemon crates/coagent-mcp crates/coagent-hook crates/coagent-scanner; do echo "  $p: $(G diff $B $H -- $p | wc -c) bytes"; done
echo "Cargo.lock blob base $(G rev-parse $B:Cargo.lock) head $(G rev-parse $H:Cargo.lock)"
echo "--- tests/ ls-tree"
G ls-tree -r $B -- crates/coagent-policy/tests/ > $W/logs/tests_base.txt; G ls-tree -r $H -- crates/coagent-policy/tests/ > $W/logs/tests_head.txt
echo "entries base $(wc -l < $W/logs/tests_base.txt) head $(wc -l < $W/logs/tests_head.txt)"
python3 -B -I - $W/logs/tests_base.txt $W/logs/tests_head.txt <<'PY'
import sys
def rd(p): return {l.split('\t')[1].strip(): l.split()[2] for l in open(p)}
a,b=rd(sys.argv[1]),rd(sys.argv[2])
print("paths only at one side:", sorted(set(a)^set(b)))
print("blob ids differing:", sorted(k for k in a if k in b and a[k]!=b[k]))
PY
echo "--- sha256 of protected files (git show) base / head"
for f in q01_gate_attacks.rs r2_gate_attacks.rs r3_gate_attacks.rs r4_gate_attacks.rs r5b_bound_probe.rs r5b_r4_regressions.rs r5b_shell_t3.rs qa_strict.rs qa_strict_m2/qa_strict.rs qa_strict_m2/common/mod.rs common/mod.rs bypass_common/mod.rs t21_bypass_refusals.rs t12_docs.rs; do
  p=crates/coagent-policy/tests/$f; a=$(G show "${B}:${p}" | shasum -a 256 | cut -c1-64); b=$(G show "${H}:${p}" | shasum -a 256 | cut -c1-64)
  echo "  $f ${a:0:8}…${a:56:8} $( [ "$a" = "$b" ] && echo SAME || echo DIFFERENT)"
done
echo "  control engine.rs b6af26c^ vs b6af26c: $(G show b6af26c^:crates/coagent-policy/src/engine.rs | shasum -a 256 | cut -c1-8) vs $(G show b6af26c:crates/coagent-policy/src/engine.rs | shasum -a 256 | cut -c1-8)"
echo "  empty-input hash (guard against an empty read): $(printf '' | shasum -a 256 | cut -c1-8)"
echo "--- appended files"
nb=$(G show $B:BACKLOG.md | wc -l | tr -d ' '); nm=$(G show $B:docs/M0-OUTCOMES.md | wc -l | tr -d ' ')
echo "BACKLOG lines base $nb head $(G show $H:BACKLOG.md | wc -l | tr -d ' '); first $nb lines equal: $( [ "$(G show $B:BACKLOG.md | shasum -a 256)" = "$(G show $H:BACKLOG.md | head -n $nb | shasum -a 256)" ] && echo YES || echo NO)"
echo "M0 lines base $nm head $(G show $H:docs/M0-OUTCOMES.md | wc -l | tr -d ' '); first $nm lines equal: $( [ "$(G show $B:docs/M0-OUTCOMES.md | shasum -a 256)" = "$(G show $H:docs/M0-OUTCOMES.md | head -n $nm | shasum -a 256)" ] && echo YES || echo NO)"
echo "control: BACKLOG first $nb lines vs base with last line dropped: $( [ "$(G show $B:BACKLOG.md | head -n $((nb-1)) | shasum -a 256)" = "$(G show $H:BACKLOG.md | head -n $nb | shasum -a 256)" ] && echo EQUAL || echo DIFFERENT)"
echo "--- dark"
RX='OwnerAllow|decide_with_owner_allow|TerminalCommands|BypassView|decide_with_mode|OwnerInputFacts|owner_input_facts|owner_mode|ModeOrigin|owner_program_word'
for s in $B $H; do echo "  ${s:0:7}: outside hits $(G grep -c -E "$RX" $s -- crates preview spikes scripts ':!crates/coagent-policy' | wc -l | tr -d ' ') files; control src: $(G grep -c -E "$RX" $s -- crates/coagent-policy/src | sed "s/^$s://" | tr '\n' ' ')"; done
echo "--- unsafe in policy src at head (lines naming unsafe): $(G grep -n unsafe $H -- crates/coagent-policy/src | sed "s/^$H://")"
