#!/bin/bash
# latest_models_arms.sh -- red-proof arms for tools/latest_models.sh (2026-10-09).
# Every arm asserts an observable that would differ if the guard were broken.
# Usage: latest_models_arms.sh [scratch-dir]   (needs network for arm 1 + fixtures)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TOOL="${LM_TOOL:-$PROJECT_DIR/2_Project_Files/tools/latest_models.sh}"
S="${1:-$(mktemp -d /tmp/lm_arms.XXXXXX)}"; mkdir -p "$S"
RUN="$S/run.$$"; mkdir -p "$RUN"          # fresh per invocation: no stale out.json, nothing deleted
DRIVEN=0; PASS=0; FAIL=0
chk() { DRIVEN=$((DRIVEN+1)); if [ "$2" = "1" ]; then PASS=$((PASS+1)); echo "  PASS $1"; else FAIL=$((FAIL+1)); echo "  FAIL $1 -- $3"; fi; }
sha() { shasum -a 256 "$1" 2>/dev/null | cut -c1-16; }
OUTJ="$RUN/out.json"
run() { # run <outfile> <errfile> VAR=val ... ; sets RC
  local o="$1" e="$2"; shift 2
  env LM_NO_API=1 LM_PIN_GLOBS="$RUN/launchers/*.command" LM_OUT="$OUTJ" "$@" "$TOOL" >"$o" 2>"$e"; RC=$?
}
jget() { python3 -I -c "import json,sys;d=json.load(open(sys.argv[1]));print($2)" "$1" 2>&1; }
mkdir -p "$RUN/launchers"
printf '#!/bin/bash\nexec claude --model claude-opus-5 "$P"\n' > "$RUN/launchers/old.command"
printf '#!/bin/bash\n# --model claude-fable-5 (comment only)\nexec claude --model "claude-opus-5-5[1m]" "$P"\n' > "$RUN/launchers/cur.command"
printf '#!/bin/bash\nexec claude --model opus "$P"\n' > "$RUN/launchers/alias.command"
printf '#!/bin/bash\nexec claude "$P"\n' > "$RUN/launchers/none.command"

echo "arm 1: LIVE run (network, docs page; no key)"
run "$RUN/o1" "$RUN/e1"
chk "live rc=0" "$([ $RC = 0 ] && echo 1)" "rc=$RC $(cat "$RUN/e1")"
OPUS="$(jget "$OUTJ" "d['levels']['opus']['model_id']")"
chk "live opus id matches ^claude-opus-N" "$(printf '%s' "$OPUS" | grep -Eq '^claude-opus-[0-9]' && echo 1)" "got: $OPUS"
SON="$(jget "$OUTJ" "d['levels']['sonnet']['model_id']")"
chk "live sonnet id matches ^claude-sonnet-N" "$(printf '%s' "$SON" | grep -Eq '^claude-sonnet-[0-9]' && echo 1)" "got: $SON"
chk "stale_pins = exactly old.command (not cur/alias/none)" "$(jget "$OUTJ" "1 if [x['launcher'].split('/')[-1] for x in d['stale_pins']]==['old.command'] else 0")" "$(jget "$OUTJ" "d['stale_pins']")"
chk "commented pin ignored + [1m] stripped (cur is current)" "$(jget "$OUTJ" "1 if [x['status'] for x in d['pins'] if x['launcher'].endswith('cur.command')]==['current'] else 0")" "pins wrong"
chk "alias pin and no-pin not reported stale" "$(jget "$OUTJ" "1 if not any(x['launcher'].endswith(('alias.command','none.command')) for x in d['stale_pins']) else 0")" "alias/none flagged"

# fixtures derived from the live page
curl -sSL -m 30 https://platform.claude.com/docs/en/models/overview.md -o "$RUN/page.md" || echo "  (page fetch for fixtures failed)"
sed 's/`claude-opus-5-5`/`claude-sonnet-5-5`/' "$RUN/page.md" > "$RUN/noopus.md"     # Opus column now claims a sonnet id: no opus level
sed 's/`claude-opus-5-5`/`opus-5-5`/' "$RUN/page.md" > "$RUN/malformed.md"
cp "$OUTJ" "$RUN/good_prev.json"

echo "arm 2: planted page with NO Opus level -> rc 3, previous kept"
H0="$(sha "$OUTJ")"; run "$RUN/o2" "$RUN/e2" LM_MODELS_URL="file://$RUN/noopus.md"
chk "no-opus rc=3" "$([ $RC = 3 ] && echo 1)" "rc=$RC"
chk "no-opus names the missing level" "$(grep -q "required level 'opus'" "$RUN/e2" && echo 1)" "$(cat "$RUN/e2")"
chk "no-opus previous JSON byte-identical" "$([ "$(sha "$OUTJ")" = "$H0" ] && echo 1)" "changed"

echo "arm 3: malformed id -> refused (rc 4), previous kept"
H0="$(sha "$OUTJ")"; run "$RUN/o3" "$RUN/e3" LM_MODELS_URL="file://$RUN/malformed.md"
chk "malformed rc=4" "$([ $RC = 4 ] && echo 1)" "rc=$RC $(cat "$RUN/e3")"
chk "malformed says REFUSED" "$(grep -q REFUSED "$RUN/e3" && echo 1)" "$(cat "$RUN/e3")"
chk "malformed previous JSON byte-identical" "$([ "$(sha "$OUTJ")" = "$H0" ] && echo 1)" "changed"

