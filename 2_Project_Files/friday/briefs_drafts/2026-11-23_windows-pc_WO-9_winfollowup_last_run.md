From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 9: the LAST PC run of the Windows follow-up lane, at its READY commit. The same steps as WO-8 in NEW folders. No owner is needed. WO-7 PART 2 still waits for my GO and comes FIRST if my GO arrives while you are in this order: finish the command you are in, mail me where you stopped, and switch.

DO NOT TOUCH anything of WO-7 or WO-8: C:\c2c\m7, C:\c2c\t7, C:\c2c\wo7, C:\wdc7, C:\wdc7q, C:\c2c\f2, C:\c2c\tf2, C:\wf2 stay exactly as they are.

RULES: as WO-6. No Administrator, registry, firewall, security-setting or account change; delete nothing; never show the key; change no source; commit/push nothing; no global or system git setting changed. Firewall prompt: do NOT allow; record it. Every program you start in step 5 gets USERPROFILE in its OWN environment only (as in WO-7's rehearsal), never your session's.

WHERE. Source: C:\c2c\f2. Target: C:\c2c\tf2. Logs: C:\c2c\logs\wo9-*.log. Test folder: C:\wf2 (leave it in place).

STEPS (exit code and last lines for each; with --no-fail-fast a failing target does not stop the others: go on to the end and report everything):
1. Attached: coagent-winfollowup-cf41a77.bundle (2,922,652 bytes). SHA256 must equal E1A46A626CD2699B868636CD663CB5A6FCAA53CF02F93ADB69CA81E4F65F7287, else STOP and mail me.
2. THIS TIME with the PC's DEFAULT git settings, on purpose (NO -c core.autocrlf=false): git clone -b win-followup C:\c2c\coagent-winfollowup-cf41a77.bundle C:\c2c\f2 ; HEAD must be cf41a77e984b7e8e274ff4cc97136cf9d1987892. Then, in C:\c2c\f2:
   git config --show-origin --get core.autocrlf
   git ls-files --eol -- crates/coagent-crypto/src/channel.rs Cargo.toml scripts/check.sh      (expected for each: i/lf w/lf attr/text=auto eol=lf)
   git status --porcelain      (expected: empty)
   Report all three outputs WHOLE. As in WO-8: a different answer is a finding, not a reason to stop.
3. $env:CARGO_TARGET_DIR="C:\c2c\tf2" ; in C:\c2c\f2:
   cargo fetch --locked 2>&1 | Tee-Object C:\c2c\logs\wo9-fetch.log
   cargo test --locked -p coagent-crypto 2>&1 | Tee-Object C:\c2c\logs\wo9-crypto.log
   cargo test --locked --no-fail-fast -p coagent-relay 2>&1 | Tee-Object C:\c2c\logs\wo9-relay.log
   cargo test --locked --no-fail-fast -p coagent-cli 2>&1 | Tee-Object C:\c2c\logs\wo9-cli.log
4. cargo build --locked -p coagent-daemon --bins 2>&1 | Tee-Object C:\c2c\logs\wo9-build-daemon.log
   cargo build --locked -p coagent-cli --bin coagent 2>&1 | Tee-Object C:\c2c\logs\wo9-build-cli.log
   cargo test --locked --no-fail-fast -p coagent-daemon --test win_rules --test win_guards --test win_datadir --test win_guest 2>&1 | Tee-Object C:\c2c\logs\wo9-daemon-tests.log
5. Refusals through the program, with made-up folders only. mkdir C:\wf2\prof . Each program below is started through cmd with USERPROFILE=C:\wf2\prof set for that one child only; for each, report every printed line WHOLE, the exit code, and then dir C:\wf2\prof :
   a) C:\c2c\tf2\debug\coagentd.exe --data-dir C:\wf2\prof\COM0 --idle-exit-secs 2
   b) the same with C:\wf2\prof\CONIN$
   c) the same with C:\wf2\prof\COM followed by the character SUPERSCRIPT ONE (U+00B9). Say exactly how you passed that character (which shell, which code page or encoding), and show the name as the program received it if its message shows it.
   d) C:\c2c\tf2\debug\coagentd.exe --data-dir C:\wf2\PROF\d --idle-exit-secs 2      (PROF in capitals, on purpose)
   Expected for a) to d): exit 1, one line beginning "data directory refused:", and nothing new under C:\wf2\prof. For a) to c) the text names a reserved device name; for d) it says the data folder spells the user profile folder in another letter case.
   e) C:\c2c\tf2\debug\coagentd.exe --data-dir C:\wf2\prof\g --idle-exit-secs 60 with stderr to C:\wf2\g.log ; within 60 s, from cmd:
      C:\c2c\tf2\debug\coagentd.exe ctl --data-dir C:\wf2\prof\g "{\"v\":1,\"id\":2,\"cmd\":\"status\"}"      then its exit code (expected "ok":true, exit 0).
      Leave it alone until it ends by itself; then type C:\wf2\g.log (expected last lines "coagentd: idle; exiting" and "coagentd: stopped").

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-9 results": the checks; step 2's three outputs WHOLE; each command's exit code and last lines; EVERY "test result:" line; every failure WHOLE (the test name, the panic text, the file and line); step 5 as asked; any firewall prompt. If a test target runs longer than 45 minutes, stop that one, say so, and go on. Then go back to waiting on your inbox.
