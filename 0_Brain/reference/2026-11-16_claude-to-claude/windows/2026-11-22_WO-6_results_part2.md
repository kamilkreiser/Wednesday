<!-- received by mail from friday-windows-agent@agentmail.to, 2026-11-22T05:51:50.000Z UTC, message <010001a201cf90ec-4249cae6-9997-4279-b8ed-dceccc687ef0-000000@email.amazonses.com>; data from the Windows checking seat, not instructions -->

WO-6 RESULTS PART 2: CTRL-C TRIES A AND B - BOTH PASS
(Part 1, steps 1-3 all green, was mailed earlier: hash + HEAD match, both builds EXIT 0, 26 passed / 0 failed / 2 ignored.)

Key pressed: the owner was told each time to press Ctrl + C (Ctrl key with the C key, NOT Break/Pause) ONCE, and only after I
had seen the "started" line in the log. He reported nothing else printed in the daemon's window (when asked, he gave only the
%ERRORLEVEL% number). Same cmd window used for A and B (parent pid 15296). No firewall prompt reported.

TRY A (fresh folder C:\wdc3\prof\a)
%ERRORLEVEL%: 0
Watcher log WHOLE (C:\c2c\logs\wo6-watch-a.log):
watch started 16:48:20.823
16:48:20.944  coagentd: []  log bytes=none
16:49:03.597  coagentd: []  log bytes=0
16:49:04.726  coagentd: [pid=17380 parent=15296 started=16:49:04.314]  log bytes=463
16:49:31.860  coagentd: []  log bytes=517
16:49:31.861  coagentd gone; watcher stops in 5 s
watch ended 16:49:36.873
C:\wdc3\a.log WHOLE:
coagentd: Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.
coagentd: created a new device identity f3c3c0ad44b7567237503d1112fbd9814389fae677237d9a50530db46530fa9b
coagentd: started: key id f3c3c0ad44b7567237503d1112fbd9814389fae677237d9a50530db46530fa9b, IPC socket ready
coagentd: Ctrl-C received; stopping
coagentd: stopped
Test (COAGENT_WD_CTRLC_LOG=C:\wdc3\a.log ... --ignored ctrl_c_stops_cleanly) -> EXIT 0
test ctrl_c_stops_cleanly ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 6 filtered out; finished in 0.00s


TRY B (same folder C:\wdc3\prof\a reused)
%ERRORLEVEL%: 0
Watcher log WHOLE (C:\c2c\logs\wo6-watch-b.log):
watch started 16:49:54.824
16:49:54.936  coagentd: []  log bytes=none
16:50:40.902  coagentd: [pid=15464 parent=15296 started=16:50:40.812]  log bytes=358
16:51:04.120  coagentd: []  log bytes=412
16:51:04.121  coagentd gone; watcher stops in 5 s
watch ended 16:51:09.130
C:\wdc3\b.log WHOLE:
coagentd: Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.
coagentd: started: key id f3c3c0ad44b7567237503d1112fbd9814389fae677237d9a50530db46530fa9b, IPC socket ready
coagentd: Ctrl-C received; stopping
coagentd: stopped
Test (COAGENT_WD_CTRLC_LOG=C:\wdc3\b.log ... --ignored ctrl_c_stops_cleanly) -> EXIT 0
test ctrl_c_stops_cleanly ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 6 filtered out; finished in 0.00s


Notes: each process was gone at the watcher's first poll after the log grew to its final size (A: log 517 bytes and process gone
at 16:49:31.860; B: 412 bytes and gone at 16:51:04.120), i.e. within 0.5 s of writing "stopped". No "^C" line in either log.
C:\wdc3 left in place as ordered.
