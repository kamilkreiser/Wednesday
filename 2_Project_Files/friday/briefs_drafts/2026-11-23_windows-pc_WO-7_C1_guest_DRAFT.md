DRAFT, NOT ISSUED.

NOTE TO FRIDAY (remove before sending). Fill <<MAIN SHA>>, <<BUNDLE NAME>>, <<BYTES>>, <<SHA256>> after tonight's merge and bundle; re-read the Mac's address at T-15 and fix <<HOST IP>> (192.168.7.98 measured 2026-11-22 20:06). <<HOST LINE>> is NEVER filled in this mail: it holds the link secret (lan.md:46-48; workspace rule: no secrets in mail). The owner types or pastes it at the prompt of join.cmd, in his own window, at the session. Plan: 2026-11-23_C1_first-link_plan_DRAFT.md.

From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 7: stage C1, the FIRST link across machines. coagentd.exe is the GUEST; the Mac hosts the relay on the home network. Then C2 if time.

AUTHORITY. The owner's standing word for the Windows lane, and his two rulings of 2026-11-20: card general-c2c-win-mac-relay-home-network-1120 ("Yes, for each Windows test session": the Mac's relay may listen on the home network for this session, stopped at its end) and card general-c2c-win-first-link-ungated-1120 = a (the first link may run on this PC without CoAgent's gate). No Claude Code session talks over the link today; you run the program and its ctl command only.

RULES: as WO-6. No Administrator, registry, firewall, security-setting or account change; delete nothing; never show the key; change no source; commit/push nothing. This PC only dials OUT, so no firewall prompt is expected. If one appears: do NOT answer it yourself; tell the owner it is not expected for an outgoing-only program; he decides at the screen (Cancel is the expected answer); record its exact text and his choice. THE INVITATION LINE: never put it in a mail, a log, a file or your own conversation; the owner enters it only at join.cmd's prompt. Ctrl-C ONCE only (a second one ends the program mid-stop).

WHERE. Source: C:\c2c\m7. Target: C:\c2c\t7 (short: long paths are off). Logs: C:\c2c\logs\wo7-*.log. Helper files: C:\c2c\wo7\. Test folder: C:\wdc7 (made-up profile C:\wdc7\prof, data folder C:\wdc7\prof\g; leave it all in place at the end). The Mac: <<HOST IP>>, port 7443.

PART 1 (now, without the owner; mail "PART 1" when done):
1. Attached: <<BUNDLE NAME>> (<<BYTES>> bytes), a bundle of the project's MERGED main. Download as before. SHA256 must equal <<SHA256>>, else STOP and mail me.
2. git clone -c core.autocrlf=false -b main C:\c2c\<<BUNDLE NAME>> C:\c2c\m7 ; HEAD must be <<MAIN SHA>>.
3. $env:CARGO_TARGET_DIR="C:\c2c\t7" ; in C:\c2c\m7, EXACTLY:
   cargo build --locked -p coagent-daemon --bins 2>&1 | Tee-Object C:\c2c\logs\wo7-build-daemon.log
   cargo test --locked -p coagent-daemon --test win_rules --test win_datadir --test win_guest 2>&1 | Tee-Object C:\c2c\logs\wo7-tests.log
   Expected as WO-6: exit 0; win_datadir 7 passed 1 ignored; win_guest 6 passed 1 ignored; win_rules 13 passed. Any other count: STOP and mail me.
4. Write these six files in C:\c2c\wo7\, EXACTLY (each starts with @echo off):
   status.cmd:
     @echo off
     C:\c2c\t7\debug\coagentd.exe ctl --data-dir C:\wdc7\prof\g "{\"v\":1,\"id\":1,\"cmd\":\"status\"}"
     echo exit %ERRORLEVEL%
   join.cmd:
     @echo off
     set /p L=Paste or type the line from the Mac, then press Enter: 
     C:\c2c\t7\debug\coagentd.exe ctl --data-dir C:\wdc7\prof\g "{\"v\":1,\"id\":2,\"cmd\":\"join\",\"args\":{\"blob\":\"%L%\"}}" > C:\c2c\logs\wo7-join.log 2>&1
     echo exit %ERRORLEVEL% >> C:\c2c\logs\wo7-join.log
     set L=
     type C:\c2c\logs\wo7-join.log
   send-request.cmd:
     @echo off
     C:\c2c\t7\debug\coagentd.exe ctl --data-dir C:\wdc7\prof\g "{\"v\":1,\"id\":3,\"cmd\":\"send\",\"args\":{\"kind\":\"request\",\"text\":\"C2X-1 request from Windows: please reply\"}}"
     echo exit %ERRORLEVEL%
   read.cmd:
     @echo off
     C:\c2c\t7\debug\coagentd.exe ctl --data-dir C:\wdc7\prof\g "{\"v\":1,\"id\":4,\"cmd\":\"inbox_read\"}"
     echo exit %ERRORLEVEL%
   ack.cmd (argument: the "ack" number from read.cmd):
     @echo off
     C:\c2c\t7\debug\coagentd.exe ctl --data-dir C:\wdc7\prof\g "{\"v\":1,\"id\":5,\"cmd\":\"inbox_ack\",\"args\":{\"upto\":%1}}"
     echo exit %ERRORLEVEL%
   reply.cmd (argument: the "id" of the Mac's request, from read.cmd):
     @echo off
     C:\c2c\t7\debug\coagentd.exe ctl --data-dir C:\wdc7\prof\g "{\"v\":1,\"id\":6,\"cmd\":\"send\",\"args\":{\"kind\":\"reply\",\"re\":\"%1\",\"text\":\"C2X-4 reply from Windows\"}}"
     echo exit %ERRORLEVEL%
   join.cmd's output holds no secret (the reply is paired / peer key id / session id, or a fixed error text that never repeats the input); the line itself is never echoed (@echo off) and the variable is cleared.
5. Read-only network facts, to C:\c2c\logs\wo7-net.log: Get-NetIPConfiguration ; Get-NetIPAddress -AddressFamily IPv4 (the prefix length of each address) ; Find-NetRoute -RemoteIPAddress <<HOST IP>> . Change nothing. If a command asks for elevation, skip it and say so.

PART 2 (with the OWNER, when Friday says the Mac's relay is up). START YOUR PROCESS WATCHER FIRST (pid, start and end times of coagentd.exe every 0.5 s, to C:\c2c\logs\wo7-watch.log). Guide the owner on screen, in plain words; record the local time of every step.
6. The owner, in a NEW Command Prompt (window W1), types:
     mkdir C:\wdc7\prof
     set USERPROFILE=C:\wdc7\prof
     C:\c2c\t7\debug\coagentd.exe --data-dir C:\wdc7\prof\g --idle-exit-secs 86400 2> C:\wdc7\g.log
   YOU check (type C:\wdc7\g.log) for the Windows notice, "created a new device identity", and "started: … IPC socket ready". If the window returns to its prompt instead: STOP; record g.log WHOLE.
7. YOU: Test-NetConnection <<HOST IP>> -Port 7443 . Must show TcpTestSucceeded : True. If False: STOP; record the whole output and step 5's log; mail me.
8. YOU: cmd /c C:\c2c\wo7\status.cmd . Must show "ok":true and exit 0. If it prints a usage text, "malformed", "bad_args" or "cannot connect": STOP; record the exact output. (This proves the quoting before the line is used.)
9. Tell the owner: "Run C:\c2c\wo7\join.cmd in a NEW Command Prompt (window W2) and enter the line from the Mac at its prompt." The line is <<HOST LINE>>: he brings it himself, you never see it. It is valid 600 s and once only. Then type C:\c2c\logs\wo7-join.log . Expected: "ok":true with "paired". If "invite not readable" or "invite_refused": tell me; the Mac makes a new line and the owner runs join.cmd again (record each try).
10. YOU: status.cmd every 5 s for up to 60 s, until "connected":true inside "session". Mail me "CONNECTED" with the time at once (short mail, no line, no key). If not connected after 60 s: STOP; record the last status WHOLE.
11. C2, only when I say so (I run the Mac's half): send-request.cmd ; then, when I say the Mac replied: read.cmd , then ack.cmd <ack> ; then, when I say the Mac sent a request: read.cmd , ack.cmd <ack> , reply.cmd <id> . Record every reply line WHOLE.
12. When I say stop: the owner presses Ctrl-C ONCE in W1 (the C key, NOT Break/Pause) and types echo %ERRORLEVEL% in W1. Then YOU: findstr /c:"C2X-" C:\wdc7\g.log (the count must be 0) and type C:\wdc7\g.log .
   Expected: g.log ends "coagentd: Ctrl-C received; stopping" then "coagentd: stopped"; %ERRORLEVEL% 0; the process gone within seconds.

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-7 results" (body line 1 "PART 1" or "PART 2"): the checks; each command's exit code and last lines; EVERY "test result:" line; wo7-net.log WHOLE; the Test-NetConnection output WHOLE; every status, join-log, send, read and ack reply WHOLE; the time of each step; g.log WHOLE; the watcher log WHOLE; %ERRORLEVEL%; the findstr count; any warning on starting the program; any firewall prompt (exact text, the owner's choice). NEVER the invitation line or the key. Then go back to waiting on your inbox.
