#!/bin/bash
C=/private/tmp/claude-501/qan2/c
G() { git -C "$C" "$@"; }
echo "a1 product paths wc -c d79ae1c..73ce645: $(G diff d79ae1c 73ce645 -- crates/coagent-daemon/src crates/coagent-daemon/build.rs scripts crates/coagent-audit crates/coagent-audit-host | wc -c)"
echo "a1 control 5e11609..d79ae1c: $(G diff 5e11609 d79ae1c -- crates/coagent-daemon/src crates/coagent-daemon/build.rs scripts crates/coagent-audit crates/coagent-audit-host | wc -c)"
echo "a2 name-only d79ae1c..73ce645:"; G diff --name-only d79ae1c 73ce645
echo "a2 control count 5e11609..d79ae1c: $(G diff --name-only 5e11609 d79ae1c | wc -l)"
echo "numstat d79ae1c..73ce645:"; G diff --numstat d79ae1c 73ce645
echo "numstat 5e11609..73ce645:"; G diff --numstat 5e11609 73ce645 -- BACKLOG.md crates/coagent-daemon/tests/aw_disk.rs docs/M0-OUTCOMES.md
echo "trees audit-host/audit at d79ae1c / head:"
for t in crates/coagent-audit-host crates/coagent-audit; do echo "$(G rev-parse d79ae1c:$t) $(G rev-parse 73ce645:$t) $t"; done
D=crates/coagent-daemon
echo "a3 blobs (d79ae1c, head, sha256-16 at head):"
for p in $D/tests/gate/gate_attacks.rs $D/tests/gate/gr2.rs $D/tests/gate/gr3.rs $D/tests/gate/gr4.rs $D/tests/gate/gate_hostile/mod.rs $D/tests/gate_r2.rs $D/tests/gate_r3.rs $D/tests/gate_r4.rs $D/tests/gate_r5_model.rs $D/tests/gate_r6_model.rs $D/tests/gate_r6_model_wrapper.rs $D/tests/gate_return.rs $D/tests/common/mod.rs $D/tests/release_audit.rs $D/tests/ipc.rs $D/tests/dn_help.rs $D/src/audit.rs $D/tests/aw_disk.rs; do
 a=$(G rev-parse --verify -q "d79ae1c:$p") || a=MISSING; b=$(G rev-parse --verify -q "73ce645:$p") || b=MISSING
 h=$(G show "73ce645:$p" | shasum -a 256 | cut -c1-16)
 [ "$a" = "$b" ] && e=EQUAL || e=DIFFER; echo "$e ${a:0:7} ${b:0:7} $h $p"; done
echo "control missing path: $(G rev-parse --verify -q d79ae1c:$D/tests/no_such.rs || echo MISSING-reported)"
