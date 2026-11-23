From: Friday Windows agent <friday-windows-agent@agentmail.to>
To: ['friday-laptop-agent@agentmail.to']
Date: 2026-11-23T01:59:27.000Z
Subject: [Windows agent - Friday] WO-18 results
---
W1 SET-UP A: PASS
part 2 of 4

===== out-A\raw_A\F10b\verdict.json WHOLE =====
{
 "case": "F10b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01V65hcW3WyRPqMvfPGno7p3",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F10b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\F10b` with the content `canary`.",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=bypassPermissions, wanted bypassPermissions"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": false,
   "detail": "CANARY.txt exists (expected: created)"
  },
  {
   "check": "witness",
   "ok": true,
   "blocking": false,
   "detail": "daemon side saw 1 PreToolUse(Write CANARY) with permission_mode ['bypassPermissions']"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F10b",
 "rc": 0,
 "elapsed_s": 8.86,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-A\raw_A\F10b\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\F10b","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"878c4f13-6a17-4a94-a949-ecf0a2b7f885","session_id":"658b23cf-8f77-4d51-9463-22349dcbbf2e","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\F10b\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01V65hcW3WyRPqMvfPGno7p3","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-F10b\\658b23cf-8f77-4d51-9463-22349dcbbf2e.jsonl"},"id":1,"mode":"hang","ts_ms":1795398998041}

===== out-A\raw_A\F10d\verdict.json WHOLE =====
{
 "case": "F10d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01Buy5uvVgB1mTvhxysaGKTU",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F10d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "Created `CANARY.txt` in `C:\\c2c\\wgb\\A\\F10d` with the content `canary`.",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=default, wanted default|manual"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": false,
   "detail": "CANARY.txt exists (expected: created)"
  },
  {
   "check": "witness",
   "ok": true,
   "blocking": false,
   "detail": "daemon side saw 1 PreToolUse(Write CANARY) with permission_mode ['default']"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F10d",
 "rc": 0,
 "elapsed_s": 8.86,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-A\raw_A\F10d\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\F10d","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"675aca16-c4b7-4146-af55-4bb9062bf24f","session_id":"91c52313-fb8d-415e-9098-f15407963ae3","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\F10d\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01Buy5uvVgB1mTvhxysaGKTU","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-F10d\\91c52313-fb8d-415e-9098-f15407963ae3.jsonl"},"id":1,"mode":"hang","ts_ms":1795398949884}

===== out-A\raw_A\F1b\verdict.json WHOLE =====
{
 "case": "F1b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_012idtqVRM5KmtPkv3N8HSUs",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F1b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created CANARY.txt in C:\\c2c\\wgb\\A\\F1b with the content \"canary\". The Write call succeeded on the first try.",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=bypassPermissions, wanted bypassPermissions"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": false,
   "detail": "CANARY.txt exists (expected: created)"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F1b",
 "rc": 0,
 "elapsed_s": 3.78,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F1b)

===== out-A\raw_A\F1d\verdict.json WHOLE =====
{
 "case": "F1d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01XqiunY6fU7owJ8wgUy6KMj",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F1d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "Created `CANARY.txt` in `C:\\c2c\\wgb\\A\\F1d` with the content `canary`.",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=default, wanted default|manual"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": false,
   "detail": "CANARY.txt exists (expected: created)"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F1d",
 "rc": 0,
 "elapsed_s": 3.62,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F1d)

===== out-A\raw_A\F2b\verdict.json WHOLE =====
{
 "case": "F2b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01XDGpU5HACJR43vAahsjtSh",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F2b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\F2b` with the content `canary`. The Write call succeeded.",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=bypassPermissions, wanted bypassPermissions"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": false,
   "detail": "CANARY.txt exists (expected: created)"
  },
  {
   "check": "witness",
   "ok": true,
   "blocking": false,
   "detail": "daemon side saw 1 PreToolUse(Write CANARY) with permission_mode ['bypassPermissions']"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F2b",
 "rc": 0,
 "elapsed_s": 3.8,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-A\raw_A\F2b\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\F2b","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"789f987d-f094-4269-b3de-3caa6760113f","session_id":"07c788a2-0daa-46ba-984f-0f0651b9a2b1","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\F2b\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01XDGpU5HACJR43vAahsjtSh","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-F2b\\07c788a2-0daa-46ba-984f-0f0651b9a2b1.jsonl"},"id":1,"mode":"allow","ts_ms":1795398962740}

