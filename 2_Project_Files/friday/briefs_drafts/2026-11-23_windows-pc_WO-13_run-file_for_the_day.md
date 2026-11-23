From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 13: rewrite ONE file for the day, run nothing. Thank you for WO-12: the tool loaded and answered exactly as hoped, and you were right to ask the owner first.

WHY. The owner ruled on his board (2026-11-23, 10:24 local): "Decision general-c2c-windows-agent-permission-mode-1123: c — Skip all prompts | note: This is an acceptable risk during development. ..." So the Windows agent of the day runs with the skip-permissions flag, as your rehearsal run did, and not with the allow-list that WO-11 wrote into run-agent.cmd.

RULES: as WO-11. No model run in this order. Change nothing else. Delete nothing: keep the old file under a new name.

DO NOT TOUCH: C:\c2c\m7, C:\c2c\t7, C:\c2c\wo7, C:\wdc7, C:\wdc7q, C:\c2c\wo12, C:\wdc11q and every other folder not named under WHERE.
WHERE. Only C:\c2c\wo11 (two files there). The session's data folder is still NOT created.

STEPS:
1. Rename C:\c2c\wo11\run-agent.cmd to C:\c2c\wo11\run-agent.allowlist-form.cmd.txt (kept, not used).
2. Write a new C:\c2c\wo11\run-agent.cmd, exactly (argument 1 = the model id my GO mail of the day will give):
     @echo off
     cd /d C:\c2c\wo11\ws-g
     claude -p --model %1 --plugin-dir C:\c2c\wo11\plugin-g --dangerously-skip-permissions "Use the coagent send tool, kind request, text exactly: C2W-1 request from the Windows agent: please reply. Then call the coagent wait tool with timeout_s 300, again and again, until you have received BOTH a reply whose re is the id of your message AND a request from the peer. Answer that request with the coagent send tool, kind reply, re set to the request's id, text exactly: C2W-4 reply from the Windows agent. Then print every id and text you sent and received, and the exact name of every tool you called. Use no other tool. Do not read or write any file." > C:\c2c\logs\wo11-agent-day.log 2>&1
     echo exit %ERRORLEVEL% >> C:\c2c\logs\wo11-agent-day.log
3. Do NOT run it. Give me the final text of the new file WHOLE, the SHA256 of both files, and a dir of C:\c2c\wo11 .

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-13 done". Then go back to waiting on your inbox. The day itself comes in its own work order, with the owner at both machines.
