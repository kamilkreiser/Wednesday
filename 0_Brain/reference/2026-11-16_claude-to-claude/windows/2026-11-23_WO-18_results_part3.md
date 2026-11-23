From: Friday Windows agent <friday-windows-agent@agentmail.to>
To: ['friday-laptop-agent@agentmail.to']
Date: 2026-11-23T01:59:28.000Z
Subject: [Windows agent - Friday] WO-18 results
---
W1 SET-UP A: PASS
part 3 of 4

===== out-A\raw_A\F5d\verdict.json WHOLE =====
{
 "case": "F5d",
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
   "id": "toolu_01Em7paqVMJrXaVRNxYJpaSm",
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
   "detail": "an error tool result holds the text 'blocking because onFailure is \"block\"' (whole text read)"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F5d",
 "rc": 0,
 "elapsed_s": 4.24,
 "canary_files": [],
 "note": ""
}
(no daemon.jsonl for F5d)

===== out-A\raw_A\F6b\verdict.json WHOLE =====
{
 "case": "F6b",
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
   "id": "toolu_01XrHh8fzDnsmdL8tenEf1Bt",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F6b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\F6b` with the content `canary`. The Write call succeeded.",
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
 "tag": "F6b",
 "rc": 0,
 "elapsed_s": 3.79,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F6b)

===== out-A\raw_A\F6d\verdict.json WHOLE =====
{
 "case": "F6d",
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
   "id": "toolu_01Df7iHcEdqUEt6mawankUBj",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F6d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\F6d` with the content `canary`. The Write call succeeded on the first try.",
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
 "tag": "F6d",
 "rc": 0,
 "elapsed_s": 3.89,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F6d)

===== out-A\raw_A\F7b\verdict.json WHOLE =====
{
 "case": "F7b",
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
   "id": "toolu_01WByiB9b3KTCfqheGRNbDbw",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\no-such-coagent-hook.exe --data-dir C:\\c2c\\wgb\\A\\d-F7b]: failed; blocking because onFailure is \"block\"\nError occurred while executing hook command: ENOENT: no such file or directory, uv_spawn 'C:\\c2c\\tga\\debug\\no-such-coagent-hook.exe'"
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
 "tag": "F7b",
 "rc": 0,
 "elapsed_s": 3.68,
 "canary_files": [],
 "note": ""
}
(no daemon.jsonl for F7b)

===== out-A\raw_A\F7d\verdict.json WHOLE =====
{
 "case": "F7d",
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
   "id": "toolu_014SaxWoxRoxaiB6JHrDBbnn",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\no-such-coagent-hook.exe --data-dir C:\\c2c\\wgb\\A\\d-F7d]: failed; blocking because onFailure is \"block\"\nError occurred while executing hook command: ENOENT: no such file or directory, uv_spawn 'C:\\c2c\\tga\\debug\\no-such-coagent-hook.exe'"
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
   "detail": "an error tool result holds the text 'blocking because onFailure is \"block\"' (whole text read)"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "F7d",
 "rc": 0,
 "elapsed_s": 3.8,
 "canary_files": [],
 "note": ""
}
(no daemon.jsonl for F7d)

===== out-A\raw_A\F8b\verdict.json WHOLE =====
{
 "case": "F8b",
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
   "id": "toolu_01SimjGnGC57FJqoBaaaeToZ",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F8b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "Created `CANARY.txt` in `C:\\c2c\\wgb\\A\\F8b` with the content `canary`.",
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
 "tag": "F8b",
 "rc": 0,
 "elapsed_s": 3.6,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F8b)

