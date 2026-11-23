W1 SET-UP B: PASS   |   PROBE tools: Bash=False PowerShell=True -> no Bash and no Monitor tool, and a PowerShell tool listed
part 1 of 4

WO-21 RESULTS (stage C, look-alike). 2026-11-23 local (UTC+11). Sender of WO-21 verified. I asked the owner at the keyboard first, as promised;
he said "Yes, run the batch" at 13:29:40. ONE runner command, run once. No bundle, no clone: the tree is WO-20's C:\c2c\mga3 (HEAD and status checked).

STEP LOG (times, exit codes, settings BEFORE, process list BEFORE and AFTER), WHOLE:

WO-21 sender verified: Friday laptop seat <friday-laptop-agent@agentmail.to>
step 0 at 13:28:56: C:\c2c\wgc2 exists: False
.claude\settings.json  8278791DFD8D3524CA064E5E30BCB2018CE7BDD575A07DFB89BA666DA6050BD6
.claude\settings.local.json  A8AFD89FBCD27902E651310A4B7306FC12D36477E53AF0B00B7DFB467A1DE225
PROCESS LIST BEFORE (name, pid, parent, start, image):
  claude.exe  pid 19716  parent 22940  started 2026-11-21 17:16:50  <PROFILE>\.local\bin\claude.exe
  node.exe  pid 23872  parent 19716  started 2026-11-21 17:16:54  C:\Program Files\nodejs\node.exe
step 1 at 13:28:56
HEAD 462faca6e65c9ad7965422a2ac6d8bf4cdc5f820
status --porcelain: (empty)
programs present: hook True, stub True
owner said YES at the keyboard to the WO-21 batch at 13:29:40
step 2 started 13:29:40.713
step 2 ended 13:32:09.241; exit 0; took 149 s
PROCESS LIST AFTER, one minute after the end (13:33:09) (name, pid, parent, start, image):
  claude.exe  pid 19716  parent 22940  started 2026-11-21 17:16:50  <PROFILE>\.local\bin\claude.exe
  node.exe  pid 23872  parent 19716  started 2026-11-21 17:16:54  C:\Program Files\nodejs\node.exe

STEP 3: my own settings checksums AFTER identical to BEFORE: True
.claude\settings.json  8278791DFD8D3524CA064E5E30BCB2018CE7BDD575A07DFB89BA666DA6050BD6
.claude\settings.local.json  A8AFD89FBCD27902E651310A4B7306FC12D36477E53AF0B00B7DFB467A1DE225
  Both process lists hold only this session (claude.exe pid 19716 started 2026-11-21 17:16:50, the parent of my shell, and its node.exe pid 23872).

C:\c2c\logs\wgc2-console.log WHOLE:
W1 run.ps1 set-up B at 2026-11-23 13:29:41 +11:00; pwsh 7.6.10; CLAUDE_CONFIG_DIR set: False
BEFORE <PROFILE>\.claude\settings.json  8278791DFD8D3524CA064E5E30BCB2018CE7BDD575A07DFB89BA666DA6050BD6
BEFORE <PROFILE>\.claude\settings.local.json  A8AFD89FBCD27902E651310A4B7306FC12D36477E53AF0B00B7DFB467A1DE225
CLAUDE program <PROFILE>\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\bin\claude.exe  version '2.1.330 (Claude Code)'  sha256 fa797c1bc7d4a3511da42622bae53a2b7f1276ae328c668f2bfef44635301caa  (launcher <PROFILE>\AppData\Roaming\npm\claude.cmd)
W1 set-up B: 32 cases, model claude-haiku-5-5, PATH entries hidden for this run's children: 2
  hidden: C:\Program Files\Git\cmd
  hidden: C:\Program Files\Git\cmd
