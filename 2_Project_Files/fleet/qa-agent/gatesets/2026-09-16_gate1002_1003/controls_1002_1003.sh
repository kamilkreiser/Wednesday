#!/bin/bash
# Controls for launch_qa_secuura_ks1123_1002_ks1165_1003.sh. EVERY launcher invocation below passes --check; nothing
# here runs the launch path (the TTY guard, exit 21, is deliberately NOT exercised — a known gap, not this drafter's).
# Negative prompts and launcher COPIES are written into a fresh mktemp -d under the session scratchpad; nothing removed.
set -u
Q=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent
G="$Q/gatesets/2026-09-16_gate1002_1003"
L="$Q/launchers/launch_qa_secuura_ks1123_1002_ks1165_1003.sh"
P="$Q/briefs/2026-09-16_secuura-1002-1003-ks1123-ks1165-tier2.prompt.txt"
T="$(mktemp -d /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9aed5a67-2729-4892-b685-13ab87142a58/scratchpad/ctl10021003.XXXXXX)"
echo "controls at $(date '+%Y-%m-%d %H:%M:%S %Z') scratch ${T:?unset}"

python3 - "$Q/launchers/launch_qa_secuura_ks1130_999_ks960_1000.sh" <<'PYC'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read().replace("launch_qa_secuura_ks1130_999_ks960_1000.sh", "")
toks = ["91793e5d4", "ab4a35d75", "0b25f823f", "HEAD_1000", "BRANCH_1000", "QA999", "QA1000", "QA9991000", "1130", "twin",
        "createuser", "conflict-target", "one read per PR", "ACTUAL_MB", "999", "1000", "960"]
n = {t: len(re.findall(re.escape(t), s)) for t in toks}
print("residual-guard positive control on the TEMPLATE: total hits", sum(n.values()), "tokens with >=1 hit", sum(1 for v in n.values() if v), "of", len(toks))
PYC

run() { # $1 label, $2 expected rc, rest = env assignments; always --check
  local label="$1" want="$2"; shift 2
  out="$(env "$@" "$L" --check 2>&1)"; rc=$?
  printf '%s\n' "$out" | tail -2 | cut -c1-300 | sed 's/^/    /'
  echo "$label rc=$rc expect $want $([ "$rc" = "$want" ] && echo PASS || echo FAIL)"
}
run "neg1 (QA1002_HEAD wrong)" 6 QA1002_HEAD=0000000000000000000000000000000000000000
run "neg1b (QA1003_HEAD wrong)" 6 QA1003_HEAD=0000000000000000000000000000000000000000
sed 's/c5488a6891e6ac6fe950c101196d8c33ab8e173f/c5488a689/g' "$P" > "$T/neg_prompt_1002_1003_no1003sha.txt"
run "neg2 (prompt lacks full #1003 SHA)" 20 QA10021003_PROMPT="$T/neg_prompt_1002_1003_no1003sha.txt"
sed 's/wednesday-agent@agentmail.to/someone@example.invalid/g' "$P" > "$T/neg_prompt_1002_1003_nomaildest.txt"
run "neg3 (prompt lacks verdict destination)" 12 QA10021003_PROMPT="$T/neg_prompt_1002_1003_nomaildest.txt"
run "neg4 (the #1002-only prompt, pre-scopewiden)" 9 QA10021003_PROMPT="$Q/briefs/2026-09-16_secuura-1002-ks1123-tier2.prompt.txt.pre-scopewiden"
# neg5: #1003's head passed as #1002's -> #1002's ls-remote refuses first (exit 6), proving heads are checked per branch
run "neg5 (#1003 head pinned as #1002)" 6 QA1002_HEAD=c5488a6891e6ac6fe950c101196d8c33ab8e173f
# neg6: develop arm GUARDED — a launcher COPY pinned to develop 80686962, whose move to now is #1001 (csrf.ts) -> exit 18
sed "s/^DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'/DEVELOP_SHA='80686962828197acf305e4010a2ed5b401285743'/" "$L" > "$T/copy_dev_8068.sh"
echo "copy6 DEVELOP_SHA lines: $(/usr/bin/grep -c "^DEVELOP_SHA='80686962828197acf305e4010a2ed5b401285743'" "$T/copy_dev_8068.sh")"
out="$(bash "$T/copy_dev_8068.sh" --check 2>&1)"; rc=$?; printf '%s\n' "$out" | tail -1 | cut -c1-400 | sed 's/^/    /'
echo "neg6 (develop moved across csrf.ts) rc=$rc expect 18 $([ "$rc" = 18 ] && echo PASS || echo FAIL)"
# pos7: develop arm OK branch — a COPY with DEVELOP_SHA=0b25f823f and CUR_DEV fixed to 4ec051032 (#1000: one auth test) -> rc 0, MOVED note
sed -e "s/^DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'/DEVELOP_SHA='0b25f823f6660ac52b665f14055799ff0c3b616d'/" \
    -e "s/^CUR_DEV=\"\$(git -C \"\$REPO\" ls-remote origin refs\/heads\/develop | cut -f1)\"\$/CUR_DEV='4ec051032fdab1bfc82854c77273735dc0b8af8c'/" "$L" > "$T/copy_dev_disjoint.sh"
echo "copy7 DEVELOP_SHA lines: $(/usr/bin/grep -c "^DEVELOP_SHA='0b25f823f6660ac52b665f14055799ff0c3b616d'" "$T/copy_dev_disjoint.sh") CUR_DEV lines: $(/usr/bin/grep -c "^CUR_DEV='4ec051032fdab1bfc82854c77273735dc0b8af8c'" "$T/copy_dev_disjoint.sh")"
out="$(bash "$T/copy_dev_disjoint.sh" --check 2>&1)"; rc=$?; printf '%s\n' "$out" | /usr/bin/grep -i 'MOVED' | cut -c1-400 | sed 's/^/    /'
echo "pos7 (develop moved, disjoint) rc=$rc expect 0 $([ "$rc" = 0 ] && echo PASS || echo FAIL)"
cp -n "$T"/neg_prompt_1002_1003_*.txt "$G/" 2>/dev/null
echo "done $(date '+%H:%M:%S %Z')"
