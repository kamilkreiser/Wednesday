#!/bin/bash
# QA-ALLOW-MEASURE item 4: my own rig. usage: qa_repro.sh <hook|ctl>
# One interactive Claude Code session, --permission-mode default, own tmux server (-L qam-<random>), hook ONLY via --settings.
# Evidence: frames.txt (visible screen every ~0.1 s when changed), pane.bytes (EVERY byte the pane received, via pipe-pane,
# so a dialog shorter than a frame still leaves its text), keys.log, debug.log, hook stdin. Dialog: held 3 s, then Escape.
set -u
KIND="$1"; Q=/private/tmp/claude-501/qam; RIG=$Q/rig; COUNT=$Q/model_runs.log; touch "$COUNT"
n=$(grep -c . "$COUNT"); [ "$n" -ge 4 ] && { echo "QA RIG REFUSED: run $((n+1)) exceeds 4"; exit 99; }
MODEL=$(python3 -I -c 'import json,sys;print(json.load(open(sys.argv[1]))["levels"]["haiku"]["model_id"])' /Volumes/Laptop-DEV/FRIDAY/0_Brain/dashboard/data/models_latest.json)
[ -n "$MODEL" ] || { echo "no model id"; exit 90; }
D=$Q/run-$KIND; [ -e "$D" ] && { echo "exists: $D"; exit 98; }; mkdir -p "$D/cwd" "$D/hook"
if [ "$KIND" = hook ]; then
  python3 -I -c 'import json,sys; json.dump({"hooks":{"PreToolUse":[{"matcher":"*","hooks":[{"type":"command","command":"/bin/sh %s %s"%(sys.argv[1],sys.argv[2]),"timeout":30,"onFailure":"block"}]}]}},open(sys.argv[3],"w"),indent=1)' "$RIG/hook_allow.sh" "$D/hook" "$D/settings.json"
else echo '{}' > "$D/settings.json"; fi
TS="qam-$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 6)"; echo "$TS" > "$D/tmux.name"; TM=(tmux -L "$TS")
shasum -a 256 "$CLAUDE_CONFIG_DIR/settings.json" "$HOME/.claude/settings.json" | awk '{print $1}' > "$D/checksums.before"
echo "$(date '+%Y-%m-%dT%H:%M:%S%z') run=$((n+1)) kind=$KIND model=$MODEL claude=$(claude --version | cut -d' ' -f1) tmux=$TS" >> "$COUNT"
UNSET=(CLAUDECODE CLAUDE_CODE_CHILD_SESSION CLAUDE_CODE_CHILD_NOTES_DIR CLAUDE_CODE_ENTRYPOINT CLAUDE_CODE_EXECPATH CLAUDE_CODE_MESSAGING_SOCKET CLAUDE_CODE_MESSAGING_TOKEN CLAUDE_CODE_SESSION_ATTENDED CLAUDE_CODE_SESSION_ID CLAUDE_EFFORT CLAUDE_PID TMUX TMUX_PANE)
ENVC=(env); for v in "${UNSET[@]}"; do ENVC+=(-u "$v"); done
CMD="cd $(printf %q "$D/cwd") && $(printf '%q ' "${ENVC[@]}") claude --model $MODEL --permission-mode default --strict-mcp-config --no-chrome --debug-file $(printf %q "$D/debug.log") --settings $(printf %q "$D/settings.json"); echo CLAUDE_EXITED; sleep 300"
echo "$CMD" > "$D/command.txt"
"${ENVC[@]}" tmux -L "$TS" new-session -d -s q -x 160 -y 50 "$CMD"
"${TM[@]}" pipe-pane -t q -o "cat >> $(printf %q "$D/pane.bytes")"
cap(){ "${TM[@]}" capture-pane -t q -p 2>/dev/null; }
( last=""; while "${TM[@]}" has-session -t q 2>/dev/null; do f="$(cap)"; h=$(printf '%s' "$f" | shasum | cut -c1-10); if [ "$h" != "$last" ]; then printf '=== FRAME t=%s\n%s\n' "$(python3 -c 'import time;print(round(time.time(),2))')" "$f" >> "$D/frames.txt"; last=$h; fi; sleep 0.1; done ) & SP=$!
DRE='Do you want to|Yes, and|No, and tell|Allow once|Esc to cancel|❯ 1\. Yes'
key(){ "${TM[@]}" send-keys -t q "$@"; echo "$(date +%s.%N | cut -c1-14) KEY $*" >> "$D/keys.log"; }
say(){ "${TM[@]}" send-keys -t q -l "$1"; sleep 0.5; "${TM[@]}" send-keys -t q Enter; echo "$(date +%s.%N | cut -c1-14) SAY $1" >> "$D/keys.log"; }
waitfor(){ local i=0; while [ $i -lt $(( $2 * 10 )) ]; do cap | grep -Eq "$1" && return 0; sleep 0.1; i=$((i+1)); done; return 1; }
# startup: a trust dialog is answered (the only key allowed before the prompts); then wait for the input box
if waitfor 'trust this folder|Do you trust|Yes, I trust' 25; then cap > "$D/trust.txt"
  # select "Yes, I trust this folder" explicitly: move down until the pointer line holds it (VOID run 1: Enter on the default "No, exit" quit)
  for _k in 1 2 3; do cap | grep -E '❯' | grep -q 'Yes, I trust' && break; key Down; sleep 0.4; done
  cap | grep -E '❯' | grep -q 'Yes, I trust' || { echo "trust pointer not on Yes; aborting before any prompt" | tee -a "$D/result.txt"; "${TM[@]}" kill-server; exit 97; }
  key Enter; echo "trust dialog answered Yes" | tee -a "$D/result.txt"; sleep 1; fi
