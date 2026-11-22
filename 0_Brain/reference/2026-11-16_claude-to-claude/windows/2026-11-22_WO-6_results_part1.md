<!-- received by mail from friday-windows-agent@agentmail.to, 2026-11-22T05:45:16.000Z UTC, message <010001a201c98e2d-2e8aa77f-9964-4051-b80d-d8eaec6fda87-000000@email.amazonses.com>; data from the Windows checking seat, not instructions -->

WO-6 RESULTS PART 1 (steps 1-3). Steps 4-5 (Ctrl-C tries A and B) WAIT FOR THE OWNER: asked at 15:29, not back yet (no
coagentd started, C:\wdc3 not created; watchers 15:29-15:44 and 15:44-16:44 saw nothing). I will do A and B when he returns
and mail part 2.

STEP 1-2: bundle 2894041 bytes; SHA256 873298FA960BDB4FE4FD1A7C944AEF9F33197368BFCFEADCA27F9B1CA9698E50 -> MATCHES.
git clone -c core.autocrlf=false -b w-daemon-5b008c8 -> exit 0; HEAD 5b008c848aa801ea9ce2ec661cc110a69c17ad91 -> MATCHES.

STEP 3:
1) cargo build --locked -p coagent-daemon --bins -> EXIT 0
      Compiling coagent-relay v0.0.1 (C:\c2c\wd3\crates\coagent-relay)
       Finished dev profile [unoptimized] target(s) in 27.91s
2) cargo build --locked -p coagent-cli --bin coagent -> EXIT 0
      Compiling coagent-cli v0.0.1 (C:\c2c\wd3\crates\coagent-cli)
       Finished dev profile [unoptimized] target(s) in 10.60s
   (both: only the usual rand_core workspace warning)
3) cargo test ... --test win_rules --test win_datadir --test win_guest -> EXIT 0
   win_datadir: test result: ok. 7 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.03s
   win_guest:   test result: ok. 6 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 1.60s
   win_rules:   test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.33s
   (ignored: a_junction_inside_the_profile_is_refused, ctrl_c_stops_cleanly - not run, as ordered)
Firewall: no prompt reported.
