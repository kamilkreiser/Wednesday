#!/bin/bash
W=/private/tmp/claude-501/qla2; H=039b9875b69918c2a83e95d84f7f8169358b59d5; M=ce7276c86aaaa222c1622620a2e8b4734fb3a187; O=02bea3d0a7eae277b67a0e488d4567bff49839af
G() { git -C $W/clone "$@"; }
FORB="crates/coagent-policy crates/coagent-hook crates/coagent-mcp crates/coagent-cli crates/coagent-daemon/src/gate.rs preview spikes Cargo.toml Cargo.lock docs/POLICY.md .gitattributes crates/coagent-daemon/tests/common crates/coagent-daemon/tests/p1p_support"
echo "forbidden vs main (M..H): $(G diff $M $H -- $FORB | wc -c) bytes"
echo "forbidden 3-dot M...H: $(G diff $M...$H -- $FORB | wc -c) bytes"
echo "forbidden O..H minus other-lane paths: $(G diff $O $H -- crates/coagent-policy crates/coagent-hook crates/coagent-mcp crates/coagent-cli crates/coagent-daemon/src/gate.rs Cargo.toml Cargo.lock docs/POLICY.md .gitattributes crates/coagent-daemon/tests/common crates/coagent-daemon/tests/p1p_support | wc -c) bytes"
echo "control (docs/DAEMON.md M..H): $(G diff $M $H -- docs/DAEMON.md | wc -c) bytes"
echo "Cargo manifests/lock vs main: [$(G diff --name-only $M $H -- '*Cargo.toml' '*Cargo.lock')]"
echo "engine.rs O..H: $(G diff $O $H -- crates/coagent-daemon/src/engine.rs crates/coagent-daemon/src/ipc.rs crates/coagent-daemon/src/lib.rs crates/coagent-daemon/src/main.rs | wc -c) bytes"
echo "unsafe in added lines: $(G diff $M $H -- crates | grep '^+' | grep -c unsafe)"
G ls-tree -r $M | grep '/tests/' > $W/tests_main.txt; G ls-tree -r $H | grep '/tests/' | grep -v 'tests/la_' > $W/tests_head.txt
echo "tests at main: $(wc -l < $W/tests_main.txt); head minus la_: $(wc -l < $W/tests_head.txt); identical: $(cmp -s $W/tests_main.txt $W/tests_head.txt && echo yes || echo NO)"
echo "scripts changed vs main: [$(G diff --name-only $M $H -- scripts)] removed lines in red script: $(G diff $M $H -- scripts/red-controls-daemon.sh | grep -c '^-[^-]')"
echo "red script O..H removed lines: $(G diff $O $H -- scripts/red-controls-daemon.sh | grep -c '^-[^-]')"
echo "other lane folders vs main: $(G diff $M $H -- spikes/W1-windows-exec-hook spikes/W4-windows-paths preview/plugin-template-windows | wc -c) bytes; files at main: $(G ls-tree -r --name-only $M -- spikes/W1-windows-exec-hook spikes/W4-windows-paths preview/plugin-template-windows | wc -l)"
echo "whole tree diff vs main paths: $(G diff --name-only $M $H | wc -l)"
echo "conflict markers at head (whole tree, lines starting <<<<<<< / >>>>>>> ):"; G grep -n -E '^(<<<<<<<|>>>>>>>)' $H | head; echo "  (and ======= exactly, in lane files):"; G grep -n -E '^=======$' $H -- BACKLOG.md docs crates/coagent-daemon scripts | head
echo "control: grep finds a planted marker in a temp blob:"; printf 'a\n<<<<<<< HEAD\n' | grep -c -E '^(<<<<<<<|>>>>>>>)'
