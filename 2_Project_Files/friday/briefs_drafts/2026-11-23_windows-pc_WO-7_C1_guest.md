From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 7: stage C1, the FIRST link across machines. coagentd.exe on this PC is the GUEST; the Mac hosts the relay on the home network. PART 1 is for NOW and needs no owner. PART 2 waits for my mail "WO-7 PART 2: GO" (the owner will be at both machines then).

AUTHORITY. The owner's standing word for the Windows lane, and his two rulings of 2026-11-20: card general-c2c-win-mac-relay-home-network-1120 ("Yes, for each Windows test session": the Mac's relay may listen on the home network for the session and is stopped at its end) and card general-c2c-win-first-link-ungated-1120 = a (the first link may run on this PC without CoAgent's gate). No Claude Code session talks over the link in this work order; you run the program and its ctl command only.

RULES: as WO-6. No Administrator, registry, firewall, security-setting or account change; delete nothing; never show the key; change no source; commit/push nothing. This PC only dials OUT, so no firewall prompt is expected. If one appears: do NOT answer it yourself; tell the owner it is not expected for an outgoing-only program; he decides at the screen (Cancel is the expected answer); record its exact text and his choice. THE INVITATION LINE holds the link's secret: never put it in a mail, a log or your own conversation, and never open, type or print the file that carries it; only join.cmd reads it. Ctrl-C ONCE only (a second one ends the program mid-stop).

WHERE. Source: C:\c2c\m7. Target: C:\c2c\t7 (short: long paths are off). Logs: C:\c2c\logs\wo7-*.log. Helper files: C:\c2c\wo7\. Session folder for PART 2: C:\wdc7 (made-up profile C:\wdc7\prof, data folder C:\wdc7\prof\g). Rehearsal folder for PART 1: C:\wdc7q (made-up profile C:\wdc7q\prof, data folder C:\wdc7q\prof\g). Leave both in place at the end. The Mac is expected at 192.168.7.98, port 7443 (measured 2026-11-22 21:38 on the Mac: mask 255.255.252.0, its firewall off); my GO mail confirms the address on the day.

WHAT I MEASURED on the Mac tonight at this same commit, on loopback (so you know what a good answer looks like): status before a join prints "ok":true with "session":null and exits 0; a join with a real line prints "paired":true; both sides showed "connected":true 2 seconds later; an unreadable line prints the fixed text {"error":{"code":"invite_refused","message":"invite not readable"}...} and exits 3; a request that is not JSON prints "request is not JSON" and exits 3; a wrong argument count prints the usage and exits 2; no program running prints "coagentd ctl: cannot connect" and exits 1; a reply without "re" is refused ("reply needs `re`: the id answered"); a program started with --idle-exit-secs N and left alone logs "coagentd: idle; exiting" then "coagentd: stopped". A real line is 359 characters (letters, digits, "-", "_", "=" and the two spaces of "coagent join "). None of this has run on Windows: say plainly where the PC differs.

PART 1 (now; mail me "PART 1" when done):
1. Attached: coagent-main-3337192.bundle (2,894,825 bytes), a bundle of the project's MERGED main. Download as before. SHA256 must equal 4D1B8E4702F173C5B7B0B2604483C7C7A90FEF0B29607F212AF6855FBFAAE0CF, else STOP and mail me.
2. git clone -c core.autocrlf=false -b main C:\c2c\coagent-main-3337192.bundle C:\c2c\m7 ; HEAD must be 33371921670acfcb6fc7634d0c4eacafa9800a8d.
3. $env:CARGO_TARGET_DIR="C:\c2c\t7" ; in C:\c2c\m7, EXACTLY:
   cargo build --locked -p coagent-daemon --bins 2>&1 | Tee-Object C:\c2c\logs\wo7-build-daemon.log
   cargo test --locked -p coagent-daemon --test win_rules --test win_datadir --test win_guest 2>&1 | Tee-Object C:\c2c\logs\wo7-tests.log
   Expected as WO-6: exit 0; win_datadir 7 passed 1 ignored; win_guest 6 passed 1 ignored; win_rules 13 passed. Any other count: STOP and mail me.
4. Write these six files in C:\c2c\wo7\ :
   status.cmd:
     @echo off
     C:\c2c\t7\debug\coagentd.exe ctl --data-dir C:\wdc7\prof\g "{\"v\":1,\"id\":1,\"cmd\":\"status\"}"
     echo exit %ERRORLEVEL%
   join.cmd (argument: the full path of the one-line text file that holds the line; with no argument it asks for the line):
     @echo off
     set L=
     if "%~1"=="" goto ask
     set /p L=<"%~1"
     goto run
     :ask
     set /p L=Paste the line from the Mac, then press Enter: 
     :run
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
   join.cmd's output holds no secret (the answer is paired / peer key id / session id, or a fixed error text that never repeats the input); the line is never echoed and the variable is cleared.
5. REHEARSAL, by yourself, so that nothing about quoting is first tried with the owner waiting. It uses a program YOU start in the rehearsal folder and that ends by itself.
   a) Make copies of status.cmd and join.cmd named status-q.cmd and join-q.cmd in which every C:\wdc7\ reads C:\wdc7q\ and wo7-join.log reads wo7-joinq.log. Change nothing else.
   b) Write C:\c2c\wo7\fake-line.txt: ONE line, the words "coagent join " followed by the letter A 346 times (359 characters in all; it is NOT a real line and holds no secret).
   c) mkdir C:\wdc7q\prof ; start C:\c2c\t7\debug\coagentd.exe --data-dir C:\wdc7q\prof\g --idle-exit-secs 60 with stderr to C:\wdc7q\g.log, as a background process whose OWN environment has USERPROFILE=C:\wdc7q\prof (for that one child process only: never for your session, the user or the machine). Record its pid and start time.
   d) cmd /c C:\c2c\wo7\status-q.cmd  -> expected "ok":true, "session":null, a "data_dir_check" text, exit 0.
   e) cmd /c C:\c2c\wo7\join-q.cmd C:\c2c\wo7\fake-line.txt  -> expected the fixed text "invite not readable" (code invite_refused), exit 3. That answer proves the whole 359 characters reached the program as one JSON text. "request is not JSON", the usage text or "bad_args" instead means the quoting or the file read is wrong: find out which, correct the HELPER files only (all six in the same way), and tell me the exact final text of each file.
   f) Leave it alone. Expected within about 60 s of your last call: g.log ends "coagentd: idle; exiting" then "coagentd: stopped", and the process is gone. Record the time. If it is still alive 3 minutes after your last call: record that, then end THAT ONE pid (your own test process, its folder is a rehearsal folder) and say so.
   g) cmd /c C:\c2c\wo7\status-q.cmd again -> expected "cannot connect", exit 1.
