From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 11: prepare stage C2 (a Claude Code agent on each machine). Everything here is for NOW, by yourself: no owner, NO MODEL RUN (never run `claude` with a prompt, never `claude -p`), no network beyond your mail. The live session comes later in its own work order.

AUTHORITY. The owner's standing word for the Windows lane, and card general-c2c-win-first-link-ungated-1120 = a (a first link may run on this PC without CoAgent's gate). This order starts only programs that end by themselves and connect to nothing but each other on this PC.

RULES: as WO-7. No Administrator, registry, firewall, security-setting or account change; delete nothing; never show a key; change no source; commit/push nothing; no global git setting. If any prompt or dialog appears: do not answer it; record its exact text and STOP. Never print the name of this PC's real user folder: where a path would show it, write <PROFILE>.

WHERE. Source: C:\c2c\m11. Target: C:\c2c\t11. Logs: C:\c2c\logs\wo11-*. Helper files and plugins: C:\c2c\wo11\. Rehearsal: C:\wdc11q (made-up profile C:\wdc11q\prof, data folder C:\wdc11q\prof\g). The data folder C:\wdc11\prof\g is NAMED in two files below but NOT created by this order. Leave everything in place at the end.
DO NOT TOUCH: C:\c2c\m7, C:\c2c\t7, C:\c2c\wo7, C:\c2c\f1, C:\c2c\f2, C:\c2c\f3, C:\c2c\tf1, C:\c2c\tf2, C:\c2c\tf3, C:\wdc7, C:\wdc7q, C:\wf1, C:\wf2, C:\wf3, C:\qf1, C:\qf2, C:\qf3, and every other folder that already exists.

STEPS (record the local time of each):
0. Check that NONE of C:\c2c\m11, C:\c2c\t11, C:\c2c\wo11, C:\wdc11, C:\wdc11q exists. If one does: STOP and mail me.
1. Attached: coagent-main-3164374.bundle (2,932,728 bytes), a bundle of the project's main. SHA256 must equal 187E2B7A07E102C4DA5649A9AE1AB76CEB07B38C6DEB533398BD07EBA4156A85, else STOP.
2. Default clone (main now has a root .gitattributes, so no -c option): git clone -b main C:\c2c\coagent-main-3164374.bundle C:\c2c\m11 . HEAD must be 3164374a8a20d73296558997438b97a41a7837ad. Then git status --porcelain (expected empty) and git ls-files --eol -- Cargo.toml crates/coagent-mcp/src/main.rs (expected i/lf w/lf on both, as WO-10 showed for other files).
3. $env:CARGO_TARGET_DIR="C:\c2c\t11" ; in C:\c2c\m11, EXACTLY, each with 2>&1 | Tee-Object C:\c2c\logs\wo11-<name>.log :
   cargo build --locked -p coagent-daemon --bins                      (name build-daemon)
   cargo build --locked -p coagent-cli --bin coagent                  (name build-cli)
   cargo build --locked -p coagent-mcp                                (name build-mcp)
   cargo test --locked --no-fail-fast -p coagent-daemon --test win_rules --test win_datadir --test win_guest --test win_guards   (name tests-daemon)
   cargo test --locked --no-fail-fast -p coagent-mcp                  (name tests-mcp)
   Expected tests-daemon, as WO-10 at a074aca (the code is the same; the difference is four .md files): win_datadir 7 passed 1 ignored; win_guards 5 passed; win_guest 6 passed 1 ignored; win_rules 16 passed; exit 0. Expected tests-mcp (expected, never run on Windows): 2 passed in the src\main.rs unit tests, 2 passed in tests\stdout_audit.rs, exit 0. Any other count, or any FAILED: STOP and mail me the failure whole.
   Then Get-FileHash (SHA256) and size of C:\c2c\t11\debug\coagentd.exe, coagent.exe, coagent-mcp.exe.
