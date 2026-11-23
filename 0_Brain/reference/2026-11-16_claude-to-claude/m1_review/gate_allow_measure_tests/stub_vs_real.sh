#!/bin/bash
# QA-ALLOW-MEASURE item 3: run the committed stub (from the extracted head) on a synthetic PreToolUse event,
# with the out file exactly as am.sh allow_out writes it, and compare its stdout bytes and exit code with the
# bytes main.rs prints: serde_json Value::to_string of {"hookSpecificOutput":{hookEventName,permissionDecision,
# permissionDecisionReason}} (keys already sorted, so BTreeMap or preserve_order give the same order) + "\n" (writeln!), exit 0.
set -u
STUB="$1"; W="$2"; mkdir -p "$W/hook"
python3 -I - "$W/hook/out.PreToolUse.json" <<'PY'
import json, sys
h = {"hookEventName": "PreToolUse", "permissionDecision": "allow", "permissionDecisionReason": "allowed by the owner"}
open(sys.argv[1], "w").write(json.dumps({"hookSpecificOutput": h}, separators=(",", ":"), ensure_ascii=False) + "\n")
PY
printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","permissionDecisionReason":"allowed by the owner"}}' > "$W/expected.txt"
echo '{"session_id":"x","hook_event_name":"PreToolUse","tool_name":"Write","tool_input":{"file_path":"a","content":"b"}}' | python3 -I "$STUB" "$W/hook" > "$W/stub.out" 2> "$W/stub.err"; echo "stub exit=$?"
cmp "$W/stub.out" "$W/expected.txt" && echo "stdout: byte-identical to the expected real-hook line ($(wc -c < "$W/expected.txt") bytes)"
echo "stderr bytes: $(wc -c < "$W/stub.err")"
# positive control: a one-byte change must be caught
sed 's/owner/0wner/' "$W/expected.txt" > "$W/ctl.txt"; cmp -s "$W/stub.out" "$W/ctl.txt" || echo "control: altered line detected as different"
# committed captures: every hook.out.PreToolUse.json of the plain-allow cases equals the expected line
for f in "$3"/*/hook.out.PreToolUse.json; do c=$(basename "$(dirname "$f")"); if cmp -s "$f" "$W/expected.txt"; then echo "$c: identical"; else echo "$c: DIFFERS (M3 adds fields by design?)"; fi; done
