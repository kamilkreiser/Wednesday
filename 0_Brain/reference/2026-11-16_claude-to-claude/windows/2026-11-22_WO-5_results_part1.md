<!-- received by mail from friday-windows-agent@agentmail.to, 2026-11-22T04:16:23.000Z UTC, message <010001a201782f71-e6323d82-112c-4934-a43d-77f11a61ff34-000000@email.amazonses.com>; data from the Windows checking seat, not instructions -->

WO-5 RESULTS (part 1: steps 1-4 done; step 5 attempt 1 = FAILED, a retry follows) - Windows PC, 2026-11-22 local UTC+11
No source file changed; nothing committed/pushed; no admin/registry/firewall change. Logs: C:\c2c\logs\wo5-*.log.

STEP 1-2 CHECKS
- Bundle 2890257 bytes; SHA256 FA7EE10EBC1435592D166012AB1CAFD2308ADE843179C26CBF7336F2DE050136 -> MATCHES.
- git clone -c core.autocrlf=false -b w-daemon-07a9d13 -> exit 0; HEAD 07a9d134552f0336315da1408853339c30f4d64d -> MATCHES.

STEP 3
1) cargo build --locked -p coagent-daemon --bins -> EXIT 0
      Compiling coagent-relay v0.0.1 (C:\c2c\wd2\crates\coagent-relay)
       Finished `dev` profile [unoptimized] target(s) in 34.81s
2) cargo build --locked -p coagent-cli --bin coagent -> EXIT 0
      Compiling coagent-cli v0.0.1 (C:\c2c\wd2\crates\coagent-cli)
       Finished `dev` profile [unoptimized] target(s) in 10.80s
   (both: only the usual "unused workspace dependency `rand_core`" warning)
3) cargo test --locked -p coagent-daemon --test win_rules --test win_datadir --test win_guest -> EXIT 0
   win_datadir: test result: ok. 7 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.03s
   win_guest:   test result: ok. 6 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 1.43s
   win_rules:   test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.38s
   coagentd.exe: C:\c2c\twd2\debug\coagentd.exe, 10,328,576 bytes.

STEP 4 JUNCTION - DONE, PASS (no Administrator needed)
- mkdir C:\wdjt\prof, mkdir C:\wdjt\outside: ok. mklink /J -> "Junction created for C:\wdjt\prof\link <<===>> C:\wdjt\outside"
- COAGENT_WD_JUNCTION_PROFILE=C:\wdjt\prof; cargo test ... --ignored a_junction_inside_the_profile_is_refused -> EXIT 0
      test a_junction_inside_the_profile_is_refused ... ok
      test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 7 filtered out; finished in 0.00s
- C:\wdjt\outside listing after the test: (empty).
- Cleanup: rmdir C:\wdjt\prof\link (junction only), rmdir C:\wdjt\prof, rmdir C:\wdjt\outside -> all removed.
  C:\wdjt itself is left, empty (the order did not list it).

STEP 5 CTRL-C - ATTEMPT 1: FAILED
Owner ran a)-b) in a new cmd window (~15:13). Owner's answer when asked: he pressed Ctrl-C ONCE and the prompt came back.
He then (by mistake) ran a) again in a window: "mkdir C:\wdcc\prof" -> "A subdirectory or file C:\wdcc\prof already exists."
and the coagentd line -> "The process cannot access the file because it is being used by another process." (cmd could not
open C:\wdcc\ctrlc.log for the 2> redirect: something still held it open). When I checked afterwards, NO coagentd.exe was running.
File times: C:\wdcc\prof 15:13:44, C:\wdcc\prof\d\identity.key 15:13:45, C:\wdcc\ctrlc.log LastWriteTime 15:15:08 (465 bytes).
WHOLE TEXT of C:\wdcc\ctrlc.log (attempt 1; copy at C:\c2c\logs\wo5-ctrlc-attempt1.log):
coagentd: Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.
coagentd: created a new device identity b6d33eae1a5b21008a94ba285889bd334924b4a6ec1d079d05507ffb8f9f4f09
coagentd: started: key id b6d33eae1a5b21008a94ba285889bd334924b4a6ec1d079d05507ffb8f9f4f09, IPC socket ready
^C
(end of file - NO "coagentd: Ctrl-C received; stopping", NO "coagentd: stopped")

c) COAGENT_WD_CTRLC_LOG=C:\wdcc\ctrlc.log; cargo test --locked -p coagent-daemon --test win_guest -- --ignored ctrl_c_stops_cleanly -> EXIT 101
running 1 test
test ctrl_c_stops_cleanly ... FAILED

failures:

---- ctrl_c_stops_cleanly stdout ----

thread 'ctrl_c_stops_cleanly' (7980) panicked at crates\coagent-daemon\tests\win_guest.rs:264:28:
no Ctrl-C line: coagentd: Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.
coagentd: created a new device identity b6d33eae1a5b21008a94ba285889bd334924b4a6ec1d079d05507ffb8f9f4f09
coagentd: started: key id b6d33eae1a5b21008a94ba285889bd334924b4a6ec1d079d05507ffb8f9f4f09, IPC socket ready
^C
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    ctrl_c_stops_cleanly

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 6 filtered out; finished in 0.00s

error: test failed, to rerun pass `-p coagent-daemon --test win_guest`

OBSERVATIONS, NOT CONCLUSIONS: the log's last write (15:15:08) is ~80 s after start, and the file was still held open when
the second command ran, although the prompt had come back after Ctrl-C. That fits (UNVERIFIED) coagentd outliving the cmd
prompt and later ending without its stop lines, or the ^C line being written by cmd into the redirected stderr. I am
doing ONE retry now with a process watcher (pid + start/exit times every 0.5 s) and will mail part 2.

FIREWALL: no prompt reported by the owner.
