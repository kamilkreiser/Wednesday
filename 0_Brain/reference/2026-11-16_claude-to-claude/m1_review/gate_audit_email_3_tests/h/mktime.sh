#!/bin/bash
# usage: mktime.sh <name> [plant]: qae3/<name> = git archive 6274318 (fetch-only repo) + qae3_time.rs [+ plant]
Q=/private/tmp/claude-501/qae3; D=$Q/$1
[ -e "$D" ] && { echo exists; exit 2; }
mkdir -p "$D" && git -C $Q/gho archive 627431877d5fa3b86f91ec23d0dc2879c800eb33 | tar -x -C "$D"
cp $Q/h/qae3_time.rs "$D/crates/coagent-audit/tests/qae3_time.rs"
python3 -B - "$D/crates/coagent-audit/Cargo.toml" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read(); s=s.replace('\n[lints]', '[[test]]\nname = "qae3_time"\n\n[lints]',1); open(p,'w').write(s)
PY
if [ -n "$2" ]; then python3 -B $Q/h/plant.py "$D" "$2" && diff -u <(git -C $Q/gho show 6274318:crates/coagent-audit/src/redact.rs) "$D/crates/coagent-audit/src/redact.rs" > $Q/logs/plant_time_$2.diff; fi
echo "$1: redact.rs $(shasum -a 256 $D/crates/coagent-audit/src/redact.rs | cut -c1-64)"