CEILING 37 model runs for this sitting (--max-runs); planned 32 cases + at most 6 repeats
CASE W1 PASS rc=0 3.7s called:ok; mode:ok; file:ok
PROBE tools: Bash=False PowerShell=True -> no Bash and no Monitor tool, and a PowerShell tool listed
CASE W2 PASS rc=0 3.9s called:ok; mode:ok; file:ok; witness:ok
CASE W3 PASS rc=0 3.5s called:ok; mode:ok; file:ok; text:ok; witness:ok
CASE W4 PASS rc=0 3.5s called:ok; mode:ok; file:ok
CASE W5 PASS rc=0 3.8s called:ok; mode:ok; file:ok; witness:ok
CASE W6 PASS rc=0 3.6s called:ok; mode:ok; file:ok; text:ok; witness:ok
CASE P1 PASS rc=0 4.7s called:ok; mode:ok; file:ok
CASE P2 PASS rc=0 5.0s called:ok; mode:ok; file:ok; witness:ok
CASE P3 PASS rc=0 4.0s called:ok; mode:ok; file:ok; text:ok; witness:ok
CASE P4 PASS rc=0 4.7s called:ok; mode:ok; file:ok
CASE P5 PASS rc=0 4.8s called:ok; mode:ok; file:ok; witness:ok
CASE P6 PASS rc=0 4.0s called:ok; mode:ok; file:ok; text:ok; witness:ok
CASE F1d PASS rc=0 3.6s called:ok; mode:ok; file:ok
CASE F2d PASS rc=0 3.7s called:ok; mode:ok; file:ok; witness:ok
CASE F3d PASS rc=0 3.5s called:ok; mode:ok; file:ok; text:ok
CASE F4d PASS rc=0 3.5s called:ok; mode:ok; file:ok; text:ok; witness:ok
CASE F5d PASS rc=0 3.7s called:ok; mode:ok; file:ok; text:ok
CASE F6d PASS rc=0 4.4s called:ok; mode:ok; file:ok
CASE F7d PASS rc=0 3.7s called:ok; mode:ok; file:ok; text:ok
CASE F8d PASS rc=0 3.7s called:ok; mode:ok; file:ok
CASE F9d PASS rc=0 8.9s called:ok; mode:ok; file:ok; text:ok; witness:ok
CASE F10d PASS rc=0 8.8s called:ok; mode:ok; file:ok; witness:ok
CASE F1b PASS rc=0 3.8s called:ok; mode:ok; file:ok
CASE F2b PASS rc=0 3.9s called:ok; mode:ok; file:ok; witness:ok
CASE F3b PASS rc=0 3.9s called:ok; mode:ok; file:ok; text:ok
CASE F4b PASS rc=0 3.5s called:ok; mode:ok; file:ok; text:ok; witness:ok
CASE F5b PASS rc=0 3.9s called:ok; mode:ok; file:ok; text:ok
CASE F6b PASS rc=0 3.7s called:ok; mode:ok; file:ok
CASE F7b PASS rc=0 3.6s called:ok; mode:ok; file:ok; text:ok
CASE F8b PASS rc=0 3.5s called:ok; mode:ok; file:ok
CASE F9b PASS rc=0 8.8s called:ok; mode:ok; file:ok; text:ok; witness:ok
CASE F10b PASS rc=0 8.9s called:ok; mode:ok; file:ok; witness:ok
SETTINGS identical before/after: True
CLAUDE INVOCATIONS 32 of a ceiling of 37 (repeats 0): each is one model run when --claude is the real Claude Code
W1 SET-UP B: PASS
AFTER  <PROFILE>\.claude\settings.json  8278791DFD8D3524CA064E5E30BCB2018CE7BDD575A07DFB89BA666DA6050BD6
AFTER  <PROFILE>\.claude\settings.local.json  A8AFD89FBCD27902E651310A4B7306FC12D36477E53AF0B00B7DFB467A1DE225
settings identical before/after (pwsh's own hashes): True
run.ps1: w1.py exit 0; summary C:\c2c\wgc2\out-B\summary_B.json

summary_B.json WHOLE:
{
 "setup": "B",
 "model": "claude-haiku-5-5",
 "cases_planned": 32,
 "model_runs": 32,
 "claude": {
  "launcher": "<PROFILE>\\AppData\\Roaming\\npm\\claude.cmd",
  "program_shown": "<PROFILE>\\AppData\\Roaming\\npm\\node_modules\\@anthropic-ai\\claude-code\\bin\\claude.exe",
  "version": "2.1.330 (Claude Code)",
  "bytes": 387754656,
  "sha256": "fa797c1bc7d4a3511da42622bae53a2b7f1276ae328c668f2bfef44635301caa"
 },
 "ceiling": 37,
 "runs_started_this_sitting": 32,
 "repeats": 0,
 "hidden_path_entries": 2,
 "stopped": null,
 "skipped": [],
 "settings_before": {
  "<PROFILE>/.claude/settings.json": "8278791dfd8d3524ca064e5e30bcb2018ce7bdd575a07dfb89ba666da6050bd6",
  "<PROFILE>/.claude/settings.local.json": "a8afd89fbcd27902e651310a4b7306fc12d36477e53af0b00b7dfb467a1de225"
 },
 "settings_after": {
  "<PROFILE>/.claude/settings.json": "8278791dfd8d3524ca064e5e30bcb2018ce7bdd575a07dfb89ba666da6050bd6",
  "<PROFILE>/.claude/settings.local.json": "a8afd89fbcd27902e651310a4b7306fc12d36477e53af0b00b7dfb467a1de225"
 },
 "settings_identical": true,
 "pass": [
  "F10b",
  "F10d",
  "F1b",
  "F1d",
  "F2b",
  "F2d",
  "F3b",
  "F3d",
  "F4b",
  "F4d",
  "F5b",
  "F5d",
  "F6b",
  "F6d",
  "F7b",
  "F7d",
  "F8b",
  "F8d",
  "F9b",
  "F9d",
  "P1",
  "P2",
  "P3",
  "P4",
  "P5",
  "P6",
  "W1",
  "W2",
  "W3",
  "W4",
  "W5",
  "W6"
 ],
 "fail": [],
 "blocking_failures": [],
 "void": [],
 "nonblocking_diff": [],
 "overall": "PASS"
}

model_runs_B.log WHOLE:
2026-11-23T13:29:42 setup=B case=W1 model=claude-haiku-5-5
2026-11-23T13:29:46 setup=B case=W2 model=claude-haiku-5-5
2026-11-23T13:29:50 setup=B case=W3 model=claude-haiku-5-5
2026-11-23T13:29:53 setup=B case=W4 model=claude-haiku-5-5
2026-11-23T13:29:57 setup=B case=W5 model=claude-haiku-5-5
2026-11-23T13:30:01 setup=B case=W6 model=claude-haiku-5-5
2026-11-23T13:30:04 setup=B case=P1 model=claude-haiku-5-5
2026-11-23T13:30:09 setup=B case=P2 model=claude-haiku-5-5
2026-11-23T13:30:14 setup=B case=P3 model=claude-haiku-5-5
2026-11-23T13:30:18 setup=B case=P4 model=claude-haiku-5-5
2026-11-23T13:30:23 setup=B case=P5 model=claude-haiku-5-5
2026-11-23T13:30:28 setup=B case=P6 model=claude-haiku-5-5
2026-11-23T13:30:32 setup=B case=F1d model=claude-haiku-5-5
2026-11-23T13:30:36 setup=B case=F2d model=claude-haiku-5-5
2026-11-23T13:30:40 setup=B case=F3d model=claude-haiku-5-5
2026-11-23T13:30:43 setup=B case=F4d model=claude-haiku-5-5
2026-11-23T13:30:47 setup=B case=F5d model=claude-haiku-5-5
2026-11-23T13:30:51 setup=B case=F6d model=claude-haiku-5-5
2026-11-23T13:30:55 setup=B case=F7d model=claude-haiku-5-5
2026-11-23T13:30:59 setup=B case=F8d model=claude-haiku-5-5
2026-11-23T13:31:02 setup=B case=F9d model=claude-haiku-5-5
2026-11-23T13:31:11 setup=B case=F10d model=claude-haiku-5-5
2026-11-23T13:31:20 setup=B case=F1b model=claude-haiku-5-5
2026-11-23T13:31:24 setup=B case=F2b model=claude-haiku-5-5
2026-11-23T13:31:28 setup=B case=F3b model=claude-haiku-5-5
2026-11-23T13:31:32 setup=B case=F4b model=claude-haiku-5-5
2026-11-23T13:31:36 setup=B case=F5b model=claude-haiku-5-5
2026-11-23T13:31:40 setup=B case=F6b model=claude-haiku-5-5
2026-11-23T13:31:43 setup=B case=F7b model=claude-haiku-5-5
2026-11-23T13:31:47 setup=B case=F8b model=claude-haiku-5-5
2026-11-23T13:31:51 setup=B case=F9b model=claude-haiku-5-5
2026-11-23T13:32:00 setup=B case=F10b model=claude-haiku-5-5

FILES under C:\c2c\wgc2\out-B\ with sizes (178 files):
  out-B\model_runs_B.log  1942
  out-B\raw_B\F10b\daemon.jsonl  563
  out-B\raw_B\F10b\daemon.jsonl.ready  48
  out-B\raw_B\F10b\daemon.jsonl.stderr  80
  out-B\raw_B\F10b\settings.json  403
  out-B\raw_B\F10b\stderr.txt  0
  out-B\raw_B\F10b\stream.jsonl  10104
  out-B\raw_B\F10b\verdict.json  1915
  out-B\raw_B\F10d\daemon.jsonl  553
  out-B\raw_B\F10d\daemon.jsonl.ready  48
  out-B\raw_B\F10d\daemon.jsonl.stderr  80
  out-B\raw_B\F10d\settings.json  403
  out-B\raw_B\F10d\stderr.txt  0
  out-B\raw_B\F10d\stream.jsonl  9982
  out-B\raw_B\F10d\verdict.json  1828
  out-B\raw_B\F1b\stderr.txt  0
  out-B\raw_B\F1b\stream.jsonl  9732
  out-B\raw_B\F1b\verdict.json  1738
  out-B\raw_B\F1d\stderr.txt  0
  out-B\raw_B\F1d\stream.jsonl  9708
  out-B\raw_B\F1d\verdict.json  1709
  out-B\raw_B\F2b\daemon.jsonl  561
  out-B\raw_B\F2b\daemon.jsonl.ready  47
  out-B\raw_B\F2b\daemon.jsonl.stderr  80
  out-B\raw_B\F2b\settings.json  439
  out-B\raw_B\F2b\stderr.txt  0
  out-B\raw_B\F2b\stream.jsonl  9738
  out-B\raw_B\F2b\verdict.json  1918
  out-B\raw_B\F2d\daemon.jsonl  551
  out-B\raw_B\F2d\daemon.jsonl.ready  47
  out-B\raw_B\F2d\daemon.jsonl.stderr  80
  out-B\raw_B\F2d\settings.json  439
  out-B\raw_B\F2d\stderr.txt  0
  out-B\raw_B\F2d\stream.jsonl  9604
  out-B\raw_B\F2d\verdict.json  1824
  out-B\raw_B\F3b\daemon.jsonl  0
  out-B\raw_B\F3b\daemon.jsonl.ready  47
  out-B\raw_B\F3b\daemon.jsonl.stderr  80
  out-B\raw_B\F3b\settings.json  439
  out-B\raw_B\F3b\stderr.txt  0
  out-B\raw_B\F3b\stream.jsonl  11967
  out-B\raw_B\F3b\verdict.json  1791
  out-B\raw_B\F3d\daemon.jsonl  0
  out-B\raw_B\F3d\daemon.jsonl.ready  47
  out-B\raw_B\F3d\daemon.jsonl.stderr  80
  out-B\raw_B\F3d\settings.json  439
  out-B\raw_B\F3d\stderr.txt  0
  out-B\raw_B\F3d\stream.jsonl  9731
  out-B\raw_B\F3d\verdict.json  1769
  out-B\raw_B\F4b\daemon.jsonl  560
  out-B\raw_B\F4b\daemon.jsonl.ready  47
  out-B\raw_B\F4b\daemon.jsonl.stderr  79
  out-B\raw_B\F4b\settings.json  439
  out-B\raw_B\F4b\stderr.txt  0
  out-B\raw_B\F4b\stream.jsonl  9743
  out-B\raw_B\F4b\verdict.json  2044
  out-B\raw_B\F4d\daemon.jsonl  550
  out-B\raw_B\F4d\daemon.jsonl.ready  47
  out-B\raw_B\F4d\daemon.jsonl.stderr  79
  out-B\raw_B\F4d\settings.json  439
  out-B\raw_B\F4d\stderr.txt  0
  out-B\raw_B\F4d\stream.jsonl  9731
  out-B\raw_B\F4d\verdict.json  2012
  out-B\raw_B\F5b\settings.json  386
  out-B\raw_B\F5b\stderr.txt  0
  out-B\raw_B\F5b\stream.jsonl  12002
  out-B\raw_B\F5b\verdict.json  1782
  out-B\raw_B\F5d\settings.json  386
  out-B\raw_B\F5d\stderr.txt  0
  out-B\raw_B\F5d\stream.jsonl  11881
  out-B\raw_B\F5d\verdict.json  1761
  out-B\raw_B\F6b\settings.json  350
  out-B\raw_B\F6b\stderr.txt  0
  out-B\raw_B\F6b\stream.jsonl  9714
  out-B\raw_B\F6b\verdict.json  1730
  out-B\raw_B\F6d\settings.json  350
  out-B\raw_B\F6d\stderr.txt  0
  out-B\raw_B\F6d\stream.jsonl  9706
  out-B\raw_B\F6d\verdict.json  1708
  out-B\raw_B\F7b\settings.json  447
  out-B\raw_B\F7b\stderr.txt  0
  out-B\raw_B\F7b\stream.jsonl  12297
  out-B\raw_B\F7b\verdict.json  1945
  out-B\raw_B\F7d\settings.json  447
  out-B\raw_B\F7d\stderr.txt  0
  out-B\raw_B\F7d\stream.jsonl  12263
  out-B\raw_B\F7d\verdict.json  1923
  out-B\raw_B\F8b\settings.json  411
  out-B\raw_B\F8b\stderr.txt  0
  out-B\raw_B\F8b\stream.jsonl  9986
  out-B\raw_B\F8b\verdict.json  1680
  out-B\raw_B\F8d\settings.json  411
  out-B\raw_B\F8d\stderr.txt  0
  out-B\raw_B\F8d\stream.jsonl  9976
  out-B\raw_B\F8d\verdict.json  1658
  out-B\raw_B\F9b\daemon.jsonl  560
  out-B\raw_B\F9b\daemon.jsonl.ready  47
  out-B\raw_B\F9b\daemon.jsonl.stderr  79
  out-B\raw_B\F9b\settings.json  438
  out-B\raw_B\F9b\stderr.txt  0
  out-B\raw_B\F9b\stream.jsonl  11973
  out-B\raw_B\F9b\verdict.json  1961
  out-B\raw_B\F9d\daemon.jsonl  550
  out-B\raw_B\F9d\daemon.jsonl.ready  47
  out-B\raw_B\F9d\daemon.jsonl.stderr  79
  out-B\raw_B\F9d\settings.json  438
  out-B\raw_B\F9d\stderr.txt  0
  out-B\raw_B\F9d\stream.jsonl  11933
  out-B\raw_B\F9d\verdict.json  1929
  out-B\raw_B\P1\stderr.txt  0
  out-B\raw_B\P1\stream.jsonl  9760
  out-B\raw_B\P1\verdict.json  1666
  out-B\raw_B\P2\daemon.jsonl  612
  out-B\raw_B\P2\daemon.jsonl.ready  46
  out-B\raw_B\P2\daemon.jsonl.stderr  79
  out-B\raw_B\P2\settings.json  438
  out-B\raw_B\P2\stderr.txt  0
  out-B\raw_B\P2\stream.jsonl  9806
  out-B\raw_B\P2\verdict.json  1846
  out-B\raw_B\P3\daemon.jsonl  611
  out-B\raw_B\P3\daemon.jsonl.ready  46
  out-B\raw_B\P3\daemon.jsonl.stderr  78
  out-B\raw_B\P3\settings.json  438
  out-B\raw_B\P3\stderr.txt  0
  out-B\raw_B\P3\stream.jsonl  12049
  out-B\raw_B\P3\verdict.json  1852
  out-B\raw_B\P4\stderr.txt  0
  out-B\raw_B\P4\stream.jsonl  9710
  out-B\raw_B\P4\verdict.json  1657
  out-B\raw_B\P5\daemon.jsonl  607
  out-B\raw_B\P5\daemon.jsonl.ready  46
  out-B\raw_B\P5\daemon.jsonl.stderr  79
  out-B\raw_B\P5\settings.json  438
  out-B\raw_B\P5\stderr.txt  0
  out-B\raw_B\P5\stream.jsonl  9882
  out-B\raw_B\P5\verdict.json  1926
  out-B\raw_B\P6\daemon.jsonl  621
  out-B\raw_B\P6\daemon.jsonl.ready  46
  out-B\raw_B\P6\daemon.jsonl.stderr  78
  out-B\raw_B\P6\settings.json  438
  out-B\raw_B\P6\stderr.txt  0
  out-B\raw_B\P6\stream.jsonl  11979
  out-B\raw_B\P6\verdict.json  1884
  out-B\raw_B\W1\stderr.txt  0
  out-B\raw_B\W1\stream.jsonl  9697
  out-B\raw_B\W1\verdict.json  1704
  out-B\raw_B\W2\daemon.jsonl  548
  out-B\raw_B\W2\daemon.jsonl.ready  46
  out-B\raw_B\W2\daemon.jsonl.stderr  79
  out-B\raw_B\W2\settings.json  438
  out-B\raw_B\W2\stderr.txt  0
  out-B\raw_B\W2\stream.jsonl  9697
  out-B\raw_B\W2\verdict.json  1871
  out-B\raw_B\W3\daemon.jsonl  547
  out-B\raw_B\W3\daemon.jsonl.ready  46
  out-B\raw_B\W3\daemon.jsonl.stderr  78
  out-B\raw_B\W3\settings.json  438
  out-B\raw_B\W3\stderr.txt  0
  out-B\raw_B\W3\stream.jsonl  9552
  out-B\raw_B\W3\verdict.json  1832
  out-B\raw_B\W4\stderr.txt  0
  out-B\raw_B\W4\stream.jsonl  9640
  out-B\raw_B\W4\verdict.json  1676
  out-B\raw_B\W5\daemon.jsonl  558
  out-B\raw_B\W5\daemon.jsonl.ready  46
  out-B\raw_B\W5\daemon.jsonl.stderr  79
  out-B\raw_B\W5\settings.json  438
  out-B\raw_B\W5\stderr.txt  0
  out-B\raw_B\W5\stream.jsonl  9802
  out-B\raw_B\W5\verdict.json  1934
  out-B\raw_B\W6\daemon.jsonl  557
  out-B\raw_B\W6\daemon.jsonl.ready  46
  out-B\raw_B\W6\daemon.jsonl.stderr  78
  out-B\raw_B\W6\settings.json  438
  out-B\raw_B\W6\stderr.txt  0
  out-B\raw_B\W6\stream.jsonl  9562
  out-B\raw_B\W6\verdict.json  1864
  out-B\summary_B.json  1511
  Empty verdict.json / daemon.jsonl files (their blocks in later parts read '(empty file, 0 bytes)'): out-B\raw_B\F3b\daemon.jsonl, out-B\raw_B\F3d\daemon.jsonl

THE PROBE'S EVIDENCE - FIRST line of out-B\raw_B\W1\stream.jsonl WHOLE:
{"type":"system","subtype":"init","cwd":"C:\\c2c\\wgc2\\B\\W1","session_id":"0f9e27a5-96eb-41b1-9ca2-bb16a0b22b4b","tools":["Task","CronCreate","CronDelete","CronList","DesignSync","Edit","EnterWorktree","ExitWorktree","Glob","Grep","ListAgents","NotebookEdit","PowerShell","PushNotification","Read","RemoteTrigger","ReportFindings","ScheduleWakeup","SendMessage","Skill","TaskStop","ToolSearch","WebSearch","Workflow","Write"],"mcp_servers":[],"model":"claude-haiku-5-5","permissionMode":"default","slash_commands":["deep-research","design","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","workflow-authoring","run","run-skill-generator","plugin-authoring","advisor","agents","auto-mode-setup","autocompact","clear","color","compact","config","output-style","context","effort","fast","focus","heapdump","init","mcp","import","model","__remote-workflow","workflow-launch-exec","reload-plugins","reload-skills","rename","ultrareview","security-review","usage-credits","extra-usage","usage","insights","recap","skill-doctor","goal","design-consent","design-revoke","list-agents","team-onboarding","anthropic-skills:built-in-browser","anthropic-skills:chrome-browser","anthropic-skills:computer-use","anthropic-skills:deep-research","anthropic-skills:docs","anthropic-skills:docx","anthropic-skills:google-workspace","anthropic-skills:import-memory","anthropic-skills:morning","anthropic-skills:pdf","anthropic-skills:pptx","anthropic-skills:skill-creator","anthropic-skills:xlsx"],"terminal_slash_commands":["doctor","color","focus","reload-plugins"],"apiKeySource":"none","claude_code_version":"2.1.330","output_style":"default","agents":["claude","Explore","general-purpose","Plan","statusline-setup","web-fetch"],"skills":["deep-research","design","design-sync","dataviz","update-config","verify","debug","code-review","simplify","batch","fewer-permission-prompts","doctor","loop","schedule","claude-api","workflow-authoring","run","run-skill-generator","plugin-authoring","anthropic-skills:built-in-browser","anthropic-skills:chrome-browser","anthropic-skills:computer-use","anthropic-skills:deep-research","anthropic-skills:docs","anthropic-skills:docx","anthropic-skills:google-workspace","anthropic-skills:import-memory","anthropic-skills:morning","anthropic-skills:pdf","anthropic-skills:pptx","anthropic-skills:skill-creator","anthropic-skills:xlsx"],"plugins":[{"name":"cc-plugin-agents-md","path":"builtin","source":"cc-plugin-agents-md@builtin"},{"name":"cc-plugin-telemetry","path":"builtin","source":"cc-plugin-telemetry@builtin"},{"name":"cc-plugin-privacy","path":"builtin","source":"cc-plugin-privacy@builtin"},{"name":"cc-plugin-plugin-authoring","path":"builtin","source":"cc-plugin-plugin-authoring@builtin"}],"capabilities":["interrupt_receipt_v1","interrupt_cancel_queued_v1","interrupt_send_now_v1","interrupt_requeue_taken_v1","msg_lifecycle_v1","request_marker_lists_v1","ask_user_question_unanswered_v1","lifecycle_wakeup_source_v1","sdk_mcp_tools_list_changed","sdk_mcp_manifests","mcp_read_resource_v1","mcp_tool_ui_meta_v1","ui_surface_v1","mcp_call_result_not_for_model_v1","mcp_call_check_permissions_v1","voice_call_talk_line_v1","withdrawn_files_note_v2","withdrawn_tools_v1","ui_pane_widget_v1","reload_plugins_refuse_if_busy_v1","get_usage_detached_v1","silent_resend_files_v1"],"analytics_disabled":false,"product_feedback_disabled":false,"served_by_anthropic":true,"uuid":"52324c8a-a2c7-4f2e-a2a8-436ab8640e82","memory_paths":{"auto":"<PROFILE>\\.claude\\projects\\C--c2c-wgc2-B-W1\\memory\\"},"original_cwd":"C:\\c2c\\wgc2\\B\\W1","additional_directories":[],"messaging_socket_path":"\\\\.\\pipe\\LOCAL\\cc-msg-e39c61b0e23b55b407f7354f09c6bbad","fast_mode_state":"off","fast_mode_disabled_reason":"sdk_opt_in_required","per_turn_effort_active":true,"ultrathink_available":false,"ultrathink_typed_raises":false,"view_mode":"default","powershell_path":"C:\\Program Files\\PowerShell\\7\\pwsh.exe"}

Streams: no zip attached (text only); kept in place under C:\c2c\wgc2\out-B\raw_B\. Checked: lines in out-B holding the real profile path: 0; the machine name: 0.

ADDITION
(a) Nothing asked for anything this order forbids. (My own addition: asking the owner first; he said yes.)
(b) Everything worked as written; the runner was started from a pwsh 7 child exactly as step 2 gives it (2>&1 | Tee-Object C:\c2c\logs\wgc2-console.log).
Parts 2 to 4: every case's verdict.json WHOLE and daemon.jsonl WHOLE where it exists.
Waiting on my inbox.
