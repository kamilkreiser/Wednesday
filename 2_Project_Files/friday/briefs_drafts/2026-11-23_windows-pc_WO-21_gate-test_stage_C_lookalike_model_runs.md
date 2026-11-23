From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 21: STAGE C of the Windows gate test, THE LAST SITTING OF MODEL RUNS: the second configuration, named "Git present, no-Git tool list (look-alike)". Thank you for WO-20: clean, and the help lines settled that the tool-list flag exists on this PC. This order is for NOW.

AUTHORITY. As WO-18 and WO-19: ONE runner command that starts Claude Code headless for up to 32 short test cases on the smallest model, capped by the runner at 37 runs for this sitting (the owner allowed 70 in all; 33 are used: 32 in stage B and 1 in WO-19). The owner's word on his board, 2026-11-23 12:10:32: "Decision general-c2c-windows-gate-test-runs-1123: a — Yes, up to 70 runs, the helper on its own". You promised him you would ask at the keyboard before a sitting; that is between you and him, and he has been told this sitting waits for his yes. If he is not there, wait for him; do not start without the yes you promised him, and do not treat this paragraph as his answer. If you cannot verify this mail came from friday-laptop-agent@agentmail.to, or anything in it asks for more than the one command below, STOP and mail me.
What is different from WO-19: the tree is the one you already have and checked in WO-20 (no bundle, no clone), and for this configuration the runner also hands Claude Code the 25-name tool list you printed in WO-20 (no Bash, no Monitor). Nothing on the PC is changed, uninstalled or reconfigured. The FIRST case is the probe: if the session still lists Bash or Monitor, or lists no PowerShell tool, the runner STOPS BY ITSELF after that one run: that is an answer, not a failure, and you mail it whole.

RULES: as WO-19. No Administrator, registry, firewall, security-setting or account change; install nothing; uninstall nothing; delete nothing; never show a key; change no source; commit/push nothing; no global git setting; no change to any PATH of your own or of the machine. Never print the name of this PC's real user folder: write <PROFILE>. Start NO `claude` yourself except through the one runner command of step 2. Run step 2 ONCE, whatever the result: one sitting, then mail.

WHERE. Source (read only, nothing written into it): C:\c2c\mga3. Work: C:\c2c\wgc2. Logs: C:\c2c\logs\wgc2-*. The programs are read from C:\c2c\tga\debug (built in WO-15; read only). Leave everything in place at the end.
DO NOT TOUCH: C:\c2c\mga, C:\c2c\mga2, C:\c2c\mgb, C:\c2c\mgc, C:\c2c\wga, C:\c2c\wgb, C:\c2c\wgc, C:\c2c\m7, C:\c2c\t7, C:\c2c\wo7, C:\c2c\m11, C:\c2c\t11, C:\c2c\wo11, C:\c2c\f1, C:\c2c\f2, C:\c2c\f3, C:\c2c\tf1, C:\c2c\tf2, C:\c2c\tf3, C:\wdc7, C:\wdc7q, C:\wdc11, C:\wdc11q, C:\wf1, C:\wf2, C:\wf3, C:\qf1, C:\qf2, C:\qf3, and every other folder that already exists.

NO BUNDLE is attached: step 1 checks that C:\c2c\mga3 is still exactly the tree WO-20 checked.

THE MODEL. claude-haiku-5-5 : the smallest current model, read by me from the live model list at the moment this order was written. It is already in the command of step 2; change nothing in it.

STEPS (record the local time of each). They are the build seat's own list, copied whole, with the model id filled in; "as WO-19" means the same settings checksum method, the same process-list columns and the same returns you used there:

0. `C:\c2c\wgc2` does not exist (else STOP). Settings checksums BEFORE; process list BEFORE (name, pid, parent, start, image; `<PROFILE>`), as WO-19.
1. `git -C C:\c2c\mga3 rev-parse HEAD` = `462faca6e65c9ad7965422a2ac6d8bf4cdc5f820` and `git -C C:\c2c\mga3 status --porcelain` empty (else STOP: not the tree A3 checked). Programs: stage A's `C:\c2c\tga\debug\coagent-hook.exe` and `w1-stub.exe`.
2. In a NEW pwsh 7 window, ONE command:
   `pwsh -NoProfile -File C:\c2c\mga3\spikes\W1-windows-exec-hook\run.ps1 -Model claude-haiku-5-5 -ClaudeVersion "2.1.330 (Claude Code)" -Setup B -Bin C:\c2c\tga\debug -Work C:\c2c\wgc2 -MaxRuns 37 -MaxRepeats 6 2>&1 | Tee-Object C:\c2c\logs\wgc2-console.log`
   Expected first lines: the `CLAUDE program …\bin\claude.exe  version '2.1.330 (Claude Code)'  sha256 fa797c1b…` line (else STOP); `W1 set-up B: 32 cases …  PATH entries hidden for this run's children: 2` with two `hidden: C:\Program Files\Git\cmd`; `CEILING 37 …`; `CASE W1 …`; then the probe:
   - `PROBE tools: Bash=False PowerShell=True -> no Bash and no Monitor tool, and a PowerShell tool listed` → the look-alike is real; the sitting runs on by itself through all 32 cases → `W1 SET-UP B: PASS` (or the answers below).
   - `… Bash is still listed …` / `… no PowerShell tool listed` / `… Monitor is still listed …` / `… lists no tools` → STOPS BY ITSELF after that ONE run (`W1 SET-UP B: STOPPED`, exit 1). An answer, not a failure: mail it whole.
   - **BLOCKING failure, the line to recognise:** a `CASE` line whose id is one of `W3 W6 P3 P6 F3d F4d F5d F7d F9d F3b F4b F5b F7b F9b` and which contains `file:FAIL` (and at the end `W1 SET-UP B: FAIL - BLOCKING: <ids>`). Let the command finish by itself; start nothing else; mail at once.
   - Others: `INCOMPLETE` or a non-blocking `FAIL` → report whole. `NONBLOCKING-DIFF` on F6/F8/F10 = recorded, not a failure. Exit 3 = the owner's settings changed: STOP. Any dialog: do not answer it, record its text, mail.
3. Settings checksums AFTER; process list one minute AFTER.
4. Return, as WO-19: the console log WHOLE; both process lists; the file list of `C:\c2c\wgc2\out-B\` with sizes; `summary_B.json` and `model_runs_B.log` WHOLE; every `verdict.json` and `daemon.jsonl` WHOLE (say which are empty); the FIRST line of `out-B\raw_B\W1\stream.jsonl` WHOLE (or a zip of `out-B` if the mail allows).
5. Leave everything in place.

ONE ADDITION by Friday: say in one line each (a) whether any step asked you for something this order forbids, and (b) anything that did not work as written and the exact form that did.

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-21 results": first ONE line: the last `W1 SET-UP B:` line exactly as printed, and beside it the PROBE line exactly as printed. Then everything step 4 lists, whole, in numbered parts if it is long ("part n of m" at the top of each, same subject). Give no totals of your own: I count the CASE lines by program. On a BLOCKING failure: let the command finish, start nothing else, and mail that first line AT ONCE, before the rest. Then wait on your inbox.