4. Claude Code facts, NO model run: claude --version ; claude --help > C:\c2c\logs\wo11-claude-help.txt . In your mail quote WHOLE every help line that names -p/--print, --model, --plugin-dir, --allowedTools (and how several tools are listed), --permission-mode (and its choices), --mcp-config, --strict-mcp-config. Say yes/no only: is CLAUDE_CONFIG_DIR set in your environment. Settings checksums BEFORE: SHA256 of every settings*.json in %USERPROFILE%\.claude and, if set, in CLAUDE_CONFIG_DIR, written to C:\c2c\logs\wo11-settings-before.txt with names relative to those folders (no full path).
5. Rehearsal daemon: mkdir C:\wdc11q\prof ; start, as a background process, exactly as WO-10 started its own (the made-up profile for that ONE child only):
     cmd.exe /d /c "set USERPROFILE=C:\wdc11q\prof&& C:\c2c\t11\debug\coagentd.exe --data-dir C:\wdc11q\prof\g --idle-exit-secs 120 2> C:\wdc11q\g.log"
   Record pid and start time. Write C:\c2c\wo11\status-q.cmd (WO-7's status.cmd with C:\c2c\t11 and C:\wdc11q\prof\g) and run it: expected "ok":true, "gate":"off", "session":null, a "data_dir_check" text, exit 0 (as WO-10 step 5e). Do steps 6, 7 and the rehearsal of step 9 within 2 minutes of each other (the daemon idles out 120 s after the last call).
6. coagent-mcp.exe BY HAND over stdio. Write C:\c2c\wo11\mcp-in.txt, UTF-8 WITHOUT a byte-order mark (check its first three bytes are not EF BB BF), exactly these seven lines:
     {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"t","version":"0"}}}
     {"jsonrpc":"2.0","method":"notifications/initialized"}
     {"jsonrpc":"2.0","id":2,"method":"tools/list"}
     {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"inbox_read","arguments":{}}}
     {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"send","arguments":{"kind":"request","text":"C2W-0 rehearsal"}}}
     {"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"wait","arguments":{"timeout_s":1}}}
     {"jsonrpc":"2.0","id":6,"method":"ping"}
   (Lines 1, 2 and 4's shape are the project's own test lines; the others follow the same form.) Run it from YOUR OWN shell, with your real USERPROFILE, on purpose (the agent's server will run that way):
     cmd /d /c "C:\c2c\t11\debug\coagent-mcp.exe --data-dir C:\wdc11q\prof\g < C:\c2c\wo11\mcp-in.txt > C:\c2c\logs\wo11-mcp-out1.txt 2> C:\c2c\logs\wo11-mcp-err1.txt" ; then the exit code.
   Expected, never run: it ends by itself within a few seconds, exit 0; stderr empty; SIX stdout lines (none for line 2), in any order: id 1 a result with "protocolVersion":"2025-06-18", "capabilities":{"tools":{}}, "serverInfo" name "coagent" version "0.0.1"; id 2 three tools named send, inbox_read, wait; id 3 and id 4 "isError":true with the text "coagent: the daemon refused (no_session)."; id 5 "isError":false with "coagent: no new peer messages."; id 6 "result":{}. If id 3 says "coagent: the CoAgent daemon is not running." instead: the server did not find the daemon's pipe; record it and STOP.
7. The same file once more with the data folder in another letter case (--data-dir C:\WDC11Q\prof\g), out to wo11-mcp-out2.txt / wo11-mcp-err2.txt. No expected answer: record what id 3 says (it tells us whether a differently spelled folder in the plugin finds the daemon).
8. Two plugin folders, written BY HAND (do NOT run preview\make-plugin.sh or any bash or python script):
   a) mkdir C:\c2c\wo11\plugin-q\.claude-plugin ; Copy-Item C:\c2c\m11\preview\plugin-template\.claude-plugin\plugin.json into it (byte for byte; give both SHA256).
   b) C:\c2c\wo11\plugin-q\.mcp.json, exactly:
     {
       "mcpServers": {
         "link": {
           "command": "C:\\c2c\\t11\\debug\\coagent-mcp.exe",
           "args": ["--data-dir", "C:\\wdc11q\\prof\\g"]
         }
       }
     }
   c) The same two files in C:\c2c\wo11\plugin-g, with "C:\\wdc11\\prof\\g" in .mcp.json (the session's folder; not created now).
   d) NO hooks folder in either. mkdir C:\c2c\wo11\ws-g (empty; the agent's working folder on the day).
   e) claude plugin validate C:\c2c\wo11\plugin-q and the same for plugin-g (a local check, no model run). Output WHOLE. If the command does not exist in this version, record its answer and go on.
