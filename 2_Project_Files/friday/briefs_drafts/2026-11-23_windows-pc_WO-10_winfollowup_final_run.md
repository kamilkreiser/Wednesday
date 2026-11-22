From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 10: the FINAL PC run of the Windows follow-up lane, after its check's notes round, plus four measurements the independent check asked for. No owner is needed. WO-7 PART 2 still waits for my GO and comes FIRST if my GO arrives while you are in this order: finish the command you are in, mail me where you stopped, and switch.

Thank you for catching the slip in WO-9's protected list: it was my fault, you read it correctly, and my sender now refuses an order whose two lines share a folder. One more correction, for your own summaries: the relay result lines of WO-8 and WO-9 sum to 125 passed (5 ignored), not 128. In this reply give no per-crate total of your own: just every "test result:" line; I sum them.

DO NOT TOUCH anything of WO-7, WO-8 or WO-9: C:\c2c\m7, C:\c2c\t7, C:\c2c\wo7, C:\wdc7, C:\wdc7q, C:\c2c\f1, C:\c2c\tf1, C:\wf1, C:\c2c\f2, C:\c2c\tf2, C:\wf2 stay exactly as they are.

RULES: as WO-6. No Administrator, registry, firewall, security-setting or account change; delete nothing; never show the key; change no source; commit/push nothing; no global or system git setting changed. Firewall prompt: do NOT allow; record it. Every program you start gets USERPROFILE in its OWN environment only, never your session's. If any step asks for elevation: skip that step and say so.

WHERE. Source: C:\c2c\f3. Target: C:\c2c\tf3. Logs: C:\c2c\logs\wo10-*.log. Test folders: C:\wf3, C:\qf1, C:\qf2, C:\qf3 (leave them all in place).

PART A: the lane's own steps (with --no-fail-fast a failing target does not stop the others: go on to the end and report everything)
1. Attached: coagent-winfollowup-a074aca.bundle (2,929,757 bytes). SHA256 must equal A6ABD47F187C3893BBBF26F31648B92B8F830EAC1702AA22BD5C3AB29E27CA28, else STOP and mail me.
2. With the PC's DEFAULT git settings (NO -c core.autocrlf=false): git clone -b win-followup C:\c2c\coagent-winfollowup-a074aca.bundle C:\c2c\f3 ; HEAD must be a074aca0b544ff6fa7dbaf186c6436f7010d207b. Then, in C:\c2c\f3:
   git config --show-origin --get core.autocrlf
   git ls-files --eol -- crates/coagent-crypto/src/channel.rs Cargo.toml scripts/check.sh      (expected for each: i/lf w/lf attr/text=auto eol=lf)
   git status --porcelain      (expected: empty)
3. $env:CARGO_TARGET_DIR="C:\c2c\tf3" ; in C:\c2c\f3:
   cargo fetch --locked 2>&1 | Tee-Object C:\c2c\logs\wo10-fetch.log
   cargo test --locked --no-fail-fast -p coagent-relay 2>&1 | Tee-Object C:\c2c\logs\wo10-relay.log
   cargo test --locked --no-fail-fast -p coagent-cli 2>&1 | Tee-Object C:\c2c\logs\wo10-cli.log
4. cargo build --locked -p coagent-daemon --bins 2>&1 | Tee-Object C:\c2c\logs\wo10-build-daemon.log
   cargo build --locked -p coagent-cli --bin coagent 2>&1 | Tee-Object C:\c2c\logs\wo10-build-cli.log
   cargo test --locked --no-fail-fast -p coagent-daemon --test win_rules --test win_guards --test win_datadir --test win_guest 2>&1 | Tee-Object C:\c2c\logs\wo10-daemon-tests.log
   (win_guards has more tests than in WO-9: report its line as it is. For the relay target that holds a_closed_first_candidate_falls_through_to_the_live_second_and_says_why, also report that test's own line from the log, ok or FAILED.)
5. Refusals through the program, exactly as WO-9's step 5 but in C:\wf3 : mkdir C:\wf3\prof ; each program through cmd with USERPROFILE=C:\wf3\prof for that one child; for each, every printed line WHOLE, the exit code, then dir C:\wf3\prof :
   a) C:\c2c\tf3\debug\coagentd.exe --data-dir C:\wf3\prof\COM0 --idle-exit-secs 2
   b) the same with C:\wf3\prof\CONIN$
   c) the same with C:\wf3\prof\COM followed by U+00B9 (say how you passed it, as before)
   d) C:\c2c\tf3\debug\coagentd.exe --data-dir C:\wf3\PROF\d --idle-exit-secs 2      (PROF in capitals, on purpose)
   e) C:\c2c\tf3\debug\coagentd.exe --data-dir C:\wf3\prof\g --idle-exit-secs 60 with stderr to C:\wf3\g.log ; within 60 s, from cmd:
      C:\c2c\tf3\debug\coagentd.exe ctl --data-dir C:\wf3\prof\g "{\"v\":1,\"id\":2,\"cmd\":\"status\"}"      then its exit code. Leave it until it ends by itself; then type C:\wf3\g.log .

