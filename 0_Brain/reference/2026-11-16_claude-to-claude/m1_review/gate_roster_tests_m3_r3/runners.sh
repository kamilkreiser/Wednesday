#!/bin/bash
# QA gate M3-ROSTER r3: the scripts this run used (scratch paths; re-create the scratch dir to re-run).

### ---- env.sh ----
export CARGO_HOME=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/mc_relayid/ch
export RUSTUP_HOME="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools/rustup"
export CARGO_TARGET_DIR=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/target
export COAGENT_TOOLS=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/tools
export PATH="/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/mc_relayid/ch/bin:$PATH"

### ---- run_check.sh ----
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/env.sh
cargo fetch --locked --manifest-path /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/clone/Cargo.toml > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/fetch.log 2>&1; echo "fetch_rc=$?" >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/fetch.log
bash /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/clone/scripts/check.sh > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/check.log 2>&1; echo "check_rc=$?" >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/check.log
bash /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/clone/scripts/red-controls-roster.sh > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/red.log 2>&1; echo "red_rc=$?" >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/red.log

### ---- qa_r3_run.sh ----
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/env.sh
export CARGO_TARGET_DIR=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/target_mut
cargo test --locked --manifest-path /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/mut/Cargo.toml -p coagent-roster --test qa_r3 -- --nocapture "$@"

### ---- qa_r3_green.sh ----
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/env.sh
for k in 1 2 3; do cargo test --locked --manifest-path /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/clone/Cargo.toml -p coagent-roster --test qa_r3 -- --nocapture 2>&1 | grep -E "R3 A6|test result|FAILED"; done

### ---- mut_run.sh ----
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/env.sh
python3 -I /Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_roster_tests_m3_r3/mutate_r3.py /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/mut /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/target_mut /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/mutation_results.tsv
echo mut_rc=$?

### ---- mut_own.sh ----
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/env.sh
OWN=1 python3 -I /Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_roster_tests_m3_r3/mutate_r3.py /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/mut /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/target_mut /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/mutation_results_own.tsv
echo own_rc=$?

### ---- merge_run.sh ----
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/env.sh
export CARGO_TARGET_DIR=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/target_merge
M=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge
G="git -C $M -c user.name=qa-gate -c user.email=qa@invalid"
$G checkout -q -b mm real/main
$G merge -q --no-edit m3-roster > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge_main.log 2>&1; echo "merge_main_rc=$?" >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge_main.log
git -C $M status --short >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge_main.log
cargo check --locked --workspace --all-targets --manifest-path $M/Cargo.toml > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/mm_check.log 2>&1; echo "check_rc=$?" >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/mm_check.log
cargo test --locked --workspace --manifest-path $M/Cargo.toml --exclude coagent-daemon > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/mm_test.log 2>&1; echo "test_rc=$?" >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/mm_test.log
$G checkout -q -b ma mm
$G merge -q --no-edit real/m3-audit > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge_audit.log 2>&1; echo "merge_audit_rc=$?" >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge_audit.log
git -C $M status --short >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge_audit.log
git -C $M diff --name-only --diff-filter=U >> /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge_audit.log

### ---- merge_audit.sh ----
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/env.sh
export CARGO_TARGET_DIR=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/target_merge
M=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge
G="git -C $M -c user.name=qa-gate -c user.email=qa@invalid"
resolve() { python3 -I -c "
import re,sys;p=sys.argv[1];s=open(p).read()
s=re.sub(r'^(<<<<<<< .*|=======|>>>>>>> .*)\n','',s,flags=re.M);open(p,'w').write(s)" "$M/BACKLOG.md"; $G add BACKLOG.md; }
resolve; $G commit -q --no-edit; echo "mm_commit=$(git -C $M rev-parse --short HEAD)"
$G merge -q --no-edit real/m3-audit > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge_audit2.log 2>&1; echo "merge_audit_rc=$?"
git -C $M diff --name-only --diff-filter=U
if git -C $M diff --name-only --diff-filter=U | grep -qx BACKLOG.md; then resolve; $G commit -q --no-edit; fi
git -C $M diff --name-only --diff-filter=U | grep . && echo "OTHER CONFLICTS" 
echo "ma_head=$(git -C $M rev-parse --short HEAD)"
cargo check --locked --workspace --all-targets --manifest-path $M/Cargo.toml > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/ma_check.log 2>&1; echo "ma_check_rc=$?"
cargo test --locked --manifest-path $M/Cargo.toml -p coagent-roster -p coagent-audit --no-fail-fast > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/ma_test.log 2>&1; echo "ma_test_rc=$?"
grep "test result" /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/ma_test.log | awk '{s+=$4; f+=$6} END {print "passed",s,"failed",f}'
grep "FAILED\|panicked" /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/ma_test.log | head

### ---- merge_daemon.sh ----
. /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/env.sh
export CARGO_TARGET_DIR=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/target_merge
M=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge
G="git -C $M -c user.name=qa-gate -c user.email=qa@invalid"
$G checkout -q -b md 56319d9
$G merge -q --no-edit real/m1-daemon > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/merge_daemon.log 2>&1; echo "merge_daemon_rc=$?"
git -C $M diff --name-only --diff-filter=U
if git -C $M diff --name-only --diff-filter=U | grep -qx BACKLOG.md; then python3 -I -c "
import re,sys;p=sys.argv[1];s=open(p).read()
s=re.sub(r'^(<<<<<<< .*|=======|>>>>>>> .*)\n','',s,flags=re.M);open(p,'w').write(s)" "$M/BACKLOG.md"; $G add BACKLOG.md; $G commit -q --no-edit; fi
git -C $M diff --name-only --diff-filter=U | grep . && echo "OTHER CONFLICTS"
echo "md_head=$(git -C $M rev-parse --short HEAD)"
cargo check --locked --workspace --all-targets --manifest-path $M/Cargo.toml > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/md_check.log 2>&1; echo "md_check_rc=$?"
cargo test --locked --manifest-path $M/Cargo.toml -p coagent-roster -p coagent-daemon --lib --no-fail-fast > /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/md_test.log 2>&1; echo "md_test_rc=$?"
grep "test result" /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_roster_r3/md_test.log | awk '{s+=$4; f+=$6} END {print "passed",s,"failed",f}'
