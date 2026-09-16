#!/bin/bash
# Controls for launch_qa_secuura_ks1123_1002.sh. EVERY launcher invocation below passes --check; nothing here runs the
# launch path (the TTY guard, exit 21, is deliberately NOT exercised — a known gap, not this drafter's to test).
# Negative prompts/copies are written into a fresh mktemp -d under the session scratchpad; nothing is removed.
set -u
Q=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent
G="$Q/gatesets/2026-09-16_gate1002"
L="$Q/launchers/launch_qa_secuura_ks1123_1002.sh"
P="$Q/briefs/2026-09-16_secuura-1002-ks1123-tier2.prompt.txt"
T="$(mktemp -d /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad/ctl1002.XXXXXX)"
echo "controls at $(date '+%Y-%m-%d %H:%M:%S %Z') scratch ${T:?unset}"

# 0. residual-guard positive control: the guard tokens DO occur in the template (so a clean output is not vacuous)
python3 - "$Q/launchers/launch_qa_secuura_ks1130_999_ks960_1000.sh" <<'PYC'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read().replace("launch_qa_secuura_ks1130_999_ks960_1000.sh", "")
toks = ["91793e5d4", "ab4a35d75", "0b25f823f", "HEAD_1000", "BRANCH_1000", "QA999", "QA1000", "QA9991000", "1130", "twin",
        "createuser", "conflict-target", "PR_N", "PR_HEAD", "pair", "both head", "one read per PR", "999", "1000", "960"]
n = {t: len(re.findall(re.escape(t), s)) for t in toks}
print("residual-guard positive control on the TEMPLATE: total hits", sum(n.values()), "tokens with >=1 hit", sum(1 for v in n.values() if v))
PYC

run() { # $1 label, $2 expected rc, rest = env assignments; always --check
  local label="$1" want="$2"; shift 2
  out="$(env "$@" "$L" --check 2>&1)"; rc=$?
  printf '%s\n' "$out" | tail -3 | sed 's/^/    /'
  echo "$label rc=$rc expect $want $([ "$rc" = "$want" ] && echo PASS || echo FAIL)"
}

# 1. wrong head override -> exit 6
run "neg1 (QA1002_HEAD wrong)" 6 QA1002_HEAD=0000000000000000000000000000000000000000
# 2. prompt without the full head SHA -> exit 20
sed 's/a376756aba1e1ae32c49ed47ba057fd80c7ed136/a376756ab/g' "$P" > "$T/neg_prompt_nosha.txt"
run "neg2 (prompt lacks full head SHA)" 20 QA1002_PROMPT="$T/neg_prompt_nosha.txt"
# 3. prompt without the verdict destination -> exit 12
sed 's/wednesday-agent@agentmail.to/someone@example.invalid/g' "$P" > "$T/neg_prompt_nomaildest.txt"
run "neg3 (prompt lacks verdict destination)" 12 QA1002_PROMPT="$T/neg_prompt_nomaildest.txt"
# 4. the exemplar #999/#1000 prompt -> exit 9 (does not name this brief)
run "neg4 (exemplar prompt)" 9 QA1002_PROMPT="$Q/briefs/2026-09-16_secuura-999-1000-ks1130-ks960-tier2.prompt.txt"
# 5. develop arm, GUARDED path: a launcher COPY pinned to develop 0b25f823f, whose move to now includes #999 (verification.ts) -> exit 18
sed "s/^DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'/DEVELOP_SHA='0b25f823f6660ac52b665f14055799ff0c3b616d'/" "$L" > "$T/copy_dev_0b25.sh"
echo "copy5 DEVELOP_SHA lines: $(/usr/bin/grep -c "^DEVELOP_SHA='0b25f823f6660ac52b665f14055799ff0c3b616d'" "$T/copy_dev_0b25.sh")"
out="$(bash "$T/copy_dev_0b25.sh" --check 2>&1)"; rc=$?; printf '%s\n' "$out" | tail -2 | cut -c1-400 | sed 's/^/    /'
echo "neg5 (develop moved across verification.ts) rc=$rc expect 18 $([ "$rc" = 18 ] && echo PASS || echo FAIL)"
# 6. develop arm, disjoint move: a COPY pinned to the base 80686962, whose move to now is #1001 only -> rc 0 with a MOVED note
sed "s/^DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'/DEVELOP_SHA='80686962828197acf305e4010a2ed5b401285743'/" "$L" > "$T/copy_dev_base.sh"
echo "copy6 DEVELOP_SHA lines: $(/usr/bin/grep -c "^DEVELOP_SHA='80686962828197acf305e4010a2ed5b401285743'" "$T/copy_dev_base.sh")"
out="$(bash "$T/copy_dev_base.sh" --check 2>&1)"; rc=$?; printf '%s\n' "$out" | /usr/bin/grep -i 'MOVED' | cut -c1-400 | sed 's/^/    /'
echo "pos6 (develop moved, disjoint) rc=$rc expect 0 $([ "$rc" = 0 ] && echo PASS || echo FAIL)"
echo "done $(date '+%H:%M:%S %Z')"
