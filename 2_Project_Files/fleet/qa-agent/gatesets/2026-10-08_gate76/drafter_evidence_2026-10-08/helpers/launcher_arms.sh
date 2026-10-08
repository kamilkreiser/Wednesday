#!/bin/bash
# launcher_arms.sh — the gate76 drafter's refusal arms for the launcher and the repin (each must refuse at ITS OWN assert: the refusing
# line is printed beside the rc, STANDING_LINES :441), plus the untampered CONTROL. Copies live in a scratch dir; the kit is never edited.
# Usage: launcher_arms.sh <kit dir> <scratch dir> <out dir>
set -u
K="$1"; S="$2"; O="$3"; mkdir -p "$S" "$O"
L="$K/launch_qa_secuura_gate76.sh"; RP="$K/repin_and_launch_gate76.sh"
H7=2b6da5f561b05a820bbe1ab5e891bff9f4f531c8; H8=64eafead891e81f5adb4e46aaa94ff6a6ace1998; D=0a6177ea5482227e83d5045b68b8577a56326ffc
# one live ls-remote, saved as the stand-in for every launcher arm (the CONTROL also runs live)
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
env -u GIT_SSH_COMMAND git -C "$REPO" -c core.sshCommand="$(git -C "$REPO" config --get core.sshCommand)" ls-remote git@github.com:Secuura/Distributed_Secuura.git \
  refs/heads/develop refs/pull/1427/head refs/pull/1428/head refs/heads/feature/ks-1274-trivy-bare-object-guard-ra18-1 \
  refs/heads/feature/ks-593-not-a-server-error-originate-three-passes-g4-1 > "$S/ls.txt"
arm() { # name want_rc cmd...
  local n="$1" w="$2"; shift 2
  "$@" > "$O/$n.out" 2> "$O/$n.err" < /dev/null; local rc=$?
  printf '%-40s rc %-3s want %-3s %s | %s\n' "$n" "$rc" "$w" "$([ "$rc" = "$w" ] && echo MATCH || echo MISMATCH)" "$(cat "$O/$n.err" "$O/$n.out" | grep -m1 -E 'REFUSING|all guards pass' | cut -c1-150)"
}
# repin arms
arm r1_wrong_head_1427      11 bash "$RP" --head-1427 "$D" --head-1428 "$H8" --develop "$D" --dry-run --no-api
arm r2_missing_head_1428     9 bash "$RP" --head-1427 "$H7" --develop "$D" --dry-run --no-api
arm r3_noapi_without_dry     9 bash "$RP" --head-1427 "$H7" --head-1428 "$H8" --develop "$D" --no-api
arm r4_wrong_develop        11 bash "$RP" --head-1427 "$H7" --head-1428 "$H8" --develop "$H7" --dry-run --no-api
# launcher arms (each on a COPY of the one input it perturbs)
arm l0_CONTROL_untampered    0 env G76_LS="$S/ls.txt" bash "$L" --check
cp -R "$K" "$S/kitcopy" 2>/dev/null; printf ' ' >> "$S/kitcopy/c4_docs_gate76.py"
arm l1_bad_pin              31 env G76_LS="$S/ls.txt" G76_FILES_DIR="$S/kitcopy" bash "$L" --check
sed 's/^C base$/C develop/' "$K/head_at_launch.txt" > "$S/hf_comp.txt"
arm l2_headfile_comparator   7 env G76_LS="$S/ls.txt" G76_HEADFILE="$S/hf_comp.txt" bash "$L" --check
sed 's/^O 1428,1427$/O 1427,1428/' "$K/head_at_launch.txt" > "$S/hf_order.txt"
arm l3_headfile_order        7 env G76_LS="$S/ls.txt" G76_HEADFILE="$S/hf_order.txt" bash "$L" --check
sed 's/NULL-RESULTS-GAP/NULL-RESULTS-XXX/g' "$K/prompt_gate76.rendered.txt" > "$S/p_kw.txt"
arm l4_keyword_missing      33 env G76_LS="$S/ls.txt" G76_PROMPT="$S/p_kw.txt" bash "$L" --check
python3 - "$K/kit.json" "$S/k_author.json" "$S/k_null.json" "$S/k_lane.json" <<'EOF'
import json, sys
K = json.load(open(sys.argv[1]))
a = dict(K, merge_seat_ordinal='Seat R 18th'); json.dump(a, open(sys.argv[2], 'w'))
n = dict(K, merge_seat=None, merge_seat_ordinal=None); json.dump(n, open(sys.argv[3], 'w'))
l = dict(K, merge_seat='Secuura/Blockchain-G'); json.dump(l, open(sys.argv[4], 'w'))
EOF
arm l5_merge_seat_is_author  8 env G76_LS="$S/ls.txt" G76_KITJSON="$S/k_author.json" bash "$L" --check
arm l6_merge_seat_unruled    8 env G76_LS="$S/ls.txt" G76_KITJSON="$S/k_null.json" bash "$L" --check
arm l7_lane_ordinal_differ   8 env G76_LS="$S/ls.txt" G76_KITJSON="$S/k_lane.json" bash "$L" --check
sed 's/merge 1427 on gate76/merge 1427 on gate75/g' "$K/prompt_gate76.rendered.txt" > "$S/p_go.txt"
arm l8_GO_1427_wrong_gate     8 env G76_LS="$S/ls.txt" G76_PROMPT="$S/p_go.txt" bash "$L" --check
sed 's/^\(2b6da5f561b05a820bbe1ab5e891bff9f4f531c8\)\(.refs\/pull\/1427\/head\)/0000000000000000000000000000000000000000\2/' "$S/ls.txt" > "$S/ls_moved.txt"
arm l9_moved_pull_head        6 env G76_LS="$S/ls_moved.txt" bash "$L" --check
arm l10_launch_no_tty        21 env G76_LS="$S/ls.txt" bash "$L"
