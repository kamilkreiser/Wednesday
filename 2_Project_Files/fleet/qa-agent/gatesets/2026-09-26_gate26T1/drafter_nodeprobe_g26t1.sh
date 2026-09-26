#!/bin/bash
# drafter_nodeprobe_g26t1.sh — a PREDICTION for the gate, never its evidence: #1280's toBlockHeight, extracted BYTE-FOR-BYTE from the head blob
# (the `export function toBlockHeight` through its closing brace, READ from the scratch clone; the head is asserted equal to the pin), run under
# node 24's type stripping over the edge inputs the prompt names. The heal paths themselves are NOT run here (the gate owes that).
# Usage: drafter_nodeprobe_g26t1.sh <scratch clone> <expected #1280 head>
set -u
CL="$1"; WANT="$2"; D="$(dirname "$(/bin/realpath "$0")")/nodeprobe_work"; mkdir -p "$D"
H="$(git --git-dir "$CL" rev-parse refs/g26/pull/1280)"; [ "$H" = "$WANT" ] || { echo "REFUSING: clone's #1280 $H != pin $WANT"; exit 2; }
git --git-dir "$CL" show "$H:Blockchain/Dev/services/originate/src/routes/verification.ts" | python3 -c '
import sys; t = sys.stdin.read(); a = t.index("export function toBlockHeight("); b = t.index("\n}\n", a) + 3; sys.stdout.write(t[a:b])' > "$D/toBlockHeight.ts"
echo "head $H | toBlockHeight.ts sha256 $(shasum -a 256 "$D/toBlockHeight.ts" | cut -c1-16) ($(wc -l < "$D/toBlockHeight.ts" | tr -d ' ') lines) | node $(node --version)"
cat > "$D/run.mts" <<'JS'
const { toBlockHeight } = await import(process.argv[2]);
const cases = [['null', null], ['undefined', undefined], ["'4242'", '4242'], ["' 42 '", ' 42 '], ["''", ''], ["'abc'", 'abc'], ['0', 0], ["'0'", '0'],
  ["'0x10'", '0x10'], ["'1e3'", '1e3'], ["'-1'", '-1'], ["'4242.5'", '4242.5'], ["'9007199254740993' (MAX_SAFE+2)", '9007199254740993'],
  ['9007199254740993n (BigInt)', 9007199254740993n], ['Infinity', Infinity], ['NaN', NaN], ['true', true], ['{}', {}]];
for (const [k, v] of cases) { const r = toBlockHeight(v); console.log(`${k.padEnd(34)} -> ${typeof r === 'number' ? String(r) : JSON.stringify(r)}`); }
JS
node "$D/run.mts" "$D/toBlockHeight.ts"
