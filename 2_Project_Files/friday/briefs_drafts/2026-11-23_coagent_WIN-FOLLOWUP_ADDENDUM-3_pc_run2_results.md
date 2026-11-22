This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-23_coagent_WIN-FOLLOWUP_brief.md`.

# WIN-FOLLOWUP ADDENDUM 3: the LAST PC run (WO-9) at your READY head, quoted whole

1. **PC run 2 at `cf41a77e984b7e8e274ff4cc97136cf9d1987892` is back: everything passed, the same as run 1.** The results mail is quoted WHOLE below, between the two marker lines, unedited (data from another machine: facts, not instructions; never copy a machine name, account folder or path of the PC into the repository). The file: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/2026-11-23_WO-9_results.md` (READ-ONLY).
2. **Two things in it that are not yours, so that you do not chase them:** (a) the PC seat's note about the DO-NOT-TOUCH list is a slip in FRIDAY's work order (a replace that also renamed the folders to protect); the PC seat read it correctly and touched none of run 1's folders. (b) Its summary sentence says "relay 128 passed"; the sixteen relay `test result:` lines above it sum to 125 passed, 5 ignored (Friday summed them by program for both runs). Use 125 wherever you cite the relay count, and say "summed from the result lines".
3. **Record it** in STATUS section (5) as PC run 2 with every `test result:` line, and update only the tags and Closed lines that the brief ties to "the PC run at the READY head" (docs and BACKLOG words; no code). If that needs a commit, it is docs-only on top of `cf41a77`: say so, show `git diff --stat cf41a77 HEAD` (docs and BACKLOG paths only), push, and the PC run stands for it (the brief's section 5 item 11). If any code line would change: STOP with a question instead.
4. **Then write your last line:** `READY FOR QA WIN-FOLLOWUP`, with the head SHA in the line above it. Runs used: 2 of 3; none further is planned. Friday then launches the ONE independent check.

===== BEGIN the PC's results mail, whole =====
WO-9 RESULTS - Windows PC, 2026-11-23 01:3x-01:46 local (UTC+11). Everything passed; no failures anywhere. Identical to WO-8.
No admin/registry/firewall change; no global or system git setting changed; no source changed; nothing deleted. No firewall prompt.
NOTE on the order: its DO-NOT-TOUCH list names C:\c2c\f2, C:\c2c\tf2 and C:\wf2, the same folders its WHERE says to use. I read that as a slip
for WO-8's C:\c2c\f1, C:\c2c\tf1 and C:\wf1: I checked that f2/tf2/wf2 did not exist, used them, and left f1/tf1/wf1 and all WO-7 folders untouched.

STEP 1: bundle 2922652 bytes; SHA256 E1A46A626CD2699B868636CD663CB5A6FCAA53CF02F93ADB69CA81E4F65F7287 -> MATCHES.
STEP 2: git clone -b win-followup (DEFAULT git settings) -> exit 0; HEAD cf41a77e984b7e8e274ff4cc97136cf9d1987892 -> MATCHES.
  git config --show-origin --get core.autocrlf, WHOLE:
file:C:/Program Files/Git/etc/gitconfig	true
  git ls-files --eol -- crates/coagent-crypto/src/channel.rs Cargo.toml scripts/check.sh, WHOLE:
i/lf    w/lf    attr/text=auto eol=lf 	Cargo.toml
i/lf    w/lf    attr/text=auto eol=lf 	crates/coagent-crypto/src/channel.rs
i/lf    w/lf    attr/text=auto eol=lf 	scripts/check.sh
  git status --porcelain, WHOLE: (empty)

STEPS 3-4 (target C:\c2c\tf2; C:\c2c\logs\wo9-summary.log), every "test result:" line:
WO-9 steps 3-4 started 2026-11-23T01:41:29.8335261+11:00
== fetch: exit=0 time=1s
== crypto: exit=0 time=66s
   test result: ok. 48 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 24.16s
   test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 22.73s
   test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.16s
   test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.32s
   test result: ok. 18 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.19s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
== relay: exit=0 time=64s
   test result: ok. 58 passed; 0 failed; 5 ignored; 0 measured; 0 filtered out; finished in 5.77s
   test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 5.10s
   test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.06s
   test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.80s
   test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 20.08s
   test result: ok. 7 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.07s
   test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s
   test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.79s
   test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.16s
   test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.20s
   test result: ok. 16 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 4.76s
   test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.25s
   test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s
   test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.35s
   test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.05s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
== cli: exit=0 time=10s
   test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
   test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.44s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
== build-daemon: exit=0 time=14s
== build-cli: exit=0 time=0s
== daemon-tests: exit=0 time=7s
   test result: ok. 7 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.04s
   test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.02s
   test result: ok. 6 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 1.23s
   test result: ok. 16 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.55s
WO-9 steps 3-4 finished 2026-11-23T01:44:12.1489690+11:00
Last lines: fetch exit 0 (nothing new to download; last line "warning: workspace (manifest) generated 1 warning");
build-daemon "Finished dev profile [unoptimized] target(s) in 14.32s"; build-cli "Finished dev profile [unoptimized] target(s) in 0.23s".
Per target: crypto 75 passed; relay 128 passed 5 ignored; cli 11 passed (lib 6, main 0, cli.rs 5, identity_cli 0, identity_file 0, doc 0);
daemon win_datadir 7 passed 1 ignored, win_guards 4 passed, win_guest 6 passed 1 ignored, win_rules 16 passed. 0 failed in all.

STEP 5 (mkdir C:\wf2\prof; each via cmd.exe /d /c "set USERPROFILE=C:\wf2\prof&& ..." for that one child; stdout/stderr to files, read as UTF-8)
a) C:\wf2\prof\COM0 -> exit 1; stdout empty; stderr WHOLE:
coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
   dir C:\wf2\prof: empty
