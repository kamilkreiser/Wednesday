VERDICT: GO WITH NOTES — head cf41a77e984b7e8e274ff4cc97136cf9d1987892

## BLUF (for the owner)
1. **The tighter Windows folder rule is sound.** I generated 300,000 folder pairs and wrote 76 hand-made tricks. None got a data folder accepted outside your profile, or with your profile's part spelled differently from `USERPROFILE`. All 33 device names are refused in every letter case (7,360 placements). **What it costs you:** you must type your profile's part exactly as `USERPROFILE` spells it. `c:\users\ann\x` is refused for `C:\Users\Ann`, with words that say how to fix it. The drive letter may be either case. Typing `"%USERPROFILE%\folder"` always works.
2. **Nothing changed on the Mac.** I built the old and the new `coagentd` myself. The `status` reply, the stop logs (SIGTERM and SIGINT), `--help` and a refusal are byte-identical. In `src/` only the Windows rule in `datadir.rs` changed. No protected file, `Cargo` file or `unsafe` changed.
3. **The PC claims are honest.** Every "RAN ON PC" line matches the PC's result files for the commit it names. The relay count is 125, summed from the result lines. The `COM¹` limit is stated. Nothing claims more than the PC showed.
4. **Nothing blocks the merge.** One small test gap is Friday's call: the relay "closed first candidate" test's new 5-second budget no longer notices, on the Mac, a refused connection reported slowly (up to 5 s). The old test caught that; a one-line test change keeps both. There are also three notes: the new text guards can be bypassed on purpose, the two reserved-name lists can drift in the safe direction, and `.gitattributes` would rewrite a future `.bat`/`.cmd` file.

# QA-WIN-FOLLOWUP: independent check of branch `win-followup` (tier 1, full)
Seat QA-WIN-FOLLOWUP; brief `friday/briefs_drafts/2026-11-23_coagent_QA-WIN-FOLLOWUP_check_brief.md` (read whole), with the builder's brief, ADDENDA 1-3, the builder's STATUS (805 lines), the PC files WO-1 to WO-9 + `WINDOWS-FINDINGS.md`, and the W-DAEMON verdict, all read whole. TESTED = I ran it at the head; READ = I read it at the head. Probes, mutants, scripts and logs: `m1_review/gate_win_followup_tests/` (`qa_wf_probe.rs`, `mutants.py` + `spec_*.json` + `mut_*.log`, `mac_compare.sh`, `red_rows.sh`, `wincheck.sh`, `blob_scan.py`, `lists.sh`, `protected.sh`, `names_scan.py`, `logs/`).
Work dir `/private/tmp/claude-501/qwf`: clone `clone`, remote `gh` = the project repo's GitHub URL; worktrees inside the clone (`b` base, `h` head, `p` probe, `ga` attributes, `rp` runner, one `m_<name>` per mutant); a target dir per tree under `t/`; `tools/` with `cargo/bin`, `rustup`, `xwin-kit` as LINKS to the project's, my own registry filled by `cargo fetch --locked`. Windows checks in the kit method (`xwin.sh`: `XWIN_CACHE_DIR` = the folder of `scripts/windows/build.sh:15`, `CARGO_NET_OFFLINE=true`, the kit's `bin` on `PATH`, the tree's `rust-toolchain.toml`, run from the tree with `env -C`). **Kit C step (cargo-xwin): ring's C code is compiled for the target; nothing is linked or run.** Nothing installed; network only `git fetch`, `git ls-remote` and `cargo fetch --locked`.

## 0. Head and base proofs (TESTED)
- `git ls-remote <GitHub URL> win-followup main` (deploy key), at the start and again before this line: `cf41a77e984b7e8e274ff4cc97136cf9d1987892 refs/heads/win-followup`, `33371921670acfcb6fc7634d0c4eacafa9800a8d refs/heads/main`. Both equal the brief.
- `git merge-base gh/main gh/win-followup` = `3337192…`. 7 commits: `ed3462c` (.gitattributes), `17f06ba` (tests first), `ca7867c` (W-1/W-2), `0ac5e8a` (W-3), `97ccf0d` (W-5/W-7, PC run 1), `8f92c41` (docs), `cf41a77` (PC-run-1 tags; PC run 2 at exactly this head).
- The builder's `STATUS_WIN_FOLLOWUP.md` ends `READY FOR QA WIN-FOLLOWUP`, head `cf41a77…` in its Final. ADDENDUM 3 quotes PC run 2 at `cf41a77`; the results file `windows/2026-11-23_WO-9_results.md` equals that quote (only the mail header lines differ). The same holds for WO-8 and ADDENDUM 2.