echo "arm 4: unreachable source -> rc 3, previous kept, age printed"
H0="$(sha "$OUTJ")"; run "$RUN/o4" "$RUN/e4" LM_MODELS_URL="http://127.0.0.1:9/nope"
chk "unreachable rc=3" "$([ $RC = 3 ] && echo 1)" "rc=$RC"
chk "unreachable prints previous age" "$(grep -Eq 'KEPT \(age [0-9.]+ h\)' "$RUN/e4" && echo 1)" "$(cat "$RUN/e4")"
chk "unreachable previous JSON byte-identical" "$([ "$(sha "$OUTJ")" = "$H0" ] && echo 1)" "changed"
run "$RUN/o4b" "$RUN/e4b" LM_MODELS_URL="http://127.0.0.1:9/nope" LM_OUT="$RUN/never_created.json"
chk "unreachable + no previous: rc=3, says none exists, no file created" "$([ $RC = 3 ] && grep -q 'No previous JSON exists' "$RUN/e4b" && [ ! -e "$RUN/never_created.json" ] && echo 1)" "rc=$RC $(cat "$RUN/e4b")"

echo "arm 5: planted 'older than previous' -> WARN"
python3 -I -c "
import json,sys
d=json.load(open(sys.argv[1])); d['levels']['opus']['model_id']='claude-opus-5-9'
json.dump(d,open(sys.argv[2],'w'))" "$RUN/good_prev.json" "$OUTJ"
run "$RUN/o5" "$RUN/e5" LM_MODELS_URL="file://$RUN/page.md"
chk "regression: rc=0 and WARN REGRESSION opus on stderr" "$([ $RC = 0 ] && grep -q 'WARN REGRESSION opus' "$RUN/e5" && echo 1)" "rc=$RC $(cat "$RUN/e5")"
chk "regression recorded in JSON warnings" "$(jget "$OUTJ" "1 if d['warnings'] else 0")" "no warnings field"
run "$RUN/o5b" "$RUN/e5b" LM_MODELS_URL="file://$RUN/page.md"
chk "no WARN on the next clean run" "$([ $RC = 0 ] && ! grep -q WARN "$RUN/e5b" && echo 1)" "$(cat "$RUN/e5b")"

echo "arm 6: API path (planted response, fake key from env; value must never be printed)"
cat > "$RUN/api.json" <<'JS'
{"data":[{"id":"claude-opus-5","display_name":"Claude Opus 5","created_at":"2026-08-01T00:00:00Z"},
{"id":"claude-opus-5-5","display_name":"Claude Opus 5.5","created_at":"2026-09-22T00:00:00Z"},
{"id":"claude-sonnet-5-5","display_name":"Claude Sonnet 5.5","created_at":"2026-09-28T00:00:00Z"}],"has_more":false,"last_id":"x"}
JS
sed 's/claude-sonnet-5-5/gpt-sonnet/' "$RUN/api.json" > "$RUN/api_bad.json"
run "$RUN/o6" "$RUN/e6" LM_NO_API= ANTHROPIC_API_KEY=sk-fake-arm-key LM_API_URL="file://$RUN/api.json"
chk "api path used, newest per level, created_at kept, no haiku invented" "$(jget "$OUTJ" "1 if d['source']['kind']=='anthropic-models-api' and d['levels']['opus']['model_id']=='claude-opus-5-5' and d['levels']['opus']['released']=='2026-09-22T00:00:00Z' and 'haiku' not in d['levels'] else 0")" "rc=$RC $(cat "$RUN/e6")"
chk "fake key never appears in output/JSON" "$(! grep -q sk-fake-arm-key "$RUN/o6" "$RUN/e6" "$OUTJ" && echo 1)" "key leaked"
run "$RUN/o6b" "$RUN/e6b" LM_NO_API= ANTHROPIC_API_KEY=sk-fake-arm-key LM_API_URL="file://$RUN/api_bad.json"
chk "api malformed id -> rc 4 REFUSED" "$([ $RC = 4 ] && grep -q REFUSED "$RUN/e6b" && echo 1)" "rc=$RC $(cat "$RUN/e6b")"
run "$RUN/o6c" "$RUN/e6c" LM_NO_API= ANTHROPIC_API_KEY=sk-fake-arm-key LM_API_URL="http://127.0.0.1:9/x" LM_MODELS_URL="file://$RUN/page.md"
chk "api down -> loud on stderr, falls back to page, source recorded as page" "$(grep -q 'API path failed' "$RUN/e6c" && jget "$OUTJ" "1 if d['source']['kind']=='docs-models-overview-page' else 0")" "rc=$RC $(cat "$RUN/e6c")"

echo
echo "latest_models arms: driven=$DRIVEN pass=$PASS fail=$FAIL (scratch: $RUN)"
[ "$FAIL" = 0 ] && [ "$DRIVEN" -gt 0 ]
