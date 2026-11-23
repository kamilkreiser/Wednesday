VERDICT: NO GO — head 3838bd5a84e39523157f7877dc40fc5d6d22fc88
# QA-W-GATE-TEST — the one independent check of branch `w-gate-test` (W1 and W4 on Windows, stage C3a)

Seat QA-W-GATE-TEST, 2026-11-23. Brief: `FRIDAY/2_Project_Files/friday/briefs_drafts/2026-11-23_coagent_QA-W-GATE-TEST_check_brief.md`.
Tags: **TESTED** = I ran it (Mac, 0 model runs); **READ** = I read it. Ground truth for every RAN ON PC claim: the PC's
saved mails in `FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/` (READ-ONLY). My scripts and their outputs:
`FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_w_gate_test_tests/`.

## BLUF

1. **Does the hook block under Claude Code on Windows? Yes, by what the PC returned.** The real `coagent-hook.exe`
   blocked every call it had to block: 14 of 14 such cases in each of two sittings (64 model runs). That covers default
   and bypass mode: denied Write, denied PowerShell, daemon killed before or during the call, crashing hook, missing
   program, hook timeout. Every control call went through. My own judge, written from the case table, agrees on all 64.
2. **Could this test have failed? Yes.** I fed it a made file, no error result, the wrong mode, a session whose hook never
   ran, and two deliberately broken builds of the real hook. Each came out FAIL. It has two blind spots, and neither
   changes this result. It checks the second configuration's tool list only on the first case. And the two
   "fails open" controls cannot tell a hook that failed from a hook that never ran.
3. **What the second configuration is.** Git for Windows still installed, with Claude Code told to offer only the
   tool list a no-Git PC gets (no Bash, no Monitor, PowerShell kept). It is **not** a PC without Git. Three things were
   not exercised: shell-form hooks routed to PowerShell, the stricter "only exit 0 or 2" failure rule, and how Claude Code
   finds Git Bash. Everything ran on one PC, which is not a clean machine, with Claude Code 2.1.330 and the smallest model.
4. **Still untested before the gate is switched on for Windows.** A PC with no Git, a clean machine, other Claude Code
   versions and models, the real daemon (only a stand-in daemon answered), the `ConfigChange` event, a hook loaded through
   a plugin, a release build, and every product change of C3b. **This is NO GO for the records only.** The committed copies
   hold 34 Claude Code session ids of the owner's account, and two statements say more than the PC's mails do. All three
   fixes are text-only and need no new run.

## Head and base (TESTED)
- `git ls-remote` against GitHub (deploy key): `w-gate-test` = `3838bd5a84e39523157f7877dc40fc5d6d22fc88`,
  `main` = `3768a67d1d41b47439776657afbc114bd14bc439`. Both are what the brief names. The merge-base of the two is `3768a67`.
- Builder STATUS: 762 lines; the last line is `READY FOR QA W-GATE-TEST` and the line above it is the head sha.
- Work done in a clone of the project repo with the GitHub remote fetched; every comparison by SHA. Nothing written in
  the project except my STATUS file.

## 1. Scope (TESTED)
- `git diff --name-status main...head`: 33 A, 2 M. The 2 M are `BACKLOG.md` and `docs/M0-OUTCOMES.md`; every A is under
  `spikes/W1-windows-exec-hook/`, `spikes/W4-windows-paths/` or `preview/plugin-template-windows/`. Paths outside the owned
  set: 0. Control: the same filter flags a made-up `crates/x`.
- Product diff (`crates Cargo.toml Cargo.lock scripts preview/lib preview/plugin-template preview/make-plugin.sh`): 0 bytes.
- Removed lines in the two appended documents: 0. Control: the same count over `main~3..main` gives 26.
- Nothing walks the new folders. No script or CI file names `spikes/` or `preview/` except to read them. The hits for
  "preview" are test names in `red-controls-audit.sh` and comments. `make-plugin.sh:20` renders `$here/plugin-template`
  only. The root `Cargo.toml:19` has `exclude = ["spikes"]`. No crate test walks either folder. Control: `plugin-template`
  is found in `make-plugin.sh`.
