#!/bin/bash
# QA-W-DAEMON: the five COAGENT_RED_WD rows run one by one (the runner's own test selection), and the
# build script's three refusals. Light runs only (one test target each); the full runner is not re-run.
W=/private/tmp/claude-501/qwd; T=$W/p
export COAGENT_TOOLS=$W/tools CARGO_TARGET_DIR=$W/target-p-red
. $T/scripts/env.sh
run() { env -C $T "$@"; }
while IFS='|' read -r var name pkg target test item; do
  out=$(run env "$var=$name" cargo test --locked -p "$pkg" --test "$target" -- --exact "$test" 2>&1)
  if grep -q "test result: FAILED" <<<"$out" && grep -qF "test $test ... FAILED" <<<"$out"; then st=RED; elif grep -q "test result: ok" <<<"$out"; then st="STILL GREEN"; else st=ERROR; fi
  echo "ROW $item $name -> $test: $st"; grep -m1 -A1 "panicked at" <<<"$out" | tail -1 | cut -c1-260 | sed 's/^/     text: /'
done < <(grep '"COAGENT_RED_WD|' $T/scripts/red-controls-daemon.sh | tr -d '" ')
echo "CLEAN (no variable): $(run cargo test --locked -p coagent-daemon --test win_rules 2>&1 | grep 'test result')"
echo "== refusals of the build script"
o=$(run env COAGENT_RED_WD=no_such_name cargo check --locked -p coagent-daemon 2>&1); echo "unknown name: exit-ish $(grep -c 'is not a known red control' <<<"$o") hit(s): $(grep -m1 -o 'COAGENT_RED_WD=no_such_name is not a known red control' <<<"$o")"
o=$(run env COAGENT_RED_WD=win_profile_case_exact cargo check --locked --release -p coagent-daemon 2>&1); echo "release: $(grep -m1 -o 'COAGENT_RED_WD is for test builds only' <<<"$o")"
for other in "COAGENT_RED_DAEMON=log_text" "COAGENT_RED_P1P=$(grep -m1 -o '"COAGENT_RED_P1P|[a-z_]*' $T/scripts/red-controls-daemon.sh | cut -d'|' -f2)" "COAGENT_RED_RR=ended_cleanup_repeats"; do
  o=$(run env COAGENT_RED_WD=win_profile_case_exact "$other" cargo check --locked -p coagent-daemon 2>&1); echo "together with $other: $(grep -m1 -o 'COAGENT_RED_WD cannot be set together[^"]*' <<<"$o" | cut -c1-60) | other panics: $(grep -m1 -E "panicked|error: failed to run custom build" <<<"$o" | cut -c1-120)"
done
echo "positive control (a known name, debug, alone, builds): $(run env COAGENT_RED_WD=win_profile_case_exact cargo check --locked -p coagent-daemon 2>&1 | grep -m1 -oE 'RED CONTROL BUILD: coagent_red=\"win_profile_case_exact\"|Finished')"