6. Read-only network facts, to C:\c2c\logs\wo7-net.log: Get-NetIPConfiguration ; Get-NetIPAddress -AddressFamily IPv4 (the prefix length of each address) ; Find-NetRoute -RemoteIPAddress 192.168.7.98 . Change nothing. If a command asks for elevation, skip it and say so. In your mail say in one line which adapter and which of this PC's addresses Windows would use to reach 192.168.7.98.

PART 2 (with the OWNER; ONLY after my mail "WO-7 PART 2: GO", which gives the Mac's address for the day). START YOUR PROCESS WATCHER FIRST (pid, start and end times of coagentd.exe every 0.5 s, to C:\c2c\logs\wo7-watch.log). Guide the owner on screen, in plain words; record the local time of every step.
7. The owner, in a NEW Command Prompt (window W1), types:
     mkdir C:\wdc7\prof
     set USERPROFILE=C:\wdc7\prof
     C:\c2c\t7\debug\coagentd.exe --data-dir C:\wdc7\prof\g --idle-exit-secs 86400 2> C:\wdc7\g.log
   YOU check (type C:\wdc7\g.log) for the Windows notice, "created a new device identity", and "started: ... IPC socket ready". If the window returns to its prompt instead: STOP; record g.log WHOLE.
8. YOU: Test-NetConnection <the Mac's address from my GO mail> -Port 7443 . Must show TcpTestSucceeded : True. If False: STOP; record the whole output and step 6's log; mail me.
9. YOU: cmd /c C:\c2c\wo7\status.cmd . Must show "ok":true and exit 0. Anything else: STOP; record the exact output.
10. The owner brings a USB stick from the Mac with ONE file on it, c2c-line.txt. Find its drive letter read-only (Get-Volume) and tell the owner to type, in a NEW Command Prompt (window W2), with that letter in place of X:
     C:\c2c\wo7\join.cmd X:\c2c-line.txt
   Do NOT open, type or print that file yourself. The line is valid 600 s and once only. Expected on his screen: "ok":true with "paired":true. If "invite not readable" or "invite_refused": mail me at once; the Mac makes a new line and the owner runs the same command again (record each try). After a join the line is spent; the owner may remove the file himself, you delete nothing.
11. YOU: status.cmd every 5 s for up to 60 s, until "connected":true inside "session". Mail me "CONNECTED" with the time at once (short mail, no line, no key). If not connected after 60 s: STOP; record the last status WHOLE.
12. C2, only when I say so by mail (I run the Mac's half): send-request.cmd ; then, when I say the Mac replied: read.cmd , then ack.cmd <ack> ; then, when I say the Mac sent a request: read.cmd , ack.cmd <ack> , reply.cmd <id> . Record every answer line WHOLE.
13. When I say stop: the owner presses Ctrl-C ONCE in W1 (the C key, NOT Break/Pause) and types echo %ERRORLEVEL% in W1. Then YOU: findstr /c:"C2X-" C:\wdc7\g.log (the count must be 0) and type C:\wdc7\g.log .
   Expected: g.log ends "coagentd: Ctrl-C received; stopping" then "coagentd: stopped"; %ERRORLEVEL% 0; the process gone within seconds.

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-7 results" (body line 1 "PART 1" or "PART 2").
PART 1: the checks; each command's exit code and last lines; EVERY "test result:" line; the final text of all six helper files if you changed any; every rehearsal answer WHOLE with its exit code; the rehearsal g.log WHOLE and the idle-exit time; wo7-net.log WHOLE and your one-line route answer.
PART 2: the Test-NetConnection output WHOLE; every status, join-log, send, read and ack answer WHOLE; the time of each step; g.log WHOLE; the watcher log WHOLE; %ERRORLEVEL%; the findstr count; any warning on starting the program; any firewall prompt (exact text, the owner's choice).
NEVER the invitation line or the key. Then go back to waiting on your inbox.
