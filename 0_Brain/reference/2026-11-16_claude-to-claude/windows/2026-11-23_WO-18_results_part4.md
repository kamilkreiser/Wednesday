From: Friday Windows agent <friday-windows-agent@agentmail.to>
To: ['friday-laptop-agent@agentmail.to']
Date: 2026-11-23T01:59:30.000Z
Subject: [Windows agent - Friday] WO-18 results
---
W1 SET-UP A: PASS
part 4 of 4

===== out-A\raw_A\P3\verdict.json WHOLE =====
{
 "case": "P3",
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
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_01A6WjAzQH9nPpz2EiFpDM4M",
   "is_error": true,
   "text": "PreToolUse:PowerShell hook error: coagent W1 stub daemon says deny"
  }
 ],
 "final_text": "REFUSED",
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
   "blocking": true,
   "detail": "CANARY.txt does not exist (expected: absent)"
  },
  {
   "check": "text",
   "ok": true,
   "blocking": false,
   "detail": "an error tool result holds the text 'stub daemon says deny' (whole text read)"
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
 "tag": "P3",
 "rc": 0,
 "elapsed_s": 4.85,
 "canary_files": [],
 "note": ""
}
===== out-A\raw_A\P3\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\P3","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"4848a50d-9eef-4119-946e-e99ec76fa930","session_id":"34f666ff-9bb4-44f2-89db-3b95f1ce8601","tool_input":{"command":"Set-Content -Path CANARY.txt -Value canary","description":"Write canary value to CANARY.txt in current directory"},"tool_name":"PowerShell","tool_use_id":"toolu_01A6WjAzQH9nPpz2EiFpDM4M","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-P3\\34f666ff-9bb4-44f2-89db-3b95f1ce8601.jsonl"},"id":1,"mode":"deny","ts_ms":1795398892022}

===== out-A\raw_A\P4\verdict.json WHOLE =====
{
 "case": "P4",
 "tool": "PowerShell",
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
   "id": "toolu_01F8hNVidPe5CWjAv4rq66Xj",
   "is_error": false,
   "text": "(PowerShell completed with no output)"
  }
 ],
 "final_text": "Done. The PowerShell command completed with no output, so `CANARY.txt` should now exist in `C:\\c2c\\wgb\\A\\P4` containing `canary`. I did not verify the file afterward, since you asked for only one tool call.",
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
 "tag": "P4",
 "rc": 0,
 "elapsed_s": 4.87,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for P4)

===== out-A\raw_A\P5\verdict.json WHOLE =====
{
 "case": "P5",
 "tool": "PowerShell",
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
   "id": "toolu_0166DixUKFzrBJJ2JtUv2vkG",
   "is_error": false,
   "text": "(PowerShell completed with no output)"
  }
 ],
 "final_text": "I ran the PowerShell command once: `Set-Content -Path CANARY.txt -Value canary` in `C:\\c2c\\wgb\\A\\P5`. It finished with no output and no error. I didn't check the file afterward, so it's not verified that `CANARY.txt` now exists with that content.",
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
   "detail": "daemon side saw 1 PreToolUse(PowerShell CANARY) with permission_mode ['bypassPermissions']"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "P5",
 "rc": 0,
 "elapsed_s": 4.85,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-A\raw_A\P5\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\P5","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"0a0f0fcf-16ef-4447-8aef-95a2016eba2e","session_id":"f0feec1f-9ce6-4a24-9fb5-164c2fdbca2f","tool_input":{"command":"Set-Content -Path CANARY.txt -Value canary","description":"Create CANARY.txt with value canary"},"tool_name":"PowerShell","tool_use_id":"toolu_0166DixUKFzrBJJ2JtUv2vkG","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-P5\\f0feec1f-9ce6-4a24-9fb5-164c2fdbca2f.jsonl"},"id":1,"mode":"allow","ts_ms":1795398901001}

===== out-A\raw_A\P6\verdict.json WHOLE =====
{
 "case": "P6",
 "tool": "PowerShell",
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
   "id": "toolu_01SnE6rhxY7s951QhuLFMBdx",
   "is_error": true,
   "text": "PreToolUse:PowerShell hook error: coagent W1 stub daemon says deny"
  }
 ],
 "final_text": "REFUSED",
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
   "detail": "an error tool result holds the text 'stub daemon says deny' (whole text read)"
  },
  {
   "check": "witness",
   "ok": true,
   "blocking": false,
   "detail": "daemon side saw 1 PreToolUse(PowerShell CANARY) with permission_mode ['bypassPermissions']"
  }
 ],
 "verdict": "PASS",
 "blocking_failure": false,
 "attempt": 0,
 "tag": "P6",
 "rc": 0,
 "elapsed_s": 3.87,
 "canary_files": [],
 "note": ""
}
===== out-A\raw_A\P6\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\P6","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"870534c9-bba8-4748-b2b1-2a500afe9745","session_id":"ad823f79-2c50-43e8-90fa-dabce78fd50f","tool_input":{"command":"Set-Content -Path CANARY.txt -Value canary","description":"Write canary value to CANARY.txt in current directory"},"tool_name":"PowerShell","tool_use_id":"toolu_01SnE6rhxY7s951QhuLFMBdx","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-P6\\ad823f79-2c50-43e8-90fa-dabce78fd50f.jsonl"},"id":1,"mode":"deny","ts_ms":1795398906001}

