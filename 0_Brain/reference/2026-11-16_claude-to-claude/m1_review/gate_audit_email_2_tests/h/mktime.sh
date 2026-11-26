#!/bin/bash
# usage: mktime.sh <name> [plant]: /private/tmp/claude-501/qae2/<name> = git archive 5aa56e1 + qae2_time.rs [+ plant]
Q=/private/tmp/claude-501/qae2; D=$Q/$1
[ -e "$D" ] && { echo exists; exit 2; }
mkdir -p "$D" && git -C $Q/c archive 5aa56e1 | tar -x -C "$D"
cp $Q/h/qae2_time.rs "$D/crates/coagent-audit/tests/qae2_time.rs"
python3 -B - "$D/crates/coagent-audit/Cargo.toml" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read(); s=s.replace('\n[lints]', '[[test]]\nname = "qae2_time"\n\n[lints]',1); open(p,'w').write(s)
PY
[ -n "$2" ] && python3 -B $Q/h/plant.py "$D" "$2" && diff -u $Q/ph/crates/coagent-audit/src/redact.rs "$D/crates/coagent-audit/src/redact.rs" > $Q/logs/plant_time_$2.diff
echo "$1: redact.rs $(shasum -a 256 $D/crates/coagent-audit/src/redact.rs | cut -c1-64)"
