#!/bin/bash
# arms_gate86.sh — the REFUSAL-ARM DRIVER for the gate86 kit. Every arm hands one tool ONE wrong or missing knob and asserts BOTH its exit code AND a reason string in its output; every family starts with a POSITIVE
# CONTROL (the same tool, right knobs, must pass) so a refusal can not be an artefact of a broken environment. Every input the arms build lives under the scratch directory given as --scratch (a canonical
# /private/tmp/claude-501/... path, REQUIRED, no default); the driver NEVER runs a real launch (no usage gate, no cockpit, no pane, no claude): arms that could reach one are listed as NOT RUN BY NAME at the end.
# It writes <scratch>/arms/<name>.{out,err,rc} and prints one line per arm: `ARM <name> rc=<got> want=<want> reason=<found|MISSING> -> OK|MISMATCH`. Exit 0 only if every arm matched.
# NOTE: the repin dry-run arms that get past the argument checks write dry_<HHMMSS>.* into the kit directory (the script's own output prefix); the driver moves those into <kit>/arms/ afterwards.
# Usage: bash arms_gate86.sh --scratch /private/tmp/claude-501/.../g86 --clone <a clone of the Secuura checkout under the scratch dir> --ready-ok
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
SCR=""; CLN=""
while [ $# -gt 0 ]; do case "$1" in --scratch) SCR="${2:-}"; shift 2 2>/dev/null || shift;; --clone) CLN="${2:-}"; shift 2 2>/dev/null || shift;; *) echo "usage: arms_gate86.sh --scratch <dir> --clone <dir>"; exit 9;; esac; done
[ -n "$SCR" ] && [ -n "$CLN" ] || { echo "REFUSING: --scratch and --clone are REQUIRED"; exit 9; }
case "$SCR" in /private/tmp/claude-501/*) ;; *) echo "REFUSING: --scratch must be under /private/tmp/claude-501/ (got $SCR)"; exit 9;; esac
case "$CLN" in "$SCR"/*) ;; *) echo "REFUSING: --clone must be under --scratch"; exit 9;; esac
[ -d "$CLN/.git" ] || [ -f "$CLN/HEAD" ] || { echo "REFUSING: --clone is not a git clone"; exit 9; }
A="$SCR/arms"; mkdir -p "$A" "$A/v"
KJSON="$GS/kit.json"
PY=/usr/bin/env
FAIL=0; NARM=0
DEV=e27b9dceff390d8048e8970efd2eab15f21b01fe
H1451=7336c6ba72031353338391235d5a99932449fe13; H1452=c2652aeaa499a000e978050c978913679c86b2c4; H1454=d3375905adc4ea03e2df3d704bb815dab9d0e7d2; H1455=5a28783cf22f022d4708d69041b8b4c751253f41
B1451=f8c86f859fe0c016a20fe413f5a53806f3592a50; B1452=4a7cc1f697f81f5b95d767dd5713ea344f3c76ea
T1451=952dea8d1487c92754a59d2072fdfb7dd89d9e23; T1452=a80f2135ff04e0ddd11c792b5eaa4b1e1564274a; T1454=a33ede92b9ac0579d3a2ba1aed710d6726360987; T1455=0c336c5ee7efd8e2e858d754f9df277097da4374
BR1451=feature/ks-591-six-post-bodies-declared-required-f12-1; BR1452=feature/ks-1364-five-post-bodies-declared-required-f13-2
BR1454=feature/ks-1355-dev-reload-names-the-slot-container-f15-4; BR1455=feature/ks-1417-env-local-example-drops-the-dead-gateway-port-f16-7
flip() { local s="$1"; local last="${s: -1}"; if [ "$last" = "0" ]; then printf '%s' "${s%?}1"; else printf '%s' "${s%?}0"; fi; }     # a wrong sha of the right shape: the last hex char becomes 0 (1 if it already was 0)
arm() {   # arm <name> <want-rc> <reason-substring> -- <command...>   (env assignments go through `env`)
  local name="$1" want="$2" reason="$3"; shift 4
  NARM=$((NARM + 1))
  "$@" > "$A/$name.out" 2> "$A/$name.err"; local rc=$?
  echo "$rc" > "$A/$name.rc"
  local found="MISSING"; /usr/bin/grep -qF -- "$reason" "$A/$name.out" "$A/$name.err" && found="found"
  local verdict="OK"; { [ "$rc" = "$want" ] && [ "$found" = "found" ]; } || { verdict="MISMATCH"; FAIL=$((FAIL + 1)); }
  echo "ARM $name rc=$rc want=$want reason($reason)=$found -> $verdict"
}
REPIN="$GS/repin_and_launch_gate86.sh"; L="$GS/launch_qa_secuura_gate86.sh"
std_args() { cat <<EOF
--seat|Seat K 3rd|--parents-n|1|--develop|$DEV|--head-1451|$H1451|--branch-1451|$BR1451|--tree-1451|$T1451|--base-1451|$B1451|--head-1452|$H1452|--branch-1452|$BR1452|--tree-1452|$T1452|--base-1452|$B1452|--head-1454|$H1454|--branch-1454|$BR1454|--tree-1454|$T1454|--base-1454|$DEV|--head-1455|$H1455|--branch-1455|$BR1455|--tree-1455|$T1455|--base-1455|$DEV
EOF
}
# build an argument array from std_args, replacing the value after flag $1 by $2 (or dropping the flag with value '@DROP@')
args_with() { local flag="$1" val="$2"; local -a out=(); local IFS='|'; local -a a; read -r -a a < <(std_args); local i=0
  while [ $i -lt ${#a[@]} ]; do
    if [ "${a[$i]}" = "$flag" ]; then [ "$val" = "@DROP@" ] || out+=("$flag" "$val"); i=$((i + 2)); else out+=("${a[$i]}"); i=$((i + 1)); fi
  done; printf '%s\n' "${out[@]}"; }
run_repin() { local name="$1" want="$2" reason="$3" flag="$4" val="$5"; shift 5; local -a v=(); while IFS= read -r l; do v+=("$l"); done < <(args_with "$flag" "$val"); arm "$name" "$want" "$reason" -- "$@" bash "$REPIN" "${v[@]}"; }
echo "== family R: repin_and_launch_gate86.sh argument arms (rc 9 malformed/missing, rc 11 WRONG VALUE vs kit.json) — none of these reaches the network"
# R0: the positive control for the V stage is the dry run already recorded in dry_run_console_final.txt (it passed); here the same arguments with ONE change each
run_repin R1_missing_seat 9 "REQUIRED argument is missing (SEAT)" --seat @DROP@ env
run_repin R2_bad_seat 9 "--seat must read" --seat "Seat 3rd" env
run_repin R3_short_head 9 "must be the FULL 40-hex" --head-1451 "${H1451:0:12}" env
run_repin R4_missing_base 9 "REQUIRED argument is missing (BS_1455)" --base-1455 @DROP@ env
run_repin R5_wrong_head 11 "WRONG VALUE --head-1452" --head-1452 "$(flip $H1452)" env
run_repin R6_wrong_branch 11 "WRONG VALUE --branch-1454" --branch-1454 feature/ks-1355-other env
run_repin R7_wrong_tree 11 "WRONG VALUE --tree-1455" --tree-1455 "$(flip $T1455)" env
run_repin R8_wrong_base_1451 11 "WRONG VALUE --base-1451" --base-1451 $DEV env
run_repin R9_wrong_base_1452 11 "WRONG VALUE --base-1452" --base-1452 $B1451 env
run_repin R10_parents_2 11 "WRONG VALUE --parents-n" --parents-n 2 env
run_repin R11_wrong_develop 11 "WRONG VALUE --develop" --develop "$(flip $DEV)" env
arm R12_unknown_flag 9 "usage: repin_and_launch_gate86.sh" -- bash "$REPIN" --bogus
arm R13_pr_not_in_batch 9 "not in this batch" -- bash "$REPIN" --head-1453 "$H1451"
std_one() { args_with --seat "Seat K 3rd" | tr '\n' '\037'; }
arm R14b_noapi_needs_dry 9 "--no-api is a dry-run option only" -- bash -c 'IFS=$'"'"'\x1f'"'"' read -r -a V <<< "$1"; shift; exec bash "$@" "${V[@]}" --no-api' _ "$(std_one)" "$REPIN"
arm R15b_clone_override_needs_dry 16 "G86_CLONE is a dry-run control only" -- bash -c 'IFS=$'"'"'\x1f'"'"' read -r -a V <<< "$1"; shift; exec env G86_CLONE="$1" bash "$2" "${V[@]}"' _ "$(std_one)" "$CLN" "$REPIN"

echo "== family D: dry runs against stand-ins (the kit clone override points at YOUR scratch clone; the ls-remote output is a file under the scratch dir)"
LSREAL="$A/v/ls_real.txt"
{ for r in refs/heads/develop refs/pull/1451/head refs/pull/1452/head refs/pull/1454/head refs/pull/1455/head; do :; done; }
printf '%s\t%s\n' $DEV refs/heads/develop $H1451 refs/pull/1451/head $H1451 "refs/heads/$BR1451" $H1452 refs/pull/1452/head $H1452 "refs/heads/$BR1452" $H1454 refs/pull/1454/head $H1454 "refs/heads/$BR1454" $H1455 refs/pull/1455/head $H1455 "refs/heads/$BR1455" > "$LSREAL"
# a stand-in with ONE moved head (pull/head of 1452)
sed "s#^${H1452}\trefs/pull/1452/head#$(flip $H1452)\trefs/pull/1452/head#" "$LSREAL" > "$A/v/ls_moved_head.txt"
# a stand-in whose branch differs from the head
sed "s#^${H1454}\trefs/heads/${BR1454}#$(flip $H1454)\trefs/heads/${BR1454}#" "$LSREAL" > "$A/v/ls_moved_branch.txt"
# a synthetic CHILD of develop that touches only a harmless new file (made in YOUR scratch clone; it makes 'develop moved' a real, resolvable, descendant sha)
CHILD="$(python3 - "$CLN" "$DEV" <<'PYEOF'
import os, subprocess, sys, tempfile
clone, dev = sys.argv[1], sys.argv[2]
env = dict(os.environ, GIT_AUTHOR_NAME='gate86', GIT_AUTHOR_EMAIL='g@invalid', GIT_COMMITTER_NAME='gate86', GIT_COMMITTER_EMAIL='g@invalid'); env.pop('GIT_SSH_COMMAND', None)
def g(*a, inp=None, e=None):
    p = subprocess.run(['git', '-C', clone] + list(a), capture_output=True, env=e or env, input=inp)
    assert p.returncode == 0, (a, p.stderr[:200]); return p.stdout.decode().strip()
tree = g('log', '-1', '--format=%T', dev); idx = os.path.join(tempfile.mkdtemp(prefix='g', dir='/private/tmp/claude-501'), 'idx'); e2 = dict(env, GIT_INDEX_FILE=idx)
g('read-tree', tree, e=e2); b = g('hash-object', '-w', '--stdin', inp=b'gate86 arm: a harmless file\n'); g('update-index', '--add', '--cacheinfo', '100644,%s,ZZ_gate86_arm.txt' % b, e=e2)
t2 = g('write-tree', e=e2); print(g('commit-tree', t2, '-p', dev, '-m', 'gate86 arm child of develop'))
PYEOF
)"
echo "synthetic develop-child $CHILD (touches only ZZ_gate86_arm.txt)"
printf '%s\t%s\n' $CHILD refs/heads/develop $H1451 refs/pull/1451/head $H1451 "refs/heads/$BR1451" $H1452 refs/pull/1452/head $H1452 "refs/heads/$BR1452" $H1454 refs/pull/1454/head $H1454 "refs/heads/$BR1454" $H1455 refs/pull/1455/head $H1455 "refs/heads/$BR1455" > "$A/v/ls_moved_develop.txt"
std_dry() { args_with --seat "Seat K 3rd" | tr '\n' '\037'; }
dry() { local name="$1" want="$2" reason="$3" ls="$4"; shift 4; arm "$name" "$want" "$reason" -- bash -c 'IFS=$'"'"'\x1f'"'"' read -r -a V <<< "$1"; ls="$2"; repin="$3"; shift 3; exec env G86_ROUTING="$G86_ROUTING_X" G86_LSFILE="$ls" G86_CLONE="$G86_CLONE_X" bash "$repin" "${V[@]}" --dry-run --no-api "$@"' _ "$(std_dry)" "$ls" "$REPIN" "$@"; }
export G86_ROUTING_X="$GS/ROUTING_PROPOSAL.txt" G86_CLONE_X="$CLN"
# D0 first: a dry run against the REAL-develop stand-in re-renders prompt_gate86.rendered.txt and head_at_launch.txt (test seat), so the L family below never depends on what an earlier run left behind
dry D0_positive_control 0 "DRY RUN COMPLETE" "$LSREAL"
echo "== family L: launch_qa_secuura_gate86.sh --check arms (overrides G86_PROMPT / G86_HEADFILE / G86_LS / G86_KITJSON / G86_FILES_DIR point at files under the scratch dir)"
P0="$GS/prompt_gate86.rendered.txt"; H0="$GS/head_at_launch.txt"
lchk() { local name="$1" want="$2" reason="$3"; shift 3; arm "$name" "$want" "$reason" -- env "$@" bash "$L" --check; }
lchk L0_positive_control 0 "all guards pass" G86_LS="$LSREAL"
vp() { python3 - "$P0" "$A/v/$1" "$2" "$3" <<'PYEOF'
import sys
src, dst, old, new = sys.argv[1:5]
t = open(src, encoding='utf-8').read()
assert old == '@FIRSTLINE@' or old in t, 'variant anchor not found: %r' % old[:60]
open(dst, 'w', encoding='utf-8').write(t.replace(old, new) if old != '@FIRSTLINE@' else new + '\n' + t.split('\n', 1)[1])
PYEOF
}
vp p_unfilled_brace.txt "Origin develop at launch:" "Origin develop at launch {{DEVELOP}}:"
lchk L1_unfilled_double_brace 8 "unfilled double-brace token" G86_LS="$LSREAL" G86_PROMPT="$A/v/p_unfilled_brace.txt"
vp p_unfilled_seat.txt "The merge seat is " "The merge seat is @MERGE_SEAT@ and also "
lchk L2_unfilled_merge_seat 8 "@MERGE_SEAT@ is unfilled" G86_LS="$LSREAL" G86_PROMPT="$A/v/p_unfilled_seat.txt"
vp p_wrong_go.txt "GO (Seat K 3rd): merge 1451 on gate86" "GO (Seat Z 9th): merge 1451 on gate86"
lchk L3_wrong_go_string 8 "GO strings must be exactly" G86_LS="$LSREAL" G86_PROMPT="$A/v/p_wrong_go.txt"
vp p_no_think.txt "@FIRSTLINE@" "think"
lchk L4_no_thinking_directive 8 "thinking directive" G86_LS="$LSREAL" G86_PROMPT="$A/v/p_no_think.txt"
vp p_no_kw.txt "MERGE-ORDER" "MERGE ORDER"
lchk L5_missing_keyword 33 "by-name keyword" G86_LS="$LSREAL" G86_PROMPT="$A/v/p_no_kw.txt"
vp p_no_hold.txt "NO MERGE, NO PUSH to any PR branch" "no merge"
lchk L6_missing_hold 39 "the HOLDS" G86_LS="$LSREAL" G86_PROMPT="$A/v/p_no_hold.txt"
vp p_no_addendum.txt "is the LAST thing you write to report.md" "is written whenever"
lchk L7_missing_addendum_rule 25 "MERGE ADDENDUM" G86_LS="$LSREAL" G86_PROMPT="$A/v/p_no_addendum.txt"
vp p_no_x9.txt "(X9) the #1455 suite" "(X9) nothing"
lchk L8_missing_named_exception_x9 39 "the HOLDS" G86_LS="$LSREAL" G86_PROMPT="$A/v/p_no_x9.txt"
vp p_no_head.txt "$H1455" "${H1455:0:12}"
lchk L9_prompt_lacks_a_head_in_full 8 "does not name the #1455 head" G86_LS="$LSREAL" G86_PROMPT="$A/v/p_no_head.txt"
hv() { python3 - "$H0" "$A/v/$1" "$2" "$3" <<'PYEOF'
import sys
src, dst, old, new = sys.argv[1:5]
t = open(src).read(); assert old in t, old; open(dst, 'w').write(t.replace(old, new, 1))
PYEOF
}
hv h_wrong_head.txt "$H1452" "$(flip $H1452)"
lchk L10_headfile_wrong_head 7 "WRONG VALUE #1452 head" G86_LS="$LSREAL" G86_HEADFILE="$A/v/h_wrong_head.txt"
hv h_wrong_base.txt "B 1454 $DEV" "B 1454 $B1451"
lchk L11_headfile_wrong_base_for_one_pr 7 "WRONG VALUE #1454 base" G86_LS="$LSREAL" G86_HEADFILE="$A/v/h_wrong_base.txt"
grep -v '^P 1455 ' "$H0" > "$A/v/h_missing_p.txt"
lchk L12_headfile_missing_a_P_line 7 "must carry exactly 4 'P ' lines" G86_LS="$LSREAL" G86_HEADFILE="$A/v/h_missing_p.txt"
hv h_bad_seat.txt "S Seat K 3rd" "S Seat 3rd"
lchk L13_headfile_bad_seat 7 "is not 'Seat X nth'" G86_LS="$LSREAL" G86_HEADFILE="$A/v/h_bad_seat.txt"
lchk L14_moved_pull_head 6 "a verdict is valid ONLY at its head" G86_LS="$A/v/ls_moved_head.txt"
lchk L15_moved_develop 17 "origin develop" G86_LS="$A/v/ls_moved_develop.txt"
python3 - "$KJSON" "$A/v/kit_bad_pin.json" <<'PYEOF'
import json, sys
k = json.load(open(sys.argv[1])); k['script_sha256']['c2_code_gate86.py'] = '0' * 64; json.dump(k, open(sys.argv[2], 'w'))
PYEOF
lchk L16_bad_pin 31 "BAD PIN" G86_LS="$LSREAL" G86_KITJSON="$A/v/kit_bad_pin.json"
mkdir -p "$A/v/files"; for f in lib_gate86.py c1_pin_gate86.py c2_code_gate86.py c3_cells_gate86.py gh_gate86.py prompt_gate86.txt launch_qa_secuura_gate86.sh repin_and_launch_gate86.sh KIT_REPORT.md RULINGS_wednesday.md READY_seatF16_tier2_batch.txt; do cp "$GS/$f" "$A/v/files/$f"; done
lchk L17_files_dir_positive_control 0 "all guards pass" G86_LS="$LSREAL" G86_FILES_DIR="$A/v/files"
printf 'tampered\n' >> "$A/v/files/READY_seatF16_tier2_batch.txt"
lchk L18_ready_copy_tampered 31 "ready_sha256_16" G86_LS="$LSREAL" G86_FILES_DIR="$A/v/files"
: > "$A/v/files/RULINGS_wednesday.md"
lchk L19_rulings_empty 30 "MISSING or empty" G86_LS="$LSREAL" G86_FILES_DIR="$A/v/files"
arm L20_launch_without_tty 21 "stdin is not a TTY" -- env G86_LS="$LSREAL" bash "$L" < /dev/null
echo "== family D (continued): the dry runs D1..D6 (D5 leaves a test develop in the rendered prompt / head file; D6 restores the real one)"
dry D1_moved_head 11 "MISMATCH" "$A/v/ls_moved_head.txt"
dry D2_branch_not_head 11 "MISMATCH" "$A/v/ls_moved_branch.txt"
dry D3_moved_develop_no_repin 10 "develop moved" "$A/v/ls_moved_develop.txt"
dry D4_moved_develop_stale_repin 10 "stale re-pin" "$A/v/ls_moved_develop.txt" --repin-develop $DEV
dry D5_moved_develop_with_repin 0 "RE-PINNED develop" "$A/v/ls_moved_develop.txt" --repin-develop $CHILD
dry D6_restore_real_render 0 "DRY RUN COMPLETE" "$LSREAL"
echo "(D0 and D5 are the POSITIVE controls of this family; D6 re-renders the kit against the real develop again, because D5 leaves a test develop in the rendered files: the refusals D1..D4 are not an artefact of the stand-in; D5 also proves the --repin-develop path end to end, launcher --check included)"
echo "== family C: the tools' required knobs (a missing / wrong value must refuse BY NAME; stderr or stdout carries the reason)"
CC="$CLN"
c1() { python3 "$GS/c1_pin_gate86.py" "$@"; }
arm C1_0_positive_control 0 "0 FAIL" -- python3 "$GS/c1_pin_gate86.py" pin --repo "$CC" --pr 1451 --head $H1451 --base $B1451 --develop $DEV --end-tree $T1451 --parents-n 1 --no-remote
arm C1_1_missing_pr 1 "--pr is REQUIRED" -- python3 "$GS/c1_pin_gate86.py" pin --repo "$CC" --head $H1451 --base $B1451 --develop $DEV --end-tree $T1451 --parents-n 1 --no-remote
arm C1_2_short_head 1 "must be a FULL 40-hex" -- python3 "$GS/c1_pin_gate86.py" pin --repo "$CC" --pr 1451 --head ${H1451:0:12} --base $B1451 --develop $DEV --end-tree $T1451 --parents-n 1 --no-remote
arm C1_3_foreign_pr 1 "is not a kit PR" -- python3 "$GS/c1_pin_gate86.py" pin --repo "$CC" --pr 1453 --head $H1451 --base $B1451 --develop $DEV --end-tree $T1451 --parents-n 1 --no-remote
arm C1_4_wrong_base_is_a_FAIL 1 "FAIL P0" -- python3 "$GS/c1_pin_gate86.py" pin --repo "$CC" --pr 1451 --head $H1451 --base $B1452 --develop $DEV --end-tree $T1451 --parents-n 1 --no-remote
arm C1_5_wrong_end_tree_is_a_FAIL 1 "FAIL P0" -- python3 "$GS/c1_pin_gate86.py" pin --repo "$CC" --pr 1451 --head $H1451 --base $B1451 --develop $DEV --end-tree $T1452 --parents-n 1 --no-remote
arm C1_6_parents_2_is_a_FAIL 1 "FAIL P0" -- python3 "$GS/c1_pin_gate86.py" pin --repo "$CC" --pr 1451 --head $H1451 --base $B1451 --develop $DEV --end-tree $T1451 --parents-n 2 --no-remote
arm C1_7_unresolvable_sha 1 "is not in" -- python3 "$GS/c1_pin_gate86.py" pin --repo "$CC" --pr 1451 --head $H1451 --base $B1451 --develop 0123456789012345678901234567890123456789 --end-tree $T1451 --parents-n 1 --no-remote
arm C1_8_docsbase_wrong_base 1 "pinned branch point" -- python3 "$GS/c1_pin_gate86.py" docsbase --repo "$CC" --pr 1451 --head $H1451 --base $DEV --develop $DEV
arm C1_9_isolation_missing_a_head 1 "--head must be given for exactly" -- python3 "$GS/c1_pin_gate86.py" isolation --repo "$CC" --develop $DEV --head 1451=$H1451 --head 1452=$H1452
arm C1_10_isolation_wrong_head 1 "FAIL I0-1454" -- python3 "$GS/c1_pin_gate86.py" isolation --repo "$CC" --develop $DEV --head 1451=$H1451 --head 1452=$H1452 --head 1454=$H1455 --head 1455=$H1455
arm C2_0_positive_control 0 "0 FAIL" -- python3 "$GS/c2_code_gate86.py" claims --repo "$CC" --pr 1455 --head $H1455 --base $DEV
arm C2_1_missing_base 1 "--base is REQUIRED" -- python3 "$GS/c2_code_gate86.py" claims --repo "$CC" --pr 1455 --head $H1455
arm C2_2_head_differs_from_kit 1 "differ from the kit pins" -- python3 "$GS/c2_code_gate86.py" claims --repo "$CC" --pr 1455 --head $H1454 --base $DEV
arm C2_3_base_differs_from_kit 1 "differ from the kit pins" -- python3 "$GS/c2_code_gate86.py" claims --repo "$CC" --pr 1451 --head $H1451 --base $DEV
arm C2_4_foreign_pr 1 "is not a kit PR" -- python3 "$GS/c2_code_gate86.py" claims --repo "$CC" --pr 1453 --head $H1451 --base $B1451
arm C2_5_handlers_for_a_script_pr 1 "handlers is for the contract PRs" -- python3 "$GS/c2_code_gate86.py" handlers --repo "$CC" --pr 1454 --head $H1454
arm C3_0_positive_control_selftest 0 "0 FAIL" -- python3 "$GS/c3_cells_gate86.py" --selftest
arm C3_1_prep_onto_existing_tree 2 "exists" -- python3 "$GS/c3_cells_gate86.py" prep --repo "$CC" --rev $H1455 --tree "$A/v/files"
arm C3_2_prep_tree_under_forbidden_root 1 "not a canonical /private/tmp/claude-501/" -- python3 "$GS/c3_cells_gate86.py" prep --repo "$CC" --rev $H1455 --tree "/Volumes/DevMASTER/!CODING/gate86_arm_tree_never_created"
arm C3_3_prep_tree_not_canonical 1 "not a canonical /private/tmp/claude-501/" -- python3 "$GS/c3_cells_gate86.py" prep --repo "$CC" --rev $H1455 --tree "/tmp/gate86_arm_tree_never_created"
arm C3_4_prep_short_rev 1 "must be a FULL 40-hex" -- python3 "$GS/c3_cells_gate86.py" prep --repo "$CC" --rev ${H1455:0:12} --tree "$A/v/new_tree_never_created"
arm C3_5_compose_missing_a_head 1 "--head for exactly" -- python3 "$GS/c3_cells_gate86.py" compose --clone "$CC" --develop $DEV --head 1451=$H1451 --out "$A/v/compose_out"
arm C3_6_compose_head_differs_from_kit 1 "differs from the kit pin" -- python3 "$GS/c3_cells_gate86.py" compose --clone "$CC" --develop $DEV --head 1451=$H1455 --head 1452=$H1452 --head 1454=$H1454 --head 1455=$H1455 --out "$A/v/compose_out"
arm C3_7_compose_clone_under_forbidden_root 1 "REFUSED" -- python3 "$GS/c3_cells_gate86.py" compose --clone "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" --develop $DEV --head 1451=$H1451 --head 1452=$H1452 --head 1454=$H1454 --head 1455=$H1455 --out "$A/v/compose_out"
arm C3_8_vitest_for_a_shell_pr 1 "vitest is for" -- python3 "$GS/c3_cells_gate86.py" vitest --repo "$CC" --pr 1454 --tree "$A/v/files" --out "$A/v/o"
arm C3_9_shell_for_a_contract_pr 1 "shell is for" -- python3 "$GS/c3_cells_gate86.py" shell --repo "$CC" --pr 1451 --tree "$A/v/files" --out "$A/v/o"
arm C3_10_regen_without_tsx 1 "tsx missing" -- python3 "$GS/c3_cells_gate86.py" regen --tree "$A/v/files" --out "$A/v/o"
arm GH_0_positive_control_selftest 0 "SELFTEST" -- python3 "$GS/gh_gate86.py" --selftest
arm GH_1_foreign_pr 2 "is not a kit PR" -- python3 "$GS/gh_gate86.py" api --pr 1453 --head $H1451
arm GH_2_missing_head 2 "--head is REQUIRED" -- python3 "$GS/gh_gate86.py" api --pr 1451
arm GH_3_wrong_head_rc1 1 "BODY sha256/16" -- python3 "$GS/gh_gate86.py" api --pr 1451 --head $H1452
arm GH_4_audit_missing_a_pin 2 "is REQUIRED" -- python3 "$GS/gh_gate86.py" audit --repo "$CC" --base1451 $B1451
echo
echo "ARMS DRIVEN: $NARM | MISMATCHES: $FAIL"
echo "NOT RUN BY NAME (each could reach a real launch / a pane / the usage gate if the guard under test failed): a real launch with a G86_* override set (rc 16 after the TTY check), rc 12 (usage gate), rc 14 (cockpit add), rc 1 (routing row absent on a REAL run: a dry run only reports it), rc 18 (READY copy sha mismatch inside the repin script: the launcher's own rc 31 on the same copy IS driven as L18)."
[ "$FAIL" = 0 ]