===== out-A\raw_A\W1\verdict.json WHOLE =====
{
 "case": "W1",
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
   "id": "toolu_01KvpuuM8NfBnJ67tFjs3Q6A",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\W1\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\W1` with the content `canary`.",
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
 "tag": "W1",
 "rc": 0,
 "elapsed_s": 4.01,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for W1)

===== out-A\raw_A\W2\verdict.json WHOLE =====
{
 "case": "W2",
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
   "id": "toolu_01KW4s1WJ9xmRa4JAJzyNLjn",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\W2\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\W2` with the content `canary`.",
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
 "tag": "W2",
 "rc": 0,
 "elapsed_s": 3.63,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-A\raw_A\W2\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\W2","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"07ad6d49-d603-4c5c-9e16-338479b3993e","session_id":"f25c5450-9738-4a7f-a25c-d3565d1e76dd","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\W2\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01KW4s1WJ9xmRa4JAJzyNLjn","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-W2\\f25c5450-9738-4a7f-a25c-d3565d1e76dd.jsonl"},"id":1,"mode":"allow","ts_ms":1795398858647}

===== out-A\raw_A\W3\verdict.json WHOLE =====
{
 "case": "W3",
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
   "id": "toolu_017UxxZ2f7GVfvNXoihbou1G",
   "is_error": true,
   "text": "PreToolUse:Write hook error: coagent W1 stub daemon says deny"
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
   "detail": "an error tool result holds the text 'stub daemon says deny' (whole text read)"
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
 "tag": "W3",
 "rc": 0,
 "elapsed_s": 3.9,
 "canary_files": [],
 "note": ""
}
===== out-A\raw_A\W3\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\W3","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"78b65a74-e82e-45cc-8f75-748d7cc08491","session_id":"342ca159-dc2f-443a-b7a8-b8e5f0a7f1d2","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\W3\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_017UxxZ2f7GVfvNXoihbou1G","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-W3\\342ca159-dc2f-443a-b7a8-b8e5f0a7f1d2.jsonl"},"id":1,"mode":"deny","ts_ms":1795398862421}

===== out-A\raw_A\W4\verdict.json WHOLE =====
{
 "case": "W4",
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
   "id": "toolu_01DSzZVqSTkqaNRy4Fo5JuGN",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\W4\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\W4` with the content `canary`. The Write call succeeded, so there was no refusal.",
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
 "tag": "W4",
 "rc": 0,
 "elapsed_s": 3.67,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for W4)

===== out-A\raw_A\W5\verdict.json WHOLE =====
{
 "case": "W5",
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
   "id": "toolu_01ERAnzQPwsHQVZhBxmTxkAa",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgb\\A\\W5\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgb\\A\\W5` with the content `canary`.",
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
 "tag": "W5",
 "rc": 0,
 "elapsed_s": 3.6,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-A\raw_A\W5\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\W5","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"fa764a29-71a3-46bf-95d9-9d9e5ca524e6","session_id":"567af057-9884-45ca-8c96-c73f7d004507","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\W5\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01ERAnzQPwsHQVZhBxmTxkAa","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-W5\\567af057-9884-45ca-8c96-c73f7d004507.jsonl"},"id":1,"mode":"allow","ts_ms":1795398870087}

===== out-A\raw_A\W6\verdict.json WHOLE =====
{
 "case": "W6",
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
   "id": "toolu_011J74snRb4ddWko1NRSXDbD",
   "is_error": true,
   "text": "PreToolUse:Write hook error: coagent W1 stub daemon says deny"
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
   "detail": "an error tool result holds the text 'stub daemon says deny' (whole text read)"
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
 "tag": "W6",
 "rc": 0,
 "elapsed_s": 4.68,
 "canary_files": [],
 "note": ""
}
===== out-A\raw_A\W6\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgb\\A\\W6","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"c4a676ae-0d5d-4b0b-811b-cbfc124f96d3","session_id":"564eff6b-1e1c-4cce-b3e7-584586e97e62","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgb\\A\\W6\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_011J74snRb4ddWko1NRSXDbD","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgb-A-W6\\564eff6b-1e1c-4cce-b3e7-584586e97e62.jsonl"},"id":1,"mode":"deny","ts_ms":1795398874628}