9. Files for the day (write them; run only the rehearsal half):
   a) status.cmd and join.cmd as WO-7's, with C:\c2c\t11 and C:\wdc11\prof\g, and join's log C:\c2c\logs\wo11-join.log . join-q.cmd: join.cmd with C:\wdc11q\prof\g and wo11-joinq.log .
   b) C:\c2c\wo11\fake-line.txt: ONE line, "coagent join " followed by the letter A 350 times (363 characters, the length of the real line on 23 Nov; not a real line). Run cmd /c C:\c2c\wo11\join-q.cmd C:\c2c\wo11\fake-line.txt : expected "invite not readable" (invite_refused), exit 3 (as WO-7 part 1 at 359 characters).
   c) start-g.txt: the three lines the owner will type in W1 (as WO-7 step 7, with C:\wdc11 and C:\c2c\t11). Do NOT run them.
   d) run-agent.cmd, written, NOT run (argument 1 = the model id, which my GO mail will give):
     @echo off
     cd /d C:\c2c\wo11\ws-g
     claude -p --model %1 --plugin-dir C:\c2c\wo11\plugin-g --permission-mode manual --allowedTools "mcp__plugin_coagent_link__send mcp__plugin_coagent_link__inbox_read mcp__plugin_coagent_link__wait ToolSearch" "Use the coagent send tool, kind request, text exactly: C2W-1 request from the Windows agent: please reply. Then call the coagent wait tool with timeout_s 300, again and again, until you have received BOTH a reply whose re is the id of your message AND a request from the peer. Answer that request with the coagent send tool, kind reply, re set to the request's id, text exactly: C2W-4 reply from the Windows agent. Then print every id and text you sent and received. Use no other tool." > C:\c2c\logs\wo11-agent-day.log 2>&1
     echo exit %ERRORLEVEL% >> C:\c2c\logs\wo11-agent-day.log
   If step 4's help text shows another spelling for --allowedTools lists or for the default permission mode, say so; do NOT change the file yourself.
10. Leave the rehearsal daemon alone. Expected within about 120 s of your last call: C:\wdc11q\g.log ends "coagentd: idle; exiting" then "coagentd: stopped" and the process is gone (as WO-10 5e at 60 s). If it is alive 5 minutes after your last call: record that, end THAT pid only, say so. Then run step 6's command once more (out to wo11-mcp-out3.txt / err3): expected ids 1, 2, 6 as before and ids 3, 4, 5 "coagent: the CoAgent daemon is not running." with "isError":true.
11. Settings checksums AFTER, as in step 4, to wo11-settings-after.txt; compare with before: expected identical.

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-11 results": each step's exit code and last lines; EVERY "test result:" line; the three file hashes; step 4's help lines WHOLE and the yes/no; the rehearsal status WHOLE; mcp-out1, out2, out3 and the three err files WHOLE; both plugin.json hashes; both validate outputs WHOLE; the fake-line answer WHOLE with exit code; g.log WHOLE with the idle-exit time; the settings comparison; the final text of every file in C:\c2c\wo11 except fake-line.txt (say its length instead). Result lines only: no totals of your own. Then go back to waiting on your inbox.
