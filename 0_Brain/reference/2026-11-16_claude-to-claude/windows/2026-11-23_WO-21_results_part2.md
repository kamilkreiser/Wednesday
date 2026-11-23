W1 SET-UP B: PASS   |   PROBE tools: Bash=False PowerShell=True -> no Bash and no Monitor tool, and a PowerShell tool listed
part 2 of 4

===== out-B\raw_B\F10b\verdict.json WHOLE =====
{
 "case": "F10b",
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
   "id": "toolu_01HqnE8dRgjPsdKNF1QCVYdP",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F10b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F10b` with the content `canary`. The Write call succeeded, so the reply is not REFUSED.",
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
===== out-B\raw_B\F10b\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\F10b","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"73f3b45e-46fc-45b1-be6f-b72239f7e0ce","session_id":"415586bd-8bcb-4cfc-aa15-7efb49d206e2","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgc2\\B\\F10b\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01HqnE8dRgjPsdKNF1QCVYdP","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-F10b\\415586bd-8bcb-4cfc-aa15-7efb49d206e2.jsonl"},"id":1,"mode":"hang","ts_ms":1795401121963}

===== out-B\raw_B\F10d\verdict.json WHOLE =====
{
 "case": "F10d",
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
   "id": "toolu_01GGtEKtFEWXMPmhUZ5Cy2V7",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F10d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F10d` with the content `canary`.",
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
 "elapsed_s": 8.82,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-B\raw_B\F10d\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\F10d","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"6cf3c613-c309-4c08-a481-f23477e6bbcc","session_id":"b8e6d2d7-d5e2-46f2-a4dc-92c9e779cb28","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgc2\\B\\F10d\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01GGtEKtFEWXMPmhUZ5Cy2V7","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-F10d\\b8e6d2d7-d5e2-46f2-a4dc-92c9e779cb28.jsonl"},"id":1,"mode":"hang","ts_ms":1795401073764}

