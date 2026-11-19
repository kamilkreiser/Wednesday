. /private/tmp/claude-501/qp1/p/lib.sh
mkdir -p $W/p/w7
D=$W/p/x7
startd $D --gate --workspace $W/p/w7 || echo startfail
t() { echo "== $1"; }
t "empty stdin"; printf '' | hk $D | san
t "non-UTF-8 stdin"; printf '\xff\xfe\x80{}' | hk $D | san
t "JSON with invalid UTF-8 inside a string"; printf '{"hook_event_name":"PreToolUse","tool_name":"\xff"}' | hk $D | san
t "stdin = []"; printf '[]' | hk $D | san
t "stdin = null"; printf 'null' | hk $D | san
t "stdin = \"x\""; printf '"x"' | hk $D | san
t "stdin = {}"; printf '{}' | hk $D | san
python3 -I -c 'import sys; sys.stdout.write("{\"hook_event_name\":\"PreToolUse\",\"session_id\":\"s\",\"tool_name\":\"Write\",\"tool_input\":" + "["*200 + "]"*200 + "}")' > $W/p/tmp/deep200.json
python3 -I -c 'import sys; sys.stdout.write("{\"hook_event_name\":\"PreToolUse\",\"session_id\":\"s\",\"tool_name\":\"Write\",\"tool_input\":" + "["*120 + "]"*120 + "}")' > $W/p/tmp/deep120.json
t "nesting 200"; hk $D < $W/p/tmp/deep200.json | san
t "nesting 120"; hk $D < $W/p/tmp/deep120.json | san
t "PreToolUse renamed PostToolUse"; ev s1 $W/p/w7 default Write "{\"file_path\":\"$W/p/w7/a\",\"content\":\"x\"}" PostToolUse | hk $D | san
t "UserPromptSubmit"; ev s1 $W/p/w7 default Write '{}' UserPromptSubmit | hk $D | san
t "lowercase pretooluse"; ev s1 $W/p/w7 default Write '{}' pretooluse | hk $D | san
t "missing hook_event_name"; printf '{"session_id":"s","tool_name":"Read","tool_input":{}}' | hk $D | san
t "PreToolUse missing session_id"; printf '{"hook_event_name":"PreToolUse","tool_name":"Read","tool_input":{"file_path":"/etc/hosts"},"cwd":"/","permission_mode":"default"}' | hk $D | san
t "dup key ConfigChange then PreToolUse"; printf '{"hook_event_name":"ConfigChange","hook_event_name":"PreToolUse","session_id":"s","cwd":"/","tool_name":"Read","tool_input":{"file_path":"/etc/hosts"},"permission_mode":"default","transcript_path":"/t"}' | hk $D | san
t "dup key PreToolUse then ConfigChange"; printf '{"hook_event_name":"PreToolUse","hook_event_name":"ConfigChange","session_id":"s","cwd":"/","source":"project_settings"}' | hk $D | san
# huge stdin > 1 MiB, PreToolUse and ConfigChange
python3 -I -c 'import sys; sys.stdout.write("{\"hook_event_name\":\"PreToolUse\",\"session_id\":\"s\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"/x\",\"content\":\"" + "a"*(1100*1024) + "\"}}")' > $W/p/tmp/big1m.json
python3 -I -c 'import sys; sys.stdout.write("{\"hook_event_name\":\"ConfigChange\",\"session_id\":\"s\",\"source\":\"project_settings\",\"file_path\":\"/x/" + "a"*(200*1024) + "\"}")' > $W/p/tmp/cc200k.json
python3 -I -c 'import sys; sys.stdout.write("{\"hook_event_name\":\"ConfigChange\",\"session_id\":\"s\",\"source\":\"project_settings\",\"file_path\":\"/x/" + "a"*(1100*1024) + "\"}")' > $W/p/tmp/cc1m.json
python3 -I -c 'import sys; sys.stdout.write("{\"hook_event_name\":\"PreToolUse\",\"session_id\":\"s\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"/x\",\"content\":\"" + "a"*(200*1024) + "\"}}")' > $W/p/tmp/big200k.json
t "PreToolUse 1.1 MiB"; hk $D < $W/p/tmp/big1m.json | san
t "PreToolUse 200 KiB"; hk $D < $W/p/tmp/big200k.json | san
t "ConfigChange 200 KiB"; hk $D < $W/p/tmp/cc200k.json | san
t "ConfigChange 1.1 MiB"; hk $D < $W/p/tmp/cc1m.json | san
t "args: none"; printf '{}' | "${RUNENV[@]}" $B/coagent-hook >/dev/null 2>&1; echo rc=$?
t "args: extra"; printf '{}' | "${RUNENV[@]}" $B/coagent-hook --data-dir $D --x >/dev/null 2>&1; echo rc=$?
t "data-dir socket path too long"; L=$W/p/$(printf 'L%.0s' $(seq 1 90)); ev s1 $W/p/w7 default Read '{}' | hk $L | san
t "socket is a regular file"; mkdir -p $W/p/rf/ipc; : > $W/p/rf/ipc/daemon.sock; ev s1 $W/p/w7 default Read '{}' | hk $W/p/rf | san
for m in garbage noline close slow11 huge wrongdec allow_nohalt okfalse_unknown ok_string partial wrongid reason_num; do
  python3 -I $W/p/stub.py $W/p/st_$m/ipc/daemon.sock $m & SP=$!; sleep 0.5
  t "stub $m (PreToolUse)"; s0=$(date +%s); ev s1 $W/p/w7 default Read '{}' | hk $W/p/st_$m | san | cut -c1-300; echo "elapsed=$(( $(date +%s)-s0 ))s"
  kill $SP; wait $SP 2>/dev/null
done
stopd $D
