source /private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5/env.sh
S=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5
( builtin pushd $C >/dev/null && bash scripts/check.sh ) > $S/check.log 2>&1; echo "check_rc=$?" >> $S/check.log