===== out-B\raw_B\F1b\verdict.json WHOLE =====
{
 "case": "F1b",
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
   "id": "toolu_018aDhAExD9qhC5RTxkQLdz4",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F1b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F1b` with the content `canary`. The Write call succeeded, so there was nothing to refuse.",
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
 "elapsed_s": 3.75,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F1b)

===== out-B\raw_B\F1d\verdict.json WHOLE =====
{
 "case": "F1d",
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
   "id": "toolu_01RRfUd34Af84tm1tQe68hUc",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F1d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F1d` with the content `canary`. The Write call succeeded, so there was no refusal.",
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
 "elapsed_s": 3.64,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
(no daemon.jsonl for F1d)

===== out-B\raw_B\F2b\verdict.json WHOLE =====
{
 "case": "F2b",
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
   "id": "toolu_01TCyivBz2iJjC3aVzdpwGfB",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F2b\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F2b` with the content `canary`. The Write call succeeded, so the word REFUSED does not apply.",
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
 "elapsed_s": 3.89,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-B\raw_B\F2b\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\F2b","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"2486ec61-2cb8-46c9-8a8d-efa492283910","session_id":"19f09438-cff3-4cd4-b26f-a403886eca25","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgc2\\B\\F2b\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01TCyivBz2iJjC3aVzdpwGfB","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-F2b\\19f09438-cff3-4cd4-b26f-a403886eca25.jsonl"},"id":1,"mode":"allow","ts_ms":1795401086595}

===== out-B\raw_B\F2d\verdict.json WHOLE =====
{
 "case": "F2d",
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
   "id": "toolu_01N7GH6g5x6eSGXeumZXRCa3",
   "is_error": false,
   "text": "File created successfully at: C:\\c2c\\wgc2\\B\\F2d\\CANARY.txt (file state is current in your context \u2014 no need to Read it back)"
  }
 ],
 "final_text": "I created `CANARY.txt` in `C:\\c2c\\wgc2\\B\\F2d` with the content `canary`.",
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
 "elapsed_s": 3.71,
 "canary_files": [
  "CANARY.txt"
 ],
 "note": ""
}
===== out-B\raw_B\F2d\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\F2d","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"9cb7b274-55bd-4cb8-b3c7-383f86e2eb1c","session_id":"440e98ef-cd53-4ca8-816d-7c2998bfbb7a","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgc2\\B\\F2d\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01N7GH6g5x6eSGXeumZXRCa3","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-F2d\\440e98ef-cd53-4ca8-816d-7c2998bfbb7a.jsonl"},"id":1,"mode":"allow","ts_ms":1795401038364}

===== out-B\raw_B\F3b\verdict.json WHOLE =====
{
 "case": "F3b",
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
   "id": "toolu_01Jyem7yHfhDk2He7QGM1TtQ",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgc2\\B\\d-F3b]: coagent gate: daemon unreachable or refused - call blocked\n"
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
 "elapsed_s": 3.94,
 "canary_files": [],
 "note": ""
}
===== out-B\raw_B\F3b\daemon.jsonl WHOLE =====
(empty file, 0 bytes)

===== out-B\raw_B\F3d\verdict.json WHOLE =====
{
 "case": "F3d",
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
   "id": "toolu_01X61G61sNZ3nYcZcUjM3AbW",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgc2\\B\\d-F3d]: coagent gate: daemon unreachable or refused - call blocked\n"
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
 "elapsed_s": 3.45,
 "canary_files": [],
 "note": ""
}
===== out-B\raw_B\F3d\daemon.jsonl WHOLE =====
(empty file, 0 bytes)

===== out-B\raw_B\F4b\verdict.json WHOLE =====
{
 "case": "F4b",
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
   "id": "toolu_01NeEePPejP2d53PWHqwY24h",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgc2\\B\\d-F4b]: coagent gate: daemon unreachable or refused - call blocked\n"
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
 "elapsed_s": 3.55,
 "canary_files": [],
 "note": "daemon killed 1.93 s after the run started, once it had logged the PreToolUse"
}
===== out-B\raw_B\F4b\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\F4b","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"bypassPermissions","prompt_id":"fbf555fc-0d77-4de4-82f9-3ca063c1fb52","session_id":"8d8a5851-f800-429f-9f5b-fc620b1dc02a","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgc2\\B\\F4b\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01NeEePPejP2d53PWHqwY24h","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-F4b\\8d8a5851-f800-429f-9f5b-fc620b1dc02a.jsonl"},"id":1,"mode":"hang","ts_ms":1795401094515}

===== out-B\raw_B\F4d\verdict.json WHOLE =====
{
 "case": "F4d",
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
   "id": "toolu_01WaUt2evyaxVJFTvzjbe4uj",
   "is_error": true,
   "text": "PreToolUse:Write hook error: [C:\\c2c\\tga\\debug\\coagent-hook.exe --data-dir C:\\c2c\\wgc2\\B\\d-F4d]: coagent gate: daemon unreachable or refused - call blocked\n"
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
 "elapsed_s": 3.49,
 "canary_files": [],
 "note": "daemon killed 1.92 s after the run started, once it had logged the PreToolUse"
}
===== out-B\raw_B\F4d\daemon.jsonl WHOLE =====
{"cmd":"gate","event":{"cwd":"C:\\c2c\\wgc2\\B\\F4d","effort":{"level":"medium"},"hook_event_name":"PreToolUse","permission_mode":"default","prompt_id":"8f011d6d-0e77-49a6-a640-5b9794c9972b","session_id":"a8aa5002-2c93-401b-81c2-8022930d97b7","tool_input":{"content":"canary","file_path":"C:\\c2c\\wgc2\\B\\F4d\\CANARY.txt"},"tool_name":"Write","tool_use_id":"toolu_01WaUt2evyaxVJFTvzjbe4uj","transcript_path":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-F4d\\a8aa5002-2c93-401b-81c2-8022930d97b7.jsonl"},"id":1,"mode":"hang","ts_ms":1795401045620}

===== out-B\raw_B\F5b\verdict.json WHOLE =====
{
 "case": "F5b",
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
   "id": "toolu_01RV1gH4kGMSB2Bxd2QbpHQn",
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
 "elapsed_s": 3.9,
 "canary_files": [],
 "note": ""
}
(no daemon.jsonl for F5b)

