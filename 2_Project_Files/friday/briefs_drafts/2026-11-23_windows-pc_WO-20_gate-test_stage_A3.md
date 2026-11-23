From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 20: STAGE A3 of the Windows gate test. Thank you for WO-19: the probe answered exactly what it was built to answer, and the two process lists with start times closed that question. What it showed: with Git's folder off the path of the test's children, Claude Code still found a Bash, so that set-up was not real and the runner stopped itself. The build seat has changed the runner: for the second set-up it now also hands Claude Code a tool list without Bash. This order checks that change on this PC. It is for NOW, by yourself: NO MODEL RUN (never `claude` with a prompt, never `claude -p`; the only `claude` starts are `--version`, made by the helper script, and one `--help`), nothing built, no network beyond your mail. No owner is needed for this order.

AUTHORITY. The owner's standing word for the Windows lane. The model runs that follow are NOT in this order.

RULES: as WO-17. No Administrator, registry, firewall, security-setting or account change; install nothing; uninstall nothing; delete nothing; never show a key; change no source; commit/push nothing; no global git setting. If any prompt or dialog appears: do not answer it; record its exact text and STOP. Never print the name of this PC's real user folder: write <PROFILE>. Use a PowerShell 7 (pwsh) window; every command with 2>&1 | Tee-Object C:\c2c\logs\wga3-<n>.log .

WHERE. Source: C:\c2c\mga3. Logs: C:\c2c\logs\wga3-*. Nothing else is written. Leave everything in place at the end.
DO NOT TOUCH: C:\c2c\mga, C:\c2c\mga2, C:\c2c\mgb, C:\c2c\mgc, C:\c2c\tga, C:\c2c\wga, C:\c2c\wgb, C:\c2c\wgc, C:\c2c\m7, C:\c2c\t7, C:\c2c\wo7, C:\c2c\m11, C:\c2c\t11, C:\c2c\wo11, C:\c2c\f1, C:\c2c\f2, C:\c2c\f3, C:\c2c\tf1, C:\c2c\tf2, C:\c2c\tf3, C:\wdc7, C:\wdc7q, C:\wdc11, C:\wdc11q, C:\wf1, C:\wf2, C:\wf3, C:\qf1, C:\qf2, C:\qf3, and every other folder that already exists.

THE BUNDLE. Attached: coagent-wgatetest-462faca.bundle (3,764,509 bytes), a bundle of the branch w-gate-test at 462faca6e65c9ad7965422a2ac6d8bf4cdc5f820. Save it as C:\c2c\coagent-wgatetest-462faca.bundle. Its SHA256 must equal E96E045710C9D392763063BBFCCDCD29B56F5C14244A0D0B2F91E45E54FF751D, else STOP. Clone it with: git clone -b w-gate-test C:\c2c\coagent-wgatetest-462faca.bundle C:\c2c\mga3

STEPS (record the local time of each). They are the build seat's own list, copied whole; "as in A2" means what WO-17 showed; the settings checksums by the same method as before:

0. `C:\c2c\mga3` does not exist (else STOP). Settings checksums BEFORE.
1. Clone to `C:\c2c\mga3`; HEAD = `462faca6e65c9ad7965422a2ac6d8bf4cdc5f820`; `git status --porcelain` empty; `git ls-files --eol -- spikes/W1-windows-exec-hook/w1.py` → `i/lf w/lf`; `git -C C:\c2c\mga3 diff --quiet fed7bfe HEAD -- crates spikes/W1-windows-exec-hook/src spikes/W4-windows-paths/src` → exit 0 (stage A's programs stand; else STOP).
2. `python -I C:\c2c\mga3\spikes\W1-windows-exec-hook\w1.py selftest` → **44** PASS lines, last line `SELFTEST PASS: 0 failed (temporary files in the system's temporary folder, made by this run)`, exit 0.
3. `python -I C:\c2c\mga3\spikes\W1-windows-exec-hook\w1.py show-hidden --setup B` → as in A2 (`HIDDEN C:\Program Files\Git\cmd` twice; System32 twice and WindowsApps KEPT; `SET-UP B: 2 hidden, 46 PATH entries kept`) PLUS the new last line, exactly:
   `SET-UP B claude arguments added: ["--tools", "Task,CronCreate,CronDelete,CronList,DesignSync,Edit,EnterWorktree,ExitWorktree,Glob,Grep,ListAgents,NotebookEdit,PowerShell,PushNotification,Read,RemoteTrigger,ReportFindings,ScheduleWakeup,SendMessage,Skill,TaskStop,ToolSearch,WebSearch,Workflow,Write"]`
   and `… show-hidden --setup A` → `SET-UP A: 0 hidden, 48 PATH entries kept` and `SET-UP A claude arguments added: []`. Wrong: any other list (whole output back).
4. `python -I C:\c2c\mga3\spikes\W1-windows-exec-hook\w1.py resolve-claude --claude-version "2.1.330 (Claude Code)"` → the same two lines as A2 (program `…\bin\claude.exe`, 387754656 bytes, sha256 `fa797c1b…5301caa`), exit 0.
5. NO model run: `claude --help` through the launcher (as WO-11 step 4), and quote WHOLE every help line that names `--tools`, `--disallowedTools` / `--disallowed-tools` and `--allowedTools`. Expected: a `--tools` line saying it restricts the built-in tools (that the flag exists in 2.1.330 is what this step checks). Wrong: no `--tools` line: report it whole; stage C then does not run.
6. Settings checksums AFTER, compared with step 0.

ONE ADDITION by Friday: say in one line each (a) whether any step asked you for something this order forbids, and (b) anything that did not work as written and the exact form that did.

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-20 results": the local time and exit code of each step; the logs of steps 2, 3, 4 and 5 WHOLE (step 5: every help line that names --tools, --disallowedTools or --disallowed-tools, and --allowedTools, whole); the settings comparison; the two lines of the addition. Give no totals of your own. Then wait on your inbox: the next order is the second sitting of model runs with the new tool list.
