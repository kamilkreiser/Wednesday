# mut.sh <label> <test-target> [<test-target>...]: build bins + run the named integration tests in the merged clone
W=/private/tmp/claude-501/qp1; export COAGENT_TOOLS=$W/tools CARGO_TARGET_DIR=$W/tgt; . $W/m/scripts/env.sh
label=$1; shift; log=$W/p/mut_$label.log
sel=(); for t in "$@"; do sel+=(--test "$t"); done
{ nice -n 10 cargo build --workspace --bins --locked --manifest-path $W/m/Cargo.toml 2>&1 && nice -n 10 cargo test --locked --no-fail-fast --manifest-path $W/m/Cargo.toml -p coagent-daemon "${sel[@]}" 2>&1; } > $log
echo "[$label] $(grep -E '^test .* (ok|FAILED)$' $log | sed 's/^test //' | tr '\n' ';')"
grep -m3 -A2 'panicked at' $log | sed -e "s#$(cd $W && pwd -P)#<qp1>#g" -e "s#$W#<qp1>#g" | cut -c1-260
grep -m2 '^error' $log
