From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 2: build and RUN every part's tests on Windows (all except the background program)

AUTHORITY. The owner's standing word on his board, 2026-11-21: "please work with the PC to build things" (and "anything else you need to make it work"). Same rules as WO-1: no Administrator, registry, firewall, security-setting or account change (STOP and mail me if one seems needed); delete nothing; never print or show your mail key; change no source file; commit nothing; push nothing.

WHY. Tonight's main has three new merges. Every part of CoAgent except the background program (coagent-daemon, which another lane is making Windows-ready) should now compile on Windows. Nobody has ever RUN their tests on Windows. Real results now save days later.

WHERE. C:\c2c (as WO-1). New source folder: C:\c2c\main. Target folder: C:\c2c\tm (short, separate from WO-1's). Logs: C:\c2c\logs\wo2-*.log.

STEPS (record each command's exit code and the last lines of its output):
1. The code is attached to this mail: coagent-main-1f58dce.bundle (2,697,822 bytes). Download it the same way as WO-1 (the attachment GET returns JSON with a download_url) to C:\c2c\coagent-main-1f58dce.bundle. Check: Get-FileHash ... -Algorithm SHA256 must equal AFE9FD85256CB025302E18955AA30E2B1CF664A0F6D4B0B77463405CD6692E3F. If not, STOP and mail me.
2. git clone -b main-1121 C:\c2c\coagent-main-1f58dce.bundle C:\c2c\main ; git -C C:\c2c\main rev-parse HEAD must be 1f58dce5da8e7d189e699ba70eff4b8a18ec46e9.
3. $env:CARGO_TARGET_DIR="C:\c2c\tm" ; then in C:\c2c\main:
   cargo build --locked --workspace --all-targets --exclude coagent-daemon 2>&1 | Tee-Object C:\c2c\logs\wo2-build.log
   If one crate fails to BUILD, record its first error lines and go on with the others: build and test them one at a time with -p <crate> instead.
4. Run the tests, ONE CRATE AT A TIME, in this order, each to its own log:
   coagent-proto, coagent-crypto, coagent-roster, coagent-audit, coagent-policy, coagent-ipc, coagent-hook, coagent-mcp, coagent-relay, coagent-cli
   cargo test --locked -p <crate> 2>&1 | Tee-Object C:\c2c\logs\wo2-<crate>.log
   Do NOT run ignored tests. A crate whose tests take more than 30 minutes: stop it (Ctrl+C), record how far it got, and go on.
   coagent-cli and coagent-relay may depend on the background program or on Unix behaviour; a build or test failure there is a RESULT, not a problem for you to solve.
5. For every crate: every "test result:" line, and for each FAILED test its name and the first 15 lines of its panic or error, verbatim. Then a one-line summary per crate (passed / failed / ignored, or "did not build" with the first error).
6. Do NOT change any source file, commit, push or fix anything. Fixing is another agent's job, and your exact failures are what it needs.

REPLY by mail to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-2 results": the hash and HEAD checks, the build result, the per-crate table, and the failure excerpts. Plain text; long logs stay in C:\c2c\logs. Then tell the owner on screen that you are done, and that the next work order will come by mail.
