source /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5/env.sh
S=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5
export COAGENT_TOOLS=$S/tools
( builtin pushd $C >/dev/null && bash scripts/red-controls-audit.sh ) > $S/red_audit.log 2>&1; echo "red_audit_rc=$?" >> $S/red_audit.log
( builtin pushd $C >/dev/null && bash scripts/red-controls-core.sh ) > $S/red_core.log 2>&1; echo "red_core_rc=$?" >> $S/red_core.log