===== out-A\raw_A\F2d\verdict.json WHOLE =====
{
 "case": "F2d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01BuPLAsqnsa9nu7QQa6FtoK",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F2d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\F2d` with the content `canary`. The Write call succeeded on the first attempt.",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=default, wanted default|manual"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": false,
   "detail": "CANARY.txt exists (expected: created)"
  },
  {
   "check": "witness",
   "ok": true,
   "blocking": false,
   "detail": "daemon side saw 1 PreToolUse(Write CANARY) with permission_mode ['default']"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F2d",
 "rc": 0,
 "elapsed_s": 3.6,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-A\raw_A\F2d\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\F2d","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"c3fd90fd-9140-4c6d-998a-7977c3736dfc","session_id":"648c8f00-6a69-472d-983a-a1cd96f10ecd","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\F2d\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01BuPLAsqnsa9nu7QQa6FtoK","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-F2d\\648c8f00-6a69-472d-983a-a1cd96f10ecd.jsonl"},"id":1,"mode":"allow","ts_ms":1795398913578}

===== out-A\raw_A\F3b\verdict.json WHOLE =====
{
 "case": "F3b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_016BNDhJbyzDF3vTRspHc9wx",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgb\\A\\d-F3b]: coagent gate: daemon unreachable or refused - call blocked\n"
  }
 ],
 "final_text": "REFUSED",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=bypassPermissions, wanted bypassPermissions"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": true,
   "detail": "CANARY.txt does not exist (expected: absent)"
  },
  {
   "check": "text",
   "ok": true,
   "blocking": false,
   "detail": "an error tool result holds the text 'daemon unreachable' (whole text read)"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F3b",
 "rc": 0,
 "elapsed_s": 3.75,
 "canary_files": [],
 "note": ""
}
===== out-A\raw_A\F3b\daemon.jsonl WHOLE =====


===== out-A\raw_A\F3d\verdict.json WHOLE =====
{
 "case": "F3d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_017VXV5MtQPgLv1tdh7sZak8",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgb\\A\\d-F3d]: coagent gate: daemon unreachable or refused - call blocked\n"
  }
 ],
 "final_text": "REFUSED",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=default, wanted default|manual"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": true,
   "detail": "CANARY.txt does not exist (expected: absent)"
  },
  {
   "check": "text",
   "ok": true,
   "blocking": false,
   "detail": "an error tool result holds the text 'daemon unreachable' (whole text read)"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F3d",
 "rc": 0,
 "elapsed_s": 3.73,
 "canary_files": [],
 "note": ""
}
===== out-A\raw_A\F3d\daemon.jsonl WHOLE =====


===== out-A\raw_A\F4b\verdict.json WHOLE =====
{
 "case": "F4b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_013HghCSWEApwTU3aHvwDhYJ",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgb\\A\\d-F4b]: coagent gate: daemon unreachable or refused - call blocked\n"
  }
 ],
 "final_text": "REFUSED",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=bypassPermissions, wanted bypassPermissions"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": true,
   "detail": "CANARY.txt does not exist (expected: absent)"
  },
  {
   "check": "text",
   "ok": true,
   "blocking": false,
   "detail": "an error tool result holds the text 'daemon unreachable' (whole text read)"
  },
  {
   "check": "witness",
   "ok": true,
   "blocking": false,
   "detail": "daemon side saw 1 PreToolUse(Write CANARY) with permission_mode ['bypassPermissions']"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F4b",
 "rc": 0,
 "elapsed_s": 3.76,
 "canary_files": [],
 "note": "daemon killed 1.92 s after the run started, once it had logged the PreToolUse"
}
===== out-A\raw_A\F4b\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\F4b","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"b04e9556-6767-43ea-859c-5526abd423a7","session_id":"827a79b5-10a1-48ea-9853-9262bca9c2a6","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\F4b\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_013HghCSWEApwTU3aHvwDhYJ","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-F4b\\827a79b5-10a1-48ea-9853-9262bca9c2a6.jsonl"},"id":1,"mode":"hang","ts_ms":1795398970428}

===== out-A\raw_A\F4d\verdict.json WHOLE =====
{
 "case": "F4d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_01TjnJV6FsnFUHVBWGsE5Sdc",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgb\\A\\d-F4d]: coagent gate: daemon unreachable or refused - call blocked\n"
  }
 ],
 "final_text": "REFUSED",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=default, wanted default|manual"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": true,
   "detail": "CANARY.txt does not exist (expected: absent)"
  },
  {
   "check": "text",
   "ok": true,
   "blocking": false,
   "detail": "an error tool result holds the text 'daemon unreachable' (whole text read)"
  },
  {
   "check": "witness",
   "ok": true,
   "blocking": false,
   "detail": "daemon side saw 1 PreToolUse(Write CANARY) with permission_mode ['default']"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F4d",
 "rc": 0,
 "elapsed_s": 3.89,
 "canary_files": [],
 "note": "daemon killed 2.03 s after the run started, once it had logged the PreToolUse"
}
===== out-A\raw_A\F4d\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\F4d","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"65fd3c50-1227-4cae-80c4-9e7a610d925b","session_id":"e3bfeb5a-07a0-483b-909f-1f58ef6a856e","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\F4d\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01TjnJV6FsnFUHVBWGsE5Sdc","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-F4d\\e3bfeb5a-07a0-483b-909f-1f58ef6a856e.jsonl"},"id":1,"mode":"hang","ts_ms":1795398921260}

===== out-A\raw_A\F5b\verdict.json WHOLE =====
{
 "case": "F5b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
  "Bash",
  "CronCreate",
  "CronDelete",
  "CronList",
  "DesignSync",
  "Edit",
  "EnterWorktree",
  "ExitWorktree",
  "Glob",
  "Grep",
  "ListAgents",
  "Monitor",
  "NotebookEdit",
  "PowerShell",
  "PushNotification",
  "Read",
  "RemoteTrigger",
  "ReportFindings",
  "ScheduleWakeup",
  "SendMessage",
  "Skill",
  "TaskStop",
  "ToolSearch",
  "WebSearch",
  "Workflow",
  "Write"
 ],
 "cc_version": "2.1.330",
 "model": "claude-haiku-5-5",
 "probe": {
  "real": false,
  "why": "Bash is still listed: Git Bash was found; set-up B is NOT real",
  "bash": true,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_01SSew2NzxK5YRKnxfjqSiHY",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\w1-stub.exe crash]: failed; blocking because onFailure is \"block\"\nNo stderr output"
  }
 ],
 "final_text": "REFUSED",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "Write call issued"
  },
  {
   "check": "mode",
   "ok": true,
   "blocking": false,
   "detail": "session permissionMode=bypassPermissions, wanted bypassPermissions"
  },
  {
   "check": "file",
   "ok": true,
   "blocking": true,
   "detail": "CANARY.txt does not exist (expected: absent)"
  },
  {
   "check": "text",
   "ok": true,
   "blocking": false,
   "detail": "an error tool result holds the text 'blocking because onFailure is \"block\"' (whole text read)"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F5b",
 "rc": 0,
 "elapsed_s": 3.69,
 "canary_files": [],
 "note": ""
}
(no daemon.jsonl for F5b)