## 1. The headline promise on macOS (TESTED + READ)
- `git diff --name-only 3337192..cf41a77 -- '*/src/*'` → `crates/coagent-daemon/src/datadir.rs` only. Its diff (sha256 `0db381c8…14df`, equal to the builder's) has 9 hunks, each READ whole and mapped to the builder brief's section 3 items:
  1. the `ReservedName` doc comment (W-1);
  2. its `Display` arm (W-1);
  3. the `WinDirRefusal` enum with the one new variant `ProfileSpelledDifferently` (W-2);
  4. its `Display` arm (W-2);
  5. the `WIN_RESERVED` doc comment and the list, 22 → 33 (W-1);
  6. the `win_reserved_brief_list` red branch in `win_check_part`;
  7. the `win_data_dir_rule` doc comment, steps 3 and 5;
  8. the `win_profile_case_exact` comment;
  9. step 5's two passes and the `win_profile_ascii_fold` red branch.
  There are 18 removed lines, all of them in these items. There is no hunk in the Unix code, the Windows `impl DataDir`, `open_windows` or the tests module, and no added `.set_permissions(`. READ: `win_data_dir_rule` is called only from `open_windows` (`#[cfg(windows)]`).
- **Mac base vs head, my own builds** (`mac_compare.sh`). `coagentd` was built at `3337192` (worktree `b`) and at `cf41a77` (worktree `h`), with own target dirs and the heavy count 0 before each. Each was started in a fresh data folder: one `status`, then a stop by signal.
  - The `status` reply is **BYTE-IDENTICAL** with key id and pid masked: `{"id":7,"ok":true,"result":{"contacts":[],"gate":"off","key_id":"<KEY>","pairing":null,"pid":<PID>,"relay":null,"relay_identity":{"refused":null,"retry_in_s":null,"source":"none"},"relay_moved_line":null,"session":null},"v":1}`, ctl exit 0.
  - The whole stderr is **BYTE-IDENTICAL** for SIGTERM ("created a new device identity" / "started: key id …, IPC socket ready" / "SIGTERM received; stopping" / "stopped", exit 0) and for SIGINT (the same, with "SIGINT received; stopping").
  - Extras, also BYTE-IDENTICAL: `--help` (35 lines) and a Unix refusal (a data folder that is a file: "data directory refused: not a real directory", exit 1).
  - Positive control: one changed byte in the reply, and one in the log, each show DIFFERENT.

## 2. N-4 adversarially (TESTED on this Mac)
- `cargo test --locked -p coagent-daemon --test win_rules` at the head: **16 passed / 0 failed**, `refusal_texts_hold_no_path` included.
- **My probe** `qa_wf_probe.rs` lives in worktree `p` and is never committed. It checks against an **independent model of Windows path resolution**: `\` and `/` alike, doubled separators collapsed, `.` dropped, `..` climbing, trailing dots and spaces stripped, `:` as a stream, my own 33-name device list. **Every ACCEPTED pair must be a plain drive path that resolution does not rewrite, on the same drive, strictly deeper than the profile, with every profile name byte-exact both as written and after resolution.**
  - Seeds `0x5157464650524f42` and `0x0badc0de20261123`, **150,000 pairs each (300,000)**: accepted **24,828 + 24,771, every one safe**. `ProfileSpelledDifferently` was given 6,153 + 6,065 times, each one checked to be an ASCII-case-only difference with no letter difference.
  - **Cost side:** I counted refused pairs that Windows would resolve inside with the profile byte-exact and clean. There were **0**: the rule refuses nothing that is inside and spelled exactly. Pairs inside only under a case fold were refused: 4,368 + 4,300 as `ProfileSpelledDifferently` and 469 + 511 as `OutsideProfile` (the non-ASCII case differences). This is the ruled-in cost.
  - The probe has teeth. Under `COAGENT_RED_WD=win_profile_ascii_fold` and `=win_profile_prefix_by_text` it reports "resolved name … not byte-exact" (for example profile `"C:\Users\Straße"`, data `"C:\Users\STRAßE\x"`). Under `=win_reserved_brief_list` it reports "accepted a pair Windows would rewrite" (`D:/Rı/COM¹/R$`). Under `=win_profile_case_exact` the hand list fails.
- **Hand cases: 76, every one as I expected.** One expectation of mine was wrong at first: `C:\Users\ann＼..＼bob` (fullwidth backslashes) replaces the name `ann` itself, so `OutsideProfile` is right. I corrected it and added `C:\Users\ann\x＼..＼bob` → accepted, one ordinary name inside.
  - Mixed `\` and `/` in profile and data folder: accepted.
  - Trailing and doubled separators on each side: one trailing separator is accepted on either side; doubled (`\\`, `//`, after the drive, inside, at the end) → `Profile(DoubledSeparator)` / `DataDir(DoubledSeparator)`.
  - Non-ASCII case at the first, middle and LAST position: `Élan`/`élan`, Cyrillic `Анна`/`анна`/`АННА`, `Straße`/`STRASSE` (both ways), `Straße`/`STRAẞE` (U+1E9E), `İlker`/`ilker`, `ılker`/`ILKER`, `Ilker`/`ılker`, and a Kelvin-sign `K` → all `OutsideProfile`.
  - `Straße` vs `STRAßE` (only ASCII letters differ) and `Ilker` vs `ilker` → `ProfileSpelledDifferently`.
  - Non-ASCII case BELOW the profile: accepted.
  - A drive-root profile (`C:\`, `C:/`) → `ProfileIsDriveRoot`; `C:` → `Profile(DriveRelative)`.
  - The data folder EQUAL to the profile: `C:\Users\ann`, `…\`, `C:/Users/ann/`, `c:\Users\ann` → `IsTheProfile`. `C:\users\ann` and `C:\Users\ANN\` → `ProfileSpelledDifferently` (names are judged before the count; a refusal either way). `…\\` → doubled.
  - One-name profile `C:\a`: `C:\a\x` and `c:\a\x` accepted; `C:\A\x` → PSD; `C:\ab\x` and `C:\b\a\x` → Outside.
  - 8.3 short names: `PROGRA~1` vs `Program Files` both ways → Outside; `ANNKRE~1` vs `annkre~1` → PSD.
  - Case at a NON-first position: `C:\Users\aNn\x` → PSD. In a deep profile `C:\a\b\c\d\Last`, `…\LAST\x` (the last name) and `…\C\d\Last\x` (a middle name) → PSD.
  - Drive-letter case alone **stays accepted** (`c:\Users\ann\x`; profile `c:\users\ann` with data `C:\users\ann\x`).
  - Case AND letters: `C:\users\bob\x`, `C:\USERS\annx\x`, `C:\Users\ANNA\x`, `C:\USERS\anx\x`, `C:\Userz\ANN\x` → all `OutsideProfile`. **The builder's two-pass order puts any letter difference before a case difference, so a folder that really is outside is never told "spell it like USERPROFILE". That is the safe and accurate order; both outcomes are refusals.**
  - `USERPROFILE=C:\USERS\ANN` with `C:\Users\ann\x` → PSD: only the text counts, not the disk.
- **Refusal texts (TESTED).** Over the 300,000 pairs, each of the 14 refusal categories met had exactly ONE text, and no text holds `\` or `/`. So no text depends on its input, and none echoes a path. The PSD text is the fixed string. Its only overlap with an input is a coincidence: "USERPROFILE" contains the letters `PROF`, as the PC test's made-up `…\PROF\d` does. The text is constant, so this is not an echo.
- **Red controls on their own text (TESTED, as the runner selects them).**
  - `win_profile_case_exact` → `property_i_inside_is_accepted` RED: "seed 0x574441454d4f4e31 case 1: profile "d:/~c0-O$7O\\ж.-ЖAÉB" data folder "D:\\~c0-O$7O/ж.-ЖAÉB/Ax"". The names are byte-identical; **only the drive letter differs**. READ: `exact` is used only for `same_drive` now.
  - `win_profile_ascii_fold` → `examples_a_profile_name_in_another_ascii_case_is_refused` RED: "a profile name in another ASCII case: c:\USERS\Ann\work".
  - `win_profile_ascii_fold` → `property_vi_…` RED: "seed … case 0: profile "G:/_~0n~~ж/Éa" data folder "g:\\_~0n~~ж/ÉA/…"".
  - Each is red on its own text.
- **What the tightening costs a Windows user** (REASONED; the drive fold and the words are TESTED; the shells' behaviour is UNVERIFIED):
  - **Lower-case typing** (`c:\users\ann\x` for `C:\Users\Ann`) is refused at start with exit 1, nothing is made, and the words say "spell that part exactly as USERPROFILE does". The cost is one retype; only the drive letter is forgiven.
  - **Command Prompt tab completion** completes with the on-disk spelling. If `USERPROFILE` spells the profile otherwise (it comes from the profile list, not from the folder), the completed path is refused, and the user must type `USERPROFILE`'s spelling.
  - **A path pasted from Explorer** ("Copy as path" or the address bar) also gives the on-disk spelling, with the same result. A pasted short name (`ANNKRE~1`) is refused for a long-name `USERPROFILE`, and the other way round (`OutsideProfile`).
  - The robust advice is **`--data-dir "%USERPROFILE%\coagent-g"`**: the Command Prompt expands it to `USERPROFILE`'s exact text, so it is accepted. The docs do not give it (Note N-4 below). It holds unless `USERPROFILE` itself ends in `\`, which would give a doubled separator and a refusal; that is UNVERIFIED as ever happening.
  - None of these costs is a safety cost.

## 3. N-1 (TESTED)
- **The 33 names** (my own list, not copied from the product) were each placed in every ASCII case mix the rule folds (2^letters spellings). Each spelling was tried bare, with `.txt`, with `` .txt` `` (a space before the dot) and with two spaces plus `.tar.gz`. Each was placed last, not last, and as a middle name in the data folder, and last and not last in the profile. **All 7,360 placements were refused** (`DataDir(ReservedName)` / `Profile(ReservedName)`). A bare trailing space, with no dot, is refused as `TrailingDotOrSpace`.
- **Near names, all ACCEPTED** (each bare, with `.txt`, and not last): `COM10`, `COM00`, `LPT10`, `CONIN`, `CONOUT`, `CLOCK`, `COM⁴`, `COM₁` (subscript), `COM¹¹`, `COM⁰`, `LPT⁴`, `CONIN$$`, `CON$`, `NUL$`, `CLOCK$$`, `COM¹x`, `xCON`, `CONx`, `COM`, `LPT`, `CONINx$`. Fullwidth `ＣＯＮ`, `ＣＯＭ1` and modifier letters `ᶜᵒⁿ` are also accepted. They are not on any list; whether Windows treats them as devices is UNVERIFIED, and as a last name the walk would still need a directory.
- **Can the two lists drift without a red test?** Mutants, each in its own worktree, against `win_rules`:
  | Mutant | Result |
  |---|---|
  | PRODUCT drops `CLOCK$` | KILLED: `examples_reserved_names_added_after_the_check`, `examples_reserved_names`, `property_v_…` |
  | PRODUCT drops `CON` | KILLED: `examples_reserved_names`, `property_v_…` |
  | PRODUCT drops `LPT³` | KILLED: the same three |
  | TEST list adds `COM10` | KILLED: `property_v_…` ("case 220: … data folder "C:\\Com10.upfv/…"") |
  | TEST list drops `CLOCK$` | **SURVIVES** (16 passed). The product is still pinned by the hand examples; only the generator's copy drifts. |
  | PRODUCT adds `NUL1` (stricter) | **SURVIVES**: nothing pins the list exactly |
  Both survivors are in the safe direction (the product refuses more, or the test's own copy is weaker). Note N-2 below gives a guard.
- **The superscript-one limit is stated wherever PC run 1 or 2 is cited** (READ): `docs/DAEMON.md` 6a step 3, `preview/demo/windows.md` step 3, BACKLOG's N-1 Closed line. `docs/WINDOWS-TESTS.md` does not cite the step-5 refusals at all. The words are as ADDENDUM 2 item 3 asks: "COM followed by U+00B9 … refused … cannot tell `COM¹` from `COM1`".

## 4. N-3, `tests/win_guards.rs` (TESTED)
Mutants of the PRODUCT source, each in its own worktree, against `cargo test --locked -p coagent-daemon --test win_guards`. The kill text is the guard's own (`mut_guards.log`). Every mutant run recompiled the daemon crate (checked in each log).
- **Required, all KILLED:**
  - the reparse test removed from `win_check_dir` ("the first `if` of win_check_dir is `if !md.file_type().is_dir() {`");
  - inverted `!win_is_reparse_point`;
  - commented out in place (`//` on its three lines);
  - the `sync_all` line dropped;
  - `sync_all` moved after the rename ("syncs on line 967 after its rename on line 966");
  - `sync_all` commented out (`//`, and a one-line `/* … */`);
  - `quarantine_bytes`' sync dropped;
  - `cfg!(unix) && ` removed ("the length test is not behind `cfg!(unix) && `").
- **Attacks on the guard's reading:**
  - A `}` inside a string in `write_atomic` (the property kept) → the guard FAILS ("found 0 times"). This is a false alarm, the safe direction.
  - A `{` in a string, in a char literal or in a `/* { */` comment, with the sync dropped → KILLED (the Windows `impl` block no longer closes: "`impl DataDir {` is 0 `#[cfg(windows)]` items").
  - A `}` string inside `win_check_dir` → KILLED ("win_check_dir has no `if`").
  - **These pass the guard while the property is gone:**
    - `a_sync_comment_multiline`: the sync line inside a multi-line `/*` … `*/`.
    - `a_sync_cfg_any`: `#[cfg(any())]` on the line above the sync.
    - `a_sync_if_false`: the sync wrapped in `if false { … }`.
    - `a_decoy_second_item`: a second `#[cfg(windows)] fn win_check_dir` inside a `mod decoy`, while the real one loses its test and its attribute becomes `#[cfg(all(windows))]`.
    - `a_shadow_const`: a local `const WIN_FILE_ATTRIBUTE_REPARSE_POINT: u32 = 0;` inside `win_is_reparse_point`.
    - `a_early_return_check_dir`: `match md.file_type().is_dir() { true => return Ok(()), … }` before the first `if`.
    - `a_length_second_wrapped`: a second length test, not behind `cfg!(unix)`, written over three lines.
    - `a_length_cfg_shadow`: a local `macro_rules! cfg` that makes `cfg!(unix)` true.
  - I then ran **Windows clippy `-D warnings`** on each of those eight, with fresh target dirs. Five pass it as well: the multi-line comment, `cfg(any())`, `if false`, the wrapped second length test and the `cfg` macro shadow. Three are caught there and not by the guard: the decoy ("unneeded sub `cfg`"), the shadow const ("never used", "comparison is always false") and the early return ("use `match` for an equality check"). Positive control: a planted type error inside `win_is_reparse_point` passes the Mac guard tests and fails the Windows clippy with E0308.
  - (My first Windows try reused APFS clones of the head's target dir. Cargo saw them fresh because the cloned outputs were newer than the sources, so those results were wrong and were discarded. Every figure above is from fresh target dirs, each showing "Compiling coagent-daemon" for the mutant's own tree.)
- **Honest refactors that make a guard FAIL while the property holds** (TESTED, each KILLED):
  - rustfmt wrapping `f.sync_all()` / `.map_err(io)?;` over two lines;
  - a helper `win_sync(&f)?`;
  - the binding renamed `file`;
  - `#[cfg(target_os = "windows")]` instead of `#[cfg(windows)]`;
  - `#[cfg(windows)] // comment`;
  - `let sock_len = …; if cfg!(unix) && sock_len > MAX_SOCKET_PATH`;
  - an unrelated `"}"` string in `write_atomic`.
  These are the failures by design; the doc comment says an honest refactor must update the guards.
- **Honest changes that make a guard PASS while the property is gone** (REASONED from the mutants above):
  - a second socket-length test that uses another binding (`path.as_os_str().len() > MAX_SOCKET_PATH`) or a wrapped form;
  - the sync moved under a condition (`if !bytes.is_empty() { f.sync_all()…; }`, the `if false` shape).
  Both are plausible in an honest edit. This is Note N-1.

## 5. `.gitattributes` (TESTED)
- The head holds exactly a `# Why:` comment line and `* text=auto eol=lf`.
- `blob_scan.py` over every entry of `git ls-tree -r cf41a77`: **801 blobs** (754 mode 100644, 44 mode 100755, 3 symbolic links), 59 empty. **0 hold a CR byte; 0 hold a NUL in the first 8,000 bytes.** Positive control: two planted blobs (`a\r\nb\r\n`, `x\0y`) are both found.
- In worktree `ga`: `git add --renormalize .` then `git status --porcelain` lists **nothing**. `git ls-files --eol`: **739 `i/lf w/lf`, 59 `i/none w/none` (empty), 3 `i/ w/` (the links)**, all `attr/text=auto eol=lf`.
- Positive control: a CRLF file added there shows `i/lf w/crlf`, and its index blob is `a\nb\n`. It was removed from the index afterwards and the tree is clean.
- **What the attribute does to future files** (TESTED in `ga`, then removed from the index; demo files in `logs/ga_demo/`):
  - a fixture that must hold CRLF → **rewritten to LF on add** (`i/lf w/crlf`, index blob ≠ file);
  - a `.bat` file → **rewritten to LF on add**;
  - a mostly-printable "binary" with CRLF and no NUL in its first 8,000 bytes → **rewritten**;
  - a random binary (9,000 bytes, no NUL) → kept (`-text`, git's printable-ratio test).
- On checkout, `eol=lf` gives a `.bat`/`.cmd` LF endings on Windows. The PC seat itself wrote its WO-7 helper `.cmd` files "CRLF line ends so cmd's goto/labels work" (`WO-7_part1_results.md`, step 4). A `.ps1` with LF is REASONED fine (UNVERIFIED). **Nothing guards against this today: Note N-3.**

## 6. The relay test edits (TESTED)
- Both diffs READ whole. `abuse::oversize_at_the_real_design_cap`: `.unwrap()` → `let _sent = …await;`, with a comment; the counter assertion is unchanged. `candidates::a_closed_first_candidate_…`: a local `CLOSED_PORT_BUDGET = 5 s` in place of `PER` in this one call; every assertion unchanged. Both test names are unchanged.
- **Relay runner**, `python3 crates/coagent-relay/red-controls/run.py --only M08 M09 M10`, from worktree `rp` at the head with `scripts/env.sh`'s environment, heavy count 0 before it: exit 0, `[RED]` ×3, "sources restored byte-for-byte", "red controls: ALL RED"; `git status --porcelain` empty after.
  - "Caught by" against `OUTPUT.txt:16-20`: M08 the same four tests in the same order; M09 the same two; M10 the same two in another order.
- **Mutants that the OLD test caught**, each run at the base test (`3337192`) and the head test (`cf41a77`), with the same `src/` edit:
  | Mutant | Base test | Head test |
  |---|---|---|
  | the relay closes on an oversize frame without counting the cut (`record_cut` skipped for `Oversize`) | KILLED by both oversize tests ("timed out waiting for: oversize cut") | KILLED, the same |
  | an oversize frame counted as `PeerClosed` instead (`WsError::Capacity(_) => CutReason::PeerClosed`) | KILLED, both | KILLED, both |
  | **the dialer reports a refused connect only after 3 s, as a refusal** (`sleep(3 s)` in the `Err` arm of `TcpStream::connect`) | **KILLED**: "assertion failed: !f.error.timed_out && !f.error.pin_mismatch" | **SURVIVES** `--test candidates` (4 passed), and **SURVIVES the whole `coagent-relay` suite** (`--no-fail-fast`, every line ok) |
- So the old `.unwrap()` was never the only check in the oversize test: the counter catches both oversize mutants on base and head.
- **Can the 5 s budget hide a slow fall-through? Yes, up to just under 5 s per refused candidate, on the Mac.** A refusal slower than 5 s still times out (`timed_out = true`, caught), and the 10 s criterion still holds. The test's stated properties are fall-through, the reason reported, the 10 s criterion and stage `TcpConnect`; all still hold in the mutant. What is lost is the old file's incidental 500 ms sensitivity on the Mac. That sensitivity would flag, for example, a regression that retries a refused connect. This is finding M-1.

## 7. The cli `cfg(unix)` gates (TESTED + READ)
- Diffs READ whole. `#![cfg(unix)]` (with its comment) is the new first line of exactly `identity_cli.rs` and `identity_file.rs`. `support/mod.rs` is byte-equal (protected).
- In `cli.rs`, `#[cfg(unix)]` sits on exactly the three tests (`relay_starts_…_on_sigint`, `sigterm_also_stops_it_cleanly`, `a_non_utf8_argument_is_a_usage_error_not_a_panic`), on `scratch`, `entries`, `struct Relay`, `spawn_relay`, `sigint`, `wait_exit`, and on the imports.
  - My use map confirms each gated helper and each gated import is used **only** by gated items. `Relay`, `Child`, `Fingerprint` and `mpsc` are used through `spawn_relay`/`Relay`; `BufRead`, `Path` and `PathBuf` appear only in gated helpers' signatures and bodies.
  - The one non-`cfg` line is the split `use std::process::{Child, Command, Stdio};` → `use std::process::Command;` + `#[cfg(unix)] use std::process::{Child, Stdio};`. It is needed: `Command` is used by all five portable tests.
  - The Windows `check` and `clippy -D warnings` of `-p coagent-cli --tests` exit 0 at the head. That shows no gated item is used by an ungated test and nothing is left unused on Windows.
- `cargo test --locked -p <crate> -- --list`, base vs head on the Mac (`lists_final.log`; the Running lines reduced to the target name):
  - **coagent-cli IDENTICAL, 60 = 60**;
  - **coagent-relay IDENTICAL, 130 = 130**;
  - **coagent-daemon 254 → 261**, and the only difference is the new target `win_guards` (4 tests) and `win_rules` +3 (`examples_a_profile_name_in_another_ascii_case_is_refused`, `examples_reserved_names_added_after_the_check`, `property_vi_…`), 13 → 16.
  - No test is stopped on the Mac beyond those the brief names (none).

## 8. Counts (READ + targeted)
- From my lists: the workspace difference is +7 tests and +1 test program, all in the daemon. The other crates' trees are byte-equal (item 10), and cli and relay are identical by name. So the builder's **check.sh 1,460 / 0 / 21 over 197 lines** follows from Friday's base 1,453 / 0 / 21 over 196: +7 passed, +1 line, no new ignored test. Likewise **test-daemon 256 + 7 = 263**. These are derived, not re-run; Friday's clean-clone merge check runs them.
- Runner rows, by the brief's pattern `^\s*"COAGENT_RED(_[A-Z0-9]+)?\|`: base **151**, head **154**. **154 is right.** The builder brief's "expected 155" contradicts its own breakdown (1 + 2 = 3 new rows).
- The WD and WF rows, run one by one exactly as the runner selects them (`red_rows.sh`: `COAGENT_RED_WD=<name> cargo test --locked -p coagent-daemon --test win_rules -- --exact <test>`): **8 of 8 RED, each on its own text.**
  - WD-2/sibling: "a sibling that only begins with the profile's name"
  - WD-2/ii: "seed … case 0: profile "e:\\0b.oBp/X-Жxp'" …"
  - WD-2/iii: "… case 2: profile "k:/Ж/ЖЖ/xba\\../PÉN" …"
  - WD-2/env: "unset"
  - WD-2/i: the drive-only case above
  - WF-1: "a reserved name added after the check: C:\Users\ann\COM0"
  - WF-2: "a profile name in another ASCII case: c:\USERS\Ann\work"
  - WF-2/vi: "… profile "G:/_~0n~~ж/Éa" …"
  These are the same texts as the builder's.

## 9. Over-claims (READ)
Every RAN ON PC statement in the diff was checked against the PC files for its commit and work order: `docs/DAEMON.md` 6a steps 3 and 5, `docs/WINDOWS-TESTS.md` §1-5, `preview/demo/windows.md` §1, §3 and §4, BACKLOG's 8 new Closed lines, and the code comments (`win_guards.rs:504`, `abuse.rs`, `candidates.rs`, which cite WO-2/WO-3 facts only).
- §1 LF clone: WO-8/WO-9 step 2; crypto 75 on the default clone (WO-8); the WO-2 failure 1 text and the WO-3 LF figure: match.
- §2 hygiene: libc download failure (WO-3 failure 3); passes after the fetch (WO-8 "three WO-3 failures now PASS"): match.
- §3 per crate: proto 7, policy 24, roster 252 (377/580 s), hook 1, mcp 4 at `1f58dce`, WO-2/WO-3; ipc 26/0/1 at `b8aa8b7`, WO-1 line 32; relay 122 of 125 (WO-3); cli lib+bins 6 (WO-2); cli 11 (WO-8); oversize 6 of 6 (WO-3 "6/6 incl. the full run"); 2,039-2,052 ms (WO-3): match.
  - "the `candidates` program: 4 passed in 2.06 s" pins an unlabelled result line to a program. It is the third relay line, which is where `candidates` comes in cargo's order (lib, abuse 13, candidates 4: the Mac's own order). The pass itself is stated by name in the PC's mail. Supported.
- §4 daemon: 7/1, 6/1, 13 at `600a6a8`, `07a9d13`, `5b008c8` (WO-4..6) and `3337192` (WO-7 part 1); "coagent.exe not built" (WO-7 part-1 stop mail); junction at `07a9d13` (WO-5 part 1, step 4 PASS); Ctrl-C at `5b008c8` (WO-6 part 2, both PASS); 33/0/2 at `97ccf0d` (WO-8): match.
- §5 audit: 259 passed, `qa_fix` 1,970 s, `fix_qam1_seat` 1,291 s, `gate_r4` 1,281 s, not finished in 120 min (WO-3); the recipe is tagged NEVER RUN (UNVERIFIED): **W-8's recipe stays NEVER RUN, as required.**
- windows.md: status form exit 0 with `data_dir_check`, `invite_refused` exit 3, the made-up line "coagent join + 346 × A", `cannot connect (NotFound)` exit 1, and the idle exit after 60 s (WO-7 part 1, steps 5d-5g); the `set /p L=<"%~1"` form (the final WO-7 order, line 29); the four step-5 refusals and the idle exit (WO-8): match.
- **Known points:**
  - The relay count: the docs and BACKLOG use **125** ("the sum of the run's `test result:` lines"). 128 appears nowhere. I summed WO-8 and WO-9 myself: 58+13+4+1+5+7+1+2+4+2+16+4+3+3+2+0 = 125, 5 ignored. This also agrees with the Mac: the relay crate lists 130 tests, 5 of them ignored. "128" in the mails is wrong.
  - The `COM¹` limit is stated (item 3).
  - **Nothing says a kit-built `.exe` was started on Windows** (windows.md §1: "NEVER RUN"; BACKLOG: "by the kit, never started on Windows").
  - **Nothing tags `LPT0`, `CONOUT$`, `CLOCK$` or the superscripts 2 and 3 as refused through the program**: only `COM0`, `CONIN$` and COM + U+00B9 are tagged.
  - Claims citing PC run 2: none in the files. The builder left the tags at `97ccf0d` (ADDENDUM 3 allowed it); run 2 equals run 1 line for line, so they under-claim by not naming it, which is acceptable.
- **No over-claim found.**
- Names scan of `docs/WINDOWS-TESTS.md` and `preview/demo/windows.md` (`names_scan.py --files`, case-insensitive; the patterns are stored base64-encoded): 0 machine names, account folders, network names, addresses, PC work folders or real paths. 3 hits, all the coordinator seat's name in "Friday's WO-n". Positive control: a planted line holding the PC's machine name, an account folder, a volume path and a PC work folder is found.

## 10. Scope (TESTED)
- `git diff --stat 3337192...cf41a77`: 15 files, 1,059 insertions, 109 deletions: `.gitattributes`, `BACKLOG.md`, the three cli test files, `build.rs` (+2 names in `WD_RED` only), `datadir.rs`, `win_guards.rs` (new), `win_rules.rs`, `abuse.rs`, `candidates.rs`, `docs/DAEMON.md` (6a steps 3 and 5 only), `docs/WINDOWS-TESTS.md` (new), `preview/demo/windows.md`, `scripts/red-controls-daemon.sh` (+3 rows and a 2-line comment in the W-DAEMON block). **Every path is on the builder brief's section 3 owned list.**
- `protected.sh` against the builder brief's section 0 item 4:
  - **23 files EQUAL** (`engine.rs`, `main.rs`, `win_datadir.rs`, `win_guest.rs`, `win_support/mod.rs`, `hygiene.rs`, cli `support/mod.rs`, `run.py`, `OUTPUT.txt`, every `Cargo.toml`, `Cargo.lock`, `check.sh`, `env.sh`, `test-daemon.sh`, `test-p1p.sh`, `scripts/windows/build.sh` and `README.md`, `rust-toolchain.toml`, `deny.toml`, `.gitignore`).
  - **14 trees EQUAL.** `crates/coagent-daemon/src` differs, and `git diff --name-status` shows only `M datadir.rs` there, as allowed.
  - Positive control: a planted wrong value prints DIFF.
- The daemon test listing without `win_`: **55 lines, sha256 `6bd8f117…ab7`, EQUAL**. The `win_` part differs only by `A win_guards.rs` and `M win_rules.rs`.
- `git diff 3337192...cf41a77 -- '*Cargo.toml' Cargo.lock`: **0 bytes**. No added line holds `unsafe`.
- `git ls-tree -d -r cf41a77 crates/coagent-daemon/src/` names only `crates`, `crates/coagent-daemon` and `crates/coagent-daemon/src`, so there is no folder under `src/`. Control: `tests/` lists 11 folders.
- **Names scan of every added line** (1,059): 0 real hits. 18 pattern hits: 14 are the coordinator seat's name in "Friday's WO-n", and the rest are made-up profile paths. Every name after a `Users` folder is `ann` (in several cases), `annx` or `bob`. The positive control (planted line) is found.
- My one light run, chosen because these are the two crates whose tests this lane edits: the full `cargo test --locked --no-fail-fast -p coagent-relay -p coagent-cli` at the head, **22 result lines, 185 passed, 0 failed, 5 ignored** (125 relay + 60 cli). Also `cargo fmt --all --check` exit 0, and host `clippy -D warnings` of the edited test targets exit 0.
- Windows type-checks at the head (kit method; **kit C step (cargo-xwin): ring's C code is compiled for the target; nothing is linked or run**):
  - daemon `--lib --bins --test win_rules --test win_datadir --test win_guest --test win_guards`: check 0, clippy `-D warnings` 0;
  - `-p coagent-relay --tests`: check 0, clippy 0;
  - `-p coagent-cli --tests`: check 0, clippy 0;
  - each with only cargo's `rand_core` manifest warning.
  - The base's `-p coagent-cli --tests` check exits 101 (E0433/E0432, `could not compile … (test "cli") due to 2 previous errors`, identity_cli 16, identity_file 16), as the builder recorded.

## Findings (none is a Blocker or a Major)
- **M-1 (Minor; relay test; TESTED). The candidate test's 5 s budget lets through, on macOS, a mutant the old test caught.**
  - Reproduction: in `crates/coagent-relay/src/client.rs`, replace `Err(e) => last = e.to_string(),` (inside `connect_pinned`'s connect loop) with `Err(e) => { tokio::time::sleep(Duration::from_secs(3)).await; last = e.to_string() }`.
    - At `3337192`: `cargo test --locked -p coagent-relay --test candidates` FAILS ("assertion failed: !f.error.timed_out && !f.error.pin_mismatch").
    - At `cf41a77`: it passes, and so does the whole `cargo test --locked --no-fail-fast -p coagent-relay`.
    - Diff: `logs/mutant_r_slow_refusal_3s_head.diff`.
  - Why Minor and not Major: section 3 names "a relay … test edit that lets through on macOS a mutant the old test caught". But this is the **5 s budget the coordinator ruled in** (builder brief 1a, P-9), and its cost is exactly this, so I treat it as I would the ruled tightening of a spelling: report the cost, do not re-rule. The mutant breaks no property the test states (fall-through, reason reported as a refusal, stage `TcpConnect`, under 10 s); it removes the old file's incidental 500 ms sensitivity on the Mac. **If Friday reads section 3 strictly, this is the one item that would make the verdict NO GO.**
  - Suggested fix scope (one line, test only, no PC run needed for the Mac side): `const CLOSED_PORT_BUDGET: Duration = if cfg!(windows) { Duration::from_secs(5) } else { PER };`, or keep 5 s and add `if !cfg!(windows) { assert!(f.elapsed < PER) }`. Either kills the mutant on the Mac and keeps the PC result.
  - NOT TESTED: whether the daemon suite (which dials through `connect_candidates`) would catch it.
- **N-1 (Note; text guards; TESTED).** Eight product mutants remove a guarded property and still pass `win_guards` (item 4). Five also pass Windows clippy:
  - the sync inside a multi-line `/* */`;
  - `#[cfg(any())]` above the sync;
  - `if false { sync }`;
  - a second, wrapped length test outside `cfg!(unix)`;
  - a local `macro_rules! cfg`.
  Two of the shapes are plausible in an honest edit: a second length test with another binding, and the sync moved under a condition. Text guards cannot see control flow, and the doc comment says they are text guards. Suggested guard scope:
  - guard 3: flag every line holding `MAX_SOCKET_PATH` in a comparison (`> MAX_SOCKET_PATH`, `MAX_SOCKET_PATH <`), joined over wrapped lines;
  - guard 2: require the sync line at the body's top-level indentation, with no attribute line above it, and no `/*` inside the guarded items.
- **N-2 (Note; list drift; TESTED).** `WIN_RESERVED` (product) and `RESERVED` (test) can drift in two directions without a red test: the test copy dropping a name, or the product adding one (item 3, both SURVIVE; both are the safe direction). Suggested guard: in `win_guards.rs` (or `win_rules.rs`), parse the `WIN_RESERVED` array out of `include_str!("../src/datadir.rs")` and assert it equals the test's `RESERVED`, names and order.
- **N-3 (Note; `.gitattributes`; TESTED).** `* text=auto eol=lf` silently rewrites to LF, on add, a future CRLF fixture, a `.bat`/`.cmd` (which the PC seat says need CRLF for `goto`/labels) or a mostly-text binary without a NUL in its first 8,000 bytes. Nothing guards this today: 0 such files exist. Suggested scope, when the first such file is added: explicit lines (`*.bat text eol=crlf`, `*.cmd text eol=crlf`, `*.<binary ext> binary`), or a check in `check.sh` that `git ls-files --eol` shows no `w/crlf` on a `text=auto` entry.
- **N-4 (Note; docs; REASONED).** `preview/demo/windows.md` step 3 and docs 6a say to spell the profile part as `USERPROFILE` does. They do not give the spelling that always works in the Command Prompt, `--data-dir "%USERPROFILE%\coagent-g"`. Adding it would remove the tab-completion and Explorer-paste costs of item 2. Docs only.

## The builder's open points, with rulings
- **Two-pass order inside step 5:** RULED correct. A letter difference anywhere gives `OutsideProfile` before any case-only difference gives `ProfileSpelledDifferently`. My probe asserts PSD only when every profile name is an ASCII-case match (12,218 PSD outcomes, 0 counter-cases). Both outcomes are refusals; the order only chooses the more accurate words.
- **The split import line in `cli.rs`** (a non-`cfg` line): RULED acceptable. It is the only way to gate `Child`/`Stdio` while `Command` stays for the five portable tests, and it is equivalent on Unix (identical `--list`, host clippy 0).
- **Two stale under-claims put in BACKLOG instead of fixed** (`datadir.rs` ~483-485 `WinPathFault`'s doc; 6a "Tests."): RULED correct handling. Both lie outside the owned places, and both say LESS than is true. A docs-and-comment-only follow-up can fix them with N-4, with no PC run.
- **Two `.gitattributes` hits outside the brief's list** (`crates/coagent-policy/tests/r2_gate_attacks.rs:374` `".Gitattributes"` and BACKLOG's CRLF entry): RULED harmless. The first is a path string in a policy gate test, READ; the second is the entry W-12 closes. Neither reads this repository's file.
- **Cases added beyond the brief** (more examples, the CRLF guard test, extra mutated copies, the `C:\Users\ann\WORK` example): RULED fine. Each only adds checks; all are green on the Mac and on the PC.
- **154 vs 155 rows:** **154** is right (item 8).
- **125 vs 128 relay:** the docs and BACKLOG use **125**, "summed from the result lines" (item 9). 128 in the PC mails is a summary slip, and the Mac's own list (130 − 5 ignored) agrees with 125.
- **94 socket nodes not carried into quarantine:** I read it as Friday did: accepted, nothing of value lost. A socket node is a name for a listening endpoint of a finished test daemon and holds no data. The move was disclosed, not hidden.
- **STATUS (9)'s UNVERIFIED list:**
  - `COM0`, `LPT0`, `CONIN$`, `CONOUT$`, `CLOCK$` reserved: stays UNVERIFIED (no page read by me); refusing more is the safe direction.
  - The `to_ascii_lowercase` non-ASCII quote: the behaviour is MEASURED by my probe (`com¹` refused; `É`/`é`, `ẞ`, Turkish `İ`/`ı` and the Kelvin sign not folded; fullwidth `ＣＯＮ` not folded).
  - A drive letter cannot be marked case-sensitive: REASONED, stays UNVERIFIED. Its cost is only that the drive keeps its fold, which the tests pin.
  - The attribute outranks `core.autocrlf`: now RAN ON PC twice (WO-8, WO-9).
  - An old CRLF tree keeping its files: UNVERIFIED, stated as such in the docs (PC command below).
  - The audit recipe: NEVER RUN, stated.
  - Single quotes in the Command Prompt, which tool prints a SHA-256, unsigned copied `.exe`, a program in the current folder: UNVERIFIED and stated as such in windows.md.
- **Anything PC run 2 shows that the builder has not answered:** nothing new. Run 2 equals run 1 line for line. The DO-NOT-TOUCH slip is Friday's (ADDENDUM 3 item 2a), and its "relay 128" is the same summary slip.

## NOT TESTED (needs the Windows PC; exact commands)
All in a NEW Command Prompt with made-up folders only, from a clone of `cf41a77` built as in WO-9 (`<t>` = its target folder), `USERPROFILE` for each child only, as WO-8/WO-9 did:
- **P-1, the other device names through the program:** `mkdir C:\qf1\prof`, then for each NAME of `LPT0`, `CONOUT$`, `CLOCK$`, `COM²`, `COM³`, `LPT¹`, `LPT²`, `LPT³`, `com0`, `Com¹.txt`, run `cmd /d /c "set USERPROFILE=C:\qf1\prof&& <t>\debug\coagentd.exe --data-dir C:\qf1\prof\NAME --idle-exit-secs 2"`, then `echo %ERRORLEVEL%` and `dir C:\qf1\prof`. Expected: each exit 1 with the reserved-name line, nothing made. (The text will still not tell the names apart.)
- **P-2, N-4 on a real case-sensitive parent** (the W-DAEMON check's P-2, now expected refused): `mkdir C:\qf2`, `fsutil.exe file setCaseSensitiveInfo C:\qf2 enable` (record whether Administrator is needed; stop if refused), `mkdir C:\qf2\ann`, `mkdir C:\qf2\ANN`, then `cmd /d /c "set USERPROFILE=C:\qf2\ann&& <t>\debug\coagentd.exe --data-dir C:\qf2\ANN\d --idle-exit-secs 2"`, `echo %ERRORLEVEL%`, `dir C:\qf2\ann C:\qf2\ANN`. Expected: exit 1, the "spells the user profile folder … in another letter case" line, nothing made in either folder.
- **P-3, the user cost:** `echo %USERPROFILE%` and `dir /x %USERPROFILE%\..`, to see whether `USERPROFILE`'s spelling equals the on-disk spelling on the owner's own account (read only; record the case, never copy the name into the repository). Then `cmd /d /c "set USERPROFILE=C:\qf1\prof&& <t>\debug\coagentd.exe --data-dir "%USERPROFILE%\g" --idle-exit-secs 2"` with `USERPROFILE` expanded inside the child (`cmd /v:on` with `!USERPROFILE!`). Expected: it starts, idles out after 2 s, and makes `C:\qf1\prof\g`.
- **P-4, an old CRLF tree meeting the attribute:** `git clone -b main <bundle of 3337192> C:\qf3` with the DEFAULT settings (CRLF checkout), then `git -C C:\qf3 fetch <bundle of cf41a77> win-followup && git -C C:\qf3 checkout FETCH_HEAD`, then `git -C C:\qf3 status --porcelain` and `git -C C:\qf3 ls-files --eol -- Cargo.toml crates/coagent-crypto/src/channel.rs`. This shows what the docs tag UNVERIFIED.
- **P-5, a kit-built `coagentd.exe` started on Windows:** NEVER RUN (unchanged; BACKLOG).
- **P-6, the slow-refusal mutant on the PC:** not needed. On Windows the refusal is ~2 s by nature, which is the point of the 5 s budget.

## What was NOT tested (table)
| Item | Why | Who could test it |
|---|---|---|
| `scripts/check.sh`, `scripts/red-controls-daemon.sh` whole, `scripts/test-daemon.sh` whole | the brief forbids them here; Friday's clean-clone merge check runs them | Friday (merge check) |
| The 1,460/197, 154-row RED run and 263 figures as full runs | derived from my `--list` counts, the row count and the 8 WD/WF rows, not re-run whole | Friday (merge check) |
| Whether the daemon suite catches M-1's slow-refusal mutant | heavy, and the suite whole is forbidden here | Friday, or a follow-up lane with M-1's fix |
| The relay runner beyond M08-M10 | only the rows naming the edited tests were asked; the builder ran the full runner | Friday (merge check) |
| P-1 to P-4 above (Windows behaviour through the program, a case-sensitive parent, the user's real spellings, an old CRLF tree) | this Mac cannot reach the PC | Friday via a PC work order |
| A kit-built `.exe` started on Windows | NEVER RUN anywhere | the PC, a later lane |
| Microsoft's page for `COM0`, `LPT0`, `CONIN$`, `CONOUT$`, `CLOCK$` | not read by me; refusing them is the safe direction | any seat, by reading the page that day |
| Whether `cmd.exe` mis-runs an LF-only `.bat`/`.cmd` (N-3's cost) | general knowledge plus the PC seat's own remark, UNVERIFIED | the PC |
| The W-8 audit recipe (`CARGO_PROFILE_DEV_OPT_LEVEL=2`) | NEVER RUN, as the docs say | the PC (optional run) |

## End state
- `git ls-remote` of the GitHub remote just before this line: `win-followup` `cf41a77e984b7e8e274ff4cc97136cf9d1987892`, `main` `33371921670acfcb6fc7634d0c4eacafa9800a8d`. Neither moved during the check.
- Nothing was pushed, merged or edited in the project. In the project repo itself I ran two read commands, `git clone <repo path>` (to make my clone) and `git -C <repo> remote get-url origin`; the second was without `--no-optional-locks` (it takes no lock, but the brief asks for that flag). The only project file written is `coagent/5_Project_History/STATUS_QA_WIN_FOLLOWUP.md`. The builder's worktree and tools root were not touched.
- Every worktree is inside my clone under `/private/tmp/claude-501/qwf`: `b`, `h`, `p`, `ga`, `rp`, `rpb` and the `m_*` mutant trees, about 50 in all. I left them in place, not deleted (about 19 GB with the target dirs), for Friday to quarantine or reuse.
- No process of mine is left running (checked: no `coagentd` and nothing from the work dir).
- **Recorded slips of mine:**
  - Once I used `cd` in a shell command, against the brief, while reading the addenda (read-only). It changed nothing.
  - I removed one superseded log I had just written myself in `gate_win_followup_tests/` (`lists_norm.log`, a comparison with a bad path mask), instead of moving it to quarantine. It was replaced by `lists_final.log`. A folder of mine with the same flaw was moved, not removed, to `lists_raw_unused/`.
  - The discarded first Windows try on cloned target dirs is described in item 4.