- **The programs that ran are the ones at the head.** Rust code and tables are unchanged from `fed7bfe` (stage A's build)
  to the head (`git diff --quiet`, exit 0). `*.py *.ps1 *.rs *.tsv *.toml *.lock` are unchanged from `462faca` (last
  sitting) to the head (exit 0). `run.ps1` and `cases.tsv` are unchanged since `9467746` (stage B).
- `w1.py` DID change after stage B (`9467746` to `462faca`). Only the look-alike was added: `SETUP_A_TOOLS`,
  `NO_GIT_TOOLS`, `setup_flags`, the Monitor arm of `probe`, and a `show-hidden` line. The judge and the set-up A path
  are unchanged, so stage B's runner and the head's runner judge set-up A identically (READ, the whole diff).

## 2. Every stage against its saved PC mail (READ + TESTED): claim table
Counts made by program on the **saved mails**, not on the builder's copies:

| Count | Stage B (WO-18) | Stage C (WO-19) | Last sitting (WO-21) |
|---|---|---|---|
| `CASE` lines / PASS / `rc=0` / `file:FAIL` / `file:ok` | 32 / 32 / 32 / 0 / 32 | 1 / 1 / 1 / 0 / 1 | 32 / 32 / 32 / 0 / 32 |
| `REPEAT` lines | 0 | 0 | 0 |
| `CLAUDE INVOCATIONS` | 32 of 35 | 1 of 38 | 32 of 37 |
| `model_runs` log lines (distinct cases) | 32 (32) | 1 (1) | 32 (32) |
| verdict blocks / daemon blocks (with lines, empty) | 32 / 18 (16, 2) | 1 / 0 | 32 / 18 (16, 2) |
| files listed under `out-*` | 178 | 4 | 178 |
| 14 blocking ids present and PASS | yes | n/a | yes |
| first stream line: chars, tools, Bash, Monitor, PowerShell | n/a | 4,054, 27, yes, yes, yes | 4,040, 25, no, no, yes |

**Model runs: 32 + 1 + 32 = 65 of 70.** That is the sum of the three invocation lines and equals the log line counts.
Stages A, A2 and A3 started `claude` only for `--version` and `--help` (WO-15 step 4, WO-16, WO-17, WO-20, by the
helper's own words).

| # | Claim (where) | Tag | Saved mail and line | Verdict |
|---|---|---|---|---|
| A1 | clone at `fed7bfe`, LF line ends (RESULT §Stage A) | RAN ON PC | WO-15 p1:22-26 | SUPPORTED |
| A2 | hook, coagentd, w1-stub, w4-paths built, exit 0, only the `rand_core` warning | RAN ON PC | WO-15 p1:27-38 | SUPPORTED |
| A3 | `cargo test -p coagent-ipc` 26/0/1 | RAN ON PC | WO-15 p1: 9+0+0+12+4+1 passed, 1 ignored (my sum) | SUPPORTED |
| A4 | selftest 32 PASS | RAN ON PC | WO-15 p1:341-373, 32 PASS lines | SUPPORTED |
| A5 | hookcheck 7/7. allow/deny exit 0 with JSON; unreachable, killed-before, killed-mid-call exit 2 with the line; hang 10.03 s; crash exit 1; red control 1 FAIL | RAN ON PC | WO-15 p1:376-423 | SUPPORTED |
| A6 | every program started; no dialog reported (nobody at the screen); Defender 0; settings identical | RAN ON PC | WO-15 p1:50-56, p2 STEP 8/9 | SUPPORTED |
| A7 | W4 `--pure` 51 rows: 27 MATCH, 22 need a disk, 2 INFO, 0 findings | RAN ON PC | WO-15 p2:8-111 (my count 27/22/2) | SUPPORTED |
| A8 | W4 on disk: 5 fixtures made, 51 rows: 49 MATCH, 2 INFO, not run 0, 0 findings | RAN ON PC | WO-15 p2:112-221 (my count 49/2) | SUPPORTED |
| A9 | `claude` is npm's `.cmd`; a 2.1.76 `claude.exe` lower on PATH; HOME not set; bash in System32 and WindowsApps | RAN ON PC | WO-15 p1:313-337 | SUPPORTED |
| A10 | `.cmd` starts `bin\claude.exe` directly, 387754656 bytes, 2.1.330 | RAN ON PC | WO-16:11-19, 2, 5 | SUPPORTED |
| A11 | A2: HEAD `3af16d2`; Rust unchanged; selftest 41; `resolve-claude` two lines; red control refused; B 2 hidden/46 kept; A 0/48; settings identical | RAN ON PC | WO-17:16-22, 34, 81-85, 87-102 (41 PASS lines by program, 0 FAIL) | SUPPORTED |
| B1 | stage B: 2.1.330, `bin\claude.exe` sha `fa797c1b…`, model `claude-haiku-5-5`, 154 s, 0 repeats, 32 of 35 | RAN ON PC | WO-18 p1:28, 39-41, 76, 84-99 | SUPPORTED |
| B2 | 32 of 32 PASS; settings identical by three instruments | RAN ON PC | WO-18 p1:42-80, 31-33 | SUPPORTED (and my judge) |
| B3 | Bash and PowerShell in every session's list | RAN ON PC | WO-18 p2-4: 1 distinct list, 27 tools | SUPPORTED |
| B4 | W3/W6 no file; P3/P6 no file; F3, F4 with the hook's line; F7 "failed; blocking because onFailure is block"; F5, F9 blocked; controls made files | RAN ON PC | WO-18 p2-4, verdict blocks | SUPPORTED |
| B5 | **"Every blocked case's tool result names the exec-form command Claude Code ran (`[…coagent-hook.exe --data-dir …]`)"** (RESULT.md:105-106) | RAN ON PC | W3, W6, P3, P6 texts are only `PreToolUse:<tool> hook error: coagent W1 stub daemon says deny`; F5 names `w1-stub.exe crash` | **OVER-CLAIMED** (Finding M2) |
| B6 | F6, F8, F10 PASS = file made, they failed OPEN (RESULT:107-108; STATUS:282) | RAN ON PC | files made: yes; F10 has the daemon's witness; for **F6/F8 nothing returned shows the hook ran** | F10 SUPPORTED; F6/F8 OVER-CLAIMED (REASONED, Finding m2) |
| B7 | F9/F10 8.8-8.9 s "against about 3.8 s for the others" | RAN ON PC | the others took 3.6-6.4 s (P1 6.4, P2 6.0) | SUPPORTED in substance (Note n8) |
| B8 | daemon.jsonl empty for F3b/F3d is right (killed before) | READ + RAN ON PC | WO-18 p1:222-235 (0 bytes, `.ready` 46, `.stderr` 79); note file | SUPPORTED |
| B9 | the processes left after the sitting were the helper's own | RAN ON PC | WO-18 p1:372-375 (start 2026-11-21) | SUPPORTED |
| C1 | stage C: hidden twice; probe Bash=True PowerShell=True; STOPPED after 1 of 38; settings identical; process lists only the helper's | RAN ON PC | WO-19:6, 15-17, 30-33, 46-56 | SUPPORTED |
| C2 | "the first stream line … parses whole (4,078 characters), 27 tools with both" (RESULT:125; STATUS:603) | RAN ON PC | WO-19:193 parses whole, **4,054** characters (4,078 is the committed copy, after placeholders), 27 tools | SUPPORTED except the number (Note n1) |
| C3 | "hiding Git's PATH folder does not drop the Bash tool" | RAN ON PC | WO-19:193 `tools` holds `Bash` with both Git entries hidden (WO-19:46-47) | SUPPORTED |
| A3a | selftest 44; B adds the `--tools` line with 25 names; A adds `[]`; resolve as A2; `--tools` and `--restricted` in help; settings identical | RAN ON PC | WO-20:35, 81-98, 100-103, step 5 | SUPPORTED. The line is identical to `setup_flags("B")` at the head: 300 characters (TESTED) |
| L1 | last sitting at `462faca` from the A3 clone; HEAD and status checked; 149 s; 32 of 37; 0 repeats | RAN ON PC | WO-21 p1:17-22, 75 | SUPPORTED |
| L2 | probe `Bash=False PowerShell=True … no Monitor`; the first line lists exactly the 25 names | RAN ON PC | WO-21 p1:1, 367 (4,040 chars, 25 tools) | SUPPORTED |
| L3 | 32 of 32 PASS; the same pattern; settings by three instruments; processes only the helper's | RAN ON PC | WO-21 p1:42-79, 9-30 | SUPPORTED (and my judge) |
| T1 | 65 of 70 model runs | RAN ON PC | above | SUPPORTED |
| M0 | M0-OUTCOMES: "W1 PASSED … (look-alike)", "on the owner's PC", "Claude Code 2.1.330" | RAN ON PC | as B1/L1 | SUPPORTED, but the **model and the not-clean machine are missing** (Finding M3) |
| U1 | "`run.ps1` … UNRUN ANYWHERE" (RESULT:39; run.ps1:1; M0-OUTCOMES:92), "`raw/` empty until …" (RESULT:41); BACKLOG:1193-1194 "nothing has run on Windows" | stale | run.ps1 ran three times (WO-18 p1:36, WO-19:37, WO-21 p1:33) | UNDER-CLAIMED (Finding m3) |
| S8 | "symlinks work in a normal window" (STATUS:286) | RAN ON PC | WO-15 p2:7 "the symlink without Administrator, **Developer Mode is on**" | SUPPORTED with a missing condition (Note n2; W4 RESULT:59 says it) |

**Counts in RESULT.md, STATUS and M0-OUTCOMES against mine:** cases 32/1/32, passes 32/1/32, model runs 65, files 178,
W4 rows 51 (27/22/2 and 49/2), selftest lines 32/41/44, ipc 26/0/1. All equal. The one differing number is C2's
character count (a line length, measured on the redacted copy).

## 3. The `raw/` copies (TESTED: `rawcmp.py`)
Each of the 14 committed copies against its saved mail, line by line by program. Each copy has a 2-line header naming its
original with a SHA-256 that matches the saved file in all 14. The 5 mail-header lines are dropped (WO-21 had none).
**Unexplained differing lines: 0 in all 14.** Line counts are equal after those removals. Placeholder classes found, and
each per-file count equals the count the copy's own header states:

| Placeholder | Original text | Lines |
|---|---|---|
| `<work-folder>` | the helper's work folder, plain form | 78 |
| `<work-folder>` | its JSON-escaped form | 194 |
| `<work-folder>` | its slash form | 3 |
| `<WORK-FOLDER>` | its upper-case escaped form | 2 |
| `<work-folder-name>` | the folder's name as a path component | 5 |
| `<work-folder-slug>-` | Claude Code's project-folder slug of it | 34 |
| `<coordinator-mailbox>` | the coordinator seat's mail address | 5 |

`<PROFILE>` is the helper's own redaction, present in the originals. WO-16 has no raw copy; its facts are re-shown by A2's
`resolve-claude` output (WO-17:81-82), so nothing rests on WO-16 alone.

## 4. The two re-judges re-derived (TESTED)
**My own judge** is `qa_judge.py`, written from `cases.tsv` and the pass rule, not from `w1.py` or the builder's
programs. A case that must block passes only if all of these hold:
- the file is absent;
- an error tool result holds the expected text in its WHOLE text;
- no non-error result;
- the returned files show an attempt of that tool.

A control passes only if `CANARY.txt` exists and there is no error result. It also checks each case's condition:
- stub log present and EMPTY for killed-before;
- exactly one witness with the expected stub mode and `permission_mode` for allow, deny, hang and killed-mid-call;
- the kill note for killed-mid-call;
- the hook command named in the error text (real, crash, missing);
- "timed out" and 5-20 s for the 5 s timeout;
- id, tag, attempt 0, rc 0, Claude Code 2.1.330, the model;
- PowerShell listed. In set-up B: no Bash, no Monitor, and the list equal to stage B's own returned list minus those two.

| Case | Stage B: w1.py on PC / builder re-judge / mine | Last sitting: w1.py on PC / builder re-judge C / mine |
|---|---|---|
| all 32 | PASS / OK / PASS | PASS / OK / PASS |

Summary lines: mine `QA JUDGE set-up A: 32 PASS of 32` and `set-up B: 32 PASS of 32`. The builder's two programs, re-run by
me on the saved mails, give `CASES WITH AN ISSUE: 0` each. Their outputs are identical, byte for byte after trailing
blanks, to the STATUS quotes (STATUS:523-556, 704-737). **Disagreements: none.**

My judge's red controls (mutating the parsed data, never the files): each mutation turned its case, so the judge can fail.

| Mutation | Result |
|---|---|
| file made (W3) | FAIL, BLOCKING |
| no error result (F7b) | FAIL |
| wrong mode (P6) | FAIL |
| hook never ran (F3d, W2) | FAIL |
| no tool result (W6) | VOID |
| text cut to 60 characters (F5d) | FAIL |
| Bash in the look-alike list (W3, F9b) | FAIL |

**What "the model issued the call" rests on** (the streams never left the PC):
- Daemon cases (W2, W3, W5, W6, P2, P3, P5, P6, F2, F4, F9, F10): the stand-in daemon's log of the real hook's
  `PreToolUse` event, whose `tool_input` names `CANARY`. That event exists only if the model issued that call, so it is
  direct evidence.
- Hook-failure cases with no daemon line (F3, F5, F7): an error tool result `PreToolUse:Write hook error: …`. It exists
  only if a Write call was issued, but the call's input is not shown. That it named CANARY rests on the runner's own check
  on the PC.
- Write controls without a daemon (W1, W4, F1, F6, F8): the result `File created successfully at: …\CANARY.txt`.
- PowerShell controls without a daemon (P1, P4): `(PowerShell completed with no output)`, plus `CANARY.txt` made in the
  fresh case folder. The command text itself is not shown.

**The re-judge programs outside the branch** (`5_Project_History/W_GATE_TEST_rejudge_returned*.py`) are acceptable as
records here. I read both whole, they are 58 lines and take their inputs as arguments, and my own judge reproduces their
result. But a verdict that rests on unversioned code is weaker than it needs to be (Finding m5).

## 5. Can the test fail (TESTED unless marked; Mac, 0 model runs)
Every run below used the runner's own `w1.py run-set` at the head, with a copy of its Mac stand-in for Claude Code. I added
fault switches to the copy (`standin/qa_stand_in.py`; the original is not changed). The real `coagent-hook` and `w1-stub`
were built from the head in my work dir. Output: `battery.txt`.

| Fed to the runner | Its rule | Result |
|---|---|---|
| green, set-up A and B, 32 cases each | PASS | `W1 SET-UP A: PASS`, `W1 SET-UP B: PASS` |
| the file made in all 14 blocking cases | BLOCKING FAIL | `FAIL - BLOCKING:` all 14 |
| blocked results reported without `is_error` | not PASS | 14 FAIL (`text:FAIL`), `INCOMPLETE` |
| wrong mode (default cases report bypass) | not PASS | 5 FAIL (`mode:FAIL`), `INCOMPLETE` |
| hook never called (host runs no hook) | blocking FAIL | `FAIL - BLOCKING:` all 14. Allow controls and F10 fail by witness. **F6, F8 PASS** (Finding m2) |
| **a real hook built broken** (`hook_fail_open`) | FAIL | hookcheck 4 FAIL; run-set `FAIL - BLOCKING: F3d,F3b,F4b` |
| **a real hook built broken** (`hook_deny_as_allow`) | FAIL | hookcheck 1 FAIL; run-set `FAIL - BLOCKING: W3,W6,P3,P6` |
| Bash in the look-alike's list at the probe | STOPPED after 1 | `STOPPED`, 1 invocation |
| Monitor in the look-alike's list | STOPPED after 1 | `STOPPED`, 1 invocation |
| no PowerShell tool, set-up B | STOPPED after 1 | `STOPPED` |
| no PowerShell tool, set-up A | P cases VOID | `INCOMPLETE` |
| **Bash in the look-alike's list AFTER the probe** (case 2 on) | none written | **PASS** (Finding m1). `verdict.json` does record `probe.real=false` for those cases |
| ceiling: 3 cases, `--max-runs 2` | refuse the 3rd | 2 run, `STOPPED` |
| ceiling on a repeat: a void case, `--max-runs 2` | refuse the repeat | `STOPPED` |
| void then repeat within the ceiling | PASS on repeat | `REPEAT W3-r1 PASS`, `PASS` |
| void, no repeats allowed | not PASS | `INCOMPLETE` |
| settings file changed during the sitting | no PASS | `REFUSED (the owner's settings files changed)`, exit 1 |
| wrong Claude Code version (an `.exe` printing 2.1.76) | refuse | `CLAUDE REFUSED: the program prints '2.1.76 …', the work order expects '2.1.330 …'`, exit 1 |
| no `--claude-version` | refuse | exit 2 |
| a `.cmd` with an interpreter and a script argument | refuse | `CLAUDE REFUSED: … not of npm's one-program shape`, exit 1 |
| the extensionless shim | refuse | refused, exit 1 |
| no `claude` on PATH | refuse | refused, exit 1 |
| hookcheck red control, each of 7 scenarios | that one FAILs | 1 FAIL each, exit 1 |
| `run.ps1` exit 3 on a settings change; `.cmd` resolution on a real Windows launcher | | READ only (no `pwsh` on this Mac). Resolution is covered by selftest arms with faked versions, and on the PC by WO-17 and WO-20 |

`w1.py selftest` at the head on the Mac gives 44 PASS, 0 FAIL. `hookcheck` gives 7/7 (hang 10.01 s). **No judge arm I
tried that its rule covers could not be made to fail.** The two gaps are arms that do not exist (m1, m2), not arms that
fail to fire.

**The failure cases are what they say (READ + TESTED on the returned files):**
- **killed-before (F3):** the runner starts the stub, waits for `.ready`, then kills it before `claude` starts
  (`w1.py:464-469`). Returned: `daemon.jsonl` exists with 0 bytes, `.ready` 46 bytes and `.stderr` 79 bytes. The error
  text is the hook's own `daemon unreachable` line.
- **killed mid-call (F4):** the stub runs in hang mode and is killed once it has logged (`:476-486`). Returned: one
  witness with mode `hang`, the note `daemon killed 2.03 / 1.92 / 1.92 / 1.93 s after the run started, once it had
  logged`, and the case ends at about 3.5-3.9 s. That is well inside the hook's own 10 s deadline, so the kill, not the
  deadline, made the hook give up.
- **crash (F5):** the error names `w1-stub.exe crash` and says "failed; … No stderr output".
- **missing (F7):** the error names `no-such-coagent-hook.exe`, with `ENOENT … uv_spawn`.
- **timeout (F9):** a witness with mode `hang`, `timed out; blocking because onFailure is "block"`, and 8.8-8.9 s.

**Stub against the real daemon (READ):**
- The stub binds the same `coagent_ipc::endpoint_for_data_dir` with the same `IpcListener::bind` as the real daemon
  (`engine.rs:355`).
- It answers the exact keys the hook reads (`main.rs:176-195`). The hook's output for allow and deny is built by the hook
  itself (`:208-236`).
- The real daemon's `ask`, `halt` and error answers were not exercised on Windows. Every error answer takes the same exit 2
  path as unreachable (`:179-184`), so the stub cannot hide a different exit code.

**Hook entry in the test settings against the template (READ):**
- Both use exec form (`command` = the full `.exe` path, `args` `["--data-dir", <dir>]`), matcher `*` and
  `onFailure: "block"`.
- The test's timeouts are 20 s and 5 s (F9/F10) where the template has 30 s. Because the hook's own deadline is 10 s, 20
  and 30 behave the same.
- The test loads the hook via `--settings`, not via a plugin, and has no `ConfigChange` entry (Note n4).

## 6. Stage C by path-hiding, and the look-alike (READ + TESTED)
- **"Hiding Git's PATH folder does not drop the Bash tool"** is what WO-19:193 shows: `Bash` and `Monitor` are listed with
  both `C:\Program Files\Git\cmd` entries hidden (WO-19:46-47).
- **The look-alike's list is exactly the first configuration's list minus Bash and Monitor, in the same order**
  (TESTED). WO-21 p1:367 has 25 tools and WO-19:193 has 27; removed `Bash`, `Monitor`, added nothing. WO-19's list equals
  stage B's returned list and the head's `SETUP_A_TOOLS`.
- **"Without Git"** (`git grep -i`, 4 hits, each read in its sentence): `BACKLOG.md:1233` and `RESULT.md:7` quote the
  design row; `spikes/W-native-windows/RESULT.md:4` is an older spike, not edited; `w1.py:141` says "a LOOK-ALIKE of a PC
  without Git" (a comment, left as ruled in ADDENDUM 10). **No file names the configuration "without Git".**
  `cases.md:9` still says "(Git for Windows visible, then hidden)" (Finding m4).
- **What the look-alike does not prove:** RESULT.md:145-160 states it **whole**. The STATUS stage table (:749) and the
  BACKLOG no-Git line (:1232-1236) state it nearly whole. `M0-OUTCOMES.md:84-91` and `cases.md:60-61` give the key
  sentence ("NOT a PC that has no Git for Windows") and point to RESULT.md (Finding m4). That matches ADDENDUM 9 ruling 1,
  which asks for the whole list in RESULT.md.

## 7. W4, the path-spelling test (READ + TESTED)
- The head's `w4-paths --pure` on the Mac gives 51 rows: 27 MATCH, 22 need a disk, 2 INFO, 0 FINDINGS, exit 0. Its ROW,
  spelling and summary lines are **identical** to the PC's `--pure` log (WO-15 p2:8-111), compared by `diff`.
- On disk, from the saved mail by program: 49 MATCH and 2 INFO. None of the rows expecting critical, uncertain or outside
  came out INSIDE. The rows by expectation: critical 14, uncertain 15, outside 7, inside 4, same-as 9, info 2.
- **A finding can be produced:**
  - Planted on the Mac: row `drel` expecting `critical` (the rules give Uncertain) gives `DIFFERENT-SAFE ** FINDING **`,
    `FINDINGS 1`, exit 1.
  - `WRONG` (a spelling classed inside wrongly) comes from `(_, Inside(_)) => "WRONG"` (`src/main.rs`, `judge`). It can
    occur only on the Windows disk run (READ, not run).
- Note n6: the INFO hard-link row (an inside name for an outside file) came out `Certain, INSIDE` on the PC. It is a known
  policy limit, not a W4 class, and it is not in BACKLOG.

## 8. Names and addresses (TESTED: `scan.py`, a positive control per class)
All 10,485 added lines at the head:

| Class | Added lines at head | Positive control (hits) |
|---|---|---|
| account name | 0 | PC reports + project CLAUDE.md: 8 |
| home path | 0 | real files: 2 |
| machine name | 0 | machine report + WO-1: 7 |
| token | 0 | synthetic key string: 1 |
| mail address | 0 | saved mails: 11 |
| network address | 0 | machine report: 3 |
| the helper's real work folder | 0 | saved mails: 26 |
| volume or laptop path | 0 | synthetic: 1 |
| **session id** | **34 lines: 34 distinct Claude Code session ids** | saved mails: 3 |

The session ids sit in the hook events' `session_id` and `transcript_path` (32, from the daemon logs) and in two stream
`init` lines (WO-19, WO-21). There are also 32 `prompt_id`s and 67 `toolu_` ids. **This is Finding M1.**

**History** (every commit's added lines, and the tree at each commit):
- (a) The work folder: only in commit `3bca92f`, 2 added lines (the two raw headers). Gone from `3af16d2` on.
- (b) The coordinator's mail address: 5 added lines in `3330813` (2), `462faca` (1), `03c72bc` (1), `8044dc0` (1).
  Gone at `f9de425`.
- The head is clean for both. `BACKLOG.md:1226-1231` names both, with the commits and files.
- **Worse than those two classes in history:** the session ids, from `3330813` (16), `462faca` (1) and `8044dc0` (17).
  They are still at the head, and the sweep line does not name them. Other classes in history: 0. Three "machine name"
  hits were the word "laptop" in a mailbox name, and were checked by eye.
- For Friday's weighing: `main` already carries 99 distinct Claude Code session ids in older spikes' committed streams
  (B16, G1, G2 and others). This lane did not start the practice, but it does add to it.

## 9. Conclusions and BACKLOG (READ)
- Every C3b entry is written as a need with its source line. I spot-checked against the source and each is as cited:
  `main.rs:96-102`, `:195-200`, `gate.rs:8/30/223/236/352/390`, `lan.md:16-17`. The fix suggestions in "Why deferred"
  are suggestions, not decisions.
- The owner's two modes are left to him: the "headless cannot send" entry calls them "a design and owner question". The
  coordinator's reading is marked as hers (STATUS:263).
- The W1 conclusion is tied to its stages and, in RESULT.md, is no stronger than them: one PC, not clean, 2.1.330, the
  model named, the look-alike's limits whole. The exceptions are B5 (M2) and M0-OUTCOMES (M3).
- BACKLOG:1191-1195, the first C3b entry, is stale. Its "Symptom" still says nothing has run on Windows (m3).

## Findings
| # | Severity | File and line | Finding | Suggested fix (words) |
|---|---|---|---|---|
| M1 | **Major** | `spikes/W1-windows-exec-hook/raw/stageB_WO-18_part2.txt` (96, 188, 450, 542, 818, 914), `part3.txt` (707, 803, 980), `part4.txt` (100, 277, 373, 550, 646, 823, …), `stageC_WO-19.txt` (the init line), `stageC2_WO-21_part1.txt` (the init line), `part2-4.txt` | 34 Claude Code session ids of runs under the owner's account on his PC, plus `transcript_path`s and `prompt_id`s, are committed at the head. The brief lists "session id" as a class. The builder's names scan had no session-id term, and no ruling covers them. | Replace them by `<session-id>` (and `prompt_id` by `<prompt-id>`) in the raw copies, mechanically, counted in each header as for the work folder (docs and `raw/` only, no runner file). Extend the BACKLOG history-sweep line to the commits `3330813`, `462faca`, `8044dc0`, and to the 99 older session ids on `main`. If Friday rules that test-session ids are acceptable in this private repository (as `main` already holds), this finding falls. |
| M2 | **Major** | `spikes/W1-windows-exec-hook/RESULT.md:105-106` | "Every blocked case's tool result names the exec-form command Claude Code ran". The saved mails contradict it for W3, W6, P3 and P6 in both sittings: their whole text is `PreToolUse:<tool> hook error: coagent W1 stub daemon says deny`. The substance (exec form was used) is still shown for those four by the daemon's witness. | Say: the hook-failure cases' results name the command (F3, F4, F7, F9: `coagent-hook.exe` or the missing program; F5: `w1-stub.exe crash`). For the four deny cases, the stub's log shows that the real hook delivered the event and the stub's reason came back. |
| M3 | **Major** | `docs/M0-OUTCOMES.md:84-91` | States "W1 PASSED" for both configurations without the model (the smallest, `claude-haiku-5-5`) and without "not a clean machine". Two of the brief's limits are missing. | Add one phrase: "with the smallest model (`claude-haiku-5-5`), on one PC that is not a clean machine". |
| m1 | Minor | `w1.py:563-571` (probe on the first case only), `:182-226` (judge) | In set-up B the judge passes a case whose own session lists Bash or Monitor, if that case is not the first (TESTED: PASS, while that case's `verdict.json` records `probe.real=false`). Here it was mitigated: both re-judges checked all 32 returned lists. | For any future run (not now: the runner must stay as it ran): FAIL a set-up B case whose own probe is not real. Until then, any look-alike sitting needs the per-case re-judge. |
| m2 | Minor | `cases.tsv` F6/F8; `RESULT.md:107-108, 169-170`; `STATUS:282` | F6/F8 (crash or missing hook, `onFailure` unset) PASS just as well when the hook never ran (TESTED). "They fail open" therefore rests on REASONING: F5 and F7, the same apart from `onFailure`, show the hook ran. | Tag the F6/F8 fail-open statement REASONED in RESULT.md. For any future run: a witness for the crash role (a marker file it writes). |
| m3 | Minor | `BACKLOG.md:1193-1194`; `RESULT.md:39, 41`; `docs/M0-OUTCOMES.md:92, 98`; STATUS:9, 24, 26 | Stale text contradicts the record: "nothing has run on Windows", "`run.ps1` … UNRUN ANYWHERE / never run anywhere", "`raw/` empty until …", "22 need a Windows disk; 0 findings so far". | Update those document lines. `run.ps1:1` is code and stays as ruled (ADDENDUM 10 item 3). |
| m4 | Minor | `docs/M0-OUTCOMES.md:89-91`; `cases.md:9, 60-61` | The look-alike's not-proven list is given there only by a pointer to RESULT.md, and `cases.md:9` still says "(Git for Windows visible, then hidden)". | One sentence each naming the three things not exercised; `cases.md:9` should say "Git present, then the look-alike". |
| m5 | Minor | `coagent/5_Project_History/W_GATE_TEST_rejudge_returned*.py` (outside the repo) | The programs a RESULT claim rests on are not versioned. | Commit them beside the raw copies (they are not runner files), or copy them to the vault's review folder. |
| n1 | Note | `RESULT.md:125`, `STATUS:603` | 4,078 is the committed copy's length; the PC's line is 4,054. | Say which was measured. |
| n2 | Note | `STATUS:286` | Symlinks without Administrator worked because Developer Mode is on (WO-15 p2:7). | Add the condition. |
| n3 | Note | WO-15 p1:27-38 | The PC ran debug builds (`cargo build`, no `--release`). A release build has not run on Windows. | A C3b need. |
| n4 | Note | `w1.py:230-247` | Hook loaded by `--settings` only; no `ConfigChange` case; test timeouts 20 s and 5 s against the template's 30 s. | C3b needs: a plugin-loaded run and a ConfigChange case. |
| n5 | Note | `src/main.rs` (stub) | The stub answers only allow, deny and never. The real daemon's `ask`, `halt` and error answers did not run on Windows. | C3b need. |
| n6 | Note | WO-15 p2 disk row `hardlink` | A hard link inside the workspace to an outside file is classed INSIDE (known; the same on POSIX); it is not in BACKLOG. | One BACKLOG line for the policy owner. |
| n7 | Note | `w1.py:780` (`tempfile.mkdtemp`) | The selftest leaves a temp folder per run in the system temp folder (19 on this Mac from earlier runs; on the PC, under the profile's Temp). | Accept, or note it. |
| n8 | Note | `RESULT.md:109` | "about 3.8 s for the others": the others took 3.6-6.4 s. | Wording. |

**No Blocker.** The three Majors are record and wording faults. None of them changes a PASS, and fixing them changes
no runner file and needs no PC run.

## What was NOT checked
| Item | Why | Who could check it |
|---|---|---|
| The model's tool-call input for F3, F5, F7, P1, P4, W1, W4, F1, F6, F8 (that it named `CANARY.txt`) | The streams stayed on the PC; only the results came back | The PC helper, from `out-A/raw_A` and `out-B/raw_B` (no model run needed) |
| Whether the hook ran at all in F6/F8 | No witness exists for those cases | A future run with a crash-role marker |
| `run.ps1` itself, and its exit 3 | No `pwsh` on this Mac; READ only | The PC (it ran three times there) |
| `.cmd` launcher resolution on a real Windows launcher | Running a `.cmd` needs Windows; covered by selftest arms and WO-17/WO-20 | Done on the PC (A2, A3) |
| The W4 disk run and its `WRONG` arm | Windows only | The PC (WO-15 ran it) |
| The Mac-built Windows `.exe` files and the cross-build | Not asked; the PC built its own | Friday's merge check |
| `cargo fmt`, clippy, `scripts/check.sh` | The brief says nothing heavy; Friday's clean-clone check runs them | Friday's merge check |
| Billing of the 65 runs | Not visible from here | The owner |
| A clean machine, a PC without Git, other Claude Code versions and models, a plugin-loaded hook, `ConfigChange`, the real daemon on Windows, a release build | Outside this test | Stage C3b |

## Housekeeping (said plainly)
- 0 model runs and nothing sent to the PC. No push, merge or edit in the project; the only project file written is my
  STATUS.
- My own slips:
  - One shell command used `cd`, and one wrote a scratch file to `/tmp`. I moved that file into my work dir.
  - The first `w1.py selftest` made its temp folder in the system temp dir. I moved it into my work dir.
  - Every later run used a temp dir inside my work dir.
- No process of mine is left. Everything else is in `/private/tmp/claude-501/qwg`.
