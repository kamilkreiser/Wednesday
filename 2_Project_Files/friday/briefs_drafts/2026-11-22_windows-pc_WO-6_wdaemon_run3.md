From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 6: the background program's LAST PC run (run 3): the Ctrl-C test twice, watched

WHY. Run 2's first Ctrl-C failed and the second passed. The builder found a real gap (Ctrl-C was armed only after the "started" line) and fixed it; this run checks the fix, twice: once on a brand-new data folder (like the failed try) and once reusing it.

RULES: as WO-5. No Administrator, registry, firewall, security-setting or account change; delete nothing; never show the key; change no source; commit/push nothing. Firewall prompt: do NOT allow; record it.

WHERE. Source: C:\c2c\wd3. Target: C:\c2c\twd3. Logs: C:\c2c\logs\wo6-*.log. Test folder: C:\wdc3 (leave it in place at the end).

STEPS (exit code and last lines for each):
1. Attached: coagent-wdaemon-5b008c8.bundle (2,894,041 bytes). Download as before. SHA256 must equal 873298FA960BDB4FE4FD1A7C944AEF9F33197368BFCFEADCA27F9B1CA9698E50, else STOP and mail me.
2. git clone -c core.autocrlf=false -b w-daemon-5b008c8 C:\c2c\coagent-wdaemon-5b008c8.bundle C:\c2c\wd3 ; HEAD must be 5b008c848aa801ea9ce2ec661cc110a69c17ad91.
3. $env:CARGO_TARGET_DIR="C:\c2c\twd3" ; in C:\c2c\wd3, EXACTLY:
   cargo build --locked -p coagent-daemon --bins 2>&1 | Tee-Object C:\c2c\logs\wo6-build-daemon.log
   cargo build --locked -p coagent-cli --bin coagent 2>&1 | Tee-Object C:\c2c\logs\wo6-build-cli.log
   cargo test --locked -p coagent-daemon --test win_rules --test win_datadir --test win_guest 2>&1 | Tee-Object C:\c2c\logs\wo6-tests.log
4. TRY A (fresh folder), with the OWNER pressing the key; START YOUR PROCESS WATCHER FIRST (pid, start and end times of coagentd.exe every 0.5 s, to C:\c2c\logs\wo6-watch-a.log). Guide the owner on screen, in plain words:
   a) In a NEW Command Prompt: mkdir C:\wdc3\prof ; set USERPROFILE=C:\wdc3\prof ; then
      C:\c2c\twd3\debug\coagentd.exe --data-dir C:\wdc3\prof\a 2> C:\wdc3\a.log
   b) YOU check from another window (type C:\wdc3\a.log) until the "started" line shows; THEN tell the owner to press **Ctrl-C** (the C key, NOT Break/Pause) ONCE in the daemon's window and wait for the prompt.
   c) The owner then types, in that same window: echo %ERRORLEVEL%   and tells you the number.
   d) In another NEW window from C:\c2c\wd3 (CARGO_TARGET_DIR=C:\c2c\twd3): set COAGENT_WD_CTRLC_LOG=C:\wdc3\a.log ; cargo test --locked -p coagent-daemon --test win_guest -- --ignored ctrl_c_stops_cleanly
5. TRY B (same folder again), exactly as step 4 but with: 2> C:\wdc3\b.log , --data-dir C:\wdc3\prof\a (the SAME folder), watcher log C:\c2c\logs\wo6-watch-b.log, and COAGENT_WD_CTRLC_LOG=C:\wdc3\b.log.
   Expected for both: the log has "started: …", "coagentd: Ctrl-C received; stopping", and LAST "coagentd: stopped" (try A also "created a new device identity …"); the test 1 passed; %ERRORLEVEL% 0; the process gone within seconds.

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-6 results": the checks; each command's exit code and last lines; EVERY "test result:" line; BOTH logs WHOLE; BOTH %ERRORLEVEL% values; BOTH watcher logs WHOLE; which key the owner pressed each time; anything printed in the daemon's window; any firewall prompt. Then go back to waiting on your inbox.