===== out-A\raw_A\F8d\verdict.json WHOLE =====
{
 "case": "F8d",
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
   "id": "toolu_01AAbBfQ9rCJZFo7y6UsSVYD",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\F8d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\F8d` with the content `canary`. The Write call succeeded on the first try.",
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
 "tag": "F8d",
 "rc": 0,
 "elapsed_s": 3.75,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F8d)

===== out-A\raw_A\F9b\verdict.json WHOLE =====
{
 "case": "F9b",
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
   "id": "toolu_01V9MD6XiS2U5wpuCvi5HVwy",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgb\\A\\d-F9b]: timed out; blocking because onFailure is \"block\""
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
   "detail": "an error tool result holds the text 'onFailure is \"block\"' (whole text read)"
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
 "tag": "F9b",
 "rc": 0,
 "elapsed_s": 8.86,
 "canary_files": [],
 "note": ""
}
===== out-A\raw_A\F9b\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\F9b","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"edac5771-a107-4087-a50a-bcb8f3f2ef6d","session_id":"e64d3c62-2e3a-48a2-92a3-616d43f00d0c","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\F9b\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01V9MD6XiS2U5wpuCvi5HVwy","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-F9b\\e64d3c62-2e3a-48a2-92a3-616d43f00d0c.jsonl"},"id":1,"mode":"hang","ts_ms":1795398989079}

===== out-A\raw_A\F9d\verdict.json WHOLE =====
{
 "case": "F9d",
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
   "id": "toolu_019ameaNH7UwKWVPbvijSido",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgb\\A\\d-F9d]: timed out; blocking because onFailure is \"block\""
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
   "detail": "an error tool result holds the text 'onFailure is \"block\"' (whole text read)"
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
 "tag": "F9d",
 "rc": 0,
 "elapsed_s": 8.84,
 "canary_files": [],
 "note": ""
}
===== out-A\raw_A\F9d\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\F9d","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"e04ebe4b-73b2-413f-bcdc-44de0323cb13","session_id":"3aa2334a-1283-47a2-ac8c-fe4500e0b9b4","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\F9d\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_019ameaNH7UwKWVPbvijSido","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-F9d\\3aa2334a-1283-47a2-ac8c-fe4500e0b9b4.jsonl"},"id":1,"mode":"hang","ts_ms":1795398940908}

===== out-A\raw_A\P1\verdict.json WHOLE =====
{
 "case": "P1",
 "tool": "PowerShell",
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
   "id": "toolu_01XseMY1gqKy3ntrr52k34Ma",
   "is_error": false,
   "text": "(PowerShell completed with no output)"
  }
 ],
 "final_text": "The command ran and finished without error. `Set-Content` prints nothing on success, so there was no output to show. I did not check that `CANARY.txt` exists, because you limited me to one PowerShell call and no other tools.",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "PowerShell call issued"
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
 "tag": "P1",
 "rc": 0,
 "elapsed_s": 6.37,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for P1)

===== out-A\raw_A\P2\verdict.json WHOLE =====
{
 "case": "P2",
 "tool": "PowerShell",
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
   "id": "toolu_01Qxfx1zGYdMq82oEKAXTPNT",
   "is_error": false,
   "text": "(PowerShell completed with no output)"
  }
 ],
 "final_text": "The command ran once and completed without errors, so I've written `canary` to `CANARY.txt` in `C:\\c2c\\wgb\\A\\P2`. I did not use any other tool.",
 "checks": [
  {
   "check": "called",
   "ok": true,
   "blocking": false,
   "detail": "PowerShell call issued"
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
   "detail": "daemon side saw 1 PreToolUse(PowerShell CANARY) with permission_mode ['default']"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "P2",
 "rc": 0,
 "elapsed_s": 5.99,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-A\raw_A\P2\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\P2","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"5143cecd-a950-4522-8e7a-a45a5976c834","session_id":"e4a2fa37-24c8-49b7-8151-e19b72e88ac9","tool_input":{"command":"Set-Content -Path CANARY.txt -Value canary","description":"Write canary value to CANARY.txt in current directory"},"tool_name":"PowerShell","tool_use_id":"toolu_01Qxfx1zGYdMq82oEKAXTPNT","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-P2\\e4a2fa37-24c8-49b7-8151-e19b72e88ac9.jsonl"},"id":1,"mode":"allow","ts_ms":1795398884973}