PART B: four measurements for the independent check (each is a finding whatever it shows; none is a reason to stop)
6. THE OTHER DEVICE NAMES. mkdir C:\qf1\prof . With USERPROFILE=C:\qf1\prof for each child, for each NAME of: LPT0, CONOUT$, CLOCK$, COM followed by U+00B2, COM followed by U+00B3, LPT followed by U+00B9, LPT followed by U+00B2, LPT followed by U+00B3, com0 (lower case), Com followed by U+00B9 followed by .txt :
   C:\c2c\tf3\debug\coagentd.exe --data-dir C:\qf1\prof\NAME --idle-exit-secs 2      then the exit code, the stderr line WHOLE, and at the end one dir C:\qf1\prof .
   Expected: each exit 1 with the reserved-device-name line; nothing made.
7. THE SPELLING THAT SHOULD ALWAYS FIT. From a Command Prompt, one child whose own environment has USERPROFILE=C:\qf1\prof and which expands that variable itself (cmd /v:on with !USERPROFILE!), running:
   C:\c2c\tf3\debug\coagentd.exe --data-dir "!USERPROFILE!\g" --idle-exit-secs 2
   Report the exact command line you used, every printed line, the exit code, and dir C:\qf1\prof . Expected: it starts, logs "idle; exiting" and "stopped" after about 2 s, exit 0, and C:\qf1\prof\g exists.
   Also, read-only, WITHOUT printing any name: is the text of your session's real USERPROFILE byte-for-byte equal to the on-disk spelling of that folder (compare in PowerShell: $env:USERPROFILE -ceq (Get-Item $env:USERPROFILE).FullName )? Report only True or False.
8. A FOLDER MARKED CASE-SENSITIVE (only if it needs NO elevation). mkdir C:\qf2 ; fsutil.exe file setCaseSensitiveInfo C:\qf2 enable . If that is refused or asks for Administrator: record the exact text, skip the rest of step 8. Otherwise: mkdir C:\qf2\ann ; mkdir C:\qf2\ANN ; then with USERPROFILE=C:\qf2\ann for the child:
   C:\c2c\tf3\debug\coagentd.exe --data-dir C:\qf2\ANN\d --idle-exit-secs 2      then the exit code, the stderr WHOLE, dir C:\qf2\ann and dir C:\qf2\ANN .
   Expected: exit 1 with the "another letter case" line; nothing made in either folder.
9. AN OLD CRLF CHECKOUT MEETING THE NEW ATTRIBUTE. The bundle of main from WO-7 is still at C:\c2c\coagent-main-3337192.bundle (read it; do not change it). With DEFAULT git settings:
   git clone -b main C:\c2c\coagent-main-3337192.bundle C:\qf3
   git -C C:\qf3 ls-files --eol -- Cargo.toml crates/coagent-crypto/src/channel.rs      (the "before": expected w/crlf)
   git -C C:\qf3 fetch C:\c2c\coagent-winfollowup-a074aca.bundle win-followup
   git -C C:\qf3 checkout FETCH_HEAD
   git -C C:\qf3 status --porcelain
   git -C C:\qf3 ls-files --eol -- Cargo.toml crates/coagent-crypto/src/channel.rs
   Report every output WHOLE (for a long status, its first 20 lines and its line count).

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-10 results": the checks; step 2's three outputs WHOLE; each command's exit code and last lines; EVERY "test result:" line under its "== name: exit=" heading as in WO-9; every failure WHOLE; steps 5 to 9 as asked; any firewall or elevation prompt. If a test target runs longer than 45 minutes, stop that one, say so, and go on. Then go back to waiting on your inbox.
