W1 SET-UP B: PASS   |   PROBE tools: Bash=False PowerShell=True -> no Bash and no Monitor tool, and a PowerShell tool listed
part 3 of 4

===== out-B\raw_B\F5d\verdict.json WHOLE =====
{
 "case": "F5d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_01WhRM1yVi2v9bSME54fJcDM",
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
 "elapsed_s": 3.66,
 "canary_files": [],
 "note": ""
}
(no daemon.jsonl for F5d)

===== out-B\raw_B\F6b\verdict.json WHOLE =====
{
 "case": "F6b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01JN5gStoJzN6a3ukNMy2aNz",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F6b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F6b` with the content `canary`. The Write call succeeded, so nothing was refused.",
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
 "elapsed_s": 3.67,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F6b)

===== out-B\raw_B\F6d\verdict.json WHOLE =====
{
 "case": "F6d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01J1hokYhcesGxCJqPWTy9jn",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F6d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F6d` with the content `canary`. The Write call succeeded, so nothing was refused.",
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
 "elapsed_s": 4.43,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F6d)

===== out-B\raw_B\F7b\verdict.json WHOLE =====
{
 "case": "F7b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_01FzGs8iHbpzHbifdEx5CLRs",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\no-such-coagent-hook.exe --data-dir C:\\c2c\\wgc2\\B\\d-F7b]: failed; blocking because onFailure is \"block\"\nError occurred while executing hook command: ENOENT: no such file or directory, uv_spawn 'C:\\c2c\\tga\\debug\\no-such-coagent-hook.exe'"
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
 "elapsed_s": 3.65,
 "canary_files": [],
 "note": ""
}
(no daemon.jsonl for F7b)

===== out-B\raw_B\F7d\verdict.json WHOLE =====
{
 "case": "F7d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_018Qq2RVVuQtLJvds2xwcjNW",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\no-such-coagent-hook.exe --data-dir C:\\c2c\\wgc2\\B\\d-F7d]: failed; blocking because onFailure is \"block\"\nError occurred while executing hook command: ENOENT: no such file or directory, uv_spawn 'C:\\c2c\\tga\\debug\\no-such-coagent-hook.exe'"
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
 "elapsed_s": 3.69,
 "canary_files": [],
 "note": ""
}
(no daemon.jsonl for F7d)

===== out-B\raw_B\F8b\verdict.json WHOLE =====
{
 "case": "F8b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01FkLAsxGoerC4otZQ7oci7d",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F8b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F8b` with the content `canary`.",
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
 "elapsed_s": 3.54,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F8b)

===== out-B\raw_B\F8d\verdict.json WHOLE =====
{
 "case": "F8d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01BrHnoLcUN5oDc1wpUnwiGz",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F8d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F8d` with the content `canary`.",
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
 "elapsed_s": 3.74,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F8d)

===== out-B\raw_B\F9b\verdict.json WHOLE =====
{
 "case": "F9b",
 "tool": "Write",
 "mode_wanted": "bypass",
 "permissionMode": "bypassPermissions",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_01Lgc4YJbkfS6JD1ayQe4bPq",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgc2\\B\\d-F9b]: timed out; blocking because onFailure is \"block\""
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
 "elapsed_s": 8.82,
 "canary_files": [],
 "note": ""
}
===== out-B\raw_B\F9b\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\F9b","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"3d3d3bd4-265f-4982-998d-7159033266ef","session_id":"1b647556-d978-4521-b31f-5f6494b3fb78","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgc2\\B\\F9b\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01Lgc4YJbkfS6JD1ayQe4bPq","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-F9b\\1b647556-d978-4521-b31f-5f6494b3fb78.jsonl"},"id":1,"mode":"hang","ts_ms":1795401112990}

===== out-B\raw_B\F9d\verdict.json WHOLE =====
{
 "case": "F9d",
 "tool": "Write",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_01CrRQ6gQV1pp3mEvNt6MbM1",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgc2\\B\\d-F9d]: timed out; blocking because onFailure is \"block\""
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
 "elapsed_s": 8.86,
 "canary_files": [],
 "note": ""
}
===== out-B\raw_B\F9d\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\F9d","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"408a8400-18d1-40cb-9b16-82f7f76c0fed","session_id":"e1fcaf5f-ece6-4c06-a35b-0d519c9fd125","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgc2\\B\\F9d\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01CrRQ6gQV1pp3mEvNt6MbM1","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-F9d\\e1fcaf5f-ece6-4c06-a35b-0d519c9fd125.jsonl"},"id":1,"mode":"hang","ts_ms":1795401064810}

===== out-B\raw_B\P1\verdict.json WHOLE =====
{
 "case": "P1",
 "tool": "PowerShell",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01XqyXyDQ6SgTTUBEaDeL6ht",
   "is_error": false,
   "text": "(PowerShell completed with no output)"
  }
 ],
 "final_text": "I ran the PowerShell command once in the current directory, and it completed with no output, so `CANARY.txt` should now contain `canary`. I didn't verify the file afterward.",
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
 "elapsed_s": 4.74,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for P1)

===== out-B\raw_B\P2\verdict.json WHOLE =====
{
 "case": "P2",
 "tool": "PowerShell",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": true,
 "tool_results_whole": [
  {
   "id": "toolu_01Y4hvsoB5agR6HFZeeZEAJL",
   "is_error": false,
   "text": "(PowerShell completed with no output)"
  }
 ],
 "final_text": "Done. I ran `Set-Content -Path CANARY.txt -Value canary` once in the current directory. It completed with no output, so the file should now exist, though I didn't check it afterward.",
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
 "elapsed_s": 5.02,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-B\raw_B\P2\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\P2","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"0fead01f-98af-4dd4-b512-2569f196e23e","session_id":"a42f7617-700c-47c4-b7ac-65b11ac755e1","tool_input":{"command":"Set-Content -Path CANARY.txt -Value canary","description":"Write canary value to CANARY.txt in current directory"},"tool_name":"PowerShell","tool_use_id":"toolu_01Y4hvsoB5agR6HFZeeZEAJL","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-P2\\a42f7617-700c-47c4-b7ac-65b11ac755e1.jsonl"},"id":1,"mode":"allow","ts_ms":1795401011758}

===== out-B\raw_B\P3\verdict.json WHOLE =====
{
 "case": "P3",
 "tool": "PowerShell",
 "mode_wanted": "default",
 "permissionMode": "default",
 "tools": [
  "Task",
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
  "real": true,
  "why": "no Bash and no Monitor tool, and a PowerShell tool listed",
  "bash": false,
  "powershell": true
 },
 "file_exists": false,
 "tool_results_whole": [
  {
   "id": "toolu_01PcyZo9Wqx4g1hGZR4yTzpm",
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
 "elapsed_s": 4.03,
 "canary_files": [],
 "note": ""
}
===== out-B\raw_B\P3\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\P3","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"ce687a04-22a2-4692-8702-eecc0cd4e8b5","session_id":"e2fc71e6-7285-4107-8313-bbd80f2bb9dd","tool_input":{"command":"Set-Content -Path CANARY.txt -Value canary","description":"Write canary value to CANARY.txt in current directory"},"tool_name":"PowerShell","tool_use_id":"toolu_01PcyZo9Wqx4g1hGZR4yTzpm","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-P3\\e2fc71e6-7285-4107-8313-bbd80f2bb9dd.jsonl"},"id":1,"mode":"deny","ts_ms":1795401016819}

