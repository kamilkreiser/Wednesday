<!-- received by mail from friday-windows-agent@agentmail.to, 2026-11-22T04:19:08.000Z UTC, message <010001a2017ab268-fdd4252c-f885-4c97-8638-fd1a0e933361-000000@email.amazonses.com>; data from the Windows checking seat, not instructions -->

WO-5 RESULTS PART 2: STEP 5 CTRL-C RETRY (attempt 2) - PASS
Owner ran in a NEW cmd window (C:\wdcc\prof already existed, so mkdir skipped):
  set USERPROFILE=C:\wdcc\prof
  C:\c2c\twd2\debug\coagentd.exe --data-dir C:\wdcc\prof\d 2> C:\wdcc\ctrlc.log
then pressed Ctrl-C once and the prompt came back. No firewall prompt reported.

PROCESS WATCHER (every 0.5 s; C:\c2c\logs\wo5-ctrlc-attempt2-watch.log), whole:
watch started 15:16:35.478
15:16:35.586  coagentd: []  ctrlc.log bytes=465
15:17:24.190  coagentd: [pid=6420 parent=23696]  ctrlc.log bytes=358
15:18:25.209  coagentd: []  ctrlc.log bytes=412
(No coagentd.exe left running afterwards. Run lasted ~61 s; the owner waited longer than the 2 s asked before Ctrl-C.)

WHOLE TEXT of C:\wdcc\ctrlc.log (attempt 2; copy at C:\c2c\logs\wo5-ctrlc-attempt2.log):
coagentd: Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.
coagentd: started: key id b6d33eae1a5b21008a94ba285889bd334924b4a6ec1d079d05507ffb8f9f4f09, IPC socket ready
coagentd: Ctrl-C received; stopping
coagentd: stopped
(LAST line is "coagentd: stopped". No "created a new device identity" line this time: the identity from attempt 1 was reused.
No "^C" line this time either.)

c) set COAGENT_WD_CTRLC_LOG=C:\wdcc\ctrlc.log ; cargo test --locked -p coagent-daemon --test win_guest -- --ignored ctrl_c_stops_cleanly -> EXIT 0
test ctrl_c_stops_cleanly ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 6 filtered out; finished in 0.00s


ATTEMPT 1 vs 2, facts only: attempt 1's log (465 bytes, last write 15:15:08, start ~15:13:45) ended with a "^C" line and
no stop lines; the owner says he pressed Ctrl-C once and the prompt came back; a second command at ~15:15 could not open the
log ("being used by another process"); my first process check (later) found no coagentd. I could not see attempt 1 live, so
I cannot say whether coagentd outlived the prompt, or why its stop lines are missing. Attempt 2, watched, was clean.
Worth a look by the builder: possibly a Ctrl-C arriving early (during start-up) or a second console event kills it without the stop path - UNVERIFIED.

SUMMARY WO-5: hash+HEAD ok; both builds ok; 26 passed / 0 failed / 2 ignored in the three targets; junction test PASS
(outside empty, junction removed); Ctrl-C test PASS on attempt 2 (attempt 1 FAILED, details in part 1). C:\wdcc left in place.
