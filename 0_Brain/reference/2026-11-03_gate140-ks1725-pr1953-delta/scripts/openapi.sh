#!/bin/bash
# (E) Rule 4: check:openapi rc 0 at the head; the yaml equals a fresh regeneration (byte-identical after a real
# write); a planted one-word drift gives rc 1; restored by bytes (backup in the session scratchpad), sha256 asserted, tree clean, check rc 0 again.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta; R=$G/repo; D=$R/Blockchain/Dev; L=$G/logs
BK=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9ee83091-a095-4b37-9c10-a5738ac0ba5f/scratchpad/g140_yaml_orig_bytes
Y=$D/docs/openapi/secuura-api.yaml; [ -f "$Y" ] || { echo "yaml not at $Y"; exit 2; }
S0=$(shasum -a 256 "$Y" | cut -d' ' -f1); echo "yaml sha256 at head: $S0  (git blob $(git -C $R rev-parse 928ee20c84dc:Blockchain/Dev/docs/openapi/secuura-api.yaml))"
npm --prefix $D run check:openapi > $L/openapi_check_head.log 2>&1; echo "check:openapi rc=$?  $(grep -E 'CHECK (PASS|FAIL)' $L/openapi_check_head.log | head -1)"
npm --prefix $D run generate-openapi > $L/openapi_regen.log 2>&1; echo "generate-openapi (write) rc=$?  $(grep 'wrote' $L/openapi_regen.log)"
S1=$(shasum -a 256 "$Y" | cut -d' ' -f1); [ "$S0" = "$S1" ] && echo "fresh regeneration BYTE-IDENTICAL ($S1)" || echo "fresh regeneration DIFFERS ($S1)"
echo "git status after regen: [$(git -C $R status --porcelain)]"
cp "$Y" $BK
TL=$(grep -n -m1 '^  title:' "$Y"); echo "plant in: $TL"
LN=${TL%%:*}; sed -i '' "${LN}s/title: \(.*\)/title: \1 Drift/" "$Y"; echo "planted line: $(sed -n "${LN}p" "$Y")"
npm --prefix $D run generate-openapi -- --check > $L/openapi_check_planted.log 2>&1; echo "planted --check rc=$?  $(grep -E 'CHECK (PASS|FAIL)' $L/openapi_check_planted.log | head -1)"
npm --prefix $D run check:openapi > $L/openapi_check_planted_full.log 2>&1; echo "planted check:openapi rc=$?"
cp $BK "$Y"
S2=$(shasum -a 256 "$Y" | cut -d' ' -f1); [ "$S0" = "$S2" ] && echo "RESTORE sha256 equal" || echo "RESTORE FAILED"
echo "git status after restore: [$(git -C $R status --porcelain)]"
npm --prefix $D run check:openapi > $L/openapi_check_restored.log 2>&1; echo "restored check:openapi rc=$?"
