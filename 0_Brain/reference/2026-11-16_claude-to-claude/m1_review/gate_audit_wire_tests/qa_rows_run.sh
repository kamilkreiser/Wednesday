#!/bin/bash
# QA-DAEMON-NOTES item 5 runner. Usage: bash qa_rows_run.sh <rows checkout> <target dir> <out dir> [rows...]
# For each row: reset the checkout to the head, plant ONE change (qa_rows.py), give EVERY .rs file a new
# mtime, build the workspace bins, run the row's test by --exact, keep the log and the first panic line.
# Then "head": the same checkout reset, every test again (must be green: proves no stale build either way).
set -u
RR="$1"; T="$2"; OUT="$3"; shift 3
QA=/private/tmp/claude-501/qdn/qa
R=/private/tmp/claude-501/qdn/r.sh
mkdir -p "$OUT"
declare -a TESTS
t_of() {
  case "$1" in
    r1) echo "-p coagent-daemon --test dn_flags -- --exact empty_relay_url_or_pin_is_refused_at_start" ;;
    r1b) echo "-p coagent-daemon --lib -- --exact link::tests::connect_with_no_candidate_names_why" ;;
    r2|r8) echo "-p coagent-daemon --test dn_cert -- --exact a_changed_relay_certificate_is_named_in_status" ;;
    r3) echo "-p coagent-daemon --test dn_invite -- --exact a_dead_relay_fails_the_waiting_invitation_truthfully" ;;
    r4) echo "-p coagent-daemon --test dn_help -- --exact run_and_main_both_call_the_gate_rule" ;;
    r4b) echo "-p coagent-daemon --test dn_help -- --exact usage_shows_the_command_prompt_form" ;;
    r5) echo "-p coagent-daemon --test dn_comments -- --exact stale_sentences_are_gone" ;;
    r6) echo "-p coagent-daemon --test dn_recovery -- --exact a_forward_ack_clears_row_54s_clock" ;;
    r7u) echo "-p coagent-mcp --bin coagent-mcp -- --exact tests::dn_wrong_argument_types_are_refused_with_fixed_texts" ;;
    r7i) echo "-p coagent-daemon --test dn_mcp -- --exact dn_mcp_wrong_argument_types_are_tool_errors_with_fixed_texts" ;;
  esac
}
plant_of() { case "$1" in r7u|r7i) echo r7 ;; *) echo "$1" ;; esac; }
run_one() { # <label> <plant or -> <testkey>
  local L="$1" P="$2" K="$3" log="$OUT/$1__$3.log"
  git -C "$RR" checkout --quiet -- . || return 9
  [ "$P" = "-" ] || python3 -B "$QA/qa_rows.py" "$RR" "$P" > "$log" 2>&1 || { echo "$L $K PLANT FAILED"; return; }
  git -C "$RR" diff > "$OUT/$L.diff"
  find "$RR/crates" -name '*.rs' -exec touch {} +
  "$R" "$RR" "$T" cargo build --workspace --bins --locked >> "$log" 2>&1 || { echo "$L $K BUILD FAILED"; return; }
  # shellcheck disable=SC2046
  "$R" "$RR" "$T" cargo test --locked $(t_of "$K") >> "$log" 2>&1
  local rc=$?
  local comp; comp=$(grep -c -E 'Compiling coagent-(daemon|mcp) ' "$log")
  local first; first=$(grep -m1 -A1 -E "^thread '.*' panicked at" "$log" | tail -1)
  local res; res=$(grep -m1 -E '^test result:' "$log")
  echo "$L | $K | exit $rc | recompiled daemon/mcp units: $comp | $res | first panic line: ${first:-none}"
}
ROWS_ALL="r1 r1b r2 r8 r3 r4 r4b r5 r6 r7u r7i"
for K in ${@:-$ROWS_ALL}; do run_one "$K" "$(plant_of "$K")" "$K"; done | tee -a "$OUT/rows.out"
for K in ${@:-$ROWS_ALL}; do run_one head - "$K"; done | tee -a "$OUT/rows.out"
git -C "$RR" checkout --quiet -- .
