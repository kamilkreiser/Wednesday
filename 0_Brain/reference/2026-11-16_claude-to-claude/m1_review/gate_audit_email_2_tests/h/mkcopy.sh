#!/bin/bash
# usage: mkcopy.sh <name> <rev>  : /private/tmp/claude-501/qae2/<name> = git archive <rev> + the probe as test target qae2_probe
Q=/private/tmp/claude-501/qae2; D=$Q/$1
[ -e "$D" ] && { echo "exists: $D"; exit 2; }
mkdir -p "$D" && git -C $Q/c archive "$2" | tar -x -C "$D" || exit 3
cp $Q/h/qae2_probe.rs "$D/crates/coagent-audit/tests/qae2_probe.rs"
python3 -B - "$D/crates/coagent-audit/Cargo.toml" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read(); s=s.replace('\n[lints]', '[[test]]\nname = "qae2_probe"\n\n[lints]',1); open(p,'w').write(s)
PY
echo "$1 = $2: redact.rs sha256 $(shasum -a 256 $D/crates/coagent-audit/src/redact.rs | cut -c1-64)"