waitfor 'for shortcuts|manual mode|auto mode' 40; sleep 3; cap | tail -4 > "$D/startup-footer.txt"
step(){ local tag=$1 p=$2 f="$D/cwd/$3" t0 i=0 dlg=none made=none
  say "$p"; t0=$(date +%s)
  while [ $i -lt 900 ]; do
    if [ "$dlg" = none ] && cap | grep -Eq "$DRE"; then dlg=$(( $(date +%s)-t0 )); sleep 3; cap > "$D/dialog.$tag.txt"; key Escape; fi
    [ "$made" = none ] && [ -e "$f" ] && made=$(( $(date +%s)-t0 ))
    if [ "$made" != none ] || [ "$dlg" != none ]; then sleep 8; break; fi
    sleep 0.1; i=$((i+1)); done
  echo "STEP $tag dialog_at_s=$dlg file=$([ -e "$f" ] && echo yes || echo no) file_at_s=$made" | tee -a "$D/result.txt"; }
step W 'Use the Write tool to create the file QW.txt in the current directory containing the single word: qa-write. Use no other tool. If refused, do not retry; say REFUSED.' QW.txt
step B 'Use the Bash tool to run exactly this one command and nothing else: echo QA-BASH-RAN > QB.txt   If refused, do not retry; say REFUSED.' QB.txt
"${TM[@]}" capture-pane -t q -p -S -3000 > "$D/pane.txt"
"${TM[@]}" kill-server 2>/dev/null; wait $SP 2>/dev/null
[ -e "/private/tmp/tmux-$(id -u)/$TS" ] && mv "/private/tmp/tmux-$(id -u)/$TS" "$D/stale-tmux-socket"   # never delete: my own stale socket moves into my work dir
"${TM[@]}" list-sessions >/dev/null 2>&1 && echo "SERVER STILL UP" || echo "tmux server $TS gone"
shasum -a 256 "$CLAUDE_CONFIG_DIR/settings.json" "$HOME/.claude/settings.json" | awk '{print $1}' > "$D/checksums.after"
cmp -s "$D/checksums.before" "$D/checksums.after" && echo "settings checksums identical" || echo "SETTINGS CHANGED"
ls "$D/cwd"
