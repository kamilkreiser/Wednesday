#!/bin/bash
# resume_qa_nexusai_rd293_599058b.sh — RESUME the RD-293 tier-2 gate session in a tmux pane.
# WHY: the headless run (launch_qa_nexusai_rd293_599058b.sh via nohup) EXITED at 08:03 when its turn ended
# while waiting on a backgrounded `npm run verify` ("I'll carry on when verify's completion notice arrives").
# A headless process has no next turn, so the wait was a death. Its report is written except the suite line,
# end head readings, cleanup and the verdict mail. Resuming keeps its context instead of re-deriving it.
# Identity: NexusAI's own az/gh dirs (trap 8a). Config dir: Tuesday's project-local .claude, where the session lives.
set -u
QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
SESSION='63a3bcc8-04b8-4493-9e97-e152fdba6959'
export CLAUDE_CONFIG_DIR='/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.claude'
export AZURE_CONFIG_DIR='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials/.azure'
export GH_CONFIG_DIR='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'
[ -f "$CLAUDE_CONFIG_DIR/projects/-Volumes-KK-T9-External-HDD--CODING-Testing-Agent-MAIN/$SESSION.jsonl" ] || { echo "session transcript missing" >&2; exit 2; }
[ -d "$AZURE_CONFIG_DIR" ] && [ -d "$GH_CONFIG_DIR" ] || { echo "NexusAI identity dirs missing" >&2; exit 3; }
PROMPT='ultrathink. Tuesday here (coordinator). Your headless process EXITED at 08:03 AEST while you were waiting on a backgrounded `npm run verify`: a headless run has no next turn, so that wait ended the session. Nothing of yours is still running (no jest process remains; /tmp/qa-rd293-vUKvr1 is still on disk). You are now resumed in a tmux pane. Finish the gate: (1) re-run `npm run verify` in your head clone IN THE FOREGROUND with a long timeout and read its VERDICT line; (2) run the base and head name-diff runs; (3) take the END head readings; (4) fill every {{...}} placeholder in your report; (5) clean up only what you created; (6) MAIL YOUR VERDICT to tuesday-agent@agentmail.to exactly as the brief specifies. From here on, never end a turn waiting on a background notice: run long commands in the foreground.'
cd "$QA_DIR" || exit 4
exec claude --resume "$SESSION" --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
