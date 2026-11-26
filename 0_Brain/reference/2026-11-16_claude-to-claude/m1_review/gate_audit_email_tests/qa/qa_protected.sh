#!/bin/bash
# usage: qa_protected.sh <repo> <brief>  : sha256 of each protected file at base and head vs the lane brief's value
R="$1"; BR="$2"; ok=0; bad=0
while read -r name val; do
  for s in 5e11609 e31b29a; do
    if out=$(git --no-optional-locks -C "$R" show "${s}:crates/coagent-audit/tests/$name" 2>/dev/null | shasum -a 256 ; exit ${PIPESTATUS[0]}); then h=${out%% *}; else h="NOT-FOUND"; fi
    [ "$h" = "$val" ] && ok=$((ok+1)) || { bad=$((bad+1)); echo "MISMATCH $s $name $h want $val"; }
  done
  echo "$name base/head = $val"
done < <(grep -E '^- `[^`]+` [0-9a-f]{64}' "$BR" | sed -E 's/^- `([^`]+)` ([0-9a-f]{64}).*/\1 \2/')
echo "ok=$ok bad=$bad"
# control: a path git show cannot find must be reported, not hashed as empty
for s in 5e11609; do if out=$(git --no-optional-locks -C "$R" show "${s}:crates/coagent-audit/tests/ae_email.rs" 2>/dev/null | shasum -a 256 ; exit ${PIPESTATUS[0]}); then echo "CONTROL hashed: ${out%% *}"; else echo "CONTROL: ae_email.rs at base reported NOT-FOUND"; fi; done