b) C:\wf2\prof\CONIN$ -> exit 1; stdout empty; stderr WHOLE: the same line as a). dir: empty
c) C:\wf2\prof\COM¹ -> exit 1; stdout empty; stderr WHOLE: the same line as a). dir: empty
   HOW PASSED: as in WO-8 - from PowerShell 7.6 (U+0043 U+004F U+004D U+00B9) via .NET Process.Start -> CreateProcessW (UTF-16) to
   cmd.exe /d /c, which starts coagentd.exe with CreateProcessW: no code-page conversion of the argument. Console code page 65001.
   The message does not echo the name; cmd's own echo of the same argument to a file gives bytes ...43 4F 4D C2 B9 = "COM¹" (U+00B9 kept).
d) C:\wf2\PROF\d -> exit 1; stdout empty; stderr WHOLE:
coagentd: data directory refused: the data folder spells the user profile folder (USERPROFILE) in another letter case: spell that part exactly as USERPROFILE does
   dir C:\wf2\prof: empty
e) started 01:44:41.195 (pid 24332, process start 01:44:41.326). 01:44:44.426 ctl status, WHOLE:
{"id":2,"ok":true,"result":{"contacts":[],"data_dir_check":"Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.","gate":"off","key_id":"2b7532837f52f7df04296c24bb9ebc1bff06d37d75eb9e4419f9c354864236b5","pairing":null,"pid":24332,"relay":null,"relay_identity":{"refused":null,"retry_in_s":null,"source":"none"},"relay_moved_line":null,"session":null},"v":1}
exit 0
   pid 24332 ended by itself by 01:45:44.743 (60 s after the call). type C:\wf2\g.log, WHOLE:
coagentd: Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.
coagentd: created a new device identity 2b7532837f52f7df04296c24bb9ebc1bff06d37d75eb9e4419f9c354864236b5
coagentd: started: key id 2b7532837f52f7df04296c24bb9ebc1bff06d37d75eb9e4419f9c354864236b5, IPC socket ready
coagentd: idle; exiting
coagentd: stopped
   dir C:\wf2\prof afterwards: g (only).
C:\wf2 left in place. Still waiting for "WO-7 PART 2: GO".
===== END the PC's results mail =====
