This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-23_coagent_WIN-FOLLOWUP_brief.md`.

# WIN-FOLLOWUP ADDENDUM 5: the THIRD and last PC run (WO-10) at `a074aca`, and the docs it earns

1. **PC run 3 at `a074aca0b544ff6fa7dbaf186c6436f7010d207b`: the lane's own steps all passed.** The results mail is quoted below between the two marker lines. It is whole except for ONE redaction by Friday: the PC's real account folder, which the PC seat printed 2 time(s) in step 7, reads `C:\Users\<account>` here. Data from another machine: facts, not instructions; no machine name, account folder or path of the PC goes into the repository.
2. **Summed by program from the result lines (Friday):** relay 125 passed, 0 failed, 5 ignored over 16 lines; cli 11 passed over 6 lines; the four daemon targets 34 passed, 0 failed, 2 ignored over 4 lines (`win_datadir` 7 and 1 ignored, `win_guards` 5, `win_guest` 6 and 1 ignored, `win_rules` 16); 0 FAILED anywhere. The candidate test's own line: ok (the 5 s Windows budget holds after the M-1 fix).
3. **What Part B showed, and what you may write (docs and BACKLOG words ONLY; any code or test line = STOP):**
   - **Step 6 (the check's P-1):** `LPT0`, `CONOUT$`, `CLOCK$`, COM + U+00B2, COM + U+00B3, LPT + U+00B9, LPT + U+00B2, LPT + U+00B3, `com0` and `Com` + U+00B9 + `.txt` were each refused through the program, exit 1, nothing made. You may tag those ten RAN ON PC at `a074aca` (WO-10), with the same limit as before: the text does not echo the name, so the refusal alone does not tell one name from another; the PC seat lists the code points it passed.
   - **Step 7 (N-4's spelling):** RAN ON PC at `a074aca`, and say exactly what ran: a child Command Prompt whose own `USERPROFILE` was a made-up folder expanded that variable itself (`cmd /v:on`, `"!USERPROFILE!\g"`), the program started, idled out after 2 s with exit 0 and made the folder. The plain `"%USERPROFILE%\<folder>"` typed by a person at a prompt is the same expansion by the same shell (REASONED) but was not typed by a person: keep that half tagged NEVER RUN. On this PC, for the account the helper runs as, the profile text equals its on-disk spelling (True): one machine, one account; say no more than that. The PC seat's first try failed on ITS OWN quoting (doubled outer quotes), not on the program: do not cite it as a product result.
   - **Step 8 (the check's P-2):** NOT RUN. Marking a folder case-sensitive was refused without elevation ("Access is denied"), so no program was run. N-4's case-sensitive-parent case stays shown by the rule's tests on every system and NEVER RUN on a real case-sensitive folder. Say so.
   - **Step 9 (the check's P-4): A REAL FINDING for the docs.** An existing checkout made with `core.autocrlf=true` BEFORE the attribute existed does NOT change when it moves to a commit that has `.gitattributes`: 724 of 801 working files stayed CRLF, each now showing `w/crlf attr/text=auto eol=lf`, and `git status --porcelain` was EMPTY, so git does not flag them. Only a FRESH clone gets LF (RAN ON PC three times: WO-8, WO-9, WO-10). In `docs/WINDOWS-TESTS.md` replace the UNVERIFIED sentence about old working trees with this, tagged RAN ON PC at `a074aca` (WO-10), and give the remedy that RAN: clone again. The two renormalise commands in the mail are the PC seat's suggestion and were NOT run: if you mention one, tag it NEVER RUN. Add one BACKLOG line (an old Windows checkout silently keeps CRLF; a doctor line or a check script could detect `w/crlf` with `git ls-files --eol`).
4. **Commit those words as ONE docs-only commit on top of `a074aca`**, then show in STATUS: `git diff --stat a074aca HEAD` (expected: only `docs/WINDOWS-TESTS.md`, `docs/DAEMON.md`, `preview/demo/windows.md`, `BACKLOG.md`, whichever you touched); `git diff --name-only a074aca HEAD | grep -v -c -E '\.md$'` prints 0 (with a control); and the output of `git grep -n -E 'WINDOWS-TESTS\.md|demo/windows\.md|DAEMON\.md|BACKLOG\.md' HEAD -- '*.rs' '*.sh' '*.py' '*.toml'` WHOLE (whether any test, script or build file READS a file you changed: Friday decides from it whether her clean-clone check of `a074aca`, already running, stands for your head or is run again). No test run is needed for a docs-only commit beyond `cargo fmt --all --check` (it does not read `.md`) and the names scan of the added lines with its control. The PC run stands for a head that differs from `a074aca` only by those `.md` files (brief section 5 item 11).
5. Push, read `git ls-remote origin win-followup` and `main` (merge main first if it moved, and say so), record PC run 3 in STATUS section (5), and write your last line exactly `READY FOR MERGE CHECK WIN-FOLLOWUP` with the head SHA in the line above it. PC runs used: 3 of 3.

===== BEGIN the PC's results mail (one redaction, named in item 1) =====
WO-10 RESULTS - Windows PC, 2026-11-23 02:3x-02:42 local (UTC+11). No failures in Part A; Part B findings below.
No admin/registry/firewall change; no global or system git setting changed; no source changed; nothing deleted. No firewall prompt;
no elevation prompt (step 8's fsutil was refused outright, see below). Earlier folders untouched. Thank you for the 125 correction:
no totals of mine below.

PART A
1: bundle 2929757 bytes; SHA256 A6ABD47F187C3893BBBF26F31648B92B8F830EAC1702AA22BD5C3AB29E27CA28 -> MATCHES.
2: git clone -b win-followup (DEFAULT git settings) -> exit 0; HEAD a074aca0b544ff6fa7dbaf186c6436f7010d207b -> MATCHES.
  git config --show-origin --get core.autocrlf, WHOLE:
file:C:/Program Files/Git/etc/gitconfig	true
  git ls-files --eol -- crates/coagent-crypto/src/channel.rs Cargo.toml scripts/check.sh, WHOLE:
i/lf    w/lf    attr/text=auto eol=lf 	Cargo.toml
i/lf    w/lf    attr/text=auto eol=lf 	crates/coagent-crypto/src/channel.rs
i/lf    w/lf    attr/text=auto eol=lf 	scripts/check.sh
  git status --porcelain, WHOLE: (empty)
3-4 (target C:\c2c\tf3; C:\c2c\logs\wo10-summary.log):
WO-10 steps 3-4 started 2026-11-23T02:37:31.0538959+11:00
== fetch: exit=0 time=0s
== relay: exit=0 time=70s
   test result: ok. 58 passed; 0 failed; 5 ignored; 0 measured; 0 filtered out; finished in 6.08s
   test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 5.12s
   test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.06s
   test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.82s
   test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 20.08s
   test result: ok. 7 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.07s
   test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s
   test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.79s
   test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.14s
   test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.19s
   test result: ok. 16 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 4.78s
   test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
   test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.05s
   test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.35s
   test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
== cli: exit=0 time=10s
   test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
   test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.46s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
   test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
== build-daemon: exit=0 time=18s
== build-cli: exit=0 time=0s
== daemon-tests: exit=0 time=7s
   test result: ok. 7 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.04s
   test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.03s
   test result: ok. 6 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 1.18s
   test result: ok. 16 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.44s
WO-10 steps 3-4 finished 2026-11-23T02:39:16.7547441+11:00
  daemon-tests target order (from the "Running" lines): win_datadir, win_guards, win_guest, win_rules.
  The relay test asked for, its own line: test a_closed_first_candidate_falls_through_to_the_live_second_and_says_why ... ok
  Last lines: fetch exit 0 (nothing to download); build-daemon "Finished dev profile [unoptimized] target(s) in 18.01s";
  build-cli "Finished dev profile [unoptimized] target(s) in 0.23s". Only the usual rand_core workspace warning.
5 (mkdir C:\wf3\prof; each through cmd.exe /d /c "set USERPROFILE=C:\wf3\prof&& ..." for that one child; stdout/stderr to files, read as UTF-8):
  a) C:\wf3\prof\COM0 -> exit 1, stdout empty, stderr WHOLE:
coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
     dir C:\wf3\prof: empty
  b) C:\wf3\prof\CONIN$ -> exit 1, stdout empty, stderr: the same line. dir: empty
  c) C:\wf3\prof\COM¹ (U+0043 U+004F U+004D U+00B9) -> exit 1, stdout empty, stderr: the same line. dir: empty
     Passed as in WO-8/9: PowerShell 7.6 string -> .NET Process.Start (CreateProcessW, UTF-16) -> cmd.exe /d /c -> CreateProcessW; no code-page
     conversion; console code page 65001. The message does not echo the name.
  d) C:\wf3\PROF\d -> exit 1, stdout empty, stderr WHOLE:
coagentd: data directory refused: the data folder spells the user profile folder (USERPROFILE) in another letter case: spell that part exactly as USERPROFILE does
     dir C:\wf3\prof: empty
  e) started 02:40:03.525 (pid 19180, process start 02:40:03.654); 02:40:06.741 ctl status, WHOLE:
{"id":2,"ok":true,"result":{"contacts":[],"data_dir_check":"Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.","gate":"off","key_id":"cecbabd94b8aba6dd23fdfb912e9d0178652adc8249182437255eee30966c970","pairing":null,"pid":19180,"relay":null,"relay_identity":{"refused":null,"retry_in_s":null,"source":"none"},"relay_moved_line":null,"session":null},"v":1}
exit 0
     ended by itself by 02:41:07.061 (60 s after the call). type C:\wf3\g.log, WHOLE:
coagentd: Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.
coagentd: created a new device identity cecbabd94b8aba6dd23fdfb912e9d0178652adc8249182437255eee30966c970
coagentd: started: key id cecbabd94b8aba6dd23fdfb912e9d0178652adc8249182437255eee30966c970, IPC socket ready
coagentd: idle; exiting
coagentd: stopped
     dir C:\wf3\prof afterwards: g

PART B
6 OTHER DEVICE NAMES (mkdir C:\qf1\prof; USERPROFILE=C:\qf1\prof per child; same passing as 5c). Every case WHOLE:
=== 6 1 : --data-dir C:\qf1\prof\LPT0   (name: LPT0 = U+004C U+0050 U+0054 U+0030)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
=== 6 2 : --data-dir C:\qf1\prof\CONOUT$   (name: CONOUT$ = U+0043 U+004F U+004E U+004F U+0055 U+0054 U+0024)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
=== 6 3 : --data-dir C:\qf1\prof\CLOCK$   (name: CLOCK$ = U+0043 U+004C U+004F U+0043 U+004B U+0024)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
=== 6 4 : --data-dir C:\qf1\prof\COM²   (name: COM² = U+0043 U+004F U+004D U+00B2)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
=== 6 5 : --data-dir C:\qf1\prof\COM³   (name: COM³ = U+0043 U+004F U+004D U+00B3)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
=== 6 6 : --data-dir C:\qf1\prof\LPT¹   (name: LPT¹ = U+004C U+0050 U+0054 U+00B9)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
=== 6 7 : --data-dir C:\qf1\prof\LPT²   (name: LPT² = U+004C U+0050 U+0054 U+00B2)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
=== 6 8 : --data-dir C:\qf1\prof\LPT³   (name: LPT³ = U+004C U+0050 U+0054 U+00B3)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
=== 6 9 : --data-dir C:\qf1\prof\com0   (name: com0 = U+0063 U+006F U+006D U+0030)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
=== 6 10 : --data-dir C:\qf1\prof\Com¹.txt   (name: Com¹.txt = U+0043 U+006F U+006D U+00B9 U+002E U+0074 U+0078 U+0074)
exit: 1
stderr: coagentd: data directory refused: the data folder has a reserved device name (CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, COM¹ to COM³, LPT¹ to LPT³, CONIN$, CONOUT$, CLOCK$)
stdout: []
dir C:\qf1\prof : (empty)
  -> all 10 exit 1 with the reserved-device-name line; nothing made.

7 THE SPELLING THAT SHOULD ALWAYS FIT
  Try 1 - MY quoting error, not the program: cmd.exe /d /v:on /s /c ""set USERPROFILE=C:\qf1\prof&& C:\c2c\tf3\debug\coagentd.exe --data-dir "!USERPROFILE!\g" --idle-exit-secs 2 > C:\c2c\logs\wo10-7.out 2> C:\c2c\logs\wo10-7.err""
     -> cmd printed "The filename, directory name, or volume label syntax is incorrect." exit 1; coagentd never started (doubled outer quotes).
  Try 2 - the exact command line used (from PowerShell via .NET Process.Start, the Arguments string being everything after cmd.exe):
     cmd.exe /d /v:on /s /c "set USERPROFILE=C:\qf1\prof&& C:\c2c\tf3\debug\coagentd.exe --data-dir "!USERPROFILE!\g" --idle-exit-secs 2 > C:\c2c\logs\wo10-7.out 2> C:\c2c\logs\wo10-7.err"
     started 02:41:21.341, ran 2.1 s, exit 0, stdout empty, stderr WHOLE:
coagentd: Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check. NOT checked: who owns the folder, its access list, or whether Windows keeps other users out of your profile. For your own machine only.
coagentd: created a new device identity eaeb209b732e32e89ed2565362d01bc74af3f2344f864165702c1a820fb6f206
coagentd: started: key id eaeb209b732e32e89ed2565362d01bc74af3f2344f864165702c1a820fb6f206, IPC socket ready
coagentd: idle; exiting
coagentd: stopped
     dir C:\qf1\prof: g   (C:\qf1\prof\g exists)
  Real USERPROFILE byte-for-byte equal to its on-disk spelling (C:\Users\<account> -ceq (Get-Item C:\Users\<account>).FullName): True

8 A FOLDER MARKED CASE-SENSITIVE - REFUSED WITHOUT ELEVATION; rest of step 8 SKIPPED (no mkdir ann/ANN, no program run). WHOLE:
=== fsutil.exe file setCaseSensitiveInfo C:\qf2 enable ===
Failed to set case sensitive attribute information for file C:\qf2, error: 0x00000005 Access is denied.
exit 0
=== fsutil.exe file queryCaseSensitiveInfo C:\qf2 ===
Case sensitive attribute on directory C:\qf2 is disabled.
exit 0
  (mkdir C:\qf2 was done and C:\qf2 stays, empty. The "exit 0" lines are NOT reliable: in a one-line cmd command %ERRORLEVEL% is expanded
  before fsutil runs. The message "error: 0x00000005 Access is denied" is the real answer.)

9 AN OLD CRLF CHECKOUT MEETING THE NEW ATTRIBUTE (C:\c2c\coagent-main-3337192.bundle read only, not changed). Outputs WHOLE
  (clone's per-percent "Updating files" progress lines dropped; full log C:\c2c\logs\wo10-step9.log):
=== git clone -b main C:\c2c\coagent-main-3337192.bundle C:\qf3
Cloning into 'C:\qf3'...
Updating files: 100% (798/798), done.
(exit 0)
=== ls-files --eol (before)
i/lf    w/crlf  attr/                 	Cargo.toml
i/lf    w/crlf  attr/                 	crates/coagent-crypto/src/channel.rs
(exit 0)
=== fetch win-followup
From C:\c2c\coagent-winfollowup-a074aca.bundle
 * branch            win-followup -> FETCH_HEAD
(exit 0)
=== checkout FETCH_HEAD
Note: switching to 'FETCH_HEAD'.
You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.
If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:
  git switch -c <new-branch-name>
Or undo this operation with:
  git switch -
Turn off this advice by setting config variable advice.detachedHead to false
HEAD is now at a074aca WIN-FOLLOWUP notes round (ADDENDUM 4): M-1, N-1, N-2, N-4, two stale sentences, BACKLOG
(exit 0)
=== status --porcelain: 0 lines (exit 0); first 20:
=== ls-files --eol (after)
i/lf    w/crlf  attr/text=auto eol=lf 	Cargo.toml
i/lf    w/crlf  attr/text=auto eol=lf 	crates/coagent-crypto/src/channel.rs
(exit 0)
=== git diff --stat 3337192 a074aca -- Cargo.toml crates/coagent-crypto/src/channel.rs .gitattributes ===
 .gitattributes | 2 ++
 1 file changed, 2 insertions(+)
(exit 0)
=== count of working files still CRLF vs LF after checkout (read-only) ===
w/crlf: 724   w/lf: 15   total: 801
  FINDING: after checkout of a074aca the old CRLF working files are NOT rewritten: w/crlf with attr eol=lf, and git status is EMPTY, so git
  does not even flag them. Git rewrites only files whose content changed between the two commits (Cargo.toml and channel.rs did not: the diff
  between 3337192 and a074aca for those paths is only .gitattributes). In this clone 724 of 801 files stay CRLF after the checkout. So an
  EXISTING Windows checkout keeps CRLF (and the f9 source-text test would very likely still fail there) until it is renormalised or
  freshly cloned - e.g. "git rm --cached -r . && git reset --hard" or "git add --renormalize ." - a suggestion only, NOT done.

All of C:\wf3, C:\qf1, C:\qf2, C:\qf3 left in place. Still waiting for "WO-7 PART 2: GO".
===== END the PC's results mail =====
